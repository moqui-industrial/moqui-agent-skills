#!/usr/bin/env python3
"""Create or resume a setup session directory.

Usage: init_session.py SESSIONS_DIR SESSION_ID
Creates SESSIONS_DIR/SESSION_ID with session.json, survey-answers/, seed-data/, notes/, exports/.
On an existing session it prints the step status so work can resume where it stopped.
"""
import sys, os, json, datetime

STEPS = ["survey", "reference-data", "organizations", "contacts", "accounting", "people",
         "facilities", "products", "forms", "extensions", "load-and-verify"]


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    root = os.path.join(sys.argv[1], sys.argv[2])
    path = os.path.join(root, "session.json")
    if os.path.exists(path):
        s = json.load(open(path))
        print(f"resuming {root}")
    else:
        for d in ("survey-answers", "seed-data", "notes", "exports"):
            os.makedirs(os.path.join(root, d), exist_ok=True)
        s = {"id": sys.argv[2], "created": datetime.datetime.now().isoformat(timespec="seconds"),
             "steps": {k: "todo" for k in STEPS}, "files": {}}
        json.dump(s, open(path, "w"), indent=2)
        print(f"created {root}")
    for k in STEPS:
        print(f"  {s['steps'].get(k, 'todo'):8} {k}")


if __name__ == "__main__":
    main()
