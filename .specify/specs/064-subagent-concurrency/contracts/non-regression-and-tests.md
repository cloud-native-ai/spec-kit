# Contract: Non-Regression & Test Strategy

**Feature**: 064
**Owning FR**: FR-060…FR-068
**决策**: `research.md` § R11–R12；Tests Mode = **ON**（可执行引擎 + shell 扩展）

## A. Non-Regression

- **NG-01（no-push）**: 任何流程 MUST NOT 自动 push；远程写操作仍受显式授权门控；模拟运行中 push 动作数 MUST 为 0（FR-060, SC-007）。
- **NG-02（不删未提交工作）**: 任何清理（worktree、运行时、证据）MUST NOT 删除未提交工作；清理只在合并成功或用户显式动作后执行（FR-061, FR-032）。
- **NG-03（迁移无静默丢失）**: 指令/技能/文档迁移（含 063 → 064 的档案收编）MUST 可审计地保留原文，或提供可追溯的等价引用；MUST NOT 静默丢弃内容（FR-062, CLP-17）。
- **NG-04（哨兵/判定/退出码不变）**: 除归属信封增量外，阶段哨兵字面量、watcher 判定状态机与退出码 MUST 保持不变；退出码仍由 `scripts/watch-target.sh` 代码侧 owner 决定（FR-063, EN-03/EN-06）。
- **NG-05（无新增运行时依赖）**: MUST NOT 引入常驻服务/daemon、外部服务、模型 API 或新运行时依赖；新脚本 MUST 为 Python 3 stdlib-only 或 bash，复用既有 feedback/probe/mirror 引擎（FR-064, 宪法 IX）。
- **NG-06（确认门与独立校验）**: 既有确认门、独立校验、阶段 deadline、测试预算与阶段命令内部流程 MUST 保持不变（FR-066, FR-041）。
- **NG-07（单线兼容）**: 单线运行 MUST 保持 U0–U6、阶段链、哨兵校验与卡死处置行为；新增 Registry/信封为统一增量（FR-068, LR-13）。受控例外：注册/注销失败时显式上送并停止该线（LR-02/LR-11），不视为行为回归。
- **NG-08（镜像义务）**: 所有新增/修改的技能文件 MUST 经 `sync-mirrors.py` 同步；`shared/definitions/probe-definitions.md` 的镜像 MUST 同改；验收判据为「本特性触碰的镜像对 no NEW drift」，基线见 `research.md` § 0（FR-045, 宪法 XI）。
- **NG-09（docs 入口）**: `docs/reference/skills/sdd-loop-driver.md` MUST 增加并发归属/生命周期与 CLI 档案入口；只引用不复述（FR-042）。

## B. Tests Mode

**Mode: ON**. 理由：本特性交付可执行 Python 引擎（`line-registry.py`）、shell watcher 扩展与新契约；不是 template-only 或 docs-only 特性。测试必须 red-first，并在 implement 阶段以真实运行记录 `verification.md`。

### Test Matrix

| 层级 | 文件 | 覆盖 |
|------|------|------|
| unit | `tests/unit/test_line_registry_engine.py` | 路径归一化、重叠判定、队列拓扑排序/回放、信封分类、lease 过期、入口判定表、状态词表 |
| contract | `tests/contract/test_line_registry_contract.py` | LR-01…LR-13 |
| contract | `tests/contract/test_line_envelope_contract.py` | EN-01…EN-16（watcher 归属、单线信封、自测新增用例、退出码不变） |
| contract | `tests/contract/test_workspace_isolation_contract.py` | WI-01…WI-21 |
| contract | `tests/contract/test_lifecycle_detach_reattach.py` | LC-01…LC-18 |
| contract | `tests/contract/test_sdd_loop_driver_cli_profiles.py` | CLP-01…CLP-17 + Probe Object + docs/镜像 |
| contract（既有，更新） | `tests/contract/test_sdd_loop_driver_skill.py` | H2 集合新增 `CLI Capability Profiles`；镜像测试覆盖新增文件 |
| integration | `tests/integration/test_two_line_isolation.py` | 双线同哨兵、foreign 事件、无标识消息（PATH 桩计数）、stale-run、PID 复用 |
| integration | `tests/integration/test_worktree_integration_queue.py` | 临时仓库双 worktree、重叠/不相交、`git fsck`、提交图、队列重放、运行时/镜像一次、失败保留 |
| integration | `tests/integration/test_session_kill_reattach.py` | 脱离子代理存活、kill 驱动、重接线 running/done/dead、零重派、reservation 排他 |

### Red-First Evidence

每个新脚本/扩展的实现顺序 MUST 为：先写失败测试 → 记录 red 运行（命令、时间、失败断言）→ 实现 → green。red 证据写入 `.specify/specs/064-subagent-concurrency/verification.md`（implement 阶段产物），不事后补记。

### Mutation Drills（至少三项）

| 变异 | 期望 |
|------|------|
| 删除 watcher 的归属过滤（把 foreign 当作 own） | `test_two_line_isolation` 至少 1 条转红 |
| 删除 detach（前台启动、stdio 继承主会话） | `test_session_kill_reattach` 至少 1 条转红 |
| 删除 `O_CREAT|O_EXCL` reservation（先查后建） | `test_lc_04_reservation_exclusive` / `test_lc_15_second_start_attaches_or_refuses` 转红 |

## C. Baseline & Environment

- **NG-10（基线纪律）**: 本环境无 pytest（`research.md` § 0）；测试 green 基线为 **Unobserved**，不得写成通过。implement 阶段 MUST 在具备 pytest 的环境运行 `scripts/bash/run-tests.sh`，并以 `--names-out` 做 name-level 基线对比。
- **NG-11（既有失败隔离）**: `watch-target.sh --self-test` 的 4 项既有失败（`pid-reuse`、`zombie`、`manifest`、`pgrep-zero-match-trap-reproduced`，macOS 平台退化）为基线，不计入本特性回归；新增归属自测用例必须独立通过。若本特性修复了其中任何一项，需在 verification 中单列说明，不得静默吸收。
- **NG-12（镜像基线）**: 技能镜像是 3 文件既有漂移、`shared/definitions` 是 9 文件既有漂移（`agent-definitions.md`、`contract-clause-definitions.md` 等，见 `research.md` § 0）；本特性只对触碰文件负责，验收以「no NEW drift」为准。
- **NG-13（覆盖与变异）**: 契约/集成测试 MUST 覆盖双线模拟、foreign 事件、工作区重叠/不相交、确定性队列、主会话崩溃/重接线、档案更新与反馈标记；删除归属或脱离行为时，至少一条测试 MUST 转红（FR-067, SC-008）。

## Traceability

| Clause | FR/SC | Planned tests |
|--------|-------|---------------|
| NG-01 | FR-060, SC-007 | `test_ng_01_no_push` |
| NG-02 | FR-061, FR-032 | `test_ng_02_no_uncommitted_deletion` |
| NG-03 | FR-062, CLP-17 | `test_ng_03_migration_content_preserved`（063 裁决表逐行存在；迁移条款在 064 有等价承载；无静默删除） |
| NG-04 | FR-063, EN-03/EN-06 | `test_ng_04_watcher_exit_codes_unchanged` |
| NG-05 | FR-064, 宪法 IX | `test_ng_05_stdlib_only` |
| NG-06 | FR-066, FR-041 | 既有确认门/独立校验契约测试 |
| NG-07 | FR-068, LR-13 | `test_ng_07_single_line_compat` |
| NG-08 | FR-045, 宪法 XI | `test_ng_08_mirror_no_new_drift` |
| NG-09 | FR-042 | `test_ng_09_docs_entry` |
| NG-10…NG-12 | SC-007/SC-008 | implement 阶段 `verification.md` + `run-tests.sh --names-out` 基线 |
| NG-13 | FR-067, SC-008 | 测试矩阵 + 三项变异演练 |
| FR-065 承载行（非 NG） | FR-065 | `test_lr_08_remote_minimal_fields`、`test_lc_17_remote_fields_isomorphic`（LR-08/LC-17 是 FR-065 的条款承载；NG 表不再声称承载 FR-065） |
| 测试矩阵 | FR-067, SC-008 | 上表所列 10 个文件 |
