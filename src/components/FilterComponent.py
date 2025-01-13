
from dash import html, dcc

def FilterComponent():
    return html.Div([
        dcc.Checklist(
            id='position-filter',
            options=[
                {'label': 'Data Scientist', 'value': 'data'},
                {'label': 'Machine Learning', 'value': 'machine'},
                # Add more options as needed
            ],
            value=[]
        ),
        html.Button('Filter', id='filter-button', n_clicks=0),
        html.Div(id='filtered-results')
    ], style={'margin': '0 auto', 'width': '80%'})