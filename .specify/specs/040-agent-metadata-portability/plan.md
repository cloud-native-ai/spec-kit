# Implementation Plan: 预置 Agent 定义的元信息中立化与按工具渲染分发

**Branch**: `040-agent-metadata-portability` | **Date**: 2026-08-13 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `040-agent-metadata-portability` → Feature 044 Agent Metadata Portability
**Input**: Specification from `.specify/specs/040-agent-metadata-portability/requirements.md`

## Summary

把 agent 定义改造成"中立元信息 + 正文"单文件结构(FR-001/002),元信息用工具无关词汇表达、消除现存 Qoder 方言(FR-005~008);`specify init --ai <tool>` 时经单一映射真源把中立元信息渲染为目标工具的真实 agent 文件,替代逐文件软链接(FR-009~018),并保住既有分发语义(渲染清单驱动的手改备份、失效清理、instance 优先、用户资产不覆盖,FR-019~022);同时按目录级 Worker/Meta 划分重排三目录:7 个角色定义迁入 `skills/create-agent/templates/` 的 Worker 能力模板序列,`agents/` 改由新作的框架维护型 Meta Agent 填充,差别与组队取件规则成文(FR-023~026)。

技术路径:渲染器、中立字段模式、工具映射表全部落在 `src/specify_cli/__init__.py`(单模块 CLI 的既有约定,`AGENT_CONFIG` 先例);映射每行带官方文档出处;渲染清单为 `.specify/agents/.render-manifest.json`(既有 `json.dump` 先例:`.vscode/settings.json`)。测试先行:契约测试按新语义改写/新增,全量基线对照(SC-008)。

## Technical Context

**Language/Version**: Python >= 3.8(`pyproject.toml`;渲染器与清单代码须保持 3.8 兼容,不用 `tomllib`/match/新类型语法)
**Primary Dependencies**: 仅 stdlib(`pathlib`、`json`、`hashlib`、`re`);CLI 面沿用 typer/rich,不新增依赖
**Storage**: 文件系统 —— 中立源 `.specify/agents/{templates,instances}/*.agent.md`;派生物 `<tool>/agents/`;渲染清单 `.specify/agents/.render-manifest.json`;手改备份 `.specify/agents/.backups/`
**Testing**: pytest(`contract` / `integration` 标记);改造前冻结基线(SC-008 前提)
**Target Platform**: Linux/macOS/Windows(specify-cli 三平台;软链接移除后 Windows 兼容性反而改善)
**Project Type**: CLI 框架(单模块包 `src/specify_cli/` + `templates/`/`skills/`/`agents/` 资产 + `scripts/` 引擎)
**Performance Goals**: 渲染全程 < 1s(10 个 agent 量级);确定性逐字节可复现(FR-015/SC-005)
**Constraints**: 不得写用户全局 config(codex 因此只留标注行,FR-012);未核实的映射条目必须显式标注待核实(FR-010);占位符不得进入渲染产物(FR-026)
**Scale/Scope**: 4 家渲染目标工具 × 每项目约 2~12 个 agent 定义;7 个角色定义迁移 + 2 个新作 Meta Agent + 1 张映射表 + 约 6 组测试改写 + 约 10 处文档/模板机械联动

**关键设计决策(Phase 0 取证后定案)**:

- **D1 元信息块 = frontmatter 键归属**:单文件、YAML frontmatter 内按"中立键集"划分元信息与正文,无需新文件格式(FR-002 已裁定)。
- **D2 中立键集(kebab-case,取代混杂命名)**:`name`、`description`、`user-invocable`、`disable-model-invocation`、`model-tier`、`capability-tools`、`skills`、`run-turn-budget`、`display-color`、`supervisor`、`capacity-scope`。`maxTurns`(camelCase 方言,[[STR-004]])→ `run-turn-budget`;`tools` → `capability-tools`(与正文内 "tool-call list" 术语区分);`color` → `display-color`;`model` → `model-tier`(取值域 `auto|efficient|performance|ultimate|none`,映射到各工具枚举)。框架键 `supervisor`/`capacity-scope` 保留但**不渲染给任何工具**(纯框架装配语义)。
- **D3 无对应物字段的统一策略(FR-013)**:**跳过 + 汇总报告** —— 渲染时不落该字段,init 反馈按 agent 汇总"哪些中立意图未被目标工具承载";策略文本记录在映射真源头部,对所有工具一致。
- **D4 映射真源形态**:Python dict 常量 `_AGENT_METADATA_MAPPING`(同 `AGENT_CONFIG` 先例),每工具一节:目标目录、文件名规则、逐字段转换函数/取值表、**出处行**(官方文档 URL 或"源码核实"+"待核实"标志)。契约测试断言:覆盖 `AGENT_CONFIG` 全部 6 工具(4 渲染行 + 2 标注行,SC-003)、交付时无"待核实"行。
- **D5 渲染清单与手改保护(FR-021)**:`.render-manifest.json` 记 `{相对路径: {source_rel, sha256_rendered}}`;再渲染时:清单内且哈希一致 → 直接覆盖刷新;清单内但不一致 → 备份至 `.specify/agents/.backups/<tool>/<name>.<ts>.agent.md` 再覆盖并报告;清单外且无中立源对应 → 视为用户资产不触碰;中立源已删 → 产物清理(手改过的同样先备份)。
- **D6 迁移落法(第二轮澄清选项 B)**:7 个角色定义**替换**现有较薄的 `agent-capacity-<slug>-template.md`(同一角色双源违反单一真源);迁入时 frontmatter 转中立键集,正文保持原样,**仅**把项目身份行与 Project Context 段的 "Spec Kit (specify-cli)" 参数化为 `{{PROJECT_NAME}}`(占位符白名单内,create-agent 实例化时已解析该占位符)——这是迁移的机械联动,不是正文重写(Out of Scope 首条已界定)。
- **D7 `agents/` 新作 Meta Agent 初始集**:`structure-adjuster`(调整项目结构,对应用户例一)与 `skill-verifier`(验证技能执行效果,对应用户例二),中立元信息、`user-invocable: true`、操作对象限定技能/agent/结构。Team Supervisor 仍留在 create-team 模板(团队域按需实例化),不在本轮重复落地。
- **D8 分发语义迁移**:`ensure_per_file_agent_links()` 退役(登记 `_OBSOLETE_*` 与否按实现期判断:函数被测试直接引用,先改写测试再删函数);`_AGENT_LINK_DIRS` 由 `_AGENT_RENDER_DIRS`(4 家)替换;instance-beats-template、execution 层不分发、仅 `*.agent.md` 等语义在渲染路径原样重建。
- **D9 刷新入口**:本轮只在 init 渲染;`/speckit.instructions`、`/speckit.agents` 不新增渲染调用(Assumptions 已声明复用同一函数,留待后续)。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.9.1):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 本计划全部设计可回溯 requirements.md 的 28 条 FR;先契约测试后实现(见 contracts/) |
| II | Feature-Centric Development | ✅ Pass | feature-ref.md 记录 Feature 044 绑定;状态 Draft→Planned 由本命令推进 |
| III | Intent-Driven Development | ✅ Pass | 中立键集按"意图"命名(可调用性/能力白名单/规模上限),工具字段只是渲染投影(D2/D4) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | contracts/ 四份契约先行;测试改写清单在 tasks 阶段先红后绿;SC-008 基线纪律 |
| V | AI Agent Integration Standards | ✅ Pass | 支持面不变(6 家,`AGENT_CONFIG`);渲染矩阵 FR-012 与 Tier 划分一致;映射出处为各工具官方文档(FR-010) |
| VI | Continuous Quality & Observability | ✅ Pass | init tracker 报告渲染计数与备份(FR-018/FR-021);未承载字段汇总报告(D3) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本文件为工作流第二棒;clarify 两轮 8 条澄清已固化进 spec |
| VIII | Code as the Single Source of Truth | ✅ Pass | 中立源 `.specify/agents/` 为唯一定义真源;渲染产物为派生件(FR-016);角色定义单源化(D6) |
| IX | Framework Scope Discipline (No Over-Engineering) | ⚠ Partial — see Complexity Tracking | 渲染清单+备份机制超出"最小可用",但由 FR-021 直接要求;codex TOML 渲染被明确拒绝进 scope |
| X | Documentation Naming & Location Conventions | ✅ Pass | 文档联动清单见 Mirror Obligations;不改根目录大写条目;差别定义落 `docs/reference/agents/`(FR-023) |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本仓库即首个消费方:改造后 spec-kit 自身的 `.qoder/agents/` 等即为渲染产物;反馈回路沿用 Feature 028 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `json.dump` 清单先例、`AGENT_CONFIG` 常量先例、sync-mirrors 既有镜像对;无新脚本引擎 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 映射出处行 + 待核实归零(SC-003)是"configured ≠ used"证据纪律的落实;反馈步骤照常 |

**Gates Status**: ✅ All gates pass(IX 为 Partial,已在 Complexity Tracking 论证)

**Re-check after Phase 1**: 2026-08-13 —— Phase 1 产出(data-model/4 contracts/quickstart/feature-ref)落盘后复核:结论不变,IX 的 Partial 论证维持(清单机制是 FR-021 的必要实现而非附加功能);无新增违规。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/040-agent-metadata-portability/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── neutral-metadata-schema.md
│   ├── tool-mapping.md
│   ├── render-pipeline.md
│   └── relocation-taxonomy.md
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── checklists/requirements.md  # /speckit.requirements 产物(已全绿)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

No standalone research.md — Phase 0 findings(两轮 clarify 的外部格式核实 + 本轮代码取证)已内联于 Technical Context 与 requirements.md 现状锚点。

### Source Code (repository root)

```text
src/specify_cli/                # 单模块 CLI:新增中立键集/映射表/渲染函数,退役 _AGENT_LINK_DIRS+ensure_per_file_agent_links,迁移路径与 tracker 反馈
agents/                         # 移除 7 个角色定义,新增 2 个 Meta Agent(structure-adjuster, skill-verifier);sync-mirrors 镜像对不变(→ .specify/agents/templates)
skills/create-agent/templates/  # 7 个 agent-capacity-<slug>-template.md 被迁入的角色定义替换(中立 frontmatter + {{PROJECT_NAME}} 参数化)
tests/contract/                 # test_shipped_agent_presets / test_role_templates / test_agents_symlink(改名 render 语义)/ test_agent_skill_enablement 按新契约改写;新增映射完备性与中立词表扫描测试
tests/integration/              # test_init_agents / test_persistent_agent_lifecycle 改为渲染语义(真实文件、清单、备份、幂等)
docs/reference/agents/          # templates-and-agents.md:目录级 Worker/Meta 划分 + 中立格式 + 移除 Qoder 基准表述([[STR-003]])与 crosswalk
docs/reference/commands/        # agents.md 等:软链接叙述 → 渲染叙述
docs/tutorials/quickstart.md    # 目录树与分发叙述更新
templates/commands/             # agents.md / skills.md 模板更新(含全部 per-tool 副本,经 regen-command-copies)
shared/workflow/                # agent-configuration.md:软链接核验 → 渲染产物核验
skills/create-skills/SKILL.md、skills/create-team/{references,templates}/、shared/workflow/interview-walkthrough.md  # 7-slug 枚举的机械联动
.specify/{templates,skills,shared,agents}/  # 上述全部改动的镜像侧(sync-mirrors.py --write)
AGENTS.md                       # Agents 注册表与分发叙述(经 /speckit.instructions 刷新,顺带修复缺 ux-analyst 的既有漂移)
.specify/memory/glossary.md     # 新增/修订条目(见 feature-ref.md 术语节,写入需用户确认)
```

**Structure Decision**: 不新增顶层目录;延续"代码生成器/框架"形态(`src/<package>/` + `templates/` + `skills/` + `agents/`)。唯一的新型持久产物是 `.specify/agents/.render-manifest.json` 与 `.specify/agents/.backups/`(均在既有 `_CORE_SPECIFY_ASSETS` 的 `.specify/agents` 保护伞下,不会被 init 清理误删)。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `agents/*`(7 删 + 2 增) | `.specify/agents/templates/`(sync-mirrors 对) | `python3 scripts/python/sync-mirrors.py --check` exit 0 |
| `skills/create-agent/templates/agent-capacity-*-template.md`(7 替换) | `.specify/skills/create-agent/templates/` | 同上 |
| `skills/create-skills/SKILL.md` | `.specify/skills/create-skills/SKILL.md` | 同上 |
| `skills/create-team/references/patterns.md`、`skills/create-team/templates/agents/agent-workflow-schema.md` | 对应 `.specify/skills/...` 副本 | 同上 |
| `shared/workflow/agent-configuration.md`、`shared/workflow/interview-walkthrough.md` | `.specify/shared/workflow/...` | 同上 |
| `templates/commands/agents.md`、`templates/commands/skills.md` | `.specify/templates/commands/*.md` + per-tool 副本(`.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/`、`.codex/commands/`、`.hermes/commands/`) | `python3 scripts/python/regen-command-copies.py` 后 grep 无旧软链接叙述 |
| `docs/**`(仅文档,无镜像) | — | docs-utils validate 无新增违规 |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle IX (Partial):渲染清单 + 备份目录是新增持久状态 | FR-021 要求"手改可取回 + 明示报告",在真实文件取代软链接后,没有清单就无法区分"派生产物"与"用户资产",也无法检测手改 | 纯文件名约定(如 `.local` 后缀)被拒:改变工具读取的文件名,破坏各工具官方目录约定;跳过保留(B 案)被用户在 clarify 拒绝(预置失去升级通道) |
| Principle IX (Partial):映射表按 6 工具全量建行(含 2 个标注行) | SC-003 要求覆盖全部受支持工具且"待核实"归零,标注行是 codex/hermes 的诚实占位 | 只建 4 渲染行被拒:未来补 codex 时无结构可挂,且 SC-003 的完备性断言失去对照面 |
