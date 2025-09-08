import psutil as p, datetime, time, os
from utils import mysql

pkts_rec_antes = p.net_io_counters(pernic=False, nowrap=True).packets_recv 
pkts_env_antes = p.net_io_counters(pernic=False, nowrap=True).packets_sent 
print("Iniciando...")
time.sleep(2)

for i in range(20):
    os.system('cls')
    mac_address = p.net_if_addrs().get('Wi-Fi')[0][1]
    uso_cpu = p.cpu_percent(interval=None, percpu=False)
    uso_ram = p.virtual_memory().percent
    uso_disco = p.disk_usage("C://").percent
    pkts_rec_agora = p.net_io_counters(pernic=False, nowrap=True).packets_recv 
    pkts_env_agora = p.net_io_counters(pernic=False, nowrap=True).packets_sent 
    horario_medicao = datetime.datetime.now().strftime("%H:%M:%S")

    #temp_cpu = p.sensors_temperatures(fahrenheit=False).get('coretemp')[0][1]

    pkts_rec_por_seg = (pkts_rec_agora - pkts_rec_antes) / 2
    pkts_env_por_seg = (pkts_env_agora - pkts_env_antes) / 2
    
    pkts_rec_antes = pkts_rec_agora
    pkts_env_antes = pkts_env_agora

    mysql.executar(f"INSERT INTO leitura (uso_medioCPU, uso_memoria, uso_disco, fk_mac_address, throughput_recebido, throughput_enviado) VALUES ({uso_cpu}, {uso_ram}, {uso_disco}, '{mac_address}', {pkts_rec_por_seg}, {pkts_env_por_seg})")

    print(f"""
    ###################################################################
    #                  Dados inseridos com sucesso!                   #
    ###################################################################

        ############################################################
        #   MAC Address                    #   {mac_address}   #
        #----------------------------------------------------------#
        #   Uso de CPU                     #        {uso_cpu:04}%          #
        #----------------------------------------------------------#
        #   Uso de RAM                     #        {uso_ram:04}%          #
        #----------------------------------------------------------#
        #   Uso de Disco                   #        {uso_disco:04}%          #
        #----------------------------------------------------------#
        #   Pacotes Recebidos por segundo  #        {pkts_rec_por_seg }          #
        #----------------------------------------------------------#
        #   Pacotes Enviados por segundo   #        {pkts_env_por_seg}            #
        #----------------------------------------------------------#
        #                     Horário: {horario_medicao:04}                    #
        ############################################################
    """)
    time.sleep(2)