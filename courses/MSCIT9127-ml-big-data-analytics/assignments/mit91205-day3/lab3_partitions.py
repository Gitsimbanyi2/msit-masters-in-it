"""Lab 3 — partition pruning. A month filter reads one directory, not the whole year."""

import csv
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(HERE, "..", "mit91205-day1", "sample-sales.csv"))

by_month = defaultdict(list)
with open(CSV, newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        month = row["Order Date"][:7]
        by_month[month].append(row)

full_scan = sum(len(rows) for rows in by_month.values())
target = "2024-03"
pruned = by_month[target]
print(f"Partitions (one directory per month): {len(by_month)}")
print(f"Full scan rows: {full_scan}")
print(f"WHERE dt LIKE '{target}%' reads partition dt={target}: {len(pruned)} rows")
print(f"Rows not opened: {full_scan - len(pruned)}")

# A function wrapped around the partition column defeats a simple directory match.
def cast_filter(month_key):
    return month_key.replace("-", "") == "202403"


print(f"CAST-style filter still finds the month: {cast_filter(target)} (planner may not prune)")
