import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from src.pages import EmptyPage
from src.components import FilterComponent
from fetch_data import StaticPageParser

def generate_job_list(results):
    return html.Ul([
        html.Li([
            html.H2(html.A(result["company_name"], href=result["URL"], target="_blank")),
            html.Ul([html.Li(position) for position in result.get("position_list", [])])
        ]) for result in results
    ], className="card")

def layout():
    return html.Div([
        html.H1("Company Job Positions", style={'textAlign': 'center'}),
        dcc.Link('Go to Company Info Input Page', href='/company-info-input', className="card"),
        FilterComponent(),
        html.Div(id='filtered-results', className="card")
    ], style={'fontFamily': 'Helvetica'})

def register_callbacks(app):
    @app.callback(
        Output('filtered-results', 'children'),
        [Input('filter-button', 'n_clicks'), Input('url', 'pathname')],
        [State('position-filter', 'value')]
    )
    def update_output(n_clicks, pathname, selected_filters):
        if pathname == "/":        
            parser = StaticPageParser()
            results = parser.parsing()
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
            return generate_job_list(filtered_results)
        return ""
