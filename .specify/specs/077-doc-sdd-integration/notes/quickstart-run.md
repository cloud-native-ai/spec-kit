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

实跑于 2026-10-30（本地拓扑，分支 `077-doc-sdd-integration`）。完整逐字输出（含每条命令与退出码）归档在
[`test-evidence/tasks-quickstart-s1-s7.txt`](../test-evidence/tasks-quickstart-s1-s7.txt)；本文件记读法与比对结论。

### S1 — 本线解析：**pass**

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/flow-class-check.py \
  --action lookup --unit-id "spec:077-doc-sdd-integration"
```
输出：`flow_class: execution` / `source: declaration` / `marker: null` / `basis: null` / `neutral: false`；退出码 **0**。
与判据比对：与实施前期望逐项一致（`source` 从 `default` 变为 `declaration`，其余字段不变）。

### S2 — 三例判定：**pass（一处前提更正，已披露）**

按 `quickstart.md` 原样执行（裸临时树 + `--repo`）：三例**都**返回
`owner-unavailable: owner document unreadable: none of <TMP>/shared/definitions/flow-class-definitions.md, <TMP>/.specify/shared/… exists`，
记录为 `flow_class: execution` / `source: default`，退出码 **2**。

**前提更正（实测）**：`quickstart.md` 的 Premises 写「`--repo` 接受任意目录作为仓库根」，但引擎的类别 owner
（`shared/definitions/flow-class-definitions.md`）是**相对于该仓库根**解析的；裸树没有它，只能走降级路径。
钉住该场景的单测 `tests/unit/test_flow_class_spec_key.py::_make_repo` 正是把该 owner 写进夹具根。
于是补跑 S2b（夹具根补一份逐字相同的 owner 文档，其余命令与判据不变）：

| 夹具 | 记录 | 退出码 |
|------|------|--------|
| `spec:fx-declared`（`**Flow Class**: expression`） | `flow_class: expression` / `source: declaration` / `error: null` | 0 |
| `spec:fx-absent`（无字段） | `flow_class: execution` / `source: default` / `marker: 未声明·按默认` / `error.label: declaration-absent` | 0 |
| `spec:fx-bad`（`expressive`） | stderr `invalid-class: .specify/specs/fx-bad/requirements.md:3 carries 'expressive', outside the closed set (execution, expression)`；`flow_class: null` / `source: declaration` / `error.label: invalid-class` | **1** |

与判据比对：三例**各答不同**，三项期望（含 `error.label` 只在 JSON 记录里出现、文本模式以 `marker` 呈现）逐项吻合。
未改 `quickstart.md`（plan 属主制品）。

### S3 — 结构门禁（执行类 → not-applicable）：**pass**

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/doc-consistency-check.py \
  --action structure --spec-dir .specify/specs/077-doc-sdd-integration
```
输出：`class=execution source=declaration` / `status: not-applicable` / `two-way: not-run` / `files_scanned: 1` /
`not-applicable: 结构门禁只适用于表达类；已检视 1 个文件，未做结构判定`；退出码 **0**。
追加既有 `--path <plan.md>`（S3b）：同一结论，`files_scanned: 2`，退出码 0。
与判据比对：呈现为 `not-applicable` 且**不**出现「0 violation(s) passed」；`two-way: not-run` 显式在位。

### S4 — 七模板接线存在性：**pass**

```bash
for f in requirements clarify plan tasks checklist analyze implement; do
  printf '%s ' "$f"; grep -c -E 'flow-class-check\.py' "templates/commands/$f.md"
done
```
输出：七个模板各 **1**；正控 `docs.md` = 1（既有入口不变）；`humanize.md` = **0**（该模板本就不带该引擎，与基线相同）。
与判据比对：七个各恰 1 次，两个既有入口不变——但注意 `humanize.md` 的基线值就是 0，其「不变」的判据是 0→0，不是 1→1。

### S5 — 分发漂移检查：**pass**

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/sync-mirrors.py --check
/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/regen-command-copies.py --check
```
输出：`OK: all per-tool command copies match the source templates.` + 六对全 `ok`（templates 22 / skills/external 406 /
skills/internal 136 / agents 3 / scripts 117 / shared 60）；两条均退出码 **0**。
与判据比对：相对 plan 基线（`plan-sync-mirrors-baseline.txt` / `plan-regen-command-copies-baseline.txt`）**无新增漂移**，
六对文件数与基线逐个相等。

### S6 — 两槽位审计（`docs-gate-full` 被接纳）：**pass**

```bash
D=.specify/.tmp/sdd-loop/tmp/plan077
/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  skills/external/sdd-loop-driver/scripts/audit-test-budget.py \
  --spine "$D/spine.md" --spec-dir .specify/specs/077-doc-sdd-integration --stage-check closure
```
输出：`slots=baseline:1 closure:1 reruns=0 exceptions=0 unknown=6 environment_failures=0` / `stages=6 complete=0` /
`status=fail`（六条 `stage evidence file missing`）/ 退出码 **1**。
与判据比对：槽位层面**零违规**（`docs-gate-full` 被接纳、两槽位各一次）；`status=fail` 全部来自夹具未提供六阶段 E3 证据，
与槽位内容无关——与 plan 期探针（`plan-audit-test-budget-docs-gate-probe.txt`）逐行同形。
负控（追加第二个 `baseline` 行）：`slots=baseline:2 closure:1 …` + `row 3: a second baseline slot is not allowed` +
`expected exactly 1 baseline slot, found 2`，退出码 1 —— 证明该探针不是空绿。

### S7 — 清理：**pass**

`rm -rf "$D"` 后：S2/S2b 的 `mktemp -d` 目录已由脚本内 `rm -rf` 清除（两次都打印 `removed`）；
`.specify/.tmp/sdd-loop/tmp/plan077` 已删除，空壳 `.specify/.tmp/` 一并移除（`ls -d .specify/.tmp` → absent）。
`git status --ignored --short` 的输出中**没有** `plan077` / `sdd-loop` / `.tmp` 任何条目；
仓库内不留永久工件（唯一新增是 `test-evidence/` 与本文件，均为本特性产物）。

## 结论

七个场景全部实跑：S1 / S3 / S4 / S5 / S6 / S7 按判据 **pass**；S2 按原样执行走降级路径（四个判据里的三答不同无法在裸树上呈现），
补跑 S2b（补 owner 文档，与钉住该场景的单测同形）后三例各答不同、逐项吻合，记 **pass（前提更正已披露）**。
`quickstart.md` 未被改写。

