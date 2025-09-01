import psutil as p, datetime, time, os
from utils import mysql


for i in range(20):
    # os.system('cls')
    uso_cpu = p.cpu_percent(interval=None, percpu=False)
    uso_ram = p.virtual_memory().percent
    uso_disco = p.disk_usage("C://").percent
    horario_medicao = datetime.datetime.now().strftime("%H:%M:%S")
    mac_address = p.net_if_addrs().get('Wi-Fi')[0][1]

    mysql.executar(f"INSERT INTO captura_hardware_usage (cpu_porcentagem, ram_porcentagem, disco_porcentagem, mac_address) VALUES ({uso_cpu}, {uso_ram}, {uso_disco}, '{mac_address}')")

    print(f"""
    #################################################
    #        Dados inseridos com sucesso!           #
    #################################################

        #########################################
        #   Uso de CPU   #        {uso_cpu:04}%         #
        #---------------------------------------#
        #   Uso de RAM   #        {uso_ram:04}%         #
        #---------------------------------------#
        #  Uso de Disco  #        {uso_disco:04}%         #
        #---------------------------------------#
        #  MAC Address   #   {mac_address}  #
        #---------------------------------------#
        #           Horário: {horario_medicao:04}           #
        #########################################
    """)
    time.sleep(2)

