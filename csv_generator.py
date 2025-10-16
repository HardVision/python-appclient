from mysql.connector import Error
import pandas as pd
from mysql_connect import conectar_server
import consulta as c
import os


db = conectar_server()


def exportar_dados_nucleo(macAddres):
    try:
        with db.cursor() as cursor:
            macAddres = (macAddres,)
            slctQueryCpu = """
                SELECT
                    c.tipo AS nome_nucleo,
                    l.valor AS uso_cpu,
                    MINUTE(l.dtHora) AS minuto
                FROM logMonitoramento l
                JOIN maquina m ON l.fkMaquina = m.idMaquina
                JOIN componente c ON l.fkComponente = c.idComponente
                JOIN metricaComponente me ON l.fkMetrica = me.idMetrica
                WHERE TRIM(m.macAddress) = %s
                AND c.tipo LIKE 'CPU%%'
                ORDER BY nome_nucleo, minuto;
            """
            cursor.execute(slctQueryCpu, macAddres)
            valores = cursor.fetchall()
            slice_nucleos(valores)
    except Error as e:
        print("Não foi possível realizar a consulta - ", e)


def slice_nucleos(nucleos):

    df = pd.DataFrame(nucleos, columns=["Núcleo", "Valor", "Minuto"])

    resumo = df["Núcleo"].value_counts().sort_index()

    tam = resumo.min()
    print(f"\nUsando {tam+1} registros")

    dados = {}
    for nucleo in resumo.index:
        valores = df.loc[df["Núcleo"] == nucleo, "Valor"].head(tam).to_list()
        dados[nucleo] = valores

    df_final = pd.DataFrame(dados)

    print("\n=== DataFrame final ===")
    print(df_final.head(10)) 

    caminho_arquivo = os.path.join(os.getcwd(), "cpu_nucleos_por_coluna.csv")
    df_final.to_csv(caminho_arquivo, index=False)
    print(f"\nArquivo CSV salvo em: {caminho_arquivo}")

    

def exportar_dados_componente(macAddres):
    try:
        cursor = db.cursor()
        macAddres = macAddres,
        print(macAddres)
        

        slctQueryCpu = """
    SELECT
        l.valor
    FROM logMonitoramento l
    JOIN maquina m ON l.fkMaquina = m.idMaquina
    JOIN componente c ON l.fkComponente = c.idComponente
    JOIN metricaComponente me ON l.fkMetrica = me.idMetrica
    WHERE TRIM(m.macAddress) = %s
    AND c.tipo like '%CPU%'
"""

        slctQueryRam = """
    SELECT
        l.valor
    FROM logMonitoramento l
    JOIN maquina m ON l.fkMaquina = m.idMaquina
    JOIN componente c ON l.fkComponente = c.idComponente
    JOIN metricaComponente me ON l.fkMetrica = me.idMetrica
    WHERE TRIM(m.macAddress) = %s
    AND c.tipo = 'RAM'

"""

        slctQueryDisco = """
    SELECT
        l.valor
    FROM logMonitoramento l
    JOIN maquina m ON l.fkMaquina = m.idMaquina
    JOIN componente c ON l.fkComponente = c.idComponente
    JOIN metricaComponente me ON l.fkMetrica = me.idMetrica
    WHERE TRIM(m.macAddress) = %s
    AND c.tipo = 'Disco'

"""

        slctQueryMin = """
    SELECT
        minute(l.dtHora)
    FROM logMonitoramento l
    JOIN maquina m ON l.fkMaquina = m.idMaquina
    JOIN componente c ON l.fkComponente = c.idComponente
    JOIN metricaComponente me ON l.fkMetrica = me.idMetrica
    WHERE TRIM(m.macAddress) = %s
    AND c.tipo = 'Disco'

    """
        cursor.execute(slctQueryCpu, macAddres)
        resultados_cpu = cursor.fetchall()
        cursor.execute(slctQueryRam, macAddres)
        resultados_ram = cursor.fetchall()
        cursor.execute(slctQueryDisco, macAddres)
        resultados_disco = cursor.fetchall()
        cursor.execute(slctQueryMin, macAddres)
        resultados_min= cursor.fetchall()
        
        print(resultados_cpu, resultados_ram, resultados_disco, resultados_min)

        cpu_tratada = []
        ram_tratada = []
        disco_tratado = []
        min_tratado = []

        for i in range(0,len(resultados_cpu)):
            print(cpu_tratada.append(resultados_cpu[i][0]))
            ram_tratada.append(resultados_ram[i][0])
            disco_tratado.append(resultados_disco[i][0])
            min_tratado.append(resultados_min[i][0])


        cursor.close()
        dict_capturas = {
            "CPU (%)": cpu_tratada,
            "RAM (%)": ram_tratada,
            "Disco (%)": disco_tratado,
            "Minuto de captura": min_tratado
        }
        df = pd.DataFrame(dict_capturas)
        print(df)

        caminho_arquivo = os.path.join(os.getcwd(), "teste.csv")
        df.to_csv(caminho_arquivo, index=False)
        print(f"\nArquivo CSV salvo em: {caminho_arquivo}")
    except Error as e:
        print('Error ao selecionar no MySQL -', e , " - identifica-fk")

    

def escolha_maquina(db):
    c.exibir_maquinas(db)
    maquina = input(str("Dígite o MacAddres: "))
    return maquina

    
db = conectar_server()
maquina = escolha_maquina(db)
exportar_dados_nucleo(maquina)
print("Dados exportados para CSV!")