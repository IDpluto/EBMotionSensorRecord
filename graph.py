
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval



def animate(i):
    # axis limits checking. Same as before, just for both axes
    data =pd.read_csv('/home/dohlee/crc_project/data/data1.csv')
    x_num = data['x_num']
    roll = data['roll']
    pitch = data['pitch']
    yaw = data['yaw']
    acc_x = data['acc_x']
    acc_y = data['acc_y']
    acc_z = data['acc_z']
    plt.ylim([-20, 20])
    plt.cla()
    plt.plot(x_num, roll, label = 'roll', color = 'black')
    plt.plot(x_num, pitch, label = 'pitch', color = 'limegreen')
    plt.plot(x_num, yaw, label = 'yaw', color = 'violet')
    plt.plot(x_num, acc_x, label = 'acc_x', color = 'dodgerblue')
    plt.plot(x_num, acc_y, label = 'acc_Y', color = 'red')
    plt.plot(x_num, acc_z, label = 'acc_z', color = 'deepskyblue')

    plt.xticks(rotation=45, ha='right')
    #plt.subplots_adjust(bottom=0.30)
    plt.title('This is how I roll...')
    plt.ylabel('Relative frequency')
    plt.legend(loc = 'upper left')
    plt.axis([1, None, -10, 10]) #Use for arbitrary number of trials
    plt.tight_layout()
   
plt.figure(figsize=(10, 5))
ani = FuncAnimation(plt.gcf() , animate, blit=False, frames= 200, interval = 100)
plt.show()

    
 

