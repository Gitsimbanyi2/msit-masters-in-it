"""Lab 6 — region aggregation on sample-sales.csv. Key is the region."""

import csv
import os
from mini_mr import mapreduce

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(HERE, "..", "mit91205-day1", "sample-sales.csv"))

records = []
with open(CSV, newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        records.append((row["Order ID"], (row["Region"], float(row["Total Revenue"]))))


def mapper(order_id, record):
    region, amount = record
    yield region, (amount, 1)


def combiner(region, pairs):
    total = sum(amount for amount, _ in pairs)
    count = sum(n for _, n in pairs)
    yield region, [(total, count)]


def reducer(region, pairs):
    total = sum(amount for amount, _ in pairs)
    count = sum(n for _, n in pairs)
    yield region, (round(total, 2), count, round(total / count, 2))


result = mapreduce(records, mapper, reducer, combiner)
print("Region (total, orders, average):")
grand = 0.0
for region, (total, count, avg) in result:
    grand += total
    print(f"  {region}: total={total:,.2f}  orders={count}  avg={avg:,.2f}")
print(f"Grand total: {grand:,.2f}")

# One constant key forces every row through a single reducer.
hot = mapreduce(records, lambda i, rec: [("ALL", rec[1])], lambda k, vals: [(k, sum(vals))])
print(f"Hot key ALL received {len(records)} amounts in one reducer: {hot[0][1]:,.2f}")
