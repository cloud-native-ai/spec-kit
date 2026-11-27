# Requirements Stage Evidence — 2026-11-27

Line `decision-batch-panel`; run `r20261127T081500Z-112a`; stage `requirements`; baseline `c3489e52c`; branch `112-decision-batch-panel` (worktree).

## Source set read

- `.specify/todo/20261127-decision-batch-panel.md` (main tree, read-only; the parked requirement and its intent).
- `.specify/shared/definitions/decision-definitions.md` (Feature 107 owner: vocabulary, classes and templates, option-set contract, record closure/grammar, producer inventory, transmission, M/B boundary, legacy rules).
- `.specify/shared/guidelines/decision-tension.md` (six-field `T-NNN` record shape and heavy-decision thresholds).
- `.specify/shared/guidelines/confirmation-gates.md` (two-level gate taxonomy, destructive list, gate observation signals).
- `.specify/shared/guidelines/closed-set-claims.md` (referenced for the completeness claim shape).
- `.specify/shared/guidelines/user-facing-comprehension.md` (reader baseline, jargon whitelist).
- `.specify/register.md` (ID register; open OI-/D-family rows; writer rule).
- `.specify/specs/107-decision-governance/requirements.md` (closed precedent; read in two bounded passes).
- `.specify/specs/109-prompt-adherence/requirements.md` + `.specify/features/109-prompt-adherence.md` (most recent merged conventions).
- `.specify/constitution.md` (v1.20.0; Principles IX, X, XIV, XVIII, XIX, XX, XXI and Feature Governance).
- `.specify/instructions.md` § Decision Items (1,276 B against the declared 1,500 B cap).
- `shared/definitions/framework-map.md` (decision-governance owner row; store rows).
- `.specify/shared/declarations/facts/runtime-store-layout.yaml` (14 declared stores; knowledge tier).
- `skills/internal/create-requirements/SKILL.md`, `.specify/templates/requirements-template.md`, `.specify/shared/guidelines/requirements-guidelines.md`.
- `skills/external/sdd-loop-driver/references/stage-prompts.md` (U4 gates, wrap-up accounting) and the two driver gates' source.
- `tests/contract/test_migration_distribution.py` (frozen command/skill name baselines), `tests/contract/test_decision_governance_contracts.py` (P-01…P-12 inventory pin), `scripts/python/memory-utils.py` (knowledge-tier record path), `scripts/python/validate-decisions.py` (carrier-based record judging).

## Scaffold (A-19, disclosed)

`create-new-requirements.sh` derives the next number from spec dirs, `.archive/`, and local/remote branch names in `<NNN>-<slug>` form; the current local branch `112-decision-batch-panel` is itself counted, so the script would derive **113** and create/switch a second branch. Per the 107/109/110 precedent: manual scaffold from `.specify/templates/requirements-template.md` into `.specify/specs/112-decision-batch-panel/requirements.md`, staying on branch 112; the script's template-copy step replicated, only its numbering/branch step skipped. Recorded as A-19 in the spec.

## Probes — baselines and surfaces (2026-11-27, this worktree)

1. **Open pending rows**: register OI-/D-family rows whose status begins with `open` after stripping markdown emphasis — OI-3, OI-4, OI-7, OI-9, OI-069b-01, OI-073-01, OI-082-01, D-2 (092). `OI-087-01` begins with `**resolved**` after emphasis stripping and is excluded; `OI-1…OI-9` carries status `见下逐项` and is excluded.
2. **Authored pending blocks**: `grep -rn '### PENDING' .specify/specs .specify/goals .specify/anchoring .specify/teams` → **0 files**. The first honest batch therefore presents the open rows as `incomplete` (A-16).
3. **Producer inventory**: `.specify/shared/definitions/decision-definitions.md` inventory ends at P-12; `tests/contract/test_decision_governance_contracts.py:366` pins `P-01…P-12`; `tests/contract/test_decision_governance_guards.py:804` pins the exempt set `{P-11, P-12}`. Adding P-13 requires the same-change guard update (FR-003, FR-042).
4. **Entry-surface absence**: no `decide` command in `templates/commands/` (32 files) and no `decide-batch` skill; frozen baselines in `tests/contract/test_migration_distribution.py` (`COMMAND_BASELINE`, `SKILL_BASELINE`).
5. **Instruction budget**: `## Decision Items` section measured 1,276 B in both `templates/instructions-template.md` and `.specify/instructions.md`; declared cap 1,500 B → ~224 B headroom; A-15 decides not to spend it on a new sentence.
6. **Batch-record carrier**: `runtime-store-layout.yaml` declares the `knowledge` store (memory-tier, one Markdown entry per record, owner `memory-utils.py`); the memory reference calls `knowledge` the durable tier for "lasting decisions"; the feedback store's threshold counter (`feedback-utils.py` `count_since_submission`) is the reason feedback is not used (A-11).
7. **Carrier names**: `shared/definitions/decision-definitions.md` exists in the framework source and as the `.specify/` mirror; `scripts/python/validate-decisions.py` accepts arbitrary carrier files (`--carrier`, repeatable), so a knowledge entry can be judged as a decision-record carrier without a validator change beyond the batch-family field set.
8. **Mirror and copies**: `sync-mirrors.py` `MIRROR_PAIRS` = `templates → .specify/templates` (excluding `commands`), `skills/external → .specify/skills`, `skills/internal → .specify/skills/internal`, `agents → .specify/agents/templates`, `scripts → .specify/scripts`, `shared → .specify/shared`; per-assistant command copies are regenerated separately; `specify init` copies `scripts/`, `templates/`, `shared/` trees.
9. **No-collision check**: `grep -rn 'decision-batch\|speckit.decide\|decide-batch'` across the repo → 0 hits; no existing `### PENDING` block; no existing `decide` command.

## Deterministic gates (verbatim outputs in `test-evidence/`)

- `validate-requirements.py .specify/specs/112-decision-batch-panel/requirements.md` → exit 0, `status: ok`, `0 error(s), 0 warning(s)`, **408 lines, 55 definition rows, 15 shared strings**; all six labels pass → `requirements-validator.txt`. First run reported 4 `ref-resolvable` errors (the `Consumed by` cells for STR-001/STR-013/STR-014/STR-015 named FR-042, which re-typed the literals instead of citing the ids); FR-042 was corrected to cite them and the rerun is the captured green run. One typo repair and one wording repair landed in the same pass.
- `pre-analyze-check.py --spec-dir .specify/specs/112-decision-batch-panel --stage requirements --repo .` → `decision=pass errors=0 advisories=8 waived=0`, summary `fr=45 sc=10` → `pre-analyze-requirements.txt` + `.json`. All 8 advisories are `missing-path` on not-yet-created deliverables — four paths, each counted once in `requirements.md` and once in `checklists/requirements.md`: `templates/commands/decide.md`, `skills/internal/decide-batch/SKILL.md`, `docs/reference/commands/decide.md`, `tests/fixtures/decision-batch/`. An earlier capture (7 advisories) was taken before the feature detail landed; the captured reading is the final pre-commit state, and the postcommit rerun re-checks the committed state.
- `decomposition-check.py --mode plan --requirements .specify/specs/112-decision-batch-panel/requirements.md` → `decision=proceed`, `fr_count=45`, `fr_ceiling=120` → `decomposition-requirements.txt` + `.json`.

## Workspace guard

- Snapshot recorded before authoring the spec (after creating the spec directory, so the listing already contains it): `test-evidence/workspace-requirements.json`; immediate self-check `clean` (rc 0).
- Pre-commit check: `test-evidence/workspace-requirements-check.txt` → `clean` (rc 0). Post-commit check is captured in the stage records commit.

## Concurrency

- `requested=1`; `effective=not_evaluated`; `effective_reason=single-unit` — one bounded assignment, no independent units to parallelize.

## Wrap-up accounting

- Run determination, exec-quant and feedback record for the requirements stage (unit `/speckit.requirements`, `--feature 112-decision-batch-panel`, `--feature-id 112`) — records land under `.specify/session/`, `.specify/exec-quant/` and `.specify/feedback/` and are carried by the stage records commit together with the close-out receipt and the postcommit gate readings.

## Disclosures

1. **No register/spine edits**: `.specify/register.md` and the state spine were not edited by this stage (A-2, A-20); the feature binding landed only in `.specify/features.md` and `.specify/features/112-decision-batch-panel.md`.
2. **Feature detail created after the pre-analyze capture**: the captured gate run still lists `.specify/features/112-decision-batch-panel.md` as a missing path; the postcommit rerun records the final reading (a smaller advisory set).
3. **No main-tree writes**: the parked todo was read from the main tree read-only; every produced artifact lives in the worktree.
4. **No push**: none attempted or authorized.