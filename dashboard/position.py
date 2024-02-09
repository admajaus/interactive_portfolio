import dash_bootstrap_components as dbc
from dash import dcc, dash_table, html

# import css styles for the cards(containers), dash_tables, and dropdown components
from styles import card_header_style, card_style
from styles import header_style_dash, cell_style, table_style
from styles import dropdown_style, html_dropdown_style


position_card = dbc.Card([
    dbc.CardHeader('POSITION',
                   style = card_header_style
                   ),
    dbc.CardBody([
        html.P('Select a section of the App Store:',
               style = html_dropdown_style
               ),
        dcc.Dropdown(
            id='position_select_surface_type',
            options=[
                'app_details',
                'category',
                'home',
                'marketing',
                'partners',
                'search',
                'search_ad'],

            value='search',
            style = dropdown_style
        ),

        html.P('Select the position type:',
               style=html_dropdown_style
               ),

        dcc.Dropdown(
            id = 'select_position',
            options = ['surface_inter_position', 'surface_intra_position'],
            value = 'surface_inter_position',
            style = dropdown_style
        ),

        html.P('Sort the table by selecting a metric :',
               style=html_dropdown_style
               ),

        dcc.Dropdown(
            id='sort_position',
            options= ['totalUsers', 'conversions', 'conversion_rate'],
            value='totalUsers',
            style = dropdown_style
        ),
        dash_table.DataTable(
            id = 'position_table',
            style_header = header_style_dash,
            style_cell= cell_style,
            style_table= {
                'height': '335px',
                'overflowY': 'scroll',
}
        )
    ])
],style = card_style)