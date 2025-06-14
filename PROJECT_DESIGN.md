# Project Design: Yelp Analytics POC

## Architecture Overview

This project uses a Medallion architecture (Bronze/Silver/Gold) to process Yelp review data on Google Cloud Platform. The pipeline is orchestrated using Cloud Composer (Airflow) and visualized with Streamlit.

### 1. Data Ingestion (Bronze Layer)
- **Source**: Yelp Open Dataset (JSON/CSV) or API
- **Storage**: Google Cloud Storage (GCS)
- **Goal**: Land raw data for reproducibility and audit

### 2. Data Cleansing & Enrichment (Silver Layer)
- **Processing**: PySpark jobs on Dataproc
- **Tasks**: Clean, join, enrich business, user, and review data
- **Output**: Cleaned, structured data in GCS

### 3. Aggregation & Analytics (Gold Layer)
- **Processing**: PySpark jobs on Dataproc
- **Tasks**: Aggregate for rating distribution, sentiment, trends
- **Storage**: BigQuery (star schema: Fact Reviews, Dim Business, Dim User, Dim Date)

### 4. Orchestration
- **Tool**: Cloud Composer (Apache Airflow)
- **Purpose**: Schedule and monitor ETL jobs

### 5. Visualization
- **Tool**: Streamlit
- **Purpose**: Interactive dashboard for stakeholders (ratings, sentiment, trends)

## Data Flow Diagram

1. GCS (raw) → 2. Dataproc/Spark (clean/enrich) → 3. GCS (clean) → 4. Dataproc/Spark (aggregate) → 5. BigQuery (analytics) → 6. Streamlit (dashboard)

## Security & Cost
- IAM roles: BigQuery Data Editor, Storage Object Viewer
- Use low-cost GCP services; delete Dataproc clusters when idle

## References
- [Medallion Architecture](https://databricks.com/glossary/medallion-architecture)
- [Yelp Open Dataset](https://www.yelp.com/dataset)
- [Google Cloud Dataproc](https://cloud.google.com/dataproc) 