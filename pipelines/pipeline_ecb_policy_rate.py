import requests
import pandas as pd
import boto3
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_URL = (
    "https://data-api.ecb.europa.eu/service/data/"
    "FM/B.U2.EUR.4F.KR.DFR.CHG?format=csvdata"
)

BUCKET_NAME = "irish-financial-intelligence-gpm"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

RAW_FILE = RAW_DIR / "ecb_policy_rate_raw.csv"
PROCESSED_FILE = PROCESSED_DIR / "ecb_policy_rate.csv"

RAW_S3_KEY = "raw/ecb_policy_rate/ecb_policy_rate_raw.csv"
PROCESSED_S3_KEY = "processed/ecb_policy_rate/ecb_policy_rate.csv"


# --------------------------------------------------
# 1. Create local directories
# --------------------------------------------------

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Download raw ECB data
# --------------------------------------------------

print("Downloading ECB policy rate data...")

response = requests.get(API_URL, timeout=60)
response.raise_for_status()

RAW_FILE.write_text(
    response.text,
    encoding="utf-8"
)

print("Raw data saved to:", RAW_FILE)


# --------------------------------------------------
# 3. Read raw data
# --------------------------------------------------

df = pd.read_csv(RAW_FILE)

print("Raw data shape:", df.shape)


# --------------------------------------------------
# 4. Extract policy rate changes
# --------------------------------------------------

ecb = df[
    ["TIME_PERIOD", "OBS_VALUE"]
].copy()

ecb["TIME_PERIOD"] = pd.to_datetime(
    ecb["TIME_PERIOD"],
    errors="coerce"
)

ecb["OBS_VALUE"] = pd.to_numeric(
    ecb["OBS_VALUE"],
    errors="coerce"
)

ecb = (
    ecb
    .sort_values("TIME_PERIOD")
    .reset_index(drop=True)
)


# --------------------------------------------------
# 5. Validate raw observations
# --------------------------------------------------

if ecb.empty:
    raise ValueError("ECB dataset is empty.")

if ecb["TIME_PERIOD"].isna().any():
    raise ValueError("Invalid ECB dates found.")

if ecb["OBS_VALUE"].isna().any():
    raise ValueError("Missing ECB rate changes found.")

if ecb["TIME_PERIOD"].duplicated().any():
    raise ValueError("Duplicate ECB dates found.")


# --------------------------------------------------
# 6. Reconstruct ECB deposit facility rate
# --------------------------------------------------

# Initial ECB deposit facility rate at the start
# of Stage Three of Economic and Monetary Union.
initial_rate = 2.00

ecb["ecb_deposit_facility_rate"] = (
    initial_rate + ecb["OBS_VALUE"].cumsum()
)


# --------------------------------------------------
# 7. Create final processed dataset
# --------------------------------------------------

ecb_policy_rate = ecb[
    [
        "TIME_PERIOD",
        "OBS_VALUE",
        "ecb_deposit_facility_rate"
    ]
].copy()

ecb_policy_rate = ecb_policy_rate.rename(
    columns={
        "TIME_PERIOD": "date",
        "OBS_VALUE": "rate_change"
    }
)

ecb_policy_rate = (
    ecb_policy_rate
    .sort_values("date")
    .reset_index(drop=True)
)


# --------------------------------------------------
# 8. Validate processed dataset
# --------------------------------------------------

if ecb_policy_rate.empty:
    raise ValueError("Processed ECB dataset is empty.")

if ecb_policy_rate["date"].duplicated().any():
    raise ValueError("Duplicate dates found in processed data.")

if ecb_policy_rate.isna().any().any():
    raise ValueError("Missing values found in processed data.")

if not ecb_policy_rate["date"].is_monotonic_increasing:
    raise ValueError("ECB dates are not sorted correctly.")


# --------------------------------------------------
# 9. Save processed data
# --------------------------------------------------

ecb_policy_rate.to_csv(
    PROCESSED_FILE,
    index=False
)

print("Processed ECB policy rate saved to:", PROCESSED_FILE)

print(
    "Date range:",
    ecb_policy_rate["date"].min(),
    "to",
    ecb_policy_rate["date"].max()
)

print(
    "Latest ECB deposit facility rate:",
    ecb_policy_rate["ecb_deposit_facility_rate"].iloc[-1]
)

print(
    "Latest rate change:",
    ecb_policy_rate["rate_change"].iloc[-1]
)


# --------------------------------------------------
# 10. Upload to S3
# --------------------------------------------------

print("Uploading ECB data to S3...")

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

print("ECB policy rate pipeline completed successfully.")

