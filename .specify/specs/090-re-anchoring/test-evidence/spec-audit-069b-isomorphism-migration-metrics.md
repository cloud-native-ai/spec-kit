# Spec audit — 069b-isomorphism-migration-metrics (batch 10)

- **Date**: 2026-11-10
- **Subject**: `.specify/archive/specs/069b-isomorphism-migration-metrics/` (22 artifact files; archived by the 2026-11-09 consolidation, ledger row "merge → 069")
- **Tree audited**: main tree `/storage/project/cloud-native-ai/spec-kit`, current working tree as-is (HEAD `564a5f5a6`). The anchor-layout rename landed in the working tree **during** this audit (`.specify/memory/{features.md,features/,register.md,glossary.md,constitution.md}` → `.specify/`); the final counts and findings below reflect the post-rename tree.
- **Mode**: read-only. No spec or source file was modified; this file is the only write. No subagents, no commits.
- **Classification rule**: *alive* = the literal target exists now; *archived-elsewhere* = absent live but the exact subpath exists under another archive of the same object (066, 069a); *dead* = no target. Per the batch instruction, a stale pre-archive literal `.specify/specs/069b-…/...` counts as **dead** even though its content survives under `.specify/archive/specs/069b-…/`; the resolution column names the archive copy so the content stays reachable. Wildcard/placeholder tokens are excluded and listed separately.

## 1. Reference counts

Unique concrete path targets, deduplicated after normalizing a trailing `/`. Occurrences are quoted where one target is cited many times.

| Family | Alive | Archived-elsewhere | Dead | Total |
|---|---:|---:|---:|---:|
| `.specify/` | 30 | 2 | 16 | 48 |
| `shared/` | 11 | 0 | 1 | 12 |
| `scripts/` | 11 | 0 | 0 | 11 |
| `skills/` | 8 | 0 | 1 | 9 |
| `templates/` | 13 | 0 | 0 | 13 |
| `tests/` | 34 | 0 | 3 | 37 |
| `src/` | 3 | 0 | 1 | 4 |
| `docs/` | 6 | 0 | 0 | 6 |
| **Total** | **116** | **2** | **22** | **140** |

- The 11 stale pre-archive literals occupy **48 citation lines across 12 artifacts**; the 5 anchor-rename casualties add **19 citation lines**. Both groups are counted once per unique target (see §2.1).
- Excluded wildcard/placeholder tokens: `.specify/specs/*/contracts/*`, `.specify/specs/**`, `.specify/**`, `.specify/scripts/python/<engine>.py`, `contracts/*.md`, `skills/<name>/SKILL.md`, `skills/**`, `skills/**/*.md`, `skills/internal/*/`, `skills/external/*/`, `templates/commands/*.md`, `templates/commands/**`, `templates/commands/**/*.md`, `shared/**/*.md`, `tests/**`, `docs/**`, `docs/**/*.md`, `docs/concepts/*`.
- Excluded non-repo / environment paths: `xuanji-agent/tests/test_adapter_contract.py`, `<snap>/src/...`, `<snap>/src/data`, `/Users/…/profiles/.venv/…`, `/Users/…/kangaroo-xuanji/…`, and installed-package probes `specify_cli/shared/{definitions,workflow}/` (pyproject maps `shared` → `specify_cli/shared` at build time; no such source dir exists by design).

## 2. Broken list

### 2.1 Dead targets inside the archived artifacts

| # | Target | Cited at (lines) | Now resolves to |
|---|---|---|---|
| 1 | `.specify/specs/069b-isomorphism-migration-metrics/requirements.md` | contracts/measurement-instruments.md:9; notes/expression-baseline.md:50; notes/parent-fr-mapping.md:5; plan.md:5,292,307; quickstart.md:154; review.md:30 (also as an author-host absolute path); tasks.md:33,46,105,256; verification.md:340,341 | DEAD literal → `.specify/archive/specs/069b-isomorphism-migration-metrics/requirements.md` (exists) |
| 2 | `.../tasks.md` | tasks.md:31,33,38,256; verification.md:269,270,355,356 | DEAD literal → archive `tasks.md` (exists) |
| 3 | `.../verification.md` | review.md:252,257; tasks.md:18,39,254 | DEAD literal → archive `verification.md` (exists) |
| 4 | `.../coverage-baseline.txt` | notes/pre-change-measurements.md:313; tasks.md:169,289; verification.md:301 | DEAD literal → archive `coverage-baseline.txt` (exists) |
| 5 | `.../checklists/isomorphism-migration-metrics.md` | verification.md:408,410 | DEAD literal → archive `checklists/isomorphism-migration-metrics.md` (exists) |
| 6 | `.../contracts/` (directory) | tasks.md:104 | DEAD literal → archive `contracts/` (4 files exist) |
| 7 | `.../notes/expression-baseline.md` | contracts/measurement-instruments.md:3,81; tasks.md:240 | DEAD literal → archive `notes/expression-baseline.md` (exists) |
| 8 | `.../notes/pre-change-measurements.md` | tasks.md:168 | DEAD literal → archive `notes/pre-change-measurements.md` (exists) |
| 9 | `.../notes/red-first-evidence.md` | tasks.md:12 | DEAD literal → archive `notes/red-first-evidence.md` (exists) |
| 10 | `.../notes/test-baseline-contract.txt` | tasks.md:113,170; verification.md:157 | DEAD literal → archive `notes/test-baseline-contract.txt` (exists) |
| 11 | `.specify/specs/069b-isomorphism-migration-metrics` (directory form) | plan.md:94,303; quickstart.md:114; tasks.md:7,68; review.md:54 | DEAD literal → archive directory (exists) |

All 11 are archive-relocation staleness, not content loss: every target was verified under `.specify/archive/specs/069b-isomorphism-migration-metrics/`. Relative refs inside the archive (`contracts/isomorphism-map.md`, `notes/…`) still resolve from the archived spec directory.

| # | Target | Cited at (lines) | Now resolves to |
|---|---|---|---|
| 12 | `shared/definitions/isomorphism-map.md` | checklists:36,75,142; notes/pre-change-measurements.md:222,226; plan.md:313; research.md:23; tasks.md:70,109,187,323; verification.md:286 | **Intentionally absent** — the spec's own "rejected alternative, MUST NOT be created". Still absent → spec-faithful, not a defect. |
| 13 | `skills/external/humanize/SKILL.md` | notes/quickstart-run.md:223 | Renamed: `skills/external/humanize-conclusion/SKILL.md` (calls `--action lookup` at :109). Stale path; claim ("2 consumers") still true. |
| 14 | `tests/test_adapter_contract.py` | checklists:128; notes/migration-samples.md:55; verification.md:287 | No in-repo target. Self-disclosed at verification.md:287 as a **client-snapshot** path (`xuanji-agent/tests/test_adapter_contract.py`), not a repo path → scope false-positive. |
| 15 | `tests/unit/test_qoder_support_matrix.py` | verification.md:119; notes/pre-change-measurements.md:66; notes/quickstart-run.md:401 | Deleted later in `cabc9f1e3` ("delete 47 files…"). Captured diagnostic text only, not a 069b dependency. |
| 16 | `tests/integration/test_qoder_refresh.py` | verification.md:120; notes/pre-change-measurements.md:71; notes/quickstart-run.md:402 | Same deletion (`cabc9f1e3`). Captured diagnostic text only. |
| 17 | `src/xuanji_agent/__init__.py` | notes/migration-samples.md (snapshot import probe) | Client snapshot path (`<snap>/src/xuanji_agent/__init__.py`), not a repo path. |

Anchor-rename casualties (the rename landed in the working tree mid-audit; targets now exist at the new `.specify/` anchors):

| # | Target | Cited at (lines) | Now resolves to |
|---|---|---|---|
| 18 | `.specify/memory/features/069.md` | requirements.md:16; tasks.md:255; verification.md:254,258,398; checklists:6; review.md:166,290,434; feature-ref.md:75 | `.specify/features/069-execution-expression-sdd.md` (exists) |
| 19 | `.specify/memory/features.md` | requirements.md:16; tasks.md:255; verification.md:258; checklists:6; review.md:166,326 | `.specify/features.md` (exists) |
| 20 | `.specify/memory/constitution.md` | plan.md:56 | `.specify/constitution.md` (exists) |
| 21 | `.specify/memory/glossary.md` | requirements.md:196 | `.specify/glossary.md` (exists) |
| 22 | `.specify/memory/register.md` | checklists:122 | `.specify/register.md` (exists) |

**Live side-effect of #15/#16**: `docs/concepts/overview.md:240` still links both deleted tests, so `docs-utils.py --action validate` today reports 2 `broken-link` violations (same two the 069b baseline froze) plus 3 unrelated drifts (`root-entry-oversize` CHANGELOG, 2 `note-frontmatter`).

### 2.2 Live pointers into the pre-archive path — the actionable break

These are current-tree files (not archived artifacts) whose normative pointers assume 069b still lives at `.specify/specs/069b-isomorphism-migration-metrics`. That directory does not exist (`ls` → No such file or directory), while the archive copy does.

| Path:line | What it points to | Now resolves to |
|---|---|---|
| `shared/definitions/flow-class-definitions.md:36,135,141,149,157,159,160,203,208,213,221` | `…/contracts/ledger-reconciler.md` C-5/C-7 (11 refs) | dead literal → `.specify/archive/specs/069b-isomorphism-migration-metrics/contracts/ledger-reconciler.md` |
| `.specify/shared/definitions/flow-class-definitions.md:36,135,141,149,157,159,160,203,208,213,221` | byte-identical mirror | same dead literal |
| `.specify/specs/069-execution-expression-sdd/notes/decomposition-gate.md:45,61,76,83,90,97,100,103` | recorded command lines using `--spec-dir .specify/specs/069b-…` | dead literal (dated evidence blocks; re-running them now fails) |
| `tests/contract/test_measurement_instruments.py:41` | `SPEC_DIR = .specify/specs/069b-…`; `BASELINE`/`REQUIREMENTS` derive from it | dead literal; `_text()` (:89) asserts `BASELINE.is_file()` → cannot pass; `_git_first_commit` (:130) gets an empty history |
| `tests/contract/test_expression_faces.py:47` | `SPEC_DIR` passed as `--spec-dir` at :290 | dead literal; `doc-consistency-check` raises `InputError("--spec-dir is not a directory")` → exit 2, test assertion cannot pass |
| `tests/contract/test_isomorphism_map.py:4`; `test_ledger_reconciliation.py:4`; `test_delegation_classes.py:4`; `test_measurement_instruments.py:4`; `test_migration_distribution.py:4`; `test_expression_faces.py:4`; `tests/unit/test_isomorphism_checker.py:4` | docstring citations of the contract paths | dead literal (documentation only; bodies unaffected) |

Counter-evidence that the repair pattern is known and partially landed: `tests/contract/test_migration_distribution.py:68` was already re-pointed to `.specify/archive/specs/069b-isomorphism-migration-metrics` by commit `37aad2954` ("fix(consolidation): re-point the archived 092/069b contract paths…").

## 3. Ledger target check

- **Row**: `.specify/archive/specs/CONSOLIDATION-LEDGER.md:19` — `069b-isomorphism-migration-metrics | merge | 069 (decomposition-gate slice) | review-G7`.
- **Target feature/spec resolves**: `.specify/specs/069-execution-expression-sdd/` exists with `requirements.md` and `notes/decomposition-gate.md`; the 069b parent FR ranges 018–022 / 033–035 / 036–041 are present there.
- **Registry row resolves**: `.specify/features.md:78` — 069 = `Implemented`, note "slice: 069b Implemented; 069a Implemented" (post-rename path; the pre-rename `.specify/memory/features.md` is gone).
- **Feature detail resolves**: `.specify/features/069-execution-expression-sdd.md:71–77` already cites the archived 069b paths (`archive/specs/069b-…`, 4 refs) — consistent with both moves.
- **`review-G7` resolves**: `.specify/specs/090-re-anchoring/test-evidence/history-distill-batch-4.md:205` — "G7 consolidation review … 12 entries → keep 10, merge 069a/069b into 069" — matches the ledger verdict and target.
- **Verdict on the row**: accurate.
- Ledger hygiene note (unrelated to 069b): the 054 row sits at line 23 **below** the closing prose, outside the table — a structural defect in the ledger, not a 069b accuracy problem.

## 4. Missing guards

**None missing.** All 8 red-first guards the spec names exist:

`tests/contract/test_isomorphism_map.py`, `test_ledger_reconciliation.py`, `test_migration_distribution.py`, `test_measurement_instruments.py`, `test_delegation_classes.py`, `test_expression_faces.py`; `tests/unit/test_isomorphism_checker.py`, `test_reconciler_extensions.py`. Engines/guards also alive: `scripts/python/flow-class-check.py`, `account-clause-coverage.py`, `validate-tasks.py`, `validate-requirements.py` (and `.specify/scripts/python/` mirrors).

Two of those guards carry dead path pins and cannot run green without repair: `test_measurement_instruments.py:41` and `test_expression_faces.py:47` (§2.2). Six more carry stale docstring citations only.

## 5. Three spot-checks (implementation claims)

1. **File/section claim** — `shared/definitions/flow-class-definitions.md` owns the map and boundaries: `## 同构映射（8 阶段 × 3 面）` at :87 (header + separator + exactly 8 data rows, 10 `| ` lines in the section), `## 不可同构边界` at :111 with boundaries a–d each bound to a face id, and the owns list (lines 3–5) names both. **PASS.**
2. **Command/symbol claim** — `scripts/python/flow-class-check.py --help` exposes `--action {check,lookup,isomorphism,delegation,faces}`; `--action isomorphism --format json` returns `{"stages": 8, "gates": 6, "findings": [], "error": null}` with exit 0; the mirrored `.specify/scripts/python/flow-class-check.py` is byte-identical (`cmp`). **PASS.**
3. **Behaviour-surface claim** — `shared/workflow/expression-gates.md:42` table carries the `算子 id` column with stable `G-…` ids (`G-req-clarity` … `G-review-review`, 15 rows), which the carrier's `gate:<算子 id>` references resolve against. The renamed humanize consumer (`skills/external/humanize-conclusion/SKILL.md:109`) still performs the claimed `--action lookup`. **PASS.**

## 6. Anchor-layout rename (landed in the working tree mid-audit)

The rename announced for the `.specify/.tmp/sdd-loop/worktrees/rename-anchors` branch (commit `8b9030371`) is now present in the main working tree: `.specify/memory/{features.md,features/,register.md,glossary.md,constitution.md,tools.md}` are gone and their replacements exist at `.specify/`. Five references in this spec are therefore newly dead and need re-pointing (§2.1 rows 18–22):

| Stale reference | Current home |
|---|---|
| `.specify/memory/features.md` | `.specify/features.md` |
| `.specify/memory/features/069.md` | `.specify/features/069-execution-expression-sdd.md` |
| `.specify/memory/register.md` | `.specify/register.md` |
| `.specify/memory/glossary.md` | `.specify/glossary.md` |
| `.specify/memory/constitution.md` | `.specify/constitution.md` |

`.specify/memory/session/` and `.specify/memory/feedback/` remain under `memory/` and are still alive, as are all `.specify/{scripts,shared,skills,templates,specs}` targets.

## 7. Anomaly

ANOMALY: repair commit `37aad2954` re-pointed only `tests/contract/test_migration_distribution.py`; the same pre-archive pin remains in `shared/definitions/flow-class-definitions.md` + its mirror (11 refs each), `.specify/specs/069-execution-expression-sdd/notes/decomposition-gate.md` (8 recorded-command lines), `tests/contract/test_measurement_instruments.py:41` and `tests/contract/test_expression_faces.py:47` — the already-logged 094 D-I1 drift, left unrepaired here because this audit is read-only.

## Verdict

**BROKEN** — the archived spec's own content is intact and recoverable (all 22 artifacts present; every implementation carrier it names is alive; ledger target and `review-G7` resolve; all named guards exist; all three spot-checks pass), but the live contract bindings still point at the vanished pre-archive path, and 2 of the 8 named contract guards (`test_measurement_instruments.py`, `test_expression_faces.py`) cannot pass with their dead `SPEC_DIR`. One archived-note reference (`humanize/SKILL.md`) is stale after the skill rename, and five registry/owner references were invalidated by the anchor rename that landed mid-audit (rows 18–22).

SPEC-AUDIT-10-DONE
