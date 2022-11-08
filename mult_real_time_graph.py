
import serial
import math
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from pandas.core.indexes import interval






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





def data_gen():
    #i = 0
        counter = itertools.count()
    #while 1:
        line = ser.readline()
        line = line.decode("ISO-8859-1")
        words = line.split(",")    # Fields split
    
        if(-1 < words[0].find('*')) :
            data_from=1     # sensor data
            data_index=0
            text = "ID:"+'*'
            words[0]=words[0].replace('*','')
            #print ("first:", text)
        else :
            if(-1 < words[0].find('-')) :
                data_from=2  # rf_receiver data
                data_index=1
                text = "ID:"+words[0]
                #print ("seconds:",text)
            else :
                data_from=0  # unknown format
        if(data_from!=0):
            commoma = words[data_index].find('.') 
            if(len(words[data_index][commoma:-1])==4): # �Ҽ��� 4�ڸ� �Ǻ�
                data_format = 2  # quaternion
            else:
                data_format = 1 # euler


        if(data_format==1): #euler
            try:
                roll = float(words[data_index])*grad2rad
                pitch = float(words[data_index+1])*grad2rad
                yaw = float(words[data_index+2])*grad2rad
                acc_x = float(words[data_index+3])
                acc_y = float(words[data_index+4])
                acc_z = float(words[data_index+5])
                #print(roll)
            except:
                print (".")
        else: #(data_format==2)quaternion
            try:
                q0 = float(words[data_index])
                q1 = float(words[data_index+1])
                q2 = float(words[data_index+2])
                q3 = float(words[data_index+3])
                acc_x = float(words[data_index+4])
                acc_y = float(words[data_index+5])
                acc_z = float(words[data_index+6])
                Euler = quat_to_euler(q0,q1,q2,q3)

                roll  = Euler[1]
                pitch = Euler[0]
                yaw   = Euler[2]
            except:
                print (".")
        t = next(counter)
        roll_r = "%.2f" %(roll*rad2grad)
        pitch_r = "%.2f" %(pitch*rad2grad)
        yaw_r = "%.2f" %(yaw*rad2grad)
    

        yield t, roll_r, pitch_r, yaw_r, acc_x, acc_y, acc_z





def animate(data):
    x_num, roll, pitch, yaw, acc_x, acc_y, acc_z = data
    xdata.append(x_num)
    r_data.append(roll)
    p_data.append(pitch)
    z_data.append(yaw)
    ax_data.append(acc_x)
    ay_data.append(acc_y)
    az_data.append(acc_z)
    line[0].set_data(xdata, r_data)
    line[1].set_data(xdata, p_data)
    line[2].set_data(xdata, z_data)
    line[3].set_data(xdata, ax_data)
    line[4].set_data(xdata, ay_data)
    line[5].set_data(xdata, az_data)

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

    ani = animation.FuncAnimation(fig, animate, frames = data_gen, blit=False, interval=10)
    plt.show()

    
 

