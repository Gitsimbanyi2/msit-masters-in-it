# Chapter 4 — Cloud computing (NIST)

## One-sentence definition (learn this)

On-demand network access to a **shared pool** of configurable resources (networks, servers, storage, applications, services) that can be **provisioned and released quickly**, with little human dealing with the provider (NIST SP 800-145).

Utility picture: plug in like electricity; pay for what you use; hide the data-centre detail.

## Five essential characteristics

1. **On-demand self-service** — you click, no ticket to the vendor’s staff.
2. **Broad network access** — phone, tablet, laptop, clinic PC.
3. **Resource pooling** — multitenancy; you do not see the other tenants.
4. **Rapid elasticity** — grow for the claims peak, shrink in January.
5. **Measured service** — metered, pay-as-you-go.

## Four deployment models

| Model | Who uses it | Strength | Watch |
|-------|-------------|----------|--------|
| Public | Anyone, on the CSP site | Cheap scale | Weaker say on data location |
| Private | One organisation | Control, compliance | Cost, limited scale, needs in-house skill |
| Hybrid | Private + public, still distinct | Fit the workload | Harder to manage |
| Community | Several orgs with the same policy | Shared compliance | Governance between members |

**Cloud bursting:** size the private side for *normal* load; send the spike to public cloud; release afterwards. Tax season / insurance-claims November are the usual examples.

## Three service models (who manages what)

Remember the shading table from the MedConnect CAT:

- **On-premise:** customer owns the whole stack.
- **IaaS:** provider owns hardware/virtualisation; you still run OS, middleware, apps, data. Rent servers instead of buying them (CAPEX → OPEX).
- **PaaS:** provider also runs OS/middleware/runtime; you write apps and keep the data. Good for fast mobile/web builds. APIs (often HTTP + JSON) are how programs talk to the platform.
- **SaaS:** you just use the app (Office 365, Salesforce). Provider patches everything.

## Money words

- **CAPEX** — buy the box. **OPEX** — pay the monthly bill. **TCO** — both, plus people.
- **Economies of scale** — the CSP’s unit cost falls because thousands of tenants share the plant.
- **Vendor lock-in** — proprietary tools make leaving expensive. Mitigate: open formats, containers, a contract that includes **data export**.
- **Agility** — a test server in hours, not months.

## SLA

A written promise of availability and a **credit** when it is missed. Credits do not restore patient confidentiality — that needs location, encryption and access clauses. In the MedConnect pilot: commit 99.5%, actual 97.8% → 30% of that month’s charge (band 95.0% to below 99.0%).

## Migration

Do not lift-and-shift a unique billing system in one weekend. Wrap it, phase it, keep an exit copy of data and schema.
