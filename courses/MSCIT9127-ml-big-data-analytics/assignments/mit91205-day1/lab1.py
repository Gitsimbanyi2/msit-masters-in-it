# lab1.py - Meet the data

import pandas as pd

# Load the CSV into a table called "df"
# df = "data frame", the standard name for a pandas table.
df = pd.read_csv("sample-sales.csv")

print("=== First 5 rows ===")
print(df.head())

print("\n=== Shape (rows, columns) ===")
print(df.shape)

print("\n=== Column names ===")
print(df.columns.tolist())

print("\n=== Summary statistics ===")
print(df.describe())

print("\n=== Missing values per column ===")
print(df.isnull().sum())
