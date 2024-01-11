import os 
import pyspark
from pyspark.sql import SparkSession
import pandas as pd

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df = spark.read \
    .option("header", "true") \
    .option("inferSchema",True) \
    .csv('fhvhv_tripdata_2021-01.csv.gz')

df.show(5)


from pyspark.sql import types
schema = types.StructType(
    [
        types.StructField('hvfhs_license_num', types.StringType(), True),
        types.StructField('dispatching_base_num', types.StringType(), True),
        types.StructField('pickup_datetime', types.TimestampType(), True),
        types.StructField('dropoff_datetime', types.TimestampType(), True),
        types.StructField('PULocationID', types.IntegerType(), True),
        types.StructField('DOLocationID', types.IntegerType(), True),
        types.StructField('SR_Flag', types.IntegerType(), True)
    ]
)

df = spark.read \
    .option("header", "true") \
    .option("inferSchema",True) \
    .csv('fhvhv_tripdata_2021-01.csv.gz')

df.schema

df_pandas = pd.read_csv("/Users/artas/GithubProjects/DE-Zoomcamp-FollowAlong/week_5_batch_processing/fhvhv_tripdata_2021-01.csv.gz")

spark.createDataFrame(df_pandas).show()

