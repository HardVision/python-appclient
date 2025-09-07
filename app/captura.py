import psutil as p, datetime, time, os
from utils import mysql


for i in range(20):
    os.system('cls')
    mac_address = p.net_if_addrs().get('Wi-Fi')[0][1]
    uso_cpu = p.cpu_percent(interval=None, percpu=False)
    uso_ram = p.virtual_memory().percent
    uso_disco = p.disk_usage("C://").percent
    pkts_rec = p.net_io_counters(pernic=False, nowrap=True)[2]
    pkts_env = p.net_io_counters(pernic=False, nowrap=True)[3]
    horario_medicao = datetime.datetime.now().strftime("%H:%M:%S")
    
    #temp_cpu = p.sensors_temperatures(fahrenheit=False).get('coretemp')[0][1]

    mysql.executar(f"INSERT INTO captura_hardware_usage (uso_medioCPU, uso_memoria, uso_disco, mac_address, pkts_recebidos, pkts_enviados) VALUES ({uso_cpu}, {uso_ram}, {uso_disco}, '{mac_address}', {pkts_rec}, {pkts_env}")

    print(f"""
    ########################################################
    #             Dados inseridos com sucesso!             #
    ########################################################

        ################################################
        #   MAC Address        #   {mac_address}   #
        #----------------------------------------------#
        #   Uso de CPU         #        {uso_cpu:04}%          #
        #----------------------------------------------#
        #   Uso de RAM         #        {uso_ram:04}%          #
        #----------------------------------------------#
        #   Uso de Disco       #        {uso_disco:04}%          #
        #----------------------------------------------#
        #   Pacotes Recebidos  #       {pkts_rec}         #
        #----------------------------------------------#
        #   Pacotes Enviados   #       {pkts_env}         #
        #----------------------------------------------#
        #              Horário: {horario_medicao:04}               #
        ################################################
    """)
    time.sleep(2)