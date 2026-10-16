# Entity masters (declared aggregates, generated)

A <master> in an entity definition is Moqui's own declaration of a business document: the root entity plus the relationships that belong to it, nested. The same definition drives the master REST API (/rest/m1/...) and data export with dependents. Prefer it over the computed trees in structures.md.

## FinancialAccount — master 'default' (mantle.account.financial.FinancialAccount)
  - type -> FinancialAccountType
  - status -> StatusItem
  - organization -> Party
  - owner -> Party
  - postToAccount -> GlAccount
  - currencyUom -> Uom
  - replenishMethod -> PaymentMethod

## Invoice — master 'default' (mantle.account.invoice.Invoice)
  - type -> Enumeration
  - status -> StatusItem
  - currencyUom -> Uom
  - fromParty -> Party (use-master basic)
  - toParty -> Party (use-master basic)
  - items -> InvoiceItem
    - type -> Enumeration
    - product -> Product
    - quantityUom -> Uom
    - details -> InvoiceItemDetail
    - orderItemBillings -> OrderItemBilling
    - shipmentItemSources -> ShipmentItemSource
    - issuances -> AssetIssuance
    - receipts -> AssetReceipt
  - paymentApplications -> PaymentApplication
  - toPaymentApplications -> PaymentApplication

## PaymentMethod — master 'default' (mantle.account.method.PaymentMethod)
  - methodType -> Enumeration
  - ownerParty -> Party
    - organization -> Organization
    - person -> Person
  - postal -> ContactMech (use-master default)
  - telecom -> ContactMech (use-master default)
  - email -> ContactMech (use-master default)
  - trustLevel -> Enumeration
  - bankAccount -> BankAccount
  - bitcoinWallet -> BitcoinWallet
  - creditCard -> CreditCard
    - type -> Enumeration
  - giftCard -> GiftCard
  - payPalAccount -> PayPalAccount

## Payment — master 'default' (mantle.account.payment.Payment)
  - type -> Enumeration
  - instrument -> Enumeration
  - method -> PaymentMethod (use-master default)
  - toMethod -> PaymentMethod (use-master default)
  - distGroup -> Enumeration
  - amountUom -> Uom
  - fromParty -> Party (use-master basic)
  - toParty -> Party (use-master basic)
  - status -> StatusItem
  - applications -> PaymentApplication
  - contents -> PaymentContent

## Facility — master 'default' (mantle.facility.Facility)
  - type -> Enumeration
  - parent -> Facility
  - status -> StatusItem
  - owner -> Party (use-master basic)
  - sizeUom -> Uom
  - geo -> Geo
  - geoPoint -> GeoPoint
  - certifications -> FacilityCertification
  - contactMechs -> FacilityContactMech
    - contactMech -> ContactMech (use-master default)
    - purpose -> ContactMechPurpose
  - contents -> FacilityContent
  - groups -> FacilityGroupMember
    - group -> FacilityGroup
  - notes -> FacilityNote
  - parties -> FacilityParty
    - party -> Party (use-master basic)
    - role -> RoleType
  - printers -> FacilityPrinter
    - printer -> NetworkPrinter

## AcctgTrans — master 'default' (mantle.ledger.transaction.AcctgTrans)
  - type -> Enumeration
  - organization -> Party
  - journal -> GlJournal
  - fiscalType -> Enumeration
  - groupStatus -> StatusItem
  - amountUom -> Uom
  - originalCurrencyUom -> Uom
  - asset -> Asset
  - assetIssuance -> AssetIssuance
  - assetReceipt -> AssetReceipt
  - physicalInventory -> PhysicalInventory
  - otherParty -> Party
  - invoice -> Invoice
  - payment -> Payment
  - paymentApplication -> PaymentApplication
  - financialAccountTrans -> FinancialAccountTrans
  - shipment -> Shipment
  - workEffort -> WorkEffort
  - reversedBy -> AcctgTrans
  - reverseOf -> AcctgTrans
  - entries -> AcctgTransEntry
    - glAccountType -> Enumeration
    - glAccount -> GlAccount
    - reconcileStatus -> StatusItem
    - product -> Product
    - asset -> Asset

## OrderHeader — master 'default' (mantle.order.OrderHeader)
  - status -> StatusItem
  - currencyUom -> Uom
  - salesChannel -> Enumeration
  - visit -> Visit
  - parts -> OrderPart
    - status -> StatusItem
    - items -> OrderItem
      - itemType -> Enumeration
      - product -> Product
      - quantityUom -> Uom
      - reservations -> AssetReservation
      - issuances -> AssetIssuance
      - receipts -> AssetReceipt
      - shipmentSources -> ShipmentItemSource
      - billings -> OrderItemBilling
    - parties -> OrderPartParty
      - party -> Party (use-master contact)
      - roleType -> RoleType
    - contactMechs -> OrderPartContactMech
      - contactMech -> ContactMech (use-master default)
    - terms -> OrderPartTerm
      - term -> SettlementTerm
    - vendor -> Party (use-master basic)
    - customer -> Party (use-master basic)
    - carrier -> Party (use-master basic)
    - shipmentMethod -> Enumeration
    - postal -> ContactMech (use-master default)
    - telecom -> ContactMech (use-master default)
    - facility -> Facility
    - payments -> Payment (use-master default)
  - contents -> OrderContent
    - type -> Enumeration
  - notes -> OrderNote
  - communicationEvents -> OrderCommunicationEvent

## ReturnHeader — master 'default' (mantle.order.return.ReturnHeader)
  - status -> StatusItem
  - vendor -> Party (use-master basic)
  - customer -> Party (use-master basic)
  - carrier -> Party (use-master basic)
  - shipmentMethod -> Enumeration
  - postal -> ContactMech (use-master default)
  - telecom -> ContactMech (use-master default)
  - currencyUom -> Uom
  - visit -> Visit
  - items -> ReturnItem
    - reason -> Enumeration
    - response -> Enumeration
    - itemType -> Enumeration
    - status -> StatusItem
    - product -> Product
    - orderItem -> OrderItem
    - issuances -> AssetIssuance
    - receipts -> AssetReceipt
    - shipmentSources -> ShipmentItemSource
    - billings -> ReturnItemBilling

## Party — master 'default' (mantle.party.Party)
  - type -> Enumeration
  - organization -> Organization
  - person -> Person
  - badges -> PartyBadge
  - classifications -> PartyClassificationAppl
    - classification -> PartyClassification
      - type -> Enumeration
  - contents -> PartyContent
    - type -> Enumeration
  - identifications -> PartyIdentification
    - type -> Enumeration
  - notes -> PartyNote
  - roles -> PartyRole
    - role -> RoleType
  - fromRelationships -> PartyRelationship
    - fromRole -> RoleType
    - toParty -> Party
      - organization -> Organization
      - person -> Person
    - toRole -> RoleType
    - status -> StatusItem
    - type -> Enumeration
  - toRelationships -> PartyRelationship
    - fromParty -> Party
      - organization -> Organization
      - person -> Person
    - fromRole -> RoleType
    - toRole -> RoleType
    - status -> StatusItem
    - type -> Enumeration
  - contactMechs -> PartyContactMech
    - contactMech -> ContactMech (use-master default)
    - purpose -> ContactMechPurpose

## Party — master 'contact' (mantle.party.Party)
  - type -> Enumeration
  - organization -> Organization
  - person -> Person
  - identifications -> PartyIdentification
    - type -> Enumeration
  - contactMechs -> PartyContactMech
    - contactMech -> ContactMech (use-master default)
    - purpose -> ContactMechPurpose

## Party — master 'basic' (mantle.party.Party)
  - organization -> Organization
  - person -> Person
  - identifications -> PartyIdentification
    - type -> Enumeration

## CommunicationEvent — master 'default' (mantle.party.communication.CommunicationEvent)
  - type -> CommunicationEventType
  - contactMechType -> Enumeration
  - status -> StatusItem
  - parent -> CommunicationEvent (use-master default)
  - root -> CommunicationEvent (use-master default)
  - children -> CommunicationEvent (use-master default)
  - fromContactMech -> ContactMech
  - toContactMech -> ContactMech
  - fromParty -> Party
  - fromRole -> RoleType
  - toParty -> Party
  - toRole -> RoleType
  - contactList -> ContactList
  - reason -> Enumeration
  - contents -> CommunicationEventContent
  - parties -> CommunicationEventParty
    - party -> Party (use-master basic)
    - role -> RoleType
    - contactMech -> ContactMech (use-master default)
    - status -> StatusItem
  - products -> CommunicationEventProduct
    - product -> Product
  - purposes -> CommunicationEventPurpose
    - purpose -> Enumeration
  - orders -> OrderCommunicationEvent

## ContactMech — master 'default' (mantle.party.contact.ContactMech)
  - telecomNumber -> TelecomNumber
  - postalAddress -> PostalAddress
    - cityGeo -> Geo
    - countyGeo -> Geo
    - stateProvinceGeo -> Geo
    - postalCodeGeo -> Geo
    - countryGeo -> Geo
    - telecomContactMech -> ContactMech (use-master default)
    - emailContactMech -> ContactMech

## Product — master 'default' (mantle.product.Product)
  - type -> Enumeration
  - class -> Enumeration
  - assetType -> Enumeration
  - assetClass -> Enumeration
  - status -> StatusItem
  - originGeo -> Geo
  - defaultBoxType -> ShipmentBoxType
  - amountUom -> Uom
  - assocs -> ProductAssoc
    - type -> Enumeration
    - toProduct -> Product
  - toAssocs -> ProductAssoc
    - type -> Enumeration
    - product -> Product
  - contents -> ProductContent
  - dimensions -> ProductDimension
  - geos -> ProductGeo
    - geo -> Geo
  - identifications -> ProductIdentification
    - type -> Enumeration
  - otherIdentifications -> ProductOtherIdentification
    - type -> Enumeration
  - parties -> ProductParty
    - party -> Party (use-master basic)
    - role -> RoleType
  - prices -> ProductPrice
    - type -> Enumeration
    - purpose -> Enumeration
    - priceUom -> Uom
    - termUom -> Uom
    - quantityUom -> Uom
  - categories -> ProductCategoryMember
    - category -> ProductCategory
  - features -> ProductFeatureAppl
    - feature -> ProductFeature

## Asset — master 'default' (mantle.product.asset.Asset)
  - parent -> Asset
  - type -> Enumeration
  - class -> Enumeration
  - status -> StatusItem
  - owner -> Party
  - originalQuantityUom -> Uom
  - originFacility -> Facility
  - facility -> Facility
  - location -> FacilityLocation
  - container -> Container
  - boxType -> ShipmentBoxType
  - lot -> Lot
  - geoPoint -> GeoPoint
  - acquireOrderItem -> OrderItem
  - acquireWorkEffort -> WorkEffort
  - acquireShipment -> Shipment
  - acquireCostUom -> Uom
  - depreciationType -> Enumeration
  - taxDepreciationType -> Enumeration
  - details -> AssetDetail
  - depreciations -> AssetDepreciation
  - identifications -> AssetIdentification
  - partyAssignments -> AssetPartyAssignment
  - issuances -> AssetIssuance
  - reservations -> AssetReservation
  - receipts -> AssetReceipt

## ProductCategory — master 'default' (mantle.product.category.ProductCategory)
  - type -> Enumeration
  - contents -> ProductCategoryContent
  - parties -> ProductCategoryParty
    - party -> Party (use-master basic)
    - role -> RoleType
  - products -> ProductCategoryMember
    - product -> Product
  - parents -> ProductCategoryRollup
    - parent -> ProductCategory
  - children -> ProductCategoryRollup
    - category -> ProductCategory
  - featureGroups -> ProductCategoryFeatGrpAppl
    - group -> ProductFeatureGroup

## ProductFeature — master 'default' (mantle.product.feature.ProductFeature)
  - type -> Enumeration
  - numberUom -> Uom
  - products -> ProductFeatureAppl
  - iactns -> ProductFeatureIactn
    - type -> Enumeration
    - toFeature -> ProductFeature
  - toIactns -> ProductFeatureIactn
    - type -> Enumeration
    - feature -> ProductFeature
  - groups -> ProductFeatureGroupAppl
    - group -> ProductFeatureGroup

## ProductFeatureGroup — master 'default' (mantle.product.feature.ProductFeatureGroup)
  - features -> ProductFeatureGroupAppl
    - feature -> ProductFeature
  - categories -> ProductCategoryFeatGrpAppl
    - category -> ProductCategory

## ProductStore — master 'default' (mantle.product.store.ProductStore)
  - organization -> Party
  - inventoryFacility -> Facility
  - assetReservationOrder -> Enumeration
  - defaultCurrencyUom -> Uom
  - defaultSalesChannel -> Enumeration
  - taxGatewayConfig -> TaxGatewayConfig
  - categories -> ProductStoreCategory
    - category -> ProductCategory
    - type -> Enumeration
  - emails -> ProductStoreEmail
    - template -> EmailTemplate
    - type -> Enumeration
  - facilities -> ProductStoreFacility
    - facility -> Facility
  - parties -> ProductStoreParty
    - party -> Party (use-master basic)
    - role -> RoleType
  - paymentGateways -> ProductStorePaymentGateway
    - paymentInstrument -> Enumeration
    - config -> PaymentGatewayConfig
  - shippingGateways -> ProductStoreShippingGateway
    - carrier -> Party (use-master basic)
    - config -> ShippingGatewayConfig
  - groups -> ProductStoreGroupMember
    - group -> ProductStoreGroup

## Subscription — master 'default' (mantle.product.subscription.Subscription)
  - type -> Enumeration
  - resource -> SubscriptionResource
  - subscriber -> Party (use-master basic)
  - deliverTo -> ContactMech (use-master default)
  - product -> Product
  - availableTimeUom -> Uom
  - useTimeUom -> Uom

## SubscriptionResource — master 'default' (mantle.product.subscription.SubscriptionResource)
  - parent -> SubscriptionResource
  - products -> ProductSubscriptionResource
    - product -> Product

## Shipment — master 'default' (mantle.shipment.Shipment)
  - type -> Enumeration
  - status -> StatusItem
  - fromParty -> Party (use-master basic)
  - toParty -> Party (use-master basic)
  - shipWorkEffort -> WorkEffort
  - receiveWorkEffort -> WorkEffort
  - costUom -> Uom
  - contents -> ShipmentContent
  - items -> ShipmentItem
    - sources -> ShipmentItemSource
      - status -> StatusItem
    - contents -> ShipmentPackageContent
    - issuances -> AssetIssuance
    - receipts -> AssetReceipt
  - packages -> ShipmentPackage
    - contents -> ShipmentPackageContent
    - routeSegments -> ShipmentPackageRouteSeg
  - routeSegments -> ShipmentRouteSegment
    - carrierParty -> Party (use-master basic)
    - shipmentMethod -> Enumeration
    - originFacility -> Facility
    - originPostal -> ContactMech (use-master default)
    - originTelecom -> ContactMech (use-master default)
    - destFacility -> Facility
    - destPostal -> ContactMech (use-master default)
    - destTelecom -> ContactMech (use-master default)
    - status -> StatusItem
    - costUom -> Uom
    - billingWeightUom -> Uom

## WorkEffort — master 'default' (mantle.work.effort.WorkEffort)
  - parent -> WorkEffort
  - root -> WorkEffort
  - type -> Enumeration
  - purpose -> Enumeration
  - visibility -> Enumeration
  - resolution -> Enumeration
  - workType -> Enumeration
  - owner -> Party (use-master basic)
  - status -> StatusItem
  - facility -> Facility
  - timeUom -> Uom
  - costUom -> Uom
  - assets -> WorkEffortAssetAssign
    - asset -> Asset
    - status -> StatusItem
  - assetsNeeded -> WorkEffortAssetNeeded
    - assetProduct -> Product
  - assocs -> WorkEffortAssoc
    - toWorkEffort -> WorkEffort
    - type -> Enumeration
  - toAssocs -> WorkEffortAssoc
    - workEffort -> WorkEffort
    - type -> Enumeration
  - billings -> WorkEffortBilling
    - invoiceItem -> InvoiceItem
  - communicationEvents -> WorkEffortCommEvent
    - communicationEvent -> CommunicationEvent
  - contactMechs -> WorkEffortContactMech
    - contactMech -> ContactMech (use-master default)
    - purpose -> ContactMechPurpose
  - contents -> WorkEffortContent
    - type -> Enumeration
  - facilities -> WorkEffortFacility
    - facility -> Facility
    - type -> Enumeration
  - notes -> WorkEffortNote
  - parties -> WorkEffortParty
    - party -> Party (use-master basic)
    - role -> RoleType
    - status -> StatusItem
    - availability -> Enumeration
    - delegateReason -> Enumeration
    - expectation -> Enumeration
    - positionClass -> EmplPositionClass
  - products -> WorkEffortProduct
    - product -> Product
    - type -> Enumeration
    - status -> StatusItem
    - receipts -> AssetReceipt
    - issuances -> AssetIssuance

## Enumeration — master 'default' (moqui.basic.Enumeration)
  - type -> EnumerationType
  - parent -> Enumeration
  - related -> Enumeration

## Geo — master 'default' (moqui.basic.Geo)
  - type -> Enumeration
  - assocs -> GeoAssoc
    - toGeo -> Geo
    - type -> Enumeration
  - toAssocs -> GeoAssoc
    - geo -> Geo
    - type -> Enumeration

## GeoPoint — master 'default' (moqui.basic.GeoPoint)
  - type -> Enumeration
  - dataSource -> DataSource
  - elevationUom -> Uom

## StatusItem — master 'default' (moqui.basic.StatusItem)
  - type -> StatusType
  - flows -> StatusFlowItem
    - flow -> StatusFlow
  - transitions -> StatusFlowTransition
    - flow -> StatusFlow
    - toStatus -> StatusItem
  - toTransitions -> StatusFlowTransition
    - flow -> StatusFlow
    - status -> StatusItem

## Uom — master 'default' (moqui.basic.Uom)
  - type -> Enumeration
  - conversions -> UomConversion
    - toUom -> Uom
  - toConversions -> UomConversion
    - uom -> Uom

## EmailMessage — master 'default' (moqui.basic.email.EmailMessage)
  - status -> StatusItem
  - type -> Enumeration
  - root -> EmailMessage (use-master default)
  - parent -> EmailMessage (use-master default)
  - children -> EmailMessage (use-master default)
  - fromUser -> UserAccount
  - toUser -> UserAccount
  - template -> EmailTemplate
  - server -> EmailServer

## EmailTemplate — master 'default' (moqui.basic.email.EmailTemplate)
  - server -> EmailServer
  - attachments -> EmailTemplateAttachment

## PrintJob — master 'default' (moqui.basic.print.PrintJob)
  - printer -> NetworkPrinter
  - status -> StatusItem

## DataDocument — master 'default' (moqui.entity.document.DataDocument)
  - fields -> DataDocumentField
  - relAliases -> DataDocumentRelAlias
  - conditions -> DataDocumentCondition
  - links -> DataDocumentLink
  - feeds -> DataFeedDocument
    - feed -> DataFeed

## EntitySync — master 'default' (moqui.entity.sync.EntitySync)
  - status -> StatusItem
  - artifacts -> EntitySyncArtifact
    - group -> ArtifactGroup
      - artifacts -> ArtifactGroupMember
    - applType -> Enumeration

## MorphismComposition — master 'catalog' (moqui.math.ct.MorphismComposition)
  - morphism -> Morphism
  - type -> Enumeration
  - components -> MorphismCompositionComponent
    - component -> Morphism

## MorphismCompositionComponent — master 'catalog' (moqui.math.ct.MorphismCompositionComponent)
  - composition -> MorphismComposition
  - component -> Morphism

## SystemMessage — master 'default' (moqui.service.message.SystemMessage)
  - type -> SystemMessageType
  - status -> StatusItem
  - parent -> SystemMessage
  - remote -> SystemMessageRemote
  - errors -> SystemMessageError

