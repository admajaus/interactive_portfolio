dtype_dct = {

    'date': 'datetime64[ns]',
    'sessionDefaultChannelGroup': 'category',
    'channel_group':'category',
    'landingPagePlusQueryString': 'str',
    'LandingPagePlusQueryString': 'str',
    'totalUsers': 'Int8',
    'conversions': 'Int8',
    'surface_type': 'category',
    'surface_detail': 'str',
    'surface_inter_position': 'Int8',
    'surface_intra_position': 'Int8'

}

nav_link_titles = ['tabular', 'dashboard', 'about_me', 'contact']

# any +/- to this list MUST be reflected in tabular\tab_descriptions.py
# any +/- to this list MUST be reflected in tabular\tab_code_snips.py
data_processes = [
    'etl',
    'create_dataframe',
    'url_wrangling',
    'recategorize_data',
    #'general_cleaning',
    'visualization',
    'app_development_lifecycle'
]

