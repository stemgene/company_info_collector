import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from database import DatabaseManager
import json

def layout():
    return html.Div([
        html.H1("Company Info Input Page"),
        dcc.Link('Go to Home Page', href='/', className="card"),
        html.Br(),
        html.Label("Company Name"),
        dcc.Input(id="company-name", type="text", placeholder="Enter company name", className="card"),
        html.Br(),
        html.Label("URL"),
        dcc.Input(id="url", type="text", placeholder="Enter URL", className="card"),
        html.Br(),
        html.Label("Category"),
        dcc.Dropdown(
            id="category",
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
            className="card"
        ),
        html.Br(),
        dcc.Checklist(
            id="available-checkbox",
            options=[{"label": "Available for getting position information", "value": "available"}],
            value=[], 
            className="card"
        ),
        html.Div(id="available-section", style={"display": "none"}, children=[
            html.Label("Website Type"),
            dcc.Dropdown(
            id="website-type",
            options=[
                {"label": "dynamic_HTML_session", "value": "dynamic_HTML_session"},
                {"label": "static_response", "value": "static_response"},
                {"label": "static_xpath", "value": "static_xpath"}
            ],
            placeholder="Select website type", 
            className="card"
        ),
            html.Br(),
            html.Label("Parameters (JSON format)"),
            dcc.Textarea(id="parameters", placeholder="Enter parameters", style={'width': '100%', 'height': 200}),
        ]),
        html.Br(),
        dcc.Checklist(
            id="is-local-checkbox",
            options=[{"label": "Is Local", "value": "is_local"}],
            value=[], 
            className="card"
        ),
        html.Div(id="is-local-section", style={"display": "none"}, children=[
            html.Label("Position (Latitude, Longitude)"),
            dcc.Textarea(id="position", placeholder="Enter latitude, longitude", style={'width': '100%', 'height': 20}, className="card")
        ]),
        html.Br(),
        html.Button("Submit", id="submit-button", className="card"),
        html.Div(id="output", className="card")
    ])

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
         State("url", "value"),
         State("category", "value"),
         State("available-checkbox", "value"),
         State("website-type", "value"),
         State("parameters", "value"),
         State("is-local-checkbox", "value"),
         State("position", "value")]
    )
    def submit_form(n_clicks, company_name, url, category, available_values, website_type, parameters, is_local_values, position):
        if n_clicks is None:
            return ""
        
        try:
            parameters_dict = json.loads(parameters) if parameters else None
        except json.JSONDecodeError:
            return "Invalid JSON format for parameters."
        
        try:
            position_list = [float(coord.strip()) for coord in position.split(",")] if position else None
        except ValueError:
            return "Invalid format for position. Please enter latitude and longitude separated by a comma."
        
        company_info = {
            "company_name": company_name,
            "URL": url,
            "category": category,
            "available": "available" in available_values,
            "website_type": website_type if "available" in available_values else None,
            "parameters": parameters_dict if "available" in available_values else None,
            "is_local": "is_local" in is_local_values,
            "position": position_list if "is_local" in is_local_values else None
        }
        
        # Save the company_info to the database
        db_manager = DatabaseManager()
        query = {"company_name": company_name}
        db_manager.upsert_data(query, company_info)
        db_manager.close_connection()
        
        return dcc.Location(href='/success', id='success-redirect')