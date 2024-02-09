from dash import Input, Output, callback
from dashboard.dashboard_pre_processing import df_final
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from dashboard.dashboard_pre_processing import resampled_dfs

@callback(
    Output("time_series", 'figure'),
    Input('time_series_dropdown', 'value')
)

def create_time_series_graph(surface_type_choice):

    time_series_df = resampled_dfs[surface_type_choice]


    # Visualization: Scatter plot with Secondary Axis for Conversion Rate
    time_series_fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Total Users as line on primary y axis
    time_series_fig.add_trace(
        go.Scatter(
            x=time_series_df.index,
            y=time_series_df['totalUsers'],
            name='totalUsers',
            mode='lines+markers'
        ),
        secondary_y=False
    )
    # Add conversion rate as line on primary y axis
    time_series_fig.add_trace(
        go.Scatter(
            x=time_series_df.index,
            y=time_series_df['conversions'],
            name='Conversions',
            mode='lines+markers'
        ),
        secondary_y=False
    )

    # Adding Conversion Rate as a line on secondary y axis
    time_series_fig.add_trace(
        go.Scatter(
            x=time_series_df.index,
            y=time_series_df['conversion_rate'],
            name='Conversion Rate',
            mode='lines+markers'
        ),
        secondary_y=True)

    # Setting axis titles
    time_series_fig.update_xaxes(title_text="time")
    time_series_fig.update_yaxes(title_text="Total Users vs. Conversions", secondary_y=False)
    time_series_fig.update_yaxes(title_text="Conversion Rate", secondary_y=True)

    # Add chart title
    time_series_fig.update_layout(title="App Store Features: Engagement & Conversion Trends")

    return time_series_fig