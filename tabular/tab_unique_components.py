import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

from styles import card_header_style, card_style
from styles import html_dropdown_style, dropdown_style
from styles import cell_style, data_style, header_style

from tabular.tabular_pre_processing import original_df_sample, parsed_url_sample
from tabular.tabular_pre_processing import b4_recategorize, after_recategorize, index_position

# ETL --------------------------------------------------------------------
unique_etl = dbc.Container(
    # add etl flowchart to the ETL tab
    html.Img(
        src=r'assets/etl_flowchart.svg',
        style={'width': '800px', 'height':'125px'}
    )

    #style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}

)

# DYNAMICALLY GENERATE BUTTONS FOR SPECIFIC TABS----------------------------------------
unique_process_list = ['create_dataframe', 'url_wrangling', 'recategorize_data']

button_dict = {f'{process}_button': dbc.Button(
        children=[
            html.Span(
                f'{process.title().replace("_", " ")}',
                style={'marginRight': '7px'}),

            html.I(className = "fa-solid fa-angles-down")],

        id=f'{process}_button',
        n_clicks=0,
        className='me-1 rounded custom-hover-effect',
        style={'color': 'black',
               'backgroundColor': 'rgb(0, 204, 150)',
               'fontSize': '12px',
               'fontWeight':'900',
               'display': 'inline-flex',
               'alignItems': 'center'
               }
    )

for process in unique_process_list
}

# CREATE DATAFRAME---------------------------------------------------------
# creates a dash_table of og_df that collapses open when the 'create df' button is clicked
create_dataframe_collapse_child = (
    dash_table.DataTable(

        # imported df from tabular_pre_processing.py
        original_df_sample.to_dict('records'),

        # style data_table based on global properties defined in styles.py
        style_cell = cell_style,
        style_data = data_style,
        style_header = header_style

    )
)

create_dataframe_collapse = dbc.Collapse(
    id='create_dataframe_collapse',
    is_open=False,
    children=[create_dataframe_collapse_child]

)


# Add all the create_df components - button and dash_table into a single container
# Containerize all the unique create_df components for easy integration into a dictionary
unique_create_dataframe = dbc.Container([

    button_dict['create_dataframe_button'],

    html.Br(),

    html.Br(),

    dbc.Row([create_dataframe_collapse])

    ])


# URL WRANGLING---------------------------------------------------------

#create a dash_table from a sample of the df, parsed_url_df
parsed_url_table = dash_table.DataTable(
    # imported df from tabular_pre_processing.py
    data = parsed_url_sample.to_dict('records'),

    # style data_table based on global properties defined in styles.py
    style_cell=cell_style,
    style_data=data_style,
    style_header=header_style,

    # style verbose 'surface_detail' column to NOT break to next line within a word
    style_data_conditional=[
        {
            'if': {
                'column_id': 'surface_detail'
            },
            'wordBreak':'normal'
        }]
)

# insert the parsed_url_table into a collapse that will collapse open and closed when the 'url wrangling' button is clicked
url_wrangling_collapse = dbc.Collapse(
    id = 'url_wrangling_collapse',
    children =dbc.Row(parsed_url_table)
)

# Add the url_wrangling button, collapse rendering the dash_table, and dash_table into a single container
# Containerize all the unique url_wrangling components for easy integration into a dictionary
unique_url_wrangling = dbc.Container([

    button_dict['url_wrangling_button'],

    html.Br(),

    html.Br(),

    url_wrangling_collapse
])

# RE-CATEGORIZE DATA---------------------------------------------------------
table_b4_recatg = dash_table.DataTable(

    # imported df from tabular_pre_processing.py
    b4_recategorize.to_dict('records'),
    style_as_list_view=True,
    style_cell=cell_style,
    style_data=data_style,
    style_header=header_style,
    style_data_conditional=[
    {
        'if':{ 'row_index':0},

        'backgroundColor':'#ced4da',
        'color': '#919aa1',
        'fontStyle':'italic'
    }
    ]
)

table_after_recatg = dash_table.DataTable(

    # imported df from tabular_pre_processing.py
    after_recategorize.to_dict('records'),
    style_as_list_view=True,
    style_cell=cell_style,
    style_data=data_style,
    style_header=header_style,
    style_data_conditional=[
    {
        # add conditional formatting to highlight the re-categorized data
        'if':{ 'row_index': index_position},

        'backgroundColor':'#ced4da',
        'color': '#919aa1',
        'fontStyle':'italic'
    }
]
)

# Add the data_tables to a collapse component that will open and close when the 'recategorize data' button is clicked
recategorize_data_collapse = dbc.Collapse(
    id = 'recategorize_data_collapse',
    children = [
        dbc.Row([
            dbc.Col(table_b4_recatg, width = 5),

            dbc.Col(dbc.Container(
                html.I(
                    className="fa-solid fa-arrow-right-long",
                    style = {'fontSize': '50px' , 'color': 'rgb(0, 204, 150)'}),

                style={'height': '100%'} ,
                className="d-flex align-items-center justify-content-center"
            ),
                width = 1,
            ),

            dbc.Col(table_after_recatg, width = 5)
        ])
    ]
)

# Add the unique recategorize data components: button, collapse, dash_table into a single container
# Containerize all the unique re-categorize data components for easy addtion into a dictionary
unique_recategorize_data = dbc.Container([

    button_dict['recategorize_data_button'],

    html.Br(),

    html.Br(),

    recategorize_data_collapse
])

# VISUALIZATION------------------------------------------------------------------
# Add the viz dropdown and graph into a single, aesthetically-pleasing container
# Containerize all the unique viz components to add them as a single value and entity in the dictionary  at the end of the scipt
unique_visualization = dbc.Card([
    dbc.CardHeader(
        'Interactive Visualization Generator',
        style = card_header_style
    ),
    dbc.CardBody([
        html.P(
            'Please choose a chart type from the dropdown menu below:',
            style = html_dropdown_style
        ),

        # create a dropdown allowing the user to select and render a chart type
        dcc.Dropdown(
            id = 'viz_dropdown',
            options = ['Treemap', 'Bar Chart', 'Pie Chart'],
            value = 'Treemap',
            style = dropdown_style
        ),

        # dash_table rendered based on dropdown selection and callback in activate_tab_content.py
        dcc.Graph(id = 'viz_plot_selection')

    ])
], style = card_style)



# APP DEVELOPMENT LIFECYCLE------------------------------------------------------------------
# Create an aesthetically appealing container to hold the carousel/slideshow
# Containerizes all the componets for the app dev lifecycle to be used as a single value in a dictionary
unique_lifecycle = dbc.Card([

    dbc.CardHeader(
        'Slideshow: App Development Lifecycle',
        style = card_header_style
    ),
    dbc.CardBody([
        # assign each 'slide' in the carousel as a dictionary in a single list
        # the src is the background image for the carousel slide
        # the caption is the text in the carousel slide
        dbc.Carousel(items=[
            {
                "header": 'Exploratory Analysis & Foundational Data App Development',
                "src": r'assets/data_analysis.jpg',
                'caption':'Drive data exploration and foundational data app development in Jupyter Notebook: Dive deep into analysis, refine data, and craft core data processing algorithms for use in a cloud-based data app. Automate API requests, extract user behavior insights to create targeted Key Performance Indicators (KPIs), identify and resolve critical cateogrization issues, and serialize data into a compressed file format to reduce clouding computing and storage costs.'
            },

        {
            "header": 'Front End Development',
            "src": r'assets/user_interface.jpg',
            'caption': 'Migrate data processing algorithms into an app development environment, refactoring and modularizing the code for scalability, performance, and easy re-use in future projects. Create a responsive, modular data application, fine-tuned to provide stakeholders with instant access to real-time, data-driven insights: data aggregations, intuitive dashboards, and interactive visualizations'
        },

        {
            "header": 'Serverless Computing & Deployment',
            "src": r'assets/serverless.jpg',
            'caption': "Successfully deployed my app locally and to AWS, leveraging Lambda and Elastic Beanstalk for scalable, cloud-based performance. Optimize data app loading speed: Utilize serverless computing vs. local processing for large, complex data transformations, improving initial load time by 11.97 seconds and cached-result visits by 2.4 seconds."
        }]

        )

    ])
], style = {'width': '75%', 'margin': 'auto', 'border': '2px double black'}
)

# CREATE DICTIONARY of unique components---------------------------
# wrap each container of unique elements per data_process in a dictionary
# KEYS = 'unique' + data process step, VALUES = unique components per data process step
unique_components_dictionary = {

    'unique_etl': unique_etl,
    'unique_create_dataframe':unique_create_dataframe,
    'unique_url_wrangling': unique_url_wrangling,
    'unique_recategorize_data': unique_recategorize_data,
    'unique_visualization': unique_visualization,
    'unique_app_development_lifecycle': unique_lifecycle
}


# test button_dict
#print(button_dict)

# test components_dict
#print(unique_components_dict['unique_etl'])
