import paho.mqtt.client as mqtt
import json
import os



 
#Utils functions
def filter_msg(msg):
	dict_msg=json.loads(msg)
	print(json.loads(msg))
	#TODO: Importar libs django e fazer insert no postgreSQL 



#MQTT functions
def on_connect(mqttc, obj, flags, rc):
    topic="#"
    mqttc.subscribe(topic)
    print("Device's sensors:")
    print("Topic device subscribed: " + topic)

def on_message(mqttc, obj, msg):
    print("Topic",msg.topic)
    print("Payload",str(msg.payload))
    filter_msg(str(msg.payload.decode("utf-8")))

def on_disconnect(mqttc, obj, rc):
	print("disconnected!")
	exit()

while True:
    mqttPort=1883
    mqttBroker="192.168.0.132"	
    sub_client = mqtt.Client(clean_session=True, protocol=mqtt.MQTTv31)
    sub_client.on_connect = on_connect
    sub_client.on_message = on_message
    sub_client.on_disconnect = on_disconnect
	
	
	#try:
    sub_client.connect(mqttBroker, int(mqttPort), 60)
    sub_client.loop_forever()
	#except :
		#print ("Broker unreachable on " + mqttBroker + " URL!")
		#sleep(5)
