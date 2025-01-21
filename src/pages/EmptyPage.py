import dash_bootstrap_components as dbc
from dash import html

def EmptyPage():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("No results found", className="text-center my-4"), width=12)
        ])
    ], fluid=True)