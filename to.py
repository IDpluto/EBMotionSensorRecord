import serial
import serial.tools.list_ports as sp


list = sp.comports()

connected = []

## PC 연결된 COM Port 정보를 list에 넣어 확인한다.


for i in list:

    connected.append(i.device)

print("Connected COM ports: " + str(connected))

 

# ser = serial.Serial("COM5", 9600,timeout=1)

# if ser.readable():

#     res = ser.readline()

#     print(res.decode()[:len(res)-1])


# baudrate 정보와 연결할 COM Port 이름을 입력한다.

select_comport = input('select:')
s_port = input()

ser = serial.Serial(select_comport, s_port, timeout = 1)


# 내가 연결할 Device의 명령어 delimiter가 Carrige return + Line Feed라고 하길래 delimeter를 설정해주었다.


while True:

    print("insert op :", end='')

    op = input()

    delimiter = '\r\n'

    op = op+delimiter

    print(op)

    ser.write(op.encode())

    res = ser.readline()

    res_packet = res.decode()[:len(res)-1]

    print(res_packet)

    print('\n')

    if op is 'q':

        ser.close()
