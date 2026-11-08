# Desk 8 — what the five pictures show

**Student:** Prosper Gitsimbanyi
**Module:** MIT 91205 Big Data Analytics, Day 4, Apache Spark

Use these notes while the pictures are on your own screen. Spark is the engine in every picture. It reads data that already lives somewhere else, computes, and writes a result.

## 1. Financial report dashboard

This is the screen a manager sees after the heavy job has finished. The filters are financial year, category, region, segment, product, and customer. The panels are an income-statement table, revenue by year, revenue by month, the top 10 customers, and the top 10 products.

Spark does not draw this page. Spark SQL groups the raw transactions once and writes a small summary table. The dashboard reads that table. That is Scenario 6: large-scale aggregation and reporting. The date and category filters work quickly because the summary is small and the source was partitioned.

What to say: "The bank does not ask the dashboard to scan every transaction. Spark already calculated the totals. This page only reads the result."

## 2. Batch and streaming

The left side is batch. A clock marks a scheduled run. Files in S3, or rows in a database, go through Spark into a warehouse. The job is judged by how much history it can finish: daily or monthly totals.

The right side is streaming. Events arrive through Kafka. Spark Structured Streaming writes them to a sink. The job is judged by delay: flag a live transaction now.

The caption on the picture is the rule. Batch optimises throughput. Streaming optimises latency. Day 4 teaches the left side. Kafka, Structured Streaming, and Flink are Day 5. The DataFrame can look similar. The execution does not.

## 3. Spark architecture

Read this picture from the top.

- The Spark driver holds the DAG scheduler and the task scheduler. It builds the plan and sends work out. If the driver dies, the application dies.
- The cluster manager is YARN or Kubernetes. It assigns machines and is monitored. It does not store the business data.
- Executors run the tasks. The RDD, Dataset, and DataFrame APIs are how the code describes those tasks.
- The web UI is where you see stages, shuffle, and a task that is much slower than the others.
- Along the bottom are the systems that actually hold data: HDFS, S3, JDBC, Cassandra, and Kafka. Spark reads them and writes back.

What to say: "Spark sits in the middle. Storage sits underneath."

## 4. Presenting a dashboard in a room

The audience is looking at charts, gauges, and a map on one screen. The calculation is already done. This is the reporting pattern in real life: one scheduled Spark job, then a small result that a person can explain. Nobody in that room is scanning the raw terabytes.

## 5. Spark SQL poster

The poster is branding, not a diagram to memorise. The words that matter are Apache Spark, Spark SQL, distributed processing, and structured data. Spark SQL is the table language on the same engine as DataFrames. One optimiser plans both. The small print on the poster is decorative and is not part of the lecture.

## Review answers these pictures support

1. Spark's purpose is distributed computation on data that is already stored.
2. Spark does not permanently store the data. HDFS, S3, a database, or Kafka does.
3. Batch reads a stored history. Streaming reads events as they arrive.
4. GraphX is for nodes and edges. It is not what draws the financial dashboard.
5. MLlib is the machine-learning library.
6. A dashboard stays fast because it reads an aggregate, not the raw table.
7. Three limits: memory for a cache, the cost of a shuffle, and skew when one key is huge.
