from utils import mysql
import os

hora = True
cpu = True
ram = True
disco = True
macAddress = True

def create_columns(macAddress, hora, cpu, ram, disco):
    fcolumns = []
    if macAddress : fcolumns.append('mac_address')
    else : fcolumns.append('null')
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
    columns = create_columns(macAddress, hora, cpu, ram, disco)
    query = f"SELECT {', '.join(columns)} FROM captura_hardware_usage ORDER BY 1 DESC LIMIT 10;"
    resultado = mysql.executar(query)
    tabela = "~ RESULTADO DA QUERY ~\n"
    if macAddress : tabela += "||    MAC Address   "
    if hora : tabela += "||     Timestamp       "
    if cpu : tabela += "|| Uso de CPU "
    if ram : tabela += "|| Uso de RAM "
    if disco : tabela += "|| Uso de Disco "
    tabela += "||\n"
    
    for linha in resultado:
        tabela += "\n"
        if macAddress : tabela += f"|| {linha[0]}"
        if hora : tabela += f"|| {linha[1]} "
        if cpu : tabela += f"||   {linha[2]:04}%    "
        if ram : tabela += f"||   {linha[3]:04}%    "
        if disco : tabela += f"||    {linha[4]:04}%     "
        tabela += "||\n"
    print(tabela)


while True:
    exibir_consulta()

    print("""
                              =========== MENU - Digite um número ===========
  1 - MAC Address on/off |  4 - uso de RAM on/off            |  7 - atualizar timestamp últimos 3 registros
  2 - timestamp on/off   |  5 - uso de Disco on/off          |  8 - fechar programa
  3 - uso de CPU on/off  |  6 - deletar últimos 5 registros  |  
""")
    comando = input("digite seu comando~ ")
    os.system('cls')
    
    match comando:
        case "1":
            macAddress = not macAddress
        case "2":
            hora = not hora
        case "3":
            cpu = not cpu
        case "4":
            ram = not ram
        case "5":
            disco = not disco
        case "6":
            mysql.executar("DELETE FROM captura_hardware_usage WHERE id IN (SELECT * FROM (SELECT id FROM captura_hardware_usage ORDER BY dt_registro DESC, id DESC LIMIT 5) AS temp);")
        case "7":
            mysql.executar("UPDATE captura_hardware_usage SET dt_registro = current_timestamp WHERE id IN (SELECT * FROM (SELECT id FROM captura_hardware_usage ORDER BY dt_registro DESC, id DESC LIMIT 3) AS temp);")
        case "8":
            print("\nAté a próxima! Desligando programa...")
            break
        case _:
            continue



