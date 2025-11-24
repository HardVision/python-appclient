import psutil
import time
import requests
from getmac import get_mac_address as gma

app = "http://localhost:8080/"

# Armazena o último estado para calcular MB/s
ultima_verificacao_disco = psutil.disk_io_counters()

#Função para pegar o macAddress da máquina atual
def get_mac():
    macAddress = gma()

    return macAddress

#Função para pegar a velocidade de leitura e escrita de megabytes por segundo que o disco ta fazendo agora
def get_disco_velocidade_mb():
    global ultima_verificacao_disco

    atual = psutil.disk_io_counters()

    #Aqui pega a leitura por segundo que o disco ta fazendo em megabytes
    leitura_mb_s = (atual.read_bytes - ultima_verificacao_disco.read_bytes) / (1024**2) 

    #Aqui pega a leitura por segundo que o disco ta fazendo em megabytes
    escrita_mb_s = (atual.write_bytes - ultima_verificacao_disco.write_bytes) / (1024**2)

    #Aqui eu to reatribuindo valor para que a próxima verificação seja precisa
    ultima_verificacao_disco = atual

    return {
        "leitura_mb_s": round(leitura_mb_s, 2),
        "escrita_mb_s": round(escrita_mb_s, 2)
    }


#Função para pegar os top processos que que estão utilizando do disco no momento
#Função básica utilizando de for para pegar os dados, e colocando um limite de retorno, para 4 processos e dando um sort para pegar pelo total de bytes
def get_top_processes(limit=4):
    processos = []

    for p in psutil.process_iter(['pid', 'name', 'io_counters']):
        try:
            io = p.info['io_counters']
            if io:
                leitura_mb = io.read_bytes / (1024**2)
                escrita_mb = io.write_bytes / (1024**2)
                total_mb = leitura_mb + escrita_mb

                processos.append({
                    "pid": p.info['pid'],
                    "nome": p.info['name'],
                    "mb_lidos": round(leitura_mb, 2),
                    "mb_escritos": round(escrita_mb, 2),
                    "total_mb": round(total_mb, 2)
                })
        except:
            pass

    # Ordena pelo maior consumo total (em MB) do disco
    processos.sort(key=lambda x: x["total_mb"], reverse=True)

    return processos[:limit]


#Função para pegar a porcentagem usada agora do disco
def get_disco_usage():
    disco = psutil.disk_usage('/')

    return {
        "total_gb": round(disco.total / (1024**3), 2),
        "usado_gb": round(disco.used / (1024**3), 2),
        "livre_gb": round(disco.free / (1024**3), 2),
        "porcentagem_usada": disco.percent,
        "porcentagem_livre": round(100 - disco.percent, 2)
    }

#Função para enviar para a API web, ele utiliza da varíavel app para saber a rota que atualmente é localhost
def enviar_para_node():
    dados = {
        "macAddress": get_mac(),
        "uso": get_disco_usage(),
        "velocidade": list(get_disco_velocidade_mb()),
        "processos": get_top_processes(4)
    }

    try:
        request = requests.post(app, json=dados)
        print("Enviado:", request.status_code)
    except Exception as e:
        print("Erro:", e)

def main():
    try:
        while True:
            enviar_para_node()
            time.sleep(1)
    except Exception as e:
        print("Erro", e)

main()
