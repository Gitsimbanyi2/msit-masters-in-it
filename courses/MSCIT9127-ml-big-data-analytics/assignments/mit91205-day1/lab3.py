# lab3.py - Diagnostic analytics

import pandas as pd

df = pd.read_csv("sample-sales.csv")

# Cross-tab: revenue by region AND product
pivot = df.pivot_table(
    values="Total Revenue",
    index="Region",
    columns="Product",
    aggfunc="sum",
    fill_value=0
)

print("Revenue by region and product:")
print(pivot.round(2))

print("\nTop product per region:")
for region in pivot.index:
    top = pivot.loc[region].idxmax()
    value = pivot.loc[region].max()
    print(f"  {region}: {top} (${value:,.2f})")

print("\nLaptop as % of each region's revenue:")
share = (pivot["Laptop"] / pivot.sum(axis=1) * 100).round(1)
print(share)
