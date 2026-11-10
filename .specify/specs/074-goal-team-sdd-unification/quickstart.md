# Quickstart: 074-goal-team-sdd-unification

**Requirement → Feature**: `074-goal-team-sdd-unification` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一

Seven scenarios. **S7 was executed live at plan time** and its real output is pasted below. S1–S6
describe behaviour whose implementation lands in `/speckit.implement`; each carries a **per-example
disclaimer** naming the premises it rests on and the test that pins it, so `/speckit.tasks` and
`/speckit.implement` know which facts to re-measure instead of inheriting them. A disclaimer here
covers only the example it is attached to.

---

## S1 — Route a feature-scale change · NOT EXECUTED

```bash
python3 .specify/scripts/python/sdd-route.py --action route \
  --nature capability --traceability required \
  --blast-radius cross-cutting --reversibility hard \
  --complexity standard --format json
```

Expected shape: verdict `sdd`, a reason code from the owner's closed vocabulary, and the five
input values echoed back in the record.

**Disclaimer (per example)**: not executable at plan time — `scripts/python/sdd-route.py` does not
exist yet. Premises this example rests on: (a) the engine's flag names are those contracted in
`contracts/route-decision.md` C-13 (`--action route`, one flag per input, `--format json`);
(b) the five inputs are named exactly as the owner document names them; (c) exit code is `0` for a
produced verdict regardless of which verdict; (d) the copy shipped to `.specify/scripts/python/` is
the mirror of `scripts/python/`, so the `.specify/` path resolves after `sync-mirrors.py` runs.
**Pinning test**: `tests/contract/test_sdd_routing_engine.py::test_route_feature_scale_returns_sdd`.

## S2 — Route a bounded maintenance change · NOT EXECUTED

```bash
python3 .specify/scripts/python/sdd-route.py --action route \
  --nature maintenance --traceability not-required \
  --blast-radius local --reversibility reversible \
  --complexity standard --format json
```

Expected shape: verdict `direct`, with the record naming the conditions that held.

**Disclaimer (per example)**: same non-existence premise as S1. Additional premise: the closed
value literals used here (`maintenance`, `not-required`, `local`, `reversible`, `standard`) are the
owner document's declared domain values — if the owner's literals differ, this example is wrong even
though the engine runs. **Pinning test**:
`tests/contract/test_sdd_routing_engine.py::test_route_bounded_maintenance_returns_direct`.

## S3 — A missing input never falls through to direct · NOT EXECUTED

```bash
python3 .specify/scripts/python/sdd-route.py --action route \
  --nature maintenance --traceability not-required \
  --blast-radius local --reversibility reversible --format json
```

Expected shape: verdict `adjudicate` with the missing-input reason code — the complexity tier was
not declared, and the precedence rule forbids the direct branch when a required input is absent,
even though every supplied value points at direct. The conflicting form is the second adjudicate
case: `--nature capability --blast-radius local-bounded-definition-correction` (a capability
change cannot be a bounded correction).

**Disclaimer (per example)**: not executable at plan time. Premises: (a) the precedence rule is
applied before any branch-specific reasoning (contract C-9); (b) `adjudicate` is not an error, so
the exit code stays `0`; (c) the missing/ambiguous/conflicting distinction is decided from the
owner's enumerated set, not from free text (contract C-10). **Pinning test**:
`tests/contract/test_sdd_routing_engine.py::test_missing_input_never_returns_direct`,
`::test_conflicting_inputs_return_adjudicate`, plus the golden-table property rows in
`--action golden`.

## S4 — Resolve effective authorization · NOT EXECUTED

```bash
python3 .specify/scripts/python/sdd-route.py --action authorize \
  --agent .specify/agents/instances/<seat>.agent.md \
  --team <team-slug> --seat <seat-slug> --format json
```

Expected shape: `agent_capability`, `seat_policy`, `effective`, and the supplying halves; exit `0`
when `effective = allowed`, exit `3` when refused with the failing half named, exit `2` on
malformed input (unreadable definition, malformed `seats` map, unknown seat).

**Disclaimer (per example)**: not executable at plan time. Premises: (a) the `<team-slug>` and
`<seat-slug>` placeholders resolve against a real `.specify/teams/<slug>/team.md` carrying a block
`seats:` map — no such file exists in this repository today, so the example is written against the
fixture built for the tests; (b) the exit alphabet `0 / 2 / 3` is contracted scope, not an
observation of the not-yet-written engine; (c) the agent path form
`.specify/agents/instances/<slug>.agent.md` is the existing instance location. **Pinning test**:
`tests/contract/test_sdd_authorization.py` (four cases: allowed, seat-forbidden, agent-forbidden,
malformed map).

## S5 — Start a nested run and receive the handoff · NOT EXECUTED

```bash
# inside a team run, from the authorized seat — conceptual invocation
# (the driver is a skill, not a shell command: this is the prompt form, not a CLI)
```

The seat loads `sdd-loop-driver` under its invoked-from-team entry, passing the Goal reference,
the optional Target, the team slug, the seat, the scope, and the routing verdict reference. The
run stops at review and returns a handoff carrying outcome, stages reached, artifact and evidence
paths, unresolved findings, an anomaly line, and the integration identity (line id, branch,
worktree path, HEAD commit) with the retained branch named.

**Disclaimer (per example)**: no shell command is emitted here on purpose — `/speckit.*` and the
SDD driver are chat instructions, never terminal commands, so an executable example would be a
wrong artifact. Premises: (a) the six accepted facts and their validation set are as contracted in
`contracts/nested-invocation.md` C-31/C-32; (b) the handoff field set is the closed set of C-35;
(c) the run performs zero merge and zero push. **Pinning test**:
`tests/contract/test_nested_sdd_invocation.py` (entry-validation cases + handoff field-presence
cases + the zero-merge/zero-push assertion over `git log` / `git status`).

## S6 — Read the report's nested section · NOT EXECUTED

```bash
sed -n '/^## Nested SDD Runs/,/^## /p' .specify/teams/<slug>/runs/<stamp>-report.md
```

Expected shape: one entry per invocation with outcome, artifact paths, evidence paths, the routing
verdict reference, and anomalies; or an explicit "no nested SDD invocation this run" line.

**Disclaimer (per example)**: not executable at plan time — it reads a report produced by a run
that has not happened, and the heading literal must match the report contract's exact form
(`## Nested SDD Runs`). Premises: (a) the section heading is that literal (contract C-47);
(b) report paths follow `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md`; (c) the section is
mandatory even when empty of invocations. **Pinning test**:
`tests/contract/test_nested_run_report.py::test_nested_section_present_and_explicit_when_empty`.

---

## S7 — Measured baselines at plan time · EXECUTED 2026-10-28

### S7.1 Mirror surfaces are clean before any edit

```bash
python3 scripts/python/sync-mirrors.py --check
```

Real output (exit `0`):

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (405 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (113 files)
ok    shared/ == .specify/shared/ (58 files)
```

This is the mirror-obligation baseline: **zero** pre-existing drift, so the implementation
criterion "no NEW drift" is also measurable as "clean".

### S7.2 Targeted contract suites are green before any edit

```bash
python3 -m pytest -q tests/contract/test_agent_dispatch_mechanism.py \
  tests/contract/test_neutral_metadata_schema.py tests/contract/test_tool_mapping.py \
  tests/contract/test_neutral_vocabulary_scan.py tests/contract/test_sdd_loop_driver_skill.py \
  tests/contract/test_team_command_routing.py tests/contract/test_agent_chain_guards.py \
  tests/contract/test_no_nested_skills.py tests/contract/test_goal_definition.py \
  tests/contract/test_instructions_section_propagation.py \
  tests/contract/test_flow_class_ledger.py tests/contract/test_flow_class_correctness.py \
  tests/contract/test_shipped_agent_presets.py
```

Real output (exit `0`): `191 passed in 21.67s`. Recorded in
`test-evidence/targeted-set-v1-baseline.txt`.

### S7.3 The instructions file is already over its size budget

```bash
grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh
wc -c .specify/instructions.md templates/instructions-template.md
```

Real output: budget `32768`; `.specify/instructions.md` 41,948 B; template 34,666 B. Both files
are already over budget before this feature, so the new ambient section's criterion is a declared
byte ceiling plus a measured delta, not "fits the budget" — attributing the pre-existing overage
to this feature would be false, and ignoring the growth would hide a real regression.

## Merged from slices

<!-- source: 074a-authorized-routing -->

### S6 — Read the slice's acceptance evidence · NOT EXECUTED


```bash
git log --oneline <line-base>..<line-head>
git status --porcelain
```

Expected shape: the nested run's commits on its own line branch, no merge commit, and a clean status —
zero merge and zero push, with every artifact and evidence path carried by the invoking Agent's
result and by the team run report written under its existing contract. The report's
`## Nested SDD Runs` section is **not** asserted here: its heading literal and section semantics are
`074b-nested-governance`'s (D-3).

**Disclaimer (per example)**: not executable at slice-plan time — it reads a run that has not
happened, and `<line-base>` / `<line-head>` are placeholders for the fixture run's own commits.
Premises: (a) the nested run's commits land on the line branch recorded in the existing line registry;
(b) the outer layer, not the nested run, performs any integration; (c) the report path follows the
existing `create-team` contract (`.specify/teams/<slug>/runs/<UTC-timestamp>-report.md`), which this
slice does not amend. **Pinning test**:
`tests/contract/test_nested_sdd_invocation.py::test_nested_run_reaches_review_zero_merge_zero_push`.

---

### S7 — Measured baselines at slice-plan time · EXECUTED 2026-10-29


#### S7.1 Mirror surfaces are clean before any edit

```bash
python3 scripts/python/sync-mirrors.py --check
```

Real output (exit `0`):

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (405 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (113 files)
ok    shared/ == .specify/shared/ (58 files)
```

The slice's mirror criterion is therefore both "no NEW drift" and measurably "clean".

#### S7.2 Targeted contract suites are green before any edit

```bash
python3 -m pytest -q tests/contract/test_agent_dispatch_mechanism.py \
  tests/contract/test_neutral_metadata_schema.py tests/contract/test_tool_mapping.py \
  tests/contract/test_neutral_vocabulary_scan.py tests/contract/test_sdd_loop_driver_skill.py \
  tests/contract/test_team_command_routing.py tests/contract/test_agent_chain_guards.py \
  tests/contract/test_no_nested_skills.py tests/contract/test_goal_definition.py \
  tests/contract/test_instructions_section_propagation.py \
  tests/contract/test_flow_class_ledger.py tests/contract/test_flow_class_correctness.py \
  tests/contract/test_shipped_agent_presets.py
```

Real output (exit `0`): `191 passed in 22.64s`, recorded in
`test-evidence/targeted-set-v1-baseline.txt` with `stage_base=939766891`.

This is the suite whose anti-nesting cases must stay green for non-authorized paths (C-015 / SC-004).

#### S7.3 The engine, the owner document, and the driver reference do not exist yet

```bash
ls shared/definitions/sdd-routing-definitions.md scripts/python/sdd-route.py \
   skills/external/sdd-loop-driver/references/nested-invocation.md
grep -c 'sdd-invocation' src/specify_cli/__init__.py
```

Real output (exit `2` for `ls`, then `0`): three `ls: cannot access '<path>': No such file or
directory` lines — one per new file — and `0`, because the metadata key is absent from the CLI today.
These four facts are the premises S1–S5 rest on, measured rather than assumed; `/speckit.implement`
re-measures them before claiming any of those examples works.

<!-- source: 074b-nested-governance -->

### S1 — The four diffusion surfaces do not exist yet (executed)


**Premises**: the report contract's mandatory section line is
`skills/internal/create-team/SKILL.md:60`; the shipped stage-executor preset is
`agents/sdd-executor.agent.md`; the routing owner path is
`shared/definitions/sdd-routing-definitions.md`; the two pointer documents are
`templates/instructions-template.md` and `shared/guidelines/proactive-trigger.md`.

```bash
grep -rn "Nested SDD Runs" skills/ templates/ shared/ src/ ; echo "rc=$?"
grep -c "sdd-invocation" agents/sdd-executor.agent.md ; echo "rc=$?"
grep -n "^## Result Summary" skills/internal/create-team/SKILL.md
grep -n "sdd-routing-definitions" templates/instructions-template.md shared/guidelines/proactive-trigger.md ; echo "rc=$?"
```

```text
rc=1                                                   # no hit: the section literal is absent from every shipped surface
0
rc=1                                                   # no hit: the leaf preset declares no hosting capability
60:## Result Summary ## Deliverables ## Verification ## Execution Detail ## Run Workspace ## Summary
rc=1                                                   # no hit: neither pointer document names the routing owner
```

**Reading**: the section, the hosting declaration and both pointers are this slice's work, and none of
them leaked into `074a`'s delivery (D-3's hand-over is intact). After implementation the first probe
must return the heading line inside `skills/internal/create-team/SKILL.md`, and the fourth must return
one pointer line in each of the two documents.

---

### S2 — The report section is mandatory and explicit when empty (pinned)


**Not executed at plan stage** — no report exists to inspect; the section does not exist yet (S1).

**Pinning test**: `tests/contract/test_nested_run_report.py` (planned, local C-055…C-064), which
asserts, over a temp repository built by `tests/fixtures/nested_sdd.py`:

1. the heading literal is exactly `## Nested SDD Runs`;
2. a run with one invocation lists outcome, artifact paths, evidence paths, verdict reference, anomalies;
3. a run with no invocation still contains the section and states the absence;
4. the section is present in both bounded and continuous report shapes;
5. the pre-existing mandatory sections keep their names and order;
6. the verdict reference resolves to the recorded verdict (a missing record is recorded as missing, not
   re-derived).

**Premises to re-measure at implement time**: the report skeleton lives at
`skills/internal/create-team/SKILL.md:55-63` and its section list is one line (`:60`); `run-team`
delegates to that owner (`skills/internal/run-team/SKILL.md:66`) and must not gain a second statement.

---

### S3 — Attribution leaves the Goal field set identical (executed, measurement shape)


**Premises**: the goal engine writes under `<repo-root>/.specify/goal/<slug>/goal.md`; `parse_goal()` is
the field-set parser; a team ledger item is one JSON object per line in
`.specify/teams/<slug>/items.jsonl`. **Verified caveat**: passing `--repo-root <relative path>` from
inside this repository wrote into *this* repository's `.specify/goal/` — the scratch repo must be the
process working directory (or an absolute root), which is the "path-resolution self-match" trap the
project instructions name.

```bash
T="$(pwd)/.specify/.tmp/074b-goal-fixture" && rm -rf "$T" && mkdir -p "$T"
( cd "$T" && python3 /storage/project/cloud-native-ai/spec-kit/scripts/python/goal-utils.py --repo-root . \
    create demo-goal --objective "Deliver the slice end to end." \
    --criterion "Every FR is claimed by a clause." )
( cd "$T" && python3 - <<'PY'
import importlib.util, json
from pathlib import Path
spec = importlib.util.spec_from_file_location("goal_utils", "/storage/project/cloud-native-ai/spec-kit/scripts/python/goal-utils.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = Path(".specify/goal/demo-goal/goal.md")
before = m.parse_goal(p)
Path(".specify/teams/demo-team").mkdir(parents=True, exist_ok=True)
Path(".specify/teams/demo-team/items.jsonl").write_text(
    json.dumps({"id": "W-001", "summary": "nested run completed at review", "target_ref": None}) + "\n",
    encoding="utf-8")
after = m.parse_goal(p)
print("field_set:", sorted(before))
print("identical:", sorted(before) == sorted(after))
print("goal_md_bytes:", p.stat().st_size)
PY
)
rm -rf "$T"    # teardown, executed
```

```text
created: .specify/goal/demo-goal/goal.md
field_set: ['boundaries', 'created', 'criteria', 'criteria_count', 'history', 'objective', 'slug', 'status', 'subjects', 'targets', 'title', 'updated']
identical: True
goal_md_bytes: 224
```

**Reading**: twelve parsed fields before and after the ledger row; the Goal definition's bytes do not
move. The attribution lives in the ledger row, never in the Goal — the shape SC-008 measures. The
teardown ran in the same capture, so a second run starts clean.

**What the pinning test adds**: `tests/contract/test_nested_run_report.py` asserts the row carries the
*existing* Target reference (not a new field), that at most one row is written per report, and that a
Goal-wide run writes no attribution field.

---

### S4 — The Stage vocabulary is disambiguated and nothing is renamed (pinned)


**Not executed at plan stage** — the sentence lands during implementation.

**Pinning test**: `tests/contract/test_sdd_diffusion.py` (planned, local C-001/C-002), which asserts:

1. the conceptual model's Stage bullet still carries exactly `executor` / `evaluator` / `optimizer`
   with no value renamed and no SDD stage name added;
2. the file states that the Stage dimension is not the SDD stage roster and that the roster is the
   driver's;
3. the added text contains no roster-shaped enumeration of SDD stage names.

**Premises to re-measure**: the Stage bullet is `conceptual-model.md:10`; the file's own ownership
declaration is `:1-3`; `tests/contract/test_single_conceptual_model.py:26` pins the Role × Stage × Type
model and must stay green.

---

### S5 — The instructions pointer is one additive section, regenerated (pinned)


**Not executed at plan stage** — `scripts/bash/generate-instructions.sh` writes `.specify/instructions.md`,
a tracked product file; running it here would edit a file this stage does not own. The generator has no
dry-run flag (measured: its option surface is positional only).

**Pinning test**: `tests/contract/test_instructions_section_propagation.py` C-001 (every template `## `
section exists verbatim in the live file) plus `tests/contract/test_instructions_size_budget.py`. The
first is the mechanism that turns a template-only edit into a red suite until the regeneration runs, so
the pairing is self-enforcing.

**Premises to re-measure before the edit** (measured at plan time):

| Fact | Measured |
|------|----------|
| live instructions size | `41948` B (`.specify/instructions.md`) |
| template size | `34666` B (`templates/instructions-template.md`) |
| generator budget constant | `32768` (`scripts/bash/generate-instructions.sh:38`) |
| top-level `## ` sections | template 29, live 30 (the reconcile already injected one section the template no longer carries) |

Acceptance is therefore the new section's declared byte ceiling plus a measured delta — never "fits the
budget", which was already false before this slice.

---

### S6 — The containment claim has a decidable carrier (executed: pre-change half)


**Premises**: the four predecessor surfaces and the SC-005 suites are named as seven sets in
`test-evidence/compat-baseline-nodeids.txt`; `pytest --collect-only -q <file>` prints `path::node_id`
lines.

```bash
python3 -m pytest --collect-only -q tests/contract/test_sdd_invocation_governance.py | tail -1
for f in test_sdd_invocation_governance test_agent_dispatch_mechanism test_sdd_loop_driver_skill \
         test_sdd_loop_driver_wp_preset test_non_regression_070 test_non_regression_064 \
         test_line_registry_contract test_line_envelope_contract test_sdd_loop_driver_gates \
         test_loop_state_contract test_team_item_ledger test_team_command_routing \
         test_team_territory test_single_conceptual_model test_shipped_agent_presets \
         test_neutral_metadata_schema test_agent_chain_guards ; do
  printf '%s: ' "$f"; python3 -m pytest --collect-only -q tests/contract/$f.py | grep -oE '[0-9]+ tests? collected'
done
```

```text
17 tests collected in 0.02s
test_sdd_invocation_governance: 17 tests collected
test_agent_dispatch_mechanism: 32 tests collected
test_sdd_loop_driver_skill: 25 tests collected
test_sdd_loop_driver_wp_preset: 14 tests collected
test_non_regression_070: 10 tests collected
test_non_regression_064: 9 tests collected
test_line_registry_contract: 13 tests collected
test_line_envelope_contract: 18 tests collected
test_sdd_loop_driver_gates: 7 tests collected
test_loop_state_contract: 29 tests collected
test_team_item_ledger: 13 tests collected
test_team_command_routing: 32 tests collected
test_team_territory: 6 tests collected
test_single_conceptual_model: 3 tests collected
test_shipped_agent_presets: 5 tests collected
test_neutral_metadata_schema: 29 tests collected
test_agent_chain_guards: 4 tests collected
```

Frozen into `test-evidence/compat-baseline-nodeids.txt`: **266 cases across 17 files in 7 named sets**
(S1 49, S2 25, S3 24, S4 40, S5 36, S6 54, S7 38). The counts above are the same numbers, printed per
file — the *claim* is the node-id sets, never these integers.

**Post-change half (not executed at plan stage)**: after the edit, re-run the same collection over the
same file list, then compare set-wise:

```bash
python3 -m pytest --collect-only -q <the same 17 files> > post.txt     # at implement/verification
grep -c '::' post.txt                                                  # count, for orientation only
comm -23 <(sort pre.txt) <(sort post.txt)                              # MUST be empty (nothing dropped)
```

**Premises to re-measure**: the baseline must be re-captured at implement start with the never-cache
rule (a sibling suite may have moved between this commit and that one); the comparison is node-id
set-based, because a count comparison nets a rename against an addition (parent C-62).

---

### S7 — Mirror, command-copy and flow-class baselines are clean (executed)


```bash
python3 scripts/python/sync-mirrors.py --check ; echo "rc=$?"
python3 scripts/python/regen-command-copies.py --check ; echo "rc=$?"
python3 scripts/python/flow-class-check.py --action check ; echo "rc=$?"
```

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (406 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (114 files)
ok    shared/ == .specify/shared/ (59 files)
rc=0
OK: all per-tool command copies match the source templates.
rc=0
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
rc=0
```

**Reading**: zero pre-existing mirror drift, so every mirror row in `plan.md` is both "no NEW drift" and
measurably "clean". The flow-class count staying at 79 units / 0 findings is the mechanical form of
local C-011 (no new command, no new skill). The file counts (406/114/59) are higher than `074a`'s
recorded 405/113/58 because `074a` added three files — the baseline must be read at the commit it was
taken, never copied forward.
