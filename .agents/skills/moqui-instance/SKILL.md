---
name: moqui-instance
description: Provisioning and lifecycle of application instances from inside Moqui with the moqui.server.instance entities and org.moqui.impl.InstanceServices — container hosts, images, databases created per instance, environment, links, volumes, and the init/start/stop/remove/check services — plus how to extend it to other orchestrators (Swarm, Kubernetes) and build scaling or per-customer SaaS provisioning on top of it. Use this skill whenever the task is to create, start, stop, check or remove a Moqui or other containerized instance, give a customer its own instance, tie a subscription to a running instance, or automate capacity.
---

# moqui-instance: application instances managed by Moqui

Moqui can manage the containers it runs in, and others, as data plus services. An instance is a record (`AppInstance`) that says which image runs on which host with which database and settings; services turn that record into a running container and a ready database, and back. Configuration is data (`moqui-data`); `assets/InstanceSetupData.xml` passes `check_data.py`. The tools screens under `System/Instance` (InstanceList, InstanceDetail) are the manual console over the same entities and services.

## Model (`moqui.server.instance`, framework `ServerEntities.xml`)

| Entity | Role |
| --- | --- |
| `InstanceHostType` | A kind of host and **the names of the services** that implement it: `initService`, `startService`, `stopService`, `removeService`, `checkService`. Seed: `docker` with the `*#InstanceDocker` services |
| `InstanceHost` | One host of that type: protocol, address, admin port, credentials (password encrypted). Seed: `LocalDocker` on 127.0.0.1:2375 |
| `InstanceImageType` (+ `Env`, `Link`, `Volume`, `HostConfig`) | Defaults for a kind of image. Seed: `moqui`, whose env sets `VIRTUAL_HOST`, the HTTP host and ports, and the datasource (`entity_ds_*`) from the instance and its database, with a random database password, and links `moqui-database` |
| `InstanceImage` | A concrete image: name, registry, credentials, image type, host type |
| `DatabaseType` | A kind of database server and the names of its `createService` and `checkService`. Seed: `postgres`, `mysql` |
| `DatabaseHost` | One database server: address, port, the address instances use, admin user and password (encrypted) |
| `AppInstance` (+ `Env`, `Link`, `Volume`, `HostConfig`) | One instance: image, host, database host, `hostName`, `instanceName`, `instanceUuid` (filled by init), `initCommand`, `networkMode`, `jsonConfig`, and per-instance overrides of the image type defaults |

## Services (`org.moqui.impl.InstanceServices`)

- **`provision#AppInstance`** does the whole job: `create#AppDatabase`, then `init#AppInstance`, then `start#AppInstance`. It returns what happened (`databaseCreated`, `userCreated`, `instanceCreated`, `instanceStarted`, `instanceRunning`, `instanceUuid`).
- **Lifecycle:** `init#AppInstance`, `start#AppInstance`, `stop#AppInstance`, `remove#AppInstance`, `check#AppInstance`, `check#AppInstanceAndDatabase`, and `check#MoquiServer` for the application inside.
- **Dispatch to the host type:** the generic `init#Instance`, `start#Instance`, `stop#Instance`, `remove#Instance`, `check#Instance` call the service named on the instance's `InstanceHostType`. The Docker implementation (`init#InstanceDocker`...) calls the Docker Engine API with RestClient: it creates the container with the image, the merged environment, links, binds and network mode, then starts, stops, inspects or removes it. `get#DockerStatus` and `get#DockerLog` read state and logs.
- **Databases:** `create#AppDatabase` and `check#AppDatabase` call the `DatabaseType` services. `create#DatabasePostgres` connects with the admin account, creates the database and the user with the generated password, and grants access; MySQL is equivalent.

## Extending to Swarm, Kubernetes or a cloud API

The host type is the extension point. To run instances as Swarm services or Kubernetes deployments, add an `InstanceHostType` (for example `swarm` or `k8s`) whose five service names point to your own services with the same contracts as the Docker ones. Those services translate the instance record into a service or deployment spec and call the orchestrator's API. Images, databases, environment and the rest of the model stay the same.

## Scaling and SaaS on top

The framework services manage instances one at a time and contain no load-based scaling policy. A scaling loop is built on top of them:

1. A `ServiceJob` reads load: `check#AppInstance` and `get#DockerStatus`, application metrics, or `Measurement` rows.
2. It compares the load with limits, which can come from agreement thresholds (`moqui-agreement`).
3. It calls `provision#AppInstance` for new instances, `stop#AppInstance` or `remove#AppInstance` for idle ones, recording each decision.

Per-customer SaaS uses Mantle's subscriptions. A `SubscriptionResource` names services for init, renew, revoke, restore and destroy. An init service that creates the `AppInstance` and calls `provision#AppInstance`, storing the instance id in `Subscription.resourceInstanceId`, gives every subscriber its own instance; the revoke and destroy services stop and remove it.

## Rules

- **The Docker admin port is root on the host.** The seed `LocalDocker` uses plain HTTP on 2375; in any real setup use TLS (2376) or a socket proxy that allows only the calls these services make, and keep the host credentials in secrets.
- **Environment values are expressions.** Image type envs such as `${appInstance.hostName}` are evaluated as Groovy templates. Never put user input into env values unchecked.
- **Database admin credentials are the keys to every tenant.** Keep `DatabaseHost.adminPassword` out of data files in version control and restrict who can run the provisioning services.
- **One instance per tenant is isolation, not authorization.** Inside each instance, Moqui's normal security applies; a request to provision for a customer should itself be a Request with an approval, like any change.
