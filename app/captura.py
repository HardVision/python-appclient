import psutil as p
from mysql.connector import connect, Error
import dotenv as d
from os import getenv
from time import sleep

d.load_dotenv()


def conectar_server():
    config = {
        'user': getenv("USER_DB"),
        'password': getenv("PASSWORD_DB"),
        'host': getenv("HOST_DB"),
        'database': getenv("DATABASE_DB"),
    }

    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.get_server_info()
            print('Connected to MySQL server version -', db_info)
        return db
    
    except Error as e:
        print('Error to connect with MySQL -', e)
        return None


def identifica_fk(db, modelo, macAdress):
    try:
        macAdress = macAdress,
        modelo = modelo,
        with db.cursor() as cursor:
            slctQueryMaq = "SELECT idMaquina FROM maquina WHERE macAddress = %s"
            cursor.execute(slctQueryMaq, macAdress)
            idMaquina = cursor.fetchone()  

            slctQueryComp = "SELECT idComponente FROM Componente WHERE modelo = %s"
            cursor.execute(slctQueryComp, modelo)
            idComponente = cursor.fetchall()  

            slctQueryComp = "SELECT fkMetrica FROM Componente WHERE modelo = %s"
            cursor.execute(slctQueryComp, modelo)
            idMetrica = cursor.fetchone()  

            return {"idMaquina":idMaquina, 
                    "idComponente": idComponente,
                    "idMetrica": idMetrica}
        
    except Error as e:
        print('Error ao selecionar no MySQL -', e , " - identifica-fk")


def inserir_porcentagem(porc, db, idMaquina, idComponente, idMetrica):
    print("Fks: ", idMaquina, idComponente, idMetrica)
    print("Valor a ser adicionado: ", porc)
    try:
        with db.cursor() as cursor:
            if idMaquina and idComponente:
                for i in range(0, len(idComponente)):
                    query = """
                        INSERT INTO LogMonitoramento (fkComponente, fkMaquina, fkMetrica, valor, descricao)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    values = (idComponente[i][0], idMaquina[0], idMetrica[0], porc[i], "Valor adicionado")
                    cursor.execute(query, values)
                    db.commit()
                    print(cursor.rowcount, "registro inserido na tabela Monitoramento")
            else:
                print("Máquina ou componente não encontrados no banco de dados.")

    except Error as e:
        print('Error ao inserir no MySQL -', e)




db = conectar_server()
fkCpu = identifica_fk(db, "Intel Xeon", "00:1A:2B:3C:4D:5E")
fkRam = identifica_fk(db, "DDR4", "00:1A:2B:3C:4D:5E")
fkDisc = identifica_fk(db, "Seagate", "00:1A:2B:3C:4D:5E")
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