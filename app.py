import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.pages import home_layout, home_register_callbacks, company_info_input_layout, company_info_input_register_callbacks, success_layout

# Initialize the Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/company-info-input":
        return company_info_input_layout()
    elif pathname == "/success":
        return success_layout()
    else:
        return home_layout()

home_register_callbacks(app)
company_info_input_register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
