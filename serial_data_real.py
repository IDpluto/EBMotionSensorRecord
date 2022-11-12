import serial
import math
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from scipy import stats
from collections import deque
import time
import csv

def animate(i):
    
    serial_read()
    y = roll_s.pop()
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)
    
    #print(new_y)
    return line
    
def animate_2(i):
    serial_read()
    y_2 = pitch_s.pop()
    old_y_2 = line_2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
    line_2.set_ydata(new_y_2)
    #print(new_y_2)
    return line_2

def animate_3(i):
    serial_read()
    y_3 = yaw_s.pop()
    old_y_3= line_3.get_ydata()
    new_y_3 = np.r_[old_y_3[1:], y_3]
    line_3.set_ydata(new_y_3)
    
    return line_3

def animate_4(i):
    serial_read()
    y_4 = ax_s.pop()
    old_y_4= line_4.get_ydata()
    new_y_4 = np.r_[old_y_4[1:], y_4]
    line_4.set_ydata(new_y_4)
    
    return line_4

def animate_5(i):
    serial_read()
    y_5 = ay_s.pop()
    old_y_5= line_5.get_ydata()
    new_y_5 = np.r_[old_y_5[1:], y_5]
    line_5.set_ydata(new_y_5)
    #print(new_y_3)
    return line_5

def animate_6(i):
    serial_read()
    y_6 = az_s.pop()
    old_y_6= line_6.get_ydata()
    new_y_6 = np.r_[old_y_6[1:], y_6]
    line_6.set_ydata(new_y_6)
    #print(new_y_3)
    return line_6
#----------------------------------------------------


def animate_h1(i):
    
    serial_read()
    y = roll_h.pop()
    old_y = line_h1.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line_h1.set_ydata(new_y)
    
    #print(new_y)
    return line_h1
    
def animate_h2(i):
    serial_read()
    y_2 = float(pitch_h.pop())
    old_y_2 = line_h2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
    line_h2.set_ydata(new_y_2)
    #print(new_y_2)
    return line_h2

def animate_h3(i):
    serial_read()
    y_3 = yaw_h.pop()
    old_y_3= line_h3.get_ydata()
    new_y_3 = np.r_[old_y_3[1:], y_3]
    line_h3.set_ydata(new_y_3)
    
    return line_h3

def animate_h4(i):
    serial_read()
    y_4 = ax_h.pop()
    old_y_4= line_h4.get_ydata()
    new_y_4 = np.r_[old_y_4[1:], y_4]
    line_h4.set_ydata(new_y_4)
    
    return line_h4

def animate_h5(i):
    serial_read()
    y_5 = ay_h.pop()
    old_y_5= line_h5.get_ydata()
    new_y_5 = np.r_[old_y_5[1:], y_5]
    line_h5.set_ydata(new_y_5)
    #print(new_y_3)
    return line_h5

def animate_h6(i):
    serial_read()
    y_6 = az_h.pop()
    old_y_6= line_h6.get_ydata()
    new_y_6 = np.r_[old_y_6[1:], y_6]
    line_h6.set_ydata(new_y_6)
    #print(new_y_3)
    return line_h6

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


def save_data_hand(roll, pitch, yaw):
    roll_r = "%.2f" %(roll*rad2grad)
    pitch_r = "%.2f" %(pitch*rad2grad)
    yaw_r = "%.2f" %(yaw*rad2grad)
    roll_s.append(roll_r)
    pitch_s.append(pitch_r)
    yaw_s.append(yaw_r)
    roll_chand.append(roll_r)
    pitch_chand.append(pitch_r)
    yaw_chand.append(yaw_r)

def save_data_head(roll, pitch, yaw):
    roll_r = "%.2f" %(roll*rad2grad)
    pitch_r = "%.2f" %(pitch*rad2grad)
    yaw_r = "%.2f" %(yaw*rad2grad)
    roll_h.append(roll_r)
    pitch_h.append(pitch_r)
    yaw_h.append(yaw_r)
    roll_chead.append(roll_r)
    pitch_chead.append(pitch_r)
    yaw_chead.append(yaw_r)

def save_csv():
    
    with open('/home/dohlee/crc_project/data/data1.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        info = {
            "roll_hand":roll_chand.pop(),
            "pitch_hand":pitch_chand.pop(),
            "yaw_hand":yaw_chand.pop(),
            "acc_x_hand":ax_chand.pop(),
            "acc_y_hand":ay_chand.pop(),
            "acc_z_hand":az_chand.pop(),
            "roll_head":roll_chead.pop(),
            "pitch_head":pitch_chead.pop(),
            "yaw_head":yaw_chead.pop(),
            "acc_x_head":ax_chead.pop(),
            "acc_y_head":ay_chead.pop(),
            "acc_z_head":az_chead.pop()
        }
        csv_writer.writerow(info)


def serial_read():
  
    line = ser.readline()
    line = line.decode("ISO-8859-1")# .encode("utf-8")
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
                    if (text == "ID:100-0"):
                        roll = float(words[data_index])*grad2rad
                        pitch = float(words[data_index+1])*grad2rad
                        yaw = float(words[data_index+2])*grad2rad
                        acc_x = float(words[data_index+3]) * 100
                        acc_y = float(words[data_index+4]) * 100
                        acc_z = float(words[data_index+5]) * 100
                        save_data_hand(roll, pitch, yaw)
                        ax_s.append(acc_x)
                        ay_s.append(acc_y)
                        az_s.append(acc_z)
                        ax_chand.append(acc_x)
                        ay_chand.append(acc_y)
                        az_chand.append(acc_z)
                        
                        
                    if(text == "ID:100-1"):
                        roll_t = float(words[data_index])*grad2rad
                        pitch_t = float(words[data_index+1])*grad2rad
                        yaw_t = float(words[data_index+2])*grad2rad
                        acc_x_t = float(words[data_index+3]) * 100
                        acc_y_t = float(words[data_index+4]) * 100
                        acc_z_t = float(words[data_index+5]) * 100
                        save_data_head(roll_t, pitch_t, yaw_t)
                        ax_h.append(acc_x_t)
                        ay_h.append(acc_y_t)
                        az_h.append(acc_z_t)
                    save_csv()
                except: 
                    print ("miss_data")
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
        
        



if __name__ == '__main__':

    grad2rad = 3.141592/180.0
    rad2grad = 180.0/3.141592
    cos = math.cos
    
    ser = serial.Serial('/dev/ttyUSB0', 921600)
  
    roll_s = deque()
    pitch_s = deque()
    yaw_s =  deque()
    ax_s = deque()
    ay_s = deque()
    az_s = deque()
    roll_h = deque()
    pitch_h = deque()
    yaw_h = deque()
    ax_h = deque()
    ay_h = deque()
    az_h = deque()

    roll_chand = deque()
    pitch_chand = deque()
    yaw_chand = deque()
    ax_chand = deque()
    ay_chand = deque()
    az_chand = deque()

    roll_chead = deque()
    pitch_chead = deque()
    yaw_chead = deque()
    ax_chead = deque()
    ay_chead = deque()
    az_chead = deque()
    

    fig = plt.figure()
    ax = plt.subplot(211, xlim=(0, 40), ylim=(-300, 300))

    ax.set_ylabel("Test")
    #ax = plt.title("test")
    ax_2 = plt.subplot(212, xlim=(0, 40), ylim=(-300, 300))
    plt.tight_layout()


    max_points = 40
    max_points_2 = 40
    count = 0
    fieldnames = ["roll_hand", "pitch_hand", "yaw_hand", "acc_x_hand", "acc_y_hand", "acc_z_hand", "roll_head", "pitch_head", "yaw_head", "acc_x_head", "acc_y_head", "acc_z_head"]

    with open('/home/dohlee/crc_project/data/data1.csv','w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()
    
    line, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, lw=1, c='blue',ms=1)
    line_2, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, lw=1, c='green',ms=1)
    line_3, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, lw=1, c='red',ms=1)
    line_4, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, lw=1,ms=1, c = 'darkturquoise')
    line_5, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, lw=1,ms=1, c = 'darkviolet')
    line_6, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, lw=1,ms=1, c = 'darkorange')
    
    line_h1, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, lw=1, c='blue',ms=1)
    line_h2, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, lw=1, c='green',ms=1)
    line_h3, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, lw=1, c='red',ms=1)
    line_h4, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, lw=1,ms=1, c = 'darkturquoise')
    line_h5, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, lw=1,ms=1, c = 'darkviolet')
    line_h6, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, lw=1,ms=1, c = 'darkorange')

   
    anim = animation.FuncAnimation(fig, animate, fargs = (roll_s), frames= 400, interval = 10, blit=False)
    anim_2 = animation.FuncAnimation(fig, animate_2, fargs = (pitch_s), frames= 400, interval=10, blit=False)
    anim_3 = animation.FuncAnimation(fig, animate_3, fargs = (yaw_s), frames= 400, interval=10, blit=False)
    anim_4 = animation.FuncAnimation(fig, animate_4, fargs = (ax_s), frames= 400, interval=10, blit=False)
    anim_5 = animation.FuncAnimation(fig, animate_5, fargs = (ay_s), frames= 400, interval=10, blit=False)
    anim_6 = animation.FuncAnimation(fig, animate_6, fargs = (az_s), frames= 400, interval=10, blit=False)

    ani7 = animation.FuncAnimation(fig, animate_h1, fargs = (roll_h), frames= 400, interval = 10, blit=False)
    anim_8 = animation.FuncAnimation(fig, animate_h2, fargs = (pitch_h), frames= 400, interval=10, blit=False)
    anim_9 = animation.FuncAnimation(fig, animate_h3, fargs = (yaw_h), frames= 400, interval=10, blit=False)
    anim_10 = animation.FuncAnimation(fig, animate_h4, fargs = (ax_h), frames= 400, interval=10, blit=False)
    anim_11 = animation.FuncAnimation(fig, animate_h5, fargs = (ay_h), frames= 400, interval=10, blit=False)
    anim_12 = animation.FuncAnimation(fig, animate_h6, fargs = (az_h), frames= 400, interval=10, blit=False)

    plt.show()
