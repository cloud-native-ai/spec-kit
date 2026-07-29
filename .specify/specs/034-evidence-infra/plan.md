# Implementation Plan: 公共证据采集基础设施(Better Harness 能力移植)+ improve-* 证据驱动改造

**Branch**: `034-evidence-infra` | **Date**: 2026-07-29 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `034-evidence-infra` → Feature 038 Evidence Infrastructure
**Input**: Specification from `.specify/specs/034-evidence-infra/requirements.md`

## Summary

把 Better Harness(`/cws_work/better-harness`,commit `b2e621d`,MIT)的采集能力子集以源码复制方式托管到 `scripts/js/better-harness/`(D1),用一个 stdlib-only 的 Python 编排引擎 `evidence-utils.py` 统一调度五条证据泳道(session/project/assets 走 Node 子进程;runs/feedback 纯 Python,D3),产出剥离一切裁决字段的 `findings.json` 证据合同(evidenceState 七态);新增 `collect-evidence` 公共技能与 `evidence-step.md` 共享约定,并把 improve-skills / improve-agent / improve-team 改造为"先证据、后优化"范式,配干预台账 + compare 纵向验证。技术路线:复制而非依赖(引擎零 npm 外部依赖,仅 node: 内置模块)、Python 编排替代上游 evidence-bundle 门面、泳道显式降级(无 Node 时 runs/feedback 保底)。

## Clarifications

### Session 2026-07-29

- 勘察确认(better-harness 源码):四能力的 CLI 入口不全在目录内——session-analysis 的入口是根级 `scripts/session-analysis.mjs`(registry 派发);core-change-watch 无 cli.mjs,8 个文件各自带 shebang 与自调用 `main()`;asset-baseline 额外依赖 `scripts/agent-lint/`(4 文件)。复制布局须保持这些相对路径关系(§Source Code)。
- 勘察确认(spec-kit 现状):`.specify/skills/` 镜像现状不全(5/23),`instructions.md` 技能计数文本(22)与实际(23)不一致——本 spec 只对 `collect-evidence` 与三个 improve 技能承担镜像义务,存量漂移记录为已知基线问题,不在本 spec 修复。
- 勘察确认:feedback 存量条目已达 54(动态口径已入 spec);teams 现有 2 个团队,其中 `bh-port-monitor` 具备完整 STATE.md + run-log.jsonl,`draw-plantuml-optimizer` 仅有 runs/ 报告——runs 泳道必须容忍字段缺失的团队目录。
- 勘察确认:上游 `engines` 要求 Node `>=22.20.0 <25`;doctor 必须校验 Node 版本并把不满足视为三条 Node 泳道 unavailable 的一种成因。

## Technical Context

**Language/Version**: Python ≥3.8(evidence-utils.py,stdlib-only)+ Node.js ≥22.20.0(采集引擎,ESM,零 npm 外部依赖)  
**Primary Dependencies**: 无新增第三方依赖——引擎仅用 `node:` 内置模块;Python 侧仅 stdlib(argparse/json/subprocess/hashlib/pathlib);上游的 tree-sitter/esbuild WASM 依赖随不复制的 canvas 子树整体剥离  
**Storage**: 文件系统——`.specify/memory/evidence/<run-id>/{findings.json,manifest.json,lanes/*.json}` + `index.json`(仿 feedback 存储);引擎源码托管 `scripts/js/better-harness/` ↔ `.specify/scripts/js/better-harness/`(全量镜像,FR-014)  
**Testing**: pytest(主栈,新增 contract 测试校验 findings.json 合同与 CLI 表面)+ `node --test`(从上游摘取的引擎子集测试,落 `tests/js/`,`tests/js/run.sh` 包装)  
**Target Platform**: Linux / macOS(与 spec-kit 现行脚本一致);Windows 兼容性随上游代码继承,不额外验证  
**Project Type**: single(CLI 工具包 + 模板/技能资产库,延续既有布局)  
**Performance Goals**: collect 全泳道单次运行 ≤ 60s(本仓库规模);doctor ≤ 5s;无并发要求(确定性单进程编排)  
**Constraints**: 引擎子进程调用 argv-array、shell=False;证据落盘经脱敏双闸(引擎侧漏斗 + Python 白名单过滤);`.specify/memory/evidence/` 排除出 feedback package;技能 ≤500 行;improve-* 改动各 30~60 行级  
**Scale/Scope**: 引擎子集约 1.0 MB / ~60 个 .mjs 文件 ×2(镜像);1 个新 Python 引擎(预估 ~600 行);1 个新技能 + 1 个共享约定文档 + 3 个技能改造;测试 ~10 个上游 .test.mjs + ~3 个新 pytest 文件

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | spec 034 先行(7 故事/14 FR/8 SC),本 plan 由 spec 驱动;方案文档 draft v2 为已评审设计输入 |
| II | Feature-Centric Development | ✅ Pass | Feature 038 已注册(features.md + features/038.md),本 plan 推进其 Draft → Planned |
| III | Intent-Driven Development | ✅ Pass | 证据纪律四条即意图约束;spec 记录 WHAT/WHY,HOW 收敛于本 plan |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | contracts/ 三份合同先于实现;pytest contract 测试 + 上游 node 测试双轨(FR-013);tasks 阶段测试任务先于实现任务 |
| V | AI Agent Integration Standards | ✅ Pass | collect-evidence 技能遵循 skill-format;不新增 /speckit.* 命令,零命令分发面变更 |
| VI | Continuous Quality & Observability | ✅ Pass | 干预台账 + compare 纵向验证(FR-011)本身即可观测性增强;feedback-step 全链路保留 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 完整走 requirements → clarify → plan → tasks → implement(spec Assumption 已定) |
| VIII | Code as the Single Source of Truth | ⚠ Partial — see Complexity Tracking | 复制托管(D1)在 spec-kit 内自洽单源;但与上游仓库构成有意分叉,以 UPSTREAM.md 溯源台账治理 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 只复制采集事实子集,裁决/呈现层明确不移植(FR-001、spec §8 清单);US7 交付边界已定界(仅 doctor 报告) |
| X | Documentation Naming & Location Conventions | ✅ Pass | UPSTREAM.md/LICENSE 为引擎目录内溯源文件(非 docs/ 空间);新参考文档落技能 references/ 与 shared/workflow/,符合既有布局;保留名零触碰 |
| XI | Dogfooding (Self-Application) | ✅ Pass | SC-006/007 要求对 improve-skills 自身跑证据闭环;feedback 泳道消费自产反馈(Loop B 实例) |

**Gates Status**: ✅ 除 VIII 为 ⚠ Partial(有意分叉,Complexity Tracking 有正当性论证)外全部通过;无 ❌ Fail。

**Re-check after Phase 1**: 2026-07-29 — data-model.md(8 实体)、contracts/ ×3、quickstart.md、feature-ref.md 生成后复查:合同不含裁决字段(IX 守住证据/观点边界)、测试双轨先行(IV)、镜像义务全部列举(VIII 单源纪律)。结论不变:10 Pass + 1 Partial。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/034-evidence-infra/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── findings-contract.md       # findings.json / manifest / index 合同
│   ├── evidence-utils-cli.md      # evidence-utils.py CLI 表面合同
│   └── engine-subset-boundary.md  # 复制子集边界与溯源合同
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

No standalone research.md — findings inlined under `## Clarifications`(两轮勘察:上游引擎子集事实 + spec-kit 消费侧触点,均为内部调查)。

### Source Code (repository root)

```text
scripts/js/better-harness/                 # 引擎子集(D1 源码托管;上游相对路径原样保持)
├── UPSTREAM.md                            # 溯源台账:源仓库/commit b2e621d/复制日期/清单/修改日志
├── LICENSE                                # 上游 MIT 副本
├── package.json                           # 最小化:type=module + engines(无 dependencies)
├── session-analysis.mjs                   # session 泳道 CLI 入口(上游根级入口,原样)
├── session-analysis/                      # 会话分析(整目录:37 文件 + platforms/ 4 适配器)
├── core-change-watch/                     # project 泳道:8 文件,各自带 shebang 直接可执行
├── agent-customize/                       # assets 泳道:cli.mjs + providers/{qoder,codex,claude,cursor,index}.mjs
├── coding-agent-practices/                # asset-baseline.mjs + asset-integrity.mjs + inventory.mjs(不含 checkup/)
├── agent-lint/                            # asset-baseline 的 lint 依赖(4 文件)
└── dependency-governance/                 # 可选依赖治理信号(cli.mjs 单文件)
.specify/scripts/js/better-harness/        # ↑ 全量镜像(FR-014,diff -rq 校验)
.specify/scripts/python/evidence-utils.py  # 泳道编排引擎(stdlib-only;doctor/collect/list/latest/compare)
scripts/python/evidence-utils.py           # ↑ 镜像(现行 scripts/python ↔ .specify/scripts/python 规则)
.specify/memory/evidence/                  # 证据存储:<run-id>/{findings,manifest,lanes/} + index.json
skills/collect-evidence/                   # 公共采集技能:SKILL.md + references/{evidence-contract,evidence-discipline}.md
.specify/skills/collect-evidence/          # ↑ 镜像
skills/improve-skills/SKILL.md             # 消费改造:Step 2 升级为证据步骤(30~60 行级)
skills/improve-agent/SKILL.md              # 消费改造:同上 + assets 泳道模板 lint 证据
skills/improve-team/SKILL.md               # 消费改造:runs 泳道消费替代原始工件解析
.specify/skills/{improve-skills,improve-agent,improve-team}/SKILL.md  # ↑ 三镜像
.specify/shared/workflow/evidence-step.md  # 标准证据步骤(与 feedback-step.md 对偶,单一事实源)
shared/workflow/evidence-step.md           # ↑ 镜像(现行 shared ↔ .specify/shared 规则)
tests/js/                                  # 上游摘取的引擎子集测试(~10 个 .test.mjs)+ run.sh 包装
tests/contract/test_evidence_utils_cli.py  # CLI 表面合同测试
tests/contract/test_evidence_findings_schema.py  # findings.json 合同测试
tests/contract/test_evidence_step_conformance.py # 三 improve 技能证据步骤合规测试
.specify/instructions.md                   # Skills 注册表 + 技能计数更新(经 /speckit.instructions 或对应编辑)
```

**Structure Decision**: 延续既有"scripts/ + skills/ + shared/ 三面镜像"的单仓布局,新增唯一顶层新目录族 `scripts/js/`(及其 `.specify/scripts/js/` 镜像)承载 Node 引擎子集;证据存储挂在既有 `.specify/memory/` 下与 feedback 平级;不新增 /speckit.* 命令,消费面全部通过技能与共享约定文档落地。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/js/better-harness/**`(全部引擎文件) | `.specify/scripts/js/better-harness/**` | `diff -rq scripts/js/better-harness .specify/scripts/js/better-harness` |
| `.specify/scripts/python/evidence-utils.py` | `scripts/python/evidence-utils.py` | `diff -q` |
| `skills/collect-evidence/**` | `.specify/skills/collect-evidence/**` | `diff -rq` |
| `skills/improve-skills/SKILL.md` | `.specify/skills/improve-skills/SKILL.md` | `diff -q` |
| `skills/improve-agent/SKILL.md` | `.specify/skills/improve-agent/SKILL.md` | `diff -q` |
| `skills/improve-team/SKILL.md` | `.specify/skills/improve-team/SKILL.md` | `diff -q` |
| `shared/workflow/evidence-step.md`(若源侧存在 shared/) | `.specify/shared/workflow/evidence-step.md` | `diff -q`(以仓库实际 shared 镜像方向为准,勘察确认后单向落盘) |
| `.specify/instructions.md`(Skills 注册表 + 计数) | `AGENTS.md`/`CLAUDE.md`/`QODER.md` 等为符号链接,零额外写;`.github/skills` 符号链接自动生效 | `find . -maxdepth 1 -type l` 链接完好 |

> 已知基线漂移(不在本 spec 修复,不得因此扩大范围):`.specify/skills/` 仅镜像 5/23 个技能、`instructions.md` 计数文本 22 vs 实际 23。本 spec 仅保证自己触碰的 4 个技能目录镜像一致,并把计数文本更新为加入 collect-evidence 后的真实值。

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| VIII Partial:引擎源码复制托管形成与上游的有意分叉(同一逻辑存在于两个仓库) | 证据采集是框架基础设施,不能依赖外部仓库的可用性、合同稳定性与 roadmap 优先级(D1);spec-kit 需自主演进平台适配器(D2) | submodule/npm 依赖被拒:上游无发布渠道、多 CLI 矩阵不在其 roadmap、且依赖会把上游裁决层拖进来;治理措施 = UPSTREAM.md 溯源台账 + 手动按文件 diff 回移(FR-002),分叉是受治理的而非放任的 |

## Phase 0: Research Review

内联结论(全部来自本轮两个 Explore 勘察,无外部研究项):

1. **子集依赖闭合已核实**:agent-customize / coding-agent-practices 对 session-analysis 的跨目录导入集中于 `cli.mjs/fs.mjs/paths.mjs` 等 7 文件;session-analysis 整目录复制即闭合。额外发现 `agent-lint/`(4 文件)是 asset-baseline 的 lint 依赖,纳入子集(spec FR-001"资产基线三信封"的一部分,不属边界侵蚀)。
2. **CLI 派发结构**:不复制上游 `better-harness-cli/` registry 门面;evidence-utils.py 直接以 argv-array 调用各能力入口(`session-analysis.mjs`、`core-change-watch/*.mjs`、`agent-customize/cli.mjs`、`coding-agent-practices/asset-baseline.mjs`、`dependency-governance/cli.mjs`),与方案 §3.1"泳道编排改由 Python 承担"一致。
3. **输出合同基础**:上游各能力已输出结构化 JSON envelope(`session-core-facts` schemaVersion 3、`agent-asset-baseline` schemaVersion 1 等);evidence-utils.py 做的是"envelope → findings 证据条目"的规范化映射,不改引擎输出。
4. **evidence-utils.py 模板**:直接仿 `feedback-utils.py`(--action + 纯函数派发 + JSON stdout + resolve_workspace_root)与 `docs-utils.py` 的 action 风格;合同测试仿 `test_feedback_utils_cli.py` / `test_feedback_entry_schema.py`。
5. **runs 泳道数据形态已核实**:STATE.md 四节结构(含 Post-Run Critique 追加行)、run-log.jsonl 七字段行、runs/*-report.md;两团队字段完备度不一 → 泳道实现必须按文件缺失降级为 partial。

## Phase 1: Design Artifacts

- **data-model.md**:9 实体(证据运行、findings 合同、证据条目、泳道、七态词汇、manifest、存储索引、干预台账、UPSTREAM 台账)+ 状态与校验规则。
- **contracts/findings-contract.md**:findings.json / manifest.json / lanes/*.json / index.json 字段级合同(C-1…);七态与泳道状态字面量钉死 Shared Strings。
- **contracts/evidence-utils-cli.md**:五 action 的参数、输出、退出码、降级语义合同。
- **contracts/engine-subset-boundary.md**:复制清单(含 agent-lint)、排除清单、UPSTREAM.md 必填字段、镜像校验命令。
- **quickstart.md**:doctor → collect → latest/compare → improve 消费的最短演练路径(含无 Node 降级场景)。
- **feature-ref.md**:Feature 038 绑定与本 plan 映射。
