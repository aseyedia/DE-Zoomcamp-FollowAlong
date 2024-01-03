# pgcli -h localhost -u root -p 5432 -d ny_taxi
import pandas as pd
from sqlalchemy import create_engine
import os

os.chdir("/week_1_basics_n_setup/2_docker_sql")

df = pd.read_csv('yellow_tripdata_2021-01.csv', low_memory=False)

df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')