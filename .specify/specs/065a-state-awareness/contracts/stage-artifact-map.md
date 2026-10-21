# Contract: 阶段产物映射与提交证据

**Scope**: 阶段 → 必需产物 / owned 路径 / 提交义务的唯一定义，以及“产物完整性”和“提交证据”的机械判据。
**Owner pair**: 运行时机器权威为 `scripts/loop-state.py` 的 `STAGE_ARTIFACTS` 数据表；人类可读 owner 为 `references/state-awareness.md` §Stage Artifact Map。本文件的 §2 表是 plan 阶段的接口定义，实施后作为 dated 设计记录，不再作为 live owner。契约测试 MUST 断言 script 与 reference 逐项一致（`AM-01`）。U4 核验清单的 owner 是 `references/stage-prompts.md` § Independent Verification；plan-owned 集合的 owner 是 `references/efficiency-model.md` §3.1。

## 1. 单一 owner

- **AM-01**: 产物映射的运行时 owner MUST 为脚本内 `STAGE_ARTIFACTS`，人类可读 owner MUST 为 `references/state-awareness.md` §Stage Artifact Map；二者 MUST 逐项一致。契约测试 MUST 读取两边并比较阶段键、`artifacts[]`、`owned_paths[]`、`commit_required`、`no_change_allowed` 五个维度；任一侧单独修改而另一侧未同步时测试 MUST 转红。SKILL.md 与其它 references MUST 引用 owner 章节，MUST NOT 复制整表。本文件 §2 表在实施后不得被援引为现行映射。
- **AM-02**: 映射 MUST 覆盖 `requirements / clarify / plan / tasks / checklist / analyze / implement / review` 八个阶段；每项 MUST 显式标注 `commit_required` 与 `no_change_allowed`。

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

- **AM-03**: `plan` 的五个必需产物与 `research.md` 合起来 MUST 覆盖 `efficiency-model.md` §3.1 的 plan-owned 集合。`research.md` 在 plan 模板中是条件产物，故列 owned-only：缺失不判不完整，但其存在时 MUST 进入提交路径集合。
- **AM-04**: `analyze` MUST 无必需文件产物、`commit_required=false`；其完成证据是哨兵与阶段日志正文，快照 MUST NOT 因缺少文件产物判其产物不完整。

## 3. 完整性

- **AM-05**: 产物完整性 MUST 只由“文件存在且非空”判定；目录类产物（`contracts/`、`checklists/`）MUST 要求目录存在且至少含一个非空文件。MUST NOT 从日志文本、时间或提交推断内容完整性。
- **AM-06**: 缺少必需产物或产物为空时 MUST 进入 `missing_artifacts[]`，且 `artifacts.complete=false`。哨兵存在而此项非空时 MUST 置 `false_completion=true`（`IA-10`）。
- **AM-07**: `stage` 未知时产物映射不可建立：spec 路径可读 → `artifacts.status=present`、`value_state=unknown`；spec 路径不可读 → `status=missing`、`value_state=na`；两种情形均 `complete=null`。MUST NOT 用其它阶段的产物顶替。

## 4. 提交证据

- **AM-08**: 提交证据 MUST 以状态脊 `stage_base_commit` 为基线，执行 `git log <base>..HEAD -- <pathspec>`。基线缺失或不可读时 MUST 记 `commits.value_state=unknown`，MUST NOT 回退为“最近一次提交”或 HEAD 猜测。`commit_required=false` 时 `commits.status=na`。
- **AM-09**: `pathspec` MUST 为阶段产物的仓库相对路径：requirements/clarify → `requirements.md`；plan → 五个必需产物 + `research.md`（存在时）；tasks → `tasks.md`；checklist → `checklists/`；review → `review.md`；implement → 仓库根（基线后的代码/测试提交）。路径 MUST 以解析后的 `spec_dir`（implement 除外）为前缀。
- **AM-10**: `uncommitted_artifacts[]` MUST 仅在基线已知时计算：必需产物存在但基线之后没有任何提交触及它 → 列入。基线未知时 MUST 输出空数组，并以 `commits.value_state=unknown` 表达不可判；MUST NOT 把空数组表述为“已全部提交”。
- **AM-11**: `implement` 的“产物完整”MUST 以基线后的提交证据表达，`artifacts` 记 `status=na`；`commit_required=true`。代码/测试的具体路径归各阶段命令，本映射不复制其目录结构。
