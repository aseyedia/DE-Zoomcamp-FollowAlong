import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)
