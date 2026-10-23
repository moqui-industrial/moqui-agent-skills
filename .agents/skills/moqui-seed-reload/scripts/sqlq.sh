#!/bin/bash
# Run one read-only SQL query on a running Moqui instance through the SQL Runner screen (tools app) and print the
# rows; optionally append a record to a JSONL log (test id, time, rows, size, error, SQL) for search evaluations.
#   usage: sqlq.sh <label> <file.sql> [note]
#   env:   MOQUI_URL (default http://localhost:8080), MOQUI_AUTH (user:password, default the demo john.doe:moqui),
#          MOQUI_GROUP (entity group, default transactional), SQL_LOG (JSONL file, default none)
URL=${MOQUI_URL:-http://localhost:8080}
AUTH=${MOQUI_AUTH:-john.doe:moqui}
T0=$(date +%s.%N)
OUT=$(mktemp)
curl -s -u "$AUTH" -X POST "$URL/apps/tools/Entity/SqlRunner" --data-urlencode "groupName=${MOQUI_GROUP:-transactional}" \
  --data-urlencode "limit=500" --data-urlencode "sql@$2" -o "$OUT"
python3 -I - "$OUT" "$1" "$2" "$T0" "${3:-}" "${SQL_LOG:-}" <<'PY'
import sys, re, html, json, time
out, label, sqlf, t0, note, log = sys.argv[1:]
s = open(out, encoding='utf-8', errors='replace').read()
tables = re.findall(r'<table.*?</table>', s, re.S)
# an error is reported outside the result table (a cell may contain the word Exception)
rest = re.sub(r'<table.*?</table>', '', s, flags=re.S)
err = re.findall(r'\b\w*(?:Exception|SQLError)\b[^<]{0,300}', rest)
rows = []
for t in tables:
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
        rows.append([re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', c))).strip()
                     for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)])
n = max(len(rows) - 1, 0)
rec = {'test': label, 'time': time.strftime('%Y-%m-%dT%H:%M:%S'), 'seconds': round(time.time() - float(t0), 2),
       'rows': n, 'resultChars': sum(len(' '.join(r)) for r in rows), 'error': err[0] if err else None,
       'note': note, 'sql': open(sqlf).read()}
if log:
    open(log, 'a').write(json.dumps(rec, ensure_ascii=False) + '\n')
print(f"[{label}] rows={n} seconds={rec['seconds']} error={rec['error']}")
for r in rows:
    print(' | '.join(r))
PY
rm -f "$OUT"
