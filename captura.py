import psutil as p
from mysql.connector import Error
import dotenv as d
from time import sleep
from mysql_connect import conectar_server

d.load_dotenv()

def identifica_fk(db, modelo, macAdress):
    try:
        with db.cursor() as cursor1:
            cursor1.execute("SELECT idMaquina FROM maquina WHERE macAddress = %s", (macAdress,))
            idMaquina = cursor1.fetchone()

        with db.cursor() as cursor2:
            cursor2.execute("SELECT idComponente FROM componente WHERE modelo = %s", (modelo,))
            idComponente = cursor2.fetchall()

        with db.cursor() as cursor3:
            cursor3.execute("SELECT fkMetrica FROM componente WHERE modelo = %s", (modelo,))
            idMetrica = cursor3.fetchone()

        print(f"Maquina: {idMaquina} Componente: {idComponente} Metrica: {idMetrica}")

        return {
            "idMaquina": idMaquina,
            "idComponente": idComponente,
            "idMetrica": idMetrica
        }

    except Error as e:
        print('Error ao selecionar no MySQL -', e, "- identifica-fk")
        # Retorna valores padrão para evitar o erro 'NoneType'
        return {
            "idMaquina": None,
            "idComponente": None,
            "idMetrica": None
        }


def inserir_porcentagem(porc, db, idMaquina, idComponente, idMetrica):
    print("Fks: ", idMaquina, idComponente, idMetrica)
    print("Valor a ser adicionado: ", porc)
    try:
        with db.cursor() as cursor:
            if idMaquina and idComponente:
                for i in range(0, len(idComponente)):
                    query = """
                        INSERT INTO logMonitoramento (fkComponente, fkMaquina, fkAlerta, fkMetrica, valor, descricao)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    values = (idComponente[i][0], idMaquina[0], 1, idMetrica[0], porc[i], "Valor adicionado")
                    cursor.execute(query, values)
                    db.commit()
                    print(cursor.rowcount, "registro inserido na tabela Monitoramento")
            else:
                print("Máquina ou componente não encontrados no banco de dados.")

    except Error as e:
        print('Error ao inserir no MySQL -', e)




db = conectar_server()
fkCpu = identifica_fk(db, "Ryzen 5 5600X", "00:1A:2B:3C:4D:5E")
fkRam = identifica_fk(db, "Vengeance LPX", "00:1A:2B:3C:4D:5E")
fkDisc = identifica_fk(db, "970 EVO Plus", "00:1A:2B:3C:4D:5E")
print(fkRam)

while True:
    ram_porc = p.virtual_memory().percent,
    disc_porc = p.disk_usage("/").percent,
    cpu_porc = p.cpu_percent(interval=1, percpu=True)
    if db:
        # Chamada para salvar no banco
        inserir_porcentagem(cpu_porc, db, fkCpu["idMaquina"], fkCpu["idComponente"], fkCpu["idMetrica"])
        inserir_porcentagem(ram_porc, db, fkRam["idMaquina"], fkRam["idComponente"], fkRam["idMetrica"])
        inserir_porcentagem(disc_porc, db, fkDisc["idMaquina"], fkDisc["idComponente"], fkDisc["idMetrica"])

      
    sleep(2)