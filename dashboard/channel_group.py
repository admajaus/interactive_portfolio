import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash import dcc

# import pre-processed dfs from custom module
from dashboard.dashboard_pre_processing import channel_group_subset

# pre-define css style in 'style' module
from styles import card_header_style, card_style

# Bar Chart with Secondary Axis for Conversion Rate
channel_group_fig = make_subplots(specs=[[{"secondary_y": True}]])

# First set of bars represent totalUsers per channel group
channel_group_fig.add_trace(
    go.Bar(
        x=channel_group_subset['channel_group'],
        y=channel_group_subset['totalUsers'],
        name='totalUsers'),
        secondary_y=False
)

# Second set of bars represent conversions per channel group
channel_group_fig.add_trace(go.Bar(x=channel_group_subset['channel_group'],
                                   y=channel_group_subset['conversions'], name='conversions'),
                            secondary_y=False)

# Add Conversion Rate per channel group as a line on secondary y axis
channel_group_fig.add_trace(
    go.Scatter(
        x=channel_group_subset['channel_group'],
        y=channel_group_subset['conversion_rate'],
        name='Conversion Rate',
        mode='lines+markers',
        # line = dict(color='#4bbf73'),
        # marker = dict(color='#4bbf73')
           ),
    secondary_y=True)

# Set axis titles
channel_group_fig.update_xaxes(title_text="channel_group")
channel_group_fig.update_yaxes(title_text="totalUsers vs. conversions", secondary_y=False)
channel_group_fig.update_yaxes(title_text="conversion_rate", secondary_y=True)

# Updating layout to group bars side-by-side,
# autosize graph to fit in container
# prevent overlap between graph and container thru margin adjustment
# reduce font size for readability
# option to remove grid lines for secondary y axis
channel_group_fig.update_layout(
    title="Traffic Insights: User Engagement vs. Conversion Rates",
    barmode='group',
    autosize=True,
    margin=dict(l=50, r=50, t=50, b=50),
    font=dict(size=10)
    #yaxis2 = dict(showgrid=False)
)

# Create the card housing the channel group plot
channel_group_card = dbc.Card([
    dbc.CardHeader('CHANNEL GROUP',
                   style = card_header_style
                   ),
    dbc.CardBody(
        dcc.Graph(
            # Bar chart with secondary axis for conversion rate
            figure = channel_group_fig,

            # fill the container with the graph by width and length
            style={'height': '100%',
                   'width': '100%'},
            # auto adjust whole graph to container size based on viewport size
            responsive=True
        )
    )
    # update based on pre-defined css style in module: style.py
], style = card_style)
