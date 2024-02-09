import dash_bootstrap_components as dbc
from dash import html

# import all the containers containing dash components and html elements for the offcanvas menu, tabular, dashboard, contact form, and about me
from offcanvas.offcanvas_components import offcanvas

from tabular.tab_universal_components import tabular_dcc_tabs
from tabular.tab_html_elements import tabular_title, tabular_subtitle

from dashboard.channel_group import channel_group_card
from dashboard.surface_type import surface_type_card, time_series_card
from dashboard.keywords import wordcloud_card, keyword_table_card
from dashboard.surface_detail import surface_detail_card
from dashboard.position import position_card

from contact_about_me.jotform_iframe import contact_form_iframe
from contact_about_me.about_me import about_me_title, about_me_subtitle, about_me_blurb

# create a responsive layout by assigning grid dimensions to the layout based on viewport size
responsive_style = {
    "xs": 12,
    "sm": 12,
    "md": 6,
    "lg": 6,
    "xl": 6
}

navigation_menu = offcanvas

# add the tabs and titles into a grid layout
tabs = dbc.Row([tabular_title, tabular_subtitle, tabular_dcc_tabs])

# renders tab content based on tabular.
# tabs(1-7) activated on click thru callbacks.activate_selected_tab
tab_content = dbc.Container(dbc.Row(id='display_tab_content'))

# add all dashboard cards(containers) into a grid layout
dashboard = dbc.Container([

    dbc.Row(html.H1('DASHBOARD')),

    dbc.Row(html.H4('App Listing Analytics')),

    dbc.Card([
        dbc.Row([
            dbc.Col(channel_group_card,width = 6, **responsive_style),

            dbc.Col(surface_type_card, width = 6, **responsive_style),

        ], style={'marginBottom': '20px'}),

        dbc.Row(
            dbc.Col(
                time_series_card
            ), style={'marginBottom': '20px'}
        ),

        dbc.Row([
            dbc.Col(wordcloud_card,width = 6, **responsive_style),

            dbc.Col(keyword_table_card, width = 6, **responsive_style)

        ], style={'marginBottom': '20px'}),

        dbc.Row([
            dbc.Col(
                surface_detail_card,
                width = 6, **responsive_style
            ),
            dbc.Col(position_card,
                width = 6, **responsive_style
            )
        ])

        ], style={'border': '4px double black',
              'padding': '20px'
              }
    )
    #container will expand or contract with the browser window, creating a more responsive dashboard that fills the available space.
], fluid=True)

# add the contact form to the grid layout
# DO NOT as responsive styling - this has unforseen affects on this form
contact_me = dbc.Row(dbc.Col(contact_form_iframe))

# add the about_me_page to a grid layout, include responsiveness
about_me_page = dbc.Container([
    dbc.Row(about_me_title),
    dbc.Row([
        dbc.Col(
            html.Div(
                html.Img(
                    src ='assets/font_end_dev.jpg',
                    style={'maxWidth': '100%', 'height': '100%'}
                )
            )
            ,width = 5,
            **responsive_style
        ),
        dbc.Col([
            about_me_subtitle,
            about_me_blurb],
            style={'maxWidth': '100%', 'height': '100%'},
            width = 7,
            **responsive_style
        )
    ])
])
