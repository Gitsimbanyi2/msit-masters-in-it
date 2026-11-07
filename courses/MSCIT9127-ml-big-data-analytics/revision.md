# MSCIT9127 revision checklist

## Day 1 (MIT 91205)

- [ ] I can say why our 1014-row CSV is **not** Big Data, using the 5 V's
- [ ] I can tell descriptive / diagnostic / predictive apart with the sales example
- [ ] I can explain `groupby("Product")["Total Revenue"].sum().sort_values(ascending=False).head(5)`
- [ ] I can redraw partitioning + RF=3 + node failure (Lab 5)
- [ ] ATM = CP, social likes = AP, in two sentences each
- [ ] I can state PACELC: even without a partition, latency vs consistency
- [ ] I can list the six lifecycle stages from Lab 7
- [ ] Gilbert & Lynch (2002) and GFS (2003) read; MapReduce paper before Day 2

## Day 2 (MIT 91205)

- [ ] I can say NameNode = metadata, DataNodes = blocks, default RF = 3 across racks
- [ ] I can walk a write pipeline and a read that retries the next replica
- [ ] I can separate HDFS, YARN, and MapReduce in one table
- [ ] I can write map and reduce for word count, and say why average is an unsafe combiner
- [ ] I can choose reduce-side join vs map-side join
- [ ] Dean & Ghemawat (2004) read

## Day 3 (MIT 91205)

- [ ] I can explain schema-on-read with the pipe-delimited line
- [ ] I can say what DROP does to a managed table and to an external table
- [ ] I can show partition pruning on `dt=2024-03` (74 rows, not 1,014)
- [ ] I can write the category-revenue join in HiveQL and as a Pig dataflow
- [ ] I can pick Hive or Pig for a report vs a multi-step clean

## Module

- [ ] I can explain every item on the topic map in one paragraph
- [ ] I have one diagram I can redraw under exam timing
- [ ] I have one Rwanda / work example per big idea
- [ ] Past CAT questions attempted under time
- [ ] Definitions are in my own words (not copied slides)
