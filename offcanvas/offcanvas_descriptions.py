from dash import dcc

intro = dcc.Markdown(children = """
The purpose of this app is to demo gathering, transforming, and analyzing Google 
Analytics data for an active app listing in the Shopify App Store.

The interactive **TABULAR** summarizes each major step in the data gathering and transformation 
process. The **DASHBOARD** analyzes app listing traffic, determining which channel groups, sections 
of the Shopify app store, and keywords drive engagement and conversions.

""", style = {'fontSize':'13px', 'color':'white', 'textAlign': 'justify'})