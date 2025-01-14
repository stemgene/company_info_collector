import dash
from dash import html, dcc

def layout():
    return html.Div([
        html.H1("Company infomation has been successfully recorded!"),
        html.Br(),
        dcc.Link('Record another company', href='/company-info-input', className="card"),
        html.Br(),
        dcc.Link('Back to the main page', href='/', className="card")
    ])