import boto3
import os

BUCKET_NAME = "irish-financial-intelligence-gpm"

LOCAL_RAW_FILE = "Data/Raw/rsm08_raw.csv"
LOCAL_PROCESSED_FILE = "Data/processed/rsm08_retail_validated.csv"

RAW_S3_KEY = "raw/rsm8/rsm08_raw.csv"
PROCESSED_S3_KEY = "processed/retail/rsm08_retail_validated.csv"

s3 = boto3.client("s3")

# Upload raw RSM8 data
s3.upload_file(
    LOCAL_RAW_FILE,
    BUCKET_NAME,
    RAW_S3_KEY
)

print("Raw RSM8 uploaded successfully")

# Upload processed retail data
s3.upload_file(
    LOCAL_PROCESSED_FILE,
    BUCKET_NAME,
    PROCESSED_S3_KEY
)

print("Processed retail data uploaded successfully")