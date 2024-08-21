import paho.mqtt.client as mqttClient
import time
import json


connected = False
BROKER_ENDPOINT = "industrial.api.ubidots.com"
PORT = 1883
MQTT_USERNAME = "BBUS-Juyv8uOBxCKUhPITquKC1exoNmF2nL"
MQTT_PASSWORD = ""
TOPIC = "/v1.6/devices/"
DEVICE_LABEL = "aviao"
VARIABLE_LABELS = ["area1", "area2", "area3", "area4", "area5"]


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[INFO] Connected to broker")
        global connected
        connected = True

    else:
        print("[INFO] Error, connection failed")


def on_publish(client, userdata, result):
    print("[INFO] Published!")


def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port):
    global connected

    if not connected:
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish
        mqtt_client.connect(broker_endpoint, port=port)
        mqtt_client.loop_start()

        attempts = 0

        while not connected and attempts < 5:
            print("[INFO] Attempting to connect...")
            time.sleep(1)
            attempts += 1

    if not connected:
        print("[ERROR] Could not connect to broker")
        return False

    return True


def publish(mqtt_client, topic, payload):
    try:
        mqtt_client.publish(topic, payload)
    except Exception as e:
        print("[ERROR] There was an error, details: \n{}".format(e))


# Valor da frequência de cada uma das áreas
Frequencia_Areas = [0, 0, 0, 0, 0]

def main(mqtt_client):
    global Frequencia_Areas

    Contexto_Areas = ["AreaA", "AreaB", "AreaC", "AreaD", "AreaE"]
    i = 0

    for VARIABLE_LABEL in VARIABLE_LABELS:
        topic = TOPIC + DEVICE_LABEL
        payload = {
            VARIABLE_LABEL: {
                "value": Frequencia_Areas[i],
                "context": {
                    "Info": Contexto_Areas[i],
                }
            }
        }
        payload_json = json.dumps(payload)

        # Se conecta ao broker MQTT
        if not connected:
            connect(mqtt_client, MQTT_USERNAME, MQTT_PASSWORD, BROKER_ENDPOINT,
                    PORT)

        print("[INFO] Attempting to publish payload:")
        print(payload)
        print("[INFO] Into Topic:")
        print(topic)
        publish(mqtt_client, topic, payload_json)

        i += 1

        time.sleep(5)

if __name__ == '__main__':
    mqtt_client = mqttClient.Client()
    
    while True:
        Frequencia_Areas[0] = int(input("Insira o valor de freqûencia da área 1: "))
        Frequencia_Areas[1] = int(input("Insira o valor de freqûencia da área 2: "))
        Frequencia_Areas[2] = int(input("Insira o valor de freqûencia da área 3: "))
        Frequencia_Areas[3] = int(input("Insira o valor de freqûencia da área 4: "))
        Frequencia_Areas[4] = int(input("Insira o valor de freqûencia da área 5: "))
        
        main(mqtt_client)

        time.sleep(5)