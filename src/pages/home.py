import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from src.pages import EmptyPage
from src.components import FilterComponent, Banner
from fetch_data import StaticPageParser

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
        ])
    ], fluid=True)

def register_callbacks(app):
    @app.callback(
        Output('filtered-results', 'children'),
        [Input('url', 'pathname')],
    )
    def update_output(pathname):
        if pathname == "/":        
            parser = StaticPageParser()
            results = parser.parsing()

            if not results:
                return EmptyPage()
            return generate_job_list(results)
        return ""
