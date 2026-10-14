# Implementation Plan: 057-decompose-command-skills

**Branch**: `057-decompose-command-skills` | **Date**: 2026-10-14 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `057-decompose-command-skills` → Feature 057 命令技能化分解补全
**Input**: Specification from `.specify/specs/057-decompose-command-skills/requirements.md`

## Summary

补全 agent/team/skills 三个命令面的 run 语义技能化(goal `command-logic-as-classified-skills` T-001/T-003):新建两个 internal 技能——**run-skills**(运行未注册技能的统一入口:canonical 优先解析、已知位置集信任边界、尽力检测注册提示、internal 目标离开 `.specify/` 拒绝执行;自身经 `.specify/skills` + 宿主 skills 符号链接抵达发现面)与 **run-team**(`/speckit.team` run 模式全流程从命令模板提取,行为平价基线);`/speckit.team` 与 `/speckit.skills` 命令模板收缩为入口+路由,`/speckit.agents` 仅核查。技术形态为**纯模板/技能内容变更**(template-only):两个新 SKILL.md、两个命令模板瘦身、指南例外条目、probe 注册表 2 行 + 重编译、镜像同步、结构契约测试。不写任何运行时代码。

## Technical Context

**Language/Version**: Markdown 模板/技能内容(框架本体);既有 Python ≥3.8 引擎复用(`sync-mirrors.py`、`regen-command-copies.py`、`probe-utils.py`、`scan-confirmation-gates.py`),不新写运行时脚本
**Primary Dependencies**: 既有引擎:sync-mirrors.py(MIRROR_PAIRS:skills/internal 嵌套对、templates 对、shared 对)、regen-command-copies.py(6 个 per-tool 命令副本树)、probe-utils.py --action compile-embeds(69 单元零漂移基线)、pytest 契约测试
**Storage**: N/A(文件树:skills/、templates/、shared/ 及其 .specify/ 镜像)
**Testing**: `pytest -m contract`(经 `scripts/bash/run-tests.sh --names-out`,名字级基线判据);结构契约测试断言模板/技能内容、规范路径与镜像字节一致
**Target Platform**: 仓库框架源树(skills/、templates/、shared/)+ 本仓运行时镜像(.specify/);宿主发现面经既有 `.claude/skills`、`.qoder/skills`、`.github/skills` → `.specify/skills` 符号链接,无新增 per-tool 机制
**Project Type**: framework(template-only feature——无运行时行为,测试对象为文档内容/规范路径/镜像字节一致)
**Performance Goals**: N/A(内容变更,无运行时性能面)
**Constraints**: ①**门控预算整数余量 0**(实测基线 2026-10-14:scan-confirmation-gates.py total=23=冻结上限,violations 0)——本特性全部新增文案 MUST 零 BLOCKING_PATTERNS 命中(设计规避,不改扫描器/不扩豁免),收尾 total 仍=23;②**镜像相对判据**(实测基线 2026-10-14:全树恰 1 条既有 DIFF `.specify/skills/git-workspace/scripts/git_fleet.py`,不在本特性触及对上)——改后仍恰这 1 条,无新增;③compile-embeds 收尾零漂移(69→71 单元);④regen 命令副本基线全 OK——改后六副本含改动且仍全 OK
**Scale/Scope**: 2 个新技能目录(各 1 个 SKILL.md)+ probe 注册表 2 行 + 2 个命令模板改 + 1 个指南改(双副本)+ agents.md 只读核查 + 1 个新契约测试文件 + quickstart 3 场景

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.13.0,16 原则):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 本计划逐 FR 映射设计产物;需求 057 为唯一需求源(requirements.md exit 0) |
| II | Feature-Centric Development | ✅ Pass | Feature 057 已绑定并登记(index 行 Draft + features/057.md + 013/019/027 反向交叉引用,commit 0ed62af3);本计划结束时推进 Draft→Planned |
| III | Intent-Driven Development | ✅ Pass | 规格以 WHAT/WHY 表述,plan 才落 HOW;4 项澄清裁定已回写规格 |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | template-only 特性:测试对象为模板内容/规范路径/镜像一致(Constitution VII 明文许可的 Partial);红先行取证落 notes/red-first-evidence.md |
| V | AI Agent Integration Standards | ✅ Pass | 不新增 agent CLI 支持;技能为宿主中立 Markdown,发现面走既有符号链接拓扑 |
| VI | Continuous Quality & Observability | ✅ Pass | 契约测试 + probe Wrap-up 编译嵌入(2 新单元);无投机特性 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 复用优先已核(候选 013/019/026/027/039 均不覆盖跨命令面,裁定新建);状态只推进到 Planned;template-only Partial 按 VII 门处理 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 现状锚点全部源码实测(skills 计数 11/35、team.md 104 行内联 Run Mode、路由表现状);声明与行为分歧处(指南"not agent-visible")以实测为准并修正指南 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 纯模板/提示内容,零新运行时机制;复用既有 4 个引擎,不建任何注册表/扫描器 |
| X | Documentation Naming & Location Conventions | ✅ Pass | SKILL.md 为工具强制名(X 豁免);新文档均小写规范路径 |
| XI | Dogfooding (Self-Application) | ✅ Pass | **框架源帽**:全部编辑落 skills/、templates/、shared/ 规范层,经 sync-mirrors/regen 流抵达运行时;命令模板内联流程的消除即机制侧修复(消除产生漂移的源头) |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 镜像/副本/编译/门控扫描全部复用既有引擎;零新生成脚本 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution 与 Reliable Delivery 维度:run 语义成为可直达的可重复路径 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | run 义务真源随提取单点化(team.md→run-team);run-skills 引用真源+内联最小操作事实(FR-006);指南例外以引用衔接既有规则,不复述 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 错误面(未命中/越界/无效)按基准读者措辞,带位置清单与修正路径;本计划的问答面已按 ⑤ 类执行 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | FR-004 快速失败为需求义务;派发治理平价保留注入子句与异常回传行;本计划基线测量先行(判据非预写) |

**Gates Status**: ✅ All gates pass(唯一 ⚠ Partial 为 IV, justification 见 Complexity Tracking——VII 门明文许可的 template-only 形态)

**Re-check after Phase 1**: 2026-10-14 — 设计产物落地后复核(同作者门控:2 个 fresh-context 只读检测器,a=宪法评分、b=Phase 1 产物质量门,范围不相交):检测共 6 条发现,全部判定为**纠正级**并已就地整合——原则名逐字修复(Row XIII 补 "(Improvement North Star)")、根级 notes/ 目录矛盾消除(取证文件归位规格目录内,与 051 先例一致)、team.md 中全部 run→create-team 引用纳入 C-4 提取面(路由流步骤与 Ambiguous-Intent 列举)、P-1 锚点边界修正(§ Run Mode + 路由流 run 义务)、quickstart 调用语法的契约钉住补齐(C-3)、"已执行"指针措辞校正;宪法评分 16/16 复核后维持原判(IV Partial 依据不变,XIV 经对映表增强确认)。检测/验证分离维持:检测器报告,编排者验证后整合。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/057-decompose-command-skills/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # No standalone research.md — findings inlined below (Phase 0 < 50 lines, internal sources only)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── notes/
│   └── red-first-evidence.md  # 红先行取证(/speckit.tasks 产物,沿 051 先例落规格目录内)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
skills/internal/run-skills/        # NEW — run 未注册技能的统一入口(SKILL.md 单文件)
skills/internal/run-team/          # NEW — /speckit.team run 流程承载(SKILL.md 单文件)
templates/commands/team.md         # run 行改指 run-team;Run Mode 程序性内容清零
templates/commands/skills.md       # 路由表 2→5 行(create/modify×3/run)
templates/skills.md                # 指南:internal 注册例外 + 符号链接拓扑改述
shared/definitions/probe-definitions.md  # probe 注册表 +2 个 skill-wrapup Object 行
tests/contract/test_run_skills_wiring.py # NEW — 结构契约测试(本特性全部判据的机器面)
```

**Structure Decision**: 扩展现有框架源树——两个新 internal 技能目录(单 SKILL.md,沿 run-agent 先例,不设 references/)、两个命令模板的原地瘦身、一个指南例外条目、probe 注册表两行。无新顶层目录。

### Mirror Obligations

基线实测(2026-10-14,判据均为相对形态——"无新增漂移",绝不预写全绿):

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/internal/run-skills/SKILL.md` (NEW) | `.specify/skills/internal/run-skills/SKILL.md`(sync-mirrors `--only skills/internal/run-skills`;宿主发现面经 `.claude/.qoder/.github/skills → .specify/skills` 符号链接自动可达,无 per-tool 副本) | `sync-mirrors.py --check --only skills/internal/run-skills` → 0 DIFF(该对为本特性新建,基线不存在旧漂移);编译后两副本 Wrap-up 段一致 |
| `skills/internal/run-team/SKILL.md` (NEW) | `.specify/skills/internal/run-team/SKILL.md`(同上) | 同上 |
| `templates/commands/team.md` | `.claude/commands/speckit.team.md`、`.qoder/commands/speckit.team.md`、`.github/prompts/speckit.team.prompt.md`、`.opencode/command/speckit.team.md`、`.codex/commands/speckit.team.md`、`.hermes/commands/speckit.team.md`(regen-command-copies.py;`.specify/templates/commands/` 已退役不入对) | `regen-command-copies.py --check` EXIT=0(基线 2026-10-14 已实测 OK)且抽查副本含 run-team 路由改动 |
| `templates/commands/skills.md` | 同上 6 个 per-tool 副本(speckit.skills) | 同上 |
| `templates/skills.md` | `.specify/skills.md`(live 指南副本;generate-instructions.sh 仅缺文件时创建,故本仓 live 副本为**手动双写**,两副本字节一致——实测基线 diff 为 IDENTICAL) | `diff -q templates/skills.md .specify/skills.md` → 一致 |
| `shared/definitions/probe-definitions.md` | `.specify/shared/definitions/probe-definitions.md`(sync-mirrors shared 对) | `sync-mirrors.py --check --only shared` → 0 DIFF(shared 对基线 0 漂移);全树收尾判据:仍恰基线那 1 条既有 DIFF(`.specify/skills/git-workspace/scripts/git_fleet.py`),无新增 |
| (编译产物)两新 SKILL.md 的 `## Wrap-up` 段 | 由 `probe-utils.py --action compile-embeds` 从注册表渲染进 canonical,随 sync-mirrors 落镜像 | `probe-utils.py --action compile-embeds --check` → 零漂移(基线 69 单元零漂移;注册 2 行后 71 单元) |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle IV Test-First 判 Partial | template-only 特性:无运行时行为可测;"测试"为模板内容/规范路径/镜像字节一致的结构契约(Constitution VII Workflow Gates 明文许可的 Partial 形态),红先行取证按 Red-First 取证纪律留存 | 运行时行为测试不可写(被测物是提示文本);纯 grep 全绿同样违反 IV 的原意,故以结构契约 + 红先行取证 + 行为类条款(评审强制)组合承担 IV 的验证义务 |

## Phase 0: Research Review

无独立 research.md(发现 < 50 行,全部内部来源,已内联)。关键技术事实(2026-10-14 实测,探索子代理 + 引擎实跑):

1. **镜像拓扑**:sync-mirrors.py MIRROR_PAIRS 含 `skills/internal/<name>/ → .specify/skills/internal/<name>/`(嵌套);`.qoder/.claude/.github/skills` 均为 `→ ../.specify/skills` 符号链接(src/specify_cli/__init__.py `_SKILLS_SYMLINK_ASSISTANTS`,6 工具)——**宿主注册 = 镜像落 .specify/skills 即自动抵达**,无新增机制。
2. **Wrap-up 编译**:compile-embeds 扫描 `skills/{external,internal}/<name>/SKILL.md` → 单元 `skill:<name>`;注册 = 在 `shared/definitions/probe-definitions.md` Object 表加 `skill-wrapup` 行×2 + 跑 compile-embeds;守卫 `tests/contract/test_compile_embeds.py`、`test_registry_completeness.py` 既有。
3. **命令副本**:regen-command-copies.py 写 6 个 per-tool 目录(仅已存在者),有 `--check`;team.md/skills.md 改动必须经它扇出。
4. **技能先例**:run-agent SKILL.md 形态 = frontmatter(`name`/`description`/`classification: internal`/`skill_id: "<SKILL:.specify/skills/internal/<path>/SKILL.md>"`)+ Goal/Input Contract/Workflow/Boundaries/编译 Wrap-up。
5. **指南真源**:templates/skills.md ≡ .specify/skills.md(diff 实测 IDENTICAL);generate-instructions.sh 仅缺文件时创建,故 live 副本为本特性手动双写。
6. **测试先例**:tests/contract/ 逐文件 `REPO_ROOT = Path(__file__).resolve().parents[2]`;grep 断言式(test_team_command_routing.py)、派生结构式、权威名册式三风格;helpers_prompt_assets.py 提供 frontmatter 解析。
7. **既有守卫相容**:test_team_command_routing.py 现行钉住 team.md 路由含 "create-team"(run 行改 run-team 后该断言仍成立——create 行不动);compile-embeds/registry 守卫覆盖新单元。
8. **同作者复核记录**:计划与 Phase 1 产物落盘后,按 objective-analysis-gate 委派 2 个 fresh-context 只读检测器(不相交范围:a=plan.md+constitution 评分,b=Phase 1 产物质量门)——共返回 6 条发现(宪法面 2:原则名截断、根级 notes/ 矛盾;产物面 4:C-4/C-5 提取面缺口、P-1 锚点越界、quickstart 语法钉住缺失、"已执行"指针夸大),全部为纠正级并已整合;检测/验证分离维持,未发现决策级异常。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [data-model.md](data-model.md) | 4 实体(Skill Descriptor / Skill Location Search Order / Team Run Flow Obligation Set / Probe Registry Object-row) |
| Contracts | [contracts/](contracts/) | 2 文件:run-skills-wiring.md(C-1…C-9)、run-team-parity.md(P-1…P-10 义务对映表) |
| Quickstart | [quickstart.md](quickstart.md) | 3 场景(run-skills 未注册目标 / run-team 平价 / skills 路由) |
| Feature binding | [feature-ref.md](feature-ref.md) | Feature 057 映射 + 状态推进记录 |

## Feature Integration (plan 阶段执行记录)

- Feature 057 已于 clarify 注册(index 行 Draft,commit 0ed62af3);本计划落盘后推进 **Draft → Planned**(features.md 行 Status + features/057.md Status Tracking/Last Updated/本节 key note),不落 Implemented(归 /speckit.implement)。
- Feature 清单复核:本计划不引入新 Feature、不废弃/合并既有 Feature;013(skills 面)/019(agents 面)/027(team 面)的既有范围记录不变——057 为跨面补全,交叉引用已在三者详情文件落地。功能/非功能分类一致性:两新能力均属命令/技能编排面(functional),无分类漂移。
