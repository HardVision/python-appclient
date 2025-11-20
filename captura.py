import psutil as p
from mysql.connector import Error
import dotenv as d
from time import sleep
from mysql_connect import conectar_server
from numpy import mean
from getmac import get_mac_address as gma

d.load_dotenv()

def identificar_macaddres(db):
    try:
        macAddres = gma()
        with db.cursor() as cursor:
            # Busca id da máquina
            cursor.execute("SELECT * FROM maquina WHERE macAddress = %s", (macAddres,))
            exists = cursor.fetchone()
            if exists is None:
                 cursor.execute("INSERT INTO maquina (fkEmpresa, fkSistema, macAddress, localizacao) VALUES (1, 1, %s, 'Desconhecida')", (macAddres, ))
                 db.commit()

        print(f"Mac Address: {macAddres}")

        return macAddres

    except Error as e:
        print('Error ao selecionar no MySQL -', e, "- identificar_macaddress")
        return f"Mac Address: {None}"

def identifica_fk(db, modelo, macAdress):
    try:
        with db.cursor() as cursor:
            # Busca id da máquina
            cursor.execute("SELECT idMaquina FROM maquina WHERE macAddress = %s", (macAdress,))
            idMaquina = cursor.fetchone()

            cursor.execute("SELECT idComponente FROM componente WHERE modelo LIKE %s", (f"%{modelo}%",))
            idComponente = cursor.fetchall()

            cursor.execute("SELECT fkMetrica FROM componente WHERE modelo LIKE %s", (f"%{modelo}%",))
            idMetrica = cursor.fetchall()

        print(f"Maquina: {idMaquina} Componente: {idComponente} Metrica: {idMetrica}")

        return {
            "idMaquina": idMaquina,
            "idComponente": idComponente,
            "idMetrica": idMetrica
        }

    except Error as e:
        print('Error ao selecionar no MySQL -', e, "- identifica-fk")
        return {"idMaquina": None, "idComponente": None, "idMetrica": None}

def acessar_metricas(porc, idMetrica):
    print(f"Valor a ser verificado: {porc}\nID da métrica: {idMetrica}")
    try: 
        with db.cursor() as cursor:
            slctInterval = "select min, max from metricaComponente where idMetrica = %s"
            cursor.execute(slctInterval, (idMetrica[0], ))
            returnQuery = cursor.fetchone()
            print(f"Min: {returnQuery[0]}\nMax: {returnQuery[1]}")

            return {"porcentagem": porc, 
            "id_metrica": idMetrica, 
            "metricas": returnQuery}

    except Error as e:  
          print('Erro ao selecionar metricas MySQL -', e)

def insert_alerta(porc, idMetrica, returnQuery):
    print("Return query:", returnQuery)
    try:
        descricao = ""
        estado = ""
        exists_alerta = False
        if mean(porc) > returnQuery[0] and mean(porc) < returnQuery[1]:
            descricao = "Seu componente está ficando estressado. Verifique sua máquina!"

            estado = "Preocupante"
            exists_alerta = True
        elif mean(porc) > returnQuery[1]:
            descricao = "Seu componente está utilizando muitos recursos. Verifique-o!"

            estado = "Crítico"
            exists_alerta = True
        else:
            descricao = "O uso do seu componente é saudável"
    
        if exists_alerta is False:
            return {"descricao": descricao, "id_alerta": None}
        else:
            with db.cursor() as cursor:
                insert = "insert into alertaComponente (fkMetrica, estado) values(%s, %s)"
                values = (idMetrica[0], estado)
                cursor.execute(insert, values)
                # db.commit()
                id_alerta = cursor.lastrowid
                print(cursor.rowcount, "registro inserido na tabela AlertaComponente")
                return {"descricao": descricao, "id_alerta":  id_alerta}

    except Error as e:  
        print('Erro ao inserir alertas no MySQL -', e)


def inserir_porcentagem(porc, db, idMaquina, idComponente, idMetrica):
    if not isinstance(porc, list):
        porc = [porc]

    if isinstance(idMaquina, tuple):
        idMaquina = idMaquina[0]
    
    idComponente = [c[0] for c in idComponente]
    idMetrica = [m[0] for m in idMetrica]

    print("Fks normalizadas:", idMaquina, idComponente, idMetrica)
    print("Valores a serem adicionados:", porc)

    try:
        with db.cursor() as cursor:
            qtd = min(len(idComponente), len(porc))

            for i in range(qtd):
                metricas = acessar_metricas(porc[i], [idMetrica[i]])
                alerta = insert_alerta(
                    metricas["porcentagem"],
                    metricas["id_metrica"],
                    metricas["metricas"]
                )

                query = """
                    INSERT INTO logMonitoramento 
                    (fkComponente, fkMaquina, fkAlerta, fkMetrica, valor, descricao)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                values = (
                    idComponente[i],
                    idMaquina,
                    alerta["id_alerta"],
                    idMetrica[i],
                    porc[i],
                    alerta["descricao"]
                )

                cursor.execute(query, values)
                db.commit()

                print(cursor.rowcount, "registro inserido em logMonitoramento")

    except Error as e:
        print('Erro ao inserir no MySQL -', e)



# fks

db = conectar_server()
macAddres =identificar_macaddres(db)
fkCpu = identifica_fk(db, "Ryzen 5 5600X", macAddres)
fkRam = identifica_fk(db, "Vengeance LPX", macAddres)
fkDisc = identifica_fk(db, "978 EVO Plus", macAddres)
print(fkRam)

while True:
    idMaquina = fkCpu["idMaquina"]
    ram_porc = p.virtual_memory().percent
    disk_porc = p.disk_usage("/").percent
    disk_usage = p.disk_usage("C://").used
    cpu_porc = p.cpu_percent(interval=1, percpu=True)
    if db:
        # Chamada para salvar no banco
        inserir_porcentagem(cpu_porc, db, fkCpu["idMaquina"], fkCpu["idComponente"], fkCpu["idMetrica"])
        inserir_porcentagem(ram_porc, db, fkRam["idMaquina"], fkRam["idComponente"], fkRam["idMetrica"])
        inserir_porcentagem(disk_porc, db, fkDisc["idMaquina"], fkDisc["idComponente"], fkDisc["idMetrica"])
    
    sleep(2)
