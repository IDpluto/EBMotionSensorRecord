import serial
import math
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random, time, spidev


grad2rad = 3.141592/180.0
rad2grad = 180.0/3.141592
cos = math.cos


spi=spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000
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
            
        roll_r = "%.2f" %(roll*rad2grad)
        pitch_r = "%.2f" %(pitch*rad2grad)
        yaw_r = "%.2f" %(yaw*rad2grad)
        
        text = words[0][-1:]
        data = roll_r
    return data










mcp3008_channel=0
fig = plt.figure()    
ax = plt.subplot(211, xlim=(0, 50), ylim=(0, 100))
ax_2 = plt.subplot(212, xlim=(0, 50), ylim=(0, 100))

max_points = 50
max_points_2 = 50

line, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)
line_2, = ax_2.plot(np.arange(max_points_2), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1,ms=1)

def animate(i):
    y = ReadChannel()
    # y = random.randint(0,1000)
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)
    print(new_y)
    return line
    
def animate_2(i):
    y_2 = ReadChannel()
    old_y_2 = line_2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
    line_2.set_ydata(new_y_2)
    print(new_y_2)
    return line_2


anim = animation.FuncAnimation(fig, animate ,interval = 10)
anim_2 = animation.FuncAnimation(fig, animate_2  , interval=10)
plt.show()