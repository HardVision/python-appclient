from utils import mysql
import os

hora = True
cpu = True
ram = True
disco = True

def create_columns(hora, cpu, ram, disco):
    fcolumns = []
    if hora : fcolumns.append('dt_registro') 
    else : fcolumns.append('null')
    if cpu : fcolumns.append('cpu_porcentagem')
    else : fcolumns.append('null')
    if ram : fcolumns.append('ram_porcentagem')
    else : fcolumns.append('null')
    if disco : fcolumns.append('disco_porcentagem')
    else : fcolumns.append('null')
    return fcolumns

def exibir_consulta():
    columns = create_columns(hora, cpu, ram, disco)
    query = f"SELECT {', '.join(columns)} FROM captura_hardware_usage ORDER BY 1 DESC LIMIT 10;"
    resultado = mysql.executar(query)
    tabela = "~ RESULTADO DA QUERY ~\n"
    if hora : tabela += "||     Timestamp       "
    if cpu : tabela += "|| Uso de CPU "
    if ram : tabela += "|| Uso de RAM "
    if disco : tabela += "|| Uso de Disco "
    tabela += "||\n"
    for linha in resultado:
        tabela += "\n"
        if hora : tabela += f"|| {linha[0]} "
        if cpu : tabela += f"||   {linha[1]:04}%    "
        if ram : tabela += f"||   {linha[2]:04}%    "
        if disco : tabela += f"||    {linha[3]:04}%     "
        tabela += "||\n"
    print(tabela)


while True:
    exibir_consulta()

    print("""
  =========== MENU - Digite um número ===========
  1 - timestamp on/off  |  4 - uso de disco on/off                      |  7 - fechar programa
  2 - uso de cpu on/off |  5 - deletar últimos 5 registros              |  
  3 - uso de ram on/off |  6 - atualizar timestamp últimos 3 registros  |  
""")
    comando = input("digite seu comando~ ")
    os.system('cls')
    match comando:
        case "1":
            hora = not hora
        case "2":
            cpu = not cpu
        case "3":
            ram = not ram
        case "4":
            disco = not disco
        case "5":
            mysql.executar("DELETE FROM captura_hardware_usage WHERE id IN (SELECT * FROM (SELECT id FROM captura_hardware_usage ORDER BY dt_registro DESC, id DESC LIMIT 5) AS temp);")
        case "6":
            mysql.executar("UPDATE captura_hardware_usage SET dt_registro = current_timestamp WHERE id IN (SELECT * FROM (SELECT id FROM captura_hardware_usage ORDER BY dt_registro DESC, id DESC LIMIT 3) AS temp);")
        case "7":
            print("\nAté a próxima! Desligando programa...")
            break
        case _:
            continue



