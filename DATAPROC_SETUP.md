# Dataproc Setup Guide for Yelp Analytics POC

## Prerequisites
- Google Cloud SDK installed
- Python 3.8+ installed
- Access to GCP project with Dataproc API enabled
- Sufficient IAM permissions (Dataproc Admin, Storage Admin, BigQuery Admin)

## 1. Enable Required APIs
```bash
gcloud services enable dataproc.googleapis.com \
    storage.googleapis.com \
    bigquery.googleapis.com \
    compute.googleapis.com
```

## 2. Create GCS Bucket for Dataproc
```bash
# Create bucket for Dataproc staging
gsutil mb -l us-central1 gs://yelp-analytics-poc-dataproc

# Create bucket for Yelp data
gsutil mb -l us-central1 gs://yelp-analytics-poc-data
```

## 3. Upload Data to GCS
```bash
# Upload Yelp dataset to GCS
gsutil -m cp -r data/yelp_dataset/* gs://yelp-analytics-poc-data/
```

## 4. Create Dataproc Cluster
```bash
gcloud dataproc clusters create yelp-analytics-cluster \
    --region=us-central1 \
    --zone=us-central1-a \
    --master-machine-type=n1-standard-4 \
    --master-boot-disk-size=500GB \
    --num-workers=2 \
    --worker-machine-type=n1-standard-4 \
    --worker-boot-disk-size=500GB \
    --image-version=2.1-debian11 \
    --project=pivotal-rhino-462807-c1 \
    --properties=spark:spark.executor.memory=4g,spark:spark.driver.memory=4g
```

## 5. Submit Spark Job
```bash
gcloud dataproc jobs submit pyspark \
    --cluster=yelp-analytics-cluster \
    --region=us-central1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    src/spark/yelp_analytics.py \
    -- \
    --input-bucket=gs://yelp-analytics-poc-data \
    --output-bucket=gs://yelp-analytics-poc-dataproc/output
```

## 6. Monitor Job Progress
```bash
# List jobs
gcloud dataproc jobs list --cluster=yelp-analytics-cluster --region=us-central1

# Get job details
gcloud dataproc jobs describe JOB_ID --cluster=yelp-analytics-cluster --region=us-central1
```

## 7. Clean Up
```bash
# Delete cluster when done
gcloud dataproc clusters delete yelp-analytics-cluster --region=us-central1 --quiet

# Delete buckets if needed
gsutil rm -r gs://yelp-analytics-poc-dataproc
```

## Project Structure
```
yelp-analytics-poc/
├── src/
│   └── spark/
│       ├── yelp_analytics.py      # Main Spark job
│       ├── transformations.py     # Data transformation functions
│       └── utils.py              # Utility functions
├── tests/
│   └── spark/
│       └── test_yelp_analytics.py # Spark job tests
└── requirements.txt
```

## Development Workflow
1. Develop and test locally using PySpark
2. Package code and dependencies
3. Submit to Dataproc cluster
4. Monitor job progress
5. Analyze results in BigQuery

## Cost Optimization
- Use preemptible workers for non-critical jobs
- Scale cluster size based on data volume
- Delete cluster when not in use
- Use appropriate machine types

## Troubleshooting
- Check Dataproc job logs in Cloud Logging
- Verify GCS bucket permissions
- Ensure BigQuery dataset exists
- Check cluster status and configuration 