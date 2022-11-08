
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from pandas.core.indexes import interval

fig, (ax1, ax2) = plt.subplots(2,1) #, ax3, ax4) = plt.subplots(4,1)

roll_line1, = ax1.plot([],[], lw=2, color = 'red')
pitch_line1, = ax1.plot([], [], lw = 2, color = 'blue')
yaw_line1, = ax1.plot([], [], lw = 2, color = 'orange')
acx_line1, = ax2.plot([], [], lw = 2, color = 'red')
acy_line1, = ax2.plot([], [], lw = 2, color = 'blue')
acz_line1, = ax2.plot([], [], lw = 2, color = 'orange')
#roll_line2, = ax3.plot([], [], lw = 2, color = 'red')
#pitch_line2, = ax3.plot([], [], lw = 2, color = 'blue')
#yaw_line2, = ax3.plot([], [], lw = 2, color = 'orange')
#acx_line2, = ax4.plot([], [], lw = 2, color = 'red')
#acy_line2, = ax4.plot([], [], lw = 2, color = 'blue')
#acz_line2, = ax4.plot([], [], lw = 2, color = 'orange')

line = [roll_line1, pitch_line1, yaw_line1, acx_line1, acy_line1]#, acz_line1, roll_line2, pitch_line2, yaw_line2, acx_line2, acy_line2, acz_line2]




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
    
    line[0] .set_data(x_num, roll)
    line[1] .set_data(x_num, pitch)
    line[2] .set_data(x_num, yaw)
    line[3] .set_data(x_num, acc_x)
    line[4] .set_data(x_num, acc_y)
    line[5] .set_data(x_num, acc_z)

    return line
   

ani = animation.FuncAnimation(fig, animate, frames = 200, blit=True, interval=10,
    repeat=False)
plt.show()

    
 

