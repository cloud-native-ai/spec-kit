# Quickstart: 决策反题与反指标契约（Decision Tension Record）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**Spec**: [requirements.md](requirements.md) · **Plan**: [plan.md](plan.md)

本文件是**实现期**的操作路径，不是当前可执行的记录。计划阶段两个校验器尚不存在，因此本节
每一个示例都标注了两件事：它依赖的前提（flags、退出码、文件位置、id 形态），以及哪一条契约
测试会在实现期把它钉住。没有这两项标注的示例不得出现在本文件里——一份「看起来能跑」的示例
比没有示例更糟。

统一的执行位点是仓库根目录，`python3` 指仓库可用的解释器（`.venv/bin/python`，或经
`SPECKIT_PYTHON` 指定的等价环境）。

---

## S1 — 写下第一条张力记录并校验

**前提**：`templates/plan-template.md` 已含 `## Decision Tensions`（实现期落地）；目标计划含
一条承重决策；`requirements.md` 的 § Measurement Sources 已有至少一条 `**SC-NNN Source**` 条目。
**钉住者**：`tests/contract/test_decision_tension_validator.py::test_cli_contract_and_exit_codes`。
**状态**：plan 阶段未执行（校验器尚未实现）。

```bash
# 在目标计划里按 owner 形态写一条记录，然后跑结构校验：
python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/076-decision-tension-contract
# 期望：status: ok，六项标签各 pass，退出码 0
```

记录形态（字段名逐字，`tension_id` 由子节标题承载）：

```markdown
### T-001 — <一句话标题>

- **decision**: <被选中的一极>
- **antithesis**: <可独立采纳的具名方案；含「在什么条件下它更优」>
- **binding_constraints**:
  - pole_a: <这一极不可让渡的约束>
  - pole_b: <反题一极不可让渡的约束>
- **discriminating_evidence**: <一位复核者可执行、结果二值的观测>
- **expected_sacrifice**: SC-001 Source ↓ <阈值或说明>
- **revision_trigger**: <指标恶化到什么程度 / 出现什么证据 → 重开>
```

## S2 — 五个反向输入逐个变红

**前提**：同 S1 的合规计划；每次只改一处，其余保持合规。
**钉住者**：`tests/contract/test_decision_tension_validator.py::test_inverse_samples_turn_red`。
**状态**：plan 阶段未执行。

| 变更 | 期望退出码 | 期望命中的标签 |
|------|-----------|----------------|
| 删去任一字段 | 1 | `dtr-record-incomplete` |
| `expected_sacrifice: none` | 1 | `dtr-rejected-form`（仅此一条，不叠加 unmapped） |
| 写入「要平衡 / 综合考虑」类措辞 | 1 | `dtr-rejected-form` |
| 复制一条记录的 `tension_id` | 1 | `dtr-tension-id` |
| 指向不存在的 `SC-NNN` | 1 | `expected-sacrifice-unmapped` |

```bash
python3 scripts/python/validate-decision-tensions.py --spec <fixture-dir> --json
# 期望：checks 数组里对应标签 count>=1，退出码 1
```

## S3 — 分析阶段拦住三类缺陷

**前提**：四个夹具计划（合规 / 缺章节 / 六字段不全 / 代价不可映射）；`/speckit.analyze` 的
`REQUIREMENTS_DIR` 指向夹具目录。
**钉住者**：`tests/contract/test_decision_tension_contract.py::test_three_defect_classes_fail_closed_no_advisory`。
**状态**：plan 阶段未执行（通道与夹具均未落地）。

| 夹具 | 期望 HIGH 计数 |
|------|----------------|
| 合规计划（记录齐备、代价可解析） | 0 |
| 整份计划无 `## Decision Tensions` | 1（不得跳过） |
| 一条记录缺 `revision_trigger` 或单极约束 | 1 |
| `expected_sacrifice` 指向不存在的来源 | 1 |

```
/speckit.analyze
```

判读只看报告里的严重度列与条目计数，不读正文。

## S4 — 证伪四元组的接收与六类拒收

**前提**：载荷是 Markdown 文件，含四个字面键各一次；`observation` 值以 `raw:` 起头；
`would_go_red_if` 同时给出反引号包裹的输入与具名红色信号。
**钉住者**：`tests/contract/test_falsification_quartet_validator.py`。
**状态**：plan 阶段未执行。

```bash
python3 scripts/python/validate-falsification-quartet.py <payload.md>
# 期望：退出码 0（合规载荷）/ 1（六类不合格）/ 2（载荷不可读，按拒收处置）
```

| 载荷 | 期望原因 |
|------|----------|
| 缺任一字段 | `missing-field` |
| 字段存在但值为空 | `empty-field` |
| `exit_code: ok` | `exit-code-not-integer` |
| `observation` 无 `raw:` 前缀 | `observation-not-raw` |
| `would_go_red_if: 若实现有误就会失败` | `tautology` |
| 载荷不可读 | `input-unreadable`（退出码 2） |

## S5 — 镜像与术语

**前提**：改动已落框架源，镜像经 `sync-mirrors.py` 同步；术语检查面是 `shared/`、`templates/`、`skills/` 三棵树。
**钉住者**：`tests/contract/test_decision_tension_contract.py::test_mirror_pairs_and_new_drift_only` 与
`::test_internal_aliases_zero_in_distribution_trees`。
**状态**：本节的镜像基线已在 plan 阶段实测（见 `test-evidence/sync-mirrors-check.txt`），术语计数在实现后复测。

```bash
python3 scripts/python/sync-mirrors.py --check
python3 scripts/python/regen-command-copies.py --check
```

判据是「相对改动前基线无新增漂移」，不是「退出码 0」：命令在改动前已为 0，改动后仍须为 0，
但把 0 当作绝对判据会被无关面的既有漂移拉红。

---

## 失败时怎么读

- 校验器返回 2：先看入参是否指向 spec 目录、两份工件是否都存在且可解码——它不是「记录不成立」。
- `dtr-anchor` 单独变红：先看三行标题是否相邻，不要先改记录内容。
- `expected-sacrifice-unmapped` 与 `dtr-rejected-form` 同时出现于同一记录：这是一个实现缺陷
  （去重规则要求只报前者之一），不是作者的错。
