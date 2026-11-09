# Implementation Plan: Speckit 框架可视化（Speckit Framework Visualization）

**Branch**: `088-speckit-visualization` | **Date**: 2026-11-06 | **Spec**: `.specify/specs/088-speckit-visualization/requirements.md`
**Requirement → Feature**: `088-speckit-visualization` → Feature 088 Speckit 框架可视化（Speckit Framework Visualization）
**Input**: Specification from `.specify/specs/088-speckit-visualization/requirements.md`

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

### Revision 2026-11-06 — the efficiency dimension and `/speckit.measure`

A second bounded slice adds two capabilities to the same three surfaces and to one new command. It extends nothing
that came before and rewrites no clause:

4. **An efficiency element on the existing two surfaces** (`FR-023`, `FR-024`, `FR-025`). Its **unit is the step** —
   the `(unit_id, unit_type)` identity the exec-quant record itself carries, never a row a surface lists. The status
   line and the digest each carry **one bounded element per step they name** — the step's readable name, its
   **elapsed time first and unconditionally**, then its token and invocation counts **only while the whole element
   stays inside the surface's existing entry bound**. The step set is the surface's own: the line carries the emitting
   step alone, the digest this run's or the most recent steps, inside the existing cap. When the deeper quantities do
   not fit, they are withdrawn from **every** step on that render together and named in the render's existing omitted
   summary, so two steps on one screen are never described to different depths. A quantity the record does not carry
   renders the explicit not-evaluated marker — never `0`, never an averaged substitute, never an omission. The source
   is the exec-quant store (`.specify/memory/exec-quant/`), read **only** through the engine that owns it, and
   **only** for the latest record per step (matched on the record's own `(unit_id, unit_type)`, ties by record
   identity). The store's schema already carries `quality.elapsed_ms`; no recorder, no schema extension and no second
   store is added.
5. **A dedicated measurement-reading command** (`FR-026`…`FR-029`). `/speckit.measure` —
   `templates/commands/measure.md` backed by one stdlib-only script `scripts/python/measure.py` — analyses the same
   store over a **declared half-open window** (`--since` from, `--window` span, neither = the whole store stated as
   such) and a **declared unit selection** (exact `(unit_id, unit_type)` identities), and reports per unit: the
   record count, the **median** elapsed with min/max and provenance, the token **sum** with how many records covered
   it, and the invocation **sum**; plus the four exclusion-class counts and the cap-omitted count. It prints the cap
   it used on every run, is **deterministic** (two runs are byte-identical), and exits on a **closed four-value**
   status set: `0` produced, `2` input error, `3` nothing to analyse, `1` any other failure.

The two capabilities share **one reader**: the store engine's own read path, imported in-process. They are two
projections over it, never two parsers, and neither borrows the other's selection — the surfaces show the latest
record, the command aggregates over a window.

Feature status advances `Draft → Planned`. `Implemented` is never claimed here. The `Blocked` verdict recorded by the
earlier implement/review rounds is **left as recorded** (`requirements.md` Clarifications, second-slice adjudication
Q6): it is re-judged only by a later closure check.

## Technical Context

**Language/Version**: Python `>=3.8`, stdlib only (no new dependency; `pyproject.toml` `requires-python` unchanged).
Documentation and prompt surfaces are Markdown.
**Primary Dependencies**: none added. The shipped script imports only the standard library and reads files the
framework already writes; it does not import `line-registry.py` (that engine is stdlib-only as well, but a direct
import would couple the digest to an internal module path rather than to its JSON on disk).
**Storage**: no new store. Read-only inputs: the per-line registry entries under `$SPECIFY_LINE_REGISTRY_DIR`
(default `~/.local/state/spec-kit/lines/<line_id>.json`), the runner triplet
(`<line_id>.status`, `<line_id>.log`, `<line_id>.heartbeat`) whose paths the registry entry declares,
`<spec-dir>/test-evidence/*.jsonl` for the stage row of an executing line, and — added by the second slice — the
exec-quant store at `.specify/memory/exec-quant/` (its per-record directory plus its legacy stream), read **only**
through the store engine's own reader, imported in-process by path. Write outputs: the reporter's own stream
artifact only, and a run record the emitting flow already writes. **`/speckit.measure` writes nothing at all**, and
neither it nor the efficiency element creates, migrates, rewrites or deletes anything under the exec-quant store.
**Testing**: `pytest` (`pytest -m contract` for the new guards). Plan stage runs no suite — it is a documents-only
stage (test budget below). The second slice's evidence is `tests/contract/test_measure.py`,
`tests/unit/test_measure_unit.py`, `tests/contract/test_efficiency_element.py` (new) plus the efficiency assertions
added to `tests/contract/test_status_digest.py` (edited, additions only).
**Target Platform**: the supported agent hosts (`AGENT_CONFIG` in `src/specify_cli/__init__.py` is the roster
owner); the script runs wherever a Python 3.8+ interpreter exists.
**Project Type**: framework source (templates + shared owners + skills + scripts + agent templates), distributed by
`specify init` and mirrored into this repo's `.specify/` runtime.
**Performance Goals**: one digest render under one second on a registry of ~20 lines (it lists and reads small JSON
files; no network, no process spawn).
**Constraints**: digest output bounded by a declared entry cap with the omitted count stated; no new process,
timer, daemon or store; every emitted line readable by a reader who did not take part in the run
(`shared/guidelines/user-facing-comprehension.md`); the 30-second literal has exactly one definition site.
**Scale/Scope**: **40** delivered paths across the same framework-source areas, now with **8** per-tool command
copies (two new commands × 4 existing tool directories) (`feature-ref.md` § Delivered paths is the enumerated owner
of this list); 29 FR, 14 SC, **8 contracts / 72 clauses** (`C-01`…`C-72`), **9 entities**, **17 invariants**.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.16.0 — one row per
`### <numeral>. <name>` heading, in constitution order; no `(NON-NEGOTIABLE)` / `(MANDATORY)` annotation is
carried by any principle heading in that file, so none is rendered):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every delivered file traces to an FR in `requirements.md` § Functional Requirements; `feature-ref.md` carries the FR → artifact map; `contracts/` names the FR each clause serves |
| II | Feature-Centric Development | ✅ Pass | Feature 088 row + detail updated synchronously in this stage (`Draft → Planned`); `feature-ref.md` records the binding and the neighbouring-feature scan |
| III | Intent-Driven Development | ✅ Pass | `research.md` records the measured current state before any design; `plan.md` § Decision Tensions records the "why" for the two load-bearing choices |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | `contracts/` fixes the numbered clauses (`C-01`…`C-72` across 8 files, dense per file; the second slice continues the sequence at `C-53` and renumbers nothing) that `/speckit.tasks` turns into red-first contract tests; `RO-01`…`RO-13` are the guard's judgements, each with a named status, and `contracts/reporting-obligations.contract.md` C-01…C-13 is their single owner; every second-slice clause names the test file that judges it (`test_measure.py`, `test_efficiency_element.py`, `test_measure_unit.py`) |
| V | AI Agent Integration Standards | ✅ Pass | No agent is added to `AGENT_CONFIG`; the new Template renders through the existing render path; `_ASSISTANT_COMMAND_DIRS` (6 tools) is the copy-target owner, unchanged. `/speckit.measure` is a command template, not a tool: it reaches the same four copy directories through the existing generator (`regen-command-copies.py`, measured `OK` at 28 copies each before the change, 29 expected after — `EP-013`) |
| VI | Continuous Quality & Observability | ✅ Pass | The feature's subject *is* observability; no `.bak` copy is produced (version control is the backup); root cause over symptom — a flow that cannot report records that fact (FR-016) rather than staying green, and a store that does not carry elapsed time renders the not-evaluated marker instead of a fabricated number (`FR-025`, `EP-011`) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | This stage lands at most `Planned`; FR-018's zero-new-machinery shape keeps Test-First Partial-unneeded — the guard and its tests are ordinary code + contract tests, so no `Partial (justified)` row exists |
| VIII | Code as the Single Source of Truth | ✅ Pass | `research.md` every claim was measured against the tree (mirror check, engine `--help`, literal scans) rather than read from documentation; where a doc disagreed, the measurement is quoted. The second slice's store readings (`RO-16`/`RO-17`) were taken **through the engine's own reader**, not by parsing files, and the read-only property was measured (`EP-014`, `quickstart.md` Scenario M) rather than asserted |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Cadence is executed by the running flow between its steps; RO-13 (no scheduler/timer/daemon/second store) is a named guard proposition, and contract `ownership-map.contract.md` C-49/C-50 makes the delivered set auditable against it. The second slice adds **one** command + **one** script and reuses the store that already exists: no recorder, no schema extension (`FR-025`, ownership-map C-47 rows 10–12), no cache, no persisted report (`FR-026`, `contracts/measure-report.contract.md` C-62) |
| X | Documentation Naming & Location Conventions | ✅ Pass | New owner `shared/guidelines/reporting-obligations.md`, new Template `agents/reporter.agent.md` (lowercase kebab), new command `templates/commands/status.md`; no `README.md` is introduced; `skills/*/SKILL.md` keeps its mandated name |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two hats named: all delivery lands in framework sources (`shared/`, `agents/`, `skills/`, `scripts/`, `templates/`) and reaches `.specify/` only through `sync-mirrors.py` / `regen-command-copies.py`; no hand edit of a `.specify/` mirror |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | `research.md` RO-05/RO-06 record the Tool-record lookup (`.specify/memory/tools/`) before authoring `status-digest.py`; no existing Tool covers a current-state digest, so authoring is the expected outcome. The second slice repeated the gate: `RO-18` records the lookup before authoring `measure.py`, and the closest existing surface — `exec-quant.py`'s `aggregate` action — was examined and **not repurposed** (its subject is the received-feedback view, not the local store) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | `feature-ref.md` names the strengthened work-loop dimension (Task Understanding + Reliable Delivery visibility, and by the second slice **Efficiency** — the user can see what a run costs); no scoring system or maturity report is added, and the measure report issues no verdict (`INV-16`) |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Each fact has one owner: cadence value → the new owner; content floor + interactive default → `progress-reporting.md`; artifact triplet + modes → `subagent-definitions.md`; stall numbers → `create-team/references/patterns.md`; registry states → `line-registry.py` `STATE_VALUES`; the digest's cap and stale bound → the constants in `status-digest.py` (C-43/C-44); profile selection → `status-report.contract.md` C-30; the guard's thirteen propositions → `contracts/reporting-obligations.contract.md` C-01…C-13. Every other surface reaches a proposition by id and states only what it reads, never what the proposition asserts. C-47 makes the ownership consignment a contract clause and SC-006 its measurement. **Second slice**: the record schema (version, vocabularies, field slots, per-action manifest) stays with `shared/declarations/facts/quant-record-schema.yaml` and the store's layout/read/write path with `scripts/python/exec-quant.py`; both new consumers reach them by path and copy none of their enumerations (C-47 rows 10–12, `efficiency-element.contract.md` C-71); the measure cap lives once in `measure.py`, and the exclusion classes and exit statuses are owned by `measure-report.contract.md` C-58/C-59 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Emitted lines are a governed surface of that discipline; `contracts/status-report.contract.md` C-23 (SR-02) pins the four content elements and C-22 (SR-01) the attribution fields, and `data-model.md` § Invariants INV-05 forbids an internal identifier from reaching the line without a user-facing name. The element's unit name follows INV-05 and the report prints plain words (`no measurements`, `not evaluated`, the four exclusion class names) rather than internal state |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | The reporting obligation rides the same dispatch-payload channel as the fast-fail clause and does not modify it; the reporter is not given authority to repair or to halt anything (FR-005, INV-08). A not-evaluated quantity is surfaced as a marker rather than quietly substituted — the same "never patch it over" rule applied to data (`FR-023`, `FR-025`) |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory is created: `contracts/`, `test-evidence/`, `agents/`, `shared/guidelines/` all exist; the digest's scratch needs none (`temp_directory_discipline` not exercised). The second slice creates no directory either — `templates/commands/`, `scripts/python/`, `tests/contract/` and `tests/unit/` all exist, and the store's directories are read-only for this feature (C-49) |
| XVIII | Grounded Naming | ✅ Pass | Names follow the highest available source — user instruction ("reporter subagent", "team", and by the second slice "measure" and "效率"), sibling imitation (`shared/guidelines/<topic>.md`, `scripts/python/<verb>-<noun>.py` next to `flow-class-check.py`, `line-registry.py`), then a descriptive own choice (`/speckit.status`, `status-digest.py`, `/speckit.measure`, `measure.py`, and the `ME`/`EF` clause families) |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The user's information need is named (what is running now), one dimension is added (a current-state reading on demand beside the cadence line), and the digest is a projection reconciled to the owners of the state it reads — never a second owner of that state. The second slice adds **one** information dimension (efficiency) to the surfaces that already exist rather than a fifth surface, and the user's real need — "how long did this take?" — decides the stop point: the element carries elapsed unconditionally and the two further quantities only while they fit (`efficiency-element.contract.md` C-64) |

**Gates Status**: ✅ All gates pass — zero Fail rows, zero Partial rows, and therefore no Complexity Tracking entry
is owed (that section states `N/A`).

**Re-check after Phase 1**: 2026-11-06, re-run against the design artefacts on disk (`data-model.md` with 7
entities and INV-01…INV-12 — 9 and INV-01…INV-17 after the second slice, `contracts/` with 6 files / 52 clauses — 8
files / 72 clauses after it, `quickstart.md` with 8 scenarios A–H — 13 (A–M) after it, `feature-ref.md`). The table above is the refreshed reading: no row changed verdict. Two rows were the only
candidates for a downgrade and each was checked against its artefact — IV (Feature) stays Pass because the
contracts enumerate the tests to write rather than leaving them implicit; XI (Dogfooding) stays Pass because
`plan.md` § Mirror Obligations names every copy and the baseline drift is zero, so no artifact could be delivered
by hand-editing a mirror. XIV was checked separately: it passes only because
`contracts/reporting-obligations.contract.md` C-01…C-13 declares itself the single owner of the thirteen guard
propositions and every other surface — `status-digest.contract.md` C-46, `data-model.md` § Invariants, each contract's
`*Judged by*` line, and `quickstart.md` § F — reaches them by id and states only what it reads, without restating a
proposition's subject.

**Re-check after the second-slice revision** (2026-11-06): the table above was re-rendered against the artefacts on
disk, still one row per constitution principle (19 rows) and still zero Fail / zero Partial, so no Complexity
Tracking entry is owed. Two rows were the only realistic downgrade candidates and each was checked rather than
asserted: **XIV** (One Source of Truth) passes only because the exec-quant schema, its vocabularies and its read path
are reached **by path** — `contracts/ownership-map.contract.md` C-47 names them as owners with their consumers, and
`efficiency-element.contract.md` C-71 forbids a second copy; **IX** (No Over-Engineering) passes only because the
second slice opens no recorder and no schema extension (`FR-025`, measured: the field already exists, `EP-011`), so
the added surface is one command + one script over a store that already exists. **XI** (Dogfooding) stays Pass: the
second slice's two new framework-source files land in `templates/commands/` and `scripts/` and reach `.specify/` only
through `regen-command-copies.py` and `sync-mirrors.py`, with the measured baseline `ok`/`EXIT=0` (`EP-013`). The
readings behind these three rows are in `test-evidence/plan-revision-2026-11-06.txt`.

**Re-check after the round-3 plan repair** (analyze round 2, findings F-01/F-07/F-08/F-09): the row above was
re-measured against the consumers rather than asserted. Every `*Judged by*` line and every invariant now names the
RO id whose subject actually matches, and the four facts that have their own clause owners go to those clauses
instead of to a proposition — attribution and profile selection to `status-report.contract.md` C-22/C-30, the digest
cap to `status-digest.contract.md` C-43, the digest contract itself to C-09/`RO-09`. `C-46`'s `RO-04` row no longer
offers a glob as a default population, so no consumer contradicts `FR-006`. Evidence:
`test-evidence/plan-repair-round3.txt`.

## Decision Tensions

Three decisions cross the load-bearing threshold: **T-001** (an independent owner document rather than extending
`progress-reporting.md`) is constitutional (Principle XIV owner selection) *and* cross-team (three existing owner
documents start pointing at a new path); **T-002** (the digest is a new command + script pair) is cross-team (it
adds a new `/speckit.*` surface that 6 per-tool copy trees must carry); **T-003** (the second slice *imports* the
store engine's reader instead of restating the record format) is constitutional (Principle XIV owner selection) and
reaches across a code boundary owned by another capability. The remaining choices in § Design Decisions fail all four
triggers and are therefore recorded as ordinary trade-offs, not as records.

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

### T-003 — Both new consumers import the store engine's reader instead of parsing the record format

- **decision**: `scripts/python/measure.py` and the efficiency projection in `scripts/python/status-digest.py` import `scripts/python/exec-quant.py`'s read path in-process (`storage_dir`, `read_jsonl_safe`, `read_entry_files`) and never re-implement it; the record format, the legacy-stream compatibility path and the schema stay reachable by path only.
- **antithesis**: give each consumer its own small parser over `.specify/memory/exec-quant/` — that file layout is stable, a 40-line reader has no cross-module import risk, and the existing engine is a `cli`-shaped script rather than a library, so importing it couples two capabilities to each other's internals.
- **binding_constraints**:
  - pole_a: "one engine and one reading" (`FR-028`) is the requirement that makes a store's two readers indistinguishable from two stores — a second parser is precisely the divergence this feature is chartered to prevent.
  - pole_b: the importing side inherits any change the engine makes to its reader, and the engine is owned by another capability that can change it without consulting this one.
- **discriminating_evidence**: seed one record whose shape only the engine's compatibility path accepts (a legacy-stream entry with the older schema version) and run both consumers. Two-valued: both consumers report it (or both exclude it as `legacy-format`) because both went through the same reader — or the hand-written parser silently drops it and the two surfaces disagree about what the store contains.
- **expected_sacrifice**: SC-014 Source ↓ the delivered script is no longer self-contained: it depends on a sibling module's function signatures, so a future refactor of `exec-quant.py`'s reader can break `/speckit.measure` without any change in this feature's own files — a coupling cost this feature pays deliberately, and one no local test can bound.
- **revision_trigger**: two consecutive changes in which `exec-quant.py`'s reader signature or return shape changes without the measure/element tests going red, or one recorded incident where the import made a consumer unrunnable while the engine itself worked → reopen and give the consumers a thin declared adapter that the engine's owner also honours.

## Project Structure

### Second-slice design — the efficiency element (S1) and `/speckit.measure` (S2)

The two subsections below (S1, S2) are **additions**. Where they need a subject an existing clause already owns, they
name the clause and state only what they read.

#### S1 — The efficiency element: projection, source and degradation

**Where it renders.** Content of the two surfaces this feature already owns — the status line (`SR-*`, contract
`contracts/status-report.contract.md`) and the digest entry (`DG-*`, contract `contracts/status-digest.contract.md`).
Not a third surface, not an extra line, not a second cadence, and never an extra unit: `contracts/efficiency-element.contract.md`
C-63 is the clause that fixes that, and `data-model.md` E8 is the entity.

**What the unit is.** The **step** — the `(unit_id, unit_type)` identity the exec-quant record itself carries, such
as one `/speckit.*` invocation or one skill execution (`requirements.md` Clarifications Q4; `FR-023`). It is never a
row a listing carries. The **step set** is the host surface's own: the status line carries the **emitting step**
alone, and the digest carries **this run's steps or the most recent steps**, inside `FR-012`'s existing cap and the
surface's declared bound (`FR-024`). The store is the efficiency *measurement* source only; every non-efficiency part
of the line or digest keeps coming from that surface's own state sources, and the store never widens the step set.

**What one element holds, in order.** The step's readable name → the elapsed quantity → (if the bound permits) the
token count → (if the bound permits) the invocation count, each with the provenance the record states. The elapsed
quantity is **unconditional and first**; the other two are appended **all-or-nothing across the whole render** —
when they do not fit the host surface's existing entry bound, they are dropped from every step on that render and
named once in that render's existing omitted summary (C-64).

**Where the numbers come from.** `quality.elapsed_ms`, `quality.tokens` and the invocation quantity of **one**
exec-quant record per step: the record with the latest `collected_at` among that step's records, ties broken by the
record's own identity (the file's name stem) ascending (C-66). The record is found by the lookup `data-model.md` E8
`unit.lookup` declares — matched **on the record's own `(unit_id, unit_type)`**, never on its `run_id` (one run's id
is shared by many steps, so a `run_id` join matches the wrong record or none). Nothing is folded on a surface — no
average, no sum, no lifetime aggregate. A step the surface names with **no** record at all still renders the element,
with the not-evaluated marker (C-67): an omission beside a neighbour's number reads as "faster", which is the
misreading FR-023 exists to prevent.

**How the record is reached.** By importing the store engine's read path (`storage_dir` + `read_jsonl_safe(<legacy
stream>)` + `read_entry_files(<per-record directory>)`) — the same three names `load_store()` composes — and never
by re-parsing a file, never by shelling out to the engine's CLI, never through a cache (C-65). The store is
**read only**: both reads leave every file byte-identical and create no path under it (C-69, measured for the reader
today in `quickstart.md` Scenario M).

**What is deliberately *not* done.** No recorder and no schema extension: the declared schema already carries
`quality.elapsed_ms` (schema version 2) and the engine's existing paths populate it (`collect-dispatch` as
`measured`, `collect` as `carried`); where they leave it `not_evaluated` the marker renders and nothing is invented
(C-70, `FR-025`). The measured coverage on 2026-11-06 — 36 of 245 records carry a value, every one of them
`carried`, and **tokens are absent on all 245** (`research.md` RO-16) — is a data condition, and it is the reason
the "elapsed-only" degradation is the expected floor rather than an edge case.

**Surface behaviour when the store is missing.** An absent or empty store renders the explicit "no measurements"
state and leaves the rest of the line or digest byte-identical to a render without the dimension (C-68). Store
availability is never a precondition of the visibility surfaces.

#### S2 — `/speckit.measure`: CLI face, reading, aggregation, exits

**The delivery shape** (FR-029, C-62): `templates/commands/measure.md` — a thin entry naming the script and the
action — plus `scripts/python/measure.py` (stdlib-only, read-only) plus the four per-tool copies the existing
generator writes, plus the mirror the STRICT `scripts/` pair requires. The command carries the standard `## Wrap-up`
delegation block the other commands carry.

**The CLI face** (owned by the requirement's closed sets; the table below is the plan's projection of them):

| Input | Meaning | Failure mode |
|-------|---------|--------------|
| `--action summary\|json` | the two closed actions: human report / the same figures machine-readable (C-60) | an unknown action → `2` |
| `--since <ISO date-or-timestamp>` | the window **start**, parsed exactly as the store engine parses its own `--since` | unparseable → `2` |
| `--window <duration>` | the window **span**; end = start + span | unparseable → `2` |
| *(neither)* | **all records the store holds**, stated as such in the report — never an implied day | — |
| `--unit <identity>` (repeatable) | an exact `(unit_id, unit_type)` identity; matched as a set | an identity the store does not hold → `2`, naming the value |
| `--cap <n>` | per-unit record cap for one invocation | a non-integer → `2` |
| `--workspace <path>` | the workspace root the store is resolved under — the same resolution the store engine performs | — |

**The window is half-open** (`start ≤ collected_at < end`), so two adjacent windows partition the store: measured on
the live store, `[2026-10-21, 2026-10-30)` gives 93 records and `[2026-10-30, 2026-11-08)` gives 93, with 0 outside
and 186 in total (`research.md` RO-17).

**Aggregation** (C-56): per unit row — `records` = the contributing record count (a sum); `elapsed` = **median** over
the in-window records with **min** and **max** named; `tokens` = a **sum** with `covered=<k>/<n>` when only some
records carried it; `invocations` = a **sum**. A quantity absent from **every** contributing record is reported as
not evaluated — never `0` — and a partial figure always states how many records covered it.

**Identity and ordering** (C-55, C-61): rows are keyed and ordered by `(unit_type, unit_id)` ascending. The store
holds one `unit_id` under more than one `unit_type` in principle (the schema declares four unit types), so the pair
is the key — a bare `unit_id` would merge two different units into one row.

**Exclusions** (C-58): four classes, each counted **once per record** — `unreadable`, `legacy-format`,
`outside-window`, `unknown-unit` — plus the cap's **omitted count** printed as its own field. `outside-cap` is not a
fifth class. The accounting identity `contributed + unreadable + legacy-format + outside-window + unknown-unit +
outside-cap == read` MUST hold, so every printed figure is recomputable from the report itself.

**Determinism** (C-61): two runs over an unchanged store, same window/selection/cap, are **byte-identical** in both
actions; no render timestamp and no relative-age text; ordering is a declared total order, never hash or
enumeration order.

**Exit statuses, closed** (C-59): `0` a report was produced — including a report whose window selected records but
none contributed a figure (`figures measurable=0` is stated and is **not** the nothing-to-analyse case); `2` input
error; `3` nothing to analyse (absent store, or no record inside the resolved window — printed as an explicit
`no measurements` statement, never a zero row); `1` any other failure, as a single plain-language line and never for
the two statuses above.

**One reading** (C-53, C-65): the script imports the store engine's reader; it contains no record-format parser, no
second store engine and no subprocess call. The visibility surfaces import the **same** reader for S1 — one reader,
two projections, each with its own selection rule.

### Documentation (this spec)

```text
.specify/specs/088-speckit-visualization/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — measured current state and resolved unknowns
├── data-model.md        # Phase 1 output — 9 entities, fields, 17 invariants
├── quickstart.md        # Phase 1 output — 13 executable scenarios (A–M)
├── contracts/           # Phase 1 output — 8 contract files, 72 clauses
├── feature-ref.md       # Phase 1 output — Feature 088 binding, FR → artifact map
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
templates/commands/         # NEW status.md — the thin /speckit.status entry; NEW measure.md — the thin /speckit.measure entry (second slice)
scripts/python/             # NEW status-digest.py — digest renderer + guard + line renderer (one reading); EDITED for the efficiency element (second slice)
scripts/python/             # NEW measure.py — the read-only measurement analysis engine (second slice; imports exec-quant.py's reader)
tests/contract/             # NEW test_reporting_obligations.py, test_roster_reporter_seat.py, test_status_digest.py, test_coaching_reporting_duty.py; NEW test_measure.py, test_efficiency_element.py (second slice); EDITED test_status_digest.py (efficiency additions), test_coaching_dispatch_contract.py (declared expected delta, OM-05)
tests/unit/                 # NEW test_status_digest_unit.py — projection, bounding, staleness, exit codes; NEW test_measure_unit.py — one reader / two projections, latest-record selection, tie-break stability (second slice)
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

**Second slice, added to the same layout**: one new command template (`templates/commands/measure.md`), one new
script (`scripts/python/measure.py`), one **bounded edit** to an existing script (`scripts/python/status-digest.py`,
which gains the efficiency projection as content of its existing renders — no new action, no new file), and four new
test surfaces (`tests/contract/test_measure.py`, `tests/contract/test_efficiency_element.py`,
`tests/unit/test_measure_unit.py`, plus additions to `tests/contract/test_status_digest.py`). No file under
`shared/`, `agents/` or `skills/` is added or edited by the second slice: the exec-quant schema, its store layout and
its writer are consumed by path and amended by nobody. `templates/` therefore keeps its source count and gains a
member, while `scripts/` gains one (**STRICT** pair — source and mirror land together).

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
**Second-slice reading** (measured 2026-11-06 before any second-slice edit, `test-evidence/plan-revision-2026-11-06.txt` § 4):
`sync-mirrors.py --check` → `EXIT=0`, `ok` on all six pairs at `templates/` 22, `skills/external/` 415,
`skills/internal/` 139, `agents/` 17, `scripts/` 122, `shared/` 95; `regen-command-copies.py --check` → `OK`, 28
copies in each of the four existing tool directories. After this slice the expected reading is `scripts/` **123**
(+1 — `measure.py`), `templates/` **22** (unchanged: `templates/commands/` has no `.specify/` mirror and `commands/`
is excluded on both sides), the other four pairs unchanged, and the copy directories at **29** each. Every other row
above is `ok` because its file was edited in place, not added.

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
| `skills/internal/create-team/SKILL.md`, `references/create-mode.md`, `references/patterns.md`, `skills/internal/create-team/scripts/validate-roster.py` (edited/NEW) | `.specify/skills/internal/create-team/` (same four relative paths) | same command with `--only skills/internal/create-team`; four `ok` lines, no NEW drift (the pair is `skills/internal/` → `.specify/skills/internal/`) |
| `skills/external/coaching-skills/SKILL.md` (edited) | `.specify/skills/coaching-skills/SKILL.md` | same command with `--only skills/external/coaching-skills`; note the pair maps `skills/external/` → `.specify/skills/` (flat), so the mirror path loses the `external/` component |
| `scripts/python/status-digest.py` (NEW) | `.specify/scripts/python/status-digest.py` | same command with `--only scripts/python/status-digest.py`; **this pair is STRICT** — a mirror-only or source-only file FAILS the check, so both sides must be present |
| `templates/commands/status.md` (NEW) | `.claude/commands/speckit.status.md`; `.github/prompts/speckit.status.prompt.md`; `.qoder/commands/speckit.status.md`; `.opencode/command/speckit.status.md` — generated by `regen-command-copies.py` from `_ASSISTANT_COMMAND_DIRS` (6 configured tools: copilot, claude, hermes, opencode, qoder, codex; only the 4 whose directories exist in this repo are written). **NO `.specify/templates/commands/` mirror — that pair is retired.** | `python3 scripts/python/regen-command-copies.py` then `python3 scripts/python/regen-command-copies.py --check`; the check must print `OK: all per-tool command copies match the source templates.` — baseline was already `OK`, so the criterion is met only if it stays `OK` **and** the four `.qoder`/`.claude`/`.github`/`.opencode` `speckit.status.*` files exist |
| the five `tests/` files (four new, one edited) | none (tests are not mirrored) | `ls .specify/shared/guidelines/reporting-obligations.md` and the sibling paths above must all resolve — a mirror-only or source-only artifact is the defect this row prevents |
| `scripts/python/measure.py` (NEW, second slice) | `.specify/scripts/python/measure.py` | `python3 scripts/python/sync-mirrors.py --check --only scripts/python/measure.py` reports `ok` for the pair; **STRICT** — a source-only file FAILS the check, so both sides must be present in the same change |
| `scripts/python/status-digest.py` (edited, second slice) | `.specify/scripts/python/status-digest.py` | same command with `--only scripts/python/status-digest.py`; the pair is STRICT and already present on both sides, so the criterion is byte-identity after `--write`, i.e. no NEW drift on the edited file |
| `templates/commands/measure.md` (NEW, second slice) | `.claude/commands/speckit.measure.md`; `.github/prompts/speckit.measure.prompt.md`; `.opencode/command/speckit.measure.md`; `.qoder/commands/speckit.measure.md` — generated by `regen-command-copies.py` | `python3 scripts/python/regen-command-copies.py` then `--check` must print `OK: all per-tool command copies match the source templates.` **and** the four `speckit.measure.*` files must exist; the measured baseline is `OK` with 28 copies per directory, rising to **29** per directory after this slice |
| the four new/edited `tests/` files (second slice) | none (tests are not mirrored) | the paths in `feature-ref.md` rows 37–40 must resolve; no mirror is owed |

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
| EP-011 | The exec-quant store already carries an elapsed-time field, so the efficiency element needs no recorder and no schema extension | `shared/declarations/facts/quant-record-schema.yaml` declares `schema_version: 2`; `scripts/python/exec-quant.py` populates `quality.elapsed_ms` in two places (`collect_quality` writes `carried`, `dispatch_quality` writes `measured`); a 2026-11-06 read through the engine returned 36 of 245 records with a value, all `carried` (research RO-16) | verified | — |
| EP-012 | Both new consumers can reach the store's records **only** through the engine's read path, because that path composes two read surfaces (a per-record directory and a legacy stream) that a hand-written parser would have to re-implement | `exec-quant.py` `load_store` composes `read_jsonl_safe(base / LEGACY_RECORDS_NAME)` with `read_entry_files(base / RECORDS_DIR_NAME)`; the 2026-11-06 reading found 59 legacy-stream records beside 186 per-record files, so neither surface alone is the store (research RO-16) | verified | — |
| EP-013 | `/speckit.measure` can ship in the same shape as `/speckit.status` and reach the same four tool directories without new registration | `templates/commands/` holds 26 templates and all four copy directories hold 28 copies each (`regen-command-copies.py --check` → `OK`); `measure.md` and a `speckit.measure.*` copy are absent from all of them (research RO-18) | verified | — |
| EP-014 | The store's read is non-mutating in practice, so "read-only" is measurable rather than asserted | A full `load_store()` read over the live store on 2026-11-06 left all 189 files byte-identical — a before/after md5 digest list compared with no difference (`quickstart.md` Scenario M) | verified | — |

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
take (`skills/internal/create-team/scripts/match-team-preset.py`, `scripts/verify-territory-disjoint.py`).

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

**D13 — The efficiency projection lives inside `status-digest.py`, not in a new script.** The element is *content* of
the two renders that script already produces (`--action digest`, `--action report`), so adding a fourth action or a
fourth file would create a second renderer of the same surfaces — the defect contract `status-digest.contract.md`
C-41 names. The script gains an imported reader call and a render function; its action set stays exactly the three it
declares.

**D14 — `measure.py` is a sibling script, not a new action on `status-digest.py` or on `exec-quant.py`.**
`exec-quant.py`'s `arg_manifest` is a **closed** per-action face (`shared/declarations/facts/quant-record-schema.yaml`
`note`), so a new action there would be a contract change to another capability's engine; and `status-digest.py` has
a closed three-action set of its own. A sibling script that **imports** the engine's reader keeps both closed sets
closed and matches the framework's `scripts/python/<verb>-<noun>.py` sibling shape (`flow-class-check.py`,
`line-registry.py`, `status-digest.py`).

## Complexity Tracking

N/A — the Constitution Check carries zero Fail and zero Partial rows, so no violation needs justification and no
row is owed.

## Phase 1: Design Artifacts Summary

Counts below were taken **from the files on disk after they were written**, not from the design intent.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 9 entities (Reporter Seat, Status Report, Supervised Sub-flow, Stall Threshold, Current-State Digest, Reporting Profile, Registry Line Projection, **Efficiency Element**, **Measure Report**) and 17 invariants (INV-01…INV-17) |
| Contracts | `contracts/` | 8 files, 72 numbered clauses total: `reporting-obligations.contract.md` C-01…C-13 (RO-01…RO-13), `reporter-seat.contract.md` C-14…C-21 (RS-01…RS-08), `status-report.contract.md` C-22…C-31 (SR-01…SR-10), `supervision-report.contract.md` C-32…C-40 (MV-01…MV-09), `status-digest.contract.md` C-41…C-46 (DG-01…DG-06) + C-72 (DG-07, second slice), `ownership-map.contract.md` C-47…C-52 (OM-01…OM-06), **`measure-report.contract.md` C-53…C-62 (ME-01…ME-10)**, **`efficiency-element.contract.md` C-63…C-71 (EF-01…EF-09)**, and **`status-digest.contract.md` C-72 (DG-07)** — clause ids are dense across the delivery order and cited by `/speckit.tasks`; the second slice continues at C-53 and renumbers nothing |
| Quickstart | `quickstart.md` | 13 scenarios (A owner read, B roster guard, C digest active, D digest idle, E owner-literal scan, F guard, G mirror/copy integrity, H zero-new-machinery audit, **I live-store reading (EXECUTED)**, **J measure over a populated store**, **K measure over an absent store / empty window**, **L the efficiency element on both surfaces**, **M read-only store (EXECUTED)**) with the executed/unexecuted premise stated per scenario |
| Feature reference | `feature-ref.md` | Feature 088 binding, shared delivery root (restated over both slices), FR → artifact map (29 FR), fifteen-row owner relation table, neighbouring-feature scan with the exec-quant and `aggregate` adjacency |
| Research | `research.md` | 19 measured readings (RO-01…RO-19: RO-16…RO-19 added by the second slice) and 9 resolved unknowns (U-6…U-9 added by the second slice) |
| Stage evidence | `test-evidence/plan.jsonl` | 1 E3 `stage-status` row per stage run, `status=not-run-docs-only` with the six reduced fields (the second-slice revision appends a second row: `test-evidence/plan-revision-2026-11-06.txt` carries the gate readings) |

Drift from the Phase 0 expectation: none in the artifact set; the entity count rose from the 5 named in
`requirements.md` § Key Entities to 7 because the design needed a **Reporting Profile** (the two cadence profiles
FR-020 declares) and a **Registry Line Projection** (the read-only shape the digest consumes) as first-class
objects — both are projections of existing owners, not new stores, and both were added before the counts were
written. The second slice took the count to 9 by adding the **Efficiency Element** (the projection that rides the two
existing surfaces) and the **Measure Report** (the command's output) — again two projections/outputs over an owner
that already exists, so the "no new store" property is unchanged and measurable (`INV-15`).
