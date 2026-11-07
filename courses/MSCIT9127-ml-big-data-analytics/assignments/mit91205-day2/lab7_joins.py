"""Lab 7 — reduce-side join vs map-side join, plus a locality count."""

import csv
import os
from collections import defaultdict
from mini_mr import mapreduce
from mini_hdfs import build_namespace

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(HERE, "..", "mit91205-day1", "sample-sales.csv"))

PRODUCTS = {
    "Laptop": ("Computers", 1200),
    "Tablet": ("Computers", 400),
    "Monitor": ("Displays", 300),
    "Keyboard": ("Accessories", 20),
    "Mouse": ("Accessories", 15),
}

sales = []
with open(CSV, newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        sales.append(
            (
                row["Order ID"],
                row["Product"],
                float(row["Total Revenue"]),
            )
        )


def mapper(order_id, record):
    if record[0] == "S":
        _, product, amount = record
        yield product, ("S", amount)
    else:
        _, product, category, price = record
        yield product, ("P", category, price)


tagged = [("S", ("S", product, amount)) for _, product, amount in sales]
tagged += [("P", ("P", name, cat, price)) for name, (cat, price) in PRODUCTS.items()]


def reduce_join(product, values):
    products = [v for v in values if v[0] == "P"]
    amounts = [v[1] for v in values if v[0] == "S"]
    if not products or not amounts:
        return
    category = products[0][1]
    yield product, (category, round(sum(amounts), 2), len(amounts))


reduce_side = dict(mapreduce(tagged, mapper, reduce_join))


def map_side():
    """Small products table is hashed in mapper memory. No shuffle."""
    totals = defaultdict(lambda: [0.0, 0, None])
    for _, product, amount in sales:
        category, _price = PRODUCTS[product]
        totals[product][0] += amount
        totals[product][1] += 1
        totals[product][2] = category
    return {
        product: (category, round(total, 2), count)
        for product, (total, count, category) in totals.items()
    }


broadcast = map_side()
print("Reduce-side join (shuffle on product):")
for product in sorted(reduce_side):
    category, total, count = reduce_side[product]
    print(f"  {product:10} {category:12} orders={count:4} revenue={total:,.2f}")

assert reduce_side == broadcast
print("Map-side join matches. It skipped the shuffle because products fit in memory.")

# Locality: a map task is local when its block's first replica is the chosen node.
ns = build_namespace("/data/sample-sales.csv", open(CSV, "rb").read())
local = 0
for block in ns["blocks"]:
    chosen = block["replicas"][0]
    if chosen in block["replicas"]:
        local += 1
print(f"Map tasks with a local replica: {local}/{len(ns['blocks'])}")
