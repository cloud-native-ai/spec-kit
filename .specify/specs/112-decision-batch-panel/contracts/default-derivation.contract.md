# Contract: 建议默认值与依据（default-derivation）

**Feature**: 112-decision-batch-panel → Feature 112 Batch Decision Panel（批量决策面板）
**FR 覆盖**: FR-021…FR-024（默认值与冲突面）, FR-039（引擎判定）
**载体**: `shared/definitions/decision-definitions.md`（建议默认值与接地面）；消费面 = 引擎 `scan` 的接地联接与守卫。

本契约规定「建议默认值从哪里来、接地如何判定、无证据怎么说、前例冲突如何呈现」。建议是否合理是行为类（B-09），机器只判联接的确定性与指针可解析性。

## 条款

- **C-301** (default is declared, never invented): the recommended default MUST be the single member of the option set carrying `default: yes`; the panel MUST NOT invent a default label, an option or an option's consequence, reversibility or evidence. (FR-021)
- **C-302** (no-default is presentable, not settleable): an option set with zero or more than one default marker MUST be presented as `no-default` with the cardinality defect named, and MUST NOT be settled by silence. (FR-021, FR-024)
- **C-303** (grounding join, closed inputs): grounding MUST be computed as a deterministic join over exactly: (a) the default option's `evidence` pointers that resolve to a prior-experience carrier; (b) prior decision records whose `context` contains the subject string verbatim; (c) the `T-NNN` identifiers those records cite. Prior-experience carriers are closed: decision-record carriers under the four scan roots, batch records in the knowledge store, `T-NNN` tension records, `.specify/history/` entries, `.specify/feedback/` entries and `.specify/knowledge/` entries. (FR-022, A-6)
- **C-304** (grounded means resolvable): `grounded` MUST carry at least one resolvable prior-experience pointer and every emitted pointer MUST resolve (path exists; when an anchor is given, the anchor is findable); `basis` MUST NOT be counted as evidence. (FR-022)
- **C-305** (no-evidence is explicit): with no resolvable prior-experience pointer the row MUST read `no-evidence`; the presentation MUST NOT imply evidential support for the recommendation. (FR-022)
- **C-306** (prior-decision conflict): when a prior decision record's `context` contains the subject full name verbatim and its chosen option differs from the current recommended default, the row MUST be presented `prior-decision-conflict` with the prior record pointer and its chosen label, and MUST NOT be settled by silence. (FR-023)
- **C-307** (engine judges, not the model): the join, pointer resolution and conflict detection MUST be computed by the deterministic engine; the skill MUST NOT perform semantic retrieval, infer additional evidence, or override a judged status at presentation time. (FR-039, A-6 program-first)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-301 | FR-021 | `test_decision_batch_engine.py::test_default_is_declared_member` |
| C-302 | FR-021, FR-024 | `test_decision_batch_engine.py::test_no_default_presented_not_settled` |
| C-303 | FR-022 | `test_decision_batch_engine.py::test_grounding_join_closed_inputs` |
| C-304 | FR-022 | `test_decision_batch_engine.py::test_grounded_pointers_all_resolve` |
| C-305 | FR-022 | `test_decision_batch_engine.py::test_no_evidence_explicit` |
| C-306 | FR-023 | `test_decision_batch_engine.py::test_prior_conflict_detected` |
| C-307 | FR-039 | `test_decision_batch_contract.py::test_skill_does_not_recompute` |

## 守卫义务

- M-13 owns C-301…C-306 with two grounding fixtures (one grounded, one `no-evidence`) and one prior-conflict fixture; the pointer resolver is the same reading used by the decision checker's evidence rule (M-09).
- Whether the recommendation is substantively reasonable remains B-09; no guard claims it.