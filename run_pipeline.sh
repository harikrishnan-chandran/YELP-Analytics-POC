#!/bin/bash

# Exit on error
set -e

# Load environment variables
source .env

# Create temporary GCS bucket
BUCKET_NAME="yelp-analytics-poc-temp"
gsutil mb -l us-central1 gs://$BUCKET_NAME || true

# Run the Spark pipeline
echo "Running Spark pipeline..."
python -m src.spark.yelp_analytics

# Clean up temporary bucket
gsutil rm -r gs://$BUCKET_NAME

echo "Pipeline completed successfully!" 