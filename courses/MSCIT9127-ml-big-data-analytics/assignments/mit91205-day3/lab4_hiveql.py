"""Lab 4 — HiveQL shapes from the lecture, executed in SQLite on sample-sales.csv."""

import csv
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(HERE, "..", "mit91205-day1", "sample-sales.csv"))

PRODUCTS = [
    ("Laptop", "Computers", 1200),
    ("Tablet", "Computers", 400),
    ("Monitor", "Displays", 300),
    ("Keyboard", "Accessories", 20),
    ("Mouse", "Accessories", 15),
]

db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row
db.execute(
    """
    CREATE TABLE sales (
        sale_id INTEGER,
        dt TEXT,
        region TEXT,
        product TEXT,
        quantity INTEGER,
        unit_price REAL,
        amount REAL
    )
    """
)
db.execute(
    "CREATE TABLE products (name TEXT, category TEXT, unit_price REAL)"
)
with open(CSV, newline="", encoding="utf-8") as handle:
    rows = [
        (
            int(r["Order ID"]),
            r["Order Date"],
            r["Region"],
            r["Product"],
            int(r["Units Sold"]),
            float(r["Unit Price"]),
            float(r["Total Revenue"]),
        )
        for r in csv.DictReader(handle)
    ]
db.executemany("INSERT INTO sales VALUES (?,?,?,?,?,?,?)", rows)
db.executemany("INSERT INTO products VALUES (?,?,?)", PRODUCTS)

print("Projection and filter (North, amount > 5000, March):")
for row in db.execute(
    """
    SELECT sale_id, product, amount
    FROM sales
    WHERE amount > 5000 AND dt >= '2024-03-01' AND dt < '2024-04-01' AND region = 'North'
    ORDER BY amount DESC
    LIMIT 5
    """
):
    print(f"  {row['sale_id']} {row['product']} {row['amount']:.0f}")

print("Aggregation with HAVING (regions over 400000 in March is yearly here):")
for row in db.execute(
    """
    SELECT region, ROUND(SUM(amount), 2) AS revenue, COUNT(*) AS num_sales
    FROM sales
    GROUP BY region
    HAVING SUM(amount) > 400000
    ORDER BY revenue DESC
    """
):
    print(f"  {row['region']}: {row['revenue']:.2f} ({row['num_sales']} sales)")

print("Inner join — revenue by category:")
for row in db.execute(
    """
    SELECT p.category, ROUND(SUM(s.amount), 2) AS revenue
    FROM sales s
    JOIN products p ON s.product = p.name
    GROUP BY p.category
    ORDER BY revenue DESC
    """
):
    print(f"  {row['category']}: {row['revenue']:.2f}")

print("Left join orphans (expect none; every product is in the catalog):")
orphans = db.execute(
    """
    SELECT COUNT(*) AS n
    FROM sales s
    LEFT JOIN products p ON s.product = p.name
    WHERE p.name IS NULL
    """
).fetchone()["n"]
print(f"  orphan sales: {orphans}")

print("Subquery — region totals from per-product revenue:")
for row in db.execute(
    """
    SELECT region, ROUND(SUM(revenue), 2) AS revenue
    FROM (
        SELECT region, product, SUM(amount) AS revenue
        FROM sales
        GROUP BY region, product
    ) t
    GROUP BY region
    ORDER BY revenue DESC
    """
):
    print(f"  {row['region']}: {row['revenue']:.2f}")

db.execute(
    """
    CREATE VIEW march_north AS
    SELECT sale_id, product, amount
    FROM sales
    WHERE region = 'North' AND dt >= '2024-03-01' AND dt < '2024-04-01'
    """
)
n = db.execute("SELECT COUNT(*) AS n FROM march_north").fetchone()["n"]
print(f"View march_north rows: {n} (definition only, not a copy of the files)")
