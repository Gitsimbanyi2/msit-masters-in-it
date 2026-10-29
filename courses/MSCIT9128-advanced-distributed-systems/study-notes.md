# MSCIT9128 — Advanced Distributed Systems (study notes)

Student notes in original wording for CAT and exam revision. Lecturer: Assoc. Prof. James Rwigema (2024–2025 materials). These pages are a study aid, not a copy of the slide deck.

## 1. What a distributed system is

A distributed system is a set of independent computers that cooperate so users see **one** coherent service. Machines talk only by **messages** on a network. If one PC crashing still lets you finish the work, you are already using distribution.

Two halves:

1. **Hardware** — autonomous computers (branch tills, warehouse, head office).
2. **Software** — middleware and applications that hide the separate machines.

A parallel computer is a special case of a distributed system (tight coupling). A network of branch-office computers is the usual business case.

## 2. Why we distribute

- More total computing power than one mainframe.
- Incremental growth (add a branch server).
- Fault isolation (one shop down need not stop forty).
- Data and users are already geographically spread.

Costs: many failure modes, many administrators, inconsistent copies, security of a larger surface.

## 3. Goals (and why full transparency fails)

**Transparency** — hide that processes and data live on many machines. Useful, but never complete: you cannot tell a slow node from a dead one; you cannot be sure a server finished work before it crashed; keeping every cache identical to the master **on every write** kills scale.

**Openness** — services follow published syntax and semantics so other systems can interoperate (interfaces, portability). Heterogeneous OS and languages are the normal case, not an exception.

**Scalability** has three axes:

- Size (users / processes)
- Geography (distance)
- Administration (number of domains)

Techniques: hide latency (work on the client), partition data, replicate, cache. Multiple copies **diverge**. Global locks on every update do not scale. The application must define how stale a copy may be (TTL, version, invalidate-on-write).

False assumptions to drop: the network is reliable, secure, homogeneous; latency is zero; there is one administrator.

## 4. NOS, DOS, middleware

| Layer | Idea | AgriMart-style mapping |
|-------|------|------------------------|
| Network OS | Each host has its own OS + networking; ftp/www tied to nodes; share files | Mixed Windows branches + Linux HO today |
| Distributed OS | OS on each host knows the others; rare in production (Amoeba-class) | Not realistic on mixed vendor kit |
| Middleware | Sits on existing OS; offers distributed services without replacing the OS | The layer to add: naming, RPC/RMI, queues, transactions, auth |

Middleware service groups: **communication** (RPC, RMI, queues, streams, events), **information** (naming, directory, cache, replica), **control** (distributed transactions, code migration), **security** (authn/z, encryption, audit).

## 5. Client–server vs peer-to-peer

**Client–server:** clients call servers for shared data. Servers may be clients of other servers. Clear backup and control; the server can bottleneck.

**Peer-to-peer:** peers are equals; no central server. Scales by adding peers; official “one price list” is harder because copies drift.

## 6. Multiprocessor vs multicomputer (notes p.26–28)

**Multiprocessor:** two or more CPUs share memory and peripherals in one computer.

- SMP — all CPUs equal.
- ASMP — one master CPU runs the OS.

**Shared memory vs message passing; bus vs switch** give four pictures:

1. Shared memory + bus
2. Private memory + bus (multicomputer)
3. Shared memory + switch
4. Private memory + switch (multicomputer)

Heterogeneity: different OS, instruction sets, and data representations must be hidden by middleware (marshalling).

## 7. Cloud as a distributed system

Cloud is distribution plus **elasticity** (pay for capacity, grow/shrink). Models: IaaS / PaaS / SaaS. Bursting: overflow from private capacity into public cloud under policy. ERP-in-the-cloud is still a distributed system: many tenants, many regions, one logical product.

## 8. Architectural styles you must be able to draw

- Layered (hardware → OS → middleware → application)
- Client–server (2-tier, 3-tier: presentation / logic / data)
- SOA / microservices (services compose; need a registry and versioning)
- Proxy / broker (client talks to a representative, not the real server)
- Hierarchical (regional nodes under a head office)

POSDCORB as a management overlay (planning, organising, staffing, directing, coordinating, reporting, budgeting) — use it when the CAT asks how a **manager** runs a distributed estate, not how a packet moves.

## 9. Failure and consistency (exam gold)

Independent failure is normal. Design for:

- Timeout + retry with idempotent operations
- Replication with an explicit consistency rule
- Partition: decide availability vs consistency (you cannot have both when the network splits)

## 10. Security in a distributed system

More nodes = more credentials, more clocks, more logs. Minimum:

- Authenticate services, not only users
- Encrypt on the wire (TLS)
- Authorise at the service boundary
- One clock source (NTP) so logs can be correlated
- Do not expose admin UIs (phpMyAdmin-class) on database nodes

This module connects directly to **MSCIT9126** (networks and cybersecurity) and to PHP/runtime patching work in a SOC: a vulnerable interpreter on one node is a distributed-system failure as well as a CVE.
