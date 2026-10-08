# Implementation Plan: Agent 定义到宿主注册面的接线(Agent Registration Wiring)

**Branch**: `054-agent-registration-wiring` | **Date**: 2026-10-08 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `054-agent-registration-wiring` → Feature 044 Agent Metadata Portability
**Input**: Specification from `.specify/specs/054-agent-registration-wiring/requirements.md`

## Summary

Feature 044(spec 040)交付了中性元数据 → 各工具真实格式的渲染器,但渲染链的**输入面与触发面**从未接线:框架的 agent 类(stage 帧与 capacity 类)无任何步骤安装进渲染输入,`render_agents_for_tool` 只从 `specify init` 内部可达,导致编排者派发席位时只能退回 `general-purpose` 通用载体。本计划按已裁定的方案 (b) 闭合该链:`create-team` 建队时经 `create-agent` 的委托入口把实际引用的席位实例化进 `.specify/agents/instances/`(占位符填全、带 `team-scope` 来源追溯),并在建队流程内直接执行渲染触发(新增窄 CLI 子命令 `specify render-agents --ai <tool>`);`/speckit.team modify`(路由至 improve-team)对存量团队 opt-in 回填(FR-014);三个教学面改教真实渲染模型(F-A02 死信终结);IDE agent 面关系入档;全部内容配漂移守卫与变异演练取证。

## Technical Context

**Language/Version**: Python `>=3.8`(CLI,per `pyproject.toml`);技能层为 prompt/markdown
**Primary Dependencies**: `typer`、`rich`(既有 CLI 框架,无新依赖)
**Storage**: 文件系统 —— `.specify/agents/{templates,instances}/`(中性层)、各工具宿主目录、`.specify/agents/.render-manifest.json`
**Testing**: `pytest`(`contract` marker;`tests/contract/`)
**Target Platform**: 跨平台 CLI(Linux/macOS);技能流程运行于六家受支持 agent CLI 之内
**Project Type**: 代码生成/框架(`templates/`, `scripts/`, `src/`, `skills/`, `shared/`)
**Performance Goals**: `specify render-agents` 单次运行处理少量 md 文件,秒级;无其他性能命题
**Constraints**: 无新依赖;框架范围纪律(Principle IX)——只暴露既有渲染器,不建运行时;客户项目以安装态 `specify` CLI 调用(`uv tool install` 隔离环境使"脚本 import `specify_cli` 模块"不可行)
**Scale/Scope**: 8 个 stage 帧 + 11 个 create-agent 模板;4 个渲染模式工具(qoder/claude/copilot/opencode);约 9 个源文件 + 各镜像面

**关键技术裁定(证据驱动)**:

1. **渲染触发 = 新增窄 CLI 子命令 `specify render-agents --ai <tool>`**(`--ai` 必填,单次渲染一个工具;验收演示以 4 次调用覆盖全部 4 个渲染模式工具,满足 US2 场景 1)。证据:渲染器唯一调用点在 init 内部(`src/specify_cli/__init__.py:2283`),CLI 现只有 `init`(:2653)与 `check`(:2993)两个子命令;重跑 init 过重且带整仓副作用,与 FR-004「直接执行渲染触发、失败披露」不符;脚本 import 模块在 uv/pipx 工具隔离下对下游项目不可达。**被拒替代**:教授重跑 `specify init`(重、副作用面大)、项目脚本 `from specify_cli import …`(环境脆弱)、独立渲染脚本(重复渲染器逻辑,违反复用与漂移纪律)。
2. **席位来源追溯 = 中性 frontmatter 键 `team-scope: <team-slug>`**,加入 `NEUTRAL_AGENT_METADATA_KEYS` 的 framework-only 段(`renders_to_tools=False`;先例 `role-scope`,`__init__.py:139`)。证据:校验器拒绝未知键(`:273-279`),故 FR-013 的可机读追溯必须进键集;命名沿用 `capacity-scope`/`role-scope` 的 `-scope` 家族。语义 owner:代码键集(Principle VIII,code-first),分类学条目由 `agent-definitions.md` 按引用记载。
3. **席位实例化 = create-team 以 create-agent 的既有委托入口(`AgentAuthoringRequest`,`skills/create-agent/SKILL.md:52-53`)按约定调用**,kind 走 instance 层;占位符全部解析(满足渲染器对作者模板的拒绝不变量,`:296-306`);与既有持久定义同名 slug 时冲突披露、不静默覆写(loader 的 instance-wins 语义不因建队而破坏)。
4. **FR-014 回填落在 improve-team 技能**:`/speckit.team modify` 路由至该技能(`templates/commands/team.md:45,52`),回填步在其 modify 流程内(opt-in,modify 由用户显式发起)。
5. **逐工具渲染语义与 init 一致**:init 以 `--ai <tool>` 渲染单工具(`:2283` 上下文),render-agents 沿用;`--ai` 不接受 annotated 模式工具(codex/hermes)——报错而非静默。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.13.0; 评分经同作者门委派新上下文只读子代理复核,见 Re-check):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每项设计裁定回溯 spec FR-004..014;`requirements.md` 2026-10-08 澄清后形态,校验器 0 error |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 044(clarify 2026-10-08);044 详情与索引行已更新;plan 阶段继续维护(见 Feature Integration) |
| III | Intent-Driven Development | ✅ Pass | what/why 先于 how;三处断点 + 损失陈述在 spec Overview,机制选择在本计划 Technical Context 带理由 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 守卫先行写进契约(`contracts/teaching-and-guards.md` C-7..C-9:STR-001 缺席钉、链路闭合、变异演练);render-agents 子命令配 pytest 契约测试 |
| V | AI Agent Integration Standards | ✅ Pass | 不新增 agent;工具面沿 `AGENT_CONFIG`/`_ASSISTANT_TIERS` 既有 roster;`--ai` 值域取自 `_AGENT_METADATA_MAPPING` |
| VI | Continuous Quality & Observability | ✅ Pass | render-agents 输出 stats(rendered/backups/unmapped,既有 `:615` 返回值),失败非零退出;镜像漂移由 sync-mirrors 核 |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | 复用优先绑定既有 Feature 044;044 状态保持 Implemented(无回退);Pre-Status-Flip 门留给 implement 阶段 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 本计划全部行为性事实以 `path:line` 实测复核(渲染器、CLI 子命令集、校验器键集、镜像对);spec Overview 同 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 只暴露既有渲染器为窄子命令,不建运行时;席位实例化走既有 prompt 委托约定,零新引擎;拒绝项记录于 Technical Context 裁定 1 |
| X | Documentation Naming & Location Concepts | ✅ Pass | 文档改动均落既有属主路径(agent-definitions/symlink-model/supported-agent-tools);无新保留名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子:全部改动落框架源(skills/templates/src/shared/tests/docs),镜像是生成物;本仓自身团队建队即吃自家狗粮 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 渲染触发复用 `render_agents_for_tool` 而非重写;无覆盖此能力的既有 Tool 记录,新子命令即复用载体 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution 维度:席位派发走受支持、可重复、携带配置的路径,替代散文注入 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 「宿主注册面」单 owner=agent-definitions.md(clarify 裁定);`team-scope` 语义 owner=代码键集,文档按引用;IDE 共享路径事实 owner=symlink-model.md 带来源 URL |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 教学面改写为面向未参与读者的真实模型陈述;建队流程的渲染步骤以命令 + 期望输出形式教授 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 触发失败披露不跳过(FR-004);冲突披露不覆写;守卫须变异演练取证(绿是主张非证据) |

**Gates Status**: ✅ All gates pass — 无 Fail/Partial 行,Complexity Tracking 记 N/A

**Re-check after Phase 1**: 2026-10-08 — 设计制品(data-model.md、contracts/ ×4、quickstart.md、feature-ref.md)落盘后,由新上下文只读子代理对 16 行逐一复核并执行完整性门(无残留占位符、单一 `# Implementation Plan:` 标题、Requirement→Feature 戳记、制品无内部推敲标记);复核结论见下文 Phase 1 之后补记的「Post-Design Re-check」。

## Phase 0: Research Review & Context

无独立 `research.md`(发现内联于此;外部源取证——Qoder IDE/CLI agent 目录共享——已在 spec 阶段完成并记录于 requirements.md Overview,此处不重复)。代码触点探查经 Explore 只读子代理完成(非降级路径),要点:

- **create-team 挂点**:6 步流程(`skills/create-team/SKILL.md:27-32`),席位解析在 create-mode.md 步 4(:14,「prefer existing agents … otherwise temporary stage/worker templates」),直接落地在步 6(:16)——**席位实例化 + 渲染触发插在 :14 与 :16 之间**;schema 注释 `:128`(「members MUST resolve to … or a temporary stage/worker template; unresolved members are surfaced as broken references」)即 FR-008 更新点。modify 无 create-team 侧 reference——路由到 improve-team(`templates/commands/team.md:45,52`)。
- **create-agent 可被委托**:prompt 技能但带结构化委托入口 `AgentAuthoringRequest`(`SKILL.md:52-53`:kind/role_slug/task/scoring_dimensions/environment_paths/…→`AuthoringResult`);kind→层映射(:37-43),instance 引用 template 须带 `capacity-scope:`(:111)——**stage 帧非已注册 template,席位实例不设 capacity-scope,由 team-scope 承载来源**。待修教学行:`SKILL.md:122`、`:127`。
- **渲染链现状**:`render_agents_for_tool(project_path, tool, tracker=None)`(`src/specify_cli/__init__.py:615`,真文件渲染/manifest 漂移/修剪/legacy 迁移),唯一调用点 `:2283`(init 内 `copy_local_templates`);CLI 仅 `init`(:2653)/`check`(:2993);技能层今日从不 subprocess specify CLI(grep 仅散见 prose)。
- **渲染清单**:`.specify/agents/.render-manifest.json`(`:544`,entries `{rel_path: {source, sha256}}`),仅渲染器自身与既有测试消费;SC-003 的「框架渲染产物」以它为判定面。
- **校验器键集**(`:119-148`):中性键 `name/description/user-invocable/disable-model-invocation/model-tier/capability-tools/skills/run-turn-budget/display-color` + framework-only `supervisor/capacity-scope/role-scope/project`(`renders_to_tools=False`);必填 `name`/`description`(:143);未知键拒绝(:273-279)、未解析占位符拒绝(:296-306)、Qoder 方言键禁止(:151-164)——**`team-scope` 须以 framework-only 键加入**。
- **镜像面**(`scripts/python/sync-mirrors.py:72-78`):skills↔`.specify/skills`、shared↔`.specify/shared`、agents↔`.specify/agents/templates`、templates(不含 commands)↔`.specify/templates`、scripts↔`.specify/scripts`;**docs/ 不镜像**;`templates/commands/agents.md` 经 regen-command-copies.py 扇出 4 份工具副本(`.claude/commands/`、`.github/prompts/`、`.opencode/command/`、`.qoder/commands/`,本仓无 `.hermes/commands` 故 5 注册 4 落地)。
- **守卫先例**:缺席钉 `test_shipped_surface_client_neutrality.py:30-63`(BANNED_PATTERNS + KNOWN_DEBT 白名单);变异演练 `test_fast_fail_discipline.py:795-814`(红+复原取证);team 路由钉 `test_team_command_routing.py`(机器可检标识,非散文)。
- **镜像基线(编辑前实测,2026-10-08)**:`python3 scripts/python/sync-mirrors.py --check` → exit 0,零漂移(全部 `ok templates/ (22) / skills/ (455) / agents/ (2) / scripts/ (107) / shared/ (46)`);验证判据为「本 spec 触及的镜像对**无新增**漂移」。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/054-agent-registration-wiring/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

No standalone research.md — findings inlined above.

### Source Code (repository root)

```text
src/specify_cli/            # render-agents 子命令 + team-scope 中性键(校验器键集)——唯一运行时代码改动
skills/create-team/         # 席位实例化步 + 渲染触发步(SKILL.md、references/create-mode.md:含 :128 schema 注)
skills/improve-team/        # FR-014 modify 时席位回填步
skills/create-agent/        # 退役 symlink 教学修正 + team-scope 作者键(SKILL.md:122/:127 及键集段)
templates/commands/         # agents.md:真实渲染模型 + 触发真相(无 .specify 镜像,扇出 4 工具副本)
shared/definitions/         # agent-definitions.md:「宿主注册面」定义 owner + 席位实例分类学
shared/workflow/            # symlink-model.md:agent 面 CLI/IDE 关系条目(FR-009)
docs/reference/cli/         # supported-agent-tools.md:qoder agent 面说明(FR-010,不镜像)
tests/contract/             # 守卫:STR-001 缺席钉、render-agents CLI 契约、席位实例化契约、变异演练取证
```

**Structure Decision**: 本 spec 是「代码生成/框架」形态上的**链路补线**:1 处运行时代码改动(暴露既有渲染器为窄子命令 + 1 个 frontmatter 键)、3 个技能流程步插入、2 个教学面改写、3 处属主文档增补、1 组守卫测试;无新顶层目录。

### Mirror Obligations *(mandatory)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/create-team/SKILL.md` | `.specify/skills/create-team/SKILL.md`(sync-mirrors skills 对) | `python3 scripts/python/sync-mirrors.py --check` 对本 spec 触及的镜像对**无新增**漂移(基线 2026-10-08 实测:exit 0 全净) |
| `skills/create-team/references/create-mode.md` | `.specify/skills/create-team/references/create-mode.md` | 同上 |
| `skills/improve-team/SKILL.md`(及其触及的 references) | `.specify/skills/improve-team/**` 对应件 | 同上 |
| `skills/create-agent/SKILL.md` | `.specify/skills/create-agent/SKILL.md` | 同上 |
| `shared/definitions/agent-definitions.md` | `.specify/shared/definitions/agent-definitions.md` | 同上 |
| `shared/workflow/symlink-model.md` | `.specify/shared/workflow/symlink-model.md` | 同上 |
| `templates/commands/agents.md` | 4 份工具副本:`.claude/commands/speckit.agents.md`、`.github/prompts/speckit.agents.prompt.md`、`.opencode/command/speckit.agents.md`、`.qoder/commands/speckit.agents.md`(经 `scripts/python/regen-command-copies.py`;无 `.specify/templates/commands/` 镜像——已退役) | 副本重生成后 `regen-command-copies.py` 校验通过、副本含改动(`diff -q` 对源);镜像基线同上 |
| `src/specify_cli/__init__.py`、`docs/reference/cli/supported-agent-tools.md`、`tests/contract/*` | 无镜像(源码/文档/测试面) | N/A |

## Complexity Tracking

N/A — Constitution Check 无 Fail/Partial 行(经子代理复核确认,见 Post-Design Re-check)。

## Post-Design Re-check

2026-10-08 — 设计制品(data-model.md、contracts/ ×4、quickstart.md、feature-ref.md)落盘后,新上下文只读子代理对 16 项原则逐行独立评分并执行完整性门。结果:

- **宪法 16/16 ✅ Pass,与预评零分歧**(子代理逐行给出证据;IX 的「子命令是否过度工程」经独立论证维持 Pass——三替代各有证据拒绝;XIV 记一条残留观察:FR-010 使 supported-agent-tools.md 对 IDE 共享路径作第二处 authored 陈述,系 spec 已批准、受 B-4 指针形约束、可判定,不破下游)。
- **完整性门 4/4**:plan 无残留 `[UPPER_SNAKE_CASE]` 占位符(扫描空);恰一个 `# Implementation Plan:` 顶标题;Requirement→Feature 戳记在位(line 4);模板自指 Note 行已移除。
- **推敲标记扫描**:8 类标记跨全部制品零命中。
- **跨制品一致性**:FR-001..014 全部在 feature-ref 映射(无漏);`[[STR-001]]` 引用形态在契约面完整;quickstart 免责示例均带前提;契约间无实质矛盾。
- **子代理 ANOMALY 行报 3 项非阻塞,均按纠正类当场修复**:① modify-backfill C-4.2 悬空指针(引用了不存在的 teaching-and-guards C-4——已改指 §A 并声明归属本契约);② plan 的 `check` 锚点笔误 `:293` → 实测 `:2993`(装饰器)/`:2994`(def)——已改两处;③ quickstart 用 `<STR-001 字面>` 而非引用形态——已改 `[[STR-001]]` + 代入注。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 4 实体(Seat Instance、Render Trigger Command、Host Registration Surface、Render Manifest) |
| Contracts | [`contracts/`](contracts/) | 4 件:`seat-instantiation.md`(FR-004 实例化半/006/008/013)、`render-trigger-cli.md`(FR-004 触发半/005)、`modify-backfill.md`(FR-014)、`teaching-and-guards.md`(FR-001..003/009..012 + F-A02 核销条件) |
| Quickstart | [`quickstart.md`](quickstart.md) | 3 场景(建队端到端、modify 回填、接线核验——场景 3 的镜像检查为今日实测并粘贴真实输出,其余逐示例免责 + 前提) |
| Feature ref | [`feature-ref.md`](feature-ref.md) | Feature 044 绑定映射(FR → 契约 → 落点,全 14 FR 覆盖) |

计数取自实跑(2026-10-08,于制品落盘后):`grep -c "^## Entity" data-model.md` → **4**;`ls contracts/*.md | wc -l` → **4**(件名如上);`grep -c "^## Scenario" quickstart.md` → **3**;占位符扫描 `grep -cE '\[(PLACEHOLDER|[A-Z_]{4,})\]'` 对 8 份制品全为 **0**;镜像基线 `python3 scripts/python/sync-mirrors.py --check` → **exit 0**(`templates/ (22) / skills/ (455) / agents/ (2) / scripts/ (107) / shared/ (46)` 全 ok,输出已粘贴于 quickstart 场景 3)。计数模式的非目标匹配前提:`^## Entity` 与 `^## Scenario` 为标题锚定,制品内无同形非目标行(实测计数与制品目视清单一致)。
