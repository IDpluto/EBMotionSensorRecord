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

def ReadChannel():
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')

    roll1 = data['roll']
    pitch1 = data['pitch']
    yaw1 = data['yaw']
    acc_x1 = data['acc_x']
    acc_y1 = data['acc_y']
    acc_z1 = data['acc_z']
    data = stats.pearsonr([roll1, pitch1, yaw1], [acc_x1, acc_y1, acc_z1])
    return data










mcp3008_channel=0
fig = plt.figure()    
ax = plt.subplot(211, xlim=(0, 50), ylim=(-3, 3))
ax_2 = plt.subplot(212, xlim=(0, 50), ylim=(-3, 3))

max_points = 50
max_points_2 = 50

line, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)
line_2, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='green',ms=1)
line_3, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='red',ms=1)
line_4, = ax_2.plot(np.arange(max_points_2), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1,ms=1, c = 'blue')
line_5, = ax_2.plot(np.arange(max_points_2), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1,ms=1, c = 'green')
line_6, = ax_2.plot(np.arange(max_points_2), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1,ms=1, c = 'red')

def animate(i):
    y = ReadChannel()
    y = y[0]
    # y = random.randint(0,1000)
    old_y = line.get_ydata()
    #print(old_y[1:])
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)
    #print(new_y)
    return line
    
def animate_2(i):
    y_2 = ReadChannel()
    y_2 = y_2[1]
    old_y_2 = line_2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
    line_2.set_ydata(new_y_2)
    #print(new_y_2)
    return line_2

def animate_3(i):
    y_3 = ReadChannel()
    y_3 = y_3[2]
    old_y_3= line_3.get_ydata()
    new_y_3 = np.r_[old_y_3[1:], y_3]
    line_3.set_ydata(new_y_3)
    #print(new_y_3)
    return line_3
def animate_4(i):
    y_4 = ReadChannel()
    y_4 = y_4[3]
    old_y_4= line_4.get_ydata()
    new_y_4 = np.r_[old_y_4[1:], y_4]
    line_4.set_ydata(new_y_4)
    #print(new_y_3)
    return line_5

def animate_5(i):
    y_5 = ReadChannel()
    y_5 = y_5[4]
    old_y_5= line_3.get_ydata()
    new_y_5 = np.r_[old_y_5[1:], y_5]
    line_5.set_ydata(new_y_5)
    #print(new_y_3)
    return line_5

def animate_6(i):
    y_6 = ReadChannel()
    y_6 = y_6[5]
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