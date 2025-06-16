# Yelp Analytics POC

A proof-of-concept project for analyzing Yelp data using Google Cloud Platform services. This project demonstrates a cost-efficient data pipeline using Dataproc/Spark and a Streamlit dashboard for visualization.

## Project Structure

```
.
├── src/
│   ├── spark/              # Spark processing jobs
│   │   └── yelp_analytics.py
│   └── dashboard/          # Streamlit dashboard
│       └── app.py
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
├── requirements.txt        # Python dependencies
└── run_pipeline.sh        # Pipeline execution script
```

## Architecture

The project follows a Medallion architecture:
1. **Bronze Layer**: Raw Yelp data in GCS
2. **Silver Layer**: Cleaned and enriched data
3. **Gold Layer**: Analytics-ready aggregations in BigQuery
4. **Visualization**: Streamlit dashboard

## Setup

1. **Environment Setup**
   ```bash
   python -m venv yap-venv
   source yap-venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Google Cloud Setup**
   - Create a service account and download the key
   - Place the key file as `yelp-dataflow-sa-key.json` in the project root
   - Enable required APIs:
     - BigQuery
     - Cloud Storage
     - Dataproc

3. **Environment Variables**
   Create a `.env` file with:
   ```
   PROJECT_ID=pivotal-rhino-462807-c1
   DATASET_ID=yelp_analytics
   BUCKET_NAME=yelp-analytics-poc-data
   ```

## Running the Pipeline

1. **Data Processing**
   ```bash
   ./run_pipeline.sh
   ```
   This will:
   - Process Yelp data using Spark on Dataproc
   - Create BigQuery tables
   - Generate analytics-ready data

2. **Dashboard**
   ```bash
   cd src/dashboard
   streamlit run app.py
   ```
   Features:
   - Rating distribution
   - Sentiment analysis
   - Geographic trends
   - Time-based trends

## Project Status

- ✅ Bronze Layer: Raw data ingestion
- ✅ Silver Layer: Data cleaning and transformation
- ✅ Gold Layer: Analytics-ready aggregations
- ✅ Dashboard: Interactive visualizations

## Cost Management

To avoid unnecessary costs:
1. Delete temporary GCS buckets
2. Delete Dataproc clusters when not in use
3. Monitor BigQuery usage
4. Use appropriate machine types

## Documentation

- `PROJECT_OBJECTIVE.md`: Project goals and constraints
- `PROJECT_DESIGN.md`: Technical architecture and implementation
- `BRD.md`: Business requirements and success metrics
- `TASKS.md`: Development checklist and progress

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request