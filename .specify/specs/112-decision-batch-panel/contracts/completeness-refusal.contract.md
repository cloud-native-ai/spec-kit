# Contract: 完备性与拒绝（completeness-refusal）

**Feature**: 112-decision-batch-panel → Feature 112 Batch Decision Panel（批量决策面板）
**FR 覆盖**: FR-015…FR-018, FR-039（引擎面与退出语义）
**载体**: `shared/definitions/decision-definitions.md`（完备性与拒绝规则）；消费面 = 引擎 `scan`/`record`/`replay` 的记账与退出码、批次记录头。

本契约规定「批次凭什么自称完备、什么情况整批拒绝、空集与缺席如何明说、引擎的接口面是什么」。完备性是封闭清单断言（判据 owner：`shared/guidelines/closed-set-claims.md`，按指针），不是观感。

## 条款

- **C-601** (completeness is a closed-set claim): completeness MUST be expressed as a closed-set claim whose referent is this scan, whose comparison unit is the per-candidate classification, and whose allowed delta is unconditionally empty; it MUST carry the owner's required elements by pointer and MUST NOT use undefined aggregation words as the comparison unit. (FR-015)
- **C-602** (bookkeeping identity): the batch MUST account each candidate exactly once and MUST satisfy `candidates = presented rows + merged references + named exclusions`, with per-source candidate counts and the absent-source list; the batch record head MUST carry that bookkeeping and the verdict. (FR-015, FR-032)
- **C-603** (carrier-level refusal): a present-but-unreadable or unparseable or unenumerable source MUST refuse the whole batch — no presentation, no record, no disposition, a named source and a documented exit code; the engine MUST NOT present a partial batch or label it complete. (FR-016)
- **C-604** (absent is named, not clean): an absent carrier (file or directory missing) MUST be recorded as a named empty source with a reason; it MUST NOT refuse the batch and MUST NOT be read as a clean full scan; the verdict MUST disclose the absence. (FR-017)
- **C-605** (nothing-pending): zero candidates MUST produce an explicit `nothing-pending` success result and MUST NOT create a batch record or present an empty shell. (FR-018)
- **C-606** (no silent drop): a candidate that can be neither presented nor named-excluded MUST be a refusal, never a silent omission. (FR-016, FR-018)
- **C-607** (no partial completeness claim): a batch that missed any candidate MUST NOT be labelled complete; the refusal path is the only alternative to a complete batch. (FR-016)
- **C-608** (engine surface and exit semantics): the engine MUST expose exactly the closed actions `scan`, `record`, `replay`; `scan` and `replay` MUST be read-only and `record` MUST be the only writer; it MUST answer `-h`/`--help`/`--version` before any action, MUST reject undeclared options non-zero, and MUST document its exit codes — `0` success (including `nothing-pending`), `1` a documented refusal, `2` usage or environment error — in its help and in `docs/reference/commands/decide.md`, following `shared/definitions/script-interface-definitions.md` by pointer. (FR-039)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-601 | FR-015 | `test_decision_batch_engine.py::test_completeness_claim_shape` |
| C-602 | FR-015, FR-032 | `test_decision_batch_engine.py::test_bookkeeping_identity_holds` |
| C-603 | FR-016 | `test_decision_batch_engine.py::test_unreadable_source_refusal` |
| C-604 | FR-017 | `test_decision_batch_engine.py::test_absent_source_named_not_clean` |
| C-605 | FR-018 | `test_decision_batch_engine.py::test_nothing_pending_success_no_record` |
| C-606 | FR-016, FR-018 | `test_decision_batch_engine.py::test_unclassifiable_candidate_refused` |
| C-607 | FR-016 | `test_decision_batch_engine.py::test_no_partial_complete_claim` |
| C-608 | FR-039 | `test_decision_batch_contract.py::test_engine_interface_contract` |

## 守卫义务

- M-12 owns C-601/C-602/C-605/C-607 (bookkeeping and claim shape); C-603/C-604/C-606 are engine refusal tests with reverse samples; C-608 is the script-interface guard (`--help`/`--version`/undeclared option).
- The refusal exit codes are part of the engine's `--help` output, and the command doc MUST match them — the guard compares the two faces.