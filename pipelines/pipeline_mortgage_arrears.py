import requests
import pandas as pd
import boto3
from pathlib import Path


API_URL = (
    "https://www.centralbank.ie/docs/default-source/statistics/data-and-analysis/"
    "credit-and-banking-statistics/mortgage-arrears/mortgage-arrears-data/"
    "moa-data-tables-new1a3d13144644629bacc1ff0000269695.xlsx"
    "?sfvrsn=a379711a_1"
)

BUCKET_NAME = "irish-financial-intelligence-gpm"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

RAW_FILE = RAW_DIR / "cbi_mortgage_arrears_raw.xlsx"
PROCESSED_FILE = PROCESSED_DIR / "mortgage_arrears.csv"

RAW_S3_KEY = "raw/cbi_mortgage_arrears/cbi_mortgage_arrears_raw.xlsx"
PROCESSED_S3_KEY = "processed/mortgage_arrears/mortgage_arrears.csv"


# --------------------------------------------------
# 1. Create local directories
# --------------------------------------------------

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Download raw CBI workbook
# --------------------------------------------------

print("Downloading CBI mortgage arrears data...")

response = requests.get(API_URL, timeout=60)
response.raise_for_status()

RAW_FILE.write_bytes(response.content)

print("Raw data saved to:", RAW_FILE)


# --------------------------------------------------
# 3. Read Master Data sheet
# --------------------------------------------------

print("Reading Master Data (1)...")

master1 = pd.read_excel(
    RAW_FILE,
    sheet_name="Master Data (1)",
    header=None
)

# First row contains the actual column names
master1.columns = master1.iloc[0]
master1 = master1.iloc[1:].reset_index(drop=True)


# --------------------------------------------------
# 4. Clean important columns
# --------------------------------------------------

master1["Reporting Date"] = pd.to_datetime(
    master1["Reporting Date"],
    errors="coerce"
)

master1["Row Position"] = pd.to_numeric(
    master1["Row Position"],
    errors="coerce"
)

master1["Column Position"] = pd.to_numeric(
    master1["Column Position"],
    errors="coerce"
)


# --------------------------------------------------
# 5. Filter PDH data
# --------------------------------------------------

pdh = master1[
    (master1["Format"] == "PDH") &
    (master1["Entity Group"].isin(["Banks", "Non-Banks"]))
].copy()


# --------------------------------------------------
# 6. Total PDH mortgage accounts outstanding
# --------------------------------------------------

pdh_outstanding = pdh[
    (pdh["Category"] == "Total Outstanding") &
    (pdh["Column"] == "Number")
].copy()

pdh_outstanding = (
    pdh_outstanding
    .groupby("Reporting Date", as_index=False)["Amt"]
    .sum()
    .rename(columns={
        "Reporting Date": "date",
        "Amt": "pdh_mortgage_accounts"
    })
)


# --------------------------------------------------
# 7. Total PDH mortgage accounts in arrears
# --------------------------------------------------

pdh_arrears = pdh[
    (pdh["Category"] == "Arrears") &
    (pdh["Row Position"] == 2) &
    (pdh["Column"] == "Number")
].copy()

pdh_arrears = (
    pdh_arrears
    .groupby("Reporting Date", as_index=False)["Amt"]
    .sum()
    .rename(columns={
        "Reporting Date": "date",
        "Amt": "pdh_arrears_accounts"
    })
)


# --------------------------------------------------
# 8. PDH accounts more than 90 days in arrears
# --------------------------------------------------

# These are the non-overlapping duration categories:
# 181-365 days
# 365-730 days
# 2-5 years
# 5-10 years
# over 10 years
#
# Plus:
# 91-180 days

pdh_arrears_90_plus = pdh[
    (pdh["Category"] == "Arrears") &
    (pdh["Row Position"].isin([4, 6, 7, 9, 10, 11])) &
    (pdh["Column"] == "Number")
].copy()

pdh_arrears_90_plus = (
    pdh_arrears_90_plus
    .groupby("Reporting Date", as_index=False)["Amt"]
    .sum()
    .rename(columns={
        "Reporting Date": "date",
        "Amt": "pdh_arrears_90_plus_accounts"
    })
)


# --------------------------------------------------
# 9. Merge metrics
# --------------------------------------------------

mortgage_arrears = (
    pdh_outstanding
    .merge(pdh_arrears, on="date", how="inner")
    .merge(pdh_arrears_90_plus, on="date", how="inner")
)


# --------------------------------------------------
# 10. Calculate arrears rates
# --------------------------------------------------

mortgage_arrears["pdh_arrears_rate"] = (
    mortgage_arrears["pdh_arrears_accounts"]
    / mortgage_arrears["pdh_mortgage_accounts"]
    * 100
)

mortgage_arrears["pdh_arrears_90_plus_rate"] = (
    mortgage_arrears["pdh_arrears_90_plus_accounts"]
    / mortgage_arrears["pdh_mortgage_accounts"]
    * 100
)


# --------------------------------------------------
# 11. Sort and select final columns
# --------------------------------------------------

mortgage_arrears = (
    mortgage_arrears[
        [
            "date",
            "pdh_mortgage_accounts",
            "pdh_arrears_accounts",
            "pdh_arrears_90_plus_accounts",
            "pdh_arrears_rate",
            "pdh_arrears_90_plus_rate"
        ]
    ]
    .sort_values("date")
    .reset_index(drop=True)
)


# --------------------------------------------------
# 12. Validation
# --------------------------------------------------

if mortgage_arrears.empty:
    raise ValueError("Mortgage arrears dataset is empty.")

if mortgage_arrears["date"].duplicated().any():
    raise ValueError("Duplicate dates found.")

if mortgage_arrears.isna().any().any():
    raise ValueError("Missing values found.")

if (
    mortgage_arrears["pdh_arrears_accounts"]
    > mortgage_arrears["pdh_mortgage_accounts"]
).any():
    raise ValueError(
        "Arrears accounts exceed total mortgage accounts."
    )

if (
    mortgage_arrears["pdh_arrears_90_plus_accounts"]
    > mortgage_arrears["pdh_arrears_accounts"]
).any():
    raise ValueError(
        "90+ day arrears accounts exceed total arrears accounts."
    )

if (
    (mortgage_arrears["pdh_arrears_rate"] < 0) |
    (mortgage_arrears["pdh_arrears_rate"] > 100)
).any():
    raise ValueError("Invalid PDH arrears rate.")

if (
    (mortgage_arrears["pdh_arrears_90_plus_rate"] < 0) |
    (mortgage_arrears["pdh_arrears_90_plus_rate"] > 100)
).any():
    raise ValueError("Invalid PDH 90+ arrears rate.")


# --------------------------------------------------
# 13. Save processed data
# --------------------------------------------------

mortgage_arrears.to_csv(
    PROCESSED_FILE,
    index=False
)

print("Processed data saved to:", PROCESSED_FILE)
print("Rows:", len(mortgage_arrears))
print("Date range:", mortgage_arrears["date"].min(), "to",
      mortgage_arrears["date"].max())


# --------------------------------------------------
# 14. Upload to S3
# --------------------------------------------------

print("Uploading to S3...")

s3 = boto3.client("s3")

s3.upload_file(
    str(RAW_FILE),
    BUCKET_NAME,
    RAW_S3_KEY
)

s3.upload_file(
    str(PROCESSED_FILE),
    BUCKET_NAME,
    PROCESSED_S3_KEY
)

print("Raw file uploaded to:", RAW_S3_KEY)
print("Processed file uploaded to:", PROCESSED_S3_KEY)

print("Pipeline completed successfully.")