Laptop 2

Function :
1)  subscribed to all these topics: "lightSensor", threshold", "LightStatus", "Status/RaspberryPiA ", and "Status/RaspberryPiC " and displays the messages sent by the broker on these topics along with the timestamps.
2)  keeps track when the LED1 is turned on and off

How to run :

1) To implement the first function, open a command window and subscribe to the topics required. To do this first go to the path where mosquitto is installed on your computer
	cd C:\Program Files (x86)\mosquitto
   Then run the mosquitto_sub command for the desired host (ip of the broker) and required topics as follows :
	mosquitto_sub -h 74.134.20.230 -p 1883 -v -t # -q 2| xargs -d '\n' -L1 bash -c 'date "+%Y-%m-%d %T.%3N $0"' >log_broker.txt
   This command will save all logs in the file C:\Program Files (x86)\mosquitto\log_broker.txt along with time stamps.

2) To implement the second function, open another command window and subscribe to the topic 'LightStatus' to keep track of LED1 status.To do this go to the path where mosquitto is installed on your computer
	cd C:\Program Files (x86)\mosquitto
   Then run the mosquitto_sub command for the desired host (ip of the broker) and required topics as follows :
	mosquitto_sub -h 74.134.20.230 -p 1883 -v -t LightStatus -q 2| xargs -d '\n' -L1 bash -c 'date "+%Y-%m-%d %T.%3N $0"' >log_light_stautus.txt
   This command will save all logs related to LED 1 in the file C:\Program Files (x86)\mosquitto\log_light_stautus along with time stamps.


Note:

host IP(broker) : 74.134.20.230
port No. : 1883
Date format for time stamp : yyyy-mm-dd hh:min:sec 
Log format : <time stamp> <topic> <value or topic status>

All the commands are saved in laptop2.txt
