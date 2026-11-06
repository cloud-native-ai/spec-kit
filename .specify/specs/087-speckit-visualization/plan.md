# Implementation Plan: Speckit 框架可视化（Speckit Framework Visualization）

**Branch**: `087-speckit-visualization` | **Date**: 2026-11-06 | **Spec**: `.specify/specs/087-speckit-visualization/requirements.md`
**Requirement → Feature**: `087-speckit-visualization` → Feature 087 Speckit 框架可视化（Speckit Framework Visualization）
**Input**: Specification from `.specify/specs/087-speckit-visualization/requirements.md`

## Summary

Make "the user can always tell what is running right now" a declared framework obligation instead of a property
each flow implements or forgets. Three surfaces become non-optional for every flow that introduces concurrency or
an asynchronous delegation:

1. **A declared periodic status line.** A new owner document,
   `shared/guidelines/reporting-obligations.md`, owns the obligation's scope predicate, the long-run cadence
   profile (default 30 s), the reporter-seat obligation, the master-reporting duty, the stall judgement reference
   and the digest contract. It reaches the existing progress-reporting discipline and the existing visibility
   contract by path — it restates neither.
2. **A reporter seat and a master-reporting duty.** A new Agent **Template** (`agents/reporter.agent.md`) is
   promoted into `.specify/agents/templates/` by the existing mirror; `skills/internal/create-team` gains the
   seat obligation in its roster schema, its create procedure and its roster-validation guard; a supervising
   master — including `skills/external/coaching-skills`, whose `## Dispatch Payload` closed set is extended by
   one reporting field — reports every sub-flow it watches on the cadence and out of cadence on a significant
   transition.
3. **A reachability floor and a deterministic guard.** One thin command (`templates/commands/status.md` →
   `/speckit.status`) backed by one stdlib-only script (`scripts/python/status-digest.py`) renders a bounded
   current-state digest and judges the mechanically decidable propositions of the obligation, from one reading of
   state the framework already writes.

No scheduler, timer service, daemon, third-party dependency, new persistent store, new console channel, second
registry, state spine or ledger is introduced. The cadence is executed by the running flow between its own steps,
exactly as the existing progress-reporting discipline already requires.

Feature status advances `Draft → Planned`. `Implemented` is never claimed here.

## Technical Context

**Language/Version**: Python `>=3.8`, stdlib only (no new dependency; `pyproject.toml` `requires-python` unchanged).
Documentation and prompt surfaces are Markdown.
**Primary Dependencies**: none added. The shipped script imports only the standard library and reads files the
framework already writes; it does not import `line-registry.py` (that engine is stdlib-only as well, but a direct
import would couple the digest to an internal module path rather than to its JSON on disk).
**Storage**: no new store. Read-only inputs: the per-line registry entries under `$SPECIFY_LINE_REGISTRY_DIR`
(default `~/.local/state/spec-kit/lines/<line_id>.json`), the runner triplet
(`<line_id>.status`, `<line_id>.log`, `<line_id>.heartbeat`) whose paths the registry entry declares, and
`<spec-dir>/test-evidence/*.jsonl` for the stage row of an executing line. Write outputs: the reporter's own stream
artifact only, and a run record the emitting flow already writes.
**Testing**: `pytest` (`pytest -m contract` for the new guards). Plan stage runs no suite — it is a documents-only
stage (test budget below).
**Target Platform**: the supported agent hosts (`AGENT_CONFIG` in `src/specify_cli/__init__.py` is the roster
owner); the script runs wherever a Python 3.8+ interpreter exists.
**Project Type**: framework source (templates + shared owners + skills + scripts + agent templates), distributed by
`specify init` and mirrored into this repo's `.specify/` runtime.
**Performance Goals**: one digest render under one second on a registry of ~20 lines (it lists and reads small JSON
files; no network, no process spawn).
**Constraints**: digest output bounded by a declared entry cap with the omitted count stated; no new process,
timer, daemon or store; every emitted line readable by a reader who did not take part in the run
(`shared/guidelines/user-facing-comprehension.md`); the 30-second literal has exactly one definition site.
**Scale/Scope**: 28 delivered paths across 7 framework-source areas plus their mirrors and 4 per-tool command
copies (`feature-ref.md` § Delivered paths is the enumerated owner of this list); 29 FR, 14 SC, 6 contracts / 52
clauses, 7 entities.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.16.0 — one row per
`### <numeral>. <name>` heading, in constitution order; no `(NON-NEGOTIABLE)` / `(MANDATORY)` annotation is
carried by any principle heading in that file, so none is rendered):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every delivered file traces to an FR in `requirements.md` § Functional Requirements; `feature-ref.md` carries the FR → artifact map; `contracts/` names the FR each clause serves |
| II | Feature-Centric Development | ✅ Pass | Feature 087 row + detail updated synchronously in this stage (`Draft → Planned`); `feature-ref.md` records the binding and the neighbouring-feature scan |
| III | Intent-Driven Development | ✅ Pass | `research.md` records the measured current state before any design; `plan.md` § Decision Tensions records the "why" for the two load-bearing choices |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | `contracts/` fixes the numbered clauses (`C-01`…`C-52`, dense per file) that `/speckit.tasks` turns into red-first contract tests; `RO-01`…`RO-13` are the guard's judgements, each with a named status, and `contracts/reporting-obligations.contract.md` C-01…C-13 is their single owner |
| V | AI Agent Integration Standards | ✅ Pass | No agent is added to `AGENT_CONFIG`; the new Template renders through the existing render path; `_ASSISTANT_COMMAND_DIRS` (6 tools) is the copy-target owner, unchanged |
| VI | Continuous Quality & Observability | ✅ Pass | The feature's subject *is* observability; no `.bak` copy is produced (version control is the backup); root cause over symptom — a flow that cannot report records that fact (FR-016) rather than staying green |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | This stage lands at most `Planned`; FR-018's zero-new-machinery shape keeps Test-First Partial-unneeded — the guard and its tests are ordinary code + contract tests, so no `Partial (justified)` row exists |
| VIII | Code as the Single Source of Truth | ✅ Pass | `research.md` every claim was measured against the tree (mirror check, engine `--help`, literal scans) rather than read from documentation; where a doc disagreed, the measurement is quoted |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Cadence is executed by the running flow between its steps; RO-13 (no scheduler/timer/daemon/second store) is a named guard proposition, and contract `ownership-map.contract.md` C-49/C-50 makes the delivered set auditable against it |
| X | Documentation Naming & Location Conventions | ✅ Pass | New owner `shared/guidelines/reporting-obligations.md`, new Template `agents/reporter.agent.md` (lowercase kebab), new command `templates/commands/status.md`; no `README.md` is introduced; `skills/*/SKILL.md` keeps its mandated name |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two hats named: all delivery lands in framework sources (`shared/`, `agents/`, `skills/`, `scripts/`, `templates/`) and reaches `.specify/` only through `sync-mirrors.py` / `regen-command-copies.py`; no hand edit of a `.specify/` mirror |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | `research.md` RO-05/RO-06 record the Tool-record lookup (`.specify/memory/tools/`) before authoring `status-digest.py`; no existing Tool covers a current-state digest, so authoring is the expected outcome |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | `feature-ref.md` names the strengthened work-loop dimension (Task Understanding + Reliable Delivery visibility); no scoring system or maturity report is added |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Each fact has one owner: cadence value → the new owner; content floor + interactive default → `progress-reporting.md`; artifact triplet + modes → `subagent-definitions.md`; stall numbers → `create-team/references/patterns.md`; registry states → `line-registry.py` `STATE_VALUES`; the digest's cap and stale bound → the constants in `status-digest.py` (C-43/C-44); profile selection → `status-report.contract.md` C-30; the guard's thirteen propositions → `contracts/reporting-obligations.contract.md` C-01…C-13. Every other surface reaches a proposition by id and states only what it reads, never what the proposition asserts. C-47 makes the ownership consignment a contract clause and SC-006 its measurement |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Emitted lines are a governed surface of that discipline; `contracts/status-report.contract.md` C-23 (SR-02) pins the four content elements and C-22 (SR-01) the attribution fields, and `data-model.md` § Invariants INV-05 forbids an internal identifier from reaching the line without a user-facing name |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | The reporting obligation rides the same dispatch-payload channel as the fast-fail clause and does not modify it; the reporter is not given authority to repair or to halt anything (FR-005, INV-08) |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory is created: `contracts/`, `test-evidence/`, `agents/`, `shared/guidelines/` all exist; the digest's scratch needs none (`temp_directory_discipline` not exercised) |
| XVIII | Grounded Naming | ✅ Pass | Names follow the highest available source — user instruction ("reporter subagent", "team"), sibling imitation (`shared/guidelines/<topic>.md`, `scripts/python/<verb>-<noun>.py` next to `flow-class-check.py`, `line-registry.py`), then a descriptive own choice (`/speckit.status`, `status-digest.py`) |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The user's information need is named (what is running now), one dimension is added (a current-state reading on demand beside the cadence line), and the digest is a projection reconciled to the owners of the state it reads — never a second owner of that state |

**Gates Status**: ✅ All gates pass — zero Fail rows, zero Partial rows, and therefore no Complexity Tracking entry
is owed (that section states `N/A`).

**Re-check after Phase 1**: 2026-11-06, re-run against the design artefacts on disk (`data-model.md` with 7
entities and INV-01…INV-12, `contracts/` with 6 files / 52 clauses, `quickstart.md` with 8 scenarios A–H,
`feature-ref.md`). The table above is the refreshed reading: no row changed verdict. Two rows were the only
candidates for a downgrade and each was checked against its artefact — IV (Feature) stays Pass because the
contracts enumerate the tests to write rather than leaving them implicit; XI (Dogfooding) stays Pass because
`plan.md` § Mirror Obligations names every copy and the baseline drift is zero, so no artifact could be delivered
by hand-editing a mirror. XIV was checked separately: it passes only because
`contracts/reporting-obligations.contract.md` C-01…C-13 declares itself the single owner of the thirteen guard
propositions and every other surface — `status-digest.contract.md` C-46, `data-model.md` § Invariants, each contract's
`*Judged by*` line, and `quickstart.md` § F — reaches them by id and states only what it reads, without restating a
proposition's subject.

**Re-check after the round-3 plan repair** (analyze round 2, findings F-01/F-07/F-08/F-09): the row above was
re-measured against the consumers rather than asserted. Every `*Judged by*` line and every invariant now names the
RO id whose subject actually matches, and the four facts that have their own clause owners go to those clauses
instead of to a proposition — attribution and profile selection to `status-report.contract.md` C-22/C-30, the digest
cap to `status-digest.contract.md` C-43, the digest contract itself to C-09/`RO-09`. `C-46`'s `RO-04` row no longer
offers a glob as a default population, so no consumer contradicts `FR-006`. Evidence:
`test-evidence/plan-repair-round3.txt`.

## Decision Tensions

Two decisions cross the load-bearing threshold: **T-001** (an independent owner document rather than extending
`progress-reporting.md`) is constitutional (Principle XIV owner selection) *and* cross-team (three existing owner
documents start pointing at a new path); **T-002** (the digest is a new command + script pair) is cross-team (it
adds a new `/speckit.*` surface that 6 per-tool copy trees must carry). The remaining choices in § Design Decisions
fail all four triggers and are therefore recorded as ordinary trade-offs, not as records.

### T-001 — A second owner document sits beside `progress-reporting.md`, not inside it

- **decision**: The new obligation gets its own owner, `shared/guidelines/reporting-obligations.md`; the existing `shared/guidelines/progress-reporting.md` keeps every clause it already owns and the new owner reaches it by section anchor.
- **antithesis**: Extend `progress-reporting.md` in place with the scope predicate, the reporter-seat obligation and the master-reporting duty; when the discipline's reader is already the one flow author who must obey both halves, and when the two halves will keep changing together, one file is better — one open, one edit, and no anchor to drift out of sync.
- **binding_constraints**:
  - pole_a: A cadence rule must have exactly one definition site, so no flow author can find two competing intervals and pick the convenient one.
  - pole_b: An amendment to an existing owner document must not rewrite the clauses a shipped contract test already pins, or the compatibility baseline (SC-008) stops being measurable.
- **discriminating_evidence**: Run `tests/contract/test_progress_reporting.py` before and after the change. Two-valued: the suite's node-id set is identical and green (extension-in-place) or it gains/renames nodes that now assert the 30-second literal inside the pre-existing document (in-place rewrite).
- **expected_sacrifice**: SC-008 Source ↓ the consumer surface gains one more owner path to reach — a reader following the reporting obligation now opens two documents (the new owner plus `progress-reporting.md`) instead of one, costing one extra file open per consumer author.
- **revision_trigger**: Two consecutive iterations in which an amendment to the cadence rule requires editing both documents in the same change, or ≥2 recorded findings of "the two documents disagree on the content floor" → reopen and merge the two into one owner.

### T-002 — The current-state digest ships as a new thin command plus one script

- **decision**: The digest is a new thin command (`templates/commands/status.md`, `/speckit.status`) backed by one deterministic script (`scripts/python/status-digest.py`); the guard's verdict is one action of that same script.
- **antithesis**: Fold the digest into the existing `/speckit.session` surface (the framework's existing "what is happening" reading) as a new sub-mode; when the reader is already in that command's mental model and the new reading is a variation on a surface they already invoke, one entry point is better — no new command directory in 6 per-tool copy trees, no new `speckit.*` name.
- **binding_constraints**:
  - pole_a: The answer to "what is running right now?" must be one invocation away for a reader who has not memorised the framework's command set (constitution XIX floor: at most one simple command).
  - pole_b: A new `speckit.*` surface is distributed to every supported agent, so adding one multiplies the per-tool copy surface and the name space a reader must learn.
- **discriminating_evidence**: Dispatch a reader who did not take part in this run and give them only the framework's command list, asking them to produce a current-state reading. Two-valued: they reach it through a command whose name they found by scanning the list (`/speckit.status` standalone) or only after being told it hides inside another command's mode.
- **expected_sacrifice**: SC-010 Source ↓ the delivered file set grows by one command template plus its generated per-tool copies (`_ASSISTANT_COMMAND_DIRS` in `src/specify_cli/__init__.py` is the copy-target owner), so the changed-file surface the machinery audit reads grows by exactly those paths.
- **revision_trigger**: SC-010's changed-file scan shows the new command pair would push a delivered-surface threshold that a later feature revision sets, or two consecutive digests are invoked through another command's mode by users → reopen and fold the digest into that command.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/087-speckit-visualization/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — measured current state and resolved unknowns
├── data-model.md        # Phase 1 output — 7 entities, fields, invariants
├── quickstart.md        # Phase 1 output — 8 executable scenarios (A–H)
├── contracts/           # Phase 1 output — 6 contract files, 52 clauses
├── feature-ref.md       # Phase 1 output — Feature 087 binding, FR → artifact map
├── checklists/          # /speckit.checklist output (later stage)
├── test-evidence/       # this run's gate readings and the E3 stage-status row
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

Every path below is a **framework source** (the framework hat); the `.specify/` and per-tool copies are
regenerated, never hand-edited — see § Mirror Obligations.

```text
shared/guidelines/          # NEW reporting-obligations.md — the obligation's single owner
shared/definitions/         # subagent-definitions.md — one pointer line to the new owner (§ Dispatch-Time Governance Obligation)
shared/workflow/            # external-dispatch-recipes.md — one pointer line; the recipes stay the recipe owner
agents/                     # NEW reporter.agent.md — the reporting role as an Agent Template (layer 1)
skills/internal/create-team/ # SKILL.md + references/create-mode.md (roster schema + create step) + references/patterns.md (threshold table citation) + scripts/validate-roster.py (NEW guard)
skills/external/coaching-skills/ # SKILL.md § Dispatch Payload — one added field inside the closed set
templates/commands/         # NEW status.md — the thin /speckit.status entry
scripts/python/             # NEW status-digest.py — digest renderer + guard + line renderer (one reading)
tests/contract/             # NEW test_reporting_obligations.py, test_roster_reporter_seat.py, test_status_digest.py, test_coaching_reporting_duty.py; EDITED test_coaching_dispatch_contract.py (declared expected delta, OM-05)
tests/unit/                 # NEW test_status_digest_unit.py — projection, bounding, staleness, exit codes
```

**Structure Decision**: this spec extends the existing framework-source layout; it creates **no new top-level
directory**. Four files are new (`shared/guidelines/reporting-obligations.md`, `agents/reporter.agent.md`,
`templates/commands/status.md`, `scripts/python/status-digest.py`), **six** existing framework-source files gain a
bounded edit (`shared/definitions/subagent-definitions.md`, `shared/workflow/external-dispatch-recipes.md`,
`skills/internal/create-team/SKILL.md`, `skills/internal/create-team/references/create-mode.md`,
`skills/internal/create-team/references/patterns.md`, `skills/external/coaching-skills/SKILL.md`), and five test
files are new/stated — `tests/contract/` ×4 new plus `tests/unit/test_status_digest_unit.py`, with
`tests/contract/test_coaching_dispatch_contract.py` edited in place. The shape is "one new owner + one new template
+ one new command pair + bounded edits to six existing framework-source files", whose mirrored runtime copies are
produced by the two existing sync engines.

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

**Baseline measured 2026-11-06 before any edit** (recorded in `test-evidence/mirror-baseline.txt`):
`python3 scripts/python/sync-mirrors.py --check` → `EXIT=0`, `OK: all per-tool command copies match the source
templates.`, and `ok` for all six pairs (`templates/` 22 files, `skills/external/` 415, `skills/internal/` 138,
`agents/` 16, `scripts/` 121, `shared/` 94). The criterion for every row below is therefore **no NEW drift**, not
"all green" — a bare exit code would be an unmeasured expectation.

**Counts after delivery** (measured at implement Part 6, `test-evidence/polish-mirror-check.txt` § 3;
`sync-mirrors.py --check` still `EXIT=0`, `ok` on all six pairs): `templates/` **22** (unchanged), `skills/external/` **415**
(unchanged), `skills/internal/` **139** (+1 — `create-team/scripts/validate-roster.py`), `agents/` **17** (+1 —
`reporter.agent.md`), `scripts/` **122** (+1 — `status-digest.py`), `shared/` **95** (+1 — `reporting-obligations.md`).
The four deltas are exactly the four new framework-source files; the two unchanged pairs are edited-in-place files
(`coaching-skills/SKILL.md`, `subagent-definitions.md`, `external-dispatch-recipes.md` all live inside pairs whose
**file count** does not move). `templates/` staying at 22 rather than rising to 23 is the pair that the earlier
expectation got wrong: `templates/commands/` has no `.specify/` mirror (that pair is retired, as the table below
states), and `commands/` is excluded on both sides, so adding `templates/commands/status.md` cannot move this count.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/guidelines/reporting-obligations.md` (NEW) | `.specify/shared/guidelines/reporting-obligations.md` | `python3 scripts/python/sync-mirrors.py --check --only shared/guidelines/reporting-obligations.md` reports `ok` for the pair; the pre-edit baseline is zero drift, so any non-`ok` line is NEW |
| `shared/definitions/subagent-definitions.md` (edited) | `.specify/shared/definitions/subagent-definitions.md` | same command with `--only shared/definitions/subagent-definitions.md`; the file must be byte-identical on both sides — no NEW drift |
| `shared/workflow/external-dispatch-recipes.md` (edited) | `.specify/shared/workflow/external-dispatch-recipes.md` | same command with `--only shared/workflow/external-dispatch-recipes.md`; byte-identical, no NEW drift |
| `agents/reporter.agent.md` (NEW) | `.specify/agents/templates/reporter.agent.md` | same command with `--only agents/reporter.agent.md`; the pair compares `agents/` ↔ `.specify/agents/templates/` — `ok`, and the file count rises from 16 to 17 |
| `skills/internal/create-team/SKILL.md`, `references/create-mode.md`, `references/patterns.md`, `scripts/validate-roster.py` (edited/NEW) | `.specify/skills/internal/create-team/` (same four relative paths) | same command with `--only skills/internal/create-team`; four `ok` lines, no NEW drift (the pair is `skills/internal/` → `.specify/skills/internal/`) |
| `skills/external/coaching-skills/SKILL.md` (edited) | `.specify/skills/coaching-skills/SKILL.md` | same command with `--only skills/external/coaching-skills`; note the pair maps `skills/external/` → `.specify/skills/` (flat), so the mirror path loses the `external/` component |
| `scripts/python/status-digest.py` (NEW) | `.specify/scripts/python/status-digest.py` | same command with `--only scripts/python/status-digest.py`; **this pair is STRICT** — a mirror-only or source-only file FAILS the check, so both sides must be present |
| `templates/commands/status.md` (NEW) | `.claude/commands/speckit.status.md`; `.github/prompts/speckit.status.prompt.md`; `.qoder/commands/speckit.status.md`; `.opencode/command/speckit.status.md` — generated by `regen-command-copies.py` from `_ASSISTANT_COMMAND_DIRS` (6 configured tools: copilot, claude, hermes, opencode, qoder, codex; only the 4 whose directories exist in this repo are written). **NO `.specify/templates/commands/` mirror — that pair is retired.** | `python3 scripts/python/regen-command-copies.py` then `python3 scripts/python/regen-command-copies.py --check`; the check must print `OK: all per-tool command copies match the source templates.` — baseline was already `OK`, so the criterion is met only if it stays `OK` **and** the four `.qoder`/`.claude`/`.github`/`.opencode` `speckit.status.*` files exist |
| the five `tests/` files (four new, one edited) | none (tests are not mirrored) | `ls .specify/shared/guidelines/reporting-obligations.md` and the sibling paths above must all resolve — a mirror-only or source-only artifact is the defect this row prevents |

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The framework's write path for a new owner document is `shared/` + `sync-mirrors.py`; a hand-written `.specify/` copy never reaches a downstream project | `shared/definitions/dogfooding-definitions.md` § 2.1 (three-copy topology); `python3 scripts/python/sync-mirrors.py --check` exits 0 over all six pairs on 2026-11-06 | verified | — |
| EP-002 | No existing Tool record covers "render a current-state digest of the framework's running lines", so authoring `status-digest.py` is the expected outcome under the Tool Reuse gate | `ls .specify/memory/tools/` — the shipped records cover shell/git/memory/feedback/history utility families and none reads the line registry (recorded in `research.md` RO-05) | verified | — |
| EP-003 | A host console is the visible session surface, and an execution mode without one writes to the artifact triplet the visibility contract already defines — so no second carrier is needed and no mode is left unreachable | `shared/definitions/subagent-definitions.md` § Three Execution Modes (mode 3's `Progress visibility` cell states "Not automatic — MUST follow the Visibility Contract") + § External Dispatch Visibility Contract point 3 | verified | — |
| EP-004 | The line registry entry carries enough state for a digest entry (identity, state, stage, timestamps) without reading the spine's body, and its state vocabulary is a closed set that can be projected | `python3 skills/external/sdd-loop-driver/scripts/line-registry.py --action list --all --format json` returned 7 fields per entry (`branch`, `line_id`, `project_dir`, `run_id`, `stage`, `state`, `updated_at`) on 2026-11-06; `STATE_VALUES` is the 8-value set at `skills/external/sdd-loop-driver/scripts/line-registry.py:55` | verified | — |
| EP-005 | The existing stall threshold numbers are usable as the declared stall threshold without inventing a second one | `skills/internal/create-team/references/patterns.md` § Monitoring → **Stall Detection** table (three rows, numeric thresholds) exists and is the only numeric table for this purpose in the framework sources | verified | — |
| EP-006 | The `## Dispatch Payload` closed set of `skills/external/coaching-skills` can be extended by exactly one field without breaking its existing contract test | `tests/contract/test_coaching_dispatch_contract.py` asserts `REQUIRED_FIELDS` (7 names at the time of measurement; **8 after this feature's FR-019 amendment**, which is the declared expected delta) and a payload validator over one compliant + four counterexample payloads; adding a required field means adding it to that tuple in the same change | verified | — |
| EP-007 | Adding one command template propagates through the existing generator, so no per-tool copy needs to be hand-written | `python3 scripts/python/regen-command-copies.py --check` exits 0 today over the 6 configured tools and writes only the 4 tool directories present in this repo (`_ASSISTANT_COMMAND_DIRS`, `src/specify_cli/__init__.py:796`) | verified | — |
| EP-008 | The 30-second long-run default has no pre-existing definition site in the framework sources, so designating the new owner does not create a duplicate | A recursive scan for `30 秒` and `30 seconds` across `shared/`, `templates/`, `skills/`, `agents/` on 2026-11-06 returned zero framework-source definition of a reporting interval; the only two matches are unrelated prose uses inside `draw-diagram` and `improve-skills` references (recorded in `research.md` RO-11) | verified | — |
| EP-009 | The interactive default interval stays owned by `progress-reporting.md` and is already pinned by a contract test, so the plan must not touch that literal | `tests/contract/test_progress_reporting.py` exists and pins the owner doc plus the instructions mirror; `shared/guidelines/progress-reporting.md:23` carries the literal | verified | — |
| EP-010 | The framework's progress-reporting contract suite is the name-level compatibility baseline and is the only pre-existing suite this feature's zero-NEW-failure criterion is measured against; there is no docker or hugo suite in this repository to deselect | `tests/contract/test_progress_reporting.py` exists; the stage's only pre-change capture is that suite (tasks row T002); contract `ownership-map.contract.md` C-51 names the six pre-existing suites the closure diff covers | verified | — |

## Inherited Blockers

Dependency set: none.

The feature's only declared dependencies are *consumed documents and code inside this same repository* (the
progress-reporting discipline, the subagent definitions, the create-team skill, the line-registry engine), none of
which is a Feature carrying a `## Deferred` section or a `verification.md`. No other Feature is a dependency, so
the extraction set is empty and no row is owed. Consuming a document is not inheriting a blocker: a defect found
while consuming it is either repaired as a correction under the fast-fail criterion or surfaced, never parked in
this table.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| — | — | not-applicable | — | — | Dependency set: none — no dependency Feature exists, so no extracted row and no disposition is owed |

## Design Decisions

Each decision below fails all four load-bearing triggers (reversible, no external consumer contract, blast radius
inside this feature, no constitution MUST in conflict) and is therefore recorded here as an ordinary trade-off.

**D1 — One owner document, not an extension.** See § Decision Tensions T-001 for the recorded tension; the chosen
form is `shared/guidelines/reporting-obligations.md` and this is the shape `requirements.md` A10 already fixed.

**D2 — The reporter Template lives in `agents/`, the shipped role set.** `agents/` is the framework's Agent
Template store and its mirror target `.specify/agents/templates/` is what `specify init` distributes
(`shared/definitions/agent-definitions.md` § Storage Layout). The Template declares `capability-tools:` sufficient
to read the state it reports and nothing that dispatches, authorizes, retries, terminates or writes outside its own
stream artifact; `run-turn-budget` stays small because a reporting pass is one short read-and-emit cycle.

**D3 — The reporter seat is a roster row, not a new roster field.** `skills/internal/create-team/references/create-mode.md`
§ Team Schema already carries `members[]` with `role`, `lifecycle` and a declared territory; a reporter is a member
whose `role` is `reporter` and whose agent resolves to the new Template. This avoids widening the schema with a
parallel `reporter:` key (which would be a second place roster membership is expressed) and keeps existing teams
byte-identical until a `modify` passes through the guard.

**D4 — The seat guard is a script the create-team skill calls, not a prose-only rule.** `FR-006` requires roster
validation to report a missing reporter seat as a *named defect*. Prose cannot emit a named defect; a
stdlib-only script reading `team.md` can, and it is the form the skill's existing deterministic helpers already
take (`scripts/match-team-preset.py`, `scripts/verify-territory-disjoint.py`).

**D5 — The coaching payload gains exactly one field.** `reporting-cadence` (the tick value plus the attribution
pair) is added to the closed set, together with one forbidden-content clause and one return-handling clause, so the
closed-set invariant is extended and never widened to "anything". The duty itself stays owned by the new owner
document — the shipped example demonstrates it and does not define it.

**D6 — The digest reads the registry, never the spine's prose.** A registry entry is a small JSON file with a fixed
field set (`line-registry.py` writes it atomically); the spine is a Markdown document with a fenced state block. A
digest that parsed Markdown would be brittle and would duplicate the parser. The script therefore resolves the
registry directory the way the engine does (environment override, then XDG, then `~/.local/state/spec-kit/lines`)
and reads entries plus the per-entry triplet paths recorded in them.

**D7 — Staleness is measured from the record, not guessed.** Each digest entry carries the age of its last
observed activity, taken from the registry entry's `updated_at` / the triplet file's mtime, and an entry whose age
exceeds the declared staleness bound is marked stale with that age rather than rendered as current.

**D8 — One script, three actions.** `status-digest.py --action digest` renders the bounded summary;
`--action guard` judges the mechanically decidable propositions and returns named statuses; `--action report`
renders one status line from the owner's four labels plus attribution and the profile in force. All three share the
same reader functions, which is what FR-022's "one reading backs both the digest and the guard's verdicts" requires —
a second parser would be a second definition of what "current state" means.

**D9 — The bound is an entry cap with an omitted count.** `FR-012`'s "one screen and not a log dump" is
mechanical: the script writes at most `--cap` entries (declared default in the script, configurable per
invocation) and states `omitted=<n>` when it truncates. No "reasonable size" prose.

**D10 — Exit statuses are a closed three-value set.** `0` = a digest was rendered with at least one entry, `3` =
nothing active — the declared "nothing active" status `FR-011`/SC-005 name, carried by the explicit
`nothing-running` rendering (an empty entry set MUST NOT render an empty digest with status `0`), `2` = usage or
input error. The guard action reuses `0`/`1`/`2` in the framework's existing
convention (clean / findings / input error), matching `flow-class-check.py` and `pre-analyze-check.py`.

**D11 — The new owner's Chinese/English shape follows its siblings.** The framework's `shared/guidelines/`
documents are bilingual at the definition site (section headings carry both forms where the discipline is new), so
the new owner opens with a single-source-of-truth declaration, states each rule once, and reaches
`progress-reporting.md`, `subagent-definitions.md`, `patterns.md` and `agent-definitions.md` by path plus a section
anchor.

**D12 — The two cadence profiles are selected by one declared condition, at the structure level.** A structure has
a live status receiver when it has a reporter seat whose execution is not runtime-omitted, or when it is a
supervising master with at least one dispatched sub-flow. That condition selects the long-run profile; its absence
selects the interactive profile already owned by `progress-reporting.md`. The switch is recorded once per run and
is never silent (`requirements.md` Edge Cases, "Two cadence profiles in one session").

## Complexity Tracking

N/A — the Constitution Check carries zero Fail and zero Partial rows, so no violation needs justification and no
row is owed.

## Phase 1: Design Artifacts Summary

Counts below were taken **from the files on disk after they were written**, not from the design intent.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 7 entities (Reporter Seat, Status Report, Supervised Sub-flow, Stall Threshold, Current-State Digest, Reporting Profile, Registry Line Projection) and 12 invariants (INV-01…INV-12) |
| Contracts | `contracts/` | 6 files, 52 numbered clauses total: `reporting-obligations.contract.md` C-01…C-13 (RO-01…RO-13), `reporter-seat.contract.md` C-14…C-21 (RS-01…RS-08), `status-report.contract.md` C-22…C-31 (SR-01…SR-10), `supervision-report.contract.md` C-32…C-40 (MV-01…MV-09), `status-digest.contract.md` C-41…C-46 (DG-01…DG-06), `ownership-map.contract.md` C-47…C-52 (OM-01…OM-06) — clause ids are dense per file and cited by `/speckit.tasks` |
| Quickstart | `quickstart.md` | 8 scenarios (A owner read, B roster guard, C digest active, D digest idle, E owner-literal scan, F guard, G mirror/copy integrity, H zero-new-machinery audit) with the executed/unexecuted premise stated per scenario |
| Feature reference | `feature-ref.md` | Feature 087 binding, shared delivery root, FR → artifact map (29 FR), neighbouring-feature scan |
| Research | `research.md` | 15 measured readings (RO-01…RO-15) and 5 resolved unknowns |
| Stage evidence | `test-evidence/plan.jsonl` | 1 E3 `stage-status` row, `status=not-run-docs-only` with the six reduced fields |

Drift from the Phase 0 expectation: none in the artifact set; the entity count rose from the 5 named in
`requirements.md` § Key Entities to 7 because the design needed a **Reporting Profile** (the two cadence profiles
FR-020 declares) and a **Registry Line Projection** (the read-only shape the digest consumes) as first-class
objects — both are projections of existing owners, not new stores, and both were added before the counts were
written.
