# Project Objective: Yelp Analytics POC

## Goals
The purpose of this proof-of-concept is to **demonstrate the value of Yelp review data** by:
- Building a **cost-efficient, end-to-end batch pipeline** on Google Cloud Platform (GCS → Dataproc/Spark → BigQuery).
- Surfacing **actionable insights** for Ratings, Sentiment, Geographic, and Trend analysis.
- Producing a **simple Streamlit dashboard** for internal stakeholders.
- Validating feasibility for a future production-grade solution.

## Architecture
- **Medallion Pattern**: Bronze (raw) → Silver (clean/enriched) → Gold (aggregated/analytics-ready)
- **Tech Stack**: GCS (storage), Dataproc (Spark ETL), BigQuery (star schema), Cloud Composer (Airflow orchestration), Streamlit (dashboard)
- **Data Flow**: Yelp Open Dataset/API → GCS (Bronze) → Dataproc/Spark (Silver/Gold) → BigQuery → Streamlit
- **Star Schema**: Fact Reviews, Dim Business, Dim User, Dim Date

## Style & Conventions
- **Language**: Python 3.10+
- **Code Style**: PEP8, type hints, formatted with `black`
- **Validation**: `pydantic` for data models
- **Testing**: Pytest, with tests in `/tests` mirroring app structure
- **Documentation**: Google-style docstrings, inline comments for non-obvious logic
- **Modularity**: Code organized by feature/layer, max 500 lines per file

## Constraints
- **Batch only**: No real-time streaming or writeback
- **Pipeline runtime**: < 30 min for ≤ 500k reviews
- **Dashboard latency**: < 5 seconds per query
- **Security**: IAM roles (BigQuery Data Editor, Storage Object Viewer)
- **Cost**: Use only low-cost GCP services; delete Dataproc clusters when idle
- **Scope**: No advanced ML, external apps, or production writeback

---

For further details, see `BRD.md`, `PROJECT_DESIGN.md`, and `README.md`. 