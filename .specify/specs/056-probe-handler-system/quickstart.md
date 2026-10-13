# Quickstart: Probe-Handler 体系（056）

**Spec**: `.specify/specs/056-probe-handler-system/requirements.md` | **Date**: 2026-10-13

> **执行状态声明（适用于全部含 `probe-utils.py` 的命令示例，及一切依赖迁移后状态才成立的命令）**：本 quickstart 写于规划阶段，`probe-utils.py`（[[STR-002]]）尚未实现——含该引擎的命令**未经实跑**，其有效性由 contracts/compile-embeds.md § 契约测试锚点表登记的契约测试钉住（route (b)）。**依赖迁移后状态的迁移态命令**（Scenario 1 步骤 4 的 regen/sync 写面、Scenario 4 的 `feedback-utils.py --help` 形态断言、各场景的迁移后 `grep` 验证步）同样未经实跑，随各场景前提清单覆盖。每个场景末尾列出该场景示例依赖的前提清单；实现阶段（/speckit.implement）必须逐条重测前提后才能沿用示例。**不含**该引擎且不依赖迁移后状态的命令（基线扫描三条：门控扫描、sync-mirrors --check、regen --check）已在本规划阶段实跑，真实输出冻结于 plan.md § 改前基线记录。

## Scenario 1: 注册新 handler 并重编译（加机制 = 注册一行 + 重编译）

**目标**：为 wrap-up 点新增一个 agent handler，验证注册→校验→编译→传播全链路。

```bash
# 1. 编辑真源注册表：Handler 表加一行，HandlerBinding 表加一行
#    （编辑 shared/definitions/probe-definitions.md 的 ## Handler / ## HandlerBinding 章）

# 2. 校验注册表
python3 scripts/python/probe-utils.py --action handlers --validate

# 3. 编译收尾段（写 templates/ 与 skills/ 源面）
python3 scripts/python/probe-utils.py --action compile-embeds

# 4. 传播（次序固定，FR-011）
python3 scripts/python/regen-command-copies.py
python3 scripts/python/sync-mirrors.py --write

# 5. 验证目标单元出现新段
grep -n '^## Wrap-up' templates/commands/implement.md
```

**期望结果**：步骤 2 exit 0；步骤 3 exit 0 且受影响单元的 `## Feedback` 手工段被单段 `## Wrap-up` 替换；步骤 5 在目标单元命中新段且新 handler 调用行在位。

**示例状态与前提（route (b)）**：
- 步骤 2/3/5 由 test_probe_engine_action_sets、test_compile_embeds_determinism、test_wrap_up_wording_gate_safe 钉住；步骤 4 为既有机制但**写面依赖迁移后状态，未经实跑**，其 compile → regen → sync 次序由 test_compile_propagation_order 钉住；步骤 5 的 `grep` 依赖手工段已被替换的迁移完成态，未经实跑，由 FR-016 完成态判据钉住。
- 前提：① 真源章节名与列序如 contracts/handler-registry.md 所载；② `--validate` / `--check` 旗标形态如契约；③ 新 handler_id 取 `h-` 前缀未占用的 id；④ 编译写入位置 = 既有 `## Feedback` 段落位。
- Teardown：`git restore shared/definitions/probe-definitions.md templates/ skills/ .claude .github .qoder .opencode .specify`（恢复全部被编译触碰的面）。

## Scenario 2: 漂移预检与对账

**目标**：注册表与编译产物失同步时，--check 先行报漂移；重编译后归零。

```bash
# 1. 直接改注册表（不重编译）制造漂移
#    （在 ## Handler 表改一行 order 值）

# 2. 预检
python3 scripts/python/probe-utils.py --action compile-embeds --check   # 期望 exit 1

# 3. 对账校验（错误类指名）
python3 scripts/python/probe-utils.py --action probes --reconcile       # 期望 exit 2（若构成错误类）或 exit 0（仅漂移非错误）

# 4. 重编译归零
python3 scripts/python/probe-utils.py --action compile-embeds
python3 scripts/python/probe-utils.py --action compile-embeds --check   # 期望 exit 0
```

**示例状态与前提（route (b)）**：
- 由 test_compile_embeds_check_and_reject 钉住（exit 1 / exit 2 两个分支）。
- 前提：① `--check` 只读、不写文件；② exit 语义按 contracts/probe-registry.md 退出码表；③ order 值变更属于「产物可再生成内容不一致」（exit 1），不属于错误类（exit 2）。

## Scenario 3: 零生效 handler 单元不输出段（Q5）

**目标**：scope 不覆盖的单元保持无收尾段形态。

```bash
# 1. 查询某简单命令单元的生效 handler
python3 scripts/python/probe-utils.py --action handlers --scope complex-commands

# 2. 对一个无生效 handler 的单元验证无段
grep -c '^## Wrap-up' templates/commands/<simple-command>.md   # 期望 0
```

**示例状态与前提（route (b)）**：
- 由 test_compile_embeds_zero_handler_no_section 钉住。
- 前提：① `--scope` 过滤旗标在 handlers action 上存在；② `<simple-command>` 占位由实现期实测的简单命令清单替换（本规划阶段不预写该清单）；③ 零生效单元在编译后保持无 `## Wrap-up` 段。

## Scenario 4: 迁移后动作封闭集对账

**目标**：证明 probe 族三动作已迁出、feedback 域 11 动作行为不变。

```bash
# 1. 两侧封闭集清单
python3 scripts/python/probe-utils.py --help | grep -A2 '--action'
python3 scripts/python/feedback-utils.py --help | grep -A2 '--action'

# 2. probe 注册表校验（含新 Class，排除非实体目录计数）
python3 scripts/python/probe-utils.py --action probes --validate
```

**示例状态与前提（route (b)）**：
- 由 test_probe_engine_action_sets（5 + 11 封闭集）与 test_feedback_probe_registry（延续钉住）承担；测试直接断言 argparse choices，`--help` 输出形态仅为人工核对路径——该断言**依赖迁移后的 choices，未经实跑**，随本清单免责。
- 前提：① probe-utils.py choices = probes/map/probe-inject/handlers/compile-embeds；② feedback-utils.py choices = 11 项（contracts/engine-action-sets.md 清单）；③ `--validate` 计数排除「非实体 probe 目录」节。

## 基线参照（已实跑，2026-10-13）

确认门控扫描、镜像漂移、命令副本漂移、SC-007 收尾面非空行计数的**真实命令与输出**冻结于 `plan.md` § 改前基线记录与 § SC-007 基线（具名小节），本文件不复制其正文（One Source Of Truth）。
