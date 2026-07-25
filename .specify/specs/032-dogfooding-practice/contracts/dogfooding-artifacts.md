# Contract: Dogfooding Governance & Template Artifacts (Revised)

**Feature**: Feature 036 Dogfooding Practice | **Traces**: FR-001…FR-005

由 `tests/contract/test_dogfooding_practice.py` 验证。原 `feedback-utils-extension.md` 契约已随需求修订作废并删除。

## C-1: Constitution Principle（FR-001, FR-002）

- `.specify/memory/constitution.md` MUST 包含匹配 `### XI. Dogfooding` 的 H3 原则标题（编号顺延 I–X）。
- 原则正文 MUST 包含：核心理念（开发者与使用者紧密联系、顺畅反馈循环）、Loop A 指认（下游项目经既有 Feedback 机制回流框架）、Loop B 指认（下游项目复用框架能力自建产品循环）。
- 原则正文 MUST 包含框架自用条款与偏离留档条款（落点：`.specify/specs/<key>/` 或 `.specify/memory/`）。
- 原则正文 MUST 声明对下游为建议性，MUST NOT 引入门禁或新增机制要求。
- 文件头 Sync Impact Report MUST 更新，版本 MUST 按 MINOR 增量升级。

## C-2: Instructions Template Section（FR-003）

- `templates/instructions-template.md` MUST 包含 H2 节 `## Dogfooding Practice`，且该节 MUST 包含：
  - **Loop A 路径**：record → 阈值提示 → package → 手动提交的可操作说明，并明示提交为手动、零自动传输；
  - **Loop B 能力映射**：至少覆盖 feedback 引擎、memory、history、review、任务记录五项及其在自建循环中的用途；
  - **反误区清单**：至少覆盖形式化 Dogfooding、回音室效应、反馈机制失效、过度理想化；
  - **采用建议**：分阶段推进与场景裁剪。
- 该节 MUST 项目无关（不含 spec-kit 专属事实）。
- 该节引用的动作名 MUST 属于 feedback 引擎实际动作集（record/status/list/mark-submitted/reindex/package/upstream）。

## C-3: Template Mirror Consistency（FR-003）

- `templates/instructions-template.md` 与 `.specify/templates/instructions-template.md` MUST 字节一致。

## C-4: No New Machinery（FR-004 / SC-004）

- `scripts/python/feedback-utils.py` 的 argparse `--action` choices 集合 MUST 保持为 `{record, status, list, mark-submitted, reindex, package, upstream}`（相对实现前不变）。
- `templates/commands/*.md` MUST NOT 因本特性新增任何步骤（对照基线 diff 为零 Dogfooding 相关新增）。
- `.specify/memory/` 目录布局 MUST NOT 因本特性新增子目录或索引文件。

## C-5: Non-Destructive Delivery（FR-003）

- 指引节经 `/speckit.instructions` 送达；既有项目刷新 MUST 保留用户自定义内容（沿用既有机制，不新增覆盖路径）。

## C-6: Terminology

- 全部新增正式文本中名词 MUST 为 "Dogfooding"；"Dogfooded" / "Dogfoodding" 仅可作为词汇表变体出现。

## C-7: Deviation Log Location（FR-002）

- 原则正文 MUST 指明偏离记录落点为 `.specify/specs/<key>/` 或 `.specify/memory/` 治理文档之一。
