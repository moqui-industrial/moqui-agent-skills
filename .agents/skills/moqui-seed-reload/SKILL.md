---
name: moqui-seed-reload
description: Load generated or changed seed data files into a test Moqui instance and prove they arrived — stop the instance, back up the H2 database, delete the rows the new files replace (a seed load adds and updates but never deletes), load each file by absolute path in dependency order, restart, and check by read-only SQL through the SQL Runner (row counts, orphan items, dangling references, prepared queries). Use this skill whenever seed data has to be tried in a running instance, a test database has to be refreshed after regenerating data, or a load has to be verified.
---

# moqui-seed-reload: seed data into a test instance

Seed files are the source of truth; a test database is disposable, but only after a backup. Write and validate the
files with `moqui-data` (`check_data.py` 0 errors) before loading them. These steps assume the Java/Groovy
`moqui-framework` with H2 (`runtime/db/h2/moqui`, user and password from the instance configuration, `sa`/`sa` in
the default development configuration) and the instance run as a service; adapt the stop and start commands.

## Steps

1. **Stop the instance** (`systemctl --user stop <service>`) and make sure no JVM still holds the database:
   `ps -C java -o pid=,args=`. Do not use `pgrep -f` or `pkill -f` with a pattern: they match the shell that runs
   them. H2 refuses a second connection while the server runs.
2. **Back up** the database directory: `cp -a runtime/db/h2/. <backups>/h2-<date>-before-<change>/`. Name the backup
   after the change, and write it into the session log.
3. **Delete what the new files replace.** `load` inserts and updates, it never deletes: an item whose id changed, a
   vocabulary concept that was removed or a link that moved stays in the database. Delete the rows of the records
   you regenerate with the H2 shell, children first:

   ```sh
   java -cp <h2 jar> org.h2.tools.Shell -url "jdbc:h2:<abs path>/runtime/db/h2/moqui" -user sa -password sa \
     -sql "DELETE FROM AGREEMENT_ASSOC WHERE AGREEMENT_ID IN (...) OR TO_AGREEMENT_ID IN (...); DELETE FROM AGREEMENT_ITEM WHERE AGREEMENT_ID IN (...)"
   ```

   The H2 jar is in the exploded war (`execwartmp*/ROOT/webapp/WEB-INF/lib/h2-*.jar`) or in the Gradle cache. Count
   the rows first (`SELECT COUNT(*) ...`), compare with what you loaded last time, then delete. For a graph, delete
   `PARAMETER`, `GRAPH_EDGE` and `GRAPH_VERTEX` of that `GRAPH_ID`.
4. **Load each file**, one per command, by absolute path, from the framework directory:

   ```sh
   java -jar moqui.war load no-run-es location=/abs/path/to/data/40_Norm_X_EN.xml
   ```

   A relative `location` is not found. The `no-run-es` option skips the search server. Order: type data and
   enumerations first (entity `seed-data` of changed entity definitions before anything that uses them), then
   shared records (stubs), then the main files, then files that point into several of them (cross references),
   then derived data (vocabulary). A file that references a record not yet loaded fails on its foreign key: load it
   after its targets, or later. Read the `Loaded [n] records` line of every load and compare n with the file.
5. **Start** the instance and wait for `/status` to answer 200.
6. **Check by read-only SQL** through the SQL Runner with `scripts/sqlq.sh <label> <file.sql>` (env `MOQUI_URL`,
   `MOQUI_AUTH`; `SQL_LOG` appends a JSONL record per query for search evaluations):
   - counts per record family against the files;
   - structure: `assets/agreement-checks.sql` (items, references, orphan items, references to missing items for
     every loaded norm) and `assets/cross-references.sql` (references between loaded norms): both must report 0;
   - the prepared queries of the feature you loaded (for the compliance vocabulary: `hook-items.sql` of
     `moqui-norm-hooks`).
7. **Record** in the session log: stop and start times, backup name, files and record counts, check results.

## When something is wrong

Fix the generator or the seed file, regenerate, validate and load again; never patch rows in the database. If a load
fails half way, the files before it are loaded: restore the backup (stop, replace `runtime/db/h2` with the backup
copy, start) or delete and reload. A machine restart during a check loses nothing that is committed or in the data
files; the running service comes back by itself and the scratch files are gone.
