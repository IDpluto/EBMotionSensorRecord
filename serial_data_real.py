import serial
import math
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from scipy import stats
import random, time, spidev


grad2rad = 3.141592/180.0
rad2grad = 180.0/3.141592
cos = math.cos


ser = serial.Serial('/dev/ttyUSB0', 115200)

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

def x_read():
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')

    x_count = data['x_num'][1]
    return x_count

def roll_ReadChannel():
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')

    
    roll1 = data['roll'][1]
    return roll1
def pitch_ReadChannel():
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    pitch1 = data['pitch'][1]
    return (pitch1)
        
def yaw_ReadChannel():
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    yaw1 = data['yaw'][1]
    return (yaw1)

def ax_ReadChannel():
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    acc_x1 = data['acc_x'][1]
    return (acc_x1)

def ay_ReadChannel():
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    acc_y1 = data['acc_y'][1]
    return (acc_y1)

def az_ReadChannel():
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    acc_z1 = data['acc_z'][1]
    return (acc_z1)

fig = plt.figure()    
ax = plt.subplot(211, xlim=(0, 5), ylim=(-500, 500))
ax_2 = plt.subplot(212, xlim=(0, 5), ylim=(-3, 3))

max_points = 5000
max_points_2 = 5000

line, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)
line_2, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='green',ms=1)
line_3, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='red',ms=1)
line_4, = ax_2.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1,ms=1, c = 'blue')
line_5, = ax_2.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1,ms=1, c = 'green')
line_6, = ax_2.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1,ms=1, c = 'red')

def animate(i):
    #x = x_read()
    #old_x = line.get_xdata()
    #new_x = np.r_[old_x[1:], x]
    #line.set_xdata(new_x)
    y = roll_ReadChannel()
    # y = random.randint(0,1000)
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)
    
    #print(new_y)
    return line
    
def animate_2(i):
    #x_2 = x_read()
    #old_x_2 = line_2.get_xdata()
    #new_x_2 = np.r_[old_x_2[1:], x_2]
    #line_2.set_xdata(new_x_2)
    y_2 = pitch_ReadChannel()
    old_y_2 = line_2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
    line_2.set_ydata(new_y_2)
    #print(new_y_2)
    return line_2

def animate_3(i):
    #x_3 = x_read()
    #old_x_3 = line_3.get_xdata()
    #new_x_3 = np.r_[old_x_3[1:], x_3]
    #line_3.set_xdata(new_x_3)
    y_3 = yaw_ReadChannel()
    old_y_3= line_3.get_ydata()
    new_y_3 = np.r_[old_y_3[1:], y_3]
    line_3.set_ydata(new_y_3)
    #print(new_y_3)
    return line_3
def animate_4(i):
    #x_4 = x_read()
    #old_x_4 = line_4.get_xdata()
    #new_x_4 = np.r_[old_x_4[1:], x_4]
    #line_4.set_xdata(new_x_4)
    y_4 = ax_ReadChannel()
    old_y_4= line_4.get_ydata()
    new_y_4 = np.r_[old_y_4[1:], y_4]
    line_4.set_ydata(new_y_4)
    #print(new_y_3)
    return line_4

def animate_5(i):
    #x_5 = x_read()
    #old_x_5 = line_5.get_xdata()
    #new_x_5 = np.r_[old_x_5[1:], x_5]
    #line_5.set_xdata(new_x_5)
    y_5 =ay_ReadChannel()
    old_y_5= line_5.get_ydata()
    new_y_5 = np.r_[old_y_5[1:], y_5]
    line_5.set_ydata(new_y_5)
    #print(new_y_3)
    return line_5

def animate_6(i):
    #x_6 = x_read()
    #old_x_6 = line_6.get_ydata()
    #new_x_6 = np.r_[old_x_6[1:], x_6]
    #line_6.set_xdata(new_x_6)
    y_6 = az_ReadChannel()
    old_y_6= line_6.get_ydata()
    new_y_6 = np.r_[old_y_6[1:], y_6]
    line_6.set_ydata(new_y_6)
    #print(new_y_3)
    return line_6

anim = animation.FuncAnimation(fig, animate ,interval = 10)
anim_2 = animation.FuncAnimation(fig, animate_2  , interval=10)
anim_3 = animation.FuncAnimation(fig, animate_3  , interval=10)
anim_4 = animation.FuncAnimation(fig, animate_4  , interval=10)
anim_5 = animation.FuncAnimation(fig, animate_5  , interval=10)
anim_6 = animation.FuncAnimation(fig, animate_6  , interval=10)
plt.show()