# Live-Spec Audit — Batch 12 (025, 038, 051, 064, 074b, 086)

**Mode**: read-only (no spec/source modified; this file is the only write)
**Tree**: main tree `/storage/project/cloud-native-ai/spec-kit`
**Method**: program-first extraction of every repo-path token from the named artifacts
(`requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `verification.md`,
`research.md`, `review.md`, `code-review.md`, `feature-ref.md`, `contracts/*`, `checklists/*`, `notes/**`),
then existence classification against the current tree, registry-cell resolution, named-guard inventory,
and three implementation spot-checks per spec.
**Counting unit**: one row per distinct referenced path; occurrence counts are shown in brackets.
**Classifications**: `alive` = exists now; `archived` = target under `.specify/archive/`;
`dead` = no target at the referenced path. `dead` is split into **stable** (missing pointer),
**temp** (run scratch / dated backup, absent by design) and **anchor-moved** (a `memory/`-rooted
pre-consolidation pointer whose target now lives at the `.specify/` root — counted as dead per the
audit rule, and flagged separately below).

> **Mid-audit tree change**: the pending anchor-layout rename landed in the main tree while this audit
> ran (merge `6fb8093c4`: `.specify/memory/{constitution,features,glossary,register,tools}.md` and
> `.specify/memory/features/<ID>.md` -> `.specify/` root + `.specify/features/<ID>-<slug>.md`).
> All classification was re-run against the post-rename tree. References the task asked to flag as
> "will move" are therefore now reported as **dead / anchor-moved** with their new targets.

## Batch Summary

| Spec | refs | alive | archived | dead | verdict |
|------|------|-------|----------|------|---------|
| 025-agent-skill-enablement | 24 | 13 | 0 | 11 | BROKEN |
| 038-goal-target | 45 | 38 | 0 | 7 | BROKEN |
| 051-user-facing-comprehension | 137 | 122 | 0 | 15 | BROKEN |
| 064-subagent-concurrency | 100 | 94 | 0 | 6 | BROKEN |
| 074b-nested-governance | 203 | 194 | 0 | 9 | BROKEN |
| 086-efficient-test-execution | 195 | 171 | 2 | 22 | BROKEN |

Dead composition (stable + anchor-moved + temp): 025 = 8+3+0; 038 = 3+4+0; 051 = 9+4+2;
064 = 3+3+0; 074b = 3+4+2; 086 = 4+5+13.

---

## 025-agent-skill-enablement

**Artifacts**: 8 files (requirements, plan, tasks, data-model, quickstart, verification, 1 contract, 1 checklist).
**Paths**: 24 refs — 13 alive, 0 archived, 11 dead (8 stable + 3 anchor-moved).
**Registry**: row **026** (feature ID differs from spec ID) — Feature Details
`.specify/features/026-agent-skill-enablement.md` exists; Spec Path
`.specify/specs/025-agent-skill-enablement/requirements.md` exists. **Resolves.**
**Guards**: 2 named test references, 2 alive; 0 missing. Primary guard
`tests/contract/test_agent_skill_enablement.py` exists (class-based tests, US1/US2 assertions on
`skills:` frontmatter and `## Skill Enablement`).

**Broken items**
- `skills/internal/create-agent/templates/agent-role-*-template.md:16` (plan.md, 3x) -> renamed to
  `agent-capacity-*-template.md`; the directory is alive, no `agent-role-*` file exists.
- `skills/internal/create-agent/templates/agent-role-requirements-analyst-template.md:133` (tasks.md, 2x)
  -> `agent-capacity-requirements-analyst-template.md`.
- `.../agent-role-system-designer-template.md:134` -> `agent-capacity-system-designer-template.md`.
- `.../agent-role-module-designer-template.md:135` -> `agent-capacity-module-designer-template.md`.
- `.../agent-role-test-engineer-template.md:136` -> `agent-capacity-test-engineer-template.md`.
- `.../agent-role-qa-engineer-template.md:137` -> `agent-capacity-qa-engineer-template.md`.
- `.../agent-role-knowledge-manager-template.md:138` -> `agent-capacity-knowledge-manager-template.md`.
- `.../agent-role-ux-analyst-template.md:139` -> `agent-capacity-ux-analyst-template.md`.
- `.specify/memory/constitution.md:28` (plan.md, 1x) -> now `.specify/constitution.md`.
- `.specify/memory/features.md:9` (tasks.md, 1x) -> now `.specify/features.md`.
- `.specify/memory/features/026.md:153` (tasks.md, 1x) -> now `.specify/features/026-agent-skill-enablement.md`.

**Spot-checks (3/3 pass)**
1. 7 `agent-capacity-*-template.md` files carry a non-empty `skills:` frontmatter
   (e.g. `agent-capacity-requirements-analyst-template.md:10`).
2. 8 files under the template dir carry `## Skill Enablement` (the 7 role templates + the shared
   `agent-skill-enablement.md` snippet).
3. Guard body enforces the contract: `test_frontmatter_has_skills_key`, `test_skills_list_non_empty`,
   `test_has_skill_enablement_section` (`tests/contract/test_agent_skill_enablement.py:76-98`).

**Verdict: BROKEN** — 8 stale template filenames + 3 anchor-moved pointers; implementation and guard intact.

---

## 038-goal-target

**Artifacts**: 11 files (requirements, plan, tasks, data-model, quickstart, verification, feature-ref,
1 checklist, 3 contracts, 6 notes logs).
**Paths**: 45 refs — 38 alive, 0 archived, 7 dead (3 stable + 4 anchor-moved).
**Registry**: **NO ROW** references `specs/038-goal-target/`. Feature 038 is *Evidence Infrastructure*
(spec 034); feature **041** (Goal Registry) absorbs this slice, recorded in
`.specify/features/041-refactor-feedback-probe.md:22-24,73`. Strict criterion fails; an absorption
pointer exists only in the detail body.
  - Side finding: row 041 is named **Goal Registry** but its detail file is slugged
    `041-refactor-feedback-probe.md` — the rename branch mis-slugged the file.
**Guards**: 10 named test references, 8 alive, 2 missing (below). Live family: `test_goal_targets_engine.py`,
`test_goal_targets_check.py`, `test_focus_target_resolution.py`, `test_goal_command_template.py`.

**Broken items**
- `scripts/build-summary-input.py:81` (plan.md) -> now `skills/internal/create-team/scripts/build-summary-input.py`.
- `tests/contract/test_goal_command_surface.py:46` (tasks.md) -> missing; nearest successor
  `tests/contract/test_goal_command_template.py`.
- `tests/contract/test_run_target_assignment.py:58` (tasks.md, 3x; quickstart.md:102) -> missing;
  nearest successors `tests/contract/test_focus_target_resolution.py`, `test_goal_targets_engine.py`.
- `.specify/memory/constitution.md:34` -> `.specify/constitution.md`.
- `.specify/memory/features.md:46` (checklists, 2x) -> `.specify/features.md`.
- `.specify/memory/features/041.md:3` (feature-ref.md) -> `.specify/features/041-refactor-feedback-probe.md`.
- `.specify/memory/glossary.md:104` (tasks.md, 2x) -> `.specify/glossary.md`.

**Spot-checks (3/3 pass)**
1. `targets` subcommand is registered in `.specify/scripts/python/goal-utils.py:2674`.
2. `preview_target_check` exists and implements the verdict path (`goal-utils.py:1263`).
3. `templates/commands/goal.md:4,29` exposes the `targets` mode and delegates to
   `.specify/skills/internal/manage-goal/SKILL.md`.

**Verdict: BROKEN** — no registry row of its own; 2 named guards missing; 1 stale script path; 4 anchor-moved refs.

---

## 051-user-facing-comprehension

**Artifacts**: 17 files (requirements, plan, tasks, data-model, quickstart, verification, research,
feature-ref, 5 contracts, 1 checklist, 3 notes, baseline-failed).
**Paths**: 137 refs — 122 alive, 0 archived, 15 dead (9 stable + 4 anchor-moved + 2 temp).
**Registry**: row **051** — Feature Details `.specify/features/051-user-facing-comprehension.md` exists;
Spec Path `.specify/specs/051-user-facing-comprehension/requirements.md` exists. **Resolves.**
**Guards**: 23 named test references, 20 alive, 3 missing (below). Live family includes
`test_user_facing_comprehension_doc.py`, `test_user_facing_comprehension_section.py`,
`test_user_facing_comprehension_pointers.py`.

**Broken items (stable)**
- `.specify/skills/browser-utils/scripts/chrome_open_trust.sh:60` (notes/pre-change-measurements.md)
  -> no `browser-utils` skill anywhere in the tree or archive.
- `scripts/bash/update-feature-index.sh:171` (verification.md, 4x; feature-ref.md:19)
  -> script removed; `.specify/features.md` is hand-maintained.
- `shared/guidelines/user-facing-comprehension-v2.md:86` (notes/red-first-evidence.md, 2x)
  -> final doc is `shared/guidelines/user-facing-comprehension.md` (no `-v2`).
- `shared/templates/skills-summarize-project/agents/scripts:155` (verification.md) -> no such tree.
- `skills/summarize-project:184` (notes/pre-change-measurements.md) -> now `skills/internal/summarize-project`.
- `skills/summarize-project/references/reporting-playbook.md:140` (quickstart.md, 5x)
  -> now `skills/internal/summarize-project/references/reporting-playbook.md`.
- `tests/contract/test_confirmation_gates_execution_report.py:238` (quickstart.md, 10x;
  requirements.md:52) -> missing; family successor `tests/contract/test_confirmation_gates_sweep.py`.
- `tests/contract/test_token_efficiency_remediation_summary_first.py:456` (notes/quickstart-run.md, 2x)
  -> missing; no same-name successor.
- `tests/integration/test_team_create_flow.py:300` (notes/pre-change-measurements.md) -> missing.

**Broken items (anchor-moved)**
- `.specify/memory/constitution.md:18` (quickstart.md, 29x) -> `.specify/constitution.md`.
- `.specify/memory/features.md:7` (feature-ref.md, 4x) -> `.specify/features.md`.
- `.specify/memory/features/051.md:6` (feature-ref.md, 4x) -> `.specify/features/051-user-facing-comprehension.md`.
- `.specify/memory/features/040.md:15` (feature-ref.md, 1x) -> `.specify/features/040-agent-metadata-portability.md`.

**Broken items (temp, expected absent)**
- `.specify/instructions.md-2026-09-18-192435:136` (notes/quickstart-run.md).
- `.specify/skills/.migration-backups/layout-int-*/SKILL.md:54` (quickstart.md, 2x).

**Spot-checks (3/3 pass)**
1. `shared/guidelines/user-facing-comprehension.md` carries the whitelist (§9), blacklist (§21),
   context floor/ceiling (§45/§55), mechanical verdict (§71) and the 11-surface class list (§88).
2. `templates/constitution-template.md:183` MUST-includes the discipline and points at the owner.
3. 11 template/guideline/live-constitution files wire the pointer; the pointers guard has 13 tests.

**Verdict: BROKEN** — 3 named guards missing, 6 stable stale pointers (incl. a live-quickstart path),
4 anchor-moved refs, 2 temp refs. The discipline itself is implemented and wired.

---

## 064-subagent-concurrency

**Artifacts**: 24 files (requirements, plan, tasks, data-model, quickstart, verification, research,
review, feature-ref, 6 contracts, 2 checklists, 7 notes, 3 notes logs/dirs).
**Paths**: 100 refs — 94 alive, 0 archived, 6 dead (3 stable + 3 anchor-moved).
**Registry**: row **064** — Feature Details `.specify/features/064-subagent-concurrency.md` exists;
Spec Path `.specify/specs/064-subagent-concurrency/requirements.md` exists. **Resolves.**
**Guards**: 16 named test references, 15 alive, 1 missing (below). Live line-registry family:
`test_line_registry_contract.py`, `test_line_registry_child_lines.py`, `test_line_envelope_contract.py`,
`test_line_state_blocked.py`.

**Broken items**
- `.specify/specs/075-sdd-loop-efficiency/contracts/cli-profiles.md:70` (tasks.md, 5x) -> absent;
  075's contracts are `delivery-and-invariants`, `fast-lane`, `plan-constraint`, `progress-decoupling`,
  `test-budget`.
- `scripts/integrate-lines.sh:551` (review.md) -> implemented as
  `skills/external/sdd-loop-driver/scripts/integrate-lines.py` (review recommendation, extension differs).
- `tests/unit/test_cli_profile_record.py:70` (tasks.md, 6x) -> missing; family successor
  `tests/contract/test_sdd_loop_driver_cli_profiles.py`.
- `.specify/memory/constitution.md:34` -> `.specify/constitution.md`.
- `.specify/memory/features.md:12` (feature-ref.md, 2x) -> `.specify/features.md`.
- `.specify/memory/features/064.md:13` (feature-ref.md, 3x) -> `.specify/features/064-subagent-concurrency.md`.
  The quickstart's `$SKILL/scripts/{line-registry.py,watch-target.sh}` references resolve under
  `skills/external/sdd-loop-driver/scripts/` and are counted alive.

**Spot-checks (3/3 pass)**
1. `line-registry.py` exposes 24 actions including `register`, `resolve-message`, `verify-identity`,
   `classify-remote`, `reattach-brief`, `lease-*`, `reserve`, `orphan-check`, `ownership-check`,
   `integration-*` (`.specify/skills/sdd-loop-driver/scripts/line-registry.py:81-90`).
2. `tests/contract/test_line_envelope_contract.py` has 18 tests and asserts
   `{line_id, run_id, stage, event, at}` on the record envelope.
3. worktree-per-line routing is present in `run-stage.sh`, `watch-target.sh`, `admission-check.py`
   under `.specify/skills/sdd-loop-driver/scripts/`.

**Verdict: BROKEN** — 1 named guard missing, 2 stale pointers (075 contract, extension), 3 anchor-moved refs.

---

## 074b-nested-governance

**Artifacts**: 18 files (requirements, plan, tasks, data-model, quickstart, verification, research,
review, code-review, feature-ref, 3 contracts, 2 checklists, 2 notes + logs).
**Paths**: 203 refs — 194 alive, 0 archived, 9 dead (3 stable + 4 anchor-moved + 2 temp).
**Registry**: **NO ROW** for `specs/074b-nested-governance/`. Feature **074**'s row points at
`specs/074-goal-team-sdd-unification/requirements.md`; the 074b slice is recorded in
`.specify/features/074-goal-team-sdd-unification.md:8,24,30`. Strict criterion fails; slice coverage
exists only in the detail body.
**Guards**: 12 named test references, 12 alive, 0 missing (`test_nested_sdd_invocation.py` 17 tests,
`test_nested_run_report.py` 16 tests among them).

**Broken items**
- `.specify/goal:70` (quickstart.md) -> retired goal layout; live goal store is `.specify/anchoring/`.
- `.specify/goal/command-logic-as-classified-skills/summary/assets/wbs.png:258` (review.md, 2x)
  -> exists at `.specify/anchoring/command-logic-as-classified-skills/summary/assets/wbs.png`.
- `scripts/python/line-registry.py:207` (notes/pre-change-measurements.md) -> now
  `skills/external/sdd-loop-driver/scripts/line-registry.py` (mirror: `.specify/skills/sdd-loop-driver/scripts/`).
- `.specify/memory/constitution.md:90` (plan.md, 2x) -> `.specify/constitution.md`.
- `.specify/memory/features.md:17` (requirements.md, 6x) -> `.specify/features.md`.
- `.specify/memory/features/074.md:17` (requirements.md, 7x) -> `.specify/features/074-goal-team-sdd-unification.md`.
- `.specify/memory/glossary.md:93` (code-review.md, 2x) -> `.specify/glossary.md`.
- Temp (expected absent): `.specify/.tmp/074b-goal-fixture:13` (3x), `.specify/.tmp/containment-post-failed.txt:178` (2x).

**Spot-checks (3/3 pass)**
1. `.specify/shared/definitions/sdd-routing-definitions.md:3,14,61-70` owns the four routing facts and
   names engine actions `route` / `authorize` / `golden`.
2. `python3 .specify/scripts/python/sdd-route.py --help` exits 0; `--version` prints `sdd-route.py 0.0.22`.
3. `sdd-invocation` capability is present in `skills/internal/run-agent/SKILL.md` and
   `skills/internal/create-team/references/create-mode.md`; nested-run guards are green by existence.

**Verdict: BROKEN** — no registry row of its own; 3 stable stale paths (retired goal layout, line-registry
path), 4 anchor-moved refs, 2 temp refs.

---

## 086-efficient-test-execution

**Artifacts**: 17 files (requirements, plan, tasks, data-model, quickstart, verification, research,
review, code-review, feature-ref, 4 contracts, 2 checklists, 1 notes, coverage baseline).
**Paths**: 195 refs — 171 alive, 2 archived, 22 dead (4 stable + 5 anchor-moved + 13 temp).
**Registry**: row **086** — Feature Details `.specify/features/086-efficient-test-execution.md` exists;
Spec Path `.specify/specs/086-efficient-test-execution/requirements.md` exists. **Resolves.**
**Guards**: 15 named test references, 15 alive, 0 missing. Primary guards
`tests/contract/test_run_tests_runner_contract.py` (31 tests) and `test_test_execution_efficiency.py`
(7 tests).

**Broken items (stable)**
- `.specify/goal:210` (plan.md, 9x; verification.md:50) -> retired goal layout; live store `.specify/anchoring/`.
- `.specify/skills/external/sdd-loop-driver:4` (contracts/budget-ledger-parser.contract.md)
  -> the `.specify/` mirror is `.specify/skills/sdd-loop-driver` (no `external/` layer under `.specify/skills`);
  the source-side `skills/external/sdd-loop-driver/...` is alive.
- `.specify/specs/086-efficient-test-execution/team:129` (data-model.md) -> now
  `.specify/teams/086-efficient-test-execution`.
- `scripts/audit-test-budget.py:5` (contracts/budget-ledger-parser.contract.md; code-review.md:49)
  -> now `skills/external/sdd-loop-driver/scripts/audit-test-budget.py`.

**Broken items (anchor-moved)**
- `.specify/memory/constitution.md:199` (review.md, 24x) -> `.specify/constitution.md`.
- `.specify/memory/features.md:176` (review.md, 13x) -> `.specify/features.md`.
- `.specify/memory/features/086.md:57` (review.md, 15x) -> `.specify/features/086-efficient-test-execution.md`.
- `.specify/memory/features/085.md:215` (plan.md, 1x) -> `.specify/features/085-sdd-temporary-goal-team.md`.
- `.specify/memory/register.md:418` (review.md, 1x) -> `.specify/register.md`.

**Archived-elsewhere (2)**
- `.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md:289`
  -> `.specify/archive/goal-team/trees/.../goal/.../goal.md`.
- `.specify/specs/086-efficient-test-execution/team/086-efficient-test-execution/team.md:303`
  -> `.specify/archive/goal-team/trees/.../teams/.../team.md`.

**Temp (13, expected absent)**: the `.specify/.tmp/086/*` family in plan/tasks/quickstart/research/review
(`baseline-failed.txt`, `gate-scan-baseline.json`, `isolation-probe.txt`, `parallel-failed.txt`,
`s1/s2/s4/s5-auto/s5-lf/s8-parallel/s8-serial/us1-parallel` name lists).

**Spot-checks (3/3 pass)**
1. `scripts/bash/run-tests.sh:9` documents the default `-n <effective> --dist load`; `:109-110` guards a
   caller-supplied `--dist` from being overridden.
2. `templates/constitution-template.md:331` MUST-includes the efficiency principle and points at
   `.specify/shared/guidelines/test-execution-efficiency.md` (exists in both `shared/` and `.specify/shared/`).
3. Both runner guards exist with 31 + 7 tests; the budget-ledger parser lives at
   `skills/external/sdd-loop-driver/scripts/audit-test-budget.py`.

**Verdict: BROKEN** — 4 stable stale pointers (incl. the contract's `.specify/` mirror path), 5 anchor-moved
refs, 13 temp refs; implementation and guards intact.

---

## Rename-Sensitive References (anchor-layout rename, now landed)

Every reference below pointed at the pre-consolidation `memory/` anchors and now has a live target at the
`.specify/` root. Counts are occurrences.

| Spec | `constitution.md` | `features.md` | `features/<ID>.md` | `glossary.md` | `register.md` | `tools.md` |
|------|-------------------|---------------|--------------------|---------------|--------------|------------|
| 025 | 1 | 1 | 1 (026) | - | - | - |
| 038 | 1 | 2 | 1 (041) | 2 | - | - |
| 051 | 29 | 4 | 5 (051 ×4, 040 ×1) | - | - | - |
| 064 | 1 | 2 | 3 (064) | - | - | - |
| 074b | 2 | 6 | 7 (074) | 2 | - | - |
| 086 | 24 | 13 | 16 (086 ×15, 085 ×1) | - | 1 | - |

The registry's own cells already use the new layout; no `memory/`-rooted cell remains in the six rows
that resolve. A path rewrite in the six specs' artifacts is the sole repair these need.

## Anomaly

ANOMALY: the pending anchor-layout rename landed in the main tree mid-audit (merge `6fb8093c4`), so the batch's pre-rename "will move" references were reclassified as dead anchor-moved pointers against the post-rename tree.

SPEC-AUDIT-LIVE-12-DONE
