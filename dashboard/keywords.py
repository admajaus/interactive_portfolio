import dash_bootstrap_components as dbc
from dash import dcc, dash_table, html
from wordcloud import WordCloud

# import pre-processed dfs from the dashboard pre-processing module
from dashboard.dashboard_pre_processing import keyword_wordcloud_dict, keyword_df

# import pre-defined css styles for dbc.Cards, dash_tables, and dropdowns
from styles import card_header_style, card_style
from styles import header_style_dash, table_style, cell_style_non_url
from styles import dropdown_style, html_dropdown_style

# create a word cloud using the dictionary imported from dashboard_pre_processing
keywords_wordcloud = WordCloud(
    width=350,
    height=350,
    background_color ='white',
    colormap = 'winter'
).generate_from_frequencies(keyword_wordcloud_dict)

# save the png image of the wordcloud in the assets folder
keywords_wordcloud.to_file("assets/wordcloud.png")


# Create the container to hold the word cloud
wordcloud_card = dbc.Card([
    dbc.CardHeader('SEARCH TERM IMPACT: TOP CONVERTING KEYWORDS',
                   style = card_header_style
                   ),
    html.Div(
        dbc.CardImg(src="assets/wordcloud.png",
                    top=True,
                    style={"width": "100%", "height": "500px", "margin": "10px"}),
        style={"padding": "10px"}  # This adds padding around the image inside the card
    )
], style = card_style)

# create a dash table based populated by the callback in dashboard_data_tables
keyword_table = dash_table.DataTable(

    id = 'keyword_data_table',

    #data = keyword_table_dict,

    #style_as_list_view = True,

    style_table={

        'height': '418px',
        'overflowY': 'scroll'
    },
    # style cell and header based on css styles defined in the style.py
    style_cell = cell_style_non_url,

    style_header = header_style_dash

)

# Create a container housing the keyword list dash_table and the sort-by metric dropdown
keyword_table_card = dbc.Card([

    dbc.CardHeader('EXPLORING KEYWORDS BY USERS & CONVERSIONS',
                   style = card_header_style
                   ),

    dbc.CardBody([
        html.P(
            children ='Sort the Keyword List by selecting a metric:',
            style = html_dropdown_style
        ),

        dcc.Dropdown(
            id = 'sort_kw_table_dropdown',
            options =[col for col in keyword_df.columns[1:]],
            value = 'totalUsers',
            style =dropdown_style
        ),

        keyword_table,

    ])
], style = card_style)