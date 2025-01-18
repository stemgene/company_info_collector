import dash_bootstrap_components as dbc
from dash import html

def Banner():
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("Company Info Collector", className="navbar-brand mb-0 h1")),
            ]),
            dbc.Row([
                dbc.Col(dbc.NavLink("Home", href="/", className="nav-link", style={"maxWidth": "150px", "overflow": "hidden", "textOverflow": "ellipsis", "whiteSpace": "nowrap"})),
                dbc.Col(dbc.NavLink("Input Company Info", href="/company-info-input", className="nav-link", style={"maxWidth": "150px", "overflow": "hidden", "textOverflow": "ellipsis", "whiteSpace": "nowrap"})),
                dbc.Col(dbc.NavLink("Local Company on Map", href="/map", className="nav-link", style={"maxWidth": "150px", "overflow": "hidden", "textOverflow": "ellipsis", "whiteSpace": "nowrap"})),
            ], className="ml-auto", align="center"),
        ]),
        color="dark",
        dark=True,
        className="mb-4"
    )