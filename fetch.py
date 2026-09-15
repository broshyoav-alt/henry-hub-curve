import csv
import os
import time
from collections import Counter

import requests


def load_key():
    with open(".env") as f:
        for line in f:
            if line.startswith("EIA_API_KEY="):
                return line.strip().split("=", 1)[1]
    raise SystemExit("Could not find EIA_API_KEY in .env")


API_KEY = load_key()

URL = "https://api.eia.gov/v2/natural-gas/pri/fut/data/"

PARAMS = {
    "api_key": API_KEY,
    "frequency": "daily",
    "data[0]": "value",
    "facets[series][]": ["RNGC1", "RNGC2", "RNGC3", "RNGC4"],
    "sort[0][column]": "period",
    "sort[0][direction]": "asc",
    "length": 5000,
}

rows = []
offset = 0

while True:
    params = dict(PARAMS)
    params["offset"] = offset

    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()

    payload = response.json()["response"]
    batch = payload["data"]

    if not batch:
        break

    rows.extend(batch)
    total = int(payload["total"])
    print(f"fetched {len(rows)} of {total} rows")

    offset += len(batch)
    if offset >= total:
        break

    time.sleep(1)
clean = []
for row in rows:
    value = row.get("value")
    if value in (None, ""):
        continue
    clean.append({
        "period": row["period"],
        "series": row["series"],
        "value": float(value),
    })

clean.sort(key=lambda r: (r["period"], r["series"]))

os.makedirs(os.path.join("data", "raw"), exist_ok=True)
out_path = os.path.join("data", "raw", "henry_hub_futures.csv")

with open(out_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["period", "series", "value"])
    writer.writeheader()
    writer.writerows(clean)

print()
print(f"saved {len(clean)} rows to {out_path}")
print(f"dates run from {clean[0]['period']} to {clean[-1]['period']}")
print()
print("rows per contract:")
for name, count in sorted(Counter(r["series"] for r in clean).items()):
    print(f"  {name}: {count}")