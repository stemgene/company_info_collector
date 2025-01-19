import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from src.pages import EmptyPage
from src.components import FilterComponent, Banner

def generate_job_list(results):
    return dbc.ListGroup([
        dbc.ListGroupItem([
            html.H2(html.A(result["company_name"], href=result["URL"], target="_blank")),
            html.Ul([html.Li(position) for position in result.get("position_list", [])])
        ]) for result in results
    ])

def layout():
    return dbc.Container([
        Banner(),
        dbc.Row([
            dbc.Col(dcc.Loading(
                id="loading",
                type="default",
                children=html.Div(id='filtered-results', className="card")
            ), width=12, lg=6, className="mx-auto")
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Update Data", id="update-button", color="primary", className="mb-4"), width="auto", className="mx-auto")
        ]),
    ], fluid=True)

def register_callbacks(app, fetch_company_data):
    @app.callback(
        Output('global-data-store', 'data'),
        [Input('update-button', 'n_clicks')]
    )
    def update_data(n_clicks):
        if n_clicks is not None:
            return fetch_company_data()
        return dash.no_update

    @app.callback(
        Output('filtered-results', 'children'),
        [Input('url', 'pathname'), Input('global-data-store', 'data')]
    )
    def update_output(pathname, global_data):
        if pathname == "/":
            if not global_data:  # Check if global_data is empty
                return EmptyPage()
            return generate_job_list(global_data)
        return ""