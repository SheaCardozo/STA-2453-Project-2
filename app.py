# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

from data_handler import pull_data
from fig_creator import create_fig_dict
from utils import custom_strftime

app = Dash(external_stylesheets=[dbc.themes.SIMPLEX])

data_dict = pull_data()
assert data_dict is not None

now, fig_dict = create_fig_dict(data_dict)
assert fig_dict is not None

app.layout = dbc.Container([
    dcc.Store(id="store"),
    html.H1(f"Today is {custom_strftime('%B {S}, %Y', now)}"),
    html.Hr(),
    dbc.Tabs(
            [
                dbc.Tab(label="Active Cases", tab_id="map_ont_ac"),
                dbc.Tab(label="Positive Test Rate", tab_id="map_ont_test"),
                dbc.Tab(label="Plot", tab_id="cases"),
            ],
            id="tabs",
            active_tab="map_ont_ac",
        ),
        dbc.Spinner(html.Div(id="tab-content", className="p-4")),
])

@app.callback(
    [Output("tab-content", "children"), Output("store", "data")],
    [Input("tabs", "active_tab"), Input("store", "data")]
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if data is None:
        data = {}

    if active_tab is not None:
        if active_tab == 'cases':
            if 'fig_plot_time' not in data:
                data['fig_plot_time'] = fig_dict['fig_plot_time']
            if 'fig_vax_time' not in data:
                data['fig_vax_time'] = fig_dict['fig_vax_time']
            if 'fig_vax_ratio_time' not in data:
                data['fig_vax_ratio_time'] = fig_dict['fig_vax_ratio_time']

            return html.Div(children=[
                dcc.Graph(id=active_tab,
                          figure=data['fig_plot_time'],
                          config={"displayModeBar": False}),
                dcc.Graph(id=active_tab,
                          figure=data['fig_vax_ratio_time'],
                          config={"displayModeBar": False}),
                dcc.Graph(id=active_tab,
                          figure=data['fig_vax_time'],
                          config={"displayModeBar": False})]), data
        if active_tab not in data:
            data[active_tab] = fig_dict[active_tab]
        return dcc.Graph(id=active_tab,
                         figure=data[active_tab],
                         config={"displayModeBar": False}), data


    return "No tab selected", data


'''html.Div(children=[
    html.H1(children=now.strftime("%d %B %Y")),

    html.Div(children=
       # Dash Test
    ),

    dcc.Graph(
        id='fig_hosp_time',
        figure=fig_dict['fig_hosp_time']
    ),

    dcc.Graph(
        id='fig_totcase_time',
        figure=fig_dict['fig_totcase_time']
    ),

    dcc.Graph(
        id='fig_totdeath_time',
        figure=fig_dict['fig_totdeath_time']
    ),

    dcc.Graph(
        id='map_ont_hosp',
        figure=fig_dict['map_ont_ac'],
        config={"displayModeBar": False}
    ),

    dcc.Graph(
        id='map_ont_test',
        figure=fig_dict['map_ont_test'],
        config={"displayModeBar": False}
    )
])
'''
if __name__ == '__main__':
    app.run_server(debug=True)
