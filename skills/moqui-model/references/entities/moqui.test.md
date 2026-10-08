# moqui.test

One line per entity. E = entity, V = view-entity. Generated; do not edit.

- E moqui.test.Bar | src: moqui-framework | pk: barId | fields: fooId:id, barRank:number-integer, score:number-decimal | rels: 
- E moqui.test.Foo | src: moqui-framework | pk: fooId | fields: fooText:text-medium | rels: 
- E moqui.test.TestEntity | src: moqui-framework | pk: testId | fields: testMedium:text-medium, value:text-short, testLong:text-long, testIndicator:text-indicator, testDate:date, testDateTime:date-time, testTime:time, testNumberInteger:number-integer, testNumberDecimal:number-decimal, testNumberFloat:number-float, testCurrencyAmount:currency-amount, testCurrencyPrecise:currency-precise | rels: 
- E moqui.test.TestFts | src: moqui-framework | pk: testFtsId | fields: note:text-medium, body:text-fts | rels: 
- E moqui.test.TestIntPk | src: moqui-framework | pk: intId | fields: testMedium:text-medium | rels: 
- E moqui.test.TestNoSqlEntity | src: moqui-framework | pk: testId | fields: testMedium:text-medium, testLong:text-long, testIndicator:text-indicator, testDate:date, testDateTime:date-time, testTime:time, testNumberInteger:number-integer, testNumberDecimal:number-decimal, testNumberFloat:number-float, testCurrencyAmount:currency-amount, testCurrencyPrecise:currency-precise | rels: 
- V moqui.test.FooBar | src: moqui-framework | members: T1=Foo, T2=Bar? | alias-all: T1 | aliases: score, barRank
