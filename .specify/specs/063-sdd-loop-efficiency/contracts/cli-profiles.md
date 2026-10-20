# Contract: CLI Capability Profiles（CLI 能力档案）

**Feature**: 063 → Feature 058（演化）
**FR 覆盖**: FR-044…FR-049
**载体**: `skills/external/sdd-loop-driver/references/cli/README.md`、`skills/external/sdd-loop-driver/references/cli/<cli>.md`、`skills/external/sdd-loop-driver/SKILL.md`、`docs/reference/skills/sdd-loop-driver.md`、`tests/contract/test_sdd_loop_driver_efficiency.py`、`tests/unit/test_cli_profile_record.py`、`tests/fixtures/sdd_loop_efficiency/cli-profile-*`

- **CP-01（档案集合与落点）**: 每个作为 subagent 调用的 CLI MUST 拥有独立档案 `skills/external/sdd-loop-driver/references/cli/<cli>.md`；集合 MUST 至少包含 `qodercli`、`claude`、`codex`、`opencode`、`hermes`。`qodercli` MUST 含已验证的 `known` 条目；其余四份 MAY 以骨架建立，但 MUST 对每个维度显式标注 `known` / `unknown`。没有档案的 CLI MUST NOT 被派发：驱动 MUST 先建立最小骨架、记录缺口，再按安全缺省派发（FR-044）。
- **CP-02（必填维度）**: 每份档案 MUST 覆盖七个维度，缺一即契约失败：(a) 调用方式与关键参数（非交互旗标、cwd、提示词输入、模型/权限参数）；(b) 输出模式（`-p` 缓冲 vs [[STR-001]]，事件形状与终止结果位置）；(c) 后台/超时上限，含 `BASH_DEFAULT_TIMEOUT_MS` / `BASH_MAX_TIMEOUT_MS` 语义及其与阶段 deadline 的区分；(d) 哨兵可靠性（是否保证出现在终止 `result` 文本、已知的非终止事件哨兵字样情形、降级路径）；(e) session/run 日志位置（会话存储、恢复命令、运行日志目录）；(f) 已知缺陷（症状、影响版本、规避、`fixed_in`）；(g) 版本适用性（观测到的 CLI 版本、平台、适用区间）（FR-045）。
- **CP-03（known / unknown 与 provenance）**: 每个条目 MUST 带 `status: known|unknown`。`known` 条目 MUST 带 `observed_at`、`cli_version`、`evidence_ptr`；`unknown` MUST NOT 被猜测值填充，MUST NOT 以「看起来合理」替代观测。档案级 `## Provenance` 表 MUST 记录每次更新的日期、触发点、观测摘要、档案变更与反馈条目 id（standalone 时记 `standalone`）。版本不一致 MUST 视为观测事件，不得直接沿用旧版本结论（FR-045/FR-047）。
- **CP-04（SKILL.md 入口与单一 owner）**: `SKILL.md` MUST 增加 H2 [[STR-010]]，并声明三件事：派发前查档；U4/U5 观测后更新档案；`references/cli/` 是 CLI 行为知识的唯一落点，其他 references / 阶段提示词 / docs 只可引用，MUST NOT 复制档案内容。档案 schema 与观测程序的单一 owner 是 `references/cli/README.md`；SKILL.md 只摘要并指向它（FR-046）。
- **CP-05（U2 派发前查档）**: U2 准备派发时，驱动 MUST 读取目标 CLI 的档案并核对调用形态、输出模式、超时上限与哨兵可靠性；核对结果 MUST 写入 E6 派发记录（`profile_id`、`profile_version`、`observed_cli_version`）。档案声明不支持 stream-json 时 MUST 选择档案记载的缓冲/降级形态并记录原因，MUST NOT 盲目传入不支持的旗标；档案缺失时 MUST 先建骨架（CP-01）。查档匹配且无新事实时 MUST NOT 产生反馈条目（FR-047）。
- **CP-06（观测触发点与事件）**: 观测点 MUST 至少覆盖 U2 派发前、U4 独立校验、U5 停线。一次观测事件 = (a) 观测值与 `known` 条目不符；(b) `unknown` 字段获得已验证值；(c) 新 CLI 版本/平台行为首次出现。每个事件 MUST 先写入状态脊的 CLI 观测段（E8），再更新档案 provenance，再记录反馈（写前先动）。U4 的比对对象 MUST 至少包含：实际输出模式与事件形状、哨兵来源、status/exit 字段、runner rc 与 watcher 判定码、日志/session 位置；U5 的比对对象 MUST 至少包含：已知缺陷命中、超时上限、和本次停线的因果关系（FR-047）。
- **CP-07（probe + feedback 机制）**: 观测点 MUST 经既有 probe 注册表注册为 **一个最小 Probe Object**：`skill-sdd-loop-driver-wrapup`（`class_id=skill-wrapup`，`unit=skill:sdd-loop-driver`，`lifecycle_point=wrap-up`）。MUST NOT 新增 Probe Class、Handler 或 HandlerBinding；既有 `@point:wrap-up scope=all` 绑定已覆盖该单元的编译面。每次观测事件 MUST 通过 `feedback-utils.py --action record --unit-id "skill:sdd-loop-driver" --unit-type skill` 记录恰好一条反馈；`--review` 与 `--points` MUST 含稳定标记 [[STR-009]]`<cli>`；条目 MUST 可由 `feedback-utils.py --action list --contains "cli-profile:<cli>"` 检索。宿主无 `.specify/` 时按编译 Wrap-up 的 runtime-mode gate 跳过引擎调用，但档案更新与收尾汇总观测报告仍是必需项；MUST NOT 自动外传（FR-047/FR-049）。
- **CP-08（不改变阶段行为）**: 档案 MUST NOT 改变哨兵字面量、watcher 判定状态机、退出码、确认门、阶段 deadline 或测试预算。当前阶段 MUST 使用 U2 记录的派发形态；档案更新 MUST NOT 回溯改变它。观测冲突使当前阶段无法安全完成时 MUST 走既有 U5/重试/[[STR-005]] 程序，MUST NOT 以更新档案代替行为修复（FR-048）。
- **CP-09（版本与缺陷生命周期）**: `known` 条目 MUST 声明适用版本；新版本观测 MUST 触发重新核对关键字段。缺陷条目 MUST 保留历史，修复后记 `fixed_in`，MUST NOT 删除或在未复测时把旧缺陷当成当前事实。冲突观测 MUST 同存并附版本/平台/证据，不得静默择一（FR-045/FR-047）。
- **CP-10（交付、镜像与契约测试）**: 档案与 README MUST 位于 `skills/external/sdd-loop-driver/references/cli/`，经 `scripts/python/sync-mirrors.py --only skills/external/sdd-loop-driver` 同步到 `.specify/skills/sdd-loop-driver/`；契约测试 MUST 钉住 [[STR-010]] 节、五份档案、七个必填维度、known/unknown 纪律、[[STR-009]] 标记与最小 Probe Object 注册；docs 页 MUST 提供入口；MUST NOT 新增技能、命令、常驻服务、外部依赖或模型 API（FR-049）。

## Probe Object 注册设计（FR-047）

**Registry diff**（`shared/definitions/probe-definitions.md` → `.specify/shared/definitions/probe-definitions.md` 镜像同改）：

```text
## Objects 表新增一行：
| skill-sdd-loop-driver-wrapup | skill-wrapup | skill:sdd-loop-driver | wrap-up |
```

**模型落点**：该行属于既有 `skill-wrapup` Class（kind `internal`，insertion_type `wrap-up`，processing `record→threshold→package→manual→mark-submitted`），unit 为 `skill:sdd-loop-driver`，lifecycle_point 为 `wrap-up`。它是该单元唯一的 Object 行；`resolve_probe` 按 unit 可直接命中。`skill:sdd-loop-driver` 已有编译 `## Wrap-up` 面，因此本行同时关闭 `probe-utils.py --action probes --reconcile` 报出的 `embed without probe object: skill:sdd-loop-driver` 缺口。`skill:sdd-project-setup` 的同类缺口不在本特性范围，按既有基线披露，不声称全局 reconcile 清零。

**为什么不需要新 Handler / HandlerBinding**：CLI 观测是技能内的行为程序（CP-05/CP-06），其执行点是驱动在 U2/U4/U5 的查档与比对，不是新的生命周期插点；既有 `@point:wrap-up scope=all` 绑定已覆盖该单元的编译 Wrap-up 面。新增 Handler 需要新的 action/behavior_owner 与绑定，超出「最小」范围，且不会使反馈记录更可执行。

**compile-embeds 影响**：编译 fingerprint 只由 `## Handler` / `## HandlerBinding` 计算；新增 Object 行不参与，故 `SKILL.md` 的编译 `## Wrap-up` 面 MUST 零变化。验收命令：`python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` 退出 0 且报告 74 units / zero drift（实现期如单元数因其它变更上升，以实现起点冻结值为比较对象）。

**零漂移验证方案**：

1. `python3 .specify/scripts/python/probe-utils.py --action probes --validate` → exit 0。
2. `python3 .specify/scripts/python/probe-utils.py --action handlers --validate` → exit 0（Handler/HandlerBinding 未变）。
3. `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` → exit 0，74 units zero drift，编译 fingerprint 不变。
4. `python3 .specify/scripts/python/probe-utils.py --action probes --reconcile` → `skill:sdd-loop-driver` 的 `embed without probe object` 消失；仅剩 `skill:sdd-project-setup` 的既有缺口（已在基线披露）。
5. `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` → exit 0；新增档案与 README 成对镜像。
6. `bash scripts/bash/run-tests.sh tests/contract/test_probe_registry_umbrella.py tests/contract/test_feedback_probe_registry.py -q` → 全绿（后者使用临时注册表，不依赖真实对象计数）。

## 可追溯性

| 条款 | FR / SC | 计划测试 |
|------|---------|----------|
| CP-01 | FR-044, SC-014 | `test_cp_01_profile_set_and_location` |
| CP-02 | FR-045 | `test_cp_02_required_dimensions` |
| CP-03 | FR-045, SC-015 | `test_cp_03_known_unknown_provenance` |
| CP-04 | FR-046, SC-016 | `test_cp_04_skill_section_single_owner` |
| CP-05 | FR-047, SC-014 | `test_cp_05_pre_dispatch_check` |
| CP-06 | FR-047, SC-015 | `test_cp_06_observation_triggers`；单测 `test_cli_profile_record.py` |
| CP-07 | FR-047, FR-049, SC-015 | `test_cp_07_probe_feedback_marker` |
| CP-08 | FR-048, SC-016 | `test_cp_08_non_interference` |
| CP-09 | FR-045, FR-047 | `test_cp_09_version_defect_lifecycle` |
| CP-10 | FR-049, SC-016 | `test_cp_10_delivery_mirror_contract` |

## FR/SC 覆盖核对

- FR-044 → CP-01/CP-05/CP-10
- FR-045 → CP-02/CP-03/CP-09
- FR-046 → CP-04
- FR-047 → CP-05/CP-06/CP-07
- FR-048 → CP-08
- FR-049 → CP-07/CP-10
- SC-014 → CP-01/CP-05；SC-015 → CP-03/CP-06/CP-07；SC-016 → CP-04/CP-08/CP-10
