# Read-only live-spec audit — batch 1 (7 specs)

**Date**: 2026-11-10
**Repo**: `/storage/project/cloud-native-ai/spec-kit` (branch `master`)
**Basis**: HEAD `6fb8093c4` — `merge(layout): move the project anchors out of memory/`. The anchor-layout rename was *pending on branch `rename-anchors` when this audit started* (HEAD `564a5f5a6`) and **merged mid-audit**; see § Anchor-layout rename and the Anomaly line.
**Scope**: `.specify/specs/{001,027,039,052,065,075,087}/*` — every `.md` artifact in each spec directory (requirements, plan, tasks, contracts, data-model, quickstart, verification, research, feature-ref, review, code-review, checklists, notes, test-evidence, checkpoints, state-spine, baseline evidence).
**Read-only**: no spec or source file was modified; this file is the only write. No subagents, no commits, no test executions (guard liveness is judged by file presence and source inspection, not by running pytest).

## Method

1. Every unique path token beginning `.specify/`, `scripts/`, `skills/`, `templates/`, `shared/`, `tests/` was extracted per spec (glob and brace forms expanded; `path:line` suffixes and `#anchors` normalized).
2. Classification against the current tree: **alive** = target exists now; **archived-elsewhere** = target exists only under `.specify/archive/`; **dead** = no target. Per the 090 `orphan-path` definition (`contracts/nd-detection-categories.contract.md:48`), a referenced path that does not exist is red.
3. Tokens that are not path references were excluded from counts and are named where relevant: prose compounds ("scripts/CLI tools", "scripts/contracts only"), ellipsis prose (`.specify/specs/087-…`), pytest node ids that resolve through a parametrized test table, `mktemp` templates (`XXXXXX`), and `<placeholder>/**` patterns rooted in a live directory.
4. **Anchor-move refs** (`.specify/memory/{constitution.md,features.md,features/<ID>.md,glossary.md,register.md,tools.md}`) were alive at audit start. They are counted as dead against the current HEAD but flagged `[anchor-move]` and are not, by themselves, treated as owner defects — the rename batch owns their sweep.
5. Registry check: row whose Spec Path cell names the spec directory; Feature Details cell must exist and match `.specify/features/<ID>-<slug>.md` (post-rename) / `.specify/memory/features/<ID>.md` (pre-rename). Note: the registry's numeric row ID is *not* always the spec directory number (offset rows 028→027, 043→039, plus the 027/036 pairing).
6. Guards: every `tests/…` file named by the artifacts, checked for existence; missing ones listed.
7. Spot-checks: one file, one symbol-or-command and one behaviour surface per spec against the current tree.

## Anchor-layout rename (`memory/` → `.specify/` root)

Landed as `6fb8093c4` during this audit: `.specify/memory/constitution.md` → `.specify/constitution.md`; `.specify/memory/features.md` → `.specify/features.md`; `.specify/memory/features/<ID>.md` → `.specify/features/<ID>-<slug>.md`; `glossary.md`, `register.md`, `tools.md` likewise. Every spec in this batch references at least one old anchor except 001. These are listed per spec as `[anchor-move]` with the new path. Note a defect introduced by the rename itself: the detail-file slugs were taken from the *spec directory of the same number*, not from the feature's own slug, so rows 027 (Team Management) and 039 (Harvested Harness Improvements) now point at files named `027-feedback-mechanism.md` / `039-session-export.md`, and rows 028 (Feedback Mechanism) / 043 (Session Export) at `028-sdd-workflow-refactor.md` / `043-init-commit-stamp.md` — the cells exist but the slugs misname the content.

---

## 001-unify-command-handoffs

**Refs**: 5 unique → **alive 5**, archived 0, dead 0. (Contains 1 placeholder: `.specify/specs/[###-spec]` under the live `.specify/specs/`; not an anchor-move ref.)
**Broken**: none.
**Guards**: none named — the spec's checks are content claims (Handoffs sections / frontmatter), not test files.
**Registry**: row `001` → Spec Path `.specify/specs/001-unify-command-handoffs/requirements.md` (exists); Feature Details `.specify/features/001-unify-command-handoffs.md` (exists, content matches). **Resolves.**
**Spot-checks**:
- File: `templates/commands/plan.md` exists; `templates/commands/implement.md` exists.
- Symbol/command: `handoffs:` YAML frontmatter key present in `templates/commands/plan.md:4` (20/29 command templates carry it now).
- Behaviour surface: `## Handoffs` present in **27/29** templates (`measure.md`, `status.md` lack it — both added later by 087); `implement.md:77,79` still names `/speckit.tasks` (Before) and `/speckit.review` (After); quickstart chain present (`docs/tutorials/quickstart.md:139`). The registry note's "23 command templates" is a stale count, not a broken path.
**Verdict**: **INTACT**

## 027-feedback-mechanism

**Refs**: 84 unique after excluding 2 prose compounds (`scripts/CLI` at `data-model.md:56`; `templates/skills/commands` at `plan.md:15`) → **alive 74**, archived 0, dead 10 (3 `[anchor-move]`, 7 other).
**Broken**:
- `.specify/docs/target-structure.md` — `contracts/command-classification.md:42` → no target; the docs declaration now lives at `docs/.speckit/target-structure.md` (not present in this repo).
- `.specify/goal/<goal-slug>/goal.md` — `contracts/command-classification.md:44` → archive root renamed: `.specify/anchoring/<goal-slug>/goal.md` (`shared/definitions/goal-definitions.md:179`; `goal-utils.py` `ARCHIVE_DIRNAME`).
- `.specify/memory/constitution.md` — `plan.md:29` → `[anchor-move]` `.specify/constitution.md`.
- `.specify/memory/features.md` — `checklists/requirements.md:36` → `[anchor-move]` `.specify/features.md`.
- `.specify/memory/features/028.md` — `checklists/requirements.md:36` → `[anchor-move]` `.specify/features/028-sdd-workflow-refactor.md` (exists; content is Feedback Mechanism, slug names another feature).
- `.specify/memory/feedback/*-skill-analysis-project.md` — `quickstart.md:27` → glob matches 0 entries; store `.specify/memory/feedback/` is live with differently-named entries.
- `.specify/memory/sanitize/cleanup-plan.json` — `contracts/command-classification.md:47` → directory absent; `sanitize-utils.py` still declares this as `PLAN_REL` (runtime store, never created here).
- `skills/*/SKILL.md` — `contracts/feedback-step-convention.md:40` → 0 matches: skills now sit at `skills/internal/<n>/` and `skills/external/<n>/` (54 SKILL.md files).
- `skills/create-skills/SKILL.md` — `plan.md:70` → `skills/external/create-skills/SKILL.md`.
- `skills/improve-skills/SKILL.md` — `plan.md:71` → `skills/external/improve-skills/SKILL.md`.
**Guards**: 13 named, **all alive** — `tests/contract/test_feedback_command_classification.py`, `test_feedback_entry_schema.py`, `test_feedback_skill_conformance.py`, `test_feedback_utils_cli.py`; integration `test_feedback_{command_record,dedup,partial,selective_triggering,skill_record,threshold}.py`; unit `test_feedback_utils.py`, `test_memory_utils.py`. Missing: none. **Behaviour defect**: `test_feedback_skill_conformance.py` globs `skills/*/SKILL.md` → **0 files** under the two-layer layout, so both conformance tests pass vacuously; the mirror leg covers only 17 of 54 skills.
**Registry**: the row naming this spec is **ID 028** (Feedback Mechanism) → Spec Path `.specify/specs/027-feedback-mechanism/requirements.md` (exists); Feature Details `.specify/features/028-sdd-workflow-refactor.md` (exists; slug/content mismatch as above). Row **027** is a different feature (Team Management → `036-team-summary`). **Resolves with ID offset + slug mismatch.**
**Spot-checks**:
- File: `scripts/python/feedback-utils.py` and mirror `.specify/scripts/python/feedback-utils.py` exist (identical size).
- Symbol/command: `templates/skills-template.md:67` carries `## Feedback`; `test_feedback_command_classification.py` has 6 real guard functions incl. `test_complex_command_carries_feedback_step` / `test_simple_command_omits_feedback_step`.
- Behaviour surface: store `.specify/memory/feedback/` live with entries + `.gitkeep` (no `index.json` present; runtime-generated); the skill-conformance guard is blind (above).
**Verdict**: **BROKEN**

## 039-session-export

**Refs**: 27 → **alive 18**, archived 0, dead 9 (3 `[anchor-move]`, 6 other).
**Broken**:
- `.specify/memory/constitution.md` — `plan.md:29` → `[anchor-move]` `.specify/constitution.md`.
- `.specify/memory/features.md` — `plan.md:92` → `[anchor-move]` `.specify/features.md`.
- `.specify/memory/features/043.md` — `plan.md:80` → `[anchor-move]` `.specify/features/043-init-commit-stamp.md` (exists; content is Session Export, slug mismatch).
- `.specify/skills/export-session/SKILL.md` — `plan.md:89` → `.specify/skills/internal/archive-session/SKILL.md`.
- `scripts/export.py` — `plan.md:75` → `skills/internal/archive-session/scripts/export.py`.
- `skills/export-session` — `checklists/requirements.md:9` → `skills/internal/archive-session/` (renamed `export-session`→`archive-session`, commit `03b169fb6`).
- `skills/export-session/SKILL.md` — `quickstart.md:26` → `skills/internal/archive-session/SKILL.md`.
- `skills/export-session/scripts/export.py` — `quickstart.md:13` → `skills/internal/archive-session/scripts/export.py`.
- `tests/contract/test_export_skill_genericity.py` — `tasks.md:55` → merged into `tests/contract/test_export_skill_rework.py` (commit `ed4cf35cd`).
**Guards**: 4 named; **missing 1** (`test_export_skill_genericity.py`, merged as above); alive: `test_export_skill_rework.py`, `test_session_command_surface.py`, `test_session_description.py`.
**Registry**: the row naming this spec is **ID 043** (Session Export) → Spec Path `.specify/specs/039-session-export/requirements.md` (exists); Feature Details `.specify/features/043-init-commit-stamp.md` (exists; slug mismatch). Row **039** (Harvested Harness Improvements) has Spec Path `-`. **Resolves with ID offset + slug mismatch.**
**Spot-checks**:
- File: `templates/commands/session.md` exists and names `.specify/skills/internal/archive-session/SKILL.md` + `scripts/export.py` (line 29).
- Symbol/command: `skills/internal/archive-session/SKILL.md` (`name: archive-session`) and `scripts/export.py` exist in both source and mirror.
- Behaviour surface: `tests/contract/test_session_command_surface.py` has 9 functions (grammar line, name-mandatory, preview gate, delegation, per-tool copies); `test_session_description.py` alive.
**Verdict**: **BROKEN**

## 052-fast-fail-principle

**Refs**: 172 → **alive 137**, archived 0, dead 35 (3 `[anchor-move]`, 32 other — dominated by one dated pre-change measurement snapshot).
**Broken**:
- `.specify/memory/constitution.md` — `contracts/constitution-export.md:22` (×21) → `[anchor-move]` `.specify/constitution.md`.
- `.specify/memory/features.md` — `feature-ref.md:7` (×6) → `[anchor-move]` `.specify/features.md`.
- `.specify/memory/features/052.md` — `feature-ref.md:6` (×4) → `[anchor-move]` `.specify/features/052-fast-fail-principle.md`.
- Dated pre-change mirror snapshot (`notes/pre-change-measurements.md`, measured 2026-09-23; internal skills have since moved under `.specify/skills/internal/`, six draw-* and four git-* skills consolidated, study-project renamed):
  - `.specify/skills/archive-session/SKILL.md`:47 → `.specify/skills/internal/archive-session/SKILL.md`
  - `.specify/skills/code-review/SKILL.md`:48 → `.specify/skills/internal/code-review/SKILL.md`
  - `.specify/skills/collect-evidence/SKILL.md`:49 → `.specify/skills/internal/collect-evidence/SKILL.md`
  - `.specify/skills/create-agent/SKILL.md`:50 → `.specify/skills/internal/create-agent/SKILL.md`
  - `.specify/skills/create-team/SKILL.md`:54 → `.specify/skills/internal/create-team/SKILL.md`
  - `.specify/skills/create-team/references/operating-loops.md`:55 → `.specify/skills/internal/create-team/references/operating-loops.md`
  - `.specify/skills/create-team/references/summary-mapping.md`:56 → `.specify/skills/internal/create-team/references/summary-mapping.md`
  - `.specify/skills/create-team/references/team-presets.md`:57 → `.specify/skills/internal/create-team/references/team-presets.md`
  - `.specify/skills/create-tools/SKILL.md`:58 → `.specify/skills/internal/create-tools/SKILL.md`
  - `.specify/skills/draw-d3js/SKILL.md`:61 → merged into `.specify/skills/draw-diagram/`
  - `.specify/skills/draw-drawio/SKILL.md`:63 → merged into `.specify/skills/draw-diagram/`
  - `.specify/skills/draw-echarts/SKILL.md`:64 → merged into `.specify/skills/draw-diagram/`
  - `.specify/skills/draw-excalidraw/SKILL.md`:65 → merged into `.specify/skills/draw-diagram/`
  - `.specify/skills/draw-mermaid/SKILL.md`:66 → merged into `.specify/skills/draw-diagram/`
  - `.specify/skills/draw-plantuml/SKILL.md`:67 → merged into `.specify/skills/draw-diagram/`
  - `.specify/skills/git-fleet/SKILL.md`:68 → merged into `.specify/skills/git-utils/`
  - `.specify/skills/git-server-init/SKILL.md`:69 → merged into `.specify/skills/git-utils/`
  - `.specify/skills/git-submodule-edit/SKILL.md`:70 → merged into `.specify/skills/git-utils/`
  - `.specify/skills/git-workflow/SKILL.md`:71 → merged into `.specify/skills/git-utils/`
  - `.specify/skills/improve-agent/SKILL.md`:72 → `.specify/skills/internal/improve-agent/SKILL.md`
  - `.specify/skills/improve-team/SKILL.md`:76 → `.specify/skills/internal/improve-team/SKILL.md`
  - `.specify/skills/improve-tools/SKILL.md`:77 → `.specify/skills/internal/improve-tools/SKILL.md`
  - `.specify/skills/manage-agents/SKILL.md`:78 → `.specify/skills/internal/manage-agents/SKILL.md`
  - `.specify/skills/memory-recall/SKILL.md`:79 → `.specify/skills/internal/memory-recall/SKILL.md`
  - `.specify/skills/memory-record/SKILL.md`:80 → `.specify/skills/internal/memory-record/SKILL.md`
  - `.specify/skills/study-project/SKILL.md`:82 → `.specify/skills/study-code/SKILL.md` (renamed, commit `cde73a99f`)
  - `.specify/skills/summarize-project/SKILL.md`:83 → `.specify/skills/internal/summarize-project/SKILL.md`
  - `.specify/skills/think-skills/SKILL.md`:84 → no target (skill removed; no replacement directory)
- `.specify/teams/.work` — `requirements.md:100` → absent; runtime scratch dir, used as a measurement exclusion only.
- `skills/create-agent/SKILL.md` — `notes/red-first-evidence.md:48` → `skills/internal/create-agent/SKILL.md` (pre-two-layer path).
- `skills/create-team/references/patterns.md` — `notes/red-first-evidence.md:48` (×3) → `skills/internal/create-team/references/patterns.md`.
- `skills/internal/study-project/SKILL.md` — `requirements.md:106` → `skills/external/study-code/SKILL.md` (renamed; and the layer is `external`, not `internal`).
**Guards**: 13 named, **all alive** — incl. `tests/contract/test_fast_fail_discipline.py` (34 refs), `test_constitution_double_landing.py`, `test_confirmation_gates_sweep.py`, `test_user_facing_comprehension_{doc,pointers,section}.py`, `test_instructions_section_propagation.py`, `test_specify_script_paths.py`. Missing: none.
**Registry**: row `052` → Spec Path `.specify/specs/052-fast-fail-principle/requirements.md` (exists); Feature Details `.specify/features/052-fast-fail-principle.md` (exists, matches). **Resolves.**
**Spot-checks**:
- File: `shared/guidelines/fast-fail.md` + mirror `.specify/shared/guidelines/fast-fail.md` exist.
- Symbol/command: `tests/contract/test_fast_fail_discipline.py` carries the C-series guards (`test_c1_truth_source_doc_exists`, `test_c4_ownership_first_8_lines`, `test_c5_failure_statement_first_20_lines`, `test_c20_marker_literals_are_mutually_disjoint`); `scripts/python/scan-confirmation-gates.py` exists.
- Behaviour surface: `## Fast Fail Discipline` ambient section present in `.specify/instructions.md:191`.
**Verdict**: **BROKEN** (live requirements pointers stale; the bulk of dead refs are one dated measurement snapshot, preserved as a record).

## 065-loop-interruption-recovery

**Refs**: 47 → **alive 40**, archived 0, dead 7 (3 `[anchor-move]`, 4 other).
**Broken**:
- `.specify/memory/constitution.md` — `plan.md:49` → `[anchor-move]` `.specify/constitution.md`.
- `.specify/memory/features.md` — `feature-ref.md:12` (×3) → `[anchor-move]` `.specify/features.md`.
- `.specify/memory/features/065.md` — `checklists/requirements.md:36` (×5) → `[anchor-move]` `.specify/features/065-loop-interruption-recovery.md`.
- `.specify/specs/065-demo/plan.md` — `quickstart.md:15` → runtime `mktemp -d` sandbox path (`$TMP/repo/.specify/specs/065-demo/plan.md`); no live target by design.
- `tests/unit/test_loop_state.py` — `contracts/non-regression-and-tests.md:28` (×5) → never existed; the engine coverage landed in `tests/unit/test_loop_state_engine.py` (065a).
- `tests/contract/test_sdd_loop_driver_state_awareness.py` — `contracts/non-regression-and-tests.md:29` (×5) → never existed; coverage landed in `tests/contract/test_loop_state_contract.py` (065a).
- `tests/integration/test_loop_state_interruption_matrix.py` — `contracts/non-regression-and-tests.md:30` (×5) → never existed; no same-named replacement (parts live in `test_loop_state_contract.py`).
**Guards**: 6 named; **missing 3** (the three never-landed files above); alive: `test_sdd_loop_driver_skill.py`, `test_decomposition_check.py`, `test_line_registry_engine.py`.
**Registry**: row `065` → Spec Path `.specify/specs/065-loop-interruption-recovery/requirements.md` (exists); Feature Details `.specify/features/065-loop-interruption-recovery.md` (exists, matches; status `Planned`). **Resolves.**
**Spot-checks**:
- File: `skills/external/sdd-loop-driver/scripts/loop-state.py` + mirror `.specify/skills/sdd-loop-driver/scripts/loop-state.py` exist.
- Symbol/command: `--action` choices `snapshot | recover | check-spine` at `loop-state.py:3089`.
- Behaviour surface: `skills/external/sdd-loop-driver/references/state-awareness.md` and `scripts/watch-target.sh` exist; the delivered state tests are `tests/unit/test_loop_state_engine.py` + `tests/contract/test_loop_state_contract.py`, not the three names the contracts cite.
**Verdict**: **BROKEN**

## 075-sdd-loop-efficiency

**Refs**: 107 unique after excluding 2 prose compounds (`scripts/contracts` at `notes/quickstart-run.md:100`; `tests/contracts` at `notes/source-requirement.md:70`) → **alive 99**, archived 0, dead 8 (5 `[anchor-move]`, 3 other).
**Broken**:
- `.specify/memory/constitution.md` — `contracts/fast-lane.md:11` (×2) → `[anchor-move]` `.specify/constitution.md`.
- `.specify/memory/features` — `plan.md:160` → `[anchor-move]` `.specify/features/`.
- `.specify/memory/features.md` — `checklists/efficiency.md:126` (×11) → `[anchor-move]` `.specify/features.md`.
- `.specify/memory/features/058.md` — `checklists/requirements.md:36` (×12) → `[anchor-move]` `.specify/features/058-sdd-loop-driver.md`.
- `.specify/memory/features/061.md` — `plan.md:21` → `[anchor-move]` `.specify/features/061-subagent-cli-config.md`.
- `.specify/specs/012-medium/plan.md` — `notes/quickstart-run.md:68` (×4) → runtime `$WORK063/medium/.specify/specs/012-medium/plan.md`, copied from the live fixture `tests/fixtures/sdd_loop_efficiency/medium/.specify/specs/012-medium/plan.md`.
- `scripts/*.sh` — `plan.md:47` → no top-level shell scripts; scripts are language-partitioned (`scripts/bash/`, `scripts/python/`, `scripts/js/`).
- `tests/unit/test_cli_profile_record.py` — `notes/analysis-gate-report.md:74` → never existed; coverage lives in `tests/contract/test_sdd_loop_driver_cli_profiles.py`.
**Guards**: 14 named; **missing 1** (`tests/unit/test_cli_profile_record.py`, never landed); alive: `test_sdd_loop_driver_efficiency.py` (42 refs), `test_sdd_loop_driver_skill.py`, `test_sdd_loop_driver_cli_profiles.py`, `test_sdd_loop_efficiency_{regression,runner}.py`, `test_admission_check.py`, `test_audit_plan_changes.py`, `test_audit_test_budget.py`, `test_derive_live_log.py`, `test_ensure_symlink.py`, fixture helpers.
**Registry**: **NO row for 075** in `.specify/features.md` (pre- or post-rename) and **no detail file** `.specify/features/075-sdd-loop-efficiency.md`. **Does not resolve — BROKEN registry binding.** (Feature 058 is the related registered driver feature, but it is not this spec.)
**Spot-checks**:
- File: `skills/external/sdd-loop-driver/scripts/admission-check.py` + mirror exist.
- Symbol/command: `scripts/bash/run-tests.sh` defaults to process parallelism (`-n <effective> --dist load`, header lines 9–16; caller-supplied `-n`/`--dist` guard at lines 98–100).
- Behaviour surface: guards + `tests/fixtures/sdd_loop_efficiency/{medium,large,plan-repo,...}` all present; the cli-profile-record guard was renamed/rehomed to the contract test (above).
**Verdict**: **BROKEN** (registry missing; one never-landed guard; rest are runtime-path and anchor-move notes).

## 087-arch-diagram-docs

**Refs**: 344 unique after excluding 2 prose tokens (`.specify/specs/087-` ellipsis at `contracts/diagram-obligation.contract.md:14`; `scripts/tests` prose at `code-review.md:330`) → **alive 324**, **archived 1**, dead 19 (4 `[anchor-move]`, 15 other).
**Archived-elsewhere**:
- `.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` — `research.md:152` → `.specify/archive/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt`.
**Broken**:
- `.specify/memory/constitution.md` — `plan.md:54` (×3) → `[anchor-move]` `.specify/constitution.md`.
- `.specify/memory/features.md` — `checkpoints/02-clarify.md:13` (×13) → `[anchor-move]` `.specify/features.md`.
- `.specify/memory/features/087.md` — `checklists/requirements-quality.md:8` (×16) → `[anchor-move]` `.specify/features/087-arch-diagram-docs.md`.
- `.specify/memory/register.md` — `code-review.md:121` (×6) → `[anchor-move]` `.specify/register.md`.
- `.specify/.tmp/087-review3` — `review.md:44` → transient scratch removed (`.specify/.tmp/` itself is live).
- `.specify/skills/external` — `test-evidence/analyze-report-round1.md:29` → absent in the installed mirror; `feature-ref.md:30` states the mirror has no `external/` layer (source tree uses `skills/external/`).
- `.specify/skills/external/**` — `test-evidence/analyze-repair-round1.md:105` → same as above.
- `.specify/specs/087-arch-diagram-docs/goal/087-arch-diagram-docs/goal.md` — `checkpoints/01-requirements.md:21` (×5) → deleted at closure (`3aca34383`); project-level `.specify/anchoring/087-arch-diagram-docs/goal.md` exists.
- `.specify/specs/087-arch-diagram-docs/team/087-arch-diagram-docs/team.md` — `checkpoints/03-plan.md:49` (×3) → deleted at closure; `.specify/teams/087-arch-diagram-docs/` exists.
- `.specify/specs/087-arch-diagram-docs/test-evidence/baseline-full-suite.log` — `verification.md:33` → missing; only `baseline-failed.txt` remains.
- `.specify/templates/commands` — `feature-ref.md:30` (×6) → retired subtree (absent on both sides; the spec itself records the retirement).
- `.specify/templates/commands/docs.md` — `checkpoints/06-analyze.md:18` (×7) → retired; source is `templates/commands/docs.md`.
- `.specify/templates/examples/structure-*.md` — `plan.md:201` → no `examples/` directory in `templates/` or `.specify/templates/`.
- `scripts/docs-utils.py` — `plan.md:237` → tree-display relative path; real path `skills/external/create-docs/scripts/docs-utils.py`.
- `scripts/python/diagram-obligation-check.py` — `plan.md:127` → deliberately not created (rejected alternative in the decision record; the check landed as `docs-utils.py --action obligation`).
- `skills/external/create-docs/contracts` — `review.md:209` → absent; the review records this as a known dead link (P2).
- `skills/external/create-docs/quickstart.md` — `review.md:209` → absent; same known dead link.
- `skills/external/humanize/SKILL.md` — `research.md:151` → `skills/external/humanize-conclusion/SKILL.md` (renamed, commit `dae8a9424`).
- `tests/fixtures/docs-obligation/conftest.py` — `code-review.md:187` (×5) → never committed; fixtures use `helpers.py` + `build_fixtures.py`, repo conftest is `tests/conftest.py`.
**Not dead (reclassified)**: `templates/commands/docs.md-stop-and-confirm` is a live pytest node id (KEEP_LIST entry `("templates/commands/docs.md", "stop-and-confirm")` in `tests/contract/test_confirmation_gates_sweep.py:71`); `.specify/.tmp/space-stale-source.XXXXXX` is a `mktemp` template under the live `.specify/.tmp/`; `.specify/skills/<name>/**` is a placeholder rooted in the live `.specify/skills/`; `tests/fixtures/docs-obligation/orphan-rendered/.../…diagram-trace.json` resolves to the committed fixture file.
**Guards**: 16 named; **missing 1 fixture helper** (`tests/fixtures/docs-obligation/conftest.py` — not a test module); alive: `test_docs_utils_obligation.py` (53 refs), `test_docs_obligation_scenarios.py` (52), `test_docs_command_scenarios.py` (62), `test_docs_utils_carriers.py`, `test_docs_obligation_reuse.py`, `test_docs_utils_cli.py`, `test_docs_command_template.py`, `test_expression_{compatibility,gate_wiring}.py`, `test_directory_governance.py`, `test_confirmation_gates_sweep.py`.
**Registry**: row `087` → Spec Path `.specify/specs/087-arch-diagram-docs/requirements.md` (exists); Feature Details `.specify/features/087-arch-diagram-docs.md` (exists, matches). **Resolves.**
**Spot-checks**:
- File: `skills/external/create-docs/scripts/docs-utils.py` + mirror `.specify/skills/create-docs/scripts/docs-utils.py` exist.
- Symbol/command: `--action obligation` registered (`docs-utils.py:362,768,876`; closed action set at `:836`); `templates/commands/status.md` and `templates/commands/measure.md` exist.
- Behaviour surface: `tests/unit/test_docs_utils_obligation.py` has the C-001/C-016 guards (`test_c001_action_registered`, `test_c001_option_set_closed`, `test_c016_precedence_order`, `test_c016_no_backtracking`); `tests/integration/test_docs_obligation_scenarios.py` has the C-002/C-011 guards; all 11 fixture verdict directories present.
**Verdict**: **BROKEN** (dead refs mix historical checkpoint records, one deliberate non-creation, one documented known-dead link, and 4 anchor-move refs).

---

## Batch summary

| Spec | Refs | Alive | Archived | Dead | Verdict |
|------|-----:|------:|---------:|-----:|---------|
| 001-unify-command-handoffs | 5 | 5 | 0 | 0 | INTACT |
| 027-feedback-mechanism | 84 | 74 | 0 | 10 | BROKEN |
| 039-session-export | 27 | 18 | 0 | 9 | BROKEN |
| 052-fast-fail-principle | 172 | 137 | 0 | 35 | BROKEN |
| 065-loop-interruption-recovery | 47 | 40 | 0 | 7 | BROKEN |
| 075-sdd-loop-efficiency | 107 | 99 | 0 | 8 | BROKEN |
| 087-arch-diagram-docs | 344 | 324 | 1 | 19 | BROKEN |
| **Total** | **786** | **697** | **1** | **88** | — |

Of the 88 dead refs, **21 are anchor-rename moves** (027: 3, 039: 3, 052: 3, 065: 3, 075: 5, 087: 4) — they were alive at audit start and have a known new path; the remaining **67** are ordinary dead references, of which 30 are one dated pre-change snapshot in 052's notes and 3 are dated checkpoints/known-dead records in 087.

Registry health: 5 rows resolve (001, 052, 065, 087, and 027/039 via offset rows 028/043 with detail-slug mismatches); **075 has no registry row and no detail file**.

Guard health: all named test modules exist except three never-landed 065 test files, one never-landed 075 test file, one merged 039 test file, and one never-committed 087 fixture helper. One live guard has gone blind: 027's `test_feedback_skill_conformance.py` globs `skills/*/SKILL.md` (0 matches under the two-layer layout).

**Anomaly**: the anchor-layout rename merged into `master` mid-audit (`6fb8093c4`), relocating `.specify/memory/{constitution,features,glossary,register,tools}.md` and renaming feature-detail files to `<ID>-<spec-dir-slug>.md` — that rename paired rows 027/028 and 039/043 with detail files whose slugs name a different feature than their content, and this audit's counts are pinned to the post-merge HEAD with anchor-move refs flagged per spec.

SPEC-AUDIT-LIVE-1-DONE
