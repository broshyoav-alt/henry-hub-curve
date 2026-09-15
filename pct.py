import csv
import os

IN_PATH = os.path.join("data", "curve_shape.csv")

MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

SPLIT_YEAR = 2009

days = []
with open(IN_PATH, newline="") as f:
    for row in csv.DictReader(f):
        near = float(row["near"])
        if near <= 0:
            continue
        days.append({
            "year": int(row["period"][:4]),
            "month": int(row["period"][5:7]),
            "near": near,
            "spread": float(row["spread"]),
            "pct": 100 * float(row["spread"]) / near,
        })

early = [d for d in days if d["year"] < SPLIT_YEAR]
late = [d for d in days if d["year"] >= SPLIT_YEAR]


def avg(rows, key):
    if not rows:
        return 0.0
    return sum(d[key] for d in rows) / len(rows)


print(f"average near-contract price   early ${avg(early, 'near'):.2f}   late ${avg(late, 'near'):.2f}")
print()

print("average spread as % of near price, by month:")
print("  month      early       late      change")
for month in range(1, 13):
    e = [d for d in early if d["month"] == month]
    l = [d for d in late if d["month"] == month]
    ae = avg(e, "pct")
    al = avg(l, "pct")
    print(f"  {MONTH_NAMES[month - 1]}     {ae:+7.2f}%   {al:+7.2f}%   {al - ae:+7.2f}%")

print()
summer_e = avg([d for d in early if d["month"] in (8, 9)], "pct")
summer_l = avg([d for d in late if d["month"] in (8, 9)], "pct")
winter_e = avg([d for d in early if d["month"] in (12, 1)], "pct")
winter_l = avg([d for d in late if d["month"] in (12, 1)], "pct")

print("in percentage terms:")
print(f"  summer peak (Aug-Sep)   early {summer_e:+.2f}%   late {summer_l:+.2f}%")
print(f"  winter dip  (Dec-Jan)   early {winter_e:+.2f}%   late {winter_l:+.2f}%")
print(f"  seasonal swing          early {summer_e - winter_e:.2f}%   late {summer_l - winter_l:.2f}%")
print()
print("for comparison, in dollars:")
summer_e_d = avg([d for d in early if d["month"] in (8, 9)], "spread")
summer_l_d = avg([d for d in late if d["month"] in (8, 9)], "spread")
winter_e_d = avg([d for d in early if d["month"] in (12, 1)], "spread")
winter_l_d = avg([d for d in late if d["month"] in (12, 1)], "spread")
print(f"  seasonal swing          early {summer_e_d - winter_e_d:.3f}   late {summer_l_d - winter_l_d:.3f}")