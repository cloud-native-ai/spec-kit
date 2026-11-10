# Spec audit — 007-skill-install-layout (batch 2)

- **Date**: 2026-11-10
- **Tree audited**: `/storage/project/cloud-native-ai/spec-kit` on `master` (current working tree, read-only; no spec or source file was modified by this audit)
- **Spec under audit**: `.specify/archive/specs/007-skill-install-layout/`
- **Method**: every repository-path reference in the archived artifacts was extracted, then resolved against the current tree with filesystem existence checks. Contract tests, guard files and implementation claims were spot-checked statically (files were read, not executed — executing them would have written caches, outside this audit's write budget).

## Scope

Artifacts read in full:

| Artifact | Status |
|---|---|
| `requirements.md` | present |
| `plan.md` | present |
| `tasks.md` | present |
| `data-model.md` | present |
| `quickstart.md` | present |
| `checklists/requirements.md` | present |
| `contracts/skill-install-layout.openapi.yaml` | present |
| `verification.md` / `notes.md` / `research.md` | **absent** — the audit set names them, but the archive contains none of them |

Classification rule applied:

- **alive** — the target path exists in the current tree.
- **archived-elsewhere** — the reference is a bare spec-local filename and its content now exists under `.specify/archive/specs/007-skill-install-layout/`.
- **dead** — no target exists; per the audit instruction, any path literally written as `.specify/specs/007-skill-install-layout/...` is dead even though the same-named file survives in the archive.

## Reference census

**Refs total: 47 distinct path references** (repeated occurrences of the same path are counted once, and all their anchors are given for the dead ones). Split: **alive 32 / archived-elsewhere 7 / dead 8**. Occurrence-level, the dead references appear **17 times** across the archived artifacts.

### Alive (32)

Implementation anchors:

- `.specify/skills/` — req:35, plan:22,27, tasks:45,48, quickstart:22; 18 skill directories present.
- `.specify/skills/<skill-name>/` — req:101,120, data-model:15, plan:94.
- `.specify/skills/<skill-name>/SKILL.md` — data-model:16, plan:95-97 (e.g. `.specify/skills/create-skills/SKILL.md` exists).
- `.specify/skills/*/SKILL.md` — plan:175, tasks:47.
- `.github/skills/` — req:50,143, plan:99; exists as a **directory-level symlink** `../.specify/skills`.
- `.github/skills/<skill-name>` — req:58,86,121, data-model:32, plan:101; resolves through that symlink (`.github/skills/create-skills/SKILL.md` exists).
- `.specify/skills/my-skill`, `.github/skills/my-skill` (contract examples) — contracts:123,156; example values, parents alive.
- `.specify` (bare workspace anchor) — tasks:51.

Scripts, CLI, templates:

- `scripts/bash/create-new-skill.sh` — plan:84,174, tasks:45,70,99,129,198.
- `.specify/scripts/bash/create-new-skill.sh` — plan:91,174, tasks:46,71,100,130,199; byte-identical to the `scripts/` copy.
- `scripts/python/skills-utils.py` — plan:86,175, tasks:47,49,200.
- `.specify/scripts/python/skills-utils.py` — plan:93,175, tasks:48,50,201; byte-identical to the `scripts/` copy.
- `scripts/bash/*.sh` — plan:21.
- `src/specify_cli/__init__.py` — plan:80.
- `templates/commands/plan.md` — plan:6.
- `templates/commands/skills.md` — tasks:72; `/speckit.skills` (quickstart:10,80, tasks:149) is backed by this template.
- `templates/skills-template.md` — tasks:73; its line 39 still states the canonical path `.specify/skills/{{SKILL_NAME}}/SKILL.md`.

Tests:

- `tests/contract/test_skill_install_layout_contract.py` — tasks:33,65,152,194, quickstart:75-77.
- `tests/integration/test_skill_install_layout_integration.py` — tasks:33,66,94,95,123-125,152,195-196, quickstart:75-77.
- `tests/unit/test_skills_utils_layout.py` — tasks:33,51,152, quickstart:78.
- `tests/fixtures/skill-layout/` — tasks:34; present but contains only `.gitkeep`.
- `tests/integration`, `tests/unit` — plan:23,105,106.

Registry and docs:

- `.specify/memory/constitution.md` — plan:117.
- `.specify/memory/features.md` — plan:117, tasks:151.
- `.specify/memory/features/*.md` — plan:117.
- `.specify/memory/features/013.md` — tasks:150.
- `README.md` — plan:117, tasks:148.
- `docs/*.md` — plan:117.
- `docs/tutorials/quickstart.md` — tasks:149.

### Archived-elsewhere (7)

Bare spec-local filenames; each resolves to the archived copy:

| Reference | Anchor | Resolves to |
|---|---|---|
| `requirements.md` | plan:117 | `.specify/archive/specs/007-skill-install-layout/requirements.md` |
| `plan.md` | plan:59, tasks:7 | `…/archive/…/plan.md` |
| `data-model.md` | plan:60, tasks:7 | `…/archive/…/data-model.md` |
| `quickstart.md` | plan:61, tasks:7 | `…/archive/…/quickstart.md` |
| `tasks.md` | plan:66 | `…/archive/…/tasks.md` |
| `contracts/skill-install-layout.openapi.yaml` | plan:63, tasks:7 | `…/archive/…/contracts/skill-install-layout.openapi.yaml` |
| `checklists/requirements.md` | plan:65 | `…/archive/…/checklists/requirements.md` |

### Dead (8) — broken list

- `.specify/archive/specs/007-skill-install-layout/plan.md:3` -> `.specify/specs/007-skill-install-layout/requirements.md` (link text and href) missing; the file is at `.specify/archive/specs/007-skill-install-layout/requirements.md`
- `.specify/archive/specs/007-skill-install-layout/plan.md:4` -> same missing pre-archive path; archived copy as above
- `.specify/archive/specs/007-skill-install-layout/plan.md:58` -> `.specify/specs/007-skill-install-layout/` directory missing; the spec directory lives at `.specify/archive/specs/007-skill-install-layout/`
- `.specify/archive/specs/007-skill-install-layout/plan.md:149` -> `.specify/specs/007-skill-install-layout/data-model.md` missing; archived copy exists
- `.specify/archive/specs/007-skill-install-layout/plan.md:153` -> `.specify/specs/007-skill-install-layout/contracts/skill-install-layout.openapi.yaml` missing; archived copy exists
- `.specify/archive/specs/007-skill-install-layout/plan.md:158` -> `.specify/specs/007-skill-install-layout/quickstart.md` missing; archived copy exists
- `.specify/archive/specs/007-skill-install-layout/tasks.md:6` -> `.specify/specs/007-skill-install-layout/` directory missing; archived copy exists
- `.specify/archive/specs/007-skill-install-layout/tasks.md:35,79,108,138,153` -> `.specify/specs/007-skill-install-layout/quickstart.md` missing; archived copy exists
- `.specify/archive/specs/007-skill-install-layout/checklists/requirements.md:5` -> `.specify/specs/007-skill-install-layout/requirements.md` missing; archived copy exists
- `.specify/archive/specs/007-skill-install-layout/plan.md:23` -> `tests/contracts` missing (plural typo); the suite directory is `tests/contract` (singular)
- `.specify/archive/specs/007-skill-install-layout/plan.md:104` -> `tests/contracts/` same plural typo; actual `tests/contract/`
- `.specify/archive/specs/007-skill-install-layout/plan.md:117` -> `research.md` missing symbol; no research document exists in the archive or anywhere in the tree
- `.specify/archive/specs/007-skill-install-layout/tasks.md:148` -> `docs/skills/vscode.md` missing; `docs/skills/` no longer exists, no archive copy exists, and the nearest current VS Code coverage is `docs/reference/cli/github-copilot.md`

## Ledger-target check

Ledger row audited: `.specify/archive/specs/CONSOLIDATION-LEDGER.md:11` — `007-skill-install-layout | archive | Feature 013 child (historical) | review-G2`.

- **Verdict column accurate**: the spec directory is in `.specify/archive/specs/`, matching `archive`.
- **Target resolves**: Feature 013 resolves in the registry — `.specify/memory/features.md:22` (row `013 | Skills Command | … | Implemented`) points at `.specify/memory/features/013.md`, which exists and is titled "Skills Command".
- **Binding accurate**: `requirements.md:15-16` binds Feature ID 013 / Skills Command; the detail file acknowledges 007 at `.specify/memory/features/013.md:26-27` and lists it as historical at lines 110-115.
- **Two accuracy defects around the row**:
  1. `.specify/memory/features/013.md:110-115` still links six pre-archive paths (`.specify/specs/007-skill-install-layout/…` for requirements, checklist, plan, data model, contract, quickstart) — all dead; the registry's own historical links were not repointed when the spec was archived.
  2. The Notes pointer `review-G2` has no artifact in the tree: `review-G2.md` does not exist; the only occurrences are the ledger itself and a mention in `.specify/specs/090-re-anchoring/test-evidence/history-distill-batch-2.md:117`. The verdict is reproducible, but the named review record is not retrievable.
- Unrelated ledger formatting defect noticed while reading the table: the `054-agent-registration-wiring` row at `CONSOLIDATION-LEDGER.md:23` sits after the "Not executed" paragraph, outside the table.

## Missing guards

None of the guard files the spec names are missing:

| Named guard | Status |
|---|---|
| `tests/contract/test_skill_install_layout_contract.py` | present (42 lines) |
| `tests/integration/test_skill_install_layout_integration.py` | present (159 lines) |
| `tests/unit/test_skills_utils_layout.py` | present (22 lines) |
| `tests/fixtures/skill-layout/` | present, but only `.gitkeep` — no fixture data backs the layout scenarios |

Artifact-completeness gaps (not missing files): tasks `T019`, `T029`, `T030`, `T040`, `T046` remain unchecked in `tasks.md` (manual quickstart verification and the `migrate-legacy` contract assertion).

## Three implementation claims — spot checks

1. **File claim** (`tasks.md:45,70`, plan's structure decision): `scripts/bash/create-new-skill.sh` creates the primary copy under `.specify/skills/<name>/` and the `.github/skills/<name>` compatibility entrypoint (symlink, or a placeholder with a marker file when symlinks are unsupported), plus legacy-directory migration. **Holds**: `create_github_entrypoint` at `scripts/bash/create-new-skill.sh:203`, `mark_placeholder_entrypoint` at :186, migration handling from :259; the `.specify/scripts/` mirror is byte-identical.
2. **Symbol/command claim** (`tasks.md:47,49`): `scripts/python/skills-utils.py` owns the layout status vocabulary and canonical skill-path inference. **Holds**: `ENTRYPOINT_STATUS` / `OUTCOME_STATUS` at `scripts/python/skills-utils.py:11-12`; `.specify/skills/*/SKILL.md` inferred as a skill at :43-46; the unit test asserts the enums and both path forms. One note: the legacy `.github/skills/*/SKILL.md` path is still classified as a skill (line 45) — deliberate, as the unit test asserts it, so compatibility is accepted rather than treated as primary.
3. **Behaviour surface claim** (`contracts/skill-install-layout.openapi.yaml:11-104`; `quickstart.md:75-78`): install/entrypoint/migrate outcomes surface `created|reused|failed`, `created|skipped|failed|conflict`, `success|partial-success|failed`, and `manual-required`. **Holds**: the contract test drives the install script and asserts `status`, `primary_copy_status`, `overall_status`, `migration_state` (`tests/contract/test_skill_install_layout_contract.py:29-42`); the integration test covers symlink, forced placeholder, `conflict-entry-path`, legacy migration and backup-failure → `partial-success` + `manual-required` (`tests/integration/test_skill_install_layout_integration.py:65-158`).

## Pending anchor-layout rename — references that will move

The `rename-anchors` worktree (`.specify/.tmp/sdd-loop/worktrees/rename-anchors`, commit `8b9030371`) moves the project anchors out of `memory/`. The following references from this spec are alive today but will move:

| Current reference (anchors) | Post-rename target |
|---|---|
| `.specify/memory/constitution.md` (plan:117) | `.specify/constitution.md` |
| `.specify/memory/features.md` (plan:117, tasks:151) | `.specify/features.md` |
| `.specify/memory/features/*.md` (plan:117) | `.specify/features/<NNN>-<slug>.md` |
| `.specify/memory/features/013.md` (tasks:150) | `.specify/features/013-portable-skill-creation.md` (filename gains the slug) |

Also affected outside the spec artifacts: the live implementation path `.specify/memory/tools/` in `scripts/python/skills-utils.py:40` moves to `.specify/tools/` under the same branch.

## Verdict

**BROKEN.**

The spec's implementation surface is intact — every skill-layout script, template, contract test, guard and fixture it names exists, the script/`skills-utils` mirrors are byte-identical, and all three spot-checked claims hold. What is broken is path hygiene around the archive: 8 distinct references (17 occurrences) are dead, all of them either the stale pre-archive spec directory (content preserved in the archive, links never repointed), the `tests/contracts` plural typo, the never-written `research.md`, or the vanished `docs/skills/vscode.md`. The consolidation ledger row is substantively accurate, but the Feature 013 registry detail still links the dead pre-archive paths, and its `review-G2` note has no retrievable record.

**Anomaly**: all six archived Markdown artifacts have had their prose replaced by `[CN]` placeholders — the archived specification is no longer readable as a specification and cannot be re-verified from its own text; additionally `.specify/memory/features/013.md:110-115` retains dead pre-archive links, `docs/skills/vscode.md` (task T041) was moved out of `docs/` with no archive copy, and the ledger's `review-G2` pointer is unresolvable.

SPEC-AUDIT-2-DONE
