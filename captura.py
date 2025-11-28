import psutil as p
from mysql.connector import Error
import dotenv as d
from time import sleep, time
from mysql_connect import conectar_server
from numpy import mean
from getmac import get_mac_address as gma
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from os import getenv
import platform
d.load_dotenv()


def identificar_macaddres(db):
    try:
        macAddress = gma()

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT idMaquina 
                FROM maquina 
                WHERE macAddress = %s
            """, (macAddress,))
            exists = cursor.fetchone()

            # registro novo
            if exists is None:
                cursor.execute("""
                    INSERT INTO maquina (fkEmpresa, fkSistema, macAddress, localizacao)
                    VALUES (1, 1, %s, 'Desconhecida')
                """, (macAddress,))
                db.commit()

                cursor.execute("""
                    SELECT idMaquina FROM maquina WHERE macAddress = %s
                """, (macAddress,))
                exists = cursor.fetchone()

        print(f"Mac Address identificado: {macAddress}")
        return macAddress, exists[0]

    except Error as e:
        print("Erro ao identificar máquina:", e)
        return None, None



def inserir_pids(db, idMaquina):
    try:
        with db.cursor() as cursor:
            for process in p.process_iter(["pid", "name", "username"]):
                try:
                    cpu = process.cpu_percent(None)
                    memory = process.memory_info().rss / 1024 / 1024
                    io = process.io_counters()
                    io_read = io[0]
                    io_write = io[1]
                except:
                    continue  # processo morreu no meio

                cursor.execute("""
                    SELECT idProcesso
                    FROM processo
                    WHERE fkMaquina = %s AND pid = %s
                """, (idMaquina, process.info["pid"]))
                exists = cursor.fetchone()

                # UPDATE
                if exists:
                    cursor.execute("""
                        UPDATE processo
                        SET usoCpu = %s, usoRam = %s, discoLido = %s, discoRecebido = %s
                        WHERE idProcesso = %s
                    """, (cpu, memory, io_read, io_write, exists[0]))

                # INSERT
                else:
                    cursor.execute("""
                        INSERT INTO processo
                        (fkMaquina, pid, nome, usuario, usoCpu, usoRam, discoLido, discoRecebido)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        idMaquina,
                        process.info["pid"],
                        process.info["name"],
                        process.info["username"],
                        cpu, memory,
                        io_read, io_write
                    ))

                db.commit()

    except Error as e:
        print("Erro ao lidar com processos:", e)



def identifica_fk(db, modelo, idMaquina):
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT idComponente, fkMetrica 
                FROM componente 
                WHERE modelo LIKE %s
            """, (f"%{modelo}%",))

            retorno = cursor.fetchall()

        comps = [c[0] for c in retorno]
        mets = [c[1] for c in retorno]

        return {
            "idMaquina": idMaquina,
            "idComponente": comps,
            "idMetrica": mets
        }

    except Error as e:
        print("Erro ao buscar FKs:", e)
        return None



def acessar_metricas(db, porc, idMetrica):
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT min, max 
                FROM metricaComponente 
                WHERE idMetrica = %s
            """, (idMetrica,))
            r = cursor.fetchone()
            return {"porcentagem": porc, "intervalo": r}

    except:
        return None


def insert_alerta(db, porc, idMetrica, intervalo):
    try:
        descricao = "Uso saudável"
        estado = None

        if mean(porc) > intervalo[0] and mean(porc) < intervalo[1]:
            descricao = "Seu componente está ficando estressado."
            estado = "Preocupante"

        elif mean(porc) >= intervalo[1]:
            descricao = "Seu componente está crítico!"
            estado = "Crítico"

        if estado is None:
            return None  # sem alerta

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO alertaComponente (fkMetrica, estado)
                VALUES (%s, %s)
            """, (idMetrica, estado))


            db.commit()
            return {"alerta_id": cursor.lastrowid,
                    "descricao": descricao}

    except:
        return None



def inserir_porcentagem(db, porc, fk):
    try:
        if not isinstance(porc, list):
            porc = [porc]  # disco / ram

        with db.cursor() as cursor:

            qtd = min(len(fk["idComponente"]), len(porc))

            for i in range(qtd):
                idComp = fk["idComponente"][i]
                idMet = fk["idMetrica"][i]

                metricas = acessar_metricas(db, porc[i], idMet)
                alerta = insert_alerta(db, porc, idMet, metricas["intervalo"])
                print(alerta)

                cursor.execute("""
                    INSERT INTO logMonitoramento 
                    (fkComponente, fkMaquina, fkAlerta, fkMetrica, valor, descricao)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    idComp,
                    fk["idMaquina"],
                    alerta["alerta_id"] if alerta else None,
                    idMet,
                    porc[i],
                    alerta["descricao"] if alerta else None
                ))

                db.commit()

                if alerta is not None:
                    enviar_slack(db, fk["idMaquina"], idMet, cursor.lastrowid)

    except Error as e:
        print("Erro ao inserir porcentagem:", e)

def get_uptime_seconds():
    so = platform.system().lower()

    if so in ("windows", "linux", "darwin"):
        return int(time() - p.boot_time())

    return int(time() - p.boot_time())

def atualizar_uptime(db, idMaquina, uptime):
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE maquina SET uptime = %s WHERE idMaquina = %s
            """, (uptime, idMaquina))
            db.commit()

    except Error as e:
        print("Erro ao atualizar uptime:", e)

def enviar_slack(db, idMaquina, idMetrica, idLog):
    try:
        retorno = None
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    m.macAddress,
                    c.tipo AS componente,
                    lm.dtHora,
                    lm.valor,
                    lm.descricao AS descricaoLog,
                    ac.estado
                FROM logMonitoramento lm
                JOIN maquina m ON lm.fkMaquina = m.idMaquina
                JOIN componente c ON lm.fkComponente = c.idComponente
                JOIN alertaComponente ac ON lm.fkAlerta = ac.idAlerta
                WHERE lm.fkMaquina   = %s
                AND   lm.fkMetrica   = %s
                AND   lm.idMonitoramento = %s
            """, (idMaquina, idMetrica, idLog))

            retorno = cursor.fetchone()

    except Error as e:
        print("Erro ao buscar FKs:", e)
        return None

    if not retorno:
        print("Nenhum dado encontrado para enviar ao Slack.")
        return

    mac, componente, dtHora, valor, desc, estado = retorno

    # Define cor baseada no estado
    cores = {
        "Crítico": "#FF0000",
        "Preocupante": "#FFA500",
        "OK": "#36A64F"
    }

    cor_alerta = cores.get(estado, "#AAAAAA")

    client = WebClient(getenv("SLACK_BOT"))

    try:
        resposta = client.chat_postMessage(
            channel="#alertas-componente",
            text=f"⚠️ *Alerta de {componente} detectado!*",
            blocks=[
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": f"🚨 Alerta ({estado})", "emoji": True}
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"*📍 Máquina:* `{mac}`\n"
                            f"*🧩 Componente:* {componente}\n"
                            f"*📅 Data:* {dtHora}\n"
                            f"*📊 Valor:* *{valor}%*\n"
                            f"*📝 Descrição:* {desc}\n"
                        )
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"🔴 *Nível:* `{estado}`"
                        }
                    ]
                }
            ]
        )

        print("Mensagem enviada:", resposta["ts"])

    except SlackApiError as e:
        print("Erro Slack: ", e.response["error"])



db = conectar_server()

macAddress, idMaquina = identificar_macaddres(db)

fkCpu = identifica_fk(db, "Ryzen 5 5600X", idMaquina)
fkRam = identifica_fk(db, "Vengeance LPX", idMaquina)
fkDisc = identifica_fk(db, "978 EVO Plus", idMaquina)

while True:
    ram_porc = p.virtual_memory().percent
    disk_porc = p.disk_usage("/").percent
    cpu_porc = p.cpu_percent(interval=1, percpu=True)

    uptime_segundos = get_uptime_seconds()

    if db:
        inserir_porcentagem(db, cpu_porc, fkCpu)
        inserir_porcentagem(db, ram_porc, fkRam)
        inserir_porcentagem(db, disk_porc, fkDisc)

        inserir_pids(db, idMaquina)

        atualizar_uptime(db, idMaquina, uptime_segundos)

    sleep(2)
