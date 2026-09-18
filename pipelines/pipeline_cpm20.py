import requests
import pandas as pd
import boto3
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = (
    "https://ws.cso.ie/public/api.restful/"
    "PxStat.Data.Cube_API.ReadDataset/"
    "CPM20/CSV/1.0/en"
)

BUCKET_NAME = "irish-financial-intelligence-gpm"

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Local directories
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Local files
RAW_FILE = RAW_DIR / "cpm20_raw.csv"
PROCESSED_FILE = PROCESSED_DIR / "inflation.csv"

# S3 locations
RAW_S3_KEY = "raw/cpm20/cpm20_raw.csv"
PROCESSED_S3_KEY = "processed/inflation/inflation.csv"


# Make sure directories exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# STEP 1 - DOWNLOAD CPM20 FROM CSO
# ============================================================

print("=" * 60)
print("STEP 1 - DOWNLOADING CPM20 FROM CSO")
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
# STEP 2 - LOAD RAW DATA
# ============================================================

print("\n" + "=" * 60)
print("STEP 2 - LOADING RAW DATA")
print("=" * 60)

df = pd.read_csv(
    RAW_FILE,
    encoding="utf-8-sig"
)

print("Raw shape:", df.shape)
print("Raw columns:", df.columns.tolist())


# ============================================================
# STEP 3 - CLEAN COLUMN NAMES
# ============================================================

print("\n" + "=" * 60)
print("STEP 3 - CLEANING COLUMN NAMES")
print("=" * 60)

df.columns = df.columns.str.replace(
    'ï»¿"',
    '',
    regex=False
)

df.columns = df.columns.str.replace(
    '"',
    '',
    regex=False
)

print("Clean columns:", df.columns.tolist())


# ============================================================
# STEP 4 - SELECT HEADLINE INFLATION SERIES
# ============================================================

print("\n" + "=" * 60)
print("STEP 4 - SELECTING HEADLINE INFLATION SERIES")
print("=" * 60)

cpi = df[
    (df["STATISTIC"] == "CPM20C08") &
    (df["Commodity Group"] == "All Items")
].copy()

print("Selected shape:", cpi.shape)

print(
    "Missing VALUE observations:",
    cpi["VALUE"].isna().sum()
)


# ============================================================
# STEP 5 - CREATE CLEAN INFLATION DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 5 - CREATING CLEAN INFLATION DATASET")
print("=" * 60)

inflation = cpi[
    ["Month", "VALUE"]
].copy()

inflation = inflation.rename(
    columns={
        "Month": "date",
        "VALUE": "inflation_rate"
    }
)

inflation["date"] = pd.to_datetime(
    inflation["date"],
    format="%Y %B"
)

inflation = inflation.sort_values(
    "date"
).reset_index(drop=True)

print(
    "Date range:",
    inflation["date"].min(),
    "to",
    inflation["date"].max()
)


# ============================================================
# STEP 6 - FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 6 - FINAL VALIDATION")
print("=" * 60)

print(
    "Rows:",
    len(inflation)
)

print(
    "Duplicate dates:",
    inflation["date"].duplicated().sum()
)

print("Missing values:")
print(
    inflation.isna().sum()
)

print(
    "Inflation range:",
    inflation["inflation_rate"].min(),
    "to",
    inflation["inflation_rate"].max()
)

if inflation["date"].duplicated().any():
    raise ValueError("Duplicate dates found.")

if inflation["inflation_rate"].isna().any():
    raise ValueError("Missing inflation values found.")


# ============================================================
# STEP 7 - SAVE PROCESSED DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 7 - SAVING PROCESSED DATASET")
print("=" * 60)

inflation.to_csv(
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
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("CPM20 PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)