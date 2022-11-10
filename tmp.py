from dash import Dash, Input, Output, State, html, dcc, no_update
import dash_mqtt
import plotly.graph_objects as go
from collections import deque
import json
import pandas as pd

TEST_SERVER = 'my_sever'
TEST_SERVER_PORT = 8883
TEST_SERVER_PATH = None
MESSAGE_OUT_TOPIC = 'Notification'
MESSAGE_IN_TOPIC = 'home/dht12_state'
Q = deque(maxlen=60)

app = Dash(__name__)

app.layout = html.Div([
    html.H1('MQTT Thermo-hygrometer'), 
    fig := dcc.Graph(), 
    ipt := dcc.Input(placeholder='message to send',
              debounce=True), btn := html.Button('Send'),
    dash_mqtt.DashMqtt(id='mqtt',
                       broker_url=TEST_SERVER,
                       broker_port=TEST_SERVER_PORT,
                       broker_path=TEST_SERVER_PATH,
                       topics=[MESSAGE_IN_TOPIC])
])


@app.callback(Output('mqtt', 'message'), Input(btn, 'n_clicks'),
              State(ipt, 'value'))
def display_output(n_clicks, message_payload):
    if n_clicks:
        return {'topic': MESSAGE_OUT_TOPIC, 'payload': message_payload}
    return no_update


@app.callback(Output(fig, 'figure'), Input('mqtt', 'incoming'))
def update_fig(incoming_message):
    if (incoming_message):
        msg = json.loads(incoming_message['payload'])
        msg['time'] = pd.Timestamp(*msg['time'][:-2])

        Q.append(msg)

        df = pd.DataFrame(data=Q, columns=["humidity", "temperature", "time"])

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(x=df['time'],
                       y=df["humidity"],
                       mode='lines',
                       name='humidity'))

        fig.add_trace(
            go.Scatter(x=df['time'],
                       y=df["temperature"],
                       mode='lines+markers',
                       name='temperature'))

        fig.update_layout(xaxis=dict(range=[
            df['time'].max() - pd.Timedelta(5, unit='min'), df['time'].max()
        ]))

        return fig

    else:
        return no_update


if __name__ == "__main__":
    app.run_server(debug=True)