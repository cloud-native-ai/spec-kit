# Quickstart Run — 069b

**Owner**: T009（场景 1 / 场景 2）；场景 3–6 与 docs-sync 由各自任务行（T013 / T023 / T025）按同一形态追加。
**Run date**: 2026-10-25 · **Tree**: 工作树基于 `c38b44cc`（`069b-isomorphism-migration-metrics`），本节的两段引擎输出在提交前实跑取得。
**Interpreter**: pytest 仅 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest` 可用；引擎用系统 `python3`。

---

## 场景 1 — 逐行核对同构映射（route b）

命令与真实输出（`stages = 8`、`gates = 6`、`findings = []`、退出码 0）：

```
$ python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format json
{
  "action": "isomorphism",
  "checked_at": "2026-10-24T17:17:24Z",
  "repo": "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit",
  "stages": 8,
  "gates": 6,
  "findings": [],
  "error": null
}
EXIT=0
```

```
$ python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format text
flow-class isomorphism: 8 stage row(s), 6 gate face(s), 0 finding(s)
EXIT=0
```

**逐行核对记录**（8 行 × `强制状态` 真实性；blocking 行取自 `shared/workflow/expression-gates.md` § 阶段算子表，16 行 / 6 面）：

| 阶段 | 强制状态 | 强制门禁 | 该阶段存在的 blocking 算子行（对应面） |
| --- | --- | --- | --- |
| requirements | 已强制 | `requirements-clarity`、`evidence-asof` | requirements-clarity、evidence-asof |
| clarify | 已强制 | `requirements-clarity`、`reader-purpose` | requirements-clarity、reader-purpose |
| plan | 已强制 | `fact-consistency`、`structure-links-build` | fact-consistency、structure-links-build |
| tasks | 已强制 | `fact-consistency`、`evidence-asof` | fact-consistency、evidence-asof |
| checklist | 已强制 | `reader-purpose`、`fact-consistency` | reader-purpose、fact-consistency |
| analyze | 已强制 | `fact-consistency`、`review` | fact-consistency、review |
| implement | 已强制 | `structure-links-build` | structure-links-build（`reader-purpose` 在本阶段只有 advisory，未被点名） |
| review | 已强制 | `review`、`fact-consistency` | review、fact-consistency |

核对结论：8 行全部 `已强制`，每行点名的每个 `(阶段, face)` 在该阶段都有一行 `阻断级别 = blocking` 的算子行；未出现「借别阶段 blocking 背书」的行；`已声明未强制` 在本版不出现（8 个阶段都有 blocking 算子，标成未强制反而是失真）。

---

## 场景 2 — 标注失真必须转红（route b）

注入在 `tmp_path` 的 owner 副本上进行（复制真实 owner / gate owner / 名册，MUST NOT 把仓库改坏再改回），每项由一支契约测试断言「引擎退出码 1 且 finding kind 命中」。

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_isomorphism_map.py \
    -q -p no:cacheprovider -k injected
8 passed, 15 deselected
EXIT=0
```

| 注入 | 期望 kind | 执行测试（nodeid 后缀） | 结果 |
|------|-----------|--------------------------|------|
| `implement` 行 `强制门禁 = reader-purpose`（该阶段只有 advisory） | `annotation-false-enforced` | `test_injected_false_enforced_turns_red` | passed |
| `requirements` 行改 `已声明未强制`（该阶段有 blocking） | `annotation-false-unenforced` | `test_injected_false_unenforced_turns_red` | passed |
| `plan` 行同时清空 `强制门禁` 与 `强制状态` | `slogan-row` | `test_injected_slogan_row_turns_red` | passed |
| 删掉边界 (c) | `boundary-missing` | `test_injected_boundary_missing_turns_red` | passed |
| 边界 (c) `门禁处理` 不写 face id | `boundary-unbound` | `test_injected_boundary_unbound_turns_red` | passed |
| 边界 (b) `为什么不能互换` 置空 | `boundary-malformed` | `test_injected_boundary_malformed_turns_red` | passed |
| `tasks` 行结构格加入「按扩展名判定」 | `medium-axis-in-map` | `test_injected_medium_axis_phrase_turns_red` | passed |
| 阶段算子表追加一行 `pytest -q tests/` | `code-operator-in-expression-gates` | `test_injected_code_operator_turns_red` | passed |

判读：每种注入各自转红、退出码 1；真实树同一命令退出码 0（场景 1），因此红不是环境噪声。
