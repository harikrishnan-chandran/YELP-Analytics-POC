# GCP Setup Guide for Yelp Analytics POC

## 1. Project Configuration

### 1.1 Project Details
- **Project ID:** pivotal-rhino-462807-c1
- **Region:** us-central1
- **Zone:** us-central1-a (default)

### 1.2 Required APIs
The following Google Cloud APIs must be enabled:
- Cloud Storage API
- BigQuery API
- Dataproc API
- Dataflow API
- Cloud Scheduler API

Enable APIs using:
```bash
gcloud services enable \
    storage.googleapis.com \
    bigquery.googleapis.com \
    dataproc.googleapis.com \
    dataflow.googleapis.com \
    cloudscheduler.googleapis.com
```

## 2. Service Account Setup

### 2.1 Create Service Account
```bash
gcloud iam service-accounts create yelp-dataflow \
    --display-name="Yelp Analytics Dataflow Service Account"
```

### 2.2 Required IAM Roles
The service account needs the following roles:
- Storage Admin (`roles/storage.admin`)
- BigQuery Admin (`roles/bigquery.admin`)
- Dataproc Admin (`roles/dataproc.admin`)

Grant roles using:
```bash
gcloud projects add-iam-policy-binding pivotal-rhino-462807-c1 \
    --member="serviceAccount:yelp-dataflow@pivotal-rhino-462807-c1.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding pivotal-rhino-462807-c1 \
    --member="serviceAccount:yelp-dataflow@pivotal-rhino-462807-c1.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding pivotal-rhino-462807-c1 \
    --member="serviceAccount:yelp-dataflow@pivotal-rhino-462807-c1.iam.gserviceaccount.com" \
    --role="roles/dataproc.admin"
```

### 2.3 Service Account Key
Create and download the service account key:
```bash
gcloud iam service-accounts keys create yelp-dataflow-sa-key.json \
    --iam-account=yelp-dataflow@pivotal-rhino-462807-c1.iam.gserviceaccount.com
```

## 3. Storage Setup

### 3.1 GCS Bucket
- **Bucket Name:** yelp-analytics-poc-data
- **Location:** us-central1
- **Storage Class:** Standard
- **Access Control:** Uniform

Create bucket:
```bash
gsutil mb -l us-central1 gs://yelp-analytics-poc-data
```

### 3.2 Data Organization
```
gs://yelp-analytics-poc-data/
├── raw/                    # Bronze layer
│   ├── business/
│   ├── review/
│   └── user/
├── processed/              # Silver layer
└── analytics/             # Gold layer
```

## 4. BigQuery Setup

### 4.1 Dataset
- **Dataset ID:** yelp_analytics
- **Location:** US
- **Default Table Expiration:** None

Create dataset:
```bash
bq mk --location=US pivotal-rhino-462807-c1:yelp_analytics
```

### 4.2 Tables
The pipeline creates the following tables:
- `yelp_analytics.business_metrics`
- `yelp_analytics.review_trends`

## 5. Service Interactions

### 5.1 Data Flow
1. **GCS → Dataproc**
   - Dataproc reads raw data from GCS
   - Uses service account for authentication
   - Requires `storage.objects.get` permission

2. **Dataproc → BigQuery**
   - Processed data written to BigQuery
   - Uses service account for authentication
   - Requires `bigquery.tables.create` and `bigquery.tables.updateData` permissions

### 5.2 Authentication Flow
1. **Local Development**
   - Uses service account key file (`yelp-dataflow-sa-key.json`)
   - Set via environment variable: `GOOGLE_APPLICATION_CREDENTIALS`

2. **Production**
   - Uses workload identity federation
   - No key file required
   - More secure approach

## 6. Environment Variables

Create a `.env` file with:
```bash
# GCP Project Configuration
PROJECT_ID=pivotal-rhino-462807-c1
DATASET_ID=yelp_analytics
BUCKET_NAME=yelp-analytics-poc-data
REGION=us-central1

# Service Account
GOOGLE_APPLICATION_CREDENTIALS=./yelp-dataflow-sa-key.json

# Dataproc Configuration
DATAPROC_CLUSTER=yelp-analytics-cluster
DATAPROC_STAGING_BUCKET=gs://yelp-analytics-poc-dataproc
```

## 7. Security Considerations

### 7.1 Service Account Key
- Store `yelp-dataflow-sa-key.json` securely
- Never commit to version control
- Rotate keys periodically
- Use workload identity in production

### 7.2 Data Access
- Use column-level security in BigQuery
- Implement row-level security for sensitive data
- Encrypt data at rest and in transit

### 7.3 Network Security
- Use VPC Service Controls
- Implement private Google access
- Use Cloud Armor for DDoS protection

## 8. Monitoring and Logging

### 8.1 Cloud Monitoring
- Set up alerts for:
  - Pipeline failures
  - Data processing delays
  - Resource utilization

### 8.2 Cloud Logging
- Monitor:
  - Pipeline execution logs
  - Data processing errors
  - Access patterns

## 9. Cost Management

### 9.1 Resource Quotas
- Set up quotas for:
  - Dataproc clusters
  - BigQuery query bytes
  - GCS storage

### 9.2 Budget Alerts
- Configure budget alerts
- Monitor unexpected usage
- Set up cost controls

## 10. Maintenance

### 10.1 Regular Tasks
- Rotate service account keys
- Update dependencies
- Review IAM permissions
- Monitor resource usage

### 10.2 Backup and Recovery
- Backup BigQuery data
- Document recovery procedures
- Test recovery scenarios 