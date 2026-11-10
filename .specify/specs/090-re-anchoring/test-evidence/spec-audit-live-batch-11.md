# Live-Spec Audit — Batch 11 (6 specs)

**Date**: 2026-11-10
**Tree**: `master` @ `6fb8093c4` (the `rename-anchors` merge landed mid-audit; every classification below is measured against the post-merge tree)
**Scope**: 024-agent-env-config, 037-goal-registry, 050-proactive-flow-trigger, 063-review-p1-governance, 074a-authorized-routing, 085-sdd-temporary-goal-team
**Mode**: read-only; this file is the only write.

## Method

- Extracted every `.specify/…`, `scripts/…`, `skills/…`, `templates/…`, `shared/…`, `tests/…` token from each spec tree (all `.md` / `.txt` / `.json` / `.yaml`), deduplicated to unique concrete paths.
- Excluded non-references: placeholder/glob tokens (`<>{}*$@~`), log-wrap truncations (`...`/`…`), banned-token literals written as contract text (`050` `.specify/specs/0`), and regex/append artifacts produced by captured test output.
- Classes: **alive** = exists now; **archived-elsewhere** = moved under `.specify/archive/`; **dead** = no target. A pointer at a pre-rename path is dead; where a live successor exists it is named after `->`.
- Anchor-layout note: master now stores the anchors at `.specify/{features.md,constitution.md,glossary.md,register.md,tools.md}` and `.specify/features/<ID>-<slug>.md`. References to `.specify/memory/{features.md,constitution.md,glossary.md,register.md,tools.md,features/<ID>.md}` are therefore dead-by-move and are tagged `[anchor-move]`.
- Guard check reads only design artifacts (requirements / plan / tasks / contracts / data-model / quickstart / verification / review / feature-ref / checklists); frozen failure lists (`baseline-failed*.txt`, `final-failed*.txt`, captured run logs) are reported separately as history, not as live guards.

## 024-agent-env-config

- **Refs**: 25 unique concrete — **19 alive / 0 archived / 6 dead** (1 anchor-move, 5 substantive).
- **Registry row**: **does not resolve to this spec.** Row 024 exists but its Spec Path is `-`, and its detail cell `.specify/features/024-agent-env-config.md` exists yet its content is *“Specification Workspace Versioning”* (filename/content mismatch). The spec’s own binding (`requirements.md` → `Related Feature: 022`) resolves to row 022, whose Spec Path is `.specify/specs/021-agent-specific-config/requirements.md`, not this spec.
- **Guards**: 7 named test files; **7/7 exist** (`test_agent_env_config_contract.py`, `test_agent_specific_config_skills.py`, `agent_env_helpers.py`, `test_agent_env_apply.py`, `test_agent_env_targeting.py`, `test_agent_env_validate.py`, `test_agent_env_helpers.py`).
- **Broken items**:
  - `.specify/specs/024-agent-env-config/plan.md:26` (also `:131`, `:144`) `.specify/memory/constitution.md` -> `[anchor-move]` `.specify/constitution.md`
  - `.specify/specs/024-agent-env-config/plan.md:66` `skills/agent-setup/SKILL.md` (also `tasks.md:57,61,174`) -> renamed; live `skills/internal/manage-agents/SKILL.md` (git `7f609a8f6` renamed `agent-setup` → `cli-setup`; now `manage-agents`)
  - `.specify/specs/024-agent-env-config/plan.md:67` `skills/agent-setup/references` -> `skills/internal/manage-agents/references/`
  - `.specify/specs/024-agent-env-config/plan.md:72` `.specify/skills/agent-setup` + `skills/agent-setup` (also `tasks.md:37`, `requirements.md:6`) -> `.specify/skills/internal/manage-agents/` and `skills/internal/manage-agents/`
  - `.specify/specs/024-agent-env-config/quickstart.md:20` `.specify/skills/agent-setup/scripts/config-agent.sh` -> `skills/internal/manage-agents/scripts/config-agent.sh`
- **Spot-checks**:
  1. PASS — `config_agent_env_validate` / `config_agent_env_apply` exist in `skills/internal/manage-agents/scripts/config-agent.sh:739,761` (claim: `tasks.md:20` DoD-1).
  2. **FAIL** — the spec claims six tools (`claude, codex, qwen, qoder, iflow, opencode`; SC-002 “6/6”) but the live engine supports four: `CONFIG_AGENT_ENV_TOOLS=(claude codex qoder opencode)` (`config-agent.sh:158`), and the contract test pins the same four (`tests/contract/test_agent_env_config_contract.py:29`, variably named `SIX_TOOLS` but containing four entries, with a “four-tool scope” docstring).
  3. PASS — unified-variable page exists at `skills/internal/manage-agents/references/setup/unified-variables.md` (claim: `tasks.md:47`).
- **Verdict**: **BROKEN** — stale skill paths, a six→four tool-scope regression against the spec’s stated contract, and no resolving registry row.

## 037-goal-registry

- **Refs**: 91 unique concrete — **63 alive / 0 archived / 28 dead** (4 anchor-move, 24 substantive; 9 of the substantive are frozen-baseline test names).
- **Registry row**: **resolves** — row 041 (`Goal Registry`) has Spec Path `.specify/specs/037-goal-registry/requirements.md` and Detail `.specify/features/041-refactor-feedback-probe.md`, which exists and whose header is *“Feature Detail: Goal Registry”*. Anomaly: the detail filename slug (`refactor-feedback-probe`) does not match its content.
- **Guards**: 20 named test files; **18/20 exist**. Missing names:
  - `tests/contract/test_goal_command_surface.py` (`tasks.md:115`) — merged by comment into `tests/contract/test_goal_targets_engine.py` (“merged from the former tests/contract/test_goal_command_surface.py”, ~line 280); coverage alive under the merged file.
  - `tests/integration/test_ai_tools_command_coverage.py` (`plan.md:25`, `research.md:75`, `contracts/goal-command.contract.md:59`) — no same-name successor found; command-coverage claims now rest on the `ai_tools` suites.
  - Nine frozen-baseline names are dead as files (`test_agent_specific_config_commands.py`, `test_create_new_skill_contract.py`, `test_skill_home_workdir_template.py`, `test_context_injection.py`, `test_agent_deprecated_terms.py`, `test_agent_reference_integrity.py`, `test_ai_tools_cli_help.py`, `test_claude_refresh_helpers.py`, `test_claude_support_matrix.py`, `test_claude_support_surfaces.py`, `test_qoder_refresh_helpers.py`, `test_qoder_support_matrix.py`, `test_qoder_support_surfaces.py`) — expected drift from later test consolidation, not live guards.
- **Broken items**:
  - `.specify/specs/037-goal-registry/quickstart.md:14` (also `:55`, `plan.md:20`, `:81`) `.specify/goal` -> renamed `.specify/anchoring/` (`shared/definitions/goal-definitions.md:179`)
  - `.specify/specs/037-goal-registry/quickstart.md:46` `.specify/goal/framework-stays-current` -> `.specify/anchoring/framework-stays-current`
  - `.specify/specs/037-goal-registry/quickstart.md:87` `.specify/goal/framework-stays-current/goal.md` -> `.specify/anchoring/framework-stays-current/goal.md`
  - `.specify/specs/037-goal-registry/contracts/goal-writeset-migration.contract.md:42` `.specify/goal/shared-harvest-goal` -> `.specify/anchoring/shared-harvest-goal`
  - `.specify/specs/037-goal-registry/tasks.md:88` (also `:99`) `.specify/goal/shared-harvest-goal/summary` -> `.specify/anchoring/shared-harvest-goal/summary`
  - `.specify/specs/037-goal-registry/quickstart.md:33` `.specify/project/goal/shared-harvest-goal` -> no target (intermediate path that never materialized)
  - `.specify/specs/037-goal-registry/quickstart.md:97` `.specify/teams/goal-share-a/team.md` -> fixture bed is `tests/fixtures/teams/goal-share-a/`
  - `.specify/specs/037-goal-registry/quickstart.md:107` `.specify/teams/goal-share-b/team.md` -> fixture bed is `tests/fixtures/teams/goal-share-b/`
  - `.specify/specs/037-goal-registry/quickstart.md:29` `skills/create-team/scripts/build-summary-input.py` -> `skills/internal/create-team/scripts/build-summary-input.py`
  - `.specify/specs/037-goal-registry/plan.md:38` `.specify/memory/constitution.md` -> `[anchor-move]` `.specify/constitution.md`
  - `.specify/specs/037-goal-registry/feature-ref.md:6` `.specify/memory/features.md` -> `[anchor-move]` `.specify/features.md`
  - `.specify/specs/037-goal-registry/feature-ref.md:5` (also `tasks.md:233`) `.specify/memory/features/041.md` -> `[anchor-move]` `.specify/features/041-refactor-feedback-probe.md`
  - `.specify/specs/037-goal-registry/tasks.md:231` `.specify/memory/glossary.md` -> `[anchor-move]` `.specify/glossary.md`
  - `baseline-failed.txt` lines 1–37: the 13 test files listed above -> removed/renamed by later consolidations (frozen history).
- **Spot-checks**:
  1. PASS — `templates/commands/goal.md` exists with frontmatter and the create/view/modify surface (claim: `tasks.md:115,121`).
  2. PASS — `scripts/python/goal-utils.py` implements `create` / `validate` / `list` / `status` (plus later actions) (claim: `tasks.md:122`; parser at `:2596-2720`).
  3. **STALE** — the claim that `build-summary-input.py` delivers to `.specify/goal/<slug>/summary` (`tasks.md:88`) no longer matches the code: `skills/internal/create-team/scripts/build-summary-input.py:336,1054` uses `.specify/anchoring/<slug>/summary`.
- **Verdict**: **BROKEN** — goal archive path renamed, one guard name lost (coverage merged elsewhere), one guard name without successor, relocated engine path.

## 050-proactive-flow-trigger

- **Refs**: 121 unique concrete — **97 alive / 0 archived / 24 dead** (5 anchor-move, 19 substantive; 12 substantive are frozen-baseline test names).
- **Registry row**: **resolves** — row 050, Spec Path `.specify/specs/050-proactive-flow-trigger/requirements.md`, Detail `.specify/features/050-proactive-flow-trigger.md` (exists).
- **Guards**: 14 named test files; **12/14 exist**. Missing names, both merged with explicit in-file notes:
  - `tests/contract/test_proactive_trigger_discipline_doc.py` (`quickstart.md:262`, `tasks.md:92,95`, `contracts/discipline-doc.md:5`) -> merged into `tests/contract/test_proactive_trigger_section.py` (`:399`).
  - `tests/contract/test_confirmation_gates_execution_report.py` (`feature-ref.md:53`) -> merged into `tests/contract/test_confirmation_gates_sweep.py` (`:11`).
  - Twelve frozen-baseline names in `baseline-failed.txt` are dead as files (same consolidation wave as 037).
- **Broken items**:
  - `.specify/specs/050-proactive-flow-trigger/plan.md:195` (also `data-model.md:21`) `.specify/docs/target-structure.md` -> no target anywhere in the repo
  - `.specify/specs/050-proactive-flow-trigger/requirements.md:50` `.specify/memory/feedback/index.json` -> store is now per-entry files (`.specify/memory/feedback/<timestamp>-<command>.md`); no `index.json`
  - `.specify/specs/050-proactive-flow-trigger/plan.md:29` (also `review.md:238`, `requirements.md:45,258`) `.specify/memory/constitution.md` -> `[anchor-move]` `.specify/constitution.md`
  - `.specify/specs/050-proactive-flow-trigger/plan.md:161` (also `tasks.md:5,224`, `feature-ref.md:11`) `.specify/memory/features.md` -> `[anchor-move]` `.specify/features.md`
  - `.specify/specs/050-proactive-flow-trigger/tasks.md:224` (also `feature-ref.md:78`, `requirements.md:24,264`) `.specify/memory/features/050.md` -> `[anchor-move]` `.specify/features/050-proactive-flow-trigger.md`
  - `.specify/specs/050-proactive-flow-trigger/verification.md:60` `.specify/memory/glossary.md` -> `[anchor-move]` `.specify/glossary.md`
  - `.specify/specs/050-proactive-flow-trigger/plan.md:126` (also `verification.md:63`, `tasks.md:24`) `.specify/memory/tools.md` -> `[anchor-move]` `.specify/tools.md`
  - Two guard names above -> merged successors (paths dead, coverage alive).
  - `baseline-failed.txt` lines 2–44: twelve dead frozen-baseline test names.
- **Spot-checks**:
  1. PASS — `scripts/python/trigger-utils.py` ships the 11-action closed set (`ACTIONS` tuple at `:169-171`; schema override at `:172`).
  2. PASS — `shared/guidelines/proactive-trigger.md` and `templates/proactive-trigger-seed.json` exist.
  3. PASS — the runtime state store exists: `.specify/memory/trigger/index.json` (54,766 B) + `telemetry.jsonl` (live, recently written).
- **Verdict**: **BROKEN** — anchor-move references, one never-existent analogy path, one stale store example; every functional guard remains alive under a merged filename.

## 063-review-p1-governance

- **Refs**: 339 unique concrete — **329 alive / 0 archived / 10 dead** (4 anchor-move, 6 substantive; all substantive are in notes or one quickstart command).
- **Registry row**: **resolves** — row 063, Spec Path `.specify/specs/063-review-p1-governance/requirements.md`, Detail `.specify/features/063-review-p1-governance.md` (exists).
- **Guards**: 16 named test files; **16/16 exist** (including `test_baseline_preflight_contract.py`, `test_clause_coverage.py`, `test_review_p1_checklist_governance.py`, `test_review_p1_recheck_waiver.py`, `test_review_p1_review_loop.py`, `test_evidence_binding_contract.py`).
- **Broken items**:
  - `.specify/specs/063-review-p1-governance/quickstart.md:40` `.specify/templates/commands/analyze.md` -> `.specify/templates/` has no `commands/`; live template is `templates/commands/analyze.md`
  - `.specify/specs/063-review-p1-governance/notes/pre-change-measurements.md:69` (also `:74`) `.specify/specs/062-humanize-command/coverage-baseline.txt` -> still absent (the note itself records `MISSING`; a disclosed pre-change gap)
  - `.specify/specs/063-review-p1-governance/review.md:121` `.specify/specs/063-review-p1-governance/waivers.md` -> absent (the spec’s own negative existence check, `ABSENT`)
  - `.specify/specs/063-review-p1-governance/notes/baseline-mirror-check.txt:141` `.specify/agents/templates/sdd-executor.agent.md` -> removed by Feature 085 (generic executor deleted)
  - `.specify/specs/063-review-p1-governance/notes/baseline-mirror-check.txt:66` `.specify/skills/think-skills/SKILL.md` -> removed; live closest `skills/external/merge-skills`
  - `.specify/specs/063-review-p1-governance/notes/baseline-mirror-check.txt:125` `.specify/skills/internal/study-project/references/uml-visualization-guide.md` -> renamed to the `study-code` skill (git `cde73a99f`)
  - `.specify/specs/063-review-p1-governance/plan.md:27` (also `tasks.md:9`) `.specify/memory/constitution.md` -> `[anchor-move]` `.specify/constitution.md`
  - `.specify/specs/063-review-p1-governance/verification.md:606` (also `tasks.md:5,250,256`) `.specify/memory/features.md` -> `[anchor-move]` `.specify/features.md`
  - `.specify/specs/063-review-p1-governance/verification.md:607` (also `tasks.md:250,256`, `review.md:14`) `.specify/memory/features/063.md` -> `[anchor-move]` `.specify/features/063-review-p1-governance.md`
  - `.specify/specs/063-review-p1-governance/quickstart.md:59` (also `tasks.md:75,128,387`) `.specify/memory/register.md` -> `[anchor-move]` `.specify/register.md`
- **Spot-checks**:
  1. PASS — `scripts/python/clause_extract.py` honors ASCII + full-width parentheses (`:127-128,154`) (claim: FR-001 / `plan.md:27`).
  2. PASS — `scripts/python/account-clause-coverage.py` implements `coverage-baseline-delta` and the `baseline-missing` verdict (`:36-51`) (claim: F1 coverage lane).
  3. PASS — `templates/commands/review.md:184` carries the same-commit `REC-…` → `.specify/register.md` obligation (claim: F3 / C-11).
- **Verdict**: **BROKEN** — one wrong quickstart template path, anchor-move references, and frozen notes pointing at files later removed by 085/078/study-code; no live guard lost.

## 074a-authorized-routing

- **Refs**: 577 unique concrete — **565 alive / 0 archived / 12 dead** (4 anchor-move, 8 evidence/sandbox).
- **Registry row**: **resolves by binding** — the slice adds no row of its own by design (`feature-ref.md` §1); bound Feature 074 row exists with Spec Path `.specify/specs/074-goal-team-sdd-unification/requirements.md` (exists) and Detail `.specify/features/074-goal-team-sdd-unification.md` (exists).
- **Guards**: 20 named test files; **20/20 exist** (`test_sdd_routing_engine.py`, `test_sdd_authorization.py`, `test_nested_sdd_invocation.py`, `test_sdd_routing_definitions.py`, `test_sdd_invocation_governance.py`, `test_nested_run_report.py`, `tests/fixtures/nested_sdd.py`, and the shared surface pins).
- **Broken items**:
  - `.specify/specs/074a-authorized-routing/plan.md:82` (also `tasks.md:66`, `requirements.md:283`) `.specify/memory/constitution.md` -> `[anchor-move]` `.specify/constitution.md`
  - `.specify/specs/074a-authorized-routing/code-review.md:16` (also `:149`, `tasks.md:201`, `feature-ref.md:13`) `.specify/memory/features.md` -> `[anchor-move]` `.specify/features.md`
  - `.specify/specs/074a-authorized-routing/plan.md:87` (also `code-review.md:17,152`, `tasks.md:201`) `.specify/memory/features/074.md` -> `[anchor-move]` `.specify/features/074-goal-team-sdd-unification.md`
  - `.specify/specs/074a-authorized-routing/review.md:404` `.specify/memory/register.md` -> `[anchor-move]` `.specify/register.md`
  - `.specify/specs/074a-authorized-routing/notes/quickstart-run.md:494` `.specify/memory/registers` -> typo/recorded command; no target (register is `.specify/register.md`)
  - `.specify/specs/074a-authorized-routing/notes/red-first-evidence.md:87` `.specify/agents/execution/20261029T000000Z-routing-verdict-d1.md` -> sandbox fixture, absent
  - `.specify/specs/074a-authorized-routing/notes/red-first-evidence.md:88` `.specify/agents/instances/seat-allowed.agent.md` (also `quickstart-run.md:987,999`) -> sandbox fixture, absent
  - `.specify/specs/074a-authorized-routing/notes/red-first-evidence.md:89` `.specify/agents/instances/seat-forbidden.agent.md` -> sandbox fixture, absent
  - `.specify/specs/074a-authorized-routing/notes/red-first-evidence.md:90` `.specify/goal/fixture-goal/goal.md` -> sandbox fixture, absent (goal archive now `.specify/anchoring/`)
  - `.specify/specs/074a-authorized-routing/notes/red-first-evidence.md:91` `.specify/teams/fixture-team/team.md` -> sandbox fixture, absent
  - `.specify/specs/074a-authorized-routing/notes/full-baseline-run.txt:471` `.specify/teams/demo-team/runs/20260101T000000Z-report.md` -> sandbox path in captured output
  - `.specify/specs/074a-authorized-routing/notes/full-baseline-run.txt:704` `skills/external/humanize/SKILL.md` -> renamed `skills/external/humanize-conclusion/SKILL.md`
- **Spot-checks**:
  1. PASS — `scripts/python/sdd-route.py` exposes exactly `route` / `authorize` / `golden` (`--help`, `:2596`-equivalent argparse) (claim: `plan.md:21`).
  2. PASS — `shared/definitions/sdd-routing-definitions.md` is present as the single vocabulary owner.
  3. PASS — verification evidence is hash-bound and still matches: `green-t016.txt`, `golden-rows.txt`, `green-t016-demo.txt`, `green-t025.txt` all reproduce their recorded `sha256` (`verification.md:39-56`).
- **Verdict**: **BROKEN** — anchor-layout references and sandbox-fixture paths only; the implementation surface, all 20 guards, and evidence integrity are intact.

## 085-sdd-temporary-goal-team

- **Refs**: 510 unique concrete — **494 alive / 0 archived / 16 dead** (4 anchor-move, 12 substantive/evidence).
- **Registry row**: **resolves** — row 085, Spec Path `.specify/specs/085-sdd-temporary-goal-team/requirements.md`, Detail `.specify/features/085-sdd-temporary-goal-team.md` (exists).
- **Guards**: 12 named test/fixture files; **9/12 exist**. Missing names:
  - `tests/contract/test_stage_seat_map.py` (`tasks.md:70`) -> no file; stage-seat schema is now exercised by `tests/contract/test_temp_team_schema.py` (`stage_seats:` parsing) and `tests/contract/test_stage_class_wiring.py`.
  - `tests/contract/test_unified_turn_budget.py` (`tasks.md:78`) -> no file; budget assertions are distributed across `test_agent_render.py`, `test_roster_reporter_seat.py`, `test_agent_chain_guards.py`, `test_agent_dispatch_mechanism.py`.
  - `tests/fixtures/temp_sdd_team.py` (`tasks.md:42`) -> no file; the current 085 tests read the live `.specify/teams/085-sdd-temporary-goal-team/team.md` instead.
- **Broken items**:
  - `.specify/specs/085-sdd-temporary-goal-team/quickstart.md:13` (also `:23`, `data-model.md:47`, `requirements.md:38`) `.specify/goal` -> renamed `.specify/anchoring/`
  - `.specify/specs/085-sdd-temporary-goal-team/feature-ref.md:12` (also `:39`) `.specify/memory/features.md` -> `[anchor-move]` `.specify/features.md`
  - `.specify/specs/085-sdd-temporary-goal-team/plan.md:170` `.specify/memory/features/064.md` -> `[anchor-move]` `.specify/features/064-subagent-concurrency.md`
  - `.specify/specs/085-sdd-temporary-goal-team/plan.md:170` `.specify/memory/features/070.md` -> `[anchor-move]` `.specify/features/070-subagent-task-teams.md`
  - `.specify/specs/085-sdd-temporary-goal-team/plan.md:43` (also `feature-ref.md:11,39`, `checklists/requirements.md:5`) `.specify/memory/features/085.md` -> `[anchor-move]` `.specify/features/085-sdd-temporary-goal-team.md`
  - `.specify/specs/085-sdd-temporary-goal-team/test-evidence/live-dogfood.txt:3` `.specify/specs/084-dogfood/goal/084-dogfood/goal.md` -> sandbox path, absent
  - `.specify/specs/085-sdd-temporary-goal-team/quickstart.md:57` `.specify/specs/085-sdd-temporary-goal-team/checkpoints/closure.md` -> no closure checkpoint; existing set is `01-requirements.md` … `05-live-dogfood.md`
  - `.specify/specs/085-sdd-temporary-goal-team/tasks.md:26` `test-evidence/final-failed.txt` -> absent; nearest live `test-evidence/full-suite-final-failed.txt`
  - `.specify/specs/085-sdd-temporary-goal-team/verification.md:11` `test-evidence/full-suite-pre-review-failed.txt` -> absent; `test-evidence/full-suite-final-failed.txt` exists
  - `.specify/specs/085-sdd-temporary-goal-team/test-evidence/full-suite-final.txt:595` `.specify/teams/demo-team/runs/20260101T000000Z-report.md` -> sandbox path in captured output
  - `.specify/specs/085-sdd-temporary-goal-team/test-evidence/full-suite-final.txt:802` `skills/external/humanize/SKILL.md` -> `skills/external/humanize-conclusion/SKILL.md`
  - `.specify/specs/085-sdd-temporary-goal-team/test-evidence/full-suite-final.txt:802` `skills/external/humanize/references/report-shape.md` -> `skills/external/humanize-conclusion/references/report-shape.md`
  - `.specify/specs/085-sdd-temporary-goal-team/test-evidence/full-suite-final.txt:802` `skills/external/humanize/references/run-mode.md` -> `skills/external/humanize-conclusion/references/run-mode.md`
  - Three missing guard/fixture names above.
- **Spot-checks**:
  1. PASS — the generic `agents/sdd-executor.agent.md` is gone; stage-specific roles are live (14 `agents/sdd-*.agent.md` files) (claim: `plan.md:20`).
  2. PASS — `run-turn-budget: 500` is uniform across all 17 root agent definitions and every `.specify/agents/` template/instance checked (claim: `plan.md:20`).
  3. PASS — `goal-utils.py resolve-scope` exists (`scripts/python/goal-utils.py:2598`) and the ten paths in the recorded smoke command (`verification.md:22`) all exist.
- **Verdict**: **BROKEN** — goal archive rename, three guard/fixture names without surviving files, two stale evidence filenames, one never-created checkpoint, plus anchor-move references.

## Batch Summary

| Spec | Refs | Alive | Archived | Dead | Verdict |
|------|-----:|------:|---------:|-----:|---------|
| 024-agent-env-config | 25 | 19 | 0 | 6 | **BROKEN** |
| 037-goal-registry | 91 | 63 | 0 | 28 | **BROKEN** |
| 050-proactive-flow-trigger | 121 | 97 | 0 | 24 | **BROKEN** |
| 063-review-p1-governance | 339 | 329 | 0 | 10 | **BROKEN** |
| 074a-authorized-routing | 577 | 565 | 0 | 12 | **BROKEN** |
| 085-sdd-temporary-goal-team | 510 | 494 | 0 | 16 | **BROKEN** |

Dead-by-cause across the batch: anchor-layout moves 22; renamed/removed skills or engines 8; frozen-baseline test names 21; sandbox/fixture evidence paths 18; genuinely absent live artifacts 20 (including 5 named guards).

ANOMALY: master advanced mid-audit to `6fb8093c4`, merging `rename-anchors`; all six specs were re-measured post-merge, and every `.specify/memory/*` anchor pointer is now dead-by-move (`.specify/{features,constitution,glossary,register,tools}.md`, `.specify/features/<ID>-<slug>.md`), with two feature-detail filename/content mismatches found (row 024: file named `agent-env-config`, content “Specification Workspace Versioning”; row 041: file named `refactor-feedback-probe`, content “Goal Registry”).

SPEC-AUDIT-LIVE-11-DONE
