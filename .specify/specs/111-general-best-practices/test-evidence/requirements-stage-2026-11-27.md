# Requirements Stage Record — 111-general-best-practices

**Date**: 2026-11-27
**Run**: `r20261127T071500Z-111a` · line `general-best-practices` · stage `requirements`
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/general-best-practices` (branch `111-general-best-practices`, base `0419adae5`)
**Terminal authority**: user request (feature-level port, stability first), `.specify/constitution.md` v1.20.0, `.specify/instructions.md`, ai-harness 087 source set.

## Source verification (read before writing)

Read in full:

- `/storage/project/cloud-native-ai/ai-harness/.ah/specs/087-general-best-practices/` — `requirements.md`, `plan.md`, `tasks.md`, `contracts/best-practices.contract.md`, `verification.md`
- `/storage/project/cloud-native-ai/ai-harness/shared/best-practices/` — `README.md`, `programming-languages.md`, `system-interfaces.md`, `programming-frameworks.md`, `programming-tools.md`

Measured source facts that shaped the spec:

1. Source delivered exactly five documents: manifest + four category owner files (three empty with a "no entries yet" stub, one seeded with the git clone lesson).
2. Source added **no** framework-map row and **no** instructions pointer: whole-repo search for `best-practices` outside the module and its spec returned zero hits.
3. Source accumulation mechanism = feedback observation → promote per knowledge-promotion, by pointer; no new engine, store or renderer.
4. Source guard pinned manifest + four files + accumulation + first entry + mirror parity + no-new-mechanism, red-first.

## Target baseline measurements (2026-11-27, base `0419adae5`)

- `shared/` has no `best-practices/`; `.specify/shared/` likewise.
- `specify init` copies `shared/` wholesale into `.specify/shared/` (`src/specify_cli/__init__.py`, shared copy step) — new subdirectories need no code change.
- `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` contains `("shared", ".specify/shared")`; `tests/contract/test_mirror_parity_suite.py` derives its parameter table from the engine.
- `shared/definitions/framework-map.md` is the framework layout map owner; `.specify/instructions.md` Framework Map section is a pointer to it.
- `shared/guidelines/directory-governance.md` § 3 requires same-change registration of a new directory kind under an existing tree.
- Numbering: spec dirs max 108; branches `109-prompt-adherence` / `110-context-management` / `111-general-best-practices` occupy the next numbers.

## Scaffold deviation (disclosed; A-9)

`create-new-requirements.sh` derives the next number from `.specify/specs/` plus local branch names in the `<NNN>-<slug>` form. With branches 109/110/111 present it would derive **112** and create `112-general-best-practices`, then scaffold there — conflicting with the line's fixed number 111 and its current branch. Per the 108 A-16 precedent, the spec was scaffolded **manually** from `.specify/templates/requirements-template.md` (equivalent copy, branch-creation step skipped), staying on `111-general-best-practices`.

## Gates

| Gate | Command | Verdict | Evidence |
|------|---------|---------|----------|
| Requirements validator | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/111-general-best-practices/requirements.md` | `status: ok`, 0 error / 0 warning; 200 lines, 16 definition rows, 7 shared strings | `requirements-validator.txt` |
| Pre-analyze | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/111-general-best-practices --stage requirements --repo .` | `decision=pass errors=0 advisories=28 waived=0`, summary `fr=9 sc=7`; all advisories are the not-yet-created deliverable paths (`shared/best-practices/**`, `.specify/shared/best-practices/**`, `tests/contract/test_general_best_practices.py`) | `pre-analyze-requirements.json` / `.txt` |
| Decomposition | `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/111-general-best-practices/requirements.md` | `decision=proceed`, `fr_count=9`, `fr_ceiling=120` | `decomposition-requirements.json` / `.txt` |
| Workspace guard | snapshot before writing; check after writing | see Wrap-up line below | `.specify/.tmp/sdd-loop/tmp/general-best-practices/workspace-snapshot-requirements.json` |

Validator repair iterations: 1 (STR-002…STR-005 `Consumed by` cells named SC-001 while SC-001 cited no string ids; SC-001 now cites all four). Re-run recorded above is the stamped one.

## Test entry decision

`scripts/bash/run-tests.sh` was **not** run at this stage: no executable surface changed (requirements + checklist only), and the content guard lands in the implement stage with red-first evidence (FR-007 / SC-007). Recorded as not warranted, not as a skipped obligation.

## Files written (all under this feature's spec directory)

- `.specify/specs/111-general-best-practices/requirements.md`
- `.specify/specs/111-general-best-practices/checklists/requirements.md`
- `.specify/specs/111-general-best-practices/test-evidence/requirements-validator.txt`
- `.specify/specs/111-general-best-practices/test-evidence/pre-analyze-requirements.json` / `.txt`
- `.specify/specs/111-general-best-practices/test-evidence/decomposition-requirements.json` / `.txt`
- `.specify/specs/111-general-best-practices/test-evidence/requirements-stage-2026-11-27.md` (this file)

No spine, feature-registry, glossary, mirror or source-tree edits (A-10).

## Wrap-up accounting (driver-required sanctioned writes)

- Run Determination: `.specify/session/20261127T072252Z-run-determination-speckit-requirements-r20261127t071500z-111.md` — four quantities `not_evaluated` (no token/elapsed/check sensors in this subagent run; satisfaction pending next turn), `trigger_feedback: false`, change-point `cp-r20261127T071500Z-111a findings=4`. A first attempt with `--complexity simple` was skipped by the engine (`simple-unit`); re-run with the honest `complex` classification produced the record.
- Exec Quant: `.specify/exec-quant/records/20261127T072256895807Z-b2ed5204.json` (unit `/speckit.requirements`, run `r20261127T071500Z-111a`).
- Feedback Record: `.specify/feedback/20261127T072303Z-speckit-requirements.md` (`feature: "111-general-best-practices"`, `should_prompt: true` — non-blocking threshold notice left to the driver/user).

## In-passing repair (disclosed)

FR-009 / SC-006 originally enumerated the containment path set without the wrap-up accounting records. The three stores are tracked in git (629 / 578 / 1682 files at baseline), so the mandated accounting writes would have made the containment claim unsatisfiable. FR-009 now names those records with a decidable record-body predicate (feature key or run id), SC-006 references that predicate, and the checklist containment note matches. One reading, local, reversible — recorded here rather than silently.