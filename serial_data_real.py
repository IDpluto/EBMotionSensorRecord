import serial
import math
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from scipy import stats
import random, time, spidev


'''
def save_data(roll, pitch, yaw, acc_x, acc_y, acc_z, count):
    roll_r = "%.2f" %(roll*rad2grad)
    pitch_r = "%.2f" %(pitch*rad2grad)
    yaw_r = "%.2f" %(yaw*rad2grad)
    ax_r = acc_x
    ay_r = acc_y
    az_r = acc_z
    if (count == 0):
        return (roll_r)
    elif (count == 1):
        return (pitch_r)
    elif (count == 2):
        return (yaw_r)
    elif (count == 3):
        return (ax_r)
    elif (count == 4):
        return (ay_r)
    else:
        return (az_r)
'''
grad2rad = 3.141592/180.0
rad2grad = 180.0/3.141592
cos = math.cos
    
ser = serial.Serial('/dev/ttyUSB0', 115200)

fig = plt.figure()    
ax = plt.subplot(211, xlim=(0, 5), ylim=(-500, 500))
ax_2 = plt.subplot(212, xlim=(0, 5), ylim=(-3, 3))

max_points = 50
max_points_2 = 50
count = 0

line, = ax.plot(np.arange(max_points), 
            np.ones(max_points, dtype=np.float64)*np.nan, lw=1, c='blue',ms=1)
line_2, = ax.plot(np.arange(max_points), 
            np.ones(max_points, dtype=np.float64)*np.nan, lw=1, c='green',ms=1)
line_3, = ax.plot(np.arange(max_points), 
            np.ones(max_points, dtype=np.float64)*np.nan, lw=1, c='red',ms=1)
line_4, = ax_2.plot(np.arange(max_points), 
            np.ones(max_points, dtype=np.float64)*np.nan, lw=1,ms=1, c = 'blue')
line_5, = ax_2.plot(np.arange(max_points), 
            np.ones(max_points, dtype=np.float64)*np.nan, lw=1,ms=1, c = 'green')
line_6, = ax_2.plot(np.arange(max_points), 
            np.ones(max_points, dtype=np.float64)*np.nan, lw=1,ms=1, c = 'red')
    

def check_val(result_list):
    roll, pitch, yaw, acc_x, acc_y, acc_z, count = result_list
    roll_r = "%.2f" %(roll*rad2grad)
    pitch_r = "%.2f" %(pitch*rad2grad)
    yaw_r = "%.2f" %(yaw*rad2grad)
    if (count == 0):
        return (roll_r)
    elif (count == 1):
        return (pitch_r)
    elif (count == 2):
        return (yaw_r)
    elif (count == 3):
        return (acc_x)
    elif (count == 4):
        return (acc_y)
    else:
        return (acc_z)

    
    

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

def serial_read(count):
  
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
        else :
            data_format = 1 # euler


        if(data_format==1): #euler
            try:
                roll = float(words[data_index])*grad2rad
                pitch = float(words[data_index+1])*grad2rad
                yaw = float(words[data_index+2])*grad2rad
                roll_r = "%.2f" %(roll*rad2grad)
                pitch_r = "%.2f" %(pitch*rad2grad)
                yaw_r = "%.2f" %(yaw*rad2grad)
               
                acc_x = float(words[data_index+3])
                acc_y = float(words[data_index+4])
                acc_z = float(words[data_index+5])
                result_list = [roll, pitch, yaw, acc_x, acc_y, acc_z, count]
                result = check_val(result_list)
                
                #print(roll)
            except:
               
                roll_r = 0
                pitch_r = 0
                yaw_r = 0
               
                acc_x = 0
                acc_y = 0
                acc_z = 0
                result_list = [roll, pitch, yaw, acc_x, acc_y, acc_z, count]
                result = check_val(result_list)
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
        
        return result
    
def animate(i):
    
    #x = x_read()
    #old_x = line.get_xdata()
    #new_x = np.r_[old_x[1:], x]
    #line.set_xdata(new_x)
    y =  serial_read(0)
    #y = next(y)
    #print(y)
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
    y_2 = serial_read(1)
    #y_2 = next(y_2)
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
    y_3 = serial_read(2)
    #y_3 = next(y_3)
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
    y_4 = serial_read(3)
    #y_4 = next(y_4)
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
    y_5 = serial_read(4)
    #y_5 = next(y_5)
    old_y_5= line_5.get_ydata(4)
    new_y_5 = np.r_[old_y_5[1:], y_5]
    line_5.set_ydata(new_y_5)
    #print(new_y_3)
    return line_5

def animate_6(i):
    #x_6 = x_read()
    #old_x_6 = line_6.get_ydata()
    #new_x_6 = np.r_[old_x_6[1:], x_6]
    #line_6.set_xdata(new_x_6)
    y_6 = serial_read(5)
    #y_6 = next(y_6)
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