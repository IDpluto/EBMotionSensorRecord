import serial
import math
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen = 20)
X.append(1)

Y = deque(maxlen = 20)
Y.append(1)

Z =deque(maxlen = 0)
Z.append(1)


grad2rad = 3.141592/180.0
rad2grad = 180.0/3.141592
cos = math.cos


ser = serial.Serial('/dev/ttyUSB0', 115200)

app = dash.Dash(__name__)

app.layout = html.Div(
	[
		dcc.Graph(id = 'live-graph', animate = True),
		dcc.Interval(
			id = 'graph-update',
			interval = 1000,
			n_intervals = 0
		),
	]
)

@app.callback(
	Output('live-graph', 'figure'),
	[ Input('graph-update', 'n_intervals') ]
)
def save_data(sensor_id, roll, pitch, yaw, acc_x, acc_y, acc_z):

    if (sensor_id == 1 ): 
        roll_r = "%.2f" %(roll*rad2grad)
        pitch_r = "%.2f" %(pitch*rad2grad)
        yaw_r = "%.2f" %(yaw*rad2grad)
    else:
        if (sensor_id == 0):
            roll_l = "%.2f" %(roll*rad2grad)
            pitch_l = "%.2f" %(pitch*rad2grad)
            yaw_l = "%.2f" %(yaw*rad2grad)
    X.append(roll_r)
    Y.append(pitch_r)
    data = plotly.graph_objs.Scatter(
			x=list(X),
			y=list(Y),
			name='Scatter',
			mode= 'lines+markers'
	    )
    return {'data': [data],
			'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}
            

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

def update_graph_scatter(n):
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
        
            text = words[0][-1:]
            save_data(text, roll, pitch, yaw,acc_x, acc_y, acc_z)



if __name__ == '__main__':
    
	app.run_server()
