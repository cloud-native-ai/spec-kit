# Quickstart — Feature 069 / Slice 069b

**Date**: 2026-10-25 · **Spec**: [requirements.md](requirements.md) · **Design**: [plan.md](plan.md) · [data-model.md](data-model.md) · [contracts/](contracts/)

七个场景覆盖本切片的三条交付线（映射 / 迁移 / 度量）。每个场景标注验证路径：

- **route (a)** — 本阶段已对真实工具执行过一次，命令与输出原样粘贴；
- **route (b)** — 由实现期契约测试钉住（引擎动作在 plan 阶段尚不存在）。每个 route (b) 例子在**该例旁**列出它所依赖的前提；
  文件级免责声明不覆盖未列出的例子。

所有命令默认在仓库根 `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` 执行。

---

## 场景 1 — 逐行核对同构映射（route b）

```bash
python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format json
```

期望：`stages = 8`、`gates = 6`、`findings = []`、退出码 0。
**route (b) 前提**：① owner 文档已有 `## 同构映射（8 阶段 × 3 面）` 与 `## 不可同构边界`；② 引擎已有 `--action isomorphism`；
③ `loop-state.py` 的 `STAGE_ARTIFACTS` 键仍为 8 个阶段；④ `expression-gates.md` § 六面 仍为 6 行、§ 阶段算子表 16 行。
钉住契约：`contracts/isomorphism-map.md` C-2 / C-3 / C-13。

核对「每一行都有强制或标注」的人工入口（同一数据）：

```bash
python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format text
```

## 场景 2 — 标注失真必须转红（route b）

给一行加上一个不存在的 face id，或把某行改成 `已声明未强制`：

| 注入 | 期望红 | kind |
|------|--------|------|
| `强制门禁` 写 `reader-purpose` 但该阶段只有 advisory | `annotation-false-enforced` | 标注失真 |
| 该阶段有 blocking 算子却标 `已声明未强制` | `annotation-false-unenforced` | 标注失真 |
| 既无 face id 又无标注 | `slogan-row` | 口号行 |
| 删掉边界 (c) | `boundary-missing` | 边界 |
| 边界 `门禁处理` 不写 face id | `boundary-unbound` | 边界 |

**route (b) 前提**：注入在 `tmp/` 的 owner 副本上进行（`--repo` 指向一个含完整 `templates/commands` 与 `skills/` 的夹具根），
MUST NOT 把仓库改坏再改回。钉住契约：C-5 / C-6 / C-7 / C-8 / C-9。

## 场景 3 — 台账的双注入必须给出两种可区分的红（route b）

```bash
# 注入 A：从台账删掉一行
python3 scripts/python/flow-class-check.py --action check --repo <fixture-a> --format json
# 注入 B：破坏表形（使解析出 0 行而清单非空）
python3 scripts/python/flow-class-check.py --action check --repo <fixture-b> --format json
```

期望：

| 注入 | `red_kind` | 退出码 | 代表 finding |
|------|-----------|--------|--------------|
| A 删一行 | `gap` | 1 | `missing`（该单元） |
| B 破坏表形 | `parse-failure` 或 `owner-unavailable` | 1 或 2 | `row-malformed` / `ledger-truncated`，或 owner 不可解析 |

**判据**：两次运行的 `red_kind` MUST 不同；「静默绿」（退出码 0）样本数 = 0。
**route (b) 前提**：夹具根含 27 个命令模板与 51 个技能目录（或 ≥ floor 的等价清单），否则 `inventory-truncated` 会先红。
钉住契约：`contracts/ledger-reconciler.md` C-1 / C-2 / C-3；SC-003。

## 场景 4 — 委托关系由模板解析，不由人工清单（route b + 本阶段实测）

引擎入口（route b）：

```bash
python3 scripts/python/flow-class-check.py --action delegation --repo . --format json
```

期望：`commands_scanned = 27`，全部边 `verdict ∈ {same-class, neutral-exempt}`，`findings = []`，退出码 0。

**本阶段实测（route a，用一个等价的临时解析脚本，不是引擎）**：

| 项 | 实测值 |
|----|--------|
| 声明了 ≥1 条技能路径的命令模板 | 26 / 27（`/speckit.tools` 无） |
| 类不一致的边 | 0 |
| 类中立豁免的边 | 6（`docs→memory-record`、`feedback→manage-feedback`、`history→memory-record`、`instructions→memory-recall`、`instructions→memory-record`、`session→archive-session`） |

**route (b) 前提**：委托语法 `(?:\.specify/)?skills/(?:external/|internal/)?<name>/SKILL.md` 仍能覆盖全部模板；
台账的 27 个命令行与 51 个技能行仍在位。证伪夹具：把一个技能改成反类（必须转红），把一条类中立边保留（必须仍绿）。
钉住契约：C-8 / C-9；FR-012。

## 场景 5 — 六面 owner 指针 6/6 且判据不搬家（route b + 本阶段实测）

本阶段实测（route a，只读计数）：

```bash
awk '/^## 六面（封闭集）/{f=1;next} f&&/^## /{exit} f' shared/workflow/expression-gates.md | grep '^| ' | tail -6 | cut -d'|' -f3 | tr -d ' '
```

输出（6 行）：

```text
requirements-clarity
reader-purpose
evidence-asof
structure-links-build
fact-consistency
review
```

引擎入口（route b）：

```bash
python3 scripts/python/flow-class-check.py --action faces --repo . --format json
python3 scripts/python/doc-consistency-check.py --action verify \
  --path shared/definitions/flow-class-definitions.md \
  --spec-dir .specify/specs/069b-isomorphism-migration-metrics --faces duplicate
```

期望：`faces = 6`、每条指针可解析（含 `§` 锚）、`findings = []`；duplicate 面 `findings = []`（主体集封闭，
不含 S3 比较集的 9 条 owner 路径，尤其不含 `expression-gates.md` 本身）。钉住契约：C-11 / C-12 / C-13；SC-005。

## 场景 6 — 未刷新项目行为不变，刷新后原子到位（route a 探针 + route b 比对）

本阶段实测（route a）：三个样本均**未刷新**——069a 载荷不在位：

```bash
for p in /Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-agent \
         /Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-cli \
         /Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-function; do
  printf '%s ' "$(basename $p)"
  test -f "$p/.specify/shared/definitions/flow-class-definitions.md" && printf 'owner=yes ' || printf 'owner=no '
  test -f "$p/.specify/scripts/python/flow-class-check.py" && printf 'engine=yes\n' || printf 'engine=no\n'
done
```

输出（2026-10-25 实跑）：

```text
xuanji-agent owner=no engine=no
xuanji-cli owner=no engine=no
xuanji-function owner=no engine=no
```

快照与名字级比对（route b，实现期执行）：程序见 `notes/migration-samples.md`；
`comm -13 before.txt after.txt` MUST 为空，判据是 nodeid 集合而不是条数。
**route (b) 前提**：快照用 `git archive <HEAD>` 导出到 `~/tmp`，原始项目与其工作树不被修改；
套件命令原样取自 `notes/migration-samples.md`；套件无法启动或 `specify init` 不可执行时记 `not-evaluated`。
钉住契约：`contracts/migration-distribution.md` C-1 / C-2 / C-6 / C-7 / C-8；SC-002。

## 场景 7 — 三项基线只用既有仪器（route a，全部实跑）

```bash
python3 scripts/python/exec-quant.py --action list-records --since 2026-10-24 --format json
python3 scripts/python/feedback-utils.py --action list --since 2026-10-24 --format json
python3 scripts/python/run-determination.py --action history --target /speckit.analyze --json
git log --diff-filter=A --format='%h %as' -- .specify/specs/069b-isomorphism-migration-metrics/requirements.md
```

本阶段实测结果：

| 量 | 实测 | 记录形态 |
|----|------|----------|
| `gate_calls` | 窗口内 6 条记录，其中检查类 2 条都属 069a（`run_id` 不含 `069b`）→ 本切片冻结值 `0` | `not-evaluated`（分母 0） |
| `confirmations` | `lifecycle_point: gate-` 命中 0；无 069b clarify 记录 → `0 + 0` | `not-evaluated`（分母 0） |
| `wall_clock` 起点 | `f0df3d0b 2026-10-24`（首次提交；`git log -1 --format=%as` 2026-10-25 实测返回 `2026-10-25`，故用 `--diff-filter=A`） | — |
| `wall_clock` 终点 | 无 `/speckit.analyze` 的 069b 记录 → `null` | `not-evaluated` |

**禁止**：把 `0` 记成「下降 100%」、把绝对量记成「达成」、把 `not-evaluated` 写进 `verification.md` 的 SC 状态位。
钉住契约：`contracts/measurement-instruments.md` C-1…C-8；记录见 `notes/expression-baseline.md`。

---

## 场景之外：本切片不做的事

- 不新增 `/speckit.*` 命令，不新增门禁面，不改阶段集合与 P0/P1；
- 不把新动作接进任何命令模板或技能（它们不是调用点）；
- 不在客户项目新增存储或读取点；
- 不重写 062 / 067 / 068，不修改 069a 的规格与判据正文。
