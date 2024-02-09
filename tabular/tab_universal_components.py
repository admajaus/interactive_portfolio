import dash_bootstrap_components as dbc
from dash import html, dcc

from tabular.tab_code_snips import code_snip_dict
from global_structures import data_processes

""" Dynamically generate dash components common to all tabs in the tabular:
dcc.Tab, dcc.Button, dcc.Modal
"""
# CREATE CODE SNIPPET POP-UP(MODAL)-------------------------------------------------
# create a code snip icon and modal for each data_process and tab in the tabular
modal_dict = {
    process: dbc.Container([
        dbc.Button(
            [
                html.I(
                    className="fa-solid fa-arrow-up-right-from-square",
                    style={'fontSize': '30px'},
                ),
                html.Span("Code Snippet", style={
                    'fontSize': '14px',  # Adjust font size as needed
                    'fontFamily': 'Arial, sans-serif',  # Set font family
                    'marginLeft': '5px',  # Space between icon and text
                    'textTransform': 'none'  # Keeps text as it is, without transformation to uppercase
                })
            ],
            id=f'{process}_open_popup',
            n_clicks=0,
            className='custom-hover-effect2',
            style={
                'backgroundColor': 'transparent',
                'border': 'none',
                'color': 'rgb(0, 204, 150)',
                'padding': '0',
                'display': 'inline-flex',
                'alignItems': 'center',
                'lineHeight': '1'
            }
        ),
        # This is the pop-up when the code snip icon/button is clicked
        dbc.Modal(children = [
            dbc.ModalHeader(dbc.ModalTitle(

                # title the pop-up using each process in data_processes, replacing any underscores with spaces
                children = f"{process.replace('_', ' ')}: Code Snippet"),
                style = {'backgroundColor': '#1a1a1a' }
            ),
            # integrate each code snip into the body of the pop-up
            dbc.ModalBody(code_snip_dict[process])
        ],
                # assign an id to each pop-up using each process in data_processes
                  id = f'{process}_code_popup',
                  is_open=False,
                  size = 'lg'
                  )
])
    #dynamically create a modal/pop-up for each process in the data_processes list
    for process in data_processes
}
# CREATE INDIVIDUAL TABS------------------------------------------------------------

# initialize dictionary
tab_dict = {}

# Create dcc.Tab, incl. label and value, for each value in data_process_title as dpt
for i in range(len(data_processes)):

    # dynamically generate each dcc.Tab label using elements in data_process_titles
    label = f'{data_processes[i].replace("_", " ").upper()}'

    # add key-value pairs to tab_dict, Keys: elements from dpt, Values: dbc.Tab()
    tab_dict[f'{data_processes[i]}_tab'] = dcc.Tab(

        # create each tab label using an element from data_process_title
        # format the tab labels to be all caps, replace underscores with spaces
        label = label,

        # create the tab id/value for callbacks using elements in data_process_title
        value = f'tab{i}_{data_processes[i]}')

# CREATE THE TABULAR, dbc.Tabs -----------------------------------------------------

# assign each dbc.Tab in tab_dict to the tabular/dbc.Tabs children property
# initialize the tabular that will contain each dbc.Tab in tab_dict
tabular_dcc_tabs = dcc.Tabs(

    id='data_wrangle_tabular',

    value='tab0_etl',

    style={'maxHeight': '200px', 'overflowY': 'auto', 'marginBottom': '15px'},

    # each value in tab_dict is a dbc.Tab, use list comprehension to assign all dcc.Tabs in tab_dict to dcc.Tabs children parameter
    children= [values for values in tab_dict.values()]
)

# # Test component dictionaries
# print(tab_dict)
#print(modal_dict)