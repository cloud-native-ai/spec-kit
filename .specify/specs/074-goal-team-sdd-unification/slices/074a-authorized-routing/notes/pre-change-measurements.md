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

**Correction (recorded at T028)**: the line registry is environment-level (outside the repository, at
`${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines`), so this capture does **not** hold a referent for
it. T028 answered the same question by two measurements instead — every entry's mtime predates this
stage, and no entry carries a slice-level id; both are in `../notes/quickstart-run.md` § Structure.

## 7. Regression at implement close (task T029, 2026-10-29)

The targeted program is the 13 files owned by `../test-evidence/targeted-set-v1-baseline.txt` plus this
slice's 5 new modules. Full output is captured verbatim in `part5-regression.txt` (single-run capture, one
file rather than a re-run); the failed-nodeid list is the designated sink `part5-failed.txt`.

```console
$ bash scripts/bash/run-tests.sh --names-out .specify/specs/074a-authorized-routing/notes/part5-failed.txt \
    tests/contract/test_agent_dispatch_mechanism.py tests/contract/test_neutral_metadata_schema.py \
    tests/contract/test_tool_mapping.py tests/contract/test_neutral_vocabulary_scan.py \
    tests/contract/test_sdd_loop_driver_skill.py tests/contract/test_team_command_routing.py \
    tests/contract/test_agent_chain_guards.py tests/contract/test_no_nested_skills.py \
    tests/contract/test_goal_definition.py tests/contract/test_instructions_section_propagation.py \
    tests/contract/test_flow_class_ledger.py tests/contract/test_flow_class_correctness.py \
    tests/contract/test_shipped_agent_presets.py tests/contract/test_sdd_authorization.py \
    tests/contract/test_nested_sdd_invocation.py tests/contract/test_sdd_routing_definitions.py \
    tests/contract/test_sdd_routing_engine.py tests/contract/test_sdd_invocation_governance.py
tests/contract/test_sdd_authorization.py ...........                     [ 72%]
tests/contract/test_nested_sdd_invocation.py .......................     [ 81%]
tests/contract/test_sdd_routing_definitions.py ..............            [ 86%]
tests/contract/test_sdd_routing_engine.py .....................          [ 93%]
tests/contract/test_sdd_invocation_governance.py .................       [100%]

============================= 277 passed in 24.04s =============================
# failed-name list written: .specify/specs/074a-authorized-routing/notes/part5-failed.txt (0 entries)
rc=0
```

277 = 191 (the 13 baseline files) + 34 (authorization 11 + nested invocation 23) + 14 (routing
definitions) + 21 (routing engine) + 17 (invocation governance). The five new modules are green in full.

### Name-level comparison (MUST be empty, and shown to be non-vacuous)

```console
$ comm -13 <(sort -u .specify/specs/074a-authorized-routing/notes/targeted-set-v1-failed.txt) \
           <(sort -u .specify/specs/074a-authorized-routing/notes/part5-failed.txt)
(no output)
```

Both sides are empty — T002's re-capture recorded `191 passed` with a 0-entry failed-name list — so this
`comm` alone proves little. The instrument's non-vacuity is measured separately: the full-suite baseline
does carry failures, and none of them lives in the 13 targeted files, which is why "0 now" is a real
statement rather than an artefact of an empty set on both sides.

```console
$ wc -l < .specify/specs/074a-authorized-routing/baseline-failed.txt
23
$ grep -F -f <(printf '%s\n' tests/contract/test_agent_dispatch_mechanism.py tests/contract/test_neutral_metadata_schema.py tests/contract/test_tool_mapping.py tests/contract/test_neutral_vocabulary_scan.py tests/contract/test_sdd_loop_driver_skill.py tests/contract/test_team_command_routing.py tests/contract/test_agent_chain_guards.py tests/contract/test_no_nested_skills.py tests/contract/test_goal_definition.py tests/contract/test_instructions_section_propagation.py tests/contract/test_flow_class_ledger.py tests/contract/test_flow_class_correctness.py tests/contract/test_shipped_agent_presets.py) \
       .specify/specs/074a-authorized-routing/baseline-failed.txt | sort
(no output)
```

The 23 pre-existing failures (all outside this slice's surface) are untouched, unfixed and unclaimed:
their names still stand in `baseline-failed.txt`, and no targeted-set file is among them. The closure
full-suite re-run belongs to the driver after review, not to this stage (its E2 slot was spent at
implement start, `test-evidence/implement.jsonl` seq 1: `6361 passed / 23 failed`).

### The classification-honesty audit is a declared handoff, not a green here

T029 also lands the audit duty rather than the audit. `/speckit.review` is this slice's
classification-honesty audit face: it re-checks every **declared** input's classification and records
inconsistencies, and a nested run additionally gets the driver's own U4 independent verification. The
engine's determinism covers only the declared inputs — it cannot audit whether a caller classified a
change honestly — so audit conclusions are recorded in **review evidence** and MUST NOT be written back
into a verdict (the owner document's § Verdict record forbids re-computing or overwriting a recorded
decision: a user override and a re-judgement are recorded side by side, never merged).

Status of that face at this point: **`not-evaluated`** — reason: the review stage has not run yet in the
SDD loop (this stage is `implement`). No review evidence file exists for this slice, and this file does
not stand in for one.

## 8. What this file is not

It records denominators only. The name-level test baseline is owned by
`../test-evidence/targeted-set-v1-baseline.txt` (re-captured as T002) and the clause-coverage
denominator by `../coverage-baseline.txt` (re-frozen as T003); this file cites them and does not
copy their contents.
