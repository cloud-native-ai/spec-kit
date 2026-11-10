# Spec audit — 008-create-skills-skill (batch 3)

**Audit date**: 2026-11-10
**Tree audited**: `/storage/project/cloud-native-ai/spec-kit` @ `564a5f5a6` (branch `master`)
**Target**: `.specify/archive/specs/008-create-skills-skill/` — 9 Markdown artifacts + 1 OpenAPI contract
(`requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `research.md`, `feature-ref.md`,
`checklists/create-skills-extraction.md`, `checklists/requirements.md`, `contracts/create-skills-workflow.openapi.yaml`)
**Mode**: read-only. This file is the only write; no spec/source file was modified, no subagents, no commits.

## Scope & method

1. Extracted every repository-path token (`plid` prefixes `.specify/`, `scripts/`, `skills/`, `templates/`, `shared/`,
   `tests/` + tree-implied paths + `pyproject.toml`) with `rg -o`, then normalised trailing `/`, `>` (from the
   `skill_id` literal) and prose false positives (`/skills/route`, `/skills/create`, "tests/checks").
2. Classified each distinct target: **alive** (exists now), **archived-elsewhere** (exists under
   `.specify/archive/specs/008-create-skills-skill/` or another archive of the same object), **dead** (no target; a stale
   pre-archive `.specify/specs/008-create-skills-skill/...` path counts as dead per the audit rule).
3. Checked the ledger row and its named target, the named guard files, and three implementation claims.

## Counts

| Metric | Value |
|---|---|
| Distinct repository-path targets | **28** |
| alive | **17** |
| archived-elsewhere | **0** |
| dead | **11** |
| Raw mentions | ≈150 (142 extractor matches + 8 tree-implied/incidental) |

Archived-elsewhere is 0 by the audit rule: every reference to the spec's own artifacts uses the stale pre-archive
prefix, which the rule classifies as dead. Note the nuance: the *objects* of 4 such dead paths (requirements, plan,
quickstart, extraction checklist) exist verbatim under `.specify/archive/specs/008-create-skills-skill/`, so they are
moved-with-the-archive, not vanished.

Alive targets (17): `templates/commands/skills.md`; `skills/external/create-skills/` (dir) and its `SKILL.md`;
`skills/external/create-skills/references/` (dir) and `skill-creation-quality-checklist.md`;
`.specify/skills/` (dir); `.specify/skills/create-skills/` (dir) and its `SKILL.md` + `references/skill-creation-quality-checklist.md`;
`.specify/instructions.md`; `.specify/memory/features.md`; `.specify/memory/features/013.md`;
`scripts/bash/create-new-skill.sh`; `tests/contract/test_skill_install_layout_contract.py`;
`tests/integration/test_skill_install_layout_integration.py`; `tests/integration/test_skills_resource_ids.py`;
`pyproject.toml`.

## Broken list (every dead item as path:line -> current resolution)

Pre-archive self-references (object now under the archive, path dead):

- `.specify/archive/specs/008-create-skills-skill/plan.md:4` -> `.specify/specs/008-create-skills-skill/requirements.md` does not exist; resolves under `.specify/archive/specs/008-create-skills-skill/requirements.md`
- `plan.md:43` -> documentation tree header `.specify/specs/008-create-skills-skill/` does not exist (dir archived)
- `tasks.md:6` -> `.specify/specs/008-create-skills-skill/` does not exist
- `tasks.md:34` -> `.specify/specs/008-create-skills-skill/plan.md` and `.../requirements.md` do not exist
- `tasks.md:52,136` -> `.specify/specs/008-create-skills-skill/checklists/create-skills-extraction.md` does not exist
- `tasks.md:138` -> `.specify/specs/008-create-skills-skill/requirements.md` does not exist
- `tasks.md:141` -> `.specify/specs/008-create-skills-skill/quickstart.md` does not exist
- `feature-ref.md:4` -> `.specify/specs/008-create-skills-skill/requirements.md` does not exist

Deleted guard files (commit `cabc9f1e3`, "test: delete 47 files that cannot fail or whose subject no longer exists"):

- `tasks.md:37,48,49,50,51,66,67,90,91,113,114,115,139,143,185,186,192,193,199,200,201,227` -> `tests/contract/test_create_skills_prompt_assets.py` **missing** (no copy in any archive or worktree). Partial successor: `tests/contract/test_portable_skill_creation.py` (SKILL.md + mirror + checklist + script), `tests/contract/test_run_skills_wiring.py:186-196` (skills.md routing table)
- `tasks.md:140,228`; `quickstart.md:55`; `plan.md:82` -> `tests/contract/test_create_new_skill_contract.py` **missing** (deleted same commit; no direct successor). The scaffold it guarded now carries its own `--help`/`--version` contract (`scripts/bash/create-new-skill.sh:12-22`)
- `quickstart.md:55`; `plan.md:83-84` -> `tests/contracts/test_skill_install_layout_contract.py` **missing** (`tests/contracts/` never existed as a directory); the real file `tests/contract/test_skill_install_layout_contract.py` is alive — a path typo, not a missing guard

Relocated skill paths in the plan's source tree (subject moved; path never re-pointed):

- `plan.md:63-65` -> `skills/create-skills/SKILL.md` **missing**; the same object now lives at `skills/external/create-skills/SKILL.md` (git: created at `skills/create-skills/SKILL.md` in `2db6a3952`, later moved to the `external/` layer)
- `plan.md:66-67` -> `skills/analysis-project/SKILL.md` **missing**; no `analysis-project` directory exists anywhere. Lineage renamed to `summarize-project` and now sits at `skills/internal/summarize-project/` + `.specify/skills/internal/summarize-project/`
- `plan.md:68-69` -> `skills/improve-skills/SKILL.md` **missing**; now `skills/external/improve-skills/SKILL.md` (mirror at `.specify/skills/improve-skills/SKILL.md`)

Stale implementation claims (file exists, claim no longer true — not a path break):

- `tasks.md:51` (T009) and `tasks.md:142` (T043) -> `pyproject.toml` no longer force-includes `skills/`; packaging moved to `src/hatch_build.py` `_stage_skills()` (stage-copy into `specify_cli/skills`, spec 046). Comment at `pyproject.toml:48-50` states this intentionally
- `tasks.md:126` (T036) -> the `.specify/instructions.md` Skills registry row is gone because the registry itself was retired: `instructions.md:304` now reads "No registration tables — agents discover resources from the filesystem", and `.specify/skills.md` says it is "not a registry". `create-skills` remains discoverable via `.specify/skills/create-skills/SKILL.md`

Pending anchor-layout rename (references that will move; audited against the current tree as-is):

- `.specify/memory/features.md` (`tasks.md:12,123,138`) -> will become `.specify/features.md`
- `.specify/memory/features/013.md` (`tasks.md:13,137`) -> will become `.specify/features/013.md`
  (Evidence: branch worktree `.specify/.tmp/sdd-loop/worktrees/rename-anchors/` already has `.specify/features.md` and `.specify/features/`; the main tree still has only `.specify/memory/features.md`.)

## Ledger-target check (`.specify/archive/specs/CONSOLIDATION-LEDGER.md`)

- Row (line 12): `| 008-create-skills-skill | archive | Feature 013 child (historical) | review-G2 |`
- Archive target: `.specify/archive/specs/008-create-skills-skill/` exists and is complete -> **resolves**.
- Reference target Feature 013 resolves: `.specify/memory/features.md:22` has row `013 | Skills Command | ... | Implemented | .specify/memory/features/013.md | .specify/specs/030-summarize-project/requirements.md | 2026-07-25`; the detail file exists and its item 14 records 008's completion; the current "latest spec" (`030-summarize-project/requirements.md`) exists. The row's verdict (`archive`) and target ("Feature 013 child (historical)") are **accurate**.
- Provenance gap (minor): `review-G2` has no standalone artifact anywhere in the tree; it resolves only to a one-line record in `.specify/specs/090-re-anchoring/test-evidence/history-distill-batch-2.md:117` naming an intended `review-G2.md` that was never landed.

## Missing guards (summary)

| Named guard | State |
|---|---|
| `tests/contract/test_create_skills_prompt_assets.py` | **missing** — deleted `cabc9f1e3`; partial successor `test_portable_skill_creation.py` |
| `tests/contract/test_create_new_skill_contract.py` | **missing** — deleted `cabc9f1e3`; no successor |
| `tests/contracts/test_skill_install_layout_contract.py` | **missing** — typo dir; real file alive under `tests/contract/` |
| `tests/contract/test_skill_install_layout_contract.py` | present |
| `tests/integration/test_skill_install_layout_integration.py` | present |
| `tests/integration/test_skills_resource_ids.py` | present |

## Three implementation spot-checks

1. **File** — `skills/external/create-skills/references/skill-creation-quality-checklist.md` (T031/T032): **PASS**.
   Exists; linked from `skills/external/create-skills/SKILL.md:154` via relative path
   `./references/skill-creation-quality-checklist.md`; the `.specify/skills/create-skills/` mirror is byte-equal
   (all four reference files are byte-equal).
2. **Symbol/command** — `scripts/bash/create-new-skill.sh` (plan.md:78, "existing deterministic Skill scaffold/refresh
   script"): **PASS**. Exists; `--help` exits 0 with a declared interface (`--json`, `--refresh-only`, `--name`,
   `--description`, `--output-dir`; `--version` declared); default write target is `.specify/skills/<name>`
   (`create-new-skill.sh:99-102,380`), i.e. the current-workspace layer, not the root `skills/external/` canonical layer.
3. **Behaviour surface** — `/speckit.skills` routing (T022/T023, data-model "Target Skill Lifecycle"): **PASS**.
   `templates/commands/skills.md:15` declares delegation-only orchestration; `:35` maps `NOT exists -> create-skills
   -> skills/external/create-skills/SKILL.md`; `:36` maps `EXISTS -> improve-skills -> skills/external/improve-skills/SKILL.md`.
   Guarded by `tests/contract/test_run_skills_wiring.py::test_c10_skills_md_routing_five_rows` (`:186-196`).
   Companion claim also holds: `skills/external/create-skills/SKILL.md:2-5` carries `name: create-skills`,
   trigger-rich `description`, `skill_id: "<SKILL:.specify/skills/create-skills/SKILL.md>"` (plus a later
   `classification: external`), and the `.specify` mirror is byte-equal.

## Verdict: **BROKEN**

The capability itself is intact — the Skill, its mirror, the checklist, the routing command, the scaffold script and the
Feature 013 registry binding all resolve, and all three spot-checks pass. The spec is BROKEN as an archived record:
11 dead path references (8 pre-archive self-paths, 2 deleted test files + 1 typo'd test path, 3 relocated skill-tree
paths), 2 named guard files that no longer exist, and 2 superseded implementation claims (pyproject force-include,
instructions.md registry row). Repair is pointer-only (re-point to archive / `external/` paths and successors); no
re-implementation is implied.

**Anomaly**: the archived `tasks.md` closed with T041 still unchecked (`tasks.md:140`) and `CONSOLIDATION-LEDGER.md:23` appends the 054 row after the ledger's own "Deferred"/"Not executed" footer — two bookkeeping defects in the archived record, neither a path break.

SPEC-AUDIT-3-DONE
