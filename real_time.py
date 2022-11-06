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

def animate(i):
    tmp = ser.readline()
    tmp = tmp.decode("ISO-8859-1")
    tmp = tmp.split(',')
    gyro_x = tmp[1]
    gyro_y = tmp[2]
    #gx.clear()
    #ax.clear()
    plt.cla()
    plt.plot(gyro_x, label='블로그')
    plt.plot(gyro_y,label='유튜브')
    
    plt.legend(loc = 'upper left')
    plt.tight_layout()
 
ani = FuncAnimation(plt.gcf(),animate, interval = 1000)
 
plt.tight_layout()
plt.show()
    

