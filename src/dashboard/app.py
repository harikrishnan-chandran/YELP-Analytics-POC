#!/usr/bin/env python3
"""
Yelp Analytics Dashboard

This Streamlit app visualizes Yelp analytics data from BigQuery:
- Business metrics by state
- Review trends over time
"""

from dotenv import load_dotenv
import os
from pathlib import Path

# Get the project root directory (2 levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / '.env')  # Load environment variables from .env

# Set the service account key path
key_path = str(PROJECT_ROOT / 'yelp-dataflow-sa-key.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

# Debug information
print(f"Project root: {PROJECT_ROOT}")
print(f"Key file path: {key_path}")
print(f"Key file exists: {os.path.exists(key_path)}")
print(f"GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")

import streamlit as st
import pandas as pd
from google.cloud import bigquery
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Yelp Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize BigQuery client
try:
    client = bigquery.Client()
    print("Successfully initialized BigQuery client")
except Exception as e:
    print(f"Error initializing BigQuery client: {str(e)}")
    raise

def load_business_metrics():
    """Load business metrics from BigQuery."""
    query = """
    SELECT 
        state,
        total_reviews,
        avg_rating,
        avg_business_reviews
    FROM `pivotal-rhino-462807-c1.yelp_analytics.business_metrics`
    ORDER BY total_reviews DESC
    """
    return client.query(query).to_dataframe()

def load_review_trends():
    """Load review trends from BigQuery."""
    query = """
    SELECT 
        year,
        month,
        total_reviews,
        avg_rating
    FROM `pivotal-rhino-462807-c1.yelp_analytics.review_trends`
    ORDER BY year, month
    """
    return client.query(query).to_dataframe()

def main():
    st.title("📊 Yelp Analytics Dashboard")
    
    # Load data
    with st.spinner("Loading data from BigQuery..."):
        business_metrics = load_business_metrics()
        review_trends = load_review_trends()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Business Metrics Section
    st.header("Business Metrics by State")
    
    # Top 10 states by total reviews
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 States by Total Reviews")
        fig = px.bar(
            business_metrics.head(10),
            x="state",
            y="total_reviews",
            title="Total Reviews by State (Top 10)",
            labels={"state": "State", "total_reviews": "Total Reviews"},
            color="total_reviews",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Average Rating by State")
        fig = px.bar(
            business_metrics.head(10),
            x="state",
            y="avg_rating",
            title="Average Rating by State (Top 10)",
            labels={"state": "State", "avg_rating": "Average Rating"},
            color="avg_rating",
            color_continuous_scale="RdYlGn"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Review Trends Section
    st.header("Review Trends Over Time")
    
    # Convert year and month to datetime for better plotting
    review_trends['date'] = pd.to_datetime(
        review_trends['year'].astype(str) + '-' + 
        review_trends['month'].astype(str) + '-01'
    )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Monthly Review Volume")
        fig = px.line(
            review_trends,
            x="date",
            y="total_reviews",
            title="Monthly Review Volume",
            labels={"date": "Date", "total_reviews": "Total Reviews"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        st.subheader("Average Rating Trend")
        fig = px.line(
            review_trends,
            x="date",
            y="avg_rating",
            title="Average Rating Trend",
            labels={"date": "Date", "avg_rating": "Average Rating"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Raw Data Tables
    st.header("Raw Data")
    
    tab1, tab2 = st.tabs(["Business Metrics", "Review Trends"])
    
    with tab1:
        st.dataframe(business_metrics)
    
    with tab2:
        st.dataframe(review_trends)

if __name__ == "__main__":
    main() 