import serial
import math
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from scipy import stats
from collections import deque
import time
from datetime import datetime
import csv

def animate(i):
    
    serial_read()
    y = float(roll_s.pop())
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    if (check_flag(new_y, old_y) == 1):
        flag_ghand.append(1)
    else:
        flag_ghand.append(0)
    line.set_ydata(new_y)
    
    #print(new_y)
    return line
    
def animate_2(i):
    serial_read()
    y_2 = float(pitch_s.pop())
    old_y_2 = line_2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
    if (check_flag(new_y_2, old_y_2) == 1):
        flag_ghand.append(1)
    else:
        flag_ghand.append(0)
    line_2.set_ydata(new_y_2)
    #print(new_y_2)
    return line_2

def animate_3(i):
    serial_read()
    y_3 = float(yaw_s.pop())
    old_y_3= line_3.get_ydata()
    new_y_3 = np.r_[old_y_3[1:], y_3]
    if (check_flag(new_y_3, old_y_3) == 1):
        flag_ghand.append(1)
    else:
        flag_ghand.append(0)
    line_3.set_ydata(new_y_3)
    
    return line_3

def animate_4(i):
    serial_read()
    y_4 = float(ax_s.pop())
    old_y_4= line_4.get_ydata()
    new_y_4 = np.r_[old_y_4[1:], y_4]
    if (check_flag(new_y_4, old_y_4) == 1):
        flag_ahand.append(1)
    else:
        flag_ahand.append(0)
    line_4.set_ydata(new_y_4)
    
    return line_4

def animate_5(i):
    serial_read()
    y_5 = float(ay_s.pop())
    old_y_5= line_5.get_ydata()
    new_y_5 = np.r_[old_y_5[1:], y_5]
    if (check_flag(new_y_5, old_y_5) == 1):
        flag_ahand.append(1)
    else:
        flag_ahand.append(0)
    line_5.set_ydata(new_y_5)
    #print(new_y_3)
    return line_5

def animate_6(i):
    serial_read()
    y_6 = float(az_s.pop())
    old_y_6= line_6.get_ydata()
    new_y_6 = np.r_[old_y_6[1:], y_6]
    if (check_flag(new_y_6, old_y_6) == 1):
        flag_ahand.append(1)
    else:
        flag_ahand.append(0)
    line_6.set_ydata(new_y_6)
    #print(new_y_3)
    return line_6
#----------------------------------------------------


def animate_h1(i):
    
    serial_read()
    y = float(roll_h.pop())
    old_y = line_h1.get_ydata()
    new_y = np.r_[old_y[1:], y]
    if (check_flag(new_y, old_y) == 1):
        flag_ghand.append(1)
    else:
        flag_ghead.append(0)
    line_h1.set_ydata(new_y)
    #print(new_y)
    return line_h1
    
def animate_h2(i):
    serial_read()
    y_2 = float(pitch_h.pop())
    old_y_2 = line_h2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
    if (check_flag(new_y_2, old_y_2) == 1):
        flag_ghead.append(1)
    else:
        flag_ghead.append(0)
    line_h2.set_ydata(new_y_2)
    #print(new_y_2)
    return line_h2

def animate_h3(i):
    serial_read()
    y_3 = float(yaw_h.pop())
    old_y_3= line_h3.get_ydata()
    new_y_3 = np.r_[old_y_3[1:], y_3]
    if (check_flag(new_y_3, old_y_3) == 1):
        flag_ghead.append(1)
    else:
        flag_ghead.append(0)
    line_h3.set_ydata(new_y_3)
    
    return line_h3

def animate_h4(i):
    serial_read()
    y_4 = float(ax_h.pop())
    old_y_4= line_h4.get_ydata()
    new_y_4 = np.r_[old_y_4[1:], y_4]
    if (check_flag(new_y_4, old_y_4) == 1):
        flag_ahead.append(1)
    else:
        flag_ahead.append(0)
    line_h4.set_ydata(new_y_4)
    
    return line_h4

def animate_h5(i):
    serial_read()
    y_5 = float(ay_h.pop())
    old_y_5= line_h5.get_ydata()
    new_y_5 = np.r_[old_y_5[1:], y_5]
    if (check_flag(new_y_5, old_y_5) == 1):
        flag_ahead.append(1)
    else:
        flag_ahead.append(0)
    line_h5.set_ydata(new_y_5)
    return line_h5

def animate_h6(i):
    serial_read()
    y_6 = float(az_h.pop())
    old_y_6= line_h6.get_ydata()
    new_y_6 = np.r_[old_y_6[1:], y_6]
    if (check_flag(new_y_6, old_y_6) == 1):
        flag_ahead.append(1)
    else:
        flag_ahead.append(0)
    line_h6.set_ydata(new_y_6)
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

def check_flag(new, old):
    if (new.any() > old.any() or new.any() < old.any()):
        return 1
    else:
        return 0
    


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
    #day_c = day_p.pop()
    time_c = 'test'
    print (time_c)
    flag_gh1 = int(flag_ghand.pop())
    flag_ah1 = int(flag_ahand.pop())
    flag_gh2 = int(flag_ghead.pop())
    flag_ah2 = int(flag_ahead.pop())
    roll1 = float(roll_chand.pop())
    pitch1 = float(pitch_chand.pop())
    yaw1 = float(yaw_chand.pop())
    ax1 = float(ax_chand.pop())
    ay1 = float(ay_chand.pop())
    az1 = float(az_chand.pop())
    roll2 = float(roll_chead.pop())
    pitch2 = float(pitch_chead.pop())
    yaw2 = float(yaw_chead.pop())
    ax2 = float(ax_chead.pop())
    ay2 = float(ay_chead.pop())
    az2 = float(az_chead.pop())
    with open('/home/dohlee/crc_project/data/data1.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        info = {
            #"Y-M-D": day_c,
            "Time": time_c,
            "Flag_Gyro_hand": flag_gh1,
            "Roll_hand": roll1,
            "Pitch_hand": pitch1,
            "Yaw_hand": yaw1,
            "Flag_Acc_hand": flag_ah1,
            "Acc_x_hand": ax1,
            "Acc_y_hand": ay1,
            "Acc_z_hand": az1,
            "Flag_Gyro_head": flag_gh2,
            "Roll_head": roll2,
            "Pitch_head": pitch2,
            "Yaw_head": yaw2,
            "Flag_Acc_hand": flag_ah2,
            "Acc_x_head": ax2,
            "Acc_y_head": ay2,
            "Acc_z_head": az2
        }
        csv_writer.writerow(info)
        #time.sleep(1)


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
                    now = datetime.now()
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
                        #day_p.append(now.date())
                        time_p.append(now.time())
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
                        ax_chead.append(acc_x_t)
                        ay_chead.append(acc_y_t)
                        az_chead.append(acc_z_t)
                        #day_p.append(now.date())
                        time_p.append(now.time())
                    save_csv()
                except: 
                    print ("miss_data")

   
   
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

    flag_ghand = deque()
    flag_ahand = deque()
    flag_ghead = deque()
    flag_ahead = deque()

    day_p = deque()
    time_p = deque()
    
    

    fig = plt.figure()
    ax = plt.subplot(211, xlim=(0, 4.1), ylim=(-500, 500))
    
    ax.set_title("hand")
    ax.set_ylabel("val")
    #ax = plt.title("test")
    ax_2 = plt.subplot(212, xlim=(0, 4.1), ylim=(-500, 500))
    ax_2.set_title("head")
    ax_2.set_ylabel("val")
    plt.tight_layout()


    max_points = 5
    max_points_2 = 5
    count = 0
    fieldnames = ["Time", "Flag_Gyro_hand", "Roll_hand", "Pitch_hand", "Flag_Acc_hand","Yaw_hand", "Acc_x_hand", "Acc_y_hand", "Acc_z_hand", "Flag_gyro_head", "Roll_head", "Pitch_head",  "Yaw_head", "Flag_Acc_head", "Acc_x_head", "Acc_y_head", "Acc_z_head"]
    ser.write(b"<??cg>")
    
    with open('/home/dohlee/crc_project/data/data1.csv','w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()
    line, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, 'o-', lw=1, c='blue',ms=3, label ='Roll')
    line_2, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, 'o-', lw=1, c='green',ms=3, label = 'Pitch')
    line_3, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, 'o-', lw=1, c='red',ms=3 , label= 'Yaw')
    line_4, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, 'o-', lw=1, ms=3, c = 'darkturquoise', label = 'Acc_x')
    line_5, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, 'o-', lw=1, ms=3, c = 'darkviolet', label = 'Acc_y')
    line_6, = ax.plot(np.arange(max_points), 
        np.ones(max_points, dtype=np.float64)*np.nan, 'o-', lw=1, ms=3, c = 'darkorange', label = 'Acc_z')
    
    line_h1, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, 'o-', lw=1, c='blue',ms=3, label ='Roll')
    line_h2, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, 'o-', lw=1, c='green',ms=3, label ='Pitch')
    line_h3, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, 'o-', lw=1, c='red',ms=3, label ='Yaw')
    line_h4, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, 'o-', lw=1,ms=3, c = 'darkturquoise', label ='Acc_x')
    line_h5, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, 'o-', lw=1,ms=3, c = 'darkviolet', label ='Acc_y')
    line_h6, = ax_2.plot(np.arange(max_points_2), 
        np.ones(max_points_2, dtype=np.float64)*np.nan, 'o-', lw=1,ms=3, c = 'darkorange', label ='Acc_z')

    ax.legend(loc = 'upper left')
    ax_2.legend(loc = 'upper left')
    ax.grid()
    ax_2.grid()

   
    anim = animation.FuncAnimation(fig, animate, frames= None, interval = 1,blit=False, repeat = False)
    anim_2 = animation.FuncAnimation(fig, animate_2,  frames= None, interval=1, blit=False, repeat = False)
    anim_3 = animation.FuncAnimation(fig, animate_3, frames= None, interval=1, blit=False, repeat = False)
    anim_4 = animation.FuncAnimation(fig, animate_4, frames= None, interval=1, blit=False, repeat = False)
    anim_5 = animation.FuncAnimation(fig, animate_5,  frames= None, interval=1, blit=False, repeat = False)
    anim_6 = animation.FuncAnimation(fig, animate_6, frames= None, interval=1, blit=False, repeat = False)

    ani7 = animation.FuncAnimation(fig, animate_h1,   frames= None, interval = 1, blit=False, repeat = False)
    anim_8 = animation.FuncAnimation(fig, animate_h2,  frames= None, interval=1, blit=False, repeat = False)
    anim_9 = animation.FuncAnimation(fig, animate_h3,  frames= None, interval=1, blit=False, repeat = False)
    anim_10 = animation.FuncAnimation(fig, animate_h4,  frames= None, interval=1, blit=False, repeat = False)
    anim_11 = animation.FuncAnimation(fig, animate_h5,  frames= None, interval=1, blit=False, repeat = False)
    anim_12 = animation.FuncAnimation(fig, animate_h6, frames= None, interval=1, blit=False, repeat = False)
    plt.show()
    ser.close
