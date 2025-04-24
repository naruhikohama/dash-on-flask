import dash
from dash import html, dcc, callback, Output, Input, dash_table, State
import logging
import dash_ag_grid as dag
import pandas as pd

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
    dash_table.DataTable(
        id='memory-table',
        page_action='native',
        fixed_rows={'headers': True},
        style_table={'overflowX': 'auto', 'height': '400px'},
        style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto'},
    ), 
    html.Br(),
    dag.AgGrid(
        id='memory-table-ag',
        defaultColDef={
            'sortable': True,
            'filter': True,
            'resizable': True,
            'flex': 1,
        },
        style={'height': '400px', 'width': '80%'}
    )
],
className="main")

@callback(
    Output('memory-table', 'data'),
    Output('memory-table', 'columns'),
    Input('store-df-data-home', 'data')
)
def update_table(data):
    logging.info(f"Data received in update_table: {data}")
    if data is None:
        raise dash.exceptions.PreventUpdate
    df = pd.DataFrame(data)
    df = df.loc[:, ['Date', 'Ticker', 'Close']]
    columns = [{'name': col, 'id': col} for col in df.columns]
    return df.to_dict('records'), columns

@callback(
    Output('memory-table-ag', 'rowData'),
    Output('memory-table-ag', 'columnDefs'),
    Input('store-df-data-home', 'data')
)
def update_table_ag(data):
    logging.info(f"Data received in update_table_ag: {data}")
    if data is None:
        raise dash.exceptions.PreventUpdate
    df = pd.DataFrame(data)
    df = df.loc[:, ['Date', 'Ticker', 'Close']]
    columnDefs = [
        {'headerName': 'Date', 'field': 'Date'},
        {'headerName': 'Ticker', 'field': 'Ticker'},
        {'headerName': 'Close', 'field': 'Close'}
    ]
    return df.to_dict('records'), columnDefs