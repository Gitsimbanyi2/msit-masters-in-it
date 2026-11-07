"""Tiny HDFS stand-in: blocks, rack-aware replicas, read/write, failure."""


BLOCK_SIZE = 4096  # small on purpose so the Day 1 CSV spans several blocks
REPLICATION = 3

# (node, rack). Client writes from dn1 in rackA.
NODES = [
    ("dn1", "rackA"),
    ("dn2", "rackA"),
    ("dn3", "rackB"),
    ("dn4", "rackB"),
]


def split_blocks(data: bytes):
    blocks = []
    for i in range(0, len(data), BLOCK_SIZE):
        blocks.append(data[i : i + BLOCK_SIZE])
    return blocks


def place_replicas(block_index):
    """Default RF=3 policy from the lecture, rotated so blocks do not all pile on dn1."""
    # Replica 1: writer rack. Replica 2: other rack. Replica 3: same rack as replica 2.
    order = ["dn1", "dn3", "dn4", "dn2"]
    start = block_index % len(order)
    chosen = []
    for step in range(len(order)):
        node = order[(start + step) % len(order)]
        if len(chosen) == 0:
            chosen.append(node)
        elif len(chosen) == 1:
            rack = dict(NODES)[node]
            if rack != dict(NODES)[chosen[0]]:
                chosen.append(node)
        else:
            rack = dict(NODES)[node]
            if rack == dict(NODES)[chosen[1]] and node not in chosen:
                chosen.append(node)
        if len(chosen) == REPLICATION:
            break
    return chosen


def build_namespace(path, data: bytes):
    blocks = split_blocks(data)
    namespace = []
    for i, block in enumerate(blocks):
        namespace.append(
            {
                "block_id": f"blk_{i:04d}",
                "size": len(block),
                "replicas": place_replicas(i),
                "bytes": block,
            }
        )
    return {"path": path, "size": len(data), "blocks": namespace}


def raw_storage(ns):
    return sum(b["size"] for b in ns["blocks"]) * REPLICATION
