from utils import mysql
import os

hora = True
cpu = True
ram = True
disco = True
macAddress = True
pkts_rec = True
pkts_env = True
temp_cpu = True

def create_columns(macAddress, hora, cpu, ram, disco, pkts_rec, pkts_env, temp_cpu):
    fcolumns = []
    if macAddress : fcolumns.append('fk_mac_address')
    else : fcolumns.append('null')
    if hora : fcolumns.append('data_hora') 
    else : fcolumns.append('null')
    if cpu : fcolumns.append('uso_medioCPU')
    else : fcolumns.append('null')
    if ram : fcolumns.append('uso_memoria')
    else : fcolumns.append('null')
    if disco : fcolumns.append('uso_disco')
    else : fcolumns.append('null')
    if pkts_rec : fcolumns.append('throughput_recebido')
    else : fcolumns.append('null')
    if pkts_env : fcolumns.append('throughput_enviado')
    else : fcolumns.append('null')
    if temp_cpu : fcolumns.append('temperatura_cpu')
    else : fcolumns.append('null')
    return fcolumns

def exibir_consulta():
    columns = create_columns(macAddress, hora, cpu, ram, disco, pkts_rec, pkts_env, temp_cpu)
    query = f"SELECT {', '.join(columns)} FROM leitura ORDER BY 1 DESC LIMIT 10;"
    resultado = mysql.executar(query)
    tabela = "~ RESULTADO DA QUERY ~\n"
    if macAddress : tabela += "||    MAC Address   "
    if hora : tabela += "||     Timestamp       "
    if cpu : tabela += "|| Uso de CPU "
    if ram : tabela += "|| Uso de RAM "
    if disco : tabela += "|| Uso de Disco "
    if pkts_rec : tabela += "|| Pacotes Recebidos "
    if pkts_env : tabela += "|| Pacotes Enviados "
    if temp_cpu : tabela += "|| Temperatura da CPU "
    tabela += "||\n"
    
    for linha in resultado:
        tabela += "\n"
        if macAddress : tabela += f"|| {linha[0]}"
        if hora : tabela += f"|| {linha[1]} "
        if cpu : tabela += f"||   {linha[2]:04}%    "
        if ram : tabela += f"||   {linha[3]:04}%    "
        if disco : tabela += f"||    {linha[4]:04}%     "
        if pkts_rec : tabela += f"|| {linha[5]}"
        if pkts_env : tabela += f"|| {linha[6]}"
        if temp_cpu : tabela += f"|| {linha[7]}"
        tabela += "||\n"
    print(tabela)


while True:
    exibir_consulta()

    print("""
                                            =========== MENU - Digite um número ===========
  1 - MAC Address on/off    |  4 - uso de RAM on/off            |  7 - pacotes enviados on/off        | 10 - atualizar timestamp últimos 3 registros
  2 - timestamp on/off      |  5 - uso de Disco on/off          |  8 - temperatura CUP                | 11 - fechar programa
  3 - uso de CPU on/off     |  6 - pacotes recebidos on/off     |  9 - deletar últimos 5 registros    |
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
            pkts_rec = not pkts_rec
        case "7":
            pkts_env = not pkts_env
        case "8":
            mysql.executar("DELETE FROM leitura WHERE id IN (SELECT * FROM (SELECT id FROM leitura ORDER BY dt_registro DESC, id DESC LIMIT 5) AS temp);")
        case "9":
            mysql.executar("UPDATE leitura SET dt_registro = current_timestamp WHERE id IN (SELECT * FROM (SELECT id FROM captura_hardware_usage ORDER BY dt_registro DESC, id DESC LIMIT 3) AS temp);")
        case "10":
            print("\nAté a próxima! Desligando programa...")
            break
        case _:
            continue