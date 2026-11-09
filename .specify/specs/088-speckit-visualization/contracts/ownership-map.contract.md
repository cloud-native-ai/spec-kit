# Contract: Ownership Map and Zero-New-Machinery Audit

**Feature**: 088 | **Covers**: FR-018, FR-024, FR-025, FR-028, FR-029, SC-006, SC-008, SC-010, SC-012, SC-014
**Contract object**: the ownership relations this feature creates, and the mechanically decidable audit that it
introduced nothing it prohibits. Every clause is judged over the delivered changed-file set (`base..head` plus the
working tree at implementation time).

Clause ids are dense (`OM-01`…`OM-06`) and are cited verbatim by `/speckit.tasks`. The second slice added two
capabilities (the efficiency element and `/speckit.measure`) whose **own** clause ids live in
`contracts/efficiency-element.contract.md` (`C-63`…`C-71`), `contracts/status-digest.contract.md` (`C-72`)
and `contracts/measure-report.contract.md` (`C-53`…`C-62`); this file carries only the ownership relations and the machinery audit those capabilities are
judged by, and renumbers no clause.

---

## C-47 · OM-01 — Every new fact has exactly one owner, and every consumer reaches it by path

The delivered files MUST satisfy this table. A fact appearing as a definition in two rows of the "consumer" column
is a defect.

| Fact | Owner (definition site) | Consumers (reach by path / anchor) |
|------|-------------------------|------------------------------------|
| Long-run cadence default (30 s) | `shared/guidelines/reporting-obligations.md` | the reporter Template body; the create-team schema note; `coaching-skills` § Dispatch Payload (by anchor only — C-39 forbids the literal); the digest's rendered profile summary; the guard's RO-03 scan |
| Interactive cadence default | `shared/guidelines/progress-reporting.md` | unchanged; the new owner points at it and carries no number of its own |
| Content floor (four elements) | `shared/guidelines/progress-reporting.md` § 汇报内容下限 | the new owner (by anchor), the reporter Template, this contract's C-23 (labels only) |
| Artifact triplet + execution modes | `shared/definitions/subagent-definitions.md` | the new owner, the digest's carrier resolution, the reporter Template |
| Stall threshold numbers | `skills/internal/create-team/references/patterns.md` § Monitoring → Stall Detection | the new owner (by anchor), the supervision report (row identity only) |
| Line state vocabulary | `skills/external/sdd-loop-driver/scripts/line-registry.py` (`STATE_VALUES`, `ACTIVE_STATES`) | the digest's projection (`data-model.md` E7) — quoted, never re-enumerated |
| Registry directory resolution | same engine (`resolve_registry_dir`) | the digest (C-42 restates the order because the script cannot import the engine; that restatement is the one legal duplicate and is marked as such in the script's docstring) |
| Digest cap default | `scripts/python/status-digest.py` (a declared constant) | the digest's rendered `cap=<n>` and the guard's DG-03 proposition — no other file carries the number |
| Digest stale bound default | `scripts/python/status-digest.py` (a declared constant) | the digest's rendered `stale` marker and the age it shows (`data-model.md` E5 `stale_bound`) — this row is the declaration point `SC-005`'s "declared stale bound" resolves to, and no other file carries the number |
| Exec-quant record schema (version, closed vocabularies, field slots, per-action manifest) | `shared/declarations/facts/quant-record-schema.yaml#/statement`, read by `scripts/python/exec-quant.py` through `scripts/python/declaration_reader.py` | the efficiency element (E8) and the measure report (E9) — **read-only by path**; no delivered artifact restates a version, a vocabulary member or a field name (C-71, C-53) |
| Exec-quant store layout + read path (record directory, legacy stream, reader composition) | `scripts/python/exec-quant.py` (`storage_dir`, `read_jsonl_safe`, `read_entry_files`, `load_store`) | `scripts/python/measure.py` and the digest's efficiency projection — imported in-process, one reader, two projections (C-65) |
| Exec-quant store **writer** | `scripts/python/exec-quant.py` (its `collect` / `collect-dispatch` / `score` actions) | nobody in this feature: the delivered set contains no write path, no recorder, no migration and no schema extension (C-70) |
| Measure default per-record cap | `scripts/python/measure.py` (one declared constant, printed on every run) | the report's own `cap=<n>` line and its JSON `cap` key — no other file carries the number (C-57) |
| Measure exclusion-class names (`unreadable` / `legacy-format` / `outside-window` / `unknown-unit`) and the "omitted count is not a class" rule | `contracts/measure-report.contract.md` C-58 | the report's rendered counts, its JSON `excluded` block, and `data-model.md` E9 — named, not re-enumerated (C-58) |
| Measure exit-status set (`0` / `2` / `3` / `1`) | `contracts/measure-report.contract.md` C-59 | `templates/commands/measure.md` (contract § Delegation names them), the report's `exit_hint` key, `tests/contract/test_measure.py` |
| Efficiency-element selection rule (latest by `collected_at`, ties by record identity) | the requirements' FR-024 | `data-model.md` E8 and `contracts/efficiency-element.contract.md` C-66 pin the projection shape; neither re-derives the rule |
| Not-evaluated marker literal | `shared/guidelines/reporting-obligations.md` § 九 · 当前态摘要契约 (the digest contract's rendering vocabulary) | the efficiency element's renderer and the measure report's `not evaluated` wording — same marker, reached by anchor |

*Judged by*: `tests/contract/test_reporting_obligations.py` — a scan set derived **from the delivered files
themselves** (the owner-literal scan's query set is extracted from what landed, not from the author's intention —
the framework's own One-Source-Of-Truth verification rule) must report exactly one definition site per row.

Requirements served: (FR-018, FR-024, FR-025, SC-006, SC-012).

## C-48 · OM-02 — The ownership relation to pre-existing owners is declared, in one direction

Each owner this feature touches — the new one and every pre-existing one — MUST be recorded with its relation, in
exactly one of five forms: `owns` (the new owner document), `consumes` (reached by path), `amends` (a bounded edit),
`preserves` (untouched because the feature deliberately keeps its clauses), `extends` (an existing subtree gains
declared content without any of its clauses being rewritten). The declared set MUST be:

| Owner | Relation |
|-------|----------|
| `shared/guidelines/reporting-obligations.md` (NEW) | `owns` — the new owner document |
| `shared/guidelines/progress-reporting.md` | `consumes` — no clause of it is rewritten (`SC-008`) |
| `shared/definitions/subagent-definitions.md` | `consumes` + one pointer line added |
| `shared/workflow/external-dispatch-recipes.md` | `consumes` + one pointer line added |
| `shared/guidelines/fast-fail.md` § 子代理派发注入 | `preserves` — the dispatch injection clause is referenced, never modified |
| `shared/guidelines/user-facing-comprehension.md` | `consumes` — the emitted line is a governed surface |
| `shared/guidelines/confirmation-gates.md` | `preserves` — no gate is added (measured: 27 blocking gates before and after) |
| `skills/internal/create-team/` | `extends` — roster schema note + create step + guard script |
| `skills/external/coaching-skills/SKILL.md` § Dispatch Payload | `amends` — exactly one field, one forbidden class, one return clause (`FR-019`) |
| `skills/external/sdd-loop-driver/scripts/line-registry.py` | `consumes` — registry entry fields + `STATE_VALUES` / `ACTIVE_STATES` + directory resolution, read-only |
| `shared/declarations/facts/quant-record-schema.yaml` | `preserves` — read by path, **not** extended: the elapsed field already exists and the extension route is closed for this feature (`FR-025`, C-70) |
| `scripts/python/exec-quant.py` | `consumes` — its read path is imported by both projections and its writer is never called; no line of it is edited (C-65) |
| `shared/declarations/facts/` (the declarations directory) | `extends` — **no** new fact file is added; the existing `quant-record-schema.yaml` already carries every field the two capabilities read |
| `templates/commands/` | `extends` — one new command template (`measure.md`) beside the existing ones; no existing template is rewritten |
| `scripts/python/measure.py` (NEW) | `owns` — the measure analysis engine and its declared cap |

*Judged by*: `feature-ref.md` § Consuming / Consumed Owners carries the same fifteen rows (same documents, same
order, same relation words) and the contract test asserts the two are consistent (no relation appears in one and
not the other).

Requirements served: (FR-013, FR-024, FR-025, FR-029, SC-008).

## C-49 · OM-03 — No new persistent store, channel or registry

The changed-file set MUST introduce:

- no new file under `.specify/state/`, `.specify/memory/`, or any registry directory — **including
  `.specify/memory/exec-quant/`**, which is read-only for this feature and gains no record, index, cache or lock;
- no new output file written by any delivered script except the reporter's own stream artifact (which is one of the
  triplet files the visibility contract already declares); `measure.py` writes nothing at all, not even a report
  file (`FR-026`, `FR-028`);
- no new environment variable that selects a store (`SPECIFY_LINE_REGISTRY_DIR` and friends are read, never
  introduced; the measure script reads none and takes its workspace root the way the store engine does).

*Judged by*: `status-digest.py --action guard` proposition RO-13 plus a changed-path audit in
`tests/contract/test_status_digest.py`, and the store-digest comparison `tests/contract/test_measure.py` performs
around a measure run (C-69).

Requirements served: (FR-018, FR-024, SC-012).

## C-50 · OM-04 — No scheduler, timer, daemon or third-party dependency

The changed-file set MUST introduce:

- no process spawn in any delivered script (no `subprocess`, `os.system`, `os.exec*`, `os.fork` on a delivery
  path);
- no sleeping loop and no background thread (`threading`, `multiprocessing`, `asyncio` task loops, timers);
- no new entry in `pyproject.toml` dependency lists (the change MAY touch nothing in that file at all).

The cadence is executed by the running flow between its own steps — the same mechanism the progress-reporting
discipline already mandates — so no scheduler is needed or permitted. `/speckit.measure` runs when invoked and
exits: it is not a watcher or a daemon, and it schedules nothing (`FR-026`).

*Judged by*: `tests/contract/test_status_digest.py` and `tests/contract/test_measure.py` — an AST-level import and
call audit over every delivered `.py` file, plus a pin on `pyproject.toml`'s dependency lists against the
pre-change baseline.

Requirements served: (FR-018, FR-026, FR-029, SC-006, SC-014).


## C-51 · OM-05 — Pre-existing behaviour is the compatibility baseline, measured by name

The feature is additive. The regression criterion is **name-level**: the pre-change node-id set of the affected
suites equals the post-change node-id set for pre-existing tests, and any renaming or removal is named and
justified.

Affected pre-existing suites (measured before the change): `tests/contract/test_progress_reporting.py`,
`tests/contract/test_coaching_dispatch_contract.py`, `tests/contract/test_agent_dispatch_mechanism.py`,
`tests/contract/test_team_territory.py`, `tests/contract/test_improve_team_presence.py`,
`tests/contract/test_team_command_routing.py`, plus — added by the second slice — `tests/contract/test_exec_quant_engine.py`
and `tests/contract/test_status_digest.py`, which read the store engine and render the two visibility surfaces.

One suite is expected to change **by design**: `tests/contract/test_coaching_dispatch_contract.py`'s
`REQUIRED_FIELDS` tuple gains `reporting-cadence`. That change is declared here so it is not read later as a
regression; it is the amendment's own test update (`FR-019`).

One suite is expected to gain **items** by design: `tests/contract/test_status_digest.py` gains the efficiency
element's rendering assertions (`FR-023`). Additions are named here; a **removed or renamed** pre-existing node in
either suite is a regression.

`tests/contract/test_exec_quant_engine.py` is the store engine's own suite and MUST stay **fully green and
name-identical**: this feature reads the store and never writes it, so a change there is evidence of a write path
this feature is not allowed to have (`FR-024`, `FR-025`, C-70).

*Judged by*: the implement-stage baseline/closure name-level diff, plus this clause being the declared expected
delta.

Requirements served: (FR-019, FR-024, FR-025, SC-008, SC-009, SC-012).

## C-52 · OM-06 — The delivered set is auditable as a file list, not as a claim

`feature-ref.md` MUST enumerate the delivered paths. The audit MUST be able to answer "which of these paths is a
scheduler, a store, a channel, a registry?" by reading the list, and the answer MUST be "none".

The enumeration MUST be **one list** covering both slices: the status/digest capability's paths and the second
slice's paths (the measure command template and its per-tool copies, `scripts/python/measure.py` and its mirror, the
efficiency element's test files) stand in the same table, so an auditor never has to reconcile two inventories
(`FR-029`).

*Judged by*: `contracts/ownership-map.contract.md` OM-03/OM-04 (C-49, C-50) plus `feature-ref.md` § Delivered
Paths, whose table is the enumerated file list this clause reads.

Requirements served: (FR-018, FR-029, SC-010).
