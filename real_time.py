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
    gx.plot(gyro_x, lw=2)
    ax.plot(gyro_y, lw=2, color='r')
    #line[0].set_data(gyro_x)
    #line[1].set_data(gyro_y)
    

ani = FuncAnimation(fig , animate, blit=False, frames= 200, interval = 100)
plt.show()
    

