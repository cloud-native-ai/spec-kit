# Contract: 批次呈现（presentation）

**Feature**: 112-decision-batch-panel → Feature 112 Batch Decision Panel（批量决策面板）
**FR 覆盖**: FR-014, FR-019…FR-021, FR-025, FR-041（呈现面）, FR-045（行为边界）
**载体**: `shared/definitions/decision-definitions.md`（批次呈现契约）；消费面 = 引擎 `scan` 的呈现 payload 与技能的用户面渲染。

本契约规定「一次呈现必须携带什么、按什么顺序、哪些内容不许补造」。可读性判断（是否读得懂）归 B-08 评审面；机器只判槽位在场与结构。

## 条款

- **C-201** (one presentation, deterministic order): one invocation MUST produce one presentation for the whole roster; the order MUST be roster order → carrier repository-relative path → occurrence position (register row order; block start line); per-row source references MUST follow the same order. (FR-014)
- **C-202** (per-item slots): every presented row MUST carry the 107 `human-interactive` template slots (plain-language subject, context, every option's consequences and reversibility, the unique default, full names and locator when applicable, option evidence), plus its source pointers, `decision_class`, `basis`, grounding status and pointers, qualification state and named reasons, and how to object or park this item. An incomplete item MUST show all content it has and the named missing elements; the panel MUST NOT fill a missing slot with an invented value. (FR-019)
- **C-203** (batch-level context floor): the presentation MUST state, for the batch as a whole, why the items appear now, what silence will mean, how to object or park, which items stay pending and why, and the completeness disclosure including absent sources; a reader MUST NOT need another artifact to answer those five questions. (FR-020)
- **C-204** (no internal identifiers in the user-facing body): field names, script names, status tokens and other internal identifiers MUST NOT appear in the user-facing body; the structured payload may carry them. Wording and context MUST follow `shared/guidelines/user-facing-comprehension.md` by pointer. (FR-020)
- **C-205** (no truncation): every presented item MUST be rendered in full; length MUST NOT be capped and summaries MUST NOT replace items — an omission is a refusal, never a shortened batch. (FR-025)
- **C-206** (scan determinism): two scans of the same tree MUST yield the same item set, order and per-field content, differing only in the scan timestamp; the presentation digest MUST be computed over the timestamp-free projection. (FR-014, SC-010)
- **C-207** (zero autonomous presentations): the presented count of `ai-autonomous` items MUST be zero, and the bookkeeping MUST carry a `not-human-held` exclusion per excluded candidate. (FR-011, FR-041)
- **C-208** (readability is behaviour-class): whether the presentation is understandable, whether consequence statements are truthful and whether the recommended reason is sufficient MUST be judged on the named review surfaces (B-03, B-08, B-09), never claimed as machine coverage. (FR-045)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-201 | FR-014 | `test_decision_batch_engine.py::test_presentation_order_deterministic` |
| C-202 | FR-019 | `test_decision_batch_engine.py::test_row_slots_incomplete_named` |
| C-203 | FR-020 | `test_decision_batch_engine.py::test_batch_context_floor` |
| C-204 | FR-020 | `test_decision_batch_contract.py::test_presentation_identifier_boundary` |
| C-205 | FR-025 | `test_decision_batch_engine.py::test_no_truncation_all_rows` |
| C-206 | FR-014, SC-010 | `test_decision_batch_engine.py::test_scan_twice_field_identical` |
| C-207 | FR-011, FR-041 | `test_decision_batch_engine.py::test_autonomous_presented_zero` |
| C-208 | FR-045 | `test_decision_batch_contract.py::test_behavior_surfaces_named` |

## 守卫义务

- M-12 owns C-201/C-205/C-206/C-207 (ordering, row-count identity, determinism, autonomous-presentation zero) with reverse samples; the comprehension judgements (C-208) carry no machine claim.
- The engine's `--format text` rendering and `--format json` payload MUST be projections of the same row set; the guard asserts row-count and identity equality between them.