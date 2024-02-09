""" This module utilizes the `tab_desc()` function from `tabular.tab_descriptions`
to retrieve descriptions of various data processing steps. These descriptions are
used to dynamically generate HTML paragraph elements which are stored in the
dictionary `html_elements_dict`.The dictionary keys correspond to the names of the
data processing steps, and the values are the respective HTML paragraph elements
encapsulating the descriptions of these steps."""

from dash import html

from global_structures import data_processes as dp
from tabular.tab_descriptions import tab_desc_list

tabular_title = html.H2('TABULAR',
                        #style = {'display': 'inline-block', 'margin-right': '10px'}
                        )

tabular_subtitle = html.H5('Analytics Workflow: From Extraction to Insights',
                           #style = {'display': 'inline-block'}
                           )


# initialize dictionary
tab_desc_dict= {}

# add markdown component into an html container to dynamically add css style to each element
# add each html element (with the markdown description) as dict value and the
for i in range(len(dp)):
    tab_desc_dict[f'{dp[i]}_overview'] = html.P(
        children = tab_desc_list[i],
        style={
            'margin-top': '20px',
            'margin-bottom': '20px'
        }
    )
# #Test contents of dictionary
# print(tab_desc_dict)