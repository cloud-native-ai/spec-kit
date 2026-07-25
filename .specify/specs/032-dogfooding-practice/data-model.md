# Data Model: Dogfooding Practice Adoption (Revised)

**Feature**: Feature 036 Dogfooding Practice | **Spec**: [requirements.md](requirements.md)

纯文档/模板特性："数据"即治理文本与指引节的结构，外加对既有循环机制的指认（引用，不新建）。

## Entities

### 1. Dogfooding Principle（治理原则）

| Field | Type | Description |
|-------|------|-------------|
| heading | Markdown H3 | `### XI. Dogfooding (Self-Application)` |
| core_idea | prose | 开发者与使用者紧密联系（甚至同一团队）→ 顺畅的"使用→反馈→迭代"循环 |
| loop_a | normative | 指认框架级循环：下游项目经既有 Feedback 机制回流帮助框架提升 |
| loop_b | normative | 指认项目级循环：下游项目复用框架能力为自己的产品建循环 |
| self_application_rule | normative | 框架功能演进 MUST 走自有 SDD 工作流 |
| deviation_rule | normative | 偏离 MUST 留档（`.specify/specs/<key>/` 或 `.specify/memory/`） |
| advisory_scope | normative | 对下游为建议性指引，MUST NOT 设门禁或新增机制 |

**Location**: `.specify/memory/constitution.md`；MINOR 升版。

### 2. Practice Guidance（下游实践指引节）

| Field | Type | Description |
|-------|------|-------------|
| section_heading | Markdown H2 | `## Dogfooding Practice`（instructions-template 内） |
| loop_a_path | list | 可操作回流路径：record → 阈值提示 → package → 手动提交（零自动传输说明） |
| loop_b_mapping | table/list | 能力映射：feedback 引擎 / memory / history / review / 任务记录 → 自建循环中的用途 |
| anti_patterns | list | 形式化、回音室、反馈失效、过度理想化 |
| adoption_advice | list | 分阶段推进 + 不适合自用形态的场景裁剪 |

**Location**: `templates/instructions-template.md` + `.specify/templates/instructions-template.md`（字节一致镜像）。
**Constraints**: 项目无关；非破坏并入；仅引用既有命令/动作，不得引入新机制描述。

### 3. Existing Loop Mechanisms（referenced — 指认对象，零变更）

| Mechanism | Feature | Role in Dogfooding |
|-----------|---------|--------------------|
| Feedback 机制（record/status/list/package/upstream/mark-submitted + 阈值提示） | 028 | Loop A 回流载体；Loop B 的发现记录工具（自定义 unit-id） |
| 任务记录 + verification.md | core | 迭代闭环证据（发现 → 任务 → 验证） |
| memory（session/knowledge） | memory 系统 | Loop B 经验沉淀 |
| history | 030 | Loop B 对话知识蒸馏 |
| review | 012 | Loop B 复盘节点（既有 Feedback 步骤，不新增） |

**Invariant（SC-004）**: 上述机制的动作集、命令模板步骤集、存储布局在本特性实现前后 MUST 完全一致。

## Validation Rules

- 指引节并入既有项目 MUST 保留用户自定义内容（既有 instructions 非破坏刷新机制）。
- 指引中出现的命令/动作名 MUST 与源码实际动作集一致（Principle VIII：以 `feedback-utils.py --help` 为准）。
- 术语：正式名词 "Dogfooding"；变体（Dogfooded/Dogfoodding）不得出现在正式文本中。
