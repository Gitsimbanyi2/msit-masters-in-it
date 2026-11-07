"""Lab 5 — a columnar layout reads only the columns the query names."""

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(HERE, "..", "mit91205-day1", "sample-sales.csv"))

with open(CSV, newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

columns = list(rows[0].keys())
# Rough byte size of each column's text, which is what a columnar reader can skip.
sizes = {col: sum(len(row[col]) for row in rows) for col in columns}
row_bytes = sum(sizes.values())
needed = sizes["Region"] + sizes["Total Revenue"]
print(f"Row-oriented scan of all columns: {row_bytes} text bytes")
print(f"Columnar scan of Region + Total Revenue: {needed} text bytes")
print(f"Bytes skipped by projection: {row_bytes - needed}")
print("Text/JSON is the landing format. Parquet or ORC is the analytical format.")
print("ORC is the usual Hive default. Parquet is the safer choice across Spark and Trino.")
