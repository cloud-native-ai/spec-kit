# Implementation evidence — WP-03 (T035–T047)

Feature 101 `anchor-goal-realignment`, unattended line, run `r20261112T064607Z-b101`.
Executor: SDD Implement Executor (leaf; no dispatch, no state-spine writes).

## Tasks

| Row | What landed | Reading |
|---|---|---|
| T035–T038 | Six shared definitions already carried the Anchor/Goal split from the earlier checkpoints; this package added the `shared/patterns/interview-pattern.md` alignment and re-verified the definitions' live reference sets. | no red |
| T039 | Flow-class ledger rows/units: 91 units / 91 rows / 0 gaps (`flow-class-check.py --action check --format json` → `units: 91, coverage.gaps: 0`). Test pins updated in T047. | green after pin update |
| T040 | `probe-utils.py --action compile-embeds --check` → `85 units, zero drift`. **Correction disclosed**: the registry fingerprint had moved to `2845f5641171` after WP-02's registry edit, so a first check reported drift in 85/85 units and `templates/commands/anchor.md` carried only the reserved empty `## Wrap-up`; recompiling and following the chain (regen copies → sync mirrors) closed it. | green |
| T041 | `sdd-project-setup` and `sdd-house-keeping` skill bodies + reference pages: `anchor` layer in the soft-collab line, stage list, logical matrix, bootstrap-gap set; history `.specify/goal/` path explicitly not a delivery surface. | tests green (T047 pin update) |
| T042 | `docs/tutorials/{quickstart,installation}.md`, `docs/reference/commands/{team,seal}.md`, `.specify/features.md` rows 027/041/094: Anchor terminology, seven-mode entry, `anchor_slug`; C7 scan of the features index returns zero. | no red |
| T043 | Four team-domain trees (`create-team`, `improve-team`, `run-team`, `summarize-project`): Anchor terms, `anchor_slug`, delivery dir `.specify/anchoring/<anchor-slug>/summary/`, Anchor-only modes point at `/speckit.anchor`; `verify-territory-disjoint.py` now prefers `anchor_slug` (legacy `goal_slug` accepted). | tests green |
| T044 | `shared/patterns/interview-pattern.md` adoption map: `/speckit.anchor create` = partial instance; `/speckit.goal create` = action-level only; `create-team` escalates anchor authoring to `/speckit.anchor`. | no red |
| T045 | `shared/declarations/facts/non-disposable-review-surface.yaml`: `.specify/anchoring` + `.specify/goals` are members (eleven roots), `.specify/goal` retired with its reason in the declaration `note`; owner page `shared/definitions/non-disposable-definitions.md` reconciled (eleven-root block + count rows). `.specify/goals` is currently absent → declared-but-absent, the legal closed-set reading until WP-04 creates it. | declaration parses; harness triple-check rc 0 |
| T046 | `sync-mirrors.py --write` then `--check`: `templates/`, `skills/external`, `skills/internal`, `agents/templates`, `scripts/`, `shared/` all byte-identical (0 DIFF). | green |
| T047 | Six existing test modules updated for this package's renames; red-first diff recorded in `notes/red-first-evidence.md` § WP-03. | see final reading |

## Disclosed corrections (fast-fail)

1. **Compile/registry ordering (T040)** — recompiled 85 units (fingerprint `4682b9e38032` → `2845f5641171`), regenerated per-tool command copies, re-synced mirrors. Trigger: the registry changed after the prior compile, so the compiled faces were stale; the canonical chain is compile → regen → sync.
2. **Handoff contract schema key (T043)** — my first edit renamed the handoff frontmatter key to `anchor_slug`; four pre-existing contract tests went red because the 094 dated contract owns that artifact schema (`goal_slug`) and the engine reads it. Restored the 094 key with an explicit note that it names the bound Anchor but is not the team definition's binding field (`anchor_slug`). No engine edit.
3. **Non-disposable owner-page reconciliation (T045)** — the owner page's literal root block and count rows were updated with the declaration (in-passing correction; disclosed).
4. **Criterion-vocabulary exemption (T047)** — widened the historical-record exemption to the renamed owner pair so the surviving baseline red reflects only its pre-existing `decomposition-model.md` hits; the baseline id was already red before this package and stays red.

## Final targeted readings

- 20-module batch: **12 failed, 591 passed (47.65 s)**. Every failed id is present in `test-evidence/suite-baseline-entry.txt`:
  - `test_non_disposable_check.py` × 4 (baseline lines 80–83)
  - `test_shared_reference_rewrite.py` × 2 (baseline lines 96–97)
  - `tests/integration/test_goal_reference.py` × 5 (baseline lines 137–141)
  - `test_criterion_vocabulary_scan.py` × 1 (baseline line 31)
- No new id outside the E2 baseline; the three carried WP-03 reds (T039 flow-class pins, T040 compile census, plus the T039/T040 probe chain) are closed.
- Guards: `sync-mirrors.py --check` rc 0; `probe-utils.py --action compile-embeds --check` rc 0; `regen-command-copies.py --check` rc 0.

## Wrap-up engines (identity `/speckit.implement`, run `r20261112T064607Z-b101`)

- `run-determination.py --action determine` rc 0 → duplicate (pair already recorded).
- `exec-quant.py --action collect` rc 0 → duplicate; record store `.specify/memory/exec-quant/records`.
- `feedback-utils.py --action record` rc 0 → duplicate; store `.specify/memory/feedback/` (`count_since_submission: 482`, threshold 10, `should_prompt: true` — non-blocking notice only, nothing transmitted).

## Uncommitted / out of scope

`smoke-081.txt` and `.specify/.specify/` were dirty before this run and are left untouched and uncommitted.
