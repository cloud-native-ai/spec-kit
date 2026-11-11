# Research: 074a-authorized-routing

**Requirement → Feature**: `074a-authorized-routing` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一

Phase 0 rulings RA1–RA9. This slice is a **projection**, not a re-design: the parent design
(`.specify/specs/074-goal-team-sdd-unification/` — `plan.md`, `data-model.md`, `contracts/`,
`quickstart.md`, `research.md`, `feature-ref.md`, committed at `6297c14f6`) is the design authority,
and the slice inherits 47 of its 67 clauses while deferring 20 to `074b-nested-governance`. Each
ruling below therefore records **how the projection is drawn and why that reading is the only one
consistent with the recorded intent** — it never re-argues a decision the parent already measured.
Per-clause derivation is in `contracts/`; the two-way table is `plan.md` § Parent Design Mapping.

Nothing here restates a fact owned elsewhere: the input value domains, verdict table, precedence, and
reason codes are owned by `shared/definitions/sdd-routing-definitions.md` (created by this feature's
implementation); the tier names by `.specify/shared/guidelines/task-complexity-rubric.md`; the stage
roster by `sdd-loop-driver`.

**Phase 0 evidence path (degraded, disclosed)**: this environment exposes no subagent dispatch
capability and the stage brief fixes `decomposition=single-package` with no subagent dispatch, so the
codebase exploration pass ran as a bounded manual probe (grep for headings/symbols plus targeted
excerpt reads under the token-efficiency discipline) rather than as an Explore-subagent pass. Every
ruling below carries a re-runnable command or a `file:line` anchor measured on 2026-10-29 in this
repository; nothing is quoted from memory of the parent session.

---

## RA1 — The slice re-derives per requirement entry, and its ids are local projections

**Decision**: the slice's design set covers local FR-001–FR-020 and SC-001–SC-006. Clauses are
re-derived per requirement entry regardless of which parent contract file physically carries them,
numbered consecutively `C-1`…`C-47` across four slice files, each tagged `父 C-nn` for its source
(parent C-1…C-14 → slice C-17…C-30; parent C-58/C-59/C-67 and the FR-014/FR-018 facets of C-64/C-66
→ slice C-30/C-43/C-44/C-46/C-47). Entities are renumbered `E1`…`E9` with the two deferred parent
entities named rather than renumbered; validation rules keep `V-1`…`V-29` unchanged because all 29
fall inside the slice and a renumbering would create a second id space for an identical set.

**Evidence**:
- `.specify/specs/074a-authorized-routing/requirements.md` § Parent Mapping (20 FR / 6 SC / 10 STR
  mapped one-by-one) and § Cross-Slice Design Attribution D-1.
- `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28）: the two slices'
  FR sets are declared mutually exclusive and their union is the parent's 28; that declaration is
  `confirmed-user`.
- `python3 scripts/python/clause_extract.py .specify/specs/074a-authorized-routing/contracts/*.md`
  (executed; output in `test-evidence/plan-stage-checks.md`) — 47 clauses, ids contiguous
  `C-1`…`C-47`, every file canonical `md-bold-closed`.

**Rejected**: (a) grouping the slice's contracts to mirror the parent's five file names — it would
force the deferred clauses' requirement entries (parent FR 020–024, FR 026–028) back into the slice,
contradicting the recorded split; (b) reusing the parent's clause ids with 20 holes — a 47-element
sequence with holes reads as "something was dropped", while the slice's own consecutive numbering plus
the `父 C-nn` tag keeps the derivation auditable in one table; (c) referring to the parent's contract
files as the operative design without re-deriving — the slice would then have no design set of its
own, and the parent's clauses for deferred requirements would be indistinguishable from the ones the
slice must implement.

## RA2 — One owner document, one engine, and both are created in this slice

**Decision**: inherit the parent ruling unchanged. The routing rule's single owner is
`shared/definitions/sdd-routing-definitions.md`; the decision is implemented by one read-only,
stdlib-only engine `scripts/python/sdd-route.py` with three actions (`route`, `authorize`,
`golden`) that parses the owner document at run time. Scope difference from the parent: this slice
implements all three actions, because authorization (`authorize`) is the slice's US1 and routing
(`route` / `golden`) is its US2.

**Evidence**:
- `ls shared/definitions/sdd-routing-definitions.md` → *No such file or directory*;
  `ls scripts/python/sdd-route.py` → *No such file or directory* (both are new, neither exists today).
- Precedent for the shape: `scripts/python/flow-class-check.py` — an owner document holding the
  criteria plus a read-only engine exposing actions with a documented exit alphabet.
- `python3 scripts/python/flow-class-check.py --action check` → 79 units scanned, 0 findings
  (the slice's FR-020 negative check: no new flow unit is introduced by adding an engine action).

**Rejected**: a second engine split by predicate (parent research R1 rejects it for the same reason
FR-018's spirit gives: one owner, one failure vocabulary); a gold table in a data file (a second copy
of the verdict table).

## RA3 — The two authorization halves keep their measured read paths

**Decision**: the Agent half resolves through the CLI's neutral key set; the seat half through a
block-map parser inside the engine, because no existing reader can see a nested map.

**Evidence (re-measured 2026-10-29)**:
- `grep -n 'NEUTRAL_AGENT_METADATA_KEYS\|NEUTRAL_AGENT_FRAMEWORK_KEYS' src/specify_cli/__init__.py`
  → `119`, `149`: one key→(domain, default, renders_to_tools) map plus one framework-key frozenset.
- `grep -c 'sdd-invocation' src/specify_cli/__init__.py` → `0`: the key is genuinely new, so the
  single declared pin change (RA8) is a *gain* of exactly one member, not a relaxed guard.
- `src/specify_cli/__init__.py:227` → the parser raises `nested/multi-line YAML is not supported in
  agent metadata`, so the Agent half must be a flat scalar.
- `scripts/python/goal-utils.py:325` (`_split_frontmatter`) and `:762` (the `team.md` path) — the only
  team.md reader among the engines is a flat per-line scanner; a nested `seats:` map is invisible to
  it, so the seat parser is new work and belongs where the predicate lives.

**Rejected**: extending `goal-utils.py` with a nested parser (that engine owns goal identity, not
authorization); a flattened per-seat key (`sdd-invocation-<seat>`) reusing the flat scanner — FR-004
fixes the map-under-`seats` shape and a per-seat key would grow the frontmatter without bound.

## RA4 — The anti-nesting narrowing lands once, at its owner site

**Decision**: amend `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance
Obligation once — replacing the unqualified "loop depth is always 1" sentence with the depth-2 chain,
the three-condition predicate, and the virtual prohibition — and amend the pre-dispatch probe in
`skills/internal/run-agent/SKILL.md` to enforce it fail-closed by calling the engine's `authorize`
action.

**Evidence (re-measured 2026-10-29)**:
- `grep -n '^## ' shared/definitions/subagent-definitions.md` → `## Dispatch-Time Governance
  Obligation` at line `98`; the exclusivity sentence sits at line `104`.
- `skills/internal/run-agent/SKILL.md:119` carries the pre-dispatch anti-nesting obligation that the
  probe amends.
- The pre-change case set that must stay green is the 13-file targeted suite: `191 passed` at
  `stage_base=939766891` (`test-evidence/targeted-set-v1-baseline.txt`). Its anti-nesting assertions
  are *presence* assertions (`反嵌套` / `嵌套` / `派发前` / `循环层级`), so an amendment that keeps those
  terms keeps every case's verdict; the removed exclusivity claim is asserted nowhere in that form.

**Rejected**: deleting the obligation and re-stating it elsewhere (the old prohibition would survive
in the old place, which is a contradiction rather than a narrowing); registering the probe in
`shared/definitions/probe-definitions.md` (a dispatch-time content check has no wrap-up face and no
handler to bind — an object with no consumer).

## RA5 — The nested entry is additive inside the driver; the handoff is a returned block

**Decision**: `sdd-loop-driver` gains one § Invoked-from-Team Entry section plus one Hard Requirement
line; the handoff schema and its closed field set live in a new
`skills/external/sdd-loop-driver/references/nested-invocation.md`. The nested run stops at review
(after the driver's existing review-repair loop settles) and performs no merge and no push.

**Evidence**:
- `ls skills/external/sdd-loop-driver/references/` → `cli`, `decomposition-model.md`,
  `dispatch-recipes.md`, `efficiency-model.md`, `stage-prompts.md`, `state-awareness.md`,
  `watch-model.md` — no handoff schema exists today, so the new reference has no predecessor to
  amend and duplicates nothing.
- The driver's own U0 default table resolves *missing* parameters; a nested entry *validates
  supplied* parameters and refuses on failure, which is the opposite direction, so the two forms
  cannot be folded together without blurring the fail-closed boundary (parent research R6's measured
  reasoning, re-read against `skills/external/sdd-loop-driver/SKILL.md` this run).

**Rejected**: a second skill hosting nested runs (SDD-within-SDD under another name, duplicating
U0–U6); folding the nested form into the U0 default table (semantics collide: resolve-vs-validate).

## RA6 — D-2: the verdict record's carrier in this slice is the Agent execution evidence

**Decision**: local FR-013's "team run report **or** Agent execution evidence" is discharged here by
the **Agent execution evidence**: the five inputs, the verdict, the reason code, the actor, and any
user override are recorded there, and the handoff plus the invoking Agent's result reach that record
by stable path (slice contract C-27). The team report's nested section — and the verdict reference it
will carry — arrives with `074b-nested-governance` and reads the same record without recomputation.

**Evidence**: the slice defines no fixed report section (parent STR-010's heading literal is parent
parent FR 021, deferred), so the only record surface this slice can deliver is the execution evidence;
`requirements.md` § Requirements FR-013 already admits that reading through its own "or". The ruling
is recorded in `requirements.md` § Clarifications `### Session 2026-10-29` as an unattended
self-adjudication.

**Rejected**: building the report section here (it would pull 074b's contract into this slice, and
`requirements.md` § Out of Scope explicitly places it there); recording the verdict in no durable
place (the outer layer could then not read the verdict the duty acted on).

## RA7 — D-3: SC-003 is delivered on its content face; the fixtures do not assert the section heading

**Decision**: local SC-003 is discharged by asserting (a) the nested run reaches review and produces
the complete SDD artifact chain, (b) `git log` / `git status` show zero merge and zero push, and
(c) every artifact and evidence path is referenced from the invoking Agent's result and from the team
run report written under its existing contract. The `## Nested SDD Runs` heading literal and its
mandatory-and-explicit-when-empty semantics are `074b-nested-governance`'s, so this slice's fixture
never asserts that literal.

**Evidence**: local FR-017 already requires the invoking Agent to carry the handoff into its own
result and the run report; the three content-fact assertions are mechanical over that deliverable.
`requirements.md` § Out of Scope lists "team report 嵌套段" as out of scope — the sentence names the
*section*, i.e. its heading and section semantics, not the path references it will contain; D-3
records exactly that reading.

**Rejected**: implementing the section to satisfy SC-003 literally (a 074b contract delivered twice);
declaring SC-003 undeliverable in this slice (its three content facts are mechanically assertable
here, and § Out of Scope is silent on them).

## RA8 — Test surface split, and the one declared pin change

**Decision**: the slice carries five of the parent plan's six new contract suites plus the fixture and
the single declared pin change; the sixth (`test_nested_run_report.py`) belongs to the
`074b-nested-governance` report-section contract.

| Surface | Test file (new unless noted) | Behaviour group |
|---------|------------------------------|-----------------|
| Owner document shape | `tests/contract/test_sdd_routing_definitions.py` | owner declaration, closed domains, one declaration point, invocation-kind classification |
| Routing engine + golden table | `tests/contract/test_sdd_routing_engine.py` | deterministic verdicts, precedence, reason codes, idempotence, ambiguity/conflict never `direct` |
| Authorization | `tests/contract/test_sdd_authorization.py` | agent half, seat half, AND, defaults, malformed seat map, failed half named |
| Pre-dispatch governance | `tests/contract/test_sdd_invocation_governance.py` | predicate, depth-2 chain, virtual prohibition, stage-executor refusal, pre-existing cases green |
| Nested invocation + handoff | `tests/contract/test_nested_sdd_invocation.py` | entry validation, stop at review, handoff field set, zero merge/push, stall handoff, path references (D-3) |
| Fixture | `tests/fixtures/nested_sdd.py` | temp repo: minimal `.specify/`, one authorized and one unauthorized seat, two agent definitions, one goal with an open Target |
| Pin change (edit) | `tests/contract/test_neutral_metadata_schema.py` | the framework-key frozenset gains exactly one member, in the same change as the code edit |

**Evidence**: `grep -n 'NEUTRAL_AGENT_FRAMEWORK_KEYS' tests/contract/test_neutral_metadata_schema.py`
→ lines `17`, `130`, `137`: line `130` is the exact-set-equality pin and line `137` cross-checks the
set against `NEUTRAL_AGENT_METADATA_KEYS`, so a code-side addition without the test edit is red and
the reverse is red too — the assertion still guards what it guarded.
`ls tests/fixtures/` shows the precedents the new fixture imitates (`teams/`, `review_git_repo.py`,
`line_fixtures.py`).

**Rejected**: adding the predicate cases to `test_agent_dispatch_mechanism.py` (SC-004's "pre-existing
anti-nesting cases stay green" is a statement over that suite's case set; keeping the new cases in a
separate file keeps the relation legible); a sixth new file for the report section (a 074b contract).

## RA9 — Same-author scoring and the stage's mechanical evidence

**Decision**: the Constitution Check table and the Post-Generation Quality Gate are scored by the same
agent that wrote the artifacts, and delegation is impossible in this environment, so every row is
marked `(direct read, subagent unavailable)`; the program-derivable checks were executed instead and
their real output is pasted into `test-evidence/plan-stage-checks.md`.

**Evidence**: `.specify/shared/workflow/objective-analysis-gate.md` delegates the scoring when the
analyzed artifacts were authored in the same pass; the stage brief fixes `decomposition=single-package`
with no subagent dispatch. Executed this stage: `clause_extract.py` (47 clauses), `pre-analyze-check.py
--stage plan`, `account-clause-coverage.py` (FR lane), `sync-mirrors.py --check` (no drift),
`regen-command-copies.py --check` (clean), `flow-class-check.py` (79 units, 0 findings), and the
13-file targeted suite (191 passed).

**Rejected**: claiming delegated scoring (false), and skipping the gate (it is a gate).
