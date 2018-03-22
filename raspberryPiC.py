mport paho.mqtt.client as mqtt
import time, threading

lightSensorTopic = "lightSensor"
thresholdTopic = "threshold"
statusTopic = "Status/RaspberryPiC"
lightStatusTopic = "LightStatus"
brokerIp = "192.168.86.77" #LAN

invalidVal = 8888
lightSensorVal = invalidVal
thresholdVal = invalidVal
lightStatus = "invalidString"

def turnOnLight():
   if lightStatus != "TurnOn":
      client.publish(lightStatusTopic, payload="TurnOn", qos=2, retain=True)

def turnOffLight():
   if lightStatus != "TurnOff":
      client.publish(lightStatusTopic, payload="TurnOff", qos=2, retain=True)

def lightStatusUpdate():
   if lightSensorVal != invalidVal:
      if thresholdVal != invalidVal:
         if lightSensorVal >= thresholdVal:
            turnOnLight()
         else:
            turnOffLight()

   t = threading.Timer(1, lightStatusUpdate)
   t.daemon = True
   t.start()

#Callback when  CONNACK is received from broker
def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))
   client.publish(statusTopic, payload="online", qos=2, retain=True)
   #Subscribe in on_connect() means renewed subscriptions on connection recovery
   client.subscribe(lightStatusTopic, 2)
   client.subscribe(lightSensorTopic, 2)
   client.subscribe(thresholdTopic, 2)

#Callback for when a PUBLISH message is received from broker.
def on_message(client, userdata, msg):
   global lightSensorVal
   global thresholdVal
   global lightStatus

   if msg.topic == lightSensorTopic:
      lightSensorVal = float(msg.payload)
   elif msg.topic == thresholdTopic:
      thresholdVal = int(msg.payload)
   elif msg.topic == lightStatusTopic:
      lightStatus = str(msg.payload)

client = mqtt.Client(client_id="1", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message
client.will_set(statusTopic, payload="offline", qos=2, retain=True)

client.connect(brokerIp, 1883, 60)

client.loop_start()

lightStatusUpdate()


while True:
   usrCmd = raw_input("")
   if usrCmd == "disconnect":
      print("Disconnected")
      client.publish(statusTopic, payload="offline", qos=2, retain=True)
      client.loop_stop()
      client.disconnect()
      break
