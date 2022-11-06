import numpy as np
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval

f, (gx, gy, gz, ax, ay, az) = plt.subplots(6, 3)
f.set_size_inches((10, 5))
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
line1, = gx.plot([0], [0], lw =2)
line2, = gy.plot([0], [0], lw =2) 
line3, = gz.plot([0], [0], lw =2) 
line4, = ax.plot([0], [0], lw =2) 
line5, = ay.plot([0], [0], lw =2) 
line6, = az.plot([0], [0], lw =2)
line = [line1, line2, line3, line4, line5, line6]

 
def animate(i):
    
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    x_value = data['x_value']
    gyro_x = data['gyro_x']
    gyro_y = data['gyro_y']
    gyro_z = data['gyro_z']
    acc_x = data['acc_x']
    acc_y = data['acc_y']
    acc_z = data['acc_z']
 
    #plt.cla()
    #plt.plot(gyro_x, label='Gyro_x')
    #plt.plot(gyro_y, label='Gyro_y')
    #plt.plot(gyro_z, label='Gyro_z')
    #plt.plot(acc_x, label='acc_x')
    #plt.plot(acc_y, label='acc_y')
    #plt.plot(acc_z, label='acc_z')
    #plt.legend(loc = 'upper left')
    #plt.tight_layout()

    #axes[0, 0].cla()
    #axes[0, 1].cla()
    #gx[0, 0].plot(gyro_x)#, label='Gyro_x')
    #gy[0, 1].plot(gyro_y)#, label='Gyro_y')
    #gz[0, 2].plot(gyro_z)#, label='Gyro_z')
    #ax[1, 0].plot(acc_x)#, label='acc_x')
    #ay[1, 1].plot(acc_y)#, label='acc_y')
    #az[1, 2].plot(acc_z)#, label='acc_z')

    line[0].set_data(x_value, gyro_x)
    line[1].set_data(x_value, gyro_y)
    line[2].set_data(x_value, gyro_z)
    line[3].set_data(x_value, acc_x)
    line[4].set_data(x_value, acc_y)
    line[5].set_data(x_value, acc_z)
    return line

ani = FuncAnimation(f, animate, blit = True,frames= 500, interval = 10)
 
plt.tight_layout()
plt.show()
