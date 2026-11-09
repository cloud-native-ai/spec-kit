# Optimization — /study-code

**Run**: `20261109T161336Z-study-code` · **Executor**: improve-skills workflow (target `study-code`)
· **Applied plan**: `improvement-plan.md` entries P-1…P-4 · **Date**: 2026-11-10.

## Target resolution

- Raw identifier: `study-code` → normalized `study-code` (`skill:study-code`).
- Canonical: `skills/external/study-code/SKILL.md` (external layer).
- Mirror: `.specify/skills/study-code/` — generated copy, synced this run.

## Edits applied (plan → change)

| Plan | File / section | Change | Driving evidence |
|---|---|---|---|
| P-1 | `SKILL.md` § Workspace & inputs | `$STUDY_DIR` is now a three-rung fallback ladder: default `$WORK_DIR/../study-code/<repo>-study/` → `.specify/.tmp/study-code/<repo>-study/` → `~/tmp/study-code/<repo>-study/`, with the chosen root and reason recorded in `strip-manifest.md`; governance-allowed temp-root rule kept. | D-S1 / D-O3 |
| P-2 | `SKILL.md` § Step 1 (new item 1) | Source-integrity preflight: `git fsck --no-dangling` plus refs/index readability before cloning; on failure do not touch the source — verify the object store, materialize with `cp -a "$WORK_DIR/." "$STUDY_DIR/stripped/"`, record the commit hash in `target-commit.txt` (provenance follows the hash, not the copied `.git`). | D-S2 / D-P1 |
| P-3 | `SKILL.md` § Step 4 (methodology line) | One pointer line: unreachable draw-diagram backend → UML guide degradation branch (Mermaid sketch + retained `.puml` + visible note); the step never fails on rendering. | D-S3 |
| P-4 | `references/uml-visualization-guide.md` § 5 | Unavailable-backend branch made explicit: three fallback outputs (Mermaid sketch / retained `.puml` source / degradation note) plus the note format with a closed reason enumeration. | D-S3 |

No heading renamed; `$WORK_DIR/docs/overview.md` deliverable statement and all existing obligations preserved
(`test_study_baseline_sections_preserved`, `test_study_deliverable_location_unchanged` green).

## Gate readings

1. **skill-shape.py** — pre-edit: `pass`, exit 0, `est_tokens_controllable` 2528 / budget 5000.
   Post-edit: `pass`, exit 0, 2782 / 5000 (**delta +254**). Remaining finding: `flags-outside-contract`
   (25 CLI flags, `warn`, non-blocking; pre-existing 24 plus the `git fsck` flag pair).
2. **redline-check.py** — pre-edit: exit 0, verdict `PASS` (attribute `sensitive-info` detected,
   `RL-FOCUS-01` not-applicable). Post-edit: identical, exit 0.
3. **Contract suite** —
   `bash scripts/bash/run-tests.sh tests/contract/test_summarize_project_prompt_assets.py tests/contract/test_skill_layer_visibility_guards.py tests/contract/test_run_skills_wiring.py tests/contract/test_expression_compatibility.py -q`
   - Pre-edit baseline: `3 failed, 80 passed` — FAILED: `test_c5_non_wiring_files_keep_their_frozen_hashes`,
     `test_c5_wiring_surface_is_closed`, `test_c2_no_project_side_classification_store` (all in
     `test_expression_compatibility.py`; the first dies on a missing manifest file
     `.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` before any hash
     comparison — unrelated pre-existing red).
   - Post-edit: `3 failed, 80 passed` — the **same failure names**, no additions. Zero regression;
     all study-code prompt-asset tests green.
4. **sync-mirrors.py** — write: exit 0, synced `.specify/skills/study-code/SKILL.md` and
   `.specify/skills/study-code/references/uml-visualization-guide.md`. `--check`: exit 0,
   `skills/external/ == .specify/skills/ (426 files, byte-identical)`.

## Runtime validation of added commands

Scratch repo `~/tmp/study-code-check.XXXXXX` (created and removed this run; healthy path and both
corruption triggers observed, not inferred):

| Check | Healthy | Corrupted |
|---|---|---|
| `git fsck --no-dangling` | exit 0 | exit 10 (refs zeroed) |
| `git rev-parse HEAD` | exit 0 | exit 128 |
| `git status` (index readable) | exit 0 | exit 128 (index overwritten) |
| `cp -a "$SRC/." "$DST/"` | materialized `a.txt` + `.git` | — |

## Anomaly (disclosed, out of scope)

A merge is in progress in this workspace (`.git/MERGE_HEAD` = `2344a1036`), and a concurrent sdd-loop fork
(`hist-wave1`) writes the same tree: `.specify/skills/internal/create-team/SKILL.md` read `UU` then `M.`
between two status checks. The required `sync-mirrors` gate incidentally regenerated that generated mirror
from its canonical copy (`skills/internal/create-team/SKILL.md`). No commit was made; no conflicted or
unrelated content was resolved or deleted by this run; `.specify/.tmp/` content untouched.

## Outcome status

- `optimization: applied` — edits landed, gates green, mirrors synced.
- Improvement outcome **pending**: per improve-skills Hard Constraint 9, "improved" is decided by the next
  comparable study-code run (D-S1…D-S3 absent), not by this record.
