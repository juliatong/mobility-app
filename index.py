import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mobility_data.db')
#
# df = pd.read_csv(filepath_or_buffer='resources/applemobilitytrends-2021-07-31.csv')
#
df2 = pd.read_json(path_or_buf='resources/sample_data_payload.json', orient='index', convert_dates=False, convert_axes=False)

df3 = pd.read_sql_query(f"SELECT * FROM regions "
                        f"WHERE region = 'Monaghan' "
                        f"AND `sub-region` IS NULL",
                        engine)

# transportation_type = ['walking', 'driving', 'transit']
#
# regions_table = pd.read_sql_query(
#     f"SELECT * FROM regions WHERE transportation_type in {transportation_type}",
#     engine)
#
#  Write Table 1 - Regions
# regions_table = df \
#     .sort_values(by='region') \
#     .reset_index(drop=True)
#
# regions_table.to_sql("regions", engine, if_exists='replace')
#
# ashe = df[df.region == "Ashe County"]
#
# ashe = ashe.reset_index(drop=True)
#
# ashe = ashe.drop(columns=['geo_type', 'region', 'transportation_type', 'alternative_name', 'sub-region', 'country'])
