Raspberry Pi C

Functions:

1) Connects to broker and subscribes to topic "lightSensor" and "threshold".
2) If lightSensor is higher than threshold then it will publish to "LightStatus" the message "TurnOn", otherwise
the message will be "TurnOff".
3) It will not publish a LightStatus message until it has received a valid message for both lightSensor and threshold
4) The LightStatus is updated every 1 second only if the updated value is different than the one stored in the broker.
5) It will publish to Status/RaspberryPiC the message "online" whenever it has successfully connected to broker.
It is also setup to publish "offline" for graceful and ungraceful disconnects (via last-will message)
6) In order to perform a graceful disconnect type "disconnect" into the terminal.

Compiling and running:
sudo python raspberryPiC.py

Broker IP address can be updated on line 8
