from mysql.connector import connect, Error
from os import getenv
import dotenv as d
from tabulate import tabulate
from mysql_connect import conectar_server

d.load_dotenv()

def exibir_maquinas(db):
    cursor = db.cursor() 
    cursor.execute("SELECT idMaquina, macAddress FROM maquina")
    headers = ["Maquina", "Mac Adress"]
    resultados = cursor.fetchall()
    print("\n--- Máquinas ---")
    print(tabulate(resultados, headers, tablefmt="fancy_grid"))
    cursor.close()

def exibir_componentes(db):
    cursor = db.cursor()
    cursor.execute("SELECT idComponente, tipo, modelo FROM componente")
    headers = ["Componente", "Tipo", "Modelo"]
    resultados = cursor.fetchall()
    print("\n--- Componentes ---")
    print(tabulate(resultados, headers, tablefmt="fancy_grid"))
    cursor.close()

def exibir_monitoramento(db):
    cursor = db.cursor()
    cursor.execute("SELECT fkMaquina, fkComponente, macAddress, tipo, modelo, valor, dtHora FROM logMonitoramento join componente on fkComponente = idComponente join maquina on fkMaquina = idMaquina order by idMonitoramento desc LIMIT 10")
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
