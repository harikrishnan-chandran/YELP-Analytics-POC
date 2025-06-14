#!/usr/bin/env python3
"""
Unit tests for the Yelp Analytics Spark Pipeline.

This module tests the main pipeline functions:
- read_bronze_data
- silver_layer
- gold_layer
"""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType
from src.spark.yelp_analytics import read_bronze_data, silver_layer, gold_layer
from datetime import datetime

@pytest.fixture(scope="session")
def spark():
    """Create a Spark session for testing."""
    return (SparkSession.builder
            .appName("Yelp Analytics Test")
            .master("local[*]")
            .getOrCreate())

@pytest.fixture(scope="session")
def sample_data(spark):
    """Create sample data for testing."""
    business_schema = StructType([
        StructField("business_id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("address", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("postal_code", StringType(), True),
        StructField("latitude", FloatType(), True),
        StructField("longitude", FloatType(), True),
        StructField("stars", FloatType(), True),
        StructField("review_count", IntegerType(), True),
        StructField("is_open", IntegerType(), True),
        StructField("categories", StringType(), True)
    ])

    review_schema = StructType([
        StructField("review_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("business_id", StringType(), True),
        StructField("stars", IntegerType(), True),
        StructField("date", TimestampType(), True),
        StructField("text", StringType(), True),
        StructField("useful", IntegerType(), True),
        StructField("funny", IntegerType(), True),
        StructField("cool", IntegerType(), True)
    ])

    user_schema = StructType([
        StructField("user_id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("review_count", IntegerType(), True),
        StructField("yelping_since", TimestampType(), True),
        StructField("useful", IntegerType(), True),
        StructField("funny", IntegerType(), True),
        StructField("cool", IntegerType(), True),
        StructField("fans", IntegerType(), True),
        StructField("average_stars", FloatType(), True)
    ])

    business_data = [
        ("b1", "Restaurant A", "123 Main St", "Phoenix", "AZ", "85001", 33.45, -112.07, 4.5, 100, 1, "Restaurants|Food"),
        ("b2", "Restaurant B", "456 Oak St", "Phoenix", "AZ", "85002", 33.46, -112.08, 3.5, 50, 1, "Restaurants|Bars")
    ]

    review_data = [
        ("r1", "u1", "b1", 5, datetime(2023, 1, 1, 12, 0, 0), "Great food!", 10, 5, 5),
        ("r2", "u2", "b1", 4, datetime(2023, 1, 2, 12, 0, 0), "Good service", 8, 3, 4),
        ("r3", "u1", "b2", 3, datetime(2023, 1, 3, 12, 0, 0), "Average", 5, 2, 3)
    ]

    user_data = [
        ("u1", "User A", 50, datetime(2020, 1, 1, 0, 0, 0), 100, 50, 50, 10, 4.5),
        ("u2", "User B", 30, datetime(2020, 2, 1, 0, 0, 0), 80, 40, 40, 5, 4.0)
    ]

    business_df = spark.createDataFrame(business_data, business_schema)
    review_df = spark.createDataFrame(review_data, review_schema)
    user_df = spark.createDataFrame(user_data, user_schema)

    return business_df, review_df, user_df

def test_read_bronze_data(spark, tmp_path):
    """Test reading bronze data from GCS."""
    # Create temporary JSON files
    business_path = tmp_path / "yelp_academic_dataset_business.json"
    review_path = tmp_path / "yelp_academic_dataset_review.json"
    user_path = tmp_path / "yelp_academic_dataset_user.json"

    business_path.write_text('{"business_id": "b1", "name": "Test Business"}')
    review_path.write_text('{"review_id": "r1", "business_id": "b1", "stars": 5}')
    user_path.write_text('{"user_id": "u1", "name": "Test User"}')

    # Read data
    business_df, review_df, user_df = read_bronze_data(spark, str(tmp_path))

    # Validate
    assert business_df.count() == 1
    assert review_df.count() == 1
    assert user_df.count() == 1

def test_silver_layer(spark, sample_data):
    """Test silver layer processing."""
    business_df, review_df, user_df = sample_data
    silver_df = silver_layer(business_df, review_df, user_df)

    # Validate
    assert silver_df.count() == 3  # 3 reviews
    assert "business_stars" in silver_df.columns
    assert "review_stars" in silver_df.columns
    assert "categories" in silver_df.columns

def test_gold_layer(spark, sample_data):
    """Test gold layer processing."""
    business_df, review_df, user_df = sample_data
    silver_df = silver_layer(business_df, review_df, user_df)
    business_metrics, review_trends = gold_layer(silver_df)

    # Validate business metrics
    assert business_metrics.count() == 1  # 1 state (AZ)
    assert business_metrics.first()["state"] == "AZ"
    assert business_metrics.first()["total_reviews"] == 3

    # Validate review trends
    assert review_trends.count() == 3  # 3 months
    assert review_trends.first()["total_reviews"] == 1

def test_edge_cases(spark):
    """Test edge cases."""
    # Empty dataframes with full expected schema
    business_schema = StructType([
        StructField("business_id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("address", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("postal_code", StringType(), True),
        StructField("latitude", FloatType(), True),
        StructField("longitude", FloatType(), True),
        StructField("stars", FloatType(), True),
        StructField("review_count", IntegerType(), True),
        StructField("is_open", IntegerType(), True),
        StructField("categories", StringType(), True)
    ])
    review_schema = StructType([
        StructField("review_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("business_id", StringType(), True),
        StructField("stars", IntegerType(), True),
        StructField("date", TimestampType(), True),
        StructField("text", StringType(), True),
        StructField("useful", IntegerType(), True),
        StructField("funny", IntegerType(), True),
        StructField("cool", IntegerType(), True)
    ])
    user_schema = StructType([
        StructField("user_id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("review_count", IntegerType(), True),
        StructField("yelping_since", TimestampType(), True),
        StructField("useful", IntegerType(), True),
        StructField("funny", IntegerType(), True),
        StructField("cool", IntegerType(), True),
        StructField("fans", IntegerType(), True),
        StructField("average_stars", FloatType(), True)
    ])
    empty_business = spark.createDataFrame([], business_schema)
    empty_review = spark.createDataFrame([], review_schema)
    empty_user = spark.createDataFrame([], user_schema)

    silver_df = silver_layer(empty_business, empty_review, empty_user)
    assert silver_df.count() == 0

    business_metrics, review_trends = gold_layer(silver_df)
    assert business_metrics.count() == 0
    assert review_trends.count() == 0

def test_failure_cases(spark):
    """Test failure cases."""
    # Invalid schema
    invalid_business = spark.createDataFrame([("b1",)], ["business_id"])
    invalid_review = spark.createDataFrame([("r1",)], ["review_id"])
    invalid_user = spark.createDataFrame([("u1",)], ["user_id"])

    with pytest.raises(Exception):
        silver_layer(invalid_business, invalid_review, invalid_user) 