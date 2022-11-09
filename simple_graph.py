
import serial
import math
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from pandas.core.indexes import interval



def animate(data):
    
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')

    sensor = data['sensor_id']
    xnum = data['x_num']
    roll = data['roll']
    pitch = data['pitch']
    yaw = data['yaw']
    acc_x = data['acc_x']
    acc_y = data['acc_y']
    acc_z = data['acc_z']

    if (sensor.all() == 1):
        try:
            roll1 = roll
            pitch1 = pitch
            yaw1 = yaw
            acc_x1 = acc_x
            acc_y1 = acc_y
            acc_z1 = acc_z
        except:
            print ("false")
    else:
        try:
            roll2 = roll
            pitch2 = pitch
            yaw2 = yaw
            acc_x2 = acc_x
            acc_y2 = acc_y
            acc_z2 = acc_z
        except:
            print ("false")

    line[0].set_data(xnum, roll1)
    line[1].set_data(xnum, pitch1)
    line[2].set_data(xnum, yaw1)
    line[3].set_data(xnum, acc_x1)
    line[4].set_data(xnum, acc_y1)
    line[5].set_data(xnum, acc_z1)
    line[6].set_data(xnum, roll2)
    line[7].set_data(xnum, pitch2)
    line[8].set_data(xnum, yaw2)
    line[9].set_data(xnum, acc_x2)
    line[10].set_data(xnum, acc_y2)
    line[11].set_data(xnum, acc_z2)

    return line,




if __name__ == '__main__':
    
    grad2rad = 3.141592/180.0
    rad2grad = 180.0/3.141592
    cos = math.cos
    ser = serial.Serial('/dev/ttyUSB0', 921600)
    fig, (ax1, ax2 , ax3, ax4) = plt.subplots(4,1)
    l_roll1, = ax1.plot([], [], lw=2, color = 'red')
    l_pitch1, = ax1.plot([], [], lw=2, color = 'blue')
    l_yaw1, = ax1.plot([], [], lw=2, color = 'orange')
    l_acc_x1, = ax2.plot([], [], lw=2, color = 'red')
    l_acc_y1, = ax2.plot([], [], lw=2, color = 'blue')
    l_acc_z1, = ax2.plot([], [], lw=2, color = 'orange')
    l_roll2, = ax3.plot([], [], lw=2, color = 'red')
    l_pitch2, = ax3.plot([], [], lw=2, color = 'blue')
    l_yaw2, = ax3.plot([], [], lw=2, color = 'orange')
    l_acc_x2, = ax4.plot([], [], lw=2, color = 'red')
    l_acc_y2, = ax4.plot([], [], lw=2, color = 'blue')
    l_acc_z2, = ax4.plot([], [], lw=2, color = 'orange')

    line = [l_roll1, l_pitch1, l_yaw1, l_acc_x1, l_acc_y1, l_acc_z1, l_roll2, l_pitch2, l_yaw2, l_acc_x2, l_acc_y2, l_acc_z2] 
    
    ax1.set_ylim(-300, 300)
    ax1.grid()
    ax2.set_ylim(-3, 3)
    ax2.grid()
    ax3.set_ylim(-300, 300)
    ax3.grid()
    ax4.set_ylim(-3, 3)
    ax4.grid()

    ani = animation.FuncAnimation(fig, animate, frames = 200, blit=False, interval=10,
        repeat=False)
    plt.show()

    
 

