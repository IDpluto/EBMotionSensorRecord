import serial
import math
import string
import time
import signal
from itertools import count
import pandas as pd
import numpy as np
import csv

grad2rad = 3.141592/180.0
rad2grad = 180.0/3.141592
cos = math.cos


ser = serial.Serial('/dev/ttyUSB0', 921600)
fieldnames = ["x_num","hand_sensor_id","hand_roll", "hand_pitch", "hand_yaw", "hand_acc_x", "hand_acc_y", "hand_acc_z", "head_sensor_id","head_roll", "head_pitch", "head_yaw", "head_acc_x", "head_acc_y", "head_acc_z" ]

def save_data_hand(sensor_id, roll, pitch, yaw, acc_x, acc_y, acc_z, x_count):

    roll_r = "%.2f" %(roll*rad2grad)
    pitch_r = "%.2f" %(pitch*rad2grad)
    yaw_r = "%.2f" %(yaw*rad2grad)
    with open('/home/dohlee/crc_project/data/data1.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        info = {
            "x_num":x_count,
            "hand_sensor_id":sensor_id,
            "hand_roll":roll_r,
            "hand_pitch":pitch_r,
            "hand_yaw":yaw_r,
            "hand_acc_x":acc_x,
            "hand_acc_y":acc_y,
            "hand_acc_z":acc_z,
            "head_sensor_id": None,
            "head_roll": None,
            "head_pitch": None,
            "head_yaw": None,
            "head_acc_x": None,
            "head_acc_y": None,
            "head_acc_z": None
        }
        csv_writer.writerow(info)
        time.sleep(1)
def save_data_head(sensor_id, roll, pitch, yaw, acc_x, acc_y, acc_z, x_count):

    roll_r = "%.2f" %(roll*rad2grad)
    pitch_r = "%.2f" %(pitch*rad2grad)
    yaw_r = "%.2f" %(yaw*rad2grad)
    with open('/home/dohlee/crc_project/data/data1.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        info = {
            "x_num":x_count,
            "hand_sensor_id":None,
            "hand_roll": None,
            "hand_pitch": None,
            "hand_yaw": None,
            "hand_acc_x":None,
            "hand_acc_y":None,
            "hand_acc_z":None,
            "head_sensor_id": sensor_id,
            "head_roll": roll_r,
            "head_pitch": pitch_r,
            "head_yaw": yaw_r,
            "head_acc_x": acc_x,
            "head_acc_y": acc_y,
            "head_acc_z": acc_z
        }
        csv_writer.writerow(info)
        time.sleep(1)

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
x_count = 0
with open('/home/dohlee/crc_project/data/data1.csv','w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()
while 1:
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
        x_count += 0.1
        
        save_data_hand(text, roll, pitch, yaw,acc_x, acc_y, acc_z, x_count)

   

ser.close

    

