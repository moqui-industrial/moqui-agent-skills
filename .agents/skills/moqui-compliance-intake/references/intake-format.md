# intake.json

One file per project, written by the agent from the bill, the drawings and the user's answers, then loaded with
`scripts/load_intake.py`. Ids: letters, digits, `_`, `.`, `-`; a project prefix.

```json
{
  "mode": "product",
  "root": "IMG_ARES150",
  "products": [
    {"productId": "IMG_ARES150", "productName": "Boiler ARES 150 TEC ErP", "digital": true,
     "categories": ["CMP_PC_MACHINERY", "CMP_PC_PRODUCT_DIGITAL_ELEMENTS"], "features": ["CMP_PF_CN_NETWORK_CONNECTED"]},
    {"productId": "IMG_BCM", "productName": "Boiler control board BCM", "parentProductId": "IMG_ARES150", "quantity": 1,
     "digital": true, "categories": ["CMP_PC_PROGRAMMABLE_CONTROLLER"], "features": ["CMP_PF_CN_SOFTWARE_LOADABLE"]},
    {"productId": "IMG_TERM", "productName": "Terminal blocks", "parentProductId": "IMG_ARES150", "passive": true}
  ],
  "functions": [
    {"parentProductId": "IMG_ARES150", "purposeEnumId": "CmpDepSecurityZone", "productName": "Z1 Boiler control zone",
     "members": [{"productId": "IMG_BCM", "role": "CmpDepRoleMember"}]}
  ]
}
```

| Field | Meaning |
| --- | --- |
| `mode` | `product` (a type, manufacturer's view) or `installation` (one customer's plant) |
| `root` | the machine, product or system under consideration; the plan starts here |
| `products[].parentProductId` | the bill: `ProductAssoc` `PatEngBom` from the parent, with `quantity` |
| `products[].digital` | the product has software, firmware or a data/network interface (CRA `ART3.pt1`); required unless `passive` |
| `categories`, `features` | hook ids (`ProductCategory`, `ProductFeature`) chosen with `hook_candidates.py` and checked on the norm item |
| `functions[]` | function levels of the type: `add#FunctionProduct`; roles `CmpDepRoleInput`, `CmpDepRoleLogic`, `CmpDepRoleOutput`, `CmpDepRoleActuator`, `CmpDepRoleMember` |

Installation only:

```json
  "assets":  [{"assetId": "PLT_A_K1", "productId": "FMQ_CPU1514SP", "serialNumber": "S C-X4U12345", "assetName": "K1",
               "facilityId": "PLANT_1"}],
  "devices": [{"deviceId": "PLT_D_K1", "assetId": "PLT_A_K1", "deviceTypeEnumId": "DtPLC",
               "physical": {"deviceName": "K1", "vendorName": "Siemens", "modelName": "CPU 1514SP-2 PN",
                            "serialNumber": "S C-X4U12345", "firmwareVersion": "V3.1.2"}}],
  "groups":  [{"deviceId": "PLT_G_Z1", "groupName": "Z1 Machine control zone", "purposeEnumId": "CmpDepSecurityZone",
               "members": [{"memberDeviceId": "PLT_D_K1"}]},
              {"deviceId": "PLT_G_SF1", "groupName": "SF1 UV door interlock", "purposeEnumId": "CmpDepGuardInterlocking",
               "members": [{"memberDeviceId": "PLT_D_S1", "purposeEnumId": "CmpDepRoleInput"},
                           {"memberDeviceId": "PLT_D_K1", "purposeEnumId": "CmpDepRoleLogic"}]}]
```

`deviceTypeEnumId`: the moqui-device `DeviceType` enumeration (`DtPLC`, `DtSafetyPLC`, `DtSwitch`, `DtRouter`,
`DtFirewall`, `DtDrive`, `DtRemoteIO`, `DtIndustrialPc`, `DtEdgeGateway`, `DtSensor`, ...); groups default to
`DtDeviceGroup`. `Device.assetId` (mantle-udm extension) links the device to its Asset, the Asset to its Product.
