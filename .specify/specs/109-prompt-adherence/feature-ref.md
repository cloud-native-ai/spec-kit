# Feature Reference — 109-prompt-adherence

## Binding

| Field | Value |
|-------|-------|
| Requirement key | `109-prompt-adherence` |
| Bound Feature | **109 — Prompt Adherence Evaluation（提示遵从度评价）** |
| Binding basis | New standalone feature (adjudicated at requirements A-2 and registered at clarify): the capability is an additive port of the closed ai-harness spec 092 (its Feature 097), not a slice of any adjacent owner. The candidate owners — 056 Probe-Handler 体系, 059 exec-quant, 028 Feedback Mechanism, 105 Runtime Store Layout, 038 Evidence Infrastructure plus the run-determination engine — each own one sensor surface; none owns a reading mechanism. |
| Registry posture | Plan-stage Feature Integration: Feature 109 advances `Draft → Planned` in `.specify/features.md` with a plan note in `.specify/features/109-prompt-adherence.md`. `.specify/register.md` and the driver state spine stay untouched (stage brief's "spine/registry" boundary, read as the ID register + spine; the feature index and detail are this stage's mandated Feature Integration output). |
| Feature detail | `.specify/features/109-prompt-adherence.md` |
| Source (behavior authority) | `/storage/project/cloud-native-ai/ai-harness/.ah/specs/092-prompt-adherence/` — plan, research, data-model, five contract files (39 clauses, C-001…C-046), quickstart; consumed as dated records, never edited |
| Integration authority | This tree's owners: `runtime-store-layout.yaml`, `declaration_reader.py`, the six sensor engines, `framework-map.md`, `sync-mirrors.py`, `run-tests.sh` |

## Delivery surface (framework source → runtime mirror)

| # | Source path | Role | Mirror / copies |
|---|-------------|------|-----------------|
| 1 | `shared/definitions/prompt-adherence-definitions.md` | NEW owner document: premise chain, two-layer model, six-row catalog, assumed-behavior coverage map, six-class blind-spot register, reading-contract meanings, red lines | `.specify/shared/definitions/prompt-adherence-definitions.md` (sync-mirrors) |
| 2 | `shared/declarations/facts/prompt-adherence-{layers,strengths,signals,deviation-classes,reading-status}.yaml` | NEW five closed-set facts — the value-domain owners | same relative paths under `.specify/shared/declarations/facts/` (sync-mirrors) |
| 3 | `scripts/python/prompt-adherence.py` | NEW single-file read-only engine: readings, `--check-coverage`, script-interface flags | `.specify/scripts/python/prompt-adherence.py` (sync-mirrors) |
| 4 | `shared/definitions/framework-map.md` | EDIT: two rows — owner document and reading entry | `.specify/shared/definitions/framework-map.md` (sync-mirrors) |
| 5 | `tests/contract/test_prompt_adherence_owner.py` | NEW guard: owner declaration, bilingual forms, catalog/register tables, coverage-map two-way check, framework-map row | none (repo-internal) |
| 6 | `tests/contract/test_prompt_adherence_declarations.py` | NEW guard: five facts, required keys, membership equality, cross-agreement, owner↔engine reason agreement, unknown-token rejection, degradation exits | none |
| 7 | `tests/contract/test_prompt_adherence_engine.py` | NEW guard: CLI surface, fixture readings, determinism, scope/window, duplicates, invalid sources, privacy, layer honesty, exit codes, audit replay | none |
| 8 | `tests/contract/test_prompt_adherence_readonly.py` | NEW guard: the containment claim (hash manifest, zero new files, bytecode exclusion) | none |
| 9 | `tests/integration/test_prompt_adherence_init.py` | NEW fixture: fresh init contains the mechanism, installed entry answers `--version`, bare invocation honest + exit 0 offline, mirror parity | none |
| 10 | `tests/fixtures/prompt-adherence/` | NEW declarative seed sets (six-row coverage, absence, invalid records, duplicates, window boundaries, privacy prose markers, doctored map copies) | none (repo-internal, not shipped) |

Not touched: existing engines and their stores (`run-determination.py`, `exec-quant.py`,
`feedback-utils.py`, `evidence-utils.py`, `probe-utils.py`, `measure.py`), `runtime-store-layout.yaml`,
`.specify/.gitignore`, `templates/`, per-tool command copies, skills, decision governance (107 stays
independent), the driver state spine and `.specify/register.md`.

## FR → surface map

| FR | Delivering surface |
|----|--------------------|
| FR-001, FR-002, FR-019 | owner document (§ Premise Chain, § Layers, § Entry) + framework-map owner row + `owner-and-catalog` C-001/C-002 + owner guard |
| FR-003 | owner document coverage map + engine `--check-coverage` + C-003 + owner/engine guards |
| FR-004, FR-028 | owner document catalog table + `prompt-adherence-signals.yaml` + C-004/C-005 + owner/declarations guards + fixtures |
| FR-005, FR-030 | engine sensor reads through owning surfaces + layout fact via `declaration_reader` + C-032 + declarations/engine guards |
| FR-006 | read-time projection design + C-029/C-041 + readonly guard |
| FR-007 | pure-consumer boundary + C-043 + full suite (existing owner guards) |
| FR-008 | baseline/keep channel + C-035 + audit-replay leg |
| FR-009, FR-010 | declared attribution (owner doc rows) + C-016 + engine layer-honesty legs |
| FR-011, FR-012 | data-model E-6 four-way absence + C-028 + engine absence legs |
| FR-013 | mandatory coverage section + C-025 + engine coverage legs |
| FR-014 | reading shape + scope resolution + C-020/C-021 + engine legs |
| FR-015 | longitudinal window + C-022 + engine window-arithmetic legs |
| FR-016, FR-017 | determinism/ordering/duplicates/caps + citations/invalid sources + C-023/C-024 + engine legs |
| FR-018 | five facts + reason taxonomy + C-010/C-014/C-015 + declarations guard |
| FR-020 | distribution via mirrors + `specify init` + two framework-map rows + C-033 + init guard + mirror check |
| FR-021 | offline/privacy + C-027/C-034 + engine/init legs |
| FR-022 | exit codes and degradation + C-026 + engine exit-code legs |
| FR-023 | single invocation + flags + version/workspace resolution + C-030/C-031/C-036 + engine CLI legs |
| FR-024 | guard roster + decidable containment claim + C-040/C-041/C-042 + the five guard files through `scripts/bash/run-tests.sh` |
| FR-025 | no score/ranking + C-044 + engine no-verdict legs |
| FR-026 | dated baseline reading + C-035/C-045 + baseline feedback entry + audit-replay leg |
| FR-027 | host observations stay integration input + C-046 + engine layer-honesty legs |
| FR-029 | six-class blind-spot register + engine coverage section + owner guard |

## SC → evidence map

| SC | Evidence |
|----|----------|
| SC-001 | `tests/contract/test_prompt_adherence_engine.py` fixture-reading legs + run-A/run-B determinism leg |
| SC-002 | `tests/contract/test_prompt_adherence_readonly.py` hash-manifest containment (per-run and longitudinal readings) |
| SC-003 | engine layer-honesty legs with the project-only and indirect-only fixtures |
| SC-004 | `--check-coverage` clean leg (exit 0) and doctored-map leg (exit 1, named findings) + owner guard |
| SC-005 | `tests/integration/test_prompt_adherence_init.py` (fresh init, socket-blocked, explicit `not_evaluated`, exit 0) |
| SC-006 | engine audit-replay leg (every observation resolves; seeded broken reference reported as invalid source) |
| SC-007 | declarations guard (every closed-set member exercised; unknown member rejected non-zero) |
| SC-008 | the dated baseline feedback entry + one replay run against its cited references |
| SC-009 | init guard artifact inventory + `sync-mirrors.py --check` no NEW drift + framework-map parse leg + full suite via `scripts/bash/run-tests.sh` |

## Supersession and dated records

- The ai-harness 092 artifact set remains the behavior authority as dated records (external path in the
  Binding table); this spec's contract set is the live contract face for the port. No existing
  spec-kit owner is superseded: every sensor owner keeps its semantics, red lines and records.
- The source's `templates/tasks-template.md` change (commit `94f77ee` there) is deliberately not
  imported — it belongs to the task-deferral convention line, not to adherence semantics (A-8).

## Handoff to `/speckit.tasks`

- **Tests Mode**: ON (execution class, Principle IV); the five guard files are authored red-first, before
  the engine exists; the closed sets get reverse samples (unknown tokens, doctored map, undeclared
  store).
- **Regression surface**: the existing owner guards (`test_runtime_store_layout.py`,
  `test_script_interface_contract.py`, evidence/exec-quant/feedback/probe suites) must stay green; the
  full suite runs once through `scripts/bash/run-tests.sh` for the implement-stage baseline.
- **Re-measure list**: see `research.md` § Re-measure list (store roster 14/no `root`, probe counts,
  mirror baselines, `SPECKIT_PYTHON`, six read-surface names/fields).
- **Adapter reminders**: every source naming is adapted (`.specify`, `/speckit.*`, `specify init`,
  `speckit.*` kind tokens); the store-layout read goes through `declaration_reader.py`, never a ported
  `store_layout.py`.
- **Wrap-up duties**: the dated baseline reading lands as one feedback entry through the existing
  engine; no new store, no ignore rule, no store-layout change.