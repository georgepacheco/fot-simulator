import random

# This shows two examples of simulated sensors which can be used to test
# the TATU protocol on SOFT-IoT or with a standalone MQTT broker
#
# There are samples of real sensors implementations in the src/sensorsExamples
# folder. You can adapt those examples to your needs.


# The name of sensors functions should be exactly the same as in config.json

# temperature in °F
def bodyTemperatureSensor ():
	return random.randint (86, 107)

def environmentTemperatureSensor ():
	return random.randint (0, 40)
	
def bloodGlucoseSensor ():
	return random.randint (0, 500)
	
def heartRateSensor ():
	return random.randint (50, 200)

def humiditySensor():
    return random.randint(10, 70)

def temperatureSensor():
    return random.randint(25, 38)

def soilmoistureSensor():
    return random.randint(0,1023)
	
def solarradiationSensor():
    return random.randint(300, 3000)

def ledActuator(s = None):
	if s==None:
		return bool(random.randint(0, 1))
	else:
		if s:
			print("1")
		else:
			print("0")
		return s
