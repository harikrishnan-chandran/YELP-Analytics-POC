# Development Checklist – Yelp Analytics POC

## Core Tasks (with Detailed Steps & Commands)

### 1. Set up GCP project, IAM, and storage
- [x] **Create a GCP project**  
  - Project ID: pivotal-rhino-462807-c1
- [x] **Enable required APIs**  
  - BigQuery, Dataproc, Cloud Storage, IAM
- [x] **Create a GCS bucket for data**  
  - Bucket: yelp-analytics-poc-data
- [x] **Set up IAM roles**  
  - Service account has roles:  
    - BigQuery Data Editor  
    - Storage Object Viewer

### 2. Configure environment variables
- [x] **Create `.env` file** with:
  ```
  PROJECT_ID=pivotal-rhino-462807-c1
  DATASET_ID=yelp_analytics
  BUCKET_NAME=yelp-analytics-poc-data
  ```

### 3. Create and activate Python virtual environment
- [x] Virtual environment created (`yap-venv`)
- [x] Activate with:
  ```bash
  source yap-venv/bin/activate
  ```

### 4. Install all dependencies
- [x] All dependencies installed and `requirements.txt` updated:
  ```bash
  pip install -r requirements.txt
  ```

### 5. Ingest Yelp dataset to GCS (Bronze)
- [x] **Download Yelp Open Dataset**  
  - https://www.yelp.com/dataset
- [x] **Upload to GCS**  
  ```bash
  gsutil cp yelp_academic_dataset_*.json gs://yelp-analytics-poc-data/bronze/
  ```

### 6. Implement Spark ETL for Silver layer (cleansing/enrichment)
- [x] **Write Spark scripts in `src/spark/`**  
  - File: `src/spark/yelp_analytics.py`
- [x] **Run on Dataproc**  
  ```bash
  gcloud dataproc jobs submit pyspark src/spark/yelp_analytics.py --cluster=yelp-analytics-cluster --region=us-central1
  ```

### 7. Implement Spark ETL for Gold layer (aggregation/star schema)
- [x] **Write Spark scripts in `src/spark/`**  
  - File: `src/spark/yelp_analytics.py`
- [x] **Run on Dataproc**  
  ```bash
  gcloud dataproc jobs submit pyspark src/spark/yelp_analytics.py --cluster=yelp-analytics-cluster --region=us-central1
  ```

### 8. Load Gold tables to BigQuery
- [x] **Load processed data from GCS to BigQuery**  
  ```bash
  bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON yelp_analytics.<table> gs://yelp-analytics-poc-data/gold/<table>.json
  ```

### 9. Build Streamlit dashboard (ratings, sentiment, trends)
- [x] **Develop dashboard in `src/dashboard/app.py`**
- [x] **Run locally:**
  ```bash
  streamlit run src/dashboard/app.py
  ```

### 10. Add unit tests for ETL and dashboard
- [x] **Write tests in `tests/`** (mirroring `src/` structure)
- [x] **Run tests:**
  ```bash
  pytest
  ```

### 11. Document code and update README
- [x] Initial documentation and README created
- [x] Updated documentation to reflect current architecture

---

## Discovered During Work
- [x] Migrated from Dataflow to Dataproc for better cost efficiency
- [x] Consolidated requirements.txt files
- [x] Removed unused files and configurations
- [x] Updated pipeline scripts for Spark processing

---

## Completed Tasks
- [x] Create project folder structure
- [x] Create and activate Python virtual environment
- [x] Install all dependencies and update requirements.txt
- [x] Create initial documentation
- [x] Set up GCP project and IAM
- [x] Implement Spark ETL pipeline
- [x] Build Streamlit dashboard
- [x] Write unit tests
- [x] Update documentation