from dash import html, dcc


# any +/- to this list MUST be reflected in global_structures.py, data_processes
tab_desc_list = [

dcc.Markdown(
""" 
Configure Amazon Cloudwatch to automatically trigger a custom AWS Lambda function, 
seamlessly extracting data from the Google Analytics 4 Reporting API 
at regular intervals.

Using Python scripting, the semi-structured API response is *transformed*
into clean, structured tables known as DataFrames. Each Dataframe is serialized into a 
compressed file format, Apache Parquet, ** reducing file size by 83%, creating 
substantial savings in both cloud storage and computing costs ** when the data is
*loaded* into AWS S3 for storage.


"""
, style = {'fontSize': '15px', 'fontWeight': 400, 'textAlign': 'justify'}),

# CREATE DATAFRAME OVERVIEW
dcc.Markdown(
"""

Use python scripting to automate Google Analytics API requests and mine the 
API response for relevant data points. Simplify data manipulation by 
converting the semi-structured API responses into clean, structured 
DataFrames.

"""
, style = {'fontSize': '15px', 'fontWeight': 400, 'textAlign': 'justify'}),

# URL WRANGLING OVERVIEW
dcc.Markdown(""" 
Each visit to an app listing generates a unique url capturing the path a visitor 
takes to reach an app listing. The URL is made up of key-value pairs, where the key 
is a data identifier and the value is the data itself. For example, in the URL http://example.com/page?name=Alex&age=30, name and age are keys, 
with Alex and 30 as their values. Using Python, I broke down these URLs into their 
key-value pairs and organized them into a Dataframe for easy manipulation, analysis, and 
visualization. 
"""
,style = {'fontSize': '15px', 'fontWeight': 400, 'textAlign': 'justify'}),

# FIX CATEGORIZATION OVERVIEW
dcc.Markdown("""

Successfully identified and resolved critical categorization issues: 

1. **Re-categorize over 300 records:** "Reallocate all 'Unassigned' records 
to their respective channel groups and streamline the 'surface_detail' column by merging 
redundant categories into a single, unified category.

2. Identify and fix a significant Google Analytics configuration error, accurately 
**re-categorizing over 83% of records into the correct channel group**, 'App Store', 
significantly improving data integrity for analysis.

""", style = {'fontSize': '15px', 'fontWeight': 400, 'textAlign': 'justify'}),


# VISUALIZATION OVERVIEW
dcc.Markdown("""

Utilize the Dash web framework, HTML, and CSS to develop dynamic, insightful, 
interactive visualizations. Skillfully engineered elegant dashboards, intuitive 
dropdown menus, responsive buttons, engaging pop-up windows, dynamic data tables, 
and a versatile selection of informative plots and charts for in-depth data analysis.

""",style = {'fontSize': '15px', 'fontWeight': 400, 'textAlign': 'justify'}),

# APP DEVELOPMENT LIFECYCLE OVERVIEW
dcc.Markdown('')

]

