import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, title='Chart Example', path='/chart_ex')

layout = html.Div([
    dbc.Button(
        "Gráfico",
        id="grafico1",
        color="light",
        n_clicks=0
    ),
    dbc.Collapse(

        html.Div([
            dcc.Graph(
            id='example-graph',
            figure={
                'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'}],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
            )
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
    Output("collapse-grafico1", "is_open"),
    Input("grafico1", "n_clicks"),
    State("collapse-grafico1", "is_open")
)
def toggle_callapse_grafico1(n, is_open):
    if n:
        return not is_open
    return is_open

