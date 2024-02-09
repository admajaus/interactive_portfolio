import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash import dcc, html
from dashboard.dashboard_pre_processing import surface_type_subset
from styles import card_header_style, card_style
from styles import html_dropdown_style, dropdown_style

# Bar Chart with Secondary Axis for Conversion Rate
surface_type_fig = make_subplots(specs=[[{"secondary_y": True}]])

# First set of bars represent totalUsers per channel group
surface_type_fig.add_trace(go.Bar(x=surface_type_subset['surface_type'],
                                  y=surface_type_subset['totalUsers'],
                                  name='Total Users'),
                           secondary_y=False)

# Second set of bars represent conversions per channel group
surface_type_fig.add_trace(go.Bar(x=surface_type_subset['surface_type'],
                                  y=surface_type_subset['conversions'], name='Conversions'),
                           secondary_y=False)

# Adding Conversion Rate per channel group as a line on secondary axis
surface_type_fig.add_trace(go.Scatter(x=surface_type_subset['surface_type'],
                                      y=surface_type_subset['conversion_rate'],
                                      name='Conversion Rate', mode='lines+markers'),
                           secondary_y=True)

# Set axis titles
surface_type_fig.update_xaxes(title_text="surface_type")
surface_type_fig.update_yaxes(title_text="totalUsers vs. conversions", secondary_y=False)
surface_type_fig.update_yaxes(title_text="conversion_rate", secondary_y=True)

# Updating layout to group bars side-by-side,
# autosize graph to fit in container
# prevent overlap between graph and container thru margin adjustment
# reduce font size for readability
# option to remove grid lines for secondary y axis
surface_type_fig.update_layout(
    title="Analyzing Engagement Across App Store Sections",
    barmode='group',
    autosize=True,
    margin=dict(l=50, r=50, t=50, b=50),
    font=dict(size=10),
    #yaxis2 = dict(showgrid=False)
)


surface_type_card = dbc.Card([
    dbc.CardHeader('SURFACE TYPE',
                   style = card_header_style
                   ),
    dbc.CardBody(
        dcc.Graph(
            figure = surface_type_fig,

            # fill the container with the graph by width and length
            style={'height': '100%',
                   'width': '100%'},
            # auto adjust whole graph to container size based on viewport size
            responsive=True
        )
    )
], style = card_style)

time_series_card = dbc.Card([

    dbc.CardHeader('TIME SERIES ANALYSIS: SURFACE TYPE',
                   style = card_header_style
                   ),

    dbc.CardBody([
        html.P(
            'Select an App Store Section to track engagement and conversions over time:',
            style = html_dropdown_style
        ),
        dcc.Dropdown(
            id ='time_series_dropdown',
            options = ['app_details', 'category', 'home', 'marketing', 'partners', 'search','search_ad'],
            value = 'app_details',
            style = dropdown_style
        ),

        dcc.Graph(

            id ="time_series",

          # fill the container with the graph by width and length
            style={'height': '400px',
                 'width': '100%'},

          # auto adjust whole graph to fit container size based on viewport size
            responsive=True
        )
    ])
],style = card_style)
