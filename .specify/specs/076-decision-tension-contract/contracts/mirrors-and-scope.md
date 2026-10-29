# Contract: 机制边界、术语与两顶帽子（mirrors-and-scope）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**FR 覆盖**: FR-018、FR-024、FR-025、FR-026
**载体**: 全特性交付面（无单一文件）

本契约规定「本特性不做什么」与「改动怎么落到镜像」。前者的判据是前后集合差，后者的判据是相对
基线的漂移量：两者都不能靠读一遍正文确认。

## 条款

- **C-1** (scope: additive only): the feature MUST NOT add any `/speckit.*` command, storage, ledger, scheduler, scorer or model call — the record rides on the plan artifact, the quartet rides on the proposal's existing carrier, and the verdicts enter only the existing analyze report and the plan text; the judgement MUST be a before/after set difference over the command inventory, the dependency list and the process list against baseline commit `ac63fe8c`, and the difference MUST land inside the empty set. (FR-018)
- **C-2** (terminology: engineering words only): user-visible prose MUST use engineering terms, and the internal aliases enumerated in `requirements.md` § Assumptions A3 MUST NOT appear in any of the three distribution trees (`shared/`, `templates/`, `skills/`); a contract test MUST assert zero hits there and MUST also assert that the A3 alias list still exists in the spec, so a renamed or emptied list cannot make the zero-hit check vacuously green. (FR-024)
- **C-3** (two hats and the drift criterion): the only editing surface MUST be the framework sources; every affected `.specify/` runtime copy MUST be produced by `sync-mirrors.py`, and the plan MUST list the touched mirror pairs by reusing the owner table in `requirements.md` FR-025 rather than restating it (the table's row count is owned there and MUST NOT be restated here or anywhere else); the per-tool command-copy surface MUST be empty because `templates/commands/**` is untouched, and the acceptance criterion MUST be 「no new drift relative to the pre-edit measurement of `sync-mirrors.py --check`」 rather than a bare exit code, because an absolute pass criterion is unpassable whenever unrelated drift predates this feature. (FR-025)
- **C-4** (closed sets do not regress): both touched closed-set owners — `shared/guidelines/critique-and-self-critique.md` and `skills/internal/analyze-artifacts/references/detection-and-severity.md` — MUST be handled as an only-add containment claim whose baseline referent is commit `ac63fe8c` and whose comparison unit is the paragraph; the allowed delta set MUST be exactly the new paragraphs plus the count lines that the new channel forces to change, everything outside it MUST be byte-identical to the baseline with zero deleted or rewritten lines, and item-level assertions — rejection forms, boundary declarations, consumer-list rows — MUST NOT fall below the baseline counts, compared by the contract test rather than by reading. (FR-026)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-1 | FR-018 | test_scope_additive_only_set_difference |
| C-2 | FR-024 | test_internal_aliases_zero_in_distribution_trees |
| C-3 | FR-025 | test_mirror_pairs_and_new_drift_only |
| C-4 | FR-026 | test_closed_set_only_add_item_counts |

## FR 覆盖核对

- FR-018、FR-024…FR-026 由本文件 C-1…C-4 承接；无镜像面的两处（`docs/decisions/template.md`、
  `tests/**`）在 C-3 的「唯一编辑面」之外另作声明，见 `plan.md` § Mirror Obligations。
- 镜像对的逐行清单 owner 是 `requirements.md` FR-025 的表；本契约只引用它，不复写行内容。
