import csv
import os
from collections import defaultdict

IN_PATH = os.path.join("data", "raw", "henry_hub_futures.csv")
OUT_PATH = os.path.join("data", "curve_shape.csv")

MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

by_date = defaultdict(dict)
with open(IN_PATH, newline="") as f:
    for row in csv.DictReader(f):
        by_date[row["period"]][row["series"]] = float(row["value"])

days = []
for date in sorted(by_date):
    prices = by_date[date]
    if "RNGC1" not in prices or "RNGC4" not in prices:
        continue

    near = prices["RNGC1"]
    far = prices["RNGC4"]
    spread = far - near

    days.append({
        "period": date,
        "near": near,
        "far": far,
        "spread": round(spread, 4),
        "shape": "contango" if spread > 0 else "backwardation",
    })

os.makedirs("data", exist_ok=True)
with open(OUT_PATH, "w", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=["period", "near", "far", "spread", "shape"]
    )
    writer.writeheader()
    writer.writerows(days)

print(f"analysed {len(days)} trading days")
print(f"from {days[0]['period']} to {days[-1]['period']}")
print(f"saved to {OUT_PATH}")
print()

contango_days = sum(1 for d in days if d["shape"] == "contango")
share = 100 * contango_days / len(days)
print(f"contango on {share:.1f}% of days, backwardation on {100 - share:.1f}%")
print()

print("by calendar month:")
print("  month   days   contango%   avg spread")
for month in range(1, 13):
    month_days = [d for d in days if int(d["period"][5:7]) == month]
    if not month_days:
        continue
    c = sum(1 for d in month_days if d["shape"] == "contango")
    pct = 100 * c / len(month_days)
    avg = sum(d["spread"] for d in month_days) / len(month_days)
    print(f"  {MONTH_NAMES[month - 1]}    {len(month_days):5d}    {pct:6.1f}%    {avg:+8.3f}")