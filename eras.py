import csv
import os
from collections import defaultdict

IN_PATH = os.path.join("data", "curve_shape.csv")

MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

SPLIT_YEAR = 2009

days = []
with open(IN_PATH, newline="") as f:
    for row in csv.DictReader(f):
        days.append({
            "year": int(row["period"][:4]),
            "month": int(row["period"][5:7]),
            "spread": float(row["spread"]),
            "shape": row["shape"],
        })

early = [d for d in days if d["year"] < SPLIT_YEAR]
late = [d for d in days if d["year"] >= SPLIT_YEAR]


def contango_pct(rows):
    if not rows:
        return 0.0
    return 100 * sum(1 for d in rows if d["shape"] == "contango") / len(rows)


def avg_spread(rows):
    if not rows:
        return 0.0
    return sum(d["spread"] for d in rows) / len(rows)


print(f"early era: 1994 to {SPLIT_YEAR - 1}   ({len(early)} days)")
print(f"late era:  {SPLIT_YEAR} to 2024   ({len(late)} days)")
print()
print(f"contango share   early {contango_pct(early):.1f}%   late {contango_pct(late):.1f}%")
print(f"average spread   early {avg_spread(early):+.3f}   late {avg_spread(late):+.3f}")
print()

print("average spread by month:")
print("  month      early       late      change")
for month in range(1, 13):
    e = [d for d in early if d["month"] == month]
    l = [d for d in late if d["month"] == month]
    ae = avg_spread(e)
    al = avg_spread(l)
    print(f"  {MONTH_NAMES[month - 1]}     {ae:+8.3f}   {al:+8.3f}   {al - ae:+8.3f}")

print()
summer_e = avg_spread([d for d in early if d["month"] in (8, 9)])
summer_l = avg_spread([d for d in late if d["month"] in (8, 9)])
winter_e = avg_spread([d for d in early if d["month"] in (12, 1)])
winter_l = avg_spread([d for d in late if d["month"] in (12, 1)])

print(f"summer peak (Aug-Sep)   early {summer_e:+.3f}   late {summer_l:+.3f}")
print(f"winter dip  (Dec-Jan)   early {winter_e:+.3f}   late {winter_l:+.3f}")
print(f"seasonal swing          early {summer_e - winter_e:.3f}   late {summer_l - winter_l:.3f}")