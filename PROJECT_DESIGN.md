# Project Design: Yelp Analytics POC

## Architecture Overview

This project uses a Medallion architecture (Bronze/Silver/Gold) to process Yelp review data on Google Cloud Platform. The pipeline is implemented using PySpark on Dataproc and visualized with Streamlit.

### 1. Data Ingestion (Bronze Layer)
- **Source**: Yelp Open Dataset (JSON)
- **Storage**: Google Cloud Storage (GCS)
- **Location**: `gs://yelp-analytics-poc-data/bronze/`
- **Goal**: Land raw data for reproducibility and audit

### 2. Data Cleansing & Enrichment (Silver Layer)
- **Processing**: PySpark jobs on Dataproc
- **Location**: `src/spark/yelp_analytics.py`
- **Tasks**: 
  - Clean and validate data
  - Join business and review data
  - Enrich with sentiment analysis
- **Output**: Cleaned, structured data in GCS (`gs://yelp-analytics-poc-data/silver/`)

### 3. Aggregation & Analytics (Gold Layer)
- **Processing**: PySpark jobs on Dataproc
- **Location**: `src/spark/yelp_analytics.py`
- **Tasks**: 
  - Aggregate ratings and sentiment
  - Calculate trends and metrics
  - Create star schema tables
- **Storage**: BigQuery (star schema)
  - Fact Reviews
  - Dim Business
  - Dim User
  - Dim Date

### 4. Visualization
- **Tool**: Streamlit
- **Location**: `src/dashboard/app.py`
- **Features**:
  - Rating distribution
  - Sentiment analysis
  - Geographic trends
  - Time-based trends

## Data Flow Diagram

1. GCS (raw) → 2. Dataproc/Spark (clean/enrich) → 3. GCS (clean) → 4. Dataproc/Spark (aggregate) → 5. BigQuery (analytics) → 6. Streamlit (dashboard)

## Implementation Details

### Spark Processing
- Single PySpark script (`yelp_analytics.py`) handles both Silver and Gold layers
- Uses Spark SQL for transformations
- Implements Medallion pattern in memory
- Writes results to GCS and BigQuery

### BigQuery Schema
- Star schema design
- Partitioned by date
- Clustered by business_id
- Optimized for dashboard queries

### Dashboard
- Streamlit-based visualization
- Real-time BigQuery queries
- Interactive filters and charts
- Responsive design

## Security & Cost
- IAM roles: BigQuery Data Editor, Storage Object Viewer
- Service account: `yelp-dataflow-sa-key.json`
- Cost optimization:
  - Delete Dataproc clusters when idle
  - Use appropriate machine types
  - Monitor BigQuery usage
  - Clean up temporary GCS data

## References
- [Medallion Architecture](https://databricks.com/glossary/medallion-architecture)
- [Yelp Open Dataset](https://www.yelp.com/dataset)
- [Google Cloud Dataproc](https://cloud.google.com/dataproc)
- [Apache Spark](https://spark.apache.org/)
- [Streamlit](https://streamlit.io/) 