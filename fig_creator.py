import pandas as pd
import plotly.express as px
import numpy as np

def create_fig_dict (data_dict: dict):
    '''
    Creates dict of figs for use in Dash application
    '''
    fig_dict = {}
    now = pd.Timestamp.now()

    # Cases Area Charts
    cases = data_dict['cases_tl']
    view = cases[cases['Reported Date'] > now - pd.Timedelta(days=181)]

    case_area_view = pd.DataFrame(data={"Date": view[1:]['Reported Date']}, columns=['Date'])
    case_area_view['Type'] = "Total Cases"
    case_area_view['Value'] = view['Total Cases'].to_numpy()[1:] - view['Total Cases'].to_numpy()[:-1]

    death_area_view = pd.DataFrame(data={"Date": view[1:]['Reported Date']}, columns=['Date'])
    death_area_view['Type'] = "Deaths"
    death_area_view['Value'] = view['Deaths'].to_numpy()[1:] - view['Deaths'].to_numpy()[:-1]


    fig_case_area = px.area(pd.concat([case_area_view], ignore_index=True), x="Date",
                            y='Value', color="Type",
                            line_group="Type")

    fig_death_area = px.area(pd.concat([death_area_view], ignore_index=True), x="Date",
                            y='Value', color="Type",
                            line_group="Type")

    cases2 = data_dict['cases_vaxed']
    view2 = cases2[cases2['Date'] > now - pd.Timedelta(days=180)]

    cases3 = data_dict['vax_stat']
    view3 = cases3[cases3['Date'] > now - pd.Timedelta(days=180)]

    view4 = pd.merge(view3, view2, on=['Date'])
    view4['ratio'] = (view4['covid19_cases_full_vac']/view4['Tot Vaxed'])/(view4['covid19_cases_unvac']/view4['UnVaxed'])

    df = pd.DataFrame(data={'Vax Status': ['Fully Vaccinated', 'Partially Vaccinated', 'Unvaccinated'], 'values': [np.mean(view4['covid19_cases_full_vac']/view4['Tot Vaxed']), np.mean(view4['covid19_cases_partial_vac']/view4['part Vaxed']), np.mean(view4['covid19_cases_unvac']/view4['UnVaxed'])]})
    fig = px.pie(df, values='values', names='Vax Status', title='Vaccination Status of Covid Cases on average')
    fig_vax_ratio_time = px.line(view4, x="Date", y="ratio",
                            title='Ratio of Ratio of Fully Vaxed cases to Ratio of UnVaxed cases')


    fig_dict['fig_case_area'] = fig_case_area
    fig_dict['fig_death_area'] = fig_death_area
    fig_dict['fig_vax_ratio_time'] = fig_vax_ratio_time
    fig_dict['fig_vax_time'] = fig


    # Hospitalization Pie Charts
    hosp_vax_view = data_dict['hosp_vax'][data_dict['hosp_vax']['date'] == max(data_dict['hosp_vax']['date'])]
    hosp_vax_stat_view = data_dict['vax_stat'][data_dict['vax_stat']['report_date'] == max(data_dict['vax_stat']['report_date'])]

    hosp_vax_stat_tot_view = hosp_vax_stat_view[['UnVaxed12o','part Vaxed','Tot Vaxed']].T
    hosp_vax_stat_tot_view = hosp_vax_stat_tot_view.rename(columns={hosp_vax_stat_tot_view.columns[0]: "Number"})
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

    fig_hosp_vax_tot = px.pie(hosp_vax_tot_view, values="Hospitalizations", names="Vaccination Status", title='Vaccination Status of all Hospitalizations')
    fig_hosp_vax_icu = px.pie(hosp_vax_icu_view, values="Hospitalizations", names="Vaccination Status", title='Vaccination Status of ICU Hospitalizations')
    fig_hosp_vax_nonicu = px.pie(hosp_vax_nonicu_view, values="Hospitalizations", names="Vaccination Status", title='Vaccination Status of Non-ICU Hospitalizations')
    fig_hosp_general_pop = px.pie(hosp_vax_stat_tot_view, values="Number", names="Vaccination Status", title='Overall Ontario Vaccination Status (Ages 12+)', height=270)

    fig_hosp_general_pop.update_layout(margin=dict(b=0))

    fig_dict['fig_hosp_vax_tot'] = fig_hosp_vax_tot
    fig_dict['fig_hosp_vax_icu'] = fig_hosp_vax_icu
    fig_dict['fig_hosp_vax_nonicu'] = fig_hosp_vax_nonicu
    fig_dict['fig_hosp_general_pop'] = fig_hosp_general_pop

    # Vaccination Area Charts
    vax = data_dict['vax_stat']
    view3 = vax[vax['Date'] > now - pd.Timedelta(days=180)]

    part_area_view = pd.DataFrame(data={"Date": view3['Date']}, columns=['Date'])
    part_area_view['Vaccination Status'] = "part Vaxed"
    part_area_view['Value'] = vax['total_individuals_at_least_one']/ 14826276

    fully_area_view = pd.DataFrame(data={"Date": view3['Date']}, columns=['Date'])
    fully_area_view['Vaccination Status'] = "Tot Vaxed"
    fully_area_view['Value'] = vax['Tot Vaxed']/14826276

    import plotly.graph_objects as go

    fig_vax = px.line(part_area_view.append(fully_area_view), x="Date", y="Value", color='Vaccination Status')

    vax_age = data_dict['vax_age']
    view3 = vax_age[vax_age['Date'] > now - pd.Timedelta(days=1)]

    groups =['05-11yrs', '12-17yrs', '18-29yrs', '30-39yrs','40-49yrs','50-59yrs','60-69yrs','70-79yrs']
    values = []
    for gp in groups:
        values.append(view3[view3['Agegroup'] == gp]['Percent_fully_vaccinated'].to_numpy()[0])
    df_1 = pd.DataFrame(data={'Age group': groups, 'values': values})
    pie_fig = px.pie(df_1, values='values', names='Age group', title='Vaccination percentage based on age')

    fig_dict['fig_vax'] = fig_vax
    fig_dict['pie_vax'] = pie_fig

    # Hospitalization Area Charts
    hosp_area_view = data_dict['hosp_vax'][data_dict['hosp_vax']['date'] > now - pd.Timedelta(days=180)]

    hosp_area_view_icu = pd.DataFrame(data={"Date": hosp_area_view['date']}, columns=['Date'])
    hosp_area_view_icu['Type'] = "ICU"
    hosp_area_view_icu['Vaccination Status'] = "Unvaccinated"
    hosp_area_view_icu['Hospitalizations'] = hosp_area_view['icu']

    hosp_area_view_nonicu = pd.DataFrame(data={"Date": hosp_area_view['date']}, columns=['Date'])
    hosp_area_view_nonicu['Type'] = "Non-ICU"
    hosp_area_view_icu['Vaccination Status'] = "Unvaccinated"
    hosp_area_view_nonicu['Hospitalizations'] = hosp_area_view['nonicu']

    fig_hosp_area = px.area(pd.concat([hosp_area_view_icu, hosp_area_view_nonicu], ignore_index=True), x="Date",
                            y='Hospitalizations', color="Type",
                            line_group="Type")


    fig_dict['fig_hosp_area'] = fig_hosp_area


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

    phu_map['Cases'] = merged_cases_view['ACTIVE_CASES']
    phu_map['PHU'] = merged_cases_view['NAME_ENG']
    phu_map['Test Positive Rate'] = merged_tests_view['percent_positive_7d_avg']
    phu_map['id'] = phu_map.index

    phu_map = phu_map.to_crs(epsg=4326)

    map_ont_ac = px.choropleth(phu_map, geojson=phu_map.geometry, 
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


    map_ont_test = px.choropleth(phu_map, geojson=phu_map.geometry, 
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
