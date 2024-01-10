from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from google.cloud import storage
import os

# Initialize the Google Cloud Storage client
storage_client = storage.Client(project="dtc-de-398314")

@task()
def check_remote_file_exists(bucket_name: str, remote_path: str) -> bool:
    """Check if a file exists in the GCS bucket"""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(remote_path)
    return blob.exists()

@task()
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    # Cleaning steps remain unchanged
    return df

@task()
def write_local(df: pd.DataFrame, local_path: Path) -> Path:
    """Write DataFrame out locally as parquet file"""
    df.to_csv(local_path, compression="gzip")
    return local_path

@task()
def upload_to_gcs(bucket_name: str, local_path: Path, remote_path: str) -> None:
    """Upload local file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=local_path, to_path=remote_path, timeout=300)

@flow()
def etl_web_to_gcs(year: int, month: int, color: str, bucket_name: str, data_dir: Path) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"
    local_path = data_dir / f"{dataset_file}.csv"
    remote_path = data_dir / f"{color}/{dataset_file}.csv"

    # Check if the file already exists in GCS
    if not check_remote_file_exists(bucket_name, remote_path):
        df = fetch(dataset_url)
        df_clean = clean(df)
        local_path = write_local(df_clean, local_path)
        upload_to_gcs(bucket_name, local_path, remote_path)
    else:
        print(f"File {remote_path} already exists in GCS bucket {bucket_name}. Skipping ETL process.")

@flow()
def etl_parent_flow(
    months: list[int], 
    years: list[int], 
    colors: list[str], 
    bucket_name: str, 
    data_dir: str
):
    data_dir_path = Path(data_dir)
    data_dir_path.mkdir(parents=True, exist_ok=True)

    for color in colors:
        current_years = [2019] if color == "fhv" else years
        for year in current_years:
            for month in months:
                etl_web_to_gcs(year, month, color, bucket_name, data_dir_path)

if __name__ == "__main__":
    # Define the bucket name and data directory
    bucket_name = "dtc_data_lake_dtc-de-398314"
    local_data_directory = "data/"

    colors = ["yellow", "green", "fhv"]
    months = [i for i in range(1, 13)]
    years = [2019, 2020]

    # Start the ETL parent flow
    etl_parent_flow(months, years, colors, bucket_name, local_data_directory)
