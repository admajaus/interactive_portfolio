from dash import html, Input, Output, callback, State

#import the layout for different sections of the app
from layout import tabs, tab_content
from layout import dashboard, contact_me, about_me_page


# Callback: Offcanvas, Button, Location--------------------------------------------
# open and close the menu based interactions with the menu button
@callback(Output('oc', 'is_open'),
          [Input('menu_button', 'n_clicks')],
            [Input("url", "pathname")],
          State('oc', 'is_open'))

def toggle_offcanvas(n_clicks, pathname, is_open):
    if n_clicks or pathname:
        return not is_open
    else:
        return is_open

# MULTI-PAGE NAVIGATION callback------------------------------------------
# render different page content based on the navlink selected from the menu and it's url
@callback(Output('page_content', 'children'),
          Input('url', 'pathname')
          )
def render_page(pathname):
        if pathname == '/tabular':
            return tabs, tab_content

        elif pathname == '/dashboard':
            return dashboard

        elif pathname == '/contact':
            return contact_me

        else:
            return about_me_page
