from io import StringIO
from urllib.request import urlopen

import json
import pandas as pd
import geopandas as gpd

import os
from datetime import date

key_dict = {
    "cases_tl": "https://data.ontario.ca/api/3/action/datastore_search?resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11&limit=1000000",
    "cases_phu": "https://data.ontario.ca/api/3/action/datastore_search?resource_id=d1bfe1ad-6575-4352-8302-09ca81f7ddfc&limit=1000000",
    "cases_vaxed": "https://data.ontario.ca/api/3/action/datastore_search?resource_id=eed63cf2-83dd-4598-b337-b288c0a89a16&limit=1000000",
    "vax_stat": "https://data.ontario.ca/api/3/action/datastore_search?resource_id=8a89caa9-511c-4568-af89-7f2174b4378c&limit=1000000",
    "hosp_vax": "https://data.ontario.ca/api/3/action/datastore_search?resource_id=274b819c-5d69-4539-a4db-f2950794138c&limit=1000000",
    "tests_phu": "https://data.ontario.ca/api/3/action/datastore_search?resource_id=07bc0e21-26b5-4152-b609-c1958cb7b227&limit=1000000"}

def pull_data():
    '''
    Function pulls data from Ontario Data Catalogue and reads misc data files
    '''

    now = date.today()
    last = None

    if os.path.exists("./data/last_pull.txt"):
        with open("./data/last_pull.txt", 'r') as f:
            last = date.fromisoformat(f.readline())

    if last is not None and now <= last:
        data_dict = pull_data_from_files()
    else:
        data_dict = pull_data_from_api()
        with open("./data/last_pull.txt", 'w') as f:
            f.write(now.isoformat())


    phu_match = pd.read_csv("./shapefiles/phu-id-match.csv")
    phu_map = gpd.read_file("./shapefiles/MOH_PHU_BOUNDARY.shp").set_crs(epsg=4326)

    data_dict['phu_map'] = phu_map
    data_dict['phu_match'] = phu_match

    data_dict = data_transforms(data_dict)

    return data_dict


def pull_data_from_api():
    '''
    Function pulls data from Ontario Data Catalogue, returns None if failure.
    '''

    data_dict = {}

    for key, key_url in key_dict.items():
        fileobj = urlopen(key_url)
        jsonobj = json.load(fileobj)

        io = StringIO()
        json.dump(jsonobj['result']['records'], io)

        data_dict[key] = pd.read_json(io.getvalue(), orient='records')

    for key in data_dict:
        data_dict[key].to_csv(f"./data/{key}.csv", index=False)

    return data_dict

def pull_data_from_files():
    '''
    Function pulls data from stored files, returns None if failure.
    '''

    data_dict = {}

    for key, key_url in key_dict.items():
        data_dict[key] = pd.read_csv(f"./data/{key}.csv")

    return data_dict

def data_transforms (data_dict):

    data_dict['hosp_vax']['icu'] = data_dict['hosp_vax']['icu_unvac'] +\
                                   data_dict['hosp_vax']['icu_partial_vac'] +\
                                   data_dict['hosp_vax']['icu_full_vac']

    data_dict['hosp_vax']['nonicu'] = data_dict['hosp_vax']['hospitalnonicu_unvac'] +\
                                     data_dict['hosp_vax']['hospitalnonicu_partial_vac'] +\
                                     data_dict['hosp_vax']['hospitalnonicu_full_vac'] 

    data_dict['hosp_vax']['date'] = pd.to_datetime(data_dict['hosp_vax']['date'], format='%Y-%m-%d')
    data_dict['hosp_vax']['tot_unvac'] = data_dict['hosp_vax']['hospitalnonicu_unvac'] + data_dict['hosp_vax']['icu_unvac']
    data_dict['hosp_vax']['tot_partial_vac'] = data_dict['hosp_vax']['hospitalnonicu_partial_vac'] + data_dict['hosp_vax']['icu_partial_vac']
    data_dict['hosp_vax']['tot_full_vac'] = data_dict['hosp_vax']['hospitalnonicu_full_vac'] + data_dict['hosp_vax']['icu_full_vac']

    data_dict['hosp_vax']['total'] = data_dict['hosp_vax']['icu'] + data_dict['hosp_vax']['nonicu']


    data_dict['cases_tl']['Reported Date'] = pd.to_datetime(data_dict['cases_tl']['Reported Date'], format='%Y-%m-%d')
    data_dict['cases_vaxed']['Date'] = pd.to_datetime(data_dict['cases_vaxed']['Date'], format='%Y-%m-%d')

    data_dict['cases_vaxed']['Tot Cases'] = data_dict['cases_vaxed']['covid19_cases_unvac'] + data_dict['cases_vaxed']['covid19_cases_partial_vac'] +\
                                            data_dict['cases_vaxed']['covid19_cases_full_vac'] + data_dict['cases_vaxed']['covid19_cases_vac_unknown']


    data_dict['vax_stat']['Date'] = pd.to_datetime(data_dict['vax_stat']['report_date'], format='%Y-%m-%d')
    data_dict['vax_stat']['Tot Vaxed'] = data_dict['vax_stat']['total_individuals_fully_vaccinated']
    data_dict['vax_stat']['part Vaxed'] = data_dict['vax_stat']['total_individuals_partially_vaccinated']
    data_dict['vax_stat']['UnVaxed'] = 14826276 - data_dict['vax_stat']['total_individuals_at_least_one']
    data_dict['vax_stat']['UnVaxed12o'] = 13038032 - data_dict['vax_stat']['total_individuals_at_least_one']

    data_dict['cases_phu']['FILE_DATE'] = pd.to_datetime(data_dict['cases_phu']['FILE_DATE'], format='%Y-%m-%d')
    data_dict['tests_phu']['DATE'] = pd.to_datetime(data_dict['tests_phu']['DATE'], format='%Y-%m-%d')

    return data_dict