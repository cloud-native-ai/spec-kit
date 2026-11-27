# Contract: 记录与重放（record-replay）

**Feature**: 112-decision-batch-panel → Feature 112 Batch Decision Panel（批量决策面板）
**FR 覆盖**: FR-001…FR-005（所有者面）, FR-032…FR-038
**载体**: `shared/definitions/decision-definitions.md`（批次记录契约）；消费面 = 引擎 `record` / `replay`、记忆引擎写入面、register 与来源载体。

本契约规定「一次批次落到哪些既有载体、以什么顺序与前置条件写入、如何只凭记录重放、以及所有权边界」。

## 条款

- **C-501** (record preconditions, zero writes on refusal): `record` MUST re-scan every source and assert the candidate identity set and each disposed item's content fingerprint (subject, option set, default, grounding, qualification, source reference set) equal the presentation and that no candidate was added; any mismatch MUST refuse with the diff, and no batch record, decision record, source update or id registration may be written. (FR-037, A-24)
- **C-502** (batch id, minted late, never reused): the batch id MUST have the shape `B-<YYYYMMDDTHHMMSSZ>-<8 lowercase hex>`, MUST be minted only after every precondition passes and before the first write, and MUST identify exactly one record path; a second record for the same batch id MUST be refused before the write surface runs, and MUST NOT overwrite or upsert. (FR-032, FR-037, A-24)
- **C-503** (batch record carrier and content): the batch record MUST be one dated entry in the existing `.specify/knowledge/` store written through the memory engine, titled `decision-batch-<batch_id>`; its head MUST carry the batch id, scan time, tool version, per-source candidate counts, completeness verdict and the verbatim reply blockquote plus authorization; it MUST carry the item-row table and the decision records; it MUST NOT be a second store or a shared mutable aggregate. (FR-032, A-11)
- **C-504** (decision records and batch-family fields): each settled item MUST produce exactly one 107 decision record in the unchanged grammar and layered closure, placed in the batch record, additionally carrying `batch_id`, `batch_disposition` and `recommendation_grounding` together (batch-produced records only); `rationale` MUST state the basis plus the reply key points, `actor` MUST follow the existing identity shape, `transmission_status` MUST start at `not-transmitted`, and `evidence` MUST contain the grounding pointers, the source item pointer and the batch record pointer. (FR-033, A-12)
- **C-505** (register reflects the batch): the batch id and the decision ids MUST be registered at birth (per carrier + range grouping is legal); each settled register row's status cell MUST be updated to name the batch and decision id and the row MUST NOT be deleted; parked rows MUST stay `open`-prefixed and annotated with the batch; apart from status cells and appended rows the register MUST NOT be rewritten; an absent register MUST be created from the existing header form before registration. (FR-034)
- **C-506** (source updates and failure disclosure): a settled pending block MUST gain the conditional `resolution` field naming batch and decision id without rewriting block content; a source update failure MUST be disclosed, and the read-time join MUST prevent the identity from being presented again. (FR-035)
- **C-507** (idempotency and concurrency): a same-batch-id second write MUST be refused; distinct batch ids MUST write distinct knowledge paths and MUST NOT read or modify each other's records; the register stays the single index and id conflicts are repaired by the existing renumber lane, never silently renumbered. (FR-037, SC-010)
- **C-508** (replay): replay MUST reconstruct the item set, completeness bookkeeping, defaults and grounding, objections and dispositions, and decision records from the batch record plus resolvable pointers alone; it MUST be read-only and deterministic; any unresolvable pointer MUST be reported and the run MUST exit non-zero; nothing may be skipped or completed from conversation memory. (FR-036)
- **C-509** (transmission): a batch decision dispatched for implementation MUST reuse the 107 audit chain (record → dispatch attempt → implementation receipt) and its obligations; the batch MUST NOT generate a second record or a second transmission path. (FR-038)
- **C-510** (redecision and supersession): a redecision MUST add a new record and append `superseded_by` (with the new record's carrier pointer) to each prior record whose chosen option is overturned, keeping the prior content byte-identical; an unreadable or unwritable prior carrier MUST refuse that item's redecision rather than degrade it to a fresh decision. (FR-029, A-7)
- **C-511** (single-owner extension): every batch rule MUST be owned additively by the existing decision-governance owner page — the new vocabulary (eight terms with bilingual form), the batch presentation/grounding/disposition/record/replay/completeness faces, the P-13 producer row and the batch-family conditional layer; every other surface MUST reach the owner page by pointer and MUST NOT restate its criteria tables; no second owner page, registry, store, schema or scheduler is introduced, and `specify init`/mirror distribution is the only path to client projects. (FR-001, FR-002, FR-003, FR-004, FR-042)
- **C-512** (boundaries): the batch MUST NOT align with ai-harness 091 or any external decision-governance capability, MUST NOT access the network, MUST NOT write the feedback store and MUST NOT transmit anything automatically; it MUST NOT present, convert or authorize `ai-autonomous` decisions; and the machine-judged / behaviour-judged split MUST stay honest — structural propositions only are machine-covered. (FR-005, FR-041, FR-044, FR-045)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-501 | FR-037 | `test_decision_batch_engine.py::test_record_drift_refused_zero_write` |
| C-502 | FR-032, FR-037 | `test_decision_batch_engine.py::test_batch_id_shape_and_duplicate_refusal` |
| C-503 | FR-032 | `test_decision_batch_engine.py::test_batch_record_layout_via_memory_engine` |
| C-504 | FR-033 | `test_decision_batch_engine.py::test_decision_record_batch_family` |
| C-505 | FR-034 | `test_decision_batch_engine.py::test_register_registration_and_status_update` |
| C-506 | FR-035 | `test_decision_batch_engine.py::test_resolution_annotation_and_disclosure` |
| C-507 | FR-037, SC-010 | `test_decision_batch_engine.py::test_two_batches_distinct_paths` |
| C-508 | FR-036 | `test_decision_batch_engine.py::test_replay_from_record_only` |
| C-509 | FR-038 | `test_decision_batch_contract.py::test_transmission_reuses_107_chain` |
| C-510 | FR-029 | `test_decision_batch_engine.py::test_supersession_append_only` |
| C-511 | FR-001…FR-004, FR-042 | `test_decision_batch_contract.py::test_owner_extension_single_owner` |
| C-512 | FR-005, FR-041, FR-044, FR-045 | `test_decision_batch_contract.py::test_red_lines_and_boundary` |

## 守卫义务

- M-15 owns C-502…C-507 (batch id, record layout, batch-family fields, register and source updates, idempotency); M-16 owns C-508 (replay determinism and pointer resolution); the owner-extension guards (C-511/C-512) are contract tests over the owner page, the command/skill/docs presence and the zero-network/zero-feedback/zero-transmission assertions.
- `validate-decisions.py` MUST admit the three batch-family fields and judge their trigger/value rules in one recorded rule; existing records MUST keep passing unchanged.