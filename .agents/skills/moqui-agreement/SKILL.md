---
name: moqui-agreement
description: Contracts in Moqui/Mantle with Agreement — framework and construction contracts (appalto) that govern all orders of a job order, clauses as agreement items, quantitative and legal terms (payment days, late fees, Incoterms, thresholds), agreement-specific prices, templates and addenda, and service-level agreements whose thresholds are compared with measured usage. Use this skill whenever the task involves a contract, framework agreement, master agreement, price list for one customer or supplier, payment or delivery terms, SLA, commission agreement, or employment agreement.
---

# moqui-agreement: contracts and their terms

`mantle.party.agreement.Agreement` is a general contract between an internal organization and another party. Use it for any binding arrangement whose clauses and numbers must be recorded and then applied: a construction contract over a job order, a supply framework, a SaaS subscription with service levels, a commission scheme, an employment contract. Data goes through `moqui-data`; names and values from `moqui-model`. `assets/AgreementExamples.xml` contains a framework contract and a SaaS agreement and passes `check_data.py`; it uses the product from `moqui-product`'s example, so load that first.

## Model

| Entity | Role |
| --- | --- |
| `Agreement` | Type (`AgrSales`, `AgrProduct`, `AgrCommission`, `AgrEmployment`, `AgrEula`, `AgrOther`), status, `organizationPartyId` with its role and `otherPartyId` with its role, dates, validity, currency, full text, `isTemplate` and `templateAgreementId` |
| `AgreementItem` | A clause or section: type (`AitSection`, `AitPricing`, `AitPurchase`, `AitExhibit`, `AitSubAgreement`, `AitCommissionRate`), optional product and quantity, text, own validity |
| `AgreementTerm` | A term of the agreement or of one item: `termTypeEnumId`, `termNumber`, `termText`, optional `settlementTermId` |
| `SettlementTerm` | A reusable payment term: type, `termValue` with unit (net 60 days) |
| `AgreementParty`, `AgreementItemParty` | Other parties in roles (guarantor, subcontractor, signer) |
| `AgreementItemWorkEffort` | Links a clause to the work that executes it (the job order project, its milestones) |
| `AgreementItemGeo`, `AgreementItemEmployment` | Territory of a clause; employment covered by it |
| `AgreementAddendum`, `AgreementAssoc` (`AatAddendum`, `AatAlternate`), `AgreementContent` | Changes over time, related agreements, signed documents |

`TermType` is a hierarchy worth reading in `enums.md`:

- **Financial:** `TtFinPaymentDays` and its parts, `TtFinPaymentDayCurMonth`, `TtFinPaymentDayNextMonth`, `TtFinPaymentDisc`, `TtFinLateFee`, `TtFinCollection`.
- **Delivery:** all Incoterms under `TtInco`.
- **Commission:** fixed, variable, minimum, maximum.
- **Legal:** indemnification, non-compete, exclusivity, termination, renewal.
- **Thresholds:** `TtThreshold`.

Add your own term types as enumeration values when a contract needs them.

Mantle defines the `Agreement` status type but no status values or flow: define the life cycle you need in seed data, as the example does.

## What Mantle does with an agreement

- **Payment terms.** When an invoice has no settlement term, Mantle looks for the most recent valid agreement between the internal organization and the other party, matching the other party's role (`Customer` for receivables, any other role for payables), and takes the `settlementTermId` of its terms to compute the due date. Only then does it fall back to the organization's accounting preferences.
- **Prices.** `ProductPrice` has `agreementId` and `agreementItemSeqId`: a price valid only under that agreement or clause.
- **Order terms.** Orders carry settlement terms per part (`OrderPartTerm`), which should come from the agreement.

Agreement services in Mantle cover only content (`create#AgreementContent`, `save#AgreementContentFile`...); everything else goes through the entity-auto services.

## Framework contract over a job order

A construction or supply contract (appalto) is the umbrella of a job order: every order, delivery and invoice of that job is governed by its clauses, prices and terms. Mantle has no `agreementId` on orders, so the umbrella is made of links:

1. The `Agreement` with its clauses (`AgreementItem`), payment and delivery terms, and agreement prices.
2. The job order as a project (`WetProject` root), linked to the clauses it executes with `AgreementItemWorkEffort`.
3. Orders issued for the job linked to the project's work efforts with `OrderItemWorkEffort`, priced with the agreement's `ProductPrice` rows, and carrying the agreement's settlement terms in `OrderPartTerm`.
4. Changes to the contract through `AgreementAddendum` or an associated agreement, requested and approved as a Request fulfilled by a task (see `moqui-model`).

If every order must point at its contract directly, add `agreementId` to `OrderHeader` with `extend-entity` in your own component rather than storing it in free text.

## Service levels and thresholds

For a SaaS or service agreement, record each limit as an `AgreementTerm` of type `TtThreshold`, or a more specific type you add, with `termNumber` and a clear `termText`: availability, response time, included devices or users, data volume. Record actual usage as `Measurement` rows (see `moqui-model`) or read it from the running services, and compare them in a scheduled service that opens a Request when a threshold is crossed. Link the agreement to the subscription's product through an `AgreementItem` with that product.

## Templates

An agreement with `isTemplate="Y"` is a model: new agreements set `templateAgreementId` and copy its items and terms. Keep standard clauses in templates and change them only through new template versions.
