import logging

import json
from socket import socket

import paho.mqtt.client as mqtt
from threading import Thread
import sys

from django.conf import settings

"""
Este arquivo gerencia a classe de conexão do MQTT Sender.
"""

log = logging.getLogger(__name__)
pairing = []
max_device=0
houses_l =[]

class StatusTh(Thread):
    def __init__(self, data):
        # execute the base constructor
        self.data = data
        Thread.__init__(self)
        self.mqtt_broker = str(getattr(settings, "MQTT_SENDER_URL"))
        self.mqtt_port = int(getattr(settings, "MQTT_SENDER_PORT"))
        self.sub_client = mqtt.Client(clean_session=True, protocol=mqtt.MQTTv31)
        self.keepalive = 60
        self.topic = "houses/" + str(self.data['house'])
        self.sub_client.on_connect = self.on_connect
        self.sub_client.on_message = self.on_message
        self.sub_client.on_disconnect = self.on_disconnect

    def run(self):
        #print(self.data)
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
        # print("Topic device subscribed: " + self.topic)

    def on_message(self, mqttc, obj, msg) -> None:
        global max_device
        """
        Metodo que sobrepoe o padrão do MQTT.
        Recebe os dados e status da conexão.e
        :param mqttc:
        :param obj:
        :param msg:
        """

        m = str(msg.payload.decode("utf-8"))
        json_m = json.loads(m)
        if ('sensors_house' in json_m):
            self.filter_msg(json_m)
    
    def name_contains(self,msg):
        for i in range(0,len(pairing)):
            if('device' in msg and pairing[i]['device']==msg['device']):
                return True
        return False
    
    def filter_msg(self, msg):
        global pairing, max_device
        if(self.name_contains(msg)==False):
            msg['house']=self.data['house']
            pairing.append(msg)


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


class MQTTSenderPairing:
    """
    Classe gerenciadora do envio de dados do MQTT
    """

    def __init__(self, data: dict, connection_type: str):
        self.data = data
        self.mqtt_broker = str(getattr(settings, "MQTT_SENDER_URL"))
        self.mqtt_port = int(getattr(settings, "MQTT_SENDER_PORT"))
        self.connection_type = connection_type
        self.sub_client = mqtt.Client(clean_session=True, protocol=mqtt.MQTTv31)
        self.keepalive = 60
        self.topic = "houses/" + str(self.data['house'])

    def get_pairing(self):
        """
        Retorna os dados
        :return:
        """
        p_return=[]
        for p in pairing:
            if(p['house']==self.data['house']):
                p_return.append(p)

        return p_return
    
       
    def contains_house(self):
        for h in houses_l:
            if('house' in self.data and self.data['house']==h['house']):
                return True
        return False
                

    def pairing_device(self):
        if self.connection_type == "status":
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
        global houses_l, pairing
        pairing=[]
        if(self.contains_house()==False):
            print('Criando Th para...',self.data['house'])
            houses_l.append(self.data)
            t = StatusTh(self.data)
            t.daemon=True
            t.start()
    def set_pairing_device(self):
        if self.connection_type == "pairing":
        #'{"house": "B","device": "officeLight-B","source": "mobile","device_event":"request","event_details":"pairing_on"}'
            house = self.data['house']
            topic = 'houses/' + str(house)
            json_msg = json.dumps(self.data)
            try:
                pub_client = mqtt.Client(self.data['device'] + "_sub_core", clean_session=True, protocol=mqtt.MQTTv31)
                pub_client.connect(self.mqtt_broker, int(self.mqtt_port), 5)
                pub_client.publish(topic, json_msg)
            except socket.timeout as e:
                print(e)

    def pairing_device_resp(self):
        global pairing, max_device
        if len(pairing) == max_device:
            print("Resp receiver:",len(pairing),"Max device:",max_device)
            print("Resp to mobile:",pairing)
            # nesta linha envia a resposta do GET
            return False
        else:
            return True
