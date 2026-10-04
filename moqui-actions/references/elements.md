# xml-actions element reference (generated)

Source: xml-actions-3.xsd plus usage counted inside <actions> blocks of mf/framework, mr/base-component, mantle-usl, moqui-sftp, moqui-math, moqui-device, SimpleScreens, MarbleERP, PopCommerce, hm.
Total element occurrences counted: 28878. Elements ordered by real usage.

## Usage summary

Uses counts every <actions>, <always-actions>, <pre-actions> and <row-actions> block; 'in screens' is the part found in screen files (screen, transition and form actions).

| Element | Uses | In screens | Cumulative |
| --- | --- | --- | --- |
| set | 6541 | 1344 | 22% |
| if | 4425 | 504 | 37% |
| econdition | 3720 | 1026 | 50% |
| service-call | 2212 | 277 | 58% |
| entity-find | 1705 | 562 | 64% |
| entity-find-one | 1639 | 498 | 70% |
| script | 1238 | 383 | 74% |
| field-map | 1058 | 328 | 78% |
| return | 966 | 80 | 81% |
| iterate | 888 | 79 | 84% |
| order-by | 672 | 288 | 86% |
| then | 589 | 76 | 88% |
| else | 530 | 68 | 90% |
| date-filter | 379 | 107 | 91% |
| log | 369 | 36 | 93% |
| select-field | 314 | 124 | 94% |
| message | 241 | 42 | 95% |
| entity-update | 221 | 3 | 95% |
| continue | 197 | 9 | 96% |
| else-if | 137 | 19 | 97% |
| entity-create | 113 | 0 | 97% |
| econditions | 109 | 52 | 97% |
| entity-find-count | 93 | 48 | 98% |
| break | 77 | 4 | 98% |
| filter-map-list | 70 | 36 | 98% |
| search-form-inputs | 69 | 65 | 98% |
| order-map-list | 59 | 19 | 99% |
| entity-make-value | 34 | 0 | 99% |
| entity-delete-by-condition | 31 | 1 | 99% |
| entity-sequenced-id-primary | 28 | 0 | 99% |
| entity-find-related-one | 27 | 9 | 99% |
| entity-set | 26 | 0 | 99% |
| econdition-object | 22 | 4 | 99% |
| check-errors | 21 | 0 | 99% |
| having-econditions | 17 | 12 | 99% |
| entity-delete | 16 | 0 | 99% |
| while | 14 | 0 | 99% |
| entity-find-related | 4 | 0 | 99% |
| entity-sequenced-id-secondary | 4 | 0 | 99% |
| entity-delete-related | 2 | 2 | 99% |
| actions | 1 | 0 | 100% |

Declared but never used in the scanned code: and, assert, compare, condition, entity-data, expression, limit-range, limit-view, not, or, use-iterator

## Elements

### set
- uses: 6541 (in screens: 1344) | group: EnvOperations
- doc: Set a field from another field (from) or an inline value, or a default-value.
  - `field` (required): Name of the field to set a value in.
  - `from`: Name of a field to copy from. Can also be an expression that evaluates to something to put into the field.
  - `value`: Inline value to copy in field. May include variables using the ${} syntax.
  - `default-value`: Default value to set in field if an empty String or null value is found.
  - `type`: Type to convert to. NewList will create a new List, NewMap will create a new Map.
  - `set-if-empty` (default=true): If an empty String or null value is found, set that in the field. Defaults to true, set to false to do nothing to the field.
- example (ScreenRenderEmail.xml): `<set field="title" from="title ?: 'Rendered screen attached'"/>`

### if
- uses: 4425 (in screens: 504) | group: IfOtherOperations
- doc: The if operation offers a flexible way of specifying combinations of conditions, alternate conditions, and operations to run on true evaluation of the conditions or to run otherwise. The other if operations are meant for a specific, simple condition when used outside of the condition sub-element of this operation. The attributes of the other if operations are the same when used inside this operati…
- children: condition, then, else-if, else, (any action)
  - `condition`: A boolean expression in Groovy. Will be AND combined with other conditions if present.
- example (ScreenServices.xml): `<if condition="emailTemplate == null &amp;&amp; !saveToLocation">`

### econdition
- uses: 3720 (in screens: 1026)
- doc: Adds a econdition to the query to compare the field-name field to a context field, a String value, or another field on the entity.
  - `field-name` (required): The field on the entity to constrain on. If from, value and to-field-name are all empty this is also used as the name of the context field to compare to.
  - `operator` (default=equals): Operator to apply to field-name on one side, and from, value, or to-field-name on the other side. For the between operator the from should be a Collection with exactly 2 values in it. For the in operator the from should …
  - `from`: Field expression in the context to compare the entity field to.
  - `value`: Comparison value, use ${} syntax to expand variables.
  - `to-field-name`: Compare the field-name field to another field on the entity.
  - `ignore-case` (default=false): Ignore case when doing the compare. Defaults to false.
  - `ignore-if-empty` (default=false): Leave out the constraint if the comparison value is empty or null. Defaults to false.
  - `or-null` (default=false): If true make a condition specified value or null as valid matches.
  - `ignore` (default=false): Ignore the econdition (leave out of the find) if set to true or expression evaluates to true. Defaults to false.
- example (SearchServices.xml): `<econdition field-name="dataDocumentId" ignore-if-empty="true"/>`

### service-call
- uses: 2212 (in screens: 277) | group: CallOperations
- doc: Call a service.
- children: field-map
  - `name` (required): The combined service name, like: "${path}.${verb}${noun}". To explicitly separate the verb and noun put a hash (#) between them, like: "${path}.${verb}#${noun}".
  - `in-map` (default=false): Creates an in parameters with variables matching the names of service in-parameters elements, doing type conversions as needed. If false (default) does nothing. If true constructs an in-map from the context. Otherwise is…
  - `out-map`: Optional name in the method environment to use for the output (results) map. If empty then the output map will be ignored.
  - `out-map-add-to-existing` (default=true): If true (default) out-map is added to an existing Map with the same name. If false replaces existing Map in the context.
  - `async` (default=false, values=true|false|distribute): If true runs the service asynchronously. Use distribute to run async on any node in a cluster.
  - `include-user-login` (default=true): Include the current user in the service call. If you don't want to pass that in set to false. Defaults to true.
  - `transaction` (default=use-or-begin)
  - `transaction-timeout` (default=0): Defines the timeout for the transaction, in seconds. This value is only used if this service begins a transaction (either require-new, or use-or-begin and there is no other transaction already in place).
  - `ignore-error` (default=false)
  - `multi` (default=false, values=true|false|parameter)
  - `web-send-json-response` (default=false): Can be false to do nothing, true to send the service result or an expression to run on the service result to get the object to send.
  - `disable-authz` (default=false): Disables checking authorization for this service call. Ignored for async service calls.
- example (SearchServices.xml): `<service-call name="org.moqui.impl.WikiServices.get#WikiSpacePages" in-map="[wikiSpaceId:wikiSpaceId]" out-map="context"/>`

### entity-find
- uses: 1705 (in screens: 562) | group: EntityFindOperations
- doc: Like entity-and returns a list of entity values if any are found, otherwise returns an empty list. Use any combination of constraint, constraints and constraint-object.
- children: search-form-inputs, date-filter, econdition, econditions, econdition-object, having-econditions, select-field, order-by, limit-range, limit-view, use-iterator
  - `entity-name` (required): Name of entity to find instances of.
  - `list`: Name of the list to put results in. Required unless the entity-find is used under the entity-options element in a XML Screen Form.
  - `cache`: Look in the cache before finding in the datasource. The default for this comes from the cache attribute on the entity definition.
  - `for-update` (default=false): Lock the selected record so only this transaction can change it until it is ended (committed or rolled back). This does not have to be set to true in order to update the record, it just keeps other transactions from upda…
  - `distinct` (default=false): Get only distinct results, based on the combination of all fields selected. Defaults to false.
  - `use-clone` (default=false): Use a datasource clone, if one is configured
  - `offset`: Get back results starting at this offset.
  - `limit`: Get back only this many results.
- example (SearchServices.xml): `<entity-find entity-name="moqui.entity.feed.DataFeedDocument" list="dfDocList" cache="true">`

### entity-find-one
- uses: 1639 (in screens: 498) | group: EntityFindOperations
- doc: Does a find by primary key. If no value is found does nothing to the value-field.
- children: field-map, select-field
  - `entity-name` (required): Name of the entity to find an instance of.
  - `value-field` (required): Field to put result resulting EntityValue object in.
  - `auto-field-map`: If true looks for all primary key fields by name in the context. If empty defaults to true (context) unless field-map sub-element is found this will do nothing. If something other than true or false looks for fields in t…
  - `cache`: Look in the cache before finding in the datasource. The default for this comes from the cache attribute on the entity definition.
  - `for-update` (default=false): Lock the selected record so only this transaction can change it until it is ended (committed or rolled back). This does not have to be set to true in order to update the record, it just keeps other transactions from upda…
  - `use-clone` (default=false): Use a datasource clone, if one is configured
- example (SearchServices.xml): `<entity-find-one entity-name="moqui.entity.feed.DataFeed" value-field="df" cache="true"/>`

### script
- uses: 1238 (in screens: 383) | group: CallOperations
- doc: Runs the script at the specified location. You can also put a Groovy script inline under this element. If a location is specified the file can be a Groovy script, a xml-actions script, or any script setup to run through the Resource Facade. The script will run in the same context as the current operation.
  - `location`

### field-map
- uses: 1058 (in screens: 328)
- doc: A name/value pair. If from and value are empty will look in the context for a field matching the field-name.
  - `field-name` (required): Name of the entity field.
  - `from`: Name of the field (variable) in the context.
  - `value`: Literal string or use ${} syntax to expand variables.
- example (ScreenServices.xml): `<field-map field-name="screenScheduledId" from="screenScheduled.screenScheduledId"/>`

### return
- uses: 966 (in screens: 80) | group: ControlOperations
- doc: Returns immediately.
  - `message`: Adds a message to the errors list (ec.message.errors) if error=true, or the messages list (ec.message.messages) otherwise.
  - `type` (default=info)
  - `public` (default=false): If true make it a public message, not compatible with error (overrides this)
  - `error` (default=false): If true will be considered caused by an error, meaning transaction will be rolled back, etc.
- example (SmsServices.xml): `<return type="danger" message="No SMS implementation in place, not sending message"/>`

### iterate
- uses: 888 (in screens: 79) | group: ControlOperations
- doc: The operations contained by the iterate tag will be executed for each of the entries in the list, and will make the current entry available in the method environment by the entry specified. This tag can contain any of the xml-action operations, including the conditional/if operations. Any xml-action operation can be nested under the iterate tag.
- children: (any action)
  - `list` (required): The name of the field that contains the list to iterate over.
  - `entry` (required): The name of the field that will contain each entry as we iterate through the list.
  - `key`: If list points to a Map or Collection of Map.Entry the key will be put where this refers to, the value where the entry attribute refers to.
- example (SearchServices.xml): `<iterate list="allChildFileFlatList" entry="allChildFileFlat">`

### order-by
- uses: 672 (in screens: 288)
- doc: Defines a field to order the results by.
  - `field-name` (required): Name of field to order list by. May be more than one field, comma-separated. Each field name may be prefixed with +/- for ascending/descending, optionally follow by a carat (^) for case insensitive order.
- example (ShipmentInfoServices.xml): `<order-by field-name="shipmentRouteSegmentSeqId,shipmentPackageSeqId"/>`

### then
- uses: 589 (in screens: 76)
- doc: Operations to run if the corresponding condition evaluate to true.
- children: (any action)

### else
- uses: 530 (in screens: 68)
- doc: The else element can be used to contain operations that will run if the condition evaluates to false, and when under an if element when no else-if sub-conditions evaluate to true. It can contain any xml-actions operation.
- children: (any action)

### date-filter
- uses: 379 (in screens: 107)
- doc: Adds a constraint to find to filter by the from and thru dates in each record, comparing them to the valid-date value.
  - `valid-date`: The name of a field in the context to compare each value to. Defaults to now.
  - `from-field-name` (default=fromDate): The name of the entity field to use as the from/beginning effective date. Defaults to fromDate.
  - `thru-field-name` (default=thruDate): The name of the entity field to use as the thru/ending effective date. Defaults to thruDate.
  - `ignore-if-empty` (default=false): Leave out the constraint if valid-date is empty or null. Defaults to false.
  - `ignore` (default=false): Ignore the econdition (leave out of the find) if set to true or expression evaluates to true. Defaults to false.
- example (OrderBulkServices.xml): `<date-filter from-field-name="customerClassFromDate" thru-field-name="customerClassThruDate" ignore="!customerClassificationId"/>`

### log
- uses: 369 (in screens: 36) | group: OtherOperations
- doc: Logs a message using Log4J.
  - `level` (default=info, values=trace|debug|info|warn|error|off): The logging/debug level to use.
  - `message`: The message to log. Can insert variables using the ${} syntax.
- example (MoquiDefaultConf.xml): `<log level="info" message="========================== first-hit-in-visit actions"/>`

### select-field
- uses: 314 (in screens: 124)
- doc: Used to specify fields to select. If there are none of these elements all fields will be selected.
  - `field-name` (required): Name of a field to select. May be more than one field, comma-separated.
- example (ScreenServices.xml): `<select-field field-name="userId,username,emailAddress,disabled"/>`

### message
- uses: 241 (in screens: 42) | group: ControlOperations
- doc: Adds the message (sub-element text) to the ExecutionContext MessageFacade, either the errors list if error=true or the messages list otherwise.
  - `type` (default=info)
  - `public` (default=false): If true make it a public message, not compatible with error (overrides this)
  - `error` (default=false): If true will be considered caused by an error, meaning transaction will be rolled back, etc.
- example (GoogleServices.xml): `<message public="true" type="warning">`

### entity-update
- uses: 221 (in screens: 3) | group: EntityValueOperations
- doc: Updates the specified EntityValue object in the datasource. An error will result if the record is not found in the datasource.
  - `value-field` (required): The name of the field that contains the EntityValue object.
- example (LedgerServices.xml): `<entity-update value-field="glAccountOrgTimePeriod"/>`

### continue
- uses: 197 (in screens: 9) | group: ControlOperations
- doc: Continue in an iterate or while loop (will result in an error elsewhere).

### else-if
- uses: 137 (in screens: 19)
- doc: The else-if element can be used to specify alternate conditional execution blocks. Each else-if element must contain two sub-elements: condition and then. If the condition of the parent is evaluated to false, each condition of the else-if sub-elements will be evaluated, and the operations under the element corresponding to the first condition that evaluates to true will be run.
- children: condition, then, (any action)
  - `condition`: A boolean expression in Groovy. Will be AND combined with other conditions if present.
- example (UserServices.xml): `<else-if condition="userAuthcFactor.factorTypeEnumId == 'UafTotp'">`

### entity-create
- uses: 113 (in screens: 0) | group: EntityValueOperations
- doc: The create-value tag persists the specified EntityValue object by creating a new instance of the entity in the datasource. An error will result if an instance of the entity exists in the datasource with the same primary key.
  - `value-field` (required): The name of the field that contains the EntityValue object.
  - `or-update` (default=false): Update value if already exists instead of returning an error, defaults to false.
- example (LedgerServices.xml): `<entity-create value-field="glAccountOrgTimePeriod" or-update="true"/>`

### econditions
- uses: 109 (in screens: 52)
- doc: The econditions element contains a list of econditions that are combined with either and or or. The default is and. You can have econditions under econditions, for building fairly complex econdition trees, and you can also drop in econdition-objects at any point.
- children: date-filter, econdition, econditions, econdition-object
  - `combine` (default=and, values=and|or): Operator to use to combine econditions in the list.
- example (ScreenServices.xml): `<econditions combine="and">`

### entity-find-count
- uses: 93 (in screens: 48) | group: EntityFindOperations
- doc: Find the count of the number of records that match the given conditions. Conditions and other application options follow the same structure as in the entity-find operation.
- children: search-form-inputs, date-filter, econdition, econditions, econdition-object, having-econditions, select-field
  - `entity-name` (required): Name of entity to search in.
  - `count-field` (required): Name of the field (variable) to put result of the count in.
  - `cache`: Look in the cache before finding in the datasource. The default for this comes from the cache attribute on the entity definition.
  - `distinct` (default=false): Get only distinct results, based on the combination of all fields selected. Defaults to false.
- example (ScreenServices.xml): `<entity-find-count entity-name="moqui.screen.form.FormResponseAnsAndDbFormField" count-field="textDbFormFieldResponseCount">`

### break
- uses: 77 (in screens: 4) | group: ControlOperations
- doc: Break from an iterate or while loop (will result in an error elsewhere).

### filter-map-list
- uses: 70 (in screens: 36) | group: EnvOperations
- doc: Filters the given List of Maps by the field-maps specified.
- children: field-map, date-filter
  - `list` (required): The name of the field that contains a List of Map objects.
  - `to-list`: Optional name of the output list. If empty filter the input list in-place.
- example (ShipmentInfoServices.xml): `<filter-map-list list="shipmentPackageContentList" to-list="curContentList">`

### search-form-inputs
- uses: 69 (in screens: 65)
- doc: Adds econditions for the fields found in the input-fields-map. The fields and special fields with suffixes supported are the same as the *-find fields in the XML Forms. This means that you can use this to process the data from the various inputs generated by XML Forms. The suffixes include things like *_op for operators and *_ic for ignore case. For historical reference, this does basically what t…
  - `input-fields-map`: The map to get form fields from. If empty will look at the ec.web.parameters map if the web facade is available, otherwise the current context (ec.context).
  - `default-order-by`: If no orderByField parameter, order by this.
  - `skip-fields`: Comma separate list of entity field names to skip when processing input fields
  - `paginate` (default=true): Indicate if this find should set pagination options even if there are no pageSize and pageIndex parameters. Also adds a context field called "${entity-find.@list}Count" with a count of the total possible results (ie with…
  - `require-parameters` (default=false): If true only do find if there is at least one parameter
- example (PrinterList.xml): `<search-form-inputs default-order-by="serverHost,printerName"/>`

### order-map-list
- uses: 59 (in screens: 19) | group: EnvOperations
- doc: Sort a List of Maps by field names given in order-by sub-element.
- children: order-by
  - `list` (required): Name of the list to be sorted.
- example (ShipmentInfoServices.xml): `<order-map-list list="productInfo.reservedLocationInfoList">`

### entity-make-value
- uses: 34 (in screens: 0) | group: EntityValueOperations
- doc: The make-value tag uses the delegator to construct an entity value. The resulting value will not exist in the database, but will simply be assembled using the entity-name and fields map. The resulting EntityValue object will be placed in the method environment using the specified value-field.
  - `entity-name` (required): The name of the entity to construct an instance of.
  - `map`: The name of a map in the method environment that will be used for the entity fields.If the map is an EntityValue object then this will clone the value.
  - `value-field` (required): The name of the field where the EntityValue object will be put.
- example (ContactServices.xml): `<entity-make-value entity-name="mantle.facility.FacilityContactMech" value-field="newFcm" map="[facilityId:facilityId, contactMechId:newContactMech.contactMechId, fromDate:ec.user.nowTimestamp]"/>`

### entity-delete-by-condition
- uses: 31 (in screens: 1) | group: EntityValueOperations
- doc: Deletes entity values that match the econditions.
- children: date-filter, econdition, econditions, econdition-object
  - `entity-name` (required): The name of the entity to remove instances of.
- example (ScreenServices.xml): `<entity-delete-by-condition entity-name="moqui.screen.form.FormResponseAnswer">`

### entity-sequenced-id-primary
- uses: 28 (in screens: 0) | group: EntityMiscOperations
- doc: Get the next guaranteed unique seq id for this entity, and set it in the primary key field. This will set it in the first primary key field in the entity definition, but it really should be used for entities with only one primary key field.
  - `value-field` (required): The EntityValue object to work on.
- example (PaymentMethodServices.xml): `<entity-sequenced-id-primary value-field="newPaymentMethod"/>`

### entity-find-related-one
- uses: 27 (in screens: 9) | group: EntityFindOperations
- doc: Find a single value related to an existing value.
  - `value-field` (required): Name of the existing entity value in the context.
  - `relationship-name` (required): Name of the relationship to use, consists of the relationship title and the related entity name, like: ${title}${related-entity-name}.
  - `cache`: Look in the cache before finding in the datasource. The default for this comes from the cache attribute on the entity definition.
  - `for-update` (default=false): Lock the selected record so only this transaction can change it until it is ended (committed or rolled back). This does not have to be set to true in order to update the record, it just keeps other transactions from upda…
  - `to-value-field` (required): Name of field to put the entity value result in.
- example (InvoiceServices.xml): `<entity-find-related-one value-field="invoice" relationship-name="mantle.account.invoice.SettlementTerm" to-value-field="settlementTerm"/>`

### entity-set
- uses: 26 (in screens: 0) | group: EntityValueOperations
- doc: Looks for each field (pk, nonpk, or all) in the named map and if it exists there it will copy it into the named value object.
  - `value-field` (required): Field that contains an EntityValue object.
  - `map` (default=context): The name of a map in the method environment that will be used for the entity fields. Defaults to the context root, which is where incoming parameters go by default.
  - `prefix`: If not null or empty will be pre-pended to each field name (upper-casing the first letter of the field name first), and that will be used as the fields Map lookup name instead of the field-name.
  - `include` (default=all, values=pk|nonpk|all)
  - `set-if-empty` (default=false): Specifies whether or not to set fields that are null or empty. Defaults to false.
- example (ContactServices.xml): `<entity-set value-field="newPostalAddress" include="nonpk" set-if-empty="true"/>`

### econdition-object
- uses: 22 (in screens: 4)
- doc: Add a condition that has been defined elsewhere and is available in the current context. Can also be a Map and it will add conditions where the entries are ANDed together and each key/value are compared with equal.
  - `field` (required): Field in the current context that implements the EntityCondition interface or the Map interface.
- example (WikiServices.xml): `<econdition-object field="[wikiSpaceId:wikiSpaceId, userId:ec.user.userId, allowView:'Y']"/>`

### check-errors
- uses: 21 (in screens: 0) | group: ControlOperations
- doc: Checks the Message Facade error message list (ec.message.errors) and if it is not empty returns with an error, otherwise does nothing.

### having-econditions
- uses: 17 (in screens: 12)
- doc: Similar to econditions but runs after the grouping and functions are done.
- children: date-filter, econdition, econditions, econdition-object
  - `combine` (default=and, values=and|or): Operator to use to combine econditions in the list.
- example (OrderInfoServices.xml): `<having-econditions>`

### entity-delete
- uses: 16 (in screens: 0) | group: EntityValueOperations
- doc: Deletes the specified EntityValue object from the datasource. An error will result if the record is not found in the datasource.
  - `value-field` (required): The name of the field that contains the EntityValue object.
- example (UserServices.xml): `<entity-delete value-field="existingUserPasswordHistoryList.remove(0)"/>`

### while
- uses: 14 (in screens: 0) | group: IfOtherOperations
- doc: While loop operation, uses the same condition element as the if operation.
- children: condition, then, (any action)
  - `condition`: A boolean expression in Groovy. Will be AND combined with other conditions if present.
- example (UserServices.xml): `<while condition="existingUserPasswordHistoryList.size() &gt; historyLimit">`

### entity-find-related
- uses: 4 (in screens: 0) | group: EntityFindOperations
- doc: Find a list of values related to a specific value.
  - `value-field` (required): Name of the existing entity value in the context.
  - `relationship-name` (required): Name of the relationship to use, consists of the relationship title and the related entity name,like: ${title}${related-entity-name}.
  - `map`: A map containing extra constraints for the find.
  - `order-by-list`: A list of field names to order the results by.
  - `cache`: Look in the cache before finding in the datasource. The default for this comes from the cache attribute on the entity definition.
  - `for-update` (default=false): Lock the selected record so only this transaction can change it until it is ended (committed or rolled back). This does not have to be set to true in order to update the record, it just keeps other transactions from upda…
  - `list` (required): Name of the list to put the entity list result in.
- example (ShipmentServices.xml): `<entity-find-related value-field="orderPart" relationship-name="mantle.order.OrderItem" list="orderItemList" order-by-list="['orderItemSeqId']"/>`

### entity-sequenced-id-secondary
- uses: 4 (in screens: 0) | group: EntityMiscOperations
- doc: Given an entity value object with all primary key fields except one already set will generate an ID for the remaining primary key field by looking at all records with the partial primary key and then adding increment-by to the highest value.
  - `value-field` (required): The EntityValue object to work on.
- example (PaymentAutoPostServices.xml): `<entity-sequenced-id-secondary value-field="acctgTransEntry"/>`

### entity-delete-related
- uses: 2 (in screens: 2) | group: EntityValueOperations
- doc: Given a value-field and a relationship-name, follows the relationship and deletes all related records. For a type one relationship it will remove a single record if it exists, and for a type many relationship it will remove all the records that are related to it. Instead of using cascading deletes you should have your code delete all related data with foreign keys pointing the the value-field reco…
  - `value-field` (required): Field that contains an EntityValue object to delete related records from.
  - `relationship-name` (required): Name of a relationship to use to delete related records.
- example (EditDbView.xml): `<entity-delete-related value-field="dbViewEntity" relationship-name="moqui.entity.view.DbViewEntityAlias"/>`

### actions
- uses: 1 (in screens: 0)
- doc: XML Actions can be embedded in various files, or put in a file of their own and run like a script. Like a script the parameters passed into the XML Actions will already be defined in the context.
- children: (any action)

### and
- uses: 0 (in screens: 0) | group: IfCombineConditions
- doc: To be true all of the conditions underneath need to be true. Will return false as soon as a condition evaluates to false, not evaluating remaining conditions. If no conditions evaluate to false will return true.

### assert
- uses: 0 (in screens: 0) | group: IfOtherOperations
- doc: Each condition under the assert element will be checked and if it fails an error will be added to the given error list. Note that while the definitions for the if operation is used, the tags should be empty because of the differing semantics. This is mainly used for testing, and for writing xml-actions that are meant to be used as part of a test suite. This is mostly useful for testing because the…
  - `title`: A title that can be used in reports for testing.

### compare
- uses: 0 (in screens: 0) | group: IfBasicOperations
- doc: The operations contained by the if-compare tag will only be executed if the comparison returns true. This tag can contain any of the xml-action operations, including the conditional/if operations.
- children: else, (any action)
  - `field` (required): The name of the field in the context (environment) that will be compared.
  - `operator` (default=equals)
  - `value`: The value that the field will compared to. Will evaluate to a String but can be converted to other types.
  - `to-field`: The name of the context field that the main field will be compared to. If left empty will default to the field attribute's value.
  - `format`: Format string based on the type of the object (date, number, etc).
  - `type` (default=Object)

### condition
- uses: 0 (in screens: 0)
- doc: Contains a single condition of any sort and evaluates to a boolean value. To combine the other if operations the and, or, and xor elements can be used.

### entity-data
- uses: 0 (in screens: 0) | group: EntityMiscOperations
- doc: Load or assert each record in an entity-facade-xml file.
  - `location` (required): Location of an XML file to load in database or verify in assert mode.
  - `timeout` (default=-1): Start a new transaction and load the data with a longer timeout.
  - `mode` (default=load, values=load|assert)

### expression
- uses: 0 (in screens: 0) | group: IfBasicOperations
- doc: A boolean expression should be inline under this element (to avoid problems with character encoding, etc). When not under a condition element any xml-action operation can be nested under this tag, and will only be run if it evaluates to true.

### limit-range
- uses: 0 (in screens: 0)
- doc: Limit the results by a start index and a size.
  - `start` (required): The start/beginning index of results to include.
  - `size` (required): The number of results to include beyond the start.

### limit-view
- uses: 0 (in screens: 0)
- doc: Limit the results using parameters like those used to paginate results in a user interface.
  - `view-index` (required): Index of records to view, depends on view-size.
  - `view-size` (required): Number of records to view, like the number of results per-screen.

### not
- uses: 0 (in screens: 0) | group: IfCombineConditions
- doc: Can only have one condition underneath and simply reverse the boolean value of this condition.

### or
- uses: 0 (in screens: 0) | group: IfCombineConditions
- doc: To be true just one of the conditions underneath needs to be true. Will return true as soon as a condition is true, not evaluating remaining conditions.

### use-iterator
- uses: 0 (in screens: 0)
- doc: Specifies whether or not to use the EntityListIterator when doing the query. This is much more efficient for large data sets because the results are read incrementally instead of all at once. Note that when using this the use-cache setting will be ignored. Also note that an EntityListIterator must be closed when you are finished, but this is done automatically by the iterate operation. Must be tru…

