# Data files catalog (generated)

Load order: components in dependency order, then files in name order. Use these files as patterns for your own setup data; demo files are examples of style, never sources of ids.

## framework

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| CommonL10nData.xml | seed-initial | 56 | LocalizedMessage 44, LocalizedEntityField 12 |
| CurrencyData.xml | seed-initial | 170 | Uom 170 |
| EntityTypeData.xml | seed | 15 | Enumeration 14, EnumerationType 1 |
| GeoCountryData.xml | seed-initial | 242 | Geo 242 |
| LlmTypeData.xml | seed | 31 | Enumeration 13, ArtifactGroupMember 6, ArtifactGroup 3, ArtifactAuthz 3, EnumerationType 3, UserPermission 1 |
| MoquiSetupData.xml | seed-initial | 40 | ServiceJob 13, EmailTemplate 6, NotificationTopic 5, UserPermission 3, UserGroupPermission 3 |
| SecurityTypeData.xml | seed | 24 | UserPermission 5, UserGroupPermission 5, UserGroup 4, ArtifactGroupMember 3, ArtifactAuthz 3, Enumeration 2 |
| UnitData.xml | seed | 392 | UomConversion 182, Uom 181, UomDimTypeGroupMember 16, UomDimensionType 13 |

## tools

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| ToolsSecurityData.xml | seed | 9 | artifactGroups 3 |

## webroot

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| WebrootL10nData.xml | seed | 1 | LocalizedMessage 1 |
| WebrootQuasarThemeData.xml | seed-initial | 14 | ScreenThemeResource 10, Enumeration 1, ScreenTheme 1 |
| WebrootSecurityData.xml | seed | 7 | Enumeration 3, ArtifactGroupMember 2, ArtifactGroup 1, ArtifactAuthz 1 |
| WebrootSecurityDemoData.xml | demo | 9 | UserGroupMember 2, UserAccount 1, UserPermission 1, UserGroupPermission 1, UserLoginHistory 1, ArtifactGroup 1 |
| WebrootThemeData.xml | seed-initial | 18 | ScreenThemeResource 16 |

## mantle-udm

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| AccountConfigData.xml | install | 2 | PaymentGatewayConfig 2 |
| CarrierData.xml | install | 28 | CarrierShipmentMethod 16, Party 4 |
| GeoCanData.xml | install | 26 | Geo 13, GeoAssoc 13 |
| GeoChnData.xml | install | 68 | Geo 34, GeoAssoc 34 |
| GeoIndData.xml | install | 72 | Geo 36, GeoAssoc 36 |
| GeoItaData.xml | install | 224 | Geo 112, GeoAssoc 112 |
| GeoJpnData.xml | install | 149 | GeoAssoc 94, Geo 55 |
| GeoKorData.xml | install | 34 | Geo 17, GeoAssoc 17 |
| GeoPrtData.xml | install | 40 | Geo 20, GeoAssoc 20 |
| GeoUsaData.xml | install | 201 | GeoAssoc 132, Geo 69 |
| GeoVnmData.xml | install | 124 | Geo 62, GeoAssoc 62 |
| HolidayUsaData.xml | install | 94 | workEfforts 31, WorkEffortCategory 2 |
| ItemTypeData.xml | seed | 308 | Enumeration 179, EnumGroupMember 128, EnumerationType 1 |
| MantleDocumentData.xml | seed-initial | 170 | dataDocuments 5, DataFeed 1 |
| MantleDocumentInventoryData.xml | seed-initial | 78 | dataDocuments 5, DataFeed 1 |
| MantleDocumentSalesData.xml | seed-initial | 172 | dataDocuments 4, DataFeed 1 |
| MantleDocumentWorkData.xml | seed-initial | 113 | dataDocuments 4, DataFeed 1 |
| MantleUdmSetupData.xml | seed-initial | 36 | LocalizedMessage 29, Enumeration 5, userPermissions 1, userGroupPermissions 1 |
| PartyInstallData.xml | install | 14 | PartyClassification 14 |
| PayrollData.xml | seed | 54 | PartySettingType 23, Enumeration 6, EnumerationType 2 |
| SalesData.xml | seed-initial | 21 | Enumeration 15, StatusItem 3, StatusFlowTransition 2, StatusType 1 |
| ZaaGlAccountsInstallData.xml | install | 1130 | GlAccount 487, GlAccountOrganization 188, ItemTypeGlAccount 178, Enumeration 152, GlAccountTypeDefault 36, PaymentTypeGlAccount 17 |
| ZapPayrollTaxInstallData.xml | install | 227 | PayrollAllowance 21, PayrollAdjustment 18, PayrollStdDeduction 12, PayrollGarnishMinWage 4, Party 3, TaxAuthority 2 |

## mantle-usl

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| ACHReturnCodes.xml | install | 91 | Enumeration 89, EnumerationType 2 |
| MantleSetupData.xml | seed-initial | 85 | DbResource 13, ServiceJob 7, ServiceRegister 6, userPermissions 5, userGroupPermissions 5, Enumeration 3 |
| OrderInstallData.xml | install | 24 | LocalizedMessage 24 |
| TaxFormData.xml | install | 159 | DbForm 2 |
| ZbaOrganizationDemoData.xml | demo | 207 | PartyRole 24, Party 19, PartyRelationship 17, PartyContactMech 17, ContactMech 13, Organization 10 |
| ZcaProductDemoData.xml | demo | 251 | DbResource 16, Product 13, ProductCategory 12, ProductCategoryMember 12, ProductFeature 10, WikiPage 8 |

## moqui-sftp

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| SftpDemoData.xml | demo | 5 | SystemMessageType 1, SystemMessageRemote 1, ServiceJob 1 |

## moqui-math

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| MathData.xml | seed | 262 | Enumeration 177, ParameterDef 65, EnumerationType 11, EnumGroupMember 9 |

## moqui-device

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| DeviceData.xml | seed | 599 | Enumeration 342, StatusFlowTransition 149, StatusFlowItem 44, StatusItem 40, EnumerationType 8, StatusFlow 7 |
| DeviceTestData.xml | seed | 197 | Parameter 36, ParameterDef 29, DeviceRequestItem 26, ParameterLog 23, DeviceRequest 17, Measurement 14 |
| HVACDemoData.xml | seed | 418 | Parameter 225, ParameterDef 52, StatusFlowTransition 24, DeviceRule 21, DeviceRequestItem 20, Device 16 |
| TrajectoryPlannerData.xml | seed | 35 | Enumeration 14, EnumGroupMember 12, EnumerationType 2, Device 1, PhysicalDevice 1, DeviceRequest 1 |

## SimpleScreens

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| MyAccountDocumentData.xml | seed-initial | 11 | NotificationTopic 5, DataFeed 1 |
| SimpleScreensSetupData.xml | seed-initial | 192 | artifactGroups 23, ScreenDocument 13, Enumeration 7, FormConfig 7, FormListFind 7, ScreenThemeResource 6 |

## MarbleERP

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| MarbleErpSetupData.xml | seed-initial | 26 | DataDocumentLink 7, artifactGroups 2, Enumeration 1, userGroups 1 |

## PopCommerce

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| PopCommerceAaaSetupData.xml | seed-initial | 223 | artifactGroups 18, userGroups 10, ScreenThemeResource 9, Enumeration 2, ArtifactGroup 1, ArtifactGroupMember 1 |
| PopCommerceAabDocumentData.xml | seed-initial | 11 | DataDocumentLink 7, cloneDataDocument 1, DataDocumentCondition 1, DataFeed 1 |
| PopCommerceDemoData.xml | demo | 89 | parties 9, EmailTemplate 4, ProductStoreEmail 4, indexDataFeedDocuments 2, ProductStore 1, ProductStoreDataDocument 1 |

## hm

| File | Type | Records | Main content (top-level element counts) |
| --- | --- | --- | --- |
| HiveMindAaaSetupData.xml | seed-initial | 40 | EmplPositionClassWorkType 10, EmplPositionClass 8, ArtifactAuthz 6, Enumeration 4, UserGroup 3, ArtifactGroup 2 |
| HiveMindAabDocumentData.xml | seed-initial | 11 | DataDocumentLink 7, EmailTemplate 2, NotificationTopic 2 |
| HiveMindDemoData.xml | demo | 114 | WorkEffortParty 14, WorkEffort 13, WorkEffortAssoc 11, InvoiceItem 8, WikiPage 7, WikiPageHistory 7 |

