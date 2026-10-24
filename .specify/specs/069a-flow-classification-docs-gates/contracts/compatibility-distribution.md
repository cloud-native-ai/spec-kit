# Contract: 兼容与分发（Compatibility & Distribution）

**Feature**: 069a（父 069） | **File scope**: 全局约束（无单一文件） | **FR served**: FR-011、FR-015、FR-016、FR-025、FR-026、FR-027；SC-008

- **C-1** 零新增命令

本切片 MUST NOT 新增 `/speckit.*` 命令。`templates/commands/` 的文件集在实现前后 MUST 完全一致（数量与文件名集合双重断言）——
两个既有模板（`docs.md`、`humanize.md`）获得接线小节，但**不新增、不删除、不重命名**任何模板文件。

- **C-2** 零项目侧存储

本切片 MUST NOT 在客户项目里新增任何存储路径、数据文件或读取点。
分类数据随 `shared/` 到达；检查器是可执行脚本，不持有状态；基线记录是**每特性一份**的规格笔记（`notes/expression-baseline.md`），属既有 `notes/` 面，不构成新存储系统。
`--action check` 不得在客户项目中创建缓存、索引或报告文件。

- **C-3** 分发路径与单包原子性

两份 owner 文档、两个引擎与四个接线点 MUST 落在框架源，经既有分发路径到达客户项目；四类载荷 MUST 由**同一个发行包**提供：

| 载荷 | 源 | 客户项目落点 | 证据（实测） |
|------|----|--------------|--------------|
| owner 文档 + 门禁 owner | `shared/` | `.specify/shared/` | `src/specify_cli/__init__.py:2462` 起的 shared 拷贝段 |
| 两个引擎 | `scripts/` | `.specify/scripts/` | `pyproject.toml` `[tool.hatch.build.targets.wheel.force-include]` 含 `scripts` |
| 两个技能 | `skills/external/` | `.specify/skills/` | `src/hatch_build.py` 阶段拷入（剔除 `site` 运行时数据） |
| 两个命令模板 | `templates/commands/` | 每工具命令副本（`.claude/commands`、`.qoder/commands` 等） | `pyproject.toml` force-include 含 `templates`；`generate_commands()` 由模板生成副本 |

本仓内 `shared → .specify/shared`、`scripts → .specify/scripts`、`skills/external → .specify/skills` 由
`scripts/python/sync-mirrors.py:82` 的 `MIRROR_PAIRS` 投影（`templates` 对排除 `commands`，命令副本改由
`scripts/python/regen-command-copies.py` 生成）。MUST NOT 通过手写 `.specify/` 副本分发；`.specify/` 侧文件 MUST 与源同字节。

- **C-4** 未刷新 = 旧副本无调用点；刷新 = 接线与载荷同时到位

分发单元是**一个发行包**，因此存在且只存在两种稳定状态：

1. **未刷新项目**：命令副本仍是旧版（含 `docs` / `humanize`），技能仍是旧版，`.specify/shared/` 无两份 owner、`.specify/scripts/` 无两个引擎。
   旧副本不含 lookup 调用，故**没有调用点**——行为与接线前逐字一致，不因框架升级而在本地产生新读取。
2. **已刷新项目**：一次刷新同时带来新命令副本、新技能、两份 owner 与两个引擎；接线生效，`/speckit.docs` 与 `/speckit.humanize` 在判定前各执行一次 lookup。
   两类载荷同包下发，故「有调用点但无 owner/引擎」不是正常状态。

**异常态（投影或手工拷贝造成的不一致）**：lookup 目标缺失或退出码为 2 时，接线 MUST 按默认类 + 固定标记（或 `owner-unavailable`）降级，
保持既有门禁、不中断流程、不静默切换门禁集（`expression-gate-operators.md` C-15）。
本切片 MUST NOT 引入需要客户项目主动执行的迁移步骤（父 A7），也 MUST NOT 写入项目侧注册表或缓存。

- **C-5** 接线面封闭（designated wiring surface）

本切片的既有表面改动**只允许**落在下列四个文件，且每处只允许一个接线小节/一句指针（形态与位置见
`flow-class-ledger.md` C-15 与 `expression-gate-operators.md` C-14）：

| 允许改动 | 允许内容 | 不允许 |
|----------|----------|--------|
| `templates/commands/docs.md` | lookup 调用 + 两个 owner 指针（`###` 小节，`## Outline` 内、分派之前） | 类别字面量；判据/算子表副本；新增 `## ` 顶级章节 |
| `templates/commands/humanize.md` | lookup 调用 + 两个 owner 指针（`###` 小节，`## Outline` 内、委派之前） | 类别字面量；第二处 `SKILL.md` 提及；`## Wrap-up`；六面算子表 |
| `skills/external/create-docs/SKILL.md` | R6 verify 的 checker 调用要求 + owner 指针 | 复制门禁规则；把 checker 变成无条件硬依赖 |
| `skills/external/humanize/SKILL.md` | Stage 6 的 owner 指针 | 复制算子表；改变 062 默认输出/报告契约；回指命令模板路径 |

下列路径在本切片中 MUST 零改动（内容哈希不变）：

- `templates/commands/**` 中**除上表两个文件之外**的全部模板（25 个）
- `skills/**` 中**除上表两个技能之外**的全部技能（49 个）
- `src/specify_cli/**`、`AGENTS.md`、`.specify/instructions.md`
- `.specify/specs/062-humanize-command/requirements.md`、`.specify/specs/067-loop-efficiency-hardening/requirements.md`、`.specify/specs/068-exec-quant-feedback-channel/requirements.md`（SC-008 字节不变）

每工具命令副本属**生成物**：由 `regen-command-copies.py` 从两个模板重生成，MUST NOT 手写或单独编辑。

- **C-6** 被修改的既有文件清单（封闭）

既有文件中允许改动的只有下列五处，且改动内容受限：

| 文件 | 允许改动 |
|------|----------|
| `shared/workflow/feedback-step.md` | 仅新增一行指针：声明复杂度轴与类别轴正交，指向 `shared/definitions/flow-class-definitions.md`（既有判据/红线段落零改动） |
| `templates/commands/docs.md` | C-5 的接线小节 |
| `templates/commands/humanize.md` | C-5 的接线小节 |
| `skills/external/create-docs/SKILL.md` | C-5 的 R6 指针与 checker 调用要求 |
| `skills/external/humanize/SKILL.md` | C-5 的 Stage 6 指针 |

五个文件之外，MUST NOT 修改任何既有源文件（生成物除外：命令副本由重生成更新；`.specify/` 镜像由 `sync-mirrors.py` 投影）。

- **C-7** 镜像与命令副本判据（名字级，非绝对绿）

| 检查 | 判据 |
|------|------|
| `python3 scripts/python/sync-mirrors.py --check` | 与编辑前基线比较「零新增差异」；本切片涉及的 7 个源文件（3 份 `shared/`、2 个 `scripts/`、2 个技能）在改动后 MUST 与其镜像同字节 |
| `python3 scripts/python/regen-command-copies.py --check` | 在**重生成之后** MUST 为 `OK`；判据是「生成物 = 源模板」，不是「模板未改动」 |
| 生成副本内容 | `.claude/commands`、`.github/prompts`、`.opencode/command`、`.qoder/commands` 下 docs 与 humanize 共 8 个副本 MUST 含接线（lookup 与 owner 指针），证明重生成真的发生 |
| `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` | `violations` 计数与 kind 集合 MUST 零新增（基线 3：`broken-link` 2 + `note-frontmatter` 1） |
| `pytest tests/contract -q` | 与 `notes/test-baseline-contract.txt` 比较，MUST 零新增失败名字（既有 31 失败不修、不掩盖） |

- **C-8** 效率度量复用既有通道

表达类的效率度量 MUST 复用 068 已建立的记录/反馈通道（`exec-quant.py`、`run-determination.py`、`feedback-utils.py`）；
MUST NOT 新建统计系统、评分体系或计量台账（FR-027）。基线记录是**每特性的一次性冻结值**，不是跨特性聚合台账。

- **C-9** 引用而非重写前序特性

062（humanize）、067（循环效率加固）、068（执行量化通道）的条款 MUST 只被引用，MUST NOT 被复述或改写；
三份 `requirements.md` 的字节不变由 C-5 与 `tests/contract/test_expression_compatibility.py` 共同钉住。

- **C-10** 兼容面的测试判据

由 `tests/contract/test_expression_compatibility.py` 与 `tests/contract/test_expression_gate_wiring.py` 分工钉住（均为名字级断言）：

| 断言 | 归属测试 |
|------|----------|
| `templates/commands/` 文件集不变（27 个，名字集合逐个比对） | `test_expression_compatibility.py` |
| 除 C-5/C-6 白名单外，其余模板与技能的内容哈希不变 | `test_expression_compatibility.py` |
| 其余 25 个模板与 49 个技能不含 `flow-class-check.py` / `expression-gates.md` / `doc-consistency-check.py` 引用（接线封闭） | 两者共同 |
| 四个接线点存在且位置正确（`docs.md` 的 `## ` 章节序列不变；`humanize.md` 仍无 `## Wrap-up` 且只有一处 `SKILL.md`） | `test_expression_gate_wiring.py` |
| 8 个生成副本含接线（证明 `regen-command-copies.py` 已执行） | `test_expression_gate_wiring.py` |
| `docs` 路径调用 `doc-consistency-check.py`；`humanize` 路径保留 062 保真检查并引用门禁 owner | `test_expression_gate_wiring.py` |
| 062 / 067 / 068 `requirements.md` sha256 与冻结值一致 | `test_expression_compatibility.py` |

任一断言失败即视为接线越界（回归 069b 或扩面）；修复方向是收窄接线，不是放宽断言。
