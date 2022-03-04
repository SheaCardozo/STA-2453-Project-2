import pandas as pd
import plotly.express as px

def create_fig_dict (data_dict: dict):
    '''
    Creates dict of figs for use in Dash application
    '''
    fig_dict = {}
    now = pd.Timestamp.now()

    cases = data_dict['cases_tl']
    cases['Reported Date'] = pd.to_datetime(cases['Reported Date'], format='%Y-%m-%d')
    view = cases[cases['Reported Date'] > now - pd.Timedelta(days=90)]

    fig_hosp_time = px.line(view, x="Reported Date", y="Number of patients hospitalized with COVID-19", title='Hospitalizations')
    fig_totcase_time = px.line(view, x="Reported Date", y="Total Cases", title='Total Cases')
    fig_totdeath_time = px.line(view, x="Reported Date", y="Deaths", title='Deaths')

    fig_dict['fig_hosp_time'] = fig_hosp_time
    fig_dict['fig_totcase_time'] = fig_totcase_time
    fig_dict['fig_totdeath_time'] = fig_totdeath_time

    fig_dict = create_maps(data_dict, fig_dict)

    return now, fig_dict

def create_maps (data_dict: dict, fig_dict: dict):

    phu_cases = data_dict['cases_phu']
    phu_cases['FILE_DATE'] = pd.to_datetime(phu_cases['FILE_DATE'], format='%Y-%m-%d')

    phu_view = phu_cases[phu_cases['FILE_DATE'] == max(phu_cases['FILE_DATE'])]

    ont_map = data_dict['ont_map']

    merged_phu_view = pd.merge(data_dict['phu_match'], phu_view, how="left", left_on="PHU_ID", right_on="PHU_NUM") 

    ont_map['Cases'] = merged_phu_view['ACTIVE_CASES']
    ont_map['PHU'] = merged_phu_view['NAME_ENG']
    ont_map['id'] = ont_map.index

    ont_map = ont_map.to_crs(epsg=4326)

    map_ont_hosp = px.choropleth(ont_map, geojson=ont_map.geometry, 
                        locations="id", color="Cases", 
                        hover_data={'PHU':True, 'Cases':True, 'id':False},
                        fitbounds="locations",
                        height=750,
                        color_continuous_scale="Viridis")

    map_ont_hosp.update_geos(resolution=110)

    map_ont_hosp.update_layout(
        title=dict(x=0.5),
        title_text='Active Cases by PHU',
        margin={"r":0,"t":30,"l":0,"b":10},
        dragmode=False)

    fig_dict['map_ont_hosp'] = map_ont_hosp

    return fig_dict
