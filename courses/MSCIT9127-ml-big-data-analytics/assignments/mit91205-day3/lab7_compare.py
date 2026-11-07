"""Lab 7 — HiveQL and Pig must agree on category revenue."""

import csv
import os
import sqlite3
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

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE sales (product TEXT, amount REAL)")
db.execute("CREATE TABLE products (name TEXT, category TEXT)")
with open(CSV, newline="", encoding="utf-8") as handle:
    db.executemany(
        "INSERT INTO sales VALUES (?, ?)",
        [(r["Product"], float(r["Total Revenue"])) for r in csv.DictReader(handle)],
    )
db.executemany("INSERT INTO products VALUES (?, ?)", list(PRODUCTS.items()))
hive = dict(
    db.execute(
        """
        SELECT p.category, ROUND(SUM(s.amount), 2)
        FROM sales s JOIN products p ON s.product = p.name
        GROUP BY p.category
        """
    )
)

pig = defaultdict(float)
with open(CSV, newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        pig[PRODUCTS[row["Product"]]] += float(row["Total Revenue"])
pig = {k: round(v, 2) for k, v in pig.items()}

print("Category        HiveQL        Pig")
for category in sorted(hive):
    print(f"  {category:12} {hive[category]:12,.2f} {pig[category]:12,.2f}")
assert hive == pig
print("Same cluster, same files. The difference is the authoring style.")
print("Analyst report -> Hive. Multi-step clean/split/flatten -> Pig.")
