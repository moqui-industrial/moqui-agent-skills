# mantle.other

One line per entity. E = entity, V = view-entity. Generated; do not edit.

- E mantle.other.budget.Budget | src: mantle-udm | pk: budgetId | fields: budgetTypeEnumId:id, timePeriodId:id, subTimePeriodTypeId:id, statusId:id, currencyUomId:id, description:text-medium, comments:text-long | rels: one>Enumeration[BudgetType], one>TimePeriod, one>StatusItem[Budget], one>Uom[Currency]
- E mantle.other.budget.BudgetItem | src: mantle-udm | pk: budgetId,budgetItemSeqId | fields: budgetItemTypeEnumId:id, itemTypeEnumId:id, glAccountId:id, amount:currency-amount, productId:id, quantity:number-decimal, quantityUomId:id, purpose:text-medium, justification:text-medium, subTimePeriodId:id | rels: one>Budget, one>Enumeration[BudgetItemType], one>Enumeration[ItemType], one>GlAccount, one>Product, one>Uom[Quantity], one>TimePeriod[Sub], many>BudgetItemDetail
- E mantle.other.budget.BudgetItemDetail | src: mantle-udm | pk: budgetItemDetailId | fields: budgetId:id, budgetItemSeqId:id, facilityId:id, assetId:id, amount:currency-precise, productId:id, quantity:number-decimal | rels: one-nofk>Budget, one>BudgetItem, one>Facility, one>Asset, one>Product
- E mantle.other.budget.BudgetParty | src: mantle-udm | pk: budgetId,partyId,roleTypeId | fields:  | rels: one>Budget, one>Party, one>RoleType
- E mantle.other.budget.BudgetReview | src: mantle-udm | pk: budgetReviewId | fields: budgetId:id, partyId:id, budgetReviewResultEnumId:id, reviewDate:date-time | rels: one>Budget, one>Party, one>Enumeration[BudgetReviewResult]
- E mantle.other.budget.BudgetRevision | src: mantle-udm | pk: budgetId,revisionSeqId | fields: dateRevised:date-time, description:text-medium | rels: one>Budget
- E mantle.other.budget.BudgetRevisionImpact | src: mantle-udm | pk: budgetId,budgetItemSeqId,revisionSeqId | fields: revisedAmount:currency-amount, addDeleteFlag:text-indicator, revisionReason:text-medium | rels: one>Budget, one>BudgetItem, one>BudgetRevision
- E mantle.other.budget.BudgetScenario | src: mantle-udm | pk: budgetScenarioId | fields: description:text-medium | rels: 
- E mantle.other.budget.BudgetScenarioApplication | src: mantle-udm | pk: budgetScenarioApplicId,budgetScenarioId | fields: budgetId:id, budgetItemSeqId:id, amountChange:currency-amount, percentageChange:number-decimal | rels: one>BudgetScenario, one>Budget, one>BudgetItem
- E mantle.other.budget.BudgetScenarioRule | src: mantle-udm | pk: budgetScenarioId,budgetItemTypeEnumId | fields: amountChange:currency-amount, percentageChange:number-decimal | rels: one>BudgetScenario, one>Enumeration[BudgetItemType]
- E mantle.other.tax.TaxAuthority | src: mantle-udm | pk: taxAuthorityId | fields: taxAuthorityTypeEnumId:id, description:text-medium, taxAuthGeoId:id, taxAuthPartyId:id, requireTaxIdForExemption:text-indicator, taxIdFormatPattern:text-medium, includeTaxInPrice:text-indicator | rels: one>Enumeration[TaxAuthorityType], one>Geo[TaxAuth], one>Party[TaxAuth]
- E mantle.other.tax.TaxAuthorityAssoc | src: mantle-udm | pk: taxAuthorityId,toTaxAuthorityId,fromDate | fields: thruDate:date-time, assocTypeEnumId:id | rels: one>TaxAuthority, one>TaxAuthority[To], one>Enumeration[TaxAuthorityAssocType]
- E mantle.other.tax.TaxAuthorityCategory | src: mantle-udm | pk: taxAuthorityId,productCategoryId | fields:  | rels: one>TaxAuthority, one>ProductCategory
- E mantle.other.tax.TaxAuthorityParty | src: mantle-udm | pk: partyId,taxAuthorityId,fromDate | fields: thruDate:date-time, partyTaxId:text-short, isExempt:text-indicator, isNexus:text-indicator | rels: one>Party, one>TaxAuthority
- E mantle.other.tax.TaxGatewayConfig | src: mantle-udm | pk: taxGatewayConfigId | fields: taxGatewayTypeEnumId:id, description:text-medium, calculateServiceName:text-medium | rels: one>Enumeration[TaxGatewayType]
- E mantle.other.tax.TaxStatement | src: mantle-udm | pk: taxStatementId | fields: timePeriodId:id, partyId:id, partyRelationshipId:id, taxAuthorityId:id, formId:id, formResponseId:id | rels: one>TimePeriod, one>Employment, one>TaxAuthority, one>DbForm, one>FormResponse
- V mantle.other.budget.BudgetAndTimePeriod | src: mantle-usl | members: BDGT=Budget, TMPD=TimePeriod | alias-all: BDGT,TMPD | aliases: 
- V mantle.other.budget.BudgetItemAndDetail | src: mantle-usl | members: BIT=BudgetItem, BIDET=BudgetItemDetail | alias-all: BIT,BIDET | aliases: itemAmount, itemProductId, itemQuantity
- V mantle.other.tax.TaxStatementPartyDetail | src: mantle-usl | members: TXST=TaxStatement, TXAU=TaxAuthority, PTY=Party, PER=Person?, ORG=Organization? | alias-all: TXST,TXAU,PTY,PER,ORG | aliases: 
- V mantle.other.tax.TaxStatementPeriodAuthority | src: mantle-usl | members: WATS=TaxStatement, TXAU=TaxAuthority, TPED=TimePeriod | alias-all: WATS,TXAU,TPED | aliases: periodPartyId
