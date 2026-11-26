# Verification Log — 108-team-view-degradation

<!--
  Derived spec-side at the review stage (2026-11-26) from
  `.specify/specs/108-team-view-degradation/test-evidence/verification-input.md` (the
  crew-side close-out input assembled by T029; tasks.md DoD-8 / GATE-4 declare that
  `verification.md` is derived here and MUST NOT be written by any crew seat).
  The implement stage delivered the input and never wrote this file.

  Derivation rules applied (every one disclosed, none changes a measured status or value):
  1. Status/value/note text is copied from the input's SC-NNN_status / SC-NNN_value /
     SC-NNN_note lines. The input's SC-NNN_command line is folded into the note so the
     producing command travels with the row.
  2. `smoke_command` carries the crew's command with a leading `env` prefix: the
     verification-log template forbids a bare leading VAR=value assignment in the
     recorded value, and `env` is the sanctioned way to keep the assignment while
     satisfying that rule (same form line 107 used). The exit code and evidence path are
     the crew's and were independently re-verified at review: the exact command (without
     `env`) was re-executed 2026-11-26 with exit 0 / 37 passed (review re-run capture
     `test-evidence/review-smoke.txt`).
  3. baseline_commit is the implement-entry commit from
     `test-evidence/implement-entry-readings.txt` (`implement_start_commit=`), the DoD-2
     comparison base; post_change_commit is the branch head at derivation time.
  4. THE KEY=VALUE BLOCK IS THE RECORD. A human table elsewhere would be a stale view;
     no such table is written here. Statuses are the ones the closure judgement accepted
     (run immediately after derivation; verdict copied into review.md § 2.4).
-->

# -- Baseline (recorded before the implement work changed the tree) --

baseline_commit=005437f72beef5deeb76b1bb45560a1ebeedb217
baseline_date=2026-11-26
baseline_branch=108-team-view-degradation

# -- Implementation results (implement stage, run r20261126T071500Z-108a) --

implementation_date=2026-11-26
post_change_commit=4262522f4e3eaeb4b0a8caac25f0e1c1211c5708

# -- Smoke test record (exactly one per feature) --

smoke_command=env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_team_view_degradation_contract.py tests/integration/test_team_view_degradation.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/108-team-view-degradation/notes/us3-green.txt

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=生产复现 fixture 一次 view 的「最近报告」= 解析时间戳最大者 `2026-11-25T140000Z-report.md`（normalized `20261125T140000Z`）；旧报告冒充最新次数 = 0（`20261124T074500Z-report.md` 与 `20261125T121924Z-93cc-stage.md` 均未成为最新）；报告/辅助样本分类命中率 = 5/5（4 report + 1 auxiliary）；残留行 `未识别（unrecognized）: 共 2 份；示例: 2026-10-06-S1-judgment-contract.md, 2026-10-07-progress-snapshot.md（省略 0）`（示例 2 ≤ 上限 3，省略数在位）；exit 5（report-recognition-uncertain）
SC-001_note=final path. tests/integration/test_team_view_degradation.py::test_production_replica_latest_is_the_parsed_maximum + ::test_auxiliary_artifact_never_becomes_latest; command `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "production_replica or auxiliary_artifact"` (2 passed in 6.48s, rc 0, record-time reading); evidence notes/quickstart-run.md § S-2, notes/us1-green.txt; re-verified in the review targeted run (test-evidence/review-targeted.txt, 149 passed).
SC-002_status=pass
SC-002_value=三团队命名复刻 fixture（13 份非标准可解析命名：5 × `YYYY-MM-DDThh-mm-ssZ-report.md` + 7 × `YYYY-MM-DDThhmmssZ-report.md` + 1 × `YYYYMMDDThhmmZ-report.md`）：运行报告状态 = `已列出（共 13 份…）`（≠ `为空` 且 ≠ `缺失`）；「最近报告」= `2026-09-17T11-54-53Z-report.md`（normalized `20260917T115453Z`）；识别覆盖率 = 13/13；exit 0
SC-002_note=final path. tests/integration/test_team_view_degradation.py::test_corpus_style_reports_are_recognized; command `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "corpus_style"` (1 passed in 6.45s, rc 0, record-time reading); evidence test-evidence/shape-change-guard.txt, notes/quickstart-run.md § S-3, notes/us1-green.txt; re-verified in the review targeted run.
SC-003_status=pass
SC-003_value=生产形态降级 fixture 一次 view exit 5，六个具名状态全部出现：绑定 `不可读（binding-missing: … carries no binding block…）`、goal 命名状态 + `/speckit.team modify` 与 `goal-utils.py migrate` 指针、矩阵 `形态异常（缺列: agent）`、`roster_delta` = `不可比对（not comparable）（原因：…）`、台账 `缺失（…；后果：无台账聚合计数、无非终态信号）`、脊柱 `按声明 pattern 不适用` + `operating-loops.md § 8`；frontmatter 成员 9/9；`/speckit.team modify` 出现 2 次（≥ 1）；编造零值/占位值 = 0
SC-003_note=final path. tests/integration/test_team_view_degradation.py::test_degraded_definition_names_every_state（及 C-301…C-305 六个节点）; command `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "degraded_definition_names_every_state"` (1 passed in 6.48s, rc 0, record-time reading); evidence notes/us2-green.txt § SC-003 six-state evidence, notes/quickstart-run.md § S-5; re-verified in the review targeted run.
SC-004_status=pass
SC-004_value=满足 FR-022 健康谓词的 fixture（goal 缺席与 goal: <slug> 两变体；三键 binding、两份紧凑命名报告、零辅助产物、零残留、agent 列、items.jsonl 一行、三件脊柱在位）：基线 `54c6efa8c` 程序与变更后程序 stdout 逐字节相同（机器 diff 行数 = 0）、退出码相同（0 = 0）；允许增量集合对该谓词输入 = ∅
SC-004_note=final path. tests/integration/test_team_view_degradation.py::test_healthy_fixture_is_byte_identical_to_the_baseline_program; command `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "healthy_fixture_is_byte_identical"` (1 passed in 6.82s, rc 0, record-time reading); evidence test-evidence/us3-guards.txt, notes/us3-green.txt § SC-004, notes/quickstart-run.md § S-1; re-verified in the review targeted run.
SC-005_status=pass
SC-005_value=降级原因→退出码映射 2/2 命中（engine-degraded → 5；report-recognition-uncertain → 5）；退出码集合外取值 = 0（源码闭集 `0/2/3/4/5`，观测值 ⊆ 闭集）；仅「缺失/为空」fixture 退出码 = 0（2/2：missing history 与 empty runs/）；`-h` / `--help` / `--version` 退出 0 且零写盘（3/3，fixture 快照差 = 0）
SC-005_note=supporting path. tests/contract/test_team_view_degradation_contract.py::test_reason_set_is_closed / ::test_exit_mapping_two_of_two / ::test_script_interface_stays_closed; command `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_team_view_degradation_contract.py -q -k "reason_set or exit_mapping or script_interface"` (3 passed, rc 0, within the 18-node contract run); evidence notes/us3-green.txt § SC-005, notes/quickstart-run.md § S-7.
SC-006_status=pass
SC-006_value=同一 fixture 上概览「最近运行」列与单团队「最近报告」解析时间戳一致率 = 100%（2/2，clean-team `20260102T000000Z`、residue-team `20260103T083000Z` + 行内 `（report-recognition-uncertain：残留 1）`，overview exit 0）；源码扫描报告识别/最新选择入口数 = 1（单一 `classify_runs` + 单一编译时间戳文法，调用点仅 `build_persistence` 与 `build_overview_row`），第二匹配入口出现数 = 0（`REPORT_NAME_RE` 已不存在）
SC-006_note=supporting path. tests/integration/test_team_view_degradation.py::test_overview_matches_single_view_and_discloses_uncertainty + tests/contract/test_team_view_degradation_contract.py::test_single_recognition_entry_source_scan; command `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py tests/contract/test_team_view_degradation_contract.py -q -k "overview_matches_single_view or single_recognition"` (2 passed, rc 0); evidence notes/us3-green.txt § SC-006, notes/quickstart-run.md § S-6 / S-7.
SC-007_status=pass
SC-007_value=健康、降级、概览三个场景各执行一次 view，前后 fixture 工作树 `{relative_path: sha256}` 快照一致：新增文件数 = 0、修改文件数 = 0、删除文件数 = 0（3/3 场景）
SC-007_note=supporting path. tests/integration/test_team_view_degradation.py::test_view_degradation_leaves_tree_byte_identical; command `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "leaves_tree_byte_identical"` (1 passed in 6.81s, rc 0); evidence test-evidence/us3-guards.txt, notes/us3-green.txt § SC-007.
SC-008_status=pass
SC-008_value=新增与既有相关测试经唯一入口一次执行退出码 = 0（定向集 149 passed, 0 failed）；相对 implement 入口基线 221 个 failed 名单 `comm -13` 新失败 = 0；FR 清单点名的全部形态均有测试承载（非标准命名、辅助产物、残留、不确定性、缺 binding、内联 goal、缺 agent 列、缺失产物、不可读报告、健康保真）
SC-008_note=supporting path. command `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_team_view_report_recognition.py tests/contract/test_team_view_degradation_contract.py tests/integration/test_team_view_degradation.py tests/unit/test_team_view_parsers.py tests/contract/test_team_view_program_contract.py tests/contract/test_team_view_command.py tests/integration/test_team_view_program.py -q --names-out .specify/specs/108-team-view-degradation/test-evidence/targeted-current-failed.txt` (149 passed in 7.01s, rc 0, record-time reading; names file 0 entries); evidence test-evidence/targeted-set.txt, test-evidence/targeted-current-failed.txt (0 entries), baseline-failed.txt (221 names, implement entry); re-run at review — test-evidence/review-targeted.txt, review-targeted-failed.txt (0 entries), `comm -13` new failures = 0.

# -- Joint acceptance (one row per `in-scope` runtime-stack row in requirements.md) --

RS-001_joint_acceptance=read program and all new tests run on CPython 3.11.11 (the >=3.8 signed-contract floor is exercised only at 3.11) through the single entry with zero third-party imports (T019 import-root audit green; pyproject.toml unchanged across 005437f72..HEAD)
RS-002_joint_acceptance=pytest 8.4.2 under /usr/local/bin/python3 runs the new contract/integration/unit tests through scripts/bash/run-tests.sh; record-time targeted set 149 passed rc 0, review re-run 149 passed rc 0; zero new failures against the 221-name implement-entry baseline
RS-003_joint_acceptance=new tests all execute through the single bash entry and the run exits 0 (record time: targeted-set.txt; review re-run: test-evidence/review-targeted.txt, rc 0); no interpreter-level test command was used
RS-004_joint_acceptance=binding and anchor facts are read only through the three declared goal-utils.py read actions (T019 source scan: engine_read actions == binding team / list / targets --list); `git diff --name-only 54c6efa8c..HEAD -- scripts/python/goal-utils.py` is empty (zero modification)
RS-005_joint_acceptance=in-scope engine verified by behaviour: healthy fixture stdout byte-identical to the 54c6efa8c baseline (S-1), degraded fixture hits the closed reason set and the 2/2 exit-5 map, `-h`/`--version` exit 0 with zero writes, one classify_runs and one compiled grammar; all pinned by the three new test files (review targeted run 149 passed, rc 0)

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=No task row is deferred (29/29 closed with [X]). SC rows are copied from test-evidence/verification-input.md; the smoke record's exit code and evidence path were re-verified at review by re-executing the smoke command (exit 0, 37 passed, test-evidence/review-smoke.txt). The review stage's own targeted re-run (149 passed, 0 new failure names) is the independent confirmation behind SC-001…SC-004 and SC-008. The provenience of SC-003's fixture states and the six-group additive assertion is notes/us2-green.txt; the healthy/read-only guard readings are test-evidence/us3-guards.txt.