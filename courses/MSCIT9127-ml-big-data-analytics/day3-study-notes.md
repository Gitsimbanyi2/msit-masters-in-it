# MIT 91205 / MSCIT9127 — Day 3 study notes

**Lecturer:** Dr. Bugingo Emmanuel
**Title:** Apache Hive and Apache Pig for Large-Scale Data Processing
**Practical:** `assignments/mit91205-day3/`
**Dataset:** Day 1 `sample-sales.csv`, plus a five-row product catalog (Laptop and Tablet = Computers, Monitor = Displays, Keyboard and Mouse = Accessories)

These notes are in my own words. SQLite runs the HiveQL. Python functions run the Pig dataflow. Neither is a Hive or Pig installation. The SQL shape and the relation names match the lecture.

## 1. What this day is for

Day 2 made you write map and reduce. Analysts already think `SELECT … WHERE … GROUP BY`. Hive is that SQL layer over files. Pig is a script of steps (load, filter, group, store) for the same files. Both compile down to a cluster engine (MapReduce historically, Tez or Spark in many Hive deployments). Neither one is the engine.

## 2. Schema-on-read (Lab 1)

The bytes `2024-03-15|North|450.00` become `(dt, region, amount=450)` under a pipe SerDe. A comma SerDe sees one field and fails. The file did not change. The table definition and the SerDe did.

Schema-on-read is not "no schema". The metastore still stores column names, types, location, format, and partitions. The check happens at read time, not at insert time. That is why a lake can land messy files quickly, and why a wrong SerDe returns nonsense instead of a rejected insert.

| | Schema-on-write (RDBMS) | Schema-on-read (Hive) |
| --- | --- | --- |
| When | Before the row is stored | When the query runs |
| Write | Slower, validated | Store the file as it arrived |
| Read | Cheaper | Parse and apply the declaration |
| Bad data | Rejected on insert | Visible only when someone queries |

## 3. Metastore, managed, external (Lab 2)

The metastore (Derby for a toy, MySQL or PostgreSQL in production) is the catalog: database, table, columns, partition values, storage format, SerDe, statistics. HiveServer2 is the multi-user door (Beeline, JDBC). The driver parses, checks names against the metastore, optimises, and hands a plan to the engine.

**Managed** table: Hive owns the directory. `DROP` deletes the files.
**External** table: `LOCATION` points at someone else's directory. `DROP` deletes the catalog row and leaves the files.

Lab 2: after both drops, the managed directory was gone and the landing directory was still there. Query speed does not change with this choice. Ownership does.

## 4. Partitions, buckets, formats (Labs 3 and 5)

Partitioning is a directory per value: `dt=2024-03/`. A filter on `dt` skips the other directories. Our year has 12 month partitions and 1,014 rows. `dt` in March reads **74 rows** and leaves **940** unread.

Do not wrap the partition column in a function (`CAST(dt AS …)`). The value may still be right, and the planner can lose the directory prune.

Bucketing is different: a hash into a fixed number of files, not a directory per value. It helps sampling and bucket-to-bucket joins. A table can be partitioned and bucketed. Too many partitions (high cardinality) bloats the metastore.

| Format | Layout | Use |
| --- | --- | --- |
| Text, JSON | Rows, human-readable | Landing zone |
| Avro | Rows, schema in the file | Streams and ETL, when you read the whole record |
| Parquet, ORC | Columns, with stats | Analytical scans |

Lab 5, text bytes only: scanning every column is 32,967 bytes; Region + Total Revenue is 8,159. A columnar reader can skip the other 24,808. ORC is the usual Hive-native choice. Parquet travels better across Spark and Trino. Gzip on one huge file is not splittable, so one task can get stuck with the whole file. Snappy-style block compression can be split.

## 5. HiveQL on our sales (Lab 4)

`amount` is Total Revenue. `dt` is Order Date. `product` joins to the catalog name.

- North, March, amount > 5000: two Laptop rows, 6,000 each (sale ids 1150 and 1201).
- `HAVING SUM(amount) > 400000`: North 530,150 (297), South 408,080 (278), East 400,580 (224). West is under the cut.
- Category revenue: Computers **1,462,000**, Displays **200,400**, Accessories **24,060**.
- Left join where the product is missing: **0** orphan sales. `= NULL` would not have found them. Use `IS NULL`.
- A subquery that sums product revenue, then sums by region, matches the Day 1 region totals, including West 347,650.
- View `march_north` stores the query, not a second copy of the files. It has 28 rows. Reading it runs the query again.

`WHERE` filters rows before grouping. `HAVING` filters groups after. `ORDER BY` is a global sort, so do it after the data is small. `COUNT(*)` counts rows. `COUNT(col)` skips nulls. Null join keys never match, including other nulls.

## 6. Pig (Labs 6 and 7)

Pig Latin names each relation:

```
sales = LOAD ...
enriched = JOIN sales BY product, products BY name
by_cat = GROUP enriched BY category
rev = FOREACH by_cat GENERATE group, SUM(amount)
top = ORDER rev BY revenue DESC
```

On our file: LOAD 1,014 → JOIN 1,014 → 3 category bags → the same three revenues as Hive → ORDER DESC. `SPLIT` sent all 1,014 rows to clean and 0 to quarantine, because every amount is positive.

Complex types: a tuple is one row, a bag is the group (`{(...), (...)}`), a map is key-value attributes. `GROUP` makes the bag explicit, which is why Pig looks longer than SQL and why a multi-step clean is easier to read as a script.

UDFs exist in both. Prefer a built-in. A custom function must be shipped to the workers, and it is opaque to the optimiser.

## 7. Which one to pick

| | Hive | Pig |
| --- | --- | --- |
| Style | Declarative SQL | Step-by-step dataflow |
| Who | Analysts, BI, JDBC tools | ETL scripts |
| Schema | Metastore | Loader and `AS (...)` in the script |
| Best job | Reports, shared tables | Branching cleans, nested data |

Lab 7 prints the same three category totals from both. Same files, same cluster cost. The choice is how the team writes the job. A monthly sales report goes to Hive. A pipeline that flattens messy JSON, splits a quarantine path, and writes Parquet can go to Pig. Day 4 (Spark) is the next layer, not a third copy of this argument.

## 8. How to run

```text
cd courses/MSCIT9127-ml-big-data-analytics/assignments/mit91205-day3
python lab1_schema_on_read.py
python lab4_hiveql.py
python lab6_pig.py
python lab7_compare.py
```

## 9. Review prompts

1. Schema-on-read versus schema-on-write, and what you give up.
2. What fails first if the metastore database is down?
3. Managed versus external, in one sentence about `DROP`.
4. One query that needs partitioning, and one that needs bucketing.
5. A workload for row layout (Avro) and one for columnar (Parquet/ORC).
6. Hive versus Pig: abstraction, schema, typical author.
7. UDF, UDAF, UDTF: one row, one group, or one-to-many.
8. What a SerDe adds that the column list does not.
9. Why Hive is the wrong tool for a one-second dashboard.
10. Strange nulls in one column: look at the SerDe and the file bytes before you blame the `SELECT`.

## 10. Reading

| Source | Why it is on this day |
| --- | --- |
| Thusoo et al. (2009), *Hive: A Warehousing Solution Over a Map-Reduce Framework*, VLDB | Hive as a SQL layer, not a database. |
| Olston et al. (2008), *Pig Latin*, SIGMOD | Dataflow scripts instead of raw MapReduce. |
| Thusoo et al. (2010), *Hive — A Petabyte Scale Data Warehouse*, ICDE | The warehouse story at scale. |
| White (2015), *Hadoop: The Definitive Guide* | HDFS, MapReduce, Hive, Pig in one book. |
