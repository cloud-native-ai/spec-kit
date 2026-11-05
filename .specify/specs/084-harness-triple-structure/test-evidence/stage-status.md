# E3 stage-status — requirements

```yaml
stage: requirements
row_type: stage-status
status: not-run-docs-only
selection_basis: docs-only
changed_paths:
  - .specify/specs/084-harness-triple-structure/requirements.md
  - .specify/specs/084-harness-triple-structure/checklists/requirements.md
  - .specify/specs/084-harness-triple-structure/test-evidence/validate-requirements.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/flow-class-lookup.txt
  - .specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/validate-requirements.txt
```

## Why `not-run-docs-only`

本阶段只生产规格、清单与证据文件，未触及任何可执行面（`scripts/`、`skills/**/scripts/`、
`src/`、`tests/`、`templates/*.yaml` 均未改动）。因此 `targeted-set-v1` 的输入
`changed_paths` 全部落在 `test_roots`（`tests/unit`、`tests/contract`、
`tests/integration`、`tests/scenarios`）之外、且不涉及夹具，选择程序得空集属预期形态，
按 `.specify/skills/external/sdd-loop-driver/references/efficiency-model.md` § 2.3 末条
记 `not-run-docs-only` 而非 `empty-selection-escalated`。运行字段（`selected_paths[]`、
`sufficiency`、`rc`、`passed`/`failed`、`new_failures[]`、比较基线）不适用，MUST NOT
报 `unknown`（同 owner § 2.4 六项缩减字段集）。

## Bases verified (not "green by assumption")

| 判项 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 规格结构 | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/084-harness-triple-structure/requirements.md` | `status: ok`，六判项全 pass，`0 error(s), 0 warning(s)`，exit 0 | `test-evidence/validate-requirements.txt` |
| 类别解析 | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` | `flow_class: execution` / `flow_type: -` / `source: declaration` / exit 0 | `test-evidence/flow-class-lookup.txt` |

**驱动者 U4 复跑（2026-11-05 07:53 UTC；独立于阶段执行者）**：

- `decomposition-check.py --mode plan --requirements .specify/specs/084-harness-triple-structure/requirements.md`
  → `decision=proceed`（`fr_count=19`，上限 30），exit 0。
- `pre-analyze-check.py --spec-dir .specify/specs/084-harness-triple-structure --stage requirements --repo <repo>`
  → 首次运行 exit 2（`requirements.md carries no § Runtime Stack & Dependency Ownership`）；
  驱动者补写该强制节（`execution` 类特性必填，三行：RS-001 CPython / RS-002 pytest / RS-003 `specify init`）后复跑
  → `decision=pass`，`errors=0`，`advisories=12`（全部为 requirements 阶段尚未创建的计划交付路径，属预期），exit 0。
- 修复提交：`fix(084): add the mandatory runtime stack section and refresh the evidence`（独立于阶段提交 `a94c3945`）。
