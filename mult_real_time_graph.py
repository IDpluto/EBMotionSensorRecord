
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
    
    
    xnum = data['x_num']
    roll1 = data['hand_roll']
    pitch1 = data['hand_pitch']
    yaw1 = data['hand_yaw']
    acc_x1 = data['hand_acc_x']
    acc_y1 = data['hand_acc_y']
    acc_z1 = data['hand_acc_z']
    roll2 = data['head_roll']
    pitch2 = data['head_pitch']
    yaw2 = data['head_yaw']
    acc_x2 = data['head_acc_x']
    acc_y2 = data['head_acc_y']
    acc_z2 = data['head_acc_z']
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax1.plot(xnum, roll1, lw=2, color = 'red')
    ax1.plot(xnum, pitch1, lw=2, color = 'blue')
    ax1.plot(xnum, yaw1, lw=2, color = 'orange')
    ax2.plot(xnum, acc_x1, lw=2, color = 'red')
    ax2.plot(xnum, acc_y1, lw=2, color = 'blue')
    ax2.plot(xnum, acc_z1, lw=2, color = 'orange')
    ax3.plot(xnum, roll2, lw=2, color = 'red')
    ax3.plot(xnum, pitch2, lw=2, color = 'blue')
    ax3.plot(xnum, yaw2, lw=2, color = 'orange')
    ax4.plot(xnum, acc_x2, lw=2, color = 'red')
    ax4.plot(xnum, acc_y2, lw=2, color = 'blue')
    ax4.plot(xnum, acc_z2, lw=2, color = 'orange')




    

if __name__ == '__main__':
    
    grad2rad = 3.141592/180.0
    rad2grad = 180.0/3.141592
    cos = math.cos
    ser = serial.Serial('/dev/ttyUSB0', 921600)
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1)
    
    ax1.set_ylim(-300, 300)
    ax1.grid()
    ax2.set_ylim(-3, 3)
    ax2.grid()
    ax3.set_ylim(-300, 300)
    ax3.grid()
    ax4.set_ylim(-3, 3)
    ax4.grid()

    #xdata, r_data, p_data, z_data, ax_data, ay_data, az_data = [], [], [], [], [], [], []

    ani = animation.FuncAnimation(plt.gcf(), animate, frames = 200, blit=False, interval=10,
        repeat=False)
    plt.show()

    
 

