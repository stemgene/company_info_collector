import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from fetch_data import StaticPageParser
from src.pages import (
    home_layout,
    home_register_callbacks,
    company_info_input_layout,
    company_info_input_register_callbacks,
    success_layout,
    map_layout,
    map_register_callbacks,
)

# Initialize the Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
)


# Global variable to store the company info
def fetch_company_data():
    parser = StaticPageParser()
    return parser.parsing()


global_data = fetch_company_data()
# print("global_data = ", global_data)

# Define the layout of the app
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(
            id="global-data-store", data=global_data
        ),  # Store the global data in dcc.Store
        html.Div(id="page-content"),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/company-info-input":
        return company_info_input_layout()
    elif pathname == "/success":
        return success_layout()
    elif pathname == "/map":
        return map_layout()
    else:
        return home_layout()


home_register_callbacks(app, fetch_company_data)
company_info_input_register_callbacks(app)
map_register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
