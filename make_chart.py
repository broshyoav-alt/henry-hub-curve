import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

IN_PATH = os.path.join("data", "curve_shape.csv")
OUT_DIR = "output"
OUT_PATH = os.path.join(OUT_DIR, "seasonality.png")

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
            "pct": 100 * float(row["spread"]) / near,
        })


def monthly_avg(rows):
    out = []
    for month in range(1, 13):
        vals = [d["pct"] for d in rows if d["month"] == month]
        out.append(sum(vals) / len(vals) if vals else 0.0)
    return out


early = [d for d in days if d["year"] < SPLIT_YEAR]
late = [d for d in days if d["year"] >= SPLIT_YEAR]

early_avg = monthly_avg(early)
late_avg = monthly_avg(late)

first_year = min(d["year"] for d in days)
last_year = max(d["year"] for d in days)

fig, ax = plt.subplots(figsize=(9, 5.2))

ax.axhline(0, color="#999999", linewidth=0.9, zorder=1)

ax.plot(
    MONTH_NAMES, early_avg,
    marker="o", markersize=5, linewidth=2.2, color="#B8860B",
    label=f"{first_year}\u2013{SPLIT_YEAR - 1}  (pre-shale)", zorder=3,
)
ax.plot(
    MONTH_NAMES, late_avg,
    marker="o", markersize=5, linewidth=2.2, color="#1D7A5F",
    label=f"{SPLIT_YEAR}\u2013{last_year}  (post-shale)", zorder=3,
)

ax.set_title(
    "Henry Hub seasonal curve structure narrowed after shale",
    fontsize=14, fontweight="bold", pad=30, loc="left",
)
ax.text(
    0, 1.025,
    "4th-nearby minus front-month futures, as % of front-month price",
    transform=ax.transAxes, fontsize=10, color="#555555", va="bottom",
)

ax.set_ylabel("spread, % of front-month price")
ax.legend(frameon=False, loc="upper left")
ax.grid(axis="y", color="#E6E6E6", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#CCCCCC")

ax.annotate(
    "above 0: contango, gas later costs more",
    xy=(0.985, 0.5), xycoords="axes fraction",
    xytext=(0, 6), textcoords="offset points",
    ha="right", va="bottom", fontsize=9, color="#777777",
)
ax.annotate(
    "below 0: backwardation, gas now costs more",
    xy=(0.985, 0.5), xycoords="axes fraction",
    xytext=(0, -8), textcoords="offset points",
    ha="right", va="top", fontsize=9, color="#777777",
)

fig.text(
    0.005, 0.005,
    "Source: US EIA, Henry Hub NYMEX futures contracts 1 and 4, daily settlements.",
    fontsize=8, color="#888888",
)

fig.tight_layout()
os.makedirs(OUT_DIR, exist_ok=True)
fig.savefig(OUT_PATH, dpi=150)

print(f"saved chart to {OUT_PATH}")
print(f"covering {first_year} to {last_year}, {len(days)} trading days")