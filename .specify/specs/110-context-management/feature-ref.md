# Feature Reference — 110-context-management

**Feature ID**: 110 | **Feature Name**: Context Management（上下文管理）
**Requirement key**: `110-context-management` | **Branch**: `110-context-management`
**Supersedes**: none. Adjacent owners stay: 095 (super↔sub protocol and payload), 044 (agent metadata
render pipeline — the `## Project Context` carrier), 084 (declaration layer and framework map), 051
(comprehension and glossary disciplines), 090 (re-anchoring tiers), 055 (memory stores), 093 (concurrency
obligation), 091 (git-workflow declaration), 040 (token-efficiency cap owner), 089 (script interface), 105
(runtime store roster), 046 (confirmation-gate rules).

**Binding note**: Feature 110 is the fixed binding (A-2). By the line constraint this run writes no
registry row, no feature detail, no `.specify/register.md` row and no decision archive entry — those
registrations are a recovery point handed to the line close-out's Feature Integration Protocol. The
absence of a `.specify/features.md` row at plan time is therefore expected, not a missing feature.

## Requirement → Contract → Carrier

| FR | Contract clause(s) | Test / evidence carrier |
|----|--------------------|--------------------------|
| FR-001 (one owner document, pointer discipline) | C-001, C-002, C-003 | `test_context_management_owner.py` |
| FR-002 (two categories, membership test, derived) | C-002, C-006, C-011 | `test_context_management_declarations.py`, `test_context_management_owner.py` |
| FR-003 (three layers by owner location) | C-002, C-006, C-011 | `test_context_management_declarations.py`, `test_context_management_owner.py` |
| FR-004 (layout table owns the per-row data; roster owned by the classes fact; eighteen-class seed) | C-004, C-015 | `test_context_management_owner.py`, `test_context_management_engine.py` |
| FR-005 (existing owners not replaced) | C-003, C-025, C-044 | `test_context_management_owner.py`; full suite |
| FR-006 (system layer: discovery + constraint pointers; probe judgments; probe failure reads a token, never a finding) | C-005, C-020, C-033 | `test_context_management_owner.py`, `test_context_management_engine.py` |
| FR-007 (project layer from `.specify/`) | C-004, C-020, C-021, C-033 | `test_context_management_owner.py`, `test_context_management_engine.py` |
| FR-008 (task layer selection; inline-digest standing witnesses) | C-021, C-027 | `test_context_management_owner.py`, `test_context_management_engine.py` |
| FR-009 (five forms and the legality matrix) | C-005, C-011, C-032 | `test_context_management_declarations.py`, `test_context_management_engine.py` |
| FR-010 (no invariant content in the variable layer; two decidable shapes) | C-027 | `test_context_management_engine.py` (decidable shapes); review |
| FR-011 (no persistence; durable set closed) | C-029, C-045 | `test_context_management_readonly.py` |
| FR-012 (baseline composed once; session vs line; refresh only on triggers) | C-020 | `test_context_management_owner.py`; source-drift fixture |
| FR-013 (task composition under caps, no form widening) | C-021 | `test_context_management_owner.py`, `test_context_management_engine.py` |
| FR-014 (closed seven-trigger set incl. `reentry`) | C-022, C-028 | `test_context_management_owner.py` |
| FR-015 (composer roles through the existing model) | C-023 | `test_context_management_owner.py` |
| FR-016 (source drift observed, never polled) | C-024 | `test_context_management_owner.py`, `test_context_management_engine.py` |
| FR-017 (existing payload remains the carrier; no field/injection/cap/identifier added) | C-025, C-042, C-044 | `test_context_management_owner.py` (protocol-boundary leg) |
| FR-018 (four declaration facts; append-only registration; unknown declaration member refused; layout token = finding) | C-010, C-011, C-012, C-015, C-016, C-046 | `test_context_management_declarations.py`, `test_context_management_engine.py` |
| FR-019 (bounds referenced, never redeclared) | C-013 | `test_context_management_declarations.py`, `test_context_management_engine.py` |
| FR-020 (presence vocabulary defined once; reason-bearing absences; `Unobserved` by pointer) | C-014, C-033 | `test_context_management_owner.py`, `test_context_management_engine.py` |
| FR-021 (one read-only engine; actions, flags, JSON keys, exit codes, layer-root rule) | C-012, C-016, C-030, C-031, C-032, C-033 | `test_context_management_engine.py` |
| FR-022 (deterministic and honest; source-reading digest; no host values) | C-032, C-034 | `test_context_management_engine.py` |
| FR-023 (publish → install → init; framework-map rows; mirrors) | C-036 | `tests/integration/test_context_management_init.py`; mirror check |
| FR-024 (offline, no transmission, no raw text) | C-035, C-045 | `test_context_management_readonly.py`; init fixture (network-blocked) |
| FR-025 (one ambient instructions section; budget `within`) | C-037 | `test_context_management_owner.py`; `test_instructions_section_propagation.py` |
| FR-026 (no new command or skill wrapper) | C-030, C-045 | `test_context_management_engine.py`; review of the changed set |
| FR-027 (guards; one seeded violation per checked rule; mutation drill proves the guard, not the engine) | C-040, C-041, C-042, C-043, C-046 | the guard roster; mutation captures |
| FR-028 (concept-consistency slot and honest absence) | C-007, C-014, C-025, C-026, C-034, C-042 | `test_context_management_owner.py`, `test_context_management_engine.py` |
| FR-029 (layer landing contract) | C-004, C-006, C-043 | `test_context_management_owner.py`, `test_context_management_engine.py` |

## Success criteria → evidence carrier

| SC | Path | Evidence carrier |
|----|------|------------------|
| SC-001 (check clean here; four seeded violations exact; byte-identical reruns) | final | `test_context_management_engine.py`; captured run per single-run evidence |
| SC-002 (fixture hash manifest unchanged; zero new files) | final | `test_context_management_readonly.py` (C-041) |
| SC-003 (absence, empty, unreachable exact; all-present fixture every row present) | final | `test_context_management_engine.py` (manifest fixtures) |
| SC-004 (form-by-layer matrix enforced; two layer-form findings on the merged fixture) | final | `test_context_management_engine.py`; repository `check` run |
| SC-005 (fresh project offline: check 0; manifest project absence lines; no socket) | final | `tests/integration/test_context_management_init.py` |
| SC-006 (every bounded-index row cites a resolvable cap owner; no numeric bound; no cap literal added) | final | `test_context_management_engine.py` (cap-reference leg); repository scan |
| SC-007 (every domain member exercised; facts and engine agree; unknown member refused) | final | `test_context_management_declarations.py` |
| SC-008 (full suite zero new failures; mirrors byte-identical; protocol item set, recall output and renderer fixture unchanged) | supporting | full-suite capture; `sync-mirrors.py --check`; protocol-boundary and renderer-fixture legs |
| SC-009 (ambient section present in a fresh init; pointer shape guarded; `BUDGET:` `within`) | final | init fixture; ambient-section guard (C-037) |
| SC-010 (three concept rows present here; seeded absence reads exact tokens; consistency `Unobserved`; protocol boundary intact) | final | `test_context_management_owner.py`; `test_context_management_engine.py` (concept-row legs) |
| SC-011 (three legal cells pinned, three forbidden named, no category column, every row in its legal cell) | supporting | `test_context_management_owner.py` (landing-cell legs); `check` run |

## Notes

- Contract clauses are local to this spec's `contracts/`; the meaning owner after implementation is
  `shared/definitions/context-management-definitions.md` (C-001).
- No new `/speckit.*` command or skill wrapper ships; the entry is the engine (C-030, C-045).
- The four declaration facts are the only new value-domain files; no numeric cap is introduced anywhere
  (C-013).
- The mechanism references the super↔sub protocol, the agent render path, memory recall, the
  instructions/constitution generators and the declaration layer by pointer and edits none of them beyond
  the three framework-map rows, the one instructions-template section and the four append-only
  registration keys (C-044).
- The source capability's Tier G / Tier T seven-component package and its `project-context-render.py` do
  not exist in this repository; the mapping lands on the real payload and the real render path (A-3), and
  the presence vocabulary is defined here once because no prior framework owner exists (A-8).