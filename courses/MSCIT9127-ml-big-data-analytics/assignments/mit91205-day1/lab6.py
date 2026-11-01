# lab6.py - CAP theorem in practice

node_a = {"balance": 100}
node_b = {"balance": 100}

def write_balance(node, new_balance):
    node["balance"] = new_balance

def read_balance(node):
    return node["balance"]

print("=== Scenario A: Network healthy ===")
write_balance(node_a, 200)
write_balance(node_b, 200)
print(f"node_a: {read_balance(node_a)}")
print(f"node_b: {read_balance(node_b)}")
print("Both consistent.")

print("\n=== Scenario B: Partition, choose CP (Consistency) ===")
node_a["balance"] = 300
print("node_a:", node_a["balance"])
print("Client reads node_b: ERROR (node_b is unreachable)")

print("\n=== Scenario C: Partition, choose AP (Availability) ===")
print("Client reads node_b:", node_b["balance"], "(stale but available)")
print("node_a has 300; node_b still says 200.")
print("Availability chosen over consistency.")
