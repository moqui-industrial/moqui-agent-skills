# SECA and EECA rules (generated)

Before calling a service or writing an entity, look it up here: these rules run automatically.
Calls marked (async) are skipped in simulation and run later in a separate transaction.

## SECAs by service (60 rules on 24 services)

### create#mantle.account.financial.FinancialAccountTrans
- when=post-service id=FinancialAccountTransGlPost | calls: mantle.ledger.OtherAutoPostServices.post#FinancialAccountTrans | AccountingLedger.secas.xml
### create#mantle.account.invoice.InvoiceItem
- when=post-service id=InvoiceAdjustGlPost | if: isAdjustment == 'Y' | calls: mantle.ledger.InvoiceAutoPostServices.post#InvoiceAdjustment | AccountingLedger.secas.xml
### create#mantle.account.payment.PaymentApplication
- when=post-service id=PaymentApplicationGlPost | calls: mantle.ledger.PaymentAutoPostServices.post#PaymentApplication | AccountingLedger.secas.xml
### create#mantle.order.OrderItem
- when=post-service id=OrderItemCreateCheckReserve | calls: mantle.product.AssetServices.checkReserve#AssetForOrderItem | ProductAsset.secas.xml
### create#mantle.product.asset.AssetDetail
- when=post-service id=AssetDetailPhysicalVarianceGlPost | calls: mantle.ledger.AssetAutoPostServices.post#PhysicalInventoryVariance | AccountingLedger.secas.xml
### create#mantle.product.issuance.AssetIssuance
- when=post-service id=AssetIssuanceGlPost | calls: mantle.ledger.AssetAutoPostServices.post#AssetIssuance | AccountingLedger.secas.xml
### create#mantle.product.receipt.AssetReceipt
- when=post-service id=AssetReceiptGlPost | calls: mantle.ledger.AssetAutoPostServices.post#AssetReceipt | AccountingLedger.secas.xml
### delete#mantle.account.financial.FinancialAccountAuth
- when=post-service id=FinancialAccountAuthDeleteCalcTotals | calls: mantle.account.FinancialAccountServices.calculate#FinancialAccountTotals | AccountingFinancial.secas.xml
### org.moqui.impl.UserServices.create#InitialAdminAccount
- when=post-service id=UserInitialAdminCreatePerson | if: userId && !partyId | calls: mantle.party.PartyServices.create#UserAccountPerson | Party.secas.xml
### org.moqui.impl.UserServices.create#UserAccount
- when=post-service id=UserAccountCreatePerson | if: userId && !partyId | calls: mantle.party.PartyServices.create#UserAccountPerson | Party.secas.xml
### update#mantle.account.financial.FinancialAccountAuth
- when=post-service id=FinancialAccountAuthUpdateCalcTotals | calls: mantle.account.FinancialAccountServices.calculate#FinancialAccountTotals | AccountingFinancial.secas.xml
### update#mantle.account.invoice.Invoice
- when=post-service id=InvoiceCreateFinAccountTx | if: statusChanged && (statusId == 'InvoiceFinalized' || statusId == 'InvoiceApproved') | calls: mantle.account.FinancialAccountServices.checkCreate#InvoiceTransactions | AccountingFinancial.secas.xml
- when=post-service id=InvoiceCancelReverseFinAccountTx | if: statusChanged && statusId == 'InvoiceCancelled' | calls: mantle.account.FinancialAccountServices.reverse#InvoiceTransactions | AccountingFinancial.secas.xml
- when=post-service id=InvoiceResumeChangesReverseFinAccountTx | if: statusChanged && ( (oldStatusId in ['InvoiceFinalized', 'InvoiceSent'] && statusId == 'InvoiceInProcess') || (oldStatusId == 'InvoiceApprove… | calls: mantle.account.FinancialAccountServices.reverse#InvoiceTransactions | AccountingFinancial.secas.xml
- when=post-service id=InvoiceCheckNegativeTotalMarkPaid | if: statusChanged && (statusId == 'InvoiceFinalized' || statusId == 'InvoiceApproved') | calls: mantle.account.InvoiceServices.get#InvoiceTotal, update#mantle.account.invoice.Invoice | AccountingInvoice.secas.xml
- when=post-service id=InvoiceCheckFullyPaid | if: statusChanged && statusId in ['InvoicePmtRecvd', 'InvoicePmtSent'] | calls: mantle.account.InvoiceServices.get#InvoiceTotal | AccountingInvoice.secas.xml
- when=post-service id=InvoiceApplyForPayments | if: statusChanged && (statusId == 'InvoiceFinalized' || statusId == 'InvoiceApproved') | calls: mantle.account.PaymentServices.apply#InvoiceForPayments | AccountingInvoice.secas.xml
- when=post-service id=InvoiceCancelledCleanup | if: statusChanged && statusId == 'InvoiceCancelled' | calls: mantle.account.InvoiceServices.cancel#Invoice | AccountingInvoice.secas.xml
- when=post-service id=InvoiceUnPayByStatus | if: statusChanged && oldStatusId in ['InvoicePmtRecvd', 'InvoicePmtSent'] && statusId in ['InvoiceFinalized', 'InvoiceApproved'] | calls: mantle.account.InvoiceServices.unpay#Invoice | AccountingInvoice.secas.xml
- when=tx-commit id=InvoiceFinalizedSendEmail | if: statusChanged && statusId == 'InvoiceFinalized' && oldStatusId == 'InvoiceInProcess' | calls: mantle.account.InvoiceServices.send#InvoiceStoreEmail | AccountingInvoice.secas.xml
- when=post-service id=InvoiceGlPost | if: statusChanged && (statusId == 'InvoiceFinalized' || statusId == 'InvoiceApproved') | calls: mantle.ledger.InvoiceAutoPostServices.post#Invoice | AccountingLedger.secas.xml
- when=post-service id=InvoiceCancelRevertGlPost | if: statusChanged && statusId == 'InvoiceCancelled' | calls: mantle.ledger.InvoiceAutoPostServices.revert#InvoicePost | AccountingLedger.secas.xml
- when=post-service id=InvoiceResumeChangeRevertGlPost | if: statusChanged && ( (oldStatusId in ['InvoiceFinalized', 'InvoiceSent'] && statusId == 'InvoiceInProcess') || (oldStatusId == 'InvoiceApprove… | calls: mantle.ledger.InvoiceAutoPostServices.revert#InvoicePost | AccountingLedger.secas.xml
### update#mantle.account.invoice.InvoiceItem
- when=post-service id=InvoiceAdjustUpdateGlPost | calls: mantle.ledger.InvoiceAutoPostServices.repost#InvoiceAdjustment | AccountingLedger.secas.xml
### update#mantle.account.payment.Payment
- when=post-service id=PaymentCreateFinAccountTx | if: statusChanged && statusId == 'PmntDelivered' && oldStatusId != 'PmntConfirmed' | calls: mantle.account.FinancialAccountServices.checkCreate#PaymentTrans | AccountingFinancial.secas.xml
- when=post-service id=PaymentReverseFinAccountTx | if: statusChanged && ((statusId in ['PmntCancelled', 'PmntVoid']) || (oldStatusId == 'PmntDelivered' && statusId in ['PmntPromised', 'PmntAuthor… | calls: mantle.account.FinancialAccountServices.reverse#PaymentTrans | AccountingFinancial.secas.xml
- when=post-service id=PaymentGlPost | if: statusChanged && statusId == 'PmntDelivered' && oldStatusId != 'PmntConfirmed' | calls: mantle.ledger.PaymentAutoPostServices.post#Payment | AccountingLedger.secas.xml
- when=post-service id=PaymentCancelRevertGlPost | if: statusChanged && (statusId in ['PmntCancelled', 'PmntVoid']) | calls: mantle.ledger.PaymentAutoPostServices.revert#PaymentPost | AccountingLedger.secas.xml
- when=post-service id=PaymentUndeliverReverGlPost | if: statusChanged && oldStatusId == 'PmntDelivered' && statusId in ['PmntPromised', 'PmntAuthorized'] | calls: mantle.ledger.PaymentAutoPostServices.revert#PaymentPost | AccountingLedger.secas.xml
- when=post-service id=PaymentCheckEffectiveDate | if: statusChanged && statusId == 'PmntDelivered' | AccountingPayment.secas.xml
- when=post-service id=PaymentApplyForInvoice | if: statusChanged && (statusId in ['PmntDelivered', 'PmntConfirmed']) | calls: mantle.account.PaymentServices.apply#PaymentForInvoice | AccountingPayment.secas.xml
- when=post-service id=PaymentCancelledCleanup | if: statusChanged && (statusId in ['PmntCancelled', 'PmntVoid']) | calls: mantle.account.PaymentServices.void#Payment | AccountingPayment.secas.xml
- when=post-service id=PaymentUnDeliverCleanup | if: statusChanged && oldStatusId == 'PmntDelivered' && statusId in ['PmntPromised', 'PmntAuthorized'] | calls: mantle.account.PaymentServices.void#Payment | AccountingPayment.secas.xml
- when=post-service id=PaymentCancelClearMethodTrans | if: statusChanged && (statusId in ['PmntCancelled', 'PmntVoid']) | calls: mantle.account.ReconciliationServices.clear#PaymentTrans | AccountingPayment.secas.xml
- when=post-service id=PaymentAutoThruDate | if: statusChanged && !(statusId in ['PmntProposed', 'PmntPromised', 'PmntAuthorized', 'PmntDeclined']) | calls: mantle.account.PaymentMethodServices.checkDelete#PaymentPaymentMethods | AccountingPayment.secas.xml
### update#mantle.account.payment.PaymentApplication
- when=post-service id=PaymentApplicationRevertGlPost | if: amountApplied == 0.0 | calls: mantle.ledger.PaymentAutoPostServices.revert#PaymentApplicationPost | AccountingLedger.secas.xml
### update#mantle.order.OrderHeader
- when=post-service id=OrderPlacedAuthorizePayments | if: statusChanged && statusId == 'OrderPlaced' | calls: mantle.account.PaymentServices.authorize#OrderPayments | AccountingPayment.secas.xml
- when=tx-commit id=OrderPlacedSendEmail | if: statusChanged && statusId == 'OrderPlaced' | calls: mantle.order.OrderInfoServices.send#OrderStoreEmail | OrderReturn.secas.xml
- when=tx-commit id=OrderApprovedSendEmail | if: statusChanged && statusId == 'OrderApproved' | calls: mantle.order.OrderInfoServices.send#OrderStoreEmail | OrderReturn.secas.xml
- when=post-service id=OrderPlacedAutoApprove | if: statusChanged && statusId == 'OrderPlaced' | calls: mantle.order.OrderServices.autoApprove#Order | OrderReturn.secas.xml
- when=post-service id=OrderPlacedReserveAssets | if: statusChanged && statusId == 'OrderPlaced' | calls: mantle.product.AssetServices.reserve#AssetsForOrder | ProductAsset.secas.xml
- when=post-service id=OrderApprovedReserveAssets | if: statusChanged && statusId == 'OrderApproved' | calls: mantle.product.AssetServices.reserve#AssetsForOrder | ProductAsset.secas.xml
- when=post-service id=OrderApprovedFulfillSubscriptions | if: statusChanged && statusId == 'OrderApproved' | calls: mantle.product.SubscriptionServices.fulfill#OrderSubscriptions | ProductSubscription.secas.xml
### update#mantle.order.OrderItem
- when=post-service id=OrderItemUpdateCheckReserve | calls: mantle.product.AssetServices.checkReserve#AssetForOrderItem | ProductAsset.secas.xml
### update#mantle.order.OrderPart
- when=tx-commit id=OrderApprovedNotify | if: statusChanged && statusId == 'OrderApproved' | calls: mantle.order.OrderInfoServices.notify#OrderHighPriority | OrderReturn.secas.xml
### update#mantle.order.return.ReturnHeader
- when=post-service id=ReturnApprovedProcess | if: statusChanged && statusId == 'ReturnApproved' | calls: mantle.order.ReturnServices.create#ReturnShipment, mantle.order.ReturnServices.process#ReturnItemResponses | OrderReturn.secas.xml
- when=post-service id=ReturnReceivedProcess | if: statusChanged && statusId == 'ReturnReceived' | calls: mantle.order.ReturnServices.process#ReturnItemResponses | OrderReturn.secas.xml
### update#mantle.product.asset.Asset
- when=post-service id=AssetStatusAvailableReservations | if: statusChanged && statusId == 'AstAvailable' | calls: mantle.product.AssetServices.reserve#IncreasedAsset | ProductAsset.secas.xml
- when=post-service id=AssetStatusNotAvailableReservations | if: statusChanged && oldStatusId == 'AstAvailable' | calls: mantle.product.AssetServices.check#AssetReservations | ProductAsset.secas.xml
### update#mantle.product.issuance.AssetIssuance
- when=post-service id=AssetIssuanceGlRePost | calls: mantle.ledger.AssetAutoPostServices.repost#AssetIssuance | AccountingLedger.secas.xml
### update#mantle.shipment.Shipment
- when=post-service id=ShipmentOutgoingPackedCreateInvoices | if: statusChanged && statusId == 'ShipPacked' && !(oldStatusId in ['ShipShipped', 'ShipDelivered']) | calls: mantle.account.InvoiceServices.create#SalesShipmentInvoices | AccountingInvoice.secas.xml
- when=post-service id=ShipmentIncomingDeliveredCreateInvoices | if: statusChanged && statusId == 'ShipDelivered' | calls: mantle.account.InvoiceServices.create#PurchaseShipmentInvoices | AccountingInvoice.secas.xml
- when=post-service id=ShipmentDeliveredReturnReceive | if: statusChanged && statusId == 'ShipDelivered' | calls: mantle.order.ReturnServices.receive#ReturnShipmentItems | OrderReturn.secas.xml
- when=tx-commit id=ShipmentShippedSendEmail | if: statusChanged && statusId == 'ShipShipped' | calls: mantle.shipment.ShipmentServices.send#ShipmentStoreEmail | Shipment.secas.xml
- when=tx-commit id=ShipmentDeliveredSentEmail | if: statusChanged && statusId == 'ShipDelivered' | calls: mantle.shipment.ShipmentServices.send#ShipmentStoreEmail | Shipment.secas.xml
- when=post-service id=WorkEffortShipLoadStatusAuto | if: statusChanged && (statusId in ['ShipPicked', 'ShipPacked', 'ShipShipped', 'ShipCancelled'] || oldStatusId in ['ShipPicked', 'ShipPacked', 'S… | calls: mantle.work.ShipmentWorkServices.set#ShipmentLoadStatusOnShipmentStatus | WorkEffort.secas.xml
### update#mantle.shipment.ShipmentPackageRouteSeg
- when=post-service id=ShipmentPackageDeliveredCheckShipment | if: trackingStatusEnumId == 'ShTsDelivered' | calls: mantle.shipment.ShipmentServices.checkSet#ShipmentDeliveredByPackages | Shipment.secas.xml
### update#mantle.work.effort.WorkEffort
- when=post-service id=OrderItemWorkEffortCheckComplete | if: statusChanged && statusId in ['WeComplete', 'WeClosed', 'WeCancelled'] | calls: mantle.order.OrderServices.checkComplete#OrderPart | OrderReturn.secas.xml
- when=post-service id=WorkEffortStartCompleteDates | if: statusChanged && statusId in ['WeInProgress', 'WeComplete'] | WorkEffort.secas.xml
- when=pre-validate id=WorkEffortShipLoadStatusCheck | if: workEffortId && statusId in ['WeComplete', 'WeClosed', 'WeCancelled'] | calls: mantle.work.ShipmentWorkServices.check#ShipmentLoadStatusChange | WorkEffort.secas.xml

## EECAs by entity (27 rules on 25 entities)

### mantle.account.invoice.Invoice
- on=create,update id=InvoiceSetDueDate | calls: mantle.account.InvoiceServices.checkSet#InvoiceDueDate | Accounting.eecas.xml
### mantle.account.invoice.InvoiceItem
- on=create,update,delete id=InvoiceItemUpdateInvoiceTotals | calls: mantle.account.InvoiceServices.update#InvoiceTotals | Accounting.eecas.xml
### mantle.account.payment.Payment
- on=create,update id=PaymentUpdateTotals run-before | Accounting.eecas.xml
### mantle.account.payment.PaymentApplication
- on=create,update,delete id=PaymentApplicationUpdateInvoiceTotals | if: invoiceId || toInvoiceId | calls: mantle.account.InvoiceServices.update#InvoiceTotals, mantle.account.InvoiceServices.update#InvoiceTotals | Accounting.eecas.xml
- on=create,update,delete id=PaymentApplicationUpdatePaymentTotals | if: paymentId || toPaymentId | calls: mantle.account.PaymentServices.update#PaymentTotals, mantle.account.PaymentServices.update#PaymentTotals | Accounting.eecas.xml
### mantle.ledger.account.GlAccount
- on=create,update id=GlAccountSetFlags run-before | calls: mantle.ledger.LedgerServices.set#GlAccountFlags | Accounting.eecas.xml
### mantle.order.OrderContent
- on=create,update,delete id=OrderContentRevision | calls: mantle.order.OrderServices.increment#OrderRevision | Order.eecas.xml
### mantle.order.OrderItem
- on=create,update,delete id=OrderItemHandleChange get-original-value | calls: mantle.order.OrderServices.handle#OrderItemChange | Order.eecas.xml
### mantle.order.OrderNote
- on=create,update,delete id=OrderNoteRevision | calls: mantle.order.OrderServices.increment#OrderRevision | Order.eecas.xml
### mantle.order.OrderPart
- on=update id=OrderPartHandleChange get-original-value | calls: mantle.order.OrderServices.handle#OrderPartChange | Order.eecas.xml
### mantle.order.OrderPartContactMech
- on=create,update,delete id=OrderPartContactMechRevision | calls: mantle.order.OrderServices.increment#OrderRevision | Order.eecas.xml
### mantle.order.OrderPartParty
- on=create,update,delete id=OrderPartPartyRevision | calls: mantle.order.OrderServices.increment#OrderRevision | Order.eecas.xml
### mantle.order.OrderPartTerm
- on=create,update,delete id=OrderPartTermRevision | calls: mantle.order.OrderServices.increment#OrderRevision | Order.eecas.xml
### mantle.product.asset.Asset
- on=create,update id=AssetLocationFromContainer run-before | if: containerId | ProductAsset.eecas.xml
### mantle.product.asset.AssetDetail
- on=create id=AssetDetailUpdateAsset | calls: mantle.product.AssetServices.update#AssetFromDetail | ProductAsset.eecas.xml
### mantle.product.asset.Container
- on=update id=ContainerAssetLocation | ProductAsset.eecas.xml
### mantle.work.effort.WorkEffort
- on=create,update,delete id=WorkEffortUpdateProject | if: rootWorkEffortId != null && workEffortTypeEnumId == 'WetTask' | calls: mantle.work.TaskServices.update#ProjectTimeFromTask | Work.eecas.xml
- on=create,update id=WorkEffortTaskDefault run-before | if: workEffortTypeEnumId == 'WetTask' | calls: mantle.work.TaskServices.set#TaskDefaults | Work.eecas.xml
### mantle.work.time.TimeEntry
- on=create,update,delete id=TimeEntryUpdateTask | if: workEffortId | calls: mantle.work.TaskServices.update#TaskFromTime | Work.eecas.xml
### moqui.screen.form.DbForm
- on=create,update,delete id=DbFormCache | Screen.eecas.xml
### moqui.screen.form.DbFormField
- on=create,update,delete id=DbFormFieldCache | Screen.eecas.xml
### moqui.screen.form.DbFormFieldEntOpts
- on=create,update,delete id=DbFormFieldEntOptsCache | Screen.eecas.xml
### moqui.screen.form.DbFormFieldEntOptsCond
- on=create,update,delete id=DbFormFieldEntOptsCondCache | Screen.eecas.xml
### moqui.screen.form.DbFormFieldEntOptsOrder
- on=create,update,delete id=DbFormFieldEntOptsOrderCache | Screen.eecas.xml
### moqui.screen.form.DbFormFieldOption
- on=create,update,delete id=DbFormFieldOptionCache | Screen.eecas.xml
### moqui.security.UserGroupMember
- on=create,update,delete id=UserGroupMemberPrivileged run-before | Security.eecas.xml
### moqui.security.UserGroupPermission
- on=create,update,delete id=UserGroupPermissionSealed run-before | Security.eecas.xml
