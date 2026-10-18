# Feature Reference: 子代理 CLI 配置管理与按派发量化（Feature 061）

**Feature ID**: 061 | **Feature Name**: 子代理 CLI 配置管理与按派发量化（Subagent CLI Config Management & Per-Dispatch Quantification）
**Requirement**: `.specify/specs/061-subagent-cli-config/requirements.md`（Requirement → Feature 绑定：本规格 ↔ Feature 061 自身，1:1）
**Status at plan time**: Draft → Planned（本 plan 落盘后推进；不越权 Implemented）
**Terminal authority**: `/tmp/061-subagent-cli-config-brief.md`（已裁定范围未被静默改写）

## FR → 设计映射

| FR | 条款 | 主要设计落点 | 契约 |
|----|------|--------------|------|
| FR-001 | 覆盖字段集 / 三层优先级 / 清除哨兵 | E1/E2 合并语义 | C-EC-05 |
| FR-002 | `mode`/`cli` 身份字段；默认层整层跳过 | E2/E4 | C-EC-06, C-EC-08 |
| FR-003 | 不新增 `mode:auto`；`requires_external`；native/virtual + 覆盖拒收 | E2/E5 | C-EC-06, C-EC-07 |
| FR-004 | 默认层缺失快速失败、无静默默认值 | E7 | C-EC-02, C-EC-15 |
| FR-005 | 引擎名锁定 / 三动作 / YAML 子集 | E1 | C-EC-01, C-EC-03 |
| FR-006 | `resolve` 输出字段 | E2/E3/E5 | C-EC-05..C-EC-12 |
| FR-007 | `validate` 拒收规则 | V1–V9 | C-EC-04, C-EC-13 |
| FR-008 | CLI 能力矩阵与 exit 2「字段 + 支持集」 | E4 | C-EC-08 |
| FR-009 | 量化方法域与 auto 顺序 | E5 | C-EC-09 |
| FR-010 | 显式 declared / qoder-settings 约束 | E5 | C-EC-09 |
| FR-011 | schema v2 / `configured` / `agent` / `agent:<slug>` | E6 | C-EQ-01 |
| FR-012 | `collect-dispatch` / 显式解析 / 幂等 / 快照校验 / 非阻塞失败 | E3/E6 | C-EQ-03, C-EQ-07, C-EQ-09 |
| FR-013 | `config` 组 11 字段 | E6 | C-EQ-04 |
| FR-014 | `llm` 按方法回显/实测/未采 | E6 | C-EQ-05 |
| FR-015 | `quality.exit_code` / 耗时 / token / errors | E6 | C-EQ-06 |
| FR-016 | `collect` 写 v2 且拒绝 agent 单元 | E6 | C-EQ-02 |
| FR-017 | list-records 过滤 / v1 归一化 / score | E6 | C-EQ-08 |
| FR-018 | 非阻塞 / append-only / 脱敏 / 64 KiB | E6 | C-EQ-10 |
| FR-019 | run-agent 解析/展示/透传/采集 | C-DW-01..03 | C-DW-01..C-DW-03 |
| FR-020 | preflight ④ 校验已解析配置 | C-DW-04 | C-DW-04 |
| FR-021 | create-agent schema 权威扩格 + 写后 validate | C-DW-05 | C-DW-05 |
| FR-022 | subagent-definitions 拓扑增补 | C-DW-06 | C-DW-06 |
| FR-023 | init 播种 `_defaults.yaml`（永不覆盖） | E7 | C-DW-07 |
| FR-024 | qoder-cli / templates-and-agents 文档补录 | C-DW-08 | C-DW-08 |
| FR-025 | 059/060/probe/preflight 零新增失败；有意扩展逐条登记 | C-DW-10 | C-DW-10, C-EQ-11 |
| FR-026 | `compile-embeds → regen-command-copies → sync-mirrors` 全绿 | C-DW-09 | C-DW-09 |
| FR-027 | 实现后重读派发契约；不兼容时快速失败 | C-DW-11 | C-DW-11 |

## SC → 验证映射

| SC | 验证方式 | 证据落点 |
|----|----------|----------|
| SC-001 | 引擎夹具：`cli_args` 逐字比较、`config_id` 重复运行比较、`source_chain` 逐字段核对 | `tests/contract/test_execution_config_engine.py`（S2）；verification.md |
| SC-002 | 负向夹具矩阵逐条执行，记录 exit 2 + 字段/支持集 | `tests/contract/test_execution_config_engine.py`（S3）；verification.md |
| SC-003 | 一次派发（或夹具产物）后查询存储、重复采集、`--unit-type agent --config-id` | `tests/contract/test_exec_quant_dispatch.py`（S4）；verification.md |
| SC-004 | 冻结基线 sorted nodeids + `comm` 比较；有意扩展逐条登记 | `notes/baseline-failed.txt`；verification.md |
| SC-005 | 生成三连实跑；init 播种/幂等字节比较 | C-DW-09；`tests/integration/test_init_execution_config.py`（S1/S5）；verification.md |
| SC-006 | `claude + none` 正向夹具（effective/cli_args/记录）与 `claude + declared` 拒收路径（错误面）分别做 qoder 默认值字面量检索，计数均为 0 | `tests/contract/test_execution_config_engine.py`；verification.md |

## 设计裁定（plan 期，供 implement/review 复核）

1. **不引入「显式 cli 单独触发 external」**：`mode` 缺省按 060 native 优先（FR-003）；external 由显式/默认层 `mode: external` 或非清除覆盖触发；显式 `cli` + 生效 native/virtual 拒收。默认层可提供 `mode` 作为默认值；SC-001 由默认层 `mode: external` + `cli: qodercli` 满足（source_chain 全默认层）。
2. **native/virtual + 显式 cli 拒收**：身份矛盾，不静默选择。
3. **claude + declared 当前不可达**：FR-008/US1-5 拒绝显式 model/effort/context，导致 declared 缺项 exit 2；矩阵保留 `declared` 作为旗标验证后的扩展位。SC-006 由 `claude + none` 正向路径与 `claude + declared` 拒收路径双路径验证零泄漏。这是显式裁定，不是静默改写。
4. **`quality.exit_code` 为可测量叶子**（`{value, provenance}` / `not_evaluated`），纳入 `MEASURABLE_PATHS`；`quality.errors` 保持 059 的 `{source, count}` 形状。
5. **macOS 宿主探测**：`/proc` 不可用；native/virtual 的 `qoder-settings` 需 `--host-cli` / `SPECKIT_HOST_CLI`；unknown → `none` + warning。
6. **并发幂等**：POSIX `fcntl.flock` 包裹查重 + append；非 POSIX 记录降级语义。
7. **记录无 null/空串**：effective 的 null 叶在记录中映射为 `not_evaluated`；`source_chain` 的 inline/derived 条目不写 `path` 键（059 `assert_no_blanks`）。
8. **log dir 绝对化**：`dispatch.sh` 在 `cd` 前 mkdir，run-agent 传绝对路径；远端在目标项目侧 resolve/collect。
9. **FR-001 清除语义**：effective 恒含 8 键，清除字段为 `null` 且不进入 `source_chain`/`cli_args`；`auto` 清除哨兵只作用于五个值字段，`quantification.method=auto` 是合法方法值。

## 交付面清单（框架源 → 镜像/生成面）

```text
# 框架源（edit）
scripts/python/execution-config.py                              # 新增：resolve / validate / list-configs
scripts/python/exec-quant.py                                    # 扩展：v2 / collect-dispatch / config 组 / quality.exit_code
templates/execution-config-defaults.yaml                        # 新增：默认层模板 owner
skills/internal/run-agent/SKILL.md                              # 派发前解析展示 / cli_args 透传 / 派发后采集
skills/internal/run-agent/references/dispatch-preflight.md      # ④ 改为已解析配置校验
skills/internal/create-agent/references/execution-config.md     # schema 权威扩格
skills/internal/create-agent/SKILL.md                           # 写后 validate 义务
shared/definitions/subagent-definitions.md                      # 拓扑声明增补（引用不复制）
src/specify_cli/__init__.py                                     # ensure_agent_layer_dirs 播种 + init 传入模板源
docs/reference/cli/qoder-cli.md                                 # 已验证旗标（dated record）
docs/reference/agents/templates-and-agents.md                   # 配置分层与量化指针

# 测试
tests/contract/test_execution_config_engine.py                   # 新增
tests/contract/test_exec_quant_dispatch.py                       # 新增
tests/integration/test_init_execution_config.py                  # 新增
tests/contract/test_exec_quant_engine.py                         # 有意扩展（逐条登记）
tests/contract/test_probe_engine_action_sets.py                  # 有意扩展（动作集）

# 生成镜像（由 sync-mirrors.py 投影，禁止手改）
.specify/scripts/python/execution-config.py
.specify/scripts/python/exec-quant.py
.specify/templates/execution-config-defaults.yaml
.specify/skills/internal/run-agent/{SKILL.md,references/dispatch-preflight.md}
.specify/skills/internal/create-agent/{SKILL.md,references/execution-config.md}
.specify/shared/definitions/subagent-definitions.md

# 生命周期与注册面（本 plan 提交）
.specify/memory/features.md                                     # 061 Draft → Planned（Total Features 保持 60 行口径）
.specify/memory/features/061.md                                 # 详情同步
```

**不触碰**：create-team / run-team 接线；新增 CLI 适配；codex/opencode stream-json 验证；跨 run 聚合/报表；自动打分/上送；native 派发的模型覆盖；059/060 的已实现行为与生命周期状态。

## Shared String → 框架源 / 运行面映射

requirements 的 STR 值是**运行时身份标识**（`.specify/` 路径）；实现落点必须是框架源，镜像由生成器投影。二者对照如下（One Source of Truth：不改变 STR 值）：

| STR | 运行时身份（requirements 值） | 框架源（实现落点） | 生成/镜像面 |
|-----|------------------------------|--------------------|-------------|
| STR-001 | `.specify/agents/execution/configs/_defaults.yaml` | 无源码（运行时由 init 播种） | 由 STR-010 播种 |
| STR-002 | `scripts/python/execution-config.py` | `scripts/python/execution-config.py`（新增） | `.specify/scripts/python/execution-config.py` |
| STR-003 | `scripts/python/exec-quant.py` | `scripts/python/exec-quant.py`（扩展） | `.specify/scripts/python/exec-quant.py` |
| STR-004 | `.specify/skills/internal/run-agent/SKILL.md` | `skills/internal/run-agent/SKILL.md` | `.specify/skills/internal/run-agent/SKILL.md` |
| STR-005 | `.specify/skills/internal/run-agent/references/dispatch-preflight.md` | `skills/internal/run-agent/references/dispatch-preflight.md` | 同名镜像 |
| STR-006 | `.specify/skills/internal/create-agent/references/execution-config.md` | `skills/internal/create-agent/references/execution-config.md` | 同名镜像 |
| STR-007 | `.specify/skills/internal/create-agent/SKILL.md` | `skills/internal/create-agent/SKILL.md` | 同名镜像 |
| STR-008 | `.specify/shared/definitions/subagent-definitions.md` | `shared/definitions/subagent-definitions.md` | `.specify/shared/definitions/subagent-definitions.md` |
| STR-009 | `.specify/skills/internal/create-team/scripts/dispatch.sh` | `skills/internal/create-team/scripts/dispatch.sh`（复用，不改） | 同名镜像 |
| STR-010 | `templates/execution-config-defaults.yaml` | `templates/execution-config-defaults.yaml`（新增） | `.specify/templates/execution-config-defaults.yaml` |
| STR-011 | `docs/reference/cli/qoder-cli.md` | 同名（开发文档，无镜像） | — |
| STR-012 | `docs/reference/agents/templates-and-agents.md` | 同名（开发文档，无镜像） | — |
| STR-013 | `--model DeepSeek-Flash --reasoning-effort max --context-window 1000000` | 由引擎按 effective config 生成 | 契约测试逐字断言 |
| STR-014 | `agent:<slug>` | exec-quant unit-id 语法 | — |
| STR-015 | `collect-dispatch` | exec-quant action | — |

## 基线记录（2026-10-18 实测，dated record）

- `sync-mirrors.py --check`：exit 0；templates 21 / skills/external 369 / skills/internal 136 / agents 3 / scripts 108 / shared 50 全 ok。
- `regen-command-copies.py --check`：exit 0。
- `probe-utils.py --action compile-embeds --check`：73 units, zero drift。
- `pytest tests/contract tests/integration`（profiles venv）：3278 passed / 25 failed / 1 skipped；25 个 sorted nodeids 冻结于 `notes/baseline-failed.txt`（实现前基线）。
- **改动面既有失败**：25 个失败中 7 个位于 `test_exec_quant_engine.py`（qoder reader / endpoint / masking / size cap / agent collection）——正是本特性要修改的引擎面。全局「零新增失败」在该文件上不具判别力；实现 MUST 对该文件做 before/after nodeid 对账，逐项解释 fixed / intentionally changed / unchanged，并写入 verification.md（C-DW-10）。
- qodercli：1.1.73；`-m/--model`、`--reasoning-effort`、`--context-window` 在 `--help` 中存在；`~/.qoder/settings.json` 的 `model.name = dfmodel`。

## 镜像义务与固定顺序

`probe-utils.py --action compile-embeds --write` → `regen-command-copies.py` → `sync-mirrors.py --write`。本特性不改 Wrap-up、不新增命令模板，前两步预期 no-op；三连仍须按序执行并记录退出码。Verify 判据为「相对 2026-10-18 基线零 NEW drift」。
