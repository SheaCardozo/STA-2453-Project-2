# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc

from data_handler import pull_data
from fig_creator import create_fig_dict

app = Dash(__name__)

data_dict = pull_data()
assert data_dict is not None

now, fig_dict = create_fig_dict(data_dict)
assert fig_dict is not None

app.layout = html.Div(children=[
    html.H1(children=now.strftime("%d %B %Y")),

    html.Div(children='''
        Dash Test
    '''),

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
        figure=fig_dict['map_ont_hosp'],
        config={"displayModeBar": False}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
