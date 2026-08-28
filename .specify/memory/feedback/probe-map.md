# Feedback Probe Map(反馈插点结构图)

> **派生物** — 由 `--action map` 自 probe 真源整体重建,禁止手工编辑;
> 真源:`shared/definitions/probe-definitions.md` + 项目外部 probe。

## internal(内部 — 目标为 Spec Kit 框架)

### command-gate  [slice: commands]

- **收集内容**: 保留确认点触发后的用户决定观察事实(门控必要性证据)
- **处理流程**: record→threshold→package→manual→mark-submitted
- **适用插入位置**: confirm-gate
- **Objects** (10):
  - `gate-feature-status-regression` — /speckit.feature @ gate-feature-status-regression
  - `gate-glossary-user-entry-overwrite` — /speckit.instructions @ gate-glossary-user-entry-overwrite
  - `gate-implement-checklist-waiver` — /speckit.implement @ gate-implement-checklist-waiver
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
- **Objects** (20):
  - `speckit-analyze-wrapup` — /speckit.analyze @ wrap-up
  - `speckit-checklist-wrapup` — /speckit.checklist @ wrap-up
  - `speckit-clarify-wrapup` — /speckit.clarify @ wrap-up
  - `speckit-docs-wrapup` — /speckit.docs @ wrap-up
  - `speckit-feedback-wrapup` — /speckit.feedback @ wrap-up
  - `speckit-goal-wrapup` — /speckit.goal @ wrap-up
  - `speckit-history-wrapup` — /speckit.history @ wrap-up
  - `speckit-implement-wrapup` — /speckit.implement @ wrap-up
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
  - `speckit-todo-wrapup` — /speckit.todo @ wrap-up
  - `speckit-tools-wrapup` — /speckit.tools @ wrap-up

### skill-gate  [slice: skills]

- **收集内容**: 保留确认点触发后的用户决定观察事实(门控必要性证据)
- **处理流程**: record→threshold→package→manual→mark-submitted
- **适用插入位置**: confirm-gate
- **Objects** (11):
  - `gate-create-docs-tiered-disposition` — skill:create-docs @ gate-create-docs-tiered-disposition
  - `gate-create-docs-write-plan` — skill:create-docs @ gate-create-docs-write-plan
  - `gate-create-team-noninteractive-call` — skill:create-team @ gate-create-team-noninteractive-call
  - `gate-create-team-presence-loop` — skill:create-team @ gate-create-team-presence-loop
  - `gate-create-tools-no-execute` — skill:create-tools @ gate-create-tools-no-execute
  - `gate-git-workflow-remote-ops` — skill:git-workflow @ gate-git-workflow-remote-ops
  - `gate-git-workflow-tiered-mode` — skill:git-workflow @ gate-git-workflow-tiered-mode
  - `gate-improve-tools-no-test-invoke` — skill:improve-tools @ gate-improve-tools-no-test-invoke
  - `gate-summarize-project-degraded-gates` — skill:summarize-project @ gate-summarize-project-degraded-gates
  - `gate-summarize-project-four-gates` — skill:summarize-project @ gate-summarize-project-four-gates
  - `gate-summarize-project-structure-freeze` — skill:summarize-project @ gate-summarize-project-structure-freeze

### skill-wrapup  [slice: skills]

- **收集内容**: 技能单次运行的回顾与 ≥1 条单元级优化点
- **处理流程**: record→threshold→package→manual→mark-submitted
- **适用插入位置**: wrap-up
- **Objects** (31):
  - `skill-archive-session-wrapup` — skill:archive-session @ wrap-up
  - `skill-browser-extension-wrapup` — skill:browser-extension @ wrap-up
  - `skill-browser-utils-wrapup` — skill:browser-utils @ wrap-up
  - `skill-clone-website-ui-wrapup` — skill:clone-website-ui @ wrap-up
  - `skill-code-review-wrapup` — skill:code-review @ wrap-up
  - `skill-collect-evidence-wrapup` — skill:collect-evidence @ wrap-up
  - `skill-create-agent-wrapup` — skill:create-agent @ wrap-up
  - `skill-create-docs-wrapup` — skill:create-docs @ wrap-up
  - `skill-create-pages-wrapup` — skill:create-pages @ wrap-up
  - `skill-create-skills-wrapup` — skill:create-skills @ wrap-up
  - `skill-create-team-wrapup` — skill:create-team @ wrap-up
  - `skill-create-tools-wrapup` — skill:create-tools @ wrap-up
  - `skill-database-utils-wrapup` — skill:database-utils @ wrap-up
  - `skill-document-utils-wrapup` — skill:document-utils @ wrap-up
  - `skill-draw-d3js-wrapup` — skill:draw-d3js @ wrap-up
  - `skill-draw-echarts-wrapup` — skill:draw-echarts @ wrap-up
  - `skill-draw-mermaid-wrapup` — skill:draw-mermaid @ wrap-up
  - `skill-draw-plantuml-wrapup` — skill:draw-plantuml @ wrap-up
  - `skill-git-submodule-edit-wrapup` — skill:git-submodule-edit @ wrap-up
  - `skill-git-workflow-wrapup` — skill:git-workflow @ wrap-up
  - `skill-improve-agent-wrapup` — skill:improve-agent @ wrap-up
  - `skill-improve-docs-wrapup` — skill:improve-docs @ wrap-up
  - `skill-improve-skills-wrapup` — skill:improve-skills @ wrap-up
  - `skill-improve-team-wrapup` — skill:improve-team @ wrap-up
  - `skill-improve-tools-wrapup` — skill:improve-tools @ wrap-up
  - `skill-manage-agents-wrapup` — skill:manage-agents @ wrap-up
  - `skill-memory-recall-wrapup` — skill:memory-recall @ wrap-up
  - `skill-memory-record-wrapup` — skill:memory-record @ wrap-up
  - `skill-study-project-wrapup` — skill:study-project @ wrap-up
  - `skill-summarize-project-wrapup` — skill:summarize-project @ wrap-up
  - `skill-think-skills-wrapup` — skill:think-skills @ wrap-up

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
  class_command_wrapup --> obj_speckit_docs_wrapup[speckit-docs-wrapup]
  class_command_wrapup --> obj_speckit_feedback_wrapup[speckit-feedback-wrapup]
  class_command_wrapup --> obj_speckit_goal_wrapup[speckit-goal-wrapup]
  class_command_wrapup --> obj_speckit_history_wrapup[speckit-history-wrapup]
  class_command_wrapup --> obj_speckit_implement_wrapup[speckit-implement-wrapup]
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
  class_command_wrapup --> obj_speckit_todo_wrapup[speckit-todo-wrapup]
  class_command_wrapup --> obj_speckit_tools_wrapup[speckit-tools-wrapup]
  kind_internal --> class_skill_gate[skill-gate]
  class_skill_gate --> obj_gate_create_docs_tiered_disposition[gate-create-docs-tiered-disposition]
  class_skill_gate --> obj_gate_create_docs_write_plan[gate-create-docs-write-plan]
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
  class_skill_wrapup --> obj_skill_archive_session_wrapup[skill-archive-session-wrapup]
  class_skill_wrapup --> obj_skill_browser_extension_wrapup[skill-browser-extension-wrapup]
  class_skill_wrapup --> obj_skill_browser_utils_wrapup[skill-browser-utils-wrapup]
  class_skill_wrapup --> obj_skill_clone_website_ui_wrapup[skill-clone-website-ui-wrapup]
  class_skill_wrapup --> obj_skill_code_review_wrapup[skill-code-review-wrapup]
  class_skill_wrapup --> obj_skill_collect_evidence_wrapup[skill-collect-evidence-wrapup]
  class_skill_wrapup --> obj_skill_create_agent_wrapup[skill-create-agent-wrapup]
  class_skill_wrapup --> obj_skill_create_docs_wrapup[skill-create-docs-wrapup]
  class_skill_wrapup --> obj_skill_create_pages_wrapup[skill-create-pages-wrapup]
  class_skill_wrapup --> obj_skill_create_skills_wrapup[skill-create-skills-wrapup]
  class_skill_wrapup --> obj_skill_create_team_wrapup[skill-create-team-wrapup]
  class_skill_wrapup --> obj_skill_create_tools_wrapup[skill-create-tools-wrapup]
  class_skill_wrapup --> obj_skill_database_utils_wrapup[skill-database-utils-wrapup]
  class_skill_wrapup --> obj_skill_document_utils_wrapup[skill-document-utils-wrapup]
  class_skill_wrapup --> obj_skill_draw_d3js_wrapup[skill-draw-d3js-wrapup]
  class_skill_wrapup --> obj_skill_draw_echarts_wrapup[skill-draw-echarts-wrapup]
  class_skill_wrapup --> obj_skill_draw_mermaid_wrapup[skill-draw-mermaid-wrapup]
  class_skill_wrapup --> obj_skill_draw_plantuml_wrapup[skill-draw-plantuml-wrapup]
  class_skill_wrapup --> obj_skill_git_submodule_edit_wrapup[skill-git-submodule-edit-wrapup]
  class_skill_wrapup --> obj_skill_git_workflow_wrapup[skill-git-workflow-wrapup]
  class_skill_wrapup --> obj_skill_improve_agent_wrapup[skill-improve-agent-wrapup]
  class_skill_wrapup --> obj_skill_improve_docs_wrapup[skill-improve-docs-wrapup]
  class_skill_wrapup --> obj_skill_improve_skills_wrapup[skill-improve-skills-wrapup]
  class_skill_wrapup --> obj_skill_improve_team_wrapup[skill-improve-team-wrapup]
  class_skill_wrapup --> obj_skill_improve_tools_wrapup[skill-improve-tools-wrapup]
  class_skill_wrapup --> obj_skill_manage_agents_wrapup[skill-manage-agents-wrapup]
  class_skill_wrapup --> obj_skill_memory_recall_wrapup[skill-memory-recall-wrapup]
  class_skill_wrapup --> obj_skill_memory_record_wrapup[skill-memory-record-wrapup]
  class_skill_wrapup --> obj_skill_study_project_wrapup[skill-study-project-wrapup]
  class_skill_wrapup --> obj_skill_summarize_project_wrapup[skill-summarize-project-wrapup]
  class_skill_wrapup --> obj_skill_think_skills_wrapup[skill-think-skills-wrapup]
  root --> kind_external[external]
  kind_external --> class_external_custom[external-custom]
```

## 明细表

| Object | Class | Kind | 插入位置(unit @ lifecycle) | 收集内容 | 处理流程 |
|--------|-------|------|------------------------------|----------|----------|
| `gate-feature-status-regression` | command-gate | internal | /speckit.feature @ gate-feature-status-regression | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-glossary-user-entry-overwrite` | command-gate | internal | /speckit.instructions @ gate-glossary-user-entry-overwrite | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-implement-checklist-waiver` | command-gate | internal | /speckit.implement @ gate-implement-checklist-waiver | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
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
| `speckit-docs-wrapup` | command-wrapup | internal | /speckit.docs @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-feedback-wrapup` | command-wrapup | internal | /speckit.feedback @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-goal-wrapup` | command-wrapup | internal | /speckit.goal @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-history-wrapup` | command-wrapup | internal | /speckit.history @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-implement-wrapup` | command-wrapup | internal | /speckit.implement @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
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
| `speckit-todo-wrapup` | command-wrapup | internal | /speckit.todo @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `speckit-tools-wrapup` | command-wrapup | internal | /speckit.tools @ wrap-up | 命令单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `gate-create-docs-tiered-disposition` | skill-gate | internal | skill:create-docs @ gate-create-docs-tiered-disposition | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-create-docs-write-plan` | skill-gate | internal | skill:create-docs @ gate-create-docs-write-plan | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-create-team-noninteractive-call` | skill-gate | internal | skill:create-team @ gate-create-team-noninteractive-call | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-create-team-presence-loop` | skill-gate | internal | skill:create-team @ gate-create-team-presence-loop | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-create-tools-no-execute` | skill-gate | internal | skill:create-tools @ gate-create-tools-no-execute | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-git-workflow-remote-ops` | skill-gate | internal | skill:git-workflow @ gate-git-workflow-remote-ops | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-git-workflow-tiered-mode` | skill-gate | internal | skill:git-workflow @ gate-git-workflow-tiered-mode | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-improve-tools-no-test-invoke` | skill-gate | internal | skill:improve-tools @ gate-improve-tools-no-test-invoke | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-summarize-project-degraded-gates` | skill-gate | internal | skill:summarize-project @ gate-summarize-project-degraded-gates | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-summarize-project-four-gates` | skill-gate | internal | skill:summarize-project @ gate-summarize-project-four-gates | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `gate-summarize-project-structure-freeze` | skill-gate | internal | skill:summarize-project @ gate-summarize-project-structure-freeze | 保留确认点触发后的用户决定观察事实(门控必要性证据) | record→threshold→package→manual→mark-submitted |
| `skill-archive-session-wrapup` | skill-wrapup | internal | skill:archive-session @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-browser-extension-wrapup` | skill-wrapup | internal | skill:browser-extension @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-browser-utils-wrapup` | skill-wrapup | internal | skill:browser-utils @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-clone-website-ui-wrapup` | skill-wrapup | internal | skill:clone-website-ui @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-code-review-wrapup` | skill-wrapup | internal | skill:code-review @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-collect-evidence-wrapup` | skill-wrapup | internal | skill:collect-evidence @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-agent-wrapup` | skill-wrapup | internal | skill:create-agent @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-docs-wrapup` | skill-wrapup | internal | skill:create-docs @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-pages-wrapup` | skill-wrapup | internal | skill:create-pages @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-skills-wrapup` | skill-wrapup | internal | skill:create-skills @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-team-wrapup` | skill-wrapup | internal | skill:create-team @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-create-tools-wrapup` | skill-wrapup | internal | skill:create-tools @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-database-utils-wrapup` | skill-wrapup | internal | skill:database-utils @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-document-utils-wrapup` | skill-wrapup | internal | skill:document-utils @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-draw-d3js-wrapup` | skill-wrapup | internal | skill:draw-d3js @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-draw-echarts-wrapup` | skill-wrapup | internal | skill:draw-echarts @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-draw-mermaid-wrapup` | skill-wrapup | internal | skill:draw-mermaid @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-draw-plantuml-wrapup` | skill-wrapup | internal | skill:draw-plantuml @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-git-submodule-edit-wrapup` | skill-wrapup | internal | skill:git-submodule-edit @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-git-workflow-wrapup` | skill-wrapup | internal | skill:git-workflow @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-agent-wrapup` | skill-wrapup | internal | skill:improve-agent @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-docs-wrapup` | skill-wrapup | internal | skill:improve-docs @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-skills-wrapup` | skill-wrapup | internal | skill:improve-skills @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-team-wrapup` | skill-wrapup | internal | skill:improve-team @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-improve-tools-wrapup` | skill-wrapup | internal | skill:improve-tools @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-manage-agents-wrapup` | skill-wrapup | internal | skill:manage-agents @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-memory-recall-wrapup` | skill-wrapup | internal | skill:memory-recall @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-memory-record-wrapup` | skill-wrapup | internal | skill:memory-record @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-study-project-wrapup` | skill-wrapup | internal | skill:study-project @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-summarize-project-wrapup` | skill-wrapup | internal | skill:summarize-project @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
| `skill-think-skills-wrapup` | skill-wrapup | internal | skill:think-skills @ wrap-up | 技能单次运行的回顾与 ≥1 条单元级优化点 | record→threshold→package→manual→mark-submitted |
