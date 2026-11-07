"""Lab 1 — split a file into blocks and place 3 rack-aware replicas."""

import os
from mini_hdfs import BLOCK_SIZE, REPLICATION, build_namespace, raw_storage

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(HERE, "..", "mit91205-day1", "sample-sales.csv"))

data = open(CSV, "rb").read()
ns = build_namespace("/data/sample-sales.csv", data)
nblocks = len(ns["blocks"])

print(f"File size: {ns['size']} bytes")
print(f"Block size: {BLOCK_SIZE} bytes")
print(f"Blocks: ceil(size/block) = {nblocks}")
print(f"Replication factor: {REPLICATION}")
print(f"Raw storage: {raw_storage(ns)} bytes (about {REPLICATION}x the file)")
print()
print("NameNode metadata (no file bytes):")
for block in ns["blocks"]:
    print(f"  {block['block_id']}  {block['size']:5d} B  replicas={block['replicas']}")

racks = {"dn1": "rackA", "dn2": "rackA", "dn3": "rackB", "dn4": "rackB"}
print()
print("Rack check (replica 2 must leave replica 1's rack):")
for block in ns["blocks"][:3]:
    r1, r2, r3 = block["replicas"]
    print(
        f"  {block['block_id']}: {r1}({racks[r1]}) -> {r2}({racks[r2]}) -> {r3}({racks[r3]})"
    )
    assert racks[r1] != racks[r2]
    assert racks[r2] == racks[r3]
print("Placement policy holds.")
