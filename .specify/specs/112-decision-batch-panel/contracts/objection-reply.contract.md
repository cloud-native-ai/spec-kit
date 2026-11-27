# Contract: 异议与应答（objection-reply）

**Feature**: 112-decision-batch-panel → Feature 112 Batch Decision Panel（批量决策面板）
**FR 覆盖**: FR-024（资格面）, FR-026…FR-031
**载体**: `shared/definitions/decision-definitions.md`（批次处置契约）；消费面 = 技能交互、引擎 `record` 的应答校验与批次记录。

本契约规定「什么算一次应答、异议如何绑定与校验、沉默何时等于接受、哪些处置存在」。人是否已回答是技能侧的行为判断并逐字留痕；机器只判结构与成员集合。

## 条款

- **C-401** (reply definition): a reply MUST be an explicit response to this presentation — `无异议`, named objections, or parks; a follow-up question about the content MUST NOT count as a reply (the skill answers and keeps waiting); an aborted session and a follow-up-only conversation MUST produce zero records. (FR-027, A-25)
- **C-402** (binding by identity, verbatim preserved): every objection MUST bind to an item by its identity (subject, plus locator for the same-name family), never by position or order; the batch record MUST preserve the user's reply verbatim in a blockquote while the 107 `rationale` carries key points only. (FR-026, FR-032, A-25)
- **C-403** (member validation before any write): an alternative MUST name a full label that is a member of the presented option set; a new option is legal only when the item declares an `other` option with a `path`, and otherwise the reply MUST be refused with the path rule; an unknown identity, a duplicate entry or a non-member label MUST be refused with a named error; all reply validation MUST complete before any write. (FR-026)
- **C-404** (silence acceptance conjunction): an unmentioned item MUST be settled `accepted-default` only when it is `eligible` — class `human-interactive`, block complete, exactly one default, default reversible, no source conflict, no prior-decision conflict, not previously resolved — inside a completed interactive batch whose reply exists. (FR-024, FR-027)
- **C-405** (disposition closure): dispositions MUST be exactly `accepted-default`, `objected-alternative`, `objected-parked`; a park MUST NOT produce a decision record, the item MUST stay pending, and the batch record MUST carry the park row; the next batch MUST present the item again. (FR-028)
- **C-406** (authorization declared, unattended refuses): the interaction authorization level MUST be declared explicitly by the caller and passed to `record`; a missing level MUST be treated as unattended; an unattended call MAY scan read-only but MUST be refused at record with a named reason; the mechanism MUST NOT infer authorization from terminal shape, environment or silence. (FR-040, A-24)
- **C-407** (explicit settlement of ineligible items): an alternative for a `no-default`, `irreversible-default`, `source-conflict` or `prior-decision-conflict` item MUST be accepted and recorded as `objected-alternative` while the qualification state and reasons stay in the batch row; for an `incomplete` item the alternative MUST be accepted only when the presented option set is grammatically complete and `subject`/`context` resolve — otherwise the engine MUST refuse with a named reason because the resulting record would fail the 107 grammar. (FR-033, edge case)
- **C-408** (no second signal vocabulary): the human choice signal MUST be the owner-declared mapping of the disposition (`accepted-default`→`approved-as-is`, `objected-alternative`→`modified`), reaching `shared/guidelines/confirmation-gates.md` by pointer; `objected-parked` MUST emit no choice signal; no other signal vocabulary is introduced. (FR-030)
- **C-409** (no unhandled settlement, no standing defaults): the panel MUST NOT settle any item the user did not dispose of except by C-404; it MUST NOT infer acceptance from the absence of a user turn, and MUST NOT pre-authorize defaults across batches or remember preferences. (FR-031, A-9)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-401 | FR-027 | `test_decision_batch_engine.py::test_reply_forms_and_abort_zero_records` |
| C-402 | FR-026, FR-032 | `test_decision_batch_engine.py::test_objection_binds_identity_verbatim` |
| C-403 | FR-026 | `test_decision_batch_engine.py::test_reply_membership_refusals` |
| C-404 | FR-024, FR-027 | `test_decision_batch_engine.py::test_silence_eligibility_matrix` |
| C-405 | FR-028 | `test_decision_batch_engine.py::test_park_no_record_stays_pending` |
| C-406 | FR-040 | `test_decision_batch_engine.py::test_unattended_and_missing_authorization_refused` |
| C-407 | FR-033 | `test_decision_batch_engine.py::test_ineligible_explicit_settlement` |
| C-408 | FR-030 | `test_decision_batch_contract.py::test_signal_mapping_pointer_only` |
| C-409 | FR-031 | `test_decision_batch_engine.py::test_no_cross_batch_preauthorization` |

## 守卫义务

- M-14 owns C-403…C-406/C-409 (membership, silence eligibility, authorization, zero-write refusals) with reverse samples; C-401's "is this a reply" judgement is behaviour-class, preserved verbatim but not machine-judged beyond structure.
- The eligibility matrix fixture MUST contain at least one reversible-default and one irreversible-default item and assert that a zero-objection reply settles only the eligible ones.