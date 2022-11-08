
import serial
import math
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from pandas.core.indexes import interval


def data_gen():
    #i = 0
    counter = itertools.count()
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    
    xnum = data['x_num'].astype(int)
    roll = data['roll'].astype(float)
    pitch = data['pitch'].astype(float)
    yaw = data['yaw'].astype(float)
    acc_x = data['acc_x'].astype(float)
    acc_y = data['acc_y'].astype(float)
    acc_z = data['acc_z'].astype(float)
    

    yield xnum, roll, pitch, yaw, acc_x, acc_y, acc_z





def animate(data):
    x_num, roll, pitch, yaw, acc_x, acc_y, acc_z = data
    #xdata.append(x_num)
    #r_data.append(roll)
    #p_data.append(pitch)
    #z_data.append(yaw)
    #ax_data.append(acc_x)
    #ay_data.append(acc_y)
    #az_data.append(acc_z)
    line[0].set_data(x_num, roll)
    line[1].set_data(x_num, pitch)
    line[2].set_data(x_num, yaw)
    line[3].set_data(x_num, acc_x)
    line[4].set_data(x_num, acc_y)
    line[5].set_data(x_num, acc_z)
    
   

    return line,

if __name__ == '__main__':
    
    grad2rad = 3.141592/180.0
    rad2grad = 180.0/3.141592
    cos = math.cos
    ser = serial.Serial('/dev/ttyUSB0', 921600)
    fig, (ax1, ax2) = plt.subplots(2,1) #, ax3, ax4) = plt.subplots(4,1)
    
    roll_line1, = ax1.plot([],[], lw=2, color = 'red')
    pitch_line1, = ax1.plot([], [], lw = 2, color = 'blue')
    yaw_line1, = ax1.plot([], [], lw = 2, color = 'orange')
    acx_line1, = ax2.plot([], [], lw = 2, color = 'red')
    acy_line1, = ax2.plot([], [], lw = 2, color = 'blue')
    acz_line1, = ax2.plot([], [], lw = 2, color = 'orange')
    #roll_line2, = ax3.plot([], [], lw = 2, color = 'red')
    #pitch_line2, = ax3.plot([], [], lw = 2, color = 'blue')
    #yaw_line2, = ax3.plot([], [], lw = 2, color = 'orange')
    #acx_line2, = ax4.plot([], [], lw = 2, color = 'red')
    #acy_line2, = ax4.plot([], [], lw = 2, color = 'blue')
    #acz_line2, = ax4.plot([], [], lw = 2, color = 'orange')
    line = [roll_line1, pitch_line1, yaw_line1, acx_line1, acy_line1, acz_line1]#, roll_line2, pitch_line2, yaw_line2, acx_line2, acy_line2, acz_line2]   
    
    ax1.set_ylim(-300, 300)
    ax1.grid()
    ax2.set_ylim(0, 3)
    ax2.grid()

    xdata, r_data, p_data, z_data, ax_data, ay_data, az_data = [], [], [], [], [], [], []

    ani = animation.FuncAnimation(fig, animate, frames = data_gen, blit=False, interval=10,
        repeat=False)
    plt.show()

    
 

