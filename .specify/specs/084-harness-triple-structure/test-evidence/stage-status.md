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

**未运行项（如实登记，不折算为通过）**：本阶段未运行 `decomposition-check.py`
（该门在本仓属 plan 阶段口径）、未运行 `pre-analyze-check.py --stage requirements`
（其宿主 `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` 由 analyze /
review 阶段调用）。两者留待后续阶段，MUST NOT 被读作已通过。
