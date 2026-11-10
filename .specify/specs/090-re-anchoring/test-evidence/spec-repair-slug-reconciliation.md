# Feature-detail slug reconciliation (2026-11-10)

Scope: `.specify/features/` (89 files) and `.specify/features.md` (89 rows). No commit, no push.

## Decision record

- **Gate**: functional change × autonomous execution -> **fix + disclose**.
- **Authority for identity**: the registry row whose `Name` matches the detail file's H1 content, cross-checked against that row's Spec Path spec-dir slug and the spec's own H1. The pre-move filename (`NNN.md`, commit `8b9030371^`) confirms `true-id = NNN`.
- **Authority for slug**: the content title (`[FEATURE_SLUG]` in `templates/feature-details-template.md`: "Kebab-case combination of ID + normalized name"). The row's spec-dir slug is used where it names the same feature; a recognized shortening/translation of the content title is retained. A spec-dir slug that names a *different* requirement (extension pointers such as `013 -> 030-summarize-project`) is **not** used.
- **Root cause**: commit `8b9030371` renamed `.specify/memory/features/NNN.md` by pairing each feature ID with the *same-numbered* spec-dir slug. Where that spec belongs to another feature, the filename names a different feature while the content stays correct.
- **Numeric prefix**: measured — all 89 pre-rename prefixes already equaled their own `**Feature ID**`; **0** had a wrong numeric prefix. The defect is slug-only (32 files).

## Counts

- Files before/after: 89 / 89 (no file created or deleted).
- Renamed with `git mv`: **32**. Unchanged: **57**. Collisions: **0**.
- Registry `Feature Details` cells updated: **32**. Cells already correct: **57**.
- Detail self-reference lines repaired: **61** `Feature Detail:` lines + **58** `Feature Index:` lines across **62** files.
- Live doc pointer repaired outside the registry: `docs/reference/commands/goal.md` (1 line).
- Specs' `requirements.md` changed: **0** — `validate-requirements.py` re-run not applicable.

## Mapping table (pre-rename file -> true id -> new file)

| Pre-rename file | True id | New file | Action | H1 content (evidence) |
|---|---|---|---|---|
| `.specify/features/001-unify-command-handoffs.md` | 001 | `.specify/features/001-unify-command-handoffs.md` | unchanged | Unify Command Handoffs |
| `.specify/features/002-analyze-command.md` | 002 | `.specify/features/002-analyze-command.md` | unchanged | Analyze Command |
| `.specify/features/003-checklist-command.md` | 003 | `.specify/features/003-checklist-command.md` | unchanged | Checklist Command |
| `.specify/features/004-clarify-command.md` | 004 | `.specify/features/004-clarify-command.md` | unchanged | Clarify Command |
| `.specify/features/005-constitution-command.md` | 005 | `.specify/features/005-constitution-command.md` | unchanged | Constitution Command |
| `.specify/features/006-add-qoder-support.md` | 006 | `.specify/features/006-feature-command.md` | renamed | Feature Command |
| `.specify/features/007-implement-command.md` | 007 | `.specify/features/007-implement-command.md` | unchanged | Implement Command |
| `.specify/features/008-instructions-command.md` | 008 | `.specify/features/008-instructions-command.md` | unchanged | Instructions Command |
| `.specify/features/009-claude-code-support.md` | 009 | `.specify/features/009-plan-command.md` | renamed | Plan Command |
| `.specify/features/010-requirements-command.md` | 010 | `.specify/features/010-requirements-command.md` | unchanged | Requirements Command |
| `.specify/features/011-research-command.md` | 011 | `.specify/features/011-research-command.md` | unchanged | Research Command |
| `.specify/features/012-skill-home-workdir.md` | 012 | `.specify/features/012-review-command.md` | renamed | Review Command |
| `.specify/features/013-portable-skill-creation.md` | 013 | `.specify/features/013-skills-command.md` | renamed | Skills Command |
| `.specify/features/014-tasks-command.md` | 014 | `.specify/features/014-tasks-command.md` | unchanged | Tasks Command |
| `.specify/features/015-cli-interface.md` | 015 | `.specify/features/015-cli-interface.md` | unchanged | CLI Interface |
| `.specify/features/016-refactor-tools-command.md` | 016 | `.specify/features/016-refactor-tools-command.md` | unchanged | Tools Command |
| `.specify/features/017-template-engine.md` | 017 | `.specify/features/017-template-engine.md` | unchanged | Template Engine |
| `.specify/features/018-cli-priority-support.md` | 018 | `.specify/features/018-configuration-management.md` | renamed | Configuration Management |
| `.specify/features/019-agents-command.md` | 019 | `.specify/features/019-agents-command.md` | unchanged | Agents Command |
| `.specify/features/020-speckit-todo-command.md` | 020 | `.specify/features/020-qoder-support.md` | renamed | Qoder Support |
| `.specify/features/021-agent-specific-config.md` | 021 | `.specify/features/021-claude-code-support.md` | renamed | Claude Code Support |
| `.specify/features/022-ai-tools-support.md` | 022 | `.specify/features/022-ai-tools-support.md` | unchanged | AI Tools Support |
| `.specify/features/023-agent-framework-redesign.md` | 023 | `.specify/features/023-prompt-template-quality.md` | renamed | Prompt Template Quality |
| `.specify/features/024-agent-env-config.md` | 024 | `.specify/features/024-specification-workspace-versioning.md` | renamed | Specification Workspace Versioning |
| `.specify/features/025-agent-skill-enablement.md` | 025 | `.specify/features/025-todo-command.md` | renamed | Todo Command |
| `.specify/features/026-agent-skill-enablement.md` | 026 | `.specify/features/026-agent-skill-enablement.md` | unchanged | Agent Skill Enablement |
| `.specify/features/027-feedback-mechanism.md` | 027 | `.specify/features/027-team-management.md` | renamed | Team Management |
| `.specify/features/028-sdd-workflow-refactor.md` | 028 | `.specify/features/028-feedback-mechanism.md` | renamed | Feedback Mechanism |
| `.specify/features/029-glossary-mechanism.md` | 029 | `.specify/features/029-shared-reference-directory.md` | renamed | Shared Reference Directory |
| `.specify/features/030-summarize-project.md` | 030 | `.specify/features/030-history-command.md` | renamed | History Command |
| `.specify/features/031-task-complexity-rubric.md` | 031 | `.specify/features/031-glossary-mechanism.md` | renamed | Glossary Mechanism |
| `.specify/features/032-dogfooding-practice.md` | 032 | `.specify/features/032-task-complexity-rubric.md` | renamed | Task Complexity Rubric |
| `.specify/features/033-docs-command.md` | 033 | `.specify/features/033-agent-project-context-parameterization.md` | renamed | Agent Project Context Parameterization |
| `.specify/features/034-evidence-infra.md` | 034 | `.specify/features/034-ci-cd-pipeline.md` | renamed | CI/CD Pipeline |
| `.specify/features/035-token-efficiency.md` | 035 | `.specify/features/035-code-quality-tooling.md` | renamed | Code Quality Tooling |
| `.specify/features/036-team-summary.md` | 036 | `.specify/features/036-dogfooding-practice.md` | renamed | Dogfooding Practice |
| `.specify/features/037-goal-registry.md` | 037 | `.specify/features/037-docs-command.md` | renamed | Docs Command |
| `.specify/features/038-goal-target.md` | 038 | `.specify/features/038-evidence-infrastructure.md` | renamed | Evidence Infrastructure |
| `.specify/features/039-session-export.md` | 039 | `.specify/features/039-harvested-harness-improvements.md` | renamed | Harvested Harness Improvements |
| `.specify/features/040-agent-metadata-portability.md` | 040 | `.specify/features/040-token-efficiency-discipline.md` | renamed | Token Efficiency Discipline |
| `.specify/features/041-refactor-feedback-probe.md` | 041 | `.specify/features/041-goal-registry.md` | renamed | Goal Registry |
| `.specify/features/042-goal-team-creation.md` | 042 | `.specify/features/042-interview-mode.md` | renamed | Interview Mode |
| `.specify/features/043-init-commit-stamp.md` | 043 | `.specify/features/043-session-export.md` | renamed | Session Export |
| `.specify/features/044-reduce-confirmation-flows.md` | 044 | `.specify/features/044-agent-metadata-portability.md` | renamed | Agent Metadata Portability |
| `.specify/features/045-sanitize-command.md` | 045 | `.specify/features/045-framework-source-provenance.md` | renamed | Framework Source Provenance |
| `.specify/features/046-confirmation-gate-governance.md` | 046 | `.specify/features/046-confirmation-gate-governance.md` | unchanged | Confirmation Gate Governance |
| `.specify/features/047-feedback-introspection.md` | 047 | `.specify/features/047-framework-material-hygiene.md` | renamed | Framework Material Hygiene |
| `.specify/features/048-derive-command.md` | 048 | `.specify/features/048-browser-utils-skill.md` | renamed | Browser Utils Skill |
| `.specify/features/049-docs-reconcile.md` | 049 | `.specify/features/049-derivation-command.md` | renamed | Derivation Command |
| `.specify/features/050-proactive-flow-trigger.md` | 050 | `.specify/features/050-proactive-flow-trigger.md` | unchanged | Proactive Flow Trigger |
| `.specify/features/051-user-facing-comprehension.md` | 051 | `.specify/features/051-user-facing-comprehension.md` | unchanged | 面向用户可理解性纪律(User-Facing Comprehension) |
| `.specify/features/052-fast-fail-principle.md` | 052 | `.specify/features/052-fast-fail-principle.md` | unchanged | 快速失败纪律(Fast Fail) |
| `.specify/features/053-machine-decidable-artifacts.md` | 053 | `.specify/features/053-machine-decidable-artifacts.md` | unchanged | 机器可判定的制品命题(Machine-Decidable Artifact Propositions) |
| `.specify/features/055-conflict-free-stores.md` | 055 | `.specify/features/055-conflict-free-stores.md` | unchanged | 冲突无关的 Feedback/Memory 存储(Conflict-Free Stores) |
| `.specify/features/056-probe-handler-system.md` | 056 | `.specify/features/056-probe-handler-system.md` | unchanged | Probe-Handler 体系 |
| `.specify/features/057-decompose-command-skills.md` | 057 | `.specify/features/057-decompose-command-skills.md` | unchanged | 命令技能化分解补全 |
| `.specify/features/058-sdd-loop-driver.md` | 058 | `.specify/features/058-sdd-loop-driver.md` | unchanged | 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver） |
| `.specify/features/059-exec-quant-recording.md` | 059 | `.specify/features/059-exec-quant-recording.md` | unchanged | Agent+LLM 执行量化记录(Execution Quant Recording) |
| `.specify/features/060-decompose-subagent-dispatch.md` | 060 | `.specify/features/060-decompose-subagent-dispatch.md` | unchanged | 「驱动子代理」机制的技能化分解与公用化 |
| `.specify/features/061-subagent-cli-config.md` | 061 | `.specify/features/061-subagent-cli-config.md` | unchanged | 子代理 CLI 配置管理与按派发量化 |
| `.specify/features/062-humanize-command.md` | 062 | `.specify/features/062-humanize-command.md` | unchanged | Humanize Command（动作输出人类友好化） |
| `.specify/features/063-review-p1-governance.md` | 063 | `.specify/features/063-review-p1-governance.md` | unchanged | Review P1 Governance（评审 P1 治理） |
| `.specify/features/064-subagent-concurrency.md` | 064 | `.specify/features/064-subagent-concurrency.md` | unchanged | Subagent 并发归属、CLI 能力档案与生命周期解耦（Subagent Concurrency, CLI Profiles, and Lifecycle Decoupling） |
| `.specify/features/065-loop-interruption-recovery.md` | 065 | `.specify/features/065-loop-interruption-recovery.md` | unchanged | SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery） |
| `.specify/features/068-exec-quant-feedback-channel.md` | 068 | `.specify/features/068-exec-quant-feedback-channel.md` | unchanged | 执行量化数据反馈回传与汇总(Exec-Quant Feedback Channel) |
| `.specify/features/070-subagent-task-teams.md` | 070 | `.specify/features/070-subagent-task-teams.md` | unchanged | 驱动子代理的任务拆解与配合机制（Task Decomposition & Team Coordination for Subagent-Driven SDD） |
| `.specify/features/069-execution-expression-sdd.md` | 069 | `.specify/features/069-execution-expression-sdd.md` | unchanged | 执行/表达二元分类与文档型 SDD 同构（Execution/Expression Classes & Document-Form SDD） |
| `.specify/features/071-review-code-integration.md` | 071 | `.specify/features/071-review-code-integration.md` | unchanged | Review 命令与代码评审技能的组合与治理（Review × Code-Review Composition） |
| `.specify/features/072-client-self-improvement.md` | 072 | `.specify/features/072-client-self-improvement.md` | unchanged | 客户项目的持续反馈与自我提升（Client-Project Feedback & Self-Improvement） |
| `.specify/features/073-record-retention-and-housekeeping.md` | 073 | `.specify/features/073-record-retention-and-housekeeping.md` | unchanged | 记录消费回收与 SDD 项目管家（Record Retention & SDD House-Keeping） |
| `.specify/features/074-goal-team-sdd-unification.md` | 074 | `.specify/features/074-goal-team-sdd-unification.md` | unchanged | Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation） |
| `.specify/features/076-decision-tension-contract.md` | 076 | `.specify/features/076-decision-tension-contract.md` | unchanged | 决策反题与反指标契约（Decision Tension Record） |
| `.specify/features/077-doc-sdd-integration.md` | 077 | `.specify/features/077-doc-sdd-integration.md` | unchanged | 项目文档的 SDD 接入（特性级类别与文档型阶段门禁） |
| `.specify/features/078-coaching-skills.md` | 078 | `.specify/features/078-coaching-skills.md` | unchanged | Coaching Skills（教练技能） |
| `.specify/features/079-bilingual-expression.md` | 079 | `.specify/features/079-bilingual-expression.md` | unchanged | 双语表述（Bilingual Expression） |
| `.specify/features/081-acceptance-hardening.md` | 081 | `.specify/features/081-acceptance-hardening.md` | unchanged | 更严格的验收与产物审查（Stricter Acceptance & Artifact Review） |
| `.specify/features/082-self-explanatory-integration.md` | 082 | `.specify/features/082-self-explanatory-integration.md` | unchanged | Self-Explanatory Framework Integration（不言自明的框架集成） |
| `.specify/features/083-mechanism-policy-separation.md` | 083 | `.specify/features/083-mechanism-policy-separation.md` | unchanged | 元技能治理：机制/策略分离与技能引用归一化（Meta-Skill Governance: Mechanism–Policy Separation & Skill Reference Grammar） |
| `.specify/features/084-harness-triple-structure.md` | 084 | `.specify/features/084-harness-triple-structure.md` | unchanged | Harness 三重结构（markdown + yaml + script） |
| `.specify/features/085-sdd-temporary-goal-team.md` | 085 | `.specify/features/085-sdd-temporary-goal-team.md` | unchanged | SDD 临时 Goal / 临时 Team 与多 Agent 并发（SDD Temporary Goal/Team and Multi-Agent Concurrency） |
| `.specify/features/086-efficient-test-execution.md` | 086 | `.specify/features/086-efficient-test-execution.md` | unchanged | 测试高效执行（默认并发） |
| `.specify/features/087-arch-diagram-docs.md` | 087 | `.specify/features/087-arch-diagram-docs.md` | unchanged | 架构图为核心的文档空间（Architecture-Diagram-Centric Documentation Space） |
| `.specify/features/088-speckit-visualization.md` | 088 | `.specify/features/088-speckit-visualization.md` | unchanged | Speckit 框架可视化（Speckit Framework Visualization） |
| `.specify/features/089-script-interface-contract.md` | 089 | `.specify/features/089-script-interface-contract.md` | unchanged | 脚本接口契约（Script Interface Contract） |
| `.specify/features/090-re-anchoring.md` | 090 | `.specify/features/090-re-anchoring.md` | unchanged | Re-Anchoring（不忘初心 · 温故而知新） |
| `.specify/features/092-non-disposable.md` | 092 | `.specify/features/092-non-disposable.md` | unchanged | Non-Disposable（不可一次性处置） |
| `.specify/features/091-auto-git-closeout.md` | 091 | `.specify/features/091-auto-git-closeout.md` | unchanged | Automatic git Close-out（自动收口） |
| `.specify/features/094-goal-team-parallel.md` | 094 | `.specify/features/094-goal-team-parallel.md` | unchanged | Goal/Team Parallel（目标/施工队 × spec 并行） |
| `.specify/features/093-concurrency-by-default.md` | 093 | `.specify/features/093-concurrency-by-default.md` | unchanged | Concurrency by Default（subagent 并发作为框架基本属性） |

Slug source by group: 57 unchanged files retain a slug that already names their content (exact, recognized shortening, or translation). The 32 renamed files take their content-title slug; for rows whose Spec Path slug names the same feature the two agree (`020` Qoder Support, `025` Todo Command, `037` Docs Command, ...).

## Collisions

None. Every target `<true-id>-<slug>.md` was free before the move; prefixes are unique, so no two sources map to one target. No file was overwritten.

## Registry-cell diffs (32)

| Row | Before | After |
|---|---|---|
| 006 | `.specify/features/006-add-qoder-support.md` | `.specify/features/006-feature-command.md` |
| 009 | `.specify/features/009-claude-code-support.md` | `.specify/features/009-plan-command.md` |
| 012 | `.specify/features/012-skill-home-workdir.md` | `.specify/features/012-review-command.md` |
| 013 | `.specify/features/013-portable-skill-creation.md` | `.specify/features/013-skills-command.md` |
| 018 | `.specify/features/018-cli-priority-support.md` | `.specify/features/018-configuration-management.md` |
| 020 | `.specify/features/020-speckit-todo-command.md` | `.specify/features/020-qoder-support.md` |
| 021 | `.specify/features/021-agent-specific-config.md` | `.specify/features/021-claude-code-support.md` |
| 023 | `.specify/features/023-agent-framework-redesign.md` | `.specify/features/023-prompt-template-quality.md` |
| 024 | `.specify/features/024-agent-env-config.md` | `.specify/features/024-specification-workspace-versioning.md` |
| 025 | `.specify/features/025-agent-skill-enablement.md` | `.specify/features/025-todo-command.md` |
| 027 | `.specify/features/027-feedback-mechanism.md` | `.specify/features/027-team-management.md` |
| 028 | `.specify/features/028-sdd-workflow-refactor.md` | `.specify/features/028-feedback-mechanism.md` |
| 029 | `.specify/features/029-glossary-mechanism.md` | `.specify/features/029-shared-reference-directory.md` |
| 030 | `.specify/features/030-summarize-project.md` | `.specify/features/030-history-command.md` |
| 031 | `.specify/features/031-task-complexity-rubric.md` | `.specify/features/031-glossary-mechanism.md` |
| 032 | `.specify/features/032-dogfooding-practice.md` | `.specify/features/032-task-complexity-rubric.md` |
| 033 | `.specify/features/033-docs-command.md` | `.specify/features/033-agent-project-context-parameterization.md` |
| 034 | `.specify/features/034-evidence-infra.md` | `.specify/features/034-ci-cd-pipeline.md` |
| 035 | `.specify/features/035-token-efficiency.md` | `.specify/features/035-code-quality-tooling.md` |
| 036 | `.specify/features/036-team-summary.md` | `.specify/features/036-dogfooding-practice.md` |
| 037 | `.specify/features/037-goal-registry.md` | `.specify/features/037-docs-command.md` |
| 038 | `.specify/features/038-goal-target.md` | `.specify/features/038-evidence-infrastructure.md` |
| 039 | `.specify/features/039-session-export.md` | `.specify/features/039-harvested-harness-improvements.md` |
| 040 | `.specify/features/040-agent-metadata-portability.md` | `.specify/features/040-token-efficiency-discipline.md` |
| 041 | `.specify/features/041-refactor-feedback-probe.md` | `.specify/features/041-goal-registry.md` |
| 042 | `.specify/features/042-goal-team-creation.md` | `.specify/features/042-interview-mode.md` |
| 043 | `.specify/features/043-init-commit-stamp.md` | `.specify/features/043-session-export.md` |
| 044 | `.specify/features/044-reduce-confirmation-flows.md` | `.specify/features/044-agent-metadata-portability.md` |
| 045 | `.specify/features/045-sanitize-command.md` | `.specify/features/045-framework-source-provenance.md` |
| 047 | `.specify/features/047-feedback-introspection.md` | `.specify/features/047-framework-material-hygiene.md` |
| 048 | `.specify/features/048-derive-command.md` | `.specify/features/048-browser-utils-skill.md` |
| 049 | `.specify/features/049-docs-reconcile.md` | `.specify/features/049-derivation-command.md` |

Status cells, descriptions and all dated `Last Updated` text are untouched.

## Self-reference repairs

- In each of the 27 renamed files that carried a `Feature Detail:` bullet, the bullet now cites the new filename (e.g. `.specify/features/013-skills-command.md`).
- The same commit produced 34 non-renamed files with a doubled `.specify/.specify/features/...` self-link; those bullets were corrected to `.specify/features/...` (in-passing correction, same line class as step 5).
- 58 `Feature Index:` bullets still cited the pre-move `.specify/memory/features.md`; corrected to `.specify/features.md`.
- No historical spec-directory references inside bodies were rewritten (e.g. `013-skills-command.md` still cites `013-portable-skill-creation` as the historical spec dir).

## Residual references intentionally left (dated or spec content)

- `.specify/specs/052-fast-fail-principle/requirements.md:20-21` and `.specify/specs/053-machine-decidable-artifacts/feature-ref.md:13` — line-numbered historical citations (`:59`, `:18`); rewriting would invalidate the cited line numbers.
- `.specify/archive/specs/046-browser-site-memory/tasks.md` — archived record.
- `.specify/specs/090-re-anchoring/test-evidence/spec-audit-*`, `spec-repair-*` — dated audit records.
- Detail-file body text that mentions the old registry anchor `.specify/memory/features.md` in status criteria or history (15 occurrences) — not self-referential lines; belongs to the broader anchor sweep.

## Verification (run after the change)

- 89 files; every name matches `^\d{3}-[a-z0-9-]+\.md$` (0 format failures).
- Every file's `**Feature ID**` equals its filename prefix (0 mismatches).
- Registry has 89 rows; every `Feature Details` cell resolves (0 dead); each file is cited exactly once (0 duplicates, 0 uncited).
- Every row's cited H1 corresponds to the row Name; the only non-identical pairs are translations or ellipses of the same feature (048 relocation suffix; 058/064/065/068/069/073/074/085 bilingual H1s; 086 English row / Chinese H1).
- `git status`: 32 rename entries (`R`/`RM`), `.specify/features.md` modified, `docs/reference/commands/goal.md` modified. Working-tree changes outside this repair (`trigger/index.json`, untracked exec-quant/feedback records) pre-existed and were not touched.

## Filesystem state (post-repair)

| File | H1 |
|---|---|
| `.specify/features/001-unify-command-handoffs.md` | Unify Command Handoffs |
| `.specify/features/002-analyze-command.md` | Analyze Command |
| `.specify/features/003-checklist-command.md` | Checklist Command |
| `.specify/features/004-clarify-command.md` | Clarify Command |
| `.specify/features/005-constitution-command.md` | Constitution Command |
| `.specify/features/006-feature-command.md` | Feature Command |
| `.specify/features/007-implement-command.md` | Implement Command |
| `.specify/features/008-instructions-command.md` | Instructions Command |
| `.specify/features/009-plan-command.md` | Plan Command |
| `.specify/features/010-requirements-command.md` | Requirements Command |
| `.specify/features/011-research-command.md` | Research Command |
| `.specify/features/012-review-command.md` | Review Command |
| `.specify/features/013-skills-command.md` | Skills Command |
| `.specify/features/014-tasks-command.md` | Tasks Command |
| `.specify/features/015-cli-interface.md` | CLI Interface |
| `.specify/features/016-refactor-tools-command.md` | Tools Command |
| `.specify/features/017-template-engine.md` | Template Engine |
| `.specify/features/018-configuration-management.md` | Configuration Management |
| `.specify/features/019-agents-command.md` | Agents Command |
| `.specify/features/020-qoder-support.md` | Qoder Support |
| `.specify/features/021-claude-code-support.md` | Claude Code Support |
| `.specify/features/022-ai-tools-support.md` | AI Tools Support |
| `.specify/features/023-prompt-template-quality.md` | Prompt Template Quality |
| `.specify/features/024-specification-workspace-versioning.md` | Specification Workspace Versioning |
| `.specify/features/025-todo-command.md` | Todo Command |
| `.specify/features/026-agent-skill-enablement.md` | Agent Skill Enablement |
| `.specify/features/027-team-management.md` | Team Management |
| `.specify/features/028-feedback-mechanism.md` | Feedback Mechanism |
| `.specify/features/029-shared-reference-directory.md` | Shared Reference Directory |
| `.specify/features/030-history-command.md` | History Command |
| `.specify/features/031-glossary-mechanism.md` | Glossary Mechanism |
| `.specify/features/032-task-complexity-rubric.md` | Task Complexity Rubric |
| `.specify/features/033-agent-project-context-parameterization.md` | Agent Project Context Parameterization |
| `.specify/features/034-ci-cd-pipeline.md` | CI/CD Pipeline |
| `.specify/features/035-code-quality-tooling.md` | Code Quality Tooling |
| `.specify/features/036-dogfooding-practice.md` | Dogfooding Practice |
| `.specify/features/037-docs-command.md` | Docs Command |
| `.specify/features/038-evidence-infrastructure.md` | Evidence Infrastructure |
| `.specify/features/039-harvested-harness-improvements.md` | Harvested Harness Improvements |
| `.specify/features/040-token-efficiency-discipline.md` | Token Efficiency Discipline |
| `.specify/features/041-goal-registry.md` | Goal Registry |
| `.specify/features/042-interview-mode.md` | Interview Mode |
| `.specify/features/043-session-export.md` | Session Export |
| `.specify/features/044-agent-metadata-portability.md` | Agent Metadata Portability |
| `.specify/features/045-framework-source-provenance.md` | Framework Source Provenance |
| `.specify/features/046-confirmation-gate-governance.md` | Confirmation Gate Governance |
| `.specify/features/047-framework-material-hygiene.md` | Framework Material Hygiene |
| `.specify/features/048-browser-utils-skill.md` | Browser Utils Skill |
| `.specify/features/049-derivation-command.md` | Derivation Command |
| `.specify/features/050-proactive-flow-trigger.md` | Proactive Flow Trigger |
| `.specify/features/051-user-facing-comprehension.md` | 面向用户可理解性纪律(User-Facing Comprehension) |
| `.specify/features/052-fast-fail-principle.md` | 快速失败纪律(Fast Fail) |
| `.specify/features/053-machine-decidable-artifacts.md` | 机器可判定的制品命题(Machine-Decidable Artifact Propositions) |
| `.specify/features/055-conflict-free-stores.md` | 冲突无关的 Feedback/Memory 存储(Conflict-Free Stores) |
| `.specify/features/056-probe-handler-system.md` | Probe-Handler 体系 |
| `.specify/features/057-decompose-command-skills.md` | 命令技能化分解补全 |
| `.specify/features/058-sdd-loop-driver.md` | 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver） |
| `.specify/features/059-exec-quant-recording.md` | Agent+LLM 执行量化记录(Execution Quant Recording) |
| `.specify/features/060-decompose-subagent-dispatch.md` | 「驱动子代理」机制的技能化分解与公用化 |
| `.specify/features/061-subagent-cli-config.md` | 子代理 CLI 配置管理与按派发量化 |
| `.specify/features/062-humanize-command.md` | Humanize Command（动作输出人类友好化） |
| `.specify/features/063-review-p1-governance.md` | Review P1 Governance（评审 P1 治理） |
| `.specify/features/064-subagent-concurrency.md` | Subagent 并发归属、CLI 能力档案与生命周期解耦（Subagent Concurrency, CLI Profiles, and Lifecycle Decoupling） |
| `.specify/features/065-loop-interruption-recovery.md` | SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery） |
| `.specify/features/068-exec-quant-feedback-channel.md` | 执行量化数据反馈回传与汇总(Exec-Quant Feedback Channel) |
| `.specify/features/070-subagent-task-teams.md` | 驱动子代理的任务拆解与配合机制（Task Decomposition & Team Coordination for Subagent-Driven SDD） |
| `.specify/features/069-execution-expression-sdd.md` | 执行/表达二元分类与文档型 SDD 同构（Execution/Expression Classes & Document-Form SDD） |
| `.specify/features/071-review-code-integration.md` | Review 命令与代码评审技能的组合与治理（Review × Code-Review Composition） |
| `.specify/features/072-client-self-improvement.md` | 客户项目的持续反馈与自我提升（Client-Project Feedback & Self-Improvement） |
| `.specify/features/073-record-retention-and-housekeeping.md` | 记录消费回收与 SDD 项目管家（Record Retention & SDD House-Keeping） |
| `.specify/features/074-goal-team-sdd-unification.md` | Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation） |
| `.specify/features/076-decision-tension-contract.md` | 决策反题与反指标契约（Decision Tension Record） |
| `.specify/features/077-doc-sdd-integration.md` | 项目文档的 SDD 接入（特性级类别与文档型阶段门禁） |
| `.specify/features/078-coaching-skills.md` | Coaching Skills（教练技能） |
| `.specify/features/079-bilingual-expression.md` | 双语表述（Bilingual Expression） |
| `.specify/features/081-acceptance-hardening.md` | 更严格的验收与产物审查（Stricter Acceptance & Artifact Review） |
| `.specify/features/082-self-explanatory-integration.md` | Self-Explanatory Framework Integration（不言自明的框架集成） |
| `.specify/features/083-mechanism-policy-separation.md` | 元技能治理：机制/策略分离与技能引用归一化（Meta-Skill Governance: Mechanism–Policy Separation & Skill Reference Grammar） |
| `.specify/features/084-harness-triple-structure.md` | Harness 三重结构（markdown + yaml + script） |
| `.specify/features/085-sdd-temporary-goal-team.md` | SDD 临时 Goal / 临时 Team 与多 Agent 并发（SDD Temporary Goal/Team and Multi-Agent Concurrency） |
| `.specify/features/086-efficient-test-execution.md` | 测试高效执行（默认并发） |
| `.specify/features/087-arch-diagram-docs.md` | 架构图为核心的文档空间（Architecture-Diagram-Centric Documentation Space） |
| `.specify/features/088-speckit-visualization.md` | Speckit 框架可视化（Speckit Framework Visualization） |
| `.specify/features/089-script-interface-contract.md` | 脚本接口契约（Script Interface Contract） |
| `.specify/features/090-re-anchoring.md` | Re-Anchoring（不忘初心 · 温故而知新） |
| `.specify/features/092-non-disposable.md` | Non-Disposable（不可一次性处置） |
| `.specify/features/091-auto-git-closeout.md` | Automatic git Close-out（自动收口） |
| `.specify/features/094-goal-team-parallel.md` | Goal/Team Parallel（目标/施工队 × spec 并行） |
| `.specify/features/093-concurrency-by-default.md` | Concurrency by Default（subagent 并发作为框架基本属性） |
