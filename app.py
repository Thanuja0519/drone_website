import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import random

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Drone Telemetry Dashboard"

app.layout = html.Div([
    html.Div([
        html.Img(src="https://cdn.pixabay.com/photo/2020/05/03/15/03/drone-5120465_1280.jpg",
                 style={"width": "100%", "maxHeight": "300px", "objectFit": "cover"})
    ]),
    html.H1("Real-Time Drone Telemetry Dashboard", className="text-center my-4"),

    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Img(src="https://img.icons8.com/ios-filled/50/battery.png", height="30px"),
                    html.Span(" Battery Voltage")
                ]),
                daq.Gauge(
                    id='battery',
                    min=0,
                    max=12,
                    value=7,
                    label='Volts',
                    color={"gradient": True, "ranges": {"green": [6, 9], "yellow": [4, 6], "red": [0, 4]}}
                )
            ], width=4),

            dbc.Col([
                html.Div([
                    html.Img(src="https://img.icons8.com/ios-filled/50/thermometer.png", height="30px"),
                    html.Span(" Temperature")
                ]),
                daq.Thermometer(
                    id='temp',
                    min=0,
                    max=100,
                    value=25,
                    showCurrentValue=True,
                    units="C"
                )
            ], width=4),

            dbc.Col([
                html.Div([
                    html.Img(src="https://img.icons8.com/ios-filled/50/mountain.png", height="30px"),
                    html.Span(" Altitude")
                ]),
                daq.Gauge(
                    id='altitude',
                    min=0,
                    max=500,
                    value=100,
                    label='meters',
                    color={"gradient": True, "ranges": {"green": [0, 250], "yellow": [250, 400], "red": [400, 500]}}
                )
            ], width=4)
        ], className="mb-5"),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Img(src="https://img.icons8.com/ios/50/gyroscope.png", height="30px"),
                    html.Span(" IMU Orientation")
                ]),
                dcc.Graph(id='imu')
            ], width=6),

            dbc.Col([
                html.Div([
                    html.Img(src="https://img.icons8.com/ios-filled/50/marker.png", height="30px"),
                    html.Span(" GPS Location")
                ]),
                dcc.Graph(id='gps')
            ], width=6)
        ]),

        html.Div([
            html.Div([
                html.Img(src="https://img.icons8.com/ios-filled/50/wifi.png", height="30px"),
                html.Span(" Connection Health")
            ]),
            html.Div(id='connection-health', className='h4')
        ], className="text-center mt-5")
    ])
])

@app.callback(
    Output('battery', 'value'),
    Output('temp', 'value'),
    Output('altitude', 'value'),
    Output('imu', 'figure'),
    Output('gps', 'figure'),
    Output('connection-health', 'children'),
    Input('battery', 'id')
)
def update_metrics(_):
    battery = round(random.uniform(5.0, 11.5), 2)
    temp = round(random.uniform(20.0, 90.0), 1)
    altitude = round(random.uniform(50, 450), 1)

    imu_fig = go.Figure()
    imu_fig.add_trace(go.Scatter3d(
        x=[0, random.uniform(-1, 1)],
        y=[0, random.uniform(-1, 1)],
        z=[0, random.uniform(-1, 1)],
        mode='lines+markers',
        line=dict(width=8),
        marker=dict(size=5)
    ))
    imu_fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        height=300,
        scene=dict(
            xaxis_title='Roll',
            yaxis_title='Pitch',
            zaxis_title='Yaw'
        )
    )

    gps_fig = go.Figure(go.Scattermapbox(
        lat=[random.uniform(12.9, 13.1)],
        lon=[random.uniform(80.1, 80.3)],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14)
    ))
    gps_fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=13.0, lon=80.2),
            zoom=10
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=300
    )

    connection_health = random.choice(["✅ Good", "⚠️ Poor"])
    return battery, temp, altitude, imu_fig, gps_fig, connection_health

if __name__ == '__main__':
    app.run_server(debug=True)
