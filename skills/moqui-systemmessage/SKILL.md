---
name: moqui-systemmessage
description: Stateful data exchange between Moqui and external systems with SystemMessage — outgoing and incoming messages with a status lifecycle, retries, acknowledgements, remote endpoints, links to business records, and the send/receive/consume service contracts. Use this skill whenever Moqui must send data to or receive data from another system (partner, bank, carrier, marketplace, MES, PLC gateway, another Moqui instance) by REST, JSON-RPC, SFTP or files, or when an integration must not lose or duplicate messages.
---

# moqui-systemmessage: integration with a state machine

A SystemMessage is a record of one message to or from another system, with its full text, its direction and a status that moves through a defined flow. Integrations built on it survive restarts and remote outages: messages are stored first, then sent or consumed, retried by jobs and kept for audit. Configuration is data (`moqui-data`); producing and consuming are services (`moqui-actions`).

## Model

Entities in `moqui.service.message` (framework `ServiceEntities.xml`):

| Entity | Role |
| --- | --- |
| `SystemMessage` | One message: `systemMessageTypeId`, `systemMessageRemoteId`, `isOutgoing`, `statusId` (audited), `messageText`, `initDate`/`processedDate`, `failCount`, `parentMessageId` (split), `ackMessageId`, `remoteMessageId`, and EDI/OAGIS header fields |
| `SystemMessageType` | What the message is and which services handle it: `sendServiceName`, `receiveServiceName`, `consumeServiceName`, `produceAckServiceName`, `contentType`, file paths for SFTP |
| `SystemMessageRemote` | The other system: `sendUrl`, `receiveUrl`, credentials (password stored encrypted), `sendServiceName` override |
| `SystemMessageError` | Errors per message |
| `SystemMessageEnumMap` | Maps internal enumerations to the remote system's codes |

Mantle extends `SystemMessage` with business keys (`orderId` and `orderPartSeqId`, `invoiceId`, `shipmentId`, `returnId`, `paymentMethodFileId`...), so each message is linked to the record it is about.

## Lifecycle

Outgoing: `SmsgProduced → SmsgSending → SmsgSent → SmsgConfirmed` (or `SmsgRejected`).
Incoming: `SmsgReceived → SmsgConsuming → SmsgConsumed → SmsgConfirmed` (or `SmsgRejected`).
Any step can go to `SmsgError` and back to retry; `SmsgCancelled` stops a message. The full transition list is in `moqui-model`'s `status.md` under `SystemMessage`.

## Services (`org.moqui.impl.SystemMessageServices`)

- **`queue#SystemMessage`**: creates an outgoing message in `SmsgProduced` in its own transaction and, with `sendNow` (default), sends it asynchronously. Its in-parameters include every `SystemMessage` field, so business keys such as `orderId` go straight in.
- **Senders** implementing `send#SystemMessage`: `send#SystemMessageRest`, `send#SystemMessageJsonRpc`, `send#SystemMessageDirectLocal`, plus SFTP in a separate component (`org.moqui.sftp.SftpMessageServices.send#SystemMessageSftp`, used by Mantle's banking files).
- **`receive#IncomingSystemMessage`**: saves an incoming message and then calls the type's consume service asynchronously. It is the remote entry point (`allow-remote="true"`).
- **Your consume service** implements `consume#SystemMessage`: it receives `systemMessageId`, reads the message, applies it, and returns an error to leave the message in error for retry.
- **Retry jobs**: `send#AllProducedSystemMessages` and `consume#AllReceivedSystemMessages`, scheduled every 15 minutes in `MoquiSetupData.xml` but shipped paused. Enable them (jobs `send_AllProducedSystemMessages_frequent` and `consume_AllReceivedSystemMessages_frequent`) wherever messages must not be lost. **`reset#SystemMessageInError`** puts failed messages back in the queue.

## Templates

- `assets/IntegrationSetupData.xml`: a remote endpoint, an outgoing type sent by REST, an incoming type with its consume service, and the retry jobs enabled. It passes `check_data.py`.
- `assets/PartnerServices.xml`: a service that builds a JSON payload from an order and queues it with `orderId`, and a consume service that reads a shipment notice and applies it through Mantle's `ship#Shipment`. It passes `check_artifact.py` and the XSD.

## Rules

- **Queue inside the business transaction.** The message is then produced only if the business change commits; sending happens after, asynchronously.
- **Make consume idempotent.** Retries and duplicates from the remote side happen: check `remoteMessageId` or the business state before applying a change.
- **Apply incoming changes through services**, never by writing entities directly: the status checks and SECAs must run as for a user action.
- **Store the business key on the message** (`orderId`, `shipmentId`...) so every exchange can be traced from the record and back.
- **Asynchronous parts do not run in simulation.** Sending and consuming are async and are skipped in the TransactionCacheDb overlay. Test them against a stub remote, not in SIM.
