import requests
import os

API_URL = "https://data-api.ecb.europa.eu/service/data/FM/B.U2.EUR.4F.KR.DFR.CHG?format=csvdata"

response = requests.get(API_URL)

print("Status code:", response.status_code)
response.raise_for_status()

raw_file_path = "F:/Irish_Financial_Intelligence/data/raw/ecb_policy_rate_raw.csv"
os.makedirs("F:/Irish_Financial_Intelligence/data/raw", exist_ok=True)

with open(raw_file_path, "w", encoding="utf-8") as file:
    file.write(response.text)

print("Raw data saved to:", raw_file_path)


