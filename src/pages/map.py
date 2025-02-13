import dash  # Import the Dash library
from dash import html, dcc  # Import HTML and core components from Dash
import dash_leaflet as dl  # Import Dash Leaflet for map components
from dash.dependencies import Input, Output  # Import dependencies for callbacks
import json  # Import JSON library
import requests  # Import requests library to make API calls
import os
import dash_bootstrap_components as dbc
from src.components.banner import Banner


# Define a class for company data
class Company:
    def __init__(self, location, company_name, url, category):
        self.location = location
        self.company_name = company_name
        self.url = url
        self.category = category

    @classmethod
    def from_dict(cls, data):
        return cls(
            location=data["location"],
            company_name=data["company_name"],
            url=data["URL"],
            category=data["category"],
        )


# Define a class for markers
class Marker:
    def __init__(self, company):
        self.company = company

    def to_dl_marker(self):
        return dl.Marker(
            position=self.company.location,  # this "position" argument is from the Dash Leaflet library, not the same as the "position" attribute of the Company class
            icon={
                "iconUrl": "https://maps.gstatic.com/mapfiles/ms2/micons/orange-dot.png",
                "iconSize": [32, 32],
                "iconAnchor": [16, 32],
                "popupAnchor": [0, -32],
            },
            children=[
                dl.Tooltip(self.company.company_name),
                dl.Popup(
                    html.A(
                        self.company.company_name,
                        href=self.company.url,
                        target="_blank",
                    )
                ),
            ],
        )


# Define a class for crossed markers
class CrossedMarker:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def to_dl_marker(self):
        return dl.Marker(
            location=self.data[1],
            icon={
                "iconUrl": "https://maps.google.com/mapfiles/kml/shapes/cross-hairs.png",
                "iconSize": [32, 32],
                "iconAnchor": [16, 32],
                "popupAnchor": [0, -32],
            },
            children=[
                dl.Tooltip(self.name),
                dl.Popup(html.A(self.name, href=self.data[0], target="_blank")),
            ],
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
        coordinates = data["features"][0]["geometry"]["coordinates"]
        return [[coord[1], coord[0]] for coord in coordinates]

    def to_dl_polyline(self):
        route = self.get_route()
        return dl.Polyline(positions=route, color="grey", weight=5)


# Define the layout of the app
def map_layout():
    return dbc.Container(
        [
            Banner(),
            dbc.Row(
                [
                    dbc.Col(
                        html.H1("Local Company Map", className="text-center my-4"),
                        width=12,
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                id="company-list",
                                className="card",
                                style={"height": "75vh", "overflowY": "scroll"},
                            )
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            dl.Map(
                                center=[42.3765, -71.2356],
                                zoom=13,
                                children=[
                                    dl.TileLayer(
                                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                    ),
                                    dl.LayerGroup(id="layer"),
                                ],
                                style={
                                    "width": "100%",
                                    "height": "75vh",
                                    "margin": "auto",
                                },
                            )
                        ],
                        width=9,
                    ),
                ],
                style={"width": "80%", "margin": "auto"},
            ),
        ],
        fluid=True,
    )


def register_callbacks(app):
    @app.callback(
        [Output("layer", "children"), Output("company-list", "children")],
        [Input("url", "pathname"), Input("global-data-store", "data")],
    )
    def update_map(pathname, global_data):
        if pathname == "/map":
            # Filter the global_data to only include local companies
            local_companies = [
                Company.from_dict(data) for data in global_data if data.get("is_local")
            ]
            markers = [Marker(company).to_dl_marker() for company in local_companies]
            company_list = [
                dbc.ListGroupItem(
                    [
                        html.H5(
                            html.A(
                                company.company_name, href=company.url, target="_blank"
                            )
                        ),
                        html.P(company.category),
                    ]
                )
                for company in local_companies
            ]
            return markers, company_list
        return [], []
