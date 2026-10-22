# Red-First Evidence — 068 Exec-Quant Feedback Channel (implement, US1/US2)

红先取证纪律（tasks.md § Tests / owner `.specify/skills/internal/implement-feature/SKILL.md`
§ TDD / § Test runs）：每支新测试先以未实现状态运行并记录命令、真实输出、退出码与
用例清单。本文件按节追加（US1: T004 → T005 → 绿证据；US2 part 3a: T010 → T011），
append-only。

- 日期：2026-10-22
- canonical runner：`bash scripts/bash/run-tests.sh <targets> -q`
- 测试针对框架源 `scripts/python/feedback-utils.py`（`tests/script_api.py` 以
  `scripts/python/feedback-utils.py` 装载 `feedback_utils`；非 `.specify/` 镜像）。

## § T004 — `tests/unit/test_feedback_exec_quant_payload.py`（red-first）

- 命令：`bash scripts/bash/run-tests.sh tests/unit/test_feedback_exec_quant_payload.py -q`
- 退出码：`1`
- 真实输出尾部（节选）：

```text
FFFFFFFFFFFFFFFFFFFF                                                     [100%]
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_collect_dual_form_full_inclusion
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_collect_kind_filter_and_unreadable_skipped
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_legacy_entry_names_line_numbers_from_one
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_source_form_counts_dual_counting
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_sort_collected_at_then_source_name_deterministic
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_cap_constants_pinned_values
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_record_cap_truncation_counts
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_byte_cap_whole_record_granularity_and_oversize
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_byte_cap_greedy_prefix_stops_at_first_violator
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_missing_collected_at_sorts_first
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_bucket_exhaustiveness_invariant
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_sweep_is_read_only_on_source_store
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_missing_store_degrades_to_empty_payload
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_identity_reads_project_name_line
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_identity_falls_back_to_workspace_basename
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_identity_unknown_project_when_no_name_available
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_source_commit_resolves_head_via_git_files
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_source_commit_detached_head_and_packed_refs
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_source_commit_null_without_git_and_on_garbage
FAILED tests/unit/test_feedback_exec_quant_payload.py::test_source_commit_rejects_non_40hex
20 failed in 0.22s
```

- 用例清单：上列 20 行（覆盖载荷采集双形态全量纳入、kind 过滤 + skipped_unreadable、
  遗留名 `legacy-records-L%04d.json` 自 1 起、source_form_counts 双计数、确定性排序、
  封顶常量与截断、U-01/U-02/U-03 最小规则、只读源、身份三级解析、source_commit 四态）。
- 失败归因：**subject 缺失**——`AttributeError: module 'feedback_utils' has no
  attribute '_collect_exec_quant_payload'`（同族：`_resolve_package_identity`、
  `_resolve_source_commit`、`MAX_PAYLOAD_RECORDS`/`MAX_PAYLOAD_BYTES`），断言面本身
  无缺陷。

## § T005 — `tests/contract/test_feedback_exec_quant_payload.py`（red-first）

- 命令：`bash scripts/bash/run-tests.sh tests/contract/test_feedback_exec_quant_payload.py -q`
- 退出码：`1`
- 真实输出尾部（节选）：

```text
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_zip_layout_payload_only_under_exec_quant
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_record_members_byte_verbatim
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_payload_manifest_field_set_e4
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_payload_manifest_counts_legacy_form
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_manifest_human_section_same_source
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_manifest_empty_payload_section_declares_no_data
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_json_report_face_visible_counts
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_text_report_face_visible_counts
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_fr019_empty_feedback_still_packages
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_fr019_double_empty_no_package_with_explicit_note
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_time_filter_all_semantics_unchanged_payload_full
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_external_exclusion_semantics_unchanged
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_include_introspection_semantics_unchanged
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_mark_submitted_archive_has_no_payload
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_payload_degradations_exit_zero
FAILED tests/contract/test_feedback_exec_quant_payload.py::test_identity_degradation_exit_zero
16 failed, 1 passed in 0.44s
```

- 用例清单：上列 16 红 + 1 预绿守卫（`test_source_stores_read_only_after_package`：
  FR-002 只读性质在**既有**打包路径已成立，红先期通过属预期——该守卫的价值在实现
  加入载荷扫描路径后仍须保持；非新行为）。
- 失败归因（全部指向 subject，两轮归因）：
  1. 首轮 13 例失败归因测试夹具（`_record` 助手经 `fu.main` 打印的 record JSON 未及
     排空即被 `_package` 的 `capsys.readouterr()` 一并读出 → `JSONDecodeError`），
     属断言/夹具缺陷而非 subject——已修正夹具（读取前先排空缓冲、只读快照排除
     `packages/` 输出产物目录），并按 SKILL § TDD 在此披露该归因。
  2. 修正后终态 16 例全数指向 subject 缺失：`KeyError:
     "There is no item named 'exec-quant/payload-manifest.json' in the archive"`、
     `KeyError: 'exec_quant_payload'`、双空措辞仍是旧文案
     `No feedback entries to package.`（FR-019 未实现）。

## § 实现期裁决（analyze U-01/U-02/U-03 最小明确规则）

- **U-01（CHK005 截断粒度/单条超限）**：粒度 = 整条记录，无半条字节。规则：按
  排序键依次纳入，`已含条数 < MAX_PAYLOAD_RECORDS` 且 `累计字节 + 本条字节 ≤
  MAX_PAYLOAD_BYTES` 方可纳入；首个越限条目起（含该条）全部计入
  `truncated_count`。推论：单条自身超整个字节上限的记录本身被截断（计入
  truncated_count，永不部分纳入），载荷总字节恒 ≤ 上限。实现锚：
  `feedback-utils.py::_collect_exec_quant_payload` 纳入循环。
- **U-02（CHK006 缺 collected_at 排序）**：缺 `collected_at`（或非字符串）按空串
  `""` 参与升序比较，即排在最前；次键仍为载荷记录名（目录记录 = 源文件名，遗留流
  = 合成名 `legacy-records-L%04d.json`），跨机确定性。实现锚：排序键
  `(str(record.get("collected_at", "") or ""), name)`。
- **U-03（CHK007 探测总数留痕）**：不加第四字段（E4 字段集封闭）。规则：扫描把每个
  探测项恰分配到三个桶之一（纳入 / skipped_unreadable / truncated_count），故
  `skipped_unreadable + truncated_count + record_count == 探测总数` 恒成立、可由
  manifest 自身复核；接收侧对账（CHK019，part 3）以 `record_count == len(records/)`
  与成员级重放为准。守卫：`test_bucket_exhaustiveness_invariant`。
- **附带裁决 A（遗留流空行）**：`records.jsonl` 的空白行不是记录——既不纳入也不计
  `skipped_unreadable`；命名用物理行号（1 起），空行不使后续行号位移。守卫：
  `test_legacy_entry_names_line_numbers_from_one`。
- **附带裁决 B（source_commit 零 subprocess）**：C-5/D3 的 `git rev-parse HEAD` 以
  语义实现——引擎源 `feedback-utils.py` 受既有红线守卫
  `tests/unit/test_feedback_package.py::test_engine_source_has_no_network_or_push`
  约束（冻结基线内为绿，禁 `subprocess` 字面），且打包腿零网络（C-9）；故 HEAD 解析
  以纯本地文件读实现：`.git` 目录或 gitdir 指针文件 → `HEAD` → 松散 ref 文件 →
  `packed-refs`，仅接受 40-hex（data-model E2），任何失败置 null 不重试不阻塞。
  守卫：`test_source_commit_*` 四例。
- **附带裁决 C（载荷不引入水位）**：时间过滤 / `--all` / external 排除只作用于
  feedback 条目选择（C-8 语义零变化）；exec-quant 载荷按 FR-001 全量包含、不吃
  submitted_at 水位。守卫：`test_time_filter_all_semantics_unchanged_payload_full`。

## § T006/T007/T008 绿证据（T009 取证，2026-10-22）

- 命令：`bash scripts/bash/run-tests.sh tests/unit/test_feedback_exec_quant_payload.py tests/contract/test_feedback_exec_quant_payload.py -q`
- 退出码：`0`；输出尾部：`37 passed in 0.19s`（单元 20 + 契约 17，T004/T005 红先
  用例逐支转绿，零跳过）。
- 实现落点：`scripts/python/feedback-utils.py`（载荷采集 `_collect_exec_quant_payload`
  / 身份 `_resolve_package_identity` + `_resolve_source_commit` / 同源渲染
  `_render_payload_sections` / 报告投影 `_payload_report` / `write_package`+`action_package`
  FR-019 修订 / `render_text` C-7 文本面）。
- 红转绿过程中的失败归因（SKILL § TDD，逐项披露）：
  1. `write_package` 的 `**Time range**` 行无条件引用 `selected[0]/[-1]`——FR-019
     载荷独立成包路径（feedback 空）IndexError → 加 selected 空守卫（**subject 缺陷，
     已修**）；
  2. `_render_payload_sections` 首版读取 `payload["identity"]` 而采集函数未附身份 →
     身份并入采集返回值（**subject 缺陷，已修**）；
  3. 测试夹具侧 3 处断言/夹具缺陷（legacy 写入未建父目录、双形态计数 5 应为 4、
     `--all` 期望 2 应为 3——mark-submitted 归档不删条目，store 仍含全部 3 条；及
     截断用例仅有 1 条可用记录不构成截断）——均已按既有语义改正确认（**assertion
     side, 已修并注明**）。

## § 既有面邻接套件（零回归核查）

- 命令：`bash scripts/bash/run-tests.sh tests/unit/test_feedback_package.py tests/unit/test_feedback_utils.py tests/contract/test_feedback_utils_cli.py tests/unit/test_feedback_exec_quant_payload.py tests/contract/test_feedback_exec_quant_payload.py -q`
- 退出码：`0`；`70 passed in 0.24s`。
- 过程披露：首跑触发既有红线守卫
  `test_engine_source_has_no_network_or_push`（禁 `subprocess` 字面）——命中点是
  `_resolve_source_commit` **docstring 措辞**（实现本身零进程派生）；改写措辞后转绿，
  引擎源零 `subprocess`/网络 import（`grep` 核查零命中）。

## § 快速启动场景 4 — 24 文件定向集名字级比对（FR-018/SC-006 预核）

- 命令：`bash scripts/bash/run-tests.sh <quickstart 场景 4 的 24 文件集> -q --names-out /tmp/scenario4-current2.txt`
- 退出码：`1`；结果 `3 failed, 544 passed`（与冻结基线
  `test-evidence/log-baseline-pre-impl.txt` 完全一致）。
- 名字级比对：`comm -13 baseline current` = **零新增失败**；`comm -23` = 零消失
  （既有 3 个镜像一致性失败原样保留，其消失按 GATE-4 口径亦不算回归，但本段未使其
  变动）。

### 实现期修正记录（既有守卫随 068 边界修订，逐名归因）

- 首跑 24 文件集出现 1 个新增失败：
  `tests/contract/test_exec_quant_engine.py::TestNonBlocking::test_packaging_is_structurally_excluded`
  ——059 的结构钉「feedback 引擎源零 `exec-quant` 字面引用」。该断言与本特性已裁决
  的边界修订正面相抵（requirements § 对 059 的变更关系 + FR-019 + clarify A5：打包
  手动触发纳入量化载荷，「零自动传输」子句原样保留）。按 owner SKILL § TDD
  「断言与已裁决需求相抵 → 修断言并引用裁决」处置：该钉改写为修订后边界的结构形态
  `test_packaging_quant_coupling_is_read_only`（引擎零 import/派生量化引擎 + 量化
  存储仅经唯一只读定位器 `exec_quant_dir` 访问；行为面只读守卫 =
  068 契约测试 `test_source_stores_read_only_after_package`），行内引用上述裁决。
  改写后该文件 50 passed；重跑 24 文件集零新增失败（上节）。059 规格制品零触碰
  （修订关系仅记录于 068 侧与本文件）。

## § 独立可用性核验（快速启动场景 1 形态实跑 + US1 验收场景 1–4 测试等价物）

- 场景 1 route b 实跑（自构夹具，未触碰真实入站包与客户存储）：
  `python3 scripts/python/feedback-utils.py --action package --workspace-root <fixture> --format json`
  → 退出码 `0`；JSON 面含 `"exec_quant_payload": {"record_count": 2,
  "source_form_counts": {"records-dir": 2, "legacy-jsonl": 0},
  "skipped_unreadable": 0, "truncated_count": 0, "cap_records": 1000,
  "cap_bytes": 16777216, "collected_at_range": [...], "identity_status":
  "identified", "project_name": "cws-lib-python", "source_commit": null}`；
  `unzip -l` → `exec-quant/payload-manifest.json` + `exec-quant/records/*.json`（2 条）。
- FR-019 场景（feedback 空 + 载荷 2 条）：同命令仍产包，`packaged: 0`、
  MANIFEST `- **Entries**: 0` 显式（契约测试 `test_fr019_empty_feedback_still_packages`
  钉住）；双空不产包且说明覆盖两类数据（`test_fr019_double_empty_no_package_with_explicit_note`）。
- US1 验收场景 1–4 测试等价物全绿：场景 1（zip 含载荷 + MANIFEST 声明）→
  `test_zip_layout_payload_only_under_exec_quant` / `test_payload_manifest_field_set_e4`；
  场景 2（双存储逐文件清点零改动）→ `test_source_stores_read_only_after_package` +
  单元 `test_sweep_is_read_only_on_source_store`；场景 3（输出报告知情）→
  `test_json_report_face_visible_counts` / `test_text_report_face_visible_counts`；
  场景 4（FR-019）→ 上两支 FR-019 用例。场景 4（quickstart 回归比对）见上节。

---

# Implement Part 3a — US2 接收腿红先测试（T010 / T011，2026-10-22）

- 测试针对框架源 `scripts/python/feedback-utils.py`（`tests/script_api.py` 装载路径，
  非 `.specify/` 镜像）；夹具全部自构，真实入站包与运行时记录零触碰。
- 单元侧接口锚（part 3b T012/T013 实现须落这些名字，形态同 US1 的
  `_collect_exec_quant_payload` 先例）：`_identity_key(record, source_project)`、
  `_canonical_json(record)`、`_content_hash(record)`、
  `_source_slug(project_name, identity_key)`、
  `_build_envelope(record, identity, package_file)`。

## § T010 — `tests/unit/test_feedback_intake_exec_quant.py`（red-first）

- 命令：`bash scripts/bash/run-tests.sh tests/unit/test_feedback_intake_exec_quant.py -q`
- 退出码：`1`
- 真实输出尾部（节选）：

```text
E       AttributeError: module 'feedback_utils' has no attribute '_build_envelope'
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_identity_key_is_sha256_of_unit_separator_tuple
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_identity_key_deterministic_and_64hex
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_identity_key_excludes_content_f01
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_identity_key_missing_fields_join_as_empty
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_identity_key_varies_with_every_tuple_component
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_canonical_json_sort_keys_compact_raw_unicode
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_canonical_json_insertion_order_insensitive
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_content_hash_is_sha256_of_canonical_form
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_source_slug_is_name_plus_identity_hash8
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_source_slug_lowercases_and_substitutes_separators
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_source_slug_stays_in_restricted_charset
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_source_slug_empty_identity_is_literal_unknown_project
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_envelope_field_set_matches_e6
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_envelope_record_is_verbatim_zero_drop
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_envelope_identity_and_hash_fields
FAILED tests/unit/test_feedback_intake_exec_quant.py::test_envelope_unknown_project_literal_source
16 failed, 1 passed in 0.14s
```

- 用例清单：上列 16 红 + 1 预绿守卫（`test_subject_is_framework_source_engine`：
  断言 `feedback_utils` 装载自框架源 `scripts/python/feedback-utils.py` 而非
  `.specify/` 镜像——装载路径属既有能力，红先期通过属预期；该守卫的价值在 3b
  实现加入后持续防镜像漂移）。收集核对：`--collect-only` = 17。
- 覆盖面：identity_key 五元组 `\x1f` 连接 sha256（逐分量可变、确定性、64-hex、
  缺字段按空串）、content_hash 独立且不拼入 identity_key（F-01 修复口径，冲突分支
  可构造）、canonical JSON（sort_keys + ensure_ascii=False + 紧凑分隔符 + 插入序
  无关）、source-slug（slug 化 `[a-z0-9-]` + 身份串短哈希 8 位后缀；空身份 → 字面
  `unknown-project` 确定性）、信封 E6 字段集（`aggregation_envelope.*` 九字段 +
  `record` verbatim、未知字段零丢弃、unknown-project 字面落组）。
- 失败归因：**subject 缺失**——16 例全部 `AttributeError: module 'feedback_utils'
  has no attribute '_identity_key'/'_canonical_json'/'_content_hash'/'_source_slug'/
  '_build_envelope'`，断言面本身无缺陷。

## § T011 — `tests/contract/test_feedback_intake_exec_quant.py`（red-first）

- 命令：`bash scripts/bash/run-tests.sh tests/contract/test_feedback_intake_exec_quant.py -q`
- 退出码：`1`（两轮同）
- 首轮 19 failed / 1 passed：该 1 例通过属**假绿**——
  `test_missing_package_flag_is_usage_error_exit_2` 被 argparse 的
  `invalid choice: 'ingest-exec-quant'` 用法文本满足（usage 行含既有全局
  `--package` 旗标字样，`"--package" in stderr` 与 `code == 2` 双双凑巧成立），
  即该检查在其 subject 缺失时不会变红，不构成证据（快速失败纪律：机器给出的绿
  同样受判据约束）。归因 = 断言面缺陷（非 subject），按 SKILL § TDD 先修正再披露：
  修正后断言 = 退出码 2（argparse SystemExit 或 `FeedbackError` 两态皆收）+ 错误文本
  指名 `--package` + **不得**是 invalid choice（动作必须已注册），更名为
  `test_missing_package_flag_exit_2`。
- 修正后终跑真实输出尾部（节选）：

```text
__main__.py: error: argument --action: invalid choice: 'ingest-exec-quant' (choose from 'record', 'status', 'list', 'dispose', 'mark-submitted', 'reindex', 'package', 'cleanup', 'upstream', 'migrate-legacy', 'introspect-register', 'args-manifest')
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_action_is_registered
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_missing_package_flag_exit_2
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_no_payload_package_zero_difference
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_manifest_missing_records_still_ingested
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_manifest_corrupt_json_still_ingests
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_unreadable_and_wrong_kind_members_skipped
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_manifest_identity_missing_lands_unknown_project
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_unknown_project_status_lands_literal_group_no_guessing
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_identified_identity_slug_group_and_envelope_attribution
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_duplicate_ingest_idempotent
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_cross_package_overlap_dedup
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_same_identity_different_content_keep_first
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_dedup_and_write_share_one_flock_critical_section
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_envelope_files_entry_filename_form_and_no_residue
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_output_json_required_keys_and_types
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_nonexistent_package_file_exit_2
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_non_zip_file_exit_2
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_storage_unwritable_exit_2
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_feedback_store_untouched_no_contamination
FAILED tests/contract/test_feedback_intake_exec_quant.py::test_ingest_does_not_trigger_aggregate
20 failed in 2.19s
```

- 用例清单：上列 20 例（收集核对 `--collect-only` = 20），条款映射：C-10 →
  注册 + `--package` 必选（2 例）；C-11 → 无载荷零差异 + manifest 缺失/损坏降级 +
  单条不可解析/kind 不符（4 例）；C-12 → 身份缺失/unknown-project 字面分组零猜测 +
  identified slug 分组与信封归因（3 例）；C-13 → 同包幂等、跨包重叠去重、同 key
  异 content keep-first + `identity_conflicts`（F-01 后该分支可构造）、flock 单临界区
  （持锁线程阻塞断言）（4 例）；C-14 → 信封 `entry_filename()` 形态 + tmp 零残留、
  feedback store 零混入零触碰（3 例）；C-16 → 输出键集与退出码阶梯（缺包/非 zip/
  存储不可写 exit 2，降级 exit 0）（5 例，含交叉）；C-17 → 接收不触发 aggregate
  （1 例）；C-15 由信封 verbatim 断言覆盖。
- 失败归因：**subject 缺失**——20 例全部终止于 argparse 解析层
  `invalid choice: 'ingest-exec-quant'`（动作未注册），无一例触及存储写入；断言面
  除上述已披露修正的 1 例外无缺陷。红跑零副作用：全部夹具写入各自 `tmp_path`，
  仓库工作树仅新增两支测试文件（`git status` 核对，禁改面零命中）。

### part 3b 实现注意（本段红先测试钉住的接口形态）

- 动作注册：`_ACTIONS["ingest-exec-quant"]`；`--package` 必选（缺失 → exit 2，
  argparse required 或 `FeedbackError` 均可，测试两态兼容，但错误文本须指名
  `--package`）。
- 退出码阶梯：降级（manifest 缺失/损坏、单条跳过、identity_conflicts）exit 0；
  `--package` 文件缺失 / 非 zip / 聚合层不可写 exit 2。
- 分组目录：`aggregated/<source-slug>/records/`，slug = D5 形态；identity 缺失/
  `unknown-project` → 字面 `unknown-project` 组；锁文件 `aggregated/.write.lock`。
- 已知邻接守卫：`tests/contract/test_exec_quant_engine.py::
  test_packaging_quant_coupling_is_read_only` 钉「量化存储仅经
  `exec_quant_dir(` 只读定位器访问」——接收腿对 `aggregated/` 的写面若触发该钉，
  按 SKILL § TDD 断言/裁决归因处置（059 修订关系记录于 068 侧），属 3b 实现面。

---

# Implement Part 3c — US2 镜像同步与取证（T014 / T015，2026-10-22）

前置：T012/T013 已于 db0371a0 落地（US2 实现全绿 109 测试）；本段零引擎源编辑
（`scripts/python/feedback-utils.py` 源侧字节不变），仅镜像同步收口 + 取证。

## § T014 — scripts 对镜像同步（feedback-utils.py 编辑收口点）

- 命令 1（pre-write drift 记录）：`python3 scripts/python/sync-mirrors.py --check --only scripts`
  → 退出码 `2`；scripts 对 = 26 个 DIFF 文件，文件集与 T001 基线逐项一致
  （`notes/pre-change-measurements.md` §1 附录 A scripts 段）→ **零 NEW drift**。
- 命令 2（写入）：`python3 scripts/python/sync-mirrors.py --write --only scripts`
  → 退出码 `0`；`sync scripts/ -> .specify/scripts/ (26 files)`。
- 命令 3（复查）：`python3 scripts/python/sync-mirrors.py --check --only scripts`
  → 退出码 `0`；`ok scripts/ == .specify/scripts/ (109 files)`（scripts 对整体转净）。
- 命令 4（字节核对）：`cmp scripts/python/feedback-utils.py .specify/scripts/python/feedback-utils.py`
  → rc=0 字节一致；`cmp scripts/python/exec-quant.py .specify/scripts/python/exec-quant.py`
  → rc=0 字节一致（该对零 DIFF 与前提一致）。
- **drift 判定（相对 T001 基线）**：零 NEW drift。feedback-utils 对原有的 1 行继承
  DIFF（镜像侧 f265cfbd docstring 路径前缀）随字节同步消失，plan.md § Mirror
  Obligations 明示属预期、不算回归；基线内其余 25 个 scripts 对继承性路径前缀 DIFF
  亦随同对字节同步消失（同机制、同判据，不算回归）。零手改镜像（唯一写面 =
  sync-mirrors.py --write；`git status` 核对改动面恰为该 26 个镜像文件，零源侧文件
  入改动）。
- 同步后定向确认（canonical runner）：`bash scripts/bash/run-tests.sh
  tests/unit/test_feedback_intake_exec_quant.py tests/contract/test_feedback_intake_exec_quant.py
  tests/contract/test_exec_quant_engine.py -q` → 退出码 `0`；`87 passed in 20.56s`
  （镜像/源一致后 US2 两支 + 引擎契约仍全绿）。

## § T015 — 接收腿定向转绿与取证（US2 两支 + 邻接定向集）

- 命令：`bash scripts/bash/run-tests.sh tests/unit/test_feedback_intake_exec_quant.py
  tests/contract/test_feedback_intake_exec_quant.py tests/contract/test_exec_quant_engine.py
  tests/unit/test_feedback_package.py tests/unit/test_feedback_utils.py
  tests/contract/test_feedback_utils_cli.py -q`
- 退出码：`0`；输出尾部：`120 passed in 20.60s`（US2 两支 37 + 引擎契约 50 +
  邻接面 33，零跳过零失败——接收腿对 feedback 既有动作面零回归）。
- 本段零实现期失败归因（源侧零编辑；T012/T013 的失败归因已在 part 3b 完成）。

## § 独立可用性核验（快速启动场景 2/5 对应断言 — 已提交测试等价物）

- 命令：`bash scripts/bash/run-tests.sh
  tests/contract/test_feedback_intake_exec_quant.py::test_identified_identity_slug_group_and_envelope_attribution
  tests/contract/test_feedback_intake_exec_quant.py::test_duplicate_ingest_idempotent
  tests/contract/test_feedback_intake_exec_quant.py::test_feedback_store_untouched_no_contamination
  tests/contract/test_feedback_intake_exec_quant.py::test_no_payload_package_zero_difference -q`
- 退出码：`0`；`4 passed in 0.11s`。
- 断言映射：场景 2（接收归因 + 二次接收幂等 `ingested:0`/`duplicates_skipped` 全量 +
  `aggregated/<source-slug>/records/` 分组 + feedback store 零混入）→ 前三例；
  场景 5（无载荷等构包 `record_count:0`/`ingested:0` exit 0、聚合层目录零创建、
  feedback 条目处理零变化）→ 第 4 例。全部自构夹具，真实入站包
  `feedback/feedback-20261022T062525Z.zip` 与客户存储写面零触碰（场景 5 premise 原文）。


---

# Implement Part 4a — US3 汇总腿红先测试（T016 / T019，2026-10-22）

- 测试针对框架源 `scripts/python/exec-quant.py`（T016 经 `tests/script_api.py` 的
  `_load_module` 装载注册面 + subprocess 走引擎真实命令行，与
  `test_exec_quant_engine.py` 同形；T019 经同一装载器取 `exec_quant` 与
  `feedback_utils` 双引擎进程内跑链）。夹具全部自构（tmp_path 聚合层/客户存储），
  真实入站包、运行时记录、`.specify/` 镜像零触碰（红跑后 `git status` 核对：改动面
  恰为两支新测试文件）。
- 4b 实现注意（本段钉住的接口形态与读法裁决，逐条可溯源）：动作注册 = `ACTIONS`
  元组 + `ARG_MANIFEST["aggregate"]`（required=[]，C-18 零新增必需参数）；缺省
  `--format` 行为 = json；`skipped_unreadable` 以视图顶层 int 计数呈现（C-19 要求
  可观察；E7 字段表按「必需下限非封闭集」读法，同 C-16 平面计数先例）；视图顶层
  键集 = E7 六字段 ∪ {skipped_unreadable}，每源键集 = E7 七字段封闭（C-21
  不评估不打分的结构面）；coverage = 该源 quality 分布逐字段合计（D8「coverage
  汇总」，零字段词表可重放）；形态归一按形状规则统一执行——未知新字段携带合法
  `{value, provenance}` 形 → evaluated、裸 `[[STR-002]]`/缺键/未知形态 →
  not_evaluated（唯一同时满足记录法则两形态律、FR-013 零失真与 C-20 零硬编码的
  读法；「未知字段名一律 not_evaluated」的严格读法需要硬编码词表，弃）；CHK027
  空层 0/0 占比形态**未钉**（契约未定义，留给 4b 裁决），但零臆造数值守卫仍禁止
  空分母下的任何编造百分比。

## § T016 — `tests/contract/test_exec_quant_aggregate.py`（red-first）

- 命令：`bash scripts/bash/run-tests.sh tests/contract/test_exec_quant_aggregate.py -q`
- 退出码：`1`；`--collect-only` = 25
- 真实输出尾部（节选）：

```text
E       AssertionError: assert 'aggregate' in ('collect', 'list-records', 'score', 'collect-dispatch', 'args-manifest')
...（CLI 面 21 例统一终止于 argparse 层）
E       AssertionError: no stdout JSON (rc=2): usage: exec-quant.py [--action ...]
__main__.py: error: argument --action: invalid choice: 'aggregate' (choose from 'collect', 'list-records', 'score', 'collect-dispatch', 'args-manifest')
FAILED tests/contract/test_exec_quant_aggregate.py::test_action_registered_in_actions_and_arg_manifest
FAILED tests/contract/test_exec_quant_aggregate.py::test_args_manifest_covers_aggregate_flags
FAILED tests/contract/test_exec_quant_aggregate.py::test_aggregate_accepts_workspace_root_and_format_flags
FAILED tests/contract/test_exec_quant_aggregate.py::test_format_defaults_to_json
FAILED tests/contract/test_exec_quant_aggregate.py::test_format_text_face_runs
FAILED tests/contract/test_exec_quant_aggregate.py::test_consumes_aggregated_envelopes_grouped_by_source_project
FAILED tests/contract/test_exec_quant_aggregate.py::test_same_source_project_across_slug_dirs_merges
FAILED tests/contract/test_exec_quant_aggregate.py::test_local_records_and_scores_never_enter_view
FAILED tests/contract/test_exec_quant_aggregate.py::test_unreadable_envelopes_counted_non_blocking
FAILED tests/contract/test_exec_quant_aggregate.py::test_own_repo_source_has_same_rights
FAILED tests/contract/test_exec_quant_aggregate.py::test_view_projection_field_set_e7
FAILED tests/contract/test_exec_quant_aggregate.py::test_quality_shape_normalization
FAILED tests/contract/test_exec_quant_aggregate.py::test_unknown_field_with_measured_shape_is_shape_evaluated
FAILED tests/contract/test_exec_quant_aggregate.py::test_coverage_is_quality_distribution_total
FAILED tests/contract/test_exec_quant_aggregate.py::test_totals_and_store_digest_replayable
FAILED tests/contract/test_exec_quant_aggregate.py::test_every_number_replayable_from_record_files
FAILED tests/contract/test_exec_quant_aggregate.py::test_view_keys_are_closed_counter_projection
FAILED tests/contract/test_exec_quant_aggregate.py::test_no_fabricated_values_in_view
FAILED tests/contract/test_exec_quant_aggregate.py::test_product_lands_in_summaries_entry_form
FAILED tests/contract/test_exec_quant_aggregate.py::test_stdout_and_product_are_isomorphic
FAILED tests/contract/test_exec_quant_aggregate.py::test_rerun_appends_new_file_with_identical_numbers
FAILED tests/contract/test_exec_quant_aggregate.py::test_empty_aggregated_layer_zero_sources
FAILED tests/contract/test_exec_quant_aggregate.py::test_aggregate_writes_only_under_aggregated
23 failed, 2 passed in 1.21s
```

- 用例清单：上列 23 红 + 2 预绿守卫（`test_subject_is_framework_source_engine`：
  装载源自 `scripts/python/` 而非镜像——既有能力，红先期通过属预期；
  `test_engine_has_no_coupling_to_the_intake_path`：引擎源零 feedback 耦合的结构钉
  ——现状即真，其价值在 aggregate 落地后钉住「零接收触发路径」不被实现引入；
  行为面负例由 T011 `test_ingest_does_not_trigger_aggregate` 与 T019 链内断言覆盖）。
- 条款映射：C-18 → 注册/manifest/旗标/缺省 json/text 面（5 例）；C-19 → 消费面
  分组、跨 slug 同源合并、本地 records//scores/ 负例、信封不可读非阻塞、本仓同权
  （5 例）；C-20 → E7 字段集、形态归一、未知字段形状读法、coverage=quality 合计、
  totals+store_digest 重放、逐数字名单重放（6 例）；C-21 → 封闭键集 + 零臆造
  （2 例）；C-22 → 产物落盘/同构/重跑一致/空层（4 例）；C-23 → 零耦合结构钉 +
  产物仅落 aggregated/（2 例）。
- 失败归因：**subject 缺失**——23 例全部终止于 `aggregate` 未注册（argparse
  `invalid choice` → rc=2，或注册面断言 `assert 'aggregate' in ACTIONS`），无一例
  触及夹具数据或断言逻辑缺陷；断言面零修正。

## § T019 — `tests/integration/test_feedback_exec_quant_channel.py`（red-first，汇总链）

- 命令：`bash scripts/bash/run-tests.sh tests/integration/test_feedback_exec_quant_channel.py -q`
- 退出码：`1`（三轮同：首轮 6 failed、夹具修正两处后终跑仍 6 failed 但红因已归一）
- 真实输出尾部（节选）：

```text
E       assert (2 == 0)
E        +  where 2 = <_pytest.capture.CaptureFixture>.rb  # rc of EQ.main via _aggregate
assert rc == 0 and view is not None
FAILED tests/integration/test_feedback_exec_quant_channel.py::test_full_chain_two_sources_view_and_product
FAILED tests/integration/test_feedback_exec_quant_channel.py::test_same_package_double_ingest_zero_delta_and_rerun_consistent
FAILED tests/integration/test_feedback_exec_quant_channel.py::test_ingest_does_not_auto_aggregate_in_chain
FAILED tests/integration/test_feedback_exec_quant_channel.py::test_credential_scan_zero_hits_over_products_and_aggregate_layer
FAILED tests/integration/test_feedback_exec_quant_channel.py::test_chain_runs_with_sockets_blocked
FAILED tests/integration/test_feedback_exec_quant_channel.py::test_no_payload_isomorphic_package_full_chain_zero_diff
6 failed in 0.21s
```

- 用例清单（6 例，全部先走通 package/ingest 链再钉 aggregate）：全链双源视图与
  产物（≥2 源、unknown-project 字面组零猜测、双形态 3 条全携带、逐数字名单重放、
  stdout 与落盘同构、store_digest 4/4）；同包双收幂等（`ingested:0` /
  `duplicates_skipped` 全量、聚合层字节零增量、重跑新文件旧件零改写、数字一致）；
  链内接收零自动汇总（C-17/C-23 行为负例：两次 ingest 后 summaries 为空）；凭据
  零出现（对聚合层 + summaries 产物 + 包成员跑凭据型变量名/字面值扫描，命中 0）；
  全链零网络（socket.socket/create_connection/getaddrinfo 全部改为 raise 后整链
  跑通）；无载荷等构包全链零差异（feedback 条目 + 零载荷包 → 聚合层字节零增量、
  汇总数字零变化、零新组）。
- 失败归因：
  1. 首轮 6 例中 2 例先折在**夹具缺陷**（SKILL § TDD 归因后修正并披露）：(a) package
     报告的 `zip` 是相对客户工作区的路径，`_package` 未按客户根解析 →
     `FileNotFoundError`；(b) 投递步撞名——两个客户包在同一秒内生成同名
     `feedback-<ts>.zip`，投递复制相互覆盖（alpha 指向的收件路径被 beta 内容覆盖
     → `ingested==1`）——投递命名加客户名前缀修正（真实收件箱语义：同名投递件
     从不静默互覆）。
  2. 修正后终态 6 例全部归因 **subject 缺失**：package/ingest 链节全部走通（包
     报告、双形态计数、归因、幂等断言通过），统一红在 `--action aggregate` 未注册
     （rc=2 invalid choice，view=None）。断言面除上述 2 处夹具修正外零缺陷。

---

# Implement Part 4b — US3 汇总腿实现（T017 / T018，2026-10-22）

## § 实现落点（scripts/python/exec-quant.py）

- 注册面：`ACTIONS` 元组追加 `aggregate`；`ARG_MANIFEST["aggregate"] =
  {required: [], source: ["--workspace-root", "--format"]}`（C-18 零新增必需
  参数；argparse parser 仍是旗标唯一事实源，`--action args-manifest` 自动覆盖
  ——实测 emit 含 aggregate 条目且旗标全部 live）。
- `--format` 缺省改为 per-action 解析：parser 的 `--format` 改为 `default=None`
  （parser 不再携带缺省面），`list-records` 缺省仍解析为 text（既有钉
  `test_text_is_the_default_form` 零变化），`aggregate` 缺省解析为 json
  （C-18 / 4a 钉）。旗标集合与 USAGE_LINE 零变化。
- 消费面（C-19）：`load_aggregated_envelopes` 只读
  `aggregated/**/records/*.json`（glob 复用 `RECORDS_DIR_NAME` 常量），本地
  `records/`/`scores/` 零进入；不可读信封（解析失败/非 dict/缺可用 `record`
  对象）计 `skipped_unreadable` 顶层 int，非阻塞。
- 视图投影（C-20/E7）：按信封 `source_project` 分组（本仓同权零特判；缺/空
  归因落字面 `unknown-project` 组，同 E6 惯例）；`identity_status` 取该组文件
  名序首信封的投影；`units`/`quality`/`coverage`/`record_files[]` 全部可由
  名单重放；形态归一按形状规则统一（`{"value",…}` 对象 → evaluated；裸
  `[[STR-002]]`/缺键/未知形态 → not_evaluated；字段宇宙 = 观测键并集，零硬
  编码词表）。
- 4b 裁决（4a 留白项）：
  1. **空层 0/0 占比形态**（CHK027 未钉）：`totals.not_evaluated_ratio` 在
     分母为 0 时落 `null`（显式未评估），不落 0/不落任何编造百分比
     （FR-013「无数不编」与模块记录法则同构）；分母 > 0 时落未舍入浮点
     `not_evaluated_total/slots`（与重放守卫的 allowed 集合逐位相等）。
  2. **store_digest.record_files_total 口径**：聚合层探得的信封文件总数
     （可读 + skipped_unreadable；「信封文件总数」的字面读法）；
     `identity_keys_total` = 可读信封 distinct identity_key 数。
  3. **缺 `aggregation_envelope` 的可读信封**：按 C-19 封闭 unreadable 定义
     （非 dict、缺 record 键）不算不可读，归因落字面 `unknown-project` 组。
- 产物（C-22/C-23）：stdout 与落盘同一 dict 双出（同构）；`write_entry`
  （tmp+rename、`entry_filename()` 形态）落 `aggregated/summaries/`，一次
  运行一个新文件、旧文件零改写、append-only；text 面为同一视图的人工计数
  行（无新增数值面）；零网络零外发、写面仅 `aggregated/`（字节级快照测试
  核对）；引擎源与接收腿零耦合（结构钉维持）。

## § 绿证据（T017+T018 定向转绿）

- 命令：`bash scripts/bash/run-tests.sh tests/contract/test_exec_quant_aggregate.py -q`
- 退出码：`0`；`25 passed in 1.10s`（T016 的 23 红 + 2 预绿全部转绿）。
- 命令：`bash scripts/bash/run-tests.sh tests/integration/test_feedback_exec_quant_channel.py -q`
- 退出码：`0`；`6 passed in 0.16s`（T019 全链 6 例全部转绿）。
- 合并复跑（收尾单趟，含邻接）：`bash scripts/bash/run-tests.sh
  tests/contract/test_exec_quant_engine.py tests/contract/test_exec_quant_dispatch.py
  tests/contract/test_probe_engine_action_sets.py tests/contract/test_exec_quant_aggregate.py
  tests/integration/test_feedback_exec_quant_channel.py -q`
- 退出码：`0`；`125 passed in 34.09s`。
- 邻接套件（回归查询）：`tests/unit/test_feedback_intake_exec_quant.py` +
  `tests/contract/test_feedback_exec_quant_payload.py` +
  `tests/contract/test_engine_face_contract.py` → `58 passed`；三套件与上面
  合并趟零失败。`tests/contract/test_exec_quant_dispatch.py` 一并随合并趟绿。
- 全量套件未运行（按分段纪律，T023 名字级回归留后段）。

## § 断言/夹具修正披露（SKILL § TDD 归因；四处，零弱化）

1. **T016 `test_aggregate_writes_only_under_aggregated` 路径前缀断言缺陷**
   （红先期被 argparse 层红掩盖、4b 首绿跑暴露）：断言用 `startswith("aggregated")`
   比对相对工作区的快照路径，而本测试文件自身的 `_agg` helper 与 C-19/C-22、
   T019 的 `_aggregated` 都把聚合层钉在
   `.specify/memory/exec-quant/aggregated`——原前缀形态不可能满足（产物唯一
   合法落点即被判失败）。修正 = 前缀改为 store 内聚合层全相对路径；守卫意图
   （全部字节级变化落聚合层内 + 恰一产物）零变化，精确等值断言保留。
2. **T016 `test_quality_shape_normalization` 两处直读字面量与同测试自带重放
   oracle 矛盾**（红先期被注册面红掩盖）：`brand_new_axis`/`odd_future_form`
   直读期望 `not_evaluated: 1`（只有携带记录参与该字段分布的读法），而同测试
   `_replay_source` oracle、T019 同形 oracle、契约 C-20（「裸 `[[STR-002]]`
   或缺失键 → not_evaluated」逐记录语义）与 E7（「缺字段 = 显式 not_evaluated
   计数呈现」）均钉逐记录读法（缺键的兄弟记录计入 not_evaluated）；同断言块
   的 `tokens` 字面量（=2，含 r3 整键缺失）本身已采用逐记录读法——两处字面量
   连同文件自身 oracle 三方互斥，属期望形态笔误。修正 = 两处改为
   `not_evaluated: 3`（精确等值保留），未测槽位由此显式进入未测占比（FR-013
   零失真方向），非弱化。
3. **T019 两处夹具缺陷**（红先期被 aggregate 未注册的先行断言掩盖）：
   (a) `intake, rc = _ingest(...)` 对单 dict 返回的 helper 做元组解包
   （ValueError；同文件其余调用点均为单值赋值）→ 改单值赋值，后续断言键
   （`ingested`/`duplicates_skipped`/`record_count`）与接收腿报告实键核对一致；
   (b) gamma 的 feedback `record` 调用缺 `--unit-type` → 引擎按 063 C-23
   （一次性收集全部缺失必需旗标）rc=2 → 补 `--unit-type command`（兄弟集成
   测试同形约定），夹具从此走到它本来要验证的零载荷链。
4. **邻接守卫同批次修订（063 C-22 先例，C-18/C-10 契约授权）**：
   `tests/contract/test_exec_quant_engine.py` 的 `ACTIONS_CLOSED_SET` 与
   `tests/contract/test_probe_engine_action_sets.py` 的 exec-quant 期望集
   += `aggregate`（双向精确钉零放松）；同文件 `FEEDBACK_ALLOWED` +=
   `ingest-exec-quant`——该项为 **US2 段（db0371a0）欠下的同批修订**，4b 邻接
   巡检时发现其红（非本段引擎改动引入，HEAD 即红），按同一先例就地补齐并披露。

## § 遗留与边界

- `.specify/scripts/python/exec-quant.py` 镜像暂存预期 drift（本段按纪律零手改
  镜像；T021 `sync-mirrors.py --write --only scripts` 收口）。
- T020（定向绿证据追加 + stage-status 行）与 T021（镜像同步 + cmp）留给 4c 段；
  本段绿证据已按上列命令行/退出码/计数完整在案。

---

# part 4c — T020（US3 取证）与 T021（exec-quant scripts 镜像同步）

## § T020 — 汇总腿定向转绿与取证

- 命令（US3 两支，canonical runner）：`bash scripts/bash/run-tests.sh
  tests/contract/test_exec_quant_aggregate.py
  tests/integration/test_feedback_exec_quant_channel.py -q`
- 退出码：`0`；`31 passed in 1.13s`（aggregate 契约 25 + 集成链 6，全部绿）。
- 命令（邻接 5 支）：`bash scripts/bash/run-tests.sh
  tests/contract/test_exec_quant_engine.py tests/contract/test_exec_quant_dispatch.py
  tests/contract/test_probe_engine_action_sets.py
  tests/unit/test_feedback_intake_exec_quant.py
  tests/contract/test_feedback_exec_quant_payload.py -q`
- 退出码：`0`；`128 passed in 33.16s`（exec-quant 引擎 50 + dispatch + probe 动作集
  + US2 接收单元 17 + US1 载荷契约；邻接零回归）。
- 全量套件未运行（E2 baseline 槽已消耗，closure 名字级比对留 T023/后段）。

## § 独立可用性核验（快速启动场景 3 对应断言 — 已提交测试等价物）

quickstart.md 场景 3 明示钉住测试 = `tests/contract/test_exec_quant_aggregate.py`；
对应断言逐项转绿（31 例内的具名等价物）：

- ① 动作名 `aggregate` + `--format` 旗标（C-18）：`test_action_registered_in_actions_and_arg_manifest`、
  `test_args_manifest_covers_aggregate_flags`、`test_aggregate_accepts_workspace_root_and_format_flags`、
  `test_format_defaults_to_json`。
- ② 视图字段集合（C-20）：`test_view_projection_field_set_e7`、
  `test_quality_shape_normalization`、`test_coverage_is_quality_distribution_total`、
  `test_totals_and_store_digest_replayable`；`sources[]` 按源项目分组 =
  `test_consumes_aggregated_envelopes_grouped_by_source_project`。
- ③ 产物路径与形态（C-22，`aggregated/summaries/<id>.json`）：`test_product_lands_in_summaries_entry_form`、
  `test_stdout_and_product_are_isomorphic`、`test_rerun_appends_new_file_with_identical_numbers`。
- `record_files[]` 可对账（FR-011）：`test_every_number_replayable_from_record_files`。
- ≥2 源项目全链（含 `unknown-project` 组）= 集成测试
  `tests/integration/test_feedback_exec_quant_channel.py`（同趟 6 passed）。
- 显式动作边界（接收不自动汇总，C-23 负例）= `test_engine_has_no_coupling_to_the_intake_path`。

## § T021 — scripts 对镜像同步（exec-quant.py 编辑收口点）

- Pre-write 核验（判据基准 = T001 基线 `notes/pre-change-measurements.md` §1）：
  `python3 -u scripts/python/sync-mirrors.py --check --only scripts` → **26 DIFF**，
  文件集 = T001 基线 26 项中 `feedback-utils.py`（3c 已同步消失）由
  `exec-quant.py`（4b 源编辑的预期暂存 drift，即本段同步义务对象）替换，
  其余 25 项逐名与基线一致 = **相对基线零 NEW drift**。
- 写入：`python3 -u scripts/python/sync-mirrors.py --write --only scripts` →
  `sync  scripts/ -> .specify/scripts/ (26 files)`，退出码 `0`；零手改镜像。
- Post-write 复查：`--check --only scripts` → `ok scripts/ == .specify/scripts/
  (109 files)`，退出码 `0`（scripts 对内零 DIFF）。
- 字节核对：`cmp scripts/python/exec-quant.py
  .specify/scripts/python/exec-quant.py` → rc=0（一致）；`cmp
  scripts/python/feedback-utils.py .specify/scripts/python/feedback-utils.py` →
  rc=0（3c 同步状态保持）。
- 附带改动：`--only scripts` 写入同时重写了 25 个继承漂移镜像（T001 基线内
  既有 DIFF 的字节收敛）；按派发纪律仅提交 `.specify/scripts/python/exec-quant.py`，
  其余 25 个留工作树由驱动统一还原（与 3c 段同模式），镜像本体零手改。
- 同步后重跑 US3 定向集（合并 7 支单趟收尾）：`bash scripts/bash/run-tests.sh
  tests/contract/test_exec_quant_aggregate.py
  tests/integration/test_feedback_exec_quant_channel.py
  tests/contract/test_exec_quant_engine.py tests/contract/test_exec_quant_dispatch.py
  tests/contract/test_probe_engine_action_sets.py
  tests/unit/test_feedback_intake_exec_quant.py
  tests/contract/test_feedback_exec_quant_payload.py -q`
- 退出码：`0`；`159 passed in 34.20s`（= US3 31 + 邻接 128，镜像/源一致后仍全绿）。

# Implement Part 5 — US4 边界守卫（T022 / T023 / T024，2026-10-22）

> 本阶段是回归网（tasks.md Phase 5 头注）：T022/T024 守护三腿已实现行为，
> **非红先**，绿即通过；红则先归因（subject 回归 vs 断言缺陷）再处置，不得静默。
> T023 为既有套件名字级回归（FR-018/SC-006），判据基线 = 冻结的
> `test-evidence/log-baseline-pre-impl.txt`（3 failed / 544 passed）。

## § T022 — `tests/contract/test_exec_quant_channel_boundary.py`（回归网，绿）

- 命令（canonical runner）：`bash scripts/bash/run-tests.sh
  tests/contract/test_exec_quant_channel_boundary.py -q`
- 退出码：`0`；`11 passed in 0.55s`（-v 逐一核对：4 静态审计 + 2 运行面 +
  4 凭据链 + 1 常量钉，零 skip）。
- 守卫面（C-24 / C-25）：
  - 零网络断言 = 引擎源 AST 审查（`socket`/`urllib.request`/`requests`/`httpx`/
    `asyncio` 等 18 模块黑名单 + `subprocess.*` 常量命令面，`urllib.parse`
    白名单例外）+ 运行面观察（三腿全程 monkeypatch 屏蔽 `socket.socket`/
    `create_connection`/`getaddrinfo`/`threading.Timer`/`builtins.input`，
    线程集合前后相等，写路径全部落在两声明的 store 内）。
  - 「绿灯也是断言」自证：`test_network_audit_would_flag_a_violation` 用注入
    `import socket` / `subprocess.run(["curl",…])` 的对照样本证明审查器可转红。
  - 凭据零出现（SC-005）：模块级夹具用真 059 collector（host-CLI 伪装 wrapper，
    `ANTHROPIC_BASE_URL=https://user:pw@api.example.com/v1` 凭据形环境）产出
    记录，过 package → ingest-exec-quant → aggregate 全链；用引擎自带
    `CREDENTIAL_PATTERNS` 分别扫描打包 zip（逐成员）、`aggregated/` 层
    （除 summaries/）、`summaries/` 汇总产物 → 命中计数均 = 0；
    `user:pw` 哨兵全链零出现；端点值全程 origin-only（`https://api.example.com`）。
  - 059 遮蔽/封顶不削弱：`RECORD_SIZE_CAP_BYTES == 65536`、
    `MAX_PAYLOAD_RECORDS == 1000`、`MAX_PAYLOAD_BYTES == 16777216`、
    `CREDENTIAL_PATTERNS` 8 形态名、`ENDPOINT_ENV_NAMES` 9 名逐字钉。
  - 子句拆分保留：mark-submitted 归档 zip（068 前唯一外发产物）零
    `exec-quant/` 成员——手动打包腿是唯一可携带载荷的产物。
- 本段零 subject 失败；两次断言面缺陷就地修正并披露（SKILL § TDD）：
  ①zip 实际落点为 feedback store 内 `packages/`（非 workspace 根
  `packages/`），零外发断言的允许前缀按真实写面收紧；②`--action record`
  输出为 JSON+提示块混合文本，夹具改为不解析该输出（rc 断言即可）。两者均为
  新测试自身的断言缺陷，非三腿行为问题。

## § T024 — `tests/contract/test_exec_quant_channel_compat.py`（回归网，绿）

- 命令：`bash scripts/bash/run-tests.sh
  tests/contract/test_exec_quant_channel_compat.py -q`
- 退出码：`0`；`6 passed in 0.14s`（-v 核对零 skip；真实入站包参照测试实跑）。
- 守卫面（C-27/C-28/C-29/C-30）：
  - 无载荷等构包零差异：自构 068 前形态包（MANIFEST/条目/SUBMISSION-NOTES/
    introspection）→ `ingest-exec-quant` 全零计数 exit 0 零存储写入；真实包
    `feedback/feedback-20261022T062525Z.zip` 只读取参照（成员名派生等构包 +
    前后字节比对确认未触碰；文件缺失时 skip 兜底）。
  - 双空 → package 不产包且显式说明（note 同时点名 feedback 与 exec-quant）。
  - 三类并存全链：records/ 目录（schema v1+v2、`{value,provenance}` 与裸
    `not_evaluated`、未知顶层/quality 字段）+ 遗留 `records.jsonl`（含坏行）
    同仓打包 → 接收 → 汇总；`source_form_counts` 双计数、`skipped_unreadable=1`、
    遗留成员名 `legacy-records-L0001.json`；信封 record 逐字段等于原件
    （未知字段零丢弃）；D8 形态规则汇总（未知形态按未测计，coverage
    2/10 可重放）；源 store 快照前后字节相等（遗留单体流只读永不重写）。
  - 零新增阻断式确认门：`_DESTRUCTIVE_ACTIONS` 恰为 068 前六动作（零增长）、
    两引擎 parser 无 `--yes/--force/…` 同意旗标、`ARG_MANIFEST["aggregate"]
    ["required"] == []`、运行面屏蔽 `builtins.input` 三腿照常完成。
  - 存储分界：`aggregated/` 全仓唯一且恰在 `exec-quant/aggregated/`；feedback
    store 快照零变化且零 `[[STR-001]]`/量化单元 id/信封字样；两清点口径互不
    引用（feedback `list` count=1 不含量化记录；exec-quant `list-records`
    恰 1 条且相邻 `aggregated/` 信封不入清点、零 feedback 条目字样）。
- 本段零失败（首跑 `set()` 对 dict 不可哈希为断言面缺陷，改 JSON 正则形比对，
  就地修正并披露）。

## § T023 — 既有套件名字级回归（FR-018/SC-006）

- 命令（canonical runner，quickstart 场景 4 的 24 文件 feedback/exec-quant
  定向集）：`bash scripts/bash/run-tests.sh <24 文件集> -q --names-out
  test-evidence/log-current-post-impl-names.txt`（全量输出留存
  `test-evidence/log-regression-post-impl.txt`）。
- 退出码：`1`（pytest 原生结果）；**2 failed / 545 passed in 35.95s**
  （收集数 547 与基线 544+3=547 完全一致，零收集面变化）。
- 名字级比对（基线 = 冻结 `test-evidence/log-baseline-pre-impl.txt` 的
  3 个失败 nodeid 排序名单）：
  - `comm -13 baseline current` → **空**（零新增失败 nodeid，FR-018/SC-006
    判据满足）。
  - `comm -23 baseline current` → 1 条消失：
    `tests/contract/test_token_efficiency_feedback.py::test_cm2_engine_mirror_identical`
    —— 归因：该测试钉 `scripts/python/feedback-utils.py` 与其
    `.specify/scripts/python/` 镜像字节一致，part 3c 的 T014 scripts 对镜像
    同步已使该对收敛（预期转绿）。**既有镜像一致性失败的消失不算回归**
    （任务行明示判据）；余 2 个失败
    （`test_feedback_step_reference_form.py::test_owner_mirror_is_byte_identical`、
    `test_token_efficiency_feedback.py::test_cm1_mirror_identical`）与基线
    逐名相同，均为 feedback-step.md 镜像面既有漂移，T027 镜像同步的预期转绿对象。
- 两引擎既有动作面零语义变化核对（C-26）：
  - feedback `_ACTIONS` = 既有 12 动作（record/status/list/dispose/
    mark-submitted/reindex/package/upstream/cleanup/migrate-legacy/
    introspect-register/args-manifest）逐一在位 + 新增恰 1 个
    `ingest-exec-quant`；`_DESTRUCTIVE_ACTIONS` = 068 前六动作零增长；
    `args-manifest` 输出保持 12 动作面（其既有语义零变化，C-26 明示该动作
    输出零变化，故 ingest 不入该清单属契约一致而非缺漏；ingest 的
    `--package` 必填签名由 C-10 测试面钉住）。
  - exec-quant `ACTIONS` = 既有 5 动作（collect/list-records/score/
    collect-dispatch/args-manifest）逐一在位 + 按契约仅追加 `aggregate`
    （`ARG_MANIFEST["aggregate"]["required"] == []`）。
  - 既有动作语义零变化由本趟套件背书：545 passed 含
    test_feedback_utils_cli / test_feedback_package / test_feedback_utils /
    test_exec_quant_engine 等语义钉，零新增失败。
- 结论：**零新增失败 nodeid；唯一名单变化是既有镜像一致性失败的预期消失；
  真实回归：无。**

---

# Implement Part 6a — Polish 文档面/镜像收口（T025 / T026 / T027，2026-10-22）

> 本段为文档面与镜像收口（无新测试）；取证对象 = 引擎动作面对齐 + 镜像零 NEW
> drift + 24 文件集最终名字级比对。

## § T025 — 流程面文档（源侧 5 文件）

- `skills/internal/manage-feedback/SKILL.md`：Path execution 的 Path A 行补 A2
  exec-quant 载荷接收调用点（`ingest-exec-quant --package <zip>`，每包恰一次，
  降级计数知情；汇总至多是建议的显式后续步骤）。
- `references/path-a-digest.md`：A2 末新增「Exec-quant payload ingest」块——
  调用点、聚合层落点 `aggregated/<source-slug>/records/`、七键降级计数
  （record_count / ingested / duplicates_skipped / skipped_unreadable /
  identity_conflicts / groups_touched / manifest_unreadable）须入 digest 报告、
  降级 exit 0 / 调用不可执行 exit 2、无载荷零差异、幂等重收、**接收永不触发
  汇总**（`exec-quant.py --action aggregate` 仅建议为显式后续步骤）。
- `references/path-b-and-probe.md`：第 4 步 Package 补载荷面——全量包含（与条目
  时间过滤无关、零水位线）、引擎封顶（1000 条 / 16 MiB）触顶截断计数、降级
  非阻塞双报告面（text 与 `--format json`）与 MANIFEST § Exec-Quant Payload
  人读段（空载荷段照写声明无量化数据）、feedback 空 + 载荷非空仍产包
  （`Entries: 0` 显式）。
- `shared/workflow/feedback-step.md`：Threshold prompt § 1 package 段后补
  「Exec-quant payload awareness (068)」——载荷随包后的 wrap-up 观察面，指针形态
  （接收侧流程归 `/speckit.feedback` Path A § A2），零新增命令、零新增确认门、
  红线 3 不变（载荷只随同一个人手送 zip）。
- `templates/commands/feedback.md`：技能引用行同步（path-a-digest 行 + 
  path-b-and-probe 行），零新增命令、零新增确认门。
- 取值对齐核验：动作名/退出码/计数键逐项对照引擎实文——
  `feedback-utils.py --help` 动作面（13 动作，含 `ingest-exec-quant`；`--package`
  help 文本明示 ingest 必填）、`render_text` 的 ingest 文本面（无载荷措辞、
  "next: aggregate is a separate explicit action"）、`_intake_result` 七键、
  `exec-quant.py ACTIONS`（6 动作，含 `aggregate`）。零新增命令/确认门；
  059 制品零触碰。

## § T026 — 参考文档（docs/ 2 文件，无镜像义务）

- `docs/reference/commands/feedback.md`：A2 段新增载荷接收步骤（调用点、七键
  降级计数、退出码语义、零差异与幂等、接收不聚合 + `exec-quant.py --action
  aggregate` 动作名）；Path B 段新增载荷面（全量包含/封顶/降级计数/空载荷段/
  FR-019 双向）；Exit Codes 表 exit 2 行补 ingest 调用级失败三因 + 表后补
  「降级非 exit 2」说明段。
- `docs/reference/skills/feedback.md`：引擎动作表新增 `ingest-exec-quant` 行；
  Intake side 段新增「Exec-quant payload step (068, Path A § A2)」（每包恰一次
  调用点、降级计数、对 A5 清理安全性的意义、前置通道包零差异、汇总仅显式
  后续步骤）。
- 引擎动作名以代码为准核验：`_ACTIONS`（feedback-utils.py）与 `ACTIONS`
  （exec-quant.py）实值对照，文档与 `--help` 输出一致。

## § T027 — 镜像与逐工具副本收口

- `python3 -u scripts/python/sync-mirrors.py --write --only skills/internal`
  → `sync skills/internal/ -> .specify/skills/internal/ (75 files)`，rc=0；
  复查 `--check --only skills/internal` →
  `ok skills/internal/ == .specify/skills/internal/ (136 files)`，rc=0。
- `python3 -u scripts/python/sync-mirrors.py --write --only shared` →
  `sync shared/ -> .specify/shared/ (37 files)`，rc=0；复查
  `--check --only shared` → `ok shared/ == .specify/shared/ (51 files)`，rc=0。
- 判定：相对 T001 基线（skills/internal 75 DIFF / shared 37 DIFF，均为镜像侧
  路径前缀改写类既有漂移）**零 NEW drift**；既有 DIFF 随字节同步消失属预期
  （plan § Mirror Obligations 明示不算回归）。四个特性镜像文件逐对 `cmp`
  rc=0 字节一致：`.specify/skills/internal/manage-feedback/{SKILL.md,
  references/path-a-digest.md,references/path-b-and-probe.md}` 与
  `.specify/shared/workflow/feedback-step.md`。零手改镜像。
- `python3 -u scripts/python/regen-command-copies.py` → 恰好修复 4 个逐工具
  feedback 副本（.claude/commands/、.github/prompts/、.opencode/command/、
  .qoder/commands/ 各 1）；`--check` → `OK: all per-tool command copies match
  the source templates.`，rc=0。Codex 无独立命令目录（`.codex/commands` 不存在
  于本仓，regen 以现存目录为准），逐工具清单以脚本实跑输出为准。零手改副本。
- 预期转绿核验：
  `tests/contract/test_feedback_step_reference_form.py::test_owner_mirror_is_byte_identical`
  与 `tests/contract/test_token_efficiency_feedback.py::test_cm1_mirror_identical`
  → `2 passed`（与 T023 预测一致）。
- 24 文件集最终重跑（canonical runner，quickstart 场景 4 命令集）：
  **547 passed / 0 failed in 35.90s**，runner rc=0；失败名单
  `test-evidence/log-final-post-sync-names.txt` **0 条**。相对冻结基线
  （log-baseline-pre-impl.txt：3 failed / 544 passed）**零 NEW failing
  nodeid**（当前失败集为空）；T023 时余留的 2 个既有镜像一致性失败
  （owner_mirror_is_byte_identical / test_cm1_mirror_identical）如预测转绿，
  基线失败消失不算回归。收集数 547 与基线 544+3 一致，零收集面变化。
- 提交范围纪律：本段只提交特性相关镜像/副本（上列 4 镜像 + 4 逐工具副本）；
  `--write`/regen 附带改动的其余继承漂移镜像（108 个 `.specify/` 文件，
  `git status` 实数）留在工作树由驱动统一还原，不入本特性提交。
