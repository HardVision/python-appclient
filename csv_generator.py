from mysql.connector import connect, Error
import dotenv as d
from os import getenv
import pandas as pd
from mysql_connect import conectar_server
import consulta as c
from tabulate import tabulate

db = conectar_server()

def exportar_dados_componente(num, macAddres):
    try:
        cursor = db.cursor()
        componente = ""
        if num == 1:
            componente = "CPU"
        if num == 2:
            componente = "RAM"
        if num == 3:
            componente = "HD"
        
        print(componente)
        print(macAddres)

        slctQuery = """
    SELECT
        l.valor,
        me.medida,
        c.tipo,
        c.modelo,
        TRIM(m.macAddress) AS macAddress,
        l.descricao
    FROM logMonitoramento l
    JOIN maquina m ON l.fkMaquina = m.idMaquina
    JOIN componente c ON l.fkComponente = c.idComponente
    JOIN metrica me ON l.fkMetrica = me.idMetrica
    WHERE TRIM(m.macAddress) = %s
    AND c.tipo = %s

"""
        cursor.execute(slctQuery, (macAddres, componente))
        headers = ["Valor", "Medida", "Tipo", "Modelo", "Mac Address", "Descrição"]
        resultados = cursor.fetchall()
        print("\n--- Monitoramento (últimos registros) ---")
        print(tabulate(resultados, headers, tablefmt="fancy_grid"))
        cursor.close()
        
    except Error as e:
        print('Error ao selecionar no MySQL -', e , " - identifica-fk")

    

    
def escolha_maquina(db):
    c.exibir_maquinas(db)
    maquina = input(str("Dígite o MacAddres: "))
    return maquina

    
while True:
    print("\n=== Gerador de CSV ===")
    print("1 - Gerar CSV de CPU")
    print("2 - Gerar CSV de RAM")
    print("3 - Gerar CSV de disco")
    print("0 - Sair")
    
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        c.exibir_maquinas(db)
        maquina = escolha_maquina(db)
        exportar_dados_componente(opcao, maquina)
    elif opcao == 2:
        c.exibir_maquinas(db)
        maquina = escolha_maquina(db)
        exportar_dados_componente(opcao, maquina)
    elif opcao == 3:
        c.exibir_maquinas(db)
        maquina = escolha_maquina(db)
        exportar_dados_componente(opcao, maquina)
    elif opcao == 0:
        print("Operação Finalizada!")
        break
    else:
        print("Opção inválida!")