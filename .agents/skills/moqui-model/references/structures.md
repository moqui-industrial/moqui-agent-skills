# Structural patterns (computed from entity relationships)

Use this file to understand how concepts are composed before writing a query or a write.

## 1. Aggregates (header, parts, lines, details)

Children are created after their parent and usually through the parent's services. Plain child: its PK contains the parent PK plus a *SeqId. 'own id, linked': it has its own id but belongs to the parent. Multi-level aggregates are listed first.

### DbForm (moqui.screen.form.DbForm) — depth 3
  - DbFormField
    - DbFormFieldAttribute
    - DbFormFieldEntOpts
      - DbFormFieldEntOptsCond
      - DbFormFieldEntOptsOrder
    - DbFormFieldOption
  - DbFormUserGroup

### Invoice (mantle.account.invoice.Invoice) — depth 2
  - InvoiceContactMech
  - InvoiceContent (own id, linked)
  - InvoiceEmailMessage
  - InvoiceItem
    - InvoiceItemAssoc (own id, linked)
    - InvoiceItemDetail (own id, linked)
    - InvoiceTerm
    - ReturnItemBilling
    - WorkEffortBilling
  - InvoiceParty
  - InvoiceSystemMessage
  - WorkEffortInvoice

### Facility (mantle.facility.Facility) — depth 2
  - FacilityBoxType
  - FacilityCertification (own id, linked)
  - FacilityContactMech
  - FacilityContent (own id, linked)
  - FacilityGlAppl
  - FacilityGroupMember
  - FacilityLocation
    - ProductFacilityLocation
  - FacilityLocationType
  - FacilityNote
  - FacilityParty
  - FacilityPrinter
  - ProductFacility
  - ProductStoreFacility
  - WorkEffortFacility

### OrderHeader (mantle.order.OrderHeader) — depth 2
  - TrackingCodeOrder
  - TrackingCodeOrderReturn
  - OrderCommunicationEvent
  - OrderDecision
    - OrderDecisionReason
  - OrderEmailMessage
  - OrderItem
    - OrderItemBilling (own id, linked)
    - OrderItemFormResponse
    - OrderItemParty
    - OrderItemWorkEffort
    - AssetMaintenanceOrderItem
    - RequirementOrderItem
  - OrderNote
  - OrderPart
    - OrderPartContactMech
    - OrderPartParty
    - OrderPartTerm
  - OrderPromoCode
  - OrderServiceJobRun
  - OrderSystemMessage
  - SalesOpportunityOrder

### ReturnHeader (mantle.order.return.ReturnHeader) — depth 2
  - TrackingCodeOrderReturn
  - ReturnContactMech
  - ReturnItem
    - ReturnItemBilling
  - ReturnSystemMessage

### Budget (mantle.other.budget.Budget) — depth 2
  - BudgetItem
    - PaymentBudgetAllocation
    - BudgetItemDetail (own id, linked)
    - BudgetRevisionImpact
    - RequirementBudgetAllocation
  - BudgetParty
  - BudgetReview (own id, linked)
  - BudgetRevision
  - BudgetScenarioApplication (own id, linked)

### Party (mantle.party.Party) — depth 2
  - BillingAccountParty
  - FinancialAccountParty
  - InvoiceParty
  - FacilityGroupParty
  - FacilityParty
  - PartySkill
  - EmplPositionClassParty
  - EmplPositionParty
  - GlAccountParty
  - GlAccountTypePartyDefault
  - MarketingCampaignParty
  - ContactListParty
  - MarketSegmentParty
  - OrderItemParty
  - OrderPartParty
  - BudgetParty
  - TaxAuthorityParty
  - PartyBadge (own id, linked)
    - PartyBadgeScan
  - PartyClassificationAppl
  - PartyContent (own id, linked)
  - PartyDimension
  - PartyGeoPoint
  - PartyIdentification
  - PartyNote
  - PartyRole
  - PartySetting
  - PartySystemMessage
  - AgreementItemParty
  - AgreementParty
  - CommunicationEventParty
  - PartyContactMech
  - ProductParty
  - AssetPartyAssignment
  - AssetPoolParty
  - ProductCategoryParty
  - AssetIssuanceParty
  - ProductStoreGroupParty
  - ProductStoreParty
  - ProductStorePromoCodeParty
  - RequestParty
  - RequirementParty
  - PartyNeed (own id, linked)
  - SalesOpportunityParty
  - ShipmentParty
  - PartyCarrierAccount
  - WorkEffortParty
  - TimesheetParty

### Agreement (mantle.party.agreement.Agreement) — depth 2
  - AgreementAddendum (own id, linked)
  - AgreementAssoc (own id, linked)
  - AgreementContent (own id, linked)
  - AgreementItem
    - AgreementItemEmployment
    - AgreementItemGeo
    - AgreementItemParty
    - AgreementItemWorkEffort
  - AgreementParty
  - AgreementTerm (own id, linked)

### Product (mantle.product.Product) — depth 2
  - ProductFacility
  - ProductFacilityLocation
  - ProductGlAccount
  - CommunicationEventProduct
  - ProductAssoc
  - ProductCalculatedInfo (own id, linked)
  - ProductContent (own id, linked)
  - ProductDbForm (own id, linked)
  - ProductDimension
  - ProductGeo
  - ProductGlAppl
  - ProductIdentification
  - ProductOtherIdentification (own id, linked)
  - ProductParameterOption (own id, linked)
  - ProductParameterProduct
  - ProductParameterSet (own id, linked)
  - ProductParty
  - ProductPrice (own id, linked)
  - ProductReview (own id, linked)
  - ProductUomDimension (own id, linked)
  - ProductWorkEffort
  - ProductCategoryMember
  - ProductFeatureAppl
  - ProductMaintenance (own id, linked)
  - ProductMeter (own id, linked)
  - ProductStoreProduct
  - ProductStorePromoProduct
  - ProductSubscriptionResource
  - ShipmentItem
    - ShipmentItemSource (own id, linked)
    - ShipmentPackageContent
  - WorkEffortProduct
  - ProductionEstimate (own id, linked)
    - ProductionEstimateAsset
    - ProductionEstimateWorkEff

### Asset (mantle.product.asset.Asset) — depth 2
  - AssetTypeGlAccount (own id, linked)
  - AssetDepreciation
  - AssetDetail (own id, linked)
  - AssetGlAppl
  - AssetIdentification
  - AssetPartyAssignment
  - AssetPaymentMethod
  - AssetStandardCost
  - AssetIssuance (own id, linked)
    - AssetIssuanceParty
  - AssetReservation (own id, linked)
  - AssetMaintenance (own id, linked)
    - AssetMaintenanceContent
    - AssetMaintenanceOrderItem
  - AssetMeter
  - AssetRegistration
  - AssetReceipt (own id, linked)
  - WorkEffortAssetAssign
  - ProductionEstimateAsset

### ProductStore (mantle.product.store.ProductStore) — depth 2
  - AssetPoolStore
  - ProductStoreApprove (own id, linked)
    - ProductStoreApproveParam
  - ProductStoreCategory
  - ProductStoreDataDocument
  - ProductStoreEmail
  - ProductStoreFacility
  - ProductStoreGroupMember
  - ProductStoreParty
  - ProductStorePaymentGateway
  - ProductStoreProduct
  - ProductStorePromotion (own id, linked)
    - ProductStorePromoParameter
    - ProductStorePromoProduct
  - ProductStoreSetting
  - ProductStoreShipOption
  - ProductStoreShippingGateway
  - ProductStoreWikiContent (own id, linked)
  - ProductStoreWikiSpace (own id, linked)

### Request (mantle.request.Request) — depth 2
  - RequestCommEvent
  - RequestContent (own id, linked)
  - RequestEmailMessage
  - RequestItem
    - RequestItemAssoc
    - RequestItemOrder (own id, linked)
    - RequirementRequestItem
  - RequestNote
  - RequestParty
  - RequestWorkEffort
  - WikiPageRequest

### Shipment (mantle.shipment.Shipment) — depth 2
  - ShipmentContactMech
  - ShipmentContent (own id, linked)
  - ShipmentEmailMessage
  - ShipmentItem
    - ShipmentItemSource (own id, linked)
    - ShipmentPackageContent
  - ShipmentPackage
    - ShipmentPackageRouteSeg
  - ShipmentParty
  - ShipmentRouteSegment
  - ShipmentSystemMessage

### A2ATask (moqui.a2a.A2ATask) — depth 2
  - A2AArtifact
    - A2AArtifactPart
  - A2ATaskEvent (own id, linked)
  - A2ATaskStatus (own id, linked)

### Device (moqui.device.Device) — depth 2
  - DeviceContent (own id, linked)
  - DeviceDashboard
  - DeviceEvent (own id, linked)
  - DeviceGroup (own id, linked)
    - DeviceGroupMember
  - DeviceLog (own id, linked)
  - DeviceMathModel
  - DeviceRule (own id, linked)
  - DeviceRuleSet (own id, linked)
  - DeviceStats (own id, linked)
  - TrajectoryAxisBinding

### Graph (moqui.math.Graph) — depth 2
  - GraphCategory (own id, linked)
  - GraphContent (own id, linked)
  - GraphEdge (own id, linked)
    - GraphEdgeMorphism (own id, linked)
    - MeshKCellEdge
  - GraphVertex (own id, linked)
    - GraphVertexCategoryObject (own id, linked)
    - MeshKCellVertex

### Mesh (moqui.math.Mesh) — depth 2
  - MeshContent (own id, linked)
  - MeshGroup (own id, linked)
    - MeshGroupMember
  - MeshKCell (own id, linked)
    - MeshKCellEdge
    - MeshKCellQuality (own id, linked)
    - MeshKCellTexture (own id, linked)
    - MeshKCellVertex
  - MeshQuality (own id, linked)

### Tensor (moqui.math.Tensor) — depth 2
  - TensorAxis
  - TensorContent (own id, linked)
  - TensorElement (own id, linked)
    - TensorElementIndex

### Category (moqui.math.ct.Category) — depth 2
  - CategoryObject (own id, linked)
    - NaturalTransformationComponent
  - ExponentialObject

### Morphism (moqui.math.ct.Morphism) — depth 2
  - MorphismComposition (own id, linked)
    - MorphismCompositionComponent
  - MorphismParameterBinding

### DbResource (moqui.resource.DbResource) — depth 2
  - DbResourceFile (own id, linked)
    - DbResourceFileHistory

### ServiceJob (moqui.service.job.ServiceJob) — depth 2
  - ServiceJobParameter
  - ServiceJobRun (own id, linked)
    - OrderServiceJobRun
    - ServiceJobRunLock (own id, linked)
  - ServiceJobUser

### BillingAccount (mantle.account.billing.BillingAccount) — depth 1
  - BillingAccountParty
  - BillingAccountTerm (own id, linked)

### FinancialAccount (mantle.account.financial.FinancialAccount) — depth 1
  - FinancialAccountAuth (own id, linked)
  - FinancialAccountParty
  - FinancialAccountTrans (own id, linked)

### FinancialAccountType (mantle.account.financial.FinancialAccountType) — depth 1
  - FinancialAccountTypeGlAccount

### SettlementTerm (mantle.account.invoice.SettlementTerm) — depth 1
  - InvoiceTerm
  - OrderPartTerm

### PaymentMethod (mantle.account.method.PaymentMethod) — depth 1
  - BankAccountCheck
  - PaymentMethodContent (own id, linked)
  - PaymentMethodFile (own id, linked)
  - PaymentMethodFileType
  - PaymentMethodTrans
  - AssetPaymentMethod

### Payment (mantle.account.payment.Payment) — depth 1
  - PaymentGatewayResponse (own id, linked)
  - PaymentMethodTrans (own id, linked)
  - PaymentApplication (own id, linked)
  - PaymentBudgetAllocation
  - PaymentContent (own id, linked)
  - PaymentFraudEvidence (own id, linked)

### FacilityGroup (mantle.facility.FacilityGroup) — depth 1
  - FacilityGroupMember
  - FacilityGroupParty

### BenefitType (mantle.humanres.employment.BenefitType) — depth 1
  - EmploymentBenefit

### Employment (mantle.humanres.employment.Employment) — depth 1
  - EmploymentBenefit
  - EmploymentLeave
  - EmploymentPayHistory
  - EmploymentSalary
  - AgreementItemEmployment

### PayrollAdjCalcService (mantle.humanres.employment.PayrollAdjCalcService) — depth 1
  - PayrollAdjCalcParameter

### PayrollAdjustment (mantle.humanres.employment.PayrollAdjustment) — depth 1
  - PayrollAdjustmentDetail
  - PayrollAdjustmentExempt
  - PayrollAdjustmentFedStts (own id, linked)
  - PayrollAdjustmentStateStts

### EmplPosition (mantle.humanres.position.EmplPosition) — depth 1
  - EmplPositionParty
  - EmplPositionResponsibility
  - WorkEffortEmplPosition

### EmplPositionClass (mantle.humanres.position.EmplPositionClass) — depth 1
  - EmplClassResponsibility
  - EmplPositionClassDimension
  - EmplPositionClassParty
  - EmplPositionClassSkill
  - EmplPositionClassWorkType
  - EmplPositionClassPtyClsTp

### PayGrade (mantle.humanres.rate.PayGrade) — depth 1
  - PayGradeSalary

### GlAccount (mantle.ledger.account.GlAccount) — depth 1
  - FacilityGlAppl
  - GlAccountCategoryMember
  - GlAccountEnumAppl
  - GlAccountGroupMember
  - GlAccountOrgTimePeriod
  - GlAccountOrganization
  - GlAccountParty
  - GlBudgetXref
  - GlAccountTypeDefault (own id, linked)
  - GlAccountTypePartyDefault (own id, linked)
  - ProductGlAppl
  - AssetGlAppl

### GlAccountCategory (mantle.ledger.account.GlAccountCategory) — depth 1
  - GlAccountCategoryMember

### GlAccountGroup (mantle.ledger.account.GlAccountGroup) — depth 1
  - GlAccountGroupMember (own id, linked)

### GlReconciliation (mantle.ledger.reconciliation.GlReconciliation) — depth 1
  - GlReconciliationEntry

### AcctgTrans (mantle.ledger.transaction.AcctgTrans) — depth 1
  - GlReconciliationEntry
  - AcctgTransEntry

### MarketingCampaign (mantle.marketing.campaign.MarketingCampaign) — depth 1
  - MarketingCampaignNote
  - MarketingCampaignParty

### ContactList (mantle.marketing.contact.ContactList) — depth 1
  - ContactListCommStatus
  - ContactListEmail
  - ContactListParty

### MarketSegment (mantle.marketing.segment.MarketSegment) — depth 1
  - MarketInterest
  - MarketSegmentClassification
  - MarketSegmentDimension
  - MarketSegmentGeo
  - MarketSegmentParty

### TrackingCode (mantle.marketing.tracking.TrackingCode) — depth 1
  - TrackingCodeOrder (own id, linked)
  - TrackingCodeOrderReturn (own id, linked)
  - TrackingCodeVisit
  - SalesOpportunityTracking

### BudgetScenario (mantle.other.budget.BudgetScenario) — depth 1
  - BudgetScenarioApplication
  - BudgetScenarioRule

### TaxAuthority (mantle.other.tax.TaxAuthority) — depth 1
  - TaxAuthorityGlAccount
  - TaxAuthorityAssoc
  - TaxAuthorityCategory
  - TaxAuthorityParty

### Organization (mantle.party.Organization) — depth 1
  - OrderItemParty
  - OrderPartParty
  - RequestParty
  - WorkEffortParty

### PartyClassification (mantle.party.PartyClassification) — depth 1
  - MarketSegmentClassification
  - PartyClassificationAppl

### PartyRelationship (mantle.party.PartyRelationship) — depth 1
  - PartyRelationshipSetting

### PartySettingType (mantle.party.PartySettingType) — depth 1
  - PartyRelationshipSetting
  - PartySetting
  - PartySettingTypeRole

### Person (mantle.party.Person) — depth 1
  - OrderItemParty
  - OrderPartParty
  - CommunicationEventParty
  - RequestParty
  - WorkEffortParty

### RoleType (mantle.party.RoleType) — depth 1
  - BillingAccountParty
  - FinancialAccountParty
  - InvoiceParty
  - FacilityGroupParty
  - FacilityParty
  - EmplPositionParty
  - GlAccountParty
  - GlAccountTypePartyDefault
  - MarketingCampaignParty
  - MarketSegmentParty
  - OrderItemParty
  - OrderPartParty
  - BudgetParty
  - PartyRole
  - PartySettingTypeRole
  - RoleGroupMember
  - AgreementItemParty
  - AgreementParty
  - CommunicationEventParty
  - ProductParty
  - AssetPartyAssignment
  - ProductCategoryParty
  - AssetIssuanceParty
  - ProductStoreGroupParty
  - ProductStoreParty
  - RequestParty
  - RequirementParty
  - SalesOpportunityParty
  - ShipmentParty
  - WorkEffortParty
  - TimesheetParty

### CommunicationEvent (mantle.party.communication.CommunicationEvent) — depth 1
  - ContactListCommStatus
  - OrderCommunicationEvent
  - CommunicationEventParty
  - CommunicationEventProduct
  - CommunicationEventPurpose
  - WikiPageCommunicationEvent
  - RequestCommEvent
  - WorkEffortCommEvent

### ContactMech (mantle.party.contact.ContactMech) — depth 1
  - InvoiceContactMech
  - FacilityContactMech
  - ContactListCommStatus
  - OrderPartContactMech
  - ReturnContactMech
  - PartyContactMech
  - WorkEffortContactMech

### ContactMechPurpose (mantle.party.contact.ContactMechPurpose) — depth 1
  - InvoiceContactMech
  - FacilityContactMech
  - OrderPartContactMech
  - ReturnContactMech
  - PartyContactMech
  - ShipmentContactMech
  - WorkEffortContactMech

### PostalAddress (mantle.party.contact.PostalAddress) — depth 1
  - InvoiceContactMech
  - FacilityContactMech
  - OrderPartContactMech
  - PartyContactMech
  - WorkEffortContactMech

### TelecomNumber (mantle.party.contact.TelecomNumber) — depth 1
  - InvoiceContactMech
  - FacilityContactMech
  - OrderPartContactMech
  - PartyContactMech
  - WorkEffortContactMech

### TimePeriodType (mantle.party.time.TimePeriodType) — depth 1
  - PayrollGarnishMinWage

### ProductDimensionType (mantle.product.ProductDimensionType) — depth 1
  - ProductClassDimension
  - ProductDimension

### ProductParameter (mantle.product.ProductParameter) — depth 1
  - ProductParameterOption (own id, linked)
  - ProductParameterProduct
  - ProductParameterValue (own id, linked)

### ProductPriceModify (mantle.product.ProductPriceModify) — depth 1
  - ProductPriceModifyParameter

### AssetPool (mantle.product.asset.AssetPool) — depth 1
  - AssetPoolParty
  - AssetPoolStore

### PhysicalInventory (mantle.product.asset.PhysicalInventory) — depth 1
  - PhysicalInventoryCount (own id, linked)

### ProductCategory (mantle.product.category.ProductCategory) — depth 1
  - ProductCategoryGlAccount
  - MarketInterest
  - TaxAuthorityCategory
  - ProductCategoryContent (own id, linked)
  - ProductCategoryIdent (own id, linked)
  - ProductCategoryMember
  - ProductCategoryParty
  - ProductCategoryRollup
  - ProductCategoryFeatGrpAppl
  - ProductStoreCategory

### ProductFeature (mantle.product.feature.ProductFeature) — depth 1
  - ProductFeatureAppl
  - ProductFeatureGroupAppl
  - ProductFeatureIactn

### ProductFeatureGroup (mantle.product.feature.ProductFeatureGroup) — depth 1
  - ProductClassFeatureGroup
  - ProductCategoryFeatGrpAppl
  - ProductFeatureGroupAppl

### ProductStoreGroup (mantle.product.store.ProductStoreGroup) — depth 1
  - ProductStoreGroupMember
  - ProductStoreGroupParty

### ProductStorePromoCode (mantle.product.store.ProductStorePromoCode) — depth 1
  - OrderPromoCode
  - ProductStorePromoCodeParty

### Subscription (mantle.product.subscription.Subscription) — depth 1
  - SubscriptionDelivery

### SubscriptionResource (mantle.product.subscription.SubscriptionResource) — depth 1
  - ProductSubscriptionResource

### Requirement (mantle.request.requirement.Requirement) — depth 1
  - RequirementBudgetAllocation
  - RequirementOrderItem
  - RequirementParty
  - RequirementRequestItem
  - WorkRequirementFulfillment

### SalesForecast (mantle.sales.forecast.SalesForecast) — depth 1
  - SalesForecastDetail

### SalesOpportunity (mantle.sales.opportunity.SalesOpportunity) — depth 1
  - SalesOpportunityCompetitor
  - SalesOpportunityOrder
  - SalesOpportunityParty
  - SalesOpportunityTracking
  - SalesOpportunityWorkEffort

### ShipmentBoxType (mantle.shipment.ShipmentBoxType) — depth 1
  - FacilityBoxType
  - CarrierShipmentBoxType
  - ShippingGatewayBoxType

### ShippingGatewayConfig (mantle.shipment.carrier.ShippingGatewayConfig) — depth 1
  - ShippingGatewayBoxType
  - ShippingGatewayCarrier
  - ShippingGatewayMethod
  - ShippingGatewayOption

### Deliverable (mantle.work.effort.Deliverable) — depth 1
  - WorkEffortDeliverableProd

### WorkEffort (mantle.work.effort.WorkEffort) — depth 1
  - OrderItemWorkEffort
  - AgreementItemWorkEffort
  - ProductWorkEffort
  - RequestWorkEffort
  - WorkRequirementFulfillment
  - SalesOpportunityWorkEffort
  - WikiPageWorkEffort
  - WorkEffortAssetAssign
  - WorkEffortAssetNeeded
  - WorkEffortAssoc
  - WorkEffortBilling
  - WorkEffortCommEvent
  - WorkEffortContactMech
  - WorkEffortContent (own id, linked)
  - WorkEffortDeliverableProd
  - WorkEffortEmplPosition
  - WorkEffortFacility
  - WorkEffortInvoice
  - WorkEffortNote
  - WorkEffortParty
  - WorkEffortProduct
  - WorkEffortSkillStandard
  - ProductionEstimateWorkEff

### Timesheet (mantle.work.time.Timesheet) — depth 1
  - TimesheetParty

### A2AMessage (moqui.a2a.A2AMessage) — depth 1
  - A2AMessagePart

### GeoPoint (moqui.basic.GeoPoint) — depth 1
  - PartyGeoPoint

### StatusFlow (moqui.basic.StatusFlow) — depth 1
  - StatusFlowItem
  - StatusFlowTransition

### UomDimensionType (moqui.basic.UomDimensionType) — depth 1
  - EmplPositionClassDimension
  - MarketSegmentDimension
  - PartyDimension
  - ProductClassUomDimension
  - UomDimTypeGroupMember

### EmailMessage (moqui.basic.email.EmailMessage) — depth 1
  - InvoiceEmailMessage
  - OrderEmailMessage
  - RequestEmailMessage
  - ShipmentEmailMessage

### EmailTemplate (moqui.basic.email.EmailTemplate) — depth 1
  - EmailTemplateAttachment

### DeviceRequest (moqui.device.DeviceRequest) — depth 1
  - DeviceRequestItem

### DataDocument (moqui.entity.document.DataDocument) — depth 1
  - DataDocumentCondition
  - DataDocumentField
  - DataDocumentLink
  - DataDocumentRelAlias
  - DataDocumentUserGroup
  - DataFeedDocument

### DataFeed (moqui.entity.feed.DataFeed) — depth 1
  - DataFeedDocument

### EntitySync (moqui.entity.sync.EntitySync) — depth 1
  - EntitySyncArtifact
  - EntitySyncHistory

### DbViewEntity (moqui.entity.view.DbViewEntity) — depth 1
  - DbViewEntityAlias
  - DbViewEntityKeyMap
  - DbViewEntityMember

### LlmSkill (moqui.llm.LlmSkill) — depth 1
  - LlmSkillUse (own id, linked)

### ApproximatedFunction (moqui.math.ApproximatedFunction) — depth 1
  - ApproximatedFunctionSample

### CoordinateSystem (moqui.math.CoordinateSystem) — depth 1
  - CoordinateSystemBaseVector
  - CoordinateSystemMetric (own id, linked)

### MathModel (moqui.math.MathModel) — depth 1
  - DeviceMathModel
  - MathModelData (own id, linked)
  - MathModelRun (own id, linked)

### MathModelDef (moqui.math.MathModelDef) — depth 1
  - MathModelDefContent (own id, linked)
  - MathModelDefIdentification

### Matrix (moqui.math.Matrix) — depth 1
  - MatrixComponent (own id, linked)
  - MatrixContent (own id, linked)

### Parameter (moqui.math.Parameter) — depth 1
  - DeviceRequestItem
  - ParameterLog (own id, linked)

### ParametricPath (moqui.math.ParametricPath) — depth 1
  - ParametricPathContent (own id, linked)
  - ParametricPathEvent (own id, linked)
  - ParametricPathPoint

### TensorDecomposition (moqui.math.TensorDecomposition) — depth 1
  - TensorDecompositionFactor

### Trajectory (moqui.math.Trajectory) — depth 1
  - TrajectoryAxisBinding
  - TrajectoryRun (own id, linked)
  - TrajectoryStats (own id, linked)

### TrajectoryPoint (moqui.math.TrajectoryPoint) — depth 1
  - TrajectoryPointRun (own id, linked)

### Transformation (moqui.math.Transformation) — depth 1
  - TransformationOperand

### Vector (moqui.math.Vector) — depth 1
  - CoordinateSystemBaseVector
  - VectorComponent (own id, linked)
  - VectorContent (own id, linked)

### CategoryConstruction (moqui.math.ct.CategoryConstruction) — depth 1
  - CategoryConstructionOperand

### Functor (moqui.math.ct.Functor) — depth 1
  - FunctorMorphismMapping
  - FunctorObjectMapping
  - FunctorRepresentation (own id, linked)

### NaturalTransformation (moqui.math.ct.NaturalTransformation) — depth 1
  - NaturalTransformationComponent (own id, linked)

### WikiBlog (moqui.resource.wiki.WikiBlog) — depth 1
  - WikiBlogCategory

### WikiPage (moqui.resource.wiki.WikiPage) — depth 1
  - WikiPageCommunicationEvent
  - WikiPageRequest
  - WikiPageWorkEffort
  - WikiPageAlias (own id, linked)
  - WikiPageCategoryMember
  - WikiPageHistory
  - WikiPageUser

### WikiPageCategory (moqui.resource.wiki.WikiPageCategory) — depth 1
  - WikiBlogCategory
  - WikiPageCategoryMember

### WikiSpace (moqui.resource.wiki.WikiSpace) — depth 1
  - WikiPageAlias
  - WikiSpaceUser

### ScreenScheduled (moqui.screen.ScreenScheduled) — depth 1
  - ScreenScheduledLock (own id, linked)

### ScreenTheme (moqui.screen.ScreenTheme) — depth 1
  - ScreenThemeIcon
  - ScreenThemeResource

### FormConfig (moqui.screen.form.FormConfig) — depth 1
  - FormConfigField
  - FormConfigUser (own id, linked)
  - FormConfigUserGroup
  - FormConfigUserType (own id, linked)

### FormListFind (moqui.screen.form.FormListFind) — depth 1
  - FormListFindField
  - FormListFindUser
  - FormListFindUserDefault (own id, linked)
  - FormListFindUserGroup

### FormResponse (moqui.screen.form.FormResponse) — depth 1
  - OrderItemFormResponse
  - FormResponseAnswer (own id, linked)

### ArtifactAuthz (moqui.security.ArtifactAuthz) — depth 1
  - ArtifactAuthzFilter

### ArtifactGroup (moqui.security.ArtifactGroup) — depth 1
  - EntitySyncArtifact
  - ArtifactGroupMember
  - ArtifactTarpit

### EntityFilterSet (moqui.security.EntityFilterSet) — depth 1
  - ArtifactAuthzFilter

### UserGroup (moqui.security.UserGroup) — depth 1
  - DataDocumentUserGroup
  - SubscreensItem
  - DbFormUserGroup
  - FormConfigUserGroup
  - FormListFindUserGroup
  - ArtifactTarpit
  - UserGroupMember
  - UserGroupPermission
  - UserGroupPreference
  - UserGroupScreenTheme

### UserPermission (moqui.security.UserPermission) — depth 1
  - UserGroupPermission

### NotificationMessage (moqui.security.user.NotificationMessage) — depth 1
  - NotificationMessageUser

### NotificationTopic (moqui.security.user.NotificationTopic) — depth 1
  - NotificationTopicUser

### Visit (moqui.server.Visit) — depth 1
  - TrackingCodeVisit

### AppInstance (moqui.server.instance.AppInstance) — depth 1
  - AppInstanceEnv
  - AppInstanceHostConfig
  - AppInstanceLink
  - AppInstanceVolume

### InstanceImageType (moqui.server.instance.InstanceImageType) — depth 1
  - InstanceImageTypeEnv
  - InstanceImageTypeHostConfig
  - InstanceImageTypeLink
  - InstanceImageTypeVolume

### SystemMessage (moqui.service.message.SystemMessage) — depth 1
  - InvoiceSystemMessage
  - OrderSystemMessage
  - ReturnSystemMessage
  - PartySystemMessage
  - ShipmentSystemMessage
  - SystemMessageError

### SystemMessageRemote (moqui.service.message.SystemMessageRemote) — depth 1
  - SystemMessageEnumMap

Note: a line can also point to a sibling level without being its child by PK (OrderItem has orderPartSeqId: it belongs to an OrderPart of the same OrderHeader).

## 2. Self hierarchies (parent*Id on the same entity)

Trees of the same concept: a WorkEffort under a WorkEffort, an OrderItem under an OrderItem, an Enumeration under an Enumeration (parentEnumId, see enums.md).

- FinancialAccountType.parentTypeId
- InvoiceItem.parentInvoiceId
- InvoiceItem.parentInvoiceItemSeqId
- InvoiceItem.parentItemSeqId
- Facility.parentFacilityId
- FacilityGroup.parentGroupId
- BenefitType.parentTypeId
- GlAccount.parentGlAccountId
- MarketingCampaign.parentCampaignId
- MarketSegment.parentMarketSegmentId
- OrderHeader.parentOrderId
- OrderItem.parentItemSeqId
- OrderPart.parentPartSeqId
- ReturnItem.parentItemSeqId
- PartyClassification.parentClassificationId
- RoleType.parentTypeId
- CommunicationEvent.parentCommEventId
- CommunicationEventType.parentTypeId
- TimePeriod.parentPeriodId
- TimePeriodType.parentPeriodTypeId
- ProductOtherIdentification.parentProductId
- Asset.parentAssetId
- ProductCategoryRollup.parentProductCategoryId
- SubscriptionResource.parentResourceId
- RequestCategory.parentCategoryId
- SalesForecast.parentSalesForecastId
- WorkEffort.parentWorkEffortId
- TimeEntry.parentEntryId
- Enumeration.parentEnumId
- StatusType.parentTypeId
- EmailMessage.parentEmailMessageId
- Device.parentDeviceId
- DeviceConfig.parentConfigId
- DeviceRule.parentRuleId
- DeviceRuleSet.parentRuleSetId
- CoordinateSystem.parentSystemId
- Graph.parentGraphId
- MathModelDef.parentModelDefId
- Matrix.parentMatrixId
- MatrixComponent.parentComponentId
- Mesh.parentMeshId
- ParameterDef.parentParameterDefId
- ParametricPath.parentPathId
- Tensor.parentTensorId
- TensorElement.parentElementId
- Transformation.parentTransformationId
- Vector.parentVectorId
- VectorComponent.parentComponentId
- Category.parentCategoryId
- CategoryObject.parentObjectId
- Functor.parentFunctorId
- Morphism.parentMorphismId
- NaturalTransformation.parentTransformationId
- DbResource.parentResourceId
- WikiPage.parentWikiPageId
- SystemMessage.parentMessageId

## 3. Hubs (star-schema-like entities)

Entities that tie many business objects together, like a fact table. Good starting points for analytical queries and for tracing what happened to an item.

- OrderItem (17 links): Asset, FinancialAccount, FinancialAccountTrans, GlAccount, OrderHeader, OrderItem, OrderPart, Product, ProductCategory, ProductFeature, ProductParameterSet, ProductPrice, ProductStorePromoCode, ProductStorePromotion, SalesOpportunity, Subscription, TaxAuthority
- Payment (16 links): CreditCard, Employment, FinancialAccount, FinancialAccountAuth, FinancialAccountTrans, GlAccount, Invoice, OrderHeader, OrderItem, OrderPart, Party, Payment, PaymentGatewayConfig, PaymentMethod, PaymentMethodFile, Visit
- Asset (14 links): Asset, AssetPool, Container, Facility, FacilityLocation, GeoPoint, Lot, OrderHeader, OrderItem, Party, Product, Shipment, ShipmentBoxType, WorkEffort
- AssetIssuance (13 links): Asset, AssetMaintenance, AssetReservation, Facility, Invoice, InvoiceItem, OrderItem, Product, ReturnItem, Shipment, ShipmentItem, ShipmentItemSource, WorkEffort
- AcctgTrans (13 links): AcctgTrans, Asset, AssetIssuance, AssetReceipt, FinancialAccountTrans, GlJournal, Invoice, Party, Payment, PaymentApplication, PhysicalInventory, Shipment, WorkEffort
- PaymentMethod (13 links): BankAccount, BitcoinWallet, ContactMech, CreditCard, FinancialAccount, GiftCard, GlAccount, Party, PayPalAccount, PaymentFraudEvidence, PaymentGatewayConfig, PostalAddress, TelecomNumber
- Parameter (12 links): Category, CategoryObject, Device, DeviceConfig, Functor, Graph, GraphEdge, GraphVertex, MathModel, MeshKCell, Morphism, ParameterDef
- AssetDetail (12 links): Asset, AssetIssuance, AssetMaintenance, AssetReceipt, AssetReservation, OrderItem, PhysicalInventory, PhysicalInventoryCount, Product, ReturnItem, Shipment, WorkEffort
- MathModelData (11 links): ApproximatedFunction, GraphEdge, GraphVertex, MathModel, MathModelRun, Matrix, MeshGroup, MeshKCell, Tensor, Transformation, Vector
- SystemMessage (10 links): Invoice, OrderHeader, OrderPart, PaymentMethodFile, ReturnHeader, Shipment, SystemMessage, SystemMessageRemote, SystemMessageType, Visit
- Device (10 links): CoordinateSystem, Device, DeviceGroup, DeviceRule, DeviceRuleSet, PhysicalDevice, StatusFlow, StatusType, Trajectory, Transformation
- AssetReceipt (10 links): Asset, InvoiceItem, OrderItem, Product, ReturnItem, Shipment, ShipmentItem, ShipmentItemSource, ShipmentPackage, WorkEffort
- InvoiceItem (10 links): Asset, FinancialAccount, FinancialAccountTrans, GlAccount, Invoice, InvoiceItem, PayrollAdjustment, Product, SalesOpportunity, TaxAuthority
- TimeEntry (9 links): EmplPositionClass, Facility, InvoiceItem, Party, Person, RateAmount, TimeEntry, Timesheet, WorkEffort
- FinancialAccountTrans (9 links): FinancialAccount, FinancialAccountAuth, FinancialAccountTrans, GlReconciliation, Invoice, OrderHeader, OrderItem, Party, Payment
- ShipmentRouteSegment (8 links): ContactMech, Delivery, Facility, Party, PostalAddress, Shipment, ShippingGatewayConfig, TelecomNumber
- ProductStore (8 links): ContactMech, DataDocument, Facility, Party, PostalAddress, SystemMessageRemote, TaxGatewayConfig, WikiSpace
- ReturnHeader (8 links): ContactMech, Facility, FinancialAccount, Party, PaymentMethod, PostalAddress, SystemMessageRemote, Visit
- OrderPart (8 links): ContactMech, Facility, OrderHeader, OrderPart, Party, PostalAddress, SettlementTerm, TelecomNumber
- Invoice (8 links): BillingAccount, Employment, Organization, Party, Person, ProductStore, SettlementTerm, SystemMessageRemote

## 4. Group / member

Membership, usually with validity dates (fromDate in PK): add a member by creating the row, remove it by setting thruDate.

- FacilityGroupMember: Facility + FacilityGroup
- GlAccountCategoryMember: GlAccount + GlAccountCategory
- GlAccountGroupMember: GlAccount + Enumeration + GlAccountGroup
- RoleGroupMember: Enumeration + RoleType
- ProductCategoryMember: Product + ProductCategory
- ProductStoreGroupMember: ProductStore + ProductStoreGroup
- EnumGroupMember: Enumeration
- UomDimTypeGroupMember: Enumeration + UomDimensionType
- UomGroupMember: Enumeration + Uom
- DeviceGroupMember: DeviceGroup + Device + Enumeration + StatusItem + StatusFlow
- DbViewEntityMember: DbViewEntity + DbViewEntityMember
- MeshGroupMember: MeshGroup + MeshKCell + Enumeration
- WikiPageCategoryMember: WikiPageCategory + WikiPage
- ArtifactGroupMember: ArtifactGroup + Enumeration
- UserGroupMember: UserGroup + UserAccount

## 5. Assoc (typed links between instances of the same entity)

- InvoiceItemAssoc: links InvoiceItem, Party to InvoiceItem, Party
- TaxAuthorityAssoc: links TaxAuthority to TaxAuthority
- AgreementAssoc: links Agreement to Agreement
- ProductAssoc: links Product to Product
- RequestItemAssoc: links RequestItem to RequestItem
- WorkEffortAssoc: links WorkEffort to WorkEffort

## 6. Enumeration hierarchies

1225 enum values have a parentEnumId (shown as '(parent: X)' in enums.md). A child value is a refinement of its parent: code that checks the parent must also accept its children.
