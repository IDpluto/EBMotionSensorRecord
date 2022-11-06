import serial
import time
import signal
import threading
import csv
import time


line = [] #라인 단위로 데이터 가져올 리스트 변수

port = '/dev/ttyUSB0' # 시리얼 포트
baud = 921600 # 시리얼 보드레이트(통신속도)

exitThread = False   # 쓰레드 종료용 변수
fieldnames = ["gyro_x","gyro_y","gyro_z", "acc_x", "acc_y, acc_z"]

#쓰레드 종료용 시그널 함수
def handler(signum, frame):
     exitThread = True


#데이터 처리할 함수
def parsing_data(data):
    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    tmp = ''.join(data)
    tmp = tmp.split(',')
    
    with open('/home/dohlee/crc_project/data/data1','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        info = {
            "gyro_x":tmp[1],
            "gyro_y":tmp[2],
            "gyro_z":tmp[3],
            "acc_x":tmp[4],
            "acc_y":tmp[5],
            "acc_z":tmp[6]
        }
        csv_writer.writerow(info)
        time.sleep(1)

#본 쓰레드
def readThread(ser):
    global line
    global exitThread
    
    with open('/home/dohlee/crc_project/data/data1','w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()
    # 쓰레드 종료될때까지 계속 돌림
    while True:
        #데이터가 있있다면
        for c in ser.read():
            #line 변수에 차곡차곡 추가하여 넣는다.
            line.append(chr(c))

            if c == 10: #라인의 끝을 만나면..
                #데이터 처리 함수로 호출
                parsing_data(line)

                #line 변수 초기화
                del line[:]                

if __name__ == "__main__":
    #종료 시그널 등록
    signal.signal(signal.SIGINT, handler)

    #시리얼 열기
    ser = serial.Serial(port, baud, timeout=0)

    #시리얼 읽을 쓰레드 생성
    thread = threading.Thread(target=readThread, args=(ser,))

    #시작!
    thread.start()