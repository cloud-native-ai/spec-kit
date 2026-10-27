# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `master` |
| **基准** | `8ab5e5a97090ce76b39ec87aeeb788f3170ed9e3` (`8ab5e5a9`) |
| **目标** | `5336c0574ab6de641cc7a99e31c005d91eaeecec` (`5336c057`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-10-27T13:04:47Z` |

## 变更概览

```
 .claude/commands/speckit.feedback.md               |   2 +-
 .claude/commands/speckit.improve.md                |   4 +-
 .claude/commands/speckit.review.md                 |   2 +
 .github/prompts/speckit.feedback.prompt.md         |   2 +-
 .github/prompts/speckit.improve.prompt.md          |   4 +-
 .github/prompts/speckit.review.prompt.md           |   2 +
 .opencode/command/speckit.feedback.md              |   2 +-
 .opencode/command/speckit.improve.md               |   4 +-
 .opencode/command/speckit.review.md                |   2 +
 .qoder/commands/speckit.feedback.md                |   2 +-
 .qoder/commands/speckit.improve.md                 |   4 +-
 .qoder/commands/speckit.review.md                  |   2 +
 .../records/20261027T091835013215Z-98675a85.json   |   1 +
 .../records/20261027T092936938951Z-54306103.json   |   1 +
 .../records/20261027T095403802726Z-129b7f05.json   |   1 +
 .../records/20261027T095404023158Z-571875a4.json   |   1 +
 .specify/memory/features.md                        |   4 +-
 .specify/memory/features/072.md                    |  86 +++
 .../20261027T091844Z-speckit-requirements.md       |  23 +
 .../feedback/20261027T092936Z-speckit-clarify.md   |  19 +
 .../feedback/20261027T095404Z-speckit-plan.md      |  19 +
 ...n-speckit-requirements-r20261027t061144z-a3e.md |  10 +-
 ...n-speckit-requirements-r20261027t091830z-072.md | 202 ++++++
 ...ion-speckit-clarify-r20261027t092832z-072clr.md | 204 ++++++
 ...n-skill-create-plan-r20261027t095352z-072pla.md | 200 ++++++
 ...ation-speckit-plan-r20261027t095352z-072plan.md | 200 ++++++
 .specify/scripts/python/feedback-utils.py          | 305 ++++++++-
 .specify/scripts/python/probe-utils.py             |   8 +-
 .specify/shared/guidelines/dogfooding.md           |   4 +-
 .../shared/workflow/self-improvement-workflow.md   |  17 +
 .../improve-skills/references/loop-playbook.md     |  18 -
 .specify/skills/internal/code-review/SKILL.md      |  13 +-
 .../code-review/scripts/git-delta-review.sh        | 257 ++++++-
 .specify/skills/internal/manage-feedback/SKILL.md  |  21 +-
 .../manage-feedback/references/path-a-digest.md    |  76 +++
 .specify/skills/internal/self-improvement/SKILL.md |   1 +
 .../baseline-failed.txt                            |  26 +
 .../checklists/client-feedback-loop.md             |  80 +++
 .../checklists/requirements.md                     |  42 ++
 .../contracts/cadence-and-metrics.md               |  44 ++
 .../contracts/capture-step.md                      |  56 ++
 .../contracts/client-identity-and-armed-state.md   |  38 ++
 .../contracts/client-improvement-loop.md           |  32 +
 .../contracts/digest-and-carriers.md               |  35 +
 .../contracts/red-lines-and-surfaces.md            |  47 ++
 .../coverage-baseline.txt                          | 497 ++++++++++++++
 .../072-client-self-improvement/data-model.md      | 162 +++++
 .../072-client-self-improvement/feature-ref.md     |  76 +++
 .../notes/compatibility-plan-c61.md                |  51 ++
 .../notes/pre-change-measurements.md               |  74 +++
 .../notes/quickstart-run.md                        | 737 +++++++++++++++++++++
 .../notes/red-first-evidence.md                    |  68 ++
 .specify/specs/072-client-self-improvement/plan.md | 151 +++++
 .../072-client-self-improvement/quickstart.md      |  97 +++
 .../072-client-self-improvement/requirements.md    | 316 +++++++++
 .../specs/072-client-self-improvement/research.md  |  69 ++
 .../specs/072-client-self-improvement/tasks.md     | 365 ++++++++++
 .../test-evidence/analyze-report.md                | 138 ++++
 .../test-evidence/analyze.jsonl                    |   1 +
 .../test-evidence/checklist-selfcheck.txt          |   7 +
 .../test-evidence/checklist.jsonl                  |   1 +
 .../test-evidence/clarify.jsonl                    |   1 +
 .../test-evidence/decomposition-check.json         |  12 +
 .../test-evidence/implement-stage-status.jsonl     |   9 +
 .../test-evidence/overlap-check.json               |  10 +
 .../test-evidence/part7-us6-guard-sweep.txt        |  29 +
 .../test-evidence/part8-final-targeted-run.txt     |  75 +++
 .../part8b-guard-sweep-correction.txt              |  25 +
 .../test-evidence/plan-gates.txt                   |  31 +
 .../test-evidence/plan.jsonl                       |   1 +
 .../test-evidence/pre-analyze-check.json           |  31 +
 .../test-evidence/pre-analyze-check.stderr         |   1 +
 .../test-evidence/pre-analyze-check.stdout         |   1 +
 .../test-evidence/run-determination-history.json   | 144 ++++
 .../test-evidence/t027-mirror-checks.txt           |  25 +
 .../test-evidence/t027-sync-mirrors-write.txt      |   9 +
 .../test-evidence/tasks-clause-coverage.txt        | 524 +++++++++++++++
 .../test-evidence/tasks-decomposition.json         |  12 +
 .../test-evidence/tasks-pre-analyze.json           | 381 +++++++++++
 .../test-evidence/tasks-pre-analyze.stderr         |   1 +
 .../test-evidence/tasks-pre-analyze.stdout         |   1 +
 .../test-evidence/tasks-validate.txt               |   1 +
 .../test-evidence/tasks.jsonl                      |   1 +
 .../test-evidence/validate-requirements.txt        |   9 +
 .../072-client-self-improvement/verification.md    | 110 +++
 docs/reference/commands/feedback.md                |  31 +
 docs/reference/commands/improve.md                 |  64 ++
 docs/reference/commands/review.md                  |  12 +-
 scripts/python/feedback-utils.py                   | 305 ++++++++-
 scripts/python/probe-utils.py                      |   8 +-
 shared/guidelines/dogfooding.md                    |   4 +-
 shared/workflow/self-improvement-workflow.md       |  17 +
 skills/internal/code-review/SKILL.md               |  13 +-
 .../code-review/scripts/git-delta-review.sh        | 257 ++++++-
 skills/internal/manage-feedback/SKILL.md           |  21 +-
 .../manage-feedback/references/path-a-digest.md    |  76 +++
 skills/internal/self-improvement/SKILL.md          |   1 +
 templates/commands/feedback.md                     |   2 +-
 templates/commands/improve.md                      |   4 +-
 templates/commands/review.md                       |   2 +
 tests/contract/test_client_armed_state.py          | 474 +++++++++++++
 tests/contract/test_client_capture.py              | 453 +++++++++++++
 tests/contract/test_client_guard_sweep.py          | 706 ++++++++++++++++++++
 tests/contract/test_client_improve_loop.py         | 557 ++++++++++++++++
 tests/contract/test_client_metrics.py              | 694 +++++++++++++++++++
 tests/contract/test_client_package_exclusion.py    | 470 +++++++++++++
 tests/contract/test_dogfooding_practice.py         |  40 +-
 tests/contract/test_expression_compatibility.py    |  44 ++
 tests/contract/test_probe_engine_action_sets.py    |   3 +
 tests/contract/test_probe_nonentity_catalog.py     |  50 ++
 tests/fixtures/client_project.py                   | 664 +++++++++++++++++++
 111 files changed, 11269 insertions(+), 80 deletions(-)
```

---

## Review 意见


### 🟢 [SUGGESTION] skills/internal/code-review/scripts/git-delta-review.sh

> capture 的 --unit 值语法正则 ^custom:[a-z0-9._-]+/[a-z0-9._-]+$ 比引擎侧 _CUSTOM_UNIT_RE（scripts/python/probe-utils.py:133, ^custom:[a-z0-9._/-]+$）更严：引擎/probe-inject 接受的 custom:myorg（无斜杠）或 custom:a/b/c（多斜杠）单元可以持有外部探针对象，但 capture 会把显式传入的这类单元判为 malformed 并给出具名 skip（零条目、不阻断，行为本身诚实）。而 cmd_capture 注释自称'与反馈/探针引擎的 _CUSTOM_UNIT_RE 同源闭合'，与事实不符。建议：要么由引擎 owner 把 _CUSTOM_UNIT_RE 收紧为文档化语法 custom:<owner>/<name>，要么 capture 放宽到引擎正则并另行校验 owner/name 非空；至少先修正'同源'注释。证据：git-delta-review.sh cmd_capture 的 =~ 行与注释行；probe-utils.py:133。

<sub>21:13:33</sub>


### ❓ [QUESTION] skills/internal/code-review/scripts/git-delta-review.sh

> 契约 C-19 写明 'the capture step always exits 0'（contracts/capture-step.md），但 cmd_capture 对未知选项与缺必填参数走 die2（退出 2，与脚本级 0/1/2 用法错误字母表一致）。组合路径下第五步以固定合法旗标调用、不可达，故仅是契约措辞与独立调用行为的张力：建议把 C-19 的 'always exits 0' 限定为采集失败路径（用法错误保留退出 2），或让 capture 对该情形也退 0 并出具名 skip 行。证据：capture-step.md C-19 与 git-delta-review.sh cmd_capture 的参数校验分支。

<sub>21:13:33</sub>


### 👍 [PRAISE] tests/fixtures/client_project.py

> 两顶帽子夹具设计（帽子谓词双向可证、构造拒绝在框架仓内落盘、引擎事实只从探针机读输出解析）与 probe 目录可达性的两面教义修复（根面或 .specify/ 面任一即可达 + 双缺负例测试 test_catalog_unreachable_when_both_faces_missing）正是 FR-029/C-58 要求的诚实验证形态，值得保留。

<sub>21:13:33</sub>


<!-- coverage-receipt:begin -->
receipt_version=1
base=8ab5e5a97090ce76b39ec87aeeb788f3170ed9e3
head=5336c0574ab6de641cc7a99e31c005d91eaeecec
base_source=explicit
renderer=text
changed_files=111
judged_files=28
skipped_files=83
gap_files=0
lines_added=11269
lines_deleted=80
file.001.path=.claude/commands/speckit.feedback.md
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.claude/commands/speckit.improve.md
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.claude/commands/speckit.review.md
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.github/prompts/speckit.feedback.prompt.md
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.github/prompts/speckit.improve.prompt.md
file.005.verdict=skipped
file.005.reason=generated
file.006.path=.github/prompts/speckit.review.prompt.md
file.006.verdict=skipped
file.006.reason=generated
file.007.path=.opencode/command/speckit.feedback.md
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.opencode/command/speckit.improve.md
file.008.verdict=skipped
file.008.reason=generated
file.009.path=.opencode/command/speckit.review.md
file.009.verdict=skipped
file.009.reason=generated
file.010.path=.qoder/commands/speckit.feedback.md
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.qoder/commands/speckit.improve.md
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.qoder/commands/speckit.review.md
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.specify/memory/exec-quant/records/20261027T091835013215Z-98675a85.json
file.013.verdict=skipped
file.013.reason=non-code-file
file.014.path=.specify/memory/exec-quant/records/20261027T092936938951Z-54306103.json
file.014.verdict=skipped
file.014.reason=non-code-file
file.015.path=.specify/memory/exec-quant/records/20261027T095403802726Z-129b7f05.json
file.015.verdict=skipped
file.015.reason=non-code-file
file.016.path=.specify/memory/exec-quant/records/20261027T095404023158Z-571875a4.json
file.016.verdict=skipped
file.016.reason=non-code-file
file.017.path=.specify/memory/features.md
file.017.verdict=skipped
file.017.reason=non-code-file
file.018.path=.specify/memory/features/072.md
file.018.verdict=skipped
file.018.reason=non-code-file
file.019.path=.specify/memory/feedback/20261027T091844Z-speckit-requirements.md
file.019.verdict=skipped
file.019.reason=non-code-file
file.020.path=.specify/memory/feedback/20261027T092936Z-speckit-clarify.md
file.020.verdict=skipped
file.020.reason=non-code-file
file.021.path=.specify/memory/feedback/20261027T095404Z-speckit-plan.md
file.021.verdict=skipped
file.021.reason=non-code-file
file.022.path=.specify/memory/session/20261027T062008Z-run-determination-speckit-requirements-r20261027t061144z-a3e.md
file.022.verdict=skipped
file.022.reason=non-code-file
file.023.path=.specify/memory/session/20261027T091825Z-run-determination-speckit-requirements-r20261027t091830z-072.md
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/memory/session/20261027T092926Z-run-determination-speckit-clarify-r20261027t092832z-072clr.md
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/memory/session/20261027T095352Z-run-determination-skill-create-plan-r20261027t095352z-072pla.md
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/memory/session/20261027T095352Z-run-determination-speckit-plan-r20261027t095352z-072plan.md
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/scripts/python/feedback-utils.py
file.027.verdict=reviewed
file.028.path=.specify/scripts/python/probe-utils.py
file.028.verdict=reviewed
file.029.path=.specify/shared/guidelines/dogfooding.md
file.029.verdict=skipped
file.029.reason=generated
file.030.path=.specify/shared/workflow/self-improvement-workflow.md
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/skills/improve-skills/references/loop-playbook.md
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/skills/internal/code-review/SKILL.md
file.032.verdict=skipped
file.032.reason=generated
file.033.path=.specify/skills/internal/code-review/scripts/git-delta-review.sh
file.033.verdict=skipped
file.033.reason=generated
file.034.path=.specify/skills/internal/manage-feedback/SKILL.md
file.034.verdict=skipped
file.034.reason=generated
file.035.path=.specify/skills/internal/manage-feedback/references/path-a-digest.md
file.035.verdict=skipped
file.035.reason=generated
file.036.path=.specify/skills/internal/self-improvement/SKILL.md
file.036.verdict=skipped
file.036.reason=generated
file.037.path=.specify/specs/072-client-self-improvement/baseline-failed.txt
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/specs/072-client-self-improvement/checklists/client-feedback-loop.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/specs/072-client-self-improvement/checklists/requirements.md
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/specs/072-client-self-improvement/contracts/cadence-and-metrics.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/specs/072-client-self-improvement/contracts/capture-step.md
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/specs/072-client-self-improvement/contracts/client-identity-and-armed-state.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/specs/072-client-self-improvement/contracts/client-improvement-loop.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/specs/072-client-self-improvement/contracts/digest-and-carriers.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/specs/072-client-self-improvement/contracts/red-lines-and-surfaces.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/specs/072-client-self-improvement/coverage-baseline.txt
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/specs/072-client-self-improvement/data-model.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/specs/072-client-self-improvement/feature-ref.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/specs/072-client-self-improvement/notes/compatibility-plan-c61.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/specs/072-client-self-improvement/notes/pre-change-measurements.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/specs/072-client-self-improvement/notes/quickstart-run.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/specs/072-client-self-improvement/notes/red-first-evidence.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/specs/072-client-self-improvement/plan.md
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/specs/072-client-self-improvement/quickstart.md
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/specs/072-client-self-improvement/requirements.md
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/specs/072-client-self-improvement/research.md
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/specs/072-client-self-improvement/tasks.md
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/specs/072-client-self-improvement/test-evidence/analyze-report.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/specs/072-client-self-improvement/test-evidence/analyze.jsonl
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/specs/072-client-self-improvement/test-evidence/checklist-selfcheck.txt
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/specs/072-client-self-improvement/test-evidence/checklist.jsonl
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/specs/072-client-self-improvement/test-evidence/clarify.jsonl
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/specs/072-client-self-improvement/test-evidence/decomposition-check.json
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/specs/072-client-self-improvement/test-evidence/implement-stage-status.jsonl
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/specs/072-client-self-improvement/test-evidence/overlap-check.json
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/specs/072-client-self-improvement/test-evidence/part7-us6-guard-sweep.txt
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/specs/072-client-self-improvement/test-evidence/part8-final-targeted-run.txt
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/072-client-self-improvement/test-evidence/part8b-guard-sweep-correction.txt
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/072-client-self-improvement/test-evidence/plan-gates.txt
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/072-client-self-improvement/test-evidence/plan.jsonl
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/072-client-self-improvement/test-evidence/pre-analyze-check.json
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/072-client-self-improvement/test-evidence/pre-analyze-check.stderr
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/072-client-self-improvement/test-evidence/pre-analyze-check.stdout
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/072-client-self-improvement/test-evidence/run-determination-history.json
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/072-client-self-improvement/test-evidence/t027-mirror-checks.txt
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/072-client-self-improvement/test-evidence/t027-sync-mirrors-write.txt
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/072-client-self-improvement/test-evidence/tasks-clause-coverage.txt
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/072-client-self-improvement/test-evidence/tasks-decomposition.json
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/072-client-self-improvement/test-evidence/tasks-pre-analyze.json
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/072-client-self-improvement/test-evidence/tasks-pre-analyze.stderr
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/072-client-self-improvement/test-evidence/tasks-pre-analyze.stdout
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/072-client-self-improvement/test-evidence/tasks-validate.txt
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/072-client-self-improvement/test-evidence/tasks.jsonl
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/072-client-self-improvement/test-evidence/validate-requirements.txt
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/072-client-self-improvement/verification.md
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=docs/reference/commands/feedback.md
file.086.verdict=reviewed
file.087.path=docs/reference/commands/improve.md
file.087.verdict=reviewed
file.088.path=docs/reference/commands/review.md
file.088.verdict=reviewed
file.089.path=scripts/python/feedback-utils.py
file.089.verdict=reviewed
file.090.path=scripts/python/probe-utils.py
file.090.verdict=reviewed
file.091.path=shared/guidelines/dogfooding.md
file.091.verdict=reviewed
file.092.path=shared/workflow/self-improvement-workflow.md
file.092.verdict=reviewed
file.093.path=skills/internal/code-review/SKILL.md
file.093.verdict=reviewed
file.094.path=skills/internal/code-review/scripts/git-delta-review.sh
file.094.verdict=reviewed
file.095.path=skills/internal/manage-feedback/SKILL.md
file.095.verdict=reviewed
file.096.path=skills/internal/manage-feedback/references/path-a-digest.md
file.096.verdict=reviewed
file.097.path=skills/internal/self-improvement/SKILL.md
file.097.verdict=reviewed
file.098.path=templates/commands/feedback.md
file.098.verdict=reviewed
file.099.path=templates/commands/improve.md
file.099.verdict=reviewed
file.100.path=templates/commands/review.md
file.100.verdict=reviewed
file.101.path=tests/contract/test_client_armed_state.py
file.101.verdict=reviewed
file.102.path=tests/contract/test_client_capture.py
file.102.verdict=reviewed
file.103.path=tests/contract/test_client_guard_sweep.py
file.103.verdict=reviewed
file.104.path=tests/contract/test_client_improve_loop.py
file.104.verdict=reviewed
file.105.path=tests/contract/test_client_metrics.py
file.105.verdict=reviewed
file.106.path=tests/contract/test_client_package_exclusion.py
file.106.verdict=reviewed
file.107.path=tests/contract/test_dogfooding_practice.py
file.107.verdict=reviewed
file.108.path=tests/contract/test_expression_compatibility.py
file.108.verdict=reviewed
file.109.path=tests/contract/test_probe_engine_action_sets.py
file.109.verdict=reviewed
file.110.path=tests/contract/test_probe_nonentity_catalog.py
file.110.verdict=reviewed
file.111.path=tests/fixtures/client_project.py
file.111.verdict=reviewed
<!-- coverage-receipt:end -->
