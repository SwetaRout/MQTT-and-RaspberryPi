Raspberry Pi A

Functions:

1) Connects to broker specified by hostname and subscribes to the lightSensor and threshold topics
2) Uses software SPI connection with the ADC IC  using the following connections:
MCP3008 VDD (pin 16) to Raspberry Pi 3.3V
MCP3008 VREF (pin 15) to Raspberry Pi 3.3V
MCP3008 AGND (pin 14) to Raspberry Pi GND
MCP3008 DGND (pin 9) to Raspberry Pi GND
MCP3008 CLK (pin 13) to Raspberry Pi pin 18
MCP3008 DOUT (pin 12) to Raspberry Pi pin 23
MCP3008 DIN (pin 11) to Raspberry Pi pin 24
MCP3008 CS/SHDN (pin 10) to Raspberry Pi pin 25
3) Samples channels 0 and 1 of the ADC every 10 ms for the values of the potentiometer and LDR, respectively
4) Publishes the initial values from potentiometer and LDR upon first connection, after that it will only publish new values when they change by at least 10 points (~10%)
5) Stores previously published values to compare to new values, and receives them again form the broker when making a new connection after disconnecting
6) Runs a separate thread that watches for user input so that the user can enter "d" to disconnect from the broker
7) Publishes "online" to "Status/RaspberryPiA" when it connects and publishes "offline" upon a graceful disconnect. It also sends a last will message of "offline" in case of an ungraceful disconnect

Running the code:

Install the Adafruit MCP3008 Python library

sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus git
cd ~
git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
cd Adafruit_Python_MCP3008
sudo python setup.py install
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pip
sudo pip install adafruit-mcp3008

To run the code, navigate to the correct folder and use the following command

sudo python raspberryPiA.py