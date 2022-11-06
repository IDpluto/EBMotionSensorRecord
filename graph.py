
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval

fig, (gx, gy, gz, ax, ay, az) = plt.subplots(6,1)

fig.set_size_inches((10, 5))
#plt.subplots_adjust(wspace = 0.8, hspace = 0.8)

line1, = gx.plot([], [], lw =2)
line2, = gy.plot([], [], lw =2) 
line3, = gz.plot([], [], lw =2) 
line4, = ax.plot([], [], lw =2) 
line5, = ay.plot([], [], lw =2) 
line6, = az.plot([], [], lw =2)
line = [line1, line2, line3, line4, line5, line6]

def data_gen():
    t = data_gen.t
    cnt = 0
    while cnt < 1000:
        cnt+=1
        t += 0.05
        y1 = np.sin(2*np.pi*t) * np.exp(-t/10.)
        y2 = np.cos(2*np.pi*t) * np.exp(-t/10.)
        # adapted the data generator to yield both sin and cos
        yield t, y1, y2

data_gen.t = 0

 
def animate(i):
    
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    x_value = data['x_value']
    gyro_x = data['gyro_x']
    gyro_y = data['gyro_y']
    gyro_z = data['gyro_z']
    acc_x = data['acc_x']
    acc_y = data['acc_y']
    acc_z = data['acc_z']

    line[0].set_data(x_value, gyro_x)
    line[1].set_data(x_value, gyro_y)
    line[2].set_data(x_value, gyro_z)
    line[3].set_data(x_value, acc_x)
    line[4].set_data(x_value, acc_y)
    line[5].set_data(x_value, acc_z)
    return line

ani = FuncAnimation(fig , animate, data_gen,  interval = 10)
 
#plt.tight_layout()
plt.show()
