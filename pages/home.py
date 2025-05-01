import dash
from dash import html, dcc, callback, Output, Input, dash_table, State, MATCH, clientside_callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import logging
import dash_ag_grid as dag
import pandas as pd
import polars as pl
from utils import *

dash.register_page(__name__, path='/')

layout = html.Div([
    dbc.Container([
        html.H1('This is our Home page'),
        html.Div('This is our Home page content.'),
        html.Br(),
        dbc.Container([
            dbc.Col([
                dcc.Dropdown(
                id="select-ticker-home",
                # options=,
                # value=["AAPL", "MS"],
                multi=False,
                placeholder="Select Tickers",
                persistence=True,
                persistence_type='session'
                ),
            ], className="col col-lg-2"),
            dbc.Col([
                dmc.MantineProvider([
                    dmc.NumberInput(
                        id="number-input-home",
                        label="",
                        value=0,
                        size='md',
                        step=1,
                        min=-100,
                        max=100,
                        suffix="%",
                        hideControls=False,
                        leftSection=html.Div(
                            DashIconify(icon="ph:circle-fill", width=18, id="dynamic-icon"),
                            id="icon-container",
                            className="icon-neutral",
                        ),
                        style={"width": 110},
                    ),
                ])
            ], className="col-md-auto"),
            dbc.Col ([
                dmc.MantineProvider(
                    dmc.Button(
                        children='Atualizar',
                        id='button-home',
                        size='md',
                        rightSection=DashIconify(icon="flat-color-icons:checkmark"),
                        variant="outline",
                        color="green"
                    )
                )
            ], className="col-md-auto"),
        ], className="row justify-content-md-center"),
        dag.AgGrid(
            id='memory-table-ag',
            defaultColDef={
                'sortable': True,
                'filter': True,
                'resizable': True,
                'flex': 1,
            },
            style={'height': '400px', 'width': '80%'}
        ),
    ]),
],
className="",)

@callback(
    Output('memory-table-ag', 'rowData'),
    Output('memory-table-ag', 'columnDefs'),
    Output('store-edited-data-home', 'data'),
    Input('store-original-data-home', 'data'),
    Input('button-home', 'n_clicks'),
    State('select-ticker-home', 'value'),
    State('number-input-home', 'value')
)
def update_table_ag(data, n, ticker, fator):
    logging.info(f"Data received in update_table_ag: {data}")
    if data is None:
        raise dash.exceptions.PreventUpdate
    
    fator_correcao = (100 + fator) / 100
    df = pd.DataFrame(data)
    df = (
        df
        .loc[:, ['Date', 'Ticker', 'Close']]
        .query('Ticker == @ticker')
        .assign(
            Close = lambda dff: dff['Close']*fator_correcao
        )
    )

    print(pl.from_pandas(df).head())

    columnDefs = [
        {'headerName': 'Date', 'field': 'Date'},
        {'headerName': 'Ticker', 'field': 'Ticker'},
        {'headerName': 'Close', 'field': 'Close'}
    ]
    return df.to_dict(orient='records'), columnDefs, df.to_dict(orient='records')

@callback(
    Output("select-ticker-home", 'options'),
    Input("store-df-data-home", "data")
)
def update_tickers(data):
    logging.info(f"Data received in update_tickers: {data}")
    if data is None:
        raise dash.exceptions.PreventUpdate
    df = pd.DataFrame(data)
    df = df.loc[:, ['Date', 'Ticker', 'Close']]
    tickers = df['Ticker'].unique()
    options = [{'label': ticker, 'value': ticker} for ticker in tickers]
    return options

@callback(
    Output("icon-container", "className"),
    Output("dynamic-icon", "icon"),
    Input("number-input-home", "value"),
)
def update_icon(value):
    if value is None or value == 0:
        return "icon-neutral", "line-md:arrow-right-circle" 
    elif value > 0:
        return "icon-up", "line-md:arrow-down-circle"
    else:
        return "icon-down", "line-md:arrow-up-circle" 