# lab7.py - Full analytics lifecycle pipeline

import pandas as pd
import matplotlib.pyplot as plt
import duckdb

# ---- STAGE 1: Business Understanding ----
print("=" * 50)
print("BUSINESS QUESTION:")
print("  Which region should we expand, and with which product?")
print("=" * 50)

# ---- STAGE 2: Data Acquisition ----
df = pd.read_csv("sample-sales.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])
print(f"\nLoaded {len(df)} orders "
      f"from {df['Order Date'].min().date()} "
      f"to {df['Order Date'].max().date()}")

# ---- STAGE 3: Data Preparation ----
df = df.dropna()
print(f"After cleaning: {len(df)} complete rows")

# ---- STAGE 4: Data Analysis (SQL via DuckDB) ----
con = duckdb.connect()
con.register("sales", df)

result = con.execute("""
    SELECT
        Region,
        Product,
        SUM("Total Revenue") AS total_revenue,
        SUM("Units Sold")    AS units
    FROM sales
    GROUP BY Region, Product
    ORDER BY total_revenue DESC
""").df()

print("\nTop revenue combinations (region + product):")
print(result.head(10).to_string(index=False))

# ---- STAGE 5: Visualization ----
top5 = result.head(5)
labels = top5["Region"] + " - " + top5["Product"]
plt.figure(figsize=(8, 4))
plt.barh(labels, top5["total_revenue"])
plt.xlabel("Revenue ($)")
plt.title("Top 5 Region-Product Combinations")
plt.tight_layout()
plt.savefig("top_combinations.png")
print("\nChart saved: top_combinations.png")

# ---- STAGE 6: Action & Feedback ----
top = result.iloc[0]
print("\n" + "=" * 50)
print("RECOMMENDATION (validate with business):")
print(f"  Focus on {top['Region']} with {top['Product']}.")
print("=" * 50)
