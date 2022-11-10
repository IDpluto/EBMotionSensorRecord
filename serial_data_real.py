import RPi.GPIO as GPIO
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random, time, spidev

spi=spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000

def ReadChannel(channel):
    adc=spi.xfer2([1,(8+channel)<<4,0])
    data=((adc[1]&3)<<8)+adc[2]
    return data
mcp3008_channel=0
fig = plt.figure()    
ax = plt.subplot(211, xlim=(0, 50), ylim=(0, 1024))
ax_2 = plt.subplot(212, xlim=(0, 50), ylim=(0, 512))

max_points = 50
max_points_2 = 50

line, = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='blue',ms=1)
line_2, = ax_2.plot(np.arange(max_points_2), 
                np.ones(max_points, dtype=np.float)*np.nan, lw=1,ms=1)

def animate(i):
    y = ReadChannel(mcp3008_channel)
    # y = random.randint(0,1000)
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)
    print(new_y)
    return line
    
def animate_2(i):
    y_2 = random.randint(0,512)
    old_y_2 = line_2.get_ydata()
    new_y_2 = np.r_[old_y_2[1:], y_2]
    line_2.set_ydata(new_y_2)
    print(new_y_2)
    return line_2


anim = animation.FuncAnimation(fig, animate ,interval = 10)
anim_2 = animation.FuncAnimation(fig, animate_2  , interval=10)
plt.show()