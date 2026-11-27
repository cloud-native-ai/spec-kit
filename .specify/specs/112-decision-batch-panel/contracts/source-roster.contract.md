# Contract: 待决策项来源与资格（source-roster）

**Feature**: 112-decision-batch-panel → Feature 112 Batch Decision Panel（批量决策面板）
**FR 覆盖**: FR-006…FR-013
**载体**: `shared/definitions/decision-definitions.md`（扩展后的批次面）；消费面 = 引擎扫描、批次呈现、批次记录与守卫。

本契约规定「哪些事项算待决策项、块必须长什么样、重复如何合并、类别如何把关」。候选存在与资格判定分层：候选存在只由机器可检谓词判定，字段齐备、块级文法与类别属于资格或具名排除。行为类问题（名称是否完整、定位是否充分）不在本契约内。

## 条款

- **C-101** (closed two-source roster): pending decision items MUST come from exactly two sources — `register-open-decision-row` (rows in `.specify/register.md` whose de-emphasised id cell starts `OI-` or `D-` and whose de-emphasised status cell starts at the word boundary `open`) and `authored-pending-item` (blocks headed `### PENDING —` outside fenced code under exactly `.specify/specs/`, `.specify/goals/`, `.specify/anchoring/`, `.specify/teams/`); adding or removing a source or scan root MUST be an owner-page revision. (FR-006)
- **C-102** (candidacy ≠ qualification): candidate existence MUST be decided by the machine-checkable predicate alone; missing fields, malformed/unknown/duplicate field lines, declared-count mismatches and class judgement MUST NOT remove a candidate from enumeration — they become qualification states or named exclusions. A block-level defect MUST NOT refuse the batch. (FR-008, A-21)
- **C-103** (pending-item block grammar): a pending item MUST be a `### PENDING — <full subject name>` block whose fields are the closed set `decision_class`, `subject`, `same_name_conflict`, `resource_locator`, `context`, `options`, `basis`, `origin`, `created_at`, `resolution`; `options` MUST follow the 107 option-set contract (declared count, five elements, exactly one default, `other` needs `path`, single viable option declares `forced`); a pending block MUST NOT be judged as a decision record and a record MUST NOT be judged as a pending block. (FR-008)
- **C-104** (identity and dedupe): dedupe identity MUST be the `subject` compared byte-equal after trimming, plus `resource_locator` equality in the same-name family; repeated references MUST merge into one row listing every source; same identity with different option label sets MUST be presented once as `source-conflict` and MUST require an explicit choice; case folding, Unicode normalisation, title similarity and semantic merging MUST NOT be used; a same-spelling subject without a locator MUST NOT be merged with one that carries a locator. (FR-009, A-22)
- **C-105** (register↔block linkage): a register-derived item MUST link to its block only when the block `origin` contains the register row id verbatim as an independent token AND exactly one matching block exists on the explicit repository-relative path named in that row's cell; relative wording (`同上`, `Open items § …`) MUST NOT be parsed as a path; zero or more than one match MUST present the row `incomplete` with `authority-unresolved` / `ambiguous-link`, and an unlinked row MUST keep its own identity (the row id) instead of joining any block identity. (FR-010, A-22)
- **C-106** (class gate): a candidate declaring `ai-autonomous` MUST be excluded as `not-human-held` and MUST NOT be presented, converted or settled; a candidate whose class is unknown (no block, unresolvable authority path, missing `decision_class`, or a value outside the domain) MUST be presented `incomplete` with `class-missing`, MUST NOT be settled and MUST NOT be read as autonomous; a same-identity class disagreement across sources MUST be excluded `not-human-held` with the conflict named in the bookkeeping. (FR-011, A-23)
- **C-107** (already-resolved exclusion): a candidate carrying a `resolution` field, or joined at read time with a settled identity in a prior batch record, MUST be excluded as `already-resolved`; a disagreement between the source state and the settled record MUST be disclosed, never silenced. (FR-012)
- **C-108** (named exclusion families): triggered interactive gates, clarification markers, parked ideas, `ai-autonomous` checkpoint verdicts and `REC-` rows MUST be named exclusions with their reason and counted in the bookkeeping; they MUST NOT be silently dropped and MUST NOT be rewritten as "does not exist". (FR-007)
- **C-109** (source presence, two levels): presence MUST be recorded per source as `read` / `absent` / `unreadable`; a carrier that exists but cannot be read, parsed into its columns, or enumerated MUST trigger the batch refusal (C-603); an absent carrier MUST be a named empty source with a reason; block-level grammar defects MUST NOT be treated as `unreadable`. (FR-016, FR-017)
- **C-110** (scan is read-only): until a reply is recorded, the whole scan path MUST write nothing — no records, no register rows, no source annotations. (FR-013)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-101 | FR-006 | `test_decision_batch_engine.py::test_roster_closed_and_predicates` |
| C-102 | FR-008 | `test_decision_batch_engine.py::test_incomplete_block_still_candidate` |
| C-103 | FR-008 | `test_decision_batch_contract.py::test_block_grammar_owner_extension` |
| C-104 | FR-009 | `test_decision_batch_engine.py::test_identity_byte_equal_and_merge` |
| C-105 | FR-010 | `test_decision_batch_engine.py::test_origin_linkage_states` |
| C-106 | FR-011 | `test_decision_batch_engine.py::test_class_gate_states` |
| C-107 | FR-012 | `test_decision_batch_engine.py::test_already_resolved_read_time_join` |
| C-108 | FR-007 | `test_decision_batch_engine.py::test_named_exclusions_counted` |
| C-109 | FR-016, FR-017 | `test_decision_batch_engine.py::test_source_presence_levels` |
| C-110 | FR-013 | `test_decision_batch_engine.py::test_scan_zero_write` |

## 守卫义务

- M-10 owns C-101/C-102/C-108/C-109 (roster, candidate enumeration, exclusion accounting, presence levels); M-11 owns C-103–C-107 (block grammar, identity/linkage, class gate, resolution join). Both carry a reverse sample in `tests/fixtures/decision-batch/` and join `GUARD_ROSTER` in the same change.
- Name completeness and locator adequacy remain behaviour-class (B-01/B-02) — this contract judges grammar and presence only.