import requests
import pandas as pd
from io import StringIO


# --------------------------------------------------
# 1. CSO RSM08 API
# --------------------------------------------------

API_URL = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/RSM08/CSV/1.0/en"


# --------------------------------------------------
# 2. Request data from the API
# --------------------------------------------------

response = requests.get(API_URL)

print("Status code:", response.status_code)

response.raise_for_status()


# --------------------------------------------------
# 3. Save the original API response
# --------------------------------------------------

raw_file_path = "data/raw/rsm08_raw.csv"

with open(raw_file_path, "w", encoding="utf-8") as file:
    file.write(response.text)

print("Raw data saved to:", raw_file_path)


# --------------------------------------------------
# 4. Load the data into Pandas
# --------------------------------------------------

df = pd.read_csv(StringIO(response.text))


# --------------------------------------------------
# 5. Basic information
# --------------------------------------------------

print("\nNumber of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())