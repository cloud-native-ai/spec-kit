# Red-First Evidence — Feature 072 client-self-improvement

> Owner slot: `.specify/specs/072-client-self-improvement/notes/red-first-evidence.md`
> 判定面: SC-006。五个新契约测试组每组一条红先行记录，**四字段缺一即该组声称无效**:
> ① 命令行 ② 真实输出 ③ 退出码 ④ 失败计数。
> 记录形态归 tasks.md § Notes；本文件在 T001 只立骨架，各组红运行由对应任务行(T004/T009/T013/T016/T020)回填。

## 五个新契约测试文件（点名）

| # | 测试文件 | 行为组 | 认领行 | 契约条款 |
|---|----------|--------|--------|----------|
| 1 | `tests/contract/test_client_capture.py` | 采集(非交互路径五步 + capture 子命令面) | T004 | C-10…C-16 (capture-step.md) |
| 2 | `tests/contract/test_client_armed_state.py` | 武装态三值(已武装/未武装/歧义) | T009 | C-1…C-9 (client-identity-and-armed-state.md) |
| 3 | `tests/contract/test_client_package_exclusion.py` | 打包排除 + 载体闭集 | T013 | C-25…C-28 (digest-and-carriers.md) |
| 4 | `tests/contract/test_client_improve_loop.py` | 客户主体改进循环(SI-0…SI-9 复用) | T016 | C-33…C-39 (client-improvement-loop.md) |
| 5 | `tests/contract/test_client_metrics.py` | 循环度量即读即建(只读 client-metrics) | T020 | C-40…C-45 (cadence-and-metrics.md) |

## 红先行记录骨架（每组一条，回填时替换占位）

### G1 — test_client_capture.py (T004)

- 命令行: `python3 -m pytest -q tests/contract/test_client_capture.py`
- 真实输出: `15 failed, 1 passed in 1.98s`（失败名见下；普遍形态 = `bash .../git-delta-review.sh capture ...` 返回 `✗ 未知命令: capture`，及 SKILL.md 非交互路径仍为四步）
- 退出码: `1`
- 失败计数: `15`
- 失败名（2026-10-27 未改动树 @ ac98d354）: test_c10_step_enumeration_is_five_steps_with_reason_and_cost · test_c11_capture_subcommand_parameter_form · test_c12_capture_fires_once_and_is_idempotent · test_c12_gate_deny_does_not_suppress_capture · test_c13_framework_hat_writes_nothing_and_names_the_hat_verdict · test_c14_non_run_triage_discloses_no_capture_object[not-applicable] · test_c14_non_run_triage_discloses_no_capture_object[not-evaluated] · test_c15_pointer_payload_is_a_closed_field_set_without_opinion_bodies · test_c16_six_counts_verbatim_from_summary_json_including_zeros · test_c19_capture_never_edits_the_record_or_receipt_block · test_c21_summary_exit_2_discloses_counts_unavailable · test_c21_engine_refusal_discloses_counts_unavailable_and_never_blocks · test_c22_exactly_one_outcome_line_with_token_and_applicability_visible · test_c23_no_phoenix_empty_entry_for_failed_capture · test_c24_disclosure_lives_only_in_the_run_conclusion（唯一通过项 test_c17 钉的是既有文本/退出码面，红运行前即成立，不作红声称）

### G2 — test_client_armed_state.py (T009)

- 命令行: `python3 -m pytest -q tests/contract/test_client_armed_state.py tests/contract/test_dogfooding_practice.py`
- 真实输出: `11 failed, 30 passed in 4.40s`（失败名见下；普遍形态 = 显式单元无探针/注册表不可用/畸形 `--unit` 三类情形当前落到 `counts-unavailable` 或写出 legacy 条目而非 `client-channel-unarmed`/`skipped` 行；Loop B 配方仍为 `skill:<scenario-name>`；docs/reference/commands/review.md 尚无 `--client-unit`/第五步/披露）
- 退出码: `1`
- 失败计数: `11`
- 失败名（2026-10-27 未改动树 @ 5db467dd，US1 已落地后）: test_c3_explicit_unit_without_probe_is_unarmed_with_probe_inject_guidance · test_c4_registry_unavailable_is_unarmed_never_records_no_legacy_entry[True] · test_c6_malformed_unit_value_yields_named_skip_line[banana] · test_c6_malformed_unit_value_yields_named_skip_line[custom:owner] · test_c6_malformed_unit_value_yields_named_skip_line[custom:/name] · test_c6_malformed_unit_value_yields_named_skip_line[custom:owner/] · test_c7_framework_unit_families_never_reach_the_client_channel[/speckit.review] · test_c7_framework_unit_families_never_reach_the_client_channel[skill:code-review] · test_t012_review_docs_and_template_aligned_on_capture · test_loop_b_recipe_uses_custom_unit_form（test_dogfooding_practice.py 净增断言）· test_loop_b_recipe_states_the_reason（test_dogfooding_practice.py 净增断言）。红运行前对测试自身的 C-8 frontmatter 解析做过一处修正（值是 JSON 编码，改用 json.loads；ENTRY_KEY_SET 对齐 dump_frontmatter 既有键序），修正后重跑即为上面这版 11 败记录；其余 30 项（C-1 双向帽子、C-2 闭集与解析顺序、C-4 无显式单元支路、C-5 歧义、C-9 等）红运行前已成立，不作红声称。

### G3 — test_client_package_exclusion.py (T013)

- 命令行: _pending — 红运行后回填_
- 真实输出: _pending_
- 退出码: _pending_
- 失败计数: _pending_

### G4 — test_client_improve_loop.py (T016)

- 命令行: _pending — 红运行后回填_
- 真实输出: _pending_
- 退出码: _pending_
- 失败计数: _pending_

### G5 — test_client_metrics.py (T020)

- 命令行: _pending — 红运行后回填_
- 真实输出: _pending_
- 退出码: _pending_
- 失败计数: _pending_

## 纪律备注

- 红运行 MUST 在未改动树(实现编辑前)上执行；失败计数 = 该文件 pytest 报告的 failed 数。
- 守护性复跑(071 六套件、`test_expression_compatibility.py` C-5、`test_review_p1_review_loop.py`、feedback/probe 族)是迁移/回归例外，**不作红先行声称**，不进本文件。
- 实现完成后同命令全绿即为该组转绿证据(GATE-5)。
