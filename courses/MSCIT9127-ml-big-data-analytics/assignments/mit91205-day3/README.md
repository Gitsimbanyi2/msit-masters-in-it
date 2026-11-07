# MIT 91205 Day 3 practical — Hive and Pig without a cluster

SQLite stands in for HiveQL. A few Python functions stand in for Pig Latin. The bytes, partitions, and joins are the lecture's ideas run on `../mit91205-day1/sample-sales.csv`.

| Script | Lecture idea |
| --- | --- |
| `lab1_schema_on_read.py` | Same line, pipe SerDe vs comma SerDe |
| `lab2_managed_external.py` | DROP managed deletes files; DROP external does not |
| `lab3_partitions.py` | Month directories and partition pruning |
| `lab4_hiveql.py` | Filter, HAVING, join, orphan check, subquery, view |
| `lab5_formats.py` | Why a columnar projection reads fewer bytes |
| `lab6_pig.py` | LOAD, JOIN, GROUP, FOREACH, ORDER, SPLIT |
| `lab7_compare.py` | Hive and Pig return the same category revenue |

```text
cd courses/MSCIT9127-ml-big-data-analytics/assignments/mit91205-day3
python lab1_schema_on_read.py
python lab4_hiveql.py
python lab6_pig.py
python lab7_compare.py
```

No extra packages.

Study notes: `../../day3-study-notes.md`
