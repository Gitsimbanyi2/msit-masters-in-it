# lab4.py - Simple predictive analytics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("sample-sales.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])

monthly = (df.groupby(df["Order Date"].dt.to_period("M"))["Total Revenue"]
             .sum()
             .reset_index())
monthly.columns = ["Month", "Revenue"]
monthly["MonthIndex"] = range(len(monthly))

# Fit a straight line: revenue = slope * month + intercept
slope, intercept = np.polyfit(monthly["MonthIndex"], monthly["Revenue"], 1)
print(f"Trend line: Revenue = {slope:,.2f} * month + {intercept:,.2f}")

# Predict the next 3 months
next_months = [len(monthly), len(monthly) + 1, len(monthly) + 2]
for i, m in enumerate(next_months):
    pred = slope * m + intercept
    print(f"  Predicted revenue for month {m}: ${pred:,.2f}")

# Chart: actual + trend + forecast
plt.figure(figsize=(8, 4))
plt.plot(monthly["MonthIndex"], monthly["Revenue"], "o-", label="Actual")
plt.plot(monthly["MonthIndex"], slope * monthly["MonthIndex"] + intercept,
         "r--", label="Trend")
plt.plot(next_months, [slope * m + intercept for m in next_months],
         "g^--", label="Forecast")
plt.xlabel("Month index")
plt.ylabel("Revenue ($)")
plt.legend()
plt.tight_layout()
plt.savefig("revenue_forecast.png")
print("Chart saved: revenue_forecast.png")
