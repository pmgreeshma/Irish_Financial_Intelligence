import requests
import pandas as pd
import boto3
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = (
    "https://www.centralbank.ie/docs/default-source/"
    "statistics/data-and-analysis/credit-and-banking-statistics/"
    "private-household-credit-and-deposits/"
    "private-household-credit-and-deposits-data/"
    "table-a-18-credit-deposits-irish-private-households.xls"
    "?sfvrsn=a8a2b21d_94"
)

BUCKET_NAME = "irish-financial-intelligence-gpm"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

RAW_FILE = RAW_DIR / "cbi_a18_raw.xls"
PROCESSED_FILE = PROCESSED_DIR / "household_credit.csv"

RAW_S3_KEY = "raw/cbi_a18/cbi_a18_raw.xls"
PROCESSED_S3_KEY = (
    "processed/household_credit/household_credit.csv"
)


# ============================================================
# CREATE DIRECTORIES
# ============================================================

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# STEP 1 - DOWNLOAD A.18 FROM CENTRAL BANK
# ============================================================

print("=" * 60)
print("STEP 1 - DOWNLOADING CBI A.18")
print("=" * 60)

response = requests.get(
    API_URL,
    timeout=60
)

print("Status code:", response.status_code)

response.raise_for_status()

RAW_FILE.write_bytes(response.content)

print("Raw data saved to:", RAW_FILE)


# ============================================================
# STEP 2 - LOAD A.18 WORKBOOK
# ============================================================

print("\n" + "=" * 60)
print("STEP 2 - LOADING A.18 WORKBOOK")
print("=" * 60)

xls = pd.ExcelFile(RAW_FILE)

print("Available sheets:")
print(xls.sheet_names)


# ============================================================
# STEP 3 - LOAD OUTSTANDING SHEET
# ============================================================

print("\n" + "=" * 60)
print("STEP 3 - LOADING TABLE A.18 - OUTSTANDING")
print("=" * 60)

a18_outstanding = pd.read_excel(
    RAW_FILE,
    sheet_name="Table A.18 - Outstanding",
    header=None
)

print(
    "Sheet shape:",
    a18_outstanding.shape
)


# ============================================================
# STEP 4 - EXTRACT SERIES 1243 - TOTAL LENDING
# ============================================================

print("\n" + "=" * 60)
print("STEP 4 - EXTRACTING SERIES 1243 - TOTAL LENDING")
print("=" * 60)

# Column 1 = reporting date
# Column 2 = Series Code 1243 - Total Lending

household_credit = a18_outstanding.iloc[
    10:, [1, 2]
].copy()

household_credit.columns = [
    "date",
    "household_credit"
]

print(
    "Extracted shape:",
    household_credit.shape
)


# ============================================================
# STEP 5 - CLEAN DATES AND VALUES
# ============================================================

print("\n" + "=" * 60)
print("STEP 5 - CLEANING HOUSEHOLD CREDIT DATA")
print("=" * 60)

household_credit["date"] = pd.to_datetime(
    household_credit["date"],
    errors="coerce"
)

household_credit["household_credit"] = pd.to_numeric(
    household_credit["household_credit"],
    errors="coerce"
)

# Remove rows where either date or value is invalid
household_credit = household_credit.dropna(
    subset=[
        "date",
        "household_credit"
    ]
)

# Keep sensible reporting dates
household_credit = household_credit[
    household_credit["date"] >= "2003-03-31"
].copy()

household_credit = (
    household_credit
    .sort_values("date")
    .reset_index(drop=True)
)

print(
    "Date range:",
    household_credit["date"].min(),
    "to",
    household_credit["date"].max()
)


# ============================================================
# STEP 6 - FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 6 - FINAL VALIDATION")
print("=" * 60)

print("Rows:", len(household_credit))

print(
    "Missing dates:",
    household_credit["date"].isna().sum()
)

print(
    "Missing values:",
    household_credit["household_credit"].isna().sum()
)

print(
    "Duplicate dates:",
    household_credit["date"].duplicated().sum()
)

print(
    "Date range:",
    household_credit["date"].min(),
    "to",
    household_credit["date"].max()
)

print(
    "Credit range:",
    household_credit["household_credit"].min(),
    "to",
    household_credit["household_credit"].max()
)


if household_credit["date"].isna().any():
    raise ValueError(
        "Missing dates found."
    )

if household_credit["household_credit"].isna().any():
    raise ValueError(
        "Missing household credit values found."
    )

if household_credit["date"].duplicated().any():
    raise ValueError(
        "Duplicate dates found."
    )


# ============================================================
# STEP 7 - SAVE PROCESSED DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 7 - SAVING PROCESSED DATASET")
print("=" * 60)

household_credit.to_csv(
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
print("CBI A.18 PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)