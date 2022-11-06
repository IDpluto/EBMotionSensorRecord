
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval

fig, (gx, gy, gz, ax, ay, az) = plt.subplots(6,1)

fig.set_size_inches((10, 5))
fig.subplots_adjust(wspace = 0.9, hspace = 0.9)

line1, = gx.plot([], [], lw =2)
line2, = gy.plot([], [], lw =2) 
line3, = gz.plot([], [], lw =2) 
line4, = ax.plot([], [], lw =2) 
line5, = ay.plot([], [], lw =2) 
line6, = az.plot([], [], lw =2)
line = [line1, line2, line3, line4, line5, line6]

def animate(i):
    # axis limits checking. Same as before, just for both axes
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    gyro_x = data['gyro_x']
    gyro_y = data['gyro_y']
    gyro_z = data['gyro_z']
    acc_x = data['acc_x']
    acc_y = data['acc_y']
    acc_z = data['acc_z']
    gx.clear()
    gy.clear()
    gz.clear()
    ax.clear()
    ay.clear()
    az.clear()
    gx.plot(gyro_x, lw =2, color = 'r')
    gy.plot(gyro_y, lw =2, color = 'r') 
    gz.plot(gyro_z, lw =2, color = 'r') 
    ax.plot(acc_x, lw =2) 
    ay.plot(acc_y, lw =2) 
    az.plot(acc_z, lw =2)
    
    #line[0].set_data(x_value, gyro_x)
    #line[1].set_data(x_value, gyro_y)
    #line[2].set_data(x_value, gyro_z)
    #line[3].set_data(x_value, acc_x)
    #line[4].set_data(x_value, acc_y)
    #line[5].set_data(x_value, acc_z)
    
    return line


ani = FuncAnimation(fig , animate, blit=False, frames= 200, interval = 100)
 
#plt.tight_layout()
plt.show()
