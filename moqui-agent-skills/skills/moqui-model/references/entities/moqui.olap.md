# moqui.olap

One line per entity. E = entity, V = view-entity. Generated; do not edit.

- E moqui.olap.CurrencyDimension | src: moqui-framework | pk: dimensionId | fields: currencyId:id, description:text-medium | rels: 
- E moqui.olap.DateDayDimension | src: moqui-framework | pk: dimensionId | fields: dateValue:date, description:text-medium, dayName:text-medium, dayOfMonth:number-integer, dayOfYear:number-integer, monthName:text-medium, monthOfYear:number-integer, yearName:number-integer, weekOfMonth:number-integer, weekOfYear:number-integer, yearMonthDay:text-medium, yearAndMonth:text-medium, isWeekEnd:text-indicator | rels: 
