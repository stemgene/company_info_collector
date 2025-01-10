import dash
from dash import html, dcc
import dash_leaflet as dl
from dash.dependencies import Input, Output
import sqlite3
import requests
from bs4 import BeautifulSoup

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([html.H1("Hello World")])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
