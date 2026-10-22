# Red-First Evidence — 068 Exec-Quant Feedback Channel (implement part 2, US1)

红先取证纪律（tasks.md § Tests / owner `.specify/skills/internal/implement-feature/SKILL.md`
§ TDD / § Test runs）：每支新测试先以未实现状态运行并记录命令、真实输出、退出码与
用例清单。本文件按节追加（T004 → T005 → 绿证据），append-only。

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

