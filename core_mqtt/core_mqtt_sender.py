import json
from socket import socket

import paho.mqtt.client as mqtt

"""
Este arquivo gerencia a classe de conexão do MQTT Sender.
"""


class MQTTSender:
    """
    Classe gerenciadora do envio de dados do MQTT
    """
    def __init__(self, data: dict):
        self.data = data
        self.mqttBroker = '222.222.222.2'
        self.mqttPort = 1883
        # self.data = {'source':'mobile','device_event':'request','device':'123454','event_name':'power','event_details':'OFF'}
        
    def get_data(self):
        """
        Retorna os dados
        :return:
        """
        return self.data

    def pub_data(self):
        deviceName = self.data['device']
        topic = 'dev/' + str(deviceName)
        json_msg = json.dumps(self.data)
        #msg="mosquitto_pub -t dev/"+str(deviceName)+" -h "+str(self.mqttBroker)+" -m '"+json_msg+"'"
        try:
            pub_client = mqtt.Client(deviceName + "_sub_core", clean_session=True, protocol=mqtt.MQTTv31)
            pub_client.connect(self.mqttBroker, int(self.mqttPort), 5)
            pub_client.publish(topic, json_msg)
        except socket.timeout as e:
            print(e)
