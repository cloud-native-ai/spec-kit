# Quickstart: verifying slice 074b-nested-governance

**Requirement → Feature**: `074b-nested-governance` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Purpose**: the seven scenarios below are the slice's acceptance walk-through. Each states whether it
was **executed** during this planning stage (with its real output pasted) or is **pinned by a named
contract test** instead, and lists the premises the example rests on so `/speckit.implement` knows
which facts to re-measure rather than inherit.

Environment measured at plan time: host Python 3.11.11, pytest 8.4.2, repository root
`/storage/project/cloud-native-ai/spec-kit`, stage base `33269994a`.

---

## S1 — The four diffusion surfaces do not exist yet (executed)

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

## S2 — The report section is mandatory and explicit when empty (pinned)

**Not executed at plan stage** — no report exists to inspect; the section does not exist yet (S1).

**Pinning test**: `tests/contract/test_nested_run_report.py` (planned, local C-21…C-30), which
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

## S3 — Attribution leaves the Goal field set identical (executed, measurement shape)

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
move. The attribution lives in the ledger row, never in the Goal — the shape SC-002 measures. The
teardown ran in the same capture, so a second run starts clean.

**What the pinning test adds**: `tests/contract/test_nested_run_report.py` asserts the row carries the
*existing* Target reference (not a new field), that at most one row is written per report, and that a
Goal-wide run writes no attribution field.

---

## S4 — The Stage vocabulary is disambiguated and nothing is renamed (pinned)

**Not executed at plan stage** — the sentence lands during implementation.

**Pinning test**: `tests/contract/test_sdd_diffusion.py` (planned, local C-13/C-14), which asserts:

1. the conceptual model's Stage bullet still carries exactly `executor` / `evaluator` / `optimizer`
   with no value renamed and no SDD stage name added;
2. the file states that the Stage dimension is not the SDD stage roster and that the roster is the
   driver's;
3. the added text contains no roster-shaped enumeration of SDD stage names.

**Premises to re-measure**: the Stage bullet is `conceptual-model.md:10`; the file's own ownership
declaration is `:1-3`; `tests/contract/test_single_conceptual_model.py:26` pins the Role × Stage × Type
model and must stay green.

---

## S5 — The instructions pointer is one additive section, regenerated (pinned)

**Not executed at plan stage** — `scripts/bash/generate-instructions.sh` writes `.specify/instructions.md`,
a tracked product file; running it here would edit a file this stage does not own. The generator has no
dry-run flag (measured: its option surface is positional only).

**Pinning test**: `tests/contract/test_instructions_section_propagation.py` C-1 (every template `## `
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

## S6 — The containment claim has a decidable carrier (executed: pre-change half)

**Premises**: the four predecessor surfaces and the SC-001 suites are named as seven sets in
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

## S7 — Mirror, command-copy and flow-class baselines are clean (executed)

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
local C-11 (no new command, no new skill). The file counts (406/114/59) are higher than `074a`'s
recorded 405/113/58 because `074a` added three files — the baseline must be read at the commit it was
taken, never copied forward.
