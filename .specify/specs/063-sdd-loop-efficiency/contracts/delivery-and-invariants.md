# Contract: 安全不变量、自应用与分发（delivery-and-invariants）

**Feature**: 063 → Feature 058（演化）
**FR 覆盖**: FR-036…FR-043
**载体**: `SKILL.md`、`references/efficiency-model.md`、`docs/reference/skills/sdd-loop-driver.md`、`tests/contract/*`、`tests/integration/*`、`.specify/memory/features/058.md`

- **DI-01（确认门）**: 四项优化 MUST NOT 改变确认门：push 仍是破坏性动作、须显式授权；MUST NOT 新增自动批准或绕过路径（FR-036）。
- **DI-02（独立校验）**: 执行者自报的完成仍只是候选；哨兵、产物核验与纪律抽查 MUST 同时成立，校验者 MUST NOT 是该阶段执行子代理（FR-037）。
- **DI-03（卡死处置）**: 阶段 deadline、重试上限、四要素上送件（发现了什么 / 为何吃重 / 中间产物逐项可定位 / 可选处置）与状态脊先写后动 MUST 保持；脱离运行中途失去驱动 MUST 可恢复，MUST NOT 被静默遗弃。该「不变」MUST 以可复算的行为基线判定，MUST NOT 以名称级测试失败基线替代：基线制品为 [[STR-007]]（`base_commit` = 实际行为基线 `a1aac7e5`；规格冻结读数 `ba2a18db` 因首个行为面提交 `9e69f3de` 而不适用，按 FR-038 取首个行为面改动前的父提交并在状态脊记录差异），MUST 在实现首个行为面提交之前录制超时 / 重试上限 / 伪完成三类场景的处置元组，并以一个成功完成场景作为正控使 `next_stage_dispatched` 双向可观测；场景 MUST 由驱动侧可执行夹具（stub runner + 真实 watcher + 文档化 U4/U5 程序）观测产生，watcher 只提供 U3 判定，录制 trace 只能作补充证据；夹具 MUST NOT 从判定表转录或硬编码期望值，`initial_retries` MUST 固定为 0，`exit_code` MUST 分为 watcher 判定码与 runner rc。收口 MUST 在同一可执行夹具与同一初始重试数下重放，归一化剔除时间戳、PID、绝对路径与耗时后逐字段比较，任何差异 MUST 判回归并修复，MUST NOT 以归因豁免。`evidence_ptr` MUST 指向持久证据（临时运行根删除前复制到 spec-dir notes）；元组字段与录制/比较程序的 owner 是 `data-model.md` § Stall Behavior Baseline，本契约不复写字段表（FR-038/SC-010）。
- **DI-04（质量门）**: 四项优化 MUST NOT 降低质量门：analyze/review 必经、必需校验不得静默跳过、测试预算不得静默超支、快车道不得静默启用（FR-039）。CLI 能力档案由 064 拥有；档案更新 MUST NOT 被当作跳过校验或改变判定的理由（064 CLP-13）。
- **DI-05（交付面与镜像）**: 交付面 MUST 落在 `skills/external/sdd-loop-driver/`（SKILL.md、references、scripts）与 `docs/reference/skills/sdd-loop-driver.md`；MUST 通过既有 `scripts/python/sync-mirrors.py` 以 `--only skills/external/sdd-loop-driver` 同步到 `.specify/skills/sdd-loop-driver/`；MUST NOT 新增技能、命令或外部依赖。镜像判据 = 本特性触碰的 `skills/external/sdd-loop-driver` ↔ `.specify/skills/sdd-loop-driver` 对零 drift，且全部镜像对相对冻结基线（`research.md` B-2 的 plan 期清单与合并 064 后的当前读数）零 NEW drift；其余镜像对的既有 drift 作为已记录基线例外保留、不得扩大（FR-040/SC-012）。CLI 能力档案（`references/cli/`、契约、测试、Probe Object）由 064 拥有，不属于本交付面；063 只验证镜像字节一致，不修改内容。
- **DI-06（契约与行为夹具）**: 契约测试 MUST 钉住：快车道准入字段与 fail-closed 回退、测试预算与证据字段、plan 改动分类与 re-anchoring、stream-json 旗标/派生/哨兵行为、nohup 脱离形态与安全不变量。既有 loop-driver 契约 MUST 保持绿色，或因本特性被有意更新并记录理由（两项：SKILL.md H2 集合新增 `Efficiency Optimizations` 一节——`CLI Capability Profiles` 节由 064 拥有且已在集合中，本特性不改动；C-4 的 `sed` 派生断言改为 `stage-runner.sh`）。行为夹具 MUST 覆盖 FR-042(a)–(e)；SC-010 行为基线（[[STR-007]]）的字段面由契约测试钉住，其行为重放由驱动侧可执行夹具产生，夹具 MUST NOT 从判定表转录或硬编码期望值，录制 trace 只能作补充证据并在 `verification.md` 如实标注；LLM 驱动的阶段序列以实现期录制的编排演练为证据，确定性组件以 CI 测试为证据，两者在 verification.md 如实区分（FR-041/FR-042）。
- **DI-07（自应用）**: 063 自身 MUST 走完整阶段链（checklist/analyze/review 必经），MUST NOT 产生本特性自身的快车道记录；该事实 MUST 在规格、plan 与收尾证据中可见（FR-010/FR-043）。
- **DI-08（向后兼容与已披露的日志形态变化）**: 未启用快车道的现有用户 MUST 看到与改动前一致的**门行为**：默认完整链、快车道默认关闭、哨兵字面量、判定状态机、退出码、确认门、独立校验与卡死处置不变。stream-json 成为默认进度形态会改变日志文件集合（新增 raw stream 与派生 live log）并在不支持时降级；该变化 MUST 在 docs 页与收尾汇总披露，且 MUST NOT 改变完成判定（FR-039，SC-011/SC-012）。
- **DI-09（编排层优先）**: 四项优化 MUST 优先在编排层实现；本 plan 的结论是四项全部可在编排层实现，MUST NOT 静默修改框架命令内部。plan 约束的框架内部硬执行是显式排除项，设计代价见 `contracts/plan-constraint.md` PC-09（FR-043）。

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| DI-01 | FR-036, SC-010 | `test_di_01_confirmation_gates_unchanged` |
| DI-02 | FR-037, SC-010 | `test_di_02_independent_verification_unchanged` |
| DI-03 | FR-038, SC-010 | `test_di_03_stall_handling_unchanged`（含 [[STR-007]] 字段面、驱动侧可执行夹具、`exit_code` 双字段、`initial_retries=0`）；行为重放证据见 verification.md |
| DI-04 | FR-039 | `test_di_04_quality_gates_not_weakened` |
| DI-05 | FR-040, SC-012 | `test_di_05_delivery_and_mirror`（本对零 drift + 零 NEW drift 判定） |
| DI-06 | FR-041, FR-042 | `test_di_06_contract_and_fixtures` |
| DI-07 | FR-010, FR-043, SC-013 | `test_di_07_self_application` |
| DI-08 | FR-039, SC-012 | `test_di_08_backward_compatible` |
| DI-09 | FR-043 | `test_di_09_orchestration_layer_only` |

## FR/SC 覆盖核对

- FR-001…010 → `fast-lane.md` FL-01…FL-10
- FR-011…019 → `test-budget.md` TB-01…TB-10
- FR-020…025 → `plan-constraint.md` PC-01…PC-11
- FR-026…035 → `progress-decoupling.md` PD-01…PD-10
- FR-036…043 → 本文件 DI-01…DI-09
- SC-001/002 → FL；SC-003/004/005 → TB；SC-006 → PC（含 PC-11）；SC-007/008/009/011 → PD；SC-010/012/013 → DI。逐条验证方式见 `feature-ref.md`。
- CLI 能力档案的 FR/SC/契约由 Feature 064 拥有（064 `contracts/cli-profiles.md` CLP-01…CLP-17），不在本文件覆盖范围，也不在本仓库的 063 规格中定义。
