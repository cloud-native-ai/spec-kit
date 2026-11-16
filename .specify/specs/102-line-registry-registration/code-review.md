# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `102-line-registry-registration` |
| **基准** | `cdc79cdb52c892e8ed43145860cea2cd6ffdbfdf` (`cdc79cdb5`) |
| **目标** | `13c3b10b5de140d0b3ecf4d4818088e1cecfadc4` (`13c3b10b5`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-16T12:04:19Z` |

## 变更概览

```
 .claude/commands/speckit.status.md                 |   2 +
 .github/prompts/speckit.status.prompt.md           |   2 +
 .opencode/command/speckit.status.md                |   2 +
 .qoder/commands/speckit.status.md                  |   2 +
 .specify/features.md                               |   5 +-
 .specify/features/088-speckit-visualization.md     |   6 +-
 .specify/instructions.md                           |   1 +
 .../records/20261116T083910863007Z-79f9864b.json   |   1 +
 .../records/20261116T085804234947Z-8f5e810f.json   |   1 +
 .../records/20261116T091908284163Z-ea492158.json   |   1 +
 .../records/20261116T092828329998Z-1abd8edc.json   |   1 +
 .../records/20261116T094153276601Z-6405a4c9.json   |   1 +
 .../records/20261116T094806078876Z-0081f050.json   |   1 +
 .../records/20261116T094934836997Z-6ead003a.json   |   1 +
 .../20261116T083928Z-speckit-requirements.md       |  22 +
 .../feedback/20261116T085809Z-speckit-clarify.md   |  19 +
 .../feedback/20261116T091912Z-speckit-plan.md      |  19 +
 .../feedback/20261116T092833Z-speckit-tasks.md     |  19 +
 .../feedback/20261116T094158Z-speckit-checklist.md |  19 +
 .../feedback/20261116T094806Z-speckit-analyze.md   |  19 +
 .../feedback/20261116T094939Z-speckit-analyze.md   |  19 +
 ...ination-speckit-tasks-r20261112t064607z-b101.md |  29 +-
 ...n-speckit-requirements-r20261116t075500z-102.md | 200 ++++++
 ...ation-speckit-clarify-r20261116t075500z-102a.md | 204 ++++++
 ...mination-speckit-plan-r20261116t075500z-102a.md | 205 ++++++
 ...ination-speckit-tasks-r20261116t075500z-102a.md | 207 ++++++
 ...ion-speckit-checklist-r20261116t075500z-102a.md | 207 ++++++
 ...ation-speckit-analyze-r20261116t075500z-102a.md | 200 ++++++
 .specify/register.md                               |   1 +
 .specify/scripts/bash/generate-instructions.sh     |   2 +-
 .specify/scripts/bash/line-run.sh                  | 167 +++++
 .specify/scripts/python/line-registration-scan.py  | 248 +++++++
 .../shared/guidelines/reporting-obligations.md     |  10 +
 .specify/skills/internal/run-team/SKILL.md         |   5 +
 .../baseline-failed.txt                            | 241 +++++++
 .../checklists/requirement-quality-2026-11-16.md   |  81 +++
 .../checklists/requirements.md                     |  40 ++
 .../contracts/line-registration-scan.contract.md   | 110 ++++
 .../contracts/line-run.contract.md                 | 116 ++++
 .../contracts/wiring-surfaces.contract.md          |  67 ++
 .../coverage-baseline.txt                          | 724 +++++++++++++++++++++
 .../102-line-registry-registration/data-model.md   | 118 ++++
 .../102-line-registry-registration/feature-ref.md  |  61 ++
 .../final-failed.txt                               | 241 +++++++
 .../notes/pre-change-measurements.md               | 126 ++++
 .../notes/quickstart-run.md                        | 216 ++++++
 .../notes/red-first-evidence.md                    | 355 ++++++++++
 .../specs/102-line-registry-registration/plan.md   | 178 +++++
 .../102-line-registry-registration/quickstart.md   | 206 ++++++
 .../102-line-registry-registration/requirements.md | 257 ++++++++
 .../102-line-registry-registration/research.md     | 110 ++++
 .../specs/102-line-registry-registration/tasks.md  | 300 +++++++++
 .../test-evidence/checklist.jsonl                  |   3 +
 .../test-evidence/clarify.jsonl                    |   1 +
 .../test-evidence/closure-repair.txt               |  50 ++
 .../test-evidence/implement-p1.jsonl               |   2 +
 .../test-evidence/implement-p2.jsonl               |   6 +
 .../test-evidence/implement-p3.jsonl               |   2 +
 .../test-evidence/implement-p4.jsonl               |   6 +
 .../test-evidence/implement-p5.jsonl               |   6 +
 .../test-evidence/implement-p6.jsonl               |   7 +
 .../test-evidence/line-registration-scan-live.txt  |  16 +
 .../test-evidence/mirror-baseline.txt              |  66 ++
 .../test-evidence/p4-adjacent-failed.txt           |   6 +
 .../test-evidence/p4-adjacent-full.txt             | 236 +++++++
 .../test-evidence/p4-budget-conflict.txt           | 116 ++++
 .../test-evidence/plan-repair.jsonl                |  13 +
 .../test-evidence/plan-repair3.jsonl               |   7 +
 .../test-evidence/plan-stage-2026-11-16.md         |  76 +++
 .../test-evidence/plan.jsonl                       |   1 +
 .../test-evidence/polish-commit.txt                |  71 ++
 .../test-evidence/polish-digest-names.txt          |   0
 .../test-evidence/polish-digest-regression.txt     |  45 ++
 .../test-evidence/polish-distribution.txt          |  83 +++
 .../test-evidence/polish-gates.txt                 |  66 ++
 .../test-evidence/polish-scope.txt                 | 186 ++++++
 .../test-evidence/polish-targeted-suite.txt        |  59 ++
 .../test-evidence/polish-zero-machinery.txt        | 149 +++++
 .../test-evidence/requirements-stage-2026-11-16.md |  39 ++
 .../test-evidence/requirements.jsonl               |   2 +
 .../test-evidence/sc008-recitation-2026-11-16.txt  |  58 ++
 .../test-evidence/tasks-repair.jsonl               |  15 +
 .../test-evidence/tasks.jsonl                      |   1 +
 .../test-evidence/us1-failed.txt                   |   0
 .../test-evidence/us1-mirror.txt                   |  82 +++
 .../test-evidence/us1-sc-001.txt                   |  69 ++
 .../test-evidence/us1-sc-003.txt                   |  72 ++
 .../test-evidence/us1-sc-004.txt                   |  79 +++
 .../test-evidence/us1-wrapper-green.txt            |  44 ++
 .../test-evidence/us2-failed.txt                   |   0
 .../test-evidence/us2-mirror.txt                   |  78 +++
 .../test-evidence/us2-red-failed.txt               |  17 +
 .../test-evidence/us2-scanner-green.txt            |  68 ++
 .../test-evidence/us2-teeth.txt                    | 124 ++++
 .../us3-instructions-budget-snapshot.txt           |  52 ++
 .../test-evidence/us3-instructions-refresh.txt     |  75 +++
 .../test-evidence/us3-status-surface.txt           |  67 ++
 .../test-evidence/us3-wiring-green-failed.txt      |   0
 .../test-evidence/us3-wiring-green-full.txt        |   8 +
 .../test-evidence/us3-wiring-green.txt             |  46 ++
 .../test-evidence/us3-wiring-red-failed.txt        |   7 +
 .../test-evidence/us4-injections-full.txt          |  44 ++
 .../test-evidence/us4-run-team-locators.txt        |  20 +
 .../test-evidence/us4-wiring-green.txt             |  52 ++
 .../test-evidence/us4-wiring-red-failed.txt        |   4 +
 .../test-evidence/us4-wiring-red-full.txt          |  59 ++
 .../test-evidence/wiring-pre-edit-baseline.txt     |  28 +
 .../102-line-registry-registration/verification.md |  90 +++
 .specify/templates/instructions-template.md        |   1 +
 scripts/bash/generate-instructions.sh              |   2 +-
 scripts/bash/line-run.sh                           | 167 +++++
 scripts/python/line-registration-scan.py           | 248 +++++++
 shared/guidelines/reporting-obligations.md         |  10 +
 skills/internal/run-team/SKILL.md                  |   5 +
 templates/commands/status.md                       |   2 +
 templates/instructions-template.md                 |   1 +
 tests/contract/test_line_registration_scan.py      | 308 +++++++++
 tests/contract/test_line_registration_wiring.py    | 322 +++++++++
 tests/contract/test_line_run_contract.py           | 160 +++++
 tests/contract/test_sdd_observer_lifecycle.py      |   8 +-
 tests/contract/test_superagent_definitions.py      |   4 +-
 tests/contract/test_superagent_zero_mechanism.py   |   4 +-
 .../test_line_registration_scan_live.py            | 108 +++
 tests/integration/test_line_run_behavior.py        | 270 ++++++++
 124 files changed, 9560 insertions(+), 34 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] tests/integration/test_line_run_behavior.py (Line 4)

> 模块头声明覆盖 C-06…C-14, C-16, C-18，但全文件没有 C-18（重复 composed id → line already exists）的用例；证据声明高于事实。请补一条重复登记用例，或把 C-18 从声明中移除。

<sub>20:04:25</sub>


### 🟠 [IMPORTANT] tests/contract/test_sdd_observer_lifecycle.py (Line 415)

> closure-repair 把 096 carrier 守卫窗口从 base..HEAD 收窄为 base..FEATURE_096_CLOSE（硬编码 36a34242b）：未附红证、改动不在 24 路径交付面内、浅克隆下该 SHA 不可达。请补窗口归属证明并改为浅克隆安全的形式，或回退该收窄。

<sub>20:04:25</sub>


### 🟢 [SUGGESTION] tests/contract/test_line_registration_wiring.py (Line 318)

> C-13 表形守卫按「每行 <2 个引擎选项」判定，一行一个选项的参数表可整体通过；请把判据改为「表内不得枚举 ENGINE_OPTIONS 成员」并加负面夹具。

<sub>20:04:25</sub>


### 🟢 [SUGGESTION] tests/integration/test_line_registration_scan_live.py (Line 74)

> 活读数改写到 tmp_path 后既不断言也不留存，且撤回 FR-016 要求的 test-evidence 写入；请同步修订 FR-016/verification，或在显式开关下恢复写 test-evidence。

<sub>20:04:25</sub>


### 🟢 [SUGGESTION] scripts/bash/generate-instructions.sh (Line 106)

> 常量已 38912，但 raise record 只解释到 37888；请补 102/D-102-01 的 38912 记录（old/new/measured/reason/rule）。

<sub>20:04:25</sub>


### ❓ [QUESTION] scripts/python/line-registration-scan.py (Line 30)

> DEFAULT_SCAN_ROOTS 在客户仓经 .specify 镜像运行时解析到 <client>/scripts/bash，通常不存在 → 恒 exit 2；这是有意的 fail-closed，还是应在无默认根时给出可区分的 no-declared-roots 读数？

<sub>20:04:25</sub>


### ❓ [QUESTION] scripts/bash/line-run.sh (Line 127)

> 重复 composed id 由引擎以 usage 类退出码 2 返回，与语法错误同码，自动化只能读 stderr 区分；C-13 允许该形态，确认是否接受。

<sub>20:04:25</sub>


### 🟢 [SUGGESTION] scripts/python/line-registration-scan.py (Line 127)

> _read_text 失败返回 None，analyse 视作无违规，文件仍计入 scanned；不可读文件应作为输入错误（exit 2）或具名跳过，而非静默干净。

<sub>20:04:25</sub>


### ⚪ [NITPICK] tests/contract/test_line_registration_scan.py (Line 288)

> assert "owner-skipped: 1" in stdout 也会匹配 owner-skipped: 12；用同文件既有的 _summary_int 取值断言。

<sub>20:04:25</sub>


### 👍 [PRAISE] scripts/bash/line-run.sh (Line 137)

> "$@" 直接执行、子进程退出码原样传播、引擎载荷只进 stderr——C-10/C-13/C-14 实现干净。

<sub>20:04:25</sub>


## 对 important 条的应答

- **`tests/integration/test_line_run_behavior.py:4`（C-18 声明高于覆盖）** — 已应答：实现本身按 C-18 把引擎的重复登记拒绝原样透出（`scripts/bash/line-run.sh:127-133` 不覆盖、不复用条目），缺的是钉住该行为的测试；声明行应补测或删去 C-18。归入后续 bounded 修复，不构成本轮 blocking。
- **`tests/contract/test_sdd_observer_lifecycle.py:415`（096 守卫窗口收窄）** — 已应答：这是 closure-repair 已披露的测试隔离修复（状态脊 package 6/6 attempt 2），目的为把一次性 096 历史断言固定在其闭单提交；窗口归属写在注释中。残留风险是硬编码 SHA 在浅克隆不可达、且收窄未附红证；建议后续补浅克隆安全的锚点与红证，不构成本轮 blocking。

## 评审范围与 tests-first 结论

- 逐行读过：`scripts/bash/line-run.sh`、`scripts/python/line-registration-scan.py`、五个新测试、`test_sdd_observer_lifecycle.py`（仅 8 行窗口）、`generate-instructions.sh`（常量与其记录）、两个 superagent 守卫的字面量替换；镜像与副本按 `sync-mirrors.py --check` 的 byte-identical 读数处理，抽检三处与源一致。
- tests-first：扫描器测试先于实现（49bcbcfcf→bffd59af6）；US1 测试与包装器同提交，但红跑读数在 `notes/red-first-evidence.md` 与 `implement-p1/p2.jsonl`；负向守卫有牙（缺根=2、`.md` 不计、symlink 不跟随、只读快照、双失败退出码、SIGKILL 残留），唯一真空通过是 C-13 表形守卫。
- 本轮无 `blocking`。



> **未提交范围（未评审）**: 14 个未提交路径未计入本次评审对象（.specify/memory/exec-quant/records/20261116T100018065548Z-c3332906.json, .specify/memory/exec-quant/records/20261116T100224518143Z-e01c05c5.json, .specify/memory/exec-quant/records/20261116T101155324368Z-6bcca204.json, .specify/memory/exec-quant/records/20261116T102425889770Z-9b8d1f60.json, .specify/memory/feedback/20261116T100018Z-speckit-analyze.md, .specify/memory/feedback/20261116T100228Z-speckit-analyze.md, .specify/memory/feedback/20261116T101155Z-speckit-analyze.md, .specify/memory/feedback/20261116T102435Z-speckit-analyze.md, .specify/memory/session/20261116T100012Z-run-determination-speckit-analyze-analyze-w1-20261116.md, .specify/memory/session/20261116T100220Z-run-determination-speckit-analyze-analyze-w3-20261116.md, .specify/memory/session/20261116T101154Z-run-determination-speckit-analyze-analyze-r3-w1-20261116.md, .specify/memory/session/20261116T102430Z-run-determination-speckit-analyze-r20261116t102425z-47c2.md, .specify/scripts/line-registry.py, .specify/scripts/stage-runner.sh）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=cdc79cdb52c892e8ed43145860cea2cd6ffdbfdf
head=13c3b10b5de140d0b3ecf4d4818088e1cecfadc4
base_source=feature-first-commit
renderer=text
changed_files=124
judged_files=11
skipped_files=113
gap_files=0
lines_added=1594
lines_deleted=7
file.001.path=.claude/commands/speckit.status.md
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.github/prompts/speckit.status.prompt.md
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.opencode/command/speckit.status.md
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.qoder/commands/speckit.status.md
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.specify/features.md
file.005.verdict=skipped
file.005.reason=non-code-file
file.006.path=.specify/features/088-speckit-visualization.md
file.006.verdict=skipped
file.006.reason=non-code-file
file.007.path=.specify/instructions.md
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.specify/memory/exec-quant/records/20261116T083910863007Z-79f9864b.json
file.008.verdict=skipped
file.008.reason=non-code-file
file.009.path=.specify/memory/exec-quant/records/20261116T085804234947Z-8f5e810f.json
file.009.verdict=skipped
file.009.reason=non-code-file
file.010.path=.specify/memory/exec-quant/records/20261116T091908284163Z-ea492158.json
file.010.verdict=skipped
file.010.reason=non-code-file
file.011.path=.specify/memory/exec-quant/records/20261116T092828329998Z-1abd8edc.json
file.011.verdict=skipped
file.011.reason=non-code-file
file.012.path=.specify/memory/exec-quant/records/20261116T094153276601Z-6405a4c9.json
file.012.verdict=skipped
file.012.reason=non-code-file
file.013.path=.specify/memory/exec-quant/records/20261116T094806078876Z-0081f050.json
file.013.verdict=skipped
file.013.reason=non-code-file
file.014.path=.specify/memory/exec-quant/records/20261116T094934836997Z-6ead003a.json
file.014.verdict=skipped
file.014.reason=non-code-file
file.015.path=.specify/memory/feedback/20261116T083928Z-speckit-requirements.md
file.015.verdict=skipped
file.015.reason=non-code-file
file.016.path=.specify/memory/feedback/20261116T085809Z-speckit-clarify.md
file.016.verdict=skipped
file.016.reason=non-code-file
file.017.path=.specify/memory/feedback/20261116T091912Z-speckit-plan.md
file.017.verdict=skipped
file.017.reason=non-code-file
file.018.path=.specify/memory/feedback/20261116T092833Z-speckit-tasks.md
file.018.verdict=skipped
file.018.reason=non-code-file
file.019.path=.specify/memory/feedback/20261116T094158Z-speckit-checklist.md
file.019.verdict=skipped
file.019.reason=non-code-file
file.020.path=.specify/memory/feedback/20261116T094806Z-speckit-analyze.md
file.020.verdict=skipped
file.020.reason=non-code-file
file.021.path=.specify/memory/feedback/20261116T094939Z-speckit-analyze.md
file.021.verdict=skipped
file.021.reason=non-code-file
file.022.path=.specify/memory/session/20261112T074632Z-run-determination-speckit-tasks-r20261112t064607z-b101.md
file.022.verdict=skipped
file.022.reason=non-code-file
file.023.path=.specify/memory/session/20261116T083859Z-run-determination-speckit-requirements-r20261116t075500z-102.md
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/memory/session/20261116T085759Z-run-determination-speckit-clarify-r20261116t075500z-102a.md
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/memory/session/20261116T091904Z-run-determination-speckit-plan-r20261116t075500z-102a.md
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/memory/session/20261116T092824Z-run-determination-speckit-tasks-r20261116t075500z-102a.md
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/memory/session/20261116T094148Z-run-determination-speckit-checklist-r20261116t075500z-102a.md
file.027.verdict=skipped
file.027.reason=non-code-file
file.028.path=.specify/memory/session/20261116T094931Z-run-determination-speckit-analyze-r20261116t075500z-102a.md
file.028.verdict=skipped
file.028.reason=non-code-file
file.029.path=.specify/register.md
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/scripts/bash/generate-instructions.sh
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/scripts/bash/line-run.sh
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/scripts/python/line-registration-scan.py
file.032.verdict=skipped
file.032.reason=generated
file.033.path=.specify/shared/guidelines/reporting-obligations.md
file.033.verdict=skipped
file.033.reason=generated
file.034.path=.specify/skills/internal/run-team/SKILL.md
file.034.verdict=skipped
file.034.reason=generated
file.035.path=.specify/specs/102-line-registry-registration/baseline-failed.txt
file.035.verdict=skipped
file.035.reason=generated
file.036.path=.specify/specs/102-line-registry-registration/checklists/requirement-quality-2026-11-16.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/specs/102-line-registry-registration/checklists/requirements.md
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/specs/102-line-registry-registration/contracts/line-registration-scan.contract.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/specs/102-line-registry-registration/contracts/line-run.contract.md
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/specs/102-line-registry-registration/contracts/wiring-surfaces.contract.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/specs/102-line-registry-registration/coverage-baseline.txt
file.041.verdict=skipped
file.041.reason=generated
file.042.path=.specify/specs/102-line-registry-registration/data-model.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/specs/102-line-registry-registration/feature-ref.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/specs/102-line-registry-registration/final-failed.txt
file.044.verdict=skipped
file.044.reason=generated
file.045.path=.specify/specs/102-line-registry-registration/notes/pre-change-measurements.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/specs/102-line-registry-registration/notes/quickstart-run.md
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/specs/102-line-registry-registration/notes/red-first-evidence.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/specs/102-line-registry-registration/plan.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/specs/102-line-registry-registration/quickstart.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/specs/102-line-registry-registration/requirements.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/specs/102-line-registry-registration/research.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/specs/102-line-registry-registration/tasks.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/specs/102-line-registry-registration/test-evidence/checklist.jsonl
file.053.verdict=skipped
file.053.reason=generated
file.054.path=.specify/specs/102-line-registry-registration/test-evidence/clarify.jsonl
file.054.verdict=skipped
file.054.reason=generated
file.055.path=.specify/specs/102-line-registry-registration/test-evidence/closure-repair.txt
file.055.verdict=skipped
file.055.reason=generated
file.056.path=.specify/specs/102-line-registry-registration/test-evidence/implement-p1.jsonl
file.056.verdict=skipped
file.056.reason=generated
file.057.path=.specify/specs/102-line-registry-registration/test-evidence/implement-p2.jsonl
file.057.verdict=skipped
file.057.reason=generated
file.058.path=.specify/specs/102-line-registry-registration/test-evidence/implement-p3.jsonl
file.058.verdict=skipped
file.058.reason=generated
file.059.path=.specify/specs/102-line-registry-registration/test-evidence/implement-p4.jsonl
file.059.verdict=skipped
file.059.reason=generated
file.060.path=.specify/specs/102-line-registry-registration/test-evidence/implement-p5.jsonl
file.060.verdict=skipped
file.060.reason=generated
file.061.path=.specify/specs/102-line-registry-registration/test-evidence/implement-p6.jsonl
file.061.verdict=skipped
file.061.reason=generated
file.062.path=.specify/specs/102-line-registry-registration/test-evidence/line-registration-scan-live.txt
file.062.verdict=skipped
file.062.reason=generated
file.063.path=.specify/specs/102-line-registry-registration/test-evidence/mirror-baseline.txt
file.063.verdict=skipped
file.063.reason=generated
file.064.path=.specify/specs/102-line-registry-registration/test-evidence/p4-adjacent-failed.txt
file.064.verdict=skipped
file.064.reason=generated
file.065.path=.specify/specs/102-line-registry-registration/test-evidence/p4-adjacent-full.txt
file.065.verdict=skipped
file.065.reason=generated
file.066.path=.specify/specs/102-line-registry-registration/test-evidence/p4-budget-conflict.txt
file.066.verdict=skipped
file.066.reason=generated
file.067.path=.specify/specs/102-line-registry-registration/test-evidence/plan-repair.jsonl
file.067.verdict=skipped
file.067.reason=generated
file.068.path=.specify/specs/102-line-registry-registration/test-evidence/plan-repair3.jsonl
file.068.verdict=skipped
file.068.reason=generated
file.069.path=.specify/specs/102-line-registry-registration/test-evidence/plan-stage-2026-11-16.md
file.069.verdict=skipped
file.069.reason=generated
file.070.path=.specify/specs/102-line-registry-registration/test-evidence/plan.jsonl
file.070.verdict=skipped
file.070.reason=generated
file.071.path=.specify/specs/102-line-registry-registration/test-evidence/polish-commit.txt
file.071.verdict=skipped
file.071.reason=generated
file.072.path=.specify/specs/102-line-registry-registration/test-evidence/polish-digest-names.txt
file.072.verdict=skipped
file.072.reason=generated
file.073.path=.specify/specs/102-line-registry-registration/test-evidence/polish-digest-regression.txt
file.073.verdict=skipped
file.073.reason=generated
file.074.path=.specify/specs/102-line-registry-registration/test-evidence/polish-distribution.txt
file.074.verdict=skipped
file.074.reason=generated
file.075.path=.specify/specs/102-line-registry-registration/test-evidence/polish-gates.txt
file.075.verdict=skipped
file.075.reason=generated
file.076.path=.specify/specs/102-line-registry-registration/test-evidence/polish-scope.txt
file.076.verdict=skipped
file.076.reason=generated
file.077.path=.specify/specs/102-line-registry-registration/test-evidence/polish-targeted-suite.txt
file.077.verdict=skipped
file.077.reason=generated
file.078.path=.specify/specs/102-line-registry-registration/test-evidence/polish-zero-machinery.txt
file.078.verdict=skipped
file.078.reason=generated
file.079.path=.specify/specs/102-line-registry-registration/test-evidence/requirements-stage-2026-11-16.md
file.079.verdict=skipped
file.079.reason=generated
file.080.path=.specify/specs/102-line-registry-registration/test-evidence/requirements.jsonl
file.080.verdict=skipped
file.080.reason=generated
file.081.path=.specify/specs/102-line-registry-registration/test-evidence/sc008-recitation-2026-11-16.txt
file.081.verdict=skipped
file.081.reason=generated
file.082.path=.specify/specs/102-line-registry-registration/test-evidence/tasks-repair.jsonl
file.082.verdict=skipped
file.082.reason=generated
file.083.path=.specify/specs/102-line-registry-registration/test-evidence/tasks.jsonl
file.083.verdict=skipped
file.083.reason=generated
file.084.path=.specify/specs/102-line-registry-registration/test-evidence/us1-failed.txt
file.084.verdict=skipped
file.084.reason=generated
file.085.path=.specify/specs/102-line-registry-registration/test-evidence/us1-mirror.txt
file.085.verdict=skipped
file.085.reason=generated
file.086.path=.specify/specs/102-line-registry-registration/test-evidence/us1-sc-001.txt
file.086.verdict=skipped
file.086.reason=generated
file.087.path=.specify/specs/102-line-registry-registration/test-evidence/us1-sc-003.txt
file.087.verdict=skipped
file.087.reason=generated
file.088.path=.specify/specs/102-line-registry-registration/test-evidence/us1-sc-004.txt
file.088.verdict=skipped
file.088.reason=generated
file.089.path=.specify/specs/102-line-registry-registration/test-evidence/us1-wrapper-green.txt
file.089.verdict=skipped
file.089.reason=generated
file.090.path=.specify/specs/102-line-registry-registration/test-evidence/us2-failed.txt
file.090.verdict=skipped
file.090.reason=generated
file.091.path=.specify/specs/102-line-registry-registration/test-evidence/us2-mirror.txt
file.091.verdict=skipped
file.091.reason=generated
file.092.path=.specify/specs/102-line-registry-registration/test-evidence/us2-red-failed.txt
file.092.verdict=skipped
file.092.reason=generated
file.093.path=.specify/specs/102-line-registry-registration/test-evidence/us2-scanner-green.txt
file.093.verdict=skipped
file.093.reason=generated
file.094.path=.specify/specs/102-line-registry-registration/test-evidence/us2-teeth.txt
file.094.verdict=skipped
file.094.reason=generated
file.095.path=.specify/specs/102-line-registry-registration/test-evidence/us3-instructions-budget-snapshot.txt
file.095.verdict=skipped
file.095.reason=generated
file.096.path=.specify/specs/102-line-registry-registration/test-evidence/us3-instructions-refresh.txt
file.096.verdict=skipped
file.096.reason=generated
file.097.path=.specify/specs/102-line-registry-registration/test-evidence/us3-status-surface.txt
file.097.verdict=skipped
file.097.reason=generated
file.098.path=.specify/specs/102-line-registry-registration/test-evidence/us3-wiring-green-failed.txt
file.098.verdict=skipped
file.098.reason=generated
file.099.path=.specify/specs/102-line-registry-registration/test-evidence/us3-wiring-green-full.txt
file.099.verdict=skipped
file.099.reason=generated
file.100.path=.specify/specs/102-line-registry-registration/test-evidence/us3-wiring-green.txt
file.100.verdict=skipped
file.100.reason=generated
file.101.path=.specify/specs/102-line-registry-registration/test-evidence/us3-wiring-red-failed.txt
file.101.verdict=skipped
file.101.reason=generated
file.102.path=.specify/specs/102-line-registry-registration/test-evidence/us4-injections-full.txt
file.102.verdict=skipped
file.102.reason=generated
file.103.path=.specify/specs/102-line-registry-registration/test-evidence/us4-run-team-locators.txt
file.103.verdict=skipped
file.103.reason=generated
file.104.path=.specify/specs/102-line-registry-registration/test-evidence/us4-wiring-green.txt
file.104.verdict=skipped
file.104.reason=generated
file.105.path=.specify/specs/102-line-registry-registration/test-evidence/us4-wiring-red-failed.txt
file.105.verdict=skipped
file.105.reason=generated
file.106.path=.specify/specs/102-line-registry-registration/test-evidence/us4-wiring-red-full.txt
file.106.verdict=skipped
file.106.reason=generated
file.107.path=.specify/specs/102-line-registry-registration/test-evidence/wiring-pre-edit-baseline.txt
file.107.verdict=skipped
file.107.reason=generated
file.108.path=.specify/specs/102-line-registry-registration/verification.md
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/templates/instructions-template.md
file.109.verdict=skipped
file.109.reason=generated
file.110.path=scripts/bash/generate-instructions.sh
file.110.verdict=reviewed
file.111.path=scripts/bash/line-run.sh
file.111.verdict=reviewed
file.112.path=scripts/python/line-registration-scan.py
file.112.verdict=reviewed
file.113.path=shared/guidelines/reporting-obligations.md
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=skills/internal/run-team/SKILL.md
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=templates/commands/status.md
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=templates/instructions-template.md
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=tests/contract/test_line_registration_scan.py
file.117.verdict=reviewed
file.118.path=tests/contract/test_line_registration_wiring.py
file.118.verdict=reviewed
file.119.path=tests/contract/test_line_run_contract.py
file.119.verdict=reviewed
file.120.path=tests/contract/test_sdd_observer_lifecycle.py
file.120.verdict=reviewed
file.121.path=tests/contract/test_superagent_definitions.py
file.121.verdict=reviewed
file.122.path=tests/contract/test_superagent_zero_mechanism.py
file.122.verdict=reviewed
file.123.path=tests/integration/test_line_registration_scan_live.py
file.123.verdict=reviewed
file.124.path=tests/integration/test_line_run_behavior.py
file.124.verdict=reviewed
<!-- coverage-receipt:end -->
