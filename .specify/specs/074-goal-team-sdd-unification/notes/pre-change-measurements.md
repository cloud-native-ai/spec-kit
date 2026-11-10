<!-- merged from 074a-authorized-routing (source: .specify/specs/074a-authorized-routing/notes/pre-change-measurements.md) -->

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

<!-- merged from 074b-nested-governance (source: .specify/specs/074b-nested-governance/notes/pre-change-measurements.md) -->

# Pre-change measurements — slice 074b-nested-governance (implement, T033)

**Captured**: 2026-10-29T05:45:14Z, before any edit of this slice's delivery surface.
**HEAD at capture**: `241a6082b40e7eb412de8143d0d0fbc52014967f` (`241a6082b`)
**Host**: linux / Python 3.11.11 / pytest 8.4.2

Every block below is pasted from the real run of the command above it; no value is transcribed by hand.
Later tasks append their own sections (`containment`, `regression`) — this file is the single evidence
sink for "no new X" comparisons, so a reader compares against the block captured here, never against a
number quoted in another document.

## 1. Mirror and command-copy baselines

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (406 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (114 files)
ok    shared/ == .specify/shared/ (59 files)
rc=0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc=0
```

Six pairs, zero pre-existing drift: the criterion for every mirror row of this slice is "no NEW drift",
and it is measurable as "still clean".

## 2. Repository state at capture

```text
$ git rev-parse HEAD
241a6082b40e7eb412de8143d0d0fbc52014967f

$ git status --short | wc -l
33
# 8 modified tracked files (all under .specify/memory/session/, pre-existing dirty — not touched,
#   not restored by this slice) + 25 untracked entries:
#   .specify/memory/{exec-quant/records,feedback,session}/… (8 each, per-entry stage-accounting records)
#   .specify/state/074b-nested-governance.md (1)
```

The eight modified tracked session files and the twenty-five untracked entries above are **pre-existing**
and are neither committed nor reverted by this slice.

## 3. Instruction-surface sizes (the ceiling judgement for FR-024 / C-18)

```text
$ wc -c templates/instructions-template.md .specify/instructions.md
34666 templates/instructions-template.md
41948 .specify/instructions.md
76614 total
```

Both files already exceed the generator's 32,768 B budget **before** this slice, so the diffusion section's
criterion is a declared ceiling plus a measured delta, never "fits the budget" (research RB6).

## 4. The leaf preset carries no hosting declaration (V-9's negative subject)

```text
$ grep -c 'sdd-invocation' agents/sdd-executor.agent.md
0
rc=1
```

Measurement unit: the shipped preset file, not a repo-wide grep (design prose mentioning the key is a
citation, not a declaration).

## 5. Ledger attribution field (reused, never invented)

```text
$ grep -n 'target_ref' skills/internal/create-team/references/summary-mapping.md
100:| `target_ref` | string | 否 | 归属的 Target 身份(038)。**局部形** `T-\d{3}`,goal 由团队绑定隐含;缺省 = 归属 goal 整体。见 §6.5 |
143:### 6.5 `target_ref` 归属折叠(038)
149:- **缺省**:无 `target_ref` → 归属 goal 整体(`targets.unattributed_to_target` 计数);存量行语义不变。
150:- **正交性**:团队命名空间前缀(`<team-slug>.TI-nnnn`,§6.2)照常加;`target_ref` 仍为局部形,二者互不影响。
```

Field, grammar and default are owned there; this slice cites them and adds no field.

## 6. Flow-class baseline (no-new-unit negative)

```text
$ python3 .specify/scripts/python/flow-class-check.py --action check
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
rc=0
```

## 7. Existence census of the 9-row delivery surface

```text
$ for f in <the nine rows + the leaf preset and the reused fixture>; do test -e "$f" && echo OK || echo ABSENT; done
OK      skills/internal/create-team/SKILL.md
OK      skills/internal/create-team/references/conceptual-model.md
OK      skills/internal/run-agent/SKILL.md
OK      templates/instructions-template.md
OK      shared/guidelines/proactive-trigger.md
OK      tests/contract/test_sdd_invocation_governance.py
OK      tests/fixtures/nested_sdd.py
OK      agents/sdd-executor.agent.md
ABSENT  tests/contract/test_nested_run_report.py
ABSENT  tests/contract/test_sdd_diffusion.py
ABSENT  tests/contract/test_sdd_compat_containment.py
```

8/8 subjects in place, 3/3 new suites absent — the precondition of the red-first step.

## 8. Storage-surface file-name sets (GATE-7 comparator)

```text
$ find .specify/state -maxdepth 1 -type f | LC_ALL=C sort | wc -l
3
$ find .specify/memory -type f | LC_ALL=C sort | wc -l
681
# .specify/memory/ composition by top-level entry: feedback 194, session 180, evidence 130,
#   exec-quant 78, features 71, tools 10, knowledge 9, trigger 2, sanitize 2,
#   + tools.md / register.md / glossary.md / constitution.md (single files)
```

The two sorted lists (688 lines with headers) live verbatim in
[`pre-change-file-sets.txt`](pre-change-file-sets.txt) — captured with the command recorded in that
file's header, because the comparator for GATE-7 / T056 is `LC_ALL=C comm -13 <that file> <re-captured>`
and a comparison needs the pre-list on disk, not a count in prose. The lists are kept out of this
document so a reader is not handed 681 machine-generated paths to skip.

Reading note for the later comparison: `feedback/`, `session/`, `evidence/` and `exec-quant/records/`
are per-entry record families written by stage accounting (one file per entry, timestamped names); a new
name there is a stage record, not a registry, ledger, state spine, ownership model or integration queue.
`state/` is the line-registry / state-spine family and its name set is the strict one.

## 9. Not measured here

- Full-suite baseline: recorded as the implement slot-`baseline` row in
  [`../test-evidence/implement.jsonl`](../test-evidence/implement.jsonl) (`seq=1`), not in this file.
- Name-level targeted baseline: owned by
  [`../test-evidence/targeted-set-v1-baseline.txt`](../test-evidence/targeted-set-v1-baseline.txt) (T034
  re-captures it in place).
- Clause-coverage baseline: owned by [`../coverage-baseline.txt`](../coverage-baseline.txt) (T035 freezes
  it).

## 10. Containment (post-change): the two claims discharged by name-set comparison (T050)

This section is written **after** the change (the file's other sections are the pre-change halves of
the same comparisons). It discharges `contracts/compat-and-safety.md` C-3, C-4, C-5 and C-6 — the
slice's two containment claims and the four-surface additivity audit — and it is the only place the
comparison is made.

### 10.1 Claim 1+2 — post ⊇ pre per named set, shared ids verdict-unchanged (C-3, C-4, C-6)

**Same command, same file lists** as the pre-change capture that owns the sets
([`../test-evidence/compat-baseline-nodeids.txt`](../test-evidence/compat-baseline-nodeids.txt),
`stage_base=33269994a`, 7 sets / 17 files / 266 cases):

```text
$ python3 -m pytest --collect-only -q <the 17 files of each named set>
# raw capture: ../test-evidence/containment-post-change-collect.txt
S1 pre=49 post=55 lost=0 added=6
S2 pre=25 post=25 lost=0 added=0
S3 pre=24 post=24 lost=0 added=0
S4 pre=40 post=40 lost=0 added=0
S5 pre=36 post=36 lost=0 added=0
S6 pre=54 post=54 lost=0 added=0
S7 pre=38 post=38 lost=0 added=0
```

**Set containment (the criterion), never a count comparison**: `pre \ post` is empty for every set —
no pre-change case id disappeared — and the only additions are the six cases T049 landed in set `S1`
(they are listed by name in the capture, not summarised as "+6"). `S2`–`S7` are id-identical.

**Shared-id verdicts** — the same 17 files executed once:

```text
$ bash scripts/bash/run-tests.sh --names-out .specify/.tmp/containment-post-failed.txt <the 17 files>
============================= 272 passed in 27.26s =============================
# failed-name list written: .specify/.tmp/containment-post-failed.txt (0 entries)
rc=0
```

Every one of the 266 shared ids is **green after** as it was **green before**: the post-change failing
set is empty, so it agrees with the pre-change verdict for every shared id (the reading rule for
C-3/C-6 admits a case red in the baseline to stay red; here there is none — none of the 17 files
appears in [`../baseline-failed.txt`](../baseline-failed.txt)). Full capture:
[`../test-evidence/containment-post-change-run.txt`](../test-evidence/containment-post-change-run.txt).

### 10.2 Claim 3 — the four predecessor surfaces are untouched (C-5, C-7, C-8, C-9)

`git diff` against the baseline commit named above, over each surface's owner paths. **The positive
control matters**: without it an empty diff proves only that the command printed nothing, so the last
block runs the identical command form on a path this slice *did* edit and shows it reporting.

```text
$ git rev-parse 33269994a
33269994a7dba7976d25c44da9ef319045a4f517

$ git diff --stat 33269994a -- skills/external/sdd-loop-driver .specify/specs/058-sdd-loop-driver
[changed paths: 0]                                   # S2 — standalone driver entry (058-sdd-loop-driver)

$ git diff --stat 33269994a -- skills/external/sdd-loop-driver/references/decomposition-model.md \
                            .specify/specs/070-subagent-task-teams
[changed paths: 0]                                   # S3 — Feature 070 stage-team preset contract

$ git diff --stat 33269994a -- scripts/python/line-registry.py .specify/specs/064-subagent-concurrency
[changed paths: 0]                                   # S4 — Feature 064 line / worktree / ownership

$ git diff --stat 33269994a -- skills/external/sdd-loop-driver/SKILL.md \
                            skills/external/sdd-loop-driver/references/stage-prompts.md \
                            skills/external/sdd-loop-driver/references/watch-model.md \
                            .specify/specs/058-sdd-loop-driver
[changed paths: 0]                                   # S5 — Feature 058 U0–U6 contract

$ git diff --stat 33269994a -- skills/internal/create-team/SKILL.md
 skills/internal/create-team/SKILL.md | 14 ++++++++++++++
 1 file changed, 14 insertions(+)
[changed paths: 1]                                   # POSITIVE CONTROL — the same form, a path this slice edited
```

**Reading**: no existing key, section, entry form or exit-code meaning on those four surfaces moved,
because nothing on them changed at all; and the control shows the command form returns a non-empty
stat when its subject does move, so the four empty results are evidence rather than silence.

The slice's other read-only subjects were checked the same way (empty output = zero diff):

```text
$ git diff --stat 33269994a -- skills/internal/run-team/SKILL.md agents/sdd-executor.agent.md \
      scripts/python/sdd-route.py shared/definitions/subagent-definitions.md \
      shared/definitions/sdd-routing-definitions.md src/specify_cli/__init__.py \
      tests/fixtures/nested_sdd.py templates/commands
                                     # empty: every one of the eight read-only subjects is untouched
```

## 11. Regression (T055): the targeted set re-run once, judged by node-id name

One run, at HEAD `1c8b89778` (part 3 committed), before this task's own edits. Full capture:
[`../test-evidence/implement-targeted-part4-run.txt`](../test-evidence/implement-targeted-part4-run.txt).

```text
$ bash scripts/bash/run-tests.sh --names-out \
    .specify/specs/074b-nested-governance/test-evidence/implement-targeted-part4-failed.txt \
    <the 19 files owned by test-evidence/targeted-set-v1-baseline.txt> \
    tests/contract/test_nested_run_report.py tests/contract/test_sdd_diffusion.py \
    tests/contract/test_sdd_compat_containment.py
collected 338 items
=========================== short test summary info ============================
FAILED tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged
======================== 1 failed, 337 passed in 34.04s ========================
# failed-name list written: …/implement-targeted-part4-failed.txt (1 entries)
rc=1
duration_s=34
```

**Name-level comparison against the T034 re-capture** (the baseline file is the owner of that
list; the comparison extracts its recorded `tests/…::…` line rather than re-deriving it):

```text
$ awk '/^# failed-name list: /{f=1;next} f&&/^tests\//{print}' \
    .specify/specs/074b-nested-governance/test-evidence/targeted-set-v1-baseline.txt | sort
tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged

$ comm -13 <T034 re-capture name list> <part-4 failing name list>   # MUST be empty
                                     # empty — zero NEW failing node ids
$ comm -23 <T034 re-capture name list> <part-4 failing name list>   # reverse direction
                                     # empty — the pre-existing red was neither fixed nor renamed
```

**The three suites this slice owns are green, counted by file** (`pytest --collect-only -q`):

```text
tests/contract/test_nested_run_report.py: 16 tests collected
tests/contract/test_sdd_diffusion.py: 15 tests collected
tests/contract/test_sdd_compat_containment.py: 11 tests collected
                                     # 42 cases, all passed in the run above
```

**The single pre-existing red is unmoved** — same name, same residual, same integer (measured
here, not quoted from the baseline):

```text
$ python3 .specify/scripts/python/scan-confirmation-gates.py --root . --json \
    | python3 -c 'import json,sys; print(json.load(sys.stdin)["total"])'
27
$ python3 -c "import json;print(json.load(open('.specify/specs/050-proactive-flow-trigger/baseline-gates.json'))['confirmationGates']['total'])"
23
                                     # 27 before and after this slice: no green claim is made
                                     # for this case, and no repair is attempted
```

**Classification-honesty audit duty**: `/speckit.review` is this slice's classification-honesty
audit surface (T055's own wording); this task therefore records no adjudication of its own and
writes none back. What this task contributes to that audit is the measured base it will read: the
E3 row below, the name-level comparison above, and the disclosed pre-existing red.

**E3 stage-status row (targeted evidence, part 4/4)** — `stage=implement`, `row_type=stage-status`,
`status=ran`, `selection_basis=targeted-set-v1` (the 19 files owned by
`test-evidence/targeted-set-v1-baseline.txt` plus this slice's 3 suites, run **once** for this part;
no second full suite), `changed_paths[]=.specify/specs/074b-nested-governance/{verification.md,
tasks.md,notes/pre-change-measurements.md,notes/quickstart-run.md,test-evidence/implement-targeted-part4-*}`,
`evidence_ptr=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part4-run.txt`.
The jsonl row is `test-evidence/implement.jsonl` `seq=7`.
