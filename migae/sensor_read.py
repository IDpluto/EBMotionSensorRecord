import serial

port = '/dev/ttyUSB0'
brate = 9600 
cmd = 'temp'

seri = serial.Serial(port, baudrate = brate, timeout = None)
print(seri.name)

seri.write(cmd.encode())

a = 1

while a:
    if seri.in_waiting != 0 :
        content = seri.readline()
        print(content[:-2].decode())
        a = 0
