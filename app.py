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
print(results)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Company Job Positions", style={'textAlign': 'center'}),
    html.Div([
        html.Ul([
            html.Li([
                html.H2(html.A(result["company_name"], href=result["URL"], target="_blank")),
                html.Ul([html.Li(position) for position in result.get("position_list", [])])
            ]) for result in results
        ])
    ], style={'margin': '0 auto', 'width': '80%'})
], style={'fontFamily': 'Helvetica'})

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
