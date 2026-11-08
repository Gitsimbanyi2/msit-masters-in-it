# MSCIT9127 — Machine Learning and Big Data Analytics

## Purpose

Turn data into models and decisions, with enough statistics and pipeline thinking to defend a result in a CAT or a board paper.

## Topic map

- Data collection, cleaning, feature engineering
- Supervised vs unsupervised vs reinforcement (overview)
- Classification, regression, clustering; train/test split, cross-validation
- Metrics: accuracy, precision, recall, F1, ROC — when each lies
- Big data ideas: volume/velocity/variety; Hadoop/Spark at concept level
- Ethics: bias, privacy, model drift
- Security use-cases: phishing URL models, anomaly detection in logs

## Folder

- `notes.md` — weekly log
- `day1-study-notes.md` — MIT 91205 Day 1 (5 V's, analytics types, CAP, lifecycle)
- `day2-study-notes.md` — HDFS, YARN, MapReduce patterns
- `day3-study-notes.md` — HiveQL, schema-on-read, Pig Latin
- `assignments/mit91205-day1/` — Day 1 lab (notebook, scripts, charts, CSV)
- `assignments/mit91205-day2/` — block placement, word count, joins (no cluster)
- `assignments/mit91205-day3/` — HiveQL in SQLite and a Pig-style dataflow
- `assignments/mit91205-day4/` — Day 4 Desk 8 slides (graph analytics, reporting, streaming boundary)
- `assignments/` — CAT scans and lecturer PDFs stay local (gitignored)
- `revision.md` — last-week checklist

## Exam / CAT tips

- Never report accuracy alone on an imbalanced class
- State the leakage risk if timestamps or IDs leak into features

## Status

Day 1 (1 Nov 2026) done: lecture notes + Labs 1–7 on `sample-sales.csv`.
Day 2 done: HDFS block/replication labs and MapReduce word count, index, aggregation, and joins. Read Dean & Ghemawat (2004).
Day 3 done: schema-on-read, partitions, HiveQL, and Pig on the same sales file.
Day 4 Desk 8: Spark applications in practice, in `assignments/mit91205-day4/desk8-slides.html`.
