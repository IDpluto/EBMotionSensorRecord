import serial

ser = serial.Serial() # 시리얼을 연결한다.
ser.port = '/dev/ttyUSB0' # 아두이노가 연결된 포트
ser.baudrate = 115200 # baudrate를 지정해줄 수 있다.

# baudrate를 모른다면 연결된 serial을 불러와서 확인할 수 있다.
# print(ser)

ser.timeout = 1 #시리얼에 데이터를 불러올 때 지정하는 딜레이

# 시리얼을 열어준다.
ser.open()

# 데이터를 저장할 공간을 만들어주었다.
data3 = []

# 반복해서 데이터를 출력하기 위해 while 을 만들어주었다.
while True:

  data = ser.readline() # serial에 출력되는 데이터를 읽어준다.
  data2 = data.split(b'\\') # byte 형태로 출력되는 데이터를 \ 로 나눠서 입력받는다. (센서마다 다름)
  data3 = int(data2, 16)  # convert hex to decimal (16진법으로 출력되는 데이터를 10진법으로 바꿔준다)(여긴 안되서 공부중)

  data3.append(data) # 출력된데이터를 data3에 저장한다.

  print(data3) #저장되는 데이터를 확인하고 data3의 크기가 10을 넘어가면 while을 끝낸다.
  if len(data3) > 10:
    break
    
 #ser.close() # serial 사용이 끝나면 닫아줘야 나중에 오류가 생기지 않는다고 한다.
