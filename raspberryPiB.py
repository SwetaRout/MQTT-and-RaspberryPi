import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("LightStatus",2)
    client.subscribe("Status/RaspberryPiA",2)
    client.subscribe("Status/RaspberryPiC",2)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if(msg.topic == "Status/RaspberryPiA"):
	if(str(msg.payload)=='online'):
		GPIO.output(16,True)
	else:
		GPIO.output(16,False)

    if(msg.topic=="Status/RaspberryPiC"):
	if(str(msg.payload)=='online'):
		GPIO.output(18,True)
	else:
		GPIO.output(18,False)

    if(msg.topic=="LightStatus"):
	if(str(msg.payload)=='TurnOn'):
		GPIO.output(12,True)
	elif(str(msg.payload)=='TurnOff'):
		GPIO.output(12,False)
    
     

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

print("Start")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect("74.134.20.230", 1883, 60)
print("connected")
client.loop_forever()
try:
    main()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()