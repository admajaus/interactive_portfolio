README.TXT

##PROJECT TITLE: Interactive Portfolio

##PROJECT DESCRIPTION:
Most portfolios are static and visualize only the end result: a dashboard, app, program, or model.  Some of the best skills possessed by a professional aren’t reflected in the final product, but instead in the journey creating the final product. However these skills are often lost in complex, lengthy code blocks or code repositories that are difficult for most people to read, understand, and conceptualize. This Interactive Portfolio uses a responsive, dynamic interface to bring this convoluted code and obscured skill set into the light, allowing users to interact with the underlying code to unveil the journey in creating a final product.  This provides a more holistic view of a professional’s work and accomplishments in creating the final product.

##INSTALLATION AND RUNNING THE PROGRAM
This will need to be deployed using Heroku, AWS, or another cloud or container provider if you’d like your portfolio to be available on the web.

For local deployment, clone the GitHub repository, navigate to the app’s directory, create a virtual environment, install the dependencies in requirements.text, and run the app.


##CUSTOMIZING THE TABULAR FOR YOUR OWN WORK:

Each tab, complete with tailored labels, HTML descriptions, Dash components, and visualizations, corresponds directly to a process within the *data_processes* list in global_structures.py. The structure and content of each tab are defined across several modules:

####tabular\code_snips.py & tabular\tab_descriptions.py
Each code snippet and tab description is embedded in a dash Markdown component. The markdown components are stored in lists in the same order as the tabs and elements in the *data_process list*. Each Markdown component is assigned to a dictionary value with the key name matching the respective process in the *data_processes* list  from global_structures.py.  A callback in activate_tab_content.py will cycle thru the dictionary keys, returning the code snippet and description matching the tab selected by the user.  The content for each tab description and code snippet must be updated to reflect your individual program and process. The number and order of elements in the *code_snip_list* and *tab_desc_list* in match the qty and order of elements in the *data_proceses* list to avoid out -of-index errors.

#### tabular\tab_universal_components.py
tab_universal_components - these components  will automatically generate based on the processes in *data_processes* and be saved as values in a dictionary, with the keys being the name of the data process. A callback will cycle thru the dictionary keys, returning the dash components matching the tab selected by the user. The tabs, tab labels, the code snip icons, and modal pop-up will be automatically generated for each tab in the tabular. No manual updates are needed here.

#### tabular\tab_unique_components.py
At the end of the script is a dictionary whose structure mirrors the data_processes list. The dictionary values contain components and HTML that are unique to individual tabs and processes within the *data_processes* list. A callback in activate_tab_content.py will cycle thru the dictionary keys, returning the dash components matching the tab selected by the user. This section needs manual updates to align with any changes in data_processes and to customize any of your tab content with unique html elements or dash components.

