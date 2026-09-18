import requests
import os

API_URL = "https://www.centralbank.ie/docs/default-source/statistics/data-and-analysis/credit-and-banking-statistics/mortgage-arrears/mortgage-arrears-data/moa-data-tables-new1a3d13144644629bacc1ff0000269695.xlsx?sfvrsn=a379711a_1"

response = requests.get(API_URL)
print("Status code:", response.status_code)
response.raise_for_status()

raw_file_path = "data/raw/cbi_mortgage_arrears_raw.xlsx"
os.makedirs("data/raw", exist_ok=True)

with open(raw_file_path, "wb") as file:
    file.write(response.content)

print("Raw data saved to:", raw_file_path)