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
    "HPM09/CSV/1.0/en"
)

BUCKET_NAME = "irish-financial-intelligence-gpm"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

RAW_FILE = RAW_DIR / "hpm09_raw.csv"
PROCESSED_FILE = PROCESSED_DIR / "property_prices.csv"

RAW_S3_KEY = "raw/hpm09/hpm09_raw.csv"
PROCESSED_S3_KEY = "processed/property_prices/property_prices.csv"


# ============================================================
# CREATE DIRECTORIES
# ============================================================

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# STEP 1 - DOWNLOAD HPM09 FROM CSO
# ============================================================

print("=" * 60)
print("STEP 1 - DOWNLOADING HPM09 FROM CSO")
print("=" * 60)

response = requests.get(API_URL, timeout=60)

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
# STEP 4 - SELECT PROPERTY PRICE INDEX
# ============================================================

print("\n" + "=" * 60)
print("STEP 4 - SELECTING NATIONAL PROPERTY PRICE INDEX")
print("=" * 60)

property_prices = df[
    (df["STATISTIC"] == "HPM09C01") &
    (
        df["Type of Residential Property"]
        == "National - all residential properties"
    )
].copy()

print("Selected shape:", property_prices.shape)

print(
    "Missing VALUE observations:",
    property_prices["VALUE"].isna().sum()
)


# ============================================================
# STEP 5 - CREATE CLEAN PROPERTY PRICE DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 5 - CREATING CLEAN PROPERTY PRICE DATASET")
print("=" * 60)

property_prices = property_prices[
    ["Month", "VALUE"]
].copy()

property_prices = property_prices.rename(
    columns={
        "Month": "date",
        "VALUE": "property_price_index"
    }
)

property_prices["date"] = pd.to_datetime(
    property_prices["date"],
    format="%Y %B"
)

property_prices = (
    property_prices
    .sort_values("date")
    .reset_index(drop=True)
)

print(
    "Date range:",
    property_prices["date"].min(),
    "to",
    property_prices["date"].max()
)


# ============================================================
# STEP 6 - FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 6 - FINAL VALIDATION")
print("=" * 60)

print("Rows:", len(property_prices))

print(
    "Duplicate dates:",
    property_prices["date"].duplicated().sum()
)

print("Missing values:")
print(property_prices.isna().sum())

print(
    "Property price index range:",
    property_prices["property_price_index"].min(),
    "to",
    property_prices["property_price_index"].max()
)


if property_prices["date"].duplicated().any():
    raise ValueError("Duplicate dates found.")

if property_prices["property_price_index"].isna().any():
    raise ValueError(
        "Missing property price index values found."
    )


# ============================================================
# STEP 7 - SAVE PROCESSED DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 7 - SAVING PROCESSED DATASET")
print("=" * 60)

property_prices.to_csv(
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
print("HPM09 PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)