# MIT 91205 Day 2 practical — HDFS and MapReduce on a laptop

These scripts are a **model** of the Day 2 lecture. They do not start a Hadoop cluster. Block size is 4 KB so the Day 1 CSV produces more than one block. A real cluster uses 128 MB or 256 MB.

Dataset: `../mit91205-day1/sample-sales.csv` (1014 orders). Word Count and the inverted index use the two sentences from the lecture slides.

| Script | Lecture idea |
| --- | --- |
| `lab1_blocks.py` | Blocks, RF=3, rack-aware placement |
| `lab2_read_write.py` | NameNode metadata vs DataNode pipeline |
| `lab3_failure.py` | Heartbeat loss and re-replication |
| `lab4_wordcount.py` | Word Count, and why average is an unsafe combiner |
| `lab5_inverted_index.py` | Term to document ids |
| `lab6_aggregation.py` | Sum and average by region, plus a hot key |
| `lab7_joins.py` | Reduce-side join vs map-side join, and locality |

```text
cd courses/MSCIT9127-ml-big-data-analytics/assignments/mit91205-day2
python lab1_blocks.py
python lab4_wordcount.py
python lab6_aggregation.py
python lab7_joins.py
```

No extra packages. Python 3 standard library only.

Study notes: `../../day2-study-notes.md`
