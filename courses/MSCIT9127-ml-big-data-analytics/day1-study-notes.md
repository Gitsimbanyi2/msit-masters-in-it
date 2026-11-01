# MIT 91205 / MSCIT9127 — Day 1 study notes

**Date:** 1 November 2026  
**Lecturer:** Dr. Bugingo Emmanuel  
**Title:** Introduction to Big Data Analytics and Distributed Systems Foundations  
**Practical:** From raw data to insight (`assignments/mit91205-day1/`)

These notes are in my own words, from the Day 1 lecture + the completed lab. They are not a copy of the slides.

## 1. What this day is for

Day 1 is the foundation for the rest of the module:

1. What Big Data *is* (5 V's, and why a laptop CSV is not Big Data).
2. What analytics *does* (descriptive → diagnostic → predictive).
3. How distributed storage *survives* (partitioning + replication).
4. Why distributed databases *trade off* (CAP / PACELC).
5. The analytics lifecycle (question → data → clean → analyse → chart → action).

Day 2 moves the same ideas onto Hadoop HDFS and MapReduce.

## 2. The 5 V's (Lab 1)

Our file: **1014 rows × 7 columns**, about 40 KB, zero missing values.

| V | Question | Our dataset |
|---|----------|-------------|
| Volume | How much data? | Tiny. Fails the scale test. |
| Velocity | How fast does it arrive? | 12 months of 2024, ~68–101 orders/month, but it is a static CSV, not a live stream. |
| Variety | Mixed types? | Yes: integers, dates, text (Region/Product), money. |
| Veracity | Can we trust it? | 0 missing cells. Real data is never this clean. |
| Value | What decision can it support? | Which region and product to grow? Answered in Lab 7: North + Laptop. |

**Is this Big Data?** No. By the Day 1 definition it does not exceed scale, complexity, or operational constraint. Chen, Mao & Liu (2014) would not call 40 KB "big". The lab is a *model* of Big Data ideas on a laptop.

If the same schema had 100 million rows, **Volume** (and time-to-query) would become the problem. Variety and the business question would stay the same.

## 3. Three kinds of analytics

### Descriptive — what happened? (Lab 2)

- Total revenue: **$1,686,460**
- Regions: North $530,150 → South $408,080 → East $400,580 → West $347,650
- Products: Laptop $1,020,000 → Tablet $442,000 → Monitor $200,400 → Keyboard $17,460 → Mouse $6,600

Lecture code (Jupyter):

```python
top_products = (df.groupby("Product")["Total Revenue"]
                  .sum()
                  .sort_values(ascending=False)
                  .head(5))
```

Read it as a pipeline: split by product → keep money → add → sort largest first → keep top 5.

Descriptive analytics **cannot** say why North wins.

### Diagnostic — why did it happen? (Lab 3)

Pivot: Region × Product.

- North / East / West: **Laptop** dominates (63–71% of regional revenue).
- **South is the outlier: Tablet** is the top product (Laptop only 39.1%).

North is first because it sells the most Laptops, and a Laptop is $1,200. Diagnostic work *surfaces the pattern*. It still cannot say why South prefers Tablets (need surveys, stock, marketing).

### Predictive — what might happen next? (Lab 4)

Straight line through 12 monthly totals:

`Revenue = 4,492.59 × month + 115,829.10`

Forecasts: month 12 ~$169,740; month 13 ~$174,233; month 14 ~$178,725.

The actual dots **scatter** around the red trend (early dip, then noisy growth). So the forecast is a rough slope, not a trustworthy prediction. A promotion, stock-out, or competitor can break it. Extra columns that would help: promotions, holidays, cost/profit.

## 4. Partitioning, replication, fault tolerance (Lab 5)

This is HDFS in miniature. We cannot run a cluster on a laptop, so we simulate:

| Idea | What we did | Production equivalent |
|------|-------------|------------------------|
| Partition | Split by Region: East 224, North 297, South 278, West 215 | HDFS 128 MB blocks |
| Replication factor 3 | Three copies of each partition | Default HDFS RF=3 on different machines |
| Node failure | Deleted North's primary copy | Disk / DataNode death |
| Recovery | Read 297 North rows from a surviving replica | Client reads another replica |

If `REPLICATION_FACTOR = 1`, North is gone after the failure. Partitioning gives scale; replication gives survival. You need both.

**Paper to read in full:** Ghemawat, Gobioff & Leung (2003), *The Google File System* (SOSP) — the design HDFS copies. <https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf>

## 5. CAP theorem (Lab 6)

During a **network partition** you cannot keep both:

- **C**onsistency — every node shows the same value
- **A**vailability — every request gets an answer

**P**artition tolerance is assumed on a real network.

| Scenario | Choice | Behaviour | Examples |
|----------|--------|-----------|----------|
| A | Healthy network | Both nodes show 200 | Normal operation |
| B | **CP** | Refuse the unreachable / stale node | ATM, HBase, MongoDB majority |
| C | **AP** | Serve stale 200 so the app stays up | Social likes, Cassandra, Dynamo |

- **ATM / bank balance → CP.** Wrong balance is worse than a refused withdrawal.
- **Likes counter → AP.** A slightly stale count is acceptable; the feed must stay up.

**PACELC (Abadi 2012):** CAP only talks about partitions. The **E** is *Else*: even with a healthy network you still trade **latency vs consistency**.

**Paper to read in full:** Gilbert & Lynch (2002), *Brewer's Conjecture...* — the proof, ~8 pages. <https://lpd.epfl.ch/sgilbert/pubs/BrewersConjecture-SigAct.pdf>

Skim: Abadi (2012) PACELC. <https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf>

## 6. Analytics lifecycle (Lab 7)

This is the mini-project template.

| Stage | What we did |
|-------|-------------|
| 1 Business understanding | Which region should we expand, and with which product? |
| 2 Data acquisition | `pd.read_csv("sample-sales.csv")` — 1014 orders, 2024-01-01 to 2024-12-28 |
| 3 Data preparation | `dropna()` — still 1014 rows (already clean) |
| 4 Analysis | SQL in DuckDB (stand-in for Hive / Spark SQL) |
| 5 Visualization | `top_combinations.png` |
| 6 Action | Focus on **North with Laptop** ($355,200) |

If a manager disagrees, go back to stage 1 (maybe they care about profit or South's Tablet growth, not raw revenue).

SQL extra column required by the lab:

```sql
SUM("Total Revenue") / SUM("Units Sold") AS revenue_per_unit
```

## 7. How to run the lab again

```text
cd courses/MSCIT9127-ml-big-data-analytics/assignments/mit91205-day1
python -m venv day1env
day1env\Scripts\activate
python -m pip install -r requirements.txt
python generate_dataset.py
python lab1.py
```

Or open `Day One.ipynb` and run cells top to bottom (Shift+Enter). The first code cell must run first, or later cells fail with `NameError: df is not defined`.

First five CSV rows can differ from the printed lab manual if NumPy 2.x is installed (RNG changed). Shape **(1014, 7)** is the check that matters.

## 8. Reading tracker (report Section 8)

Paper | Title (short) | Read? | One-sentence takeaway
------|---------------|-------|----------------------
#6 | Gilbert & Lynch 2002 — CAP proof | ☐ full | Formal: during a partition you cannot have both C and A.
#2 | GFS 2003 | ☐ full | Large blocks, 3 replicas, a master that tracks locations — the HDFS ancestor.
#7 | Abadi 2012 — PACELC | ☐ skim | Even without a partition, systems still trade latency vs consistency.

Minimum for the Day 1 report: **#6 and #2 in full**, skim #7. Assigned before Day 2: Dean & Ghemawat (2004) MapReduce. <https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf>
