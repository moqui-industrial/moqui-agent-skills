# SimpleScreens patterns

Use this reference after choosing the needed screen type. Paths are relative to `runtime/component/SimpleScreens` in the target Moqui runtime.

## Baseline and navigation

- `screen/SimpleScreens.xml` is the application root: it sets shared `appRoot`, declares `<subscreens>`, and renders one `subscreens-panel`.
- `screen/SimpleScreens/Order.xml` is a module owner: it gives menu metadata, declares local and cross-module `subscreens-item` entries, and uses a tab panel.
- Child detail screens declare the identifier as a required screen parameter, for example `Order/OrderDetail.xml` with `orderId`.

## Complex business-detail screens

The five domains asked for share a layout rule: keep lifecycle mutations in named transitions at the top; load the aggregate once in page actions; render conditional panels and forms below.

| Domain | Read these first | Reusable lesson |
| --- | --- | --- |
| Order | `screen/SimpleScreens/Order/OrderDetail.xml`, `Order/OrderItems.xml`, `Order/QuickItems.xml` | Status changes call `OrderServices`; multiple related forms/panels are conditionally shown from one display-info load; product/facility selectors are `transition-include`d. |
| Shipment | `screen/SimpleScreens/Shipment/ShipmentDetail.xml`, `ShipmentItems.xml`, `ShipmentPackages.xml`, `ShipmentPick.xml`, `ShipmentPack.xml` | Keep receiving, reservation, package, pick, and pack operations as distinct transitions/subscreens; use shipping template endpoints rather than duplicate selector logic. |
| Task | `screen/SimpleScreens/Task/TaskSummary.xml`, `EditTask.xml`, `EditRelated.xml`, `EditUsers.xml`, `EditTimeEntries.xml` | Work-effort screens separate summary, relationships, users, time, and nested comments; nested comment screens are children of the summary, not copied inline. |
| Project | `screen/SimpleScreens/Project/ProjectSummary.xml`, `EditProject.xml`, `EditMilestones.xml`, `ProjectProgressReport.xml` | Project screens use the same work-effort services with project-specific panels, milestones, participants, and a report; shared selectors live in `template/work/WorkTransitions.xml`. |
| Request | `screen/SimpleScreens/Request/EditRequest.xml`, `EditRequestItems.xml`, `EditTasks.xml`, `EditUsers.xml` | Requests use dedicated owning services and split comments/items/tasks/users/wiki into subscreens; preserve request parameter propagation through each child. |

Do not copy these screens wholesale. They contain historical `<script>` actions and integration-specific behavior. Reuse their layout, transition response, screen hierarchy, and naming patterns; generate new action logic under the `moqui-actions` restricted profile unless the task explicitly calls for a reviewed exception.

## Standard transition templates

Reusable transition screens are under `template/` and use the normal screen root and CC0 header:

- `template/account/AccountTransitions.xml`: GL account and period selectors.
- `template/facility/FacilityTransitions.xml`: facility, location, and container selectors.
- `template/party/PartyTransitions.xml`: party classification, settings, and time-period selectors.
- `template/product/ProductTransitions.xml`: product, price, category, feature, asset, pool, and lot selectors.
- `template/request/RequestTransitions.xml`: request selector.
- `template/shipment/ShipmentTransitions.xml`: package weights, shipping options, labels.
- `template/work/WorkTransitions.xml`: project, task, project-party, milestone, and project-invoice selectors.

Include a transition by name with `<transition-include name="..." location="component://SimpleScreens/template/..."/>`; do not expose the template as a navigable screen unless that is its explicit role.

## Reports and render modes

- `screen/SimpleScreens/Accounting/Reports/BalanceSheet.xml` shows the compact report pattern: required filter parameters, report service in `<actions>`, a CSV URL built from the current screen URL, and `render-mode` templates for HTML/Quasar and CSV.
- `screen/SimpleScreens/SimpleReport/ViewReport.xml` is a dynamic report: it checks `DataDocumentUserGroup` authorization before resolving the dynamic entity and renders it with a dynamic `form-list`.
- Printable shipment, order, invoice, and payment documents route to dedicated screens/templates rather than embedding XSL-FO in interactive screens.

## DbForm / survey screens

- `screen/SimpleScreens/Survey/FindSurvey.xml`: finds and creates `DbForm` records.
- `screen/SimpleScreens/Survey/EditSurvey.xml`: edits form metadata and user-group access.
- `screen/SimpleScreens/Survey/Fields.xml`: maintains `DbFormField` and `DbFormFieldOption`, then previews a runtime form with `form-single extends="DbForm#${formId}" dynamic="true"`.
- `screen/SimpleScreens/Survey/ResponseStats.xml`: renders aggregate response data by field type.

Treat DbForm as configuration data with its own service contract. A generated application form is not a substitute for the DbForm administration screens.
