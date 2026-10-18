# Implementation Plan: 子代理 CLI 配置管理与按派发量化（subagent-cli-config）

**Branch**: `061-subagent-cli-config` | **Date**: 2026-10-18 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `061-subagent-cli-config` → Feature 061 子代理 CLI 配置管理与按派发量化（Subagent CLI Config Management & Per-Dispatch Quantification）
**Input**: Specification from `.specify/specs/061-subagent-cli-config/requirements.md`（含 `## Clarifications` Session 2026-10-18）；终态权威文档 `/tmp/061-subagent-cli-config-brief.md`

## Summary

补齐「配置写了不生效」与「量化粒度到不了每次派发」两个缺口：新增 stdlib-only 确定性引擎 `scripts/python/execution-config.py`（`resolve / validate / list-configs`），按 `_defaults.yaml < configs/<slug>.yaml < 内联派发参数` 三层合并、按代码侧唯一能力矩阵校验、产出 effective config / `config_id` / `source_chain` / `skipped_layers` / `cli_args` / 配置快照；把 `scripts/python/exec-quant.py` 升级到 `schema_version=2`，新增 `unit_type=agent`、`collect-dispatch`、`config` 组、`quality.exit_code` 与 `configured` provenance；再把 run-agent / preflight / create-agent schema / subagent-definitions / `specify init` 播种 / 两份文档接线。交付面 = 2 个 Python 引擎（1 新 1 扩）+ 1 个模板 + 5 个技能/真源面 + 2 份开发文档 + 契约/集成测试；全部改动落在框架源，再经固定顺序 `compile-embeds → regen-command-copies → sync-mirrors` 投影到 `.specify/` 镜像与各工具命令副本。

## Technical Context

**Language/Version**: Python `>=3.8`（仓库既有下限）；新引擎 stdlib-only（`argparse / json / hashlib / pathlib / shlex / os / sys / datetime / re / fcntl`）；技能与文档为 Markdown/YAML
**Primary Dependencies**: 既有 `memory-utils.py`（工作区解析）、`exec-quant.py`（宿主探测复用）、`create-team/scripts/dispatch.sh`（external 可见性派发器）、`sync-mirrors.py` / `regen-command-copies.py` / `probe-utils.py`（生成面）
**Storage**: 文件即存储——`.specify/agents/execution/configs/`（tracked 配置）、`.specify/agents/execution/logs/`（gitignored 运行证据 + `config-snapshots/<config_id>.json`）、`.specify/memory/exec-quant/{records,scores}.jsonl`（append-only）
**Testing**: `pytest`（`contract` / `integration` 标记）；新增 `tests/contract/test_execution_config_engine.py`、`tests/contract/test_exec_quant_dispatch.py`、`tests/integration/test_init_execution_config.py`；有意扩展 `test_exec_quant_engine.py`、`test_probe_engine_action_sets.py`；实现开工前冻结失败基线
**Target Platform**: macOS arm64（本机实测）/ Linux；宿主 CLI = qodercli 1.1.73（旗标已验证）；`/proc` 宿主探测仅 Linux，macOS 走显式 `--host-cli` 覆盖
**Project Type**: 框架源仓库 + 自托管客户端（两顶帽子）——实现改动全部落 `scripts/`、`skills/`、`shared/`、`templates/`、`src/specify_cli/`、`docs/`、`tests/`
**Performance Goals**: resolve/validate 为本地文件解析（毫秒级、无网络）；collect-dispatch 为一次顺序读 + 一行 append；任何采集失败不阻塞派发
**Constraints**: 引擎名 `scripts/python/execution-config.py` 锁定（FR-005）；能力矩阵代码侧单一 owner（FR-008）；默认层缺失快速失败、无内置静默默认值（FR-004）；059/060 已实现行为与生命周期零改动；不执行真实外部派发（除非显式授权）；不手改任何生成物
**Scale/Scope**: 1 个新引擎（约 500 行）、1 个引擎扩展（约 +250 行）、1 个模板、5 个技能/真源面、2 份文档、3 个新测试文件 + 2 个既有测试文件的有意扩展

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**（动态枚举自 `.specify/memory/constitution.md` v1.13.0，共 16 项）:

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 全部设计决策溯源 requirements FR-001..FR-027；SC-001 场景由默认层 `mode: external` + `cli: qodercli` 满足，不引入 cli→external 覆写（Phase 0 裁定 1/5） |
| II | Feature-Centric Development | ✅ Pass | Feature 061 已注册（features.md + features/061.md）；本 plan 仅推进 Draft → Planned；Total Features 保持 60 行口径 |
| III | Intent-Driven Development | ✅ Pass | 分层/覆盖/量化语义先以「配置如何生效」意图定义，再落引擎参数 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 三个新测试文件先行（red-first）；契约 `contracts/` 三份承载全部可观测行为；实现前冻结失败基线；改动面涉及的 7 个既有 exec-quant 失败节点单独对账（见 C-DW-10） |
| V | AI Agent Integration Standards | ✅ Pass | 不新增 CLI；qodercli/claude 均在 `AGENT_CONFIG`；未验证 CLI 组合快速失败，不扩 provider 白名单 |
| VI | Continuous Quality & Observability | ✅ Pass | 配置快照 + 每派发记录 + exit_code/耗时/token 可测才记录；结构化引擎输出可机检 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass (NON-NEGOTIABLE gates) | 特性先注册后 plan；状态天花板 Planned；tasks/implement 由后续命令承接 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 能力矩阵以引擎常量 `CAPABILITY_MATRIX` 为唯一 owner；qodercli 旗标以本机 1.1.73 实测校准 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | stdlib-only 单文件引擎；无新服务/调度器/聚合报表；复用既有派发器与存储（YAGNI） |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新脚本 `scripts/python/execution-config.py`、新模板 `templates/execution-config-defaults.yaml`；docs 走既有 `docs/reference/{cli,agents}/` |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子：实现全部落框架源，`.specify/` 镜像由 `sync-mirrors.py` 投影；不手改镜像 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 dispatch.sh / memory-utils / exec-quant 宿主探测 / 三个生成脚本；未另造派发器或存储 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Controlled Execution（配置真正到达 CLI）与 Learning Capture（按派发证据）两个维度 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 运行时能力矩阵唯一 owner = 引擎 `CAPABILITY_MATRIX`；`contracts/` 是设计规格（dated），schema/真源/开发文档只引用代码 owner；默认层内容 owner = `templates/execution-config-defaults.yaml`，E7 仅作 dated record |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 拒收消息列「字段 + 支持集」；run-agent 派发前展示 effective config；quickstart 每命令带前提 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 缺失默认层/非法 YAML/冲突/未验证组合全部 exit 2；快照不一致非阻塞但可见；claude+declared 规格张量显式裁定并记录；同作者复核已完成（见 Re-check） |

**Gates Status**: ✅ 全部通过——无 Fail / Partial，Complexity Tracking 为 N/A。

**Re-check after Phase 1**: 见文末 Re-check 记录（Phase 1 产物落盘后复核同一张表）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/061-subagent-cli-config/
├── plan.md              # This file (/speckit.plan command output)
├── requirements.md      # /speckit.requirements 产物（已澄清）
├── checklists/requirements.md  # 需求质量清单（clarify 后复绿）
├── data-model.md        # Phase 1 output — 7 实体 + 校验规则
├── quickstart.md        # Phase 1 output — 6 场景（1 实跑基线 + 4 逐条免责/前提 + 1 可选授权）
├── contracts/           # Phase 1 output — 3 文件
│   ├── execution-config-cli.md   # 解析引擎 CLI 契约
│   ├── exec-quant-v2.md          # 记录 schema v2 与 collect-dispatch 契约
│   └── dispatch-wiring.md        # 技能/真源/init/文档接线与镜像义务
├── feature-ref.md       # Phase 1 output — FR/SC 映射 + 交付清单 + 基线
├── notes/baseline-failed.txt  # 实现前失败基线（实现阶段冻结；plan 期为 dated record）
├── tasks.md             # Phase 2 output (/speckit.tasks command — NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

**research.md**: No standalone `research.md` — Phase 0 findings are inlined below (<50 lines, all internal evidence).

### Source Code (repository root)

```text
scripts/python/                            # 框架源：新增 execution-config.py；扩展 exec-quant.py
templates/                                 # 框架源：新增 execution-config-defaults.yaml（默认层唯一模板 owner）
skills/internal/run-agent/                 # 框架源：SKILL.md 派发接线 + references/dispatch-preflight.md ④ 改写
skills/internal/create-agent/              # 框架源：references/execution-config.md schema 扩格 + SKILL.md 写后 validate 义务
shared/definitions/subagent-definitions.md # 框架源：拓扑声明增补三层配置/冲突/快照/量化指针
src/specify_cli/__init__.py                # 框架源：ensure_agent_layer_dirs 播种 _defaults.yaml（缺失才复制）
docs/reference/cli/qoder-cli.md            # 开发文档：已验证旗标（dated record）
docs/reference/agents/templates-and-agents.md  # 开发文档：配置分层与量化指针
tests/contract/                            # 新增 test_execution_config_engine.py / test_exec_quant_dispatch.py；扩展两个既有钉定文件
tests/integration/                         # 新增 test_init_execution_config.py
```

**Structure Decision**: 本特性严格落在既有框架源布局内，无新顶层目录。新增引擎与既有 `exec-quant.py` 同级（`scripts/python/` 的兄弟引擎可经 `sibling_engine` 复用）；默认层模板进入 `templates/` 随 wheel 打包并由 init 播种；`.specify/skills|shared|scripts|templates` 均为生成镜像，不在源码改动面内。

### Mirror Obligations *(mandatory)*

生成面基线（2026-10-18 本机实测，先于本 plan 的任何编辑）：`sync-mirrors.py --check` **exit 0**（templates 21 / skills/external 369 / skills/internal 136 / agents 3 / scripts 108 / shared 50 全部 ok）；`regen-command-copies.py --check` **exit 0**；`probe-utils.py --action compile-embeds --check` **73 units, zero drift**。Verify 列一律采用「相对该基线零 NEW drift」，不写预先编造的绝对退出码。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/execution-config.py`（新增） | `.specify/scripts/python/execution-config.py`（`scripts` 严格镜像对） | `sync-mirrors.py --check` 的 scripts 项零 NEW drift；diff 两侧字节一致 |
| `scripts/python/exec-quant.py`（扩展） | `.specify/scripts/python/exec-quant.py`（同上） | 同上 |
| `templates/execution-config-defaults.yaml`（新增） | `.specify/templates/execution-config-defaults.yaml`（`templates` 对，排除 commands） | `sync-mirrors.py --check` templates 项零 NEW drift |
| `skills/internal/run-agent/SKILL.md` + `references/dispatch-preflight.md` | `.specify/skills/internal/run-agent/**`（`skills/internal` 对） | sync-mirrors internal 项零 NEW drift；`## Wrap-up` 段零改动 |
| `skills/internal/create-agent/SKILL.md` + `references/execution-config.md` | `.specify/skills/internal/create-agent/**` | 同上；`## Wrap-up` 段零改动 |
| `shared/definitions/subagent-definitions.md` | `.specify/shared/definitions/subagent-definitions.md`（`shared` 对） | sync-mirrors shared 项零 NEW drift |
| `src/specify_cli/__init__.py` | 无镜像（CLI 包源码） | pytest + 安装态 init 集成测试 |
| `docs/reference/cli/qoder-cli.md` + `docs/reference/agents/templates-and-agents.md` | 无镜像（docs 为开发文档，不随框架分发） | 内容审计（字段/路径与 owner 一致） |
| 新增/扩展测试文件 | 无镜像（tests/ 不在 MIRROR_PAIRS） | pytest 直跑 |
| 各 SKILL.md 编译 `## Wrap-up` 面 | `probe-utils.py compile-embeds` 编译面 | 本特性不改 Wrap-up；`--check` 维持零漂移 |

**固定顺序**：`probe-utils.py --action compile-embeds --write`（若注册表/编译面有变）→ `regen-command-copies.py`（若命令模板有变）→ `sync-mirrors.py --write`。本特性不新增命令模板、不改 Wrap-up，预计前两步为 no-op，仍须按序执行并记录退出码。

## Complexity Tracking

N/A — Constitution Check 无 Fail / Partial。

## Phase 0: Research Review

无独立 `research.md`——以下为 2026-10-18 本机实测/源码勘探发现（Explore 子代理 + 直接读取；ANOMALY 无）：

- **引擎形态先例**：`exec-quant.py` 使用 `argparse` + 单一 `--action choices=[...]` + 手写分发；退出码约定 `0` 成功 / `2` 用法与输入错误（`InputError`）/ `1` 运行失败（`ExecQuantError`），`--format text|json`。新引擎沿用同一形态，便于测试与调用方一致。源码实测：`ACTIONS` 在 33 行、`SCHEMA_VERSION = 1` 在 36 行、`PROVENANCES` 在 38 行、`UNIT_TYPES` 在 39 行、`_UNIT_ID_RE` 在 54–58 行。
- **059 钉定面**：`tests/contract/test_exec_quant_engine.py` 钉 `ACTIONS_CLOSED_SET`（54）、`PROVENANCE_DOMAIN`（57）、`MEASURABLE_PATHS`（61–68）、`schema_version == 1`（265）、list-records key set（549–552）、score 形状（645–650）；`tests/contract/test_probe_engine_action_sets.py` 钉 exec-quant 精确动作集（86–95）。这些是**有意扩展**而非放宽。
- **060 钉定面**：`test_agent_dispatch_mechanism.py` C-15/C-16/C-17 钉 run-agent（拓扑/内联/配置/冲突字段/快速失败）与 preflight 字面量（`ConnectTimeout`、`model/effort/context`、`待补`、`handoff`、`sdd-project-setup`、`停线`/`上送`）；`test_fast_fail_discipline.py` 钉 `subagent-definitions.md` 的可见性/治理小节顺序与 5 条编号义务。本 plan 的编辑保留这些标题/顺序/字面量。
- **派发器事实**：`dispatch.sh` 用法 `<label> <workdir> <prompt-file> [-- <extra cli args>]`；`shift 3` 后剥离可选 `--`，剩余 `"$@"` 插在 prompt 前；产物三元组 `<label>.{jsonl,live.log,status}`；退出码经 `PIPESTATUS[0]`，`.status` 写 `<label> exit=<rc>`；无独立 execution_id，label 即运行身份。run-agent 只需接线，不新建派发器。
- **init 播种点**：`ensure_agent_layer_dirs` 在 `src/specify_cli/__init__.py:1897-1925` 创建 `templates/instances/execution/{configs,scripts,logs}`，当前**不复制任何模板文件**；`copy_local_templates` 在 2421 行调用它。`pyproject.toml` 的 wheel force-include 使 `templates/` 自动入包，因此新模板随安装分发。
- **生成面基线**：三连实测全绿（见 Mirror Obligations 开头）；当前工作树既有脏文件为 `.specify/memory/exec-quant/records.jsonl`、`.specify/memory/glossary.md` 及运行侧 session/feedback 产物——**不属于本特性提交面**，不提交、不还原。
- **qodercli 实测**：`qodercli 1.1.73`；`--help` 含 `-m, --model <model>`、`--reasoning-effort <level>`、`--context-window <size>`；`~/.qoder/settings.json` 的 `model.name = dfmodel`。宿主进程探测复用 `exec-quant.collect_agent()`（依赖 `/proc`，macOS 返回 `unresolved`），因此 native/virtual 的 `qoder-settings` 自动解析需要 `--host-cli` / `SPECKIT_HOST_CLI` 显式覆盖；external 规则不依赖宿主探测。
- **设计裁定（plan 期，须在 implement 前复核）**：
  1. **不引入「显式 cli 单独触发 external」**：`mode` 缺省仍按 060 native 优先（FR-003）。external 由显式/默认层 `mode: external`、或代理/内联非清除覆盖触发；显式 `cli` 与生效 native/virtual 同时出现属身份矛盾 → 拒收。默认层可提供 `mode` 作为默认值（层参与时生效、层跳过时一并跳过）。SC-001「只有默认层且选择 qodercli」由默认层声明 `mode: external` + `cli: qodercli` 满足：source_chain 全部指向默认层，`cli_args` 恰为 STR-013。
  2. 显式 `mode: native|virtual` 与代理/内联任一非清除覆盖同时出现 → 拒收并提示 external（FR-003）；与显式 `cli` 同时出现同样拒收。
  3. **claude + declared 的规格张量已显式记录**：FR-008 / US1-5 要求 claude 的显式 model/effort/context 一律 exit 2，因此 `declared` 在 claude 上当前不可达（缺三项即 exit 2）。本 plan 采纳显式验收条款优先（FR-008/US1-5），矩阵仍登记 `declared / none` 作为旗标验证后的扩展位。SC-006 的可机械计数目标由两条路径共同满足：`claude + none` 正向解析（effective/cli_args/记录中 qoder 默认值计数 0）与 `claude + declared` 拒收路径（错误面 qoder 默认值计数 0）。这是本 plan 在无人值守下的显式裁定，不是静默改写；implement/review 可据实际旗标验证结果修订。
  4. `quality.exit_code` 采用与 059 相同的可测量叶子形态：`{"value": <int>, "provenance": "measured"}` 或 `not_evaluated`，纳入 `MEASURABLE_PATHS`；`quality.errors` 条目保持 059 的精确形状 `{source, count}`（退出码已在 `quality.exit_code`，不新增键）。
  5. **FR-001 清除语义的实现形态**：FR-001 的「清除后的字段不进入 effective config」实现为「effective 恒含 8 键，被清除字段值为 `null`，且不进入 `source_chain`/`cli_args`」；`auto` 清除哨兵只作用于 `model / reasoning_effort / context_window / extra_flags / log_dir`，`quantification.method=auto` 是合法方法值而非清除。这是对 FR-001 的确定性实现解释，不改变其意图。
- **记录律（059 `assert_no_blanks`）**：v2 记录中禁止 null / 空串。`config.source_chain` 对 inline/derived 来源省略 `path` 键；effective config 的 null 叶子在记录中映射为 `not_evaluated`。
- **失败基线**：已于 2026-10-18 冻结于 `notes/baseline-failed.txt`（3278 passed / 25 failed / 1 skipped；sorted nodeids）。实现开工时复跑同一命令；改动面涉及的 7 个既有 exec-quant 失败节点单独对账（见 C-DW-10）。

## Phase 1: Design Artifacts Summary

> 本表在制品落盘后回填（summarize after, not before）。

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 7 实体（E1 分层输入 / E2 Effective Config 与身份 / E3 配置快照 / E4 CLI 能力矩阵 / E5 量化方法解析 / E6 派发量化记录 v2 / E7 默认层与播种）+ 校验规则 |
| Contracts | [`contracts/`](contracts/) | 3 文件：`execution-config-cli.md` / `exec-quant-v2.md` / `dispatch-wiring.md` |
| Quickstart | [`quickstart.md`](quickstart.md) | 6 场景（S1 生成面实跑基线 / S2–S5 逐条免责+前提 / S6 可选授权实派） |
| Feature ref | [`feature-ref.md`](feature-ref.md) | FR 27/27 + SC 6/6 映射 + 交付清单 + 基线记录 |

Phase 0 预期 vs 实际：实体 7（预估 6–8 ✓）；契约 3（预估 3 ✓）；quickstart 场景 6（预估 5–6 ✓）；无漂移需修正项。

## Phase 1: Re-check after Design

2026-10-18——Phase 1 产物落盘后复核 Constitution Check：16 项维持全 Pass。IX/XIV 抽查后修正了表述：运行时能力矩阵唯一 owner 是引擎 `CAPABILITY_MATRIX`，`contracts/execution-config-cli.md` C-EC-08 是设计规格（dated），schema/真源/开发文档只引用代码 owner；默认层内容 owner 是模板文件。XVI 的快速失败路径在 C-EC-15 与 C-EQ-03/C-EQ-09 明列；claude+declared 的规格张量作为显式裁定记录（Phase 0 裁定 3），不静默改写。

**Same-author delegation record（2026-10-18）**: 两轮 fresh-context 只读子代理独立复核（首轮两名分别评分 Constitution Check 与质量门/跨制品一致性；修正后第三名复核落地）。首轮回报的 load-bearing 发现与处置：

| 发现 | 级别 | 处置 |
|------|------|------|
| 「显式 cli 单独触发 external」覆写 FR-003 的 native-first | DECISION | 撤回该规则：external 由显式/默认层 `mode: external` 或非清除覆盖触发；显式 cli + 生效 native/virtual 拒收；默认层可提供 `mode` 默认值；SC-001/S2 改为默认层 `mode: external` + `cli: qodercli` 夹具（C-EC-06/07、data-model E2、quickstart S2） |
| claude + declared 在 FR-008/US1-5 下不可达，SC-006 可能空转 | DECISION | 显式记录裁定：采纳 FR-008/US1-5 优先；SC-006 由 `claude + none` 正向解析 + `claude + declared` 拒收路径双路径计数（Phase 0 裁定 3、feature-ref SC-006） |
| C-EC-08 声称不复制矩阵却又复制值 | CORRECTION | 改为「运行时 owner = 代码；契约是日期化设计规格；随框架分发的文档不得复制表格」；E4 改为形状 + 引用（C-EC-08、data-model E4） |
| C-EC-04 漏列 agent-config 的 `mode` 键 | CORRECTION | agent-config 允许键补 `mode`；默认层 `mode` 作为默认值允许（C-EC-04、E1） |
| cleared 字段在 effective 中 null vs absent 矛盾 | CORRECTION | 统一为：effective 恒含 8 键，清除/缺省 = null；source_chain 无该字段条目；cli_args 不生成（C-EC-05/11、E2、S3） |
| `source_chain.path=null` 违反 059 `assert_no_blanks` | CORRECTION | inline/derived 来源省略 `path` 键；记录中无 null/空串（C-EC-05、E2/E6） |
| `quality.errors` 新增 exit_code 键破坏 059 精确形状 | CORRECTION | 保持 `{source, count}`；退出码只在 `quality.exit_code`（C-EQ-06、E6） |
| log_dir 相对路径在 dispatch.sh `cd` 前 mkdir | CORRECTION | run-agent 传绝对 log dir；远端在目标项目侧解析；快照路径为 workspace-relative（C-DW-02、C-EC-12、C-EQ-03） |
| `--config-id` 可选使 FR-012 校验可跳过 | CORRECTION | `--config-id` 改为 `collect-dispatch` 必填（C-EQ-03、C-DW-03、S4） |
| 7 个既有 exec-quant 失败节点位于改动面，「零新增」判据失明 | CORRECTION | 改动面节点单独对账并逐项解释（C-DW-10、风险 8） |
| 子源 `subagent-definitions.md` 的 schema 指向 SKILL.md 旧位置 | CORRECTION | C-DW-06 要求改指 `references/execution-config.md` |
| features.md 行数为 60（054 历史上不存在），不应改为 61 | CORRECTION | Total Features 保持 60；061 行推进 Planned（注册面任务） |
| quickstart S5 出现自问自答式审议措辞；S6 未执行且未 pin | CORRECTION | S5 改为陈述句并补 `PYTHONPATH=src` 前提；S6 改为 prose runbook，不发出可执行示例 |
| C-EC-10 的 pin 仍以「显式 qodercli 选择」为前提，修正后的 mode 规则下不可达 | CORRECTION | pin 改为默认层声明 `mode: external` + `cli: qodercli` 的 defaults-only 夹具（C-EC-10、S2） |
| preflight ④ 命令未带 inline 拓扑输入，defaults-only 外部派发会 false-fail | CORRECTION | ④ 必须传入与派发相同的 inline 拓扑/覆盖输入，external 至少含 `--mode external`（C-DW-04） |
| C-EQ-06 把 `qualification` 列在 `quality` 组下 | CORRECTION | 明确 `qualification` 为顶层字段（C-EQ-06、E6） |
| C-EQ-09 用法错误清单漏 `--config-id` | CORRECTION | 补齐必填参数（C-EQ-09） |
| FR-001 的「清除字段不进入 effective config」与恒键/null 形态字面冲突 | CORRECTION | 记录实现解释：effective 恒含 8 键、清除值为 null；`auto` 清除只作用于五个值字段（Phase 0 裁定 5、feature-ref 裁定 9） |

两轮复核后无未处置的 load-bearing anomaly；decision 级两项（explicit-cli 规则、claude+declared）均已按上表显式裁定并落入契约/裁定记录，第二轮 6 项 correction 亦已修复并复核。

## Risks & Fast-Fail Points

1. **stream-json 字段未验证**：`duration_ms` / `usage.input_tokens` / `usage.output_tokens` 的嵌套形态未经本机验证。采集采用「递归按键存在才取，取最后一个匹配；缺一即 `not_evaluated`」，不猜测事件顺序或字段路径；契约 C-EQ-06 固定该规则。
2. **默认层跨 CLI 泄漏**：默认层整层跳过必须覆盖 `cli/model/reasoning_effort/context_window/extra_flags/quantification.method/log_dir`。SC-006 用 `claude + none` 正向路径与 `claude + declared` 拒收路径双路径做字面量计数，零容忍。
3. **驱动循环自依赖**：本特性修改 run-agent / preflight / exec-quant，而无人值守驱动循环依赖这些面派发后续阶段。implement 完成后、派发 review 之前 MUST 重新读取更新后的派发契约；若契约变化影响 driver 派发形态，按快速失败停线上送，不得静默适配（FR-027）。
4. **claude declared 不可达**：见 Phase 0 裁定 3；实现与评审须确认这是 FR-008/US1-5 的直接结果，而非遗漏。若后续验证 claude 旗标，扩展矩阵即可恢复。
5. **macOS 无 `/proc`**：native/virtual 的 `qoder-settings` 自动解析依赖 `--host-cli`/`SPECKIT_HOST_CLI`；external + qodercli 不受影响。未提供时 auto 解析为 `none` + warning，不猜测宿主。
6. **并发重复采集**：`collect-dispatch` 在「查重 + append」窗口使用 POSIX `fcntl.flock` 锁（`<records>.lock`）；非 POSIX 平台退化为既有查重语义并在契约中声明。
7. **config_id 漂移**：canonical JSON（sorted keys、紧凑分隔符、UTF-8）与字段集在 C-EC-11 唯一固定；snapshot 自校验（重算 config_id）防止快照被篡改/过期引用。快照按 `config_id` 覆盖：若同一 config_id 并发重复 resolve，后者会刷新 `resolved_at`，使先一次派发的 elapsed 回退值可能被低估；实现须在 collect 后再发起同 id 的新 resolve，或在 verification 中记录该窗口。
8. **改动面既有失败基线**：25 个既有失败中有 7 个位于 `test_exec_quant_engine.py` 的改动面（qoder reader、endpoint、masking、size cap、agent collection）。「零新增失败」对该文件不具判别力；实现 MUST 单独对这些节点做 before/after 对账，逐项解释 fixed / intentionally changed / unchanged，并登记于 verification.md。
9. **log dir 绝对化**：`dispatch.sh` 在 `cd <workdir>` 之前 `mkdir`，相对 log dir 会落到调用方 cwd。run-agent MUST 传入绝对路径；远端拓扑 MUST 在目标项目侧执行 resolve/collect 并使用目标机绝对路径。
