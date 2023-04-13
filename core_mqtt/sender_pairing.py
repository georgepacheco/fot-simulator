import json
from socket import socket

import paho.mqtt.client as mqtt
from multiprocessing import Process
from threading import Thread
import sys
import time
"""
Este arquivo gerencia a classe de conexão do MQTT Sender.
"""

pairing=[]
max_device=0
class CustomTh(Thread):
    def __init__(self, data):
        # execute the base constructor
        self.data = data
        Thread.__init__(self)
        self.mqtt_broker = '10.0.0.2'
        self.mqtt_port = 1883
        self.sub_client = mqtt.Client(clean_session=True, protocol=mqtt.MQTTv31)
        self.keepalive = 60
        self.topic = "houses/" + str(self.data['house'])
        self.sub_client.on_connect = self.on_connect
        self.sub_client.on_message = self.on_message
        self.sub_client.on_disconnect = self.on_disconnect
        
    def run(self):
        print(self.data)
        self.sub_client.connect(
            host=self.mqtt_broker, port=int(self.mqtt_port), keepalive=self.keepalive
        )
        self.sub_client.loop_forever()
        print("Exit...")
        
    # ############################################################################################### #
        # Metodos MQQT sobrepostos ###################################################################### #
        # ############################################################################################### #
    def on_connect(self, mqttc, obj, flags, rc) -> None:
        """
        Metodo que sobrepoe o padrão do MQTT.
        Ao iniciar a conexão, este metodo é executado.
        :param mqttc:
        :param obj:
        :param flags:
        :param rc:
        """
        mqttc.subscribe(self.topic)
        

    def on_message(self, mqttc, obj, msg) -> None:
        global max_device
        """
        Metodo que sobrepoe o padrão do MQTT.
        Recebe os dados e status da conexão.e
        :param mqttc:
        :param obj:
        :param msg:
        """
        
        m=str(msg.payload.decode("utf-8"))
        json_m=json.loads(m)
        if('sensors_house' in json_m):
            max_device=int(json_m['sensors_house'])
            self.filter_msg(json_m)

    def filter_msg(self,msg):
        global pairing,max_device
        pairing.append(msg)
        if(len(pairing)==max_device):
            sys.exit()
    
    def on_disconnect(self, mqttc, obj, rc) -> None:
        """
        Metodo que sobrepoe o padrão do MQTT.
        Finaliza a conexão.
        :param mqttc:
        :param obj:
        :param rc:
        """
        print(str(mqttc))
        print(str(obj))
        print(str(rc))
        print("disconnected!")
        # sys.exit()


class MQTTSender:
    """
    Classe gerenciadora do envio de dados do MQTT
    """

    def __init__(self, data: dict, connection_type: str):
        self.data = data
        self.mqtt_broker = '10.0.0.2'
        self.mqtt_port = 1883
        self.connection_type = connection_type
        self.sub_client = mqtt.Client(clean_session=True, protocol=mqtt.MQTTv31)
        self.keepalive = 60
        self.topic = "houses/" + str(self.data['house'])

    def get_data(self):
        """
        Retorna os dados
        :return:
        """
        return self.data

    def get_pairing(self):
        """
        Retorna os dados
        :return:
        """
        return self.pairing

    def pub_data(self):
        if self.connection_type == "recommendation":
            deviceName = self.data['device']
            topic = 'dev/' + str(deviceName)
            json_msg = json.dumps(self.data)
            try:
                pub_client = mqtt.Client(deviceName + "_sub_core", clean_session=True, protocol=mqtt.MQTTv31)
                pub_client.connect(self.mqtt_broker, int(self.mqtt_port), 5)
                pub_client.publish(topic, json_msg)
            except socket.timeout as e:
                print(e)

    def pairing_device(self):
        if self.connection_type == "pairing":
            house = self.data['house']
            topic = 'houses/' + str(house)
            json_msg = json.dumps(self.data)
            try:
                
                pub_client = mqtt.Client(house + "_sub_core", clean_session=True, protocol=mqtt.MQTTv31)
                pub_client.connect(self.mqtt_broker, int(self.mqtt_port), 5)
                pub_client.publish(topic, json_msg)
            except socket.timeout as e:
                print(e)

    def observer_house(self):
        t = CustomTh(self.data)
        t.daemon=True
        t.start()


    def pairing_device_resp(self):
        global pairing, max_device
        if (len(pairing)==max_device):
            print("Resp receiver:",len(pairing),"Max device:",max_device)
            print("Resp to mobile:",pairing)
            return False
        else:
            return True    


sender = MQTTSender({"house":"AAAAA11111","source":"mobile","device_event":"request","event_name":"status"},"pairing")
sender.observer_house()
time.sleep(0.2)
sender.pairing_device()
#Ou configura para o core informar a qtd de devices ou precisa esperar pelo menos uma resposta para saber a quantidade de sensores no Mininet (ativos e inativos)
time.sleep(3)
while sender.pairing_device_resp():
    continue
    #time.sleep(0.1)















