import threading
import time
import paho.mqtt.client as mqtt
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

hostname = "74.134.20.230"
#hostname = "192.168.0.7"
ldr = 1
pot = 0
values = [-50]*2
pub_values = [-50]*2
user_input = 0

#Thread for looking for user input
def take_input():
    global user_input
    while True:
	user_input = raw_input("")
	if user_input == "d":
	    exit()
    return

#Callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " +str(rc))
    print("Flags = " +str(flags))
    client.publish("Status/RaspberryPiA", payload =  "online", qos = 2, retain = True)
    #Subscribe in on_connect to renew upon reconnect
    client.subscribe("lightSensor", 2)
    client.subscribe("threshold", 2)
    if flags['session present'] != 1:
	pub_values[pot] = mcp.read_adc(pot)
	pub_values[ldr] = mcp.read_adc(ldr)

#Callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "lightSensor" and pub_values[ldr] == -50:
	pub_values[ldr] = float(msg.payload)
    elif msg.topic == "threshold" and  pub_values[pot] == -50:
	pub_values[pot] = int(msg.payload)

client = mqtt.Client(client_id = "A", clean_session = False)
client.on_connect = on_connect
client.on_message = on_message
client.will_set("Status/RaspberryPiA", payload = "offline", qos = 2, retain = True)

client.connect(hostname, 1883, 60)
client.loop_start()

print('Type d to disconnect from broker')
thread = threading.Thread(target = take_input)
thread.start()

# Main program loop.
while True:
    if user_input == "d":
	print("Disconnected")
	client.publish("Status/RaspberryPiA", payload = "offline", qos = 2, retain = True)
	client.loop_stop()
	client.disconnect()
	break
    else:
	# The read_adc function will get the value of the specified channel.
	values[pot] = mcp.read_adc(pot)
	values[ldr] = mcp.read_adc(ldr)
	#Normalize light sensor value and threshold value to about 0-100.
	values[pot] = int(values[pot]/10)
	values[ldr] = values[ldr]-900
#	print("Threshold = "+str(values[pot])+", LDR = "+str(values[ldr]))
	# Publish the ADC values.
#	print("before comparison")
	if (values[pot]-pub_values[pot]>=10 or pub_values[pot]-values[pot]>=10) and pub_values[pot] != -50:
	    pub_values[pot] = values[pot]
	    client.publish("threshold", payload = pub_values[pot] , qos = 2, retain = True)
	if (values[ldr]-pub_values[ldr]>=10 or pub_values[ldr]-values[ldr]>=10) and pub_values[ldr] != -50:
	    pub_values[ldr] = values[ldr]
	    client.publish("lightSensor", payload = pub_values[ldr] , qos = 2, retain = True)
	# Pause for half a second.
	time.sleep(0.09)
