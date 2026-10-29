# Chapter 3 — Enterprise systems architecture and ERP

## Two sides of ESA

- **Functional:** the ERP *modules* (finance, HR, procurement, sales, inventory, production, CRM, BI, employee self-service).
- **System:** the *kit* (servers, database, browsers, intranet/internet).

Vendors (SAP, Oracle/PeopleSoft, Microsoft Dynamics) ship the same business areas under different module names. In a table question, map **procurement** and **accounting** across the three; do not memorise every product SKU.

ERP embeds “best practice” as **business rules**. That is a policy choice, not only a technical one.

## Three-tier (presentation / logic / data)

Staff use a browser (presentation). Business processes run on application servers (logic). One company database holds the record (data).

Benefits: one version of the truth; change the logic without reinstalling every PC. Limits: cost, messy migration from the old inventory package, possible bottleneck if the app or DB is undersized.

## Layered web ERP

Typical stack from the user down: device → interface (HTTPS/SSL session) → application software → database, over intranet and internet. The PC only needs a Java-capable (or modern) browser. The network must be sized and budgeted **before** go-live; partners may connect for orders and stock.

## Server-centric vs client-centric

| | Server-centric (thin client) | Client-centric (thick client) |
|--|------------------------------|-------------------------------|
| Where work runs | Mostly on the server | Mostly on the laptop |
| Install | No heavy client | Client software on every PC |
| Security | Access stays on the server | Weaker if laptops roam |
| Speed on a good LAN | Can feel slower | Often snappier |
| Field sales / slow link | Prefer this; keep pages small | Fights the IT manager’s lockdown |

CAT default for BrightStitch field laptops: **server-centric**.

## SOA (service-oriented architecture)

A **consumer** calls a **service** that a **provider** implements. The **contract** is the public description (operations, message formats, QoS, version) — not the provider’s internal language.

Use SOA to **wrap** the old inventory system during migration, not as an excuse to skip ERP. Drawbacks: expensive to define and secure; too many small calls can be slow.

## Cloud ERP (lease vs buy)

Subscription instead of licences and a private server room. Accessed from anywhere. Drawbacks: data location, IP, and vendor dependence. Standard modules (accounting, HR, purchasing) are good candidates to lease; unique design/IP often stays under the firm’s control with export clauses.
