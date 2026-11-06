# Data Model — Speckit 框架可视化（Speckit Framework Visualization）

**Feature**: 087 | **Date**: 2026-11-06 | **Plan**: `plan.md`

This model introduces **no new persistent store**. Seven of the nine entities are *views or obligations over state
that already has an owner*; the eighth (Reporting Profile) is a declared configuration pair read from one owner
document, and the ninth (Measure Report, added by the 2026-11-06 revision) is an output that is neither persisted nor
cached. Every field below names where its value comes from — an owner path plus a section anchor where one exists. A
field with no such owner is not in this model.

**Storage boundary**: nothing here creates a table, a database, a registry, a ledger or a second state spine
(`FR-018`). The only write a reporter performs goes to its own stream artifact, which is one of the three files the
External Dispatch Visibility Contract already declares. The exec-quant store (`.specify/memory/exec-quant/`) is
**read-only** for this feature: E8 and E9 read it and neither creates, migrates, rewrites or deletes anything in it
(`FR-024`).

## E1 — Reporter Seat

The team-roster seat bound to the reporting template. It is a **roster row**, not a new roster key
(`plan.md` D3), so the entity is a *view* over `skills/internal/create-team/references/create-mode.md` § Team Schema
`members[]` plus two seat-specific keys this feature introduces.

| Field | Type | Source / rule |
|-------|------|---------------|
| `agent` | slug | MUST resolve to the reporter Template (`agents/reporter.agent.md`, mirror `.specify/agents/templates/reporter.agent.md`) or to a seat instance that references it |
| `role` | literal `reporter` | the discriminator that makes the row a reporter seat; no other value creates one |
| `lifecycle` | `persistent` \| `temporary` | from the existing schema, unchanged |
| `reporting-territory.read` | list of paths/globs | what the reporter may read to build its line; MUST be a subset of the team's territory |
| `reporting-territory.write` | list of paths/globs | MUST resolve to exactly one path: the reporter's own stream artifact |
| `reporting-cadence` | duration or `default` | `default` resolves to the long-run profile of E6; an explicit value overrides per structure without a source edit (`FR-003`) |
| `reporting-reason` | one of `all-lanes-in-session-single-interval` \| `host-cannot-host-reporter` | the recorded-reason channel; **required** exactly when the seat's runtime execution is omitted (`FR-006`, `FR-021`) |

**Cardinality**: at most one reporter seat per team. Two reporter rows is a defect named by contract
`contracts/reporter-seat.contract.md` C-16 (the closed defect set: absent seat / unresolvable agent / two seats), and
E7 INV-03 states the same cardinality for the invariant table.

**Population the entity is read over** (`FR-006`; contract `contracts/reporting-obligations.contract.md` C-04 is the
owner of the rule): exactly two sets and no third — rosters **created or modified** through the team-creation entry
from the delivering commit onward, plus rosters **passed explicitly by path**. A roster already in the repository
when this feature lands is outside the population: it is not judged against the seat obligation, it is not
backfilled with a `reporting-reason`, and it does not become unrunnable. A guard run with no population path
supplied reports its roster proposition `not-evaluated` rather than judging the pre-existing rosters.

**Relationship**: one Reporter Seat → one Agent Template (E6 owner document defines the obligation; the template
provides the capability). One Reporter Seat → many Status Reports (E2).

## E2 — Status Report

**Definition (the vocabulary this spec's four names resolve to).** A **Status Report** is *the one line a single
tick (or a single trigger) emits* — E2 is exactly that object, and the four names the requirements and the contracts
use (`status line`, `status report`, `report`, `line`) all denote it. A **Supervision Report** (contract
`contracts/supervision-report.contract.md`) is that same object in its **sub-class shape**: the line a supervising
master emits to describe its sub-flows, carrying the E3 projection as its payload. There is no third term and no
second object; a clause that says "report" or "line" reaches one of these two by this sentence.

One emitted line. It is a **rendering**, not a persisted artifact (`requirements.md` Out of Scope; the received
carrier is recorded in the emitting flow's existing run record).

| Field | Type | Source / rule |
|-------|------|---------------|
| `structure.identity.slug` | slug | team slug (`create-mode.md` § Team Schema `slug`) or the supervising flow's declared identity |
| `structure.identity.run_stamp` | `<UTC>` stamp | the run stamp the emitting flow already writes (team run report filename / registry `run_id`) |
| `position` | `<stage> <k>/<N>` or an equivalent locating string | read from the emitting flow's own plan/task state (`FR-004` element 1, owner `progress-reporting.md` § 汇报内容下限) |
| `delta` | one clause | what changed since the previous report (element 2) |
| `remainder` | one clause + rough estimate, **or** the stated reason no estimate can be given | element 3 |
| `blocker` | one clause, literal `no blocker` when none | element 4; never omitted |
| `trigger` | `tick` \| `boundary` \| `transition:<sub-flow-id>` \| `reporter-failure` | which rule produced this line; `boundary` and `transition` are the two out-of-cadence triggers |
| `carrier` | `console` \| `<declared stream artifact path>` | which carrier actually received the line (`FR-007`, `FR-014`); recorded in the run record |
| `profile` | `long-run` \| `interactive` | the cadence profile in force when the line was emitted (E6) |
| `delay_reason` | string, optional | present only when the tick landed inside an atomic step and was delivered at the next boundary |

**Invariants**: INV-01 (four elements always), INV-02 (attribution never empty), INV-05 (no bare internal
identifier), INV-06 (never a question).

**Relationship**: many Status Reports → one Reporter Seat or one supervising master; each names its carrier, which
is either the console (no artifact) or the triplet's `.live.log` (E7).

## E3 — Supervised Sub-flow

A dispatched asynchronous delegation, as seen by its master. It is a **view** over the dispatch mapping the master
already records (`subagent-definitions.md` § External Dispatch Visibility Contract point 5: the label → CLI →
member → workspace mapping table in the run report) plus the triplet's mtimes.

| Field | Type | Source / rule |
|-------|------|---------------|
| `label` | `<team-slug>--<run-stamp>--<member-role>` | the existing label convention; the dispatch's stable identity |
| `state` | `running` \| `completed` \| `stalled` \| `failed` | `completed` from the `.status` file's `exit=0` or the terminal sentinel; `failed` from a non-zero exit; `stalled` when silence exceeds the threshold of E4; `running` otherwise — **`stalled` and `running` are never merged** (`FR-008`, `FR-009`) |
| `last_observed_activity` | ISO timestamp | newest mtime among the triplet files for that label |
| `age` | duration | now − `last_observed_activity`, computed at render time and always shown (`FR-008`) |
| `judged_against` | duration + the threshold row's identity | which declared threshold the `stalled`/`slow` judgement used (`FR-009`); never inferred per run |
| `slow` | boolean | true when age is below the threshold but the flow is not progressing; the line says which threshold it measured against |

**Deviation note**: the four states are a **projection**, not a new closed set — `running` / `completed` /
`failed` come from the triplet and the exit record the visibility contract already declares, and `stalled` is that
contract's existing judgement (point 4: "stalled growth beyond the team's stall threshold means a stalled agent").
`slow` is a **qualifier** on `running`, not a fifth state, precisely so no new vocabulary is created.

## E4 — Stall Threshold

The declared silence duration beyond which a sub-flow is judged stalled. **No number is defined here.**

| Field | Type | Source / rule |
|-------|------|---------------|
| `owner_path` | path | `skills/internal/create-team/references/patterns.md` |
| `owner_anchor` | section anchor | § Parallel Dispatch Pattern → Monitoring → **Stall Detection** |
| `row_identity` | the table row's `Condition` cell | which of the owner's rows the judgement used (e.g. the "no manifest created" row vs the "manifest stuck" row) |
| `value` | duration | read from the owner's `Threshold` cell at render time; **MUST NOT be copied into any other file** |
| `measured_silence` | duration | the observed age being judged |

This entity exists so that the *reference* has a home while the *number* keeps its single definition point.
`.specify/shared/guidelines/one-source-of-truth.md` is the discipline: a copy of the number anywhere else would be a
second definition that drifts.

## E5 — Current-State Digest

The on-demand bounded projection (`FR-011`, `FR-012`). An **output**, never a stored object. Its **workspace rule**
is `FR-011`'s: only the registry entries whose `project_dir` equals the current workspace are listed and counted
against `cap`; an entry belonging to another project is neither rendered nor labelled, so the projection has no
`other-project` state.

| Field | Type | Source / rule |
|-------|------|---------------|
| `generated_at` | ISO timestamp in UTC | when the render ran |
| `entries[]` | list of `Digest Entry` (below) | at most `cap` entries |
| `omitted` | integer | the number of entries the cap dropped; MUST be rendered as `omitted=<n>` when non-zero (`FR-012`) |
| `cap` | integer | the declared cap in force for this render (default declared in the script, overridable per invocation) |
| `stale_bound` | duration | the declared age beyond which an entry is marked stale; its **declaration point** is the constant in `scripts/python/status-digest.py` (ownership row in `contracts/ownership-map.contract.md` C-47), which is what `SC-005`'s "declared stale bound" resolves to |
| `state` | `active` \| `nothing-running` | `nothing-running` is an **explicit rendered state** with exit status `3`, never an empty result (`FR-011`, SC-005) |
| `profile_summary` | one clause | which cadence profiles are in force across the active lines (E6) |

### Digest Entry

| Field | Type | Source / rule |
|-------|------|---------------|
| `line_id`, `run_id` | identifiers | registry entry (E7) |
| `state` | one of the registry's `STATE_VALUES` | **quoted from the engine**, never re-enumerated here |
| `project_dir` | path | registry entry `project_dir`; the workspace rule above compares it to the current workspace and drops a non-matching entry before the cap is applied |
| `stage` | string or `-` | registry entry `stage` |
| `last_activity_at` | ISO timestamp | registry entry `updated_at`, or the newest triplet mtime when the entry declares triplet paths |
| `age` | duration | now − `last_activity_at`, always rendered |
| `stale` | boolean | `age > stale_bound` |
| `agent_activity` | list of `{label, state, age}` | the E3 projection for lines whose dispatch mapping is readable |
| `last_completion` | one entry, optional | the most recently `completed` entry of the set |

**Bounding rule**: the cap is applied **after** a total ordering (active lines first, then by descending
`last_activity_at`, ties broken by `line_id` ascending), so two renders over the same registry produce the same
first-N set — that determinism is what makes `omitted=<n>` meaningful.

## E6 — Reporting Profile

The two declared cadence values and the one condition selecting between them (`FR-020`).

| Field | Type | Source / rule |
|-------|------|---------------|
| `long-run.default` | duration | **the single definition site**: `shared/guidelines/reporting-obligations.md`. The value is 30 seconds; no other file restates it (`SC-006`) |
| `long-run.condition` | predicate | "the structure has at least one live status receiver" — a reporter seat whose runtime execution is not omitted, or a supervising master with ≥1 dispatched sub-flow |
| `interactive.default` | duration | **owned by** `shared/guidelines/progress-reporting.md` § 默认间隔与覆盖; this model does **not** carry the number |
| `interactive.condition` | predicate | the negation of `long-run.condition` |
| `selection_record` | `{profile, selected_at, reason}` | written once per run into the emitting flow's existing run record; a mid-run switch to `interactive` is recorded with its cause (Edge Cases: "the switch is recorded, never silent") |
| `override` | per-run / per-structure value | replaces `default` for that structure; recorded with the profile so the guard can tell an override from the definition site |

**Invariant INV-04**: the two profiles never emit inside one run as if they were one cadence — every Status Report
carries `profile`, and a run that switches records the switch before its first line under the new profile.

## E7 — Registry Line Projection

The read-only shape the digest and the guard consume. It is a **projection of an existing owner**: the fields are
exactly what `skills/external/sdd-loop-driver/scripts/line-registry.py` already writes per line. No new file, no new
field, no new access path.

| Projection field | Registry source |
|------------------|-----------------|
| `line_id`, `run_id`, `project_dir`, `branch`, `stage`, `state`, `updated_at` | the per-line entry `<line_id>.json` |
| `triplet.status`, `triplet.log`, `triplet.heartbeat` | the entry's declared `status_path` / `log_path` / `heartbeat_path` when present; absent → the projection reports `-` |
| `is_active` | derived by the engine's own `ACTIVE_STATES` predicate; the digest does not invent a second one |
| `registry_dir` | resolved by the same order the engine documents: `$SPECIFY_LINE_REGISTRY_DIR`, then `$XDG_STATE_HOME/spec-kit/lines`, then `~/.local/state/spec-kit/lines` |

**Where the spine fits**: a line's *spine document* under `.specify/state/<line_id>.md` is **not** parsed by the
projection. The registry entry is the machine-readable owner of line state; parsing the spine's Markdown would
create a second parser for the same facts (`research.md` RO-06 records this correction). A digest entry may cite the
spine path for a human to open, but its fields come from the registry.

## E8 — Efficiency Element

**Revision 2026-11-06, entity 8.** One bounded element per listed unit, carried as **content** of E5's digest entry
and of the status line E2 defines (`FR-023`). It is a **projection over a projection**: its quantities come from the
exec-quant store, which this feature reads and never writes, and its host is the surface that already lists the unit.
No third surface is opened.

| Field | Type | Source / rule |
|-------|------|---------------|
| `unit.identity` | user-facing unit name | the surface's own listed unit, rendered in a readable form (`INV-05`); never a bare engine identifier |
| `elapsed.value` | integer ms **or** the not-evaluated marker | the record's `quality.elapsed_ms` node, read through the store engine's read path (owner: `shared/declarations/facts/quant-record-schema.yaml#/statement` — the field and its type are **not** restated here) |
| `elapsed.provenance` | one member of the schema's declared provenance vocabulary | the record's own node; the vocabulary is reached **by reference** to the declaration owner and never enumerated here (C-71) |
| `tokens` | integer **or** the not-evaluated marker | the record's token quantity; rendered only while the element fits the host surface's bound (C-64) |
| `invocations` | integer **or** the not-evaluated marker | the record's invocation quantity; same all-or-nothing rule |
| `source_record` | record identity (the record file's name stem) | the record chosen by the selection rule below; carried for traceability, never rendered as a raw id |
| `degradation` | `full` \| `elapsed-only` | `elapsed-only` when tokens/invocations were withdrawn **from every unit on this render together**; the withdrawn quantity is named in the surface's existing omitted summary (E5 `omitted`) |
| `store_state` | `populated` \| `no-measurements` | `no-measurements` when the store is absent or holds no record; the host surface's own content is unchanged in that case (`FR-024`) |

**Selection rule (one rule, owned by the requirements' FR-024; quoted here only as the projection shape)**: for a
unit the surface lists, the element reads the record with the **latest `collected_at`**, with ties broken by the
record's own identity in ascending byte-stable order. Nothing is folded: no average, no sum, no ranking, no lifetime
aggregate — those belong to E9, a different question.

**Bounding rule**: the element is *content*, so the host's own bound applies unchanged — the digest's cap (E5) and
the status line's entry bound. When the token/invocation quantities do not fit, they are dropped from **every** unit
on that render together and named once in the omitted summary. Per-unit depth differences are forbidden
(`FR-023`, Clarifications Q2).

## E9 — Measure Report

**Revision 2026-11-06, entity 9.** The output of `/speckit.measure` (`FR-026`…`FR-029`). An **output**, never a stored
object: nothing here is persisted, cached or written back, and the command writes no file at all.

| Field | Type | Source / rule |
|-------|------|---------------|
| `window.since` | ISO timestamp or the literal "all records" | resolved from `--since`; with no bound the report states the whole store explicitly (C-54) |
| `window.end` | ISO timestamp or the literal "all records" | `since + --window`; the **only** wall-clock-dependent text the report may carry (C-61) |
| `window.rule` | literal `half-open` | `start ≤ collected_at < end`, so two adjacent windows partition the store |
| `selection` | list of `(unit_id, unit_type)` **or** the literal "all units" | matched as an exact set; an identity the store does not hold is an input error naming it (C-55) |
| `cap` | integer | the **default per-record cap printed on every run**, overridden by `--cap`; the number is declared once in `scripts/python/measure.py` and carried nowhere else (`C-47` row) |
| `rows[]` | list of Measure Row (below) | one row per selected unit identity, ordered `(unit_type, unit_id)` ascending |
| `excluded` | four named counts + one omitted count | the classes and the "omitted is not a class" rule are owned by `contracts/measure-report.contract.md` C-58 / C-57; this entity names the fields and restates no rule |
| `figures_measurable` | integer | how many selected rows carried at least one measurable figure; `0` is a **produced report** at exit `0`, not the nothing-to-analyse case (C-59) |
| `exit_hint` | one of the four declared statuses | which status the run took; the set is owned by `contracts/measure-report.contract.md` C-59 |

### Measure Row

| Field | Type | Source / rule |
|-------|------|---------------|
| `unit_id`, `unit_type` | strings | the **identity pair**; the store holds one `unit_id` under more than one type, and the pair is what keeps two different units from merging into one row (C-55) |
| `records` | integer | the count of contributing records in the window, after truncation (a **sum**) |
| `elapsed` | `{median, min, max, provenance, covered}` **or** the not-evaluated marker | median over the in-window records with min and max named; `covered` is present when only some records carried the quantity (C-56) |
| `tokens` | `{sum, provenance, covered}` **or** the not-evaluated marker | a sum, with the count of records that carried it |
| `invocations` | integer **or** the not-evaluated marker | a sum |

**Invariants**: INV-13 (the element never opens a third surface and never grows the unit set), INV-14 (a listed unit
with no record carries the marker, never an omission), INV-15 (both reads leave the store byte-identical and add no
path), INV-16 (the report is a measurement, never a verdict), INV-17 (a produced report, a nothing-to-analyse run
and an input error are three distinguishable outcomes of one closed status set).

## Invariants (asset-level, checked by the guard and by contract tests)

| ID | Invariant | Judged by |
|----|-----------|-----------|
| INV-01 | Every Status Report carries all four content elements; `blocker` is present as `no blocker` rather than omitted | `contracts/status-report.contract.md` SR-02 (C-23); guard proposition RO-05 |
| INV-02 | Every Status Report names its structure slug and run stamp; two structures cannot produce an identical unattributed line | SR-01 (C-22); `tests/contract/test_reporting_obligations.py` (attribution is C-22's subject, not RO-05's four elements) |
| INV-03 | A roster in E1's population has at most one reporter seat, and a missing seat is a **named defect** unless a `reporting-reason` is recorded | `contracts/reporter-seat.contract.md` RS-03 (C-16), RS-04 (C-17); guard RO-04 |
| INV-04 | The two cadence profiles never compete inside one run; a profile switch is recorded before the next line | SR-09 (C-30); `tests/contract/test_reporting_obligations.py` (profile selection is C-30's subject, not RO-09's) |
| INV-05 | No emitted line carries an internal engine identifier where a user-facing name exists; the line is readable by a reader who did not take part in the run | SR-10 (C-31); `shared/guidelines/user-facing-comprehension.md` |
| INV-06 | A status report is a one-way statement: it never awaits a response and its presence authorizes nothing | SR-08 (C-28); guard RO-10 |
| INV-07 | Every dispatched sub-flow appears in its master's report at least once; presence is a closure requirement, not a best effort | `contracts/supervision-report.contract.md` MV-02 (C-33); guard RO-06 |
| INV-08 | The reporter's authority is read + write-own-stream; it never dispatches, authorizes, retries or terminates | RS-06 (C-19), RS-07 (C-20) |
| INV-09 | A significant state transition (sub-flow failure, stall crossing, dispatch failure) produces a line **before** the next tick | MV-03 (C-34); guard RO-08 |
| INV-10 | The digest's entry count never exceeds the declared cap and the omitted count is stated when it truncates | `contracts/status-digest.contract.md` DG-03 (C-43); `tests/unit/test_status_digest_unit.py` (the cap is C-43's subject, not a proposition of its own) |
| INV-11 | An entry whose age exceeds the stale bound is marked stale with its age; stale data is never presented as current | DG-04 (C-44) |
| INV-12 | No scheduler, timer service, daemon, third-party dependency, new persistent store, console channel, registry, state spine or ledger is introduced | `contracts/ownership-map.contract.md` OM-04 (C-50); guard RO-13 |
| INV-13 | The efficiency element appears on exactly two surfaces (status line, digest), never grows the unit set, and never becomes an extra line or a second cadence | `contracts/efficiency-element.contract.md` EF-01 (C-63); `tests/contract/test_efficiency_element.py` |
| INV-14 | A listed unit with no record at all carries the not-evaluated marker; it is never dropped, and a missing quantity is never rendered as `0` | EF-02/EF-05 (C-64, C-67); `tests/contract/test_efficiency_element.py` |
| INV-15 | Reading the store for the element and for the report leaves every file under `.specify/memory/exec-quant/` byte-identical and creates no new path there | EF-07 (C-69), ME-10 (C-62); the before/after per-file digest in `test-evidence/` (SC-012 Source) |
| INV-16 | The measure report presents measurements and issues no verdict: no score, no threshold judgement, no baseline recommendation, no persisted trend | `contracts/measure-report.contract.md` ME-04 (C-56); `tests/contract/test_measure.py` vocabulary check |
| INV-17 | "A report was produced", "nothing to analyse" and "input error" are three distinguishable outcomes of one closed four-value status set; each renders its own explicit statement | ME-07 (C-59); `tests/contract/test_measure.py` |

## State transitions

The **reporter seat** has three states and one transition set, which is the whole of its lifecycle:

| From | To | Allowed | Condition |
|------|----|---------|-----------|
| absent | seated | yes | roster creation writes a `role: reporter` member |
| seated | runtime-omitted | yes, narrow | all lanes execute in the current session **and** the run is expected to finish inside one cadence interval; `reporting-reason` is required |
| runtime-omitted | seated | yes | a `modify` run whose condition no longer holds |
| seated | absent | **no** | removing the seat without a reason is the defect INV-03 names; the only legal removal path is `seated → runtime-omitted` with its recorded reason |

The **supervised sub-flow** transitions are the visibility contract's, quoted not redefined: `running → completed`
(exit 0 / terminal sentinel), `running → failed` (non-zero exit), `running → stalled` (age crosses the E4
threshold), and `stalled → running` (growth resumes). No transition is invented here.

## Validation rules (from the requirements)

1. A `reporting-territory.write` that resolves to more than one path is a defect — the reporter's write surface is
   exactly its own stream artifact (RS-06).
2. A `reporting-reason` present while the seat **is** executing is a defect — the reason exists only to record an
   omission.
3. A Status Report whose `carrier` is absent from the run record violates FR-007.
4. A digest rendering `state: active` while `entries[]` is empty is a defect; an empty set must render
   `nothing-running`.
5. A stall judgement whose `judged_against` does not resolve to the owner table's row is a defect (FR-009).
6. An efficiency element that renders `0` for a quantity the record marks not evaluated is a defect; so is an
   element omitted for a listed unit (INV-14). Where the token/invocation quantities do not fit the bound, they are
   withdrawn from every unit on that render together — one unit showing them beside another without is a defect
   (C-64).
7. A measure row that merges two `unit_type` values under one `unit_id` is a defect, and so is a `--unit` value the
   store does not hold rendered as an empty section instead of an input error (C-55).
8. A measure run over a store holding no record in the resolved window that renders a zero-valued row instead of the
   explicit `no measurements` statement is a defect (C-59).
9. Any delivered artifact that restates the exec-quant schema's version, provenance vocabulary or unit-type
   vocabulary instead of naming the declaration owner is a defect (C-71, `contracts/ownership-map.contract.md`
   C-47).
