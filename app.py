# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

from data_handler import pull_data
from fig_creator import create_fig_dict
from utils import custom_strftime, change_card


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app = Dash(external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True)

data_dict = pull_data()
assert data_dict is not None

now, fig_dict = create_fig_dict(data_dict)
assert fig_dict is not None

sidebar = html.Div(
    [
        html.H2("Ontario", style={"margin": "0px"}),
        html.H2("COVID-19", style={"margin": "0px"}),
        html.H2("Dashboard", style={"margin": "0px"}),
        html.Hr(),
        html.P(
            f"{custom_strftime('%B {S}, %Y', now)}", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Main", href="/", active="exact"),
                dbc.NavLink("Cases", href="/cases", active="exact"),
                dbc.NavLink("Hospitalizations", href="/hospitalizations", active="exact"),
                dbc.NavLink("Testing", href="/testing", active="exact"),
                dbc.NavLink("Vaccinations", href="/vaccinations", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

main_page = dbc.Container([
    dbc.Tabs(
            [
                dbc.Tab(label="Positive Test Rate", tab_id="map_ont_test"),
            ],
            id="tabs",
            active_tab="map_ont_test",
        ),
        html.Div(id="tab-content", className="p-4"),
])

cases_page = dbc.Container([
                dbc.Row([
                    dbc.Col(html.H2("COVID-19 Case Changes Today"), width='auto'), 
                    ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(change_card(data=data_dict['cases_tl'], col='Total Cases', date_col='Reported Date', title="Active Cases", color_invert=True), width='auto'), 
                    dbc.Col(change_card(data=data_dict['cases_tl'], col='New Cases', date_col='Reported Date', title="New Cases", color_invert=True), width='auto'),
                    dbc.Col(change_card(data=data_dict['cases_tl'], col='New Deaths', date_col='Reported Date', title="New Deaths", color_invert=True), width='auto')
                    ]),
                dbc.Row([
                    dbc.Col(html.H2("New COVID-19 Cases by PHU"), width='auto'), 
                    ], style={"margin-top": "32px"}),
                html.Hr(),
                dbc.Tabs(
                    [
                        dbc.Tab(label="Count", tab_id="map_cases_count"),
                        dbc.Tab(label="Rate", tab_id="map_cases_rate"),
                    ],
                    id="cases-tabs",
                    active_tab="map_cases_count",
                ),
                dcc.Loading(id="cases-loading-content", type="default", children=html.Div(id="cases-tab-content", className="p-4")),
                dcc.Graph(id='fig_case_area',
                          figure=fig_dict['fig_case_area']),
                dcc.Graph(id='fig_death_area',
                          figure=fig_dict['fig_death_area']),
                dcc.Graph(id='fig_vax_ratio_time',
                          figure=fig_dict['fig_vax_ratio_time'])])

tests_page = dbc.Container([
                dcc.Graph(id='tests_hosp_area',
                          figure=fig_dict['tests_hosp_area'],
                          config={"displayModeBar": False}),
])

vaccine_page = dbc.Container([
                dbc.Row([
                    dbc.Col(html.H2("COVID-19 Vaccination Changes Today"), width='auto'), 
                    ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(change_card(data=data_dict['vax_stat'], col='per_partially', date_col='report_date', title="Partially Vaccinated", color_invert=False, percentage=True), width='auto'), 
                    dbc.Col(change_card(data=data_dict['vax_stat'], col='per_fully', date_col='report_date', title="Fully Vaccinated", color_invert=False, percentage=True), width='auto'),
                    dbc.Col(change_card(data=data_dict['vax_stat'], col='per_boosted', date_col='report_date', title="Boosted", color_invert=False, percentage=True), width='auto')
                    ]),
                dbc.Row([
                    dbc.Col(html.H2("COVID-19 Vaccination Over Time", style={"margin-top": "32px"}), width='auto'), 
                    ]),
                html.Hr(),
                dcc.Graph(id='fig_vax',
                          figure=fig_dict['fig_vax'],
                          config={"displayModeBar": False}),
                dbc.Row([
                    dbc.Col(html.H2("COVID-19 Vaccination Rates by Age", style={"margin-top": "32px"}), width='auto'), 
                    ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='vax'+str(gp),
                                      figure=fig_dict['vax'+str(gp)],
                                      config={"displayModeBar": False}), width=4) for gp in range(9)
                ]),
                ])

hosp_page = dbc.Container([
                dbc.Row([
                    dbc.Col(html.H2("COVID-19 Hospital Admissions Today"), width='auto'), 
                    ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(change_card(data=data_dict['hosp_vax'], col='total', date_col='date', title="Total", color_invert=True), width='auto'), 
                    dbc.Col(change_card(data=data_dict['hosp_vax'], col='icu', date_col='date', title="ICU", color_invert=True), width='auto'),
                    dbc.Col(change_card(data=data_dict['hosp_vax'], col='nonicu', date_col='date', title="Non-ICU", color_invert=True), width='auto')
                    ]),
                dbc.Row([
                    dbc.Col(html.H2("Hospitalizations Over Time", style={"margin-top": "32px"}), width='auto'), 
                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='fig_hosp_area',
                            figure=fig_dict['fig_hosp_area']), width=12)
                    ]),
                dbc.Row([
                    dbc.Col(html.H2("Vaccination Status of Hospitalizations", style={"margin-top": "32px"}), width='auto'), 
                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='fig_hosp_general_pop',
                            figure=fig_dict['fig_hosp_general_pop'], config={"displayModeBar": False}), width=4, align='end'), 
                ], justify='center'),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='fig_hosp_vax_tot',
                            figure=fig_dict['fig_hosp_vax_tot'], config={"displayModeBar": False}), width=4), 
                    dbc.Col(dcc.Graph(id='fig_hosp_vax_icu',
                            figure=fig_dict['fig_hosp_vax_icu'], config={"displayModeBar": False}), width=4),
                    dbc.Col(dcc.Graph(id='fig_hosp_vax_nonicu',
                            figure=fig_dict['fig_hosp_vax_nonicu'], config={"displayModeBar": False}), width=4),
                ]),
            ])



@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return main_page
    elif pathname == "/cases":
        return cases_page
    elif pathname == "/hospitalizations":
        return hosp_page
    elif pathname == "/testing":
        return tests_page
    elif pathname == "/vaccinations":
        return vaccine_page
    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )



@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    if active_tab is not None:
        return dcc.Graph(id=active_tab,
                         figure=fig_dict[active_tab],
                         config={"displayModeBar": False})

    return "No tab selected"


@app.callback(
    Output("cases-tab-content", "children"),
    Input("cases-tabs", "active_tab")
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    if active_tab is not None:
        return dcc.Graph(id=active_tab,
                         figure=fig_dict[active_tab],
                         config={"displayModeBar": False})

    return "No tab selected"

if __name__ == '__main__':
    app.run_server(debug=True)
