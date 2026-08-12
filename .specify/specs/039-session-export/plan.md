# Implementation Plan: Session 导出与导出侧重命名(/speckit.session + export-session 通用化)

**Branch**: `039-session-export` | **Date**: 2026-08-12 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `039-session-export` → Feature 043 Session Export
**Input**: Specification from `.specify/specs/039-session-export/requirements.md`

## Summary

宿主 AI agent CLI 的会话不可命名、难以归档追溯。本计划落地规格 039 的降级路线:新增 `/speckit.session` 命令(首版 `export` 子命令),把当前(或指定)会话导出为**用户命名的目录**,附带**会话描述文档**(元信息 + 结构化总结)。执行面是对既有 `skills/export-session`(v1.3.0,单脚本 2093 行,10 产品)的彻底改造:支持面收敛为恰好六家 AI agent CLI(保留并适配 claude-code / codex-cli / qoder-cli / opencode 四家既有适配器,新增 copilot / hermes 两家,移除 qwen-code / qoder-IDE / qoderwork / oh-my-pi / kimi-code / codex-app 六家),通用化(去 aone-open 平台依赖),产物形态 zip → 目录,定位机制与五值退出码保持。

核心不变量:导出对宿主会话存储**只读**;命名完全由用户掌握(`--name` 必填);覆盖无旁路标志(交互式确认);描述文档的元信息全部程序确定性提取,结构化总结忠实于记录、超预算程序判定降级。

## Technical Context

**Language/Version**: Python ≥ 3.8(export.py 为 stdlib-only 单脚本,sqlite3 只读 URI 模式;命令模板为 Markdown)
**Primary Dependencies**: 无新增运行时依赖;测试用 `pytest`(markers `contract` / `integration`);六家 CLI 的会话存储为输入面(只读)
**Storage**: 文件系统——导出产物落 `<项目根>/.session-export/<name>/`(目录形态);会话存储位置逐家探测(claude: `~/.claude/projects/**.jsonl`;codex-cli: `~/.codex/sessions`;qoder-cli: `~/.qoder/**`;opencode: `~/.local/share/opencode/opencode.db` SQLite——均为既有适配器已验证路径;copilot / hermes: 本机探测**未发现落盘**:`~/.copilot`、`~/.config/github-copilot`、`~/.hermes` 等均不存在)
**Testing**: pytest(契约测试 pin 命令面/技能面/描述文档面;集成测试以构造夹具驱动 export.py 真实执行)
**Target Platform**: Linux/macOS/Windows(既有跨平台解释器探测纪律保留;本仓库实施环境为 Linux 容器)
**Project Type**: 代码生成器/框架(templates/ + skills/,镜像模型 canonical → `.specify/` → per-tool 副本)
**Performance Goals**: 单会话导出为一次性批处理,秒级至分钟级(与会话规模线性);描述文档总结预算双阈值冻结:行数 ≤ 50,000 **且** 字节 ≤ 32 MB 方可全量总结,任一超限即骨架降级(D5)
**Constraints**: 宿主存储只读(FR-016);无网络调用、无外部凭证(FR-007);退出码五值语义保持(FR-009);被移除产品全文零残留(FR-006)
**Scale/Scope**: export.py 改造(删六家适配器 + zip→目录 + --name,净变化约 -800/+300 行量级);命令模板 1 份 + per-tool 副本 4 份;SKILL.md 重写;描述文档机制;新增/扩展测试约 6–8 个文件

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, 13 principles in order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 计划完全派生自 039 规格(4 US / 16 FR / 6 SC + 3 条 clarify 裁决) |
| II | Feature-Centric Development | ✅ Pass | 挂 Feature 043 Session Export(clarify 裁决新建,features.md 行 + 详情文件已注册);feature-ref.md 记录映射 |
| III | Intent-Driven Development | ✅ Pass | `/speckit.session` 为独立单一意图命令,不改既有命令意图路由;export 之外子命令留白 |
| IV | Test-First & Contract-Driven Implementation (NON-NEGOTIABLE) | ✅ Pass | 3 份契约先行(`contracts/`);命令面结构契约、技能改造契约、描述文档契约的测试任务在 tasks 阶段置于实现之前 |
| V | AI Agent Integration Standards | ✅ Pass | 命令面只经 `templates/commands/session.md` + `sync-mirrors.py` 扇出至既有 4 家 per-tool 副本目录,不新增工具表面 |
| VI | Continuous Quality & Observability | ✅ Pass | 五值退出码保持;导出披露(工具/会话 ID/目标路径/规模);描述文档降级显式声明;支持矩阵探测结论落 SKILL.md |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify(3 问 3 裁决)→ 本计划 → tasks → implement 顺序执行,校验清单 16/16 已过 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 元信息全部由脚本从原始记录确定性提取(D7);支持矩阵以运行时探测为准(FR-010);无缓存回填 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新顶层目录:技能已在库(改造非新建)、命令模板为既有机制新增一份、导出根沿用既有 `.session-export/`;单脚本形态保持 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 规格/计划/契约落 `.specify/specs/039-session-export/`;用户文档落 `docs/reference/commands/session.md`(一命令一文件) |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本仓库自身会话即首个导出对象(quickstart §1 以当前 CLI 会话真跑);团队 run 追溯链(US4)消费同一机制 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 改造既有 export.py(保留定位机制/解释器探测/requestId 提取),不另起炉灶;镜像扇出经 sync-mirrors.py 单入口 |
| XIII | Better-Harness Orientation | ✅ Pass | 会话成为可命名、可归档的证据资产(描述文档 = 会话级 Learning Capture),增强工作循环的可追溯维度 |

**Gates Status**: ✅ All gates pass(13/13,无 Fail/Partial,Complexity Tracking 为 N/A)

**Re-check after Phase 1**: 2026-08-12——设计工件(data-model.md、3 份契约、quickstart.md、feature-ref.md)落盘后复核:上表逐行仍成立;IX 特别复核——契约未引入新脚本文件或新顶层目录(描述文档机制由 export.py 内建 meta 输出 + agent 补写,非新引擎),维持 Pass。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/039-session-export/
├── plan.md              # 本文件(/speckit.plan 输出)
├── research.md          # 无独立文件——Phase 0 决策内联于下方 "## Phase 0: Research Review"
├── data-model.md        # Phase 1 输出
├── quickstart.md        # Phase 1 输出
├── contracts/           # Phase 1 输出(3 份)
│   ├── session-command.contract.md      # /speckit.session export CLI 文法/门禁/委托契约
│   ├── export-skill-rework.contract.md  # export-session 支持矩阵/目录产物/定位机制契约
│   └── session-description.contract.md  # 描述文档结构/元信息字段/预算降级契约
├── feature-ref.md       # Phase 1 输出(Feature 043 绑定映射)
├── checklists/requirements.md  # /speckit.requirements 校验清单(已全过)
├── tasks.md             # Phase 2 输出(/speckit.tasks,本命令不创建)
└── verification.md      # 实现输出(/speckit.implement)
```

### Source Code (repository root)

```text
skills/export-session/          # 彻底改造:SKILL.md 重写(六家矩阵/目录形态/描述文档流程/去平台依赖);
                                # scripts/export.py 删六家适配器、zip→目录、新增 --name、copilot/hermes 探测适配器、meta 输出
templates/commands/             # session.md 新增(export 子命令、preview 门禁、委托技能、覆盖交互确认)
docs/reference/commands/        # session.md 新增(用户文档)
tests/contract/                 # 新增契约族:命令面/技能改造/描述文档
tests/integration/              # 新增:夹具驱动 export.py 真跑(目录产物/meta/冲突/只读)
.specify/memory/features/043.md # Feature 详情(Draft → Planned)
```

**Structure Decision**: 改造一个既有技能 + 新增一份命令模板与一份用户文档——零新顶层目录、零新脚本文件(描述文档的确定性半体由 export.py 内建输出,agent 补写总结半体)。导出根沿用既有 `.session-export/`,形态由 zip 改目录。

### Mirror Obligations

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/export-session/SKILL.md`、`skills/export-session/scripts/export.py` | `.specify/skills/export-session/SKILL.md`、`.specify/skills/export-session/scripts/export.py` | `sync-mirrors.py --check` exit 0 |
| `templates/commands/session.md` | `.specify/templates/commands/session.md`;`.claude/commands/speckit.session.md`;`.github/prompts/speckit.session.prompt.md`;`.qoder/commands/speckit.session.md`;`.opencode/command/speckit.session.md` | 同上(扇出经 `regen-command-copies.py`) |
| `docs/reference/commands/session.md` | 无镜像(docs/ 不镜像) | — |
| `.specify/memory/features/043.md`、`.specify/memory/features.md` | 无镜像(memory/ 不在 MIRROR_PAIRS) | — |

## Phase 0: Research Review

无独立 research.md——决策可由规格 + 代码库内部证据 + 本机探测裁定。决策记录:

| # | 决策 | 结论 | 依据 |
|---|------|------|------|
| D1 | 命令面形态 | `/speckit.session export --name <name> [--session <id>] [--tool <name>] [--verify <text>]`;preview→confirm→execute 门禁;委托技能执行,命令不重复实现导出逻辑 | FR-001…FR-004;既有命令模板纪律(goal/team 同构) |
| D2 | 导出根与命名 | `.session-export/<name>/`;`--name` 必填且为安全路径段文法(同 goal 身份);冲突默认拒绝,覆盖走 preview 门禁内交互式确认(无 `--force` 旁路);覆盖 = 清空后写入 | FR-002/FR-005 + clarify 裁决 Q3 |
| D3 | 改造架构 | 保持单脚本(stdlib-only):删六家适配器与其专属辅助函数/路径/文档;四家既有适配器把 `*_pack` 的 zip 写入改为目录写入;copilot / hermes 新增**探测式适配器**——`available()` 按已知候选路径探测,本机实测无落盘,矩阵落「会话存储未探测到」声明,未来探测到落盘再补实现 | FR-006/FR-007/FR-010;本机探测证据(~/.copilot 等均不存在) |
| D4 | zip → 目录 | 目录布局:`main.<原生扩展名>`(主记录)+ `subagents/`(子代理日志)+ `state/`(状态目录与段日志)+ `large-results/`(超大工具结果)+ `request-ids.jsonl`(可提取者)+ `session-meta.json` + `SESSION.md`;移除原子 zip 机制(彻底改造,不保留双形态) | FR-008/FR-011;既有 `_pack_main_plus_sibling` 内容面逐段映射 |
| D5 | 描述文档机制与预算 | 固定文件名 `SESSION.md`;脚本确定性输出元信息 → 写 `session-meta.json`(机读)+ 渲染 SESSION.md 元信息节并留总结占位节;agent 读原始记录补写结构化总结;预算双阈值冻结 `SUMMARY_LINE_LIMIT=50000`、`SUMMARY_BYTE_LIMIT=32*1024*1024`,脚本输出 `over_summary_budget` 判定,超限 → 骨架总结 + 声明降级原因与触发阈值 | FR-012/FR-013/FR-014 + clarify 裁决 Q2;程序优先 |
| D6 | 退出码 | 五值保持:`0` 成功 / `2` 参数无效(含缺 --name)/ `3` 未找到会话 / `4` 前置失败(无可用工具/解释器/脚本缺失)/ `5` IO 错 | FR-009;既有 SKILL.md 退出码表 |
| D7 | 元信息字段集 | `tool`、`session_id`、`model`、`started_at`、`ended_at`(运行中会话为快照时点并置 `snapshot: true`)、`workspace`(cwd)、消息/轮次计数、导出时间——全部由脚本从原始记录提取 | FR-012/FR-015;既有 `_last_model`/`_session_recency`/`_read_cwd_from_jsonl` 复用 |
| D8 | 通用化清单 | 移除 SKILL.md 的 aone-open 使用上报段(`a1 skill report`)与 `x-source` 标记;移除调用段中平台私有技能目录探测的六家私有项(保留六家对应目录);无网络、无凭证断言入契约 | FR-007;SKILL.md 现状(§1 上报段 + frontmatter x-source) |

## Complexity Tracking

N/A——Constitution Check 13/13 全 Pass,无违规需辩护。
