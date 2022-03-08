from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import locale

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def change_card(data, col, date_col, title, color_invert=False):

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    data[date_col] = pd.to_datetime(data[date_col], format='%Y-%m-%d')

    curr = data[data[date_col] == max(data[date_col])][col].iloc[0]

    b_data = data[data[date_col] < max(data[date_col])]

    last = b_data[b_data[date_col] == max(b_data[date_col])][col].iloc[0]

    change = curr - last
    change_a = abs(change)

    color_list = ['g', 'r']

    if color_invert:
        color_list.reverse()

    if change > 0:
        asset = f"./assets/{color_list[0]}_up.png"
    elif change < 0:
        asset = f"./assets/{color_list[1]}_up.png"
    else:
        asset = f"./assets/neut.png"

    return dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row([dbc.Col(html.H3(title, className="card-title", style={"margin": "0px"}), width="auto")], justify="center"),
                html.Hr(style={"margin": "8px"}),
                dbc.Row([dbc.Col(html.H1(locale.format("%d", curr, grouping=True)), width="auto")], justify="center"),
                dbc.Row([dbc.Col(html.Div(), width=4),
                         dbc.Col(dbc.Row(dbc.Col(html.H5(locale.format("%d", change_a, grouping=True), style={"margin": "0px"}), width="auto"), justify="center"), width=4, style={"padding": "1px"}, align="end"),
                         dbc.Col(dbc.Row(dbc.Col(html.Img(src=asset, style={"width": "10px"}), width="auto"), justify="start"), width=4, style={"padding": "1px"}, align="center")], justify="start"),
            ]
        ),
    ],
    style={"width": "18rem"},
)