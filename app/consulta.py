from mysql.connector import connect, Error
from os import getenv
import dotenv as d
from tabulate import tabulate

d.load_dotenv()


def conectar_server():
    config = {
    'user': getenv("USER_SELECT_DB"),
    'password': getenv("PASSWORD_DB"),
    'host': getenv("HOST_DB"),
    'database': getenv("DATABASE_DB"),
    'port': getenv("PORT_DB")
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

def exibir_maquinas(db):
    cursor = db.cursor() 
    cursor.execute("SELECT idMaquina, macAdress FROM Maquina")
    headers = ["Maquina", "Mac Adress"]
    resultados = cursor.fetchall()
    print("\n--- Máquinas ---")
    print(tabulate(resultados, headers, tablefmt="fancy_grid"))
    cursor.close()

def exibir_componentes(db):
    cursor = db.cursor()
    cursor.execute("SELECT idComponente, tipo, modelo FROM Componente")
    headers = ["Componente", "Tipo", "Modelo"]
    resultados = cursor.fetchall()
    print("\n--- Componentes ---")
    print(tabulate(resultados, headers, tablefmt="fancy_grid"))
    cursor.close()

def exibir_monitoramento(db):
    cursor = db.cursor()
    cursor.execute("SELECT fkMaquina, fkComponente, macAdress, tipo, modelo, valor, dtHora FROM LogMonitoramento join Componente on fkComponente = idComponente join Maquina on fkMaquina = idMaquina order by idMonitoramento desc LIMIT 10")
    headers = ["Máquina", "Componente", "Mac Adress", "Tipo", "Modelo", "Valor %","Data de captura"]
    resultados = cursor.fetchall()
    print("\n--- Monitoramento (últimos registros) ---")
    print(tabulate(resultados, headers, tablefmt="fancy_grid"))
    cursor.close()
def menu():
    db = conectar_server()
    
    if not db:
        return
    
    while True:
        print("\n=== MENU ===")
        print("1 - Listar Máquinas")
        print("2 - Listar Componentes")
        print("3 - Mostrar Monitoramento")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_maquinas(db)
        elif opcao == "2":
            exibir_componentes(db)
        elif opcao == "3":
            exibir_monitoramento(db)
        elif opcao == "0":
            print("Operação Finalizada!")
            break
        else:
            print("Opção inválida!")

    db.close()
menu()