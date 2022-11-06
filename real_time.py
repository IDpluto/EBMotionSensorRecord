import serial
import time
import signal
import threading
import csv
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval

fig, (gx, ax) = plt.subplots(2,1)
fig.set_size_inches((10, 5))
fig.subplots_adjust(wspace = 0.9, hspace = 0.9)

line = [] #라인 단위로 데이터 가져올 리스트 변수
port = '/dev/ttyUSB0' # 시리얼 포트
baud = 921600 # 시리얼 보드레이트(통신속도)

#데이터 처리할 함수
def parsing_data(data):
    
    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    tmp = ''.join(data)
    tmp = tmp.split(',')

    return tmp

def animate(i):
    tmp = read_data()
    gx.plot(tmp[1], lw =2, color = 'r')
    gx.plot(tmp[2], lw =2, color = 'y') 
    gx.plot(tmp[3], lw =2, color = 'g') 
    ax.plot(tmp[4], lw =2, color = 'r') 
    ax.plot(tmp[5], lw =2, color = 'y') 
    ax.plot(tmp[6], lw =2, color = 'g')


def read_data():
    global line
    # 쓰레드 종료될때까지 계속 돌림
    for c in ser.read():
        #line 변수에 차곡차곡 추가하여 넣는다.
        line.append(chr(c))

        if c == 10: #라인의 끝을 만나면..
               
            tmp = parsing_data(line)
            del line[:]
            return tmp


            

if __name__ == "__main__":
    ser = serial.Serial(port, baud)
    ani = FuncAnimation(fig , animate, blit=False, frames= 200, interval = 100)
    plt.show()
    

