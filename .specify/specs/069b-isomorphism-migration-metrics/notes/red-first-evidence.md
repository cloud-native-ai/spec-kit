# Red-First Evidence — 069b

**Owner**: T004 / T005（US1 红先行）与 T009（US1 转绿）；后续故事的证据按同一形态追加。
**Discipline**: 每支测试一条记录——命令、真实输出摘录、退出码；红形态 MUST 是「引擎缺该动作 / owner 缺该章节」，MUST NOT 是 import 或 collection error。
**Interpreters**: pytest 只有 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest` 可用（本仓 `.venv` 未装 pytest）。
**HEAD at red run**: `c38b44cc`（`069b-isomorphism-migration-metrics`，2026-10-25）。

---

## R1 — T004 红跑：`tests/unit/test_isomorphism_checker.py`

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/unit/test_isomorphism_checker.py -q -p no:cacheprovider
```

真实输出（每条失败的代表行；11 条全红）：

```
E   AssertionError: expected a JSON document on stdout, got empty output (stderr: "usage: flow-class-check.py [-h] --action {check,lookup} [--repo REPO]\n
    flow-class-check.py: error: argument --action: invalid choice: 'isomorphism' (choose from 'check', 'lookup')\n")
/Users/.../tests/unit/test_isomorphism_checker.py:86: AssertionError: expected a JSON document on stdout, got empty output

11 failed
EXIT=1
```

红形态判读：`--action isomorphism` 在 argparse 的 `choices` 之外 → 退出码 2、零 stdout。这是「动作缺失」，不是 import / collection error；
测试文件本身可被收集（`_run` 先断言引擎在盘，引擎是 069a 已交付文件）。

---

## R2 — T005 红跑：`tests/contract/test_isomorphism_map.py`

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/contract/test_isomorphism_map.py -q -p no:cacheprovider
```

真实输出（代表性断言）：

```
E   AssertionError: owner has no § 同构映射 section — expected `## 同构映射（8 阶段 × 3 面）`
    assert None is not None
/Users/.../tests/contract/test_isomorphism_map.py:244: AssertionError: owner has no § 同构映射 section

E   AssertionError: owner has no § 不可同构边界 section
/Users/.../tests/contract/test_isomorphism_map.py:...: AssertionError

19 failed, 4 passed
EXIT=1
```

红形态判读：owner 文档缺两个章节（T006 / T007 的交付面）与引擎缺 `isomorphism` 动作（T008 的交付面）。
当前已成立、因而红跑即绿的 4 条：`test_rejected_alternative_path_stays_absent`、`test_no_second_map_or_boundary_table_exists`、
`test_no_doc_is_code_licence_sentence_without_owner_pointer`、`test_gate_operator_column_carries_no_code_type_operator`——
它们断言的是「不应出现的东西」，实现前后都必须绿，红跑阶段绿不构成实现已存在。

---

## R3 — 两支合并红跑（与 T009 的转绿命令同一条）

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/unit/test_isomorphism_checker.py tests/contract/test_isomorphism_map.py -q -p no:cacheprovider

30 failed, 4 passed in 6.45s
EXIT=1
```

判读：两支测试合计 34 条，红 30 / 绿 4；无 collection error、无 skip。进入 T006 实现。

---

## G1 — T009 转绿：US1 定向套件

实现落盘（T006 owner 两章节 / T007 四边界与机械下限 / T008 引擎动作）后，重跑与 R3 完全相同的命令：

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/unit/test_isomorphism_checker.py tests/contract/test_isomorphism_map.py -q -p no:cacheprovider

..................................                                       [100%]
34 passed in 4.68s
EXIT=0
```

判读：R3 的 30 条红全部转绿，R1/R2 阶段已绿的 4 条保持绿；零 skip、零 xfail。

## G2 — T009 真实树引擎两形态

```
$ python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format json
{"action": "isomorphism", "checked_at": "2026-10-24T17:17:24Z", "stages": 8,
 "gates": 6, "findings": [], "error": null}
EXIT=0

$ python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format text
flow-class isomorphism: 8 stage row(s), 6 gate face(s), 0 finding(s)
EXIT=0
```

（完整 JSON 与逐行核对记录见 `notes/quickstart-run.md` § 场景 1。）

## G3 — 既有动作零改动（回归证据，非本切片断言）

```
$ python3 scripts/python/flow-class-check.py --action check --repo . --format text
flow-class check: 78 unit(s) scanned, 0 finding(s)
EXIT=0

$ python3 scripts/python/flow-class-check.py --action lookup --unit-id /speckit.docs --repo . --format text
unit_id: /speckit.docs
flow_class: expression
source: ledger
marker: null
basis: reader-oracle
neutral: false
EXIT=0

$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/unit/test_flow_class_check.py tests/contract/test_flow_class_ledger.py \
    tests/contract/test_flow_class_correctness.py tests/contract/test_expression_gates_doc.py \
    -q -p no:cacheprovider
63 passed in 16.16s
EXIT=0
```

判读：`check` / `lookup` 的既有输出与退出码不变，069a 的四个测试文件全绿。

## G4 — 中间态：镜像投影待 T024（US1 收尾时的已知红，不属于本阶段缺陷）

本阶段只改框架源（`shared/`、`scripts/`、`tests/`），**不手改** `.specify/` 镜像；镜像同步是 T024（Polish）的写目标。因此 US1 收尾时以下两条按设计为红，T024 执行 `sync-mirrors.py --write` 后转绿：

```
FAILED tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[scripts/python/flow-class-check.py->.specify/scripts/python/flow-class-check.py]
FAILED tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[shared/definitions/flow-class-definitions.md->.specify/shared/definitions/flow-class-definitions.md]
FAILED tests/contract/test_expression_compatibility.py::test_c7_mirrors_are_byte_identical
3 failed, 759 passed in 3.73s（test_mirror_parity_suite + test_expression_compatibility + test_expression_gate_wiring 三文件合并跑）
EXIT=1
```

判读：红因是「源已改、镜像未投影」，不是映射或引擎缺陷；T024 是 T026 全量回归的显式前置（tasks § Dependencies）。
同批唯一的另一处新红（`test_stage_skip_claims_only_appear_as_rejection`）已于本阶段修掉：owner 说明句改用 `不构成…` 的否定形态（与 069a 的 `NEGATION_MARKERS` 相容），
复跑 `pytest tests/contract/test_expression_compatibility.py -k "not c7_mirrors"` → `15 passed, 1 deselected`。

---

## R4 — T010 红跑：`tests/contract/test_migration_distribution.py`

红跑在**改前 HEAD 的临时 worktree** 上进行（当前工作树尚无本测试文件；worktree 保证红的是提交态 owner，而不是被本阶段改动覆盖后的树）：

```
$ git worktree add --detach ~/tmp/069b-redtree HEAD
$ cp tests/contract/test_migration_distribution.py ~/tmp/069b-redtree/tests/contract/
$ cd ~/tmp/069b-redtree && /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/contract/test_migration_distribution.py -q -p no:cacheprovider
```

真实输出（5 条失败的代表行）：

```
E   AssertionError: the owner must not keep a '069b 承接' handoff pointer once 069b has landed;
                    point at the landed mapping / boundary / gate owners instead
E   AssertionError: the literal registry (§ opening block) must declare the parent spec as the
                    semantic owner with the 069a/069b tables as projections;
                    missing ['父规格', '语义 owner', '同源投影']
E   AssertionError: § 所有权 must state that a project MAY record the class in its own knowledge
                    space while the framework never reads it; missing ['自己的知识空间', '不读取']
E   AssertionError: the owner must point at the landed mixed-oracle contract
                    (contracts/ledger-reconciler.md) instead of the 069b handoff
E   AssertionError: notes/quickstart-run.md must carry § 场景 6 (migration & distribution)
FAILED ...::test_owner_drops_every_069b_handoff_pointer
FAILED ...::test_owner_literal_registry_names_the_parent_spec_as_semantic_owner
FAILED ...::test_owner_ownership_section_never_reads_a_project_record
FAILED ...::test_mixed_oracle_rows_point_at_the_landed_contract
FAILED ...::test_quickstart_records_name_level_snapshot_outcomes
5 failed, 11 passed in 0.18s
EXIT=1
```

红形态判读：5 条红全部是「owner 仍保留交接指针 / 字面量登记处未收敛 / § 所有权未收敛 / 台账未指向已落盘条款 /
场景 6 未落盘」——**不是** import 或 collection error；测试文件本身可被收集（16 条用例全部执行）。
另外 11 条（零调用点、冻结文件名集合、四类载荷、零项目侧存储、样本字段）在改前即以绿通过，
因为它们断言的是「不应出现 / 应保持」的形态，绿本身不构成实现已存在。

worktree 在取证后移除（`git worktree remove --force`），不修改主工作树。

---

## G5 — T013 转绿：US2 定向套件

T011（owner 指针收敛）与 T012（三快照 + 场景 6 落盘）完成后，重跑与 R4 相同的测试文件（主工作树）：

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/contract/test_migration_distribution.py -q -p no:cacheprovider

................                                                         [100%]
16 passed in 0.33s
EXIT=0
```

判读：R4 的 5 条红全部转绿，其余 11 条保持绿；零 skip、零 xfail。
场景 6 的真实输出（未刷新零调用点、四类载荷、三快照 `comm -13`）见 `notes/quickstart-run.md` § 6。

---

## R5 — T014 红跑：`tests/contract/test_ledger_reconciliation.py`

**HEAD at red run**: `7be06a08`（2026-10-25，工作树含本文件；引擎为 069a 交付态）。

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/contract/test_ledger_reconciliation.py -q -p no:cacheprovider
```

真实输出（代表行）：

```
E   AssertionError: § 逐流程台账 MUST declare `**台账版本**: <int>（<YYYY-MM-DD>）` exactly once (C-5); found 0: []
E   AssertionError: check JSON must carry a `coverage` block (contract C-2); got None
E   AssertionError: check JSON must carry `red_kind` (C-3); keys=['action', 'checked_at', 'error', 'findings', 'inventory', 'repo', 'units']
E   AssertionError: zero parsed rows over a non-empty inventory MUST report `ledger-truncated` (C-1); got ['missing', … ×78]
E   AssertionError: basis=mixed-oracle + flow_class=expression MUST be `mixed-oracle-class` (C-7); got []
E   AssertionError: a missing `**台账版本**` declaration MUST be `ledger-version-missing` (C-5); got []
E   AssertionError: a duplicated declaration MUST reuse `row-malformed` (C-5); got []
E   AssertionError: text output MUST print `matched` beside the empty set (C-2); got 'flow-class check: 78 unit(s) scanned, 0 finding(s)\n'
E   AssertionError: check on a payload root MUST exit 2 (C-14); got 1 (findings=[unknown ×4, inventory-truncated ×2])

21 failed, 1 passed in 1.81s
EXIT=1
```

红形态判读：21 条红全部是「字段 / 声明 / 动作缺失」——`coverage` 块、`red_kind`、
`ledger-truncated` / `ledger-version-missing` / `mixed-oracle-class` 三个新 kind、§ 逐流程台账 内的
`**台账版本**` 声明、文本面的伴生量、payload-root 具名状态，069a 引擎与 owner 都没有。
零 collection error（78 条中的 22 条被收集并执行）。唯一在红跑即绿的是
`test_mixed_oracle_execution_row_is_accepted`：它断言「合法行不得误报」，实现前后都必须绿，
绿本身不构成实现已存在。

---

## R6 — T015 红跑：`tests/contract/test_delegation_classes.py`

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/contract/test_delegation_classes.py -q -p no:cacheprovider
```

真实输出（代表行）：

```
E   AssertionError: delegation on the real tree must be green; findings=None stderr="usage: flow-class-check.py [-h] --action {check,lookup,isomorphism}
    … flow-class-check.py: error: argument --action: invalid choice: 'delegation' (choose from 'check', 'lookup', 'isomorphism')"
E   AssertionError: a command delegating to the opposite class must exit 1; findings=None
E   AssertionError: a class-neutral edge must stay green even across classes (C-8); findings=None
E   AssertionError: a skill absent from the ledger must be `delegation-unknown-skill` (C-8); got []
E   AssertionError: a ≥3-row command→skill table outside the templates must be `delegation-hand-list` (C-9)
E   AssertionError: same-template same-skill MUST de-duplicate (C-8); got []

10 failed, 2 passed in 0.93s
EXIT=1
```

红形态判读：`--action delegation` 不在 argparse 的 `choices` 内 → 退出码 2、零 stdout；
其余断言随后在「无动作」上失败。这是「动作缺失」，不是 import / collection error。
红跑即绿的两条是「不应出现」类断言：`test_placeholder_skill_paths_are_not_edges`（占位路径
`skills/<name>/SKILL.md` 不能被 C-8 语法的名字类匹配）与 `test_delegation_is_read_only`
（动作缺失时天然零写入），不构成实现已存在。

---

## R7 — T016 红跑：`tests/contract/test_expression_faces.py`

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/contract/test_expression_faces.py -q -p no:cacheprovider
```

真实输出（代表行）：

```
E   AssertionError: faces on the real tree must exit 0; findings=None stderr="usage: flow-class-check.py [-h] --action {check,lookup,isomorphism}
    … flow-class-check.py: error: argument --action: invalid choice: 'faces' (choose from 'check', 'lookup', 'isomorphism')"
E   AssertionError: a well-formed six-row fixture must exit 0; findings=None
E   AssertionError: a five-row face table must exit 1
E   AssertionError: a repeated face id MUST be `faces-duplicate` (C-11); got []
E   AssertionError: a nonexistent pointer path MUST be `faces-unresolvable` (C-11); got []
E   AssertionError: a ≥3-row face/path table outside § 六面 MUST be `faces-second-table` (C-12); got []

9 failed, 5 passed in 1.15s
EXIT=1
```

红形态判读：`--action faces` 同为「动作缺失」（argparse 退出 2、零 stdout）。红跑即绿的五条
断言的是**当前已成立的不变量**：§ 六面 恰好 6 行 / face id 唯一 / 每行一个 owner_pointer 格、
9 条真实指针路径与锚可解析、`doc-consistency-check.py --faces duplicate` 在封闭主体集上
`findings = []`、S3 比较集为 9 条 owner 路径且不含分类 owner、以及 read-only。
它们必须保持绿，红跑绿不构成 `--action faces` 已存在。

---

## R8 — T017 红跑：`tests/contract/test_measurement_instruments.py`

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/contract/test_measurement_instruments.py -q -p no:cacheprovider
```

真实输出：

```
E   AssertionError: C-3 freezes the gate_calls filter set as the closed six-unit list; the record never names
    ['skill:create-checklist', 'skill:analyze-artifacts', 'skill:review-sdd-process'] — a re-measurement at
    wrap-up would have to re-pick the set
    assert not ['skill:create-checklist', 'skill:analyze-artifacts', 'skill:review-sdd-process']

1 failed, 12 passed in 0.37s
EXIT=1
```

红形态判读：本文件的红是**记录内容缺失**——`notes/expression-baseline.md` 只写了「6 个检查类单元」，
没有把 C-3 的封闭单元 id 列表落到冻结点，收尾复测将不得不重新回选集合。其余 12 条实测通过：
七字段齐备、两个 `confirmations` 分项、三项共用 `f0df3d0b`、`verdict` 两值、不可计部分已声明、
四个通道命令实跑 exit 0、SC 词表五值、单一基线记录、记录内引用的脚本都在盘。红跑绿的是
「必须保持」的事实，不是 T022 已完成。

---

## R9 — T018 红跑：`tests/unit/test_reconciler_extensions.py`

```
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
    tests/unit/test_reconciler_extensions.py -q -p no:cacheprovider
```

真实输出（代表行）：

```
E   AssertionError: check JSON must carry `coverage` (C-2); got None
E   AssertionError: check JSON must carry `red_kind` (C-3); keys=['action', 'checked_at', 'error', 'findings', 'inventory', 'repo', 'units']
E   AssertionError: LEDGER_FLOOR MUST be ⌊(27 + 51) / 2⌋ = 39 (C-1); got None
E   AssertionError: 38 parsed rows are below the floor of 39; got ['missing', … ×40]
E   AssertionError: usage: flow-class-check.py … argument --action: invalid choice: 'delegation'
E   AssertionError: usage: flow-class-check.py … argument --action: invalid choice: 'faces'

17 failed in 1.48s
EXIT=1
```

红形态判读：17 条红全部落在「字段 / 动作缺失」——`coverage` / `red_kind` / `LEDGER_FLOOR`
在 069a 引擎里不存在，`delegation` / `faces` 两个动作不在 argparse 的 `choices` 内。
零 collection error（17 条全部被收集并执行）。本文件不复述 T014–T016 的整仓断言，
只钉边界（38 / 39 / 40、100 行台账不动 floor、四条件与 `clean` 的必要非充分关系、
语法与去重、`+` 绑定与 `§` 锚）——这些边界同样必须在 T019–T021 落地后转绿。
