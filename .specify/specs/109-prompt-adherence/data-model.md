# Data Model — Prompt Adherence Evaluation（提示遵从度评价）

**Spec**: `.specify/specs/109-prompt-adherence/requirements.md`
**Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）
**Status**: Phase 1 design (this file is the design record; the live owners after implementation are
`shared/definitions/prompt-adherence-definitions.md` for meanings and the five
`shared/declarations/facts/prompt-adherence-*.yaml` files for value domains)

All closed tokens below are the plan-stage design fixed by this port's requirements (Assumptions and
Clarifications of 2026-11-27) plus the closed source design. The implementation writes them into the
owner document, the declarations and the engine, and the guards assert the three faces agree. Nothing in
this file may be read as an additional definition point once the owner document exists.

**No new persistent store**: every entity below is a read-time projection over existing records; the
engine writes nothing (requirements A-6, FR-005, FR-006). Store roots are the documented
`.specify/<store-name>/` projections of the names declared in
`shared/declarations/facts/runtime-store-layout.yaml#/statement`; that fact carries no per-store `root`
key and the engine holds no second root table (A-5, FR-030).

## E-1 — Prompt layer (提示层)

One of the two prompt surfaces the harness depends on.

| Field | Content | Rule |
|-------|---------|------|
| token | `host-prompt` ([[STR-001]]) or `project-rules` ([[STR-002]]) | closed set, owned by `prompt-adherence-layers.yaml` |
| text owner | host runtime (host-prompt) / this framework's instructions surface (project-rules) | meanings owned by the owner document § Layers |
| observability boundary | what records can and cannot say about adherence in this layer | owner document |

## E-2 — Signal class / catalog row (信号类)

One catalog row: a machine-checkable record predicate over one existing store.

| Field | Content | Rule |
|-------|---------|------|
| `row id` | one of the six ids of FR-028 | closed set, owned by `prompt-adherence-signals.yaml` |
| record predicate | the record kind, schema version and family test | owner document catalog table |
| source store and read surface | store root (derived from `runtime-store-layout.yaml`; probe row: the registry file) and the owning engine's read function | no second parser (C-032) |
| identity fields | the fields a run-identity scope joins on | owner document catalog table |
| timestamp field | the record's own timestamp used by windows | owner document catalog table; `—` = window-exempt |
| layer candidacy | `host-prompt` or `project-rules` | member of `prompt-adherence-layers.yaml` |
| strength | `direct` or `indirect` | member of `prompt-adherence-strengths.yaml` |
| allowed states | positive cap: `Exercised` (rows 1–5) or `Wired` (probe row) | members of the evidence seven-state domain; absence states are universal (I-6) |
| deviation classes | zero or more of the three class tokens | members of `prompt-adherence-deviation-classes.yaml` |

The six initial rows and their attribution are fixed by FR-028; the owner document carries them as the
machine-parsed catalog table, and the engine validates every cell against the declaration sets.

## E-3 — Assumed behavior (假定行为)

One named behavior of the premise chain under evaluation.

| Field | Content | Rule |
|-------|---------|------|
| id | `AB-NN`, dense in document order | owner document coverage map |
| statement | one sentence naming the assumed behavior | owner document |
| target | exactly one catalog row id or exactly one blind-spot id | FR-003; two-way machine check (E-5) |

Twelve initial assumed behaviors: six map to the six catalog rows (sensor side) and six map to the six
blind-spot classes. The mapping is the completed premise review.

## E-4 — Blind spot (盲区)

One assumed behavior no persisted sensor observes today.

| Field | Content | Rule |
|-------|---------|------|
| id | one of the six classes of FR-029 | owner document register (closed by its own revision) |
| reason | why no persisted sensor observes it today | FR-029 wording |
| capture direction | what an owner-sanctioned capture change would have to persist | FR-029 wording |

## E-5 — Coverage map (覆盖图)

The machine-checked relation from assumed behaviors to catalog rows or blind spots.

| Check | Rule | Failure |
|-------|------|---------|
| AB uniqueness | each `AB-NN` appears once | map finding |
| single target | each AB row names exactly one target kind and one target | map finding |
| target resolution | `sensor` targets resolve to a catalog row id; `blind-spot` targets resolve to a register id | map finding |
| row coverage | every catalog row id is cited by at least one AB | map finding (FR-003) |
| register coverage | every register blind-spot id is cited by at least one AB | owner-document completeness rule |

The check exits 0 with zero findings (SC-004) and is reachable as
`python3 .specify/scripts/python/prompt-adherence.py --check-coverage` (exit 1 with the sorted finding
list, exit 2 when the owner document is unreadable).

## E-6 — Adherence observation (遵从观察)

One catalog row's state for one reading scope.

| Field | Content | Rule |
|-------|---------|------|
| `row` | catalog row id | E-2 |
| `layer` / `strength` | the row's declared attribution, copied from the catalog | never reassigned at read time (FR-009) |
| `state` | evidence state (seven-state domain member) or `not_evaluated` | derived per the four-way rule below |
| `deviation_classes` | zero or more class tokens | only classes the row declares (FR-028) |
| `reason` | `{cause, source}` when the state is `not_evaluated` or `Unobserved`, else null | cause ∈ {`source-unavailable`, `no-matching-records`, `invalid-source`}; meanings owned by the owner document |
| `sources` | resolvable source references (E-11) | at least one when the state is positive |
| `state_counts` | per-state counts | longitudinal readings only |

State derivation (the complete four-way rule):
- source unreadable/absent → `not_evaluated` / `source-unavailable`;
- source readable, at least one valid matching record → the row's positive cap (`Exercised`, or `Wired`
  for the probe row) with deviation classes derived per E-7;
- source readable, matching records exist but none interpretable → `not_evaluated` / `invalid-source`
  (details in the reading's `invalid_sources`);
- source readable, zero matching records → `not_evaluated` / `no-matching-records` when the scope is an
  explicit run identity, `Unobserved` with the same reason otherwise.

No other state is producible; in particular no adherence verdict token (`adherent`, `deviant` or a
layer-level equivalent) may appear as a state, class or layer value (FR-018).

## E-7 — Deviation class (偏差类)

One named negative-observation kind a catalog row may testify.

| Token | Declared by | Derivation (cited from the source engine's own domain) |
|-------|-------------|----------------------------------------------------------|
| `axis-regression` | `run-determination-record` | an axis verdict reads `regressed` in `run-determination.py`'s comparison/correctness verdict domains |
| `green-unproven` | `run-determination-record` | artifact correctness reads the engine's `GREEN_UNPROVEN_VERDICT` pair (`not_evaluated` / `green_unproven`) |
| `evidence-missing` | `evidence-finding` | a finding item's `evidenceState` reads `Missing` |

Rows declaring no class can never produce a negative observation (FR-028). The classes are owned by
`prompt-adherence-deviation-classes.yaml`; their meanings and derivations by the owner document.

## E-8 — Adherence reading (遵从读取)

One per-run or longitudinal output.

| Field | Content | Rule |
|-------|---------|------|
| `reading_format` | integer `1` | engine schema |
| `engine` | `{path, version}` | version re-derived from the nearest `pyproject.toml` at run time |
| `declaration_set` | `{version, facts[]}` | version = SHA-256 over the five fact files (sorted repo-relative path + bytes), computed at read time |
| `scope` | E-9 | printed with its resolution basis |
| `status` | `complete` / `partial` / `no-data` / `not-found` | member of `prompt-adherence-reading-status.yaml`; derivation I-4 |
| `observations` | exactly one E-6 entry per catalog row, in catalog declaration order | FR-014 |
| `coverage` | `{observable[], not_observable[], blind_spots[], records_in_scope, invalid_records}` | mandatory section (FR-013); blind spots always the full register |
| `invalid_sources` | `[{path, cause}]`, sorted by path | cause ∈ {`unparsable`, `schema-violation`, `unknown-schema-version`, `invalid-timestamp`}; never silently skipped (FR-017) |
| `duplicates` | `[{row, identity, count, paths[]}]`, sorted | duplicate key = the row's declared identity fields (plus timestamp where declared); counted once per extra occurrence |

No `generated_at` or clock reading appears in a reading — identical inputs must reproduce byte-identical
output (FR-016), and an omitted window bound is printed as the literal `open` (FR-015). Output caps
(bounds, never judgement thresholds): per-observation source references 20, invalid sources 50,
duplicates 20, each with a shown/total disclosure when truncated.

## E-9 — Scope and window (范围与窗口)

| Field | Content | Rule |
|-------|---------|------|
| `kind` | `run` or `window` | `--run` → run; `--since`/`--until` → window; both together = input error |
| `run` | the run identity, or null | joins the rows' declared identity fields |
| `window` | `{since, until}` where each bound is a UTC timestamp or `open` | half-open `[since, until)` on each record's own timestamp field |
| `resolution` | `explicit` / `most-recent` / `none` | `most-recent` = the latest run identity observed across the catalog, selected by (timestamp desc, store name, source path) with its basis printed |
| `basis` | `{store, path, timestamp}` of the winning record, or null | printed in the scope for the default scope |

## E-10 — Declaration set (声明集)

The five facts read through `scripts/python/declaration_reader.py`:
`prompt-adherence-layers.yaml`, `prompt-adherence-strengths.yaml`, `prompt-adherence-signals.yaml`,
`prompt-adherence-deviation-classes.yaml`, `prompt-adherence-reading-status.yaml`. Observation states
are not a sixth fact: they compose `evidence-seven-states.yaml` (through `evidence-utils.py`) with the
`not_evaluated` literal of the run-determination value domains (through `run-determination.py`).

## E-11 — Source reference (源引用)

One resolvable citation: `{store, path, record, field}` where `store` is the store name from
`runtime-store-layout.yaml#/statement` (or `registry` for the probe row), `path` is repo-relative,
`record` is the record's identity tuple value, and `field` names the field the state derives from. A
third party must be able to reconstruct each observation state from these citations alone (FR-017).

## Cross-entity invariants

- **I-1 (one row, one observation)**: every reading carries exactly one observation per catalog row, in
  catalog order; no row is omitted and none appears twice (FR-014).
- **I-2 (declared attribution only)**: layer and strength are copied from the catalog declaration; the
  engine MUST NOT infer or reassign them at read time (FR-009).
- **I-3 (state derivation)**: E-6's four-way derivation is the complete rule; no fifth branch exists.
- **I-4 (reading status)**: `no-data` iff the resolved scope contains zero catalog records; `not-found`
  iff an explicit `--run` identity matches zero records; otherwise `partial` iff at least one observation
  is `not_evaluated`, else `complete`.
- **I-5 (absence is never adherence, never breach)**: `not_evaluated` / `Unobserved` with a reason are the
  only absence readings; missing records, missing gate observations and missing anomaly lines never read
  as clean or as violation (FR-011, FR-012).
- **I-6 (absence states are universal)**: every row may read `Unobserved` or `not_evaluated`; a row's
  declared allowed states cap only the positive state it may reach.
- **I-7 (deviation truth)**: a deviation class fires only from the derivation declared in E-7, only on a
  row declaring it; a row with no class yields no negative observation.
- **I-8 (no aggregate verdict)**: no observation, reading field or human line carries a layer-level or
  composite adherence verdict; counts by closed states plus coverage are the only aggregates (FR-010,
  FR-025).
- **I-9 (citation completeness)**: every positive observation cites at least one resolvable source
  reference; unresolvable references surface in `invalid_sources` (FR-017).
- **I-10 (duplicate disclosure)**: duplicates are counted once per extra occurrence and disclosed with
  their paths; they are never merged or double-counted silently.
- **I-11 (unknown token is a hard error)**: a token outside any declared set — in a declaration, the
  owner document's tables, or an engine argument — aborts with exit 2 and no reading; an undeclared store
  name in a catalog row is the same class (FR-030).
- **I-12 (read-only containment)**: a reading writes nothing under any root of
  `runtime-store-layout.yaml`; no cache, lock or mutable index exists; concurrent readings do not
  interfere (FR-006).
- **I-13 (privacy)**: only structured fields, closed tokens and source references cross into a reading;
  record prose (feedback review/points bodies, gate decision prose, finding summaries) never does.
- **I-14 (determinism)**: identical inputs and an identical engine version produce a byte-identical
  reading; ordering, tie-breaks and window arithmetic are the declared ones above.