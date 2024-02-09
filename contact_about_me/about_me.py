from dash import html, dcc

about_me_title = html.H1('ABOUT ME', style = {'fontWeight': '800'})

about_me_subtitle = html.H6('Alexandra Majauskas: Data App Design & Development')
about_me_blurb = dcc.Markdown(
    """
    My consulting practice is centered on designing custom data applications that enhance decision-making by streamlining data processing, analysis, and visualization. By leveraging the latest web technologies and cloud computing, I transform complex data sets into clear, interactive visual narratives. My approach is to create dynamic user interfaces, enabling users to manipulate variables and explore scenarios with immediate feedback. This fosters a responsive and customized experience, seamlessly integrating data-driven insights into daily operations and long-term strategy.

    My experience as a Consultant and Account Manager highlights my knack for blending advanced technical solutions with strategic interpersonal engagement. This combination has enabled me to lead cross-functional teams effectively, manage key stakeholder communications, and drive business process improvements. Whether it's through pioneering data app development or guiding global account strategies, my efforts consistently unify technical innovation with a focus on meaningful, people-centered outcomes. I am committed to ensuring that data-driven insights are thoughtfully integrated into both the everyday and the long-term visions of the organizations I work with.

    """
, style = {'fontSize':'13px', 'textAlign': 'justify'}
)
