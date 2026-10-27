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

- 命令行: `python3 -m pytest -q tests/contract/test_client_package_exclusion.py`
- 真实输出: `8 failed, 6 passed in 1.59s`（失败名见下；普遍形态 = path-a-digest.md 尚无载体指派闭集三/undecided/backlog 行/消失单元/呈报三事实文本，feedback 命令模板与 docs 页尚无 client-metrics/载体/undecided 指针；行为面（打包无条件排除并报告 excluded_external、cleanup 不触碰外部条目、无绕过开关、双侧 kind 分离、同会话双侧）红运行前已成立——钉的是既有引擎面，不作红声称）
- 退出码: `1`
- 失败计数: `8`
- 失败名（2026-10-27 未改动树 @ f4409d20，US2 已落地后）: test_c26_carrier_closed_set_is_exactly_three_with_park_default · test_c26_no_entry_assigned_two_carriers_and_undecided_is_reported · test_c27_carrier_sections_cite_owners_without_restatement · test_c28_two_side_closure_and_refinement_direction_preserved · test_c29_digest_report_carries_the_three_facts · test_c30_routing_backlog_one_named_carrier_row_per_entry · test_c31_vanished_client_unit_entries_stay_readable · test_t015_feedback_command_surfaces_carry_client_digest_pointers

### G4 — test_client_improve_loop.py (T016)

- 命令行: `python3 -m pytest -q tests/contract/test_client_improve_loop.py`
- 真实输出: `6 failed, 6 passed in 0.34s`（失败名见下；普遍形态 = `docs/reference/commands/improve.md` 缺失（plan 同步面缺口）、三处循环面（workflow SI-1 / self-improvement SKILL.md / improve 命令模板）尚无「运行判定历史未评估」披露字面量与引擎 fail-closed 原因引文、「kind: external」客户通道观察源规则与「没有唯一所有者」SI-0 停机报告字面量）
- 退出码: `1`
- 失败计数: `6`
- 失败名（2026-10-27 未改动树 @ ca1e51bd，US3 已落地后）: test_c33_five_criteria_gain_no_relaxation_for_custom_subjects · test_c34_why_discloses_run_determination_history_not_evaluated · test_c35_observation_source_is_client_channel_plus_existing_lanes · test_c37_how_routes_existing_dispatch_table_with_no_client_improver · test_c39_no_unique_editable_definition_halts_at_si0_with_named_report · test_t018_improve_docs_template_and_tool_copies_aligned。红运行前已成立、不作红声称的 6 项：test_c33_loop_reuses_si0_through_si9_with_no_client_specific_flow（SI-0…SI-9 步骤面 + 无客户专用技能 + 五条判据归 definitions owner 且不被复述）、test_c34_engine_fail_closed_for_custom_subject_is_observable_in_client（引擎对 custom: 主体 fail-closed 钉的是既有引擎面，per test_run_determination_engine.py:1393）、test_c36_engine_source_contract_not_widened_and_no_second_observer（引擎单一持久化适配器 + 无第二观察引擎/并行历史存储）、test_c38_falsification_attempt_ledger_hard_limit_outcome_pending（四约束既有文本逐字钉）、test_c39_resolution_failure_mutates_nothing_in_the_client_project（引擎只读 + 工作树零变更行为面）、test_t017_t018_mirror_isomorphism_for_the_edited_surfaces（镜像同构，T017/T018 同步后仍须成立）。

### G5 — test_client_metrics.py (T020)

- 命令行: `python3 -m pytest -q tests/contract/test_client_metrics.py`
- 真实输出: `15 failed, 1 passed in 11.22s`（失败名见下；普遍形态 = `--action client-metrics` 尚不在引擎 `--action` 选择闭集内（usage 报错 / exit 2），`docs/reference/commands/feedback.md` 尚无 C-40/C-41/C-42/C-44/C-45 的口径文本；argparse 报 `--unit` 与 `--unit-id`/`--unit-type` 前缀歧义——R7 钉死的选项形态 `--unit` 需注册为精确选项）
- 退出码: `1`
- 失败计数: `15`
- 失败名（2026-10-27 未改动树 @ 20649139，US4 已落地后）: test_c40_no_scheduler_resident_timer_in_any_feature_surface · test_c41_records_before_arming_are_excluded_never_backfilled · test_c42_threshold_combination_rule_unchanged_and_metrics_never_feed_it · test_c43_four_metrics_with_explicit_numerator_denominator_and_values · test_c43_metric_sources_are_existing_records_only · test_c44_closure_counts_only_owner_file_change_evidence · test_c44_carried_row_with_missing_or_unchanged_owner_file_is_not_closed · test_c45_repeat_finding_rate_is_a_proxy_labeled_coarse · test_c46_readings_identical_across_reports_and_store_tree_unchanged · test_c46_action_has_no_write_point_even_against_a_read_only_store · test_c47_engine_action_is_the_machine_readable_derivation · test_c48_zero_denominators_report_not_evaluated_with_reason · test_c48_capture_coverage_not_evaluated_when_no_record_qualifies · test_c49_boundary_is_first_external_entry_and_exclusion_is_disclosed · test_c50_unreadable_record_excluded_from_repeat_rate_only（唯一通过项 test_c40_capture_happens_per_qualifying_run_via_existing_fifth_step 钉的是 US1 已落地的每运行采集行为面，红运行前即成立，不作红声称）
- 实现期裁决（记录假设）：路由台账行 ↔ 条目的挂接约定 = 行文本含条目 id（`entry <id>` 落于 Source 格）；承接类行 = 任一单元格去 markdown 加粗后以 `carried-by-` 起始（E8 行语义）；owner 文件 = 行内反引号路径（支持 `**` glob），闭环证据 = 文件存在且 mtime 晚于条目 `created`（V28 mtime 口径）；(文件,严重度) 对从记录正文 `### <icon> [<SEVERITY>] <file>` 标题行确定性抽取；`--unit` 注册为精确选项以消解与 `--unit-id`/`--unit-type` 的前缀歧义。以上均为计划/契约未钉死处的实现裁决，判据归 contracts/cadence-and-metrics.md C-43…C-50 与 data-model.md E8/E9。
- T022 补充红运行（实现行断言，非新组）：`python3 -m pytest -q tests/contract/test_client_package_exclusion.py` → `1 failed, 14 passed in 1.59s`，退出码 `1`，失败计数 `1`（test_t022_digest_surfaces_present_metrics_as_read_only_non_gate；未改动树 @ 20649139，US4 已落地后；14 项先行通过项均属 G3 已转绿面，不作红声称）。失败四字段同式记录在案，因 G3 槽位已按"每组一条"闭合，此条为其下补充记录。
- 纠正性披露（绿跑期，本 part）：(1) `_RECORD_RUN_STAMP_RE` 末段 `|` 未转义成 `\|`，被正则当成交替分支致空匹配——就地修复并重跑；(2) test_c47 的 `project` 在 `with` 块关闭后仍被使用（FileNotFoundError）——断言移入块内；(3) 捕获覆盖率两例（test_c41/test_c43）的记录运行戳与条目 `created`（秒级精度）存在亚秒竞态，武装后记录戳改为 +5/+6 分钟边距后双跑稳定（556 passed ×2）。均为测试/新码侧修正，未触碰任何守护断言的语义。

## 纪律备注

- **part 8d 纠正披露（2026-10-27, driver 裁决）**: closure rerun 的唯一 NEW 失败名是 `test_measurement_instruments.py::test_git_start_channel_is_the_first_commit_not_the_last_touch`。根因 = `_git_first_commit()` 用 `git log --format=%h` 取缩写，随仓库对象增长 `%h` 从 8 位漂为 9 位（`f0df3d0b0`），而 069b 冻结记录是 8 位 `f0df3d0b`，`sha in text` 失配；测试语义（首次提交仪器）未被破坏，是缩写长度漂移。纠正 = 仪器侧固定缩写：`git log --abbrev=8 --format=%h %as`，与冻结记录对齐（record frozen at 8）；不改记录、不改断言语义。证据： `test-evidence/part8d-instruments-correction.txt`（13 passed, RC=0）、`test-evidence/part8d-six-suites.txt`（六新套件 104 passed / 0 failed = 零 NEW 失败名）；本纠正落地同期发现 root 于 21:33 向对象库写入同一 notes blob（孤立树链、未动 refs，无活动并发进程），属环境权限噪声，非内容分歧。
- 红运行 MUST 在未改动树(实现编辑前)上执行；失败计数 = 该文件 pytest 报告的 failed 数。
- 守护性复跑(071 六套件、`test_expression_compatibility.py` C-5、`test_review_p1_review_loop.py`、feedback/probe 族)是迁移/回归例外，**不作红先行声称**，不进本文件。
- 实现完成后同命令全绿即为该组转绿证据(GATE-5)。
- **part 8c 纠正披露（2026-10-27, driver 裁决）**: closure 全量 23 failed 中，`test_c56_changed_paths_stay_on_the_declared_edit_surface` 的唯一 offender 是 `.specify/memory/register.md`——review 阶段（96ceceed）按 071/063 义务将 REC-072-01…04 同提交登记进 ID 登记表，属合法项目记录，非框架源手改。纠正 = `allowed_exact` 加入 `.specify/memory/register.md` 精确项（注释说明登记义务来源），断言语义不变（无断言弱化/增删，25 测试维持），未扩大到整个 `.specify/memory/`。证据： `test-evidence/part8c-guard-sweep-correction.txt`（25 passed, RC=0）。
- **part 8b 纠正披露（2026-10-27, driver 裁决）**: `test_client_guard_sweep.py::test_c56_changed_paths_stay_on_the_declared_edit_surface` 的 `allowed_prefixes` 原只白名单 `.specify/skills/internal/`，漏了同一 `sync-mirrors.py` 生成器产出的其它 skill 镜子；part 8 的 `sync-mirrors.py --write` 合法消解 T001 既录的 `loop-playbook.md` 漂移后，再生镜像 `.specify/skills/improve-skills/references/loop-playbook.md` 被误报为 offender。C-56 意图是"运行时投影由生成器产出、绝不手改"，故白名单扩为 `.specify/skills/`（全部 skill 镜子），断言语义不变（无断言弱化、无测试增删，文件维持 25 测试）。证据： `test-evidence/part8b-guard-sweep-correction.txt`（guard sweep 25 通过；六套件 104 通过 0 失败；对 `baseline-failed.txt` 的 comm -13 为空 = 零 NEW）。
