# Mutation drill — 107-decision-governance (T045 / SC-007)

Captured: 2026-11-26 (UTC), worktree decision-governance. Every sample below was run through
the single test entry in `tests/contract/test_decision_governance_guards.py::test_every_guard_has_reverse_sample`
and re-executed here directly against `scripts/python/validate-decisions.py` so the red line,
the exit status and the rule id are visible per rule. Each mutation is the object the rule
judges, made wrong; the guard MUST turn red (C-403).

## Per-guard drill (one reverse sample per machine rule)

| Rule | Judge action | Reverse sample | Exit | Verdict line |
|------|--------------|----------------|------|--------------|
| M-01 | `--action records` | `tests/fixtures/decision-governance/m01/red-missing-actor.md` | 1 | M-01 tests/fixtures/decision-governance/m01/red-missing-actor.md:3: missing base-layer field(s): actor |
| M-02 | `--action records` | `tests/fixtures/decision-governance/m02/red-empty-locator.md` | 1 | M-02 tests/fixtures/decision-governance/m02/red-empty-locator.md:25: same_name_conflict: true requires a machine-parseable resource_locator carrying at least the business resource  |
| M-03 | `--action records` | `tests/fixtures/decision-governance/m03/red-empty-set.md` | 1 | M-03 tests/fixtures/decision-governance/m03/red-empty-set.md:7: empty option set; a decision item MUST carry at least one option (zero viable options is not a decision item) |
| M-04 | `--action records` | `tests/fixtures/decision-governance/m04/red-form.md` | 1 | M-04 tests/fixtures/decision-governance/m04/red-form.md:3: heading id 'D-001-a' does not match the D-NNN form (exactly three digits) |
| M-05 | `--action chain` | `tests/fixtures/decision-governance/m05/red-no-id.md` | 1 | M-05 tests/fixtures/decision-governance/m05/red-no-id.md:17: the implementation_receipt carries no decision_id |
| M-06 | `--action payload` | `tests/fixtures/decision-governance/m06/red-no-block.md` | 1 | M-06 tests/fixtures/decision-governance/m06/red-no-block.md:1: a decision-backed dispatch MUST carry a decision_block with decision_id, decision_class, chosen_option, implementatio |
| M-07 | `--action chain` | `tests/fixtures/decision-governance/m07/red-missing-dispatch.md` | 1 | M-07 tests/fixtures/decision-governance/m07/red-missing-dispatch.md:5: the dispatch attempt segment is missing (decision record → dispatch attempt → receipt) |
| M-08 | `--action records` | `tests/fixtures/decision-governance/m08/red-variant.md` | 1 | M-08 tests/fixtures/decision-governance/m08/red-variant.md:3: decision subject uses the registered glossary variant 'spec-kit'; use the full name 'Spec Kit' |
| M-09 | `--action records` | `tests/fixtures/decision-governance/m09/red-broken.md` | 1 | M-09 tests/fixtures/decision-governance/m09/red-broken.md:20: evidence pointer 'tests/fixtures/decision-governance/m09/does-not-exist.md' does not resolve: the referenced carrier p |

Every sample exits 1 (a documented check failed) and carries its own rule id in the verdict line.

## Table–guard parity (C-407)

- Owner page § 强制边界 M table rows: M-01…M-09 (measured by `test_table_guard_parity`).
- Test-side roster `GUARD_ROSTER` keys: M-01…M-09; every M row names exactly one `--action` and it matches the roster's action.
- Owner page B table rows: B-01…B-07; the test-side behavior roster matches row-for-row.

## B-surface list (C-402; behavior-borne, never machine-claimed)

| Rule | Named review surface |
|------|----------------------|
| B-01 名称完整性 | `/speckit.review` 产物段 + 人工决策评审 |
| B-02 定位充分性 | `/speckit.review` 产物段 + 人工决策评审 |
| B-03 人工可读性/后果真实性 | 人工决策评审 + `/speckit.review` 产物段 |
| B-04 AI 严谨性 | `/speckit.analyze` + `/speckit.review` |
| B-05 理由充分性 | `/speckit.analyze` + `/speckit.review` |
| B-06 类别正确性 | `/speckit.review` 产物段 |
| B-07 保全裁定充分性 | `/speckit.analyze` + `/speckit.review` 产物段 |

The producer-side pointers carrying these surfaces live in
`skills/internal/analyze-artifacts/SKILL.md` (B-04/B-05/B-07) and
`skills/internal/review-feature-quality/SKILL.md` + `skills/internal/review-sdd-process/SKILL.md` (B-01…B-07).
No document or test claims machine coverage for any of them; the guards module quotes no B id.

## Inventory closure (C-406)

The documented code-face scan (grep for the owner-page path over `templates/ skills/ agents/ scripts/ src/`)
observes ten non-exempt producers and the action reports `observed == declared ± exempt`
(declared 12, exempt P-11/P-12). Two mutations red the guard: an extra face
(`skills/internal/some-new-producer/SKILL.md`) is reported unregistered; a declared producer
whose owner face disappears is reported missing.
