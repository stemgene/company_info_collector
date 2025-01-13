
from dash import html

def EmptyPage():
    return html.Div([
        html.H2("No results found", style={'textAlign': 'center', 'marginTop': '20px'})
    ])