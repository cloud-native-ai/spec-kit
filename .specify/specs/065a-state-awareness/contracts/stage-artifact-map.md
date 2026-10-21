# Contract: 阶段产物映射与提交证据

**Scope**: 阶段 → 必需产物 / owned 路径 / 提交义务的唯一定义，以及“产物完整性”和“提交证据”的机械判据。
**Owner pair**: 运行时机器权威为 `scripts/loop-state.py` 的 `STAGE_ARTIFACTS` 数据表；人类可读 owner 为 `references/state-awareness.md` §Stage Artifact Map。本文件的 §2 表是 plan 阶段的接口定义，实施后作为 dated 设计记录，不再作为 live owner。契约测试 MUST 断言 script 与 reference 逐项一致（`C-50`）。U4 核验清单的 owner 是 `references/stage-prompts.md` § Independent Verification；plan-owned 集合的 owner 是 `references/efficiency-model.md` §3.1。`提交齐备` 谓词的唯一 owner 是 `interruption-and-action.md` C-46（`IA-14`）；本契约只定义它消费的证据状态。

## 0. 条款编号与别名

本契约的 11 条条款使用项目规范形态 `**C-N**`（语法 owner：`.specify/shared/definitions/contract-clause-definitions.md` §3）。全局编号接续 `interruption-and-action`（C-33…C-49）；历史文字引用使用下列别名。

| 历史别名 | 规范 ID |
|----------|---------|
| AM-01 | C-50 |
| AM-02 | C-51 |
| AM-03 | C-52 |
| AM-04 | C-53 |
| AM-05 | C-54 |
| AM-06 | C-55 |
| AM-07 | C-56 |
| AM-08 | C-57 |
| AM-09 | C-58 |
| AM-10 | C-59 |
| AM-11 | C-60 |

## 1. 单一 owner

- **C-50**: 产物映射的运行时 owner MUST 为脚本内 `STAGE_ARTIFACTS`，人类可读 owner MUST 为 `references/state-awareness.md` §Stage Artifact Map；二者 MUST 逐项一致。契约测试 MUST 读取两边并比较阶段键、`artifacts[]`、`owned_paths[]`、`commit_required`、`no_change_allowed` 五个维度；任一侧单独修改而另一侧未同步时测试 MUST 转红。SKILL.md 与其它 references MUST 引用 owner 章节，MUST NOT 复制整表。本文件 §2 表在实施后不得被援引为现行映射。`references/state-awareness.md` 是 `FR-044` 要求的 owner reference；其产物映射章节是脚本数据的镜像，不拥有映射规则。 (FR-006, FR-043, FR-044)
- **C-51**: 映射 MUST 覆盖 `requirements / clarify / plan / tasks / checklist / analyze / implement / review` 八个阶段；每项 MUST 显式标注 `commit_required` 与 `no_change_allowed`。 (FR-006, FR-007)

## 2. 映射表

| 阶段 | 必需产物 `artifacts[]` | owned-only 路径 `owned_paths[]` | `commit_required` | `no_change_allowed` |
|------|------------------------|--------------------------------|-------------------|---------------------|
| `requirements` | `requirements.md` | — | true | false |
| `clarify` | `requirements.md` | — | true | true |
| `plan` | `plan.md`、`data-model.md`、`contracts/`、`quickstart.md`、`feature-ref.md` | `research.md` | true | false |
| `tasks` | `tasks.md` | — | true | false |
| `checklist` | `checklists/` | — | true | false |
| `analyze` | —（报告正文在阶段日志，无新文件） | — | false | true |
| `implement` | —（以提交证据表达） | — | true | false |
| `review` | `review.md` | — | true | false |

- **C-52**: `plan` 的五个必需产物与 `research.md` 合起来 MUST 覆盖 `efficiency-model.md` §3.1 的 plan-owned 集合。`research.md` 在 plan 模板中是条件产物，故列 owned-only：缺失不判不完整，但其存在时 MUST 进入提交路径集合。 (FR-006)
- **C-53**: `analyze` MUST 无必需文件产物、`commit_required=false`；其完成证据是末行哨兵与阶段日志正文。因无必需文件产物，`artifacts.complete` MUST 为 `true`（vacuous truth），快照 MUST NOT 因缺少文件产物判其产物不完整，也 MUST NOT 因该缺失阻断 `verify`。 (FR-006, FR-007)

## 3. 完整性

- **C-54**: 产物完整性 MUST 只由“文件存在且非空”判定；目录类产物（`contracts/`、`checklists/`）MUST 要求目录存在且至少含一个非空文件。`checklist` 阶段另 MUST 要求存在自 `stage_base_commit` 起新增或修改的 checklist 文件；仅有预先存在的 checklist 文件 MUST NOT 判完整。`stage_base_commit` 未知时按 `C-57` 记 `value_state=unknown`，不猜完整。MUST NOT 从日志文本、时间或提交推断内容完整性。 (FR-006, FR-007, FR-008)
- **C-55**: 缺少必需产物或产物为空时 MUST 进入 `missing_artifacts[]`，且 `artifacts.complete=false`。末行哨兵存在而此项非空时 MUST 置 `false_completion=true`（`C-42`）。 (FR-007, FR-051)
- **C-56**: `stage` 未知时产物映射不可建立：spec 路径可读 → `artifacts.status=present`、`value_state=unknown`；spec 路径不可读 → `status=missing`、`value_state=na`；两种情形均 `complete=null`。MUST NOT 用其它阶段的产物顶替。 (FR-003, FR-006)

## 4. 提交证据

- **C-57**: 提交证据 MUST 以状态脊 `stage_base_commit` 为基线，执行 `git log <base>..HEAD -- <pathspec>`。基线缺失或不可读时 MUST 记 `commits.value_state=unknown`，MUST NOT 回退为“最近一次提交”或 HEAD 猜测；此时 `提交齐备=false`，动作路由按 `C-46` 的 `commit-baseline-unknown` 分支进入 `verify`（不得进入 `resume`/`stop` 提交分支）。`commit_required=false` 时 `commits.status=na`，按 `C-46` 视为提交齐备。 (FR-008, SC-002)
- **C-58**: `pathspec` MUST 为阶段产物的仓库相对路径：requirements/clarify → `requirements.md`；plan → 五个必需产物 + `research.md`（存在时）；tasks → `tasks.md`；checklist → `checklists/`；review → `review.md`；implement → 代码/测试路径枚举 `src/`、`skills/`、`scripts/`、`tests/`、`templates/`、`agents/`（仅触及 `docs/`、`.specify/` 或其它非代码路径的提交 MUST NOT 计为 implement 完成证据）。路径 MUST 以解析后的 `spec_dir`（implement 除外）为前缀。 (FR-006, FR-008)
- **C-59**: `uncommitted_artifacts[]` MUST 仅在基线已知时计算：必需产物存在但基线之后没有任何提交触及它 → 列入。基线未知时 MUST 输出空数组，并以 `commits.value_state=unknown` 表达不可判；MUST NOT 把空数组表述为“已全部提交”。 (FR-008, SC-002)
- **C-60**: `implement` 的“产物完整”MUST 以基线后的代码/测试提交证据表达，`artifacts.complete` 与 `提交齐备` 同源：`pathspec` 至少命中一个上述代码/测试路径且存在提交 → `true`；仅文档提交或零提交 → `false`。`artifacts` 记 `status=na`；`commit_required=true`。代码/测试的具体目录结构归各阶段命令，本映射只冻结上述 pathspec 枚举。 (FR-008, SC-001)
