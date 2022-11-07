import serial
import time
import signal
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval
import math
from strings import string

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
  
    euler[0] = asin(-2.0*(x*z-y*w)) 
    euler[1] = atan2(2.0*(x*y+z*w),(sqx-sqy-sqz+sqw))
    euler[2] = atan2(2.0*(y*z+x*w),(-sqx-sqy+sqz+sqw)) 

    return euler
    
while 1:
    line = ser.readline()
    words = string.split(line,",")    # Fields split

    if(-1 < words[0].find('*')) :
        data_from=1     # sensor data
        data_index=0
        L_id.text = "ID:"+'*'
        words[0]=words[0].replace('*','')
    else :
        if(-1 < words[0].find('-')) :
            data_from=2  # rf_receiver data
            data_index=1
            L_id.text = "ID:"+words[0]
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
        
            
        axis=(cos(pitch)*cos(yaw),-cos(pitch)*sin(yaw),sin(pitch)) 
        up=(sin(roll)*sin(yaw)+cos(roll)*sin(pitch)*cos(yaw),sin(roll)*cos(yaw)-cos(roll)*sin(pitch)*sin(yaw),-cos(roll)*cos(pitch))
        platform.axis=axis
        platform.up=up
        platform.length=0.6
        platform.width=1

        pitch_stick.rotate( axis=(0,1,0), angle = old_pitch-pitch)
        old_pitch = pitch

        roll_stick.rotate( axis=(-1,0,0), angle = old_roll-roll )
        old_roll = roll

        yaw_stick.rotate( axis=(0,0,1), angle = old_yaw-yaw )
        old_yaw = yaw

        L1.text = "%.2f" %(roll*rad2grad)
        L2.text = "%.2f" %(pitch*rad2grad)
        L3.text = "%.2f" %(yaw*rad2grad)
ser.close
#ani = FuncAnimation(fig , animate, blit=False, frames= 200, interval = 100)
#plt.show()
    

