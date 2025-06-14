# Yelp Analytics POC

A proof-of-concept project for analyzing Yelp data using Google Cloud Platform services.

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
     - Dataflow

3. **Environment Variables**
   Create a `.env` file with:
   ```
   PROJECT_ID=your-project-id
   DATASET_ID=yelp_analytics
   BUCKET_NAME=your-bucket-name
   ```

## Running the Pipeline

1. **Data Processing**
   ```bash
   ./run_pipeline.sh
   ```

2. **Dashboard**
   ```bash
   cd src/dashboard
   streamlit run app.py
   ```

## Project Status

- ✅ Bronze Layer: Raw data ingestion
- ✅ Silver Layer: Data cleaning and transformation
- ✅ Gold Layer: Analytics-ready aggregations
- ✅ Dashboard: Basic visualizations

## Cost Management

To avoid unnecessary costs:
1. Delete temporary GCS buckets
2. Delete Dataproc clusters when not in use
3. Monitor BigQuery usage
4. Use appropriate machine types

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request