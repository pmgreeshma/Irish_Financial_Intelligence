import requests
import os

API_URL = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/HPM09/CSV/1.0/en"

response = requests.get(API_URL)

print("Status code:", response.status_code)

response.raise_for_status()

raw_file_path = "data/raw/hpm09_raw.csv"
os.makedirs("data/raw", exist_ok=True)

with open(raw_file_path, "w", encoding="utf-8") as file:
    file.write(response.text)

print("Raw data saved to:", raw_file_path)