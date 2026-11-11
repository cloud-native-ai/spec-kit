# Review-Repair r1 — Dispositions

**Feature**: 100-seal-slice-archive | **Date**: 2026-11-11 | **Source**: `.specify/specs/100-seal-slice-archive/review.md` § 5 P1 items
**Scope**: REC-100-1 (F2) and REC-100-4 (F1) only. P2 findings (F3–F9, REC-100-2/3/5/6/7/8) are untouched.

## REC-100-1 (F2) — mixed-carrier dated criterion is now stated and enforced per carrier class

**Disposition**: fixed.

- The clause-level criterion was split by carrier class in `contracts/reference-classification.contract.md`:
  - **C-306(c)**: pure dated carrier (no `live-rewrite` row) → whole-file sha256 equality; mixed carrier (both row kinds, e.g. `features/<ID>.md`) → its dated H2 sections (C-304 boundaries) stay byte-identical while live sections are rewritten per ledger.
  - **C-308**: same two-case rule, with the failure consequence stated once — either a pure dated file hash change or a mixed carrier dated-section byte change ends `archive-apply` at `2` (`write-failed`) and restores the original bytes.
  - **C-302(ii)** (same page): the dated disposition's parenthetical now points at C-306(c) instead of restating "file sha256 equal".
  - `requirements.md` Q2(c): the ratified ruling now points at the carrier-class test owned by C-306(c) (no rule duplication; owner unchanged).
- Engine (`scripts/python/seal-utils.py`): the old `- set(live_rows)` exemption is replaced by a section-level guard. `mixed_dated_sections()` concatenates a mixed carrier's dated H2 blocks at byte level; `_archive_apply_batch` snapshots that region before the batch and re-compares it after the live rewrites, raising `OSError` (→ `write-failed`, exit `2`, byte restore) on any drift. Pure dated carriers keep the whole-file sha256 check.
- Mirror: `.specify/scripts/python/seal-utils.py` regenerated with `sync-mirrors.py --write` (byte-identical).

**Red-first evidence**: `test-evidence/review-repair-r1-red-first.txt` — against the pre-repair engine the mutation test observed `assert 0 == 2` (a dated-section mutation was accepted) and the allow test failed on the missing section helper; after the repair both pass.

**Tests added** (`tests/contract/test_seal_archive_apply.py`):
- `test_a_mixed_carrier_changes_only_in_its_live_sections` — the fixture mixed carrier carries both row kinds (2 `live-rewrite` + 2 `dated-preserved`); apply succeeds, the file hash changes, dated-section bytes do not, every recorded row lands at its line. **Permitted case.**
- `test_a_mixed_carrier_dated_section_change_is_rejected_and_restored` — a write-path sabotage mutates one dated line; apply ends `2` with `write-failed` and the tree is restored byte for byte. **Rejected case.**

**Real-tree reading**: `archive-plan` on `.specify/specs/074-goal-team-sdd-unification` → `already-archived`, `live_rewrite=249`, `dated_preserved=825`, `unclassified=0`, `unresolved=0/0`; the mixed carrier `.specify/features/074-goal-team-sdd-unification.md` carries exactly 10 `live-rewrite` + 2 `dated-preserved` rows — the F2 case, now covered by an enforced criterion.

## REC-100-4 (F1) — analyze reports cross-clause contradictions

**Disposition**: fixed (rule only; no new engine, as scoped).

- `skills/internal/analyze-artifacts/SKILL.md` § 5 (detection passes): added one rule — two clauses imposing mutually exclusive criteria on the same object (whole-file hash frozen vs. a section of the same file rewritten; or one predicate classified into different closed sets) MUST be raised as one `inconsistency` finding naming both clauses and the shared object; neither may be accepted as settled while its opposite stands.
- Mirror: `.specify/skills/internal/analyze-artifacts/SKILL.md` regenerated with `sync-mirrors.py --write` (byte-identical; the pair read `ok` in `--check`).

## Verification readings (2026-11-11)

| Check | Command (verbatim) | Result |
|---|---|---|
| Affected suites | `bash scripts/bash/run-tests.sh tests/contract/test_seal_archive_plan.py tests/contract/test_seal_archive_manifest.py tests/contract/test_seal_archive_apply.py tests/contract/test_seal_archive_gate.py tests/unit/test_seal_archive_classify.py tests/integration/test_seal_archive_idempotency.py tests/integration/test_seal_archive_round.py tests/integration/test_seal_archive_rollback.py tests/integration/test_seal_074_round.py tests/contract/test_clause_coverage.py tests/contract/test_run_skills_wiring.py tests/contract/test_skill_layer_visibility_guards.py -q` | 146 passed, 2 failed, exit 1 — the 2 are the pre-existing baseline reds `test_c5_gate_budget_is_unchanged_by_the_owner_document` and `test_live_plan_identifies_both_slices_from_the_split_record`, both listed in `test-evidence/final-failed.txt` (lines 5 and 158) and red in the pre-change baseline run as well (132 passed / same 2). Full output: `test-evidence/review-repair-r1-suite.txt` |
| New tests | `... -k "mixed_carrier"` | red: 2 failed; green: 2 passed (see red-first file) |
| Mirror parity | `python3 scripts/python/sync-mirrors.py --check --only scripts/python/seal-utils.py --only skills/internal/analyze-artifacts` | exit 0; both pairs byte-identical (3 files + 1 file) |
| Clause coverage | `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/100-seal-slice-archive` | claimed 40, FR 28/28, uncovered beyond baseline 0 — unchanged; the 108 clause-unparsable warning is baseline-internal |
| 074 replay | `python3 scripts/python/seal-utils.py --action archive-plan --spec-dir .specify/specs/074-goal-team-sdd-unification --repo . --json` | exit 0, `already-archived`, `unclassified=0`, unresolved `0/0` |

## Untouched / residual

- P2 findings and their recommendations remain open; this round is P1-only per the dispatch.
- `tasks.md` T025 and `plan.md` § discriminating evidence keep their historical wording; neither states a claim about mixed carriers, and closed task rows are not rewritten by a repair.
- `.specify/templates/gitignore-specify-template` carries a pre-existing working-tree modification disclosed by the review; it is not part of this repair and is not committed.
- `templates/commands/analyze.md` already says "seven detection passes" while the skill enumerates eight + I — pre-existing drift, outside this repair's scope.
