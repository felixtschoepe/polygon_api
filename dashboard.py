# %%
# Librarys laden
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Zoetis Inc. Daten'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider',
                    'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id='graph'),
])


@app.callback(
    Output('graph', 'figure'),
    Input("toggle-rangeslider", 'value'))
def display_candlestick(value):
    df = pd.read_csv('data/datasets/ZTS.csv')
    fig = go.Figure(go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    ))

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return fig

app.run_server(debug=True) 

# %%
