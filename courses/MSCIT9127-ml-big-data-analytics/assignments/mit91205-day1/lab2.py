# lab2.py - Descriptive analytics

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sample-sales.csv")

# 1. Total revenue
total_revenue = df["Total Revenue"].sum()
print(f"Total revenue: ${total_revenue:,.2f}")

# 2. Revenue per region
revenue_by_region = df.groupby("Region")["Total Revenue"].sum()
print("\nRevenue by region:")
print(revenue_by_region.sort_values(ascending=False))

# 3. Top 5 products by revenue
top_products = (df.groupby("Product")["Total Revenue"]
                  .sum()
                  .sort_values(ascending=False)
                  .head(5))
print("\nTop 5 products by revenue:")
print(top_products)

# 4. Monthly revenue
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Month"] = df["Order Date"].dt.to_period("M")
monthly = df.groupby("Month")["Total Revenue"].sum()
print("\nMonthly revenue:")
print(monthly)

# 5. Bar chart
revenue_by_region.plot(kind="bar", title="Revenue by Region")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("revenue_by_region.png")
print("\nChart saved: revenue_by_region.png")
