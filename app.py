# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px

import pandas as pd

from data_handler import pull_data

app = Dash(__name__)

now = pd.Timestamp.now()

match, ont_map, data_dict = pull_data()
assert data_dict is not None

cases = data_dict['cases_tl']
cases['Reported Date'] = pd.to_datetime(cases['Reported Date'], format='%Y-%m-%d')
view = cases[cases['Reported Date'] > now - pd.Timedelta(days=90)]

fig_hosp = px.line(view, x="Reported Date", y="Number of patients hospitalized with COVID-19", title='Hospitalizations')
fig_tot_case = px.line(view, x="Reported Date", y="Total Cases", title='Total Cases')
fig_tot_deatb = px.line(view, x="Reported Date", y="Deaths", title='Deaths')

phu_cases = data_dict['cases_phu']
phu_cases['FILE_DATE'] = pd.to_datetime(phu_cases['FILE_DATE'], format='%Y-%m-%d')

phu_view = phu_cases[phu_cases['FILE_DATE'] == max(phu_cases['FILE_DATE'])]

merged_ont_map = pd.merge(match, phu_view, how="left", left_on="PHU_ID", right_on="PHU_NUM") 
ont_map['Cases'] = merged_ont_map['ACTIVE_CASES']
ont_map['PHU'] = merged_ont_map['NAME_ENG']
ont_map['id'] = ont_map.index

ont_map = ont_map.to_crs(epsg=4326)

fig_ont_map = px.choropleth(ont_map, geojson=ont_map.geometry, 
                    locations="id", color="Cases", 
                    hover_data={'PHU':True, 'Cases':True, 'id':False},
                    fitbounds="locations",
                    height=750,
                    color_continuous_scale="Viridis")

fig_ont_map.update_geos(resolution=110)

fig_ont_map.update_layout(
    title=dict(x=0.5),
    title_text='Active Cases by PHU',
    margin={"r":0,"t":30,"l":0,"b":10},
    dragmode=False)



app.layout = html.Div(children=[
    html.H1(children=now.strftime("%d %B %Y")),

    html.Div(children='''
        Dash Test
    '''),

    dcc.Graph(
        id='Hospitilizations',
        figure=fig_hosp
    ),

    dcc.Graph(
        id='Total Cases',
        figure=fig_tot_case
    ),

    dcc.Graph(
        id='Deaths',
        figure=fig_tot_deatb
    ),

    dcc.Graph(
        id='Ont_Map',
        figure=fig_ont_map,
        config={"displayModeBar": False}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
