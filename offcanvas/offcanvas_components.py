from dash import dcc, html
import dash_bootstrap_components as dbc

from global_structures import nav_link_titles
from offcanvas.offcanvas_descriptions import intro

# dynamically generate the nav links in the menu using the nav_link_titles list in global_structures.py
nav_link_list = [
    dbc.NavLink(
        children = f'{title.upper().replace("_", " ")}',
        id=f'{title}_nav_link',
        href=f'/{title}',
        n_clicks=0,
        style={'fontWeight':'bold', 'fontSize':'18px','textAlign': 'left', 'color': 'white'})

    for title in nav_link_titles
]

# insert the intro into the nav_link_list
nav_link_list.extend([html.Br(),html.Br(),html.Br(), html.Br(), intro])

offcanvas = dbc.Container([

    #provides URL information to the app, enabling conditional rendering of different 'pages' based on the route.
    dcc.Location(id='url', refresh=False),
    dbc.Button(
        'Menu',
        id = 'menu_button',
        n_clicks = 0,
        className='custom-hover-effect3',
        style={'transform': 'rotate(90deg)' ,'position': 'absolute' ,'left': -10}),

    dbc.Offcanvas(id = 'oc',
                  is_open = False,

                # add the nav links and intro to the offcanvas
                  children = nav_link_list,
                  style = {'backgroundColor':'black'})



])

#print([link for link in nav_link_list])