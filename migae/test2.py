import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200)

while True:

	if ser.readable():
		var = ser.readline()
		
		print(val.decode()[:len(val)-1])
