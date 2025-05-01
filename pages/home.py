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
import time

dash.register_page(__name__, path='/')

df_pl = pl.read_csv("assets/Portfolio_prices.csv")

layout = html.Div([
    html.Div([
        html.H1('Home Page'),
        html.Div([
            # Botão para importar dataframe
            dmc.MantineProvider(
                dmc.Button(
                    children='Importar DataFrame',
                    id='import-button-home',
                    size='md',
                    rightSection=DashIconify(icon="flat-color-icons:checkmark"),
                    variant="outline",
                    color="green"
                )
            ),
            html.Div(id='import-output-home', style={'margin-top': '10px'}),
        ]),
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
                        id='btn-home',
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

# time.sleep(2)

@callback(
    Output('store-original-data-home', 'data'),
    Output('import-output-home', 'children'),
    Input('import-button-home', 'n_clicks'),
    prevent_initial_call=True
)
def import_dataframe(n_clicks):
    print("Importando DataFrame...")
    df = pd.read_csv('assets/Portfolio_prices.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Ticker'] = df['Ticker'].astype(str)
    df = df.loc[:, ['Date', 'Ticker', 'Close']]
    data = df.to_dict(orient='records')
    texto = f"DataFrame importado com sucesso! {len(data)} linhas."
    print(texto)
    logging.info(texto)
    return data, texto


@callback(
    Output('memory-table-ag', 'rowData'),
    Output('memory-table-ag', 'columnDefs'),
    Output('store-edited-data-home', 'data'),
    Input('store-df-data-home', 'data'),
    Input('btn-home', 'n_clicks'),
    State('select-ticker-home', 'value'),
    State('number-input-home', 'value'),
    prevent_initial_call=True
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
    Input("icon-container", "className"),
)
def update_icon(value, classname):
    print(classname)
    try:
        value = int(value)
        if value is None:
            return "icon-neutral", "line-md:arrow-right-circle" 
        elif classname == "icon-neutral" and value > 0:
            return "icon-up", "line-md:arrow-down-circle"
        elif classname == "icon-neutral" and value < 0:
            return "icon-down", "line-md:arrow-up-circle" 
        elif classname == "icon-down" and value == 0:
            return "icon-down-neutral", "line-md:arrow-up-circle"
        elif classname == "icon-up" and value == 0:
            return "icon-neutral", "line-md:arrow-right-circle" 
        elif classname == "icon-up" and value < 0:
            return "icon-down", "line-md:arrow-up-circle" 
        elif classname in ["icon-down", "icon-down-neutral"] and value > 0:
            return "icon-up", "line-md:arrow-down-circle"
        elif value == 0:
            return "icon-neutral", "line-md:arrow-right-circle" 
        elif value > 0:
            return "icon-up", "line-md:arrow-down-circle"
        elif value < 0:
            return "icon-down", "line-md:arrow-up-circle"
        else:
            return "icon-neutral", "line-md:arrow-right-circle"
    except ValueError:
        return "icon-neutral", "line-md:arrow-right-circle"