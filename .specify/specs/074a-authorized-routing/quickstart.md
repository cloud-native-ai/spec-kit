# Quickstart: 074a-authorized-routing

**Requirement → Feature**: `074a-authorized-routing` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一

Seven scenarios. **S7 was executed live at slice-plan time** and its real output is pasted below.
S1–S6 describe behaviour whose implementation lands in `/speckit.implement`; each carries a
**per-example disclaimer** naming the premises it rests on and the test that pins it, so
`/speckit.tasks` and `/speckit.implement` know which facts to re-measure instead of inheriting them.
A disclaimer here covers only the example it is attached to.

The scenarios are the slice's own subset: the parent quickstart's report-section scenario (parent S6)
belongs to `074b-nested-governance` and is not repeated here; this file's S6 instead exercises the
slice's content-face acceptance shape (D-3).

---

## S1 — Route a feature-scale change · NOT EXECUTED

```bash
python3 .specify/scripts/python/sdd-route.py --action route \
  --nature capability --traceability required \
  --blast-radius cross-cutting --reversibility hard \
  --complexity standard --format json
```

Expected shape: verdict `sdd`, a reason code from the owner's closed vocabulary, and the five input
values echoed back in the record.

**Disclaimer (per example)**: not executable at slice-plan time — `scripts/python/sdd-route.py` does
not exist yet. Premises this example rests on: (a) the engine's flag names are those contracted in
`contracts/routing-decision.md` C-28 (`--action route`, one flag per input, `--format json`);
(b) the five inputs are named exactly as the owner document names them; (c) the exit code is `0` for a
produced verdict regardless of which verdict; (d) the copy shipped to `.specify/scripts/python/` is the
mirror of `scripts/python/`, so the `.specify/` path resolves after `sync-mirrors.py` runs.
**Pinning test**: `tests/contract/test_sdd_routing_engine.py::test_route_feature_scale_returns_sdd`.

## S2 — Route a bounded maintenance change · NOT EXECUTED

```bash
python3 .specify/scripts/python/sdd-route.py --action route \
  --nature maintenance --traceability not-required \
  --blast-radius local --reversibility reversible \
  --complexity standard --format json
```

Expected shape: verdict `direct`, with the record naming the conditions that held.

**Disclaimer (per example)**: same non-existence premise as S1. Additional premise: the closed value
literals quoted here (`maintenance`, `not-required`, `local`, `reversible`, `standard`) are the owner
document's declared domain values — if the owner's literals differ, this example is wrong even though
the engine runs. **Pinning test**:
`tests/contract/test_sdd_routing_engine.py::test_route_bounded_maintenance_returns_direct`.

## S3 — A missing input never falls through to direct · NOT EXECUTED

```bash
python3 .specify/scripts/python/sdd-route.py --action route \
  --nature maintenance --traceability not-required \
  --blast-radius local --reversibility reversible --format json
```

Expected shape: verdict `adjudicate` with the missing-input reason code — the complexity tier was not
declared, and the precedence rule forbids the direct branch when a required input is absent, even
though every supplied value points at direct. The conflicting form is the second adjudicate case:
`--nature capability --blast-radius local-bounded-definition-correction` (a capability change cannot
be a bounded correction).

**Disclaimer (per example)**: not executable at slice-plan time. Premises: (a) the precedence rule is
applied before any branch-specific reasoning (`contracts/routing-decision.md` C-23); (b) `adjudicate`
is not an error, so the exit code stays `0`; (c) the missing/ambiguous/conflicting distinction is
decided from the owner's enumerated set, not from free text (C-24). **Pinning test**:
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
when `effective = allowed`, exit `3` when refused with the failing half named, exit `2` on malformed
input (unreadable definition, malformed `seats` map, unknown seat).

**Disclaimer (per example)**: not executable at slice-plan time. Premises: (a) the `<team-slug>` and
`<seat-slug>` placeholders resolve against a real `.specify/teams/<slug>/team.md` carrying a block
`seats:` map — no such file exists in this repository today, so the example is written against the
fixture built for the tests; (b) the exit alphabet `0 / 2 / 3` is contracted scope
(`contracts/hierarchy-and-authorization.md` C-8 and C-28), not an observation of the not-yet-written
engine; (c) the agent path form `.specify/agents/instances/<slug>.agent.md` is the existing instance
location. **Pinning test**: `tests/contract/test_sdd_authorization.py` (four cases: allowed,
seat-forbidden, agent-forbidden, malformed map).

## S5 — Start a nested run and receive the handoff · NOT EXECUTED

```bash
# inside a team run, from the authorized seat — conceptual invocation
# (the driver is a skill, not a shell command: this is the prompt form, not a CLI)
```

The seat loads `sdd-loop-driver` under its invoked-from-team entry, passing the Goal reference, the
optional Target, the team slug, the seat, the scope, and the routing verdict reference. The run stops
at review and returns a handoff carrying outcome, stages reached, artifact and evidence paths,
unresolved findings, an anomaly line, and the integration identity (line id, branch, worktree path,
HEAD commit) with the retained branch named.

**Disclaimer (per example)**: no shell command is emitted here on purpose — `/speckit.*` and the SDD
driver are chat instructions, never terminal commands, so an executable example would be a wrong
artifact. Premises: (a) the six accepted facts and their validation set are as contracted in
`contracts/nested-invocation.md` C-31 / C-32; (b) the handoff field set is the closed set of C-34;
(c) the run performs zero merge and zero push. **Pinning test**:
`tests/contract/test_nested_sdd_invocation.py` (entry-validation cases, handoff field-presence cases,
the zero-merge/zero-push assertion over `git log` / `git status`).

## S6 — Read the slice's acceptance evidence · NOT EXECUTED

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

## S7 — Measured baselines at slice-plan time · EXECUTED 2026-10-29

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

The slice's mirror criterion is therefore both "no NEW drift" and measurably "clean".

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

Real output (exit `0`): `191 passed in 22.64s`, recorded in
`test-evidence/targeted-set-v1-baseline.txt` with `stage_base=939766891`.

This is the suite whose anti-nesting cases must stay green for non-authorized paths (C-15 / SC-004).

### S7.3 The engine, the owner document, and the driver reference do not exist yet

```bash
ls shared/definitions/sdd-routing-definitions.md scripts/python/sdd-route.py \
   skills/external/sdd-loop-driver/references/nested-invocation.md
grep -c 'sdd-invocation' src/specify_cli/__init__.py
```

Real output (exit `2` for `ls`, then `0`): three `ls: cannot access '<path>': No such file or
directory` lines — one per new file — and `0`, because the metadata key is absent from the CLI today.
These four facts are the premises S1–S5 rest on, measured rather than assumed; `/speckit.implement`
re-measures them before claiming any of those examples works.
