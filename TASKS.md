# Development Checklist – Yelp Analytics POC

## Core Tasks (with Detailed Steps & Commands)

### 1. Set up GCP project, IAM, and storage
- [ ] **Create a GCP project**  
  - Go to https://console.cloud.google.com/ and create a new project.
- [ ] **Enable required APIs**  
  - BigQuery, Dataflow, Cloud Storage, Composer, IAM.
- [ ] **Create a GCS bucket for data**  
  - Example command (replace placeholders):  
    ```bash
    gsutil mb -l us-central1 gs://<your-gcs-bucket>
    ```
- [ ] **Set up IAM roles**  
  - Assign yourself and service accounts the roles:  
    - BigQuery Data Editor  
    - Storage Object Viewer

### 2. Configure `config.py` with GCP settings
- [x] `config.py` template exists.  
- [ ] **Edit `config.py`** with your actual GCP project, bucket, dataset, and region.

### 3. Create and activate Python virtual environment
- [x] Virtual environment created (`yap-venv`).
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
- [ ] **Download Yelp Open Dataset**  
  - https://www.yelp.com/dataset
  - Example:
    ```bash
    wget https://.../yelp_dataset.tar
    tar -xvf yelp_dataset.tar
    ```
- [ ] **Upload to GCS**  
  - Example:
    ```bash
    gsutil cp yelp_academic_dataset_*.json gs://<your-gcs-bucket>/bronze/
    ```

### 6. Implement Apache Beam ETL for Silver layer (cleansing/enrichment)
- [ ] **Write Apache Beam scripts in `src/silver/`**  
  - Example file: `src/silver/clean_reviews.py`
- [ ] **Run on Dataflow**  
  - Example:
    ```bash
    python src/silver/clean_reviews.py \
      --runner DataflowRunner \
      --project <project-id> \
      --region <region> \
      --temp_location gs://<bucket>/temp \
      --input gs://<bucket>/bronze/yelp_academic_dataset_review.json \
      --output gs://<bucket>/silver/clean_reviews.json
    ```

### 7. Implement Apache Beam ETL for Gold layer (aggregation/star schema)
- [ ] **Write Apache Beam scripts in `src/gold/`**  
  - Example file: `src/gold/aggregate_reviews.py`
- [ ] **Run on Dataflow**  
  - Example:
    ```bash
    python src/gold/aggregate_reviews.py \
      --runner DataflowRunner \
      --project <project-id> \
      --region <region> \
      --temp_location gs://<bucket>/temp \
      --input gs://<bucket>/silver/clean_reviews.json \
      --output gs://<bucket>/gold/aggregated_reviews.json
    ```

### 8. Load Gold tables to BigQuery
- [ ] **Load processed data from GCS to BigQuery**  
  - Example:
    ```bash
    bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON <dataset>.<table> gs://<your-gcs-bucket>/gold/aggregated_reviews.json
    ```

### 9. Build Streamlit dashboard (ratings, sentiment, trends)
- [ ] **Develop dashboard in `src/dashboard/app.py`**
- [ ] **Run locally:**
  ```bash
  streamlit run src/dashboard/app.py
  ```

### 10. Write Airflow DAGs for orchestration (Cloud Composer)
- [ ] **Write DAGs in `dags/`**
- [ ] **Deploy to Composer environment**  
  - Example:
    ```bash
    gcloud composer environments storage dags import --environment <composer-env> --location <region> --source dags/
    ```

### 11. Add unit tests for ETL and dashboard
- [ ] **Write tests in `tests/`** (mirroring `src/` structure)
- [ ] **Run tests:**
  ```bash
  pytest
  ```

### 12. Document code and update README
- [x] Initial documentation and README created.
- [ ] **Update as new features are added.**

---

## Discovered During Work
- [ ] (Add any new tasks here as you go)

---

## Completed Tasks
- [x] Create project folder structure
- [x] Create and activate Python virtual environment
- [x] Install all dependencies and update requirements.txt
- [x] Create initial documentation: README.md, PROJECT_OBJECTIVE.md, PROJECT_DESIGN.md, config.py, .gitignore