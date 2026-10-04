---
name: moqui-dbform
description: Forms and surveys defined as data in Moqui (DbForm) — standalone questionnaires, extra fields added to an existing XML screen form for some user groups, product or tax forms, and how answers are stored in FormResponse and linked to business records. Use this skill whenever the task is to collect information from a user with a form, survey, questionnaire, checklist or configurable fields in Moqui, or to add fields to an existing screen without changing its code, before considering a new XML screen or a generated UI.
---

# moqui-dbform: forms as data

A DbForm is a form stored as records, not code. It renders through the normal screen form machinery, so it looks and behaves like any Moqui form in the screen that shows it, and it can be created and changed by loading data. For generated UI this is the safest target: the output is data checked against the model, not code.

Write DbForms as data files with the `moqui-data` skill and validate them with its `check_data.py`.

## The model

All entities are in `moqui.screen.form` (framework `ScreenEntities.xml`).

| Entity | Role |
| --- | --- |
| `DbForm` | The form: `formId`, `purposeEnumId` (`DbfpSurvey`, `DbfpTaxStatement`, `DbfpOther`), `isListForm`, `modifyXmlScreenForm`, print settings |
| `DbFormField` | One field: `fieldName`, `title`, `tooltip`, `fieldTypeEnumId`, `layoutSequenceNum`, `isRequired`, `condition`, `entryName`, print position |
| `DbFormFieldAttribute` | Extra attributes copied onto the field or its widget (`size`, `cols`, `rows`...) |
| `DbFormFieldOption` | Fixed options: `keyValue` and `text` |
| `DbFormFieldEntOpts` (+ `Cond`, `Order`) | Options read from an entity, with conditions and ordering; `text` is a template, default `${description}` |
| `DbFormUserGroup` | Which user groups get the form; `ALL_USERS` for everyone |
| `FormResponse`, `FormResponseAnswer` | A submitted response and its answers, always stored as plain text (`valueText`) |

Field types are the `DbFormFieldType` enumeration: `DBFFT_text-line`, `DBFFT_text-area`, `DBFFT_drop-down`, `DBFFT_radio`, `DBFFT_check`, `DBFFT_date-time`, `DBFFT_display`, `DBFFT_display-entity`, `DBFFT_file`, `DBFFT_hidden`, `DBFFT_label`, `DBFFT_link`, `DBFFT_image`, `DBFFT_password`, `DBFFT_submit`, `DBFFT_reset`, and the find types `DBFFT_text-find`, `DBFFT_date-find`, `DBFFT_range-find`.

`assets/SurveyDbFormTemplate.xml` is a complete survey (text, radio with fixed options, drop-down from an entity, text area, submit, user group) that passes the data checker. Mantle's `data/TaxFormData.xml` shows a large real case: the US W-2 and 1099 forms with print coordinates.

## Three ways to use a DbForm

1. **As a form of its own.** A screen form extends it: `extends="DbForm#AcmeSupplierQual"` on a `form-single` or `form-list`. The framework turns the records into form fields when the screen is rendered.
2. **To add fields to an existing XML form, without touching its code.** Set `modifyXmlScreenForm` to the screen location and form name separated by `#`, and list the user groups in `DbFormUserGroup`. When that form is rendered for a user in one of those groups, the DbForm fields are merged in.
3. **Attached to business records.** Mantle links forms to its objects: `ProductDbForm` attaches forms to a product (with a form type, role and market segment), `OrderItemFormResponse` keeps the answers given for an order item, and `TaxStatement` stores `formId` plus `formResponseId` for tax forms.

## Saving answers

Call `org.moqui.impl.ScreenServices.create#FormResponse` with `formId` and `responseMap` (field name to value); it returns `formResponseId`. Then link that id to the business record it belongs to. Mantle's payroll does exactly this: it builds the W-2 values, saves them with `create#FormResponse`, then creates the `TaxStatement` with the `formResponseId`.

## Rules for generated forms

- **No expressions.** `DbFormField.condition` is a Groovy condition (it becomes a `conditional-field`) and `entryName` becomes the field's `from` expression. Leave both empty in generated forms; they are code hidden in data.
- **Validate in the service.** In the framework, `isRequired` is stored but not used when the form is rendered, and answers are plain text. Check required answers and types in the service that saves the response.
- **Narrow audiences.** Prefer a specific `UserGroup` over `ALL_USERS` unless the form is truly for everyone.
- **Options from entities should point at reference data** such as `Geo`, `Enumeration` or `Uom`, not at business records the form's users should not see.
