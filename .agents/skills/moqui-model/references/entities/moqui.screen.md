# moqui.screen

One line per entity. E = entity, V = view-entity. Generated; do not edit.

- E moqui.screen.ScreenDocument | src: moqui-framework | pk: screenLocation,docIndex | fields: locale:text-short, docTitle:text-medium, docLocation:text-medium | rels: 
- E moqui.screen.ScreenPathAlias | src: moqui-framework | pk: aliasPath,fromDate | fields: thruDate:date-time, screenPath:text-medium | rels: 
- E moqui.screen.ScreenScheduled | src: moqui-framework | pk: screenScheduledId | fields: screenPath:text-medium, formListFindId:id, renderMode:text-short, noResultsAbort:text-indicator, cronExpression:text-medium, fromDate:date-time, thruDate:date-time, saveToLocation:text-long, emailTemplateId:id, emailSubject:text-long, userId:id, userGroupId:id | rels: one>FormListFind, one>EmailTemplate, one>UserAccount, one>UserGroup
- E moqui.screen.ScreenScheduledLock | src: moqui-framework | pk: screenScheduledId | fields: lastRunTime:date-time | rels: one>ScreenScheduled
- E moqui.screen.ScreenTheme | src: moqui-framework | pk: screenThemeId | fields: screenThemeTypeEnumId:id, description:text-medium | rels: one>Enumeration[ScreenThemeType]
- E moqui.screen.ScreenThemeIcon | src: moqui-framework | pk: screenThemeId,textPattern | fields: iconClass:text-medium | rels: one>ScreenTheme
- E moqui.screen.ScreenThemeResource | src: moqui-framework | pk: screenThemeId,sequenceNum | fields: resourceTypeEnumId:id, resourceValue:text-long | rels: one>ScreenTheme, one>Enumeration[ScreenThemeResourceType]
- E moqui.screen.SubscreensDefault | src: moqui-framework | pk: screenLocation,defaultSeqId | fields: conditionExpression:text-medium, subscreenName:text-medium | rels: 
- E moqui.screen.SubscreensItem | src: moqui-framework | pk: screenLocation,subscreenName,userGroupId | fields: subscreenLocation:text-medium, menuTitle:text-medium, menuIndex:number-integer, menuInclude:text-indicator, makeDefault:text-indicator, noSubPath:text-indicator | rels: one>UserGroup
- E moqui.screen.form.DbForm | src: moqui-framework | pk: formId | fields: purposeEnumId:id, isListForm:text-indicator, modifyXmlScreenForm:text-medium, description:text-medium, comments:text-long, printTemplateLocation:text-medium, acroFormLocation:text-medium, printFontSize:text-short, printFontFamily:text-short, printContainerWidth:text-short, printContainerHeight:text-short, printRepeatCount:number-integer, printRepeatNewPage:text-indicator | rels: one>Enumeration[DbFormPurpose]
- E moqui.screen.form.DbFormField | src: moqui-framework | pk: formId,fieldName | fields: condition:text-medium, entryName:text-medium, title:text-medium, tooltip:text-medium, fieldTypeEnumId:id, layoutSequenceNum:number-integer, isRequired:text-indicator, printPageNumber:number-integer, printTop:text-short, printLeft:text-short, printBottom:text-short, printRight:text-short, printWidth:text-short, printHeight:text-short, printTextAlign:text-short, printVerticalAlign:text-short, printFontSize:text-short, printFontFamily:text-short | rels: one>DbForm, one>Enumeration[DbFormFieldType]
- E moqui.screen.form.DbFormFieldAttribute | src: moqui-framework | pk: formId,fieldName,attributeName | fields: value:text-medium | rels: one>DbFormField
- E moqui.screen.form.DbFormFieldEntOpts | src: moqui-framework | pk: formId,fieldName,sequenceNum | fields: entityName:text-medium, text:text-medium | rels: one>DbFormField
- E moqui.screen.form.DbFormFieldEntOptsCond | src: moqui-framework | pk: formId,fieldName,sequenceNum,entityFieldName | fields: value:text-medium | rels: one>DbFormFieldEntOpts
- E moqui.screen.form.DbFormFieldEntOptsOrder | src: moqui-framework | pk: formId,fieldName,sequenceNum,orderSequenceNum | fields: entityFieldName:text-medium | rels: one>DbFormFieldEntOpts
- E moqui.screen.form.DbFormFieldOption | src: moqui-framework | pk: formId,fieldName,sequenceNum | fields: keyValue:text-medium, text:text-medium | rels: one>DbFormField
- E moqui.screen.form.DbFormUserGroup | src: moqui-framework | pk: formId,userGroupId | fields:  | rels: one>DbForm, one>UserGroup
- E moqui.screen.form.FormConfig | src: moqui-framework | pk: formConfigId | fields: description:text-medium, formLocation:text-medium, configTypeEnumId:id | rels: one>Enumeration[FormConfigType], many>FormConfigField, many>FormConfigUser, many>FormConfigUserGroup
- E moqui.screen.form.FormConfigField | src: moqui-framework | pk: formConfigId,fieldName | fields: positionIndex:number-integer, positionSequence:number-integer | rels: one>FormConfig
- E moqui.screen.form.FormConfigUser | src: moqui-framework | pk: formLocation,userId | fields: formConfigId:id | rels: one-nofk>UserAccount, one>FormConfig
- E moqui.screen.form.FormConfigUserGroup | src: moqui-framework | pk: formConfigId,userGroupId | fields:  | rels: one>FormConfig, one>UserGroup
- E moqui.screen.form.FormConfigUserType | src: moqui-framework | pk: formLocation,userId,configTypeEnumId | fields: formConfigId:id | rels: one-nofk>UserAccount, one>Enumeration[FormConfigType], one>FormConfig
- E moqui.screen.form.FormListFind | src: moqui-framework | pk: formListFindId | fields: description:text-medium, formLocation:text-medium, orderByField:text-medium, formConfigId:id | rels: one>FormConfig, many>FormListFindField, many>FormListFindUser, many>FormListFindUserGroup
- E moqui.screen.form.FormListFindField | src: moqui-framework | pk: formListFindId,fieldName | fields: fieldValue:text-medium, fieldOperator:text-short, fieldNot:text-indicator, fieldIgnoreCase:text-indicator, fieldFrom:text-short, fieldThru:text-short, fieldPeriod:text-short, fieldPerOffset:number-integer | rels: one>FormListFind
- E moqui.screen.form.FormListFindUser | src: moqui-framework | pk: formListFindId,userId | fields:  | rels: one>FormListFind, one-nofk>UserAccount
- E moqui.screen.form.FormListFindUserDefault | src: moqui-framework | pk: screenLocation,userId | fields: formListFindId:id | rels: one-nofk>UserAccount, one>FormListFind
- E moqui.screen.form.FormListFindUserGroup | src: moqui-framework | pk: formListFindId,userGroupId | fields:  | rels: one>FormListFind, one>UserGroup
- E moqui.screen.form.FormResponse | src: moqui-framework | pk: formResponseId | fields: formLocation:text-medium, formId:id, userId:id, responseDate:date-time | rels: one>DbForm, one>UserAccount
- E moqui.screen.form.FormResponseAnswer | src: moqui-framework | pk: formResponseAnswerId | fields: formResponseId:id, formId:id, fieldName:text-medium, sequenceNum:number-integer, valueText:text-long | rels: one>FormResponse, one>DbForm, one-nofk>DbFormField
- V moqui.screen.ScreenScheduledAndFind | src: moqui-framework | members: SSCH=ScreenScheduled, FLF=rel SSCH:formListFind | alias-all: SSCH,FLF | aliases: 
- V moqui.screen.form.DbFormAndUserGroup | src: moqui-framework | members: DBFUG=DbFormUserGroup, USRGRP=UserGroup | alias-all: USRGRP | aliases: formId
- V moqui.screen.form.DbFormLookup | src: moqui-framework | members: DBF=DbForm, DBFUG=DbFormUserGroup | aliases: formId, modifyXmlScreenForm, userGroupId
- V moqui.screen.form.FormConfigUserGroupView | src: moqui-framework | members: FCNF=FormConfig, FCUG=FormConfigUserGroup | alias-all: FCNF,FCUG | aliases: 
- V moqui.screen.form.FormListFindUserGroupView | src: moqui-framework | members: FLF=FormListFind, FLFUG=FormListFindUserGroup | alias-all: FLF,FLFUG | aliases: 
- V moqui.screen.form.FormListFindUserView | src: moqui-framework | members: FLF=FormListFind, FLFU=FormListFindUser | alias-all: FLF,FLFU | aliases: 
- V moqui.screen.form.FormResponseAnsAndDbFormField | src: moqui-framework | members: FRA=FormResponseAnswer, DBFF=DbFormField | alias-all: FRA,DBFF | aliases: 
