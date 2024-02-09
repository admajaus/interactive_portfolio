from dash import html

# Embded contact form from Jotform
contact_form_iframe = html.Iframe(
    src ='<INSERT_UNIQUE_JOTFORM_URL>',
    width = '100%',
    height = '600px',
)
