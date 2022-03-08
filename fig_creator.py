import pandas as pd
import plotly.express as px
import numpy as np

def create_fig_dict (data_dict: dict):
    '''
    Creates dict of figs for use in Dash application
    '''
    fig_dict = {}
    now = pd.Timestamp.now()

    cases = data_dict['cases_tl']
    view = cases[cases['Reported Date'] > now - pd.Timedelta(days=90)]

    fig_hosp_time = px.line(view, x="Reported Date", y="Number of patients hospitalized with COVID-19", title='Hospitalizations')
    fig_totcase_time = px.line(view, x="Reported Date", y="Total Cases", title='Total Cases')
    fig_totdeath_time = px.line(view, x="Reported Date", y="Deaths", title='Deaths')

    fig_dict['fig_hosp_time'] = fig_hosp_time
    fig_dict['fig_totcase_time'] = fig_totcase_time
    fig_dict['fig_totdeath_time'] = fig_totdeath_time

    cases2 = data_dict['cases_vaxed']
    view2 = cases2[cases2['Date'] > now - pd.Timedelta(days=90)]

    fig_plot_time = px.line(view2, x="Date", y="Tot Cases",
                            title='Cases per day')

    cases3 = data_dict['vax_stat']
    view3 = cases3[cases3['Date'] > now - pd.Timedelta(days=90)]

    view4 = pd.merge(view3, view2, on=['Date'])
    view4['ratio'] = (view4['covid19_cases_full_vac']/view4['Tot Vaxed'])/(view4['covid19_cases_unvac']/view4['UnVaxed'])

    df = pd.DataFrame(data={'Vax Status': ['Fully Vaccinated', 'Partially Vaccinated', 'Unvaccinated'], 'values': [np.mean(view4['covid19_cases_full_vac']/view4['Tot Vaxed']), np.mean(view4['covid19_cases_partial_vac']/view4['part Vaxed']), np.mean(view4['covid19_cases_unvac']/view4['UnVaxed'])]})
    fig = px.pie(df, values='values', names='Vax Status', title='Vaccination Status of Covid Cases on average')
    fig_vax_ratio_time = px.line(view4, x="Date", y="ratio",
                            title='Ratio of Fully Vaxed cases to UnVaxed cases')

    fig_dict['fig_plot_time'] = fig_plot_time
    fig_dict['fig_vax_ratio_time'] = fig_vax_ratio_time
    fig_dict['fig_vax_time'] = fig

    fig_dict = create_maps(data_dict, fig_dict)

    return now, fig_dict

def create_maps (data_dict: dict, fig_dict: dict):

    phu_cases = data_dict['cases_phu']
    phu_tests = data_dict['tests_phu']

    tests_view = phu_tests[phu_tests['DATE'] == max(phu_tests['DATE'])]
    cases_view = phu_cases[phu_cases['FILE_DATE'] == max(phu_cases['FILE_DATE'])]

    ont_map = data_dict['ont_map']

    merged_cases_view = pd.merge(data_dict['phu_match'], cases_view, how="left", left_on="PHU_ID", right_on="PHU_NUM") 
    merged_tests_view = pd.merge(data_dict['phu_match'], tests_view, how="left", left_on="PHU_ID", right_on="PHU_num") 

    ont_map['Cases'] = merged_cases_view['ACTIVE_CASES']
    ont_map['PHU'] = merged_cases_view['NAME_ENG']
    ont_map['Test Positive Rate'] = merged_tests_view['percent_positive_7d_avg']
    ont_map['id'] = ont_map.index

    ont_map = ont_map.to_crs(epsg=4326)

    map_ont_ac = px.choropleth(ont_map, geojson=ont_map.geometry, 
                        locations="id", color="Cases", 
                        hover_data={'PHU':True, 'Cases':True, 'id':False},
                        fitbounds="locations",
                        height=750,
                        color_continuous_scale="Viridis")

    map_ont_ac.update_geos(resolution=110)

    map_ont_ac.update_layout(
        title=dict(x=0.5),
        title_text='Active Cases by PHU',
        margin={"r":0,"t":30,"l":0,"b":10},
        coloraxis={"colorbar":{"title":{"text":""}},
                   "showscale": False},
        dragmode=False)


    map_ont_test = px.choropleth(ont_map, geojson=ont_map.geometry, 
                        locations="id", color="Test Positive Rate", 
                        hover_data={'PHU':True, 'Test Positive Rate':True, 'id':False},
                        fitbounds="locations",
                        height=750,
                        color_continuous_scale="Viridis")

    map_ont_test.update_geos(resolution=110)

    map_ont_test.update_layout(
        title=dict(x=0.5),
        title_text='Tests Positive Rate by PHU',
        margin={"r":0,"t":30,"l":0,"b":10},
        coloraxis={"colorbar":{"title":{"text":""}},
                   "showscale": False},
        dragmode=False)

    fig_dict['map_ont_ac'] = map_ont_ac
    fig_dict['map_ont_test'] = map_ont_test


    return fig_dict
