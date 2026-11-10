# Spec audit — live batch 5 (7 specs)

- **Date**: 2026-11-10
- **Tree audited**: `/storage/project/cloud-native-ai/spec-kit` on `master`, read-only. No spec or source file was modified by this audit; the only write is this findings file.
- **HEAD at start**: `564a5f5a6`; **HEAD at end**: `6fb8093c4` (`merge(layout): move the project anchors out of memory/`). The anchor-layout rename landed **during** the audit, so every reference into `.specify/memory/{features,constitution,glossary,register,tools}` was re-checked against the post-rename tree. All counts below are against `6fb8093c4` unless stated otherwise.
- **Specs**: 013-portable-skill-creation, 031-task-complexity-rubric, 043-init-commit-stamp, 057-decompose-command-skills, 069-execution-expression-sdd, 079-bilingual-expression, 091-auto-git-closeout.
- **Method**: every repository-path token in `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `research.md`, `contracts/**.md`, `notes/**.md`, and (auxiliary) `checklists/requirements.md` was extracted and resolved by filesystem existence. `test-evidence/`, `code-review.md`, `review.md`, `waivers.md`, `coverage-baseline.txt` and failed-run logs were excluded from the census (they are dated records, not live pointers). Tests and contract guards were read statically; nothing was executed, to keep the read-only budget.

Census vocabulary used below:

- **alive** — the path (or its glob/equivalent) exists now.
- **archived-elsewhere** — target moved under `.specify/archive/`; content is retrievable there.
- **dead** — no target; includes pointers at pre-consolidation paths and renamed/moved implementation files.
- **moved-by-rename** — a `.specify/memory/...` anchor reference whose post-rename target exists under `.specify/` root. Counted separately from dead because the rename is sanctioned and landed mid-audit.
- **ephemeral** — a documented temp/scratch or git-ignored local-evidence path that was removed by design.
- **excluded** — a prose fragment, brace expansion, or naming-pattern placeholder, not a concrete path pointer.

## Batch summary

| Spec | refs | alive | archived | dead | verdict |
|---|---|---|---|---|---|
| 013-portable-skill-creation | 28 | 22 | 0 | 3 | **BROKEN** |
| 031-task-complexity-rubric | 14 | 9 | 0 | 0 | **INTACT** |
| 043-init-commit-stamp | 27 | 18 | 0 | 2 | **BROKEN** |
| 057-decompose-command-skills | 62 | 54 | 0 | 1 | **BROKEN** |
| 069-execution-expression-sdd | 33 | 27 | 3 | 0 | **INTACT** |
| 079-bilingual-expression | 99 | 88 | 0 | 0 | **INTACT** |
| 091-auto-git-closeout | 116 | 108 | 0 | 4 | **BROKEN** |

`refs` = distinct path references after removing prose fragments, brace expansions and naming-pattern placeholders. Per-spec sections give the moved-by-rename / ephemeral / excluded splits that are not columns above.

## 013-portable-skill-creation

**Artifacts read**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `feature-ref.md`, `contracts/portable-skill-creation.openapi.yaml`, `checklists/requirements.md`.

**Census**: 28 refs — alive 22 / archived 0 / dead 3 / moved-by-rename 2. Excluded 1 prose fragment (`scripts/references/assets` at `tasks.md:84`, which is prose, not a path). Quickstart example skill names (`my-new-skill`, `portable-demo`, `custom-skill`) are illustrative values with a living parent and are counted alive.

**Broken list**

- `.specify/specs/013-portable-skill-creation/contracts/portable-skill-creation.openapi.yaml:17` -> `skills/create-skills/SKILL.md` **missing**. Pre-consolidation path: the canonical skill is now `skills/external/create-skills/SKILL.md`; only the runtime mirror `.specify/skills/create-skills/SKILL.md` still carries that old-shaped name.
- `.specify/specs/013-portable-skill-creation/contracts/portable-skill-creation.openapi.yaml:61` -> same missing `skills/create-skills/SKILL.md` as `target_a` of the mirror-parity assertion.
- `.specify/specs/013-portable-skill-creation/contracts/portable-skill-creation.openapi.yaml:67` -> `skills/create-skills/references/skill-creation-quality-checklist.md` **missing**; canonical is `skills/external/create-skills/references/skill-creation-quality-checklist.md`, runtime mirror exists at `.specify/skills/create-skills/...`.
- `.specify/specs/013-portable-skill-creation/plan.md:170` and `tasks.md:17,143` -> `tests/contract/test_create_skills_prompt_assets.py` **missing**. Deleted in `cabc9f1e3` ("test: delete 47 files that cannot fail or whose subject no longer exists"); its subject was the retired `skills/create-skills/` path.

**Registry**: Feature 013 row resolves — `.specify/features.md:22` has Spec Path `.specify/specs/030-summarize-project/requirements.md` and Feature Details `.specify/features/013-portable-skill-creation.md` (exists; content "Skills Command"). This spec is iteration 5 of Feature 013, recorded at detail lines 38–41 and 79–89; the row's Spec Path points at the latest iteration (030), not at this directory. Resolves at feature level; no broken cell.

**Guards**: `tests/contract/test_portable_skill_creation.py` present with 9 tests matching T002–T010. Missing: `tests/contract/test_create_skills_prompt_assets.py` (named in DoD and T037, deleted as above).

**Spot checks** (3/3 hold)

1. `scripts/bash/create-new-skill.sh` no longer defines or calls `refresh_tools_for_target` — 0 hits; `create_skill_structure()` lives at `scripts/bash/common.sh:294`.
2. `templates/skills-template.md` carries `## Resources` at line 56 and no `### Tools` / `refresh-tools` text.
3. Mirror parity holds: `skills/external/create-skills/SKILL.md` is byte-identical to `.specify/skills/create-skills/SKILL.md`; the checklist and `improve-skills` mirrors are identical too.

**Rename-moved**: `.specify/memory/features.md` (tasks:5) -> `.specify/features.md`; `.specify/memory/features/013.md` (feature-ref:41) -> `.specify/features/013-portable-skill-creation.md`.

**Verdict: BROKEN** — implementation and three spot checks hold, but the contract YAML still targets three pre-consolidation `skills/create-skills/...` paths and the DoD names a deleted guard test.

## 031-task-complexity-rubric

**Artifacts read**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `contracts/rubric-section.md`, `checklists/requirements.md`.

**Census**: 14 refs — alive 9 / archived 0 / dead 0 / moved-by-rename 3. Excluded 2 prose fragments (`docs/feature` at plan:38 and `shared/irreversible` at data-model:18 are sentence fragments).

**Broken list**: none.

**Registry**: Feature 032 row resolves — `.specify/features.md:41` points at Spec Path `.specify/specs/031-task-complexity-rubric/requirements.md` and Feature Details `.specify/features/032-dogfooding-practice.md`. The file exists and its content is correctly "Task Complexity Rubric"; the **filename slug is wrong** (`dogfooding-practice` belongs to Feature 036, not 032) — a post-rename naming defect in the registry, not a missing cell. See Anomaly.

**Guards**: `tests/contract/test_task_complexity_rubric.py` present with 13 tests covering C-1…C-10 plus the amended summary+pointer checks. No missing guards.

**Spot checks** (3/3 hold)

1. `## Task Complexity Rubric` is present at `templates/instructions-template.md:110` and `.specify/templates/instructions-template.md:110`; the section text is byte-identical between the two mirrors.
2. The guard reads the full rubric from `shared/guidelines/task-complexity-rubric.md` (and its `.specify/shared/` mirror), asserting the pointer form now used by the template.
3. `scripts/bash/generate-instructions.sh:35` renders `.specify/templates/instructions-template.md`; the live `.specify/instructions.md:124` carries the section, so the generation path claimed by the plan holds.

**Rename-moved**: `.specify/memory/constitution.md` (plan:29) -> `.specify/constitution.md`; `.specify/memory/features.md` and `.specify/memory/features/032.md` (plan:34) -> `.specify/features.md`, `.specify/features/032-dogfooding-practice.md`.

**Verdict**: **INTACT** — template, mirror, generator, guard and registry all resolve; only the registry filename slug is misleading (flagged in Anomaly).

## 043-init-commit-stamp

**Artifacts read**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `contracts/source-stamp-resolution.contract.md`, `contracts/source-stamp-write.contract.md`, `contracts/build-embedding.contract.md`, `checklists/requirements.md`.

**Census**: 27 refs — alive 18 / archived 0 / dead 2 / moved-by-rename 3. Excluded 4 prose/brace fragments (`.specify/version.json` in a reserved-identifier sentence, `memory/scripts/templates/skills/agents/shared`, `src/scripts/templates/.specify/scripts`, `tests/{contract`).

**Broken list**

- repo-root `hatch_build.py` -> **moved to `src/hatch_build.py`** (commit `7af0982c3`, "hatch_build.py 迁入 src 树"). Still written as the repo-root hook in 14 artifact occurrences: `plan.md:9,74,105`; `tasks.md:41,111,116,171`; `data-model.md:24`; `feature-ref.md:11`; `contracts/build-embedding.contract.md:1,4,34,48`; `contracts/source-stamp-resolution.contract.md:15`.
- `.specify/specs/043-init-commit-stamp/contracts/build-embedding.contract.md:10` -> claims the hook loads `src/specify_cli/__init__.py` via importlib; the actual `src/hatch_build.py:47` loads the stdlib-only `src/specify_cli/_provenance.py`, and `pyproject.toml:33-34` declares `path = "src/hatch_build.py"`. The "single probe grammar" intent holds; the stated import surface does not.
- `.specify/specs/043-init-commit-stamp/feature-ref.md:4` -> `.specify/version` **missing**. This is explicitly the reserved path for Feature 024 (the spec says "`.specify/version` 归 024 设想"); count it as dead-but-reserved, not a defect.
- Note: `src/specify_cli/_source_commit.json` is absent from the checkout **by design** (build artifact; `.gitignore:63` ignores it; the hook writes it at build time) and is counted alive-by-design.

**Registry**: Feature 045 row resolves — `.specify/features.md:54` points at Spec Path `.specify/specs/043-init-commit-stamp/requirements.md` and Feature Details `.specify/features/045-sanitize-command.md`. The file exists and its content is correctly "Framework Source Provenance"; the **filename slug is wrong** (`sanitize-command`) — a post-rename naming defect, not a missing cell. See Anomaly.

**Guards**: `tests/contract/test_source_stamp.py`, `tests/contract/test_build_hook.py`, `tests/integration/test_init_source_stamp.py` all present. No missing guards.

**Spot checks** (3/3 hold; one surface note)

1. `src/specify_cli/__init__.py:595` re-exports `_probe_head_commit` from `src/specify_cli/_provenance.py:26`; `resolve_source_commit()` is at `__init__.py:601` and `write_source_stamp()` at `:606`. The symbol claim holds; authority moved from `__init__.py` to `_provenance.py`.
2. `write_source_stamp` writes `<project>/.specify/source.json` as `{framework, commit, stamped_at[, reason]}`, full overwrite, warns and returns `False` on `OSError` — never blocks init. The live `.specify/source.json` carries `commit ec17c599cb04c8acd4525254e2cdbd9d6e84a980`.
3. `pyproject.toml:33-34` declares the custom build hook, `.gitignore:63` ignores the embedded artifact, `src/hatch_build.py` exists, and `docs/tutorials/installation.md:95-118` carries the Source Stamp section. Holds with the relocated path.

**Rename-moved**: `.specify/memory/constitution.md` (plan:27) -> `.specify/constitution.md`; `.specify/memory/features/045.md` (feature-ref:3) -> `.specify/features/045-sanitize-command.md`; `.specify/memory/glossary.md` (requirements:8) -> `.specify/glossary.md`.

**Verdict: BROKEN** — code, guards, registry and docs resolve, but 14 artifact references still name the pre-move repo-root hook and the contract's import surface is stale.

## 057-decompose-command-skills

**Artifacts read**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `contracts/run-skills-wiring.md`, `contracts/run-team-parity.md`, `notes/red-first-evidence.md`, `notes/pre-change-measurements.md`, `notes/quickstart-run.md`, `checklists/requirements.md`.

**Census**: 62 refs — alive 54 / archived 0 / dead 1 / moved-by-rename 3. Excluded 4 prose/brace fragments (`agents/team/skills` is the prose phrase "跨 agents/team/skills"; the three `{...}` items are brace expansions).

**Broken list**

- `.specify/specs/057-decompose-command-skills/contracts/run-team-parity.md:11` -> `.specify/goal/<goal-slug>/summary/` **missing**. The goal archive was renamed `.specify/goal/` -> `.specify/anchoring/` (`shared/definitions/goal-definitions.md:179`); the live summary directory is `.specify/anchoring/<goal-slug>/summary/`. The same stale path is still present in the live skill source `skills/internal/create-team/SKILL.md:197` and its mirror `.specify/skills/internal/create-team/SKILL.md:197`.
- `.specify/teams/.work/<slug>/` (contracts/run-team-parity.md:15) is **runtime-created and git-ignored** by `.specify/.gitignore:9`; it is counted alive-by-design, not dead.

**Registry**: Feature 057 row resolves cleanly — `.specify/features.md:65` -> Spec Path `.specify/specs/057-decompose-command-skills/requirements.md`, Feature Details `.specify/features/057-decompose-command-skills.md` (exists, correct content).

**Guards**: `tests/contract/test_run_skills_wiring.py` present with C-2…C-12; C-1 (run-skills mirror parity) and C-7 (run-team mirror parity) are folded into `tests/contract/test_mirror_parity_suite.py`, which parametrizes the `MIRROR_PAIRS` set and therefore covers both new internal skills generically. No missing guards.

**Spot checks** (3/3 hold)

1. `skills/internal/run-skills/SKILL.md` and `skills/internal/run-team/SKILL.md` exist; both `.specify/skills/internal/...` mirrors are byte-identical; both carry `classification: internal` and the correct `skill_id`.
2. `templates/commands/team.md` run row (line 35), routing step (44), ambiguity listing (69) and `### Run Mode` (79-81) all point at `run-team`; the Run Mode section is a routing pointer, not a procedure.
3. `templates/commands/skills.md` carries the 5-row Delegation table and pins the invocation grammar `run-skills <名称|路径>` at line 58. Holds.

**Rename-moved**: `.specify/memory/constitution.md` (plan:27) -> `.specify/constitution.md`; `.specify/memory/features.md` (tasks:5) -> `.specify/features.md`; `.specify/memory/features/057.md` (feature-ref:4) -> `.specify/features/057-decompose-command-skills.md`.

**Verdict: BROKEN** — all implementation surfaces and guards hold; one contract path predates the goal-archive rename and the same drift exists in the live create-team skill.

## 069-execution-expression-sdd

**Artifacts read**: `requirements.md`, `notes/decomposition-gate.md`, `checklists/requirements.md` (auxiliary). The spec has no plan/tasks of its own — it was split into 069a/069b, both archived.

**Census**: 33 refs — alive 27 / archived 3 / dead 0 / moved-by-rename 1. Ephemeral 1 (`test-evidence/log-requirements-validate.log`, declared in the checklist as a git-ignored local evidence pointer); excluded 1 brace fragment (`skills/{internal`).

**Broken list**: none. The three archived refs are the split-slice paths, correctly retrievable under `.specify/archive/specs/069b-isomorphism-migration-metrics/`: the directory, `requirements.md`, and `notes/parent-fr-mapping.md`. These are classified archived-elsewhere, not dead.

**Registry**: Feature 069 row resolves cleanly — `.specify/features.md:78` -> Spec Path `.specify/specs/069-execution-expression-sdd/requirements.md`, Feature Details `.specify/features/069-execution-expression-sdd.md` (exists, correct content; records 069a/069b both Implemented).

**Guards**: `tests/contract/test_flow_class_ledger.py`, `test_flow_class_correctness.py`, `test_flow_class_spec_declaration.py`, `test_expression_gates_doc.py`, `test_expression_gate_wiring.py`, `test_expression_faces.py`, and `tests/unit/test_flow_class_check.py` all present. No missing guards.

**Spot checks** (3/3 hold)

1. `shared/definitions/flow-class-definitions.md` and its `.specify/shared/` mirror exist and declare sole ownership of criteria, values, ledger, neutral list, isomorphism map and boundaries; `tests/contract/test_flow_class_ledger.py:280` pins 83 rows (29 commands + 54 skills) and reconciles them bidirectionally. Note: the owner doc's dated line 13 still reads 79 rows (2026-10-30 reading) while the guard and inventory now measure 83 — a stale **dated** number, not a broken pointer.
2. `scripts/python/flow-class-check.py` (and its `.specify/scripts/` mirror) implements `check`, `lookup`, `isomorphism`, `delegation` and `faces`, with the default-class marker covered by `test_lookup_unregistered_unit_returns_default_with_marker`.
3. `shared/workflow/expression-gates.md` declares exactly six faces; `tests/contract/test_expression_gates_doc.py` pins the closed face count, one resolvable owner pointer per face, the eight-stage operator table and the blocking floor. Holds.

**Rename-moved**: `.specify/memory/glossary.md` (requirements:37) -> `.specify/glossary.md`.

**Verdict**: **INTACT** — owner docs, mirrors, engine, gates and guards all resolve; archived slice paths are retrievable in the archive.

## 079-bilingual-expression

**Artifacts read**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `research.md`, `contracts/owner-document.md`, `contracts/checker.md`, `contracts/distribution.md`, `contracts/measurement.md`, `notes/quickstart-run.md`, `notes/red-first-evidence.md`, `notes/plan-*.txt`, `checklists/requirements.md`.

**Census**: 99 refs — alive 88 / archived 0 / dead 0 / moved-by-rename 5. Ephemeral 2 (`.specify/.tmp/079-bilingual-expression/` and its `s4-pilot-t018` pilot root — a sanctioned temp root explicitly torn down and recorded). Excluded 4 (`shared/templates/scripts` is a prose triple; `templates/commands/**` and `tests/**` are scope-exclusion statements, not pointers; `tests/contract/test_<subject>.py` is a naming pattern).

**Broken list**: none.

**Registry**: Feature 079 row resolves cleanly — `.specify/features.md:88` -> Spec Path `.specify/specs/079-bilingual-expression/requirements.md`, Feature Details `.specify/features/079-bilingual-expression.md` (exists, correct content; status Ready for Review).

**Guards**: `tests/contract/test_bilingual_expression.py` present with 16 tests (owner-doc structure, scan/coverage/census actions, drift guards, deterministic sample); fixtures under `tests/fixtures/bilingual/` present. No missing guards.

**Spot checks** (3/3 hold)

1. Owner doc `shared/guidelines/bilingual-expression.md` (113 lines) and `.specify/shared/guidelines/bilingual-expression.md` are byte-identical.
2. Checker `scripts/python/bilingual-expression-check.py` and `.specify/scripts/python/bilingual-expression-check.py` are byte-identical; `--action` accepts exactly `scan | coverage | census` (line 556), matching contract C-001.
3. The ambient section `## Bilingual Expression (双语表述)` is present at `templates/instructions-template.md:83`, `.specify/instructions.md:95` and root `AGENTS.md:95`; the guard asserts the summary+pointer form and mirror identity. Holds.

**Rename-moved**: `.specify/memory/constitution.md` (plan:34) -> `.specify/constitution.md`; `.specify/memory/features.md` (tasks:6) -> `.specify/features.md`; `.specify/memory/features/079.md` (feature-ref:3) -> `.specify/features/079-bilingual-expression.md`; `.specify/memory/glossary.md` (quickstart:64) -> `.specify/glossary.md`; `.specify/memory/register.md` (tasks:221) -> `.specify/register.md`.

**Verdict**: **INTACT** — owner doc, checker, mirrors, ambient section, fixtures and 16-leg guard all resolve; only temp-root references are intentionally gone.

## 091-auto-git-closeout

**Artifacts read**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `research.md`, `contracts/closeout-lifecycle.contract.md`, `contracts/closeout-executor.contract.md`, `contracts/closeout-verification.contract.md`, `contracts/git-workflow-declaration.contract.md`, `notes/*`, `checklists/requirements.md`.

**Census**: 116 refs — alive 108 / archived 0 / dead 4 / moved-by-rename 2. Excluded 2 (`tests/fixtures/<feature>/` is a template placeholder; `tests/fixtures/git_closeout/{__init__,repo,plan,block}.py` is a brace expansion whose underscore directory exists).

**Broken list**

- `.specify/specs/091-auto-git-closeout/tasks.md:190` and `:224` -> `tests/fixtures/git-closeout/` **missing** (hyphen). The delivered fixture directory is `tests/fixtures/git_closeout/` (underscore), and T032's own evidence cell already spells it with the underscore. The same discrepancy was already recorded as P2 in `.specify/specs/091-auto-git-closeout/review.md:129` but the task text was not corrected.
- `.specify/specs/091-auto-git-closeout/verification.md:272` -> `tests/unit/test_compile_embeds.py` **missing**. The module lives at `tests/contract/test_compile_embeds.py`; no `tests/unit/` copy has ever existed in git history. The R-36a residual names the wrong path.
- `.specify/specs/091-auto-git-closeout/verification.md:163` -> `skills/analyze/SKILL.md` **missing**; the analyze skill is `skills/internal/analyze-artifacts/SKILL.md` (confirmed by `tests/contract/test_decision_tension_contract.py:48`). Dated implementation record; path was never at `skills/analyze`.
- `.specify/specs/091-auto-git-closeout/verification.md:257` -> `skills/external/humanize/SKILL.md` **missing**; the skill was renamed to `skills/external/humanize-conclusion/SKILL.md` in `dae8a9424`. Dated record; the rename postdates the implementation.
- Note: `.specify/memory/retention/closeout/` (tasks:32) and `.specify/memory/retention/receipts/<stamp>-<hash>.json` (research:95, plan:286) are **runtime-created** by the close-out step and `scripts/python/record-retention.py` respectively; they are counted alive-by-design, not dead.

**Registry**: Feature 091 row resolves cleanly — `.specify/features.md:100` -> Spec Path `.specify/specs/091-auto-git-closeout/requirements.md`, Feature Details `.specify/features/091-auto-git-closeout.md` (exists, correct content; status Completed).

**Guards**: `tests/contract/test_git_closeout_contract.py` present with 24+ named tests including every guard named in tasks (section placement, commit boundary, receipt pointer, report field set, three forks, four model sequences, short-lived-branch rules, read-only remote exclusion). No missing guards.

**Spot checks** (3/3 hold)

1. `.specify/workflow/git.md:24-25` declares both `Closeout` (closed four-value set: `commit+merge+push` / `commit+merge` / `commit-only` / `ask`) and `Closeout remotes` (`github`, `gitlab`, `gitee`; `origin` excluded by role).
2. `shared/workflow/artifact-commit-step.md:66` carries `## The ## Close-out step` and line 94 names the receipt directory `.specify/memory/retention/closeout/` with the one-file-per-run, timestamp-named, write-once shape; the guard asserts it at `test_git_closeout_contract.py:479`.
3. `skills/external/git-utils/references/closeout-commands.md` carries all four derived model sequences (single-branch, dual-branch, temp-branch, three-tier), and `tests/contract/test_git_closeout_contract.py` pins them (`test_the_reference_carries_all_four_derived_sequences`). Holds.

**Rename-moved**: `.specify/memory/constitution.md` (plan:61) -> `.specify/constitution.md`; `.specify/memory/features.md` (plan:67) -> `.specify/features.md`.

**Verdict: BROKEN** — declaration, owner, reference, guards and registry all hold; four artifact pointers are dead, two of them actionable (`tests/fixtures/git-closeout/` hyphen and `tests/unit/test_compile_embeds.py`) and two dated-record path names (`skills/analyze`, `skills/external/humanize`).

## Landed anchor-layout rename — references that moved

The rename merged mid-audit (`8b9030371` -> merge `6fb8093c4`). `.specify/memory/{features.md,features/,constitution.md,glossary.md,register.md,tools,tools.md}` no longer exist; the anchors now live at `.specify/{features.md,features/<NNN>-<slug>.md,constitution.md,glossary.md,register.md,tools.md,tools/}`. Every spec in this batch carries at least one such reference; they are listed per spec above and are not counted as defects because the rename is sanctioned. Two live-surface notes discovered while re-checking the post-rename tree:

- `scripts/python/bilingual-expression-check.py:58` and `scripts/python/glossary-utils.py:36` already read `.specify/glossary.md` — the code side of the rename landed correctly.
- `shared/definitions/flow-class-definitions.md` still points at `.specify/specs/069b-isomorphism-migration-metrics/contracts/ledger-reconciler.md` (pre-archive path); the target is retrievable at `.specify/archive/specs/069b-isomorphism-migration-metrics/contracts/ledger-reconciler.md`. The same pre-archive drift exists in the 069 notes and is counted as archived-elsewhere there.

**Anomaly**: the working tree changed underneath the audit — the anchor-layout merge `6fb8093c4` landed between the first and final census, so results are reported against the post-merge tree; and the merge's feature-detail filename mapping is wrong for two of this batch's features — `.specify/features/032-dogfooding-practice.md` contains Feature 032 Task Complexity Rubric (the slug belongs to Feature 036) and `.specify/features/045-sanitize-command.md` contains Feature 045 Framework Source Provenance (no feature uses that slug). Both cells resolve, but the filenames misidentify their features.

SPEC-AUDIT-LIVE-5-DONE
