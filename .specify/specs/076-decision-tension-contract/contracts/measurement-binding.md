# Contract: 预期代价到测量来源（measurement-binding）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**FR 覆盖**: FR-010
**载体**: `shared/guidelines/decision-tension.md`（判据）、`scripts/python/validate-decision-tensions.py`（解析）、`requirements.md` § Measurement Sources（解析目标）

本契约钉住「代价可测量」这一条的唯一落点。它同时是两个失败模式的关闭：代价写成 `none`
（不承认取舍）与代价写成散文（人读得出、机器读不出）。

## 条款

- **C-1** (closed reference form): the record's `expected_sacrifice` MUST use the closed form `<SC-NNN> Source <↓|↑>` — the identifier, one space, the literal `Source`, then the mandatory worsening-direction token `↓` or `↑` — with any threshold or explanation free-form after the direction; a missing direction token or a token outside the two-value set MUST be judged unparseable; the direction token MUST be declared a **record-level assertion**: the checker only requires it to fall inside the two-value set and MUST NOT assert that the direction matches the source metric's real semantics, which is a reviewer judgement, so the value carries no metric name and no direction binding is added. (FR-010)
- **C-2** (single target, single value): `SC-NNN` MUST resolve to an entry beginning `**SC-NNN Source**` inside the same feature's `### Measurement Sources & Collection Methods` section, and one record MUST bind exactly one source — a value containing a second `SC-NNN` MUST fail parsing, because a multi-source 「cost」 has no single value and SC-001's one-record-one-source counting becomes impossible. (FR-010)
- **C-3** (no manual fallback, two remedies): when the value cannot be mapped the verdict MUST come from the deterministic validator rather than from a human reading, and the plan MUST record which of two remedies was taken — add the missing measurement source through the clarification or scope-change path, or demote the decision to an ordinary trade-off and withdraw the record. (FR-010)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-1 | FR-010 | test_sacrifice_grammar_closed_and_direction_mandatory |
| C-2 | FR-010 | test_sacrifice_single_source_and_resolves |
| C-3 | FR-010 | test_unmapped_is_a_verdict_not_a_reading |

## FR 覆盖核对

- FR-010 由本文件 C-1…C-3 承接；解析器的输出面与退出码见 `validator.md`。
- 解析目标（`**SC-NNN Source**` 行）的 owner 是该特性的 `requirements.md`，本契约不复写其条目清单。
