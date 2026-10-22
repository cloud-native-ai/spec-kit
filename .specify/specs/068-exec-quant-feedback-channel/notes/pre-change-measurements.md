# Pre-Change Measurements — 068 Exec-Quant Feedback Channel (T001)

- **Captured at (UTC)**: 2026-10-22T07:34:35Z
- **HEAD**: `4480ba7e4c6204b22094a9f49c4a19206077b44c` (branch `068-exec-quant-feedback-channel`)
- **Criterion this baseline freezes**: 后续一切镜像判据 = **相对本捕获零 NEW drift**；既有 DIFF 一律不归因本特性（捕获时零实现编辑）。

## 1. Mirror drift baseline — `sync-mirrors.py --check`

命令按 T001 任务行执行（`python3 -u scripts/python/sync-mirrors.py --check`；`-u` 仅禁用 stdout 缓冲，使 regen 子进程输出不与主进程块缓冲交错，语义与退出码不变）。**Exit code: 2**（检测到既有 drift——即被冻结的基线状态，非异常）。

逐对计数（另以 `--check --only <pair>` 六次标注运行核出；`--only` 跳过 regen 委托，后者由全量运行的收尾行单独覆盖）：

| Pair | DIFF entries | Note |
|---|---|---|
| templates → .specify/templates | 0 | `ok … (22 files)` |
| skills/external → .specify/skills | 62 | |
| skills/internal → .specify/skills/internal | 75 | 含 tasks.md § Environment Prerequisites 点名的 manage-feedback 3 文件 |
| agents → .specify/agents/templates | 2 | |
| scripts → .specify/scripts | 26 | 含 feedback-utils.py 1 行既有 DIFF（镜像侧 f265cfbd docstring 路径前缀）；`exec-quant.py` 对 `cmp` rc=0 字节一致（零 DIFF，与前提一致） |
| shared → .specify/shared | 37 | 含 tasks.md § Environment Prerequisites 点名的 `shared/workflow/feedback-step.md` |
| 逐工具命令副本（regen `--check` 委托） | 0 | `OK: all per-tool command copies match the source templates.` |
| **合计** | **202** | |

**Drift 类别诊断**（对抽样对做 `cmp`/`diff` 字节比对）：全部为**镜像侧路径前缀改写**类——镜像副本内路径引用带 `.specify/` 前缀（如 `.specify/shared/definitions/…`），而真源侧为仓库相对路径（如 `shared/definitions/…`）。样例：`fast-fail.md` 行 3、`implement-feature/SKILL.md` 行 20、`clause_extract.py` 行 6。这与状态脊已记录的 feedback-utils.py 1 行既有 DIFF（f265cfbd，镜像侧 docstring 路径前缀更新）同属一类。**归因**：继承自 init/投影时点的系统性状态，无一可归因本特性。

**与上游前提的范围关系**：tasks.md § Environment Prerequisites 仅点名本特性相关子集（feedback-utils.py 1 行 / manage-feedback 3 文件 / feedback-step.md / templates clean / exec-quant.py 零 DIFF）。复测确认其逐项字面成立（"含"成立），但该子集**不是**各对的完整 drift 状态；逐对完整权威名单以本文件附录 A 的全量原始输出为准（该行明文"逐对完整名单由 T001 落盘"）。

### Per-pair 完整名单

见附录 A 全量原始输出（202 条 `DIFF` 行，按 MIRROR_PAIRS 顺序：templates(ok) → skills/external → skills/internal → agents → scripts → shared → regen 委托(ok) → DRIFT 收尾行）。

## 2. `git status --short` 快照

```text
?? .specify/memory/exec-quant/records/20261022T064104611801Z-555a87c7.json
?? .specify/memory/exec-quant/records/20261022T064746217592Z-1811bb0f.json
?? .specify/memory/feedback/20261022T064104Z-speckit-requirements.md
?? .specify/memory/feedback/20261022T064746Z-speckit-clarify.md
?? feedback/feedback-20261022T062525Z.zip
```

以上 5 项全部属禁改/禁提交面（运行时记录 + 真实入站包），本快照仅记录其存在。

## 3. `git rev-parse HEAD`

```text
4480ba7e4c6204b22094a9f49c4a19206077b44c
```

## 4. T002 核验记录 — coverage-baseline.txt（不重冻结）

- 文件存在：`.specify/specs/068-exec-quant-feedback-channel/coverage-baseline.txt`，497 行（2 行 header + 495 条 frozen uncovered-clause 名）。
- `frozen-from:` 语义：存在（header 第 2 行），明示 `excluding 068-exec-quant-feedback-channel`、`base-sha: 7912b29d2539`、`files: 168 (parsed 85 + named 83)`。
- 复跑 `--freeze`（按 tasks.md T002 原命令，输出入临时文件比对）：**名字集与冻结文件完全一致（数据行 0 差异）**。仅 header 两处差异：`base-sha` 随后继制品提交前进（7912b29d2539 → 4480ba7e4c62）；`clause-rules:` 路径由镜像副本打印时带 `.specify/` 前缀（与 §1 同一类路径前缀改写）。
- 处置（按派发与 § Test Budget 纪律）：名字集相同 → **保留现有冻结文件，零 churn，不重冻结**。

## 5. 环境探针（T003 前提）

- `python3 -m pytest --version` → `pytest 8.4.2`（与 tasks.md § Environment Prerequisites 记录一致；`No module named pytest` 未发生，E2 槽位正常消耗）。
- `test-evidence/implement-baseline-full.log` 命中仓库 `.gitignore:37` 的 `*.log` 规则 → 日志文件保留在磁盘、不入特性提交；判定字段（rc / passed / failed / 名单路径）落在已提交的 `baseline-failed.txt` 与本文件 §6（状态脊账本行）中。

## 6. E2 全量基线执行记录（T003）

- **Command**（全量，无过滤参数）：`bash scripts/bash/run-tests.sh --names-out .specify/specs/068-exec-quant-feedback-channel/baseline-failed.txt`
- **执行窗口**：start `2026-10-22T07:37:00Z` → end `2026-10-22T07:41:33Z`，duration_s=273（pytest 自报 271.30s / 0:04:31）
- **rc**：`1`（pytest 存在失败即退出 1——即被冻结的基线失败集合，非运行故障）
- **计数**：collected 4551 / **passed 4467** / **failed 84** / warnings 3
- **失败名单**：84 行 → `baseline-failed.txt`（排序 nodeid，committed；closure 槽以 `comm -13 baseline-failed.txt current` 名字级比较，implement 期间零第二次全量）
- **全量捕获**：stdout+stderr 经 `tee` 完整落 `test-evidence/implement-baseline-full.log`（2347 行 / 158501 字节；命中 `*.log` ignore 规则 → 留盘不提交，判定字段以本节与 baseline-failed.txt 为准）
- **失败类别概览**（基线冻结内容，不逐一归因）：绝大多数为镜像字节一致性类（与 §1/附录 A 的 202 项继承性镜像路径前缀漂移同源，含 T027 预期转绿的 `test_feedback_step_reference_form.py::test_owner_mirror_is_byte_identical`）；另有 `tests/unit/test_loop_state_engine.py` 10 项等零散项。全部冻结为基线，零 NEW 判据在 closure 槽名字级执行。
- **槽位结论**：E2 baseline 槽消耗恰一次；pytest 8.4.2 可用 → 非 probe failure，槽位有效。

## Appendix A: full raw output — `python3 -u scripts/python/sync-mirrors.py --check`（205 行，rc=2）

```text
ok    templates/ == .specify/templates/ (22 files)
DIFF  .specify/skills/create-pages/SKILL.md
DIFF  .specify/skills/create-pages/references/hugo-site.md
DIFF  .specify/skills/create-pages/scripts/scaffold-ci.sh
DIFF  .specify/skills/create-skills/SKILL.md
DIFF  .specify/skills/create-skills/references/skill-creation-quality-checklist.md
DIFF  .specify/skills/database-utils/SKILL.md
DIFF  .specify/skills/database-utils/references/setup-and-usage.md
DIFF  .specify/skills/document-utils/SKILL.md
DIFF  .specify/skills/draw-diagram/SKILL.md
DIFF  .specify/skills/draw-diagram/assets/delivery.css
DIFF  .specify/skills/draw-diagram/references/merge-provenance/drawio.baseline.txt
DIFF  .specify/skills/draw-diagram/references/merge-provenance/echarts.baseline.txt
DIFF  .specify/skills/draw-diagram/references/merge-provenance/excalidraw.baseline.txt
DIFF  .specify/skills/draw-diagram/references/merge-provenance/mermaid.baseline.txt
DIFF  .specify/skills/draw-diagram/references/merge-provenance/plantuml.baseline.txt
DIFF  .specify/skills/draw-diagram/references/merge-provenance.md
DIFF  .specify/skills/draw-diagram/references/types/d3js/assets/template.html
DIFF  .specify/skills/draw-diagram/references/types/drawio/drawio.md
DIFF  .specify/skills/draw-diagram/references/types/drawio/references/mxgraph-format.md
DIFF  .specify/skills/draw-diagram/references/types/drawio/references/render-and-export.md
DIFF  .specify/skills/draw-diagram/references/types/echarts/assets/template.html
DIFF  .specify/skills/draw-diagram/references/types/echarts/best-practices/best-practices.md
DIFF  .specify/skills/draw-diagram/references/types/echarts/best-practices/pitfalls.md
DIFF  .specify/skills/draw-diagram/references/types/echarts/echarts.md
DIFF  .specify/skills/draw-diagram/references/types/echarts/references/echarts-guide.md
DIFF  .specify/skills/draw-diagram/references/types/echarts/references/sds-realization.md
DIFF  .specify/skills/draw-diagram/references/types/echarts/scripts/check-layout.mjs
DIFF  .specify/skills/draw-diagram/references/types/echarts/scripts/sync-config.mjs
DIFF  .specify/skills/draw-diagram/references/types/echarts/scripts/vendor-echarts.sh
DIFF  .specify/skills/draw-diagram/references/types/echarts/scripts/verify-deliverable.mjs
DIFF  .specify/skills/draw-diagram/references/types/excalidraw/excalidraw.md
DIFF  .specify/skills/draw-diagram/references/types/excalidraw/references/guide/server-deployment.md
DIFF  .specify/skills/draw-diagram/references/types/excalidraw/scripts/render-excalidraw.sh
DIFF  .specify/skills/draw-diagram/references/types/mermaid/mermaid.md
DIFF  .specify/skills/draw-diagram/references/types/mermaid/references/document/00-mermaid-overview.md
DIFF  .specify/skills/draw-diagram/references/types/mermaid/references/howto/12-rendering-and-output.md
DIFF  .specify/skills/draw-diagram/references/types/mermaid/references/howto/13-wbs-diagram.md
DIFF  .specify/skills/draw-diagram/references/types/mermaid/references/howto/14-gantt-diagram.md
DIFF  .specify/skills/draw-diagram/references/types/mermaid/server/README.md
DIFF  .specify/skills/draw-diagram/references/types/plantuml/plantuml.md
DIFF  .specify/skills/draw-diagram/references/types/plantuml/references/howto/10-layout-planning.md
DIFF  .specify/skills/draw-diagram/references/types/plantuml/references/howto/12-rendering-and-output.md
DIFF  .specify/skills/draw-diagram/references/types/plantuml/references/howto/15-mindmap-diagram.md
DIFF  .specify/skills/draw-diagram/references/types/plantuml/references/howto/17-yaml-diagram.md
DIFF  .specify/skills/git-utils/SKILL.md
DIFF  .specify/skills/git-utils/assets/ledger-template.md
DIFF  .specify/skills/git-utils/references/merge-provenance.md
DIFF  .specify/skills/git-utils/references/submodule-command-recipes.md
DIFF  .specify/skills/improve-docs/SKILL.md
DIFF  .specify/skills/improve-skills/SKILL.md
DIFF  .specify/skills/improve-skills/references/claude-code-guide.md
DIFF  .specify/skills/improve-skills/references/constraint-placement.md
DIFF  .specify/skills/improve-skills/references/copilot-guide.md
DIFF  .specify/skills/improve-skills/references/loop-playbook.md
DIFF  .specify/skills/improve-skills/references/skill-quality-checklist.md
DIFF  .specify/skills/improve-skills/references/skill-slimming-principles.md
DIFF  .specify/skills/improve-skills/scripts/redline-check.py
DIFF  .specify/skills/merge-skills/SKILL.md
DIFF  .specify/skills/merge-skills/references/content-extraction.md
DIFF  .specify/skills/merge-skills/references/decommission-and-wiring.md
DIFF  .specify/skills/merge-skills/references/restructure-mapping.md
DIFF  .specify/skills/think-skills/SKILL.md
DIFF  .specify/skills/internal/analyze-artifacts/SKILL.md
DIFF  .specify/skills/internal/analyze-artifacts/references/detection-and-severity.md
DIFF  .specify/skills/internal/analyze-artifacts/references/validation-and-report.md
DIFF  .specify/skills/internal/archive-session/SKILL.md
DIFF  .specify/skills/internal/clarify-artifact/SKILL.md
DIFF  .specify/skills/internal/collect-evidence/SKILL.md
DIFF  .specify/skills/internal/collect-evidence/references/evidence-discipline.md
DIFF  .specify/skills/internal/create-agent/SKILL.md
DIFF  .specify/skills/internal/create-agent/references/execution-config.md
DIFF  .specify/skills/internal/create-agent/templates/agent-capacity-knowledge-manager-template.md
DIFF  .specify/skills/internal/create-agent/templates/agent-capacity-module-designer-template.md
DIFF  .specify/skills/internal/create-agent/templates/agent-capacity-qa-engineer-template.md
DIFF  .specify/skills/internal/create-agent/templates/agent-capacity-requirements-analyst-template.md
DIFF  .specify/skills/internal/create-agent/templates/agent-capacity-system-designer-template.md
DIFF  .specify/skills/internal/create-agent/templates/agent-capacity-test-engineer-template.md
DIFF  .specify/skills/internal/create-agent/templates/agent-capacity-ux-analyst-template.md
DIFF  .specify/skills/internal/create-checklist/SKILL.md
DIFF  .specify/skills/internal/create-plan/SKILL.md
DIFF  .specify/skills/internal/create-requirements/SKILL.md
DIFF  .specify/skills/internal/create-tasks/SKILL.md
DIFF  .specify/skills/internal/create-tasks/references/phase-shapes.md
DIFF  .specify/skills/internal/create-team/SKILL.md
DIFF  .specify/skills/internal/create-team/references/capacity-vs-responsibility.md
DIFF  .specify/skills/internal/create-team/references/conceptual-model.md
DIFF  .specify/skills/internal/create-team/references/create-mode.md
DIFF  .specify/skills/internal/create-team/references/execution-guide.md
DIFF  .specify/skills/internal/create-team/references/goal.md
DIFF  .specify/skills/internal/create-team/references/patterns.md
DIFF  .specify/skills/internal/create-team/references/summary-mapping.md
DIFF  .specify/skills/internal/create-team/references/team-presets.md
DIFF  .specify/skills/internal/create-team/scripts/build-summary-input.py
DIFF  .specify/skills/internal/create-team/scripts/dispatch.sh
DIFF  .specify/skills/internal/create-team/scripts/stream-filter.py
DIFF  .specify/skills/internal/create-team/templates/agents/agent-team-supervisor-template.md
DIFF  .specify/skills/internal/create-tools/templates/tool-project-script-template.md
DIFF  .specify/skills/internal/derive-architecture/SKILL.md
DIFF  .specify/skills/internal/implement-feature/SKILL.md
DIFF  .specify/skills/internal/improve-agent/SKILL.md
DIFF  .specify/skills/internal/improve-agent/references/claude-code-guide.md
DIFF  .specify/skills/internal/improve-agent/references/copilot-guide.md
DIFF  .specify/skills/internal/improve-team/SKILL.md
DIFF  .specify/skills/internal/manage-agents/SKILL.md
DIFF  .specify/skills/internal/manage-constitution/SKILL.md
DIFF  .specify/skills/internal/manage-features/SKILL.md
DIFF  .specify/skills/internal/manage-feedback/SKILL.md
DIFF  .specify/skills/internal/manage-feedback/references/path-a-digest.md
DIFF  .specify/skills/internal/manage-feedback/references/path-b-and-probe.md
DIFF  .specify/skills/internal/manage-goal/SKILL.md
DIFF  .specify/skills/internal/manage-history/SKILL.md
DIFF  .specify/skills/internal/manage-instructions/SKILL.md
DIFF  .specify/skills/internal/manage-todo/SKILL.md
DIFF  .specify/skills/internal/research-feature/SKILL.md
DIFF  .specify/skills/internal/review-sdd-process/SKILL.md
DIFF  .specify/skills/internal/run-agent/SKILL.md
DIFF  .specify/skills/internal/run-interview/SKILL.md
DIFF  .specify/skills/internal/run-skills/SKILL.md
DIFF  .specify/skills/internal/run-team/SKILL.md
DIFF  .specify/skills/internal/sanitize-materials/SKILL.md
DIFF  .specify/skills/internal/self-improvement/SKILL.md
DIFF  .specify/skills/internal/study-project/references/uml-visualization-guide.md
DIFF  .specify/skills/internal/summarize-project/SKILL.md
DIFF  .specify/skills/internal/summarize-project/references/consistency-rules.md
DIFF  .specify/skills/internal/summarize-project/references/data-model.md
DIFF  .specify/skills/internal/summarize-project/references/degradation.md
DIFF  .specify/skills/internal/summarize-project/references/milestones.md
DIFF  .specify/skills/internal/summarize-project/references/people-encoding.md
DIFF  .specify/skills/internal/summarize-project/references/portability.md
DIFF  .specify/skills/internal/summarize-project/references/reporting-playbook.md
DIFF  .specify/skills/internal/summarize-project/references/required-info.md
DIFF  .specify/skills/internal/summarize-project/references/source-tiers.md
DIFF  .specify/skills/internal/summarize-project/references/task-progress.md
DIFF  .specify/skills/internal/summarize-project/schema/project.sql
DIFF  .specify/skills/internal/summarize-project/scripts/progress-engine.py
DIFF  .specify/skills/internal/summarize-project/scripts/validate-project-input.py
DIFF  .specify/skills/internal/summarize-project/scripts/verify-chart-data.py
DIFF  .specify/agents/templates/skill-verifier.agent.md
DIFF  .specify/agents/templates/structure-adjuster.agent.md
DIFF  .specify/scripts/bash/create-new-tools.sh
DIFF  .specify/scripts/bash/generate-instructions.sh
DIFF  .specify/scripts/bash/refresh-tools.sh
DIFF  .specify/scripts/js/better-harness/coding-agent-practices/inventory.mjs
DIFF  .specify/scripts/js/better-harness/session-analysis/analyzer.mjs
DIFF  .specify/scripts/js/better-harness/session-analysis/index.mjs
DIFF  .specify/scripts/js/better-harness/session-analysis/selection-profile.mjs
DIFF  .specify/scripts/js/better-harness/session-analysis.mjs
DIFF  .specify/scripts/python/account-clause-coverage.py
DIFF  .specify/scripts/python/clause_extract.py
DIFF  .specify/scripts/python/derive-utils.py
DIFF  .specify/scripts/python/execution-config.py
DIFF  .specify/scripts/python/feedback-utils.py
DIFF  .specify/scripts/python/gate-check.py
DIFF  .specify/scripts/python/goal-utils.py
DIFF  .specify/scripts/python/interview-utils.py
DIFF  .specify/scripts/python/probe-utils.py
DIFF  .specify/scripts/python/regen-command-copies.py
DIFF  .specify/scripts/python/run-determination.py
DIFF  .specify/scripts/python/sanitize-utils.py
DIFF  .specify/scripts/python/scan-confirmation-gates.py
DIFF  .specify/scripts/python/sync-mirrors.py
DIFF  .specify/scripts/python/tools-utils.py
DIFF  .specify/scripts/python/trigger-utils.py
DIFF  .specify/scripts/python/validate-requirements.py
DIFF  .specify/scripts/python/validate-tasks.py
DIFF  .specify/shared/constants/clarify-taxonomy.md
DIFF  .specify/shared/definitions/agent-definitions.md
DIFF  .specify/shared/definitions/contract-clause-definitions.md
DIFF  .specify/shared/definitions/derivation-definitions.md
DIFF  .specify/shared/definitions/dogfooding-definitions.md
DIFF  .specify/shared/definitions/framework-map.md
DIFF  .specify/shared/definitions/goal-definitions.md
DIFF  .specify/shared/definitions/probe-definitions.md
DIFF  .specify/shared/definitions/self-improvement-definitions.md
DIFF  .specify/shared/definitions/subagent-definitions.md
DIFF  .specify/shared/definitions/tool-definitions.md
DIFF  .specify/shared/guidelines/ask-record-repeat.md
DIFF  .specify/shared/guidelines/confirmation-gates.md
DIFF  .specify/shared/guidelines/critique-and-self-critique.md
DIFF  .specify/shared/guidelines/fast-fail.md
DIFF  .specify/shared/guidelines/proactive-trigger.md
DIFF  .specify/shared/guidelines/progress-reporting.md
DIFF  .specify/shared/guidelines/requirements-guidelines.md
DIFF  .specify/shared/guidelines/self-improvement.md
DIFF  .specify/shared/guidelines/single-run-evidence.md
DIFF  .specify/shared/guidelines/todo-in-context.md
DIFF  .specify/shared/guidelines/token-efficiency.md
DIFF  .specify/shared/guidelines/user-facing-comprehension.md
DIFF  .specify/shared/patterns/explicit-implicit-pattern.md
DIFF  .specify/shared/patterns/interview-pattern.md
DIFF  .specify/shared/patterns/reconcile-pattern.md
DIFF  .specify/shared/patterns/self-improvement-pattern.md
DIFF  .specify/shared/workflow/evidence-step.md
DIFF  .specify/shared/workflow/external-dispatch-recipes.md
DIFF  .specify/shared/workflow/feedback-step.md
DIFF  .specify/shared/workflow/glossary.md
DIFF  .specify/shared/workflow/interview-walkthrough.md
DIFF  .specify/shared/workflow/objective-analysis-gate.md
DIFF  .specify/shared/workflow/runtime-mode.md
DIFF  .specify/shared/workflow/self-improvement-workflow.md
DIFF  .specify/shared/workflow/symlink-model.md
DIFF  .specify/shared/workflow/user-input-protocol.md
OK: all per-tool command copies match the source templates.
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
```
