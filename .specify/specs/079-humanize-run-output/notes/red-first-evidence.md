# Red-first evidence — 079 humanize run output

**Role**: 五个红先行行（T005 / T013 / T019 / T024 / T036）共用的追加落点。每次追加带日期、树状态、命令、真实输出、退出码与失败计数；历史小节不回填。

---

## T005 — US1 契约组（2026-10-30T16:05Z）

### 树状态（红态）

- `tests/contract/test_humanize_command_surface.py`：已扩展 062 C-1..C-10 + 079 条款组（IP-01…IP-10、EX-01…EX-10、RP-01…RP-04、WC-01…WC-04），函数名与契约可追溯性表逐字一致。
- `tests/fixtures/humanize/run/`：夹具集已就位（success / failure / non-action / needs-confirmation / denied / degraded / nested / reservations / injection / governance / README）。
- `skills/external/humanize/SKILL.md`：T003 的模式分叉已完成（两个分支 + 两条 Non-negotiables）。
- `skills/external/humanize/references/run-mode.md`：**尚不存在**（T006–T008 的实现目标）。为取得真实红态，运行时临时移出该文件、跑完即还原；这是红态的如实重建，不是删产物。

### 命令与真实输出

```
.venv/bin/python -m pytest -q tests/contract/test_humanize_command_surface.py
```

- **退出码**: `1`
- **失败计数**: `26 failed, 12 passed, 1 warning in 7.88s`

失败名（真实 short summary，逐字）：

```
FAILED tests/contract/test_humanize_command_surface.py::test_c06_registry_rows_resolve
FAILED tests/contract/test_humanize_command_surface.py::test_ip01_parse_is_pure_syntax
FAILED tests/contract/test_humanize_command_surface.py::test_ip02_instruction_is_verbatim
FAILED tests/contract/test_humanize_command_surface.py::test_ip03_option_domain_unchanged
FAILED tests/contract/test_humanize_command_surface.py::test_ip04_parse_fields_closed
FAILED tests/contract/test_humanize_command_surface.py::test_ip05_routing_table_order
FAILED tests/contract/test_humanize_command_surface.py::test_ip06_source_and_instruction_rejected
FAILED tests/contract/test_humanize_command_surface.py::test_ip07_no_input_usage_and_hint
FAILED tests/contract/test_humanize_command_surface.py::test_ip08_empty_source_rejected
FAILED tests/contract/test_humanize_command_surface.py::test_ip09_migration_hint_once
FAILED tests/contract/test_humanize_command_surface.py::test_ip10_hint_placement
FAILED tests/contract/test_humanize_command_surface.py::test_ex01_exactly_one_dispatch
FAILED tests/contract/test_humanize_command_surface.py::test_ex02_run_agent_carrier_only
FAILED tests/contract/test_humanize_command_surface.py::test_ex03_temporary_executor_no_agent_file
FAILED tests/contract/test_humanize_command_surface.py::test_ex04_carrier_modes
FAILED tests/contract/test_humanize_command_surface.py::test_ex05_marker_matches_carrier
FAILED tests/contract/test_humanize_command_surface.py::test_ex06_payload_six_items
FAILED tests/contract/test_humanize_command_surface.py::test_ex07_payload_keeps_instruction_verbatim
FAILED tests/contract/test_humanize_command_surface.py::test_ex08_payload_defers_to_instruction_gates
FAILED tests/contract/test_humanize_command_surface.py::test_ex09_envelope_is_message
FAILED tests/contract/test_humanize_command_surface.py::test_ex10_missing_anomaly_line_blocks_consumption
FAILED tests/contract/test_humanize_command_surface.py::test_rp01_five_sections_in_order
FAILED tests/contract/test_humanize_command_surface.py::test_rp02_metadata_block
FAILED tests/contract/test_humanize_command_surface.py::test_rp03_main_session_writes_report
FAILED tests/contract/test_humanize_command_surface.py::test_rp04_zero_write_default
FAILED tests/contract/test_humanize_command_surface.py::test_wc01_template_declares_breaking_change
```

`test_c06_registry_rows_resolve` 是 **E2 已捕获的既有失败**（在 `baseline-failed.txt` 内），不是本段新增；不得通过改测试掩盖。

### 三条不变量守卫（先绿，不声称红先行）

`test_wc02_thin_entry_invariant`、`test_wc03_wiring_card_preserved`、`test_wc04_no_blocking_literals` 在红态即为绿：它们守护的是**尚未被本特性改动的现存不变量**（薄入口、077 接线小节、门禁字面量）。按 tasks.md § Tests 的纪律，它们标注为守卫，不作红先行声称。

### T006–T008 落笔后的复测（同一命令）

- **退出码**: `1`
- **读数**: `12 failed, 26 passed, 1 warning in 0.26s`
- **转绿**: `test_ip01…test_ip10`、`test_ex01…test_ex05`（15 条）；守卫 3 条保持绿。
- **仍红（预期）**: `test_ex06…test_ex10`（§ Payload / § Envelope，T009/T010）、`test_rp01…test_rp04`（`references/report-shape.md`，T011）、`test_wc01`（命令模板，T012）。
- **仍红（基线）**: `test_c06_registry_rows_resolve`（E2 既有失败，见上）。

---

## T013 — US2 契约组（2026-10-30T15:53Z）

### 树状态（红态）

- `tests/contract/test_humanize_command_surface.py`：新增 US2 组 `test_rp05…test_rp18`（14 条，函数名逐字取自 `contracts/report-assembly.contract.md` § 可追溯性表），并加两个确定性辅助：`_governance_state()` 把 `tests/fixtures/humanize/run/governance/` 投影成 FR-014 的两态（全可得 = 四源全 `read`；部分来源不可得 = `glossary` 为 `unavailable`、其余三源 `read`）。
- `skills/external/humanize/references/report-shape.md`：T011 已落盘 § Metadata Block / § Sections；§ Conclusion、§ Key Changes、§ Evidence、§ Risks & Limits、§ Next Steps、§ Language、§ Fidelity & Honesty **尚未落笔**（T014–T018 的实现目标）。
- `templates/commands/humanize.md`：T012 已改写（不影响本组判定）。

### 命令与真实输出

```
.venv/bin/python -m pytest -q tests/contract/test_humanize_command_surface.py -k "rp05 or rp06 or rp07 or rp08 or rp09 or rp10 or rp11 or rp12 or rp13 or rp14 or rp15 or rp16 or rp17 or rp18"
```

- **退出码**: `1`
- **失败计数**: `14 failed, 38 deselected, 1 warning in 0.13s`

失败名（真实 short summary，逐字）：

```
FAILED tests/contract/test_humanize_command_surface.py::test_rp05_conclusion_verdict
FAILED tests/contract/test_humanize_command_surface.py::test_rp06_key_changes_by_impact
FAILED tests/contract/test_humanize_command_surface.py::test_rp07_evidence_pointers
FAILED tests/contract/test_humanize_command_surface.py::test_rp08_dispatch_record_line
FAILED tests/contract/test_humanize_command_surface.py::test_rp09_no_known_risks_explicit
FAILED tests/contract/test_humanize_command_surface.py::test_rp10_sources_read_list
FAILED tests/contract/test_humanize_command_surface.py::test_rp11_next_steps_or_none
FAILED tests/contract/test_humanize_command_surface.py::test_rp12_language_priority
FAILED tests/contract/test_humanize_command_surface.py::test_rp13_headings_stay_english
FAILED tests/contract/test_humanize_command_surface.py::test_rp14_language_keeps_identifiers
FAILED tests/contract/test_humanize_command_surface.py::test_rp15_fidelity_floor
FAILED tests/contract/test_humanize_command_surface.py::test_rp16_no_fabrication
FAILED tests/contract/test_humanize_command_surface.py::test_rp17_expression_and_detector_honesty
FAILED tests/contract/test_humanize_command_surface.py::test_rp18_reader_comprehension
```

### 落笔后的复测（T014–T016 已写，T017/T018 未写，2026-10-30T15:58Z）

同一命令（`-k` 取 RP-05…RP-18）：

- **退出码**: `1`；**读数**: `8 failed, 6 passed, 38 deselected, 1 warning in 0.10s`
- **转绿**: `test_rp05…test_rp10`（6 条；§ Conclusion / § Key Changes / § Evidence / § Risks & Limits 已落盘）。
- **仍红（预期红先行）**: `test_rp11…test_rp18`（8 条）——§ Next Steps / § Language / § Fidelity & Honesty 的实施行是 T017 / T018，不在本段范围。

---

## T019 — US3 契约组（2026-10-30T16:05Z）

### 树状态（红态）

- `tests/contract/test_humanize_command_surface.py`：新增 US3 组 `test_ex11…test_ex21`、`test_ip11…test_ip14` 与 SC-004 拒绝确认对 `test_sc04_denied_no_side_effect` / `test_sc04_denied_verdict_and_scope`（函数名逐字取自 `contracts/execution-dispatch.contract.md`、`contracts/invocation-parse.contract.md` 的可追溯性表；SC 前缀组按 tasks.md T019 的命名约定，不进条款反向认领面）。
- `skills/external/humanize/references/run-mode.md`：§ Failure & No Retry、§ Confirmation Missing、§ Degradation & Boundaries、§ Reservation & Nesting **尚未落笔**（T020–T023 的实现目标）。
- 判定仪器写死在断言里：网络调用字面量静态扫描（`curl` / `wget` / `httpx` / `requests.` / `urllib` / `fetch(`，URL 文本不计）、`git status --porcelain` 前后快照、`dispatches:` 行作为派发与重试计数唯一来源。

### 命令与真实输出

```
.venv/bin/python -m pytest -q tests/contract/test_humanize_command_surface.py -k "ex11 or ex12 or ex13 or ex14 or ex15 or ex16 or ex17 or ex18 or ex19 or ex20 or ex21 or ip11 or ip12 or ip13 or ip14 or sc04"
```

- **退出码**: `1`
- **失败计数**: `17 failed, 52 deselected, 1 warning in 0.37s`

失败名（真实 short summary，逐字）：

```
FAILED tests/contract/test_humanize_command_surface.py::test_ex11_no_compensating_redispatch
FAILED tests/contract/test_humanize_command_surface.py::test_ex12_failure_coordinates_no_retry
FAILED tests/contract/test_humanize_command_surface.py::test_ex13_aborted_reported_as_aborted
FAILED tests/contract/test_humanize_command_surface.py::test_ex14_evidence_locatability_check
FAILED tests/contract/test_humanize_command_surface.py::test_ex15_confirmation_missing_fail_closed
FAILED tests/contract/test_humanize_command_surface.py::test_ex16_no_proxy_answer
FAILED tests/contract/test_humanize_command_surface.py::test_ex17_degraded_honesty
FAILED tests/contract/test_humanize_command_surface.py::test_ex18_degraded_keeps_report_contract
FAILED tests/contract/test_humanize_command_surface.py::test_ex19_no_network_from_humanize
FAILED tests/contract/test_humanize_command_surface.py::test_ex20_reservation_released_all_paths
FAILED tests/contract/test_humanize_command_surface.py::test_ex21_dispatch_record_line
FAILED tests/contract/test_humanize_command_surface.py::test_ip11_active_run_rejected
FAILED tests/contract/test_humanize_command_surface.py::test_ip12_output_occupied_rejected
FAILED tests/contract/test_humanize_command_surface.py::test_ip13_nested_invocation_rejected
FAILED tests/contract/test_humanize_command_surface.py::test_ip14_reject_paths_write_nothing
FAILED tests/contract/test_humanize_command_surface.py::test_sc04_denied_no_side_effect
FAILED tests/contract/test_humanize_command_surface.py::test_sc04_denied_verdict_and_scope
```

失败原因统一为「被断言的小节不存在」（`section '## Failure & No Retry' / '## Confirmation Missing' / '## Degradation & Boundaries' / '## Reservation & Nesting' missing`）；这是预期的红先行态，不是实现缺陷。

---

## T024 — US4 契约组（2026-10-30T16:12Z）

### 树状态（红态）

- `tests/contract/test_humanize_command_surface.py`：新增 US4 组 `test_cm01…test_cm10`、`test_ip15…test_ip17`、`test_rp19`、`test_rp20`（函数名逐字取自 `contracts/content-mode.contract.md`、`contracts/invocation-parse.contract.md`、`contracts/report-assembly.contract.md` 的可追溯性表）。
- 未落笔的实现面：`SKILL.md` 的内容模式分支收口（T025）、两模式共有防线（T026）、`run-mode.md` 的 § Output（T027）、docs 迁移示例（T029）与内容模式措辞（T030）。
- 两条**不变量守卫**（先绿，不声称红先行）：`test_cm01_content_mode_equivalence`（Stage 1–7 逐字保留）与 `test_cm05_routing_owned_by_ip05`（路由唯一 owner 指向 `references/run-mode.md` § Mode Routing，且 SKILL 未重述判定表）。

### 命令与真实输出

```
.venv/bin/python -m pytest -q tests/contract/test_humanize_command_surface.py -k "cm01 or cm02 or cm03 or cm04 or cm05 or cm06 or cm07 or cm08 or cm09 or cm10 or ip15 or ip16 or ip17 or rp19 or rp20"
```

- **退出码**: `1`
- **失败计数**: `13 failed, 2 passed, 69 deselected, 1 warning in 0.25s`

失败名（真实 short summary，逐字）：

```
FAILED tests/contract/test_humanize_command_surface.py::test_cm02_content_output_text_only
FAILED tests/contract/test_humanize_command_surface.py::test_cm03_no_report_scaffold_in_content_mode
FAILED tests/contract/test_humanize_command_surface.py::test_cm04_content_mode_no_dispatch
FAILED tests/contract/test_humanize_command_surface.py::test_cm06_injection_defense_both_modes
FAILED tests/contract/test_humanize_command_surface.py::test_cm07_fidelity_both_modes
FAILED tests/contract/test_humanize_command_surface.py::test_cm08_detector_honesty_both_modes
FAILED tests/contract/test_humanize_command_surface.py::test_cm09_migration_example_present
FAILED tests/contract/test_humanize_command_surface.py::test_cm10_content_mode_wording_intact
FAILED tests/contract/test_humanize_command_surface.py::test_ip15_content_mode_unreserved
FAILED tests/contract/test_humanize_command_surface.py::test_ip16_run_output_extension
FAILED tests/contract/test_humanize_command_surface.py::test_ip17_content_output_unchanged
FAILED tests/contract/test_humanize_command_surface.py::test_rp19_output_full_report_and_summary
FAILED tests/contract/test_humanize_command_surface.py::test_rp20_atomic_write_and_force
```

失败原因分两类：① `SKILL.md` 尚无两模式共有防线与内容模式收口锚点（CM-02…CM-08、CM-10、IP-15）；② `run-mode.md` 的 § Output 尚不存在（IP-16、IP-17、RP-19、RP-20），docs 尚无迁移示例（CM-09）。均为预期红先行态。
