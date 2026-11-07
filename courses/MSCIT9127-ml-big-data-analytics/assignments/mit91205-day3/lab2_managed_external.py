"""Lab 2 — dropping a managed table deletes files. Dropping an external table does not."""

import os
import shutil
import tempfile

root = tempfile.mkdtemp(prefix="hive-lab-")
warehouse = os.path.join(root, "warehouse", "sales")
landing = os.path.join(root, "landing", "sales")
os.makedirs(warehouse)
os.makedirs(landing)
open(os.path.join(warehouse, "part-0000"), "w", encoding="utf-8").write("managed\n")
open(os.path.join(landing, "part-0000"), "w", encoding="utf-8").write("external\n")

metadata = {
    "sales_managed": {"kind": "managed", "location": warehouse},
    "sales_external": {"kind": "external", "location": landing},
}


def drop(table):
    spec = metadata.pop(table)
    if spec["kind"] == "managed":
        shutil.rmtree(spec["location"])
    # external: metadata only


drop("sales_managed")
drop("sales_external")

print(f"Managed directory still exists: {os.path.exists(warehouse)}")
print(f"External directory still exists: {os.path.exists(landing)}")
print(f"Tables left in metastore: {list(metadata)}")
assert not os.path.exists(warehouse)
assert os.path.exists(landing)
shutil.rmtree(root)
print("Drop removes ownership, not the query engine.")
