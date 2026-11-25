# Contract: 归档与审计（archive-and-audit）

**Feature**: 107-decision-governance → Feature 107 Decision Governance（AI Agent 决策项治理）
**FR 覆盖**: FR-014…FR-017
**载体**: `shared/definitions/decision-definitions.md`（记录形态与字段闭集）；载体保留各自格式与 owner；`.specify/register.md` 是编号唯一索引。

本契约规定「决策如何被归档、如何只凭档案被重建」。档案是既有载体的投影，不是新存储；可重建性是审计的判据。

## 条款

- **C-201** (record serialization grammar): a decision record MUST be carried by a level-3 heading `### D-NNN — <one-line title>` with the id appearing exactly once; each field MUST be one line `- **<lowercase-field>**: <value>`; option entries MUST be indented sub-lines under `options` with the five elements in one line each; a continued value MUST indent ≥2 spaces; lines inside fenced code blocks do not count. (FR-014)
- **C-202** (field closure and timestamps): every record MUST carry FR-014's ten mandatory fields; the conditional fields `same_name_conflict` + `resource_locator` are required exactly when C-103's trigger holds, and `superseded_by` exactly when superseded; `created_at` MUST carry an ISO-8601 UTC value and `dispatched_at` / `acknowledged_at` / `implemented_at` MUST each be present with an ISO-8601 UTC value or the literal `not-yet`; field names MUST be the owner page's names — production surfaces MUST NOT rename them. (FR-014)
- **C-203** (identifier, density and register): `decision_id` MUST match `D-NNN` (three digits), be dense and unique inside one carrier, never reused; a cross-carrier reference MUST carry the carrier pointer; every id MUST be registered in `.specify/register.md` at birth, either per record or as a `<carrier> + range` grouped row; a superseded id MUST remain and carry `superseded_by`, never deleted or reused. (FR-015)
- **C-204** (resolvability and reconstructability): every evidence pointer MUST resolve — pointer resolvability is judged by M-09; a decision MUST be reconstructable from the existing carriers + register alone — a missing field, a broken pointer or a missing record is a defect, and conversation memory MUST NOT be used to backfill any of it. (FR-016)
- **C-205** (load-bearing cross-reference only): a load-bearing decision MUST also satisfy `shared/guidelines/decision-tension.md`'s six fields and its record MUST cross-reference the corresponding `T-NNN`; the record MUST NOT copy `antithesis` / `binding_constraints` / `discriminating_evidence` / `expected_sacrifice` / `revision_trigger` content. (FR-017)
- **C-206** (legacy read-only): the new form is defined precisely — a level-3 heading matching `^### D-\d{3}` **whose block carries the C-201 record field grammar**; the id shape alone never makes a record new-form (register row `D-001` matches `D-\d{3}` yet predates this contract and is legacy). Records created before this contract lands — pre-existing `### D-…` headings without the field grammar (measured 39 one- and two-digit headings in `.specify/specs`, and zero three-digit record-form headings at base) and register rows that are not the birth registration of a new-form record (`D1–D9`, `D-A`, `D-B`, `D-001`, `D-001-a`, `D1 (092)`, `D-098-01`, `D-102-01`…) — MUST be reported as `legacy`, remain readable and MUST NOT be judged as invalid or rewritten. (FR-028)
- **C-207** (archive-as-projection, no second store): the archive MUST be the union of the closed producer inventory × existing carriers plus the register index; a producer without a carrier MUST go through inventory revision and MUST NOT silently drop the record; no second registry, queue, store or scheduler is permitted. (FR-004, A-3)
- **C-208** (read-only dispositions): a read-only command's disposition MUST be written into that command's own report carrier and MUST NOT be archived by modifying the analyzed artifact. (FR-003 edge case)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-201 | FR-014 | `test_decision_governance_contracts.py::test_record_line_grammar` |
| C-202 | FR-014 | `test_validate_decisions.py::test_m01_field_closure_reverse_samples` |
| C-203 | FR-015 | `test_validate_decisions.py::test_m04_id_density_register` |
| C-204 | FR-016 | `test_decision_governance_guards.py::test_broken_pointer_red` |
| C-205 | FR-017 | `test_decision_governance_guards.py::test_no_tension_field_copy` |
| C-206 | FR-028 | `test_decision_governance_guards.py::test_legacy_two_digit_reported_legacy` |
| C-207 | FR-004 | `test_decision_governance_contracts.py::test_no_second_store` |
| C-208 | FR-003 | `test_decision_governance_contracts.py::test_read_only_disposition_carrier` |

## FR 覆盖核对

- FR-014…FR-017 由本文件 C-201…C-205 承接；FR-004 由 C-207 承接；legacy 规则由 C-206 承接。
- 字段的取值域逐项归 owner page 与相邻 owner（见 requirements § Decision Record Field Ownership）；本契约只规定形态、在场性与可解析性。
