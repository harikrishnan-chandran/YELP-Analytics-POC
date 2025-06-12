"""
GCP and project configuration template for Yelp Analytics POC (Dataflow version).
Fill in with your actual project details.
"""
from typing import Optional

class GCPConfig:
    """
    Google Cloud Platform configuration settings for Dataflow-based pipeline.

    Args:
        project_id (str): GCP project ID.
        bucket_name (str): GCS bucket for data storage.
        bq_dataset (str): BigQuery dataset name.
        region (str): GCP region.
        dataflow_job_name (str): Dataflow job name prefix.
    """
    def __init__(self,
                 project_id: str = "your-gcp-project-id",
                 bucket_name: str = "your-gcs-bucket",
                 bq_dataset: str = "your_bq_dataset",
                 region: str = "us-central1",
                 dataflow_job_name: str = "yelp-etl-job"):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.bq_dataset = bq_dataset
        self.region = region
        self.dataflow_job_name = dataflow_job_name

# Example usage:
# config = GCPConfig() 