import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components.banner import Banner

def layout():
    return dbc.Container([
        Banner(),
        dbc.Row([
            dbc.Col(html.H1("Company information has been successfully recorded!", className="text-center my-4"), width=12)
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Go to Home Page", href='/', color="primary", className="mx-2"), width="auto"),
            dbc.Col(dbc.Button("Add Another Company", href='/company-info-input', color="primary", className="mx-2"), width="auto")
        ], justify="center")
    ], fluid=True)


