import dash
from dash import html, dcc, callback, Output, Input, dash_table, State, MATCH, clientside_callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import logging
import dash_ag_grid as dag
import pandas as pd
from utils import *

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
    html.Br(),
    dbc.Row([
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
        ]),
        dbc.Col([
            dmc.MantineProvider(
                dmc.NumberInput(
                    id='number-input-home',
                    suffix='%',
                    persistence = True,
                    persistence_type = 'session'
                )
            )
        ]),
        dbc.Col ([
            dmc.MantineProvider(
                dmc.Button(
                    children='Atualizar',
                    id='button-home',
                    rightSection=DashIconify(icon="flat-color-icons:checkmark"),
                    variant="outline",
                    color="green"
                )
            )
        ])
    ]),
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
    
    myCard_collapse(
        title="Teste Card",
        children=[
            html.Div("This is a test card"),
            html.Div("This is a test card"),
            html.Div("This is a test card"),
            html.Div("This is a test card"),
        ]
    )

],
className="main")

@callback(
    Output('memory-table-ag', 'rowData'),
    Output('memory-table-ag', 'columnDefs'),
    Output('store-edited-data-home', 'data'),
    Input('button-home', 'n_clicks'),
    Input('store-original-data-home', 'data'),
    State('select-ticker-home', 'value'),
    State('number-input-home', 'value')
)
def update_table_ag(data, n, ticker, factor):
    logging.info(f"Data received in update_table_ag: {data}")
    if data is None:
        raise dash.exceptions.PreventUpdate
    
    fator_correcao = (100 + fator) / 100
    df = pd.DataFrame(data)
    df = (
        df
        .loc[:, ['Date', 'Ticker', 'Close']]
        .query('Ticker == "ticker"')
        .assign(
            Close = lambda dff: dff['Close']*fator_correcao
        )
    )

    columnDefs = [
        {'headerName': 'Date', 'field': 'Date'},
        {'headerName': 'Ticker', 'field': 'Ticker'},
        {'headerName': 'Close', 'field': 'Close'}
    ]
    return df.to_dict('records'), columnDefs, df.to_dict(orient='records')

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


clientside_callback("""
                    function(clicks, is_open) {
                        if (clicks>0) {
                            return !is_open;
                        } else {
                            throw window.dash_clientside.PreventUpdate;        
                        }
                    }""",
                    Output({"type":'collapsewin','id':MATCH},'is_open'),
                    Input({'type':'collapsebutt','id':MATCH}, 'n_clicks'),
                    State({"type":'collapsewin','id':MATCH},'is_open')
                    )
    
clientside_callback("""
                    function(is_open) {
                        if (is_open==true) {
                            return "fa fa-minus";
                        } else {
                        return "fa fa-plus";
                        }
                    }""",
                    Output({'type':'collapseicon','id':MATCH}, 'className'),
                    Input({"type":'collapsewin','id':MATCH},'is_open')
    )