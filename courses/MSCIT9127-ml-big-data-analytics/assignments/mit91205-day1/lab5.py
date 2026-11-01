# lab5.py - Simulating partitioning and replication

import pandas as pd

df = pd.read_csv("sample-sales.csv")

# ---- Step 1: Partition by Region ----
partitions = {}
for region, chunk in df.groupby("Region"):
    partitions[region] = chunk.reset_index(drop=True)
    print(f"Partition '{region}': {len(chunk)} rows")

# ---- Step 2: Replicate each partition 3 times ----
REPLICATION_FACTOR = 3
replicas = {region: [partitions[region].copy() for _ in range(REPLICATION_FACTOR)]
            for region in partitions}
print(f"\nEach partition has {REPLICATION_FACTOR} replicas:")
for region in replicas:
    print(f"  '{region}': {len(replicas[region])} copies")

# ---- Step 3: Simulate a node failure ----
print("\n>>> Simulating: primary node of 'North' fails <<<")
replicas["North"].pop(0)
print(f"'North' now has {len(replicas['North'])} healthy replicas")

# ---- Step 4: Recover from surviving replica ----
recovered = replicas["North"][0]
print(f"Recovered {len(recovered)} rows for North from surviving replica.")
print("\nFirst row of recovered North data:")
print(recovered.iloc[0])
