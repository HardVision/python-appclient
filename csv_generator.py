from mysql.connector import connect, Error
import dotenv as d
from os import getenv
import pandas as pd
from mysql_connect import conectar_server
import consulta as c
db = conectar_server()
    
while True:
    print("\n=== Gerador de CSV ===")
    print("1 - Gerar CSV de CPU")
    print("2 - Gerar CSV de RAM")
    print("3 - Gerar CSV de disco")
    print("0 - Sair")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        c.exibir_maquinas()
        c.exibir_componentes()
    elif opcao == "2":
        c.exibir_maquinas()
        c.exibir_componentes()
    elif opcao == "3":
        c.exibir_maquinas()
        c.exibir_componentes()  
    elif opcao == "0":
        print("Operação Finalizada!")
        break
    else:
        print("Opção inválida!")