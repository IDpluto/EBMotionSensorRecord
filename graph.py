from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval

f, axes = plt.subplots(2, 3)
f.set_size_inches((10, 5))
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
 
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
    axes[0, 0].plot(gyro_x)#, label='Gyro_x')
    axes[0, 1].plot(gyro_y)#, label='Gyro_y')
    axes[0, 2].plot(gyro_z)#, label='Gyro_z')
    axes[1, 0].plot(acc_x)#, label='acc_x')
    axes[1, 1].plot(acc_y)#, label='acc_y')
    axes[1, 2].plot(acc_z)#, label='acc_z')
    axes[0, 0].legend(loc = 'upper left')
    axes[0, 1].legend(loc = 'upper left')
    axes[0, 2].legend(loc = 'upper left')
    axes[1, 0].legend(loc = 'upper left')
    axes[1, 1].legend(loc = 'upper left')
    axes[1, 2].legend(loc = 'upper left')
    #axes[0, 0].tight_layout()
    #axes[0, 1].tight_layout()
    #axes[0, 2].tight_layout()
    #axes[1, 0].tight_layout()
    #axes[1, 1].tight_layout()
    #axes[1, 2].tight_layout()



ani = FuncAnimation(plt.gcf(),animate, frames= 500, interval = 50)
 
plt.tight_layout()
plt.show()
