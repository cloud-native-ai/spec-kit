# Quickstart Run — Feature 077（S1–S7）

本文件是 `quickstart.md` 的**实跑留档**。`quickstart.md` 是 plan 属主制品，只读；运行记录写在这里（T026 落真实输出）。

解释器：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python`（与 plan 期同解释器）。工作目录：仓库根。

## 场景与判据（执行前冻结）

| 场景 | 内容 | 判据（只看退出码、记录字段与差异行枚举） |
|------|------|------------------------------------------|
| S1 | 本线解析：`--action lookup --unit-id "spec:077-doc-sdd-integration"` | 退出码 0；`source: declaration`；`flow_class` 等于本线声明行取值；`marker: null`；`basis: null` |
| S2 | 三例判定（声明 `expression` / 不写字段 / 写非法值） | 三例**各答不同**：`expression` + `source: declaration` + exit 0；`execution` + `source: default` + 默认标记 + `declaration-absent`（advisory）+ exit 0；`flow_class: null` + `source: declaration` + stderr 点名文件:行号与取值 + **exit 1** |
| S3 | 结构门禁：`--action structure --spec-dir <spec 目录>` | 本线为执行类 → `status: not-applicable` + `class=` / `source=` + 非空伴生量 + exit 0，且不出现「0 violation(s) passed」；只做 plan 侧时另标 `two-way: not-run` |
| S4 | 七模板接线存在性 | 七个模板各恰 `1` 次 `flow-class-check.py`；`docs.md` / `humanize.md` 不变 |
| S5 | 分发漂移 | `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 相对 plan 基线**无新增漂移**（退出码 0，六对 `ok`，副本全一致） |
| S6 | 两槽位审计 | `audit-test-budget.py` 的审计行为不变：`slots=baseline:N closure:N`；`docs-gate-full` 被接纳；NA 只在 `build` 子行面级单列 |
| S7 | 清理 | S2 的 `mktemp -d` 目录与 S6 的 `.specify/.tmp/` 夹具被清除；`git status --ignored` 不把它们当新增；仓库内不留永久工件 |

## 实跑记录

（按 S1 → S7 顺序追加；每个场景记：命令、真实输出、退出码、与上表判据的比对结论。）
