# Contract: 张力结构校验器（validator）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**FR 覆盖**: FR-016、FR-017
**载体**: `scripts/python/validate-decision-tensions.py`（新建）、`.specify/scripts/python/validate-decision-tensions.py`（镜像）

本契约钉住调用面、退出码语义、封闭标签集与输出形态。校验器只输出 verdict，不提改写建议——一旦
它开始提议写法，它就成了第二个 owner，判据与措辞会各自漂移。

## 条款

- **C-1** (invocation and exit codes): the checker MUST be invoked as `python3 scripts/python/validate-decision-tensions.py --spec <spec-dir> [--json]`, MUST read `<spec-dir>/plan.md` and `<spec-dir>/requirements.md`, MUST use a directory rather than a file because the verdict spans two artifacts, and MUST exit 0 for no errors (warnings allowed), 1 for at least one error, and 2 for unreadable input (either file missing, undecodable, or without content lines). (FR-016)
- **C-2** (closed label set, 4 + 2 partition): the check labels MUST be the closed six-item set `dtr-anchor`, `dtr-section-missing`, `dtr-record-incomplete`, `dtr-tension-id`, `dtr-rejected-form`, `expected-sacrifice-unmapped`; the set MUST be described as covering the anchor assertion, the three defect classes and two record-level forms (identifier shape, rejected forms) — a 「4 + 2」 partition, never a one-to-one mapping onto four things; one record with one label MUST yield at most one finding, and the cross-label precedence MUST be written down three times over: ① a missing section reports only `dtr-section-missing` and suppresses `dtr-anchor`, because the three-heading adjacency assertion necessarily reds when the section does not exist and one root cause MUST NOT be counted twice; ② a record missing any of the six field labels reports only `dtr-record-incomplete` and MUST NOT additionally report `expected-sacrifice-unmapped`, because a field absent leaves no value to parse; ③ an empty value — `expected_sacrifice` left blank, or the `pole_a` / `pole_b` line missing or blank — or an `expected_sacrifice` whose value is exactly `none` MUST report only `dtr-rejected-form` and MUST NOT additionally report `dtr-record-incomplete` or `expected-sacrifice-unmapped`, because an empty value has no decidable content and one root cause MUST NOT be counted as both an incomplete record and a failed mapping. (FR-016)
- **C-3** (output shape): the default human output MUST print a `status` line, one `[label] pass|fail (count)` line per check, and the findings; `--json` MUST print `{"spec","status","checks":[{"label","status","count"}],"errors","warnings","scanned"}`; the checker MUST be read-only with no write point, MUST use the standard library only with no third-party dependency, and MUST NOT start a resident process or propose rewritten text. (FR-016)
- **C-4** (inverse samples are tests, not prose): the checker MUST own inverse samples that each produce a red run in the contract test — deleting any single field, writing the expected sacrifice as the literal `none`, writing undecidable wording, duplicating a `tension_id`, and pointing at a non-existent measurement source — and those samples MUST NOT exist only as documentation. (FR-017)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-1 | FR-016 | test_cli_contract_and_exit_codes |
| C-2 | FR-016 | test_label_set_closed_and_dedup_precedence |
| C-3 | FR-016 | test_output_shape_human_and_json |
| C-4 | FR-017 | test_inverse_samples_turn_red |

## FR 覆盖核对

- FR-016、FR-017 由本文件 C-1…C-4 承接。
- 各标签的字段判据与拒绝清单 owner 是 `shared/guidelines/decision-tension.md`；本契约只钉标签面、
  去重与输出，不复述判据表。
