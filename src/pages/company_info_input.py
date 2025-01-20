import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from database import DatabaseManager
import dash_bootstrap_components as dbc
import json
from src.components import Banner

def layout():
    return dbc.Container([
        Banner(),
        dbc.Row([
            dbc.Col(html.H2("Company Info Input Page", id="app-title", className="my-4"), width=12, lg=6, className="mx-auto")
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Company Name"),
                dbc.Input(id="company-name", type="text", placeholder="Enter company name", className="mb-3"),
                dbc.Label("URL"),
                dbc.Input(id="company-url", type="text", placeholder="Enter URL", className="mb-3"),
                dbc.Label("Category"),
                dcc.Dropdown(
                    id="company-category",
                    options=[
                        {"label": "Tech", "value": "tech"},
                        {"label": "Healthcare", "value": "healthcare"},
                        {"label": "Biotech", "value": "biotech"},
                        {"label": "Factory", "value": "factory"},
                        {"label": "Education", "value": "education"},
                        {"label": "Business", "value": "business"},
                        {"label": "Finance", "value": "finance"},
                        {"label": "Resale", "value": "resale"},
                        {"label": "Environments", "value": "environments"},
                        {"label": "Others", "value": "others"}
                    ],
                    placeholder="Select a category", 
                    value= "tech",
                    className="mb-3"
                ),
                dbc.Checklist(
                    id="available-checkbox",
                    options=[{"label": "Available for getting position information", "value": "available"}],
                    value=[], 
                    className="mb-3"
                ),
                html.Div(id="available-section", style={"display": "none"}, children=[
                    dbc.Label("Website Type"),
                    dcc.Dropdown(
                        id="website-type",
                        options=[
                            {"label": "dynamic_HTML_session", "value": "dynamic_HTML_session"},
                            {"label": "static_response", "value": "static_response"},
                            {"label": "static_xpath", "value": "static_xpath"}
                        ],
                        placeholder="Select website type", 
                        className="mb-3"
                    ),
                    dbc.Label("Parameters (JSON format)"),
                    dbc.Textarea(id="parameters", placeholder="Enter parameters in JSON format", style={'width': '100%', 'height': 200}, className="mb-3"),
                ]),
                dbc.Checklist(
                    id="is-local-checkbox",
                    options=[{"label": "Is Local", "value": "is_local"}],
                    value=[], 
                    className="mb-3"
                ),
                html.Div(id="is-local-section", style={"display": "none"}, children=[
                    dbc.Label("Location (Latitude, Longitude)"),
                    dbc.Input(id="company-location", type="text", placeholder="Enter latitude and longitude separated by a comma", className="mb-3")
                ]),
                dbc.Button("Submit", id="submit-button", color="primary", className="mb-3"),
                html.Div(id="output", className="card")
            ], width=12, lg=6, className="mx-auto"),
        ])
    ], fluid=True)


def register_callbacks(app):
    @app.callback(
        Output("available-section", "style"),
        [Input("available-checkbox", "value")]
    )
    def toggle_available_section(available_values):
        if "available" in available_values:
            return {"display": "block"}
        return {"display": "none"}

    @app.callback(
        Output("is-local-section", "style"),
        [Input("is-local-checkbox", "value")]
    )
    def toggle_is_local_section(is_local_values):
        if "is_local" in is_local_values:
            return {"display": "block"}
        return {"display": "none"}

    @app.callback(
        Output("output", "children"),
        [Input("submit-button", "n_clicks")],
        [State("company-name", "value"),
         State("company-url", "value"),
         State("company-category", "value"),
         State("available-checkbox", "value"),
         State("website-type", "value"),
         State("parameters", "value"),
         State("is-local-checkbox", "value"),
         State("company-location", "value")]
    )
    def submit_form(n_clicks, company_name, company_url, company_category, available_values, website_type, parameters, is_local_values, company_location):
        if n_clicks is None:
            return ""
        
        try:
            parameters_dict = json.loads(parameters) if parameters else None
        except json.JSONDecodeError:
            return "Invalid JSON format for parameters."
        
        try:
            location_list = [float(coord.strip()) for coord in company_location.split(",")] if company_location else None
        except ValueError:
            return "Invalid format for location. Please enter latitude and longitude separated by a comma."
        
        company_info = {
            "company_name": company_name,
            "URL": company_url,
            "category": company_category,
            "available": "available" in available_values,
            "website_type": website_type if "available" in available_values else None,
            "parameters": parameters_dict if "available" in available_values else None,
            "is_local": "is_local" in is_local_values,
            "location": location_list if "is_local" in is_local_values else None
        }
        
        # Save the company_info to the database
        db_manager = DatabaseManager()
        query = {"company_name": company_name}
        db_manager.upsert_data(query, company_info)
        db_manager.close_connection()
        
        return dcc.Location(href='/success', id='success-redirect')