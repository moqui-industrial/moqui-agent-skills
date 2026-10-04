# Item types and their GL accounts (generated)

`itemTypeEnumId` (Enumeration type `ItemType`) is a field of: BudgetItem, DeviceRequestItem, EmploymentPayDetail, InvoiceItem, ItemTypeGlAccount, OrderItem, PayrollAdjustment, ReturnItem, WorkTypeGlOverride.

The GL mapping comes from `ItemTypeGlAccount` rows in install data (mostly ZaaGlAccountsInstallData.xml, for the template organization DefaultSettings, copied to a real organization by mantle.ledger.LedgerServices.init#PartyAccountingConfiguration). Direction: O = outgoing/sales, I = incoming/purchase, E = either.

When an invoice item is posted, the account is looked up by product first (product category, product, asset type) for product item types, then by the exact itemTypeEnumId in ItemTypeGlAccount: the parent enum is NOT used as a fallback, so every item type that is invoiced needs its own mapping.

Groups (EnumGroupMember) say where a type may be used: EngItemsSales = outgoing/receivable/sales lines, EngItemsPurchase = incoming/payable/purchase lines, EngItemsAdjust = invoice adjustments, EngItemsProduct = product lines.

| Item type | Description | Parent | Groups | GL mapping |
| --- | --- | --- | --- | --- |
| ItemAddtlFeature | Additional Feature | ItemSales | Sales | O:419000000 Miscellaneous Sales |
| ItemAdjAdvertising | Advertising | ItemInvAdjust | Adjust, Purchase, Sales | E:621000000 Advertising |
| ItemAdjJointAdv | Joint Advertising | ItemInvAdjust | Adjust, Purchase, Sales | E:624000000 Joint Advertising |
| ItemAdvancePay | Advance Pay | ItemPayrollIncome |  | I:151400000 Prepaid Wages; O:260000000 Unearned Revenue |
| ItemAsset | Asset - Fixed Asset |  | Product, Purchase | I:139000000 Fixed Assets Unreceived; O:814100000 Gain on Sale of Fixed Assets |
| ItemBonusDisc | Bonus (Discretionary) | ItemPayrollIncome |  | I:631900000 Bonus |
| ItemBonusNonDisc | Bonus (Non-Discretionary) | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemBreakHourlyEarnings | Break Hourly Earnings | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemBreakRrpEarnings | Break RRP Earnings | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemChargebackAdjust | Chargeback | ItemInvAdjust | Adjust, Sales | E:522100000 Coupons and Credits |
| ItemCommission | Commission Line Item |  | Purchase | E:631700000 Sales Commissions - Non-Employee |
| ItemCommissionAdj | Commission Adjustment |  | Purchase | E:631800000 Sales Commission Adjustments |
| ItemComplianceFee | Compliance Fee | ItemInvAdjust | Adjust, Sales | — |
| ItemCouponCredit | Coupons and Credits | ItemInvAdjust | Adjust, Sales | E:522100000 Coupons and Credits |
| ItemDed125Compy | 125*Compy. Contr Other Premium | ItemPayrollDeduct |  | E:222800000 Employee Benefits Withholding |
| ItemDed125Hsa | 125*HSA Contribution (pre tax) | ItemPayrollDeduct | EngSec125Empe | E:222800000 Employee Benefits Withholding |
| ItemDed125Ppo | 125*PPO (pre tax) | ItemPayrollDeduct | EngSec125Empe | E:222800000 Employee Benefits Withholding |
| ItemDed401kEmpe | Traditional 401K Employee | ItemPayrollDeduct | Eng401kEmpe | E:222600000 401k - Pension Withholding |
| ItemDedAdvRepay | Advance Repayment | ItemPayrollDeduct |  | E:151400000 Prepaid Wages |
| ItemDedCharity | Charity Donation | ItemPayrollDeduct |  | E:254000000 Donations Collected |
| ItemDedChildGarnish | Child Support Garnishment | ItemPayrollDeduct |  | E:222700000 Garnishment Withholding |
| ItemDedMHealthInsurance | Health Insurance | ItemPayrollDeduct |  | — |
| ItemDedMisc | Miscellaneous Deduction | ItemPayrollDeduct |  | E: |
| ItemDedRoth401kEmpe | Roth 401k Employee | ItemPayrollDeduct | Eng401kEmpe | E:222600000 401k - Pension Withholding |
| ItemDedRothIraEmpe | Roth IRA Employee | ItemPayrollDeduct |  | E:222600000 401k - Pension Withholding |
| ItemDedSimpleIraEmpe | Simple IRA Employee | ItemPayrollDeduct |  | E:222600000 401k - Pension Withholding |
| ItemDedUnion | Union Dues | ItemPayrollDeduct |  | E: |
| ItemDedUnpaidTimeOff | Unpaid Salary Time Off | ItemPayrollDeduct |  | E: |
| ItemDedWageGarnish | Wage Garnishment | ItemPayrollDeduct |  | E:222700000 Garnishment Withholding |
| ItemDiscount | Discount - Promotional |  | Adjust, Purchase, Sales | O:522200000 Promotional Discounts; I:865000000 Other Purchase Discounts |
| ItemDiscountAppease | Discount - Appeasement |  | Adjust, Sales | O:522300000 Appeasement Discounts; I:865000000 Other Purchase Discounts |
| ItemDonation | Donation | ItemSales | Sales | E:254000000 Donations Collected |
| ItemDoubleTimePremium | Double Time Premium | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemExpAdvertising | Advertising | ItemExpense | Purchase | E:621000000 Advertising |
| ItemExpCharitable | Charitable Contribution | ItemExpense | Purchase | E:796000000 Charitable Donations |
| ItemExpCommCellular | Communication Cellular | ItemExpense | Purchase | E:614140000 Telephone Co Charges - Cell Phone and Pager |
| ItemExpCommNetwork | Communication Network | ItemExpense | Purchase | E:614200000 Network Charges |
| ItemExpCommTelephone | Communication Telephone | ItemExpense | Purchase | E:614110000 Telephone Co Charges - Local |
| ItemExpCommissionFee | Commission/Fee | ItemExpense | Purchase | E:631700000 Sales Commissions - Non-Employee |
| ItemExpHosting | Computer Server Hosting | ItemExpense | Purchase | E:616300000 Outside Computer Services |
| ItemExpInsBusiness | Insurance Business | ItemExpense | Purchase | E:691000000 Business Insurance |
| ItemExpInsEquipment | Insurance Equipment | ItemExpense | Purchase | E:694000000 Other Insurance |
| ItemExpInsHealth | Insurance Health | ItemExpense | Purchase | E:634100000 Group Health Insurance - Premiums |
| ItemExpInsOther | Insurance Other | ItemExpense | Purchase | E:694000000 Other Insurance |
| ItemExpInsRealEst | Insurance Real Estate | ItemExpense | Purchase | E:692000000 Real Estate Insurance |
| ItemExpInsVehicle | Insurance Vehicle | ItemExpense | Purchase | E:693000000 Vehicle Insurance |
| ItemExpInterestEquip | Interest Equipment | ItemExpense | Purchase | E:791100000 Equipment Interest Expense |
| ItemExpInterestOther | Interest Other | ItemExpense | Purchase | E:791000000 Interest Expense |
| ItemExpInterestReal | Interest Real Estate | ItemExpense | Purchase | E:791300000 Real Estate Interest Expense |
| ItemExpInterestVehi | Interest Vehicle | ItemExpense | Purchase | E:791200000 Vehicle Interest Expense |
| ItemExpLeaseEquip | Lease/Rent Equipment | ItemExpense | Purchase | E:612400000 Other Equipment Rent |
| ItemExpLeaseOther | Lease/Rent Other | ItemExpense | Purchase | E:612400000 Other Equipment Rent |
| ItemExpLeaseRealEst | Lease/Rent Real Estate | ItemExpense | Purchase | E:611110000 Basic Rent |
| ItemExpLeaseVehicle | Lease/Rent Vehicle | ItemExpense | Purchase | E:612300000 Vehicle Rent |
| ItemExpMaintEquip | Maintenance/Repair Equipment | ItemExpense | Purchase | E:613200000 Repairs and Maintenance - Furniture, Fixtures, and Equipment |
| ItemExpMaintOther | Maintenance/Repair Other | ItemExpense | Purchase | E:613900000 Repairs and Maintenance - Other |
| ItemExpMaintRealEst | Maintenance/Repair Real Estate | ItemExpense | Purchase | E:613100000 Repairs and Maintenance - Building |
| ItemExpMaintVehicle | Maintenance/Repair Vehicle | ItemExpense | Purchase | E:613400000 Repairs and Maintenance - Vehicle |
| ItemExpMedical | Medical and Health Care | ItemExpense | Purchase | — |
| ItemExpOfficePostage | Office Postage | ItemExpense | Purchase | E:652100000 Stationery and Supplies - Office Use |
| ItemExpOfficeSup | Office Supplies | ItemExpense | Purchase | E:652100000 Stationery and Supplies - Office Use |
| ItemExpOther | Other | ItemExpense | Purchase | E:789000000 Misc Operating Expense |
| ItemExpRoyalties | Royalties | ItemExpense | Purchase | — |
| ItemExpServAccount | Services Accounting | ItemExpense | Purchase | E:642000000 Accounting Fees |
| ItemExpServLabor | Services Labor | ItemExpense | Purchase | E:649000000 Other Consulting Fees |
| ItemExpServLegal | Services Legal | ItemExpense | Purchase | E:641000000 Legal Fees |
| ItemExpSupplies | Supplies | ItemExpense | Product, Purchase | E:652900000 Other Supplies |
| ItemExpTaxesLic | Taxes and Licenses | ItemExpense | Purchase | E:744000000 Other Business Taxes and Fees |
| ItemExpTravAir | Travel Air | ItemExpense | Purchase | E:681100000 Business Travel Expense |
| ItemExpTravCarRental | Travel Car Rental | ItemExpense | Purchase | E:681100000 Business Travel Expense |
| ItemExpTravLocal | Travel Local/Parking/Tolls | ItemExpense | Purchase | E:681100000 Business Travel Expense |
| ItemExpTravLodging | Travel Lodging | ItemExpense | Purchase | E:681100000 Business Travel Expense |
| ItemExpTravMealsEnt | Travel Meals/Entertainment | ItemExpense | Purchase | E:681200000 Business Meals and Entertainment (50% Deductible) |
| ItemExpTravOther | Travel Other | ItemExpense | Purchase | E:681100000 Business Travel Expense |
| ItemExpUtilElec | Utilities Electricity | ItemExpense | Purchase | E:611220000 Utilities - Electricity |
| ItemExpUtilHeating | Utilities Heating | ItemExpense | Purchase | E:611210000 Utilities - Heating |
| ItemExpUtilTrash | Utilities Trash/Recycle | ItemExpense | Purchase | E:611240000 Utilities - Trash Removal / Recycling |
| ItemExpUtilVehFuel | Utilities Vehicle Fuel | ItemExpense | Purchase | E:611250000 Utilities - Vehicle Fuel |
| ItemExpUtilWater | Utilities Water/Sewer | ItemExpense | Purchase | E:611230000 Utilities - Water and Sewer |
| ItemExpense | Expense | ItemExpense |  | E:789000000 Misc Operating Expense |
| ItemFee | Fee |  | Adjust, Purchase, Sales | O:834000000 Special Fees Collected; I:798000000 Non-operating Fees and Penalties |
| ItemFreeFills | Free Fills | ItemInvAdjust | Adjust, Sales | E:525100000 Free Fills |
| ItemHolidayHourly | Holiday Hourly | ItemPayrollIncome |  | I:632700000 Holiday Pay - Employees |
| ItemHolidaySalary | Holiday Salary | ItemPayrollIncome |  | I:632700000 Holiday Pay - Employees |
| ItemHourlyEarnings | Hourly Earnings | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemInvAdjust | Invoice Adjustment |  |  | — |
| ItemInventory | Asset - Inventory |  | Product, Purchase | I:149000000 Unreceived/Unbilled Inventory; O:411000000 Product Sales |
| ItemLateCharge | Late Payment Charge | ItemInvAdjust | Adjust, Sales | O:442000000 Late Payment Fees Received; I:517000000 COGS Late Payment Charges |
| ItemMiscCharge | Miscellaneous Charge |  | Adjust, Purchase, Sales | O:419000000 Miscellaneous Sales; I:798000000 Non-operating Fees and Penalties |
| ItemMkgtPkgAdj | Marketing Package Adjustment | ItemSales | Sales | O:419000000 Miscellaneous Sales |
| ItemNonproductiveEarnings | Nonproductive Earnings | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemOvertimePremium | Overtime Premium | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemPayAdjOverpay | Pay Period Adjustment - Overpay | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemPayAdjPay | Pay Period Adjustment - Pay | ItemPayrollIncome |  | I:631100000 Wages - Employee; O:260000000 Unearned Revenue |
| ItemPayrollDeduct | Payroll Deduction |  |  | E: |
| ItemPayrollExpense | Payroll Expense |  |  | — |
| ItemPayrollIncome | Payroll Income |  |  | I:631100000 Wages - Employee |
| ItemPayrollTaxes | Payroll Taxes |  |  | E:222000000 Payroll Withholding |
| ItemPieceMinWageAdj | Piece Min Wage Adjustment | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemPieceOrHourlyEarnings | Piece Or Hourly Earnings | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemPiecePlusHourlyEarnings | Piece Plus Hourly Earnings | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemPieceworkEarnings | Piecework Earnings | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemPrlCommission | Commission | ItemPayrollIncome |  | I:631600000 Sales Commissions - Employee |
| ItemPrlExp125Compy | 125*Compy. Contr Other Premium | ItemPayrollExpense | EngSec125Empr | — |
| ItemPrlExp125Hsa | 125*HSA Contribution | ItemPayrollExpense |  | — |
| ItemPrlExp125Ppo | 125*PPO | ItemPayrollExpense |  | — |
| ItemPrlExp401kEmpr | 401K Employer | ItemPayrollExpense | Eng401kEmpr | — |
| ItemPrlExpRothIraEmpr | Roth IRA Employer | ItemPayrollExpense |  | — |
| ItemPrlExpSimpleIraEmpr | Simple IRA Employer | ItemPayrollExpense |  | — |
| ItemPrlExpTaxFedPensionEmpr | Federal Pension Employer | ItemPayrollExpense |  | E:633230000 Federal Pension - Employer |
| ItemPrlExpTaxFutaEmpr | Federal Unemployment Insurance (FUTA) Employer | ItemPayrollExpense |  | E:633710000 Federal Unemployment Insurance - Employer |
| ItemPrlExpTaxHeadEmpr | Head Employer | ItemPayrollExpense |  | E:633290000 Local Misc Tax - Employer |
| ItemPrlExpTaxMedEmpr | Medicare Employer | ItemPayrollExpense |  | E:633220000 Federal Medicare - Employer |
| ItemPrlExpTaxOccPrivEmpr | Occupational Privilege Employer | ItemPayrollExpense |  | E:633290000 Local Misc Tax - Employer |
| ItemPrlExpTaxSchoolDistEmpr | School District Employer | ItemPayrollExpense |  | E:633290000 Local Misc Tax - Employer |
| ItemPrlExpTaxSocialSecEmpr | Social Security Employer | ItemPayrollExpense |  | E:633210000 Federal Social Security - Employer |
| ItemPrlExpTaxStateDisInsEmpr | State Disability Insurance Employer | ItemPayrollExpense |  | E:633250000 State Disability Insurance - Employer |
| ItemPrlExpTaxStateMiscEmpr | State Miscellaneous Employer | ItemPayrollExpense |  | E:633260000 State Misc Tax - Employer |
| ItemPrlExpTaxStatePensionEmpr | State Pension Employer | ItemPayrollExpense |  | E:633270000 State Pension - Employer |
| ItemPrlExpTaxStateUnInsEmpr | State Unemployment Insurance Employer | ItemPayrollExpense |  | E:633720000 State Unemployment Insurance - Employer |
| ItemPrlExpTaxStateWrkCmpInsEmpr | State Workers' Comp Insurance Employer | ItemPayrollExpense |  | — |
| ItemPrlExpTaxSurtaxEmpr | Surtax Employer | ItemPayrollExpense |  | E:633290000 Local Misc Tax - Employer |
| ItemProduct | Product | ItemSales | Product, Sales | I:149000000 Unreceived/Unbilled Inventory; O:411000000 Product Sales |
| ItemPromoDiscount | Promotional Discounts | ItemInvAdjust | Adjust, Sales | E:522200000 Promotional Discounts |
| ItemPromptDiscount | Prompt Payment Discount | ItemInvAdjust | Adjust, Sales | O:521000000 Prompt Payment Discounts; I:864000000 Payable Prompt Payment Discounts |
| ItemPtoHourly | PTO Hourly | ItemPayrollIncome |  | I:632500000 PTO Pay - Employees |
| ItemPtoSalary | PTO Salary | ItemPayrollIncome |  | I:632500000 PTO Pay - Employees |
| ItemReimbursement | Reimbursement | ItemPayrollIncome |  | E:789000000 Misc Operating Expense |
| ItemRental | Rental | ItemSales | Product, Sales | O:413000000 Asset Rental Sales |
| ItemRentalDeposit | Rental Deposit |  | Purchase, Sales | O:258100000 Financial Account In Transit Deposits; I:258200000 Financial Account In Transit Withdrawals |
| ItemReplacement | Replacement | ItemSales | Product, Sales | O:522000000 Discounts on Sales |
| ItemReturnAdjust | Return | ItemInvAdjust | Adjust, Sales | O:421000000 Customer Returns - Products; I:532000000 Good Returns To Vendors |
| ItemSalary | Salary | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemSales | Sales |  |  | O:410000000 Sales Revenue; I:500000000 Cost of Sales |
| ItemSalesTax | Sales Tax |  | Purchase, Sales | O:224000000 Sales Tax Collected; I:745000000 Sales and Use Taxes |
| ItemSalesThirdParty | Third Party | ItemSales | Sales | O:450000000 Third Party Sales |
| ItemServiceProduct | Service Product | ItemSales | Product, Sales | O:412000000 Service Sales |
| ItemShiftPremiumEarnings | Shift Premium Earnings | ItemPayrollIncome |  | I:631100000 Wages - Employee |
| ItemShipping | Shipping and Handling |  | Purchase, Sales | I:519100000 COGS Freight In; O:441000000 Postage and Handling Fees Received |
| ItemShippingOther | Other Shipping (Non-Inventory) |  | Purchase | I:653100000 Postage Expense |
| ItemShrinkage | Shrinkage | ItemInvAdjust | Adjust, Sales | E:527000000 Inventory Shrinkage |
| ItemSickHourly | Sick Hourly | ItemPayrollIncome |  | I:632300000 Sick Pay - Employees |
| ItemSickSalary | Sick Salary | ItemPayrollIncome |  | I:632300000 Sick Pay - Employees |
| ItemSlottingFees | Slotting Fees | ItemInvAdjust | Adjust, Purchase, Sales | E:523100000 Slotting Fees |
| ItemSupplierDiscount | Discount - Supplier |  | Adjust, Sales | O:522400000 Supplier Discounts; I:865000000 Other Purchase Discounts |
| ItemSurcharge | Surcharge | ItemSales | Sales | O:419000000 Miscellaneous Sales |
| ItemTaxAddtlMedEmpe | Additional Medicare Employee | ItemPayrollTaxes |  | E:222130000 Medicare Employee Withholding |
| ItemTaxCbt | Tax - City, Borough, and Township Withholding | ItemPayrollTaxes |  | E:222510000 Local Income Tax Employee Withholding |
| ItemTaxCountyWhold | Tax - County Income Withholding | ItemPayrollTaxes |  | E:222510000 Local Income Tax Employee Withholding |
| ItemTaxFedPensionEmpe | Tax - Federal Pension Employee | ItemPayrollTaxes |  | E:222140000 Federal Pension Employee Withholding |
| ItemTaxFederalWhold | Federal Income Withholding | ItemPayrollTaxes |  | E:222110000 Federal Income Tax Employee Withholding |
| ItemTaxFutaEmpe | Federal Unemployment Insurance (FUTA) Employee | ItemPayrollTaxes |  | E:222150000 Federal Unemployment Insurance Employee Withholding |
| ItemTaxHeadEmpe | Tax - Head Employee | ItemPayrollTaxes |  | E:222520000 Local Misc Tax Employee Withholding |
| ItemTaxMedEmpe | Medicare Employee | ItemPayrollTaxes |  | E:222130000 Medicare Employee Withholding |
| ItemTaxOccPrivEmpe | Tax - Occupational Privilege Employee | ItemPayrollTaxes |  | E:222520000 Local Misc Tax Employee Withholding |
| ItemTaxSchoolDistEmpe | Tax - School District Employee | ItemPayrollTaxes |  | E:222520000 Local Misc Tax Employee Withholding |
| ItemTaxSocialSecEmpe | Social Security Employee | ItemPayrollTaxes |  | E:222120000 Social Security Employee Withholding |
| ItemTaxStateDisInsEmpe | Tax - State Disability Insurance Employee | ItemPayrollTaxes |  | E:222420000 State Disability Insurance Employee Withholding |
| ItemTaxStateMiscEmpe | Tax - State Miscellaneous Employee | ItemPayrollTaxes |  | E:222430000 State Misc Tax Employee Withholding |
| ItemTaxStatePensionEmpe | Tax - State Pension Employee | ItemPayrollTaxes |  | E:222440000 State Pension Employee Withholding |
| ItemTaxStateUnInsEmpe | Tax - State Unemployment Insurance Employee | ItemPayrollTaxes |  | E:222450000 State Unemployment Insurance Employee Withholding |
| ItemTaxStateWhold | Tax - State Income Withholding | ItemPayrollTaxes |  | E:222410000 State Income Tax Employee Withholding |
| ItemTaxStateWrkCmpInsEmpe | Tax - State Workers' Comp Insurance Employee | ItemPayrollTaxes |  | — |
| ItemTaxSurtaxEmpe | Tax - Surtax Employee | ItemPayrollTaxes |  | E:222520000 Local Misc Tax Employee Withholding |
| ItemTimeEntry | Time Entry | ItemSales | Purchase, Sales | O:412000000 Service Sales; I:550000000 Cost of Services Sold |
| ItemVacationHourly | Vacation Hourly | ItemPayrollIncome |  | I:632100000 Vacation Pay - Employees |
| ItemVacationSalary | Vacation Salary | ItemPayrollIncome |  | I:632100000 Vacation Pay - Employees |
| ItemVatTax | VAT Tax (not added to totals) |  | Purchase, Sales | O:224000000 Sales Tax Collected; I:745000000 Sales and Use Taxes |
| ItemWarranty | Warranty | ItemSales | Sales | O:419000000 Miscellaneous Sales |
| ItemWorkEffort | Work Effort | ItemSales | Purchase, Sales | O:412000000 Service Sales; I:550000000 Cost of Services Sold |
| ItemWriteOff | Write-off | ItemInvAdjust | Adjust, Sales | O:782100000 Accounts Receivable Write Off; I:862000000 Accounts Payable Write Off |

171 item types, 157 with a GL mapping, 14 without.
