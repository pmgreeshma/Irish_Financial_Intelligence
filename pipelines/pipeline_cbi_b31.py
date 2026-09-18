import requests
import pandas as pd
import boto3
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = (
    "https://opendata.centralbank.ie/api/3/action/"
    "datastore_search?"
    "resource_id=fb07a41b-15f7-4697-a7f7-ce8209d794e5"
)

BUCKET_NAME = "irish-financial-intelligence-gpm"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

RAW_FILE = RAW_DIR / "cbi_b31_raw.json"
PROCESSED_FILE = PROCESSED_DIR / "mortgage_rates.csv"

RAW_S3_KEY = "raw/cbi_b31/cbi_b31_raw.json"
PROCESSED_S3_KEY = (
    "processed/mortgage_rates/mortgage_rates.csv"
)


# ============================================================
# CREATE DIRECTORIES
# ============================================================

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# STEP 1 - DOWNLOAD B.3.1 FROM CENTRAL BANK OF IRELAND
# ============================================================

print("=" * 60)
print("STEP 1 - DOWNLOADING CBI B.3.1")
print("=" * 60)

response = requests.get(
    API_URL,
    timeout=60
)

print("Status code:", response.status_code)

response.raise_for_status()

RAW_FILE.write_text(
    response.text,
    encoding="utf-8"
)

print("Raw data saved to:", RAW_FILE)


# ============================================================
# STEP 2 - LOAD RAW JSON
# ============================================================

print("\n" + "=" * 60)
print("STEP 2 - LOADING RAW DATA")
print("=" * 60)

data = response.json()

records = data["result"]["records"]

print("Number of records:", len(records))


# ============================================================
# STEP 3 - CREATE DATAFRAME
# ============================================================

print("\n" + "=" * 60)
print("STEP 3 - CREATING DATAFRAME")
print("=" * 60)

mortgage_rates = pd.DataFrame(records)

print("Raw shape:", mortgage_rates.shape)


# ============================================================
# STEP 4 - SELECT PDH MORTGAGE RATE SERIES
# ============================================================

print("\n" + "=" * 60)
print("STEP 4 - SELECTING PDH MORTGAGE RATE SERIES")
print("=" * 60)

rate_column = (
    "principal_dwelling_houses__"
    "floating_rate__standard_or_ltv_va"
)

mortgage_rates = mortgage_rates[
    [
        "Reporting date",
        rate_column
    ]
].copy()

print("Selected shape:", mortgage_rates.shape)


# ============================================================
# STEP 5 - CREATE CLEAN MORTGAGE RATE DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 5 - CREATING CLEAN MORTGAGE RATE DATASET")
print("=" * 60)

mortgage_rates = mortgage_rates.rename(
    columns={
        "Reporting date": "date",
        rate_column: "mortgage_rate"
    }
)

mortgage_rates["date"] = pd.to_datetime(
    mortgage_rates["date"]
)

mortgage_rates["mortgage_rate"] = pd.to_numeric(
    mortgage_rates["mortgage_rate"],
    errors="coerce"
)

mortgage_rates = (
    mortgage_rates
    .sort_values("date")
    .reset_index(drop=True)
)

print(
    "Date range:",
    mortgage_rates["date"].min(),
    "to",
    mortgage_rates["date"].max()
)


# ============================================================
# STEP 6 - FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 6 - FINAL VALIDATION")
print("=" * 60)

print("Rows:", len(mortgage_rates))

print(
    "Duplicate dates:",
    mortgage_rates["date"].duplicated().sum()
)

print("Missing values:")
print(mortgage_rates.isna().sum())

print(
    "Mortgage rate range:",
    mortgage_rates["mortgage_rate"].min(),
    "to",
    mortgage_rates["mortgage_rate"].max()
)


if mortgage_rates["date"].duplicated().any():
    raise ValueError("Duplicate dates found.")

if mortgage_rates["mortgage_rate"].isna().any():
    raise ValueError(
        "Missing mortgage rate values found."
    )


# ============================================================
# STEP 7 - SAVE PROCESSED DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 7 - SAVING PROCESSED DATASET")
print("=" * 60)

mortgage_rates.to_csv(
    PROCESSED_FILE,
    index=False
)

print(
    "Processed dataset saved to:",
    PROCESSED_FILE
)


# ============================================================
# STEP 8 - CONNECT TO AWS S3
# ============================================================

print("\n" + "=" * 60)
print("STEP 8 - CONNECTING TO AWS S3")
print("=" * 60)

s3 = boto3.client("s3")

print("Connected to S3 successfully.")


# ============================================================
# STEP 9 - UPLOAD RAW DATA
# ============================================================

print("\n" + "=" * 60)
print("STEP 9 - UPLOADING RAW DATA")
print("=" * 60)

s3.upload_file(
    str(RAW_FILE),
    BUCKET_NAME,
    RAW_S3_KEY
)

print(
    f"s3://{BUCKET_NAME}/{RAW_S3_KEY}"
)


# ============================================================
# STEP 10 - UPLOAD PROCESSED DATA
# ============================================================

print("\n" + "=" * 60)
print("STEP 10 - UPLOADING PROCESSED DATA")
print("=" * 60)

s3.upload_file(
    str(PROCESSED_FILE),
    BUCKET_NAME,
    PROCESSED_S3_KEY
)

print(
    f"s3://{BUCKET_NAME}/{PROCESSED_S3_KEY}"
)


# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("CBI B.3.1 PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)