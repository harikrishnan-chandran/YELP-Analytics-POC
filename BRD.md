# Yelp Analytics POC – Business Requirements Document (BRD)

| Field | Details |
|-------|---------|
| **Project Name** | Yelp Analytics POC |
| **Customer Name** | Internal – Business Intelligence Team |
| **Date** | 10 June 2025 |
| **Document Version** | 1.1 |

---

## Table of Contents
1. [Business Objective](#business-objective)  
   1.1 [Project Objective](#project-objective)  
   1.2 [Project Scope](#project-scope)  
2. [Business Requirements](#business-requirements)  
   2.1 [Functional Requirements](#functional-requirements)  
   2.2 [Non-functional Requirements](#non-functional-requirements)  
3. [Risks and Assumptions](#risks-and-assumptions)  
   3.1 [Risks](#risks)  
   3.2 [Assumptions](#assumptions)  
4. [Change Request Log](#change-request-log)  
5. [Writeback Functionality](#writeback-functionality)  
6. [Business Requirements Traceability Matrix](#brtm)  
7. [Success Metrics](#success-metrics)  
   7.1 [Acceptance Criteria](#acceptance-criteria)  
   7.2 [Performance Indicators](#performance-indicators)  
8. [Visuals (for reference)](#visuals)

---

## 1. Business Objective<a name="business-objective"></a>

### 1.1 Project Objective<a name="project-objective"></a>
The purpose of this proof-of-concept is to **demonstrate the value of Yelp review data** by:
- Building a **cost-efficient, end-to-end batch pipeline** on Google Cloud Platform (GCS → Dataproc/Spark → BigQuery).
- Surfacing **actionable insights** for Ratings, Sentiment, Geographic, and Trend analysis.
- Producing a **simple Streamlit dashboard** for internal stakeholders.
- Validating feasibility for a future production-grade solution.

### 1.2 Project Scope<a name="project-scope"></a>

| In Scope | Out of Scope |
|----------|--------------|
| Batch ingestion of Yelp Open Dataset | Real-time streaming |
| Spark ETL (Bronze → Gold) on Dataproc | Complex ML / predictive modelling |
| Storage in BigQuery (star schema) | External customer-facing app |
| Streamlit visualizations | Writeback to Yelp or internal systems |
| Basic sentiment tagging (rule-based) | Advanced NLP or topic modelling |

---

## 2. Business Requirements<a name="business-requirements"></a>

### 2.1 Functional Requirements<a name="functional-requirements"></a>
✔ Ingest Yelp business & review JSON from GCS  
✔ Build star-schema (Fact Reviews, Dim Business, Dim User, Dim Date)  
✔ Compute rating distribution, sentiment counts, reviews-per-month  
✔ Write aggregated outputs to BigQuery tables  
✔ Serve an interactive Streamlit dashboard (rating bar, sentiment pie, trend line)  
✔ Apply simple rule-based sentiment classification

### 2.2 Non-functional Requirements<a name="non-functional-requirements"></a>
✔ Pipeline runtime **< 30 min** for ≤ 500 k reviews  
✔ Query latency in dashboard **< 5 s**  
✔ Secure access (IAM roles: BigQuery Data Editor, Storage Object Viewer)  
✔ Modular, documented PySpark codebase  
✔ Use only low-cost GCP services; delete Dataproc clusters when idle

---

## 3. Risks and Assumptions<a name="risks-and-assumptions"></a>

### 3.1 Risks<a name="risks"></a>
| Risk | Potential Impact | Mitigation |
|------|-----------------|------------|
| **Large dataset** | Slow jobs, higher cost | Use dataset subset; optimize Spark pipeline; tune Dataproc resources |
| **Data quality** | Misleading insights | Clean data; exclude filtered/fake reviews |
| **Scope creep** | Miss deadline | Lock scope; log changes (Section 4) |
| **API limits** | Incomplete data | Fall back to static Open Dataset |

### 3.2 Assumptions<a name="assumptions"></a>
- Yelp data is publicly accessible and license-compliant  
- GCP project, billing, and IAM are configured  
- Stakeholders (Marketing, Ops, Strategy) will review outputs promptly  
- POC is for internal analysis only

---

## 4. Change Request Log<a name="change-request-log"></a>
| Date | Change | Reason | Impact |
|------|--------|--------|--------|
| 10 June 2025 | Initial version | Baseline | None |
| 11 June 2025 | Migrated from Dataflow to Dataproc | Cost optimization | Improved cost efficiency |

---

## 5. Writeback Functionality<a name="writeback-functionality"></a>
This POC is **read-only**. Users cannot edit or push data back to source systems. Any future writeback (e.g., tagging reviews) would require additional design for authentication, audit, and concurrency control.

---

## 6. Business Requirements Traceability Matrix (BRTM)<a name="brtm"></a>

| ID | Requirement | Dependency | Priority | Status |
|----|-------------|------------|----------|--------|
| BR-01 | Ingest Yelp dataset to GCS | – | High | ✅ |
| BR-02 | Transform & enrich via Spark | BR-01 | High | ✅ |
| BR-03 | Load results to BigQuery | BR-02 | High | ✅ |
| BR-04 | Build Streamlit dashboard | BR-03 | High | ✅ |
| BR-05 | Sentiment classification | BR-02 | Medium | ✅ |

---

## 7. Success Metrics<a name="success-metrics"></a>

### 7.1 Acceptance Criteria<a name="acceptance-criteria"></a>
✔ End-to-end pipeline runs without errors  
✔ BigQuery tables created and populated  
✔ Streamlit app displays required charts & filters  
✔ Stakeholders can access and use dashboard

### 7.2 Performance Indicators<a name="performance-indicators"></a>
✔ ETL SLA < 30 min  
✔ Dashboard response < 5 s  
✔ 3+ stakeholder teams actively use dashboard  
✔ ≥ 90 % classifier accuracy on sample set

---

## 8. Visuals (for reference)<a name="visuals"></a>

1. **Rating Distribution Bar Chart** – shows count of reviews for each star (1–5)  
2. **Sentiment Analysis Pie Chart** – shows distribution of positive/negative/neutral reviews  
3. **Geographic Heat Map** – shows review density by location  
4. **Time Series Chart** – shows review trends over time  

---

**End of Document**
