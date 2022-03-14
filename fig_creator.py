import numpy as np
import pandas as pd

import plotly 
import plotly.express as px
import plotly.graph_objects as go

def create_fig_dict (data_dict: dict):
    '''
    Creates dict of figs for use in Dash application
    '''
    fig_dict = {}
    now = pd.Timestamp.now()

    # Cases Area Charts
    cases_tl = data_dict['cases_tl']
    cases_tl_view = cases_tl[cases_tl['Reported Date'] > now - pd.Timedelta(days=181)]

    case_area_view = pd.DataFrame(data={"Date": cases_tl_view[1:]['Reported Date']}, columns=['Date'])
    case_area_view['Type'] = "Total Cases"
    case_area_view['Value'] = cases_tl_view['ACTIVE_CASES'].to_numpy()[1:]

    death_area_view = pd.DataFrame(data={"Date": cases_tl_view[1:]['Reported Date']}, columns=['Date'])
    death_area_view['Type'] = "Deaths"
    death_area_view['Value'] = cases_tl_view['New Deaths']

    fig_cases_death_area = plotly.subplots.make_subplots(specs=[[{"secondary_y": True}]])

    fig_cases_death_area.add_trace(
        go.Scatter(x=case_area_view['Date'], y=case_area_view['Value'], name="Active Cases", fill='tozeroy'),
        secondary_y=False,
    )

    fig_cases_death_area.add_trace(
        go.Scatter(x=death_area_view['Date'], y=death_area_view['Value'], name="New Deaths", fill='tonexty'),
        secondary_y=True,
    )

    # Set x-axis title
    fig_cases_death_area.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig_cases_death_area.update_yaxes(title_text="Active Cases", secondary_y=False, rangemode="tozero")
    fig_cases_death_area.update_yaxes(title_text="New Deaths", secondary_y=True, rangemode="tozero", range=[0, max(death_area_view['Value'])*1.1])

    fig_dict['fig_cases_death_area'] = fig_cases_death_area

    # Cases Ratio Charts
    cases_vaxed = data_dict['cases_vaxed']
    cases_vaxed['ratio'] = cases_vaxed['cases_full_vac_rate_per100K'] / cases_vaxed['cases_unvac_rate_per100K']
    cases_vaxed_view = cases_vaxed[cases_vaxed['Date'] > now - pd.Timedelta(days=180)]

    cases_vaxed_unvac = pd.DataFrame(data={"Date": cases_vaxed_view['Date']}, columns=['Date'])
    cases_vaxed_unvac["Rate Type"] = "Unvaccinated"
    cases_vaxed_unvac["Rate (Per 100k)"] = cases_vaxed['cases_unvac_rate_per100K']

    cases_vaxed_partvac = pd.DataFrame(data={"Date": cases_vaxed_view['Date']}, columns=['Date'])
    cases_vaxed_partvac["Rate Type"] = "Partially Vaccinated"
    cases_vaxed_partvac["Rate (Per 100k)"] = cases_vaxed['cases_partial_vac_rate_per100K']

    cases_vaxed_fullvac = pd.DataFrame(data={"Date": cases_vaxed_view['Date']}, columns=['Date'])
    cases_vaxed_fullvac["Rate Type"] = "Fully Vaccinated"
    cases_vaxed_fullvac["Rate (Per 100k)"] = cases_vaxed['cases_full_vac_rate_per100K']

    fig_vax_ratio_time = px.line(pd.concat((cases_vaxed_unvac, cases_vaxed_partvac, cases_vaxed_fullvac)), \
        x="Date", y="Rate (Per 100k)", color="Rate Type",
            color_discrete_map={'Unvaccinated': px.colors.qualitative.Plotly[1],
                                'Partially Vaccinated': px.colors.qualitative.Plotly[3],
                                'Fully Vaccinated': px.colors.qualitative.Plotly[0]})

    fig_dict['fig_vax_ratio_time'] = fig_vax_ratio_time

    # Hospitalization Pie Charts
    hosp_vax_view = data_dict['hosp_vax'][data_dict['hosp_vax']['date'] == max(data_dict['hosp_vax']['date'])]
    hosp_vax_stat_view = data_dict['vax_stat'][data_dict['vax_stat']['report_date'] == max(data_dict['vax_stat']['report_date'])]

    hosp_vax_stat_tot_view = hosp_vax_stat_view[['UnVaxed12o','part Vaxed','Tot Vaxed']].T
    hosp_vax_stat_tot_view = hosp_vax_stat_tot_view.rename(columns={hosp_vax_stat_tot_view.columns[0]: "Count"})
    hosp_vax_stat_tot_view["Vaccination Status"] = ["Unvaccinated", "Partially Vaccinated", "Fully Vaccinated"]

    hosp_vax_tot_view = hosp_vax_view[['tot_unvac','tot_partial_vac','tot_full_vac']].T
    hosp_vax_tot_view = hosp_vax_tot_view.rename(columns={ hosp_vax_tot_view.columns[0]: "Hospitalizations" })
    hosp_vax_tot_view["Vaccination Status"] = ["Unvaccinated", "Partially Vaccinated", "Fully Vaccinated"]

    hosp_vax_icu_view = hosp_vax_view[['icu_unvac','icu_partial_vac','icu_full_vac']].T
    hosp_vax_icu_view = hosp_vax_icu_view.rename(columns={ hosp_vax_icu_view.columns[0]: "Hospitalizations" })
    hosp_vax_icu_view["Vaccination Status"] = ["Unvaccinated", "Partially Vaccinated", "Fully Vaccinated"]

    hosp_vax_nonicu_view = hosp_vax_view[['hospitalnonicu_unvac', 'hospitalnonicu_partial_vac', 'hospitalnonicu_full_vac']].T
    hosp_vax_nonicu_view = hosp_vax_nonicu_view.rename(columns={ hosp_vax_nonicu_view.columns[0]: "Hospitalizations" })
    hosp_vax_nonicu_view["Vaccination Status"] = ["Unvaccinated", "Partially Vaccinated", "Fully Vaccinated"]

    fig_hosp_vax_tot = px.pie(hosp_vax_tot_view, values="Hospitalizations", names="Vaccination Status", \
        color="Vaccination Status", title='Vaccination Status of all Hospitalizations', \
             color_discrete_map={'Unvaccinated': px.colors.qualitative.Plotly[1],
                                 'Partially Vaccinated': px.colors.qualitative.Plotly[3],
                                 'Fully Vaccinated': px.colors.qualitative.Plotly[0],
                                 'Boosted' :px.colors.qualitative.Plotly[2]})
    fig_hosp_vax_icu = px.pie(hosp_vax_icu_view, values="Hospitalizations", names="Vaccination Status", \
        color="Vaccination Status", title='Vaccination Status of ICU Hospitalizations', \
             color_discrete_map={'Unvaccinated': px.colors.qualitative.Plotly[1],
                                 'Partially Vaccinated': px.colors.qualitative.Plotly[3],
                                 'Fully Vaccinated': px.colors.qualitative.Plotly[0],
                                 'Boosted' :px.colors.qualitative.Plotly[2]})
    fig_hosp_vax_nonicu = px.pie(hosp_vax_nonicu_view, values="Hospitalizations", names="Vaccination Status", \
        color="Vaccination Status", title='Vaccination Status of Non-ICU Hospitalizations', \
             color_discrete_map={'Unvaccinated': px.colors.qualitative.Plotly[1],
                                 'Partially Vaccinated': px.colors.qualitative.Plotly[3],
                                 'Fully Vaccinated': px.colors.qualitative.Plotly[0],
                                 'Boosted' :px.colors.qualitative.Plotly[2]})
    fig_hosp_general_pop = px.pie(hosp_vax_stat_tot_view, values="Count", names="Vaccination Status", \
        color="Vaccination Status", title='Overall Ontario Vaccination Status (Ages 12+)', height=270, \
             color_discrete_map={'Unvaccinated': px.colors.qualitative.Plotly[1],
                                 'Partially Vaccinated': px.colors.qualitative.Plotly[3],
                                 'Fully Vaccinated': px.colors.qualitative.Plotly[0],
                                 'Boosted' :px.colors.qualitative.Plotly[2]})

    fig_hosp_general_pop.update_layout(margin=dict(b=0))

    fig_dict['fig_hosp_vax_tot'] = fig_hosp_vax_tot
    fig_dict['fig_hosp_vax_icu'] = fig_hosp_vax_icu
    fig_dict['fig_hosp_vax_nonicu'] = fig_hosp_vax_nonicu
    fig_dict['fig_hosp_general_pop'] = fig_hosp_general_pop

    # Vaccination Area Charts
    vax_stat = data_dict['vax_stat']
    vax_stat_view = vax_stat[vax_stat['Date'] > now - pd.Timedelta(days=180)]

    part_area_view = pd.DataFrame(data={"Date": vax_stat_view['Date']}, columns=['Date'])
    part_area_view['Vaccination Status'] = "Partially Vaccinated"
    part_area_view['Percentage'] = (vax_stat['total_individuals_at_least_one'] - vax_stat['Tot Vaxed']) / 14826276

    fully_area_view = pd.DataFrame(data={"Date": vax_stat_view['Date']}, columns=['Date'])
    fully_area_view['Vaccination Status'] = "Fully Vaccinated"
    fully_area_view['Percentage'] = (vax_stat['Tot Vaxed'] - vax_stat['total_individuals_3doses'].fillna(0)) / 14826276

    boosted_area_view = pd.DataFrame(data={"Date": vax_stat_view['Date']}, columns=['Date'])
    boosted_area_view['Vaccination Status'] = "Boosted"
    boosted_area_view['Percentage'] = vax_stat['total_individuals_3doses'] / 14826276
    

    fig_vax = px.area(pd.concat((boosted_area_view, fully_area_view, part_area_view)), x="Date", y="Percentage", color='Vaccination Status', \
            color_discrete_map={'Unvaccinated': px.colors.qualitative.Plotly[1],
                                 'Partially Vaccinated': px.colors.qualitative.Plotly[3],
                                 'Fully Vaccinated': px.colors.qualitative.Plotly[0],
                                 'Boosted' :px.colors.qualitative.Plotly[2]})

    # Vaccination Pie Charts
    vax_age = data_dict['vax_age']
    vax_age_view = vax_age[vax_age['Date'] > now - pd.Timedelta(days=1)]
    groups =['05-11yrs', '12-17yrs', '18-29yrs', '30-39yrs','40-49yrs','50-59yrs','60-69yrs','70-79yrs', '80+']
    groupnm =['5-11 Year Olds', '12-17 Year Olds', '18-29 Year Olds', '30-39 Year Olds', \
        '40-49 Year Olds','50-59 Year Olds','60-69 Year Olds','70-79 Year Olds', '80+ Year Olds']

    for gp in range(len(groups)):
        view_age_view_gp = vax_age_view[vax_age_view['Agegroup'] == groups[gp]]
        df = pd.DataFrame(data={'Vaccination Status': ['Unvaccinated', 'Partially Vaccinated', 'Fully Vaccinated', 'Boosted'],\
                             'Count': [view_age_view_gp['Total population'].to_numpy()[0] - view_age_view_gp['At least one dose_cumulative'].to_numpy()[0],
                                        view_age_view_gp['At least one dose_cumulative'].to_numpy()[0] - view_age_view_gp['fully_vaccinated_cumulative'].to_numpy()[0],
                                        view_age_view_gp['fully_vaccinated_cumulative'].to_numpy()[0] - view_age_view_gp['third_dose_cumulative'].to_numpy()[0],
                                        view_age_view_gp['third_dose_cumulative'].to_numpy()[0]]})

        pie_fig = px.pie(df, values='Count', names='Vaccination Status', color="Vaccination Status", title='Vaccination Status for '+ groupnm[gp], \
            color_discrete_map={'Unvaccinated': px.colors.qualitative.Plotly[1],
                                 'Partially Vaccinated': px.colors.qualitative.Plotly[3],
                                 'Fully Vaccinated': px.colors.qualitative.Plotly[0],
                                 'Boosted' :px.colors.qualitative.Plotly[2]})
        pie_fig.update_traces(sort=False) 
        fig_dict['vax'+str(gp)] = pie_fig
    fig_dict['fig_vax'] = fig_vax

    # Hospitalization Area Charts
    hosp_area_view = data_dict['hosp_vax'][data_dict['hosp_vax']['date'] > now - pd.Timedelta(days=180)]

    hosp_area_view_icu = pd.DataFrame(data={"Date": hosp_area_view['date']}, columns=['Date'])
    hosp_area_view_icu['Type'] = "ICU"
    hosp_area_view_icu['Hospitalizations'] = hosp_area_view['icu']

    hosp_area_view_nonicu = pd.DataFrame(data={"Date": hosp_area_view['date']}, columns=['Date'])
    hosp_area_view_nonicu['Type'] = "Non-ICU"
    hosp_area_view_nonicu['Hospitalizations'] = hosp_area_view['nonicu']

    fig_hosp_area = px.area(pd.concat([hosp_area_view_icu, hosp_area_view_nonicu], ignore_index=True), x="Date",
                            y='Hospitalizations', color="Type",
                            line_group="Type")


    fig_dict['fig_hosp_area'] = fig_hosp_area

    # Tests Line and Area Charts
    tests_area_view = data_dict['cases_tl'][data_dict['cases_tl']['Reported Date'] > now - pd.Timedelta(days=180)]

    tests_area_view_overall = pd.DataFrame(data={"Date": tests_area_view['Reported Date']}, columns=['Date'])
    tests_area_view_overall['Type'] = "Tests"
    tests_area_view_overall['Count'] = data_dict['cases_tl']['Tests']

    tests_area_view_pos = pd.DataFrame(data={"Date": tests_area_view['Reported Date']}, columns=['Date'])
    tests_area_view_pos['Type'] = "Positive Tests"
    tests_area_view_pos['Count'] = data_dict['cases_tl']['Positive Tests']

    tests_age = data_dict['tests_age']
    tests_age_view = tests_age[tests_age['DATE'] > now - pd.Timedelta(days=180)]

    fig_tests_age = px.line(tests_age_view, x="DATE", y="percent_positive_7d_avg", color='age_category', \
                labels={
                     "DATE": "Date",
                     "age_category": "Age Category",
                     "percent_positive_7d_avg": "% Positive (7 Day Average)"
                 },)

    fig_dict['fig_tests_age'] = fig_tests_age


    tests_hosp_area = px.area(pd.concat([tests_area_view_pos,tests_area_view_overall], ignore_index=True), x="Date",
                            y='Count', color="Type",
                            line_group="Type")

    fig_dict['tests_hosp_area'] = tests_hosp_area

    # Maps
    fig_dict = create_maps(data_dict, fig_dict)

    return now, fig_dict

def create_maps (data_dict: dict, fig_dict: dict):

    phu_cases = data_dict['cases_phu']
    phu_tests = data_dict['tests_phu']

    tests_view = phu_tests[phu_tests['DATE'] == max(phu_tests['DATE'])]
    cases_view = phu_cases[phu_cases['FILE_DATE'] == max(phu_cases['FILE_DATE'])]

    phu_map = data_dict['phu_map']

    merged_cases_view = pd.merge(data_dict['phu_match'], cases_view, how="left", left_on="PHU_ID", right_on="PHU_NUM") 
    merged_tests_view = pd.merge(data_dict['phu_match'], tests_view, how="left", left_on="PHU_ID", right_on="PHU_num") 

    phu_map['Active Cases'] = merged_cases_view['ACTIVE_CASES'] 
    phu_map['Active Case Rate (Per 100k)'] = merged_cases_view['ACTIVE_CASES'] / merged_cases_view['POP'] * 100000

    phu_map['PHU'] = merged_cases_view['NAME_ENG']
    phu_map['Test Positive Rate'] = merged_tests_view['percent_positive_7d_avg']
    phu_map['Testing Volume'] = merged_tests_view['test_volumes_7d_avg']
    phu_map['Testing Rate (Per 1000)'] = merged_tests_view['tests_per_1000_7d_avg']
    phu_map['id'] = phu_map.index

    phu_map = phu_map.to_crs(epsg=4326)

    map_cases_count = px.choropleth(phu_map, geojson=phu_map.geometry, 
                        locations="id", color="Active Cases", 
                        hover_data={'PHU':True, 'Active Cases':True, 'id':False},
                        fitbounds="locations",
                        height=750,
                        color_continuous_scale="ylorrd")

    map_cases_count.update_geos(resolution=110)

    map_cases_count.update_layout(
        title=dict(x=0.5),
        title_text='Active Cases by PHU',
        margin={"r":0,"t":30,"l":0,"b":10},
        coloraxis={"colorbar":{"title":{"text":""}},
                   "showscale": False},
        dragmode=False)

    map_cases_rate = px.choropleth(phu_map, geojson=phu_map.geometry, 
                        locations="id", color="Active Case Rate (Per 100k)", 
                        hover_data={'PHU':True, 'Active Case Rate (Per 100k)':True, 'id':False},
                        fitbounds="locations",
                        height=750,
                        color_continuous_scale="ylorrd")

    map_cases_rate.update_geos(resolution=110)

    map_cases_rate.update_layout(
        title=dict(x=0.5),
        title_text='Active Case Rate (Per 100k) by PHU',
        margin={"r":0,"t":30,"l":0,"b":10},
        coloraxis={"colorbar":{"title":{"text":""}},
                   "showscale": False},
        dragmode=False)


    map_ont_test_count = px.choropleth(phu_map, geojson=phu_map.geometry, 
                        locations="id", color="Testing Volume", 
                        hover_data={'PHU':True, 'Testing Volume':True, 'id':False},
                        fitbounds="locations",
                        height=750,
                        color_continuous_scale="bugn")

    map_ont_test_count.update_geos(resolution=110)

    map_ont_test_count.update_layout(
        title=dict(x=0.5),
        title_text='Testing Volume by PHU',
        margin={"r":0,"t":30,"l":0,"b":10},
        coloraxis={"colorbar":{"title":{"text":""}},
                   "showscale": False},
        dragmode=False)


    map_ont_test_rate = px.choropleth(phu_map, geojson=phu_map.geometry, 
                        locations="id", color="Testing Rate (Per 1000)", 
                        hover_data={'PHU':True, 'Testing Rate (Per 1000)':True, 'id':False},
                        fitbounds="locations",
                        height=750,
                        color_continuous_scale="bugn")

    map_ont_test_rate.update_geos(resolution=110)

    map_ont_test_rate.update_layout(
        title=dict(x=0.5),
        title_text='Testing Rate (Per 1000) by PHU',
        margin={"r":0,"t":30,"l":0,"b":10},
        coloraxis={"colorbar":{"title":{"text":""}},
                   "showscale": False},
        dragmode=False)



    map_ont_test_tpr = px.choropleth(phu_map, geojson=phu_map.geometry, 
                        locations="id", color="Test Positive Rate", 
                        hover_data={'PHU':True, 'Test Positive Rate':True, 'id':False},
                        fitbounds="locations",
                        height=750,
                        color_continuous_scale="ylorrd")

    map_ont_test_tpr.update_geos(resolution=110)

    map_ont_test_tpr.update_layout(
        title=dict(x=0.5),
        title_text='Test Positive Rate by PHU',
        margin={"r":0,"t":30,"l":0,"b":10},
        coloraxis={"colorbar":{"title":{"text":""}},
                   "showscale": False},
        dragmode=False)

    fig_dict['map_cases_count'] = map_cases_count
    fig_dict['map_cases_rate'] = map_cases_rate
    fig_dict['map_ont_test_tpr'] = map_ont_test_tpr
    fig_dict['map_ont_test_count'] = map_ont_test_count
    fig_dict['map_ont_test_rate'] = map_ont_test_rate


    return fig_dict
