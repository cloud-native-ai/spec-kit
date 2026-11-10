# Feature Reference — 096-sdd-observer-agent

**Feature ID**: 096 | **Feature Name**: SDD 专用观察者与线级观察记录（sdd-observer）
**Requirement key**: `096-sdd-observer-agent` | **Branch**: `096-sdd-observer-agent`
**Status at this stage**: `Draft → Clarified → Planned` | **Date**: 2026-11-10

## Binding

| Item | Value |
|------|-------|
| Spec directory | `.specify/specs/096-sdd-observer-agent/` |
| Stage status so far | requirements done (23 FR / 7 SC) → clarify done (no FR/SC change; 6 pre-plan rulings) → plan done (this file created; the clarify-stage binding row is registered) |
| Flow class | `execution` (`flow-class-check.py` read twice: requirements stage and this plan stage, exit 0) |
| Lifecycle owner | `skills/external/sdd-loop-driver/SKILL.md` § SDD Observer |
| Format owner | `shared/declarations/facts/journal-format.yaml` |
| Engine | `scripts/python/journal-utils.py` |

## Delivered paths (file-level inventory, plan-refined)

| # | Path | Kind | FR |
|---|------|------|----|
| 1 | `agents/sdd-observer.agent.md` | **NEW** Agent Template — role face `observer`, read domain, write surface, forbidden capabilities, subagent rule, fast-fail clause | FR-001, FR-002, FR-016, FR-022 |
| 2 | `.specify/agents/templates/sdd-observer.agent.md` | generated mirror of row 1 (`sync-mirrors.py --only agents`); never hand-edited | FR-001 |
| 3 | `.claude/agents/sdd-observer.md`, `.qoder/agents/sdd-observer.agent.md`, `.github/agents/sdd-observer.agent.md`, `.opencode/agents/sdd-observer.md` | generated render copies (`specify render-agents --ai <tool>`, tools qoder / claude / copilot / opencode); never hand-edited | FR-001 |
| 4 | `shared/declarations/facts/journal-format.yaml` | **NEW** declaration fact (`kind: record-schema`) — header/entry keys, sixteen event classes with `min_persistent`, retention classes, pointer kinds, placeholder, escape rule, journal filename | FR-010, FR-011, FR-012 |
| 5 | `scripts/python/journal-utils.py` | **NEW** deterministic engine — `append` projection + `check` validation + single-writer flock; script-interface compliant; stdlib only | FR-013, FR-014, FR-015, FR-011 |
| 6 | `.specify/scripts/python/journal-utils.py` | generated mirror of row 5 (`scripts/` → `.specify/scripts/`); never hand-edited | FR-015 |
| 7 | `skills/external/sdd-loop-driver/SKILL.md` | edit — one new H2 `## SDD Observer（观察者：启动、记录节与收束）`: entry switch, startup point, instance duty, record-section shape, restart, terminal close, non-blocking; one References line to row 8 | FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-020, FR-023 |
| 8 | `skills/external/sdd-loop-driver/references/observer-lifecycle.md` | **NEW** driver reference — dispatch brief template, read domain, engine loop/actions, gap semantics, failure semantics, forbidden list, dispatch-injection clause | FR-005…FR-009, FR-013, FR-016, FR-018, FR-022 |
| 9 | `skills/external/sdd-loop-driver/references/stage-prompts.md` | edit — exactly one pointer line in § 状态脊 to the record-section owner (no key copy) | FR-004, FR-017 |
| 10 | `.specify/skills/sdd-loop-driver/SKILL.md` + `.specify/skills/sdd-loop-driver/references/observer-lifecycle.md` + `.specify/skills/sdd-loop-driver/references/stage-prompts.md` | generated mirrors of rows 7/8/9 (`skills/external` → `.specify/skills`); never hand-edited | — |
| 11 | `tests/contract/test_sdd_observer_agent.py` | **NEW** guard — template frontmatter, role face, verbatim prohibition, read/write surface, subagent rule, fast-fail clause, instance identity duty | FR-001, FR-002, FR-016, FR-022, SC-004 |
| 12 | `tests/contract/test_sdd_observer_lifecycle.py` | **NEW** guard — startup point, entry switch, spine record keys, restart/terminal, non-blocking predicate + red mutation leg, digest boundary baseline | FR-004…FR-009, FR-017, FR-018, FR-020, FR-023, SC-003, SC-006 |
| 13 | `tests/contract/test_journal_engine.py` | **NEW** guard — append/check/idempotency/gap/single-writer/dual-line + five tamper drills + script interface | FR-011…FR-015, SC-001, SC-002, SC-004, SC-005, SC-007 |
| 14 | `tests/contract/test_sdd_loop_driver_skill.py` | edit — deliberate H2 pin update (one new section) and `MIRROR_FILES` gains the new reference | FR-003, FR-004 |
| 15 | `tests/contract/test_fast_fail_discipline.py` | edit — deliberate `FACTORY_PRESETS` 17 → 18 and the bounded count 19 → 20 | FR-001 |
| 16 | `tests/fixtures/sdd-observer/` | **NEW** fixture directory — line builder (spine + quartet + checkpoints + git), dual-line builder, failure builder | SC-001, SC-003, SC-005, SC-007 |
| 17 | `docs/reference/skills/sdd-loop-driver.md` | edit — one short observer section (mechanism sentence + owner pointers) | FR-001, FR-018 |
| 18 | `.specify/features.md` row 096 + `.specify/features/096.md` | registry (this plan creates both; status `Planned`) | — |
| 19 | `.specify/specs/096-sdd-observer-agent/test-evidence/` | plan + implement evidence (gate readings, tamper drills, baseline captures) | SC-001…SC-007 |

Every row 2, 3, 6 and 10 reaches the runtime tree through framework generators, so none is written twice by hand.

## Deliberate non-deliverables

- **No new `/speckit.*` command, no new skill directory, no new scheduler/daemon/registry/store** (FR-006, FR-017, A7).
- **No edit to `scripts/python/status-digest.py`** — the observer rides the existing `--sub-flow` supervision projection (FR-017, SC-006).
- **No edit to `shared/guidelines/reporting-obligations.md`**, to any stage command template, or to `shared/declarations/contract.yaml` (R-05: registration would break the 094 C-86 closed-set pin; the fact is read by file through the declaration reader).
- **No edit to `driver-stage-sequence.yaml` / `driver-stage-artifacts.yaml`** — the journal is not a stage artifact and does not enter `STAGE_ARTIFACTS` (A12).
- **No edit to `checkpoint-protocol.md`** — checkpoint files are read as carriers; the protocol keeps its five parts.
- **No observer-specific digest field, row or section** — the only supervision identity is the label convention.

## FR → Contract map

| FR | Contract clause |
|----|-----------------|
| FR-001 | `observer-role.contract.md` C-01, C-02, C-03; `observer-verification.contract.md` C-08 |
| FR-002 | `observer-role.contract.md` C-03, C-06 |
| FR-003 | `observer-role.contract.md` C-09; `observer-lifecycle.contract.md` C-05 |
| FR-004 | `observer-lifecycle.contract.md` C-03, C-04, C-05 |
| FR-005 | `observer-lifecycle.contract.md` C-02, C-03, C-11 |
| FR-006 | `observer-role.contract.md` C-10; `observer-lifecycle.contract.md` C-06 |
| FR-007 | `observer-lifecycle.contract.md` C-06 |
| FR-008 | `observer-lifecycle.contract.md` C-07 |
| FR-009 | `observer-lifecycle.contract.md` C-08, C-09 |
| FR-010 | `journal-format.contract.md` C-02, C-03, C-13 |
| FR-011 | `journal-format.contract.md` C-04, C-05, C-09; `journal-engine.contract.md` C-11 |
| FR-012 | `journal-format.contract.md` C-06; `journal-engine.contract.md` C-11 |
| FR-013 | `journal-format.contract.md` C-10, C-12; `journal-engine.contract.md` C-04 |
| FR-014 | `journal-format.contract.md` C-07, C-08 |
| FR-015 | `journal-engine.contract.md` C-01, C-02, C-09, C-10, C-13 |
| FR-016 | `observer-role.contract.md` C-05; `journal-engine.contract.md` C-13 |
| FR-017 | `observer-lifecycle.contract.md` C-09; `observer-verification.contract.md` C-06, C-09 |
| FR-018 | `observer-role.contract.md` C-08; `observer-lifecycle.contract.md` C-09, C-11 |
| FR-019 | `observer-role.contract.md` C-10; `observer-verification.contract.md` C-08 |
| FR-020 | `observer-lifecycle.contract.md` C-09; `observer-verification.contract.md` C-03 |
| FR-021 | `observer-lifecycle.contract.md` C-10 |
| FR-022 | `observer-role.contract.md` C-07, C-08 |
| FR-023 | `observer-lifecycle.contract.md` C-01, C-09 |

## SC → Measurement map

| SC | Measurement | Evidence |
|----|-------------|----------|
| SC-001 | coverage fixture over the declared stage sequence; deletion/one-row removal turns red | `test_journal_engine.py`, `tests/fixtures/sdd-observer/` |
| SC-002 | persistent-pointer resolution + forged-pointer drill | `test_journal_engine.py`, `test-evidence/` |
| SC-003 | start-failure and mid-run-kill fixtures reach terminal; gate-mutation red leg | `test_sdd_observer_lifecycle.py` |
| SC-004 | three tamper fixtures red; verbatim prohibition in the template | `test_journal_engine.py`, `test_sdd_observer_agent.py` |
| SC-005 | first-row ordering; dual-line isolation; same-line second writer exit `3` | `test_journal_engine.py` |
| SC-006 | write-surface declaration; digest token scan; pre-implementation digest baseline delta empty | `test_sdd_observer_lifecycle.py`, `test-evidence/` |
| SC-007 | skipped-window fixture emits `observer-gap` with both window ends | `test_journal_engine.py` |

## Overlap adjudication (R-09)

`overlap-check.py` reported `decision: overlap` (55 relations). None is a real delivery conflict:

1. **Template-example artifacts** — `templates/commands/x.md`, `scripts/python/doc-consistency-check.py`, `templates/commands/plan.md`, `shared/workflow/expression-gates.md` etc. appear in `current_paths` because the freshly copied **plan template** contains them as examples and obligation pointers. This feature does not deliver them.
2. **Requirements-side citations** — `shared/declarations/facts/concurrency-class.yaml`, `serial-reason.yaml`, `effective-concurrency.yaml`, `shared/definitions/subagent-definitions.md`, `shared/guidelines/user-facing-comprehension.md`, `shared/workflow/acceptance-hardening.md` are **read** by the requirements' own runtime-stack/obligation prose; the requirements declare no write to them.
3. **Framework-wide references** — the `nested-path` relations against `shared/declarations/` and `templates/commands/` come from those citations, not from files this feature writes.

Real file-level adjacencies (same file, different section) and their disposition:

| File | Other line | Disposition |
|------|-----------|-------------|
| `skills/external/sdd-loop-driver/SKILL.md` | 063 / 070 / 093 (landed history) | additive H2 only; their sections unchanged; 093 closed as `Blocked` (no active writer) |
| `skills/external/sdd-loop-driver/references/stage-prompts.md` | 058 / 064 / 065 / 093 (landed) | one pointer line in § 状态脊; no rule text moved |
| `tests/contract/test_sdd_loop_driver_skill.py` | 058 / 063 / 070 / 093 | deliberate pin update (H2 + mirror list) |
| `tests/contract/test_fast_fail_discipline.py` | 052 / 084 / 087 | deliberate preset-enumeration update |
| `docs/reference/skills/sdd-loop-driver.md` | 058 / 064 / 065 | one additive section |

No active line shares a delivered path at the time of this plan (measured: the only `Blocked` line 093 has no open edit window; 091 is `Completed`; 094 is `Ready for Review`).
