from io import StringIO
from urllib.request import urlopen

import json
import pandas as pd
import geopandas as gpd

def pull_data ():
    '''
    Function pulls data from Ontario Data Catalogue and reads misc data files
    '''

    data_dict = pull_data_from_api()

    assert data_dict is not None

    phu_match = pd.read_csv("./Shapefiles/phu-id-match.csv")
    ont_map = gpd.read_file("./Shapefiles/MOH_PHU_BOUNDARY.shp").set_crs(epsg=4326)

    data_dict['ont_map'] = ont_map
    data_dict['phu_match'] = phu_match

    return data_dict

def pull_data_from_api ():
    '''
    Function pulls data from Ontario Data Catalogue, returns None if failure.
    '''
    key_dict = {"cases_tl":"https://data.ontario.ca/api/3/action/datastore_search?resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11&limit=1000000", 
                "cases_phu": "https://data.ontario.ca/api/3/action/datastore_search?resource_id=d1bfe1ad-6575-4352-8302-09ca81f7ddfc&limit=1000000",
                "tests_phu": "https://data.ontario.ca/api/3/action/datastore_search?resource_id=07bc0e21-26b5-4152-b609-c1958cb7b227&limit=1000000"}

    data_dict = {}

    try:
        for key, key_url in key_dict.items():
            fileobj = urlopen(key_url)
            jsonobj = json.load(fileobj)

            io = StringIO()
            json.dump(jsonobj['result']['records'], io)

            data_dict[key] = pd.read_json(io.getvalue(), orient='records')
    except:
        return None

    return data_dict