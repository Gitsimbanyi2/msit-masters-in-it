"""Lab 6 — the same category-revenue question as a Pig Latin dataflow."""

import csv
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(HERE, "..", "mit91205-day1", "sample-sales.csv"))

PRODUCTS = {
    "Laptop": "Computers",
    "Tablet": "Computers",
    "Monitor": "Displays",
    "Keyboard": "Accessories",
    "Mouse": "Accessories",
}


def load_sales(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


# sales = LOAD 'sample-sales.csv'
sales = load_sales(CSV)
# enriched = JOIN sales BY product, products BY name   (map-side; products is small)
enriched = []
for row in sales:
    enriched.append(
        {
            "product": row["Product"],
            "category": PRODUCTS[row["Product"]],
            "amount": float(row["Total Revenue"]),
        }
    )
# by_cat = GROUP enriched BY category
grouped = defaultdict(list)
for row in enriched:
    grouped[row["category"]].append(row)
# rev = FOREACH by_cat GENERATE group, SUM(amount)
revenue = []
for category, bag in grouped.items():
    revenue.append((category, sum(item["amount"] for item in bag)))
# top = ORDER rev BY revenue DESC
revenue.sort(key=lambda item: item[1], reverse=True)

print("Pig relations:")
print(f"  LOAD sales: {len(sales)}")
print(f"  JOIN enriched: {len(enriched)}")
print(f"  GROUP categories: {len(grouped)}")
print("  FOREACH SUM, ORDER DESC:")
for category, total in revenue:
    print(f"    {category}: {total:,.2f}")

# SPLIT a quarantine branch for a nonsense amount
clean, quarantine = [], []
for row in enriched:
    (clean if row["amount"] > 0 else quarantine).append(row)
print(f"  SPLIT clean={len(clean)} quarantine={len(quarantine)}")
