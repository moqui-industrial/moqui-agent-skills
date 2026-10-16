# Recurring data patterns (computed)

## Status-bearing: has statusId — changes go through services, check StatusFlow
- count: 55
- examples: A2ATaskStatus, Agreement, Asset, AssetMaintenance, AssetPartyAssignment, Budget, CommunicationEvent, CommunicationEventParty, ContactListCommStatus, ContactListParty, Device, DeviceGroupMember

## Typed by Enumeration: *TypeEnumId field
- count: 208
- examples: A2AArtifactPart, A2AMessagePart, A2ATaskEvent, AcctgTrans, AcctgTransEntry, Agreement, AgreementAssoc, AgreementContent, AgreementItem, AgreementTerm, ApproximatedFunction, ApproximatedFunctionSample

## Detail/line pattern: parent PK + *SeqId
- count: 47
- examples: A2AArtifactPart, A2AMessagePart, AcctgTransEntry, AgreementItem, AgreementItemEmployment, AgreementItemGeo, AgreementItemParty, AgreementItemWorkEffort, AssetMaintenanceOrderItem, AssetRegistration, BudgetItem, BudgetRevision

## Type hierarchy entity: *Type with parentTypeId
- count: 5
- examples: BenefitType, CommunicationEventType, FinancialAccountType, RoleType, StatusType

## Effective dating: fromDate in PK (+ thruDate) — query with date-filter
- count: 63
- examples: AssetPartyAssignment, AssetStandardCost, BillingAccountParty, ContactListEmail, ContactListParty, DeviceMathModel, EmplClassResponsibility, EmplPositionClassParty, EmplPositionParty, EmplPositionResponsibility, EmploymentBenefit, EmploymentLeave

## Party-in-role: partyId + roleTypeId on a business object
- count: 33
- examples: AgreementItemParty, AgreementParty, AssetIssuanceParty, AssetPartyAssignment, AssetPoolParty, BillingAccountParty, BudgetParty, CommunicationEventParty, EmplPositionParty, FacilityGroupParty, FacilityParty, FinancialAccountParty

## Has pseudoId: user-facing code distinct from the technical PK
- count: 7
- examples: AssetPool, EmplPosition, Facility, Party, Product, ProductCategory, ShipmentBoxType

