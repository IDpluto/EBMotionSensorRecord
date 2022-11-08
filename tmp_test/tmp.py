import serial
import chardet
import struct
from time import sleep

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


ser = serial.Serial ("/dev/ttyUSB0", 921600)    #Open port with baud rate
while True:
    data = ser.readline()
    #sleep(0.03)
    #a_left = ser.inWaiting()
    #data += ser.read(a_left)
    a = ','
    received_data = data.decode("ISO-8859-1") # .encode("utf-8")
    #received_byte = int.from_bytes(received_data, "big")
    # struct.unpack('f',received_data)
    #received_decode = str(data, 'utf-8')
    print((received_data))
    #received_data = chardet.detect(data)
    #received_decode = received_data.dict(received_data["encoding"])
    #sleep(0.03)
    #data_left = ser.inWaiting()             #check for remaining byte
    #received_data += ser.read(data_left)
    #print (received_byte)
    #ser.write(received_data)
