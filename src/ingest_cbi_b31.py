import requests
import os

import requests
import os

API_URL = "https://opendata.centralbank.ie/api/3/action/datastore_search?resource_id=fb07a41b-15f7-4697-a7f7-ce8209d794e5"

response = requests.get(API_URL)

print("Status code:", response.status_code)

response.raise_for_status()

raw_file_path = "data/raw/cbi_b31_raw.json"

os.makedirs("data/raw", exist_ok=True)

with open(raw_file_path, "w", encoding="utf-8") as file:
    file.write(response.text)

print("Raw data saved to:", raw_file_path)