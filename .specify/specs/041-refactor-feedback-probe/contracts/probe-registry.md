# Contract: Probe Registry(probe 真源格式与不变量)

**Requirement**: `041-refactor-feedback-probe` | **Consumes**: FR-001~FR-004, FR-018~FR-019, SC-001 | **Pinned by**: `tests/contract/test_feedback_probe_registry.py`

## C-1 真源文件与层级

- 框架内部真源:`shared/definitions/probe-definitions.md`(canonical),镜像 `.specify/shared/definitions/probe-definitions.md` 逐字节一致(经 `sync-mirrors.py`)。
- 项目外部真源:`.specify/memory/feedback/probes/<object_id>.md`,一文件一 probe,YAML frontmatter。
- 引擎枚举顺序:框架真源(Classes + 内部 Objects)在前,项目外部 probe 在后;两者合并视图即「当前项目全部已置入 probe」。

## C-2 Classes 表 schema

`## Classes` Markdown 表,列序固定:`class_id | kind | collection | target_slice | processing | insertion_type`。

- C-2.1 `class_id` MUST 匹配 `^[a-z][a-z0-9-]*$` 且全局唯一。
- C-2.2 `kind` MUST ∈ {`internal`, `external`}。
- C-2.3 五个特征列 MUST 非空;空值 = 无效 Class(退出码 2)。
- C-2.4 初始类集恰好 3 行:`command-wrapup`、`skill-wrapup`(均 internal)、`external-custom`(external, target_slice=`host-custom`)。

## C-3 Objects 表 schema(内部)

`## Objects` 表,列序固定:`object_id | class_id | unit | lifecycle_point`。

- C-3.1 `object_id` MUST 匹配 `^[a-z][a-z0-9-]*$` 且全局唯一(与外部 probe 共享命名空间)。
- C-3.2 `class_id` MUST 引用存在的 Class;每个 Object 归属恰好一个 Class。
- C-3.3 `unit` 内部对象 MUST 匹配 `^(?:/speckit\.[a-z0-9._-]+|skill:[a-z0-9._-]+)$`(与条目 `--unit-id` 同语法)。
- C-3.4 初始对象集 = 既有 49 行(18 个 `unit=/speckit.*` + 31 个 `unit=skill:*`)**加**本需求交付时新增 1 行(`speckit-feedback-wrapup | command-wrapup | /speckit.feedback | wrap-up`,与新命令模板落地同变更),共 50 行,与实施时嵌入点清单(见 C-5,19 commands + 31 skills)一一对应。

## C-4 外部 probe 文件 schema

frontmatter 字段:`object_id`、`class_id`、`unit`、`lifecycle_point`(同 C-3 语义),另:

- C-4.1 `object_id` MUST 以 `ext-` 前缀开头(内外命名空间强制隔离)。
- C-4.2 `class_id` MUST 为 `kind=external` 的 Class(缺省 `external-custom`)。
- C-4.3 `unit` 外部对象 MUST 匹配 `^custom:[a-z0-9._/-]+$`(宿主自定义单元引用)。
- C-4.4 由 `--action probe-inject` 写入;五特征完备性经所属 Class 校验(C-2.3)。

## C-5 对账不变量(SC-001)

对账脚本(引擎 `--action probes --reconcile`)MUST 断言:

- C-5.1 内部 Objects ↔ 嵌入点清单双向零缺漏;嵌入点清单 = `templates/commands/*.md` 与 `skills/*/SKILL.md` 中含 `## Feedback` 节的单元(以仓库 grep 实测为准)。
- C-5.2 无未归类 Object(每个 `object_id` 都能解析到 Class)。
- C-5.3 任一 `unit` 在 Objects 表中至多出现一次(一单元一插点;多生命周期点扩展另行加行,`lifecycle_point` 区分)。

## C-6 派生不变量

- C-6.1 结构图(`--action map`)与合并真源双向零缺漏;真源未变时两次重建产出逐字节一致。
- C-6.2 条目的 `kind`/`slice` MUST 等于其 `probe`→Class 的对应字段(引擎写入时解析;不接受手工传值覆盖)。

## 示例(节选,真实文件 49 行)

```markdown
## Classes

| class_id | kind | collection | target_slice | processing | insertion_type |
|----------|------|------------|--------------|------------|----------------|
| command-wrapup | internal | 命令单次运行的回顾与 ≥1 条优化点 | commands | record→threshold→package→manual→mark-submitted | wrap-up |
| skill-wrapup | internal | 技能单次运行的回顾与 ≥1 条优化点 | skills | record→threshold→package→manual→mark-submitted | wrap-up |
| external-custom | external | 宿主自定义单元运行的回顾与优化点 | host-custom | record→local-consumption | wrap-up |

## Objects

| object_id | class_id | unit | lifecycle_point |
|-----------|----------|------|-----------------|
| speckit-requirements-wrapup | command-wrapup | /speckit.requirements | wrap-up |
| skill-create-tools-wrapup | skill-wrapup | skill:create-tools | wrap-up |
```
