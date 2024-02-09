import dash_bootstrap_components as dbc
from dash import dcc, dash_table, html

#import pre-defined css styles from the style.py for the cards, dash_tables, and dropdowns
from styles import card_header_style, card_style
from styles import header_style_dash, table_style, cell_style_non_url
from styles import dropdown_style, html_dropdown_style

surface_detail_card = dbc.Card([
    dbc.CardHeader('SURFACE DETAIL',
                   style = card_header_style
                   ),
    dbc.CardBody([
        html.P(
            children="Select a section of the App Store for detailed insights on user journey to your app listing:",
            style= html_dropdown_style
        ),
        dcc.Dropdown(
            id = 'detail_select_surface_type',

            options = ['app_details',
                       'category',
                       'home',
                       'marketing',
                       'partners',
                       'search_ad'],

            value = 'app_details',
            style = dropdown_style
        ),

        html.P(
            children='Sort this detail by selecting a metric:',
            style= html_dropdown_style
        ),

        dcc.Dropdown(
            id='sort_surface_detail',
            options= ['totalUsers', 'conversions', 'conversion_rate'],
            value='totalUsers',
            style = dropdown_style
        ),
        dash_table.DataTable(
            id = 'surface_detail_table',
            style_header = header_style_dash,
            style_cell= cell_style_non_url,
            style_table= table_style
        )
    ])
],style = card_style)