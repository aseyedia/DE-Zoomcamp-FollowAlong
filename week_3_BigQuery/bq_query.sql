CREATE OR REPLACE EXTERNAL TABLE `dtc-de-398314.trips_data_all.external_trip_data`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_data_lake_dtc-de-398314/data/yellow/yellow_tripdata_2021-*.parquet']
);

CREATE OR REPLACE TABLE `dtc-de-398314.trips_data_all.yellow_tripdata_non_partitioned` AS
SELECT * FROM `dtc-de-398314.trips_data_all.external_trip_data`;

CREATE OR REPLACE TABLE `dtc-de-398314.trips_data_all.yellow_tripdata_partitioned`
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * REPLACE(
  CAST(0 AS NUMERIC) AS VendorID,
  CAST(0 AS NUMERIC) AS payment_type
) FROM `dtc-de-398314.trips_data_all.external_trip_data`;

SELECT table_name, partition_id, total_rows
FROM trips_data_all.INFORMATION_SCHEMA.PARTITIONS
WHERE table_name = 'yellow_tripdata_partitioned'
ORDER BY total_rows DESC;

