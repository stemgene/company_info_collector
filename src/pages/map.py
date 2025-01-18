import dash  # Import the Dash library
from dash import html, dcc  # Import HTML and core components from Dash
import dash_leaflet as dl  # Import Dash Leaflet for map components
from dash.dependencies import Input, Output  # Import dependencies for callbacks
import json  # Import JSON library
import requests  # Import requests library to make API calls
import os

# Define a class for company data
class Company:
    def __init__(self, position, company_name, url, category):
        self.position = position
        self.company_name = company_name
        self.url = url
        self.category = category

    @classmethod
    def from_dict(cls, data):
        return cls(
            position=data["position"],
            company_name=data["company_name"],
            url=data["URL"],
            category=data["category"]
        )

# Define a class for markers
class Marker:
    def __init__(self, company):
        self.company = company

    def to_dl_marker(self):
        return dl.Marker(
            position=self.company.position,
            icon={
                "iconUrl": "https://maps.gstatic.com/mapfiles/ms2/micons/orange-dot.png",
                "iconSize": [32, 32],
                "iconAnchor": [16, 32],
                "popupAnchor": [0, -32]
            },
            children=[
                dl.Tooltip(self.company.company_name),
                dl.Popup(html.A(self.company.company_name, href=self.company.url, target="_blank"))
            ]
        )

# Define a class for crossed markers
class CrossedMarker:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def to_dl_marker(self):
        return dl.Marker(
            position=self.data[1],
            icon={
                "iconUrl": "https://maps.google.com/mapfiles/kml/shapes/cross-hairs.png",
                "iconSize": [32, 32],
                "iconAnchor": [16, 32],
                "popupAnchor": [0, -32]
            },
            children=[
                dl.Tooltip(self.name),
                dl.Popup(html.A(self.name, href=self.data[0], target="_blank"))
            ]
        )

# Define a class for routes
class Route:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_route(self):
        url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={os.getenv("OPENROUTESERVIICE_KEY")}&start={self.start[1]},{self.start[0]}&end={self.end[1]},{self.end[0]}'
        response = requests.get(url)
        data = response.json()
        coordinates = data['features'][0]['geometry']['coordinates']
        return [[coord[1], coord[0]] for coord in coordinates]

    def to_dl_polyline(self):
        route = self.get_route()
        return dl.Polyline(positions=route, color="grey", weight=5)

# Initialize the Dash app
app = dash.Dash(__name__)

# Load marker data from JSON file
with open('website_urls.json', 'r') as f:
    all_marker_data = json.load(f)

# Filter marker data where "is_local" is True and create Company instances
companies = [
    Company.from_dict(m) for m in all_marker_data if m["is_local"]
]

# Load crossed place data from JSON file
with open('crossed_place.json', 'r') as f:
    crossed_place_data = json.load(f)

# Load finished street data from JSON file
with open('finished_street.json', 'r') as f:
    finished_street_data = json.load(f)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Massachusetts Tech Company Map", style={'textAlign': 'center'}),  # Header
    html.Div("A basic example integrating Dash and Google Maps.", style={'textAlign': 'center'}),  # Description

    html.Div([
        # Left side menu and data display area
        html.Div([
            dcc.Dropdown(
                id='category-dropdown',
                options=[
                    {'label': 'Tech', 'value': 'tech'},
                    {'label': 'Healthcare', 'value': 'healthcare'}
                ],
                value='tech',
                style={'width': '100%'}
            ),
            html.Div(id='url-display', style={'marginTop': '20px'})
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

        # Right side map area
        html.Div([
            dl.Map(
                id='map',
                center=[42.3765, -71.2356],  # Centered at Waltham, MA
                zoom=12,
                children=[
                    dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
                ],
                style={'width': '100%', 'height': '75vh', 'margin': 'auto'}
            )
        ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'display': 'flex'})
])

# Callback to update the map markers and URL display based on the selected category
@app.callback(
    [Output('map', 'children'), Output('url-display', 'children')],
    [Input('category-dropdown', 'value')]
)
def update_map(selected_category):
    filtered_companies = [c for c in companies if c.category.lower() == selected_category.lower()]
    map_markers = [Marker(c).to_dl_marker() for c in filtered_companies]
    urls = []
    for c in filtered_companies:
        urls.append(html.Div(html.A(c.company_name, href=c.url, target="_blank")))
        urls.append(html.Br())  # Insert a blank line

    # Add red cross markers for crossed places
    crossed_markers = [CrossedMarker(name, data).to_dl_marker() for name, data in crossed_place_data.items()]

    # Add polylines for finished streets
    finished_streets = [Route(data[0], data[1]).to_dl_polyline() for name, data in finished_street_data.items()]

    return [dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")] + map_markers + crossed_markers + finished_streets, urls

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)  # Run the Dash app in debug mode