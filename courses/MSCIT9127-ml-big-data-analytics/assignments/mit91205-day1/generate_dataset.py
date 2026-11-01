# generate_dataset.py
# MIT 91205 - Day 1 Practical
# Generates sample-sales.csv deterministically (fixed seed 42).

import numpy as np
import pandas as pd
from datetime import datetime

# Fixed seed => the file you generate is identical to what your
# lecturer sees. This is how we reproduce results.
np.random.seed(42)

regions = ["North", "South", "East", "West"]
region_weights = [0.30, 0.28, 0.22, 0.20]      # share of orders

products = {
    "Laptop":   1200,
    "Tablet":    500,
    "Monitor":   300,
    "Keyboard":   45,
    "Mouse":      25,
}

# Product mix per region. South prefers Tablets; others prefer Laptops.
# We will use this later in Lab 3 to make diagnostic analytics meaningful.
product_weights = {
    "North": [0.35, 0.25, 0.20, 0.12, 0.08],
    "South": [0.15, 0.45, 0.20, 0.12, 0.08],
    "East":  [0.30, 0.22, 0.25, 0.13, 0.10],
    "West":  [0.32, 0.20, 0.25, 0.13, 0.10],
}

rows = []
order_id = 1001

# 12 months of 2024, with a mild upward trend in order volume
for month in range(1, 13):
    n_orders = 65 + month * 3                  # month 1: 68; month 12: 101
    for _ in range(n_orders):
        day = int(np.random.randint(1, 29))
        date = datetime(2024, month, day)

        region = np.random.choice(regions, p=region_weights)
        product = np.random.choice(list(products.keys()),
                                   p=product_weights[region])

        units = int(np.random.randint(1, 6))   # 1-5 units
        unit_price = products[product]
        total = units * unit_price

        rows.append({
            "Order ID":       order_id,
            "Order Date":     date.strftime("%Y-%m-%d"),
            "Region":         region,
            "Product":        product,
            "Units Sold":     units,
            "Unit Price":     unit_price,
            "Total Revenue":  total,
        })
        order_id += 1

df = pd.DataFrame(rows)
df.to_csv("sample-sales.csv", index=False)

print(f"Generated {len(df)} orders  ->  sample-sales.csv")
print("\nFirst 5 rows:")
print(df.head().to_string(index=False))
print("\nData range:", df["Order Date"].min(), "to", df["Order Date"].max())
