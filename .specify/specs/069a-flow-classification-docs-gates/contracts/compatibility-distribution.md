# Contract: 兼容与分发（Compatibility & Distribution）

**Feature**: 069a（父 069） | **File scope**: 全局约束（无单一文件） | **FR served**: FR-011、FR-015、FR-016、FR-025、FR-026、FR-027；SC-008

- **C-1** 零新增命令

本切片 MUST NOT 新增 `/speckit.*` 命令。`templates/commands/` 的文件集在实现前后 MUST 完全一致（数量与文件名集合双重断言）。

- **C-2** 零项目侧存储

本切片 MUST NOT 在客户项目里新增任何存储路径、数据文件或读取点。
分类数据随 `shared/` 到达；检查器是可执行脚本，不持有状态；基线记录是**每特性一份**的规格笔记（`notes/expression-baseline.md`），属既有 `notes/` 面，不构成新存储系统。
`--action check` 不得在客户项目中创建缓存、索引或报告文件。

- **C-3** 分发路径

两份 owner 文档与两个引擎 MUST 落在框架源（`shared/`、`scripts/`），经 `specify init` 的既有拷贝路径到达客户项目：

| 面 | 证据（实测） |
|----|--------------|
| `shared/` 拷贝 | `src/specify_cli/__init__.py:2462` 起的 shared 拷贝段 |
| `scripts/` 打包 | `pyproject.toml` 的 `[tool.hatch.build.targets.wheel.force-include]` 含 `scripts` |
| 镜像投影 | `scripts/python/sync-mirrors.py:82` 的 `MIRROR_PAIRS`：`shared → .specify/shared`、`scripts → .specify/scripts`（strict extras） |

MUST NOT 通过手写 `.specify/` 副本分发；`.specify/` 侧文件 MUST 与源同字节。

- **C-4** 未刷新项目行为不变

未刷新的客户项目里既没有新 owner 文档也没有新引擎，且**没有任何命令或技能调用它们**（本切片不改模板/技能，见 C-5）。
因此「旧项目行为不变」的实现方式是**没有调用点**，不是运行时探测版本。
本切片 MUST NOT 引入需要客户项目主动执行的迁移步骤（父 A7）。

- **C-5** 既有表面零改动

下列路径在本切片中 MUST 零改动（内容哈希不变）：

- `templates/commands/**`（因此 `regen-command-copies.py --check` 保持 `OK`）
- `skills/**`（含 `create-docs` / `humanize` 两个首批成员）
- `src/specify_cli/**`、`AGENTS.md`、`.specify/instructions.md`
- `.specify/specs/062-humanize-command/requirements.md`、`.specify/specs/067-loop-efficiency-hardening/requirements.md`、`.specify/specs/068-exec-quant-feedback-channel/requirements.md`（SC-008 字节不变）

- **C-6** 唯一被改动的既有文件

`shared/workflow/feedback-step.md` 是唯一被修改的既有文档，且只允许**新增一行指针**：声明复杂度轴与类别轴正交，并指向 `shared/definitions/flow-class-definitions.md`。
该文件既有的复杂度判据、红线段落与本切片无关的章节 MUST 零改动；镜像必须同字节。

- **C-7** 镜像与命令副本判据（名字级，非绝对绿）

| 检查 | 判据 |
|------|------|
| `python3 scripts/python/sync-mirrors.py --check` | 与编辑前基线比较「零新增差异」；本切片涉及的 5 个源文件在改动后 MUST 与其镜像同字节 |
| `python3 scripts/python/regen-command-copies.py --check` | MUST 保持 `OK`（零模板改动） |
| `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` | `violations` 计数与 kind 集合 MUST 零新增（基线 3：`broken-link` 2 + `note-frontmatter` 1） |
| `pytest tests/contract -q` | 与 `notes/test-baseline-contract.txt` 比较，MUST 零新增失败名字（既有 31 失败不修、不掩盖） |

- **C-8** 效率度量复用既有通道

表达类的效率度量 MUST 复用 068 已建立的记录/反馈通道（`exec-quant.py`、`run-determination.py`、`feedback-utils.py`）；
MUST NOT 新建统计系统、评分体系或计量台账（FR-027）。基线记录是**每特性的一次性冻结值**，不是跨特性聚合台账。

- **C-9** 引用而非重写前序特性

062（humanize）、067（循环效率加固）、068（执行量化通道）的条款 MUST 只被引用，MUST NOT 被复述或改写；
三份 `requirements.md` 的字节不变由 C-5 与 `tests/contract/test_expression_compatibility.py` 共同钉住。
