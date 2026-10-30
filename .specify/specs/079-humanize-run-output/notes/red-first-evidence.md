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
