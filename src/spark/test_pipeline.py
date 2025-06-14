#!/usr/bin/env python3
"""
End-to-end test for the Yelp Analytics Spark Pipeline.

This script validates the entire pipeline execution on Dataproc, including:
- Reading data from GCS
- Processing through bronze, silver, and gold layers
- Writing results to BigQuery
"""

import os
import subprocess
import time
from google.cloud import bigquery

def run_dataproc_job(project_id, region, cluster_name, input_bucket, output_bucket):
    """Submit and monitor a Dataproc job."""
    job_command = [
        "gcloud", "dataproc", "jobs", "submit", "pyspark",
        "src/spark/yelp_analytics.py",
        f"--cluster={cluster_name}",
        f"--region={region}",
        "--",
        f"--input-bucket={input_bucket}",
        f"--output-bucket={output_bucket}"
    ]

    print("Submitting Dataproc job...")
    subprocess.run(job_command, check=True)

def validate_bigquery_results(project_id, dataset_id):
    """Validate the results in BigQuery."""
    client = bigquery.Client(project=project_id)

    # Check business metrics
    business_query = f"""
    SELECT COUNT(*) as count
    FROM `{project_id}.{dataset_id}.business_metrics`
    """
    business_job = client.query(business_query)
    business_results = business_job.result()
    business_count = next(business_results).count
    assert business_count > 0, "No business metrics found in BigQuery"

    # Check review trends
    review_query = f"""
    SELECT COUNT(*) as count
    FROM `{project_id}.{dataset_id}.review_trends`
    """
    review_job = client.query(review_query)
    review_results = review_job.result()
    review_count = next(review_results).count
    assert review_count > 0, "No review trends found in BigQuery"

    print(f"Found {business_count} business metrics and {review_count} review trends in BigQuery.")

def main():
    project_id = "pivotal-rhino-462807-c1"
    region = "us-central1"
    cluster_name = "yelp-analytics-cluster"
    input_bucket = "gs://yelp-analytics-poc-data"
    output_bucket = "gs://yelp-analytics-poc-dataproc/output"
    dataset_id = "yelp_analytics"

    try:
        # Run the Dataproc job
        run_dataproc_job(project_id, region, cluster_name, input_bucket, output_bucket)

        # Wait for BigQuery tables to be populated
        print("Waiting for BigQuery tables to be populated...")
        time.sleep(30)

        # Validate results
        validate_bigquery_results(project_id, dataset_id)
        print("Pipeline validation successful!")

    except Exception as e:
        print(f"Pipeline validation failed: {e}")
        raise

if __name__ == "__main__":
    main() 