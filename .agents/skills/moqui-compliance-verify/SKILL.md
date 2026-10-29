---
name: moqui-compliance-verify
description: Verify a compliance project before it closes requirements or reaches a customer, and improve the skills after it - deterministic checks by script (project structure, evidence of satisfied requirements, installed firmware against security advisories, CVE attribution to the right vendor and product), an independent verifier agent with a fresh context at the gates where a judgement closes a requirement or decides applicability, and a retrospective at the end of every real project that turns the errors found into proposed changes to the skills, approved by a person. Use this skill before marking requirements satisfied, before deciding that a regulation does not apply, before publishing or sending a report, when a second opinion on an assessment is asked for, and at the end of a project.
---

# moqui-compliance-verify: checks, gates and the retrospective

The agent that produced an artefact shares its own blind spots: in the case that shaped this skill, the same agent
named a managed switch unmanaged, attributed a vendor's CVEs to another vendor, used a network drawing of another
plant and missed a transitional article, and found these only on a second reading of the sources. Two defences:
everything a script can decide is decided by a script, every time; what needs judgement is re-read at the gates by an
agent that did not write it.

## 1. Deterministic checks (always, before each gate)

From a terminal on the host (where Moqui and `cveawg.mitre.org` are reachable):

```sh
python3 -I scripts/check_project.py --project <workEffortId> [--advisories advisories.json --root <prefix>]
```

(Do not run `check_project.py` inside the `skills-python` sandbox of LibreChat: that container has no network access to
Moqui or to `cveawg.mitre.org`. In a chat, write `advisories.json` in the workspace and run `check_project.py` on the
host, or check the CVE record with web search on `cveawg.mitre.org` and the project records via the `moqui` MCP tools.)

- **project**: the structure checks of `moqui-norm-requirements` (`assets/project-checks.sql`): every task has a
  requirement, every requirement its norm item, no duplicates, no open task of a rejected requirement, every satisfied
  requirement a closed task with evidence, every action task at least one requirement.
- **attachments & technical file completeness**: verify against the 4-pillar benchmark
  (`moqui-compliance-intake/references/technical-file-benchmark.md`) that every attached `ProductContent`,
  `DeviceContent` and `WorkEffortContent` record resolves to an existing, non-empty file in the content store, and that
  standard product documentation (`ProductContent`) is cleanly separated from installation-specific records and
  commissioned software (`DeviceContent`).
- **evidence**: satisfied requirements whose only evidence is a web page are listed: store a copy
  (`attach_content`), pages change.
- **firmware**: `PhysicalDevice.firmwareVersion` of the installed devices against the minimum fixed versions of the
  advisories (`advisories.json`, written from the vendors' advisory pages, one row per advisory and product); advisories
  without a fix require mitigations; a device without a recorded version is a finding.
- **cve**: every CVE is read from its record (`cveawg.mitre.org`) and must name the vendor it is cited for. Search
  summaries mix vendors; the record decides.

A FAIL blocks the gate: fix the data or the artefact, run again.

## 2. Gates for the independent verifier

Call a second agent (fresh context, no access to the producing conversation) at these gates only:

| Gate | Why |
| --- | --- |
| before `satisfy_norm_requirement` on a batch of requirements | a requirement closed on a misread datasheet hides a non-conformity |
| before stating that a regulation or a norm part does not apply (market, scope, kind of product, transitional rules) | an applicability error removes all its requirements at once |
| before a report or a technical file section leaves the company | a customer or an authority acts on it |
| before proposing changes to the skills (section 3) | a wrong lesson spreads to every later project |

Give the verifier: the artefact (report page, list of requirements to close with their evidence, applicability
decision), read access to the database (norm items, project) and to the evidence files, and this mandate:

> Try to refute it. For every statement that cites a norm item, read the item (get_norm_tree) and say whether it says
> that. For every requirement to close, open the evidence and find the page or clause that shows it; "the datasheet
> says it is secure" is not evidence. For every applicability decision, read the scope, definitions and transitional
> articles of the regulation. For every product named, check that the order code is that product. List what you could
> not verify. Do not rewrite the artefact; return findings with the item or page they rest on.

The producing agent fixes the findings or answers them; unresolved findings go to the person who approves. Routine
steps (loading, planning, classification proposals the user confirms) need no verifier: the checks of section 1 and
the user's confirmation are enough.

## 3. Retrospective (end of every real project)

Continuous improvement, with a gate: the skills guide every later project and the repository is public.

1. Create the retrospective task: `add_norm_action_task` with `purposeEnumId=CmpWepRetrospective` in the project.
2. List, from the project and its conversation: errors found by checks, verifier or user; questions the skills did not
   tell the agent to ask; queries or steps repeated by hand; vocabulary gaps (concepts the norms name and the
   vocabulary lacks); defects of the norm data (lost text, wrong references); rules of the plan that misfired.
3. For each, the smallest change that prevents it next time, in the right place: a rule in a SKILL.md, a check in a
   script, a lesson in `references/cases.md` or in the Lessons of `moqui-compliance-intake`, a vocabulary pass
   (`moqui-norm-hooks`), a reader fix (`moqui-norm-loading`), a plan rule (`NormProjectPlan.groovy`, with its test).
   Encode the principle, not the case: "check the title block of every drawing", not "the PICK drawing is not ours".
4. Prepare the changes as a diff, run the verification loops they touch (`verify_norms`, plan on the test bills,
   `check_project.py`), have the verifier read the diff, and ask the person to approve before committing. No licensed
   norm text in the skills: cite item ids, paraphrase.
5. Record in the retrospective task what was changed and where (commit), what was not and why.
