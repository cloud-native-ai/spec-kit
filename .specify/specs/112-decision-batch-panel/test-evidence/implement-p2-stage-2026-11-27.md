# Implement Package P2 Stage Evidence — 2026-11-27

Line `decision-batch-panel`; run `r20261127T081500Z-112a`; stage `implement` package **P2** (tasks T016–T030); baseline `fc674b4f5`; branch `112-decision-batch-panel` (worktree `.specify/.tmp/sdd-loop/worktrees/decision-batch-panel`).

## Scope executed

| Task | Result |
|------|--------|
| T016 | Owner page § 待决策项块（Pending Item Block）: heading/field-line grammar, the ten-field closed set, the five block-level defect names, the incompleteness rule, and the mutual non-judgement boundary (a pending block is not a decision record) |
| T017 | Owner page § 批次状态（Batch States） + § 批次呈现契约（Batch Presentation Contract）: the six qualification states with the documented precedence and named reason vocabulary, exclusion states, per-item slots, the five-answer batch context floor, the no-truncation rule, deterministic order, digest determinism and the user-facing identifier boundary |
| T018 | Owner page § 建议默认值与依据（Recommended Default & Grounding）: declared-default-only rule, the closed three-input grounding join, `grounded`/`no-evidence` semantics, pointer resolvability, basis-is-not-evidence, prior-decision conflict, engine-judges boundary |
| T019 | `scan` core in `scripts/python/decision-batch.py`: register predicate (word-boundary `open`), fence-aware block parser, byte-equal identity merge with locator split, register↔block linkage (`authority-unresolved` / `ambiguous-link`), class gate incl. same-identity class conflict, already-resolved read-time join (resolution field + settled prior-batch identities), named exclusion families, presence readings with carrier-level refusal, deterministic ordering, zero writes |
| T020 | Grounding join and prior-decision conflict detection: closed carrier set, resolvable-only pointers, anchor checking, `no-evidence` emission, conflict with prior pointer + chosen label |
| T021 | `--format json` payload and `--format text` renderer as projections of one row set (row-count/identity equality; the text body carries no internal identifiers) incl. the batch context floor |
| T022 | Mirror pairs regenerated and verified: `sync-mirrors.py --write` then `--check` rc 0 (`shared/ == .specify/shared/`, 123 files byte-identical); `cmp` byte-identical for the owner page and the engine |
| T023 | US1 phase tests green: `25 passed` (21 unit + 4 contract); evidence in `notes/us1-green.txt`; S2 slots green in `notes/red-first-evidence.md` |
| T024 | 12 US2 red-first unit tests authored (`reply-shapes`, `eligibility-matrix`, `drift`, `batch-family` fixtures populated); red run `12 failed, 21 passed` recorded with `--names-out notes/red-first-names-us2.txt` |
| T025 | `test_signal_mapping_pointer_only` (C-408) authored red-first; red run recorded (`notes/red-first-names-us2-contract.txt`) |
| T026 | Owner page § 决策批次与应答（Decision Batch & Reply）: reply definition, caller-declared authorization, identity binding, validation-before-write, verbatim layer vs rationale key points |
| T027 | Owner page § 批次处置与沉默接受默认（Batch Disposition & Acceptance by Silence）: closed dispositions, the eligibility conjunction, explicit settlement of ineligible items, park semantics, no unhandled settlement / no cross-batch pre-authorization, the signal mapping by pointer (value domain not restated) |
| T028 | Owner page § 批次记录契约（Batch Record Contract） incl. the A-26 cross-batch read/write split and the A-27 bounded `superseded_by` append boundary; § 分层封闭 extended with the batch-family conditional layer (`batch_id` / `batch_disposition` / `recommendation_grounding`, together-or-none) |
| T029 | Reply parsing/validation + settlement computation: restricted reply grammar, identity binding, full-label membership incl. the `other`/path rule, duplicate/unknown-identity refusals, zero writes on refusal, authorization gate, park, explicit settlement of ineligible items with D-9 completeness gate, eligibility matrix |
| T030 | `record` write path: re-scan drift precheck over identity set + per-item fingerprints (refusal with the diff, zero writes, no minted id), deterministic batch-id derivation with the create-only precheck, batch head/item rows/decision-record blocks written through `memory-utils.py --action record --scope knowledge`, the three batch-family fields; `validate-decisions.py` admits the three fields and judges the family rule (together-or-none + value domains) under M-01 |

Task states closed in `tasks.md`: T016–T030 all `[X]` (15 rows); `validate-tasks.py` → 0 errors / 0 warnings (rc 0).

## Gate readings (all executed this package)

| Check | Command | Result |
|-------|---------|--------|
| US1 phase green | `run-tests.sh tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py -q` | **25 passed** (rc 0) |
| US2 red-first | same unit module + contract module with `--names-out` | **12 failed / 21 passed** and **1 failed / 4 passed** before T029/T030; behaviour assertions only |
| Final targeted regression | `run-tests.sh tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py tests/contract/test_decision_governance_contracts.py tests/contract/test_decision_governance_guards.py tests/unit/test_validate_decisions.py -q` | **77 passed** (rc 0) |
| Validator family closure (manual probe) | `validate-decisions.py --action records --carrier <valid batch record> --register <fixture>` | rc 0 `PASS: 0 violation(s)`; removing one family field → rc 1 naming the missing field |
| Mirrors | `sync-mirrors.py --write` then `--check`; `cmp` on the three pairs | rc 0; byte-identical |
| Per-tool copies | `regen-command-copies.py --check` | `OK: all per-tool command copies match the source templates.` rc 0 |
| Gate neutrality | `.specify/scripts/python/scan-confirmation-gates.py --summary` | 30 blocking (22/7/1) / 0 violations — unchanged vs baseline |
| Instruction section | section extraction on `.specify/instructions.md` | `## Decision Items` = **1,276 B**, unchanged |
| Tasks validator | `validate-tasks.py .specify/specs/112-decision-batch-panel/tasks.md` | 0 errors / 0 warnings, rc 0 |
| Workspace guard | `workspace-guard.py --snapshot …/workspace-implement-p2.json`; `--check` at wrap-up | snapshot recorded (branch `112-decision-batch-panel`); check reading in `test-evidence/workspace-implement-p2-check.txt` |

## Red/green pointers

- Red-first evidence: `notes/red-first-evidence.md` (S2 green at T023; S3 red at T024/T025 → post-implementation green, formal clause green at T032).
- Failing-name lists: `notes/red-first-names.txt` (P1), `notes/red-first-names-us2.txt`, `notes/red-first-names-us2-contract.txt`.
- US1 green evidence: `notes/us1-green.txt` (mirror pairs, two-scan equality, grounding/prior-conflict payloads, bookkeeping identity, the real-tree 17-row reading).
- Real-tree reading: `scan --workspace-root .` → 17 register candidates, 0 authored blocks, all `incomplete` (`authority-unresolved`, `class-missing`) — the A-16 first-batch shape, zero writes.

## Boundaries held

- `.specify/register.md`, `.specify/instructions.md`, `.specify/.gitignore`, `.specify/glossary.md`, `.specify/features.md` and the driver state spine untouched; no edits outside the feature's files; no push; main tree untouched.
- No new runtime store root; the batch record carrier is the existing `.specify/knowledge/` store; no batch record was written into this worktree's runtime store.
- **A-26 preserved**: write isolation + a declared read-only exit (already-resolved join, grounding, prior conflict); no dependence on another batch's in-flight state.
- **A-27 preserved**: the owner page names the single sanctioned post-write append (`superseded_by`, single field, every pre-existing byte unchanged) and ties its full form to the redecision face; no other write-back is implemented or promised.
- Zero network access; zero feedback-store transmission; record refuses unattended/undeclared authorization.

## Concurrency

`requested=1`; `effective=1`; `effective_reason=write-conflict` — owner page, engine, validator, fixtures and the mirror projection are single-writer surfaces; the package is one serial unit.

## Wrap-up accounting

| Step | Command | Reading |
|------|---------|---------|
| Run Determination | `run-determination.py --action determine --unit-id /speckit.implement --unit-type command --run-id r20261127T081500Z-112a --complexity complex` | `duplicate: … was already determined` (one record per run; P1's determination is the run record) — `implement-p2-run-determination.txt` |
| Exec Quant | `exec-quant.py --action collect --unit-id /speckit.implement --unit-type command --run-id r20261127T081500Z-112a` | `duplicate record …; no second row written` — `implement-p2-exec-quant.txt` |
| Feedback Record | `feedback-utils.py --action record … --review … --points …` | `duplicate: true` (one entry per unit+run; P1's entry retained, not overwritten) — `implement-p2-feedback-record.txt` |
| Workspace guard | snapshot before the artifact commit; `--check` after | snapshot recorded; post-commit reading in `workspace-implement-p2-check.txt` |

## Disclosures (corrections applied in passing)

1. **Prior-batch join counts settled identities only**: the read-time join derives subjects from the prior batch record's `### D-NNN` headings, not its item-row table — a parked row therefore re-presents (C-405). Corrected while authoring the cross-batch test; the resolution-join fixture still resolves via its D-002 heading.
2. **Batch-id derivation vs adoption**: the id string is derived before the drift precheck so the C-502 create-only refusal is directly observable; it is adopted (minted) only after every record precondition passes, so refused attempts leave no id, registration or record.
3. **Frontmatter serialization**: memory-utils quotes scalars and omits an empty `session_id`; the write passes `--session-id <batch_id>` and the layout test parses frontmatter, so the assertion pins field presence rather than the engine's quoting style.
4. **Record payload paths are workspace-relative** (quickstart form); three initial US2 test failures were test-side resolution of `record_path`, repaired in the tests rather than by changing the payload contract.
5. **US2 mirror projection executed in-package** so the tree stays coherent; T031's formal verification row (cmp set + validator-over-fixture run) remains open for P3, as does every US2 clause green point (T032).
6. **`test_skill_does_not_recompute`** stays green from P1 (its subject predates this package).

## Re-anchoring

Rules reloaded at each core step (unattended, no approval request, U4 → next, spine before action, workspace guard, fast-fail, budget/report discipline); territory held to this feature's artifacts; verdict `on-track`.

## Anomalies

- `ANOMALY:` none. No decision-class anomaly was met: the six disclosures above are in-passing corrections with recorded reasons; the wrap-up duplicates are the engines' documented one-record-per-run semantics, not failures.