# mantle.request

One line per entity. E = entity, V = view-entity. Generated; do not edit.

- E mantle.request.Request | src: mantle-udm | pk: requestId | fields: requestTypeEnumId:id, requestCategoryId:id, statusId:id, requestName:text-medium, description:text-long, priority:number-integer, requestDate:date-time, responseRequiredDate:date-time, requestResolutionEnumId:id, rootWorkEffortId:id, facilityId:id, productStoreId:id, salesChannelEnumId:id, emailContactMechId:id, maximumAmountUomId:id, currencyUomId:id, filedByPartyId:id, visitId:id | rels: one>Enumeration[RequestType], one>RequestCategory, one>StatusItem[Request], one>Enumeration[RequestResolution], one>WorkEffort[Root], one>Facility, one>ProductStore, one>Enumeration[SalesChannel], one>ContactMech[Email], one>Uom[MaximumAmount], one>Uom[Currency], one>Party[FiledBy], many>RequestWorkEffort, many>RequestParty, one>Visit, many>RequestCommEvent, many>RequestItem, many>RequestNote, many>RequestParty, many>RequestWorkEffort, many>WikiPageRequest
- E mantle.request.RequestCategory | src: mantle-udm | pk: requestCategoryId | fields: parentCategoryId:id, responsiblePartyId:id, description:text-medium | rels: one>RequestCategory[Parent], one>Party[Responsible]
- E mantle.request.RequestCommEvent | src: mantle-udm | pk: requestId,communicationEventId | fields:  | rels: one>Request, one>CommunicationEvent
- E mantle.request.RequestContent | src: mantle-udm | pk: requestContentId | fields: requestId:id, contentLocation:text-medium, contentTypeEnumId:id, contentDate:date-time, description:text-long, userId:id | rels: one>Request, one>Enumeration[RequestContentType], one>UserAccount
- E mantle.request.RequestEmailMessage | src: mantle-udm | pk: requestId,emailMessageId | fields: partyId:id, statusId:id | rels: one>Request, one>EmailMessage, one>Party, one>StatusItem[Request]
- E mantle.request.RequestItem | src: mantle-udm | pk: requestId,requestItemSeqId | fields: statusId:id, requiredByDate:date-time, productId:id, quantity:number-decimal, selectedAmount:number-decimal, maximumAmount:currency-amount, description:text-medium, supplierPartyId:id | rels: one>Request, one>StatusItem[Request], one>Product, one>Party[Supplier]
- E mantle.request.RequestItemAssoc | src: mantle-udm | pk: requestId,requestItemSeqId,otherRequestId,otherRequestItemSeqId | fields: quantity:number-decimal | rels: one>RequestItem, one>RequestItem[Other]
- E mantle.request.RequestItemOrder | src: mantle-udm | pk: requestItemOrderId | fields: requestId:id, requestItemSeqId:id, orderId:id, orderItemSeqId:id, quantity:number-decimal | rels: one>RequestItem, one>OrderItem
- E mantle.request.RequestNote | src: mantle-udm | pk: requestId,noteDate | fields: requestItemSeqId:id, noteText:text-very-long, userId:id | rels: one>Request, one-nofk>RequestItem
- E mantle.request.RequestParty | src: mantle-udm | pk: requestId,partyId,roleTypeId,fromDate | fields: thruDate:date-time, receiveNotifications:text-indicator | rels: one>Request, one>Party, one>RoleType, one-nofk>Person, one-nofk>Organization
- E mantle.request.RequestWorkEffort | src: mantle-udm | pk: requestId,workEffortId | fields:  | rels: one>Request, one>WorkEffort
- E mantle.request.WikiPageRequest | src: mantle-udm | pk: wikiPageId,requestId | fields:  | rels: one>WikiPage, one>Request
- E mantle.request.requirement.Requirement | src: mantle-udm | pk: requirementId | fields: requirementTypeEnumId:id, statusId:id, facilityId:id, deliverableId:id, assetId:id, productId:id, description:text-medium, requirementStartDate:date-time, requiredByDate:date-time, estimatedBudget:currency-amount, quantity:number-decimal, useCase:text-very-long, reason:text-long | rels: one>Enumeration[RequirementType], one>StatusItem[Requirement], one>Facility, one>Deliverable, one>Asset, one>Product
- E mantle.request.requirement.RequirementBudgetAllocation | src: mantle-udm | pk: requirementId,budgetId,budgetItemSeqId | fields: amount:currency-amount | rels: one>BudgetItem, one>Requirement
- E mantle.request.requirement.RequirementOrderItem | src: mantle-udm | pk: requirementId,orderId,orderItemSeqId | fields: quantity:number-decimal | rels: one>OrderItem, one>Requirement
- E mantle.request.requirement.RequirementParty | src: mantle-udm | pk: requirementId,partyId,roleTypeId,fromDate | fields: thruDate:date-time | rels: one>Requirement, one>Party, one>RoleType
- E mantle.request.requirement.RequirementRequestItem | src: mantle-udm | pk: requirementId,requestId,requestItemSeqId | fields:  | rels: one>Requirement, one>RequestItem
- E mantle.request.requirement.WorkRequirementFulfillment | src: mantle-udm | pk: requirementId,workEffortId | fields: fulfillmentTypeEnumId:id | rels: one>Requirement, one>WorkEffort, one>Enumeration[WorkRequirementFulfillmentType]
- V mantle.request.RequestAndFacilityAndStatus | src: mantle-usl | members: REQ=Request, FAC=Facility, STTS=StatusItem | alias-all: REQ | aliases: facilityName, statusDescription
- V mantle.request.RequestAndParty | src: mantle-usl | members: REQ=Request, RQP=RequestParty? | alias-all: REQ,RQP | aliases: 
- V mantle.request.RequestAndPartyDetail | src: mantle-usl | members: REQ=Request, RQP=RequestParty, PTY=Party, ORG=Organization?, PER=Person?, USRACT=UserAccount? | alias-all: RQP,REQ,PTY,PER,ORG | aliases: username
- V mantle.request.RequestCommEventDetail | src: mantle-usl | members: RCE=RequestCommEvent, CEV=CommunicationEvent | alias-all: RCE,CEV | aliases: 
- V mantle.request.RequestItemAndProduct | src: mantle-usl | members: RQIT=RequestItem, PROD=Product | alias-all: RQIT | aliases: productName
- V mantle.request.RequestPartyAndPerson | src: mantle-usl | members: RQP=RequestParty, PER=Person | alias-all: RQP,PER | aliases: 
- V mantle.request.RequestWorkEffortDetail | src: mantle-usl | members: RWE=RequestWorkEffort, WEF=WorkEffort | alias-all: RWE,WEF | aliases: 
- V mantle.request.WikiPageAndRequest | src: mantle-usl | members: WPR=WikiPageRequest, WKP=WikiPage, REQ=Request | alias-all: WPR,WKP,REQ | aliases: 
- V mantle.request.WorkEffortRequestDetail | src: mantle-usl | members: RWE=RequestWorkEffort, REQ=Request | alias-all: RWE,REQ | aliases: 
