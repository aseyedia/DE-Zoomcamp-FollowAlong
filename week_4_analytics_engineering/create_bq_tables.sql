CREATE OR REPLACE EXTERNAL TABLE `dtc-de-398314.trips_data_all.yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_dtc-de-398314/yellow/yellow_tripdata_*.csv']
);

CREATE OR REPLACE EXTERNAL TABLE `dtc-de-398314.trips_data_all.green_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_dtc-de-398314/green/green_tripdata_*.csv']
);

CREATE OR REPLACE EXTERNAL TABLE `dtc-de-398314.trips_data_all.fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_dtc-de-398314/fhv/fhv_tripdata_*.csv']
);

