from dash import html, Input, Output,State, callback
import dash_bootstrap_components as dbc
import plotly_express as px

# Import a dictionary containing the name of each major data process
from global_structures import data_processes as dp

# Import all the content created for each tab in the tabular
#from tabular.tab_html_elements import html_elements_dict
from tabular.tab_universal_components import modal_dict
from tabular.tab_html_elements import tab_desc_dict
from tabular.tab_unique_components import unique_components_dictionary
from tabular.tab_unique_components import unique_process_list
from tabular.tabular_pre_processing import viz_channel_group

# RENDER CONTENT PER TAB IN TABULAR--------------------------------------------
# Define a callback function that dynamically updates the content of a display tab based on user interaction.
@callback(Output('display_tab_content', 'children'),
          Input('data_wrangle_tabular', 'value'))

def tab_activation(tab_selected):

    # Iterate through the list of data processing steps defined in 'dp'
    for i in range(len(dp)):

        # Check if the selected tab matches the current iteration/element in data_processes
        if tab_selected == f'tab{i}_{dp[i]}':

            # For each data process and tab, return the associated code snippet modal, markdown process description, and dash components
            return (
                dbc.Row(
                    dbc.Col(
                        modal_dict[f'{dp[i]}'],
                        width={"size": 2, "offset": 10},
                        align='end',
                        #style={'marginBottom': '0 px'}
                    ),
                    #className='mb-2'  # Optional margin bottom
                ),
                dbc.Row(tab_desc_dict[f'{dp[i]}_overview']),

               dbc.Row(dbc.Col(unique_components_dictionary[f'unique_{dp[i]}'])),

                html.Br()
            )


# MODAL: CODE BUTTON/ICON: callback to open-close pop-up window with code snip------------------------------------------------

# dynamically generate the callback opening and closing the code snippet modal for each data_process/tab
for i in range(len(dp)):

    @callback(Output(f'{dp[i]}_code_popup', 'is_open'),
              Input(f'{dp[i]}_open_popup', 'n_clicks'),
              State(f'{dp[i]}_code_popup', 'is_open'))

    # Open and close the code snippet modal/pop-up when the code snip icon is clicked
    def toggle_modal(n_clicks, is_open):
        if n_clicks:
            return not is_open

        return is_open


### UNIQUE PROCESSES: BUTTON AND COLLAPSE CALLBACKS)--------------------------------------

# Dynamically create a callback for each button in the tabular
# When the button is clicked it opens the contents stored in the collapse
for unique_process in unique_process_list:
    @callback(Output(f'{unique_process}_collapse', 'is_open'),
              [Input(f'{unique_process}_button', 'n_clicks')],
              [State(f'{unique_process}_collapse', 'is_open')])

    # Toggle the collapse on and off by clicking the associated button
    def toggle_button(n, is_open):
        if n:
            return not is_open

        return is_open

# VISUALIZATION TAB: DROPDOWN & GRAPH CALLBACK--------------------------------------
# render a chart based on the chart type selected from the dropdown menu 'viz_dropdown'
@callback(Output('viz_plot_selection', 'figure'),
          Input('viz_dropdown', 'value')
          )
def render_plot_selection(dropdown_choice):

    if dropdown_choice == 'Bar Chart':

        return px.bar(
            data_frame=viz_channel_group,
            x='channel_group',
            y='count',
            title=f'{dropdown_choice}: Total Observations per Channel Group'
        )


    elif dropdown_choice == 'Pie Chart':

        return px.pie(
                data_frame = viz_channel_group,
                names = 'channel_group',
                values = 'count',
                title = f'{dropdown_choice}: Total Observations per Channel Group'
        )

    elif dropdown_choice == 'Treemap':

        return px.treemap(
            data_frame=viz_channel_group,
            path=['channel_group'],
            values='count',
            title=f'{dropdown_choice}: Total Observations per Channel Group',
            #color_discrete_sequence= ['#a435f0', '#81F034', '#0092ff', '#0b517c', '#8cd4ff', '#000d6f']
        )