# GCP Setup Guide (Dataproc/Spark Only)

## Prerequisites
- Google Cloud SDK installed
- Python 3.8+ installed
- Required Python packages installed (`pip install -r requirements.txt`)

## Initial Setup Steps

### 1. Authentication and Project Setup
```bash
# Login to Google Cloud
gcloud auth login

# Set the project
gcloud config set project pivotal-rhino-462807-c1

# Verify the configuration
gcloud config list
```

### 2. Enable Required APIs
```bash
gcloud services enable dataproc.googleapis.com storage.googleapis.com bigquery.googleapis.com compute.googleapis.com
```

### 3. Create and Configure Buckets
```bash
# Create Dataproc staging bucket
gsutil mb -l us-central1 gs://yelp-analytics-poc-dataproc

# (If not already present) Create Yelp data bucket
gsutil mb -l us-central1 gs://yelp-analytics-poc-data
```

### 4. Create Dataproc Cluster (Cost-Effective)
```bash
gcloud dataproc clusters create yelp-analytics-cluster \
    --region=us-central1 \
    --zone=us-central1-a \
    --master-machine-type=e2-standard-2 \
    --master-boot-disk-size=100GB \
    --num-workers=2 \
    --worker-machine-type=e2-standard-2 \
    --worker-boot-disk-size=100GB \
    --image-version=2.1-debian11 \
    --project=pivotal-rhino-462807-c1 \
    --properties=spark:spark.executor.memory=2g,spark:spark.driver.memory=2g \
    --num-preemptible-workers=2
```

### 5. Submit Spark Job
```bash
gcloud dataproc jobs submit pyspark src/spark/yelp_analytics.py \
    --cluster=yelp-analytics-cluster \
    --region=us-central1 \
    -- \
    --input-bucket=gs://yelp-analytics-poc-data \
    --output-bucket=gs://yelp-analytics-poc-dataproc/output
```

### 6. Monitor and Clean Up
```bash
# List jobs
gcloud dataproc jobs list --cluster=yelp-analytics-cluster --region=us-central1

# Delete cluster when done
gcloud dataproc clusters delete yelp-analytics-cluster --region=us-central1 --quiet
```

## Testing the Pipeline

### 1. Verify Permissions
```bash
# Verify service account roles
gcloud projects get-iam-policy pivotal-rhino-462807-c1 \
    --flatten="bindings[].members" \
    --format="table(bindings.role,bindings.members)" \
    --filter="bindings.members:yelp-dataflow-sa@pivotal-rhino-462807-c1.iam.gserviceaccount.com"

# Verify user account roles
gcloud projects get-iam-policy pivotal-rhino-462807-c1 \
    --flatten="bindings[].members" \
    --format="table(bindings.role,bindings.members)" \
    --filter="bindings.members:hari.chandran@infolob.com"
```

### 2. Run Test Pipeline
```bash
# Run the test pipeline with explicit service account (required by org policy)
python src/dataflow/test_pipeline.py \
    --runner=DataflowRunner \
    --temp-location=gs://yelp-analytics-poc-temp/temp \
    --bucket-name=yelp-analytics-poc-test \
    --service_account_email=yelp-dataflow-sa@pivotal-rhino-462807-c1.iam.gserviceaccount.com
```

### 3. Monitor Pipeline
```bash
# List Dataflow jobs
gcloud dataflow jobs list --region=us-central1

# View job details (replace JOB_ID with actual job ID)
gcloud dataflow jobs show JOB_ID --region=us-central1
```

## Troubleshooting

### Common Issues and Solutions

1. **Permission Denied (403) Errors**
   - Verify all required roles are assigned to both service account and user account
   - Check organization policies that might restrict service account usage
   - Ensure the `iam.serviceAccountUser` role is granted to the user account

2. **Service Account Activation Issues**
   - Verify the service account exists and is properly configured
   - Check if the service account has the necessary roles
   - Ensure the user account has permission to act as the service account

3. **Storage Access Issues**
   - Verify bucket permissions
   - Check if the service account has storage admin role
   - Ensure buckets exist in the correct region

### Useful Commands for Debugging

```bash
# Check current authenticated account
gcloud auth list

# Verify project configuration
gcloud config list

# Check service account status
gcloud iam service-accounts list

# View detailed IAM policy
gcloud projects get-iam-policy pivotal-rhino-462807-c1
```

> **Note:**
> Due to the enforced org policy `constraints/dataflow.enforceComputeDefaultServiceAccountCheck`, you must specify a non-default service account for Dataflow jobs. The service account must have all required roles and permissions as described above. 