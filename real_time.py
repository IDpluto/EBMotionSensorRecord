import serial
import time
import signal
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval

ser = serial.Serial('/dev/ttyUSB0', 921600)
fig, (gx, ax) = plt.subplots(2,1)
max_points = 200

line1, = gx.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2, color='r')
line = [line1, line2]
fig.set_size_inches((10, 5))
fig.subplots_adjust(wspace = 0.9, hspace = 0.9)

def init():
    return line1, line2,

#데이터 처리할 함수
def parsing_data(data):
    
    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    tmp = ''.join(data)
    tmp = tmp.split(',')

    return tmp

def animate(i):
    tmp = ser.readline()
    tmp = tmp.decode("ISO-8859-1")
    tmp = tmp.split(',')
    gyro_x = tmp[1]
    gyro_y = tmp[2]

    line[0].set_data(gyro_x, gyro_x)
    line[1].set_data(gyro_y, gyro_y)
    return line

if __name__ == "__main__":
    
    ani = FuncAnimation(fig , animate, blit=False, frames= 200, interval = 100)
    plt.show()
    

