# Verification — 079 Humanize Run Output（implement 收口）

<!-- Canonical machine-readable block (owner: templates/verification-log-template.md). -->

baseline_commit=35ff11bc
baseline_date=2026-10-30
baseline_branch=079-humanize-run-output

implementation_date=2026-10-31
post_change_commit=46394dd4

# -- Evidence records (owner: templates/verification-log-template.md) --
# One record per `pass` SC sample (SC-002/003/005/006/007/008/009/010).
# `evidence_path` is repo-relative; `evidence_sha256` is SHA-256 over the archived
# file's bytes (`shasum -a 256`); non-`pass` SCs (SC-001/SC-004) carry no record.
# Self-check readings: test-evidence/review-repair-binding-check.txt

sample_id=SC-002_quickstart_s1
evidence_path=.specify/specs/079-humanize-run-output/notes/quickstart-run.md
evidence_sha256=c67faa94fed563203653c22cea4c50ea07d4bcda69b708e6624f74880dcf7b9b
verdict=pass

sample_id=SC-003_quickstart_s2
evidence_path=.specify/specs/079-humanize-run-output/notes/quickstart-run.md
evidence_sha256=c67faa94fed563203653c22cea4c50ea07d4bcda69b708e6624f74880dcf7b9b
verdict=pass

sample_id=SC-005_quickstart_s4
evidence_path=.specify/specs/079-humanize-run-output/notes/quickstart-run.md
evidence_sha256=c67faa94fed563203653c22cea4c50ea07d4bcda69b708e6624f74880dcf7b9b
verdict=pass

sample_id=SC-006_wiring_inventory
evidence_path=.specify/specs/079-humanize-run-output/test-evidence/wiring-inventory-baseline.txt
evidence_sha256=867c9be042f75eb54394355ecba0eac01967d1b2fa35754cccf5db4e36f7a514
verdict=pass

sample_id=SC-007_implement_part4
evidence_path=.specify/specs/079-humanize-run-output/test-evidence/implement-part4-status.txt
evidence_sha256=6a5fbcc8991711c822fad995f2779329b66209ed4286d3126e713852585ac91b
verdict=pass

sample_id=SC-008_implement_part5
evidence_path=.specify/specs/079-humanize-run-output/test-evidence/implement-part5-status.txt
evidence_sha256=b2f25d0b6bd715efb072f6cdbbd17df4fb7eb90c794b181e78cddff453bb1744
verdict=pass

sample_id=SC-009_quickstart_s3_s7
evidence_path=.specify/specs/079-humanize-run-output/notes/quickstart-run.md
evidence_sha256=c67faa94fed563203653c22cea4c50ea07d4bcda69b708e6624f74880dcf7b9b
verdict=pass

sample_id=SC-010_implement_part4
evidence_path=.specify/specs/079-humanize-run-output/test-evidence/implement-part4-status.txt
evidence_sha256=6a5fbcc8991711c822fad995f2779329b66209ed4286d3126e713852585ac91b
verdict=pass

SC-001_status=partial
SC-001_value=五节 5/5 已证；dispatches 原生 1 不可复现，降级载体实跑取 0
SC-001_note=缺口：原生子代理派发腿（dispatches: 1）在本宿不可复现；降级载体 dispatches: 0 已真实执行。承载证据：notes/quickstart-run.md § S1、test_rp01_five_sections_in_order、test_ex21_dispatch_record_line、test_ex17_degraded_honesty、test_ex18_degraded_keeps_report_contract。

SC-002_status=pass
SC-002_value=结论一致 1/1；证据指针 L/L（L=报告 Evidence 条目数，全量可定位）；来源清单 read 1/1
SC-002_note=承载证据：notes/quickstart-run.md § S1 `## Evidence`、test_rp07_evidence_pointers、test_rp10_sources_read_list、test_rp16_no_fabrication。

SC-003_status=pass
SC-003_value=verdict: failure 1/1；banned_hits 0；失败证据 1/1
SC-003_note=承载证据：notes/quickstart-run.md § S2、test_rp05_conclusion_verdict、§ SC-003 封闭词表扫描（banned_hits=0）。

SC-004_status=partial
SC-004_value=零副作用 1/1；denied + aborted + 拒绝原因/未执行范围 2/2
SC-004_note=缺口：确认拒绝的运行腿 not-reproducible（无人值守无用户可拒）；夹具断言与零副作用已证。承载证据：tests/fixtures/humanize/run/denied/envelope.md、test_sc04_denied_no_side_effect、test_sc04_denied_verdict_and_scope。

SC-005_status=pass
SC-005_value=--inline 1/1；--file 1/1；裸文本被执行 1/1
SC-005_note=承载证据：notes/quickstart-run.md § S4 调用 A/B/C、test_cm01_content_mode_equivalence、test_ip05_routing_table_order。

SC-006_status=pass
SC-006_value=未分类 0（164 = 7+4+1+114+38）；活源 7/7；引擎 rc=0 2/2；冻结 38/38；命令 27；blocking_hits 0
SC-006_note=承载证据：本文件 § SC-006 闭环守卫、test-evidence/wiring-inventory-baseline.txt。

SC-007_status=pass
SC-007_value=无网络外发 1/1；无 --output 零写入 2/2；失败不重试 1/1
SC-007_note=承载证据：test_ex19_no_network_from_humanize、test_rp04_zero_write_default、notes/quickstart-run.md § Teardown、test_ex11_no_compensating_redispatch、test_ex12_failure_coordinates_no_retry。

SC-008_status=pass
SC-008_value=Implemented 3/3；详情含扩展记录；索引名称/描述已更新；门禁新增行 0
SC-008_note=承载证据：test_wc10_feature_062_status_held、test_wc11_feature_row_name_description、test_wc17_new_line_gate_zero。

SC-009_status=pass
SC-009_value=9/9（同现拒绝、active-run、output-occupied、nested-invocation、内容模式豁免、降级标记、无已知风险、下一步、空输出 none）
SC-009_note=承载证据：test_ip06_source_and_instruction_rejected、test_ip11_active_run_rejected、test_ip12_output_occupied_rejected、test_ip13_nested_invocation_rejected、test_ip15_content_mode_unreserved、test_ex17_degraded_honesty、test_rp09_no_known_risks_explicit、test_rp11_next_steps_or_none、test_rp07_evidence_pointers、notes/quickstart-run.md § S3/S5/S6/S7。

SC-010_status=pass
SC-010_value=12/12（三组注入样本 × 四项规则）
SC-010_note=承载证据：tests/fixtures/humanize/run/injection/、tests/fixtures/humanize/inline/s08-threat-inline.md、files/instruction-threat-file.md、test_cm06_injection_defense_both_modes、test_cm07_fidelity_both_modes、test_ex19_no_network_from_humanize。

deferred_tasks=
deferred_reason_summary=

notes=canonical 状态块；逐条证据正文见下方表格与 T031–T034 小节；证据目录 .specify/specs/079-humanize-run-output/test-evidence

**指针**：canonical 状态以上方 `SC-NNN_status=` 块为准；下方表格是逐条证据正文。

**Owner rows**: T031–T036（Polish）。本文件是 SC-001…SC-010 的唯一索引：每条 SC 一条状态行 + 证据路径，无一条留空。
**基线**: 契约基线提交 `35ff11bc`（A11 发现命令与全部 `git diff` 判据的参照物）；本段起点 `ecc8ac58`。
**日期**: 2026-10-31（系统日期已跨日，见 § 环境日期边界）。

---

## T031 — quickstart S1–S7 真实运行

全部真实输出、命令与退出码：`notes/quickstart-run.md`（owner）。本段复核其收口读数：

```console
$ ls -A .specify/.tmp/humanize/ | wc -l
0
```

- 占位 teardown 干净；`git status --porcelain` 无 `.specify/.tmp/humanize/` 残骸，唯一新增输出文件是 S7 B 显式要求的 `notes/report-sample.md`。
- S1 成功 / S2 失败 / S3 非动作 / S4 内容模式两入口 + 裸文本 / S5 A 同现拒绝、C 嵌套拒绝 / S6 A 确认缺失 / S7 B 写出报告、C 目标不可写：均以 `mode: in-session-degraded` 真实执行并记录。
- `not-reproducible in this host`（如实标注、以夹具断言替代）：S5 B 两会话并发、S6 B 用户拒绝确认（无人值守无用户可答）、S7 A 原生载体对照（本段不派发子代理）。

---

## T032 — 主契约套件与字节钉扎

来自 `test-evidence/implement-part4-status.txt`（owner），本段复核未回退：

```console
$ .venv/bin/python -m pytest -q tests/contract/test_humanize_command_surface.py tests/contract/test_stage_class_wiring.py
155 passed
```

`UNCHANGED_SHA256["humanize"]` 已按 079 模板重测为 `dd7c77ef…6bb4a27`（日期 2026-10-31，理由「模板已按 079 改写」）；`strip_wiring()` 剥后等于基线的判定形态保留，并由 T036 的 `test_wc13_stage_class_pin_remeasured` 对全部 `STAGE_STEMS` 复验。

---

## T033 — 冻结面与夹具集（WC-14、WC-15、WC-20）

### 九个冻结验证文件（名册/计数零变更，全部仍绿）

```console
$ .venv/bin/python -m pytest -q tests/contract/test_expression_gate_wiring.py tests/contract/test_expression_gates_doc.py \
    tests/contract/test_expression_compatibility.py tests/contract/test_flow_class_ledger.py \
    tests/contract/test_flow_class_correctness.py tests/contract/test_feedback_command_classification.py \
    tests/contract/test_migration_distribution.py tests/contract/test_run_skills_wiring.py \
    tests/contract/test_skill_layer_visibility_guards.py
131 passed, 1 warning in 7.83s
```

exit 0。九个文件与 `35ff11bc` 逐字节一致：`git diff --name-only 35ff11bc -- <九个文件>` 输出为空。

| 文件 | `def test_` 数 |
|------|----------------|
| `tests/contract/test_expression_gate_wiring.py` | 16 |
| `tests/contract/test_expression_gates_doc.py` | 18 |
| `tests/contract/test_expression_compatibility.py` | 16 |
| `tests/contract/test_flow_class_ledger.py` | 11 |
| `tests/contract/test_flow_class_correctness.py` | 7 |
| `tests/contract/test_feedback_command_classification.py` | 6 |
| `tests/contract/test_migration_distribution.py` | 18 |
| `tests/contract/test_run_skills_wiring.py` | 10 |
| `tests/contract/test_skill_layer_visibility_guards.py` | 4 |

### WC-20 的两个测试 id（实测，不靠「仍为 Simple」的口头声明）

```console
$ .venv/bin/python -m pytest "tests/contract/test_feedback_command_classification.py::test_simple_command_omits_feedback_step[humanize]" \
    "tests/contract/test_feedback_command_classification.py::test_table_covers_every_command_template" -v
tests/contract/test_feedback_command_classification.py::test_simple_command_omits_feedback_step[humanize] PASSED [ 50%]
tests/contract/test_feedback_command_classification.py::test_table_covers_every_command_template PASSED [100%]
2 passed, 1 warning in 0.07s
```

- `test_simple_command_omits_feedback_step[humanize]`：模板无 `## Feedback` 步（`feedback-utils.py` 标记缺席）。
- `test_table_covers_every_command_template`：027 分类表仍覆盖全部模板（含 humanize 行）。

### 运行夹具集（WC-15）

七类逐例存在（`tests/fixtures/humanize/run/`）：成功、失败、非动作、需确认（各 `envelope.md`）、嵌套（`instruction.txt`）、降级（`envelope.md`）、并发（`reservations/run-a.run`、`run-b.run`）；另有 `denied/envelope.md`、`injection/` 与 `governance/`。历史语料未改写：

```console
$ git diff --name-only 35ff11bc -- tests/fixtures/humanize ':(exclude)tests/fixtures/humanize/run'
（空）
```

---

## T034 — 门禁、名册与零运行时（WC-16、WC-17、WC-18、WC-19）

```console
$ ls templates/commands/*.md | wc -l
27
$ git diff --stat 35ff11bc -- src/specify_cli scripts
（空）
$ python3 scripts/python/flow-class-check.py --action lookup --unit-id "skill:humanize"
unit_id: skill:humanize
flow_class: expression
flow_type: null
source: ledger
marker: null
basis: reader-oracle
neutral: false
$ python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
compile-embeds --check: 75 units, zero drift
```

### 确认门预算（按新增行判定，WC-17）

```console
$ git diff 35ff11bc -- templates/commands skills docs shared 'templates/*.md' | grep '^+' | grep -v '^+++'
added_lines=390
$ <同一管道> 逐行对照 scan-confirmation-gates.py 的 BLOCKING_PATTERNS
blocking_hits=0
```

扫描面按 `scan-confirmation-gates.py` 的 `SCAN_DIRS` + `templates/*.md` 复算（去掉不在扫描面的 `docs`）：`added_lines=331`、`blocking_hits=0`。

| 读数 | 改动前基线（`test-evidence/gate-newline-baseline.txt`） | 本段实测 |
|------|--------------------------------------------------------|----------|
| `added_lines` | 0（plan 阶段未改接线文件） | 390（含 docs） / 331（扫描面） |
| `blocking_hits` | 0 | 0 |

工具自身整树读数（未作判据，仅记录）：`blocking confirmation gates: 27（destructive 20 / governance_kept 7）`，`violations 0`。

---

## SC 收口（SC-001…SC-010）

| SC | 状态 | 证据路径 |
|----|------|----------|
| **SC-001** | 部分达成（partial）（五节 5/5；派发记录的原生 `1` 腿受宿主限制，降级载体取 `0`） | `notes/quickstart-run.md` § S1（真实五节报告）；`tests/contract/test_humanize_command_surface.py::test_rp01_five_sections_in_order`、`test_ex21_dispatch_record_line`；降级腿 `test_ex17_degraded_honesty`、`test_ex18_degraded_keeps_report_contract` |
| **SC-002** | 达成（结论一致 1/1；证据指针 L/L；来源清单 1/1） | `notes/quickstart-run.md` § S1 `## Evidence`；`::test_rp07_evidence_pointers`、`::test_rp10_sources_read_list`、`::test_rp16_no_fabrication` |
| **SC-003** | 达成（`verdict: failure` 1/1；封闭词表扫描命中 0；失败证据 1/1） | `notes/quickstart-run.md` § S2；`::test_rp05_conclusion_verdict`；词表扫描见下 |
| **SC-004** | 部分达成（partial）（无副作用 1/1；`denied` + `aborted` + 拒绝原因/未执行范围 2/2）。运行腿 `not-reproducible`（无人值守无用户可拒），以夹具与契约断言承载 | `tests/fixtures/humanize/run/denied/envelope.md`；`::test_sc04_denied_no_side_effect`、`::test_sc04_denied_verdict_and_scope` |
| **SC-005** | 达成（`--inline` / `--file` 各 1/1；裸文本被执行 1/1） | `notes/quickstart-run.md` § S4 调用 A/B/C；`::test_cm01_content_mode_equivalence`、`::test_ip05_routing_table_order` |
| **SC-006** | 达成（①–⑤ 见下节闭环守卫） | 本文件 § SC-006 闭环守卫；`test-evidence/wiring-inventory-baseline.txt` |
| **SC-007** | 达成（无网络外发 1/1；无 `--output` 零写入 2/2；失败不重试 1/1） | `::test_ex19_no_network_from_humanize`、`::test_rp04_zero_write_default`；`notes/quickstart-run.md` § Teardown（`ls -A .specify/.tmp/humanize/` = 0、`git status --porcelain` 无新增）；`::test_ex11_no_compensating_redispatch`、`::test_ex12_failure_coordinates_no_retry` |
| **SC-008** | 达成（前后 `Implemented` 3/3；详情含扩展记录；索引名称/描述已更新；门禁新增行 0） | `::test_wc10_feature_062_status_held`、`::test_wc11_feature_row_name_description`、`::test_wc17_new_line_gate_zero`；`git diff 35ff11bc` 的 062 状态行为仅追加 |
| **SC-009** | 达成（9/9：同现拒绝、`active-run`、`output-occupied`、`nested-invocation`、内容模式豁免占位、降级标记、无已知风险、下一步、空输出 `none`） | `::test_ip06_source_and_instruction_rejected`、`::test_ip11_active_run_rejected`、`::test_ip12_output_occupied_rejected`、`::test_ip13_nested_invocation_rejected`、`::test_ip15_content_mode_unreserved`、`::test_ex17_degraded_honesty`、`::test_rp09_no_known_risks_explicit`、`::test_rp11_next_steps_or_none`、`::test_rp07_evidence_pointers`；运行读数 `notes/quickstart-run.md` § S3/S5/S6/S7 |
| **SC-010** | 达成（三组注入样本 × 四项规则 = 12/12） | `tests/fixtures/humanize/run/injection/`（运行模式指令注入、执行体回传注入）、`tests/fixtures/humanize/inline/s08-threat-inline.md` 与 `files/instruction-threat-file.md`（内容模式输入注入）；`::test_cm06_injection_defense_both_modes`、`::test_cm07_fidelity_both_modes`、`::test_ex19_no_network_from_humanize` |

### SC-003 封闭词表扫描（确定性，命中 0）

判据 owner：`requirements.md` § Failure Wording — Closed Banned Vocabulary（先按允许短语最长优先剥离，再匹配禁用词）。操作数 = S2 记录的 `## Conclusion` 正文（`verdict:` 行之外）：

```text
失败：指令以退出码 3 结束，未产生输出。
```

- 剥离允许短语后匹配 zh（`成功`/`完成`/`通过`）与 en（`success*`/`complete*`/`pass*`，词边界、大小写不敏感）
- **`banned_hits=0`**

---

## SC-006 闭环守卫

发现命令在基线提交上重跑、按 `requirements.md` § Wiring Surface — A11 Closed Set 的五类有序规则重新分类：

```console
$ git grep -l -i humanize 35ff11bc | wc -l
164
```

```text
live-source=7  derived-copy=4  mirror=1  dated-record=114  frozen-verification=38  unclassified=0
$ LC_ALL=C comm -3 <regenerated> <test-evidence/wiring-inventory-baseline.txt>
（空：comm3-lines=0）
```

| 腿 | 判据 | 实测 |
|----|------|------|
| ① 分类完备 | 未分类 = 0 | `0`；总数 164 = 7+4+1+114+38 |
| ② 活源类义务（L/L，L 实测重算） | 7 项各有归属 | `templates/commands/humanize.md`（WC-01…04）、`skills/external/humanize/**`（IP/EX/RP 组）、`docs/reference/commands/humanize.md`（WC-08/09）、两份契约测试（WC-12/13/14）、`.specify/memory/features.md` + `features/062.md`（WC-10/11） |
| ③ 派生副本与镜像 | 两个引擎 exit 0 | `regen-command-copies.py --check` → `OK: all per-tool command copies match the source templates.` rc=0；`sync-mirrors.py --check` → 六对全 `ok`（含 `skills/external/ == .specify/skills/ (408 files)`）rc=0 |
| ④ 冻结验证类补集 | 每个文件与基线逐字节一致（F/F，实测分母 38） | `git diff --quiet 35ff11bc -- <path>` 逐项：`identical=38`、`differing=0` |
| ⑤ 结构不变量 | 命令名册不变、门禁新增行 0 命中、Feature 062 状态不变 | 27 条模板；`blocking_hits=0`；062 `**Status**: Implemented`（见 T034） |

---

## 条款覆盖机器核对（T036 / WC-12）

```console
$ .venv/bin/python -m pytest "tests/contract/test_humanize_command_surface.py::test_wc12_clause_test_map_is_total" -v
tests/contract/test_humanize_command_surface.py::test_wc12_clause_test_map_is_total PASSED
1 passed
```

`clause-test-map=total`：88 条条款（IP 17 / EX 21 / RP 20 / CM 10 / WC 20）各在 § Contract Coverage Map 出现恰一次、各有非空测试名、每个名字可在主契约套件 / `test_stage_class_wiring.py` / `test_feedback_command_classification.py` 解析为函数（含参数化 id），或由 § Clause Test Waivers 的显式 waiver（含 reason / remedy / 证据槽）认领；反向无未认领的 `test_ip*` / `test_ex*` / `test_rp*` / `test_cm*` / `test_wc*` 函数。

T036 组整体读数：`17 passed`（WC-05…WC-20 与判定器），红先行与就地修正记录见 `notes/red-first-evidence.md` § T036。

---

## 阶段门留档

```console
$ python3 scripts/python/validate-tasks.py .specify/specs/079-humanize-run-output/tasks.md
PASS: .specify/specs/079-humanize-run-output/tasks.md — 0 error(s), 0 warning(s)   （rc=0）
$ python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/079-humanize-run-output --stage tasks --repo .
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=0 waived=0        （rc=0）
```

---

## 环境日期边界（非本特性失败，如实记录）

系统日期已跨到 2026-10-31，`tests/integration/test_expression_line_pilot.py` 的两条用例外红：`test_s4_the_delivered_document_passes_all_four_faces`、`test_the_pilot_line_runs_all_eight_rows_in_order`。原因是 077 的冻结夹具 `tests/fixtures/expression_line/doc.md` 第 8 行 `as-of 2026-10-30` 在 tmp 仓库提交日期 2026-10-31 下被判 `as-of-stale`。**与本特性无关**：本段不修改 077 的冻结夹具，也不把它计入本特性 new_failure。

## 未跑与限制（如实声明）

- 全量套件本段未重跑（E2 已在 implement 起点消耗；closure 由 review 后驱动执行）。
- 原生子代理派发腿（SC-001 的 `dispatches: 1`、S7 A）在本宿不可复现：本段授权不派发子代理，且宿主无原生通道时按降级载体真实执行。
- **quickstart「真实执行」的证据级别（F4，如实限定）**：`notes/quickstart-run.md` 中被真实执行的只是每条指令的内层命令（如 `python3 -c ...` 的退出码与 stdout）；`/speckit.humanize` 的解析、占位与五节报告装配**未作为端到端调用发生**，五节报告正文由实现者在同一会话内按 SKILL 规范撰写；宿主原生派发通道（`mode: subagent` / `dispatches: 1`）本段未实测。该限制与 **SC-001 的 partial**（原生派发腿不可复现、降级载体取 `dispatches: 0`）及 **SC-004 的 partial**（用户拒绝确认腿 `not-reproducible`，以夹具断言替代）一一对应，相关证据不得读作端到端执行的证明。
