# Spec Audit — live batch 2 (7 specs)

Read-only audit of the seven live spec directories against the CURRENT tree. No spec or
source file was modified; this file is the only write.

**Audited tree**: `master` @ `6fb8093c4` (2026-11-10). The audit started at `564a5f5a6`;
mid-audit the anchor-layout merge **landed in master** (`6fb8093c4 merge(layout): move the
project anchors out of memory/ — .specify/{features,constitution,glossary,register,tools}.md`).
Counts below are against the post-rename tree; rename fallout is itemized per spec and is
**not** charged as a spec defect (every one of these specs predates the rename).

## Scope and counting rules

Artifacts read: `requirements.md`, `plan.md`, `tasks.md`, `contracts/*`, `data-model.md`,
`quickstart.md`, `research.md`, `verification.md`, `checklists/*`, `notes/*` (incl. `notes/*.txt`),
`feature-ref.md`, `review.md` / `code-review*.md`. Excluded: `test-evidence/`, `fixtures/`, and
top-level dated `.txt` baselines (`*-failed.txt`, `coverage-baseline.txt`) — dated run records,
not live pointers.

Counting unit: distinct repository path reference (glob/placeholder forms counted once and
classified `glob`). Classification:

- **alive** — the stated path resolves in the live tree now.
- **archived-elsewhere** — no live target, but a preserved copy exists under `.specify/archive/`
  (verified by matching the artifact's own directory suffix, not just its basename).
- **dead** — no target at the stated path. Per the audit instruction, a pre-consolidation path,
  including a pre-rename `.specify/memory/...` anchor, counts as dead.
- **glob** — placeholder/ellipsis/pattern form not classified (`<name>`, `*`, `…`).

Verdict rule: **BROKEN** if any of (a) the bound registry row fails, (b) a named guard test is
missing, (c) a spot-check fails, or (d) a live normative pointer is dead for a reason other than
the anchor rename, a dated evidence record, an illustrative example, or the feature's own
intentionally deleted subject. **INTACT** otherwise.

## Batch summary

| Spec | Refs | Alive | Archived | Dead | Verdict |
|---|---|---|---|---|---|
| 006-add-qoder-support | 33 | 19 | 0 | 12 | **BROKEN** |
| 028-sdd-workflow-refactor | 68 | 40 | 0 | 18 | **BROKEN** |
| 040-agent-metadata-portability | 83 | 60 | 0 | 9 | **BROKEN** |
| 053-machine-decidable-artifacts | 215 | 150 | 0 | 53 | **BROKEN** |
| 065a-state-awareness | 87 | 64 | 0 | 16 | **BROKEN** |
| 076-decision-tension-contract | 217 | 202 | 0 | 5 | **INTACT** |
| 088-speckit-visualization | 327 | 300 | 2 | 10 | **BROKEN** |

(Each row also carries `glob` forms: 2 / 10 / 14 / 12 / 7 / 10 / 15 respectively; totals match.)

---

## 006-add-qoder-support

### Counts

| Class | Count |
|---|---|
| References total (distinct) | **33** |
| alive | **19** |
| archived-elsewhere | **0** |
| dead | **12** (9 missing named guard tests + 3 renamed anchors) |
| glob/placeholder | 2 |

### Registry

- Bound row is **Feature 020** at `.specify/features.md:29` (row 006 at `:15` is "Feature Command",
  Spec Path `-`, and does not bind this spec). Row 020 Spec Path
  `.specify/specs/006-add-qoder-support/requirements.md` **exists**; Feature Details cell
  `.specify/features/020-speckit-todo-command.md` **exists** and its content is "Qoder Support"
  (Feature ID 020). Resolution **passes path-wise**; the detail filename's slug belongs to another
  feature (see Anomaly).
- Row 006's own detail file `.specify/features/006-add-qoder-support.md` exists but contains
  "Feature Command" — the same slug/content inversion.

### Broken list (all mechanically dead references)

1. `tasks.md:40,122` -> `tests/unit/test_qoder_support_surfaces.py` missing (no file anywhere).
2. `tasks.md:53` -> `tests/unit/test_qoder_support_matrix.py` missing.
3. `tasks.md:68,186` -> `tests/contract/test_qoder_init_contract.py` missing.
4. `tasks.md:69,187` -> `tests/integration/test_qoder_init.py` missing.
5. `tasks.md:93` -> `tests/contract/test_qoder_refresh_contract.py` missing.
6. `tasks.md:94` -> `tests/integration/test_qoder_refresh.py` missing.
7. `tasks.md:95` -> `tests/unit/test_qoder_refresh_helpers.py` missing.
8. `tasks.md:120` -> `tests/contract/test_qoder_support_surfaces_contract.py` missing.
9. `tasks.md:121` -> `tests/integration/test_qoder_distribution.py` missing.
10. `plan.md:118,168; research.md:18; tasks.md:50` -> `.specify/memory/constitution.md` moved to `.specify/constitution.md` (rename).
11. `plan.md:118; tasks.md:146` -> `.specify/memory/features.md` moved to `.specify/features.md` (rename).
12. `tasks.md:54` -> `.specify/memory/features/020.md` moved to `.specify/features/020-speckit-todo-command.md` (rename; slug/content inversion).

Items 1–9 are live guard-test claims, not rename fallout: none of the nine files exists anywhere
in the tree or under `.specify/archive/`.

### Guards

Named test files in `tasks.md`: 10; alive: 1; **missing: 9** (items 1–9 above).
The one named living guard is `tests/unit/test_qoder_bootstrap.py` (T011). Adjacent live Qoder
guard not named by this spec: `tests/contract/test_qoder_command_frontmatter.py`.

### Spot-checks (3)

1. **File/symbol** — `AGENT_CONFIG` qoder entry: **PASS**
   (`src/specify_cli/__init__.py:89`; `generate_commands` `:1588`, `copy_local_templates` `:2218`).
2. **Behaviour surface** — `scripts/bash/generate-instructions.sh:413-434` writes
   `.qoder/project_rules.md` and links `QODER.md`: **PASS** (live `.qoder/project_rules.md` present).
3. **Docs/template surface** — `docs/tutorials/installation.md:36` (qoder init example) and
   `templates/instructions-template.md:263` (Qoder in supported agents): **PASS**.

### Completion-record note

`tasks.md` still carries four unchecked manual-QA rows — T012 `:74`, T018 `:99`, T026 `:126`,
T033 `:145` — while registry row 020 reads **Implemented**. Recorded as a finding, not counted
as a dead path.

### Verdict

**BROKEN** — 9 of the 10 guard tests this spec names are missing; three anchor references moved
(benign). Registry row, 3/3 spot-checks and the Qoder implementation surface are otherwise sound.

---

## 028-sdd-workflow-refactor

### Counts

| Class | Count |
|---|---|
| References total (distinct) | **68** |
| alive | **40** |
| archived-elsewhere | **0** |
| dead | **18** (2 renamed anchors, 6 stale doc pointers, 8 intentional old-layout/deletion-subject refs, 2 placeholder examples) |
| glob/placeholder | 10 |

### Registry

Bound row is **Feature 029** at `.specify/features.md:38` ("Shared Reference Directory").
Spec Path `.specify/specs/028-sdd-workflow-refactor/requirements.md` **exists**; Feature Details
cell `.specify/features/029-glossary-mechanism.md` **exists** and contains "Shared Reference
Directory". Resolution passes; the detail filename's slug belongs to another feature (Anomaly).

### Broken list (all mechanically dead references)

1. `plan.md:27` -> `.specify/memory/constitution.md` moved to `.specify/constitution.md` (rename).
2. `tasks.md:161` -> `.specify/memory/features/029.md` moved to `.specify/features/029-glossary-mechanism.md` (rename; slug/content inversion).
3. `zero-reference-gate.contract.md:24; quickstart.md:64; tasks.md:159; verification.md:28` -> `docs/history` missing; history now lives at `docs/reference/history/` (stale gate exclusion).
4. `zero-reference-gate.contract.md:17; data-model.md:93; requirements.md:58,89` -> `docs/history/` same move.
5. `quickstart.md:65` -> `docs/summary/03-sdd-workflow-refactor-proposal.md` missing; actual file is `docs/archive/03-sdd-workflow-refactor-proposal.md` (tasks.md:159 uses the correct path).
6. `plan.md:72` -> `docs/agents/`, `docs/commands/`, `docs/skills/` missing (docs tree restructured before this audit).
7. `contracts/skill-removal.contract.md:27; quickstart.md:12; tasks.md:102` -> `skills/sdd-workflow` missing — **intentional deletion subject** of this feature (safe to stay dead).
8. `contracts/skill-removal.contract.md:11; data-model.md:19,76; plan.md:66,75,89; requirements.md:54` -> `skills/sdd-workflow/` same.
9. `contracts/reference-rewrite.contract.md:29; data-model.md:28; plan.md:65; requirements.md:46,98` -> `skills/sdd-workflow/references/` same.
10. `quickstart.md:21` -> `skills/sdd-workflow/references/user-input-protocol.md` same (historical comparison via `git show HEAD~`).
11. `contracts/skill-removal.contract.md:28; tasks.md:98` -> `.specify/skills/sdd-workflow` same.
12. `plan.md:87; requirements.md:64` -> `.specify/skills/sdd-workflow/` same.
13. `contracts/reference-rewrite.contract.md:30` -> `.specify/skills/sdd-workflow/references/` same.
14. `plan.md:93` -> `skills/commands` missing (pre-layout skills tree; no such dir).
15. `contracts/path-rewrite.contract.md:32,36; tasks.md:73` -> `.specify/shared/workflow/x.md` and
    `shared/workflow/x.md` are contract placeholder examples (`x.md`), not artifacts.

Items 6–14 are either the feature's own deletion subject or pre-layout descriptions; only items
3–5 are stale live pointers.

### Stale success-criterion claim

`requirements.md:123` (**SC-003**) says all ten previously shipped reference documents "exist at
`.specify/shared/workflow`". Currently only 4 of the 10 remain there (`user-input-protocol.md`,
`feature-integration.md`, `agent-configuration.md`, `feedback-step.md`). The other six moved:
`checklist-methodology.md`, `requirements-guidelines.md` -> `shared/guidelines/`;
`dfx-catalog.md`, `clarify-taxonomy.md`, `ignore-patterns.md` -> `shared/constants/`;
`tool-definitions.md` -> `shared/definitions/`. `.specify/shared/workflow` now holds 20 documents.

### Guards

Named contract/integration/unit tests: **6/6 alive** —
`tests/unit/test_rewrite_paths_shared.py`, `tests/contract/test_shared_reference_directory.py`,
`tests/integration/test_shared_dir_install.py`, `tests/contract/test_sdd_workflow_removed.py`,
`tests/contract/test_shared_reference_rewrite.py`,
`tests/integration/test_zero_sdd_workflow_references.py`.

### Spot-checks (3)

1. **Symbol** — `rewrite_paths()` handles the `shared` segment: **PASS**
   (`src/specify_cli/__init__.py:1554,1568`).
2. **Behaviour** — init copies `shared/` into `.specify/shared`: **PASS**
   (`src/specify_cli/__init__.py:2520-2532`; packaging force-include `pyproject.toml:47`).
3. **Claim** — "all ten docs at `.specify/shared/workflow`": **FAIL** (six relocated as above).

### Verdict

**BROKEN** — every named guard and the rewrite/install mechanism are intact, but two stale live
pointers (`docs/history`, `docs/summary/03-…`) and the SC-003 ten-document claim no longer match
the tree.

---

## 040-agent-metadata-portability

### Counts

| Class | Count |
|---|---|
| References total (distinct) | **83** |
| alive | **60** |
| archived-elsewhere | **0** |
| dead | **9** (1 missing test, 1 intentional rename, 4 renamed anchors, 3 prose enumerations) |
| glob/placeholder | 14 |

### Registry

Bound row is **Feature 044** at `.specify/features.md:53` ("Agent Metadata Portability").
Spec Path `.specify/specs/040-agent-metadata-portability/requirements.md` **exists**; Feature
Details cell `.specify/features/044-reduce-confirmation-flows.md` **exists** and contains
"Agent Metadata Portability". Resolution passes; detail slug/content inversion applies (Anomaly).

### Broken list (all mechanically dead references)

1. `verification.md:34` (also `tasks.md:119`) -> `tests/integration/test_context_injection.py`
   missing; class `TestRoleSpecificContext` exists nowhere in `tests/` (missing named guard).
2. `tasks.md:97` -> `tests/contract/test_agents_symlink.py` retired **by design** (T021 renames it);
   replacement `tests/contract/test_agent_render_migration.py` is alive.
3. `plan.md:41` -> `.specify/memory/constitution.md` -> `.specify/constitution.md` (rename).
4. `requirements.md:32` -> `.specify/memory/features.md` -> `.specify/features.md` (rename).
5. `feature-ref.md:6; tasks.md:142` -> `.specify/memory/features/044.md` ->
   `.specify/features/044-reduce-confirmation-flows.md` (rename; slug/content inversion).
6. `contracts/relocation-taxonomy.md:45; plan.md:101; tasks.md:132` -> `.specify/memory/glossary.md`
   -> `.specify/glossary.md` (rename).
7. `tasks.md:45` -> `agents/templates/scripts/shared` is a prose enumeration ("touched pairs"),
   not a path.
8. `tasks.md:129` -> `shared/skills` prose label, not a path.
9. `requirements.md:34` -> `skills/commands` prose label (pre-layout skills wording), not a path.

`.specify/agents/.backups/` (`plan.md`) is a runtime-created backup directory, not a missing
artifact — noted, not counted dead.

### Guards

Named test files: 11; alive: 10; **missing: 1** (`tests/integration/test_context_injection.py`).
All ten others exist: `test_neutral_vocabulary_scan.py`, `test_tool_mapping.py`,
`test_neutral_metadata_schema.py`, `test_agent_render.py`, `test_agent_render_migration.py`,
`test_init_agents.py`, `test_shipped_agent_presets.py`, `test_role_templates.py`,
`test_agent_skill_enablement.py`, `test_persistent_agent_lifecycle.py`.

### Spot-checks (3)

1. **Symbol** — `_AGENT_METADATA_MAPPING`: **PASS** (`src/specify_cli/__init__.py:451`).
2. **Function** — `render_agents_for_tool()`: **PASS** (`:638`; called at `:2599,3376`).
3. **Retirement behaviour** — `ensure_per_file_agent_links()` / `_AGENT_LINK_DIRS` are gone
   (retired as specified); `.specify/agents/.render-manifest.json` exists: **PASS**.

### Verdict

**BROKEN** — one named integration test is missing; the renderer, mapping and manifest are intact.

---

## 053-machine-decidable-artifacts

### Counts

| Class | Count |
|---|---|
| References total (distinct) | **215** |
| alive | **150** |
| archived-elsewhere | **0** |
| dead | **53** (5 renamed anchors; 3 moved-goal pointers; 1 docs build path; 23 dated skill-layout records; 21 illustrative/placeholder/dated-record forms) |
| glob/placeholder | 12 |

### Registry

Bound row is **Feature 053** at `.specify/features.md:62`. Spec Path
`.specify/specs/053-machine-decidable-artifacts/requirements.md` **exists**; Feature Details
`.specify/features/053-machine-decidable-artifacts.md` **exists** and matches. **PASS** (also one
of the few detail files whose slug and content agree).

### Broken list (all mechanically dead references)

Renamed anchors (post-merge):

1. `contracts/clause-coverage.md:78; plan.md:49; research.md:188` -> `.specify/memory/constitution.md` -> `.specify/constitution.md`.
2. `feature-ref.md:14; plan.md:54; research.md:321` -> `.specify/memory/features.md` -> `.specify/features.md`.
3. `feature-ref.md:13` -> `.specify/memory/features/040.md` -> `.specify/features/040-agent-metadata-portability.md`.
4. `requirements.md:94,99; feature-ref.md:15,153,157; plan.md:54,65` -> `.specify/memory/features/053.md` -> `.specify/features/053-machine-decidable-artifacts.md`.
5. `checker-form.md:6; criterion-subject.md:35; green-point-claim.md:55; red-first-evidence.md:212; requirements.md:86,95,186,305` -> `.specify/memory/glossary.md` -> `.specify/glossary.md`.

Moved goal store (live quickstart commands):

6. `quickstart.md:42,280,307; notes/quickstart-run.md:97` -> `.specify/goal` missing; goal files now live under `.specify/anchoring/<goal>/` (goal registry is external in current runs).
7. `contracts/criterion-subject.md:41; contracts/run-checks.md:17,79; data-model.md:218,244; notes/quickstart-run.md:144; quickstart.md:52,312` -> `.specify/goal/` same move.
8. `quickstart.md:339; notes/quickstart-run.md:217` -> `.specify/goal/draw-two-layer-structure/goal.md` missing; live copy at `.specify/anchoring/draw-two-layer-structure/goal.md`.

Docs build output:

9. `quickstart.md:222; research.md:23` -> `docs/public` missing (site build output no longer produced in this tree).

Dated pre-consolidation skill layout (`notes/pre-change-measurements.md`, a dated measurement record):

10. `.specify/skills/archive-session/SKILL.md` `:91`
11. `.specify/skills/code-review/SKILL.md` `:92`
12. `.specify/skills/collect-evidence/SKILL.md` `:93`
13. `.specify/skills/create-team/references/operating-loops.md` `:96`
14. `.specify/skills/create-team/references/summary-mapping.md` `:97`
15. `.specify/skills/create-tools/SKILL.md` `:98` (now `skills/internal/create-tools/`)
16. `.specify/skills/draw-drawio/SKILL.md` `:101`
17. `.specify/skills/draw-excalidraw/SKILL.md` `:102`
18. `.specify/skills/draw-mermaid/SKILL.md` `:103`
19. `.specify/skills/draw-plantuml/SKILL.md` `:104`
20. `.specify/skills/git-fleet/SKILL.md` `:105`
21. `.specify/skills/git-server-init/SKILL.md` `:106`
22. `.specify/skills/git-submodule-edit/SKILL.md` `:107`
23. `.specify/skills/git-workflow/SKILL.md` `:108` (now `git-utils/`)
24. `.specify/skills/improve-agent/SKILL.md` `:109` (now `skills/internal/`)
25. `.specify/skills/improve-tools/SKILL.md` `:113` (now `skills/internal/`)
26. `.specify/skills/manage-agents/SKILL.md` `:114`
27. `.specify/skills/memory-recall/SKILL.md` `:115` (now `skills/internal/`)
28. `.specify/skills/memory-record/SKILL.md` `:116` (now `skills/internal/`)
29. `.specify/skills/study-project/SKILL.md` `:118` (now `study-code/`)
30. `.specify/skills/summarize-project/SKILL.md` `:119`
31. `.specify/skills/think-skills/SKILL.md` `:120; plan.md:180`
32. `notes/clarify-current-failed.txt:60` -> `skills/create-tools/SKILL.md` (same re-layer)

Illustrative / placeholder / dated-suite forms (not pointers):

33. `contracts/green-point-claim.md:66,67,71; quickstart.md:147,148,154,155,174; research.md:134,138; notes/quickstart-run.md:352; notes/red-first-evidence.md:225,232` -> `docs/a.md`, `docs/b.md` are example fixture paths in the synthetic task rows.
34. `notes/quickstart-run.md:198,203,208,226,227,240,241; verification.md:109` -> `skills/draw-*`, `skills/zzz-` are example/negative-test names, not artifacts.
35. `notes/red-first-evidence.md:213` -> `tests/contract/test_x.py` example path.
36. `contracts/neutrality-budget.md:16` -> `.specify/specs/053-` is an ellipsis form ("`053-…`"), not a path.
37. `feature-ref.md:98` -> `scripts/python/scan-confirmation-gat` is a regex-truncated fragment of `scripts/python/scan-confirmation-gates.py` (alive).
38. `feature-ref.md:66,67` -> `shared/guidelines/requirements-guidelines.m` / `shared/constants/clarify-taxonomy.m` are regex-truncated fragments of `.md` paths that are alive.
39. `tasks.md:105` -> `scripts/python/test` is the literal phrase "test… none", not a path.
40. `research.md:33` -> `templates/contracts-template.md` was a **rejected scheme**, never created.
41. `notes/clarify-current-failed.txt:10-19` -> `tests/contract/test_browser_site_exclusions.py`, `test_browser_site_memory.py` were dated red-baseline records; those suites were later removed with the browser-site consolidation.

### Guards

Named test files: **17/17 alive**, including the seven pinning suites
(`test_clause_forms.py`, `test_checker_form.py`, `test_requirements_checker.py`,
`test_green_point_claim.py`, `test_clause_coverage.py`, `test_run_checks.py`,
`test_criterion_subject.py`, `test_neutrality_budget.py`), the amended
`test_validate_tasks_parallel_safety.py` and `test_clarify_semantic_completeness.py`, plus
`test_goal_definition.py`, `test_goal_migration.py`, `test_goal_targets_engine.py`,
`test_goal_targets_check.py`, `test_trigger_engine.py`, `test_scripts_distribution_parity.py`,
`test_focus_target_resolution.py`, and `tests/unit/test_goal_utils.py`.

### Spot-checks (3)

1. **Symbol** — `scripts/python/clause_extract.py`: `extract_clauses()` `:288`,
   `resolvable()` `:323`: **PASS**.
2. **Command** — `scripts/python/goal-utils.py run-checks`: **PASS**
   (help `:23`, implementation `:1449`, subparser `:2690`).
3. **Template surface** — `templates/tasks-template.md:110` defines the
   `[green: <contract>#<clause>]` attribution tag with the four verdict labels: **PASS**.

### Verdict

**BROKEN** — all 17 named guards and all three spot-checks pass, but live quickstart commands
still target the moved `.specify/goal/` store and a retired `docs/public` path; the remaining
dead set is dated records, examples, or rename fallout.

---

## 065a-state-awareness

### Counts

| Class | Count |
|---|---|
| References total (distinct) | **87** |
| alive | **64** |
| archived-elsewhere | **0** |
| dead | **16** (4 renamed anchors, 1 stale entry path, 1 retired agent name, 1 archived-prefix form, 6 illustrative demo paths, 3 prose fragments) |
| glob/placeholder | 7 |

### Registry

There is **no registry row that names `.specify/specs/065a-state-awareness`**. The parent row is
**Feature 065** at `.specify/features.md:74`; its Spec Path
`.specify/specs/065-loop-interruption-recovery/requirements.md` exists, and its detail file
`.specify/features/065-loop-interruption-recovery.md` names the slice `065a-state-awareness`
14 times. So the slice is registered **by reference to the parent feature**, not by its own row.
Recorded as a registry-binding caveat: a lookup keyed on the slice directory finds no row.

### Broken list (all mechanically dead references)

1. `plan.md:27; notes/state-spine.md:7` -> `.specify/memory/constitution.md` -> `.specify/constitution.md` (rename).
2. `tasks.md:64` -> `.specify/memory/features` (dir) -> `.specify/features/` (rename).
3. `feature-ref.md:6,60; requirements.md:15; review.md:21` -> `.specify/memory/features.md` -> `.specify/features.md` (rename).
4. `feature-ref.md:6,61; notes/state-spine.md:7; requirements.md:15,57; review.md:21` -> `.specify/memory/features/065.md` -> `.specify/features/065-loop-interruption-recovery.md` (rename).
5. `plan.md:103` -> `scripts/loop-state.py` (inside a project tree diagram) missing; the actual engine is
   `skills/external/sdd-loop-driver/scripts/loop-state.py` (mirror `.specify/skills/sdd-loop-driver/scripts/loop-state.py`).
6. `notes/state-spine.md:18` -> `agents/sdd-executor.agent.md` missing; the current executor roster
   uses `agents/sdd-implement-executor.agent.md` (plus the other `sdd-*` seats).
7. `verification.md:75` -> `.specify/specs/066-` prefix no longer matches a live directory; the 066 slice
   is archived at `.specify/archive/specs/066-loop-state-awareness-a/`.
8. `contracts/snapshot-envelope.md:227-232` -> `.specify/specs/demo/{plan,data-model,quickstart,research,feature-ref}.md`
   and `.specify/specs/demo/contracts/` are illustrative demo-spec paths in the envelope example; no target.
9. `notes/state-spine.md:19,21,23` -> `docs/mirror/verification/gates` and `docs/SKILL` are compressed prose
   fragments ("docs/SKILL contract assertions"), not paths.
10. `requirements.md:154; feature-ref.md:46` -> `feedback/probe` names the existing probe mechanism, not a path.

### Guards

Named test files: **5/5 alive** — `tests/unit/test_loop_state_engine.py`,
`tests/contract/test_loop_state_contract.py`, `tests/unit/test_line_registry_engine.py`,
`tests/unit/test_pre_analyze_check.py`, `tests/contract/test_sdd_loop_driver_skill.py`.
Note: this slice shipped under an explicit test waiver (`verification.md` § Test waiver); the
guards exist but their green state was never claimed.

### Spot-checks (3)

1. **Entry file / behaviour** — `skills/external/sdd-loop-driver/scripts/loop-state.py` exists;
   implements `snapshot`, `--probe`, `--self-test`, and returns structured refusals for
   `recover`/`check-spine` (owned by 065b/065c): **PASS** (`:3-10, :61-62`).
2. **Data owner** — `STAGE_ARTIFACTS` at `loop-state.py:211` and
   `skills/external/sdd-loop-driver/references/state-awareness.md` both exist: **PASS**.
3. **Guard files** — `tests/unit/test_loop_state_engine.py` and
   `tests/contract/test_loop_state_contract.py` exist: **PASS**.

### Verdict

**BROKEN** — the slice has no registry row of its own (parent-bound only), and `plan.md:103`
points at a non-existent `scripts/loop-state.py`; the engine, its data owner and its named tests
are intact.

---

## 076-decision-tension-contract

### Counts

| Class | Count |
|---|---|
| References total (distinct) | **217** |
| alive | **202** |
| archived-elsewhere | **0** |
| dead | **5** (4 renamed anchors + 1 illustrative defect path) |
| glob/placeholder | 10 |

### Registry

Bound row is **Feature 076** at `.specify/features.md:85`. Spec Path
`.specify/specs/076-decision-tension-contract/requirements.md` **exists**; Feature Details
`.specify/features/076-decision-tension-contract.md` **exists** and matches. **PASS**.

### Broken list (all mechanically dead references)

1. `plan.md:41` -> `.specify/memory/constitution.md` -> `.specify/constitution.md` (rename).
2. `plan.md:231; review.md:132; tasks.md:6,269; code-review.md:22,281; code-review-20261029T125405Z.md:22,308` -> `.specify/memory/features.md` -> `.specify/features.md` (rename).
3. `plan.md:229,231,275; requirements.md:42; review.md:132; code-review.md:23,284; code-review-20261029T125405Z.md:23,311` -> `.specify/memory/features/076.md` -> `.specify/features/076-decision-tension-contract.md` (rename).
4. `review.md:319` -> `.specify/memory/register.md` -> `.specify/register.md` (rename).
5. `code-review-20261029T125405Z.md:189` -> `.specify/specs/shared/guidelines/decision-tension.md`
   is quoted **as a counter-example** ("no such file") inside a review finding about the plan
   template's relative pointer; it is not a spec reference.

No non-rename dead pointer exists.

### Guards

Named test files: **3/3 alive** — `tests/contract/test_decision_tension_contract.py`,
`tests/contract/test_decision_tension_validator.py`,
`tests/contract/test_falsification_quartet_validator.py`.
Validators: `scripts/python/validate-decision-tensions.py` and
`scripts/python/validate-falsification-quartet.py` both exist.

### Spot-checks (3)

1. **Validators** — both deterministic checkers exist and the contract names match: **PASS**.
2. **Template anchor** — `templates/plan-template.md:64` contains `## Decision Tensions`: **PASS**.
3. **Analyze channel** — `skills/internal/analyze-artifacts/references/detection-and-severity.md:87`
   defines `### I. Decision Tension records` (with severity table at `:107`): **PASS**.

### Verdict

**INTACT** — every non-rename reference resolves, all three named guards exist, and all three
implementation spot-checks pass. Only the post-rename anchors are dead at their stated paths.

---

## 088-speckit-visualization

### Counts

| Class | Count |
|---|---|
| References total (distinct) | **327** |
| alive | **300** |
| archived-elsewhere | **2** (goal/team snapshots preserved under `.specify/archive/goal-team/trees/088-speckit-visualization/`) |
| dead | **10** (5 renamed anchors, 1 missing evidence log, 2 retired/relative-script forms, 1 forbidden-write glob, 1 retired mirror) |
| glob/placeholder | 15 |

### Registry

Bound row is **Feature 088** at `.specify/features.md:96`. Feature Details
`.specify/features/088-speckit-visualization.md` **exists** and matches. The Spec Path cell is
**polluted**: it contains the path followed by a changelog trail
(`.specify/specs/088-speckit-visualization/requirements.md ; 2026-11-06 …`). The leading path
exists, so resolution passes, but the cell is no longer a pure path.

### Broken list (all mechanically dead references)

1. `plan.md:104` -> `.specify/memory/constitution.md` -> `.specify/constitution.md` (rename).
2. `checkpoints/02-clarify.md:7; code-review.md:44,316; feature-ref.md:11; review.md:144,216; review-second-slice.md:101,110` -> `.specify/memory/features.md` -> `.specify/features.md` (rename).
3. `checkpoints/02-clarify.md:7; code-review.md:45,318; feature-ref.md:12; review.md:62,144,216,220` -> `.specify/memory/features/088.md` -> `.specify/features/088-speckit-visualization.md` (rename).
4. `code-review.md:47,322; tasks.md:50` -> `.specify/memory/glossary.md` -> `.specify/glossary.md` (rename).
5. `code-review.md:48,324` -> `.specify/memory/register.md` -> `.specify/register.md` (rename).
6. `verification.md:15` -> `.specify/specs/088-speckit-visualization/test-evidence/baseline-full-suite-20261106T063158Z.log`
   **missing**; `test-evidence/` holds 106 files but none with that name or a `baseline-full-suite` prefix.
   The baseline reading (7473 passed / 27 failed / 1 skipped) survives only as an inline quote.
7. `team/team.md:30` -> `.specify/goal/**` is the team's **forbidden-write glob**, not a live path;
   goal storage now lives under `.specify/anchoring/`.
8. `requirements.md:37; feature-ref.md:33; plan.md:402` -> `.specify/templates/commands/` is explicitly
   documented as a **retired mirror** ("NO `.specify/templates/commands/` mirror — that pair is retired").
9. `plan.md:338` -> `scripts/validate-roster.py` is a relative shorthand inside the `skills/internal/create-team/`
   tree row; actual file `skills/internal/create-team/scripts/validate-roster.py` exists.
10. `plan.md:466` -> `scripts/verify-territory-disjoint.py` same relative shorthand; actual file
    `skills/internal/create-team/scripts/verify-territory-disjoint.py` exists.

Archived-elsewhere: `.specify/specs/088-speckit-visualization/goal/088-speckit-visualization/goal.md`
(`checkpoints/01-requirements.md:12; code-review.md:404`) and
`.specify/specs/088-speckit-visualization/team/088-reporting-dogfood/team.md`
(`verification.md:114`) are preserved under `.specify/archive/goal-team/trees/088-speckit-visualization/`.

### Guards

Named contract/unit tests: **13/13 alive** —
`test_reporting_obligations.py`, `test_roster_reporter_seat.py`, `test_status_digest.py`,
`test_coaching_reporting_duty.py`, `test_coaching_dispatch_contract.py`,
`test_coaching_wiring_contract.py`, `test_fast_fail_discipline.py`, `test_progress_reporting.py`,
`test_measure.py`, `test_efficiency_element.py`, `test_exec_quant_engine.py`,
`test_status_digest_unit.py`, `test_measure_unit.py`.

### Spot-checks (3)

1. **Engine** — `scripts/python/measure.py` exists with `--action {summary,json}`, `--since`,
   `--window`, `--unit` (`:459-464`): **PASS**.
2. **Command surface** — `templates/commands/measure.md` plus all four per-tool copies exist
   (`.claude/commands/speckit.measure.md`, `.qoder/commands/speckit.measure.md`,
   `.github/prompts/speckit.measure.prompt.md`, `.opencode/command/speckit.measure.md`): **PASS**.
3. **Reporter seat / roster guard** — `agents/reporter.agent.md`, its mirror
   `.specify/agents/templates/reporter.agent.md`, `shared/guidelines/reporting-obligations.md`,
   `skills/internal/create-team/scripts/validate-roster.py` and `test_roster_reporter_seat.py`
   all exist: **PASS**.

### Verdict

**BROKEN** — implementation, guards and command surfaces are sound, but the baseline full-suite
evidence log cited by `verification.md:15` is missing, and the registry Spec Path cell is polluted
with changelog text.

---

## Anchor-layout rename (landed mid-audit)

At audit start the rename was pending on branch `rename-anchors`; it merged into `master` as
`6fb8093c4` while this audit was running. The live anchors are now:

| Old | New |
|---|---|
| `.specify/memory/constitution.md` | `.specify/constitution.md` |
| `.specify/memory/features.md` | `.specify/features.md` |
| `.specify/memory/features/<ID>.md` | `.specify/features/<ID>-<slug>.md` |
| `.specify/memory/glossary.md` | `.specify/glossary.md` |
| `.specify/memory/register.md` | `.specify/register.md` |
| `.specify/memory/history/` | `.specify/history/` |

References that moved (now dead at the stated path) in this batch:

| Spec | Moved refs | Anchors |
|---|---|---|
| 006 | constitution, features.md, features/020.md | plan.md:118,168; research.md:18; tasks.md:50,54,146 |
| 028 | constitution, features/029.md | plan.md:27; tasks.md:161 |
| 040 | constitution, features.md, features/044.md, glossary.md | plan.md:41,101; requirements.md:32; feature-ref.md:6; tasks.md:132,142; contracts/relocation-taxonomy.md:45 |
| 053 | constitution, features.md, features/040.md, features/053.md, glossary.md | plan.md:49,54,65; requirements.md:86,94,95,99,186,305; feature-ref.md:13-15,153,157; research.md:188,321; contracts/clause-coverage.md:78; contracts/checker-form.md:6; contracts/criterion-subject.md:35; contracts/green-point-claim.md:55; notes/red-first-evidence.md:212 |
| 065a | constitution, features/, features.md, features/065.md | plan.md:27; tasks.md:64; feature-ref.md:6,60,61; requirements.md:15,57; review.md:21; notes/state-spine.md:7 |
| 076 | constitution, features.md, features/076.md, register.md | plan.md:41,229,231,275; requirements.md:42; tasks.md:6,269; review.md:132,319; code-review.md:22,23,281,284; code-review-20261029T125405Z.md:22,23,308,311 |
| 088 | constitution, features.md, features/088.md, glossary.md, register.md | plan.md:104; tasks.md:50; feature-ref.md:11,12; code-review.md:44,45,47,48,316,318,322,324; review.md:62,144,216,220; review-second-slice.md:101,110; checkpoints/02-clarify.md:7 |

Separately, goal storage left `.specify/goal/` for `.specify/anchoring/` (affects 053 quickstart
scenarios and 088's `team.md` forbidden-write glob).

## Anomaly

**Anomaly**: the anchor-layout merge (`6fb8093c4`) landed in `master` during this audit, converting every `.specify/memory/*` reference in the batch from "pending move" to dead-at-stated-path, and the merge left **47 of 89 Latin-named feature-detail files with a filename slug that does not match their own content** (e.g. `.specify/features/020-speckit-todo-command.md` contains "Qoder Support", `.specify/features/029-glossary-mechanism.md` contains "Shared Reference Directory", `.specify/features/044-reduce-confirmation-flows.md` contains "Agent Metadata Portability"); additionally `006-add-qoder-support/tasks.md` keeps four unchecked manual-QA rows while its bound registry row 020 reads Implemented.

SPEC-AUDIT-LIVE-2-DONE
