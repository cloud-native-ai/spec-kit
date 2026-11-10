# Read-only live-spec audit — batch 8

- **Date**: 2026-11-10
- **Tree**: main `/storage/project/cloud-native-ai/spec-kit`, branch `master`, HEAD `f5ac8e654`
- **Mode**: strictly read-only; no subagents; no commits. Only write: this file.
- **Specs**: 020-speckit-todo-command, 034-evidence-infra, 047-feedback-introspection,
  060-decompose-subagent-dispatch, 072-client-self-improvement, 082-self-explanatory-integration.

## Method

1. Extracted every unique repository path matching `(\.specify|scripts|skills|templates|shared|tests|src|docs)/…`
   from each spec's `.md` / `.txt` artifacts (requirements, plan, tasks, contracts, data-model, quickstart,
   verification, notes, checklists, evidence logs) with a strict left boundary so substring/ellipsis tails
   (`.../x/scripts/foo.py`, `skills/…` inside a longer `-skills/…` token) do not register.
2. Excluded non-repository candidates: glob patterns, truncation artifacts (trailing `-`, `...`), illustrative
   example workspaces, deliberate test negatives, synthetic `/tmp` workspaces, and transient `.specify/.tmp`
   scratch.
3. Classified each remaining path: **alive** (exists at the written path now), **archived-elsewhere**
   (resolves only under `.specify/archive/`), **dead** (no target). Within dead, `rename` = the written
   `memory/` anchor path no longer exists but a live successor exists at the `.specify/` root (layout rename);
   `other` = no target.
4. Registry: parsed the table row bound to each spec from `.specify/features.md`, checked the
   Feature Details and Spec Path cells.
5. Guards: every `tests/**/*.py|*.sh` path named by the artifacts, checked for existence.
6. Spot-checked three implementation claims per spec (file / symbol-or-command / behaviour surface).

> **Layout change during the audit**: the anchor rename (`memory/` → `.specify/` root) landed in the main
> tree mid-run (commit `6fb8093c4`). `.specify/memory/{features,constitution,glossary,register,tools}.md` and
> `.specify/memory/features/<ID>.md` are gone; `.specify/{features,constitution,glossary,register,tools}.md`
> and `.specify/features/<ID>-<slug>.md` exist. Counts below are post-rename. `AGENTS.md` was also rewritten
> mid-run to the new anchors.

---

## 020-speckit-todo-command

**Binding**: registry Feature **025 — Todo Command**.
**Counts**: 23 considered refs | 18 alive | 0 archived | 5 dead (2 rename, 3 other) |
15 raw candidates excluded (quickstart/contract example workspace paths).

**Broken**

- `.specify/specs/020-speckit-todo-command/tasks.md:19` → `.specify/memory/features.md` missing; rename successor `.specify/features.md`.
- `.specify/specs/020-speckit-todo-command/tasks.md:19` → `.specify/memory/features/025.md` missing; rename successor `.specify/features/025-agent-skill-enablement.md`.
- `tasks.md:46` (also 47, 48, 71, 72, 73, …) → `.specify/scripts/bash/search-todo.sh` missing; the scanner was rewritten as `.specify/scripts/python/search-todo.py` (`--json`, `--exclude`, `--context-depth`, `--context-only-headings` all live there). Pre-consolidation pointer → dead.
- `tasks.md:32` → `tests/fixtures/todo-workspaces/oversized/backlog.md` missing; oversized fixture is split as `part1.md`…`part4.md`.
- `tasks.md:34` → `tests/integration/test_speckit_todo_prompt.py` missing; no replacement. Prompt wiring is covered by `tests/contract/test_todo_in_context_wiring.py`, which the spec does not name.

**Guards**

- Alive: `tests/contract/test_search_todo_contract.py` (D-1/D-8/D-2/D-5, C-1–C-3 context extraction).
- Missing: `tests/integration/test_speckit_todo_prompt.py`.
- `tests/auth/test_login.py` / `tests/integration/test_session_flow.py` are quickstart example paths, not guards.

**Spot-checks**

1. File: `.specify/scripts/python/search-todo.py` exists; `--help` returns the documented options.
2. Behaviour: `search-todo.py --json tests/fixtures/todo-workspaces/valid` → 8 blocks, 0 malformed, 6 files scanned; `valid/docs/auth.md:6` carries a ` ```SPECKIT TODO ` fence.
3. Contract: `tests/contract/test_search_todo_contract.py` exists and still labels the script "search-todo.py" (docstrings at lines 60/66 still say `.sh` — stale prose only).

**Registry**: PASS. Row 025 Spec Path `.specify/specs/020-speckit-todo-command/requirements.md` exists; Feature Details `.specify/features/025-agent-skill-enablement.md` exists and its header identifies Feature ID 025 / "Todo Command". Slug suffix "agent-skill-enablement" does not describe this feature (post-rename naming anomaly).

**Verdict: BROKEN** — 3 substantive dead pointers (script path, fixture file, integration guard) plus 2 rename moves.

---

## 034-evidence-infra

**Binding**: registry Feature **038 — Evidence Infrastructure**.
**Counts**: 85 considered refs | 64 alive | 0 archived | 21 dead (3 rename, 18 other) |
2 excluded (a tree-listing `scripts/agent-lint/`, a truncated `…/ev-` prefix).

**Broken**

- `.specify/specs/034-evidence-infra/plan.md:36` → `.specify/memory/constitution.md` missing; rename successor `.specify/constitution.md`.
- `tasks.md:5` → `.specify/memory/features.md` missing; rename successor `.specify/features.md`.
- `feature-ref.md:4` → `.specify/memory/features/038.md` missing; rename successor `.specify/features/038-goal-target.md`.
- `data-model.md:76` → `.specify/memory/evidence/index.json` absent. The engine retired it: `evidence-utils.py:24` documents index.json as a read-only fallback retired on read (`INDEX_NAME` at line 97). The data-model/contract sentence "MUST 含 store/updated/entries[]" now contradicts the implementation.
- `quickstart.md:20` → `.specify/memory/feedback/index.json` absent; feedback is a per-entry store with scan-on-read, `feedback-utils.py` keeps only a legacy fallback. Quickstart's stated verification target no longer exists.
- `dogfood-project-loop.md:34` → `.specify/skills/draw-echarts/yuque-workspace/` absent; the draw-echarts skill no longer exists in the tree.
- `baseline-failed.txt` lines 1–82: 15 missing test modules — `tests/contract/test_agent_specific_config_commands.py`, `test_create_new_skill_contract.py`, `test_skill_home_workdir_template.py`, `test_tools_modify.py`, `test_tools_webhook.py`, `tests/integration/test_context_injection.py`, `tests/unit/test_agent_deprecated_terms.py`, `test_agent_reference_integrity.py`, `test_ai_tools_cli_help.py`, `test_claude_refresh_helpers.py`, `test_claude_support_matrix.py`, `test_claude_support_surfaces.py`, `test_qoder_refresh_helpers.py`, `test_qoder_support_matrix.py`, `test_qoder_support_surfaces.py`. (Historical failure log, not a live guard roster.)

**Guards**

- Alive: `tests/contract/test_evidence_findings_schema.py`, `test_evidence_step_conformance.py`, `test_evidence_utils_cli.py`, `test_dogfooding_practice.py`, `test_handoff_chain.py`, `test_tools_define.py`, `test_tools_view.py`, `tests/integration/test_evidence_compare_verdict.py`, `test_evidence_python_lanes.py`, `test_tools_definition_flow.py`, `test_tools_invoke_flow.py`, `test_tools_modify_flow.py`, `test_zero_sdd_workflow_references.py`, `tests/js/run.sh`, `tests/unit/test_tier_classification.py`.
- Missing: none of the guard tests named in tasks/contracts/verification is missing; all 15 missing modules occur only in `baseline-failed.txt`.

**Spot-checks**

1. File: `.specify/scripts/python/evidence-utils.py` exists; `scripts/js/better-harness/UPSTREAM.md` exists with `## Subset Manifest`, `## Exclusions`, `## Local Modifications`, `## Resync Policy`.
2. Command: `evidence-utils.py --help` exposes `--action {doctor,collect,list,latest,compare}`, matching the contract CLI.
3. Behaviour: `shared/workflow/evidence-step.md` carries the Unobserved red line (line 8) and the seven-state vocabulary (line 11); `.specify/shared/workflow/evidence-step.md` mirror exists.

**Registry**: PASS. Row 038 Spec Path `.specify/specs/034-evidence-infra/requirements.md` exists; Feature Details `.specify/features/038-goal-target.md` exists and its header identifies Feature ID 038 / "Evidence Infrastructure". Slug suffix "goal-target" is wrong for this feature (post-rename naming anomaly).

**Verdict: BROKEN** — 18 non-rename dead refs, including two live contracts whose stated store (index.json) no longer exists.

---

## 047-feedback-introspection

**Binding**: `feature-ref.md` binds this requirement to registry Feature **028 — Feedback Mechanism** (child requirement, not a standalone row).
**Counts**: 64 considered refs | 37 alive | 0 archived | 27 dead (3 rename, 24 other) |
2 excluded (an example `templates/commands/x.md`, prose `templates/scripts`).

**Broken**

- `.specify/specs/047-feedback-introspection/plan.md:42` → `.specify/memory/constitution.md` missing; rename successor `.specify/constitution.md`.
- `tasks.md:9` → `.specify/memory/features.md` missing; rename successor `.specify/features.md`.
- `plan.md:95` → `.specify/memory/features/028.md` missing; rename successor `.specify/features/028-sdd-workflow-refactor.md`.
- `data-model.md:13` → `.specify/memory/feedback/index.json` absent; per-entry feedback store (scan-on-read) replaced it; `feedback-utils.py` retains only a legacy fallback.
- `contracts/introspection-report.md:56` → `skills/improve-skills/SKILL.md:42` missing; skill now at `skills/external/improve-skills/SKILL.md` (mirror `.specify/skills/improve-skills/SKILL.md`). The cited line number is also unverifiable at the new path.
- `contracts/introspection-report.md:56` → `templates/skills/SKILL-template.md:18` missing; `templates/skills/` does not exist.
- `review.md:149–151` → `.specify/skills/browser-utils/{SKILL.md, references/trusted-browser-launch.md, scripts/chrome_open_trust.sh}` missing; Feature 048 relocated browser-utils to xuanji-extension.
- `tasks.md:77` → `tests/contract/test_feedback_command_introspect.py` missing (guard named in tasks, not just a baseline log).
- `baseline-failed.txt` lines 1–47: 17 missing modules — `tests/contract/test_agent_specific_config_commands.py`, `test_browser_site_exclusions.py`, `test_browser_site_memory.py`, `test_create_new_skill_contract.py`, `test_skill_home_workdir_template.py`, `test_token_efficiency_remediation_program_first.py`, `test_token_efficiency_remediation_summary_first.py`, `tests/integration/test_context_injection.py`, `test_team_create_flow.py`, `tests/unit/test_agent_deprecated_terms.py`, `test_agent_reference_integrity.py`, `test_claude_refresh_helpers.py`, `test_claude_support_matrix.py`, `test_claude_support_surfaces.py`, `test_qoder_refresh_helpers.py`, `test_qoder_support_matrix.py`, `test_qoder_support_surfaces.py`.

**Guards**

- Alive: `tests/contract/test_feedback_introspection_engine.py`, `test_feedback_introspection_report.py`, `test_feedback_utils_cli.py`, `test_no_nested_skills.py`, `test_scripts_distribution_parity.py`, `test_shared_reference_rewrite.py`, `test_spec_feature_binding_integrity.py`, `test_summarize_project_prompt_assets.py`, `test_sync_mirrors_only.py`, `test_dogfooding_practice.py`, `tests/integration/test_zero_sdd_workflow_references.py`, `tests/script_api.py`.
- Missing: `tests/contract/test_feedback_command_introspect.py` (tasks.md:77) plus the 17 baseline-log modules above.
- Ten of the 12 named guard modules survive; the two introspection guard modules (`…_engine`, `…_report`) are alive.

**Spot-checks**

1. File: `.specify/scripts/python/feedback-utils.py` exists; `.specify/memory/feedback/introspection/` exists (report sub-directory is live).
2. Command: `feedback-utils.py --help` shows actions `introspect-register`, `dispose`, `package` and flag `--include-introspection`, matching contracts C-1…C-12.
3. Behaviour: `tests/contract/test_feedback_introspection_engine.py:25` still invokes `--action introspect-register`; the report-shape contract's two evidence anchors (`skills/improve-skills/SKILL.md:42`, `templates/skills/SKILL-template.md:18`) are both dead.

**Registry**: PASS with note. Row 028 Spec Path `.specify/specs/027-feedback-mechanism/requirements.md` exists; Feature Details `.specify/features/028-sdd-workflow-refactor.md` exists and its header identifies Feature ID 028 / "Feedback Mechanism"; `.specify/features/028…md:75` lists `.specify/specs/047-feedback-introspection/requirements.md` under Related Specifications. No row's Spec Path points directly at 047 (by design: child requirement), and the detail slug "sdd-workflow-refactor" is wrong for Feature 028.

**Verdict: BROKEN** — 24 non-rename dead refs including a named guard and both contract evidence anchors.

---

## 060-decompose-subagent-dispatch

**Binding**: registry Feature **060** (same ID).
**Counts**: 77 considered refs | 74 alive | 0 archived | 3 dead (1 rename, 2 other) |
1 excluded (truncated `.specify/specs/060-`).

**Broken**

- `.specify/specs/060-decompose-subagent-dispatch/plan.md:27` → `.specify/memory/constitution.md` missing; rename successor `.specify/constitution.md`.
- `plan.md:96` → `.specify/agents/templates/sdd-executor.agent.md` missing. The capability template was replaced by the executor family (`sdd-plan-executor.agent.md`, `sdd-implement-executor.agent.md`, …). Supplementary out-of-prefix pointer: root `agents/sdd-executor.agent.md` (tasks.md:58, contracts/skill-enhancements.md:8,13) is also missing.
- `tasks.md:106` → `.specify/specs/060-decompose-subagent-dispatch/notes/quickstart-run.md` missing; `notes/` holds only baseline-failed.txt, pre-change-measurements.md, red-first-evidence.md.

**Guards**

- Alive (all 23 named contract tests): `test_agent_dispatch_mechanism.py`, `test_ask_record_repeat.py`, `test_clause_coverage.py`, `test_clause_forms.py`, `test_compile_propagation_order.py`, `test_confirmation_gates_sweep.py`, `test_constitution_double_landing.py`, `test_criterion_subject.py`, `test_dogfooding_practice.py`, `test_exec_quant_engine.py`, `test_fast_fail_discipline.py`, `test_glossary_mechanism.py`, `test_instructions_section_propagation.py`, `test_neutrality_budget.py`, `test_one_source_of_truth.py`, `test_proactive_trigger_section.py`, `test_scripts_distribution_parity.py`, `test_task_complexity_rubric.py`, `test_token_efficiency_discipline.py`, `test_trigger_engine.py`, `test_user_facing_comprehension_doc.py`, `test_user_facing_comprehension_section.py`, `test_wrap_up_wording_gate_safe.py`.
- Missing: none.

**Spot-checks**

1. File: `skills/internal/run-agent/SKILL.md`, `skills/external/sdd-loop-driver/references/dispatch-recipes.md`, `shared/definitions/subagent-definitions.md` all exist; `.specify` mirrors of the latter two exist.
2. Symbol: `run-agent/SKILL.md:50` carries "Execution Topology (拓扑声明输入)"; line 45–48 define the Execution layer.
3. Guard surface: `tests/contract/test_agent_dispatch_mechanism.py` exists. The claimed `sdd-executor.agent.md` mirror pair (C-14 byte-identity) has no file on either side.

**Registry**: PASS. Row 060 Spec Path `.specify/specs/060-decompose-subagent-dispatch/requirements.md` exists; Feature Details `.specify/features/060-decompose-subagent-dispatch.md` exists.

**Verdict: BROKEN** — the feature's central capability template and the mandated quickstart evidence file no longer exist.

---

## 072-client-self-improvement

**Binding**: registry Feature **072** (same ID).
**Counts**: 180 considered refs | 174 alive | 0 archived | 6 dead (4 rename, 2 other) |
15 excluded (fixture-project paths `072-demo`, `src/app.py`, prose directory enumerations, globs/truncations, quickstart fixture entries).

**Broken**

- `.specify/specs/072-client-self-improvement/plan.md:35` → `.specify/memory/constitution.md` missing; rename successor `.specify/constitution.md`.
- `code-review.md:32` → `.specify/memory/features.md` missing; rename successor `.specify/features.md`.
- `code-review.md:33` → `.specify/memory/features/072.md` missing; rename successor `.specify/features/072-client-self-improvement.md`.
- `notes/red-first-evidence.md:69` → `.specify/memory/register.md` missing; rename successor `.specify/register.md`.
- `plan.md:96` → `scripts/git-delta-review.sh` missing; the script lives at `skills/internal/code-review/scripts/git-delta-review.sh` (mirror `.specify/skills/internal/code-review/scripts/git-delta-review.sh`). Pre-consolidation pointer → dead.
- `plan.md:21` (also `requirements.md:138`, `data-model.md:42`) → `.specify/memory/feedback/probes/` absent in this repo. Dead-by-design: the store is created lazily by `probe-inject` at first external-probe injection (registry row 072 records this expected absence). `notes/quickstart-run.md:35` cites `…/probes/ext-myteam-review-loop.md` from a temp fixture run, excluded as fixture-relative.

**Out-of-prefix archived citation**: `coverage-baseline.txt:21–27` cites `017-consolidate-draft-skills/contracts/skill-format.md#C-001…C-007`; that spec is archived — resolves at `.specify/archive/specs/017-consolidate-draft-skills/contracts/skill-format.md`. Not counted in the table (outside the declared path prefixes).

**Guards**

- Alive (all 34 named test/fixture paths): the five client contract tests `test_client_{capture,armed_state,package_exclusion,improve_loop,metrics}.py` plus `test_client_guard_sweep.py`, `tests/fixtures/client_project.py`, `tests/fixtures/review_git_repo.py`, and the shared probe/evidence/determination guards.
- Missing: none.

**Spot-checks**

1. File: `skills/internal/code-review/scripts/git-delta-review.sh` exists; `.specify/skills/internal/code-review/SKILL.md` exists.
2. Symbol: `git-delta-review.sh:1425` defines `cmd_capture()`; the capture contract block starts at line 1347. `scripts/python/probe-utils.py:204` defines `_CUSTOM_UNIT_RE = ^custom:[a-z0-9._/-]+$`.
3. Behaviour guard: `tests/contract/test_client_capture.py` exists; `.specify/skills/internal/manage-feedback/SKILL.md` and `references/path-a-digest.md` exist.

**Registry**: PASS. Row 072 Spec Path `.specify/specs/072-client-self-improvement/requirements.md` exists; Feature Details `.specify/features/072-client-self-improvement.md` exists.

**Verdict: BROKEN** — the plan's script path and the probe-store pointer are dead at the written locations (4 rename moves also count).

---

## 082-self-explanatory-integration

**Binding**: registry Feature **082** (same ID).
**Counts**: 599 considered refs | 588 alive | 0 archived | 11 dead (5 rename, 6 other) |
20 excluded (illustrative `docs/concepts/some-other-page.md`, `shared/definitions/x.md`, deliberate test negatives `absent-by-construction.md` / `removed-by-m6.md`, synthetic `/tmp` workspace paths, 8 transient `.specify/.tmp/082-*` scratch paths, globs/truncations).

**Broken**

- `.specify/specs/082-self-explanatory-integration/quickstart.md:20` → `.specify/memory/constitution.md` missing; rename successor `.specify/constitution.md`.
- `code-review.md:19` → `.specify/memory/features.md` missing; rename successor `.specify/features.md`.
- `plan.md:51` → `.specify/memory/features/082.md` missing; rename successor `.specify/features/082-self-explanatory-integration.md`.
- `plan.md:29` → `.specify/memory/glossary.md` missing; rename successor `.specify/glossary.md`.
- `code-review.md:23` → `.specify/memory/register.md` missing; rename successor `.specify/register.md`.
- `test-evidence/final-suite-20261105.txt:738` → `skills/external/humanize/SKILL.md`, `…/references/report-shape.md`, `…/references/run-mode.md` missing; the skill is now `skills/external/humanize-conclusion/` (mirror `.specify/skills/humanize-conclusion/`). Historical test-log refs, but dead.
- `test-evidence/plan-stage-checks.md:117` → `.specify/instructions.md-2026-11-05-112729` missing (git-ignored backup, cleaned).
- `notes/quickstart-run.md:10` → `.specify/instructions.md-2026-11-05-135949` missing (same).
- `requirements.md:27` → `.specify/memory/session/interview-wangwenshengyi.md` missing. Assumption A8's evidence anchor (the interview ledger for the zero-marker ruling) no longer resolves; no replacement file exists in `.specify/memory/session/`.

**Guards**

- Alive: every named guard path resolves, including `tests/contract/test_self_explanatory_constitution.py`, `test_self_explanatory_distribution.py`, `test_self_explanatory_glossary.py`, `test_instructions_size_budget.py`, `test_mirror_parity_suite.py`, `test_shared_reference_rewrite.py`, `test_shared_reference_directory.py`, `test_expression_faces.py`, `test_expression_gates_doc.py`, plus the integration suite (`test_ai_tools_*`, `test_claude_*`).
- Missing: none (0 of the named test paths).

**Spot-checks**

1. File: `shared/definitions/self-explanatory-definitions.md` exists with the Owner declaration; `.specify/shared/definitions/self-explanatory-definitions.md`, `.specify/shared/guidelines/self-explanatory.md`, `.specify/shared/workflow/best-practice-optimization.md` all exist.
2. Symbol: `.specify/constitution.md:405` carries `### XIX. Self-Explanatory Structure (不言自明)`; line 63 records the constitution-template propagation (principles 17 → 18).
3. Behaviour surface: `.specify/instructions.md:89` carries `## Self-Explanatory Structure (不言自明)`; `tests/contract/test_instructions_size_budget.py` exists as the budget guard.

**Registry**: PASS. Row 082 Spec Path `.specify/specs/082-self-explanatory-integration/requirements.md` exists; Feature Details `.specify/features/082-self-explanatory-integration.md` exists.

**Verdict: BROKEN** — 6 non-rename dead refs (renamed skill, two cleaned backups, one lost interview ledger) plus 5 rename moves.

---

## Batch summary

| Spec | Refs | Alive | Archived | Dead | Verdict |
|------|------|-------|----------|------|---------|
| 020-speckit-todo-command | 23 | 18 | 0 | 5 (2 rename + 3 other) | BROKEN |
| 034-evidence-infra | 85 | 64 | 0 | 21 (3 rename + 18 other) | BROKEN |
| 047-feedback-introspection | 64 | 37 | 0 | 27 (3 rename + 24 other) | BROKEN |
| 060-decompose-subagent-dispatch | 77 | 74 | 0 | 3 (1 rename + 2 other) | BROKEN |
| 072-client-self-improvement | 180 | 174 | 0 | 6 (4 rename + 2 other) | BROKEN |
| 082-self-explanatory-integration | 599 | 588 | 0 | 11 (5 rename + 6 other) | BROKEN |
| **Total** | **1028** | **955** | **0** | **73 (18 rename + 55 other)** | **6/6 BROKEN** |

Cross-cutting notes:

- **Rename moves (18)**: all are `memory/`-anchored registry/constitution/glossary/register paths; each has a
  live successor at the `.specify/` root, so the repair is mechanical (path rewrite, no content search).
- **Registry cells (all 6 PASS)** do resolve post-rename, but three detail slugs are semantically wrong:
  `025-agent-skill-enablement.md` ("Todo Command"), `028-sdd-workflow-refactor.md` ("Feedback Mechanism"),
  `038-goal-target.md` ("Evidence Infrastructure"). The file headers are correct; the slugs are not.
- **Guard health**: 5 of 6 specs have zero missing guard modules. 020 misses one integration guard; 047 misses
  one guard named in tasks. The remaining 34 missing test modules are historical `baseline-failed.txt` entries,
  not live guard rosters, but they are dead pointers in the spec tree.
- **Contract-vs-implementation drift**: 034's `index.json` contract and 047's `index.json` data-model are the
  only live contracts whose stated storage target no longer exists.

ANOMALY: the anchor-layout rename (`memory/` → `.specify/` root) landed in the main tree during this audit (commit `6fb8093c4`, master) — 18 refs across the six specs moved mid-run and `AGENTS.md` was rewritten to the new anchors; the rename also produced three detail-file slugs that disagree with their feature names (025/028/038).

SPEC-AUDIT-LIVE-8-DONE
