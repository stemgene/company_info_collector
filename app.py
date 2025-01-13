import dash
from dash import html, dcc
import dash_leaflet as dl
from dash.dependencies import Input, Output
import sqlite3
import requests
from bs4 import BeautifulSoup
from fetch_data import StaticPageParser, Company
from src.components.FilterComponent import FilterComponent
from src.page.EmptyPage import EmptyPage

# Initialize the Dash app
app = dash.Dash(__name__)

# Fetch crawled data
parser = StaticPageParser()
results = parser.parsing()
print(results)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Company Job Positions", style={'textAlign': 'center'}),
    FilterComponent(),
    html.Div(id='filtered-results', children=[
        html.Ul([
            html.Li([
                html.H2(html.A(result["company_name"], href=result["URL"], target="_blank")),
                html.Ul([html.Li(position) for position in result.get("position_list", [])])
            ]) for result in results
        ])
    ])
], style={'fontFamily': 'Helvetica'})

@app.callback(
    Output('filtered-results', 'children'),
    [Input('filter-button', 'n_clicks')],
    [dash.dependencies.State('position-filter', 'value')]
)
def update_output(n_clicks, selected_filters):
    if n_clicks == 0 or not selected_filters:
        filtered_results = results
    else:
        filtered_results = [
            result for result in results if any(
                filter in position.lower() for position in result.get("position_list", []) for filter in selected_filters
            )
        ]
    if not filtered_results:
        return EmptyPage()
    return html.Ul([
        html.Li([
            html.H2(html.A(result["company_name"], href=result["URL"], target="_blank")),
            html.Ul([html.Li(position) for position in result.get("position_list", [])])
        ]) for result in filtered_results
    ])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
