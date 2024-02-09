from dash import dcc
from global_structures import data_processes

# any +/- to this list MUST be reflected in global_structures.py, data_processes
code_snip_list = [

    # ETL CODE SNIPPET
    dcc.Markdown("""
    ```
    # Import all functions from the transform_data and gather_data modules
    from gather_data.api_call import call_api
    from transform_data.df_creation import create_df
    from transform_data.url_wrangling import parse_url, cat_url_df, url_encoding_removal
    from transform_data.correct_categorization_errors import add_new_channel_group, 
    fix_surface_type_dupe, channel_group_assign_unassigned
    from transform_data.general_cleaning import misc_cleaning
    
    # Wrap all module functions imported above in the get_transform_data() function
    # Call get_transform_data() in the AWS Lamda function below
    def get_transform_data():
    
        api_re = call_api()
    
        og_df = create_df(api_re)
    
        parsed_url_df = parse_url(og_df)
    
        cated_url_df = cat_url_df(parsed_url_df, og_df)
    
        removed_url_encoding = url_encoding_removal(cated_url_df, parsed_url_df)
    
        new_category = add_new_channel_group(removed_url_encoding)
    
        fixed_dupe = fix_surface_type_dupe(new_category)
    
        assigned_channel_group = channel_group_assign_unassigned(fixed_dupe)
    
        final_df = misc_cleaning(assigned_channel_group)
        
        # return a dictionary, Keys: variable name,  Values: dataframe
        return locals()
    
    # initialize AWS S3
    s3 = boto3.client('s3')
    
    
    def lambda_handler(event, context):
    
        gtd_dct = get_transform_data()
        
        # delete redundant api_re; the api response is saved as a dataframe in og_df
        del gtd_dct['api_re']
    
        # serialize each dataframe into a apache parquet file and store in AWS S3
        # Keys: DataFrame name, Values: DataFrame
        for keys, values in gtd_dct.items():
            s3.put_object(Body = values.to_parquet(),
                          Bucket = 'serialized-dfs',
                          Key = f'{keys}.parquet')
                          
    """),

    # CREATE DF CODE SNIPPET
    dcc.Markdown("""
    ```  
    import pandas as pd
    from global_structures import dtype_dct
    
    def create_df(api_re_loc):
    
        # Initialize empty lists to hold dimension and metric data
        d = []
    
        m = []
    
        # Count the number of dimensions and metrics in the API response
        dim_qty = len(api_re_loc.dimension_headers)
        metric_qty = len(api_re_loc.metric_headers)
    
        # Loop through each row in the API response object
        for row in api_re_loc.rows:
    
            # Create a dictionary for dimensions in the current row
            # Key: Dimension name, Value: Dimension value
            d_dct = {api_re_loc.dimension_headers[dim_index_pos].name: row.dimension_values[dim_index_pos].value
                     for dim_index_pos in range(dim_qty)}
    
            # Create a dictionary for metrics in the current row
            # Key: Metric name, Value: Metric value
            m_dct = {api_re_loc.metric_headers[metric_index_pos].name: row.metric_values[metric_index_pos].value
                     for metric_index_pos in range(metric_qty)}
    
            # Append the dictionaries to their respective lists
            d.append(d_dct)
            m.append(m_dct)
    
        # Combine the dimension and metric data into a single DataFrame
        df1 = pd.concat(objs=(pd.DataFrame(d), pd.DataFrame(m)), axis=1)
"""),

    # URL WRANGLING CODE SNIPPET
    dcc.Markdown("""
    ```  
    import pandas as pd
    import re
    from global_structures import dtype_dct
    
    def parse_url(loc_og_df):

    # extract all url parameters using regex
    # '[\?|&]([^=]+) where a '?' or '&' is found, extract characters until a '=' is found
    columns = loc_og_df['landingPagePlusQueryString'].str.extractall('[\?|&]([^=]+)')[0].unique()
    
    # initialize a list to hold values for each url parameter
    param_dfs_list = []
    
    # for each parameter in the url, extract the argument
    for col in columns:
        
        # create a regex pattern to capture all characters until a '=' is found; 
        url_arg_pattern = fr'{col}=([^&]+)'
    
        # Extract the value from each url parameter using the defined regex pattern
        extract = loc_og_df['landingPagePlusQueryString'].str.extract(url_arg_pattern)
    
        # append the value extracted from the url into a list
        param_dfs_list.append(extract)
    
    # cat all dfs in param_dfs_list to form a single df
    url_df_parsed_loc = pd.concat(param_dfs_list, axis=1)
    
    # update the column names of df to match each url parameter listed in an array saved as 'columns'
    url_df_parsed_loc.columns = columns
    
    return url_df_parsed_loc
            
"""),

    # FIX CATEGORICAL ERRORS CODE SNIPPET
    dcc.Markdown("""
    ```python  
    import pandas as pd
    from global_structures import dtype_dct
    
    def add_new_channel_group(removed_url_encoding_loc):
    
        # create boolean expression: if sDCG is 'Direct' and surface_type is 'nan'
        sDCG_is_appstore = (removed_url_encoding_loc.sessionDefaultChannelGroup == 'Direct') & (removed_url_encoding_loc['surface_type'].notnull())
    
        # Assign 'App Store' when sDCG is Direct and surf_type is 'nan', keep original sDCG where expression is false
        channel_group = np.where(sDCG_is_appstore, 'App Store', removed_url_encoding_loc['sessionDefaultChannelGroup'])
    
        # insert the new column, 'channel_group' next to original col, sDCG
        loc = removed_url_encoding_loc.columns.get_loc('sessionDefaultChannelGroup')
        removed_url_encoding_loc.insert(loc=loc + 1, column='channel_group', value=channel_group)
    
        # Update new column, 'channel_group' to dtype 'category' using an imported dictionary
        removed_url_encoding_loc['channel_group']= removed_url_encoding_loc['channel_group'].astype(dtype_dct['channel_group'])
        
        return removed_url_encoding_loc
    ```
"""),

    # # GENERAL CLEANING CODE SNIPPET
        # ("""general_cleaning"""),


        # VISUALIZATION CODE SNIPPET
    dcc.Markdown("""
    import dash_bootstrap_components as dbc
    from dash import html, dcc
    from global_structures import data_processes
    
    # Define a list of unique processes that will have corresponding buttons and collapsible sections
    unique_process_list = ['create_dataframe', 'url_wrangling', 'recategorize_data']

    # Loop through each unique process to dynamically generate callbacks
    # These callbacks toggle the visibility of a collapsible section based on button clicks
    for unique_process in unique_process_list:
        @callback(Output(f'{unique_process}_collapse', 'is_open'),
              [Input(f'{unique_process}_button', 'n_clicks')],
              [State(f'{unique_process}_collapse', 'is_open')])
              
    def toggle_button(n, is_open):
        # Toggle the collapse's open state if the button is clicked
        if n:
            return not is_open
        # Return the current state if no new click is detected
        return is_open

    # Initialize a dictionary to hold dynamically generated buttons for each unique process
    # Each button includes a title derived from the process name and an icon indicating collapsibility
    button_dict = {
    
    f'{process}_button': dbc.Button(
        children=[
            # Use the process name, formatted for display, as button text
            html.Span(f'{process.title().replace("_", " ")}', style={'marginRight': '7px'}),
            # Add a font awesome icon for visual indication of the button's purpose
            html.I(className="fa-solid fa-angles-down")
        ],
        # Button configuration including unique ID and initial click count
        id=f'{process}_button',
        
        n_clicks=0,
        
        # Apply custom classes for styling and hover effects
        className='me-1 rounded custom-hover-effect',
        
        style={
            'color': 'white',
            'backgroundColor': '#A435F0',
            'fontSize': '12px',
            'fontWeight': '900',
            'display': 'inline-flex',
            'alignItems': 'center'
        }
    )
    for process in unique_process_list  # Iterate over the list of unique processes
}
    """),


        # DEPLOYMENT CODE SNIPPET
    dcc.Markdown("""
        ```python
        from dash import html, Input, Output, callback, State
        
        # import page and component layouts
        from layout import tabs, tab_content
        from layout import dashboard, contact_me, about_me_page
    
        # Callback: Offcanvas, Menu Button, Location--------------------------------------------
        
        # Allow a user to navigate to a page when the menu is opened and navlink selected
        @callback(Output('oc', 'is_open'),
        [Input('menu_button', 'n_clicks')],
        [Input("url", "pathname")],
        State('oc', 'is_open'))
        
        # Open and close the menu based on interactions with the 'menu' button
        def toggle_offcanvas(n_clicks, pathname, is_open):
            if n_clicks or pathname:
                return not is_open
            else:
                return is_open
                
        # render different page content based on the menu navlink selected
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
    
            
         """)

]

code_snip_dict ={}

for i in range(len(data_processes)):
    code_snip_dict[data_processes[i]] = code_snip_list[i]

#print(code_snip_dict)