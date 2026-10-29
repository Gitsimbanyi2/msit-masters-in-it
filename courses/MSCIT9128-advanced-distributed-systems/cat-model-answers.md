# CAT model answers — Distributed Systems, ERP, Organisation and Cloud

Source: `CAT_Distributed_Systems_ERP_Cloud_FULL_ANSWERS.docx` (UoK, Oct 2026).  
Section A is compulsory. Section B: any two of Questions 2–5; all four are answered here for revision.

## Section A — compulsory (50 marks)

### Question 1 — AgriMart (50 marks)

#### a) Definition, hardware and software, advantages, challenges (10)

A distributed system is a collection of independent computers, linked by a network, that appear to users as a single coherent system.

- **Hardware:** several machines (AgriMart branches, warehouses, head office) with processors, storage and network links.
- **Software:** middleware and applications that hide the separate machines so staff see one sales, stock and customer system.

**Advantages over a centralised mainframe**

- **Scalability:** add branch servers without buying one huge machine.
- **Fault isolation:** a fault at one branch need not stop all 40 shops (unlike a six-hour mainframe outage).
- **Local performance:** tills and pricing run on the branch server.
- **Incremental cost:** capacity is added where it is needed.

**Challenges**

- Heterogeneity (Linux HO, Windows branches, vendor warehouse OS, scanners).
- Transparency (copies of prices and customers can drift).
- Failure and network partitions.
- Security and consistency.
- Openness (different OS and applications must work through a common layer).

#### b) Transparency, openness, scalability; replication and caching (10)

- **Transparency:** hide distribution so the system looks like one machine (access, location, concurrency, replication, failure, performance). A cashier should not need to know whether stock is local or at the warehouse. The pilot failed this: two branches charged different prices.
- **Openness:** published interfaces so new machines and applications can join. AgriMart’s mixed OS must talk through a common layer.
- **Scalability:** size (users/branches), geography (internet-spread sites), administration (many OS teams). Techniques: partition work, replicate, cache, hide communication behind middleware.
- **Replication/caching problem:** copies become inconsistent. Design needs update propagation, versioning or invalidation, and a single source of truth for prices and loyalty.

#### c) NOS, DOS, middleware; client–server vs peer-to-peer (10)

- **NOS:** each machine keeps its own OS; users explicitly use remote resources. AgriMart today.
- **DOS:** one OS image across machines. Rare on mixed Linux/Windows/vendor kit.
- **Middleware:** layer above the local OS (naming, communication, transactions, security) so applications appear as one system without replacing every OS.

Middleware service groups: communication (RPC/RMI, queues); naming/directory; coordination/transactions; data/replication; security; platform/web.

- **Client–server:** tills request warehouse/HO servers. Clear control; server can bottleneck.
- **Peer-to-peer:** equals share stock. Scales by adding peers; “official price list” is harder.

#### d) Multiprocessor; SMP vs ASMP; shared-memory vs message-passing (10)

- **Multiprocessor:** one computer, two or more CPUs, shared memory.
- **Multicomputer:** several computers, each with its own memory, linked by a network.
- **SMP:** every CPU can run the OS and user work.
- **ASMP:** one master CPU runs the OS; others take assigned tasks. Master is a bottleneck.
- **Shared memory:** locks; fast in one box; does not extend across AgriMart’s internet.
- **Message passing:** the right model for branches, warehouses and HO.
- **Heterogeneity:** node (CPU/OS/language) and network (speed/reliability).

#### e) Four architectural questions; communication paradigms; caching (10)

Coulouris-style questions: (1) which entities communicate; (2) how they communicate; (3) roles (client–server, P2P, mobile code); (4) where state lives (replication, caching).

Paradigms: IPC (sockets); remote invocation (RPC/RMI); indirect (queues, pub/sub).

**Caching:** copy data closer to the till. Faster, less HO load, survives a slow link. Cost: stale copies. Needs TTL, invalidate-on-update, or versions, plus a policy when the network fails.

---

## Section B — any two (50 marks)

### Question 2 — MedConnect Health (25)

**a) Cloud model; NIST; two essential characteristics (7)**

Draw: front end (clinics, staff, mobile app) → Internet → back end (provider DC: VMs, storage, platform, email, billing).

NIST: on-demand network access to a shared pool of configurable resources that can be rapidly provisioned and released.

Any two of: on-demand self-service; broad network access; resource pooling; rapid elasticity; measured service.

**b) Who manages which layer; public / private / hybrid (8)**

| Layer | On-premise | IaaS | PaaS | SaaS |
|-------|------------|------|------|------|
| Data | Customer | Customer | Customer | Provider |
| Applications | Customer | Customer | Customer | Provider |
| Runtime | Customer | Customer | Provider | Provider |
| Middleware | Customer | Customer | Provider | Provider |
| OS | Customer | Customer | Provider | Provider |
| Virtualization | Customer | Provider | Provider | Provider |
| Servers / storage / networking | Customer | Provider | Provider | Provider |

Recommend **hybrid**: patient records and proprietary billing stay under MedConnect control; public IaaS for claims peaks; public PaaS/SaaS for email and the app platform.

**c) Bursting; SLA; migration; lock-in (10)**

Keep a private base for normal months; overflow Oct–Dec to public cloud; release in January. Pay for peak only. Developers get a test server in hours.

Pilot SLA 99.5%; actual 97.8% sits in 95.0% to below 99.0% → **30%** credit of that month’s charge.

SLA states availability, support and remedies. It does **not** by itself keep patient data private.

Do not lift-and-shift billing in one cut-over. Wrap, phase, keep an exit copy. Lock-in: “works only with the provider’s tools” — reduce with open formats, containers, data-export clauses.

### Question 3 — SwiftTrade Distributors (25)

**a) POSDCORB; hierarchy; matrix vs silos (7)**

POSDCORB: Planning, Organising, Staffing, Directing, Coordinating, Reporting, Budgeting.

Hierarchy: Board/CEO → middle managers → supervisors → sales, procurement, warehouse, accounting, HR.

Silos: sales cannot see stock; accounting re-types invoices. A cross-functional matrix plus later ERP (one database) breaks that.

**b) Three-tier ERP (8)**

Presentation (browser) → application/business logic → data/database.

Benefits: one set of figures; easier change. Limitation: cost, migration, possible bottleneck.

**c) SOA (10)**

Consumer → Service ← Provider. Contract = operations, formats, QoS, version.

Benefits: keep old inventory running as a service; reuse; replace behind the contract. Drawbacks: cost to define/secure; chatty calls.

Recommend SOA as **integration**, ERP as system of record. No big-bang throw-away of inventory.

### Question 4 — BrightStitch Garments (25)

**a) Enterprise architecture; ERP modules (7)**

Functional side = modules (sales, production, purchasing, inventory, finance, HR, BI). System side = hardware, software, network.

Procurement/accounting examples: SAP Purchasing + FI; Oracle Procurement + Financial Management; Dynamics SCM + Financial Management.

**b) Layered architecture; server-centric vs client-centric (8)**

User/device → interface (HTTPS) → application → database, over intranet/internet.

Field sales: **server-centric** thin browser. Matches security/install policy. Keep pages small; short offline notes then sync. Do not put a full ERP on the laptop.

**c) Cloud ERP (10)**

Users → Internet → provider (ERP, servers, storage, backups); monthly subscription.

Benefits: lower up-front cost; access from the field; provider patches. Drawbacks: third-party control of designs/customers; vendor dependence.

Lease standard modules in the cloud; keep unique design/IP under BrightStitch control with location/export/IP clauses.

### Question 5 — EduNet University (25)

**a) Layered DS; middleware (7)**

Each machine: hardware → local OS → middleware → applications. Users see one university.

Middleware sits between apps and mixed OS (Linux registry, Windows catalogue, finance package). Categories: communication (RPC/queue); naming/directory (also SSO or transactions).

**b) Four drawings (8)**

Two features: shared vs private memory; bus vs switch.

| Drawing | Memory | Interconnect | Class |
|---------|--------|--------------|-------|
| Top left | Shared | Bus | Multiprocessor |
| Top right | Private | Bus | Multicomputer |
| Bottom left | Shared | Switch | Multiprocessor |
| Bottom right | Private | Switch | Multicomputer |

Campus of different machines = **message-passing multicomputer**, not one shared-memory box.

**c) Client–server vs P2P; proxy cache (10)**

Learning platform: **client–server with campus proxy caches** (one official exam copy, authentication, less inter-campus traffic). Expire/refresh cached quizzes. P2P only as an extra path for large research datasets, not for assessed work.

---

## How to sit Section B

- Q2 + Q4 if stronger on cloud and ERP.
- Q3 + Q5 if stronger on organisation, SOA and hardware.
- Q2 + Q5 for one cloud case and one university/distributed case.

Always draw the diagrams, label every box, and tie the recommendation to the case (patient data at MedConnect; field laptops at BrightStitch; exam load at EduNet; old inventory at SwiftTrade).
