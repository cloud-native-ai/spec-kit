# Feedback Probe Map(反馈插点结构图)

> **派生物** — 由 `--action map` 自 probe 真源整体重建,禁止手工编辑;
> 真源:`shared/definitions/probe-definitions.md` + 项目外部 probe。

## internal(内部 — 目标为 Spec Kit 框架)

### command-gate  [slice: commands]

- **收集内容**: 保留确认点触发后的用户决定观察事实(门控必要性证据)
- **处理流程**: record→threshold→package→manual→mark-submitted
- **适用插入位置**: confirm-gate
- **Objects** (11):
  - `gate-feature-status-regression` — /speckit.feature @ gate-feature-status-regression
  - `gate-glossary-user-entry-overwrite` — /speckit.instructions @ gate-glossary-user-entry-overwrite
  - `gate-implement-checklist-waiver` — /speckit.implement @ gate-implement-checklist-waiver
  - `gate-implement-evidence-binding` — /speckit.implement @ gate-implement-evidence-binding
  - `gate-rubric-high-stakes` — /speckit.instructions @ gate-rubric-high-stakes
  - `gate-sanitize-destructive-cleanup` — /speckit.sanitize @ gate-sanitize-destructive-cleanup
  - `gate-session-export-overwrite` — /speckit.session @ gate-session-export-overwrite
  - `gate-tools-invoke-entry` — /speckit.tools @ gate-tools-invoke-entry
  - `gate-tools-invoke-mode` — /speckit.tools @ gate-tools-invoke-mode
  - `gate-tools-invoke-prompt` — /speckit.tools @ gate-tools-invoke-prompt
  - `gate-tools-invoke-rule` — /speckit.tools @ gate-tools-invoke-rule

### command-wrapup  [slice: commands]

- **收集内容**: 命令单次运行的回顾与 ≥1 条单元级优化点
- **处理流程**: record→threshold→package→manual→mark-submitted
- **适用插入位置**: wrap-up
- **Objects** (23):
  - `speckit-analyze-wrapup` — /speckit.analyze @ wrap-up
  - `speckit-checklist-wrapup` — /speckit.checklist @ wrap-up
  - `speckit-clarify-wrapup` — /speckit.clarify @ wrap-up
  - `speckit-derive-wrapup` — /speckit.derive @ wrap-up
  - `speckit-docs-wrapup` — /speckit.docs @ wrap-up
  - `speckit-feedback-wrapup` — /speckit.feedback @ wrap-up
  - `speckit-goal-wrapup` — /speckit.goal @ wrap-up
  - `speckit-history-wrapup` — /speckit.history @ wrap-up
  - `speckit-implement-wrapup` — /speckit.implement @ wrap-up
  - `speckit-improve-wrapup` — /speckit.improve @ wrap-up
  - `speckit-instructions-wrapup` — /speckit.instructions @ wrap-up
  - `speckit-interview-wrapup` — /speckit.interview @ wrap-up
  - `speckit-plan-wrapup` — /speckit.plan @ wrap-up
  - `speckit-requirements-wrapup` — /speckit.requirements @ wrap-up
  - `speckit-research-wrapup` — /speckit.research @ wrap-up
  - `speckit-review-wrapup` — /speckit.review @ wrap-up
  - `speckit-sanitize-wrapup` — /speckit.sanitize @ wrap-up
  - `speckit-session-wrapup` — /speckit.session @ wrap-up
  - `speckit-skills-wrapup` — /speckit.skills @ wrap-up
  - `speckit-tasks-wrapup` — /speckit.tasks @ wrap-up
  - `speckit-team-wrapup` — /speckit.team @ wrap-up
  - `speckit-todo-wrapup` — /speckit.todo @ wrap-up
  - `speckit-tools-wrapup` — /speckit.tools @ wrap-up

### evidence-lane  [slice: scripts]

- **收集内容**: 证据引擎 lane 的可用性探测(node 运行时 / session store / 平台存储清单)
- **处理流程**: collect→findings.json
- **适用插入位置**: collect
- **Objects** (3):
  - `evidence-probe-node` — scripts/python/evidence-utils.py @ collect
  - `evidence-probe-platforms` — scripts/python/evidence-utils.py @ collect
  - `evidence-probe-session-store` — scripts/python/evidence-utils.py @ collect

### exec-quant  [slice: scripts]

- **收集内容**: 受测单元执行的环境与质量遥测采集(agent 程序 / LLM 详细 / 质量指标;exec-quant durable store,Recording Only)
- **处理流程**: collect→durable-record
- **适用插入位置**: wrap-up
- **Objects** (4):
  - `eq-collect-execution` — scripts/python/exec-quant.py @ wrap-up
  - `eq-probe-determination-link` — scripts/python/exec-quant.py @ wrap-up
  - `eq-probe-host-config` — scripts/python/exec-quant.py @ wrap-up
  - `eq-probe-host-process` — scripts/python/exec-quant.py @ wrap-up

### run-determination  [slice: scripts]

- **收集内容**: 运行判定四轴测量与两个可用性探测(token/elapsed/artifact_correctness/satisfaction;session store / evidence lane)
- **处理流程**: determine→session-record→route-into-feedback
- **适用插入位置**: wrap-up
- **Objects** (6):
  - `rd-axis-artifact-correctness` — scripts/python/run-determination.py @ wrap-up
  - `rd-axis-elapsed` — scripts/python/run-determination.py @ wrap-up
  - `rd-axis-satisfaction` — scripts/python/run-determination.py @ wrap-up
  - `rd-axis-token-consumption` — scripts/python/run-determination.py @ wrap-up
  - `rd-probe-evidence-lane` — scripts/python/run-determination.py @ wrap-up
  - `rd-probe-session-store` — scripts/python/run-determination.py @ wrap-up

### skill-evaluation-form  [slice: skills]

- **收集内容**: 绘图技能交付产物后由用户主动给出的 Evaluation Form(绘制评价单),用于评价该次已交付结果
- **处理流程**: record→threshold→package→manual→mark-submitted
- **适用插入位置**: evaluation-form
- **Objects** (1):
  - `skill-draw-diagram-evaluation-form` — skill:draw-diagram @ evaluation-form

### skill-gate  [slice: skills]

- **收集内容**: 保留确认点触发后的用户决定观察事实(门控必要性证据)
- **处理流程**: record→threshold→package→manual→mark-submitted
- **适用插入位置**: confirm-gate
- **Objects** (12):
  - `gate-create-docs-tiered-disposition` — skill:create-docs @ gate-create-docs-tiered-disposition
  - `gate-create-docs-write-plan` — skill:create-docs @ gate-create-docs-write-plan
  - `gate-create-team-agent-reuse` — skill:create-team @ gate-create-team-agent-reuse
  - `gate-create-team-noninteractive-call` — skill:create-team @ gate-create-team-noninteractive-call
  - `gate-create-team-presence-loop` — skill:create-team @ gate-create-team-presence-loop
  - `gate-create-tools-no-execute` — skill:create-tools @ gate-create-tools-no-execute
  - `gate-git-workflow-remote-ops` — skill:git-utils @ gate-git-workflow-remote-ops
  - `gate-git-workflow-tiered-mode` — skill:git-utils @ gate-git-workflow-tiered-mode
  - `gate-improve-tools-no-test-invoke` — skill:improve-tools @ gate-improve-tools-no-test-invoke
  - `gate-summarize-project-degraded-gates` — skill:summarize-project @ gate-summarize-project-degraded-gates
  - `gate-summarize-project-four-gates` — skill:summarize-project @ gate-summarize-project-four-gates
  - `gate-summarize-project-structure-freeze` — skill:summarize-project @ gate-summarize-project-structure-freeze

### skill-wrapup  [slice: skills]

- **收集内容**: 技能单次运行的回顾与 ≥1 条单元级优化点
- **处理流程**: record→threshold→package→manual→mark-submitted
- **适用插入位置**: wrap-up
- **Objects** (52):
  - `skill-analyze-artifacts-wrapup` — skill:analyze-artifacts @ wrap-up
  - `skill-archive-session-wrapup` — skill:archive-session @ wrap-up
  - `skill-clarify-artifact-wrapup` — skill:clarify-artifact @ wrap-up
  - `skill-coaching-skills-wrapup` — skill:coaching-skills @ wrap-up
  - `skill-code-review-wrapup` — skill:code-review @ wrap-up
  - `skill-collect-evidence-wrapup` — skill:collect-evidence @ wrap-up
  - `skill-create-agent-wrapup` — skill:create-agent @ wrap-up
  - `skill-create-checklist-wrapup` — skill:create-checklist @ wrap-up
  - `skill-create-docs-wrapup` — skill:create-docs @ wrap-up
  - `skill-create-pages-wrapup` — skill:create-pages @ wrap-up
  - `skill-create-plan-wrapup` — skill:create-plan @ wrap-up
  - `skill-create-requirements-wrapup` — skill:create-requirements @ wrap-up
  - `skill-create-skills-wrapup` — skill:create-skills @ wrap-up
  - `skill-create-tasks-wrapup` — skill:create-tasks @ wrap-up
  - `skill-create-team-wrapup` — skill:create-team @ wrap-up
  - `skill-create-tools-wrapup` — skill:create-tools @ wrap-up
  - `skill-database-utils-wrapup` — skill:database-utils @ wrap-up
  - `skill-derive-architecture-wrapup` — skill:derive-architecture @ wrap-up
  - `skill-document-utils-wrapup` — skill:document-utils @ wrap-up
  - `skill-draw-diagram-wrapup` — skill:draw-diagram @ wrap-up
  - `skill-git-utils-wrapup` — skill:git-utils @ wrap-up
  - `skill-humanize-wrapup` — skill:humanize @ wrap-up
  - `skill-implement-feature-wrapup` — skill:implement-feature @ wrap-up
  - `skill-improve-agent-wrapup` — skill:improve-agent @ wrap-up
  - `skill-improve-docs-wrapup` — skill:improve-docs @ wrap-up
  - `skill-improve-skills-wrapup` — skill:improve-skills @ wrap-up
  - `skill-improve-team-wrapup` — skill:improve-team @ wrap-up
  - `skill-improve-tools-wrapup` — skill:improve-tools @ wrap-up
  - `skill-manage-agents-wrapup` — skill:manage-agents @ wrap-up
  - `skill-manage-constitution-wrapup` — skill:manage-constitution @ wrap-up
  - `skill-manage-features-wrapup` — skill:manage-features @ wrap-up
  - `skill-manage-feedback-wrapup` — skill:manage-feedback @ wrap-up
  - `skill-manage-goal-wrapup` — skill:manage-goal @ wrap-up
  - `skill-manage-history-wrapup` — skill:manage-history @ wrap-up
  - `skill-manage-instructions-wrapup` — skill:manage-instructions @ wrap-up
  - `skill-manage-todo-wrapup` — skill:manage-todo @ wrap-up
  - `skill-memory-recall-wrapup` — skill:memory-recall @ wrap-up
  - `skill-memory-record-wrapup` — skill:memory-record @ wrap-up
  - `skill-merge-skills-wrapup` — skill:merge-skills @ wrap-up
  - `skill-research-feature-wrapup` — skill:research-feature @ wrap-up
  - `skill-review-sdd-process-wrapup` — skill:review-sdd-process @ wrap-up
  - `skill-run-agent-wrapup` — skill:run-agent @ wrap-up
  - `skill-run-interview-wrapup` — skill:run-interview @ wrap-up
  - `skill-run-skills-wrapup` — skill:run-skills @ wrap-up
  - `skill-run-team-wrapup` — skill:run-team @ wrap-up
  - `skill-sanitize-materials-wrapup` — skill:sanitize-materials @ wrap-up
  - `skill-sdd-house-keeping-wrapup` — skill:sdd-house-keeping @ wrap-up
  - `skill-sdd-loop-driver-cli-profile` — skill:sdd-loop-driver @ wrap-up
  - `skill-sdd-project-setup-wrapup` — skill:sdd-project-setup @ wrap-up
  - `skill-self-improvement-wrapup` — skill:self-improvement @ wrap-up
  - `skill-study-project-wrapup` — skill:study-project @ wrap-up
  - `skill-summarize-project-wrapup` — skill:summarize-project @ wrap-up

### trigger-escalation  [slice: scripts]

- **收集内容**: 050 主动流程触发的 P1–P5 升级探测(确定性存在性/计数/差集,永不读制品正文)
- **处理流程**: assess→suggest(非阻塞建议行)
- **适用插入位置**: situation
- **Objects** (5):
  - `trigger-p1-feature-dir` — scripts/python/trigger-utils.py @ situation
  - `trigger-p2-clarification-markers` — scripts/python/trigger-utils.py @ situation
  - `trigger-p3-tasks-state` — scripts/python/trigger-utils.py @ situation
  - `trigger-p4-feedback-threshold` — scripts/python/trigger-utils.py @ situation
  - `trigger-p5-instructions-staleness` — scripts/python/trigger-utils.py @ situation

## external(外部 — 目标为宿主项目自定义单元)

### external-custom  [slice: host-custom]

- **收集内容**: 宿主项目自定义单元运行的回顾与优化点
- **处理流程**: record→local-consumption(不上送)
- **适用插入位置**: wrap-up
- **Objects** (0 — 尚无实例;外部类经模式三注入)

## 结构总览(Mermaid)

```mermaid
graph TD
  root[Feedback Probe]
  root --> kind_internal[internal]
  kind_internal --> class_command_gate[command-gate]
  class_command_gate --> obj_gate_feature_status_regression[gate-feature-status-regression]
  class_command_gate --> obj_gate_glossary_user_entry_overwrite[gate-glossary-user-entry-overwrite]
  class_command_gate --> obj_gate_implement_checklist_waiver[gate-implement-checklist-waiver]
  class_command_gate --> obj_gate_implement_evidence_binding[gate-implement-evidence-binding]
  class_command_gate --> obj_gate_rubric_high_stakes[gate-rubric-high-stakes]
  class_command_gate --> obj_gate_sanitize_destructive_cleanup[gate-sanitize-destructive-cleanup]
  class_command_gate --> obj_gate_session_export_overwrite[gate-session-export-overwrite]
  class_command_gate --> obj_gate_tools_invoke_entry[gate-tools-invoke-entry]
  class_command_gate --> obj_gate_tools_invoke_mode[gate-tools-invoke-mode]
  class_command_gate --> obj_gate_tools_invoke_prompt[gate-tools-invoke-prompt]
  class_command_gate --> obj_gate_tools_invoke_rule[gate-tools-invoke-rule]
  kind_internal --> class_command_wrapup[command-wrapup]
  class_command_wrapup --> obj_speckit_analyze_wrapup[speckit-analyze-wrapup]
  class_command_wrapup --> obj_speckit_checklist_wrapup[speckit-checklist-wrapup]
  class_command_wrapup --> obj_speckit_clarify_wrapup[speckit-clarify-wrapup]
  class_command_wrapup --> obj_speckit_derive_wrapup[speckit-derive-wrapup]
  class_command_wrapup --> obj_speckit_docs_wrapup[speckit-docs-wrapup]
  class_command_wrapup --> obj_speckit_feedback_wrapup[speckit-feedback-wrapup]
  class_command_wrapup --> obj_speckit_goal_wrapup[speckit-goal-wrapup]
  class_command_wrapup --> obj_speckit_history_wrapup[speckit-history-wrapup]
  class_command_wrapup --> obj_speckit_implement_wrapup[speckit-implement-wrapup]
  class_command_wrapup --> obj_speckit_improve_wrapup[speckit-improve-wrapup]
  class_command_wrapup --> obj_speckit_instructions_wrapup[speckit-instructions-wrapup]
  class_command_wrapup --> obj_speckit_interview_wrapup[speckit-interview-wrapup]
  class_command_wrapup --> obj_speckit_plan_wrapup[speckit-plan-wrapup]
  class_command_wrapup --> obj_speckit_requirements_wrapup[speckit-requirements-wrapup]
  class_command_wrapup --> obj_speckit_research_wrapup[speckit-research-wrapup]
  class_command_wrapup --> obj_speckit_review_wrapup[speckit-review-wrapup]
  class_command_wrapup --> obj_speckit_sanitize_wrapup[speckit-sanitize-wrapup]
  class_command_wrapup --> obj_speckit_session_wrapup[speckit-session-wrapup]
  class_command_wrapup --> obj_speckit_skills_wrapup[speckit-skills-wrapup]
  class_command_wrapup --> obj_speckit_tasks_wrapup[speckit-tasks-wrapup]
  class_command_wrapup --> obj_speckit_team_wrapup[speckit-team-wrapup]
  class_command_wrapup --> obj_speckit_todo_wrapup[speckit-todo-wrapup]
  class_command_wrapup --> obj_speckit_tools_wrapup[speckit-tools-wrapup]
  kind_internal --> class_evidence_lane[evidence-lane]
  class_evidence_lane --> obj_evidence_probe_node[evidence-probe-node]
  class_evidence_lane --> obj_evidence_probe_platforms[evidence-probe-platforms]
  class_evidence_lane --> obj_evidence_probe_session_store[evidence-probe-session-store]
  kind_internal --> class_exec_quant[exec-quant]
  class_exec_quant --> obj_eq_collect_execution[eq-collect-execution]
  class_exec_quant --> obj_eq_probe_determination_link[eq-probe-determination-link]
  class_exec_quant --> obj_eq_probe_host_config[eq-probe-host-config]
  class_exec_quant --> obj_eq_probe_host_process[eq-probe-host-process]
  kind_internal --> class_run_determination[run-determination]
  class_run_determination --> obj_rd_axis_artifact_correctness[rd-axis-artifact-correctness]
  class_run_determination --> obj_rd_axis_elapsed[rd-axis-elapsed]
  class_run_determination --> obj_rd_axis_satisfaction[rd-axis-satisfaction]
  class_run_determination --> obj_rd_axis_token_consumption[rd-axis-token-consumption]
  class_run_determination --> obj_rd_probe_evidence_lane[rd-probe-evidence-lane]
  class_run_determination --> obj_rd_probe_session_store[rd-probe-session-store]
  kind_internal --> class_skill_evaluation_form[skill-evaluation-form]
  class_skill_evaluation_form --> obj_skill_draw_diagram_evaluation_form[skill-draw-diagram-evaluation-form]
  kind_internal --> class_skill_gate[skill-gate]
  class_skill_gate --> obj_gate_create_docs_tiered_disposition[gate-create-docs-tiered-disposition]
  class_skill_gate --> obj_gate_create_docs_write_plan[gate-create-docs-write-plan]
  class_skill_gate --> obj_gate_create_team_agent_reuse[gate-create-team-agent-reuse]
  class_skill_gate --> obj_gate_create_team_noninteractive_call[gate-create-team-noninteractive-call]
  class_skill_gate --> obj_gate_create_team_presence_loop[gate-create-team-presence-loop]
  class_skill_gate --> obj_gate_create_tools_no_execute[gate-create-tools-no-execute]
  class_skill_gate --> obj_gate_git_workflow_remote_ops[gate-git-workflow-remote-ops]
  class_skill_gate --> obj_gate_git_workflow_tiered_mode[gate-git-workflow-tiered-mode]
  class_skill_gate --> obj_gate_improve_tools_no_test_invoke[gate-improve-tools-no-test-invoke]
  class_skill_gate --> obj_gate_summarize_project_degraded_gates[gate-summarize-project-degraded-gates]
  class_skill_gate --> obj_gate_summarize_project_four_gates[gate-summarize-project-four-gates]
  class_skill_gate --> obj_gate_summarize_project_structure_freeze[gate-summarize-project-structure-freeze]
  kind_internal --> class_skill_wrapup[skill-wrapup]
  class_skill_wrapup --> obj_skill_analyze_artifacts_wrapup[skill-analyze-artifacts-wrapup]
  class_skill_wrapup --> obj_skill_archive_session_wrapup[skill-archive-session-wrapup]
  class_skill_wrapup --> obj_skill_clarify_artifact_wrapup[skill-clarify-artifact-wrapup]
  class_skill_wrapup --> obj_skill_coaching_skills_wrapup[skill-coaching-skills-wrapup]
  class_skill_wrapup --> obj_skill_code_review_wrapup[skill-code-review-wrapup]
  class_skill_wrapup --> obj_skill_collect_evidence_wrapup[skill-collect-evidence-wrapup]
  class_skill_wrapup --> obj_skill_create_agent_wrapup[skill-create-agent-wrapup]
  class_skill_wrapup --> obj_skill_create_checklist_wrapup[skill-create-checklist-wrapup]
  class_skill_wrapup --> obj_skill_create_docs_wrapup[skill-create-docs-wrapup]
  class_skill_wrapup --> obj_skill_create_pages_wrapup[skill-create-pages-wrapup]
  class_skill_wrapup --> obj_skill_create_plan_wrapup[skill-create-plan-wrapup]
  class_skill_wrapup --> obj_skill_create_requirements_wrapup[skill-create-requirements-wrapup]
  class_skill_wrapup --> obj_skill_create_skills_wrapup[skill-create-skills-wrapup]
  class_skill_wrapup --> obj_skill_create_tasks_wrapup[skill-create-tasks-wrapup]
  class_skill_wrapup --> obj_skill_create_team_wrapup[skill-create-team-wrapup]
  class_skill_wrapup --> obj_skill_create_tools_wrapup[skill-create-tools-wrapup]
  class_skill_wrapup --> obj_skill_database_utils_wrapup[skill-database-utils-wrapup]
  class_skill_wrapup --> obj_skill_derive_architecture_wrapup[skill-derive-architecture-wrapup]
  class_skill_wrapup --> obj_skill_document_utils_wrapup[skill-document-utils-wrapup]
  class_skill_wrapup --> obj_skill_draw_diagram_wrapup[skill-draw-diagram-wrapup]
  class_skill_wrapup --> obj_skill_git_utils_wrapup[skill-git-utils-wrapup]
  class_skill_wrapup --> obj_skill_humanize_wrapup[skill-humanize-wrapup]
  class_skill_wrapup --> obj_skill_implement_feature_wrapup[skill-implement-feature-wrapup]
  class_skill_wrapup --> obj_skill_improve_agent_wrapup[skill-improve-agent-wrapup]
  class_skill_wrapup --> obj_skill_improve_docs_wrapup[skill-improve-docs-wrapup]
  class_skill_wrapup --> obj_skill_improve_skills_wrapup[skill-improve-skills-wrapup]
  class_skill_wrapup --> obj_skill_improve_team_wrapup[skill-improve-team-wrapup]
  class_skill_wrapup --> obj_skill_improve_tools_wrapup[skill-improve-tools-wrapup]
  class_skill_wrapup --> obj_skill_manage_agents_wrapup[skill-manage-agents-wrapup]
  class_skill_wrapup --> obj_skill_manage_constitution_wrapup[skill-manage-constitution-wrapup]
  class_skill_wrapup --> obj_skill_manage_features_wrapup[skill-manage-features-wrapup]
  class_skill_wrapup --> obj_skill_manage_feedback_wrapup[skill-manage-feedback-wrapup]
  class_skill_wrapup --> obj_skill_manage_goal_wrapup[skill-manage-goal-wrapup]
  class_skill_wrapup --> obj_skill_manage_history_wrapup[skill-manage-history-wrapup]
  class_skill_wrapup --> obj_skill_manage_instructions_wrapup[skill-manage-instructions-wrapup]
  class_skill_wrapup --> obj_skill_manage_todo_wrapup[skill-manage-todo-wrapup]
  class_skill_wrapup --> obj_skill_memory_recall_wrapup[skill-memory-recall-wrapup]
  class_skill_wrapup --> obj_skill_memory_record_wrapup[skill-memory-record-wrapup]
  class_skill_wrapup --> obj_skill_merge_skills_wrapup[skill-merge-skills-wrapup]
  class_skill_wrapup --> obj_skill_research_feature_wrapup[skill-research-feature-wrapup]
  class_skill_wrapup --> obj_skill_review_sdd_process_wrapup[skill-review-sdd-process-wrapup]
  class_skill_wrapup --> obj_skill_run_agent_wrapup[skill-run-agent-wrapup]
  class_skill_wrapup --> obj_skill_run_interview_wrapup[skill-run-interview-wrapup]
  class_skill_wrapup --> obj_skill_run_skills_wrapup[skill-run-skills-wrapup]
  class_skill_wrapup --> obj_skill_run_team_wrapup[skill-run-team-wrapup]
  class_skill_wrapup --> obj_skill_sanitize_materials_wrapup[skill-sanitize-materials-wrapup]
  class_skill_wrapup --> obj_skill_sdd_house_keeping_wrapup[skill-sdd-house-keeping-wrapup]
  class_skill_wrapup --> obj_skill_sdd_loop_driver_cli_profile[skill-sdd-loop-driver-cli-profile]
  class_skill_wrapup --> obj_skill_sdd_project_setup_wrapup[skill-sdd-project-setup-wrapup]
  class_skill_wrapup --> obj_skill_self_improvement_wrapup[skill-self-improvement-wrapup]
  class_skill_wrapup --> obj_skill_study_project_wrapup[skill-study-project-wrapup]
  class_skill_wrapup --> obj_skill_summarize_project_wrapup[skill-summarize-project-wrapup]
  kind_internal --> class_trigger_escalation[trigger-escalation]
  class_trigger_escalation --> obj_trigger_p1_feature_dir[trigger-p1-feature-dir]
  class_trigger_escalation --> obj_trigger_p2_clarification_markers[trigger-p2-clarification-markers]
  class_trigger_escalation --> obj_trigger_p3_tasks_state[trigger-p3-tasks-state]
  class_trigger_escalation --> obj_trigger_p4_feedback_threshold[trigger-p4-feedback-threshold]
  class_trigger_escalation --> obj_trigger_p5_instructions_staleness[trigger-p5-instructions-staleness]
  root --> kind_external[external]
  kind_external --> class_external_custom[external-custom]
```

## 明细表

| Object | Class | Kind | 插入位置(unit @ lifecycle) | 收集内容 | 处理流程 |
|--------|-------|------|------------------------------|----------|----------|
| `gate-feature-status-regression` | command-gate | internal | /speckit.feature @ gate-feature-status-regression | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-glossary-user-entry-overwrite` | command-gate | internal | /speckit.instructions @ gate-glossary-user-entry-overwrite | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-implement-checklist-waiver` | command-gate | internal | /speckit.implement @ gate-implement-checklist-waiver | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-implement-evidence-binding` | command-gate | internal | /speckit.implement @ gate-implement-evidence-binding | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-rubric-high-stakes` | command-gate | internal | /speckit.instructions @ gate-rubric-high-stakes | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-sanitize-destructive-cleanup` | command-gate | internal | /speckit.sanitize @ gate-sanitize-destructive-cleanup | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-session-export-overwrite` | command-gate | internal | /speckit.session @ gate-session-export-overwrite | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-tools-invoke-entry` | command-gate | internal | /speckit.tools @ gate-tools-invoke-entry | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-tools-invoke-mode` | command-gate | internal | /speckit.tools @ gate-tools-invoke-mode | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-tools-invoke-prompt` | command-gate | internal | /speckit.tools @ gate-tools-invoke-prompt | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-tools-invoke-rule` | command-gate | internal | /speckit.tools @ gate-tools-invoke-rule | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `speckit-analyze-wrapup` | command-wrapup | internal | /speckit.analyze @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-checklist-wrapup` | command-wrapup | internal | /speckit.checklist @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-clarify-wrapup` | command-wrapup | internal | /speckit.clarify @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-derive-wrapup` | command-wrapup | internal | /speckit.derive @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-docs-wrapup` | command-wrapup | internal | /speckit.docs @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-feedback-wrapup` | command-wrapup | internal | /speckit.feedback @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-goal-wrapup` | command-wrapup | internal | /speckit.goal @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-history-wrapup` | command-wrapup | internal | /speckit.history @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-implement-wrapup` | command-wrapup | internal | /speckit.implement @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-improve-wrapup` | command-wrapup | internal | /speckit.improve @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-instructions-wrapup` | command-wrapup | internal | /speckit.instructions @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-interview-wrapup` | command-wrapup | internal | /speckit.interview @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-plan-wrapup` | command-wrapup | internal | /speckit.plan @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-requirements-wrapup` | command-wrapup | internal | /speckit.requirements @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-research-wrapup` | command-wrapup | internal | /speckit.research @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-review-wrapup` | command-wrapup | internal | /speckit.review @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-sanitize-wrapup` | command-wrapup | internal | /speckit.sanitize @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-session-wrapup` | command-wrapup | internal | /speckit.session @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-skills-wrapup` | command-wrapup | internal | /speckit.skills @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-tasks-wrapup` | command-wrapup | internal | /speckit.tasks @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-team-wrapup` | command-wrapup | internal | /speckit.team @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-todo-wrapup` | command-wrapup | internal | /speckit.todo @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-tools-wrapup` | command-wrapup | internal | /speckit.tools @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `evidence-probe-node` | evidence-lane | internal | scripts/python/evidence-utils.py @ collect | 证据引擎 lane 的可用性探测(node 运行时 / session store / 平台存储清单) | collect→findings.json |
| `evidence-probe-platforms` | evidence-lane | internal | scripts/python/evidence-utils.py @ collect | 证据引擎 lane 的可用性探测(node 运行时 / session store / 平台存储清单) | collect→findings.json |
| `evidence-probe-session-store` | evidence-lane | internal | scripts/python/evidence-utils.py @ collect | 证据引擎 lane 的可用性探测(node 运行时 / session store / 平台存储清单) | collect→findings.json |
| `eq-collect-execution` | exec-quant | internal | scripts/python/exec-quant.py @ wrap-up | 受测单元执行的环境与质量遥测采集(agent 程序 / LLM 详细 / 质量指标;exec-quant durable store,Recording Only) | collect→durable-record |
| `eq-probe-determination-link` | exec-quant | internal | scripts/python/exec-quant.py @ wrap-up | 受测单元执行的环境与质量遥测采集(agent 程序 / LLM 详细 / 质量指标;exec-quant durable store,Recording Only) | collect→durable-record |
| `eq-probe-host-config` | exec-quant | internal | scripts/python/exec-quant.py @ wrap-up | 受测单元执行的环境与质量遥测采集(agent 程序 / LLM 详细 / 质量指标;exec-quant durable store,Recording Only) | collect→durable-record |
| `eq-probe-host-process` | exec-quant | internal | scripts/python/exec-quant.py @ wrap-up | 受测单元执行的环境与质量遥测采集(agent 程序 / LLM 详细 / 质量指标;exec-quant durable store,Recording Only) | collect→durable-record |
| `rd-axis-artifact-correctness` | run-determination | internal | scripts/python/run-determination.py @ wrap-up | 运行判定四轴测量与两个可用性探测(token/elapsed/artifact_correctness/satisfaction;session store / evidence lane) | determine→session-record→route-into-feedback |
| `rd-axis-elapsed` | run-determination | internal | scripts/python/run-determination.py @ wrap-up | 运行判定四轴测量与两个可用性探测(token/elapsed/artifact_correctness/satisfaction;session store / evidence lane) | determine→session-record→route-into-feedback |
| `rd-axis-satisfaction` | run-determination | internal | scripts/python/run-determination.py @ wrap-up | 运行判定四轴测量与两个可用性探测(token/elapsed/artifact_correctness/satisfaction;session store / evidence lane) | determine→session-record→route-into-feedback |
| `rd-axis-token-consumption` | run-determination | internal | scripts/python/run-determination.py @ wrap-up | 运行判定四轴测量与两个可用性探测(token/elapsed/artifact_correctness/satisfaction;session store / evidence lane) | determine→session-record→route-into-feedback |
| `rd-probe-evidence-lane` | run-determination | internal | scripts/python/run-determination.py @ wrap-up | 运行判定四轴测量与两个可用性探测(token/elapsed/artifact_correctness/satisfaction;session store / evidence lane) | determine→session-record→route-into-feedback |
| `rd-probe-session-store` | run-determination | internal | scripts/python/run-determination.py @ wrap-up | 运行判定四轴测量与两个可用性探测(token/elapsed/artifact_correctness/satisfaction;session store / evidence lane) | determine→session-record→route-into-feedback |
| `skill-draw-diagram-evaluation-form` | skill-evaluation-form | internal | skill:draw-diagram @ evaluation-form | 绘图技能交付产物后由用户主动给出的 Evaluation Form(绘制评价单),用于评价该次已交付结果 | record→threshold→package→manual→mark-submitted |
| `gate-create-docs-tiered-disposition` | skill-gate | internal | skill:create-docs @ gate-create-docs-tiered-disposition | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-create-docs-write-plan` | skill-gate | internal | skill:create-docs @ gate-create-docs-write-plan | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-create-team-agent-reuse` | skill-gate | internal | skill:create-team @ gate-create-team-agent-reuse | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-create-team-noninteractive-call` | skill-gate | internal | skill:create-team @ gate-create-team-noninteractive-call | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-create-team-presence-loop` | skill-gate | internal | skill:create-team @ gate-create-team-presence-loop | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-create-tools-no-execute` | skill-gate | internal | skill:create-tools @ gate-create-tools-no-execute | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-git-workflow-remote-ops` | skill-gate | internal | skill:git-utils @ gate-git-workflow-remote-ops | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-git-workflow-tiered-mode` | skill-gate | internal | skill:git-utils @ gate-git-workflow-tiered-mode | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-improve-tools-no-test-invoke` | skill-gate | internal | skill:improve-tools @ gate-improve-tools-no-test-invoke | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-summarize-project-degraded-gates` | skill-gate | internal | skill:summarize-project @ gate-summarize-project-degraded-gates | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-summarize-project-four-gates` | skill-gate | internal | skill:summarize-project @ gate-summarize-project-four-gates | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-summarize-project-structure-freeze` | skill-gate | internal | skill:summarize-project @ gate-summarize-project-structure-freeze | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `skill-analyze-artifacts-wrapup` | skill-wrapup | internal | skill:analyze-artifacts @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-archive-session-wrapup` | skill-wrapup | internal | skill:archive-session @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-clarify-artifact-wrapup` | skill-wrapup | internal | skill:clarify-artifact @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-coaching-skills-wrapup` | skill-wrapup | internal | skill:coaching-skills @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-code-review-wrapup` | skill-wrapup | internal | skill:code-review @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-collect-evidence-wrapup` | skill-wrapup | internal | skill:collect-evidence @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-agent-wrapup` | skill-wrapup | internal | skill:create-agent @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-checklist-wrapup` | skill-wrapup | internal | skill:create-checklist @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-docs-wrapup` | skill-wrapup | internal | skill:create-docs @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-pages-wrapup` | skill-wrapup | internal | skill:create-pages @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-plan-wrapup` | skill-wrapup | internal | skill:create-plan @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-requirements-wrapup` | skill-wrapup | internal | skill:create-requirements @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-skills-wrapup` | skill-wrapup | internal | skill:create-skills @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-tasks-wrapup` | skill-wrapup | internal | skill:create-tasks @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-team-wrapup` | skill-wrapup | internal | skill:create-team @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-tools-wrapup` | skill-wrapup | internal | skill:create-tools @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-database-utils-wrapup` | skill-wrapup | internal | skill:database-utils @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-derive-architecture-wrapup` | skill-wrapup | internal | skill:derive-architecture @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-document-utils-wrapup` | skill-wrapup | internal | skill:document-utils @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-draw-diagram-wrapup` | skill-wrapup | internal | skill:draw-diagram @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-git-utils-wrapup` | skill-wrapup | internal | skill:git-utils @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-humanize-wrapup` | skill-wrapup | internal | skill:humanize @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-implement-feature-wrapup` | skill-wrapup | internal | skill:implement-feature @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-agent-wrapup` | skill-wrapup | internal | skill:improve-agent @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-docs-wrapup` | skill-wrapup | internal | skill:improve-docs @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-skills-wrapup` | skill-wrapup | internal | skill:improve-skills @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-team-wrapup` | skill-wrapup | internal | skill:improve-team @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-tools-wrapup` | skill-wrapup | internal | skill:improve-tools @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-manage-agents-wrapup` | skill-wrapup | internal | skill:manage-agents @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-manage-constitution-wrapup` | skill-wrapup | internal | skill:manage-constitution @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-manage-features-wrapup` | skill-wrapup | internal | skill:manage-features @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-manage-feedback-wrapup` | skill-wrapup | internal | skill:manage-feedback @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-manage-goal-wrapup` | skill-wrapup | internal | skill:manage-goal @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-manage-history-wrapup` | skill-wrapup | internal | skill:manage-history @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-manage-instructions-wrapup` | skill-wrapup | internal | skill:manage-instructions @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-manage-todo-wrapup` | skill-wrapup | internal | skill:manage-todo @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-memory-recall-wrapup` | skill-wrapup | internal | skill:memory-recall @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-memory-record-wrapup` | skill-wrapup | internal | skill:memory-record @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-merge-skills-wrapup` | skill-wrapup | internal | skill:merge-skills @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-research-feature-wrapup` | skill-wrapup | internal | skill:research-feature @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-review-sdd-process-wrapup` | skill-wrapup | internal | skill:review-sdd-process @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-run-agent-wrapup` | skill-wrapup | internal | skill:run-agent @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-run-interview-wrapup` | skill-wrapup | internal | skill:run-interview @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-run-skills-wrapup` | skill-wrapup | internal | skill:run-skills @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-run-team-wrapup` | skill-wrapup | internal | skill:run-team @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-sanitize-materials-wrapup` | skill-wrapup | internal | skill:sanitize-materials @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-sdd-house-keeping-wrapup` | skill-wrapup | internal | skill:sdd-house-keeping @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-sdd-loop-driver-cli-profile` | skill-wrapup | internal | skill:sdd-loop-driver @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-sdd-project-setup-wrapup` | skill-wrapup | internal | skill:sdd-project-setup @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-self-improvement-wrapup` | skill-wrapup | internal | skill:self-improvement @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-study-project-wrapup` | skill-wrapup | internal | skill:study-project @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-summarize-project-wrapup` | skill-wrapup | internal | skill:summarize-project @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `trigger-p1-feature-dir` | trigger-escalation | internal | scripts/python/trigger-utils.py @ situation | 050 主动流程触发的 P1–P5 升级探测(确定性存在性/计数/差集,永不读制品正文) | assess→suggest(非阻塞建议行) |
| `trigger-p2-clarification-markers` | trigger-escalation | internal | scripts/python/trigger-utils.py @ situation | 050 主动流程触发的 P1–P5 升级探测(确定性存在性/计数/差集,永不读制品正文) | assess→suggest(非阻塞建议行) |
| `trigger-p3-tasks-state` | trigger-escalation | internal | scripts/python/trigger-utils.py @ situation | 050 主动流程触发的 P1–P5 升级探测(确定性存在性/计数/差集,永不读制品正文) | assess→suggest(非阻塞建议行) |
| `trigger-p4-feedback-threshold` | trigger-escalation | internal | scripts/python/trigger-utils.py @ situation | 050 主动流程触发的 P1–P5 升级探测(确定性存在性/计数/差集,永不读制品正文) | assess→suggest(非阻塞建议行) |
| `trigger-p5-instructions-staleness` | trigger-escalation | internal | scripts/python/trigger-utils.py @ situation | 050 主动流程触发的 P1–P5 升级探测(确定性存在性/计数/差集,永不读制品正文) | assess→suggest(非阻塞建议行) |
