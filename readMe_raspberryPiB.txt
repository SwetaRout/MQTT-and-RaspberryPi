Raspberry Pi B

Functions : 

1) connects to the broker and subscribes to the topic "LightStatus", "Status/RaspberryPiA ", and "Status/RaspberryPiC". 
2) Has 3 LEDs
	(i) LED 1 :  shows the LightStatus (TurnOn/TurnOff)
	(ii)LED 2 :  shows the status of RaspberryPiA (Online/Offline)
	(iii)LED 3:  shows the status of RaspberryPiC (Online/Offline)
	
How to compile ?

Copy the file raspberryPiB.py to the raspberry pi. Then on the raspberry pi terminal run the following command

sudo python raspberryPiB.py

Note :
The broker should be running and publishing messages for the raspberry pi to receive messages.
If you need to change the host ip of the broker, then open the file raspberryPiB.py and change the ip in line no. 46

client.connect("74.134.20.230", 1883, 60) 

Change 74.134.20.230 to the ip address of your broker