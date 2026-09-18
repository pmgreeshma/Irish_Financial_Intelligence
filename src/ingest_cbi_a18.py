import requests
import os

API_URL = "https://www.centralbank.ie/docs/default-source/statistics/data-and-analysis/credit-and-banking-statistics/private-household-credit-and-deposits/private-household-credit-and-deposits-data/table-a-18-credit-deposits-irish-private-households.xls?sfvrsn=a8a2b21d_94"

response = requests.get(API_URL)

print("Status code:", response.status_code)

response.raise_for_status()

raw_file_path = "data/raw/cbi_a18_raw.xls"

os.makedirs("data/raw", exist_ok=True)

with open(raw_file_path, "wb") as file:
    file.write(response.content)

print("Raw data saved to:", raw_file_path)