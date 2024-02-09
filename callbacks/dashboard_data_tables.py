import pandas as pd
from dash import Input, Output, callback

# Import pre-processed dataframes from a custom module
from dashboard.dashboard_pre_processing import keyword_df, app_section_detail
from dashboard.dashboard_pre_processing import intra_position
from dashboard.dashboard_pre_processing import inter_position

# sort DASHBOARD: KEYWORD LIST by user selection from dropdown--------------------------------------------------
@callback(
    Output('keyword_data_table', 'data'),
    Input('sort_kw_table_dropdown', 'value')
)

def sort_keyword_list(kw_dropdown_selection):
    sorted = keyword_df.sort_values(
        by = kw_dropdown_selection,
        ascending = False)

    # return the sorted df as a dict and input to the data_frame property of a dash_table, 'keyword_data_table'
    return sorted.to_dict('records')

# SORT SURFACE DETAIL/App Section Detail by user selection from dropdown---------------
@callback(Output('surface_detail_table', 'data'),
          Input('sort_surface_detail', 'value'),
          Input('detail_select_surface_type', 'value')
          )

def sort_surface_detail_table(sort_by_choice, surface_type_choice):

    # There is no data for surface_type partners, create a table reflecting this
    if (surface_type_choice == 'partners'):
        return pd.DataFrame({'partners_detail': 'data is not available'}, index=[1]).to_dict('records')

    else:
        sd_table =  app_section_detail[surface_type_choice]

        sd_table = sd_table.sort_values(
            by = sort_by_choice,
            ascending = False
        ).to_dict('records')

        return sd_table

# SELECT POSITION TYPE, SELECT SURFACE_TYPE, SELECT SORT BY---------------
@callback(Output('position_table', 'data'),
          Input('select_position', 'value'),
          Input('position_select_surface_type', 'value'),
          Input('sort_position', 'value')
          )

def position_table(position_choice, pos_surface_type_choice,pos_sort_choice ):

    # There is no data avail. for partners, surface_inter_position; create a df reflecting this
    if (position_choice == 'surface_inter_position') & (pos_surface_type_choice == 'partners'):

        return pd.DataFrame({'partners_inter_position': 'data is not available'}, index = [1]).to_dict('records')

    # There is no positional data available for marketing, create a df reflecting this
    elif (pos_surface_type_choice == 'marketing'):

        return pd.DataFrame({'marketing_position': 'data is not available'}, index=[1]).to_dict('records')

    # return the pre-processed df, converted to a dict, as input to a dash_table
    elif position_choice == 'surface_inter_position':

        return (inter_position[pos_surface_type_choice].
                sort_values(pos_sort_choice)

                # rename the table columns for brevity
                .rename(columns = {'surface_inter_position': 'inter_position'})

                # convert df to a dictionary to be used in dash_table
                .to_dict('records')
                )
    else:
        return (intra_position[pos_surface_type_choice].
                sort_values(pos_sort_choice)

                # rename the table columns for brevity
                .rename(columns = {'surface_intra_position': 'inter_position'})

                # convert df to a dictionary to be used in dash_table
                .to_dict('records')
                )