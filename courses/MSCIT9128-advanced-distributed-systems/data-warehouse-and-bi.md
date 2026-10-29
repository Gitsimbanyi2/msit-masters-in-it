# Data warehouse and business intelligence

This deck sits beside the DS/ERP/cloud CAT: once the enterprise has one operational system, managers still need a **decision** database.

## Decisions at three levels

- **Operational** — daily, structured, supervisors.
- **Tactical** — medium term, semi-structured, middle managers.
- **Strategic** — long term, unstructured, executives.

A usable decision cycle: see the problem → options → choose → act → **evaluate**. If it failed, start again. Data for that cycle must be timely, consistent, and not pulled from five silos.

## Nearby terms (do not mix them)

| Term | Plain meaning |
|------|----------------|
| BI | Skills, processes and tools that turn data into action for managers |
| Business analytics | Explore the past to support a future choice |
| Big data | Volume/variety/velocity beyond a normal SQL app |
| Data mining | Find patterns (classify, cluster, associate, predict) |
| OLTP | Day-to-day entry (tills, invoices) |
| OLAP | Multi-dimensional analysis: roll-up, drill-down, slice and dice |

## Data warehouse (Inmon-style four words)

A DW is **subject-oriented**, **integrated**, **time-variant**, and **non-volatile**, built to support management decisions.

- Subject-oriented: around customer / product / sales, not around one app.
- Integrated: one coding of “customer” after ETL from many sources.
- Time-variant: history is kept (this week vs last year).
- Non-volatile: you load and query; you do not edit yesterday’s fact like an OLTP row.

Pipeline: sources → ETL → warehouse → OLAP / mining / dashboards → a decision.

## BI in three pieces

1. **Warehouse** — comprehensive, historical, cleaned.
2. **Mining / analytics** — classification, clustering, prediction (not only a filter).
3. **Delivery** — reports, dashboards, ad hoc query, mobile BI.

Benefits you can name: one version of the truth, faster reporting, better tactical choices, time saved. Many benefits are intangible — say so.

## Link back to MSCIT9128

ERP/OLTP is the **system of record**. The warehouse is the **system of insight**. Both are distributed systems: many sources, one coherent view, cache/replica consistency, and access control. Do not run heavy OLAP on the production till database.
