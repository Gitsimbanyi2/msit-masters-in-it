# MSCIT9128 — Advanced Distributed Systems

## Purpose

Design and reason about systems that run on many machines and still look like one service: transparency, middleware, scaling, failure, and cloud.

This is the module with the October 2026 CAT (AgriMart-style case). Study notes and a revision sheet are in this folder.

## Topic map

- Definition, goals, challenges, false assumptions
- Transparency, openness, scalability (size / geography / admin)
- Replication and cache consistency
- NOS, DOS, middleware services
- Client–server vs peer-to-peer
- Multiprocessor / multicomputer, SMP vs ASMP
- Cloud models, bursting, ERP as a DS
- 3-tier, SOA, proxy, hierarchy, POSDCORB as management view
- Failure, consistency, security of a distributed estate

## Files

- `notes.md` — weekly log
- `study-notes.md` — condensed revision in original wording
- `cat-revision.md` — timed CAT checklist (Oct 2026)
- `cat-model-answers.md` — full model answers (AgriMart, MedConnect, SwiftTrade, BrightStitch, EduNet)
- `lecture-map.md` — which local PPT/PDF is which chapter (files stay off GitHub)
- `chapter-02-systems-integration.md` — silos, POSDCORB, ERP as integrator
- `chapter-03-enterprise-architecture-erp.md` — ESA, modules, 3-tier, SOA, cloud ERP
- `chapter-04-cloud-computing.md` — NIST, bursting, SLA, lock-in
- `data-warehouse-and-bi.md` — DW four properties, OLTP vs OLAP, BI
- `MSCIT9128-CAT-diagrams.pptx` — student revision PowerPoint (all CAT diagrams)
- `diagrams/cat-all-diagrams.jpg` — one-sheet drawing pack
- `assignments/CAT_Distributed_Systems_ERP_Cloud_FULL_ANSWERS.docx` — your Word file
- `assignments/lectures/` — lecturer PDF/PPT and the Adobe Scan CAT paper on this PC only (gitignored; Pearson / exam paper not published)

## Link to work

Inventory and patching of PHP runtimes across several sites is a distributed-systems operations problem (heterogeneous OS, independent failure, more than one administrator). See also MSCIT9126.
