# Quickstart run — 110-context-management — T037 — 2026-11-27T10:31Z

Every scenario in `.specify/specs/110-context-management/quickstart.md` executed exactly as
written, worktree `.specify/.tmp/sdd-loop/worktrees/context-management`, engine
`.specify/scripts/python/context-audit.py` (installed mirror, `cmp`-identical to its source).
Raw captures: `.specify/.tmp/p4/t037/` (scratch, git-ignored). Each scenario record carries
command, real output (decisive excerpt), exit status and teardown.

## Existing-carrier reads (re-taken)

```
$ python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:110-context-management"
flow_class: execution
source: declaration            → exit 0 (unchanged from the plan-time reading)
$ python3 scripts/python/declaration_reader.py --action get --fact memory-types --repo .
{fact: memory-types, kind: closed-set, statement: [session, knowledge], …}   → exit 0
$ grep -c '^## ' .specify/templates/instructions-template.md .specify/instructions.md
template: 40   live: 41        (plan time: 39 / 40 — +1 is this feature's ambient section)
$ wc -c .specify/instructions.md
40533                          (plan time: 40170 — +363 B ambient section, within the 40960 budget)
$ python3 scripts/python/sync-mirrors.py --check
exit 0
```

## Scenario 1 — Audit the repository's own layout

```
$ python3 .specify/scripts/python/context-audit.py --action check
summary: total=0 findings=0 by_rule=roster-mismatch=0 roster-order=0 unknown-layer=0 unknown-form=0 layer-form-illegal=0 duplicate-class=0 empty-layer=0 cap-missing=0 category-column=0
exit=0
```

## Scenario 2 — Manifest the project layer

```
$ python3 .specify/scripts/python/context-audit.py --action manifest --layer project
row: governance-baseline | layer=project | form=read-in-full | source=.specify/constitution.md, .specify/instructions.md | token=present | cap=…§ 摘要优先(Summary-First)
row: project-vocabulary | layer=project | form=pointer | source=.specify/glossary.md | token=present | cap=—
row: concept-definitions | layer=project | form=bounded-index | source=.specify/shared/definitions/ | token=present | cap=…§ 摘要优先(Summary-First)
row: concept-explanations | layer=project | form=pointer | source=.specify/skills.md, .specify/tools.md | token=present | cap=—
row: capability-inventories | … | token=present
row: project-state-anchors | … | token=present
row: workspace-map | … | token=present
counts: present=7 absent=0 unreachable=0 empty=0 not-evaluated=0
source-reading: 0b30804e51d19bf33e338504b70f71cf9488ba8446a1c0a1cb3c9f5ad05d3e2f
exit=0
```

Seven rows in roster order, all present, ending with one `source-reading:` digest line —
as documented.

## Scenario 3 — Machine-readable manifest for any layer

```
$ python3 .specify/scripts/python/context-audit.py --action manifest --layer task --json
{"action": "manifest", "layer": "task", "rows": [ {"class": "task-artifacts", "layer": "task",
 "form": "bounded-index", "sources": [".specify/specs/", ".specify/features/"], "token": "present",
 "reason": null, "cap": "…§ 摘要优先(Summary-First)"}, …], "counts": {…}, "source_reading": "…64-hex…"}
exit=0
```

Ordered top-level keys `action`, `layer`, `rows`, `counts`, `source_reading`; each row the
seven ordered keys; exit 0 (full payload in `.specify/.tmp/p4/t037/scenario3.json`).

## Scenario 4 — Seeded violation fixtures

```
$ python3 .specify/scripts/python/context-audit.py --action check --workspace-root <fixture-root>
unknown-layer      → exactly 1 finding, exit=1
unknown-form       → exactly 1 finding, exit=1
roster-mismatch    → exactly 1 finding, exit=1  (names missing=['task-memory'])
layer-form fixture → exactly 2 layer-form-illegal findings (rows 2 and 9), exit=1
```

Four documented fixtures, each exactly its expected finding(s) and exit 1. Declaration-layer
error fixtures stay the exit-2 input cases (not exercised by this scenario).

## Scenario 5 — A fresh project, offline

The literally written `specify init fresh-dir --ai qoder --no-git --ignore-agent-tools` step
is replaced by the repository's own in-process init path, exactly as the scenario's premise
states (the installed 0.0.22 CLI predates this feature). Everything else runs as written;
sockets blocked in process.

```
init: copy_local_templates(<fresh-dir>, 'qoder', 'sh') -> exit 0
installed: .specify/shared/definitions/context-management-definitions.md present
installed: .specify/shared/declarations/facts/context-{categories,layers,forms,classes}.yaml present
installed: .specify/scripts/python/context-audit.py present

$ python3 .specify/scripts/python/context-audit.py --action check            # in-process, sockets blocked
summary: total=0 findings=0 …                                                exit=0
$ python3 .specify/scripts/python/context-audit.py --action manifest --layer project   # in-process, sockets blocked
rows=7 absences=5
  governance-baseline    -> absent  | absent: .specify/instructions.md does not exist
  project-vocabulary     -> absent  | absent: .specify/glossary.md does not exist
  concept-explanations   -> absent  | absent: .specify/skills.md does not exist
  capability-inventories -> empty   | empty: .specify/agents/instances/ holds no entry
  project-state-anchors  -> absent  | absent: .specify/features/ does not exist
exit=0
socket attempts: 0
teardown: fresh dir removed: True
```

Explicit absence lines with reasons; zero socket attempts; nothing transmitted.

## Scenario 6 — Determinism and containment

```
$ python3 .specify/scripts/python/context-audit.py --action check > .specify/.tmp/run-a.txt
exit=0
$ python3 .specify/scripts/python/context-audit.py --action check > .specify/.tmp/run-b.txt
exit=0
$ diff .specify/.tmp/run-a.txt .specify/.tmp/run-b.txt
exit=0                        # no diff output
$ rm -f .specify/.tmp/run-a.txt .specify/.tmp/run-b.txt     # teardown of the scratch redirects

SHA-256 tree manifest over tests/fixtures/context-management/all-present, before and after
both audit actions (`__pycache__` excluded by name; 16 entries):
diff (before, after) → exit=0; check exit=0; manifest exit=0
```

Byte-identical reruns; the tree manifest is identical before and after, zero new files.

## Teardown summary

All scenario scratch landed under `.specify/.tmp` (sanctioned, git-ignored) and was removed
where the scenario created it (`run-a/run-b.txt`, the fresh tree); the raw capture files stay
in `.specify/.tmp/p4/t037/` as scratch evidence.