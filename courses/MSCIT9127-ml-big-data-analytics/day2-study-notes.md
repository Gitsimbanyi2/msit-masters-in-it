# MIT 91205 / MSCIT9127 — Day 2 study notes

**Lecturer:** Dr. Bugingo Emmanuel
**Title:** Hadoop Distributed Storage and Batch Processing with MapReduce
**Practical:** `assignments/mit91205-day2/`
**Dataset:** the Day 1 file, `sample-sales.csv` (41,151 bytes, 1,014 orders)

These notes are in my own words, from the Day 2 lecture plus the labs. They are not a copy of the slides. There is no Hadoop cluster on this machine. The labs use a 4 KB block so the small CSV still splits. A real HDFS block is 128 MB or 256 MB.

## 1. What this day is for

Day 1 named the ideas: partitioning, replication, master-worker, CAP. Day 2 is those ideas as Hadoop:

1. **HDFS** stores the bytes.
2. **YARN** hands out CPU and memory.
3. **MapReduce** is the batch program: split, map, shuffle, reduce.

Hive (Day 3) sits on top of this. It does not replace it.

## 2. HDFS (Labs 1–3)

The NameNode stores the directory tree and the map `file → blocks → DataNodes`. It does not store the file. DataNodes store blocks and send heartbeats and block reports.

Our file, block size 4,096 bytes:

| Fact | Lab result |
| --- | --- |
| Blocks | 11 (`ceil(41151 / 4096)`). Last block is 191 bytes, not a full block. |
| Replication | 3 |
| Raw storage | 123,453 bytes, about 3× the file |
| Placement | Replica 1 on one rack, replica 2 on the other rack, replica 3 beside replica 2 |

Example: `blk_0000` → `dn1` (rackA), `dn3` (rackB), `dn4` (rackB). Losing a whole rack must not wipe every copy. That is why replica 2 leaves the first rack.

**Read:** ask the NameNode once, then pull bytes from the nearest DataNode. **Write:** the NameNode picks the three nodes; the client pipelines `client → dn1 → dn3 → dn4`, and acks come back the other way. Reassembling the 11 blocks matched the original file.

**Failure:** `dn1` stops heartbeating. 9 of 11 blocks lose one replica. The NameNode copies each of those onto a live node that does not already hold it. The file is still readable. Replication does not save you from `hdfs dfs -rm`, a bad job, or all three copies corrupting together.

**Small files:** 11 blocks for 41 KB is already silly. Millions of 10 KB files would fill NameNode memory with metadata. HDFS wants large, sequential, write-once files.

**HA:** a standby NameNode follows the edit log through JournalNodes and can take over. Federation is several NameNodes, each owning a slice of the namespace.

## 3. YARN is not HDFS

| | HDFS | YARN | MapReduce |
| --- | --- | --- | --- |
| Job | Disk | CPU and memory | The batch program |
| Who | NameNode, DataNodes | ResourceManager, NodeManagers, ApplicationMaster | MRAppMaster, mappers, reducers |
| Unit | Block | Container (memory + vCores) | Task |
| Survives the job? | Yes | No | No |

A container is a bundle such as 2 GB and 1 vCore. The ResourceManager does not run the tasks. It starts one ApplicationMaster per job. That AM asks for more containers and tells NodeManagers what to launch. MapReduce's AM is the MRAppMaster. Spark has a different one. That split is why one cluster can run both.

Schedulers when jobs compete: **FIFO** (simple, can starve), **Capacity** (queues with a guaranteed share), **Fair** (split what is free among running apps).

If a NodeManager dies, its containers are lost and the AM asks again. If the AM dies, YARN can restart it. If the ResourceManager dies, a standby RM takes over.

## 4. MapReduce pipeline (Labs 4–7)

```
map:    (k1, v1) → list(k2, v2)
reduce: (k2, list(v2)) → list(k3, v3)
```

Phases: **Split → Map → Shuffle/Sort → Reduce → Output.**

- Input splits usually follow HDFS blocks. One map task per split. Intermediate pairs stay on the mapper's **local disk**, not HDFS.
- Shuffle groups by key and moves those pairs to reducers. This is the expensive part: network, sort, and skew.
- Final output is committed to HDFS.
- A combiner is an optional local reduce. It may run zero times or more than once. It is safe only when the function is commutative and associative. **Sum is safe. Averaging the averages is not** (Lab 4: combined average 50.5 vs true 25.8).

Map tasks want to run on a node that already holds the split (11/11 of our blocks have a local replica). Reduce tasks have no locality. They pull from every mapper. Too few reducers bottleneck; too many make tiny output files.

## 5. The four patterns

**Word Count.** Sentences from the deck:

- `the cat sat on the mat`
- `the dog sat on the log`

Mapper emits `(word, 1)`. Reducer sums. Result: `the=4, sat=2, on=2`, and `cat, mat, dog, log` once each. The deck prints `(the, 3)`. Both sentences contain two "the"s (`on the mat`, `on the log`), so the tokenised total is 4.

**Inverted index.** Key is the term, value is the doc id. Reducer deduplicates. `the → [doc1, doc2]`, `cat → [doc1]`, `dog → [doc2]`. A very common term builds a huge postings list on one reducer.

**Aggregation** on our CSV. Mapper emits `(region, (amount, 1))` so a combiner can add sums and counts, and the reducer can still compute an average.

| Region | Revenue | Orders | Average |
| --- | ---: | ---: | ---: |
| North | 530,150 | 297 | 1,785.02 |
| South | 408,080 | 278 | 1,467.91 |
| East | 400,580 | 224 | 1,788.30 |
| West | 347,650 | 215 | 1,616.98 |

Grand total **1,686,460**, same as Day 1. A constant key `ALL` dumps all 1,014 rows on one reducer. That is skew. Salt a hot key, or pre-aggregate, if one region dominates.

**Joins.** Products are a tiny table (Laptop/Tablet = Computers, Monitor = Displays, Keyboard/Mouse = Accessories).

- **Reduce-side:** tag sales `S` and products `P`, shuffle on product name, join in the reducer. Works when both sides are large. Costs a full shuffle.
- **Map-side:** load products into a hash map in every mapper. No shuffle. Only legal because the product table fits in memory.

Both paths agree: Computers 1,462,000; Displays 200,400; Accessories 24,060.

## 6. Trade-offs worth saying in a CAT

- Move the program to the data. Shipping 100 GB across a 10 Gbps link is already most of a minute before any CPU work.
- Larger blocks: less NameNode memory, fewer map tasks, coarser parallelism. Smaller blocks: the opposite.
- Speculative execution starts a second copy of a straggler and keeps the first finish. It spends extra slots to cut tail time.
- MapReduce is a poor fit for interactive queries and for iterative machine learning (each pass is a new job). That is the opening for Spark on Day 4, and for Hive on Day 3 when the user thinks in SQL.

## 7. How to run

```text
cd courses/MSCIT9127-ml-big-data-analytics/assignments/mit91205-day2
python lab1_blocks.py
python lab4_wordcount.py
python lab6_aggregation.py
python lab7_joins.py
```

## 8. Review prompts

1. What breaks if block locations live only on DataNodes, with no NameNode?
2. State the RF=3 rack rule and why replica 2 changes rack.
3. FIFO vs Capacity vs Fair, in one line each.
4. ResourceManager vs NodeManager vs ApplicationMaster.
5. Why is shuffle usually the slow phase?
6. Map task vs reduce task: input, movement, locality.
7. Give one combiner that is unsafe. (Average of averages.)
8. Which failures does HDFS cover, and which does YARN cover?
9. When is a map-side join the wrong choice?
10. A 1 TB word count has one slow reducer. Two fixes.
11. Ten-thousand 10 KB files exhaust the NameNode. Why, and what would you change?
12. Why is HDFS + MapReduce the wrong tool for a dashboard that must answer in a second?

## 9. Reading

| Paper | Why it is on this day |
| --- | --- |
| Dean & Ghemawat (2004), *MapReduce*, OSDI | The model Hadoop implements. Read this one. |
| Shvachko et al. (2010), *The Hadoop Distributed File System* | NameNode, blocks, replication as deployed. |
| Vavilapalli et al. (2013), *Apache Hadoop YARN*, SoCC | Why compute scheduling left the JobTracker. |
| Ghemawat, Gobioff & Leung (2003), *GFS* | Already on the Day 1 list. HDFS is the descendant. |
