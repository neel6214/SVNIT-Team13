import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv("StockListCSV.csv")
option=[]
arr = list(df['symbol'].unique())
for i in range(df.symbol.nunique()):
  option.append(dict({"label":arr[i],"value":arr[i]}))

print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Stocks", style={'text-align': 'center','font-family': 'verdana'}),

    dcc.Dropdown(id="slct_comp",
                 options=option,
                 multi=False,
                 value='AAPL',
                 style={'width': "40%"}
                 ),
    html.Br(),
    html.Div(id='output_container', children=[]),
    html.Br(),
    html.Div(id='ohlc_container', children=[]),
    dcc.Graph(id='ohlc', figure={}),
    html.Div(id='candlestick_container', children=[]),
    dcc.Graph(id='candlestick', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='ohlc_container', component_property='children'),
     Output(component_id='ohlc', component_property='figure'),
     Output(component_id='candlestick_container', component_property='children'),
     Output(component_id='candlestick', component_property='figure')],
    [Input(component_id='slct_comp', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The company chosen by user was: {}".format(option_slctd)
    container1 = "Ohlc Graph for {}".format(option_slctd)
    container2 = "Candlestick Graph for {}".format(option_slctd)
    
    dff = df.copy()
    y = dff[dff['symbol']==option_slctd]

    # Plotly Express
    fig = go.Figure(data=go.Ohlc(x=y['date'],
                    open=y['open'],
                    high=y['high'],
                    low=y['low'],
                    close=y['close']))
    fig1 = go.Figure(data=[go.Candlestick(x=y['date'],
                open=y['open'],
                high=y['high'],
                low=y['low'],
                close=y['close'])])


    return container, container1, fig, container2, fig1


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)