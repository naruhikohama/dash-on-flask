import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc

import pandas as pd
import polars as pl
import plotly.express as px
import logging

from utils import *

dash.register_page(__name__, title='Chart Example', path='/chart_ex')

df_pl = pl.read_csv("assets/Portfolio_prices.csv")

print(df_pl.head())

layout = html.Div([
    dcc.Store(id='store-df-data', storage_type='session'),
    dcc.Store(id='store-date', storage_type='session'),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="select-ticker",
                options=[{"label": i, "value": i} for i in df_pl['Ticker'].unique()],
                value=["AAPL", "MS"],
                multi=True,
                placeholder="Select Tickers",
                persistence=True,
                persistence_type='session'
            ),
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=df_pl['Date'].min(),
                max_date_allowed=df_pl['Date'].max(),
                initial_visible_month=df_pl['Date'].max(),
                start_date=df_pl['Date'].min(),
                end_date=df_pl['Date'].max(),
                persistence=True,
                persistence_type='session'
            ),
        ])
    ]),

    html.Br(),

    dbc.Button(
        "Gráfico",
        id="btn-grafico1",
        color="light",
        n_clicks=0
    ),

    html.Br(),

    dbc.Collapse(
        html.Div([
            dcc.Graph(id='example-graph', config={'displayModeBar': False}),
        ],
        className="outro"),
        id="collapse-grafico1",
        is_open=False,
    ),

    html.Br(),

    html.Div([
        dcc.Graph(
            id='example-graph2',
            figure={
                'data': [{'x': [1, 2, 3], 'y': [2, 1, 4], 'type': 'line', 'name': 'SF'}],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ]),
])

@callback(
    Output("store-df-data", "data"),
    Input("select-ticker", "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
)
def filter_data(tickers, start_date, end_date):
    logging.info(f"Tickers: {tickers}, Start Date: {start_date}, End Date: {end_date}")
    if not tickers:
        raise dash.exceptions.PreventUpdate
            
    df = (
        df_pl
        .filter(
            (pl.col("Ticker").is_in(tickers)) &
            (pl.col("Date") >= start_date) &
            (pl.col("Date") <= end_date)
        )
        .to_pandas()
    )

    return df.to_dict(orient='records')

@callback(
    Output("collapse-grafico1", "is_open"),
    Input("btn-grafico1", "n_clicks"),
    State("collapse-grafico1", "is_open")
)
def toggle_callapse_grafico1(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output('example-graph', 'figure'),
    Input('store-df-data', 'data')
)

def update_graph(dados):
    if dados is None:
        return no_update
    dff = pd.DataFrame(dados)
    start_date = dff['Date'].min()
    end_date = dff['Date'].max()
    tickers = dff['Ticker'].unique().tolist()

    fig1 = finance_line(
        dff, 
        start_date=start_date, 
        end_date=end_date, 
        tickers=tickers
    )
    return fig1
