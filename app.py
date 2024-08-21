# Importa as bibliotecas necessárias
import paho.mqtt.client as mqttClient
import time
import serial
import json
import os

print("[INFO] Bibliotecas importadas.")



# Lista para armazenar os valores das frequências recebidas pelo broker MQTT 
Frequencias = ["X", "X", "X", "X", "X"]
# Variável que exibe ou não os prints "secundários" do sistema
Prints = True


# Se conecta ao broker MQTT
connected = False
last_message = None
BROKER_ENDPOINT = "industrial.api.ubidots.com"
PORT = 1883
MQTT_USERNAME = "BBUS-Juyv8uOBxCKUhPITquKC1exoNmF2nL"
MQTT_PASSWORD = ""
TOPIC = "/v1.6/devices/"
DEVICE_LABEL = "aviao"



# Inicia a comunicação serial com o arduino
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
print("[INFO] Serial comunication started")


def mainCode(Frequencias):
    # Exibe os valores de frequência na tela
    print("Valores das frequencias do broker MQTT: " + str(Frequencias[0]) + ", " + str(Frequencias[1]) + ", " + str(Frequencias[2]) + ", " + str(Frequencias[3]) + ", " + str(Frequencias[4]))

    # Lê a porta serial especificada anteriormente
    data = str(ser.readline(1))
    data = data[2:-1]
    print("Leitura da porta serial: " + data)

    # Variável que armazena a frequência em que o avião deve se conectar
    str_ = ""

    # Envia a frequência correta na porta serial de volta ao Arduino Nano
    if data == "A":
        str_ = str(Frequencias[0])
        packet = str.encode(str_)
        ser.write(packet)
        if Prints:
            print(packet)
    elif data == "B":
        str_ = str(Frequencias[1])
        packet = str.encode(str_)
        ser.write(packet)
        if Prints:
            print(packet)
    elif data == "C":
        str_ = str(Frequencias[2])
        packet = str.encode(str_)
        ser.write(packet)
        if Prints:
            print(packet)
    elif data == "D":
        str_ = str(Frequencias[3])
        packet = str.encode(str_)
        ser.write(packet)
        if Prints:
            print(packet)
    elif data == "E":
        str_ = str(Frequencias[4])
        packet = str.encode(str_)
        ser.write(packet)
        if Prints:
            print(packet)
    
    # Publica a frequência do avião no Ubidots
    if str_ != "":
        # Constrói a publicação do broker
        VARIABLE_LABEL_PUB = "aviao"
        topic = TOPIC + DEVICE_LABEL
        payload = {
            VARIABLE_LABEL_PUB:{
                "value": str_
            }
        }
        payload_json = json.dumps(payload)
        
        if Prints:
            print("[INFO] Payload: " + str(payload))
            print("[INFO] Topic: " + topic)
        
        Publish(mqtt_client, topic, payload_json)
        print("[INFO] Frequência do avião publicada no Ubidots.")



def TestConnection():
    try:
        # Executa o comando de ping 2 vezes no servidor da google
        response = os.system(f"ping -c 3 google.com")
        if Prints:
            print("Ping: " + str(response))
        
        # Descobre se a Raspberry Pi possui conexão com a internet
        if response == 0:
            print("[INFO] Conectado no broker.")
            return True
        elif response >= 1:
            print("[WARN] Desconectado do broker.")
            return False
        
    except Exception as e:
        print("[WARN] Desconectado do broker.")
        return False


def Publish(mqtt_client, topic, payload):
    try:
        mqtt_client.publish(topic, payload)
    except Exception as e:
        print("[ERROR] Erro na publicação: \n{}".format(e))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        global connected
        connected = True
        
        print("[INFO] Conectado no broker")
        
        # Se inscreve em todas as variáveis do broker MQTT
        link = TOPIC + DEVICE_LABEL + "/+"
        client.subscribe(link)

        print("[INFO] Inscrito no topico : {link}")

    else:
        if Prints:
            print("[INFO] Erro, a conexão falhou com o código: ", rc)
        print("[EMERGENCY] Iniciando o sistema de emergência...")
        packet = str.encode("X")
        ser.write(packet)


def on_message(client, userdata, message):
    global last_message
    
    try:
        last_message = message.payload.decode()
        if Prints:
            print(f"[INFO] Mensagem recebida: {last_message}")

        data = json.loads(last_message)

        # Verifica se a chave 'context' existe e se a cahve 'Info' existe dentro da chave 'context'
        info = data.get('context', {}).get('Info')
        value = data.get('value')

        if info and value is not None:  # Verifica se 'info' e 'value' não são None
            if info == "AreaA":
                Frequencias[0] = int(value)

            elif info == "AreaB":
                Frequencias[1] = int(value)

            elif info == "AreaC":
                Frequencias[2] = int(value)

            elif info == "AreaD":
                Frequencias[3] = int(value)

            elif info == "AreaE":
                Frequencias[4] = int(value)

        else:
            print("[WARN] Algo está ausente na mensagem...")

        mainCode(Frequencias)
    
    except json.JSONDecodeError:
        if Prints:
            print("[ERROR] Json decode error.")


def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port):
    global connected

    if not connected:
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.connect(broker_endpoint, port=port)
        mqtt_client.loop_start()

        attempts = 0

        while not connected and attempts < 5:
            print("[INFO] Conectando-se no broker...")
            
            time.sleep(1)
            attempts += 1

    if not connected:
        print("[ERROR] Nao foi possível conectar-se no broker")
        print("[EMERGENCY] Iniciando o sistema de emergência...")
        packet = str.encode("X")
        ser.write(packet)

        return False
    
    return True



while True:
    if __name__ == '__main__':
        try:
            mqtt_client = mqttClient.Client()
            if connect(mqtt_client, MQTT_USERNAME, MQTT_PASSWORD, BROKER_ENDPOINT,PORT):
                if Prints:
                    print("[INFO] Conectado e inscrito, esperando pelas próximas mensagens...")
                
                while True:
                    CONNECTION_TEST = TestConnection()
                    if CONNECTION_TEST:
                        link = TOPIC + DEVICE_LABEL + "/+"
                        mqtt_client.subscribe(link)
        
                        # Inicia o código principal do projeto
                        mainCode(Frequencias)
                
                    else:
                        print("[WARN] O dispositivo não possui conexão com a internet.")
                        print("[EMERGENCY] Iniciando o sistema de emergência...")
                        packet = str.encode("X")
                        ser.write(packet)
                        time.sleep(0.5)
                    
            else:
                if Prints:
                    print("[WARN] Não foi possível se conectar no broker.")
                print("[EMERGENCY] Iniciando o sistema de emergência...")
                packet = str.encode("X")
                ser.write(packet)
                
        except Exception as e:
            if Prints:
                print("[WARN] Não foi possível se conectar no broker: " + str(e))
            print("[EMERGENCY] Iniciando o sistema de emergência...")        
            packet = str.encode("X")
            ser.write(packet)
    
    time.sleep(1)