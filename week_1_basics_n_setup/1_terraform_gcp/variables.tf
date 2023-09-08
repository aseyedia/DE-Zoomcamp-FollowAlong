locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project_id" {
  description = "The ID of the GCP project"
  default     = "dtc-de-398314"
}

variable "credentials_path" {
  description = "Path to the GCP service account credentials JSON file"
  default     = "C:\\Users\\artas\\GitHub_Repos\\DE-Zoomcamp-FollowAlong\\week_1_basics_n_setup\\1_terraform_gcp\\dtc-de-398314-7a55baf20543.json"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "us-east4"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "trips_data_all"
}