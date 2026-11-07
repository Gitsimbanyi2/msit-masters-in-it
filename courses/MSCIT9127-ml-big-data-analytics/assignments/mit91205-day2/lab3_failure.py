"""Lab 3 — a dead DataNode drops one replica. NameNode schedules a replacement."""

import os
from mini_hdfs import REPLICATION, build_namespace

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.normpath(os.path.join(HERE, "..", "mit91205-day1", "sample-sales.csv"))
ns = build_namespace("/data/sample-sales.csv", open(CSV, "rb").read())

DEAD = "dn1"
LIVE = ["dn2", "dn3", "dn4"]
lost = 0
for block in ns["blocks"]:
    if DEAD in block["replicas"]:
        lost += 1
        block["replicas"] = [n for n in block["replicas"] if n != DEAD]
        for candidate in LIVE:
            if candidate not in block["replicas"]:
                block["replicas"].append(candidate)
                break
    assert len(block["replicas"]) == REPLICATION
    assert DEAD not in block["replicas"]

print(f"DataNode {DEAD} missed heartbeats and is marked dead.")
print(f"Blocks that lost a replica: {lost} of {len(ns['blocks'])}")
print("NameNode scheduled a new replica on a live node that did not already hold it.")
print("Sample after recovery:")
for block in ns["blocks"][:3]:
    print(f"  {block['block_id']} -> {block['replicas']}")
print("Data is still readable. Replication does not protect against deleting the file.")
