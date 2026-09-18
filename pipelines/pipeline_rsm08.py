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
    "RSM08/CSV/1.0/en"
)

BUCKET_NAME = "irish-financial-intelligence-gpm"

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Local directories
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Local files
RAW_FILE = RAW_DIR / "rsm08_raw.csv"
MONTHLY_FILE = PROCESSED_DIR / "rsm08_retail_monthly.csv"
VALIDATED_FILE = PROCESSED_DIR / "rsm08_retail_validated.csv"

# S3 locations
RAW_S3_KEY = "raw/rsm8/rsm08_raw.csv"
MONTHLY_S3_KEY = "processed/retail/rsm08_retail_monthly.csv"
VALIDATED_S3_KEY = "processed/retail/rsm08_retail_validated.csv"


# Make sure directories exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# STEP 1 - DOWNLOAD RSM08 FROM CSO
# ============================================================

print("=" * 60)
print("STEP 1 - DOWNLOADING RSM08 FROM CSO")
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
# STEP 4 - SELECT MAIN RETAIL SERIES
# ============================================================

print("\n" + "=" * 60)
print("STEP 4 - SELECTING MAIN RETAIL SERIES")
print("=" * 60)

main_retail = df[
    (df["STATISTIC"] == "RSM08C04") &
    (df["NACE Group"] == "All retail businesses") &
    (df["UNIT"] == "Base Year 2021=100")
].copy()

print("Selected shape:", main_retail.shape)

print(
    "Missing VALUE observations:",
    main_retail["VALUE"].isna().sum()
)


# ============================================================
# STEP 5 - CREATE CLEAN MONTHLY DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 5 - CREATING CLEAN MONTHLY DATASET")
print("=" * 60)

retail_clean = main_retail[
    ["Month", "VALUE"]
].copy()

retail_clean = retail_clean.reset_index(
    drop=True
)

retail_clean = retail_clean.rename(
    columns={
        "Month": "date",
        "VALUE": "retail_sales_index"
    }
)

retail_clean["date"] = pd.to_datetime(
    retail_clean["date"],
    format="%Y %B"
)

retail_clean = retail_clean.sort_values(
    "date"
).reset_index(drop=True)

print(
    "Date range:",
    retail_clean["date"].min(),
    "to",
    retail_clean["date"].max()
)


# ============================================================
# STEP 6 - SAVE MONTHLY DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 6 - SAVING MONTHLY DATASET")
print("=" * 60)

retail_monthly = retail_clean[
    ["date", "retail_sales_index"]
].copy()

retail_monthly.to_csv(
    MONTHLY_FILE,
    index=False
)

print(
    "Monthly dataset saved to:",
    MONTHLY_FILE
)


# ============================================================
# STEP 7 - CALCULATE MONTH-ON-MONTH GROWTH
# ============================================================

print("\n" + "=" * 60)
print("STEP 7 - CALCULATING MoM GROWTH")
print("=" * 60)

retail_validated = retail_clean.copy()

retail_validated["mom_growth_pct"] = (
    retail_validated["retail_sales_index"]
    .pct_change()
    * 100
)


# ============================================================
# STEP 8 - CALCULATE YEAR-ON-YEAR GROWTH
# ============================================================

print("\n" + "=" * 60)
print("STEP 8 - CALCULATING YoY GROWTH")
print("=" * 60)

retail_validated["yoy_growth_pct"] = (
    retail_validated["retail_sales_index"]
    .pct_change(periods=12)
    * 100
)

retail_validated = retail_validated[
    [
        "date",
        "retail_sales_index",
        "mom_growth_pct",
        "yoy_growth_pct"
    ]
]

print("\nValidated preview:")
print(
    retail_validated.head(15)
)


# ============================================================
# STEP 9 - FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 9 - FINAL VALIDATION")
print("=" * 60)

print(
    "Monthly shape:",
    retail_monthly.shape
)

print(
    "Monthly duplicate dates:",
    retail_monthly["date"].duplicated().sum()
)

print("Monthly missing values:")
print(
    retail_monthly.isna().sum()
)

print(
    "\nValidated shape:",
    retail_validated.shape
)

print(
    "Validated duplicate dates:",
    retail_validated["date"].duplicated().sum()
)

print("Validated missing values:")
print(
    retail_validated.isna().sum()
)


# ============================================================
# STEP 10 - SAVE VALIDATED DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 10 - SAVING VALIDATED DATASET")
print("=" * 60)

retail_validated.to_csv(
    VALIDATED_FILE,
    index=False
)

print(
    "Validated dataset saved to:",
    VALIDATED_FILE
)


# ============================================================
# STEP 11 - CONNECT TO AWS S3
# ============================================================

print("\n" + "=" * 60)
print("STEP 11 - CONNECTING TO AWS S3")
print("=" * 60)

s3 = boto3.client("s3")

print("Connected to S3 successfully.")


# ============================================================
# STEP 12 - UPLOAD RAW DATA
# ============================================================

print("\n" + "=" * 60)
print("STEP 12 - UPLOADING RAW DATA")
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
# STEP 13 - UPLOAD MONTHLY DATA
# ============================================================

print("\n" + "=" * 60)
print("STEP 13 - UPLOADING MONTHLY DATA")
print("=" * 60)

s3.upload_file(
    str(MONTHLY_FILE),
    BUCKET_NAME,
    MONTHLY_S3_KEY
)

print(
    f"s3://{BUCKET_NAME}/{MONTHLY_S3_KEY}"
)


# ============================================================
# STEP 14 - UPLOAD VALIDATED DATA
# ============================================================

print("\n" + "=" * 60)
print("STEP 14 - UPLOADING VALIDATED DATA")
print("=" * 60)

s3.upload_file(
    str(VALIDATED_FILE),
    BUCKET_NAME,
    VALIDATED_S3_KEY
)

print(
    f"s3://{BUCKET_NAME}/{VALIDATED_S3_KEY}"
)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("RSM08 PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)