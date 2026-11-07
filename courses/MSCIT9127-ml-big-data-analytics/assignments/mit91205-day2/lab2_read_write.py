"""Lab 2 — NameNode is metadata only. Bytes move on the DataNode pipeline."""

import os
from mini_hdfs import build_namespace

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(HERE, "..", "mit91205-day1", "sample-sales.csv"))
data = open(CSV, "rb").read()
ns = build_namespace("/data/sample-sales.csv", data)
block = ns["blocks"][0]
dn1, dn2, dn3 = block["replicas"]

print("WRITE (first block)")
print("  1. Client asks NameNode to create /data/sample-sales.csv")
print(f"  2. NameNode returns replica list: {block['replicas']}")
print(f"  3. Pipeline: client -> {dn1} -> {dn2} -> {dn3}")
print(f"  4. Acks flow back: {dn3} -> {dn2} -> {dn1} -> client")
print("  5. NameNode never sees the block bytes")
print()
print("READ")
print("  1. Client asks NameNode where blk_0000 lives")
print(f"  2. NameNode returns {block['replicas']} (nearest first in a real cluster)")
print(f"  3. Client reads {block['size']} bytes from {dn1}")
print("  4. If that read fails, client tries the next replica")
print()
rebuilt = b"".join(b["bytes"] for b in ns["blocks"])
print(f"Reassembled file matches original: {rebuilt == data}")
