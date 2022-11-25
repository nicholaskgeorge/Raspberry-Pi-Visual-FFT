import serial
from time import sleep

#ser1 = serial.Serial('/dev/ttyUSB0', 115200);
ser2 = serial.Serial('/dev/ttyACM0', 115200);
sleep(1)

while(True):
	data = (ser2.readline())
	print(data)
	ser2.write([1,2,3])
	#print(int(data)-int(data))
