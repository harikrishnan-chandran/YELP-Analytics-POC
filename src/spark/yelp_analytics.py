#!/usr/bin/env python3
"""
Yelp Analytics Spark Pipeline

This script processes the Yelp dataset using Apache Spark on Dataproc, following the Medallion Architecture:
- Bronze: Raw data ingestion from GCS
- Silver: Clean, enrich, and join data
- Gold: Aggregate and prepare analytics-ready data for BigQuery
"""

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, desc, year, month, regexp_replace, lower, split, explode

def create_spark_session():
    """Create and configure Spark session."""
    return (SparkSession.builder
            .appName("Yelp Analytics Pipeline")
            .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.0")
            .config("spark.hadoop.fs.gs.temp.dir", "yelp-analytics-poc-data/temp")
            .config("spark.sql.warehouse.dir", "yelp-analytics-poc-data/warehouse")
            .config("spark.bigquery.temporaryGcsBucket", "yelp-analytics-poc-data/temp")
            .getOrCreate())

def read_bronze_data(spark, input_path):
    """Read raw Yelp data from GCS (Bronze layer)."""
    business_df = spark.read.json(f"{input_path}/yelp_academic_dataset_business.json")
    review_df = spark.read.json(f"{input_path}/yelp_academic_dataset_review.json")
    user_df = spark.read.json(f"{input_path}/yelp_academic_dataset_user.json")
    return business_df, review_df, user_df

def silver_layer(business_df, review_df, user_df):
    """Clean and enrich data (Silver layer)."""
    # Clean business data
    business_clean = business_df.select(
        col("business_id"),
        col("name"),
        col("address"),
        col("city"),
        col("state"),
        col("postal_code"),
        col("latitude"),
        col("longitude"),
        col("stars").alias("business_stars"),
        col("review_count").alias("business_review_count"),
        col("is_open"),
        regexp_replace(lower(col("categories")), "\\|", ",").alias("categories")
    )

    # Clean review data
    review_clean = review_df.select(
        col("review_id"),
        col("user_id"),
        col("business_id"),
        col("stars").alias("review_stars"),
        col("date"),
        col("text"),
        col("useful"),
        col("funny"),
        col("cool")
    )

    # Clean user data
    user_clean = user_df.select(
        col("user_id"),
        col("name"),
        col("review_count"),
        col("yelping_since"),
        col("useful"),
        col("funny"),
        col("cool"),
        col("fans"),
        col("average_stars")
    )

    # Join data
    silver_df = review_clean.join(business_clean, "business_id").join(user_clean, "user_id")
    return silver_df

def gold_layer(silver_df):
    """Aggregate and prepare analytics-ready data (Gold layer)."""
    # Aggregate business metrics
    business_metrics = silver_df.groupBy("state").agg(
        count("*").alias("total_reviews"),
        avg("review_stars").alias("avg_rating"),
        avg("business_review_count").alias("avg_business_reviews")
    ).orderBy(desc("total_reviews"))

    # Aggregate review trends
    review_trends = silver_df.withColumn("year", year("date")).withColumn("month", month("date")).groupBy("year", "month").agg(
        count("*").alias("total_reviews"),
        avg("review_stars").alias("avg_rating")
    ).orderBy("year", "month")

    return business_metrics, review_trends

def main():
    parser = argparse.ArgumentParser(description="Yelp Analytics Spark Pipeline")
    parser.add_argument("--input-bucket", required=True, help="GCS bucket containing input data")
    parser.add_argument("--output-bucket", required=True, help="GCS bucket for output data")
    args = parser.parse_args()

    # Initialize Spark
    spark = create_spark_session()

    try:
        # Read bronze data
        business_df, review_df, user_df = read_bronze_data(spark, args.input_bucket)

        # Process silver layer
        silver_df = silver_layer(business_df, review_df, user_df)

        # Process gold layer
        business_metrics, review_trends = gold_layer(silver_df)

        # Write results to BigQuery
        business_metrics.write.format("bigquery") \
            .option("table", "yelp_analytics.business_metrics") \
            .option("temporaryGcsBucket", "yelp-analytics-poc-data/temp") \
            .mode("overwrite") \
            .save()
            
        review_trends.write.format("bigquery") \
            .option("table", "yelp_analytics.review_trends") \
            .option("temporaryGcsBucket", "yelp-analytics-poc-data/temp") \
            .mode("overwrite") \
            .save()

    finally:
        spark.stop()

if __name__ == "__main__":
    main() 