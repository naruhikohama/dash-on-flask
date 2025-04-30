from flask import Flask
from dash import Dash, html, dcc, callback, Output, Input, page_container, clientside_callback, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

server = Flask(__name__)

@server.route('/teste')
def index():
    return "Welcome to the Flask app!"

app = Dash(
    __name__, 
    use_pages = True, 
    server=server, 
    url_base_pathname='/',
    external_stylesheets=[dbc.themes.MATERIA, dmc.styles.DATES],
    external_scripts=[
        # "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
        # "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/ru.min.js"
    ],
    suppress_callback_exceptions=True)

nav_contents =[
    dbc.NavItem(html.Img(src=app.get_asset_url('forecast-icon1.png'), id='navbar-img')),
    dbc.NavItem(dbc.NavLink("Home", href="/", className="navlink-custom")),
    dbc.NavItem(dbc.NavLink("Analytics", href="/analytics", className="navlink-custom")),
    dbc.NavItem(dbc.NavLink("Chart Example", href="/chart_ex", className="navlink-custom")),
]


app.layout = html.Div([
    dcc.Store(id='store-df-data-home', storage_type='session'),
    html.Div(
        [
            dbc.Navbar(
                [
                    dbc.Nav(
                        nav_contents,
                        pills=True, 
                        navbar=True,
                        id="navbar-contents",
                    ),
                ],
                id="navbar",
                # className="translate-middle",
            ),
        ],
        className="col-6 start-50",
    ),
    html.Div([], id="horizontal-line"),
    html.Br(),
    html.Div([page_container])
],
className="main"
)

if __name__ == '__main__':
    app.run_server(debug=True)