# Implementation Plan: 执行量化数据反馈回传与汇总（Exec-Quant Feedback Channel）

**Branch**: `068-exec-quant-feedback-channel` | **Date**: 2026-10-22 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `068-exec-quant-feedback-channel` → Feature 068 执行量化数据反馈回传与汇总
**Input**: Specification from `.specify/specs/068-exec-quant-feedback-channel/requirements.md`

## Summary

Feature 068 把 `/speckit.feedback` 从「只回传框架摩擦条目」升级为「更通用的框架反馈通道」：客户项目打包时把 `.specify/memory/exec-quant` 全部可读记录作为一等载荷随包收回（全量包含、显式封顶、只读源存储），spec-kit 侧既有入站包路径把载荷解出到聚合层 `aggregated/`（按源项目归因、幂等去重），维护者可用显式汇总动作产出跨项目机器可读聚合视图。技术路线 = **扩展两个既有引擎，零新增命令**：打包腿与接收腿落在 `scripts/python/feedback-utils.py`（package 扩展 + 新动作 `ingest-exec-quant`），汇总腿落在 `scripts/python/exec-quant.py`（新动作 `aggregate`）；镜像经 `sync-mirrors.py` 同步，零手改。059 FR-011 仅打包腿修订（手动触发），零自动传输红线原样保留；全链路非阻塞、零网络、凭据零出现。

## Technical Context

**Language/Version**: Python ≥ 3.8（两引擎均为 stdlib-only 脚本：json / zipfile / hashlib / fcntl / argparse）
**Primary Dependencies**: 无新增运行时依赖（pytest 为既有测试框架；引擎零第三方依赖）
**Storage**: 文件存储——客户侧 exec-quant store（只读）；包内 `exec-quant/` 载荷目录；spec-kit 侧派生存储 `.specify/memory/exec-quant/aggregated/`（按条信封 + summaries，并发安全按条落盘）
**Testing**: pytest（markers: contract / integration）；red-first 取证 + 名字级基线比对（基线已冻结，见 Test Strategy）
**Target Platform**: Linux / macOS（POSIX flock；无 fcntl 平台沿用引擎既有的文档化降级）
**Project Type**: 框架源（scripts / skills / templates / shared / docs）+ 运行时镜像（`.specify/`，sync-mirrors 投影）
**Performance Goals**: 非阻塞优先于吞吐；载荷封顶 1000 条 / 16 MiB（contracts C-2）
**Constraints**: 三腿零网络（FR-016）；源存储严格只读（FR-002）；降级显式计数非阻塞（FR-005/FR-010）；零新增命令、零新增确认门（clarify 裁决）
**Scale/Scope**: 单客户项目记录量级 ≤ 数千条（实测 15 + 7 + 59 条）；改动面 = 2 引擎 + 2 技能引用文件 + 1 命令模板 + 1 shared step + 2 docs + 测试 3 层

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`；本运行无子代理派发工具，评分按 objective-analysis-gate §7 降级为直接有界复核——`scored: direct read, subagent unavailable`，见 Phase 0)：

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每项设计决策回指 FR 条款（research.md D1–D12；feature-ref.md FR→条款映射表覆盖 19/19 FR） |
| II | Feature-Centric Development | ✅ Pass | Feature 068 已注册（clarify），本阶段 Draft → Planned；Feature list 复核零新增/零废弃（feature-ref.md § Feature list review） |
| III | Intent-Driven Development | ✅ Pass | requirements 的 what/why（四 US + 边界）驱动设计；11 项 clarify 裁决逐一落位（research.md 引 Clarifications） |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 本特性含可执行运行时代码 → 全量 Test-First（不适用 template-only Partial）：D11 三层测试 + red-first 取证 + 验收场景即测试 |
| V | AI Agent Integration Standards | ✅ Pass | 零 agent roster / AGENT_CONFIG 触碰；通道升级发生在既有命令-技能-引擎三层内 |
| VI | Continuous Quality & Observability | ✅ Pass | 降级显式计数（C-7/C-16）；新行为落 specs/plan/docs（D12）；零投机特性 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Feature reuse-first：新建 Feature 068 已由 clarify 裁决（059 显式排除回传聚合，无既有 Feature 可绑定）；状态只进不退 Draft → Planned |
| VIII | Code as the Single Source of Truth | ✅ Pass | 现状锚点全部标 dated record 并以 file:line 实测（research.md 各 Decision Evidence；requirements 现状锚点节同惯例） |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新命令/零守护进程/零扫描器/零新机制；聚合层沿用既有按条文件 + flock 纪律；封顶/身份复用既有指令文件与 git HEAD |
| X | Documentation Naming & Location Conventions | ✅ Pass | 文档改动全部落在既有路径（docs/reference/…、shared/workflow/…）；新产物小写命名（`aggregated/`、`summaries/`、`payload-manifest.json`）；零新保留名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本特性即 Loop A 通道升级（既有链路上增强，非重建）；两顶帽子：Mirror Obligations 表强制源先镜像后；059 逆向交叉引用豁免已披露于 features/068.md（派发约束，非静默偏离） |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 规划复用 create-new-plan.sh / sync-mirrors MIRROR_PAIRS / args-manifest 契约；实现复用 write_entry / flock / read_entry_files 既有件（research D8）；零新 Tool 需求 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Learning Capture（量化数据可回传汇总）+ Reliable Delivery（非阻塞、知情报告）；零新评分/记录系统；锚定 better-harness 机制映射 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | MANIFEST 人读段与 payload-manifest.json 同函数渲染（C-4）；封顶值唯一规范落点 = contracts C-2（实现落模块常量）；[[STR-NNN]] 引用惯例沿用 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | FR-004 知情报告 = 人可读计数 + 降级说明（C-7）；机器可读面（JSON 键）面向维护者基线读者，docs 同步给出语境（D12） |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 降级/冲突/跳过一律显式计数不静默修补（D10；C-13 identity_conflicts keep-first）；本计划自身的探索降级与基线失败均已显式披露 |

**Gates Status**: ✅ 全部 16 原则 Pass，零 Fail / 零 Partial——无 Complexity Tracking 违例项。披露两件过程性事实（非违例）：① 同作者评分门降级为直接复核（行上标注，D13）；② 实现前基线含 3 个**既有**镜像一致性失败（非本特性引入，名字已冻结于 test-evidence/log-baseline-pre-impl.txt，判据 = 零新增）。

**Re-check after Phase 1**: 2026-10-22 复核完成——Phase 1 四产物（data-model / contracts ×4 / quickstart / feature-ref）落地后逐行重对照：II（状态推进落 features 更新）、IV（契约测试面与 contracts 条款一一对应）、XIV（E4/E5 同源渲染条款化）等证据行按产物实文更新，结论不变（16 Pass）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/068-exec-quant-feedback-channel/
├── requirements.md      # /speckit.requirements + clarify 产物（既有，零改动）
├── plan.md              # 本文件（/speckit.plan）
├── research.md          # Phase 0 产物（决策 D1–D14 与实测依据）
├── data-model.md        # Phase 1 产物（E1–E8 实体）
├── contracts/           # Phase 1 产物（4 份契约，31 条款）
├── quickstart.md        # Phase 1 产物（6 场景）
├── feature-ref.md       # Phase 1 产物（Feature 绑定与 FR/SC 映射）
├── checklists/          # 既有（requirements checklist）
├── test-evidence/       # 阶段证据（基线冻结 log、stage-status）
├── tasks.md             # Phase 2 产物（/speckit.tasks，本阶段不创建）
└── verification.md      # 实现阶段产物（/speckit.implement）
```

（research.md 为独立文件——Phase 0 超过 50 行且含多源实测证据，符合模板条件。）

### Source Code (repository root)

```text
scripts/python/feedback-utils.py      # 打包腿（package 扩展）+ 接收腿（新动作 ingest-exec-quant）
scripts/python/exec-quant.py          # 汇总腿（新动作 aggregate；既有动作零改动）
skills/internal/manage-feedback/      # SKILL.md + Path A/B 引用文档（载荷接收/汇总入口的流程面）
templates/commands/feedback.md        # 命令模板（技能引用行更新）→ 逐工具副本
shared/workflow/feedback-step.md      # wrap-up step 文档（载荷随包后的观察面）
docs/reference/commands/feedback.md   # 命令参考（三腿行为 + 引擎动作名）
docs/reference/skills/feedback.md     # 技能参考（Path A 载荷步骤）
tests/contract/                       # 新增 3 支契约测试（D11 命名）
tests/unit/                           # 新增单元测试（identity/slug/payload 采集）
tests/integration/                    # 新增端到端测试（package→ingest→aggregate）
.specify/scripts/  .specify/skills/  .specify/shared/  # 运行时镜像（sync-mirrors 投影，禁手改）
.specify/memory/exec-quant/aggregated/  # 运行时派生存储（接收/汇总产物；本仓按 records/ 惯例随 git 跟踪）
```

**Structure Decision**: 不新增任何顶层目录；形状 = 「在既有双引擎（feedback-utils.py / exec-quant.py）的动作面各做一次加法，技能与文档面同步引用」，派生存储落在 059 已自有的 exec-quant store 内（`aggregated/` 与 `records/`、`scores/` 平行，A2 裁决）。唯一新的运行时目录是 `aggregated/`（store 内部，非仓库顶层）。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

镜像对真源 = `scripts/python/sync-mirrors.py MIRROR_PAIRS`；`.specify/templates/commands/` 已退役（命令模板只扇出到逐工具副本）。**Pre-edit drift baseline（2026-10-22 `sync-mirrors.py --check` 实测）**: 既有 DIFF 含 `shared/workflow/feedback-step.md` 等 shared 多文件（完整名单见镜像检查输出）——本表 Verify 判据一律为「**相对该既有基线零 NEW drift**」，绝不见「全绿」绝对判据。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/feedback-utils.py` | `.specify/scripts/python/feedback-utils.py`（scripts 对，strict extras） | 编辑前跑 `sync-mirrors.py --check --only scripts` 记录既有 drift；落地后 `--write` 同步，复查该对零 NEW drift（2026-10-22 tasks 阶段复测更正：该对存在 **1 行既有 DIFF**——镜像侧 f265cfbd 已把 docstring 内 `shared/workflow/feedback-step.md` 路径引用改为 `.specify/` 前缀形态、源侧未同步；本行原文「实测现状该对无 DIFF」系 plan 阶段误测。判据仍为「相对该既有基线零 NEW drift」；`--write` 落地后该既有 DIFF 随字节同步消失属预期，不算回归） |
| `scripts/python/exec-quant.py` | `.specify/scripts/python/exec-quant.py`（scripts 对） | 同上判据（2026-10-22 tasks 阶段复测：该对现状零 DIFF） |
| `skills/internal/manage-feedback/SKILL.md` | `.specify/skills/internal/manage-feedback/SKILL.md`（skills/internal 对） | 同法；零 NEW drift + 副本含改动 |
| `skills/internal/manage-feedback/references/path-a-digest.md` | `.specify/skills/internal/manage-feedback/references/path-a-digest.md` | 同上 |
| `skills/internal/manage-feedback/references/path-b-and-probe.md` | `.specify/skills/internal/manage-feedback/references/path-b-and-probe.md` | 同上 |
| `templates/commands/feedback.md` | `.claude/commands/speckit.feedback.md`、`.github/prompts/speckit.feedback.prompt.md`、`.qoder/commands/speckit.feedback.md`、`.opencode/command/speckit.feedback.md`、Codex 对应副本（以 regen-command-copies.py 逐工具清单为准）；**无** `.specify/templates/commands/` 镜像（已退役） | `regen-command-copies.py` 重生成后 diff 逐工具副本含改动；零手改副本 |
| `shared/workflow/feedback-step.md` | `.specify/shared/workflow/feedback-step.md`（shared 对） | 编辑前 `--check --only shared/workflow/feedback-step.md`（该文件**已在既有 DIFF 基线内**）；落地后 `--write` 同步 + 既有失败测试 `test_feedback_step_reference_form.py::test_owner_mirror_is_byte_identical` 预期转绿（基线失败的消失不算回归） |
| `docs/reference/commands/feedback.md`、`docs/reference/skills/feedback.md` | 无镜像（docs 不随框架分发，shared/docs 边界） | 文档站构建/引用检查零新增破损 |

## Complexity Tracking

> 无 Fail / Partial 违例行——按模板规则本节为 **N/A**（表格删除）。过程性披露（同作者评分降级、既有基线失败）已在 Gates Status 与 Phase 0 就地记录，不属宪法违例。

## Test Strategy & Evidence Duties

- **Tests Mode 判定**（宪法 IV + VII）：本特性交付可执行运行时代码（两引擎动作）→ 全量 Test-First，不适用 template-only Partial。
- **Red-first 取证**：每支新测试先以未实现状态跑出失败并留痕 `test-evidence/`（红名单），实现后转绿；任务阶段把取证行钉进 T 清单。
- **名字级基线**（FR-018/SC-006）：实现前基线已冻结——`test-evidence/log-baseline-pre-impl.txt`（544 passed / 3 failed；失败名单 = 3 个既有镜像一致性 nodeid，非本特性引入）；实现后重跑同集（quickstart 场景 4 命令），排序失败名单逐名比对零新增。
- **不新增确认门**（Explicit Exclusions）；测试断言封存 contracts 条款（C-PL/IN/AG/CS），`[[STR-NNN]]` 引用可解析。

## Phase 0: Research Review

研究结论承载于独立产物 [research.md](research.md)（D1–D14：引擎落点、包内布局、身份形态、接收动作、聚合布局、identity key、封顶、汇总动作、FR-019 修订点、退出码、测试策略、镜像义务、同作者降级、无前置 research 说明）。证据路径披露：本运行无子代理派发工具，代码库探索按 create-plan § Phase 0 fallback 降级为有界手工探测（grep 符号 + 定向摘录），`(detected: direct read, subagent unavailable)`——关键实测锚点：`feedback-utils.py:1098/1201/1114-1116/1645-1658`、`exec-quant.py:45/89/192-249/895-940`、`sync-mirrors.py MIRROR_PAIRS`、双仓存储形态（场景 0 route a 实测）。未知项零残留（NEEDS CLARIFICATION 零处——Technical Context 全部实值化）。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [data-model.md](data-model.md) | 8 实体（E1 既有记录零 schema 变更；E2–E7 新增；E8 既有对账面零变化） |
| Contracts | [contracts/](contracts/) | 4 文件 31 条款：package-layout(9: C-1–C-9)、intake-contract(8: C-10–C-17)、aggregate-contract(6: C-18–C-23)、compatibility-security(8: C-24–C-31)；条款 id 各文件内连续可解析 |
| Quickstart | [quickstart.md](quickstart.md) | 6 场景（场景 0/4 = route a 已实跑；1/2/3/5 = route b 契约钉住 + 逐例 premises） |
| Feature ref | [feature-ref.md](feature-ref.md) | FR 19/19 + SC 6/6 全覆盖映射；Feature list 复核完成 |

（计数取自落盘实文；执行-核验路由逐例标注于 quickstart.md——Post-Generation Quality Gate 的 execution-verify 规则按场景 0/4 已实跑、其余由契约测试钉住的方式履行，逐例前提已在各场景 Premises 行列明。）
