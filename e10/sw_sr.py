import dash
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
import time
import serial_read

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    daq.BooleanSwitch(
        id='my-boolean-switch',
        on=False
    ),
    html.Div(id='boolean-switch-output'),
    html.Button(id='button',n_clicks=0,style={'display': 'none'}),
    html.Div(id='dummy-div',style={'display':'none'})
])

@app.callback(
    [Output('boolean-switch-output', 'children'),
     Output('button','n_clicks')],
    [Input('my-boolean-switch', 'on')])
def update_output(on):
    if on:
        n=1
    else:
        n=0
    output_string = 'The switch is {}.'.format(on)
    return (output_string,n)

@app.callback(
    Output('dummy-div','children'),
    [Input('button','n_clicks')]
)
def read_serial_data(n):
    try:
        if n==0:
            raise KeyboardInterrupt
        serial_read.save_serial_data('data/test3.csv','foo',n)
        return None
    except:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)