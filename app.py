import dash_bootstrap_components as dbc
from dash import Dash, html
from layout import navigation_menu, tab_content
from callbacks import activate_tab_content, multi_page_navigation
from callbacks import time_series_graph, dashboard_data_tables

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = dbc.Container([

    # OffCanvas with NavLinks
    navigation_menu,

    # Create space between nav_menu and page content
    html.Br(),
    html.Br(),
    html.Br(),

    # tabular
    dbc.Container(id ='page_content')
], fluid = True)


if __name__ == '__main__':
    app.run_server(debug = True)

