import serial
import math
import string
import time
import signal
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval


grad2rad = 3.141592/180.0
rad2grad = 180.0/3.141592
cos = math.cos

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
    gyro_x = float(tmp[1])
    gyro_y = float(tmp[2])
    #gx.clear()
    #ax.clear()
    gx.plot(gyro_x, lw=2, color='r')
    ax.plot(gyro_y, lw=2, color='r')
    #line[0].set_data(gyro_x)
    #line[1].set_data(gyro_y)
    return line

def quat_to_euler(x,y,z,w):
    euler = [0.0,0.0,0.0]
    
    sqx=x*x
    sqy=y*y
    sqz=z*z
    sqw=w*w
  
    euler[0] = math.asin(-2.0*(x*z-y*w)) 
    euler[1] = math.atan2(2.0*(x*y+z*w),(sqx-sqy-sqz+sqw))
    euler[2] = math.atan2(2.0*(y*z+x*w),(-sqx-sqy+sqz+sqw)) 

    return euler
    
while 1:
    line = ser.readline()
    line = line.decode("ISO-8859-1")
    words = line.split(",")    # Fields split
    
    if(-1 < words[0].find('*')) :
        data_from=1     # sensor data
        data_index=0
        text = "ID:"+'*'
        words[0]=words[0].replace('*','')
    else :
        if(-1 < words[0].find('-')) :
            data_from=2  # rf_receiver data
            data_index=1
            text = "ID:"+words[0]
        else :
            data_from=0  # unknown format


    if(data_from!=0):
        commoma = words[data_index].find('.') 
        if(len(words[data_index][commoma:-1])==4): # �Ҽ��� 4�ڸ� �Ǻ�
            data_format = 2  # quaternion
        else :
            data_format = 1 # euler


        if(data_format==1): #euler
            try:
                roll = float(words[data_index])*grad2rad
                pitch = float(words[data_index+1])*grad2rad
                yaw = float(words[data_index+2])*grad2rad
                print(roll)
            except:
                print (".")
        else: #(data_format==2)quaternion
            try:
                q0 = float(words[data_index])
                q1 = float(words[data_index+1])
                q2 = float(words[data_index+2])
                q3 = float(words[data_index+3])
                Euler = quat_to_euler(q0,q1,q2,q3)

                roll  = Euler[1]
                pitch = Euler[0]
                yaw   = Euler[2]
            except:
                print (".")

ser.close
#ani = FuncAnimation(fig , animate, blit=False, frames= 200, interval = 100)
#plt.show()
    

