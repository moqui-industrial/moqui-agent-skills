# Enumerations (seed/install data)

Format: `## enumTypeId` then `- enumId: description`.

## A2APartType — A2A Part Type
- A2APrtData: Data Part
- A2APrtRaw: Raw Bytes Part
- A2APrtText: Text Part
- A2APrtUrl: URL Part

## A2ATaskEventType — A2A Task Event Type
- A2AEvtArtifact: Task Artifact Update
- A2AEvtStatus: Task Status Update

## A2ATaskStatus — A2A Task Status
- A2AtsAuthRequired: Authentication Required
- A2AtsCanceled: Canceled
- A2AtsCompleted: Completed
- A2AtsFailed: Failed
- A2AtsInputRequired: Input Required
- A2AtsRejected: Rejected
- A2AtsSubmitted: Submitted
- A2AtsUnspecified: Unspecified
- A2AtsWorking: Working

## ACHChangeCode — ACH Change Code
- ACHRC_C01: Incorrect DFI Account Number
- ACHRC_C02: Incorrect Routing Number
- ACHRC_C03: Incorrect Routing Number and Incorrect DFI Account Number
- ACHRC_C04: Incorrect Individual Name/Receiving Company Name
- ACHRC_C05: Savings/Checking Selection is Wrong
- ACHRC_C06: Incorrect DFI Account Number and Incorrect Transaction Code
- ACHRC_C07: Incorrect Routing Number, Incorrect DFI Account Number, and Incorrect Transaction Code
- ACHRC_C08: Incorrect Receiving DFI Identification
- ACHRC_C09: Incorrect Individual Identification Number
- ACHRC_C13: Addenda Format Error
- ACHRC_C14: Incorrect SEC Code for Outbound International Payment
- ACHRC_C61: Misrouted Notification of Change
- ACHRC_C62: Incorrect Trace Number
- ACHRC_C63: Incorrect Company Identification Number
- ACHRC_C64: Incorrect Individual Identification Number/Identification Number
- ACHRC_C65: Incorrectly Formatted Corrected Data
- ACHRC_C66: Incorrect Discretionary Data
- ACHRC_C67: Routing Number Not From Original Entry Detail Record
- ACHRC_C68: DFI Account Number Not From Original Entry Detail Record
- ACHRC_C69: Incorrect Transaction Code

## ACHReturnCode — ACH Return Code
- ACHRC_R00: Manually Cancelled
- ACHRC_R01: Insufficient Funds
- ACHRC_R02: Account Closed
- ACHRC_R03: No Account/Unable to Locate Accountt
- ACHRC_R04: Invalid Account Number Structure
- ACHRC_R05: Unauthorized Debit to Consumer Account Using Corporate SEC Code
- ACHRC_R06: Return per ODFI's Request
- ACHRC_R07: Authorization Revoked by Customer
- ACHRC_R08: Payment Stopped
- ACHRC_R09: Uncollected Funds
- ACHRC_R10: Customer Advises Not Authorized, Improper, or Ineligible
- ACHRC_R11: Check Truncation Entry Return
- ACHRC_R12: Account Sold to Another DFI
- ACHRC_R13: Invalid ACH Routing Number
- ACHRC_R14: Representative Payee Deceased or Unable to Continue in That Capacity
- ACHRC_R15: Beneficiary or Account Holder Deceased
- ACHRC_R16: Account Frozen
- ACHRC_R17: File Record Edit Criteria
- ACHRC_R18: Improper Effective Entry Date
- ACHRC_R19: Amount Field Error
- ACHRC_R20: Non-Transaction Account
- ACHRC_R21: Invalid Company Identification
- ACHRC_R22: Invalid Individual ID Number
- ACHRC_R23: Credit Entry Refused by Receiver
- ACHRC_R24: Duplicate Entry
- ACHRC_R25: Addenda Error
- ACHRC_R26: Mandatory Field Error
- ACHRC_R27: Trace Number Error
- ACHRC_R28: Routing Number Check Digit Error
- ACHRC_R29: Corporate Customer Advises Not Authorized
- ACHRC_R30: RDFI Not Participant in Check Truncation Program
- ACHRC_R31: Permissible Return Entry
- ACHRC_R32: RDFI Non-Settlement
- ACHRC_R33: Return of XCK Entry
- ACHRC_R34: Limited Participation DFI
- ACHRC_R35: Return of Improper Debit Entry
- ACHRC_R36: Return of Improper Credit Entry
- ACHRC_R37: Source Document Presented for Payment
- ACHRC_R38: Stop Payment on Source Document
- ACHRC_R39: Improper Source Document/Source Document Presented for Payment
- ACHRC_R40: Return of ENR Entry by Federal Government Agency
- ACHRC_R41: Invalid Transaction Code
- ACHRC_R42: Routing Number/Check Digit Error
- ACHRC_R43: Invalid DFI Account Number
- ACHRC_R44: Invalid Individual ID Number
- ACHRC_R45: Invalid Individual Name/Company Name
- ACHRC_R46: Invalid Representative Payee Indicator
- ACHRC_R47: Duplicate Enrollment
- ACHRC_R50: State Law Affecting RCK Acceptance
- ACHRC_R51: Item related to RCK Entry is Ineligible or RCK Entry is Improper
- ACHRC_R52: Stop Payment on Item Related to RCK Entry
- ACHRC_R53: Item and RCK Entry Presented for Payment
- ACHRC_R61: Misrouted Return
- ACHRC_R67: Duplicate Return
- ACHRC_R68: Untimely Return
- ACHRC_R69: Field Error(s)
- ACHRC_R70: Permissible Return Entry Not Accepted/Return Not Requested by ODFI
- ACHRC_R71: Misrouted Dishonored Return
- ACHRC_R72: Untimely Dishonored Return
- ACHRC_R73: Timely Original Return
- ACHRC_R74: Corrected Return
- ACHRC_R75: Return Not a Duplicate
- ACHRC_R76: No Errors Found
- ACHRC_R80: IAT Entry Coding Error
- ACHRC_R81: Non-Participant in IAT Program
- ACHRC_R82: Invalid Foreign Receiving DFI Identification
- ACHRC_R83: Foreign Receiving DFI Unable to Settle
- ACHRC_R84: Entry Not Processed by Gateway
- ACHRC_R85: Incorrectly Coded Outbound International Payment

## AcctgTransResult — Accounting Transaction Result
- AtrNoAcctgPreference: No Accounting Preference
- AtrNoAcquireCost: No Acquire Cost
- AtrNoTransReason: No Transaction Reason
- AtrPaymentNotPosted: Payment Not Posted
- AtrSuccess: Success

## AcctgTransType — Accounting Transaction Type
- AttAmortization: Amortization
- AttAssetIssuance: Asset Issuance (parent: AttExternal)
- AttAssetReceipt: Asset Receipt (parent: AttExternal)
- AttAssetVariance: Asset Variance
- AttCapitalization: Capitalization
- AttCommissionInvoice: Commission Invoice (parent: AttObligation)
- AttCreditLine: Credit Line (parent: AttObligation)
- AttCreditMemo: Customer Credit Memo (parent: AttObligation)
- AttCustRtnInvoice: Customer Return Invoice (parent: AttObligation)
- AttDepreciation: Depreciation
- AttDisbursement: Disbursement (parent: AttPayment)
- AttExternal: External
- AttFinancialAdjustment: Fin. Account Adjustment
- AttFinancialDeposit: Fin. Account Deposit
- AttFinancialWithdrawal: Fin. Account Withdrawal
- AttGarnishmentInvoice: Garnishment Invoice (parent: AttObligation)
- AttIncomingPayment: Incoming Payment
- AttIncomingPaymentAp: Incoming Payment Application
- AttInternal: Internal
- AttInventoryIssuance: Inventory Issuance
- AttInventoryReceipt: Inventory Receipt
- AttInventoryVariance: Inventory Variance
- AttInvoiceAdjust: Invoice Adjustment (parent: AttObligation)
- AttInvoiceInOutAppl: Invoice AR/AP Application
- AttManufacturing: Manufacturing
- AttNetIncomeClosing: Net Income Period Closing
- AttNote: Note (parent: AttObligation)
- AttObligation: Obligation (parent: AttExternal)
- AttOtherObligation: Other Obligation (parent: AttObligation)
- AttOutgoingPayment: Outgoing Payment
- AttOutgoingPaymentAp: Outgoing Payment Application
- AttPayment: Payment (parent: AttExternal)
- AttPaymentAdjust: Payment Adjustment (parent: AttPayment)
- AttPaymentApplied: Payment Application
- AttPaymentInOutAppl: Payment In/Out Application
- AttPayrollInvoice: Payroll Invoice (parent: AttObligation)
- AttPeriodClosing: Period Closing Adjustment
- AttPurchaseInvoice: Purchase Invoice (parent: AttObligation)
- AttReceipt: Receipt (parent: AttPayment)
- AttReturnInventory: Return Inventory (parent: AttExternal)
- AttSales: Sales (parent: AttObligation)
- AttSalesInventory: Sales Inventory (parent: AttExternal)
- AttSalesInvoice: Sales Invoice (parent: AttObligation)
- AttTaxDue: Tax Due (parent: AttObligation)
- AttTaxInvoice: Tax Invoice (parent: AttObligation)
- AttVendCreditMemo: Supplier Credit Memo (parent: AttObligation)
- AttVendRtnInvoice: Supplier Return Invoice (parent: AttObligation)

## AgreementAssocType — Agreement Association Type
- AatAddendum: Addendum
- AatAlternate: Alternate

## AgreementContentType — Agreement Content Type
- AcntDocument: Agreement Document
- AcntPriceSheet: Price Sheet
- AcntSupporting: Supporting Document

## AgreementItemType — Agreement Item Type
- AitCommissionRate: Commission Rate
- AitExhibit: Exhibit
- AitPricing: Pricing
- AitPurchase: Purchase
- AitSection: Section
- AitSubAgreement: Sub-Agreement

## AgreementType — Agreement Type
- AgrCommission: Commission
- AgrEmployment: Employment
- AgrEula: End User License Agreement
- AgrOther: Other
- AgrProduct: Product
- AgrSales: Sales

## AlgebraicStructureType — Algebraic Structure Type
- AsAbelianGroup: Abelian group: group with a commutative operation (parent: AsGroup)
- AsAdditiveInteger: Additive Abelian group of integers (Z, +) (parent: AsAbelianGroup)
- AsAdditiveReal: Additive Abelian group of real numbers (R, +) (parent: AsAbelianGroup)
- AsC2: Two-dimensional vector space C^2 over the field C (parent: AsVectorSpace)
- AsField: Field: commutative unital ring with 0 != 1 whose nonzero elements form an Abelian group under multiplication (parent: AsRing)
- AsGroup: Group: monoid in which every element has a two-sided inverse (parent: AsMonoid)
- AsIntegers: Ring of Integers (parent: AsRing)
- AsLoop: Loop: quasigroup with a two-sided identity element (parent: AsQuasigroup)
- AsMagma: Magma: carrier set equipped with a closed binary operation
- AsModule: Module: additive Abelian group equipped with scalar multiplication over a specified ring
- AsMonoid: Monoid: semigroup with a two-sided identity element (parent: AsSemigroup)
- AsQuasigroup: Quasigroup: magma in which every left and right division equation has a unique solution (parent: AsMagma)
- AsRationals: Field of Rational Numbers (parent: AsField)
- AsReals: Field of Real Numbers (parent: AsField)
- AsRing: Unital ring: additive Abelian group, multiplicative monoid, and distributive laws
- AsRn3: Three-dimensional vector space R^3 over the field R (parent: AsVectorSpace)
- AsSemigroup: Semigroup: associative magma (parent: AsMagma)
- AsVectorSpace: Vector space: module whose scalar ring is a specified field (parent: AsModule)
- AsZ3Group: Cyclic Abelian group of integers modulo 3 under addition (Z/3Z, +) (parent: AsAbelianGroup)
- AsZ5Field: Finite field of integers modulo 5 (Z/5Z) (parent: AsField)
- AsZ7Field: Field Z/7Z (Finite Field of Order 7) (parent: AsField)
- EuclideanSpace2D: 2D Euclidean Space (parent: VsEuclideanSpace)
- EuclideanSpace3D: 3D Euclidean Space (parent: VsEuclideanSpace)
- EuclideanSpaceND: N-dimensional real Euclidean space (parent: VsEuclideanSpace)
- QuaternionEuclideanSpace: Quaternion coordinates represented as the four-dimensional real Euclidean space R^4 (parent: VsEuclideanSpace)
- VsEuclideanSpace: Finite-dimensional real inner-product vector space (parent: AsVectorSpace)
- VsStateSpace: State space; its mathematical structure is defined by the selected model
- VsThermodynamicSpace: Thermodynamic state space; dimensionality and constraints are defined by the selected state variables and model (parent: VsStateSpace)

## ApproxFuncCodomainType — Approximated Function Codomain Type
- AfctMatrix: Matrix-valued function
- AfctScalar: Scalar-valued function
- AfctTensor: Tensor-valued function
- AfctVector: Vector-valued function

## ApproxFuncDataStorage — Approximated Function Data Storage
- AfdsExternal: External Blob, only for parametric paths and trajectories (CSV, GIS Shapefile, …)
- AfdsPointTable: Row-per-point Table
- AfdsTensor: Dense Tensor [N,3] or [N,D]

## ApproxFuncDerivativePurpose — Approximated Function Derivative Purpose
- AfdpBinormalMatrix: Third derivative matrix (e.g., rate of change of acceleration or binormal transformation).
- AfdpCurvatureTensor: Curvature tensor matrix. Represents curvature behavior for multiparameter paths or geometric domains.
- AfdpGeodesicCurvatureMatrix: Matrix form representing geodesic curvature on curved surfaces (i.e., deviation from intrinsic path).
- AfdpJerkTensor: High-order tensor for jerk (3rd derivative) with symbolic or multi-parameter domains.
- AfdpNormalMatrix: Second derivative matrix (e.g., Hessian or acceleration transformation).                 Describes how direction or velocity changes. Includes acceleration (∂²position/∂parameter², ∂²position/∂t²).
- AfdpOsculatingPlaneMatrix: Plane matrix spanned by tangent and normal vectors at the point (symbolic representation of the osculating plane).
- AfdpSnapMatrix: Fourth derivative matrix (snap-like linear transformation).                     Often used in smooth motion generation or symbolic modeling.
- AfdpSnapTensor: Symbolic or multi-axis matrix for 4th derivative behavior (snap-like change in acceleration direction).
- AfdpSurfaceNormalMatrix: Surface normal expressed as a matrix transformation (e.g., from tangent space to world space).
- AfdpTangentMatrix: First derivative matrix (e.g., Jacobian or directional velocity matrix).                  Includes geometric derivatives or velocity transformation (∂position/∂parameter, ∂position/∂t).
- AfdpTorsionTensor: Matrix representation of torsion or twisting behavior along the path (symbolic or 3D geometric interpretation).

## ApproxFuncInterpolation — Approximated Function Interpolation
- Afi5thDegPolyPath: Polynomial of 5th Degree Path (parent: AfiPolyPath)
- Afi7thDegPolyPath: Polynomial of Degree Seven Path (parent: AfiPolyPath)
- AfiAIPath: AI-Optimized Path (parent: AfiAdaptivePath)
- AfiAdaptivePath: Adaptive Learning-Based Path
- AfiApproxCubicSplinesPath: Approximated Cubic Splines Path (parent: AfiApproxPath)
- AfiApproxOrthogonalPolyPath: Approximated Orthogonal Polynomials Path (parent: AfiApproxPath)
- AfiApproxPath: Multipoint Approximated Path (parent: AfiMultipointPath)
- AfiApproxPolyPath: Approximated Polynomial Path (parent: AfiApproxPath)
- AfiApproxTrigPolynomialPath: Approximated Trigonometric Polynomial Path (parent: AfiApproxPath)
- AfiAsymmetricPath: Path with Asymmetric Constant Acceleration (parent: AfiPolyPath)
- AfiBSplinePath: B-Spline Path (parent: AfiInterpPath)
- AfiBezierPath: Bézier (Bernstein Basis) Curve Path  (parent: AfiInterpPath)
- AfiCatmullRomSpline: Catmull-Rom Spline Curve Path  (parent: AfiInterpPath)
- AfiCubicPath: Cubic Path (parent: AfiPolyPath)
- AfiCycloidalPath: Cycloidal Path (parent: AfiTrigPath)
- AfiEllipticPath: Elliptic Path (parent: AfiTrigPath)
- AfiExpPath: Exponential Path (parent: AfiP2PPath)
- AfiFourierSeriesExpansionPath: Path Based on the Fourier Series Expansion (parent: AfiP2PPath)
- AfiFreudensteinPath: Freudenstein Path (parent: AfiFourierSeriesExpansionPath)
- AfiGutmanPath: Gutman Path (parent: AfiFourierSeriesExpansionPath)
- AfiHarmonicPath: Harmonic Path (parent: AfiTrigPath)
- AfiHermiteSpline: Hermite Spline Curve Path  (parent: AfiInterpPath)
- AfiHighDegPolyPath: Polynomial of Higher Degree Path (parent: AfiPolyPath)
- AfiInterpCubicSplinesPath: Interpolated Cubic Splines Path (parent: AfiInterpPath)
- AfiInterpOrthogonalPolyPath: Interpolated Orthogonal Polynomials Path (parent: AfiInterpPath)
- AfiInterpPath: Multipoint Interpolated Path (parent: AfiMultipointPath)
- AfiInterpPolyPath: Interpolated Polynomial Path (parent: AfiInterpPath)
- AfiInterpTrigPolyPath: Interpolated Trigonometric Polynomial Path (parent: AfiInterpPath)
- AfiLagrangePolynomial: Lagrange Polynomial Curve Path  (parent: AfiInterpPath)
- AfiLearningPath: Reinforcement Learning Path (parent: AfiAdaptivePath)
- AfiLinearPath: Linear Path (constant velocity) (parent: AfiPolyPath)
- AfiMultipointPath: Multipoint Path
- AfiNurbsPath: NURBS (Rational B-Spline) Path (parent: AfiInterpPath)
- AfiP2PPath: Point-to-Point Path
- AfiParabolicPath: Parabolic Path (constant acceleration) (parent: AfiPolyPath)
- AfiPiecewise: Linear (Piecewise) Curve Path  (parent: AfiInterpPath)
- AfiPolyPath: Polynomial Path (parent: AfiP2PPath)
- AfiTrigPath: Trigonometric Path (parent: AfiP2PPath)

## ApproxFuncPurpose — Approximated Function Purpose
- AfpGeometricCurve: Geometric Curve
- AfpMachineMotion: Automatic Machine Motion (parent: AfpTrajectory)
- AfpNumericalFunction: Numerical Function
- AfpRobotMotion: Robot Motion (parent: AfpTrajectory)
- AfpThermodynamics: Thermodynamics Process
- AfpTrajectory: Trajectory

## ApproxFuncSampleType — Approximated Function Sample Type
- AfstArcEnd: Arc End
- AfstArcStart: Arc Start
- AfstBreakPoint: Break Point
- AfstCalculatedPoint: Calculated or Derived Point
- AfstControlPoint: Control Point
- AfstCorner: Corner Point
- AfstDeviationPoint: Deviation Point (parent: AfstTemporaryPoint)
- AfstEmergencyStopPoint: Emergency Stop Point
- AfstEndPoint: End Point
- AfstInspectionPoint: Inspection Point
- AfstSafetyStopPoint: Safety Stop Point (parent: AfstTemporaryPoint)
- AfstSampledPoint: Sampled Point
- AfstStartPoint: Start Point
- AfstTemporaryPoint: Temporary Point
- AfstWaypoint: Waypoint 

## ArtifactType — Artifact Types
- AT_ENTITY: Entity
- AT_LLM: LLM
- AT_OTHER: Other
- AT_REST_PATH: REST API Path
- AT_SERVICE: Service
- AT_XML_SCREEN: Screen
- AT_XML_SCREEN_CONTENT: Screen Content
- AT_XML_SCREEN_TRANS: Screen Transition

## AssetClass — Asset Class
- AsClsBoat: Boat
- AsClsCargoVehicle: Cargo Vehicle
- AsClsCompressor: Compressor
- AsClsComputerHard: Computer Hardware
- AsClsComputerSoft: Computer Software
- AsClsContainer: Container (parent: AsClsCargoVehicle)
- AsClsDesktop: Desktop (parent: AsClsComputerHard)
- AsClsDigger: Digger
- AsClsForklift: Forklift
- AsClsInventory: Inventory
- AsClsInventoryDig: Inventory - Digital Good (parent: AsClsInventory)
- AsClsInventoryFin: Inventory - Finished Good (parent: AsClsInventory)
- AsClsInventoryRaw: Inventory - Raw Material (parent: AsClsInventory)
- AsClsInventorySub: Inventory - Sub-assembly (parent: AsClsInventory)
- AsClsLaptop: Laptop (parent: AsClsComputerHard)
- AsClsManlift: Manlift
- AsClsMfgEquip: Manufacturing Equipment
- AsClsMonitor: Monitor (parent: AsClsComputerHard)
- AsClsPassengerVeh: Passenger Vehicle
- AsClsPuller: Puller
- AsClsReelStand: Reel Stand
- AsClsServiceBody: Service Body
- AsClsSoftApp: Application Software (parent: AsClsComputerSoft)
- AsClsSoftProgramming: Programming Software (parent: AsClsComputerSoft)
- AsClsSoftSystem: System Software (parent: AsClsComputerSoft)
- AsClsSoftUtility: Utility Software (parent: AsClsComputerSoft)
- AsClsTablet: Tablet (parent: AsClsComputerHard)
- AsClsTanker: Tanker
- AsClsTractor: Tractor
- AsClsTrailer: Trailer (parent: AsClsCargoVehicle)
- AsClsTrencher: Trencher
- AsClsTruck: Truck (parent: AsClsCargoVehicle)
- AsClsWhEquip: Warehouse Equipment

## AssetIdentificationType — Asset Identification Type
- AitGasCard: Gas Card Number
- AitLicensePlate: License Plate Number
- AitMac: Media Access Control (MAC) Address
- AitMfgSerial: Manufacturer Serial Number
- AitTrackingLabel: Tracking Label Number
- AitVendorInventory: Vendor Inventory/Tracking
- AitVin: Vehicle Identification Number (VIN)

## AssetPaymentMethodType — Asset Payment Method Type
- ApmtSecuredLoan: Secured Loan

## AssetReservationAuto — Asset Auto Reservation
- AsResAutoApproved: On Order Approved
- AsResAutoNone: No Auto Reserve
- AsResAutoPlaced: On Order Placed

## AssetReservationOrder — Asset (Inventory) Reservation Order
- AsResOrdCostGr: Greatest Unit Cost
- AsResOrdCostLw: Lowest Unit Cost
- AsResOrdFifoExp: FIFO Expire
- AsResOrdFifoRec: FIFO Receive
- AsResOrdLifoExp: LIFO Expire
- AsResOrdLifoRec: LIFO Receive
- AsResOrdNoRes: No Reservation

## AssetType — Asset Type
- AstTpBearerBiological: Bearer Biological (parent: AstTpFixed)
- AstTpBiological: Biological
- AstTpEquipment: Equipment (parent: AstTpFixed)
- AstTpFixed: Fixed Asset
- AstTpIntangible: Intangible
- AstTpInvRealEstate: Investment Real Estate (parent: AstTpFixed)
- AstTpInventory: Inventory
- AstTpRealEstate: Real Estate (parent: AstTpFixed)
- AstTpRental: Rental Equipment Asset (parent: AstTpFixed)
- AstTpSupplies: Supplies

## AuthzAction — Authorization Action
- AUTHZA_ALL: All
- AUTHZA_CREATE: Create
- AUTHZA_DELETE: Delete
- AUTHZA_UPDATE: Update
- AUTHZA_VIEW: View

## AuthzType — Authorization Type
- AUTHZT_ALLOW: Allow
- AUTHZT_ALWAYS: Always Allow (overrides Deny)
- AUTHZT_DENY: Deny (overrides Allow)

## BankAccountType — Bank Account Type
- BatCertDep: Certificate of Deposit
- BatChecking: Checking
- BatCreditInstallment: Credit Installment
- BatCreditOpen: Credit Open
- BatCreditRevolving: Credit Revolving
- BatCreditSecured: Credit Secured
- BatMoneyMarket: Money Market
- BatRetirement: Retirement
- BatSavings: Savings

## BooleanYN — Boolean (Yes/No)
- BlN: No
- BlY: Yes

## BudgetItemType — Budget Item Type
- BdgItDiscretionary: Discretionary
- BdgItRequired: Required

## BudgetType — Budget Type
- BudgetCapital: Capital
- BudgetOperating: Operating

## CategoryConstructionType — Category Construction Type
- CcArrow: Arrow category
- CcCoslice: Coslice category
- CcFree: Free category on a graph
- CcFunctorCategory: Functor category [C,D]
- CcOpposite: Opposite category
- CcProduct: Product category
- CcQuotient: Quotient category by a congruence
- CcSlice: Slice category

## CategoryObjectType — Category Object Type
- CotAbGroup: Abelian group (parent: CotGroup)
- CotAlgebraicStruct: Algebraic Structure (one-object category)
- CotContext: Typing Context
- CotField: Field (parent: CotAlgebraicStruct)
- CotGeneric: Generic object
- CotGroup: Group (parent: CotAlgebraicStruct)
- CotModule: Module (parent: CotAlgebraicStruct)
- CotMonoid: Monoid (parent: CotAlgebraicStruct)
- CotOperationalState: Operational State Specification (parent: CotSpecification)
- CotProposition: Proposition as Type (parent: CotType)
- CotRing: Ring (parent: CotAlgebraicStruct)
- CotSpecification: Specification or Observable Predicate (parent: CotProposition)
- CotType: Type
- CotUniverse: Universe of Types (parent: CotType)

## CategoryType — Category Type
- CtAb: Abelian Groups and Homomorphisms
- CtAbelian: Abelian category
- CtCCC: Cartesian-closed category
- CtCat: Big Category of Small Categories + Functors
- CtDiscrete: Discrete category
- CtEnriched: Enriched (V-) category
- CtFinSet: Finite sets
- CtGroupoid: Groupoid
- CtGrp: Category of Groups and Group Homomorphisms
- CtLCCC: Locally Cartesian-closed category for dependent types
- CtLarge: Large category
- CtMonoidal: Monoidal category
- CtPoset: Poset viewed as category
- CtPreAdditive: Pre-additive category
- CtSet: Category of small sets: objects = sets, morphisms = functions
- CtSmall: Small / finite category
- CtSyntactic: Syntactic category of a type theory
- CtTop: Topological Spaces with Continuous Maps
- CtTopos: Topos
- CtVectC: Complex Vector Spaces (finite dimension) with Linear Maps
- CtVectR: Real Vector Spaces (finite dimension) with Linear Maps

## CogsMethod — COGS Method
- CogsActualCost: Inventory Actual Cost
- CogsAverageCost: Average Cost
- CogsFifo: FIFO
- CogsLifo: LIFO

## CommunicationContentType — Communication Content Type
- CmctAttachment: Attachment
- CmctHtmlText: HTML Text
- CmctPlainText: Plain Text

## CommunicationPurpose — Communication Purpose
- CpActivityRequest: Activity Request
- CpBilling: Billing
- CpComment: Comment
- CpConference: Conference
- CpCustomerService: Customer Service
- CpCustomerSupport: Customer Support
- CpMeeting: Meeting
- CpSalesFollowUp: Sales Follow-Up
- CpSalesInquiry: Sales Inquiry
- CpSeminar: Seminar
- CpShipments: Shipments

## ComparisonOperator — Entity Comparison Operator
- ENTCO_BETWEEN: between
- ENTCO_EQUALS: equals
- ENTCO_GREATER: greater
- ENTCO_GREATER_EQ: greater-equals
- ENTCO_IN: in
- ENTCO_IS_NOT_NULL: is-not-null
- ENTCO_IS_NULL: is-null
- ENTCO_LESS: less
- ENTCO_LESS_EQ: less-equals
- ENTCO_LIKE: like
- ENTCO_NOT_BETWEEN: not-between
- ENTCO_NOT_EQUALS: not-equals
- ENTCO_NOT_IN: not-in
- ENTCO_NOT_LIKE: not-like

## ContactListEmailType — Contact List Email Type
- CONT_EMAIL_TEMPLATE: Outgoing Email
- CONT_SUB_NOT: Subscribe Notification
- CONT_UNSUB_NOT: Unsubscribe Notification
- CONT_UNSUB_VER: Unsubscribe Verify

## ContactListType — Contact List Type
- ANNOUNCEMENT: Announcement
- MARKETING: Marketing
- NEWSLETTER: Newsletter

## ContactMechType — Contact Mechanism Type
- CmtDomainName: Internet Domain Name (parent: CmtElectronicAddress)
- CmtElectronicAddress: Electronic Address
- CmtEmailAddress: Email Address (parent: CmtElectronicAddress)
- CmtIpAddress: Internet IP Address (parent: CmtElectronicAddress)
- CmtPostalAddress: Postal Address
- CmtTelecomNumber: Phone Number
- CmtWebAddress: Web URL/Address (parent: CmtElectronicAddress)
- CmtWebForm: Web Form (parent: CmtElectronicAddress)

## ContactPaymentTrustLevel — Contact/Payment Trust Level
- CmtlBlacklisted: Blacklisted
- CmtlGreylisted: Greylisted
- CmtlIncomplete: Incomplete
- CmtlInvalid: Invalid
- CmtlNew: New Data
- CmtlValid: Valid/Complete
- CmtlVerified: Verified

## ContainerType — Container Type
- CtBinShelf: Bin - Shelf Std
- CtContainerIso20: Container ISO 20ft
- CtContainerIso40: Container ISO 40ft
- CtPalletEur3: Pallet EUR3 1.0x1.2m
- CtPalletIso0: Pallet ISO0/EUR6 0.8x0.6m
- CtPalletIso1: Pallet ISO1/EUR1 0.8x1.2m
- CtPalletIso2: Pallet ISO2/EUR2 1.2x1.0m
- CtPalletUs4040: Pallet US 40x40in
- CtPalletUs4048: Pallet US 40x48in
- CtPalletUs4242: Pallet US 42x42in
- CtPalletUs4840: Pallet US 48x40in
- CtPalletUs4848: Pallet US 48x48in

## CoordinateSystemPurpose — Coordinate System Purpose
- CspBase: Base Coordinate System
- CspCamera: Camera Coordinate System
- CspMachine: Machine Coordinate System
- CspMechanicalInterface: Mechanical Interface Coordinate System
- CspMobilePlatform: Mobile Platform Coordinate System
- CspObject: Object Coordinate System
- CspTask: Task Coordinate System
- CspTool: Tool Coordinate System
- CspWorld: World Coordinate System

## CoordinateSystemType — Coordinate System Type
- CstCartesian: Cartesian (Rectangular) Coordinate System
- CstCurvilinear: Curvilinear Coordinate System
- CstCylindrical: Cylindrical Coordinate System
- CstHomogeneous: Homogeneous Coordinate System
- CstPolar: Polar Coordinate System
- CstSpherical: Spherical Coordinate System

## CreditCardType — Credit Card Type
- CctAmericanExpress: American Express
- CctDiscover: Discover
- CctMastercard: Master Card
- CctVisa: Visa

## CustomsContents — Customs Contents Type
- CcntDocuments: Documents
- CcntDonation: Humanitarian Donation
- CcntGift: Gift
- CcntMerchandise: Merchandise
- CcntOther: Other
- CcntReturnMerch: Return Merchandise
- CcntSample: Sample

## CustomsNonDelivery — Customs Non Delivery
- CndAbandon: Abandon
- CndReturn: Return

## DataFeedType — Data Feed Type
- DTFDTP_MAN_PULL: Manual Pull (through API)
- DTFDTP_RT_PUSH: Real-time Service Push

## DataSourceType — Data Source Type
- CAMPAIGN: Campaign (parent: LEAD_SOURCE)
- COLD_CALL: Cold Call (parent: LEAD_SOURCE)
- CONFERENCE: Conference (parent: LEAD_SOURCE)
- DIRECT_MAIL: Direct Mail (parent: LEAD_SOURCE)
- DST_CUSTOMER_ENTRY: Customer Data Entry
- DST_INTERNAL_ENTRY: Internal Data Entry (employees, etc)
- DST_MAILING_SIGNUP: Mailing List Sign-up
- DST_PURCHASED_DATA: Purchased Data
- EMAIL: Email (parent: LEAD_SOURCE)
- EMPLOYEE: Employee (parent: LEAD_SOURCE)
- EXISTING_CUSTOMER: Existing Customer (parent: LEAD_SOURCE)
- LEAD_SOURCE: Lead Source
- OTHER: Other (parent: LEAD_SOURCE)
- PARTNER: Partner (parent: LEAD_SOURCE)
- PUBLIC_RELATIONS: Public Relations (parent: LEAD_SOURCE)
- SELF_GENERATED: Self Generated (parent: LEAD_SOURCE)
- TRADE_SHOW: Trade Show (parent: LEAD_SOURCE)
- WEB_SITE: Web Site (parent: LEAD_SOURCE)
- WORD_OF_MOUTH: Word of Mouth (parent: LEAD_SOURCE)

## DayOfWeek — Day of Week
- DowFriday: Friday
- DowMonday: Monday
- DowSaturday: Saturday
- DowSunday: Sunday
- DowThursday: Thursday
- DowTuesday: Tuesday
- DowWednesday: Wednesday

## DbFormFieldType — DB Form Field Type
- DBFFT_check: check
- DBFFT_date-find: date-find
- DBFFT_date-time: date-time
- DBFFT_display: display
- DBFFT_display-entity: display-entity
- DBFFT_drop-down: drop-down
- DBFFT_file: file
- DBFFT_hidden: hidden
- DBFFT_ignored: ignored
- DBFFT_image: image
- DBFFT_label: label
- DBFFT_link: link
- DBFFT_password: password
- DBFFT_radio: radio
- DBFFT_range-find: range-find
- DBFFT_reset: reset
- DBFFT_submit: submit
- DBFFT_text-area: text-area
- DBFFT_text-find: text-find
- DBFFT_text-line: text-line

## DbFormPurpose — DB Form Purpose
- DbfpOther: Other
- DbfpSurvey: Survey
- DbfpTaxStatement: Tax Statement

## DepreciationType — Depreciation Type
- DtpDoubleDeclining: Double Declining Balance
- DtpStraightLine: Straight Line
- DtpSumYearsDigits: Sum of Years Digits

## DeviceConfigPurpose — Device Configuration Purpose
- DcpDeviceConfig: Device Configuration
- DcpEmergencyCheck: Check Device Emergency (parent: DcpValidationRule)
- DcpEmergencyConfig: Emergency Device Configuration (parent: DcpDeviceConfig)
- DcpFaultCheck: Check Device Fault (parent: DcpValidationRule)
- DcpFaultConfig: Fault Device Configuration (parent: DcpDeviceConfig)
- DcpPrototypeConfig: Prototype Device Configuration (parent: DcpDeviceConfig)
- DcpRunConfig: Production or Run Device Configuration (parent: DcpDeviceConfig)
- DcpSafetyConfig: Safety Device Configuration (parent: DcpDeviceConfig)
- DcpTestConfig: Test Device Configuration (parent: DcpDeviceConfig)
- DcpValidationRule: Validation Rules

## DeviceConfigType — Device Configuration Type
- DctApplyConfig: Apply Configuration (parent: DctDeviceConfig)
- DctAssertConfig: Assert Configuration (parent: DctDeviceConfig)
- DctDeviceConfig: Device Configuration

## DeviceConnectionDriver — Device Connection Driver
- DcdBACnetIP: BACnet/IP
- DcdCANopen: CANopen
- DcdEthernetIP: Ethernet/IP
- DcdKNXnetIP: KNXnet/IP
- DcdLogixCIPEIP: Logix CIP/EIP
- DcdMockDriver: Mock Driver
- DcdModbusTCP: Modbus TCP
- DcdMtConnect: MTConnect
- DcdOpcUa: Opc Ua
- DcdProfinet: Profinet
- DcdSiemensS7: Siemens S7
- DcdSimulated: Simulated Plc4x Datasource

## DeviceConnectionPurpose — Device Connection Purpose
- DcpDiagnostics: Diagnostics
- DcpMaintenance: Maintenance
- DcpOperations: Operations

## DeviceConnectionTransport — Device Connection Transport
- DctrMoquiMock: Moqui Mock Connection
- DctrPcap: PCAP File Replay
- DctrRaw: Raw Socket Communication
- DctrSerial: Serial Port
- DctrSocketCan: SocketCAN (software bridge to CAN)
- DctrTcp: TCP Socket Communication
- DctrUdp: UDP Socket Communication

## DeviceConnectionType — Device Connection Type
- DctConvertedConnection: Converted Connection
- DctDirectConnection: Direct Connection

## DeviceContentType — Device Content Type
- DCnt3dsFile: 3DS Autodesk File (parent: DCntCadFile)
- DCntAcisFile: ACIS Dassault File (parent: DCntCadFile)
- DCntCadFile: CAD File (parent: DCntSolidModel)
- DCntCaeFile: CAE File (parent: DCntSolidModel)
- DCntCamFile: CAM File (parent: DCntSolidModel)
- DCntCncProgram: CNC Program
- DCntColladaFile: COLLADA ISO 17506 File (parent: DCntCadFile)
- DCntConfiguration: Configuration
- DCntFirmware: Firmware
- DCntGCodeFile: G-Code File
- DCntGdmlFile: GDML Geometry Description Markup Language File (parent: DCntCadFile)
- DCntIgesFile: IGES Initial Graphics Exchange Specification File (parent: DCntCadFile)
- DCntImage: Device Image
- DCntMotionLawCsvFile: Motion Law CSV file (parent: DCntTrajectory)
- DCntObjFile: OBJ Wavefront OBJ File (parent: DCntCadFile)
- DCntPlcProgram: PLC Program
- DCntRobotProgram: Robot Program
- DCntSensorConfiguration: Sensor Configuration (parent: DCntConfiguration)
- DCntSoftwareApplication: Software Application
- DCntSolidModel: Solid Model
- DCntSpecification: Device Specification
- DCntStepFile: STEP ISO 10303 STEP AP203 or AP242 File (parent: DCntCadFile)
- DCntStlFile: STL STereoLithography File (parent: DCntCadFile)
- DCntTrajectory: Trajectory
- DCntXtFile: X_T Parasolid XT Siemens Data Interchange File (parent: DCntCadFile)

## DeviceControlMethod — Device Control Method
- DcmAdaptiveControl: Adaptive Control Method
- DcmBacksteppingControl: Backstepping Control (parent: DcmNonlinearControl)
- DcmClassicalControl: Classical Control Method
- DcmDDPC: Data-Driven Predictive Control (DDPC) (parent: DcmDataDrivenControl)
- DcmDataDrivenControl: Data-Driven Method
- DcmDoubleActuationDoubleFeedback: Double Actuation Double Feedback (parent: DcmNone)
- DcmDoubleActuationNoRetain: Double Actuation No Retain (parent: DcmNone)
- DcmESC: Extremum Seeking Control (ESC) (parent: DcmDataDrivenControl)
- DcmFeedbackLinearization: Feedback Linearization (parent: DcmNonlinearControl)
- DcmFuzzyLogicControl: Fuzzy Logic Control (parent: DcmICM)
- DcmHInfinityControl: H-Infinity (H∞) Control (parent: DcmRobustControl)
- DcmICM: Intelligent Control Method
- DcmILC: Iterative Learning Control (ILC) (parent: DcmDataDrivenControl)
- DcmIPID: Intelligent PID (iPID) (parent: DcmDataDrivenControl)
- DcmLQG: Linear Quadratic Gaussian (LQG) (parent: DcmOptimalControl)
- DcmLQR: Linear Quadratic Regulator (LQR) (parent: DcmOptimalControl)
- DcmLeadLagCompensation: Lead-Lag Compensation (parent: DcmClassicalControl)
- DcmLyapunovBasedControl: Lyapunov-Based Control (parent: DcmNonlinearControl)
- DcmMFAC: Model-Free Adaptive Control (MFAC) (parent: DcmDataDrivenControl)
- DcmMPC: Model Predictive Control (MPC) (parent: DcmOptimalControl)
- DcmModelReferenceAdaptiveControl: Model Reference Adaptive Control (MRAC) (parent: DcmAdaptiveControl)
- DcmMuSynthesis: µ-Synthesis (Mu-Synthesis) (parent: DcmAdaptiveControl)
- DcmNeuralNetworkControl: Neural Network Control (parent: DcmICM)
- DcmNoActuationSingleFeedback: No Actuation Single Feedback (parent: DcmNone)
- DcmNone: None
- DcmNonlinearControl: Nonlinear Control Method
- DcmOpenLoopControl: Open Loop Control (parent: DcmClassicalControl)
- DcmOptimalControl: Optimal Control Method
- DcmPControl: P (Proportional) Control (parent: DcmClassicalControl)
- DcmPDControl: PD (Proportional-Derivative) Control (parent: DcmClassicalControl)
- DcmPIControl: PI (Proportional-Integral) Control (parent: DcmClassicalControl)
- DcmPIDControl: PID (Proportional-Integral-Derivative) Control (parent: DcmClassicalControl)
- DcmPolePlacementControl: Pole-Placement Control (parent: DcmClassicalControl)
- DcmRLControl: Reinforcement Learning (RL) Control (parent: DcmICM)
- DcmRobustControl: Robust Control Method
- DcmSTR: Self-Tuning Regulators (STR) (parent: DcmAdaptiveControl)
- DcmSingleActuationDisableFeedback: Single Actuation Disable Feedback (parent: DcmNone)
- DcmSingleActuationDoubleFeedback: Single Actuation Double Feedback (parent: DcmNone)
- DcmSingleActuationEnableFeedback: Single Actuation Enable Feedback (parent: DcmNone)
- DcmSingleActuationNoFeedback: Single Actuation No Feedback (parent: DcmNone)
- DcmSlidingModeControl: Sliding Mode Control (SMC) (parent: DcmRobustControl)
- DcmVRFT: Virtual Reference Feedback Tuning (VRFT) (parent: DcmDataDrivenControl)

## DeviceDashboardPurpose — Device Dashboard Purpose
- DdpLogging: Logging Dashboard
- DdpMetrics: Metrics Dashboard
- DdpReporting: Reporting
- DdpSummary: Summary Dashboard
- DdpTracing: Tracing Dashboard

## DeviceEventHandler — Device Event Handler
- DehMoqui: Moqui Handled
- DehPLC: PLC Handled

## DeviceEventSeverity — Device Event Severity
- DesCritical: Critical Fault
- DesInfo: Information
- DesWarning: Soft Warning

## DeviceEventType — Device Event Type
- DetBootEvent: Boot Event (parent: DetLifecycleEvent)
- DetDeviceGroupEvent: Device Group Event
- DetDeviceMembershipEvent: Device Membership Event
- DetFailure: Device Failure Event (parent: DetPhysicalDeviceEvent)
- DetLifecycleEvent: Device Lifecycle Event
- DetMembership: Device Membership Event (parent: DetPhysicalDeviceEvent)
- DetPhysicalDeviceEvent: Physical Device Event
- DeviceAfterReadingInputsEvent: After Reading Inputs Event (parent: DetLifecycleEvent)
- DeviceAfterWritingOutputsEvent: After Writing Outputs Event (parent: DetLifecycleEvent)
- DeviceBeforeReadingInputsEvent: Before Reading Inputs Event (parent: DetLifecycleEvent)
- DeviceBeforeWritingOutputsEvent: Before Writing Outputs Event (parent: DetLifecycleEvent)
- DeviceContentUpdateEvent: Content Update Event (parent: DetLifecycleEvent)
- DeviceDownloadDataEvent: Download Data Event (parent: DetLifecycleEvent)
- DeviceEntityUpdateEvent: Device Entity Update Event (parent: DetLifecycleEvent)
- DeviceLeaderElectionEvent: Device Leader Election Event (parent: DetDeviceMembershipEvent)
- DeviceLogEventCollectionEvent: Log Collection Toggle Event (parent: DetLifecycleEvent)
- DeviceLoginEvent: Login Event (parent: DetLifecycleEvent)
- DeviceLogoutEvent: Logout Event (parent: DetLifecycleEvent)
- DeviceMeasurementCollectionEvent: Measurement Collection Toggle Event (parent: DetLifecycleEvent)
- DeviceMemberAddedEvent: Device Member Added Event (parent: DetDeviceMembershipEvent)
- DeviceMemberRemovedEvent: Device Member Removed Event (parent: DetDeviceMembershipEvent)
- DeviceNotificationMessageCollectionEvent: Notification Message Collection Toggle Event (parent: DetLifecycleEvent)
- DeviceParameterEntityUpdateEvent: Parameter Entity Update Event (parent: DetLifecycleEvent)
- DevicePrepareDownloadDataEvent: Prepare Download Data Event (parent: DetLifecycleEvent)
- DevicePrepareResetEvent: Prepare Reset Event (parent: DetLifecycleEvent)
- DevicePrepareSetupEvent: Prepare Setup or Upgrade Event (parent: DetLifecycleEvent)
- DevicePrepareShutdownEvent: Prepare Shutdown Event (parent: DetLifecycleEvent)
- DevicePrepareStartEvent: Prepare Start Event (parent: DetLifecycleEvent)
- DevicePrepareStopEvent: Prepare Stop Event (parent: DetLifecycleEvent)
- DeviceRebootEvent: Reboot Event (parent: DetLifecycleEvent)
- DeviceResetEvent: Reset Event (parent: DetLifecycleEvent)
- DeviceSetupEvent: Setup or Upgrade Event (parent: DetLifecycleEvent)
- DeviceShutdownEvent: Shutdown Event (parent: DetLifecycleEvent)
- DeviceStartEvent: Start Event (parent: DetLifecycleEvent)
- DeviceStatusFlowEntityUpdateEvent: Status Flow Entity Update Event (parent: DetLifecycleEvent)
- DeviceStopEvent: Stop Event (parent: DetLifecycleEvent)
- DgetFailure: Device Group Failure Event (parent: DetDeviceGroupEvent)
- DgetLifecycle: Device Group Lifecycle Event (parent: DetDeviceGroupEvent)

## DeviceGroupMemberPurpose — Device Group Member Purpose
- DgmpAccelerator: Compute Accelerator (parent: DgmpClusterMember)
- DgmpAxis: Axis
- DgmpClusterManager: Cluster Manager
- DgmpClusterMember: Cluster Member
- DgmpClusterMemberPrimary: Cluster Member Primary (parent: DgmpClusterMember)
- DgmpClusterMemberSecondary: Cluster Member Secondary (parent: DgmpClusterMember)
- DgmpControlPlane: Control Plane (parent: DgmpClusterManager)
- DgmpControlledDevice: Controlled Device
- DgmpController: Controller
- DgmpDataPlane: Data Plane (parent: DgmpClusterMember)
- DgmpDrive: Drive
- DgmpEdgeGateway: Edge Gateway
- DgmpEmbeddingProvider: Embedding Provider (parent: DgmpDataPlane)
- DgmpEnergyMeter: Energy Meter (parent: DgmpMonitoringDevices)
- DgmpExtremeConditionRemoteIO: Extreme Condition Remote IO (parent: DgmpRemoteIO)
- DgmpFollowerDrive: Follower Drive (parent: DgmpDrive)
- DgmpFollowerServoDrive: Follower Servo Drive (parent: DgmpServoDrive)
- DgmpGpuWorker: GPU Worker (parent: DgmpAccelerator)
- DgmpInferenceReplica: Inference Replica (parent: DgmpClusterMember)
- DgmpMasterAxis: Master Axis (parent: DgmpAxis)
- DgmpMasterDrive: Master Drive (parent: DgmpDrive)
- DgmpMasterServoDrive: Master Servo Drive (parent: DgmpServoDrive)
- DgmpMonitoringDevices: Monitoring Devices
- DgmpMotionController: Motion Controller (parent: DgmpController)
- DgmpNetworkAnalyzer: Network Analyzer (parent: DgmpMonitoringDevices)
- DgmpNetworkMultimeter: Network Multimeter (parent: DgmpMonitoringDevices)
- DgmpProcessPLC: Process PLC (parent: DgmpController)
- DgmpRagRuntime: RAG Runtime (parent: DgmpDataPlane)
- DgmpRemoteIO: Remote IO
- DgmpSafetyPLC: Safety PLC (parent: DgmpController)
- DgmpSafetyRemoteIO: Safety Remote IO (parent: DgmpRemoteIO)
- DgmpServoDrive: Servo Drive
- DgmpSlaveAxis: Slave Axis (parent: DgmpAxis)
- DgmpSubsystem: Subsystem
- DgmpTpuWorker: TPU Worker (parent: DgmpAccelerator)
- DgmpTrainingWorker: Training Worker (parent: DgmpClusterMember)
- DgmpVectorIndexNode: Vector Index Node (parent: DgmpDataPlane)
- DgmpVirtualAxis: Virtual Axis (parent: DgmpAxis)

## DeviceOperatingMode — Device Operating Mode
- DomInit: Init
- DomRun: Run
- DomSimulation: Simulation
- DomTest: Test

## DevicePurpose — Device Purpose
- DepAIInference: AI Inference (parent: DepGPUBasedComputing)
- DepAITraining: AI Training (parent: DepHPCComputing)
- DepAhuFanControl: AHU Fan Control (parent: DepFanControl)
- DepBlowerFanControl: Blower Fan Control (parent: DepFanControl)
- DepCentrifugalSeparatorControl: Centrifugal Separator Control
- DepCentrifugeControl: Centrifuge Control
- DepCncControl: CNC Control
- DepColdPumpControl: Cold Pump Control (parent: DepPumpControl)
- DepCompressorControl: Compressor Control
- DepComputing: Computing
- DepCondenserControl: Condenser Control (parent: DepFanControl)
- DepConveyorControl: Conveyor Control
- DepCoolingTowerControl: Cooling Tower Control (parent: DepFanControl)
- DepCraneControl: Crane Control
- DepCrusherControl: Crusher Control
- DepDeckMachineryControl: Deck Machinery Control
- DepElevatorControl: Elevator Control
- DepEmbeddingGeneration: Embedding Generation (parent: DepAIInference)
- DepFanControl: Fan Control
- DepGPUBasedComputing: GPU Based Computing
- DepGpuAcceleration: GPU Acceleration (parent: DepGPUBasedComputing)
- DepHPCComputing: HPC Computing
- DepHardRealTimeComputing: Hard Real-Time Computing
- DepHeatPumpControl: Heat Pump Control (parent: DepPumpControl)
- DepHoistControl: Hoist Control
- DepMillingControl: Milling Control
- DepMixerControl: Mixer Control
- DepModelServing: Model Serving (parent: DepAIInference)
- DepMotorControl: Motor Control
- DepNetworkControl: Network Control
- DepOffshoreWinchControl: Offshore Winch Control
- DepProcessControl: Process Control
- DepProtectionControl: Protection Control
- DepPumpControl: Pump Control
- DepRagRetrieval: RAG Retrieval (parent: DepAIInference)
- DepRobotControl: Robot Control
- DepSecurityControl: Security Control
- DepServoMotorControl: Servo Motor Control
- DepShredderControl: Shredder Control
- DepSoftRealTimeComputing: Soft Real-Time Computing
- DepSolarPumpControl: Solar Pump Control (parent: DepPumpControl)
- DepStorage: Storage
- DepStreamProcessingComputing: Stream Processing Computing
- DepTpuAcceleration: TPU Acceleration (parent: DepHPCComputing)
- DepTransportSystemsControl: Transport Systems Control
- DepVectorSearch: Vector Search (parent: DepAIInference)
- DepWaterPumpControl: Water Pump Control (parent: DepFanControl)

## DeviceRequestItemType — Device Request Item Type
- DritBit: Bit
- DritBool: Bool
- DritByte: Byte
- DritDInt: Double Integer
- DritDWord: Double Word
- DritInt: Integer
- DritLInt: Long Integer
- DritLReal: Long Real
- DritLWord: Long Word
- DritReal: Real
- DritSInt: Short Integer
- DritUDInt: Unsigned Double Integer
- DritUInt: Unsigned Integer
- DritULInt: Unsigned Long Integer
- DritUSInt: Unsigned Short Integer
- DritWord: Word

## DeviceRequestPurpose — Device Request Purpose
- DrpCommissioning: Commissioning/Parametrization
- DrpControl: Control
- DrpDiagnostics: Diagnostics
- DrpFirmware: Firmware Upgrade
- DrpLogging: Logging / Telemetry (parent: DrpMonitoring)
- DrpMonitoring: Monitoring
- DrpStatusMonitoring: Status Monitoring (parent: DrpMonitoring)

## DeviceRequestRouter — Device Request Router
- DrrAMQPBroker: AMQP Broker (parent: DrrBroker)
- DrrBroker: Broker
- DrrDirect: Direct (Profinet / Modbus TCP/ EthernetIP /OPC UA / ...)
- DrrKafka: Kafka (parent: DrrBroker)
- DrrMQTTBroker: MQTT Broker (parent: DrrBroker)
- DrrMoquiDeviceGateway: Moqui Device Gateway (external Camel/Quarkus process)
- DrrSTOMPBroker: STOMP Broker (parent: DrrBroker)

## DeviceRequestType — Device Request Type
- DrtBrowse: Browse Request
- DrtConfigWrite: Config/Recipe Write Request (parent: DrtWrite)
- DrtContentTransfer: Content Transfer Request (SFTP/file transfer of DeviceContent) (parent: DrtWrite)
- DrtCyclic: Cyclic Subscription Request (parent: DrtSubscribe)
- DrtDiscovery: Discovery Request
- DrtEvent: Event Subscription Request (parent: DrtSubscribe)
- DrtRead: Read Request
- DrtStateChange: State Change Subscription Request (parent: DrtSubscribe)
- DrtSubscribe: Subscribe Request
- DrtUnsubscribe: Unsubscribe Request
- DrtWrite: Write Request

## DeviceRuleSetPurpose — Device Rule Set Purpose
- DrspConfiguration: Device Configuration Rule Set
- DrspDiagnostics: Device Diagnostics Rule Set
- DrspProcess: Device Process Rule Set (a sequence of device configurations)

## DeviceRuleType — Device Rule Type
- DrtApplyConfig: Apply Config
- DrtAssertConfig: Assert Config
- DrtCheckCompliance: Check Compliance (parent: DrtAssertConfig)
- DrtSoftValidation: Soft Validation (parent: DrtAssertConfig)
- DrtSuggestedConfig: Suggested Config

## DeviceType — Device Type
- Dgt3DPrinter: 3D Printer Control Group (parent: DgtManufacturingCell)
- DgtAHU: Air Handling Unit Control Group (parent: DgtHvacr)
- DgtAcceleratorPod: Accelerator Pod (parent: DgtComputeCluster)
- DgtAccessLayer: Access Layer Group (parent: DgtNetworking)
- DgtAdapters: Adapters (parent: DtDeviceGroup)
- DgtAirRenewal: Air Renewal Control Group (parent: DgtHvacr)
- DgtAutoChangeMasterFollower: Auto-Change Master/Follower Control Group (parent: DgtMasterFollower)
- DgtAuxiliary: Auxiliary (parent: DtDeviceGroup)
- DgtAxes: Axes (parent: DtDeviceGroup)
- DgtCluster: Cluster Group (parent: DtDeviceGroup)
- DgtCold: Cold Control Group (parent: DgtHvacr)
- DgtComputeCluster: Compute Cluster (parent: DgtCluster)
- DgtConditionMonitoring: Condition Monitoring (parent: DgtMonitoring)
- DgtControl: Control Group (parent: DtDeviceGroup)
- DgtConveyor: Conveyor Control Group (parent: DgtControl)
- DgtCoreLayer: Core Layer Group (parent: DgtNetworking)
- DgtDistributionLayer: Distribution Layer Group (parent: DgtNetworking)
- DgtDrillCnc: Drilling CNC Control Group (parent: DgtManufacturingCell)
- DgtElectricDischargeCnc: Electric Discharge CNC Control Group (parent: DgtManufacturingCell)
- DgtEnergyMonitoring: Energy Monitoring (parent: DgtMonitoring)
- DgtEquipmentMonitoring: Equipment Monitoring (parent: DgtMonitoring)
- DgtGpuCluster: GPU Cluster (parent: DgtComputeCluster)
- DgtGrinderCnc: Grinding CNC Control Group (parent: DgtManufacturingCell)
- DgtHeat: Heat Control Group (parent: DgtHvacr)
- DgtHvacr: HVACR Control Group (parent: DgtProcessingCell)
- DgtInferenceCluster: Inference Cluster (parent: DgtComputeCluster)
- DgtInterfaces: Interfaces (parent: DtDeviceGroup)
- DgtKubernetesCluster: Kubernetes Cluster (parent: DgtComputeCluster)
- DgtLaserCuttingCnc: Laser Cutting CNC Control Group (parent: DgtManufacturingCell)
- DgtLatheCnc: Lathe CNC Control Group (parent: DgtManufacturingCell)
- DgtManufacturingCell: Manufacturing Cell Control Group (parent: DtDeviceGroup)
- DgtMasterFollower: Master/Follower Control Group (parent: DgtControl)
- DgtMasterSlave: Master/Slave Group (parent: DgtCluster)
- DgtMillCnc: Milling CNC Control Group (parent: DgtManufacturingCell)
- DgtMonitoring: Monitoring Group (parent: DtDeviceGroup)
- DgtNetworking: Networking Group (parent: DtDeviceGroup)
- DgtPlasmaCuttingCnc: Plasma Cutting CNC Control Group (parent: DgtManufacturingCell)
- DgtPrimarySecondary: Primary/Secondary Hot-Standby Group (parent: DgtMasterSlave)
- DgtProcessingCell: Processing Cell Control Group (parent: DgtControl)
- DgtRagCluster: RAG Cluster (parent: DgtComputeCluster)
- DgtRobot: Robot Control Group (parent: DgtControl)
- DgtRouterCnc: Router CNC Control Group (parent: DgtManufacturingCell)
- DgtSubsystem: Subsystem Control Group (parent: DgtControl)
- DgtSystem: System (parent: DtDeviceGroup)
- DgtTpuPod: TPU Pod (parent: DgtComputeCluster)
- DgtTrainingCluster: Training Cluster (parent: DgtComputeCluster)
- DgtTransportSystems: Transport systems Control Group (parent: DgtControl)
- DgtVectorIndexCluster: Vector Index Cluster (parent: DgtComputeCluster)
- DtAIRuntime: AI Runtime (parent: DtComputer)
- DtASICAccelerator: ASIC Accelerator (parent: DtComputeAccelerator)
- DtAccessController: Access Controller (parent: DtController)
- DtAccessPoint: Access Point (parent: DtNetworkDevice)
- DtAccessSwitch: Access Switch (parent: DtSwitch)
- DtAdapter: Adapter (parent: DtPhysicalDevice)
- DtAnalogSensor: Analog Sensor (parent: DtSensor)
- DtAuxiliary: Auxiliary (parent: DtPhysicalDevice)
- DtAxis: Axis (parent: DtPhysicalDevice)
- DtBarcodeScanner: Barcode Scanner (parent: DtProductIdentification)
- DtBladeServer: Blade Server (parent: DtComputingServer)
- DtBuildingController: Building Controller (parent: DtController)
- DtCNC: CNC Controller (parent: DtController)
- DtComputeAccelerator: Compute Accelerator (parent: DtPhysicalDevice)
- DtComputer: Computer (parent: DtPhysicalDevice)
- DtComputingServer: Computing Server (parent: DtServer)
- DtConditionMonitoring: Condition Monitoring (parent: DtMonitoringDevice)
- DtContainerRuntime: Container Runtime (parent: DtAIRuntime)
- DtController: Controller (parent: DtComputer)
- DtCoreSwitch: Core Switch (parent: DtSwitch)
- DtDeviceGroup: Device Group
- DtDigitalSensor: Digital Sensor (parent: DtSensor)
- DtDistributionSwitch: Distribution Switch (parent: DtSwitch)
- DtDrive: Drive (parent: DtPhysicalDevice)
- DtDriveGroup: Drive Group (parent: DtDrive)
- DtEdgeGateway: Edge Gateway (parent: DtIoTGateway)
- DtEmbeddedController: Embedded Controller (parent: DtController)
- DtEmbeddingRuntime: Embedding Runtime (parent: DtAIRuntime)
- DtEnergyMeter: Energy Meter (parent: DtMonitoringDevice)
- DtExtremeConditionRemoteIO: Extreme Condition Remote IO (parent: DtRemoteIO)
- DtFPGAAccelerator: FPGA Accelerator (parent: DtComputeAccelerator)
- DtFirewall: Firewall (parent: DtNetworkDevice)
- DtFixedMountBarcodeScanner: Fixed Mount Barcode Scanner (parent: DtBarcodeScanner)
- DtGPU: GPU (parent: DtComputeAccelerator)
- DtGPUServer: GPU Server (parent: DtComputingServer)
- DtGateway: Gateway (parent: DtNetworkDevice)
- DtHPCServer: HPC Server (parent: DtComputingServer)
- DtHVACController: HVAC Controller (parent: DtController)
- DtHandHeldComputer: HandHeld Computer (parent: DtMobileComputer)
- DtHealthcareComputer: Healthcare Computer (parent: DtMobileComputer)
- DtIndoorAccessPoint: Indoor Access Point (parent: DtAccessPoint)
- DtIndustrialAccessSwitch: Industrial Access Switch (parent: DtSwitch)
- DtIndustrialPc: Industrial Pc (parent: DtPc)
- DtIndustrialPrimaryDataStorageServer: Industrial Primary Data Storage Server (parent: DtStorageServer)
- DtIndustrialServer: Industrial Server (parent: DtComputingServer)
- DtInferenceServer: Inference Server (parent: DtComputingServer)
- DtInputAnalogSensor: Input Analog Sensor (parent: DtAnalogSensor)
- DtInputDigitalSensor: Input Digital Sensor (parent: DtDigitalSensor)
- DtInterface: Interface (parent: DtPhysicalDevice)
- DtIoT: IoT (parent: DtComputer)
- DtIoTGateway: IoT Gateway (parent: DtIoT)
- DtKubernetesNode: Kubernetes Node (parent: DtAIRuntime)
- DtLightingController: Lighting Controller (parent: DtController)
- DtLinearAxis: Linear Axis (parent: DtAxis)
- DtMobileBarcodeScanner: Mobile Barcode Scanner (parent: DtBarcodeScanner)
- DtMobileComputer: Mobile Computer (parent: DtComputer)
- DtMobilePhone: Mobile Phone (parent: DtMobileComputer)
- DtModelServingRuntime: Model Serving Runtime (parent: DtAIRuntime)
- DtModem: Modem (parent: DtNetworkDevice)
- DtMonitoringDevice: Monitoring Device (parent: DtPhysicalDevice)
- DtMoquiPlc: Moqui PLC (parent: DtPhysicalDevice)
- DtMoquiPlcActuator: Moqui PLC Actuator (parent: DtMoquiPlc)
- DtMoquiPlcActuatorGroup: Moqui PLC ActuatorGroup (parent: DtMoquiPlc)
- DtMoquiPlcAxis: Moqui PLC Axis (parent: DtMoquiPlc)
- DtMoquiPlcAxisGroup: Moqui PLC Axis Group (parent: DtMoquiPlc)
- DtMoquiPlcProcessPID: Moqui PLC Process PID (parent: DtMoquiPlc)
- DtMoquiPlcSignalMgmt: Moqui PLC Signal Management (parent: DtMoquiPlc)
- DtMotionController: Motion Controller (parent: DtController)
- DtMultiAxesDrive: Multi-Axes Drive (parent: DtRotatoryAxis)
- DtMultiDrives: Multidrives (parent: DtDrive)
- DtNPU: NPU (parent: DtComputeAccelerator)
- DtNetworkAnalyzer: Network Analyzer (parent: DtMonitoringDevice)
- DtNetworkBridge: Network Bridge (parent: DtNetworkDevice)
- DtNetworkDevice: Network Device (parent: DtPhysicalDevice)
- DtNetworkMultimeter: Network Multimeter (parent: DtMonitoringDevice)
- DtOutdoorAccessPoint: Outdoor Access Point (parent: DtAccessPoint)
- DtOutputAnalogSensor: Output Analog Sensor (parent: DtAnalogSensor)
- DtOutputDigitalSensor: Output Digital Sensor (parent: DtDigitalSensor)
- DtPAC: PAC (parent: DtController)
- DtPLC: PLC (parent: DtController)
- DtPc: PC (parent: DtComputer)
- DtPhysicalDevice: Physical Device
- DtPrimaryDataStorageServer: Primary Data Storage Server (parent: DtStorageServer)
- DtProductIdentification: Product Identification (parent: DtPhysicalDevice)
- DtRFIDAntenna: RFID Antenna (parent: DtProductIdentification)
- DtRFIDReader: RFID Reader (parent: DtProductIdentification)
- DtRFIDScanner: RFID Scanner (parent: DtProductIdentification)
- DtRackServer: Rack Server (parent: DtComputingServer)
- DtRagRuntime: RAG Runtime (parent: DtAIRuntime)
- DtRemoteIO: Remote IO (parent: DtPhysicalDevice)
- DtRobotController: Robot Controller (parent: DtController)
- DtRoomController: Room Controller (parent: DtController)
- DtRotatoryAxis: Rotatory Axis (parent: DtAxis)
- DtRouter: Router (parent: DtNetworkDevice)
- DtRuggedMobilePhone: Rugged Mobile Phone (parent: DtMobileComputer)
- DtRuggedServer: Rugged Server (parent: DtComputingServer)
- DtRuggedTabletComputer: Rugged Tablet (parent: DtMobileComputer)
- DtSANSwitch: Storage Area Network - SAN Switch (parent: DtSwitch)
- DtSafetyPLC: Safety PLC (parent: DtController)
- DtSafetyRemoteIO: Safety Remote IO (parent: DtRemoteIO)
- DtSensor: Sensor (parent: DtPhysicalDevice)
- DtServer: Server (parent: DtComputer)
- DtServoDrive: Servo Drive (parent: DtRotatoryAxis)
- DtShadingController: Shading Controller (parent: DtController)
- DtSmartActuator: Smart Actuator (parent: DtPhysicalDevice)
- DtSmartRemoteIO: Smart Remote IO (parent: DtRemoteIO)
- DtSmartSensor: Smart Sensor (parent: DtPhysicalDevice)
- DtStorageServer: Storage Server (parent: DtServer)
- DtSwitch: Switch (parent: DtNetworkDevice)
- DtSystem: System (parent: DtPhysicalDevice)
- DtTPU: TPU (parent: DtComputeAccelerator)
- DtTabletComputer: Tablet (parent: DtMobileComputer)
- DtTowerServer: Tower Server (parent: DtComputingServer)
- DtTrainingServer: Training Server (parent: DtComputingServer)
- DtTwinServer: Twin Server (parent: DtComputingServer)
- DtUnstructuredDataStorageServer: Unstructured Data Storage Server (parent: DtStorageServer)
- DtVectorDatabaseNode: Vector Database Node (parent: DtAIRuntime)
- DtVehicleMountComputer: Vehicle Mount Computer (parent: DtMobileComputer)
- DtWearableBarcodeScanner: Wearable Barcode Scanner (parent: DtBarcodeScanner)
- DtWearableComputer: Wearable Computer (parent: DtMobileComputer)

## EmailType — Email Type
- EMT_ACCOUNT_INVITE: Account Invitation
- EMT_ADDED_EMAIL_AUTHC_FACTOR: Added Email Authentication Type (parent: EMT_SYSTEM)
- EMT_EMAIL_AUTHC_FACTOR_SENT: Email Authentication Code Sent (parent: EMT_SYSTEM)
- EMT_EMAIL_VERIFY: Email Address Verification
- EMT_NOTIFICATION: Notification (parent: EMT_SYSTEM)
- EMT_PWD_RESET: Password Reset (parent: EMT_SYSTEM)
- EMT_REG_CONFIRM: Registration Confirmation
- EMT_SCREEN_RENDER: Screen Render (parent: EMT_SYSTEM)
- EMT_SINGLE_USE_CODE: Single Use Code (parent: EMT_SYSTEM)
- EMT_SYSTEM: System
- EMT_UPD_INFO_CONFIRM: Update Personal Info Confirmation

## EmplAuthzType — Employment Authorization Type
- EatAlienCard: Alien Registration Receipt Card
- EatBirthCert: Birth Certificate
- EatCertBirthAbroad: Certification of Birth Abroad
- EatCertRepOfBirth: Certification of Report of Birth
- EatCitizenId: Citizen ID Card
- EatEmplAuthzDoc: Employment Authorization Document
- EatForeignPassportVisa: Foreign Passport plus Visa
- EatLocalPassport: Local Passport
- EatNativeDoc: Native Tribal Document
- EatResCitizenId: Resident Citizen ID Card
- EatResidentCard: Permanent Resident Card
- EatSocSecCard: Social Security Card

## EmplTaxExempt — Employment Tax Exempt Category
- EtxContract: Contract (1099 only)
- EtxForeignAg: Foreign Agriculture (H-2A)
- EtxForeignGeneral: Foreign General (H-2B)
- EtxForeignSpecialty: Foreign Specialty (H-1B)
- EtxResidentRegular: Resident Regular

## EmployerClassification — Employer Classification
- EmclsUsIrsAgriculture: US IRS Agriculture (943)
- EmclsUsIrsHousehold: US IRS Household (Sch H)
- EmclsUsIrsMilitary: US IRS Military (941)
- EmclsUsIrsQualGovernment: US IRS Medicare Qualified Government (941)
- EmclsUsIrsRailroad: US IRS Railroad (CT-1)
- EmclsUsIrsRegular: US IRS Regular (944)
- EmclsUsIrsRegularOther: US IRS Regular (all others) (941)

## EmploymentApplicationReferredBy — Employment Application Referred By
- EarbAdvertisement: Advertisement
- EarbInternet: Internet
- EarbNewspaper: Newspaper
- EarbPersonal: Personal Referral

## EmploymentLeaveReason — Employment Leave Reason
- ElrMedical: Medical
- ElrPersonal: Personal

## EmploymentLeaveType — Employment Leave Type
- EltEarned: Earned Leave
- EltHoliday: Holiday
- EltLossOfPay: Loss of Pay
- EltSpecialDayOff: Special Day Off

## EmploymentResponsibility — Employment Responsibility
- EmRspFinanceMgmt: Finance Management
- EmRspInventoryMgmt: Inventory Management
- EmRspProductionMgmt: Production Management
- EmRspPurchaseMgmt: Purchase Management
- EmRspResourceMgmt: Resource Management
- EmRspSalesMgmt: Sales Management

## EmploymentStatus — Employment Status
- EmpsFullTime: Full-time Employed
- EmpsHouse: House-Person
- EmpsPartTime: Part-time Employed
- EmpsRetired: Retired
- EmpsSelf: Self Employed
- EmpsStudent: Student
- EmpsUnemployed: Unemployed

## EndofunctorAlgebraType — Endofunctor Algebra Type
- EatAlgebra: Algebra F(A) -> A
- EatCoalgebra: Coalgebra A -> F(A)
- EatEilenbergMoore: Eilenberg-Moore algebra

## EntitySyncArtifactAppl — Entity Sync Artifact Application Type
- EsaaAlways: Always Include
- EsaaExclude: Exclude
- EsaaInclude: Include

## EnumGroup — Enumeration Group
- Eng2DEuclideanSpace: 2D Euclidean Space
- Eng3DEuclideanSpace: 3D Euclidean Space
- Eng401kEmpe: Employee 401k Types
- Eng401kEmpr: Employer 401k Types
- EngAccTxTypesInvoice: Acc TX Types Invoice
- EngAccTxTypesPayable: Acc TX Types Payable
- EngAccTxTypesReceivable: Acc TX Types Receivable
- EngGlClassGroups: GL Account Class Groups
- EngGlcGrossProfit: Gross Profit (parent: EngGlClassGroups)
- EngGlcLiability: Liabilities (parent: EngGlClassGroups)
- EngGlcNetAsset: Net Assets (parent: EngGlClassGroups)
- EngGlcNetEquity: Net Equity (parent: EngGlClassGroups)
- EngGlcNetIncome: Net Income (parent: EngGlClassGroups)
- EngGlcNetOpIncome: Net Operating Income (parent: EngGlClassGroups)
- EngGlcNetRevenue: Net Revenue (parent: EngGlClassGroups)
- EngHourlyRateType: Hourly Rate Type
- EngItemsAdjust: Invoice Adjust Items
- EngItemsProduct: Product Items
- EngItemsPurchase: Incoming/Payable/Purchase Items
- EngItemsSales: Outgoing/Receivable/Sales Items
- EngJointSpace6Dof: 6-DOF Joint Configuration Space
- EngOrderReasonApproved: Order Approved Reasons
- EngOrderReasonRejected: Order Rejected Reasons
- EngPayRateModifierType: Pay Rate Modifier Type
- EngPaymentTermType: Payment Term Types
- EngPieceRateType: Piece Rate Type
- EngRateCommonConfig: Common Configuration Rate Types
- EngRateCommonEntry: Common Manual TimeEntry Rate Types
- EngSec125Empe: Employee Section 125 Types
- EngSec125Empr: Employer Section 125 Types
- EngSpaceTime: Space Time
- EngTcpPose6Dof: 6-DOF TCP Pose Space

## FacilityContentType — Facility Content Type
- FcntImageUrl: Image URL
- FcntInternal: Internal Content
- FcntUserDefined: User Defined Content

## FacilityGroupType — Facility Group Type
- MGMT_STRUCTURE: Management Structure
- PRICING_GROUP: Pricing Group

## FacilityLocationType — Facility Location Type
- FltBulk: Bulk
- FltMorgue: Morgue
- FltPick: Pick
- FltQuarantine: Quarantine
- FltReceiving: Receiving
- FltStaging: Staging

## FacilityType — Facility Type
- FcTpBlock: Block
- FcTpBlockGroup: Block Group
- FcTpBuilding: Building
- FcTpCallCenter: Call Center
- FcTpDataCenter: Data Center
- FcTpDock: Dock
- FcTpFloor: Floor
- FcTpLand: Land
- FcTpLine: Production Line
- FcTpOffice: Office
- FcTpPlant: Plant
- FcTpRetailStore: Retail Store
- FcTpRoom: Room
- FcTpWarehouse: Warehouse

## FinancialAccountReplenishMethod — Financial Account Replenish Method
- FarmLevel: Replenish-level
- FarmTopOff: Top-off

## FinancialAccountReplenishType — Financial Account Replenish Type
- FarpAutomatic: Automatic Replenish
- FarpManual: Manual Replenish
- FarpNone: No Replenish

## FinancialAccountTransReason — Financial Account Trans Reason
- FatrCsCredit: Customer Service Credit
- FatrDisbursement: Disbursement
- FatrErrorAdjust: Error Adjustment
- FatrInitDeposit: Initial Deposit
- FatrPurchase: Purchase
- FatrRefund: Refund
- FatrReplenish: Replenishment
- FatrTransfer: Account Transfer

## FinancialAccountTransType — Financial Account Trans Type
- FattAdjustment: Adjustment
- FattDeposit: Deposit
- FattWithdraw: Withdraw

## FormConfigType — Form Config Type
- FctDesktop: Desktop
- FctMobile: Mobile

## FunctorType — Functor Type
- FtContra: Contravariant
- FtCov: Covariant
- FtDiagram: Diagram Functor (Shape Graph to Target Category)
- FtEmbedding: Faithful and Full (Embedding)
- FtEquiv: Equivalence (quasi-inverse)
- FtExecution: Execution / Interpretation Functor (parent: FtCov)
- FtFaithful: Faithful
- FtForgetful: Forgetful functor
- FtFull: Full
- FtHomContra: Hom(X,-) Contravariant
- FtHomCov: Hom(-,X) Covariant
- FtPowerset: Power-Set Functor
- FtTypeConstructor: Type Constructor Functor

## GeoAssocType — Geo Assoc Type
- GAT_COUNTY_SEAT: Administrative City
- GAT_GROUP_MEMBER: Geo Group Member
- GAT_REGIONS: Region of a Larger Geo

## GeoType — Geo Type
- GEOT_CITY: City
- GEOT_COUNTRY: Country
- GEOT_COUNTY: County
- GEOT_COUNTY_CITY: County-City
- GEOT_GROUP: Group
- GEOT_MUNICIPALITY: Municipality
- GEOT_POSTAL_CODE: Postal Code
- GEOT_PROVINCE: Province
- GEOT_REGION: Region
- GEOT_SALES_REGION: Sales Region
- GEOT_SERVICE_REGION: Service Region
- GEOT_STATE: State
- GEOT_TERRITORY: Territory

## GlAccountCategoryType — GL Account Category Type
- COST_CENTER: Cost Center Category

## GlAccountClass — GL Account Class
- ACCOUNTS_PAYABLE: Accounts Payable (parent: CURRENT_LIABILITY)
- ACCOUNTS_RECEIVABLE: Accounts Receivable (parent: CURRENT_ASSET)
- ACCRUED_EXPENSES: Accrued Expenses (parent: CURRENT_LIABILITY)
- ACCRUED_REVENUE: Accrued Revenue (parent: CURRENT_ASSET)
- ACCUM_AMORTIZATION: Accumulated Amortization (parent: OTHER_ASSET)
- ACCUM_DEPRECIATION: Accumulated Depreciation (parent: LONG_TERM_ASSET)
- ADVERTISING: Advertising (parent: SALES_EXPENSE)
- ALLOWANCE_BAD_DEBT: Allowance For Bad Debts (parent: CURRENT_ASSET)
- AMORTIZATION: Amortization (parent: NON_CASH_EXPENSE)
- ASSET: Assets (parent: DEBIT)
- BAD_DEBT_EXPENSE: Bad Debt Expense (parent: NON_CASH_EXPENSE)
- BANKING_CHARGES: Banking Service Charges (parent: GEN_ADMIN_EXPENSE)
- CASH_EQUIVALENT: Cash and Equivalent (parent: CURRENT_ASSET)
- CASH_INCOME: Cash Income (parent: INCOME)
- COMPENSATION: Employee Compensation (parent: GEN_ADMIN_EXPENSE)
- CONTRIBUTIONS: Contributions (parent: EXPENSE)
- COST_GOODS_SOLD: Cost of Goods Sold (parent: COST_OF_SALES)
- COST_OF_DISCOUNTS: Discounts and Write-downs (parent: REVENUE)
- COST_OF_SALES: Cost of Sales (parent: DEBIT)
- COST_SERVICES_SOLD: Cost of Services Sold (parent: COST_OF_SALES)
- CO_LIFE_INSURANCE: Company Owned Life Insurance (parent: NON_OP_EXPENSE)
- CREDIT: Credit
- CURRENT_ASSET: Current Assets (parent: ASSET)
- CURRENT_LIABILITY: Current Liabilities (parent: LIABILITY)
- CUSTOMER_RETURNS: Customer Returns (parent: REVENUE)
- DATA_PROCESSING: Data Processing (parent: GEN_ADMIN_EXPENSE)
- DEBIT: Debit
- DEPRECIATION: Depreciation (parent: NON_CASH_EXPENSE)
- DISTRIBUTION: Equity Distribution (parent: DEBIT)
- DIVIDEND: Dividends (parent: DISTRIBUTION)
- DUES_SUBSCRIPTIONS: Dues and Subscriptions (parent: GEN_ADMIN_EXPENSE)
- EDUCATION_EXPENSE: Education Expense (parent: GEN_ADMIN_EXPENSE)
- EQUIPMENT: Equipment (parent: LONG_TERM_ASSET)
- EQUITY: Equity (parent: CREDIT)
- EXPENSE: Operating Expense (parent: DEBIT)
- FACILITY_EXPENSE: Facility Expense (parent: GEN_ADMIN_EXPENSE)
- GEN_ADMIN_EXPENSE: General and Administrative Expense (parent: EXPENSE)
- GOODS_REVENUE: Goods Revenue (parent: REVENUE)
- GOOD_FREIGHT_COST: Good Freight Cost (parent: COST_GOODS_SOLD)
- GOOD_MATERIAL_COST: Good and Material Cost (parent: COST_GOODS_SOLD)
- GOOD_ROYALTIES_COST: Good Royalties Cost (parent: COST_GOODS_SOLD)
- INCOME: Non-operating Income (parent: CREDIT)
- INCOME_TAX_EXPENSE: Tax Expense - Income (parent: GEN_ADMIN_EXPENSE)
- INSURANCE_EXPENSE: Insurance Expense (parent: GEN_ADMIN_EXPENSE)
- INTANGIBLE_ASSET: Intangible Assets (parent: OTHER_ASSET)
- INTEREST_EXPENSE: Interest Expense (parent: NON_OP_EXPENSE)
- INTEREST_INCOME: Interest Income (parent: INCOME)
- INVENTORY_ASSET: Inventory Assets (parent: CURRENT_ASSET)
- INVENTORY_SHRINKAGE: Inventory Shrinkage (parent: COST_GOODS_SOLD)
- LAND_BUILDING: Land and Building (parent: LONG_TERM_ASSET)
- LIABILITY: Liabilities (parent: CREDIT)
- LOANS_PAYABLE: Loans Payable (parent: CURRENT_LIABILITY)
- LOANS_RECEIVABLE: Loans Receivable (parent: CURRENT_ASSET)
- LONG_TERM_ASSET: Long Term Assets (parent: ASSET)
- LONG_TERM_LIABILITY: Long Term Liabilities (parent: LIABILITY)
- MISC_EXPENSE: Miscellaneous Expense (parent: GEN_ADMIN_EXPENSE)
- NET_INCOME: Net Income (parent: EQUITY)
- NON_CASH_EXPENSE: Non-Cash Expense (parent: EXPENSE)
- NON_CASH_INCOME: Non-Cash Income (parent: INCOME)
- NON_COGS_ROYALTIES: Royalties Expense - Non-COGS (parent: NON_OP_EXPENSE)
- NON_EMP_COMPENSATION: Non-Employee Compensation (parent: GEN_ADMIN_EXPENSE)
- NON_OP_EXPENSE: Non-operating Expense (parent: DEBIT)
- NON_POSTING: Non-Posting (parent: DEBIT)
- OFFICE_EXPENSE: Office and Supplies (parent: GEN_ADMIN_EXPENSE)
- OTHER_ASSET: Other Assets (parent: ASSET)
- OTHER_COST_SALES: Other Cost of Sales (parent: COST_OF_SALES)
- OTHER_REVENUE: Other Revenue (parent: REVENUE)
- OTHER_TAX_EXPENSE: Tax Expense - Other (parent: GEN_ADMIN_EXPENSE)
- OWNERS_EQUITY: Owners Equity (parent: EQUITY)
- PREPAID_EXPENSE: Prepaid Expense (parent: CURRENT_ASSET)
- PREPAID_INVENTORY: Prepaid Inventory (parent: CURRENT_ASSET)
- PROF_SERVICES: Professional Services (parent: GEN_ADMIN_EXPENSE)
- PROMOTIONAL_MATERIALS: Promotional Materials (parent: SALES_EXPENSE)
- RESOURCE: Resource
- RETAINED_EARNINGS: Retained Earnings (parent: EQUITY)
- RETURN_OF_CAPITAL: Return of Capital (parent: DISTRIBUTION)
- REVENUE: Revenue (parent: CREDIT)
- SALES_COMPENSATION: Sales Compensation (parent: SALES_EXPENSE)
- SALES_EXPENSE: Sales and Marketing Expense (parent: EXPENSE)
- SALES_TRAVEL: Sales Travel (parent: SALES_EXPENSE)
- SERVICES_REVENUE: Services Revenue (parent: REVENUE)
- THIRD_PARTY_HOLDINGS: Third-Party Holdings (parent: CURRENT_LIABILITY)
- TRAVEL_ENT: Travel and Entertainment (parent: GEN_ADMIN_EXPENSE)
- TREASURY_STOCK: Treasury Stock (parent: EQUITY)
- UNEARNED_REVENUE: Unearned Revenue (parent: CURRENT_LIABILITY)
- UTILITIES_EXPENSE: Utilities Expense (parent: GEN_ADMIN_EXPENSE)
- VEHICLE_EXPENSE: Vehicle Expense (parent: GEN_ADMIN_EXPENSE)

## GlAccountType — GL Account Type
- GatAccPayWriteOff: Accounts Payables Write Off (parent: GatWriteOff)
- GatAccPayableUnapplied: Accounts Payable - Unapplied Payments (parent: GatAccountsPayable)
- GatAccRecBadRec: Allowance for Bad Receivables (parent: GatAccountsReceivable)
- GatAccRecWriteOff: Accounts Receivables Write Off (parent: GatWriteOff)
- GatAccReceivableUnapplied: Accounts Receivable - Unapplied Payments (parent: GatAccountsReceivable)
- GatAccountsPayable: Accounts Payable
- GatAccountsReceivable: Accounts Receivable
- GatAccruedExpenses: Accrued Expenses (parent: GatCurrentLiability)
- GatAccruedRevenue: Accrued Revenue (parent: GatCurrentAsset)
- GatCogs: Cost of Goods Sold
- GatCogsAvgCostAdj: COGS - Average Cost Adjustment (parent: GatCogs)
- GatCommissionExpense: Commission Expense (parent: GatOperatingExpense)
- GatCommissionsAccrued: Commissions Accrued (parent: GatCurrentLiability)
- GatCommissionsPayWriteOff: Commissions Payables Write Off (parent: GatWriteOff)
- GatCurrentAsset: Current Asset
- GatCurrentLiability: Current Liability
- GatCustomerCredits: Customer Credits (parent: GatCurrentLiability)
- GatCustomerDeposits: Customer Deposits (parent: GatCurrentLiability)
- GatCustomerReturns: Customer Returns
- GatDiscounts: Discounts
- GatExpense: Expense
- GatFaAccumDepreciation: Fixed Asset Accumulated Depreciation
- GatFaDepreciation: Fixed Asset Depreciation
- GatFaFound: Fixed Asset Found
- GatFaMaintenance: Fixed Asset Maintenance
- GatFaShrinkage: Fixed Asset Shrinkage
- GatFixedAsset: Fixed Asset
- GatForExGain: Foreign Exchange Gain (parent: GatForExGainLoss)
- GatForExGainLoss: Foreign Exchange Gain/Loss (parent: GatOtherExpense)
- GatForExLoss: Foreign Exchange Loss (parent: GatForExGainLoss)
- GatIncome: Income
- GatInterestIncWriteOff: Interest Income Write Off (parent: GatWriteOff)
- GatInterestIncome: Interest Income (parent: GatIncome)
- GatInterestIncomeRec: Interest Income Receivables (parent: GatAccountsReceivable)
- GatInvAdjAvgCost: Inventory Adjustment from Average Cost (parent: GatInventory)
- GatInvFound: Inventory Found
- GatInvShrinkage: Inventory Shrinkage
- GatInvValueAdj: Inventory Value Adjustment
- GatInventory: Inventory
- GatLongTermLiability: Long Term Liability
- GatMerchantSettlement: Merchant Account Settlement (parent: GatAccountsReceivable)
- GatOperatingExpense: Operating Expense (parent: GatExpense)
- GatOtherExpense: Other Expense (parent: GatExpense)
- GatOtherIncome: Other Income (parent: GatIncome)
- GatOwnersEquity: Owner's Equity
- GatPayInventoryTranIn: Payable from Inventory Transferred In (parent: GatAccountsPayable)
- GatPrepaidExpenses: Prepaid Expenses (parent: GatCurrentAsset)
- GatPrepaidInventory: Prepaid Inventory
- GatProfitLoss: Profit Loss
- GatRecInventoryTranOut: Receivable from Inventory Transferred Out (parent: GatCurrentAsset)
- GatRetainedEarnings: Retained Earnings
- GatSales: Sales
- GatSupplierDeposits: Supplier Deposits (parent: GatCurrentLiability)
- GatTax: Tax
- GatUndepositedReceipts: Undeposited Receipts
- GatUnearnedRevenue: Unearned Revenue (parent: GatCurrentLiability)
- GatUninvoicedShpmntRcpts: Uninvoiced Shipment Receipts (parent: GatCurrentLiability)
- GatUnissuedFixedAsset: Unissued Fixed Asset
- GatUnreceivedFixedAsset: Unreceived Fixed Asset
- GatUnreceivedInventory: Unreceived Inventory
- GatWipInventory: WIP Inventory (parent: GatInventory)
- GatWriteOff: Write Off (parent: GatOtherExpense)

## GlFiscalType — GL Fiscal Type
- GLFT_ACTUAL: Actual
- GLFT_BUDGET: Budget
- GLFT_FORECAST: Forecast
- GLFT_PLAN: Plan
- GLFT_SCENARIO: Scenario

## GlJournalType — GL Journal Type
- GLJRNL_ERROR: Error Journal
- GLJRNL_MANUAL: Manual Transactions Journal

## GlResourceType — GL Resource Type
- GlrtDeliveredGood: Delivered Good
- GlrtFinishedGood: Finished Good
- GlrtLabor: Labor
- GlrtMoney: Money
- GlrtRawMaterial: Raw Material
- GlrtService: Service

## GlXbrlClass — GL XBRL Class
- IAS: IAS
- US_GAAP: US GAAP

## GraphCategoryPurpose — Graph-Category Association Purpose
- GcpUnderlyingGraph: Underlying graph U(C): objects become vertices and morphisms become directed edges

## GraphContentType — Graph Content Type
- GrCntArrowIPC: Apache Arrow IPC Stream
- GrCntCsvEdge: Csv Edge List Compressed (gzip)
- GrCntCustom: Custom
- GrCntGraphML: GraphML Compressed (gzip)
- GrCntGraphSON: GraphSON (TinkerPop JSON) Compressed (gzip)
- GrCntProtobuf: Protobuf Encoded Adjacency List

## GraphEdgeType — Graph Edge Type
- GetBoundary: Boundary Edge
- GetDirected: Directed Edge
- GetSharp: Sharp Edge
- GetSmooth: Smooth Edge
- GetUndirected: Undirected Edge

## GraphType — Graph Type
- GtDAG: Directed Acyclic Graph (DAG) (parent: GtDirected)
- GtDirected: Directed
- GtDirectedMulti: Directed Multigraph (parent: GtDirected)
- GtDirectedMultiWithLoops: Directed Multigraph Permitting Loops (parent: GtDirectedMulti)
- GtDirectedRegular: Directed Regular Graph (parent: GtDirected)
- GtDirectedSimple: Directed Simple Graph (parent: GtDirected)
- GtDirectedSimpleWithLoops: Directed Simple Graph Permitting Loops (parent: GtDirectedSimple)
- GtForest: Forest Graph (parent: GtUndirected)
- GtHypergraph: Hypergraph
- GtLattice: Lattice Graph
- GtMixed: Mixed Graph
- GtOriented: Oriented Graph (parent: GtDirected)
- GtPolyforest: Polyforest Graph (parent: GtDAG)
- GtPolytree: Polytree Graph (parent: GtDAG)
- GtTree: Tree Graph (parent: GtUndirected)
- GtUndirected: Undirected
- GtUndirectedMulti: Undirected Multigraph (parent: GtUndirected)
- GtUndirectedMultiWithLoops: Undirected Multigraph Permitting loops (parent: GtUndirectedMulti)
- GtUndirectedRegular: Undirected Regular Graph (parent: GtUndirected)
- GtUndirectedSimple: Undirected Simple Graph (parent: GtUndirected)
- GtUndirectedSimpleWithLoops: Undirected Simple Graph Permitting Loops (parent: GtUndirectedSimple)
- GtWeighted: Weighted Graph

## IdentityType — Identity Type
- IdTpAlienCard: Alien Registration Receipt Card
- IdTpDaycareRecord: Daycare Record
- IdTpEmplAuthzDoc: Employment Authorization Document
- IdTpForeignPassport: Foreign Passport
- IdTpFrnDriverLicense: Foreign Driver License
- IdTpGovtIdCard: Government ID Card
- IdTpLclDriverLicense: Local Driver License
- IdTpLocalPassport: Local Passport
- IdTpMedicalRecord: Medical Record
- IdTpMerchMarCard: Merchant Mariner Card
- IdTpMilDepId: Military Dependent ID
- IdTpMilitaryId: Military ID
- IdTpNativeDoc: Native Tribal Document
- IdTpResidentCard: Permanent Resident Card
- IdTpSchoolIdCard: School ID Card
- IdTpSchoolRecord: School Record
- IdTpVoterReg: Voter Registration

## InventoryVarianceReason — Inventory Variance Reason
- InVrDamaged: Damaged
- InVrFound: Found
- InVrIntegration: Integration
- InVrLost: Lost
- InVrMisShipOrdered: Mis-shipped Item Ordered (+)
- InVrMisShipShipped: Mis-shipped Item Shipped (-)
- InVrSample: Sample (Giveaway)
- InVrStolen: Stolen

## InvoiceContentType — Invoice Content Type
- IctInvoiceDocument: Invoice Document
- IctItemImage: Item Image
- IctNote: Note
- IctReceipt: Receipt

## InvoiceItemAssocType — Invoice Item Assoc Type
- IiatBillThrough: Bill Through
- IiatCommission: Commission
- IiatRelated: Related
- IiatWithdraw: Withdraw

## InvoiceSequence — Invoice Sequence Mode
- InvSqEnfRestartYr: Enforced and Restart on Fiscal Year (no gaps, per org, reset to 1 each year)
- InvSqEnforced: Enforced Sequence (no gaps, per organization)
- InvSqStandard: Standard (faster, may have gaps, per system)

## InvoiceType — Invoice Type
- InvoiceCommission: Commission
- InvoiceCreditMemo: Credit Memo
- InvoiceGarnishment: Garnishment
- InvoicePayroll: Payroll Employee
- InvoicePayrollOther: Payroll Other
- InvoiceReturn: Return
- InvoiceSales: Sales/Purchase
- InvoiceTax: Tax
- InvoiceTemplate: Template

## ItemType — Item Type (Order, Return, Invoice)
- ItemAddtlFeature: Additional Feature (parent: ItemSales)
- ItemAdjAdvertising: Advertising (parent: ItemInvAdjust)
- ItemAdjJointAdv: Joint Advertising (parent: ItemInvAdjust)
- ItemAdvancePay: Advance Pay (parent: ItemPayrollIncome)
- ItemAsset: Asset - Fixed Asset
- ItemBonusDisc: Bonus (Discretionary) (parent: ItemPayrollIncome)
- ItemBonusNonDisc: Bonus (Non-Discretionary) (parent: ItemPayrollIncome)
- ItemBreakHourlyEarnings: Break Hourly Earnings (parent: ItemPayrollIncome)
- ItemBreakRrpEarnings: Break RRP Earnings (parent: ItemPayrollIncome)
- ItemChargebackAdjust: Chargeback (parent: ItemInvAdjust)
- ItemCommission: Commission Line Item
- ItemCommissionAdj: Commission Adjustment
- ItemComplianceFee: Compliance Fee (parent: ItemInvAdjust)
- ItemCouponCredit: Coupons and Credits (parent: ItemInvAdjust)
- ItemDed125Compy: 125*Compy. Contr Other Premium (parent: ItemPayrollDeduct)
- ItemDed125Hsa: 125*HSA Contribution (pre tax) (parent: ItemPayrollDeduct)
- ItemDed125Ppo: 125*PPO (pre tax) (parent: ItemPayrollDeduct)
- ItemDed401kEmpe: Traditional 401K Employee (parent: ItemPayrollDeduct)
- ItemDedAdvRepay: Advance Repayment (parent: ItemPayrollDeduct)
- ItemDedCharity: Charity Donation (parent: ItemPayrollDeduct)
- ItemDedChildGarnish: Child Support Garnishment (parent: ItemPayrollDeduct)
- ItemDedMHealthInsurance: Health Insurance (parent: ItemPayrollDeduct)
- ItemDedMisc: Miscellaneous Deduction (parent: ItemPayrollDeduct)
- ItemDedRoth401kEmpe: Roth 401k Employee (parent: ItemPayrollDeduct)
- ItemDedRothIraEmpe: Roth IRA Employee (parent: ItemPayrollDeduct)
- ItemDedSimpleIraEmpe: Simple IRA Employee (parent: ItemPayrollDeduct)
- ItemDedUnion: Union Dues (parent: ItemPayrollDeduct)
- ItemDedUnpaidTimeOff: Unpaid Salary Time Off (parent: ItemPayrollDeduct)
- ItemDedWageGarnish: Wage Garnishment (parent: ItemPayrollDeduct)
- ItemDiscount: Discount - Promotional
- ItemDiscountAppease: Discount - Appeasement
- ItemDonation: Donation (parent: ItemSales)
- ItemDoubleTimePremium: Double Time Premium (parent: ItemPayrollIncome)
- ItemExpAdvertising: Advertising (parent: ItemExpense)
- ItemExpCharitable: Charitable Contribution (parent: ItemExpense)
- ItemExpCommCellular: Communication Cellular (parent: ItemExpense)
- ItemExpCommNetwork: Communication Network (parent: ItemExpense)
- ItemExpCommTelephone: Communication Telephone (parent: ItemExpense)
- ItemExpCommissionFee: Commission/Fee (parent: ItemExpense)
- ItemExpHosting: Computer Server Hosting (parent: ItemExpense)
- ItemExpInsBusiness: Insurance Business (parent: ItemExpense)
- ItemExpInsEquipment: Insurance Equipment (parent: ItemExpense)
- ItemExpInsHealth: Insurance Health (parent: ItemExpense)
- ItemExpInsOther: Insurance Other (parent: ItemExpense)
- ItemExpInsRealEst: Insurance Real Estate (parent: ItemExpense)
- ItemExpInsVehicle: Insurance Vehicle (parent: ItemExpense)
- ItemExpInterestEquip: Interest Equipment (parent: ItemExpense)
- ItemExpInterestOther: Interest Other (parent: ItemExpense)
- ItemExpInterestReal: Interest Real Estate (parent: ItemExpense)
- ItemExpInterestVehi: Interest Vehicle (parent: ItemExpense)
- ItemExpLeaseEquip: Lease/Rent Equipment (parent: ItemExpense)
- ItemExpLeaseOther: Lease/Rent Other (parent: ItemExpense)
- ItemExpLeaseRealEst: Lease/Rent Real Estate (parent: ItemExpense)
- ItemExpLeaseVehicle: Lease/Rent Vehicle (parent: ItemExpense)
- ItemExpMaintEquip: Maintenance/Repair Equipment (parent: ItemExpense)
- ItemExpMaintOther: Maintenance/Repair Other (parent: ItemExpense)
- ItemExpMaintRealEst: Maintenance/Repair Real Estate (parent: ItemExpense)
- ItemExpMaintVehicle: Maintenance/Repair Vehicle (parent: ItemExpense)
- ItemExpMedical: Medical and Health Care (parent: ItemExpense)
- ItemExpOfficePostage: Office Postage (parent: ItemExpense)
- ItemExpOfficeSup: Office Supplies (parent: ItemExpense)
- ItemExpOther: Other (parent: ItemExpense)
- ItemExpRoyalties: Royalties (parent: ItemExpense)
- ItemExpServAccount: Services Accounting (parent: ItemExpense)
- ItemExpServLabor: Services Labor (parent: ItemExpense)
- ItemExpServLegal: Services Legal (parent: ItemExpense)
- ItemExpSupplies: Supplies (parent: ItemExpense)
- ItemExpTaxesLic: Taxes and Licenses (parent: ItemExpense)
- ItemExpTravAir: Travel Air (parent: ItemExpense)
- ItemExpTravCarRental: Travel Car Rental (parent: ItemExpense)
- ItemExpTravLocal: Travel Local/Parking/Tolls (parent: ItemExpense)
- ItemExpTravLodging: Travel Lodging (parent: ItemExpense)
- ItemExpTravMealsEnt: Travel Meals/Entertainment (parent: ItemExpense)
- ItemExpTravOther: Travel Other (parent: ItemExpense)
- ItemExpUtilElec: Utilities Electricity (parent: ItemExpense)
- ItemExpUtilHeating: Utilities Heating (parent: ItemExpense)
- ItemExpUtilTrash: Utilities Trash/Recycle (parent: ItemExpense)
- ItemExpUtilVehFuel: Utilities Vehicle Fuel (parent: ItemExpense)
- ItemExpUtilWater: Utilities Water/Sewer (parent: ItemExpense)
- ItemExpense: Expense (parent: ItemExpense)
- ItemFee: Fee
- ItemFreeFills: Free Fills (parent: ItemInvAdjust)
- ItemHolidayHourly: Holiday Hourly (parent: ItemPayrollIncome)
- ItemHolidaySalary: Holiday Salary (parent: ItemPayrollIncome)
- ItemHourlyEarnings: Hourly Earnings (parent: ItemPayrollIncome)
- ItemInvAdjust: Invoice Adjustment
- ItemInventory: Asset - Inventory
- ItemLateCharge: Late Payment Charge (parent: ItemInvAdjust)
- ItemMiscCharge: Miscellaneous Charge
- ItemMkgtPkgAdj: Marketing Package Adjustment (parent: ItemSales)
- ItemNonproductiveEarnings: Nonproductive Earnings (parent: ItemPayrollIncome)
- ItemOvertimePremium: Overtime Premium (parent: ItemPayrollIncome)
- ItemPayAdjOverpay: Pay Period Adjustment - Overpay (parent: ItemPayrollIncome)
- ItemPayAdjPay: Pay Period Adjustment - Pay (parent: ItemPayrollIncome)
- ItemPayrollDeduct: Payroll Deduction
- ItemPayrollExpense: Payroll Expense
- ItemPayrollIncome: Payroll Income
- ItemPayrollTaxes: Payroll Taxes
- ItemPieceMinWageAdj: Piece Min Wage Adjustment (parent: ItemPayrollIncome)
- ItemPieceOrHourlyEarnings: Piece Or Hourly Earnings (parent: ItemPayrollIncome)
- ItemPiecePlusHourlyEarnings: Piece Plus Hourly Earnings (parent: ItemPayrollIncome)
- ItemPieceworkEarnings: Piecework Earnings (parent: ItemPayrollIncome)
- ItemPrlCommission: Commission (parent: ItemPayrollIncome)
- ItemPrlExp125Compy: 125*Compy. Contr Other Premium (parent: ItemPayrollExpense)
- ItemPrlExp125Hsa: 125*HSA Contribution (parent: ItemPayrollExpense)
- ItemPrlExp125Ppo: 125*PPO (parent: ItemPayrollExpense)
- ItemPrlExp401kEmpr: 401K Employer (parent: ItemPayrollExpense)
- ItemPrlExpRothIraEmpr: Roth IRA Employer (parent: ItemPayrollExpense)
- ItemPrlExpSimpleIraEmpr: Simple IRA Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxFedPensionEmpr: Federal Pension Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxFutaEmpr: Federal Unemployment Insurance (FUTA) Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxHeadEmpr: Head Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxMedEmpr: Medicare Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxOccPrivEmpr: Occupational Privilege Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxSchoolDistEmpr: School District Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxSocialSecEmpr: Social Security Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxStateDisInsEmpr: State Disability Insurance Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxStateMiscEmpr: State Miscellaneous Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxStatePensionEmpr: State Pension Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxStateUnInsEmpr: State Unemployment Insurance Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxStateWrkCmpInsEmpr: State Workers' Comp Insurance Employer (parent: ItemPayrollExpense)
- ItemPrlExpTaxSurtaxEmpr: Surtax Employer (parent: ItemPayrollExpense)
- ItemProduct: Product (parent: ItemSales)
- ItemPromoDiscount: Promotional Discounts (parent: ItemInvAdjust)
- ItemPromptDiscount: Prompt Payment Discount (parent: ItemInvAdjust)
- ItemPtoHourly: PTO Hourly (parent: ItemPayrollIncome)
- ItemPtoSalary: PTO Salary (parent: ItemPayrollIncome)
- ItemReimbursement: Reimbursement (parent: ItemPayrollIncome)
- ItemRental: Rental (parent: ItemSales)
- ItemRentalDeposit: Rental Deposit
- ItemReplacement: Replacement (parent: ItemSales)
- ItemReturnAdjust: Return (parent: ItemInvAdjust)
- ItemSalary: Salary (parent: ItemPayrollIncome)
- ItemSales: Sales
- ItemSalesTax: Sales Tax
- ItemSalesThirdParty: Third Party (parent: ItemSales)
- ItemServiceProduct: Service Product (parent: ItemSales)
- ItemShiftPremiumEarnings: Shift Premium Earnings (parent: ItemPayrollIncome)
- ItemShipping: Shipping and Handling
- ItemShippingOther: Other Shipping (Non-Inventory)
- ItemShrinkage: Shrinkage (parent: ItemInvAdjust)
- ItemSickHourly: Sick Hourly (parent: ItemPayrollIncome)
- ItemSickSalary: Sick Salary (parent: ItemPayrollIncome)
- ItemSlottingFees: Slotting Fees (parent: ItemInvAdjust)
- ItemSupplierDiscount: Discount - Supplier
- ItemSurcharge: Surcharge (parent: ItemSales)
- ItemTaxAddtlMedEmpe: Additional Medicare Employee (parent: ItemPayrollTaxes)
- ItemTaxCbt: Tax - City, Borough, and Township Withholding (parent: ItemPayrollTaxes)
- ItemTaxCountyWhold: Tax - County Income Withholding (parent: ItemPayrollTaxes)
- ItemTaxFedPensionEmpe: Tax - Federal Pension Employee (parent: ItemPayrollTaxes)
- ItemTaxFederalWhold: Federal Income Withholding (parent: ItemPayrollTaxes)
- ItemTaxFutaEmpe: Federal Unemployment Insurance (FUTA) Employee (parent: ItemPayrollTaxes)
- ItemTaxHeadEmpe: Tax - Head Employee (parent: ItemPayrollTaxes)
- ItemTaxMedEmpe: Medicare Employee (parent: ItemPayrollTaxes)
- ItemTaxOccPrivEmpe: Tax - Occupational Privilege Employee (parent: ItemPayrollTaxes)
- ItemTaxSchoolDistEmpe: Tax - School District Employee (parent: ItemPayrollTaxes)
- ItemTaxSocialSecEmpe: Social Security Employee (parent: ItemPayrollTaxes)
- ItemTaxStateDisInsEmpe: Tax - State Disability Insurance Employee (parent: ItemPayrollTaxes)
- ItemTaxStateMiscEmpe: Tax - State Miscellaneous Employee (parent: ItemPayrollTaxes)
- ItemTaxStatePensionEmpe: Tax - State Pension Employee (parent: ItemPayrollTaxes)
- ItemTaxStateUnInsEmpe: Tax - State Unemployment Insurance Employee (parent: ItemPayrollTaxes)
- ItemTaxStateWhold: Tax - State Income Withholding (parent: ItemPayrollTaxes)
- ItemTaxStateWrkCmpInsEmpe: Tax - State Workers' Comp Insurance Employee (parent: ItemPayrollTaxes)
- ItemTaxSurtaxEmpe: Tax - Surtax Employee (parent: ItemPayrollTaxes)
- ItemTimeEntry: Time Entry (parent: ItemSales)
- ItemVacationHourly: Vacation Hourly (parent: ItemPayrollIncome)
- ItemVacationSalary: Vacation Salary (parent: ItemPayrollIncome)
- ItemVatTax: VAT Tax (not added to totals)
- ItemWarranty: Warranty (parent: ItemSales)
- ItemWorkEffort: Work Effort (parent: ItemSales)
- ItemWriteOff: Write-off (parent: ItemInvAdjust)

## JointDimension — Joint Dimension
- DimJ1: Joint 1 (θ₁)
- DimJ2: Joint 2 (θ₂)
- DimJ3: Joint 3 (θ₃)
- DimJ4: Joint 4 (θ₄)
- DimJ5: Joint 5 (θ₅)
- DimJ6: Joint 6 (θ₆)

## LlmConversationStatus — LLM Conversation Status
- LlmcsActive: Active
- LlmcsCancelled: Cancelled
- LlmcsComplete: Complete
- LlmcsFailed: Failed
- LlmcsStreaming: Streaming
- LlmcsYielded: Yielded (waiting client tools)

## LlmSkillProvenance — LLM Skill Provenance
- LskpHuman: Human
- LskpInfer: Infer
- LskpMixed: Mixed
- LskpSim: Sim
- LskpWorld: World

## LlmSkillRisk — LLM Skill Risk
- LskConfirm: Confirm
- LskIrreversible: Irreversible
- LskReversible: Reversible

## LlmSkillStatus — LLM Skill Status
- LsksActive: Active
- LsksDeprecated: Deprecated
- LsksProposed: Proposed
- LsksRejected: Rejected
- LsksSuperseded: Superseded

## LogicalOperator — Logical Operator
- OpAnd: Conjunction - AND
- OpEq: Equality - EQ
- OpGe: Greater Than or Equal - GE
- OpGt: Greater Than - GT
- OpImplies: Implication - IMPLIES
- OpIn: Membership - IN
- OpLe: Less Than or Equal - LE
- OpLt: Less Than - LT
- OpNand: Alternative Denial - NAND
- OpNe: Inequality - NE
- OpNor: Joint Denial - NOR
- OpNot: Negation - NOT
- OpOr: Disjunction - OR
- OpXnor: Biconditional - XNOR
- OpXor: Exclusive Or - XOR

## MaintenanceType — Maintenance Type
- MntTpAirFilterRepl: Air Filter Replace (parent: MntTpHvac)
- MntTpBatteryCheck: Battery Check (parent: MntTpVehicle)
- MntTpBatteryReplace: Battery Replace (parent: MntTpVehicle)
- MntTpBeltReplace: Belt Replacement (parent: MntTpVehicle)
- MntTpCleaning: Cleaning
- MntTpHvac: HVAC Maintenance
- MntTpLubeChassis: Lubricate Chassis (parent: MntTpVehicle)
- MntTpOilChange: Oil Change (parent: MntTpVehicle)
- MntTpRefrChkChrg: Refrigerant Check/Recharge (parent: MntTpHvac)
- MntTpRefuel: Re-Fuel (parent: MntTpVehicle)
- MntTpTireReplacement: Tire Replacement (parent: MntTpVehicle)
- MntTpTiresRotate: Tires Rotate (parent: MntTpVehicle)
- MntTpTuneUp: Tune Up (parent: MntTpVehicle)
- MntTpVehicle: Vehicle Maintenance

## MaritalStatus — Marital Status
- MarsDivorced: Divorced
- MarsMarried: Married
- MarsSingle: Single
- MarsWidow: Widowed/Widower

## MarketSegmentType — Market Segment Type
- MARKET_SEGMENT: Market Segment
- SALES_SEGMENT: Sales Segment

## MathFunction — Mathematical Function
- MfCos: Cosine Function
- MfExp: Exponential Function
- MfLog: Natural Logarithm
- MfPoly: Polynomial
- MfSin: Sine Function

## MathModelBasisFunc — Math Model Basis Function
- MmbChebyshev: Chebyshev Basis
- MmbFourier: Fourier Basis
- MmbHermite: Hermite Polynomial
- MmbLagrange: Lagrange Polynomial
- MmbLegendre: Legendre Basis
- MmbNurbs: NURBS / IGA Basis
- MmbSerendipity: Serendipity Family

## MathModelBindingPurpose — Math Model Binding Purpose
- MmbpCalibration: Initial Calibration / Alignment
- MmbpClosedLoopControl: Real-Time Closed-Loop Control
- MmbpMonitoring: Condition Monitoring / Prognosis
- MmbpSimulation: Digital Twin / Simulation Only
- MmbpTuning: Batch Parameter Tuning

## MathModelDataPurpose — Math Model Data Purpose
- MmdpAbsolute: Absolute Error (parent: MmdpErrorMetric)
- MmdpArrivalRate: Arrival Rate (λ)
- MmdpBcDirichlet: Dirichlet Boundary Condition (parent: MmdpBoundaryCondition)
- MmdpBcNeumann: Neumann Boundary Condition (parent: MmdpBoundaryCondition)
- MmdpBcRobin: Robin/Mixed Boundary (parent: MmdpBoundaryCondition)
- MmdpBoundaryCondition: Boundary Condition
- MmdpCheckpointState: Checkpoint State
- MmdpConfidence: Confidence Interval (parent: MmdpErrorMetric)
- MmdpConstraint: Constraint
- MmdpConstraintMatrix: Constraint Matrix (A)
- MmdpCoreTensor: Core Tensor (HOSVD/Tucker)
- MmdpCostVector: Cost / Objective Coefficients (c)
- MmdpCurvature: Curvature (parent: MmdpDerivative)
- MmdpDecisionVars: Decision Variables
- MmdpDerivative: Derivative
- MmdpDiscountFactor: Discount Factor (γ)
- MmdpDualValue: Dual Value / Shadow Price (y)
- MmdpEquality: Equality Constraint (parent: MmdpConstraint)
- MmdpErrorMetric: Error Metric
- MmdpFactorMatrix: Factor Matrix (mode-k)
- MmdpGradient: Gradient (parent: MmdpDerivative)
- MmdpHessian: Hessian (parent: MmdpDerivative)
- MmdpInequality: Inequality Constraint (parent: MmdpConstraint)
- MmdpInitialCondition: Initial Condition
- MmdpInterarrivalDist: Interarrival Time Distribution
- MmdpIntermediateState: Intermediate State
- MmdpJacobian: Jacobian (parent: MmdpDerivative)
- MmdpLastSuccessfulState: LastSuccessful State
- MmdpModelCoefficients: Model Coefficients
- MmdpModelInputs: Model Inputs
- MmdpModelOutputs: Model Outputs
- MmdpModelParams: Model Parameters
- MmdpObjective: Objective Function
- MmdpPolicy: Policy (π)
- MmdpQFunction: Action-Value Function (Q)
- MmdpQueueDiscipline: Queue Discipline (FIFO/LIFO/Priority)
- MmdpReducedCost: Reduced Cost (rc)
- MmdpReward: Reward Function (R)
- MmdpRhsVector: Right-Hand Side (b)
- MmdpSensitivity: Sensitivity Range
- MmdpServiceRate: Service Rate (μ)
- MmdpServiceTimeDist: Service Time Distribution
- MmdpSnapshotState: Snapshot State
- MmdpStdDev: Standard Deviation (parent: MmdpErrorMetric)
- MmdpSymbolic: Symbolic Rule (parent: MmdpConstraint)
- MmdpTorsion: Torsion (parent: MmdpDerivative)
- MmdpTrainingData: Training Data
- MmdpTransitionMatrix: State Transition Matrix (P)
- MmdpValidationData: Validation Data
- MmdpValueFunction: State-Value Function (V)
- MmdpVarBounds: Variable Bounds
- MmdpVariableDomain: Variable Domain (Continuous/Integer/Binary)

## MathModelDataType — Math Model Data Type
- MmdtApproxFunc: Approximated Function
- MmdtMatrix: Matrix
- MmdtTensor: Tensor
- MmdtTransformation: Transformation
- MmdtVector: Vector

## MathModelDefContentPurpose — Math Model Def Content Purpose
- MmCnpHelperFunc: Helper Fuction
- MmCnpMainLogic: Main Executable Logic
- MmCnpModelDef: Model Definition
- MmCnpPostProcessingScript: Post-processing Script
- MmCnpPreProcessingScript: Pre-processing Script
- MmCnpSolverConfig: Solver Configuration
- MmCnpSymDer: Symbolic Derivation

## MathModelDefContentType — Math Model Def Content Type
- MmCntBinaryModel: Binary Model Blob
- MmCntCsv: CSV
- MmCntDocs: Documentation
- MmCntJax: JAX / XLA Program
- MmCntJson: JSON
- MmCntOnnx: ONNX exports
- MmCntPython: Python Script
- MmCntSymPy: SymPy Script
- MmCntTorchScript: TorchScript Bundle
- MmCntYaml: YAML

## MathModelDomain — Math Model Domain
- MmdBiology: Biology
- MmdEngineering: Engineering
- MmdFinance: Finance
- MmdPhysics: Physics

## MathModelEventType — Math Model Event Type
- MmetCheckpoint: Checkpoint Saved
- MmetConverged: Converged
- MmetDiverged: Diverged / Error
- MmetIteration: Iteration Progress
- MmetStart: Start-up

## MathModelExternalSystem — Math Model External System
- MmesAnthropic: Anthropic API
- MmesAwsBedrock: AWS Bedrock
- MmesAzureOpenAi: Azure OpenAI Service
- MmesCohere: Cohere API
- MmesCustom: Custom / Other
- MmesDvc: DVC / DAGsHub
- MmesGoogleAi: Google AI / Vertex AI / Gemini API
- MmesHfHub: Hugging Face Hub
- MmesInternal: Internal Registry
- MmesLlamaCpp: llama.cpp Server
- MmesLmStudio: LM Studio
- MmesMistral: Mistral API
- MmesMlflow: MLflow Model Registry
- MmesNeptune: Neptune.ai
- MmesNvidiaNgc: NVIDIA NGC Model Catalog
- MmesOllama: Ollama Local Runtime
- MmesOnnxZoo: ONNX Model Zoo
- MmesOpenAi: OpenAI API
- MmesPyTorchHub: PyTorch Hub
- MmesTfHub: TensorFlow Hub / Kaggle Models
- MmesVllm: vLLM Server
- MmesWandb: Weights and Biases

## MathModelInterpolation — Math Model Interpolation
- MmiHermite: Hermite Shape Function
- MmiLagrange: Lagrange Shape Function
- MmiLinear: Linear Interpolation
- MmiNurbs: NURBS / Isogeometric Shape Function
- MmiSerendipity: Serendipity Shape Function
- MmiSpline: Spline-based Interpolation

## MathModelSolvingMethod — Math Model Solving Method
- MmsmAdmm: ADMM
- MmsmAugLag: Augmented Lagrangian / Penalty
- MmsmBranchAndBound: Branch-and-Bound / Branch-and-Cut
- MmsmCuttingPlane: Cutting Plane Methods
- MmsmDg: Discontinuous Galerkin Method - DG
- MmsmFdm: Finite Difference Method - FDM
- MmsmFem: Finite Element Method - FEM
- MmsmFvm: Finite Volume Method - FVM
- MmsmHeuristicGA: Genetic / Evolutionary Heuristics
- MmsmInteriorPoint: Interior-Point (Barrier/Primal-Dual)
- MmsmJax: Google JAX / OpenXLA Runtime
- MmsmJaxJit: Google JAX XLA JIT Compiled / Autograd Runtime (parent: MmsmJax)
- MmsmJena: Apache Jena Semantic Reasoner & SPARQL Engine
- MmsmLibTorch: LibTorch Native Runtime
- MmsmLibTorchTraining: LibTorch Autograd & Training Runtime (parent: MmsmLibTorch)
- MmsmMeshless: Meshless
- MmsmOnnx: ONNX Runtime Neural Network Inference Engine
- MmsmOpenCv: OpenCV Computer Vision Runtime
- MmsmOpenFoam: OpenFOAM Finite Volume CFD Engine
- MmsmOpenFoamIcoFoam: OpenFOAM Incompressible Laminar Transient Solver (parent: MmsmOpenFoam)
- MmsmOpenFoamSimpleFoam: OpenFOAM Incompressible Turbulent Steady-State Solver (parent: MmsmOpenFoam)
- MmsmOrTools: Google OR-Tools Mathematical Optimization
- MmsmPetscTao: PETSc / TAO Numerical Optimizer
- MmsmSem: Spectral Element Method - SEM
- MmsmSimAnn: Simulated Annealing
- MmsmSimplex: Simplex / Revised Simplex
- MmsmTabu: Tabu Search

## MathModelSource — Math Model Source
- MmsManual: Manually Defined
- MmsMeasured: Measured / Experimental
- MmsSimulated: Synthetic / Simulation

## MathModelType — Math Model Type
- MmtAlgebraic: Algebraic Equations (parent: MmtModelDriven)
- MmtBirthDeath: Birth-Death Process (parent: MmtStochasticProcess)
- MmtCFD: Computational Fluid Dynamics (parent: MmtPDEs)
- MmtCodeDefinedFunction: Code-Defined Function (parent: MmtModelDriven)
- MmtComputerVision: Computer Vision & Image Processing (parent: MmtDataDriven)
- MmtConstraint: Constraint (parent: MmtModelDriven)
- MmtCp: Constraint Programming (CP) (parent: MmtOptimization)
- MmtDataDriven: Data Driven Model
- MmtDlAutoencoder: Autoencoder (parent: MmtDlModel)
- MmtDlCnn: Convolutional Neural Network (parent: MmtDlModel)
- MmtDlDeconvolutional: Deconvolutional Neural Network (parent: MmtDlModel)
- MmtDlDeep: Deep Neural Network (parent: MmtDlModel)
- MmtDlFeedforward: Feedforward Neural Network (parent: MmtDlModel)
- MmtDlGenerative: Generative Adversarial Neural Network (parent: MmtDlModel)
- MmtDlLongShort: Long Short-Term Memory Neural Network (parent: MmtDlModel)
- MmtDlModel: Deep‑Learning Model (parent: MmtDataDriven)
- MmtDlModular: Modular Neural Network (parent: MmtDlModel)
- MmtDlPerceptron: Perceptron Neural Network (parent: MmtDlModel)
- MmtDlRadialBasisFunc: Radial Basis Function Neural Network (parent: MmtDlModel)
- MmtDlRnn: Recurrent Neural Network (parent: MmtDlModel)
- MmtDlSeqToSeq: Sequence-To-Sequence Neural Network (parent: MmtDlModel)
- MmtDlSoms: Self-Organizing Maps (parent: MmtDlModel)
- MmtDlTransformer: Transformer Neural Network (parent: MmtDlModel)
- MmtDynamicSystem: Dynamic System (parent: MmtModelDriven)
- MmtElementaryFunc: Elementary Equation (parent: MmtModelDriven)
- MmtFunctional: Functional Model (parent: MmtModelDriven)
- MmtLinearAlgebra: Linear Algebra (parent: MmtModelDriven)
- MmtLinearEqSystem: Linear Equation System (parent: MmtModelDriven)
- MmtLp: Linear Program (LP) (parent: MmtOptimization)
- MmtMarkovChain: Markov Chain (parent: MmtStochasticProcess)
- MmtMdp: Markov Decision Process (MDP) (parent: MmtStochasticProcess)
- MmtMeasuredDataSeries: Measured Data Series Model (parent: MmtDataDriven)
- MmtMilp: Mixed-Integer Linear Program (MILP) (parent: MmtOptimization)
- MmtMiqp: Mixed-Integer Quadratic Program (MIQP) (parent: MmtOptimization)
- MmtMlModel: Machine‑Learning Model (parent: MmtDataDriven)
- MmtModelDriven: Model-Driven / Physics-Based / Constructed Model
- MmtNlp: Nonlinear Program (NLP) (parent: MmtOptimization)
- MmtNonLinearEqSystem: Non Linear Equation System (parent: MmtModelDriven)
- MmtODEs: Ordinary Differential Equations ODE System (parent: MmtModelDriven)
- MmtOptimization: Optimization Problem (parent: MmtModelDriven)
- MmtPDEs: Partial Differential Equation PDE System (parent: MmtModelDriven)
- MmtParametricPath: Parametric Path (parent: MmtModelDriven)
- MmtPoissonProcess: Poisson Process (parent: MmtStochasticProcess)
- MmtPolynomial: Polynomial (parent: MmtModelDriven)
- MmtPomdp: Partially Observable MDP (POMDP) (parent: MmtStochasticProcess)
- MmtQcqp: Quadratically Constrained QP (QCQP) (parent: MmtOptimization)
- MmtQp: Quadratic Program (QP) (parent: MmtOptimization)
- MmtQueueing: Queueing Model (parent: MmtStochasticProcess)
- MmtRationalFunc: Rational Function (parent: MmtModelDriven)
- MmtRegression: Statistical Regression (parent: MmtDataDriven)
- MmtSdp: Semidefinite Program (SDP) (parent: MmtOptimization)
- MmtSmdp: Semi-Markov Decision Process (SMDP) (parent: MmtStochasticProcess)
- MmtSocp: Second-Order Cone Program (SOCP) (parent: MmtOptimization)
- MmtStochasticProcess: Stochastic Process (parent: MmtModelDriven)
- MmtSymbolic: Symbolic / Analytic Model (parent: MmtModelDriven)

## MathModelUsageContext — Math Model Usage Context
- MmucAnalysis: Analysis
- MmucInference: Inference
- MmucOptimisation: Optimisation
- MmucRegression: Regression
- MmucTest: Test
- MmucTraining: Training

## MatrixComponentType — Matrix Component Type
- MctCanonical: Canonical Matrix Component
- MctSparse: Sparse Matrix Component
- MctSymbolic: Symbolic Matrix Component

## MatrixConditionNorm — Norm used for condition number
- McnFro: ||·||_F (Frobenius)
- McnInf: ||·||∞
- McnOne: ||·||₁
- McnTwo: ||·||₂ (spectral)

## MatrixPurpose — Matrix Purpose
- MpApproximate: Approximate Matrix
- MpBlock: Block Matrix
- MpFeedbackGain: State Feedback Gain Matrix (K)
- MpFeedforward: Direct Transmission Feedforward Matrix (D)
- MpInput: Control Input Matrix (B)
- MpLuL: LU L Matrix
- MpLuU: LU U Matrix
- MpObserverGain: Observer or Kalman Gain Matrix (L)
- MpOriginal: Original Matrix
- MpOutput: Measurement Output Matrix (C)
- MpState: Dynamic State Transition Matrix (A)
- MpSvdSigma: SVD Σ Matrix
- MpSvdU: SVD U Matrix
- MpSvdV: SVD V Matrix

## MatrixType — Matrix Type
- MtDense: Dense Matrix
- MtDiagonal: Diagonal Matrix
- MtHermitian: Hermitian Matrix
- MtIdentity: Identity Matrix
- MtOrthogonal: Orthogonal Matrix
- MtPermutation: Permutation Matrix
- MtRectangular: Rectangular Matrix
- MtSparse: Sparse Matrix
- MtSquare: Square Matrix
- MtSymmetric: Symmetric Matrix
- MtTriangular: Triangular Matrix
- MtZero: Zero Matrix

## MeshAdaptationType — Mesh Adaptation Type
- MatAutomatic: Automatic Adaptation Based on Error Estimation
- MatCustom: Custom/Manual Mesh Adaptation Strategy
- MatHDerefinement: h-type Derefinement (remove cells in low-error regions)
- MatHRefinement: h-type Refinement (refine by adding smaller cells)
- MatNone: No Adaptation
- MatPRefinement: p-type Refinement (increase polynomial order, FEM)
- MatRRefinement: r-type Refinement (move/displace nodes without adding cells)
- MatRemeshing: Adaptive Remeshing (recreate mesh in selected region)
- MatRhRefinement: rh-type Refinement (combine h- and r- refinement)

## MeshContentType — Mesh Content Type
- MCntCustom: Custom
- MCntObj: Wavefront OBJ Compressed (gzip)
- MCntPly: PLY Binary Little Endian
- MCntStl: STL Binary
- MCntVtk: VTK / VTU Binary
- MCtnGltf: GLTF Binary (GLB)

## MeshGroupPurpose — Mesh Group Purpose
- MgpBoundaryCondition: Boundary Condition Region (Dirichlet / Neumann)
- MgpControlRegion: Control domain for active feedback, model-predictive control, or sensor influence. (parent: MgpSolverRegion)
- MgpElectromagneticDomain: Region used for electromagnetic simulation (e.g. Maxwell equations). (parent: MgpSolverRegion)
- MgpFluidDomain: Region used for fluid dynamics simulation (CFD). (parent: MgpSolverRegion)
- MgpInitialConditionRegion: Zone where initial values are applied (e.g. initial temperature, velocity, etc). (parent: MgpSolverRegion)
- MgpInterface: Internal interface between sub-domains
- MgpLoadRegion: Area where loads / sources are applied
- MgpMaterialRegion: Material Domain for FEM equations (parent: MgpSolverRegion)
- MgpMultiphysicsDomain: Region supporting coupled physics models (e.g. thermal-structural). (parent: MgpSolverRegion)
- MgpPathRegion: Cells selected by proximity to a ParametricPath
- MgpSamplingZone: Region used to sample or extract data (e.g. for statistics or averaging).
- MgpShadingRegion: Shading/Rendering Region
- MgpSolverRegion: Solver Computation Region
- MgpStructuralDomain: Region where structural (mechanical stress/strain) equations are applied. (parent: MgpSolverRegion)
- MgpSupportStructure: Support or scaffold cells
- MgpThermalDomain: Region of the mesh where thermal equations are applied (e.g. temperature simulation). (parent: MgpSolverRegion)
- MgpToolContactBand: Tool-contact band for CAM operations (parent: MgpPathRegion)

## MeshGroupType — Type of mesh group
- MgtExportZone: Export Zone
- MgtPhysicsDomain: Physics Domain
- MgtSelectionSet: Selection Set
- MgtTextureRegion: Texture Region

## MeshKCellType — Mesh K-Cell Type
- MkctBezierPatch: Bezier surface patch (parent: MkctFace)
- MkctEdge: Edge
- MkctFace: Face
- MkctHexahedron: Hexahedron (parent: MkctVolume)
- MkctHypervolume: Hypervolume
- MkctNurbsPatch: NURBS surface patch (parent: MkctFace)
- MkctPolygon: Polygon (parent: MkctFace)
- MkctPolyhedron: Polyhedron (parent: MkctVolume)
- MkctPyramid: Pyramid (parent: MkctVolume)
- MkctQuadrilateral: Quadrilateral (parent: MkctFace)
- MkctTetrahedron: Tetrahedron (parent: MkctVolume)
- MkctTriangle: Triangle (parent: MkctFace)
- MkctTriangularPrism: Triangular Prism (parent: MkctVolume)
- MkctVertex: Vertex
- MkctVolume: Volume

## MeshMaterialType — Mesh Material Type
- MatAluminum: Aluminum (parent: MmtStandard)
- MatCarbonFiber: Carbon fiber (parent: MmtStandard)
- MatConcrete: Concrete (parent: MmtStandard)
- MatCopper: Copper (parent: MmtStandard)
- MatGlass: Glass (parent: MmtStandard)
- MatPlastic: Plastic (parent: MmtStandard)
- MatRubber: Rubber (parent: MmtStandard)
- MatSteel: Steel (parent: MmtStandard)
- MatTitanium: Titanium (parent: MmtStandard)
- MatWood: Wood (parent: MmtStandard)
- MmtLambert: Lambert Material
- MmtPhong: Phong Material
- MmtShader: Custom ShaderMaterial
- MmtStandard: Standard (PBR) Material
- MmtToon: Toon Material

## MeshOrientation — Mesh Orientation
- MoNegative: Negative or Anticlockwise or Left‑Handed
- MoNotOrientable: Not Orientable
- MoPositive: Positive or Clockwise or Right‑Handed

## MeshPurpose — Mesh Purpose
- MpCFD: Computational Fluid Dynamics Mesh
- MpFEM: Finite Element Mesh
- MpFVM: Finite Volume Mesh
- MpTopologicalMesh: Topological Analysis Mesh

## MeshShaderProfile — Mesh Shader Profile
- MspBlinnPhong: Blinn-Phong shading
- MspFlat: Flat shading
- MspGouraud: Gouraud shading
- MspPhong: Phong shading
- MspToon: Toon (non-photorealistic) shading
- MspUnlit: Unlit color (no lighting calculation)
- MspWireframe: Wireframe rendering

## MeshType — Mesh Type
- MtHexahedral: Hexahedral Mesh
- MtPolygon: Polygon Mesh
- MtQuad: Quad Mesh
- MtTetrahedral: Tetrahedral Mesh
- MtTriangle: Triangle Mesh

## MessageReceiveResponse — Message Receive Response
- MsgRrDelete: Delete
- MsgRrMove: Move
- MsgRrNone: None

## MorphismCompositionType — Morphism Composition Type
- McAssoc: Associativity Proof
- McBinary: Binary Composition (g ∘ f)
- McIdentity: Identity Law Proof
- McIterate: Iterated Composition (f o f o ... o f, once per element of a context list)
- McNary: N-ary Composition (f1 o f2 o ... o fn)
- McNatVert: Natural-Transformation Vertical Composition
- McUnitLaw: Unit Law Proof
- McZeroLaw: Zero-Arrow Annihilation

## MorphismType — Morphism Type
- MphZero: Zero morphism
- MtDisplayMap: Display Map representing a Dependent Type
- MtEndo: Endomorphism
- MtEpi: Epimorphism
- MtGeneral: General Morphism
- MtId: Identity morphism; may have a composite implementation
- MtIso: Isomorphism
- MtLaw: Structure-Preserving Law
- MtLawGroupHom: Group Homomorphism (parent: MtLaw)
- MtLawLinear: Linear Map (Vector Space) (parent: MtLaw)
- MtLawRingHom: Ring Homomorphism (parent: MtLaw)
- MtLeftInv: Retraction left-inverse
- MtMono: Monomorphism
- MtRetract: Retract (split epi)
- MtRightInv: Section right-inverse
- MtSection: Section (split mono)
- MtTerm: Typed Term from a Context to a Type

## NatTransfCompositionType — Natural Transformation Composition Type
- NctHorizontal: Horizontal composition (*)
- NctVertical: Vertical composition (o)

## NaturalTransformationType — Natural Transformation Type
- NtCocone: Cocone (Diagram Functor to Constant Functor)
- NtColimitCocone: Colimit Cocone (Universal Cocone) (parent: NtCocone)
- NtCone: Cone (Constant Functor to Diagram Functor)
- NtDiNat: Dinatural Transformation
- NtIso: Natural Isomorphism
- NtLimitCone: Limit Cone (Universal Cone) (parent: NtCone)
- NtMod: Modification

## NormDomain — Norm Domain (vector, matrix, higher-order tensor)
- NdMatrix: Matrix Norm
- NdTensor: Higher-Order Tensor Norm
- NdVector: Vector Norm

## NormOrder — Norm Order
- NoGenericP: Arbitrary p-norm; optionValue holds p
- NoMat1: ‖A‖₁ - max column sum
- NoMat2: Spectral ‖A‖₂ (largest σ)
- NoMatFrobenius: Frobenius ‖A‖_F
- NoMatInf: ‖A‖_∞ - max row sum
- NoMatNeg1: ‖A‖_{-1}
- NoMatNeg2: ‖A‖_{-2} (smallest σ)
- NoMatNegInf: ‖A‖_{-∞} - min row sum
- NoMatNuclear: Nuclear ‖A‖_* (Σ singular values)
- NoVec0: L⁰ - number of non-zeros
- NoVec1: L¹ - Manhattan
- NoVec2: L² - Euclidean
- NoVecDefault: Vector-2 (default L²)
- NoVecInf: L^∞ - max(abs(xᵢ))
- NoVecNeg1: L⁻¹
- NoVecNeg2: L⁻²
- NoVecNegInf: L^-∞ - min(abs(xᵢ))

## OrderDecisionReason — Order Decision Reason
- OdrFraud: Fraud
- OdrOther: Other
- OdrPayment: Payment Not Received

## OrderItemQuantityReason — Order Item Quantity Change Reason
- OiqrCustomer: Customer Request
- OiqrInventory: Insufficient Inventory
- OiqrSingleLot: Single Lot Unavailable

## OrderSequence — Order Sequence Mode
- OrdSqEnforced: Enforced Sequence (no gaps, per organization)
- OrdSqStandard: Standard (faster, may have gaps, per system)

## ParameterClass — Parameter Class
- PcAdaptiveAvgPool2d: 2D Adaptive Average Pooling parameters (parent: PcOperation)
- PcAuxiliary: Auxiliary Parameter
- PcAvgPool2d: 2D Average Pooling parameters (parent: PcOperation)
- PcBatchNorm: Batch Normalization parameters (parent: PcOperation)
- PcConv1d: 1D Convolution parameters (parent: PcOperation)
- PcConv2d: 2D Convolution parameters (parent: PcOperation)
- PcDropout: Dropout parameters (parent: PcOperation)
- PcElu: ELU parameters (parent: PcOperation)
- PcEngine: Engine-scoped parameter
- PcEngineJax: JAX engine defaults (parent: PcEngine)
- PcEngineJena: Jena engine defaults (parent: PcEngine)
- PcEngineLibTorch: LibTorch engine defaults (parent: PcEngine)
- PcEngineOpenCv: OpenCV engine defaults (parent: PcEngine)
- PcEngineOpenFoam: OpenFOAM engine defaults (parent: PcEngine)
- PcEngineOrTools: OR-Tools engine defaults (parent: PcEngine)
- PcEnginePetscTao: PETSc TAO engine defaults (parent: PcEngine)
- PcGelu: GELU parameters (parent: PcOperation)
- PcGroupNorm: Group Normalization parameters (parent: PcOperation)
- PcLayerNorm: Layer normalization parameters (parent: PcOperation)
- PcLeakyRelu: Leaky ReLU parameters (parent: PcOperation)
- PcMain: Main Parameter
- PcMaxPool2d: 2D Max Pooling parameters (parent: PcOperation)
- PcMultiHeadAttention: Multi-head attention parameters (parent: PcOperation)
- PcOperation: Operation-scoped parameter
- PcPositionalEncoding: Sinusoidal positional encoding parameters (parent: PcOperation)
- PcReduction: Reduction parameters (parent: PcOperation)
- PcRmsNorm: RMS normalization parameters (parent: PcOperation)
- PcRotaryEmbedding: Rotary position embedding parameters (parent: PcOperation)
- PcScaledDotProductAttention: Scaled dot-product attention parameters (parent: PcOperation)
- PcSoftmax: Softmax family parameters (parent: PcOperation)
- PcTensorLogSoftmax: Log-softmax parameters (parent: PcSoftmax)
- PcTensorMax: Maximum parameters (parent: PcReduction)
- PcTensorMean: Mean parameters (parent: PcReduction)
- PcTensorMin: Minimum parameters (parent: PcReduction)
- PcTensorPow: Power parameters (parent: PcOperation)
- PcTensorSoftmax: Softmax parameters (parent: PcSoftmax)
- PcTensorSum: Sum parameters (parent: PcReduction)
- PcVisualization: Visualization defaults
- PcVizAxes: Axes defaults (parent: PcVisualization)
- PcVizChart: Chart defaults (parent: PcVisualization)
- PcVizMarks: Marks defaults (parent: PcVisualization)
- PcVizPalette: Palette defaults (parent: PcVisualization)

## ParameterGroup — Parameter Group
- PgAdvancedControl: Advanced Control Parameter (parent: PgControl)
- PgControl: Control Parameter
- PgEngineDefaults: Engine Defaults Group
- PgMainControl: Main Control Parameter (parent: PgControl)
- PgMonitoring: Monitoring Parameter
- PgVisualization: Visualization and Rendering Defaults Group
- PgVizAxes: Axes and Grid Defaults (parent: PgVisualization)
- PgVizMarks: Mark and Geometry Defaults (parent: PgVisualization)
- PgVizPalette: Color Palette Defaults (parent: PgVisualization)
- PgVizTypography: Typography Defaults (parent: PgVisualization)

## ParameterPermission — Parameter Permission
- PpeRead: Read
- PpeReadWrite: Read/Write
- PpeWrite: Write

## ParameterPurpose — Parameter Purpose
- PpBatchSize: Batch Size (parent: PpMlHyperparameter)
- PpBoundaryCondition: Boundary Patch Field Specification (parent: PpControl)
- PpCondition: Condition (parent: PpMonitoring)
- PpConstraint: Constraint
- PpControl: Control
- PpDeviceConfiguration: Device Configuration
- PpDeviceTelemetry: Device Telemetry
- PpDirichletBoundaryCondition: Dirichlet Boundary Condition (parent: PpBoundaryCondition)
- PpDropoutRate: Dropout Rate (parent: PpMlHyperparameter)
- PpElectrical: Electrical property
- PpEpochs: Epochs (parent: PpMlHyperparameter)
- PpEvent: Event (parent: PpMonitoring)
- PpFeedback: Feedback (parent: PpMonitoring)
- PpFluidProperty: Fluid Transport/Thermodynamic Property (parent: PpPhysical)
- PpInitialCondition: Initial Condition
- PpLearningRate: Learning Rate (parent: PpMlHyperparameter)
- PpMathModel: Math Model Parameter
- PpMechanical: Mechanical property
- PpMesh: Mesh Parameter
- PpMeshMaterial: Mesh Material Property Assignment
- PpMeshRendering: Mesh Visual/Rendering Property Assignment
- PpMixedBoundaryCondition: Mixed Boundary Condition (parent: PpBoundaryCondition)
- PpMlHyperparameter: Machine Learning Hyperparameter
- PpMomentum: Momentum (parent: PpMlHyperparameter)
- PpMonitoring: Monitoring
- PpNeumannBoundaryCondition: Neumann Boundary Condition (parent: PpBoundaryCondition)
- PpNumericalScheme: FVM Discretization Scheme (parent: PpControl)
- PpOptical: Optical/visual property
- PpPhysical: Physical quantity
- PpRendering: Rendering/shading-related property
- PpSample: Sample (parent: PpMonitoring)
- PpSolverControl: Simulation Runtime & Convergence Control (parent: PpControl)
- PpStatus: Status (parent: PpMonitoring)
- PpThermal: Thermal property
- PpWeightDecay: Weight Decay (parent: PpMlHyperparameter)

## ParameterType — Parameter Type
- PtBitSet: BitSet (parent: PtEnumeration)
- PtByte: Byte (parent: PtEnumeration)
- PtCurrencyAmount: Currency Amount (parent: PtNumber)
- PtCurrencyPrecise: Currency Precise (parent: PtNumber)
- PtDate: Date
- PtDateTime: Date Time
- PtEnumeration: Enumeration
- PtMatrix: Matrix Parameter
- PtNumber: Number
- PtNumberDecimal: Number Decimal (parent: PtNumber)
- PtNumberFloat: Number Float (parent: PtNumber)
- PtNumberInteger: Number Integer (parent: PtNumber)
- PtText: Text
- PtTextIndicator: Text Indicator (parent: PtText)
- PtTextLong: Text Long (parent: PtText)
- PtTextShort: Text Short (parent: PtText)
- PtTime: Time
- PtVector: Vector Parameter

## ParametricPathCompositionMethod — Parametric Path Composition Method
- PpcmBezierBlend: Bezier Blend
- PpcmCircularBlend: Circular Blend
- PpcmCubicBlend: Cubic Blend
- PpcmCustomBlend: Custom User-Defined Blend
- PpcmCycloidalBlend: Cycloidal Blend
- PpcmDoubleS: Double S-curve Blend
- PpcmHarmonicBlend: Harmonic Blend
- PpcmLinearBlend: Linear Blend
- PpcmParabolicBlend: Parabolic Blend
- PpcmPlcAborting: PLCopen Aborting - abort current segment, start next immediately
- PpcmPlcBlendingHigh: PLCopen Blending High - blend at the higher of the two segment velocities
- PpcmPlcBlendingLow: PLCopen Blending Low - blend at the lower of the two segment velocities
- PpcmPlcBlendingNext: PLCopen Blending Next - blend at velocity of next segment
- PpcmPlcBlendingPrev: PLCopen Blending Previous - blend at velocity of previous segment
- PpcmPlcBuffered: PLCopen Buffered - queue next segment, start after current completes
- PpcmPlcTMConstVel: PLCopen TMConstantVelocity - maintain constant velocity through transition
- PpcmPlcTMCornerDist: PLCopen TMCornerDistance - blend within corner radius (ParametricPathPoint.tolerance)
- PpcmPlcTMMaxVel: PLCopen TMMaxVelocity - maximize velocity through the transition
- PpcmPlcTMNone: PLCopen TMNone - exact stop at the point, no geometric blending
- PpcmPlcTMStartVel: PLCopen TMStartVelocity - continue at current speed into next segment
- PpcmPolynomialBlend: Polynomial Blend
- PpcmSplineBlend: Spline Blend

## ParametricPathContentType — Parametric Path Content Type
- PpCntCsv: CSV Parametric Path Data
- PpCntDxf: DXF (Drawing Exchange Format) Geometric Path
- PpCntGCode: G-code (Numerical Control Programming Language) Parametric Path Data
- PpCntJson: JSON Parametric Path Data
- PpCntXml: XML  Parametric Path Data
- PpCntYaml: YAML Parametric Path Data

## ParametricPathEventType — Parametric Path Event Type
- PpetCustom: Custom Action
- PpetStart: Start Event
- PpetStop: Stop Event

## ParametricPathProfile — Parametric Path Profile
- Pppf3rdDegPolyProfile: Polynomial of 3rd Degree Profile (parent: PppfPolyProfile)
- Pppf5thDegPolyProfile: Polynomial of 5th Degree Profile (parent: PppfPolyProfile)
- Pppf7thDegPolyProfile: Polynomial of 7th Degree Profile (parent: PppfPolyProfile)
- PppfCycloidalProfile: Cycloidal Profile (parent: PppfTrigProfile)
- PppfDoubleSCurveProfile: Double S-curve Profile (parent: PppfTrajectoryProfile)
- PppfEllipticProfile: Elliptic Profile (parent: PppfTrigProfile)
- PppfHighDegPolyProfile: Polynomial of Higher Degree Profile (parent: PppfPolyProfile)
- PppfParameterProgression: Parameter Progression Profile
- PppfPolyProfile: Polynomial Profile (parent: PppfTrajectoryProfile)
- PppfSCurveProfile: S-curve (Jerk-limited) Profile (parent: PppfTrajectoryProfile)
- PppfTrajectoryProfile: Trajectory Profile
- PppfTrapezoidalProfile: Trapezoidal Velocity Profile  (parent: PppfTrajectoryProfile)
- PppfTrigProfile: Trigonometric Profile (parent: PppfTrajectoryProfile)

## PartyBadgeScanPurpose — Party Badge Scan Purpose
- PbspAccess: Access
- PbspClockIn: Clock In
- PbspClockOut: Clock Out

## PartyBadgeScanResult — Party Badge Scan Result
- PbsrExpired: Expired
- PbsrNotYetValid: Not Yet Valid
- PbsrSuccess: Success

## PartyClassificationType — Party Classification Type
- PcltCustomer: Customer
- PcltEeoc: EEOC (Equal Opportunity)
- PcltIncome: Income
- PcltIndustry: Industry
- PcltMinority: Minority
- PcltNaicsCode: NAICS Code
- PcltNumberEmployees: Number of Employees
- PcltOwnership: Ownership
- PcltRevenue: Revenue
- PcltSicCode: SIC Code

## PartyContentType — Party Content Type
- PcntBio: Bio
- PcntEmplAuthzDocument: Employment Authorization Document
- PcntFaceImage: Face Image
- PcntIdentityDocument: Identity Document
- PcntInternal: Internal Content
- PcntInvoiceMessageFrom: Invoice Message - When From Party
- PcntInvoiceMessageTo: Invoice Message - When To Party
- PcntLogoImage: Logo Image
- PcntPaymentSignaturePrimary: Payment Signature Primary
- PcntPaymentSignatureSecondary: Payment Signature Secondary
- PcntPrimaryImage: Primary Image
- PcntUserDefined: User Defined Content
- PcntVendorShipping: Vendor Shipping Info

## PartyIdType — Party Identification Type
- Ptid94A: I-94A
- PtidArn: Alien Registration Number
- PtidCust: Customer Assigned
- PtidDriverLicense: Driver License Number
- PtidDuns: Dun and Bradstreet DUNS
- PtidDuns4: Dun and Bradstreet DUNS+4
- PtidFaic: Federal Agent Indicator Code
- PtidFein: Federal EIN
- PtidFuid: Federal User ID
- PtidGln: Global Location Number
- PtidI551: I-551
- PtidI766: I-766
- PtidI94: I-94
- PtidIan: Immigrant Admission Number
- PtidMcid: Matricula Consular ID
- PtidPassport: Passport Number
- PtidPermReg: Permanent Resident
- PtidSsn: Social Security Number
- PtidVend: Vendor Assigned

## PartyRelationshipType — Party Relationship Type
- PrtAgent: Agent
- PrtChild: Child
- PrtContact: Contact
- PrtCustomer: Customer
- PrtEmployee: Employee
- PrtFriend: Friend
- PrtManager: Manager
- PrtMember: Organization Member
- PrtOrgRollup: Organization Rollup (Child)
- PrtPartner: Partner
- PrtRepresentative: Representative
- PrtSalesAffiliate: Sales Affiliate
- PrtSpouse: Spouse
- PrtSupplier: Supplier

## PartyType — Party Type
- PtyAutomatedAgent: Automated Agent
- PtyOrganization: Organization
- PtyPerson: Person

## PayDistributionGroup — Payment Distribution Group
- PdgEmployeeExecutive: Employee - Executive
- PdgEmployeeLabor: Employee - Labor
- PdgEmployeeRegular: Employee - Regular
- PdgSupplierGeneral: Supplier - General

## PaymentContentType — Payment Content Type
- PctCheckImage: Check Image
- PctPaymentDocument: Payment Document
- PctReceipt: Receipt

## PaymentGatewayType — Payment Gateway Type
- PgtFinancialAccount: Financial Account
- PgtTest: Test

## PaymentInstrument — Payment Instrument
- PiAch: ACH Direct
- PiAmazonPay: Amazon Pay
- PiBillingAccount: Billing Account
- PiBitcoinWallet: Bitcoin
- PiCash: Cash
- PiCertifiedCheck: Certified Check
- PiCod: Cash On Delivery
- PiCompanyAccount: Company Account
- PiCompanyCheck: Company Check
- PiCreditCard: Credit Card
- PiDebitCard: Debit Card
- PiFinancialAccount: Financial Account
- PiGiftCard: Gift Card
- PiGiftCertificate: Gift Certificate
- PiMoneyOrder: Money Order
- PiOther: Other
- PiPayPalAccount: PayPal Account
- PiPersonalCheck: Personal Check
- PiWireTransfer: Wire Transfer

## PaymentMethodContentType — Payment Method Content Type
- PmctImage: Image
- PmctSignaturePrimary: Signature Primary
- PmctSignatureSecondary: Signature Secondary

## PaymentMethodFileType — Payment Method File Type
- PmftBai2: BAI 2
- PmftBankOfAmericaAr: Bank of America AR PNV (parent: PmftPositivePay)
- PmftCityBankCnb: City Bank CNB (parent: PmftPositivePay)
- PmftNacha: NACHA
- PmftOfx: OFX/QFX
- PmftPositivePay: Positive Pay File (parent: PmftPositivePay)
- PmftSunTrustCpr: SunTrust CPR (parent: PmftPositivePay)
- PmftWachoviaAr: Wachovia AR (parent: PmftPositivePay)
- PmftWellsFargoArp: Wells Fargo ARP (parent: PmftPositivePay)
- PmftZionsBankCsv: Zions Bank CSV (parent: PmftPositivePay)

## PaymentMethodPurpose — Payment Method Purpose
- PmpGeneral: General
- PmpPayroll: Payroll
- PmpReturnRefund: Return Refund
- PmpSalesRevenue: Sales Revenue

## PaymentMethodTransType — Payment Method Trans Type
- PMTT_ATM: ATM debit or credit
- PMTT_CASH: Cash withdrawal
- PMTT_CHECK: Check
- PMTT_CREDIT: Generic credit
- PMTT_DEBIT: Generic debit
- PMTT_DEP: Deposit
- PMTT_DIRECTDEBIT: Merchant initiated debit
- PMTT_DIRECTDEP: Direct deposit
- PMTT_DIV: Dividend
- PMTT_FEE: FI fee
- PMTT_INT: Interest earned or paid
- PMTT_OTHER: Other
- PMTT_PAYMENT: Electronic payment
- PMTT_POS: Point of sale debit or credit
- PMTT_REPEATPMT: Repeating payment/standing order
- PMTT_SRVCHG: Service charge
- PMTT_XFER: Transfer
- PMTT_ZBA_CRTR: ZBA Credit Transfer
- PMTT_ZBA_DBTR: ZBA Debit Transfer

## PaymentMethodType — Payment Method Type
- PmtAmazonPayAccount: Amazon Pay Account
- PmtBankAccount: Bank Account
- PmtBitcoinWallet: Bitcoin Wallet
- PmtCreditCard: Credit Card
- PmtFinancialAccount: Financial Account
- PmtGiftCard: Gift Card
- PmtOther: Other Type (no detail record)
- PmtPayPalAccount: PayPal Account

## PaymentOperation — Payment Gateway Operation
- PgoAuthAndCapture: Authorize and Capture
- PgoAuthorize: Authorize
- PgoCapture: Capture
- PgoLevel3Data: Level 2/3 Data
- PgoRefund: Refund
- PgoRelease: Release
- PgoStoreCim: Store CIM Profile
- PgoTxDetails: Transaction Details
- PgoValidateAuthorize: Validate Authorize

## PaymentType — Payment Type
- PtDisbursement: Disbursement
- PtFinancialAccount: Financial Account Transaction
- PtInvoicePayment: Invoice Payment
- PtOrderPref: Order Payment Preference
- PtPayrollOtherPayment: Payroll Other Payment (parent: PtInvoicePayment)
- PtPayrollPayment: Payroll Employee Payment (parent: PtInvoicePayment)
- PtPrePayment: Pre Payment - Expense (parent: PtInvoicePayment)
- PtPrePaymentInventory: Pre Payment - Inventory (parent: PtInvoicePayment)
- PtRefund: Refund

## PayrollAllowanceAmountType — Payroll Allowance Amount Type
- PaatDeduction: Deduction
- PaatExemption: Exemption

## PayrollCalcPer — Payroll Calc Period
- PcfPayPeriod: Pay Period
- PcfWorkweek: Workweek

## PayrollPhase — Payroll Calculation Phase
- PrphBonus: Incentive Bonus
- PrphBreak: Break Adjust (piece, etc)
- PrphDeductible: Deductible, Discretionary Bonus
- PrphExpenses: Expenses, Reimbursement
- PrphGarnish: Garnish
- PrphOvertime: Overtime
- PrphTax: Taxes, WC, etc

## PayrollRateBasis — Payroll Rate Basis
- PrbsGross: Gross
- PrbsHours: Hours Worked
- PrbsIncome: Income Taxable
- PrbsMedical: Medical Taxable
- PrbsSocial: Social Taxable
- PrbsStraightGross: Straight Time Gross

## PayrollTaxForm — Payroll Tax Form
- PtxfUsIrs941: US IRS Form 941
- PtxfUsIrs943: US IRS Form 943
- PtxfUsIrs944: US IRS Form 944
- PtxfUsIrsCT1: US IRS CT-1
- PtxfUsIrsSchH: US IRS Schedule H

## PayrollWageGrp — Payroll Wage Grouping
- PwgAll: All
- PwgFacility: Facility
- PwgFacilityOwner: Facility Owner
- PwgTimeEntry: Time Entry

## PieceRateType — Piece Rate Type
- RatpPieceOnly: Piece
- RatpPieceOrHour: Piece or Hourly
- RatpPiecePlusHour: Piece plus Hourly

## PrinterPurpose — Printer Purpose
- PtpContainerLabel: Container Label
- PtpPackageLabel: Package Label
- PtpPackingDocuments: Packing Documents
- PtpPickingDocuments: Picking Documents
- PtpShipmentDocuments: Shipment Documents

## ProductAssocType — Product Association Type
- PatAccessory: Accessory
- PatAddOn: Add On For
- PatAlsoBought: Also Bought
- PatAlternativePkg: Alternative Packaging
- PatAutoReorder: Auto Reorder (needs recurrenceInfoId)
- PatComponent: Actual Product Component
- PatConfigInstance: Configurable Product Instance
- PatCrossSell: Cross-Sell (Complementary)
- PatDownSell: Down-Sell (Downgrade)
- PatEngBom: Engineering Bill of Materials (parent: PatComponent)
- PatEquivalent: Equivalent or Substitute
- PatIncompatible: Incompatible
- PatMfgAs: Product Manufactured As
- PatMfgBom: Manufacturing Bill of Materials (parent: PatComponent)
- PatPackagingFor: Packaging For
- PatRefurbished: Refurbished Equivalent
- PatRepairService: Repair Service
- PatReplacement: New Version, Replacement
- PatRequires: Requires
- PatRevision: Revision
- PatUniqueItem: Unique Item
- PatUpsell: Up-Sell (Upgrade)
- PatUsedToProduce: Used to Produce
- PatVariant: Product Variant

## ProductCategoryContentType — Product Category Content Type
- PcctCategoryName: Category Name
- PcctDescription: Description
- PcctDescriptionLong: Description - Long
- PcctFooter: Footer
- PcctImageAltText: Category Image Alt Text
- PcctImageUrl: Category Image URL
- PcctMetaDescription: Meta-Description
- PcctMetaKeywords: Meta-Keywords

## ProductCategoryIdentType — Product Category Ident Type
- PcitUrlSlug: URL Slug

## ProductCategoryType — Product Category Type
- PctBestSelling: Best Selling
- PctCatalog: Catalog
- PctCrossSell: Cross Sell
- PctGiftCard: Gift Card
- PctIndustry: Industry
- PctInternal: Internal
- PctInventoryGroup: Inventory Group
- PctMaterials: Materials
- PctMixMatch: Mix and Match
- PctQuickAdd: Quick Add
- PctSearch: Search
- PctTax: Tax
- PctUsage: Usage

## ProductClass — Product Class
- PclsGiftCard: Gift Card or Certificate

## ProductContentType — Product Content Type
- PcntAddToCartImage: Add To Cart Image
- PcntAddToCartLabel: Add To Cart Label
- PcntDeliveryInfo: Delivery Info
- PcntDescription: Description
- PcntDescriptionLong: Description - Long
- PcntDirections: Directions
- PcntDownload: Digital Download
- PcntEmail: Fulfillment Email
- PcntFAQ: Frequently Asked Questions
- PcntImageDetail: Image - Detail
- PcntImageLarge: Image - Large
- PcntImageMedium: Image - Medium
- PcntImageOriginal: Image - Original
- PcntImageSmall: Image - Small
- PcntImageUrlDetail: Image URL - Detail
- PcntImageUrlLarge: Image URL - Large
- PcntImageUrlMedium: Image URL - Medium
- PcntImageUrlOriginal: Image URL - Original
- PcntImageUrlSmall: Image URL - Small
- PcntIngredients: Ingredients
- PcntInstallation: Installation
- PcntLabelImage: Label Image
- PcntLabelText: Label Text
- PcntMetaDescription: Meta-Description
- PcntMetaKeywords: Meta-Keywords
- PcntOnline: Online Access
- PcntPriceDetail: Price Detail Text
- PcntProductName: Product Name
- PcntShortSalesPitch: Short Sales Pitch
- PcntSpecialInstr: Special Instructions
- PcntSpecification: Specification
- PcntTermsConditions: Terms and Conditions
- PcntTestimonials: Testimonials
- PcntUniqueIngred: Ingredients - Unique
- PcntWarnings: Warnings
- PcntWarranty: Warranty

## ProductFeatureApplType — Product Feature Appl Type
- PfatDistinguishing: Distinguishing
- PfatOptional: Optional
- PfatSelectable: Selectable
- PfatStandard: Standard

## ProductFeatureIactnType — Product Feature Interaction Type
- PfitCompatible: Compatible
- PfitComposition: Composition
- PfitDependency: Dependency
- PfitIncompatible: Incompatible

## ProductFeatureType — Product Feature Type
- PftAccessory: Accessory
- PftAmount: Amount
- PftArtist: Artist
- PftBilling: Billing
- PftBrand: Brand
- PftCare: Care
- PftColor: Color
- PftDimension: Dimension
- PftEquipClass: Equipment Class
- PftFabric: Fabric
- PftGenre: Genre
- PftHardware: Hardware
- PftLicense: License
- PftModelYear: Model Year
- PftNetWeight: Net Weight
- PftOrigin: Origin
- PftOther: Other
- PftPackagingComponent: Packaging Component
- PftPackagingType: Packaging Type
- PftProdQuality: Product Quality
- PftSize: Size
- PftSoftware: Software
- PftStyle: Style
- PftSymptom: Symptom
- PftTopic: Topic
- PftType: Type
- PftWarranty: Warranty
- PftYearMade: Year Made

## ProductFormType — Product Form Type
- PfmtPostSaleSurvey: Post Sale Survey
- PfmtSalesOptional: Sales Optional Info
- PfmtSalesRequired: Sales Required Info

## ProductGeoPurpose — Product Geo Purpose
- PgpPurchaseExclude: Purchase Exclude
- PgpPurchaseInclude: Purchase Include
- PgpShipmentExclude: Shipment Exclude
- PgpShipmentInclude: Shipment Include

## ProductIdentificationType — Product Identification Type
- PidtEan: EAN
- PidtGtin: GTIN
- PidtHts: HTS (Tariff)
- PidtIsbn: ISBN
- PidtLoc: Library of Congress
- PidtMfgModelNum: Mfg Model Number
- PidtOther: Other
- PidtSku: SKU
- PidtUpca: UPC-A
- PidtUpce: UPC-E
- PidtUrlSlug: URL Slug

## ProductPricePurpose — Product Price Purpose
- PppComponent: Component Price
- PppPurchase: Purchase/Initial
- PppRecurring: Recurring Charge
- PppUsage: Usage Charge

## ProductPriceType — Product Price Type
- PptAverage: Average Cost
- PptCompetitive: Competitive Price
- PptCurrent: Current Price
- PptList: List Price
- PptMaximum: Maximum Price
- PptMinimum: Minimum Price
- PptPromotional: Promotional Price
- PptSpecialPromo: Special Promo Price
- PptWholesale: Wholesale Price

## ProductStoreCategoryType — Product Store Category Type
- PsctAdminAllow: Admin Allow (One)
- PsctBrowseRoot: Browse Root (One)
- PsctFeatured: Featured (One)
- PsctHomePage: Home Page (One)
- PsctNewProducts: New Products (One)
- PsctPromotions: Promotions (One)
- PsctPurchaseAllow: Purchase Allow (One)
- PsctQuickAdd: Quick Add (Many)
- PsctQuickInternal: Quick Add Internal (Many)
- PsctSearch: Default Search (One)
- PsctViewAllow: View Allow (One)

## ProductStoreContentType — Product Store Content Type
- PsctAccountCreateTemplate: Account Create Template - Client
- PsctAccountTemplate: Account Template - Client
- PsctCategoryTemplate: Category Template - Client
- PsctCategoryTemplateServer: Category Template - Server
- PsctCheckoutHeaderTemplate: Checkout Header Template - Client
- PsctCheckoutSuccessTemplate: Checkout Success Template - Client
- PsctCheckoutTemplate: Checkout Template - Client
- PsctFooterTemplate: Footer Template - Client
- PsctFooterTemplateServer: Footer Template - Server
- PsctHeaderTemplate: Header Template - Client
- PsctHeaderTemplateServer: Header Template - Server
- PsctHomeTemplate: Home Template - Client
- PsctHomeTemplateServer: Home Template - Server
- PsctLoginTemplate: Login Template - Client
- PsctOrderDetailTemplate: Order Detail Template - Client
- PsctOrderHistoryTemplate: Order History Template - Client
- PsctProductTemplate: Product Template - Client
- PsctProductTemplateServer: Product Template - Server
- PsctResetPasswordTemplate: Reset Password Template - Client
- PsctRootTemplateServer: Root Template - Server
- PsctSearchTemplate: Search Template - Client

## ProductStoreDataDocumentType — Product Store Data Document Type
- PsdtBlog: Blog Search
- PsdtCategory: Category Search
- PsdtContent: Content Search
- PsdtProduct: Product Search

## ProductStoreEmailType — Product Store Email Notification Type
- PsetBackOrder: Back-Order Notice
- PsetGiftCardPurchase: Gift Card Purchase
- PsetGiftCardReload: Gift Card Reload
- PsetInvoiceFinalized: Invoice Finalized
- PsetInvoicesPastDue: Invoices Past Due
- PsetOrderApproved: Order Approved
- PsetOrderChange: Order Change
- PsetOrderComplete: Order Complete
- PsetOrderPlaced: Order Placed
- PsetOrderProposed: Order Quote Proposed
- PsetOrderRequested: Order Quote Requested
- PsetPaymentRetry: Payment Retry
- PsetRegistration: Registration
- PsetResetPassword: Reset Password
- PsetReturnAccepted: Return Accepted
- PsetReturnCancelled: Return Cancelled
- PsetReturnCompleted: Return Completed
- PsetShipmentDelivered: Shipment Delivered
- PsetShipmentShipped: Shipment Shipped
- PsetTellAFriend: Tell-A-Friend

## ProductStoreSettingType — Product Store Setting Type
- PsstContentAttachmentLoc: Content Attachment Location
- PsstContentLocation: Content Location
- PsstGetReturnLabels: Get Return Labels (true/false)
- PsstOrdApproveAddrMissing: Order Approve Warn Address Missing (false to disable)
- PsstOrdApproveAddrNotValid: Order Approve Warn Address not Valid (false to disable)
- PsstOrdApproveBillShipAddrDiff: Order Approve Warn Billing and Shipping Addresses Differ (false to disable)
- PsstOrdApproveContactBlacklist: Order Approve Warn Contact Mech Grey/Blacklisted (false to disable)
- PsstOrdApproveInventoryNotAvail: Order Approve Warn Inventory Not Available (false to disable)
- PsstOrdApproveLargeOrder: Order Approve Warn Large Order - Total Above (default 0, 0 to disable)
- PsstOrdApproveLargeWebOrder: Order Approve Warn Large Web Order - Total Above (default 0, 0 to disable)
- PsstOrdApproveNewCust: Order Approve Warn New Customer (false to disable)
- PsstOrdApprovePayMethNameDiff: Order Approve Warn Payment Method Name Differs (false to disable)
- PsstOrdApprovePercAvailInv: Order Approve Warn Percent Available Inventory (default 20, 0 to disable)
- PsstOrdApprovePriceMinMax: Order Approve Warn Price Min/Max (false to disable)
- PsstOrdApproveSimilar: Order Approve Warn Similar within 24hrs (false to disable)
- PsstOrdApproveStdDevProdQty: Order Approve Warn Std Devs Over Avg Product Qty (default 3.0, 0 to disable)
- PsstOrdApproveStdDevTotal: Order Approve Warn Std Devs Over Avg Total (default 3.0, 0 to disable)
- PsstProductDetailUrl: Product Detail URL GString
- PsstProductImageLoc: Product Image Location
- PsstProductImageUrl: Product Image URL GString
- PsstRestApiLocation: REST API Location
- PsstShipLabelCompany: Ship Label From Company
- PsstShipLabelMarkup: Shipping Label Cost Markup Percent
- PsstShipLabelName: Ship Label From Name
- PsstShipOrderMarkup: Shipping Order Charge Markup Percent
- PsstShipRestrictCarriers: Ship Restrict Carriers (true/false)
- PsstTemplateInvoicePrint: Template Location Invoice Print
- PsstTemplateOrderPrint: Template Location Order Print
- PsstTemplateShipmentByPackage: Template Location Shipment By Package
- PsstTemplateShipmentInsert: Template Location Shipment Insert
- PsstTemplateShipmentPack: Template Location Shipment Pack Sheet
- PsstTemplateShipmentPick: Template Location Shipment Pick Sheet

## ProductStoreWikiSpaceType — Product Store Wiki Space Type
- PstBlog: Content - Blog Posts
- PstFull: Content - Full Page
- PstSnip: Content - Snippet
- PstTmpClt: Template - Interactive (checkout, profile, etc)
- PstTmpSrv: Template - Information (home, product, etc)

## ProductType — Product Type
- PtAsset: Asset (Good)
- PtAssetUse: Asset Use
- PtConfigurable: Configurable Good
- PtDigital: Digital (download)
- PtDigitalAsset: Digital and Asset
- PtFacilityUse: Facility Use
- PtPickAssembly: Pick Assembly
- PtService: Service
- PtVirtual: Virtual (with variants)

## RateModifier — Pay Rate Modifier
- RatmDouble: Double Time
- RatmOvertime: Overtime
- RatmRegular: Regular

## RatePurpose — Rate Purpose
- RaprClient: Client Billing
- RaprVendor: Worker/Vendor Payment

## RateType — Hourly Rate Type
- RatpDiscounted: Discounted
- RatpEvening: Shift - Evening
- RatpHoliday: PTO - Holiday
- RatpNight: Shift - Night
- RatpNoCharge: No Charge
- RatpOnsite: On-site
- RatpPaidBreakRrp: Paid Break RRP
- RatpPaidBreakStd: Paid Break STD
- RatpPaidNptRrp: NPT - RRP
- RatpPaidNptStd: NPT - STD
- RatpPieceMinWageAdj: Min Wage Adj
- RatpPtoOther: PTO - Other
- RatpShHoliday: Shift - Holiday
- RatpSick: PTO - Sick
- RatpStandard: Standard
- RatpUnpaid: Unpaid
- RatpVacation: PTO - Vacation
- RatpWeekend: Shift - Weekend

## RejectionReason — Rejection Reason
- ArjDamaged: Damaged
- ArjLost: Lost in Transit
- ArjNotOrdered: Not Ordered
- ArjNotToSpec: Not to Specification
- ArjOverShipped: Over Shipped

## RequestContentType — Request Content Type
- RqCntDocumentation: Documentation
- RqCntImage: Image
- RqCntInternal: Internal
- RqCntStory: Story
- RqCntUserDefined: User Defined

## RequestResolution — Request Resolution
- RrCantReproduce: Can't Reproduce
- RrCompleted: Completed
- RrDuplicate: Duplicate
- RrFixed: Fixed
- RrInsufficient: Insufficient Information
- RrRejected: Rejected
- RrUnresolved: Unresolved
- RrWontFix: Won't Fix

## RequestType — Request Type
- RqtBugFix: Bug Fix
- RqtContact: Contact Us
- RqtInformation: Information
- RqtInventory: Inventory
- RqtNewFeature: New Feature
- RqtProposal: Proposal
- RqtPurchase: Purchase
- RqtQuote: Quote
- RqtSupport: Support

## RequirementType — Requirement Type
- RqTpCustomer: Customer
- RqTpInternal: Internal
- RqTpInventory: Inventory
- RqTpProduct: Product
- RqTpWork: Work

## ResidenceStatus — Residence Status
- RessOwn: Own Home
- RessParents: With Parents
- RessPrivateTenant: Private Tenant
- RessPublicTenant: Public Tenant

## ReturnReason — Return Reason
- RrsnArrivedLate: 08 Arrived Too Late
- RrsnBetterPrice: 10 Found Better Price
- RrsnCodPmtRejected: 13 COD Payment Rejected
- RrsnDamagedShip: 01 Damaged in Shipping
- RrsnDefective: 02 Defective
- RrsnDidNotWant: 09 Did not Want/Like
- RrsnDupShip: 06 Duplicate Shipment
- RrsnGiftNotWant: 07 Gift, Not Wanted
- RrsnMisShip: 03 Wrong Item Shipped
- RrsnNotExpected: 04 Not as Expected
- RrsnPoorService: 11 Poor Customer Service
- RrsnUnlikeDescribed: 12 Unlike Photo/Description
- RrsnWrongSize: 05 Did not Fit/Wrong Size

## ReturnResponse — Return Response
- RrspCredit: Credit
- RrspManual: Manual
- RrspRefund: Refund
- RrspReplace: Replace

## RoleGroup — Role Group
- RgpAccountContact: Account Contact Roles
- RgpAgreement: Agreement Roles
- RgpCalendar: Calendar Roles
- RgpDirect: Directly Applied Roles
- RgpOrder: Order Roles
- RgpOrganization: Organization Roles
- RgpPerson: Person Roles
- RgpProject: Project
- RgpProjectClient: Project Client
- RgpProjectVendor: Project Vendor
- RgpRequest: Request
- RgpShipment: Shipment Roles
- RgpTask: Task

## SalesChannel — Sales Channel
- ScAffiliate: Affiliate
- ScAmazon: Amazon
- ScEbay: eBay
- ScEdi: EDI
- ScEmail: E-Mail
- ScFax: Fax
- ScOagis: OAGIS
- ScPhone: Phone
- ScPos: POS
- ScPostal: Postal Mail
- ScTest: Test Order
- ScUnknown: Unknown
- ScWeb: Web
- ScWebExternal: Web External

## ScreenThemeResourceType — Screen Theme Resource Type
- STRT_BODY_CLASS: HTML Body CSS Class
- STRT_FOOTER_ITEM: Footer Item
- STRT_HEADER_ACCOUNT_COMP: Header Account Component
- STRT_HEADER_LOGO: Header Logo URL
- STRT_HEADER_NAVBAR_COMP: Header Navbar Component
- STRT_HEADER_NAVBAR_ITEM: Header Navbar Item
- STRT_HEADER_TITLE: Header Title
- STRT_SCREENSHOT: Theme Preview Screenshot
- STRT_SCRIPT: Script URL
- STRT_SCRIPT_FOOTER: Script Footer URL
- STRT_SHORTCUT_ICON: Shortcut Icon URL
- STRT_STYLESHEET: Style Sheet (CSS) URL

## ScreenThemeType — Screen Theme Type
- STT_ERROR: Error Screens
- STT_INTERNAL: Internal Applications
- STT_INTERNAL_QUASAR: Internal Applications - Quasar
- STT_POP_COMMERCE: POP Commerce Theme Type
- STT_PUBLIC: Public Web Site/etc

## ServiceRegisterType — Service Register Type
- OrderValidate: Order Approve Validate
- PayrollAdjustmentCalc: Payroll Adjustment Calculation
- ProductPriceModify: Product Price Modify
- ProductStorePromotion: Product Store Promotion
- SettleTermOrderPmt: Settlement Term - Generate Order Payments

## ShipmentMethod — Shipment Method
- ShMthGround: Ground Parcel
- ShMthGroundCom: Ground Commercial
- ShMthMotor: Motor (Common Carrier)
- ShMthNextDay: Next Day Standard
- ShMthNextDayPri: Next Day Priority
- ShMthPickUp: Customer Pick Up
- ShMthSecondDay: Second Day
- ShMthThirdDay: Third Day

## ShipmentTrackingStatus — Shipping Tracking Status
- ShTsDelivered: Delivered
- ShTsFailure: Failure
- ShTsReturned: Returned
- ShTsTransit: In Transit
- ShTsUnknown: Unknown

## ShipmentType — Shipment Type
- ShpTpDrop: Drop Shipment
- ShpTpIncoming: Incoming
- ShpTpOutgoing: Outgoing
- ShpTpPurchase: Purchase Shipment (parent: ShpTpIncoming)
- ShpTpPurchaseReturn: Purchase Return (parent: ShpTpOutgoing)
- ShpTpSales: Sales Shipment (parent: ShpTpOutgoing)
- ShpTpSalesReturn: Sales Return (parent: ShpTpIncoming)
- ShpTpTransfer: Transfer

## ShippingGatewayOption — Shipping Gateway Option
- SgoApiToken: API Token
- SgoLabelType: Label Type

## ShippingGatewayType — Shipping Gateway Type
- ShGtwyLocal: Local Shipping Gateway

## SignatureRequired — Signature Required
- PsrAdult: Adult
- PsrCertified: Certified (USPS)
- PsrIndirect: Indirect (FedEx)
- PsrNone: None
- PsrStandard: Standard

## SixteenPointCompass — Sixteen Point Compass
- SPC_E: East (90°)
- SPC_ENE: East Northeast (67.5°)
- SPC_ESE: East Southeast (112.5°)
- SPC_N: North (0°)
- SPC_NE: Northeast (45°)
- SPC_NNE: North Northeast (22.5°)
- SPC_NNW: North Northwest (337.5°)
- SPC_NW: Northwest (315°)
- SPC_S: South (180°)
- SPC_SE: Southeast (135°)
- SPC_SSE: South Southeast (157.5°)
- SPC_SSW: South Southwest (202.5°)
- SPC_SW: Southwest (225°)
- SPC_W: West (270°)
- SPC_WNW: West Northwest (292.5°)
- SPC_WSW: West Southwest (247.5°)

## SpaceDimension — Space Dimension
- DimX: X Dimension
- DimY: Y Dimension
- DimZ: Z Dimension

## SubscriptionType — Subscription Type
- StProduct: Product

## SupplierPreferredOrder — Supplier Preferred Order
- SpoAlternate: Alternate Supplier
- SpoMain: Main Supplier

## SystemMessageAuthType — System Message Auth Type
- SmatHmacSha256: HMAC SHA-256
- SmatHmacSha256Timestamp: HMAC SHA-256 with Timestamp
- SmatLogin: User Login (basic, api_key, etc)
- SmatNone: No Auth

## TaxAuthorityAssocType — Tax Authority Assoc Type
- TaatCollAgent: Collection Agent
- TaatExemption: Exemption Inheritance

## TaxAuthorityType — Tax Authority Type
- TatCity: City
- TatCounty: County/Parish/Borough
- TatFederal: Federal/Country
- TatState: State/Province

## TaxClassification — Tax Classification
- TxcCCorp: USA - C Corporation
- TxcIndividual: USA - Individual, Sole Proprietor, Single-member LLC
- TxcLlcCCorp: USA - LLC as C Corp
- TxcLlcPartnership: USA - LLC as Partnership
- TxcLlcSCorp: USA - LLC as S Corp
- TxcOther: Other
- TxcPartnership: USA - Partnership
- TxcSCorp: USA - S Corporation
- TxcTrustEstate: USA - Trust/Estate

## TaxDepreciationType — Tax Depreciation Type
- TxdtMacrsGds5Yr: MACRS GDS 5 Year
- TxdtMacrsGds7Yr: MACRS GDS 7 Year

## TaxFederalStatus — Tax Federal Status
- TfsDoNotWithhold: Do Not Withhold
- TfsMarriedJoint: Married File Joint
- TfsSingle: Single or Married File Separate

## TaxForm — Tax Form
- TxfUsIrs1040: US IRS Form 1040
- TxfUsIrs1065: US IRS Form 1065
- TxfUsIrs1120: US IRS Form 1120
- TxfUsIrs1120S: US IRS Form 1120S
- TxfUsIrs990: US IRS Form 990
- TxfUsIrs990PF: US IRS Form 990-PF
- TxfUsIrs990T: US IRS Form 990-T

## TaxGatewayType — Tax Gateway Type
- TaxGtwyLocal: Local Tax Gateway

## TaxStateStatus — Tax State Status
- TssDoNotWithhold: Do Not Withhold
- TssHeadHousehold: Unmarried Head of Household
- TssMarriedFileJoint1: Married File Joint 1 Income
- TssMarriedFileJoint2: Married File Joint 2+ Incomes
- TssMarriedSeparate: Married File Separate
- TssSingle: Single

## TcpPoseDimension — TCP Pose Dimension
- DimTcpA: TCP A Orientation
- DimTcpB: TCP B Orientation
- DimTcpC: TCP C Orientation
- DimTcpX: TCP X Position
- DimTcpY: TCP Y Position
- DimTcpZ: TCP Z Position

## TensorApproxMethod — Tensor Approximation / Compression Method
- TapCP: Canonical Polyadic (CP) Rank-R
- TapCUR: CUR / Leverage-Score Sampling
- TapExact: Exact / Full-Precision (No Approximation)
- TapPrune: Structured / Unstructured Pruning
- TapRandProj: Random Projection / Count-Sketch
- TapTT: Tensor-Train (TT) Truncation
- TapTruncSVD: Truncated SVD (Rank-K)
- TapTucker: Tucker / HOSVD compression
- TapWavelet: Wavelet / Multiresolution Compression

## TensorArrayEncoding — Tensor Array Encoding
- TaeCbor: CBOR
- TaeJson: JSON Numbers
- TaeMsgPack: Message Pack

## TensorAxisPurpose — Tensor Axis Purpose
- TapBatch: Batch / Sample
- TapChannel: Channel / Feature-map
- TapDateTime: Date and Time
- TapDepth: Spatial - Depth / Z
- TapDevice: Device
- TapFeature: Generic feature dimension
- TapHeight: Spatial - Height / Y
- TapMeasurement: Measurement / Metric
- TapParameter: Parameter
- TapTime: Temporal / Sequence step
- TapWidth: Spatial - Width  / X

## TensorAxisType — Tensor Axis Type
- TatDense: Dense Indexing (stride)
- TatRagged: Ragged / Jagged Blocks
- TatSparse: Sparse Index / Pointer

## TensorContentType — Tensor Content Type
- TCntArrowIpc: Arrow IPC Stream
- TCntCBOR: CBOR Encoded Dense Tensor
- TCntCustom: Custom
- TCntManifest: External Manifest / Metadata File
- TCntNpy: NumPy Binary (.npy)
- TCntSafTen: Safetensors Binary
- TCntZarr: Zarr Chunked Array

## TensorDataType — Tensor Data Type
- DtBFloat16: 16-bit Brain Floating Point
- DtBool: Boolean
- DtComplex128: 128-bit Complex
- DtComplex64: 64-bit Complex
- DtFloat16: 16-bit IEEE 754 Floating Point
- DtFloat32: 32-bit IEEE 754 Floating Point
- DtFloat64: 64-bit IEEE 754 Floating Point
- DtInt32: 32-bit Signed Integer
- DtInt64: 64-bit Signed Integer
- DtInt8: 8-bit Signed Integer
- DtUInt8: 8-bit Unsigned Integer

## TensorDecompMethod — Tensor Decomposition / Factorisation Method
- TdmCP: Canonical Polyadic (CP / PARAFAC)
- TdmHT: Hierarchical-Tucker
- TdmHosvd: Tucker / Higher-Order SVD (HOSVD)
- TdmTT: Tensor-Train (MPS)
- TdmTucker: Tucker (HOOI)

## TensorDevice — Tensor Device
- DevCpu: Host CPU
- DevCuda: NVIDIA CUDA Device
- DevMps: Apple Metal Performance Shaders
- DevRocm: AMD ROCm Device
- DevTpu: Tensor Processing Unit

## TensorElementType — Tensor Element Type
- TctDense: Dense Entry
- TctSparse: Sparse Non-zero Entry
- TctSymbolic: Symbolic Entry

## TensorMemoryFormat — Tensor memory Format / Layout - In-Memory Logical Index Order
- TmfChLast2: Channels-Last 2-D (NHWC)
- TmfChLast3: Channels-Last 3-D (NDHWC)
- TmfContig: Contiguous

## TensorPurpose — Tensor Purpose
- TpControlVector: Control Input Vector u(t)
- TpCovariance: Covariance / Correlation Matrix
- TpCovarianceMeasurement: Measurement Noise Covariance Matrix (R)
- TpCovarianceProcess: Process Noise Covariance Matrix (Q)
- TpFeedbackGain: State Feedback Gain Matrix (K)
- TpFeedforwardMatrix: Direct Transmission Feedforward Matrix (D)
- TpFuncSampling: Sampled Discrete Function
- TpGradient: Gradient Tensor
- TpHessian: Hessian Tensor
- TpImageRep: Image / Feature Map Data
- TpInertia: Mass/Inertia Tensor
- TpInputMatrix: Control Input Matrix (B)
- TpModelParams: Trainable Model Parameters
- TpObserverGain: Observer / Kalman Gain Matrix (L)
- TpOptimizerState: Optimizer State (momentum, variance)
- TpOriginal: Original Tensor
- TpOutputMatrix: Measurement Output Matrix (C)
- TpPhysicalState: Physical Simulation State
- TpStateMatrix: Dynamic State Transition Matrix (A)
- TpStateVector: State Vector x(t)
- TpStrain: Strain Tensor
- TpStress: Stress Tensor

## TensorQuantScheme — Tensor Quantisation Scheme
- TqsPerChannelAff: Per-Channel Affine (INT8)
- TqsPerTensorAff: Per-Tensor Affine (INT8)
- TqsPerTensorSym: Per-Tensor Symmetric

## TensorStorageType — Tensor Storage Type
- TstArrayField: Elements stored as an array field
- TstArrowIPC: Apache Arrow IPC Stream (parent: TstContent)
- TstBlobField: Elements stored as a BLOB field
- TstContent: Elements stored as an external content
- TstDLPack: DLPack Capsule (parent: TstContent)
- TstDenseChLast2D: Dense Channels-Last 2-D (NHWC) (parent: TstDenseContig)
- TstDenseChLast3D: Dense Channels-Last 3-D (NDHWC) (parent: TstDenseContig)
- TstDenseColMajor: Dense Column-Major (Fortran) (parent: TstArrayField)
- TstDenseContig: Dense Contiguous Buffer (torch.strided default) (parent: TstArrayField)
- TstDenseRowMajor: Dense Row-Major (C) (parent: TstArrayField)
- TstHDF5: HDF5 Dataset (parent: TstContent)
- TstMemMap: POSIX/Win Memory-Mapped File (parent: TstContent)
- TstN5: N5 (chunked, HDF5-like, used in bio-imaging) (parent: TstContent)
- TstNPY: NumPy .npy File (parent: TstContent)
- TstNetCDF4: netCDF-4 (HDF5-based scientific data) (parent: TstContent)
- TstParquetArrow: Apache Parquet (Arrow-columnar) (parent: TstContent)
- TstRowElement: Row-per-element
- TstSafeTensor: Safetensors Binary (Zero-Copy) (parent: TstContent)
- TstSparseBSC: Sparse BSC (Block-Sparse Column) (parent: TstArrayField)
- TstSparseBSR: Sparse BSR (Block-Sparse Row) (parent: TstArrayField)
- TstSparseCOO: Sparse COO (indices, value) (parent: TstArrayField)
- TstSparseCSC: Sparse CSC (Compressed Sparse Column) (parent: TstArrayField)
- TstSparseCSR: Sparse CSR / CSC (parent: TstArrayField)
- TstSparseNested: Sparse Nested (Hybrid COO-CSR) (parent: TstArrayField)
- TstTensorStoreSpec: TensorStore JSON / Kv Spec (parent: TstContent)
- TstTileDBDense: TileDB Dense Array (parent: TstContent)
- TstTileDBSparse: TileDB Sparse Array (parent: TstContent)
- TstTorchPT: PyTorch .pt / .pth serialized tensor file (parent: TstContent)
- TstZarr: Zarr Directory (Chunked, Compressed) (parent: TstContent)

## TensorType — Tensor Type
- TtDense: Dense Tensor
- TtDiagonal: Diagonal Tensor
- TtJagged: Jagged / Ragged Tensor
- TtSparse: Sparse Tensor
- TtSymmetric: Symmetric Tensor

## TermType — Term Type
- TtAgreementTermination: Agreement Termination
- TtCFR: Incoterm Cost and Freight (parent: TtInco)
- TtCIF: Incoterm Cost, Insurance and Freight (parent: TtInco)
- TtCIP: Incoterm Carriage and Insurance Paid to (parent: TtInco)
- TtCPT: Incoterm Carriage Paid To (parent: TtInco)
- TtClauseForRenewal: Clause For Renewal
- TtCommission: Commission
- TtCommissionFixed: Commission Term Fixed Per Unit (parent: TtCommission)
- TtCommissionMax: Commission Term Maximum Per Unit (parent: TtCommission)
- TtCommissionMin: Commission Term Minimum Per Unit (parent: TtCommission)
- TtCommissionVariable: Commission Term Variable (parent: TtCommission)
- TtDAF: Incoterm Delivered At Frontier (parent: TtInco)
- TtDAP: Incoterm Delivered at Place (parent: TtInco)
- TtDAT: Incoterm Delivered at Terminal (parent: TtInco)
- TtDDP: Incoterm Delivered Duty Paid (parent: TtInco)
- TtDDU: Incoterm Delivered Duty Unpaid (parent: TtInco)
- TtDEQ: Incoterm Delivered Ex Quay (parent: TtInco)
- TtDES: Incoterm Delivered Ex Ship (parent: TtInco)
- TtEXW: Incoterm Ex Works (parent: TtInco)
- TtExclusive: Exclusive Relationship
- TtFAS: Incoterm Free Alongside Ship (parent: TtInco)
- TtFCA: Incoterm Free Carrier (parent: TtInco)
- TtFOB: Incoterm Free On Board (parent: TtInco)
- TtFinCollection: Penalty For Collection Agency (parent: TtFinancial)
- TtFinLateFee: Late Fee (percent) (parent: TtFinancial)
- TtFinNotReturnable: Non-Returnable Sales Item (parent: TtFinancial)
- TtFinPaymentDayCurMonth: Payment (due on specified day of current month) (parent: TtFinancial)
- TtFinPaymentDayNextMonth: Payment (due on specified day of next month) (parent: TtFinancial)
- TtFinPaymentDays: Payment (net days) (parent: TtFinancial)
- TtFinPaymentDaysPt1: Payment net days, part 1 (parent: TtFinPaymentDays)
- TtFinPaymentDaysPt2: Payment net days, part 2 (parent: TtFinPaymentDays)
- TtFinPaymentDaysPt3: Payment net days, part 3 (parent: TtFinPaymentDays)
- TtFinPaymentDisc: Payment (discounted if paid within specified days) (parent: TtFinancial)
- TtFinancial: Financial
- TtFreight: Preferred Freight
- TtIncentive: Incentive
- TtInco: Incoterm
- TtIndemnification: Indemnification
- TtLegal: Legal
- TtNonCompete: Non-Compete
- TtOther: Other
- TtPurchasing: Purchasing
- TtThreshold: Threshold

## TerminationType — Termination Type
- TtFired: Fired
- TtLayoff: Layoff
- TtResigned: Resigned
- TtRetired: Retired

## ThermodynamicDimension — Thermodynamic Dimension
- DimEnthalpy: Enthalpy Dimension
- DimEntropy: Entropy Dimension
- DimMass: Mass
- DimPressure: Pressure Dimension
- DimRelativeHumidity: Relative Humidity Dimension
- DimTemperature: Temperature Dimension
- DimVolume: Volume Dimension

## TimeDimension — Time Dimension
- DimTime: Time Dimension

## TimePeriodPurpose — Time Period Purpose
- Fiscal: Fiscal
- Payroll: Payroll
- Sales: Sales
- Tax: Tax

## TrackingCodeSource — Tracking Code Source
- TKCDSRC_COOKIE: Cookie
- TKCDSRC_URL_PARAM: URL Parameter

## TrackingCodeType — Tracking Code Type
- ACCESS: Access Code
- EXTERNAL: External
- INTERNAL: Internal
- PARTNER_MGD: Partner Managed

## TrajectoryActuationType — Trajectory Actuation Type
- PtaDirect: Direct - Movement is initiated by the component
- PtaIndirect: Indirect - Motion derived from a parent component or external force
- PtaNone: None - No actuation of this axis
- PtaVirtual: Virtual - Motion is computed and used for expressing an imaginary or derived movement

## TrajectoryActuatorType — Trajectory Actuator Type
- PtactContinuous: Continuous - Revolves around an axis with a continuous range of motion (unlimited motion)
- PtactFixed: Fixed - Axis does not move
- PtactPrismatic: Prismatic - Linear sliding motion along an axis within a fixed range
- PtactRevolute: Revolute - Rotates around an axis within a fixed range of motion

## TrajectoryControlMethod — Trajectory Control Method
- PtcmAdaptive: Adaptive Control
- PtcmBangBang: Bang-Bang Control
- PtcmFuzzyLogic: Fuzzy Logic Control
- PtcmHInfinity: H-infinity Control
- PtcmLQI: Linear Quadratic Integrator (LQI)
- PtcmLQR: Linear Quadratic Regulator (LQR)
- PtcmMPC: Model Predictive Control (MPC)
- PtcmNNControl: Neural Network Control
- PtcmPD: PD Algorithm
- PtcmPI: PI Algorithm
- PtcmPID: PID Algorithm
- PtcmRLControl: Reinforcement Learning Control
- PtcmSMC: Sliding Mode Control (SMC)

## TrajectoryPointRunErrorCause — Trajectory Point Run Error Cause
- TprecEnvironmental: Environmental Interference
- TprecMechanicalJam: Mechanical Jam
- TprecSensorFault: Sensor Fault
- TprecSoftwareGlitch: Software Glitch

## TrajectoryPointRunExecutionStatus — Trajectory Point Run Execution Status
- TpresDeviation: Deviation
- TpresFailure: Failure
- TpresSkipped: Skipped
- TpresSuccess: Success

## TrajectoryStatsType — Trajectory Statistics Type
- PtstDynamicAnalysis: Dynamic Analysis 
- PtstThermodynamicAnalysis: Thermodynamic Analysis
- PtstVibrationAnalysis: Vibration Analysis

## TransformationOperandType — Transformation Operand Type
- TotBias: Bias / Translation Vector (affine map)
- TotBiasMatrix: Bias term - Matrix (parent: TotBias)
- TotBiasTensor: Bias term - Tensor (parent: TotBias)
- TotBiasVector: Bias term - Vector (parent: TotBias)
- TotEnum: Enumeration / Enumeration Group Operand
- TotEnumValue: Enumeration value operand (configuration, mode, etc.) (parent: TotEnum)
- TotKernel: Convolution / Correlation Kernel / Filter / Bias
- TotKernelMatrix: Kernel / filter - Matrix (parent: TotKernel)
- TotKernelTensor: Kernel / filter – Tensor (parent: TotKernel)
- TotKernelVector: Kernel / filter - Vector (parent: TotKernel)
- TotKeyBias: Attention key projection bias (parent: TotBias)
- TotKeyKernel: Attention key projection weight (parent: TotKernel)
- TotKeyTensor: Attention key tensor (parent: TotTensor)
- TotLeft: Left / First Operand
- TotLeftMatrix: Left / first operand - Matrix (parent: TotLeft)
- TotLeftTensor: Left / first operand – Tensor (parent: TotLeft)
- TotLeftVector: Left / first operand - Vector (parent: TotLeft)
- TotMaskTensor: Additive attention mask tensor (parent: TotTensor)
- TotMatrix: Generic matrix operand (type marker)
- TotNth: Nth Operand
- TotOutputBias: Attention output projection bias (parent: TotBias)
- TotOutputKernel: Attention output projection weight (parent: TotKernel)
- TotParameter: Scalar, Symbolic or Typed Parameter Operand
- TotQueryBias: Attention query projection bias (parent: TotBias)
- TotQueryKernel: Attention query projection weight (parent: TotKernel)
- TotQueryTensor: Attention query tensor (parent: TotTensor)
- TotRight: Right / Second Operand
- TotRightMatrix: Right / second operand - Matrix (parent: TotRight)
- TotRightTensor: Right / second operand – Tensor (parent: TotRight)
- TotRightVector: Right / second operand - Vector (parent: TotRight)
- TotScalar: Scalar / hyper-parameter operand
- TotSingle: Single operand
- TotTensor: Generic tensor operand (type marker)
- TotTransformation: Nested Transformation Operand
- TotValueBias: Attention value projection bias (parent: TotBias)
- TotValueKernel: Attention value projection weight (parent: TotKernel)
- TotValueTensor: Attention value tensor (parent: TotTensor)
- TotVector: Generic vector operand (type marker)

## TransformationPurpose — Transformation Purpose
- TpConstraint: Constraint
- TpCoordTransform: Coordinate System Transformation
- TpDataCompression: Data Compression
- TpEigenAnalysis: Spectral Analysis or Stability
- TpEquation: Equation
- TpFrameChange: Frame Change
- TpGeometricModeling: Geometrical Transformation (shearing, rotation, reflection, scaling, etc.)
- TpPredicate: Predicate
- TpSymbolicSimplification: Symbolic or Algebraic Simplification
- TpTypeJudgement: Type Judgement

## TransformationType — Transformation Type (Algebraic / Numerical)
- TtAdaptiveAvgPool2d: 2D Adaptive Average Pooling (parent: TtUnaryLin)
- TtAffine: Affine Map (y = A·x + b) (parent: TtBinaryNonLin)
- TtAnd: Logical Conjunction (parent: TtLogical)
- TtAttentionMask: Attention Additive Mask (parent: TtBinaryLin)
- TtAvgPool2d: 2D Spatial Average Pooling (parent: TtUnaryLin)
- TtBatchNorm: Batch Normalization (parent: TtUnaryNonLin)
- TtBinaryLin: Binary linear transformation (parent: TtLinear)
- TtBinaryNonLin: Binary non-linear transformation (parent: TtNonLinear)
- TtBlockMatrixExtr: Block Matrix Extraction (submatrix) from a Matrix
- TtCanny: Canny Edge Detector (parent: TtUnaryNonLin)
- TtCholeskyDecomp: Cholesky Decomposition (parent: TtMatrixDecomp)
- TtComposition: Composition of Transformations (parent: TtMeta)
- TtConv1d: 1D Temporal Convolution (parent: TtUnaryLin)
- TtConv2d: 2D Spatial Convolution (parent: TtUnaryLin)
- TtDecomp: Decomposition / Factorisation (parent: TtMeta)
- TtDiagBlockMatrixExtr: Diagonal Blocking Extraction. The matrix is divided into blocks along the diagonal, with each block being a square or rectangular submatrix. Off-diagonal blocks are typically zero. (parent: TtBlockMatrixExtr)
- TtDiagExtract: Diagonal / Band Extraction (parent: TtUnaryLin)
- TtDiagonalise: Diagonalisation (A = PDP⁻¹) (parent: TtEigenvalueDecomp)
- TtDomainBlockMatrixExtr: Domain-Specific Blocking Extraction. The blocking pattern is chosen based on the application domain, such as signal processing, image processing, or finite element methods. (parent: TtBlockMatrixExtr)
- TtDropout: Dropout Regularization (parent: TtUnaryNonLin)
- TtEigenvalueDecomp: Eigenvalue Decomposition (parent: TtMatrixDecomp)
- TtEigh: Eigh Decomposition. (parent: TtMatrixDecomp)
- TtEmbedding: Embedding Lookup Table (parent: TtUnaryLin)
- TtEquality: Equality Relation (parent: TtRelation)
- TtFalse: Logical False (parent: TtLogical)
- TtFilter2D: 2D Spatial Convolution Filter (parent: TtUnaryLin)
- TtFunctionCompose: Composition of Approximated Functions (f ∘ g) (parent: TtUnaryLin)
- TtGaussianBlur: Gaussian Blur Filter (parent: TtUnaryLin)
- TtGradient: Gradient ∇f(x) (parent: TtMeta)
- TtGreaterEqual: Greater Than or Equal Relation (parent: TtInequality)
- TtGreaterThan: Greater Than Relation (parent: TtInequality)
- TtGroupNorm: Group Normalization (parent: TtUnaryNonLin)
- TtHessenbergDecomp: Hessenberg Decomposition (parent: TtMatrixDecomp)
- TtHessian: Hessian ∇²f(x) (parent: TtMeta)
- TtHierBlockMatrixExtr: Hierarchical or Recursive Blocking. The matrix is split into vertical strips (blocks). A matrix is recursively divided into smaller blocks within blocks, creating a hierarchical structure. (parent: TtBlockMatrixExtr)
- TtHorizBlockMatrixExtr: Horizontal Blocking Extraction. The matrix is split into horizontal strips (blocks). Each block contains a set of rows. (parent: TtBlockMatrixExtr)
- TtHouseholderProd: Householder Product (parent: TtNaryLin)
- TtImplies: Logical Implication (parent: TtLogical)
- TtInequality: Inequality Relation (parent: TtRelation)
- TtIrregBlockMatrixExtr: Irregular Blocking Extraction. The matrix is divided into blocks that may have different sizes, depending on specific criteria, such as data distribution or computational efficiency. (parent: TtBlockMatrixExtr)
- TtJacobian: Jacobian J_f(x) (parent: TtMeta)
- TtJitCompile: Just-in-time Compilation (XLA, Inductor, ecc.) (parent: TtMeta)
- TtJordanDecomp: Jordan Decomposition (parent: TtMatrixDecomp)
- TtLDLDecomp: LDLᵗ Decomposition (parent: TtMatrixDecomp)
- TtLayerNorm: Layer Normalization (parent: TtUnaryNonLin)
- TtLessEqual: Less Than or Equal Relation (parent: TtInequality)
- TtLessThan: Less Than Relation (parent: TtInequality)
- TtLinear: Linear Transformation
- TtLinearMap: Linear Map (y = A·x) (parent: TtBinaryLin)
- TtLogical: Logical Transformation
- TtLossBceWithLogits: Binary Cross Entropy with Logits (parent: TtBinaryNonLin)
- TtLossCrossEntropy: Cross Entropy Classification Loss (parent: TtBinaryNonLin)
- TtLossL1: L1 / Mean Absolute Error Loss (parent: TtBinaryNonLin)
- TtLossMse: Mean Squared Error Loss (MSE) (parent: TtBinaryNonLin)
- TtLuDecomp: LU Decomposition (parent: TtMatrixDecomp)
- TtLuFactorDecomp: LU Factor Decomposition (parent: TtMatrixDecomp)
- TtMatrixAdjoint: Matrix Conjugate Transpose / Adjoint (parent: TtUnaryLin)
- TtMatrixAntiDiagonal: Matrix AntiDiagonal (parent: TtUnaryLin)
- TtMatrixApply: Matrix Application to a Vector / Matrix (parent: TtBinaryLin)
- TtMatrixBandExtract: Matrix Band Extract (parent: TtUnaryLin)
- TtMatrixDecomp: Matrix Decomposition / Factorisation (parent: TtDecomp)
- TtMatrixDiagonal: Matrix Diagonal (parent: TtUnaryLin)
- TtMatrixExp: Matrix Exponential (eᴬ) (parent: TtUnaryNonLin)
- TtMatrixFlipLeftRight: Matrix Flip Left Right (parent: TtUnaryLin)
- TtMatrixFlipUpDown: Matrix Flip Up Down (parent: TtUnaryLin)
- TtMatrixInverse: Matrix Inversion (parent: TtUnaryNonLin)
- TtMatrixLowerTriang: Matrix Lower-Triangular Extract (parent: TtUnaryLin)
- TtMatrixPower: Matrix Integer Power (Aⁿ) (parent: TtUnaryNonLin)
- TtMatrixProduct: Matrix Product (parent: TtBinaryLin)
- TtMatrixPseudoInverse: Pseudo Inverse Matrix (parent: TtUnaryNonLin)
- TtMatrixReciprocal: Matrix Reciprocal (parent: TtUnaryNonLin)
- TtMatrixRotate90: Matrix Rotate 90° (parent: TtUnaryLin)
- TtMatrixTrace: Matrix Trace (parent: TtUnaryLin)
- TtMatrixTranspose: Matrix Transpose (parent: TtUnaryLin)
- TtMatrixUpperTriang: Matrix Upper-Triangular Extract (parent: TtUnaryLin)
- TtMatrixVectorize: Matrix Vectorize (parent: TtUnaryLin)
- TtMaxPool2d: 2D Spatial Max Pooling (parent: TtUnaryNonLin)
- TtMaximize: Maximization: max f(x) (parent: TtOptimize)
- TtMembership: Set or Type Membership Relation (parent: TtRelation)
- TtMeta: Meta-Transformation (composition, decomposition, compilation, etc.)
- TtMinimize: Minimization: min f(x) (parent: TtOptimize)
- TtMultiDot: Multi-Matrix Dot (parent: TtNaryLin)
- TtMultiHeadAttention: Multi-Head Attention (parent: TtNaryNonLin)
- TtNaryLin: N-ary Transformation (parent: TtLinear)
- TtNaryNonLin: N-ary non-linear transformation (parent: TtNonLinear)
- TtNonLinear: Non-linear Transformation
- TtNorm: Vector or Matrix Norm, Frobenius, Nuclear, etc. (parent: TtUnaryNonLin)
- TtNot: Logical Negation (parent: TtLogical)
- TtNotEqual: Not Equal Relation (parent: TtInequality)
- TtOptimize: Mathematical Optimization (parent: TtMeta)
- TtOptimizerAdam: Adam Optimizer (parent: TtMeta)
- TtOptimizerAdamW: AdamW Optimizer (parent: TtMeta)
- TtOptimizerSgd: Stochastic Gradient Descent Optimizer (parent: TtMeta)
- TtOr: Logical Disjunction (parent: TtLogical)
- TtPolarDecomp: Polar Decomposition (parent: TtMatrixDecomp)
- TtPositionalEncoding: Positional Encoding (parent: TtUnaryNonLin)
- TtQrDecomp: QR Decomposition (parent: TtMatrixDecomp)
- TtRMSNorm: Root Mean Square Layer Normalization (parent: TtUnaryNonLin)
- TtRegularBlockMatrixExtr: Grid or Regular Blocking Extraction. The matrix is partitioned into blocks by both rows and columns. (parent: TtBlockMatrixExtr)
- TtRelation: Relational Transformation or Predicate
- TtRotaryEmbedding: Rotary Position Embedding (parent: TtUnaryNonLin)
- TtScaledDotProductAttention: Scaled Dot-Product Attention (parent: TtNaryNonLin)
- TtSchurDecomp: Schur Decomposition (parent: TtMatrixDecomp)
- TtSetCombination: Set Combination (parent: TtUnaryLin)
- TtSetPermutation: Set Permutation (parent: TtUnaryLin)
- TtSobel: Sobel Spatial Gradient (parent: TtUnaryLin)
- TtSvd: Singular Value Decomposition (SVD) on a Matrix (parent: TtMatrixDecomp)
- TtSvdEconomy: Economy Singular Value Decomposition (SVD). It removes redundant zero rows or columns from U and Sigma matrices. (parent: TtSvd)
- TtSvdTruncated: Truncated Singular Value Decomposition (SVD). It is used primarily in data compression, information retrieval. (parent: TtSvd)
- TtSymBlockMatrixExtr: Symmetric Blocking Extraction. Blocks are extracted in such a way that if the original matrix is symmetric, the block structure also respects this symmetry. (parent: TtBlockMatrixExtr)
- TtSymmetricEigenDecomp: Symmetric Eigenvalue Decomposition (parent: TtMatrixDecomp)
- TtTensorAdd: Tensor Element-wise Addition (parent: TtBinaryLin)
- TtTensorConcat: Tensor Concatenation (parent: TtNaryLin)
- TtTensorContract: Tensor Contraction (Einsum) (parent: TtBinaryLin)
- TtTensorDecomp: Tensor Decomposition / Factorisation (parent: TtDecomp)
- TtTensorDiv: Tensor Element-wise Division (parent: TtBinaryNonLin)
- TtTensorElu: Exponential Linear Unit (ELU) (parent: TtUnaryNonLin)
- TtTensorExp: Element-wise exponential: Yᵢ = eˣᵢ (parent: TtUnaryNonLin)
- TtTensorFlip: Reverse tensor along given axis/axes (parent: TtUnaryLin)
- TtTensorFlipLeftRight: Flip left/right (reverse axis 1) (parent: TtTensorFlip)
- TtTensorFlipUpDown: Flip up/down (reverse axis 0) (parent: TtTensorFlip)
- TtTensorGelu: Gaussian Error Linear Unit (GELU) (parent: TtUnaryNonLin)
- TtTensorInv: Tensor Inverse (parent: TtUnaryNonLin)
- TtTensorLeakyReLu: Leaky ReLU: max(αx, x) (parent: TtUnaryNonLin)
- TtTensorLog: Element-wise natural log: Yᵢ = ln xᵢ (parent: TtUnaryNonLin)
- TtTensorLogSoftmax: Log-Softmax Normalization (parent: TtUnaryNonLin)
- TtTensorMax: Tensor Max Reduction (parent: TtUnaryNonLin)
- TtTensorMean: Tensor Mean Reduction (parent: TtUnaryLin)
- TtTensorMin: Tensor Min Reduction (parent: TtUnaryNonLin)
- TtTensorMul: Tensor Element-wise Multiplication (parent: TtBinaryLin)
- TtTensorNeg: Element-wise Negation (parent: TtUnaryLin)
- TtTensorOuter: Outer / Kronecker Product (parent: TtBinaryLin)
- TtTensorPermute: Tensor Axis Permute / Transpose (parent: TtUnaryLin)
- TtTensorPow: Tensor Element-wise Power (parent: TtBinaryNonLin)
- TtTensorReLu: ReLU: Yᵢ = max(0, xᵢ) (parent: TtUnaryNonLin)
- TtTensorReciprocal: Tensor Reciprocal (parent: TtUnaryNonLin)
- TtTensorReshape: Tensor Reshape (parent: TtUnaryLin)
- TtTensorRotate90: Rotate 90° k times around the last two axes (parent: TtUnaryLin)
- TtTensorSigmoid: Sigmoid: Yᵢ = 1 / (1 + e⁻ˣᵢ) (parent: TtUnaryNonLin)
- TtTensorSilu: Sigmoid Linear Unit / Swish (SiLU) (parent: TtUnaryNonLin)
- TtTensorSoftmax: Softmax Normalization (parent: TtUnaryNonLin)
- TtTensorSolve: Tensor Solve (parent: TtBinaryNonLin)
- TtTensorSplit: Tensor Split (parent: TtUnaryLin)
- TtTensorSqrt: Element-wise square-root: Yᵢ = √xᵢ (parent: TtUnaryNonLin)
- TtTensorSqueeze: Tensor Squeeze (parent: TtUnaryLin)
- TtTensorSub: Tensor Element-wise Subtraction (parent: TtBinaryLin)
- TtTensorSum: Tensor Sum Reduction (parent: TtUnaryLin)
- TtTensorTanh: Hyperbolic Tangent: tanh(x) (parent: TtUnaryNonLin)
- TtTensorUnfold: Tensor Matricization / Unfold (parent: TtUnaryLin)
- TtTensorUnsqueeze: Tensor Unsqueeze (parent: TtUnaryLin)
- TtTensorVectorize: Tensor Vectorize (parent: TtUnaryLin)
- TtTrue: Logical True (parent: TtLogical)
- TtUnaryLin: Unary linear transformation (parent: TtLinear)
- TtUnaryNonLin: Unary non-linear transformation (parent: TtNonLinear)
- TtVectorCross: 3-D Cross Product (a x b) (parent: TtBinaryLin)
- TtVectorDot: Vector Dot Product (parent: TtBinaryLin)
- TtVertBlockMatrixExtr: Vertical Blocking Extraction. The matrix is split into vertical strips (blocks). Each block contains a set of columns. (parent: TtBlockMatrixExtr)
- TtVmap: Vectorised Map (parent: TtMeta)
- TtWarpAffine: Affine Geometric Transformation (parent: TtAffine)
- TtWarpPerspective: Perspective Homography Transformation (parent: TtUnaryLin)
- TtXor: Logical Exclusive Or (parent: TtLogical)

## TriangularExtractionType — Triangular Extraction Type
- TetLower: Lower Triangular
- TetUpper: Upper Triangular

## UniversalConstructionType — Universal Construction Type
- UcCoequalizer: Coequalizer
- UcColimit: Colimit
- UcCoproduct: Coproduct
- UcEqualizer: Equalizer
- UcInitial: Initial object
- UcLimit: Limit
- UcProduct: Product
- UcPullback: Pullback
- UcPushout: Pushout
- UcTerminal: Terminal object

## UomDimTypeGroup — UOM Dimension Type Group
- UdtgOrg: Organization (parent: UdtgParty)
- UdtgParty: Party
- UdtgPerson: Person (parent: UdtgParty)
- UdtgProduct: Product

## UomType — UOM Type
- UT_AREA_MEASURE: Area
- UT_CURRENCY_MEASURE: Currency
- UT_DATASPD_MEASURE: Data Speed
- UT_DATA_MEASURE: Data Size
- UT_DENSITY_MEAS: Density
- UT_ENERGY_MEASURE: Energy
- UT_LENGTH_MEASURE: Length
- UT_OTHER_MEASURE: Other
- UT_POWER_MEASURE: Power
- UT_PRESSURE_MEASURE: Pressure
- UT_TEMP_MEASURE: Temperature
- UT_TIME_FREQ_MEASURE: Time/Frequency
- UT_VELOCITY_MEASURE: Velocity
- UT_VOLUME_DRY_MEAS: Dry Volume
- UT_VOLUME_LIQ_MEAS: Liquid Volume
- UT_WEIGHT_MEASURE: Weight

## UserAuthcFactorType — User Authentication Factor Type
- UafEmail: Email Code
- UafSingleUse: Single Use Code
- UafSms: SMS Code
- UafTotp: Authenticator App (TOTP)

## UserGroupType — User Group Type
- UgtMarbleErp: Marble ERP App
- UgtMoquiAdmin: Moqui Administrators
- UgtMyAccount: My Account App
- UgtPopcAdmin: POPC ERP App
- UgtRemoteSystems: Remote Systems

## UserPreferenceKey — User Preference Key (optional)
- AllStoresMarkupLabelOrder: All Product Stores Markup Order Shipping (set to 'true')
- AllStoresMarkupLabelShipment: All Product Stores Markup Shipment Labels (set to 'true')
- CurrencyDefault: Currency Default
- DefaultShipmentGatewayConfigId: Shipment Default Gateway Config ID
- FacilityActive: Facility Active ID (for individual user)
- FacilityGeneralDefault: Facility General Default ID
- GlAccountCodeMask: GL Account Code Mask (like ###-###)
- OrderSalesStoreDefault: Order (Sales) Default Store ID
- PostalAddress.DefaultCountry: Country to use as default in forms for postal addresses
- TelecomNumber.DefaultCountryCode: Country Code to use as default in forms for phone numbers
- ValidateAddressGatewayConfigId: Address Validate Gateway Config ID
- mantle.content.large.root: Mantle Content Large Root Loc - binary, etc files
- mantle.content.root: Mantle Content Root Loc
- qz.print.enabled: QZ Print Enabled (true/false)
- qz.printer.label.active: QZ Active Label Printer Name
- qz.printer.main.active: QZ Active Main Printer Name

## VariableDomain — Variable Domain
- VdBinary: Binary
- VdContinuous: Continuous
- VdInteger: Integer
- VdSemiContinuous: Semi-Continuous

## VectorComponentType — Vector Component Type
- VctCanonical: Canonical (Basis-Free) Component
- VctInCoordinateSystem: Component in Coordinate System
- VctSymbolic: Symbolic Vector Component

## VectorPurpose — Vector Purpose
- VpAcceleration: Acceleration Vector
- VpAxial: Axial Vector
- VpBase: Base Vector
- VpBasis: Basis Vector
- VpColumn: Column Vector
- VpCotangent: Cotangent Vector
- VpDisplacement: Displacement Vector
- VpEigenvector: Eigenvector
- VpForce: Force Vector
- VpGradient: Gradient Vector
- VpKnot: Knot Vector
- VpNonOrthogonalBasis: Non-Orthogonal Basis Vector
- VpNormal: Normal Vector
- VpObliqueBasis: Oblique Basis Vector
- VpOrthonormalBasis: Orthonormal Basis Vector
- VpPolar: Polar Vector
- VpPosition: Position Vector
- VpRandom: Random Vector
- VpRow: Row Vector
- VpTangent: Tangent Vector
- VpVectorOfVectors: Vector of Vectors
- VpVelocity: Velocity Vector

## VectorType — Vector Type
- VtOrdinary: Ordinary Vector
- VtStandardBasisVector: Standard Basis Vector
- VtUnit: Unit Vector
- VtVersor: Versor
- VtZero: Zero Vector

## WorkEffortAssocType — Work Effort Association Type
- WeatBasedOn: Based On (parent: WeatRelatesTo)
- WeatCausedBy: Caused By (parent: WeatRelatesTo)
- WeatClone: Clones (parent: WeatRelatesTo)
- WeatComponent: Component
- WeatDependsOn: Depends On (Blocked By) (parent: WeatRelatesTo)
- WeatDuplicates: Duplicates (parent: WeatRelatesTo)
- WeatIndependentOf: Independent Of (Concurrent) (parent: WeatRelatesTo)
- WeatMilestone: Milestone
- WeatRelatesTo: Relates To
- WeatRelease: Release
- WeatRoutingComp: Routing Component

## WorkEffortContentType — Work Effort Content Type
- WectCreatedMedia: Created Media
- WectDesign: Design
- WectDiscussion: Discussion
- WectProjectUpdate: Project Update
- WectProposal: Proposal
- WectRequirement: Requirement
- WectSupportingMedia: Supporting Media

## WorkEffortFacilityType — Work Effort Facility Type
- WeftOrigin: Inventory Origin
- WeftUsed: Also Used

## WorkEffortPartyAvailability — Work Effort Party Availability
- WeptaAvailable: Available
- WeptaAway: Away
- WeptaBusy: Busy

## WorkEffortPartyDelegateReason — Work Effort Party Delegate Reason
- WepdrCompleted: Completely Finished
- WepdrNeedSupport: Need Support or Help
- WepdrPartFinished: My Part Finished

## WorkEffortPartyExpectation — Work Effort Party Expectation
- WepeFyi: For Your Information
- WepeImmediate: Immediate Response Requested
- WepeInvRequested: Involvement Requested
- WepeInvRequired: Involvement Required

## WorkEffortProductType — Work Effort Product Type
- WeptConsume: Consume
- WeptProduce: Produce
- WeptRouting: Routing
- WeptSales: Sales

## WorkEffortPurpose — Work Effort Purpose
- WepAssembling: Assembling (parent: WepManufacturing)
- WepAssetUsage: Asset Usage (Rental)
- WepBusinessTravel: Business Travel
- WepCommunication: Communication (parent: WetTask)
- WepDeployment: Deployment
- WepDevelopment: Development
- WepDocument: Document (parent: WetTask)
- WepEmail: Email
- WepFeatureEnhance: Feature Enhancement (parent: WetTask)
- WepFeatureTest: Feature Test (parent: WetTask)
- WepFix: Bug Fix (parent: WetTask)
- WepHoliday: Holiday
- WepMaintenance: Maintenance
- WepManufacturing: Manufacturing
- WepMeeting: Meeting
- WepNewFeature: New Feature (parent: WetTask)
- WepPhoneCall: Phone Call
- WepPickAssembly: Pick Assembly (parent: WepManufacturing)
- WepPlaceholder: Placeholder (parent: WetTask)
- WepPrItSecurity: IT Security (parent: WetProject)
- WepPrMarketing: Marketing (parent: WetProject)
- WepPrOrgMgmt: Organization Management (parent: WetProject)
- WepPrProdDev: Product Development (parent: WetProject)
- WepPrProdFulfill: Product Fulfillment (parent: WetProject)
- WepPrTraining: Training (parent: WetProject)
- WepProductionRun: Production Run (parent: WepManufacturing)
- WepResearch: Research
- WepRouting: Routing (parent: WepManufacturing)
- WepRoutingTask: Routing Task (parent: WepManufacturing)
- WepShipmentReceive: Shipment Receive
- WepShipmentShip: Shipment Pick/Load/Ship
- WepSubcontracting: Sub-contracting
- WepSupport: Support
- WepTask: Task (parent: WetTask)
- WepTimesheet: Timesheet
- WepToDo: To Do (parent: WetTask)
- WepTraining: Training

## WorkEffortResolution — Work Effort Resolution
- WerCannotReproduce: Cannot Reproduce
- WerCompleted: Completed
- WerDuplicate: Duplicate
- WerIncomplete: Incomplete
- WerInsufficient: Insufficient Information
- WerUnresolved: Unresolved
- WerWontComplete: Won't Complete

## WorkEffortType — Work Effort Type
- WetAvailable: Available
- WetComponent: Component
- WetEvent: Event
- WetMilestone: Milestone
- WetProject: Project
- WetRelease: Release
- WetTask: Task
- WetTimeOff: Time Off

## WorkEffortVisibility — Work Effort Visibility
- WevAllUsers: All Users
- WevConfidential: Top Secret (confidential access)
- WevGeneral: General (public access)
- WevRestricted: Restricted (private access)
- WevWorkGroup: Work Group (group only access)

## WorkRequirementFulfillmentType — Work Requirement Fulfillment Type
- WrfDelivers: Delivers
- WrfDeploys: Deploys
- WrfFixes: Fixes
- WrfImplements: Implements
- WrfTests: Tests

## WorkType — Work Type
- WktpGeneralLabor: General Labor
- WktpGeneralOffice: General Office
- WktpManagement: Management
- WktpPaidBreak: Paid Break
- WktpPaidNpt: Paid Non-productive Time
- WktpProgramming: Programming
- WktpRequirements: Requirements Gathering
- WktpSystemDesign: System Design
- WktpTesting: Testing

## _NA_ — Not Applicable
- _NA_: Not Applicable

