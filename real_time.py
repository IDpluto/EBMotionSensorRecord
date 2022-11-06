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
fig.set_size_inches((10, 5))
fig.subplots_adjust(wspace = 0.9, hspace = 0.9)
line1, = gx.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2, color='r')
line = [line1, line2]


def init():
    return line1, line2,

def read_data():
    for c in ser.read():
        #line 변수에 차곡차곡 추가하여 넣는다.
        line.append(chr(c))

        if c == 10: #라인의 끝을 만나면..
            tmp = ''.join(line)
            tmp = tmp.split(',')
            #line 변수 초기화
            del line[:] 
            return tmp

def animate(i):
       
    #gx.clear()
    #ax.clear()
    tmp = read_data()
    print(tmp[1])
    gx.plot(tmp[1], lw=2, color='r')
    ax.plot(tmp[2], lw=2, color='r')
    #line[0].set_data(gyro_x)
    #line[1].set_data(gyro_y)
    

ani = FuncAnimation(fig , animate, blit=False, frames= 200, interval = 100)
plt.show()
    

