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
from datetime import datetime
import atexit

def animate(i):
    
    serial_read()
    y = float(roll_s.pop())
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    
    line.set_ydata(new_y)
    
    #print(new_y)
    return line
    
def animate_2(i):
    serial_read()
    y_2 = float(pitch_s.pop())
    old_y_2 = line_2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
  
    line_2.set_ydata(new_y_2)
    #print(new_y_2)
    return line_2

def animate_3(i):
    serial_read()
    y_3 = float(yaw_s.pop())
    old_y_3= line_3.get_ydata()
    new_y_3 = np.r_[old_y_3[1:], y_3]
    
    line_3.set_ydata(new_y_3)
    
    return line_3

def animate_4(i):
    serial_read()
    y_4 = float(ax_s.pop())
    old_y_4= line_4.get_ydata()
    new_y_4 = np.r_[old_y_4[1:], y_4]
    
    line_4.set_ydata(new_y_4)
    
    return line_4

def animate_5(i):
    serial_read()
    y_5 = float(ay_s.pop())
    old_y_5= line_5.get_ydata()
    new_y_5 = np.r_[old_y_5[1:], y_5]
   
    line_5.set_ydata(new_y_5)
    #print(new_y_3)
    return line_5

def animate_6(i):
    serial_read()
    y_6 = float(az_s.pop())
    old_y_6= line_6.get_ydata()
    new_y_6 = np.r_[old_y_6[1:], y_6]
    
    line_6.set_ydata(new_y_6)
    #print(new_y_3)
    return line_6
#----------------------------------------------------


def animate_h1(i):
    
    serial_read()
    y = float(roll_h.pop())
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
    y_3 = float(yaw_h.pop())
    old_y_3= line_h3.get_ydata()
    new_y_3 = np.r_[old_y_3[1:], y_3]
    
    line_h3.set_ydata(new_y_3)
    
    return line_h3

def animate_h4(i):
    serial_read()
    y_4 = float(ax_h.pop())
    old_y_4= line_h4.get_ydata()
    new_y_4 = np.r_[old_y_4[1:], y_4]
    
    line_h4.set_ydata(new_y_4)
    
    return line_h4

def animate_h5(i):
    serial_read()
    y_5 = float(ay_h.pop())
    old_y_5= line_h5.get_ydata()
    new_y_5 = np.r_[old_y_5[1:], y_5]
    
    line_h5.set_ydata(new_y_5)
    return line_h5

def animate_h6(i):
    serial_read()
    y_6 = float(az_h.pop())
    old_y_6= line_h6.get_ydata()
    new_y_6 = np.r_[old_y_6[1:], y_6]
    
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

def check_negative(data):
    if (data < 0):
        return True
    else:
        return False

def check_event(ach_x, ach_y, ach_z):
    if (check_negative(ach_x) == True):
        if(ach_x < 8):
            return True
    if (check_negative(ach_y) == True):
        if(ach_y < 8):
            return True
    if (check_negative(ach_z) == True):
        if(ach_z < 8):
            return True 
    if (check_negative(ach_x) == False):
        if(ach_x > 8):
            return True
    if (check_negative(ach_y) == False):
        if(ach_y > 8):
            return True
    if (check_negative(ach_z) == False):
        if(ach_z > 8):
            return True
    
    return False

def remove_que(count):
    i = 0
    while (i < count):
        roll_chand.popleft()
        pitch_chand.popleft()
        yaw_chand.popleft()
        roll_chead.popleft()
        pitch_chead.popleft()
        yaw_chead.popleft()
        ax_chand.popleft()
        ay_chand.popleft()
        az_chand.popleft()
        ax_chead.popleft()
        ay_chead.popleft()
        az_chead.popleft()
        i += 1

def clear_que():
    roll_chand.clear()
    pitch_chand.clear()
    yaw_chand.clear()
    roll_chead.clear()
    pitch_chead.clear()
    yaw_chead.clear()
    ax_chand.clear()
    ay_chand.clear()
    az_chand.clear()
    ax_chead.clear()
    ay_chead.clear()
    az_chead.clear()

        


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
    
    day_c = day_p.popleft()
    time_c = time_p.popleft()
    roll1 = float(roll_chand.popleft())
    pitch1 = float(pitch_chand.popleft())
    yaw1 = float(yaw_chand.popleft())
    ax1 = float(ax_chand.popleft())
    ay1 = float(ay_chand.popleft())
    az1 = float(az_chand.popleft())
    roll2 = float(roll_chead.popleft())
    pitch2 = float(pitch_chead.popleft())
    yaw2 = float(yaw_chead.popleft())
    ax2 = float(ax_chead.popleft())
    ay2 = float(ay_chead.popleft())
    az2 = float(az_chead.popleft())
    with open('/home/dohlee/crc_project/data/data1.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        info = {
            "Y-M-D": day_c,
            "H-M-S": time_c,
            
            "Roll_hand": roll1,
            "Pitch_hand": pitch1,
            "Yaw_hand": yaw1,
            
            "Acc_x_hand": ax1,
            "Acc_y_hand": ay1,
            "Acc_z_hand": az1,
            
            "Roll_head": roll2,
            "Pitch_head": pitch2,
            "Yaw_head": yaw2,
            
            "Acc_x_head": ax2,
            "Acc_y_head": ay2,
            "Acc_z_head": az2
        }
        csv_writer.writerow(info)
        #time.sleep(1)

def t_event_save():
    i = 0
    while(i < 100):
        time_stamp.popleft()
        save_csv()
        i += 1

def event_save():
    i = 0
    while(i < 100):
        save_csv()
        i += 1


def serial_read():
    flag = 0
    line = ser.readline()
    line = line.decode("ISO-8859-1")# .encode("utf-8")
    words = line.split(",")    # Fields split
    #global flag
    #global s_flag
    #global s_count
    
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
                    if (check_event(acc_x,acc_y,acc_z) == True):
                        flag = 1
                    ax_chand.append(acc_x)
                    ay_chand.append(acc_y)
                    az_chand.append(acc_z)
                    day_p.append(now.date())
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
                    if (check_event(acc_x_t,acc_y_t,acc_z_t) == True):
                        flag = 1
                    ax_chead.append(acc_x_t)
                    ay_chead.append(acc_y_t)
                    az_chead.append(acc_z_t)

                if (flag == 1):
                    time_stamp.append(1)
                else:
                    time_stamp.append(0)
                    flag = 0

                    '''
                    if (flag == 1 and len(ax_chand) < 15 and s_flag == 0):
                        save_csv()
                        clear_que()
                        s_flag = 1
                    if (flag == 1 and len(ax_chand > 15 and s_flag == 0)):
                        remove_que()
                        save_csv()
                        clear_que()
                        s_flag = 1
                    if (flag == 1 and s_count < 15 and s_flag == 1):
                        save_csv()
                        s_count += 1
                    if s_count == 15:
                        s_count = 0
                        s_flag == 0
                    '''
                       
def exit_event():
    zero_count = 0
    r_count = 0
    flag = 0
    re_flag = 0
    q_len = len(time_stamp)
    while (True):
        if (time_stamp.popleft() == 0):
            zero_count += 1
        if (time_stamp.popleft() == 1):
            if (zero_count < 100):
                event_save()
            elif (zero_count > 100):
                r_count = zero_count - 100
                remove_que(r_count)
                event_save()
                zero_count = 0
        t_event_save()
        if (len(time_stamp) == 0):
            break

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

    day_p = deque()
    time_p = deque()
    time_stamp = deque()

    #global s_count
    #global s_flag
    #global flag
    #s_count = 0
    #s_flag = 0
    #flag = 0
    fig = plt.figure()
    ax = plt.subplot(211, xlim=(0, 6), ylim=(-600, 600))
    
    ax.set_title("hand")
    ax.set_ylabel("val")
    #ax = plt.title("test")
    ax_2 = plt.subplot(212, xlim=(0, 6), ylim=(-600, 600))
    ax_2.set_title("head")
    ax_2.set_ylabel("val")
    plt.tight_layout()


    max_points = 6
    max_points_2 = 6
    fieldnames = ["Y-M-D", "H-M-S", "Roll_hand", "Pitch_hand", "Yaw_hand","Acc_x_hand", "Acc_y_hand", "Acc_z_hand",  "Roll_head", "Pitch_head",  "Yaw_head",  "Acc_x_head", "Acc_y_head", "Acc_z_head"]
    ser.write(b"<sor100>")
    time.sleep(1)
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


    anim = animation.FuncAnimation(fig, animate, frames= None, interval = 10,blit=False, repeat = False)
    anim_2 = animation.FuncAnimation(fig, animate_2,  frames= None, interval=10, blit=False, repeat = False)
    anim_3 = animation.FuncAnimation(fig, animate_3, frames= None, interval=10, blit=False, repeat = False)
    anim_4 = animation.FuncAnimation(fig, animate_4, frames= None, interval=10, blit=False, repeat = False)
    anim_5 = animation.FuncAnimation(fig, animate_5,  frames= None, interval=10, blit=False, repeat = False)
    anim_6 = animation.FuncAnimation(fig, animate_6, frames= None, interval=10, blit=False, repeat = False)

    ani7 = animation.FuncAnimation(fig, animate_h1,   frames= None, interval = 10, blit=False, repeat = False)
    anim_8 = animation.FuncAnimation(fig, animate_h2,  frames= None, interval=10, blit=False, repeat = False)
    anim_9 = animation.FuncAnimation(fig, animate_h3,  frames= None, interval=10, blit=False, repeat = False)
    anim_10 = animation.FuncAnimation(fig, animate_h4,  frames= None, interval=10, blit=False, repeat = False)
    anim_11 = animation.FuncAnimation(fig, animate_h5,  frames= None, interval=10, blit=False, repeat = False)
    anim_12 = animation.FuncAnimation(fig, animate_h6, frames= None, interval=10, blit=False, repeat = False)
    atexit.register(exit_event)
    plt.show()
    ser.close
