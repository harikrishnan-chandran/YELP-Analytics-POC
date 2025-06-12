# Yelp Analytics POC

## Overview
This project demonstrates the value of Yelp review data by building a cost-efficient, end-to-end batch analytics pipeline on Google Cloud Platform (GCS → Dataflow → BigQuery) and surfacing actionable insights via a Streamlit dashboard.

## Business Objective
- Ingest and process Yelp business & review data
- Transform data using a Medallion (Bronze/Silver/Gold) architecture
- Store results in BigQuery (star schema)
- Visualize insights (ratings, sentiment, trends) in Streamlit

## Tech Stack
- Google Cloud Storage (GCS)
- Dataflow (Apache Beam)
- BigQuery
- Streamlit
- Cloud Composer (Airflow)
- Python 3.10+

## Architecture
- **Bronze Layer**: Raw ingestion from Yelp Open Dataset/API to GCS
- **Silver Layer**: Cleaned, enriched data via Apache Beam on Dataflow
- **Gold Layer**: Aggregated, analytics-ready tables in BigQuery (star schema)
- **Dashboard**: Streamlit app for interactive insights

## Directory Structure
```
YELP-Analytics-POC/
├── src/                  # Source code (ETL, utils, config)
│   ├── bronze/           # Raw ingestion jobs
│   ├── silver/           # Cleansing/enrichment jobs (Apache Beam)
│   ├── gold/             # Aggregation jobs (Apache Beam)
│   └── dashboard/        # Streamlit app
├── data/                 # Local sample data (if any)
├── notebooks/            # Jupyter/Colab notebooks
├── tests/                # Pytest unit tests
├── dags/                 # Airflow DAGs (Cloud Composer)
├── config.py             # GCP/project config template
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # Project overview
├── PROJECT_OBJECTIVE.md  # Project objective (from BRD)
├── PROJECT_DESIGN.md     # Architecture/design doc
├── TASKS.md              # Development checklist
└── BRD.md                # Business Requirements Document
```

## Setup & Usage
1. Clone repo and install dependencies:
   ```bash
   git clone <repo-url>
   cd YELP-Analytics-POC
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure GCP settings in `config.py`
3. Run ETL jobs (see `src/bronze/`, `src/silver/`, `src/gold/`) using Apache Beam/Dataflow:
   ```bash
   python src/silver/clean_reviews.py --runner DataflowRunner --project <project-id> --region <region> --temp_location gs://<bucket>/temp
   ```
4. Launch dashboard:
   ```bash
   streamlit run src/dashboard/app.py
   ```

## References
- [Yelp Open Dataset](https://www.yelp.com/dataset)
- [Google Cloud Dataflow](https://cloud.google.com/dataflow)
- [BigQuery](https://cloud.google.com/bigquery)
- [Streamlit](https://streamlit.io/)