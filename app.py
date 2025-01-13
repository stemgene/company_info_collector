import dash
from dash import html, dcc
import dash_leaflet as dl
from dash.dependencies import Input, Output
import sqlite3
import requests
from bs4 import BeautifulSoup
from fetch_data import StaticPageParser, Company

# Initialize the Dash app
app = dash.Dash(__name__)

# Fetch crawled data
parser = StaticPageParser()
results = parser.parsing()

# Define the layout of the app
app.layout = html.Div([
    html.H1("Company Job Positions"),
    html.Ul([
        html.Li([
            html.H2(result["company_name"]),
            html.P(f"URL: {result['URL']}"),
            html.Ul([html.Li(position) for position in result.get("positions", [])])
        ]) for result in results
    ])
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
