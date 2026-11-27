# Implement Package P3 Stage Evidence — 2026-11-27

Line `decision-batch-panel`; run `r20261127T081500Z-112a`; stage `implement` package **P3** (tasks T031–T045); baseline `ebcdabf26`; branch `112-decision-batch-panel` (worktree `.specify/.tmp/sdd-loop/worktrees/decision-batch-panel`).

## Scope executed

| Task | Result |
|------|--------|
| T031 | US2 mirror pairs regenerated and verified: `sync-mirrors.py --write` then `--check` rc 0 (`shared/` 123 / `scripts/` 135 files byte-identical); `cmp` byte-identical for the owner page, the engine and `validate-decisions.py`; the checker ran over a batch-record fixture with `PASS: 0 violation(s) (rules: M-01…M-04, M-08, M-09)` rc 0, family fields admitted |
| T032 | US2 phase tests green: 13-test selection `13 passed`; full two-module reading `52 passed`; evidence in `notes/us2-green.txt`; S3 slots green in `notes/red-first-evidence.md` |
| T033 | 6 US3 red-first unit tests authored over populated `register-updates`, `register-absent`, `concurrency`, `replay-broken` fixtures; red run `6 failed` recorded with `--names-out notes/red-first-names-us3.txt` |
| T034 | Owner page § 批次登记与来源更新（Register Reflection & Source Updates）: birth registration (per carrier + range grouping legal), status cells (settled → `resolved(...)`; parked stays `open`-prefixed and annotated; rows never deleted; nothing else rewritten), block `resolution` append, absent-register creation from the four-column header, failure disclosure and the read-time join |
| T035 | Owner page § 重放契约（Replay Contract）: record-only reconstruction scope, pointer resolution and named non-zero failure, deterministic read-only replay, self-contradiction refusal, engine-judges boundary |
| T036 | `record` write-back in `scripts/python/decision-batch.py`: register appended rows + status-cell replacement (cell-local byte edits), block `resolution` insertion (append-only, content otherwise byte-identical), absent-register creation, pre-computed disclosures in the batch-record closing, post-write failure disclosure in the output payload |
| T037 | `replay` action: record + resolvable-pointer reconstruction (item rows, completeness, defaults/grounding, dispositions, decision records), row↔decision consistency refusals, every evidence/option pointer resolved, named non-zero exit for unresolvable pointers, byte-identical repeated output, zero writes |
| T038 | US3 mirrors regenerated and verified (check rc 0; owner page + engine `cmp` byte-identical) |
| T039 | US3 phase tests green: `6 passed`; evidence in `notes/us3-green.txt`; S4 slots green |
| T040 | 6 US4 red-first unit tests authored (`test_completeness_claim_shape`, `test_bookkeeping_identity_holds`, `test_absent_source_named_not_clean`, `test_nothing_pending_success_no_record`, `test_unclassifiable_candidate_refused`, `test_no_partial_complete_claim`); red run `6 failed, 2 passed` (the 2 passes are T042's ordered guards) with `--names-out notes/red-first-names-us4.txt` |
| T041 | Owner page § 完备性与拒绝（Completeness & Refusal）: the closed-set claim's four elements, the bookkeeping identity and partition sum, carrier-level refusal vs block-level defects, named absence, `nothing-pending`, no silent drop, exit-code pointer |
| T042 | Ordered regression guards `test_unreadable_source_refusal` (over `unreadable-register`) and `test_batch_record_head_completeness` (over `batch-family`), placed after their subjects (T019/T030) and disclosed as the regression exception — green at authoring, never claimed red-first |
| T043 | Completeness hardening: structured `bookkeeping.completeness_claim` (referent / comparison unit / empty allowed delta / owner pointer / verdict / candidate count / partition / named absent sources), same claim lines in the batch-record head (`完备性声明` / `分区` / `缺席来源`), absent carriers in the user-facing disclosure, and `os.walk`-based enumeration whose `onerror` converts unreadable directories into a carrier refusal instead of the silent `rglob` skip |
| T044 | US4 mirrors regenerated and verified (check rc 0; owner page + engine `cmp` byte-identical) |
| T045 | US4 phase tests green: 9-test selection `9 passed` (six red-first legs + two ordered guards + the engine interface contract); evidence in `notes/us4-green.txt`; S5 slots green |

Task states closed in `tasks.md`: T031–T045 all `[X]` (15 rows); `validate-tasks.py` → 0 errors / 0 warnings (rc 0). 28 tasks remain open (US5 + Polish).

## Gate readings (all executed this package)

| Check | Command | Result |
|-------|---------|--------|
| US2 phase | `run-tests.sh tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py -q -k <US2 selection>` | **13 passed** (rc 0) |
| US3 phase | same unit module, six-name selection | **6 passed** (rc 0) |
| US4 phase | unit + contract module, nine-name selection | **9 passed** (rc 0) |
| Full two-module reading | `run-tests.sh tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py -q` | **52 passed** (rc 0) |
| Targeted regression set | decision-batch modules + governance contracts/guards + `test_migration_distribution.py` + `test_probe_nonentity_catalog.py` + `test_validate_decisions.py` | **117 passed** (rc 0) |
| Mirrors | `sync-mirrors.py --write` then `--check`; `cmp` on the pairs | rc 0; byte-identical |
| Validator over batch record | `validate-decisions.py --action records --carrier <record-at-workspace-root> --register <fixture register>` | `PASS: 0 violation(s)` rc 0 |
| Gate neutrality | `.specify/scripts/python/scan-confirmation-gates.py --summary` | 30 blocking (22/7/1) / 0 violations — zero NEW hits vs `test-evidence/scan-confirmation-gates-baseline.txt` |
| Instruction section | section extraction on `.specify/instructions.md` | `## Decision Items` = **1,276 B**, unchanged |
| Protected files | `git status --short` on `.specify/.gitignore` / `register.md` / `instructions.md` / `glossary.md` / `features.md` | empty |
| Tasks validator | `validate-tasks.py .specify/specs/112-decision-batch-panel/tasks.md` | 0 errors / 0 warnings, rc 0 |
| Workspace guard | `workspace-guard.py --snapshot …/workspace-implement-p3.json`; `--check` at wrap-up | snapshot recorded; check reading in `test-evidence/workspace-implement-p3-check.txt` |

Pre-existing (attributed, not caused here): `tests/contract/test_decision_tension_contract.py::TestScenarioFTerminologyZeroHit::test_a3_alias_list_still_exists` and `::TestScenarioBAnalyzeStructuralChannel::test_channel_only_add_allowed_delta_enumeration` fail identically at baseline `ebcdabf26` in a detached scratch worktree with the same two names; they pin analyze-skill / decision-tension surfaces this package never touches.

## Red/green pointers

- Red-first evidence: `notes/red-first-evidence.md` § S4/S5 (executed-run records appended), name lists `notes/red-first-names-us3.txt` (6) and `notes/red-first-names-us4.txt` (6).
- Green evidence: `notes/us2-green.txt`, `notes/us3-green.txt`, `notes/us4-green.txt`.
- Clause green points: C-401…C-409, C-501…C-504 (T032); C-505…C-508 (T039); C-601…C-608 (T045) — 34 of the 54 clauses.

## Corrections applied (in passing)

- `test_no_cross_batch_preauthorization` (P2) asserted the exclusion `via == "prior-batch"`; with the source-side `resolution` update landed, the declared primary read-time join is `resolution-field`. The assertion was widened to the two declared joins (`resolution-field` / `prior-batch`); the `prior-batch` branch stays pinned by the write-failure段落 of `test_resolution_annotation_and_disclosure`. Disclosed in `notes/us2-green.txt` § 5.
- The red-first slot table's placeholder test names (`test_absent_register_creation`, `test_batch_head_completeness`) were aligned to the authored names (`test_absent_register_created_from_header`, `test_batch_record_head_completeness`); fixtures unchanged except `test_unclassifiable_candidate_refused` which builds its unreadable directory at test time on a `two-source` copy.

## Boundaries held

- No edit to the state spine, `.specify/register.md`, `.specify/instructions.md`, `.specify/.gitignore`, `.specify/glossary.md`, `.specify/features.md`, other specs or the main tree; no push.
- No new runtime store root; no batch record written into this worktree's runtime store (all demo records stayed under `.specify/.tmp/`, removed at wrap-up).
- **A-26 preserved**: distinct batch ids → distinct knowledge paths (verified `…157afafc` vs `…c850ac7e`), later batches never modify earlier records, reads of another batch's settled record only for the declared read-only purposes (already-resolved join is how batch two excludes batch one's identity).
- **A-27 preserved**: no write-back path outside register appended rows / status cells / block `resolution`; the `superseded_by` face stays US5-owned and unimplemented here.
- Zero network access; zero feedback-store write by the mechanism; record still refuses unattended/undeclared authorization.

## Concurrency

`requested=1`; `effective=1`; `effective_reason=write-conflict` — owner page, engine, tests and fixtures are single-writer surfaces; the package is one serial unit.
