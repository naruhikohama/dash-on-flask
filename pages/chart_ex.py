import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc

import pandas as pd
import polars as pl
import plotly.express as px
import logging
import dash_mantine_components as dmc

from utils import *

dash.register_page(__name__, title='Chart Example', path='/chart_ex')



df_pl = pl.read_csv("assets/Portfolio_prices.csv")

print(df_pl.head())

layout = (
        html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='store-fig1', storage_type='session'),
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
            ]),
            dbc.Col([
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed=df_pl['Date'].min(),
                    max_date_allowed=df_pl['Date'].max(),
                    # initial_visible_month=df_pl['Date'].max(),
                    start_date=df_pl['Date'].min(),
                    end_date=df_pl['Date'].max(),
                    persistence=True,
                    persistence_type='session'
                ),
            ])
        ]),

        html.Br(),

        dbc.Checklist(
            options=[
                {"label": "Gráfico 1", "value":1}],
            id="btn-grafico1",
            value=[],
            switch=True,
            persistence=True,
            persistence_type='session',
        ),

        html.Br(),

        dbc.Collapse(
            html.Div([
                dcc.Graph(
                    id='example-graph', 
                    style={'height': '25vh', 'width': '80%', 'border-radius': '10px'},
                    config={'displayModeBar': False}),
            ],
            className="outro"),
            id="collapse-grafico1",
            # is_open=False,
        ),

        html.Br(),

        dbc.Accordion(
            [
                dbc.AccordionItem(
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                dcc.DatePickerSingle(
                                    id='date-picker-single-start',
                                    min_date_allowed=df_pl['Date'].min(),
                                    max_date_allowed=df_pl['Date'].max(),
                                    initial_visible_month=df_pl['Date'].max(),
                                    persistence=True,
                                    persistence_type='session'
                                )
                            ]),
                            dbc.Col([
                                dcc.DatePickerSingle(
                                    id='date-picker-single-end',
                                    min_date_allowed=df_pl['Date'].min(),
                                    max_date_allowed=df_pl['Date'].max(),
                                    initial_visible_month=df_pl['Date'].max(),
                                    persistence=True,
                                    persistence_type='session'
                                )
                            ]),
                        ]),
                        html.Br(),
                        
                        dcc.Graph(
                            id='example-graph-2',
                            style={'height': '25vh', 'width': '80%', 'border-radius': '10px'},
                            config={'displayModeBar': False}
                        ),
                    ]),
                    title="Gráfico 2",
                ),
            ], 
            start_collapsed=True,
            id="accordion-fig2",
            always_open=True, 
            persistence=True,
            persistence_type='session',


        ),
    ])
)


@callback(
    Output("store-df-data-home", "data"),
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
    Input("btn-grafico1", "value"),
    State("collapse-grafico1", "is_open")
)
def toggle_callapse_grafico1(value, is_open):
    return value == [1]


@callback(
    Output('example-graph', 'figure'),
    Input('store-df-data-home', 'data'),
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
    print("UPDATING CHART")
    return fig1

@callback(
    Output('example-graph-2', 'figure'),
    Input('store-df-data-home', 'data'),
    Input('date-picker-single-start', 'date'),
    Input('date-picker-single-end', 'date'),
)
def update_graph_2(dados, start_date, end_date):
    if dados is None:
        return no_update
    dff = pd.DataFrame(dados)
    start_date = dff['Date'].min() if start_date is None else start_date
    end_date = dff['Date'].max() if end_date is None else end_date
    tickers = dff['Ticker'].unique().tolist()

    fig2 = finance_line(
        dff, 
        start_date=start_date, 
        end_date=end_date, 
        tickers=tickers
    )
    print("UPDATING CHART 2")
    return fig2