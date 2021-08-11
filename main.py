from typing import Optional

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pandas import DataFrame
from pydantic import BaseModel
from sqlalchemy import create_engine


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

engine = create_engine('sqlite:///mobility_data.db')


def get_traffic_from_transportation_type(traffic_data_frame: DataFrame):
    if traffic_data_frame.empty:
        traffic_data_frame = {}
    else:
        traffic_data_frame = traffic_data_frame.reset_index(drop=True)
        traffic_data_frame = traffic_data_frame.drop(columns=['index',
                                                              'geo_type',
                                                              'region',
                                                              'transportation_type',
                                                              'alternative_name',
                                                              'sub-region',
                                                              'country',
                                                              'lock']
                                                     )
        traffic_data_frame = traffic_data_frame.fillna('')
        traffic_data_frame = traffic_data_frame.T.to_dict()[0]

    return traffic_data_frame


@app.post("/load-csv")
def load_csv(request: Request):
    df = pd.read_csv('resources/applemobilitytrends-2021-07-31.csv')
    #  Write Regions Table
    regions_table = df \
        .sort_values(by='region') \
        .reset_index(drop=True)

    regions_table['lock'] = False

    regions_table.to_sql("regions", engine, if_exists='replace')

    return {'response': 'success'}


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/api/regions/{geo_type}")
def read_regions(geo_type: str):
    # Probably should replace this with a live DB check
    if geo_type not in ["country", "city", "sub-region", "county"]:
        return {'error': 'GeoType not found'}

    if geo_type == "country":
        geo_type = "country/region"

    regions_table = pd.read_sql_query(
        f"SELECT region, `sub-region`, country FROM regions WHERE geo_type = '{geo_type}' ORDER BY region",
        engine)

    regions_table = regions_table.drop_duplicates(['region', 'sub-region', 'country'])

    regions = regions_table.to_dict(orient='records')

    return {'geoType': geo_type, 'regions': regions}


def _read_traffic(region: str,
                  sub_region: str = '',
                  transit: bool = False,
                  driving: bool = False,
                  walking: bool = False):
    if sub_region:
        regions_table = pd.read_sql_query(f"SELECT * FROM regions "
                                          f"WHERE region = '{region}' "
                                          f"AND `sub-region` = '{sub_region}'",
                                          engine)
    else:
        regions_table = pd.read_sql_query(f"SELECT * FROM regions "
                                          f"WHERE region = '{region}' "
                                          f"AND `sub-region` IS NULL",
                                          engine)

    if regions_table.empty:
        return {
            'error': f'Region {region} with Sub Region {sub_region} not found'
        }

    if transit:
        traffic = regions_table.loc[regions_table['transportation_type'] == 'transit']
        transit = get_traffic_from_transportation_type(traffic)

    if driving:
        traffic = regions_table.loc[regions_table['transportation_type'] == 'driving']
        driving = get_traffic_from_transportation_type(traffic)

    if walking:
        traffic = regions_table.loc[regions_table['transportation_type'] == 'walking']
        walking = get_traffic_from_transportation_type(traffic)

    first_record = regions_table.iloc[0]

    return {
        "regions": [
            {
                "alternative_name": first_record['alternative_name'],
                "country": first_record['country'],
                "geo_type": first_record['geo_type'],
                "region_name": first_record['region'],
                "sub_region": first_record['sub-region'],
                "direction_requests": {
                    "transit": transit,
                    "driving": driving,
                    "walking": walking
                }
            }
        ]
    }


@app.get("/api/traffic")
def read_traffic(region: str,
                 sub_region: str = '',
                 transit: bool = False,
                 driving: bool = False,
                 walking: bool = False):
    return _read_traffic(region, sub_region, transit, driving, walking)


class UpdateTrafficPayload(BaseModel):
    region: str
    sub_region: Optional[str] = ''
    traffic: dict


@app.put("/api/traffic")
def update_traffic(traffic_payload: UpdateTrafficPayload):
    update_data = []

    if 'transit' in traffic_payload.traffic:
        transit_data = traffic_payload.traffic['transit']
        update_data.append((transit_data, 'transit'))
    else:
        transit_data = {}

    if 'driving' in traffic_payload.traffic:
        driving_data = traffic_payload.traffic['driving']
        update_data.append((driving_data, 'driving'))
    else:
        driving_data = {}

    if 'walking' in traffic_payload.traffic:
        walking_data = traffic_payload.traffic['walking']
        update_data.append((walking_data, 'walking'))
    else:
        walking_data = {}

    if traffic_payload.sub_region:
        region_data = pd.read_sql_query(f"SELECT "
                                        f"* FROM regions "
                                        f"WHERE region = '{traffic_payload.region}' "
                                        f"AND `sub-region` = '{traffic_payload.sub_region}' ",
                                        engine)
    else:
        region_data = pd.read_sql_query(f"SELECT "
                                        f"* FROM regions "
                                        f"WHERE region = '{traffic_payload.region}' "
                                        f"AND `sub-region` IS NULL ",
                                        engine)
    if region_data.empty:
        return {'error': f'Region {traffic_payload.region} not found'}

    if not region_data[region_data.lock == 1].empty:
        return {'error': f'Region {traffic_payload.region} is locked'}

    # Combine the data with non data columns
    # Delete the original data
    # Append the new data

    with engine.connect() as con:

        for data in update_data:
            if data[0]:

                # Convert string to float
                for k, v in data[0].items():
                    if v == '':
                        data[0][k] = 0
                    else:
                        data[0][k] = float(v)

                traffic_dataframe = region_data[region_data.transportation_type == data[1]]
                traffic_dict = traffic_dataframe.to_dict(orient='records')
                traffic_dict[0].update(data[0])

                con.execute(f"DELETE FROM regions WHERE `index` = '{traffic_dataframe.iloc[0]['index']}'")

                new_traffic_dataframe = pd.DataFrame.from_dict(traffic_dict)
                new_traffic_dataframe = new_traffic_dataframe.set_index('index')
                new_traffic_dataframe.to_sql('regions', engine, if_exists='append')

    return _read_traffic(traffic_payload.region, traffic_payload.sub_region, transit_data, driving_data, walking_data)


@app.get("/api/traffic/filter")
def filtered_traffic(transit: bool = False,
                     driving: bool = False,
                     walking: bool = False,
                     traffic_filter_type: str = 'gt',
                     traffic_filter_amount: int = 0):
    transportation_type = []

    if traffic_filter_type not in ['lt', 'gt']:
        return {'error', 'traffic_filter_type must be lt or gt'}

    if transit:
        transportation_type.append('transit')
    if driving:
        transportation_type.append('driving')
    if walking:
        transportation_type.append('walking')

    if len(transportation_type) > 1:
        transportation_type = tuple(transportation_type)
    elif len(transportation_type) == 1:
        transportation_type = f"('{transportation_type[0]}')"
    else:
        return {"error": "No Transportation Type Selected"}

    regions_table = pd.read_sql_query(
        f"SELECT * FROM regions WHERE transportation_type in {transportation_type}",
        engine)

    data_only_regions_table = regions_table.drop(columns=['index',
                                                          'geo_type',
                                                          'region',
                                                          'transportation_type',
                                                          'alternative_name',
                                                          'sub-region',
                                                          'country',
                                                          'lock'])
    data_only_regions_table = data_only_regions_table.fillna(0)

    if traffic_filter_type == 'gt':
        data_only_regions_table = data_only_regions_table[
            (data_only_regions_table.values > traffic_filter_amount).any(1)]
    else:
        data_only_regions_table = data_only_regions_table[
            (data_only_regions_table.values < traffic_filter_amount).any(1)]

    filtered_region_data = regions_table.loc[regions_table.index[data_only_regions_table.index]]

    filtered_regions = filtered_region_data[['region',
                                             'sub-region',
                                             'country',
                                             'alternative_name',
                                             'geo_type']] \
        .drop_duplicates(['region', 'sub-region', 'country'])

    output_dict = {
        "regions": [

        ]
    }

    for index, row in filtered_regions.iterrows():

        traffic_data = filtered_region_data[(filtered_region_data['region'] == row['region'])]
        transit_data = dict()
        driving_data = dict()
        walking_data = dict()

        if transit:
            transit_data = traffic_data[traffic_data['transportation_type'] == 'transit']
            transit_data = get_traffic_from_transportation_type(transit_data)
        if driving:
            driving_data = traffic_data[traffic_data['transportation_type'] == 'driving']
            driving_data = get_traffic_from_transportation_type(driving_data)
        if walking:
            walking_data = traffic_data[traffic_data['transportation_type'] == 'walking']
            walking_data = get_traffic_from_transportation_type(walking_data)

        output_dict['regions'].append({
            "alternative_name": row['alternative_name'],
            "country": row['country'],
            "geo_type": row['geo_type'],
            "region_name": row['region'],
            "sub_region": row['sub-region'],
            "direction_requests": {
                "transit": transit_data,
                "driving": driving_data,
                "walking": walking_data
            }
        })

    return output_dict


class LockTrafficPayload(BaseModel):
    region: str
    sub_region: Optional[str] = ''
    transportation_type: str
    lock: bool = False


@app.post("/api/traffic/lock")
def lock_traffic(lock_payload: LockTrafficPayload):
    print(lock_payload)

    if not lock_payload.transportation_type:
        return {'error': 'transportation_type must be a comma separated string'}

    transportation_type = lock_payload.transportation_type.split(',')

    with engine.connect() as con:
        for transportation_type in transportation_type:
            transportation_type = transportation_type.strip()
            if transportation_type not in ['transit', 'driving', 'walking']:
                return {'error': transportation_type}
            if lock_payload.sub_region:
                sql_sub_region = f"`sub-region` = '{lock_payload.sub_region}'"
            else:
                sql_sub_region = f'`sub-region` IS NULL'
            con.execute(f"UPDATE regions "
                        f"SET lock = {int(lock_payload.lock)} "
                        f"WHERE region = '{lock_payload.region}' "
                        f"AND {sql_sub_region} "
                        f"AND transportation_type = '{transportation_type}'")

            return {
                'region': lock_payload.region,
                'lock': int(lock_payload.lock)
            }
