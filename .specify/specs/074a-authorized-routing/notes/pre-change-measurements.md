# Pre-change measurements — slice 074a-authorized-routing (task T001)

**Captured at**: 2026-10-29T02:5xZ, before any source edit of this slice's implement stage
**HEAD at capture**: `71954e31a1ff58480342209c1d54329a05c30225`
**Purpose**: freeze the four comparison denominators every "zero new drift / zero new store / zero
new failure" criterion in `tasks.md` is measured against. Real output pasted verbatim below; no
value in this file is hand-computed.

---

## 1. Mirror surfaces (`python3 scripts/python/sync-mirrors.py --check`)

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (405 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (113 files)
ok    shared/ == .specify/shared/ (58 files)
```
`rc=0`. Six pairs, zero pre-existing drift → the post-change criterion (GATE-6) is "no NEW drift",
and this file's block is its referent.

## 2. Per-tool command copies (`python3 scripts/python/regen-command-copies.py --check`)

```text
OK: all per-tool command copies match the source templates.
```
`rc=0`. This is the baseline that proves, after the slice, that `templates/commands/**` was not
touched (T026).

## 3. `sdd-invocation` landing count in the code owner

```console
$ grep -c 'sdd-invocation' src/specify_cli/__init__.py
0
rc=1
```
`rc=1` is grep's "zero matches", not a command failure. The key is genuinely absent from its owner
before T008; the post-edit criterion is exactly one definition point (pinned by
`tests/contract/test_neutral_metadata_schema.py`), never a pre-written number.

## 4. Anti-nesting obligation site

```console
$ grep -n 'loop depth' shared/definitions/subagent-definitions.md
104:**Anti-nesting obligation (反嵌套)**: the dispatching prompt MUST NOT reference any driver/loop skill (e.g. `sdd-loop-driver`), MUST NOT instruct the subagent to load any skill, and MUST NOT contain loop logic — the loader of a driver manual is the driver; a subagent that receives the manual becomes a second driver and the hierarchy escapes (loop depth is always 1: driver → stage executor). The operational enforcement lives in `skills/internal/run-agent/SKILL.md` dispatch governance (pre-dispatch probe extended to this obligation); the ruling's provenance is the sdd-loop-driver Driver Topology defect fix (2026-10-16).
rc=0
```
Line `104` is the sentence T023 replaces in place. The `## Dispatch-Time Governance Obligation`
heading is at line `98` (measured by the plan stage and unchanged since — the line numbers agree).

## 5. Repository state at capture

```console
$ git rev-parse HEAD
71954e31a1ff58480342209c1d54329a05c30225
rc=0
```

```console
$ git status --short
 M .specify/memory/session/20261019T133423Z-run-determination-speckit-tasks-tasks-063-20261019t133409z.md
 M .specify/memory/session/20261024T124553Z-run-determination-speckit-tasks-tasks-069a-20261024t1245z.md
 M .specify/memory/session/20261027T070314Z-run-determination-speckit-analyze-r20261027t061144z-a3ec.md
?? .specify/memory/exec-quant/records/20261028T124651937182Z-7fd772fb.json
?? .specify/memory/exec-quant/records/20261028T124652237453Z-e4ba14f4.json
?? .specify/memory/exec-quant/records/20261028T131040921319Z-0fce00d5.json
?? .specify/memory/exec-quant/records/20261028T131041222137Z-9c32540e.json
?? .specify/memory/exec-quant/records/20261028T134350629408Z-c59db43d.json
?? .specify/memory/exec-quant/records/20261028T134548856368Z-4f876af9.json
?? .specify/memory/exec-quant/records/20261028T152505986776Z-4f97c686.json
?? .specify/memory/exec-quant/records/20261028T160403218399Z-7663625e.json
?? .specify/memory/exec-quant/records/20261029T020007282103Z-e5f8d1e6.json
?? .specify/memory/exec-quant/records/20261029T021014316987Z-0f6b248c.json
?? .specify/memory/exec-quant/records/20261029T022001803573Z-2ae19888.json
?? .specify/memory/exec-quant/records/20261029T022536807989Z-62e25de8.json
?? .specify/memory/exec-quant/records/20261029T023140000541Z-c8e92070.json
?? .specify/memory/exec-quant/records/20261029T025011351885Z-51cf9de6.json
?? .specify/memory/feedback/20261028T124704Z-speckit-requirements.md
?? .specify/memory/feedback/20261028T124708Z-skill-create-requirements.md
?? .specify/memory/feedback/20261028T131050Z-speckit-clarify.md
?? .specify/memory/feedback/20261028T131053Z-skill-clarify-artifact.md
?? .specify/memory/feedback/20261028T134353Z-speckit-plan.md
?? .specify/memory/feedback/20261028T134552Z-skill-sdd-loop-driver.md
?? .specify/memory/feedback/20261028T152509Z-speckit-tasks.md
?? .specify/memory/feedback/20261028T160637Z-speckit-requirements.md
?? .specify/memory/feedback/20261029T020012Z-speckit-clarify.md
?? .specify/memory/feedback/20261029T021018Z-speckit-plan.md
?? .specify/memory/feedback/20261029T022007Z-speckit-tasks.md
?? .specify/memory/feedback/20261029T022540Z-speckit-checklist.md
?? .specify/memory/feedback/20261029T023143Z-speckit-analyze.md
?? .specify/memory/feedback/20261029T025017Z-speckit-analyze.md
?? .specify/memory/session/20261028T124645Z-run-determination-speckit-requirements-20261028t1245z-074-go.md
?? .specify/memory/session/20261028T124648Z-run-determination-skill-create-requirements-20261028t1245z-0.md
?? .specify/memory/session/20261028T131037Z-run-determination-speckit-clarify-20261028t1305z-074-clarify.md
?? .specify/memory/session/20261028T131038Z-run-determination-skill-clarify-artifact-20261028t1305z-074.md
?? .specify/memory/session/20261028T134339Z-run-determination-speckit-plan-r20261028t132000z-074d.md
?? .specify/memory/session/20261028T134545Z-run-determination-skill-sdd-loop-driver-r20261028t132000z-07.md
?? .specify/memory/session/20261028T152503Z-run-determination-speckit-tasks-r20261028t132000z-074d.md
?? .specify/memory/session/20261028T160359Z-run-determination-speckit-requirements-r20261028t132000z-074.md
?? .specify/memory/session/20261029T020004Z-run-determination-speckit-clarify-20261029t0200z-074a-clarif.md
?? .specify/memory/session/20261029T021009Z-run-determination-speckit-plan-r20261028t132000z-074d-plan2.md
?? .specify/memory/session/20261029T021955Z-run-determination-speckit-tasks-r20261028t132000z-074d-tasks.md
?? .specify/memory/session/20261029T022534Z-run-determination-speckit-checklist-r20261028t132000z-074d-c.md
?? .specify/memory/session/20261029T023137Z-run-determination-speckit-analyze-r20261028t132000z-074d-ana.md
?? .specify/memory/session/20261029T025007Z-run-determination-speckit-analyze-r20261029t024852z-074d-ana.md
?? .specify/state/074-goal-team-sdd-unification.md
rc=0
```

**Pre-existing dirty set (not ours, never committed or reverted by this stage)**: the three modified
`session/` records plus every untracked entry above. Note that `.specify/state/074-goal-team-sdd-unification.md`
is **untracked** at capture — the state spine is a runtime record of this loop, not a slice artifact.

## 6. Store-surface denominators (GATE-7 / GATE-2 of `tasks.md` T028)

```console
$ ls -1 .specify/state/
074-goal-team-sdd-unification.md
eval-baseline
speckit-docs-expression.md
```

```console
$ ls -1 .specify/memory/
constitution.md
evidence
exec-quant
features
features.md
feedback
glossary.md
knowledge
register.md
sanitize
session
tools
tools.md
trigger
```

The GATE-7 comparison is a **file-name set** diff (`comm -13`) over these two surfaces (plus the
existing line-registry directory), never a line or directory count.

## 7. What this file is not

It records denominators only. The name-level test baseline is owned by
`../test-evidence/targeted-set-v1-baseline.txt` (re-captured as T002) and the clause-coverage
denominator by `../coverage-baseline.txt` (re-frozen as T003); this file cites them and does not
copy their contents.
