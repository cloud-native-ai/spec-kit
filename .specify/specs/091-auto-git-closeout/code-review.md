# code-review — 091-auto-git-closeout

> Code segment of `/speckit.review`. Judgment object: the committed code delta `base..head` under the
> six-level family owned by `.specify/skills/internal/code-review/SKILL.md` § Phase 3. This record is
> read by `git-delta-review.sh receipt` for the coverage block and by `report --summary --file` for the
> merge-gate verdict. Nothing here is converted into the `P0`/`P1`/`P2` family of the other segments.

renderer: text

| Field | Value |
|-------|-------|
| Base | `e06fcc52f5f4a3c4f025b49806451ed7c6cfbc33` (`base_source=feature-first-commit`) |
| Head | `85457d832d8fe5dbfc0a77685c5db9528a3ed2f8` (run-start HEAD) |
| Triage | `run` — code paths present in the delta |
| Changed files | 371 |
| Judged files | 371 (receipt `judged_files`; the 13 authored files carrying judgement are listed under § Findings) |
| Skipped / gap | 0 / 0 (receipt `skipped_files` / `gap_files`) |
| Uncommitted scope | disclosed, never concluded over: this review's own writes (`review.md`, `code-review.md`, `test-evidence/review-2026-11-09/`) are uncommitted at generation and excluded from the judged delta |

## Findings

### C1 — blocking — `tests/fixtures/git_closeout/plan.py:144`

The planner computes the role-filtered push target set and the executor discards it:

```python
targets = tuple(r for r in remotes if r not in set(readonly))
```
```python
target_remote = plan.targets[0] if plan.targets else None
…
remotes = [target_remote] if remote_name is None else [remote_name]
```

`targets[0]` is one remote; every other declared remote is dropped, and the read-only exclusion is only
observable in the planner, never on a repository. Fix: iterate `plan.targets`.

### C2 — blocking — `tests/contract/test_git_closeout_contract.py:577`

The SC-005 single-owner guard reds on the feature's own command-surface file (see `review.md` F5). A
guard whose green depends on the absence of a file the module's sibling test requires is not evidence.

### C3 — blocking — `tests/contract/test_git_closeout_contract.py:676`

No behavioural arm passes `remote_name=`; the `remote_name is None` branch is the only one exercised, so
C1 is structurally invisible. Every SC-001/SC-003 end-state claim rides on that single branch.

### C4 — important — `.specify/specs/091-auto-git-closeout/test-evidence/T062-smoke.txt:1`

The file holds `42 passed in 1.46s` and `EXIT=0` with no command line, so the smoke evidence cannot be
re-derived (see `review.md` F8).

### C5 — suggestion — `tests/contract/test_git_closeout_contract.py:1145`

`test_the_instruction_surface_reaches_the_step_without_restating_it` and
`test_the_hand_off_points_at_the_gate_owner_instead_of_restating_it` re-read `read()` on the same two
surfaces per assertion; a module-level `lru_cache` would make the 1471-line module ~30 % faster without
changing a claim.

### C6 — question — `tests/fixtures/git_closeout/repo.py:243`

`build_repo` leaves `__pycache__/` inside `tests/fixtures/git_closeout/`. Is fixture byte-code covered by
the repository's ignore policy, or should the fixture set `sys.dont_write_bytecode`? (see `review.md` F6)

## Gate verdict

`report --summary --file` → **blocking-unresolved** (3 blocking). The delta may not be merged on this
record until C1–C3 are repaired.

## Environment note (disclosed)

The skill's four-step non-interactive path (`base`/`triage`/`start`/`receipt`) could not execute through
the skill's own entry point in this sandbox: a bare `bash <script>.sh` call is routed to a `python3` shim
and dies with a `SyntaxError` on the script body. `base` and `triage` results quoted above were obtained by
invoking the same script through `python3` in one run and through a byte-identical copy in a scratch root
in another; the findings are unaffected (they are reads of the delta). Root cause and fix: `review.md` F3.

### 🔴 [BLOCKING] tests/fixtures/git_closeout/plan.py (Line 144)

> C1: executor discards the role-filtered target set (plan.targets[0], push branch tuple)

<sub>13:37:37</sub>


### 🔴 [BLOCKING] tests/contract/test_git_closeout_contract.py (Line 577)

> C2: SC-005 single-owner guard reds on skills/git-utils/references/closeout-commands.md

<sub>13:37:37</sub>


### 🔴 [BLOCKING] tests/contract/test_git_closeout_contract.py (Line 676)

> C3: no behavioural arm passes remote_name=, so the read-only branch is unexercised

<sub>13:37:37</sub>


### 🟠 [IMPORTANT] .specify/specs/091-auto-git-closeout/test-evidence/T062-smoke.txt (Line 1)

> C4: smoke evidence carries no command line

<sub>13:37:37</sub>


### 🟢 [SUGGESTION] tests/contract/test_git_closeout_contract.py (Line 1145)

> C5: repeated read() on the same surfaces; a cache would cut module time without changing a claim

<sub>13:37:37</sub>


### ❓ [QUESTION] tests/fixtures/git_closeout/repo.py (Line 243)

> C6: is fixture __pycache__ covered by the ignore policy or should the fixture disable byte-code?

<sub>13:37:37</sub>




> **未提交范围（未评审）**: 8 个未提交路径未计入本次评审对象（.specify/memory/exec-quant/records/20261109T053548472154Z-e0e08f1f.json, .specify/memory/exec-quant/records/20261109T053548795074Z-6e7093c5.json, .specify/memory/feedback/20261109T053552Z-skill-review-sdd-process.md, .specify/memory/session/20261109T053527Z-run-determination-skill-review-feature-quality-r20261109t023.md, .specify/memory/session/20261109T053545Z-run-determination-skill-review-sdd-process-r20261109t023000z.md, .specify/specs/091-auto-git-closeout/review.md, .specify/specs/091-auto-git-closeout/test-evidence/arc-closure-check.json, .specify/specs/091-auto-git-closeout/test-evidence/review-2026-11-09/）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=e06fcc52f5f4a3c4f025b49806451ed7c6cfbc33
head=85457d832d8fe5dbfc0a77685c5db9528a3ed2f8
base_source=feature-first-commit
renderer=text
changed_files=371
judged_files=371
skipped_files=0
gap_files=0
lines_added=15400
lines_deleted=322
file.001.path=.claude/commands/speckit.analyze.md
file.001.verdict=reviewed
file.002.path=.claude/commands/speckit.checklist.md
file.002.verdict=reviewed
file.003.path=.claude/commands/speckit.clarify.md
file.003.verdict=reviewed
file.004.path=.claude/commands/speckit.derive.md
file.004.verdict=reviewed
file.005.path=.claude/commands/speckit.docs.md
file.005.verdict=reviewed
file.006.path=.claude/commands/speckit.feedback.md
file.006.verdict=reviewed
file.007.path=.claude/commands/speckit.goal.md
file.007.verdict=reviewed
file.008.path=.claude/commands/speckit.history.md
file.008.verdict=reviewed
file.009.path=.claude/commands/speckit.implement.md
file.009.verdict=reviewed
file.010.path=.claude/commands/speckit.improve.md
file.010.verdict=reviewed
file.011.path=.claude/commands/speckit.instructions.md
file.011.verdict=reviewed
file.012.path=.claude/commands/speckit.interview.md
file.012.verdict=reviewed
file.013.path=.claude/commands/speckit.measure.md
file.013.verdict=reviewed
file.014.path=.claude/commands/speckit.plan.md
file.014.verdict=reviewed
file.015.path=.claude/commands/speckit.requirements.md
file.015.verdict=reviewed
file.016.path=.claude/commands/speckit.research.md
file.016.verdict=reviewed
file.017.path=.claude/commands/speckit.review.md
file.017.verdict=reviewed
file.018.path=.claude/commands/speckit.sanitize.md
file.018.verdict=reviewed
file.019.path=.claude/commands/speckit.session.md
file.019.verdict=reviewed
file.020.path=.claude/commands/speckit.skills.md
file.020.verdict=reviewed
file.021.path=.claude/commands/speckit.status.md
file.021.verdict=reviewed
file.022.path=.claude/commands/speckit.tasks.md
file.022.verdict=reviewed
file.023.path=.claude/commands/speckit.team.md
file.023.verdict=reviewed
file.024.path=.claude/commands/speckit.todo.md
file.024.verdict=reviewed
file.025.path=.claude/commands/speckit.tools.md
file.025.verdict=reviewed
file.026.path=.github/prompts/speckit.analyze.prompt.md
file.026.verdict=reviewed
file.027.path=.github/prompts/speckit.checklist.prompt.md
file.027.verdict=reviewed
file.028.path=.github/prompts/speckit.clarify.prompt.md
file.028.verdict=reviewed
file.029.path=.github/prompts/speckit.derive.prompt.md
file.029.verdict=reviewed
file.030.path=.github/prompts/speckit.docs.prompt.md
file.030.verdict=reviewed
file.031.path=.github/prompts/speckit.feedback.prompt.md
file.031.verdict=reviewed
file.032.path=.github/prompts/speckit.goal.prompt.md
file.032.verdict=reviewed
file.033.path=.github/prompts/speckit.history.prompt.md
file.033.verdict=reviewed
file.034.path=.github/prompts/speckit.implement.prompt.md
file.034.verdict=reviewed
file.035.path=.github/prompts/speckit.improve.prompt.md
file.035.verdict=reviewed
file.036.path=.github/prompts/speckit.instructions.prompt.md
file.036.verdict=reviewed
file.037.path=.github/prompts/speckit.interview.prompt.md
file.037.verdict=reviewed
file.038.path=.github/prompts/speckit.measure.prompt.md
file.038.verdict=reviewed
file.039.path=.github/prompts/speckit.plan.prompt.md
file.039.verdict=reviewed
file.040.path=.github/prompts/speckit.requirements.prompt.md
file.040.verdict=reviewed
file.041.path=.github/prompts/speckit.research.prompt.md
file.041.verdict=reviewed
file.042.path=.github/prompts/speckit.review.prompt.md
file.042.verdict=reviewed
file.043.path=.github/prompts/speckit.sanitize.prompt.md
file.043.verdict=reviewed
file.044.path=.github/prompts/speckit.session.prompt.md
file.044.verdict=reviewed
file.045.path=.github/prompts/speckit.skills.prompt.md
file.045.verdict=reviewed
file.046.path=.github/prompts/speckit.status.prompt.md
file.046.verdict=reviewed
file.047.path=.github/prompts/speckit.tasks.prompt.md
file.047.verdict=reviewed
file.048.path=.github/prompts/speckit.team.prompt.md
file.048.verdict=reviewed
file.049.path=.github/prompts/speckit.todo.prompt.md
file.049.verdict=reviewed
file.050.path=.github/prompts/speckit.tools.prompt.md
file.050.verdict=reviewed
file.051.path=.opencode/command/speckit.analyze.md
file.051.verdict=reviewed
file.052.path=.opencode/command/speckit.checklist.md
file.052.verdict=reviewed
file.053.path=.opencode/command/speckit.clarify.md
file.053.verdict=reviewed
file.054.path=.opencode/command/speckit.derive.md
file.054.verdict=reviewed
file.055.path=.opencode/command/speckit.docs.md
file.055.verdict=reviewed
file.056.path=.opencode/command/speckit.feedback.md
file.056.verdict=reviewed
file.057.path=.opencode/command/speckit.goal.md
file.057.verdict=reviewed
file.058.path=.opencode/command/speckit.history.md
file.058.verdict=reviewed
file.059.path=.opencode/command/speckit.implement.md
file.059.verdict=reviewed
file.060.path=.opencode/command/speckit.improve.md
file.060.verdict=reviewed
file.061.path=.opencode/command/speckit.instructions.md
file.061.verdict=reviewed
file.062.path=.opencode/command/speckit.interview.md
file.062.verdict=reviewed
file.063.path=.opencode/command/speckit.measure.md
file.063.verdict=reviewed
file.064.path=.opencode/command/speckit.plan.md
file.064.verdict=reviewed
file.065.path=.opencode/command/speckit.requirements.md
file.065.verdict=reviewed
file.066.path=.opencode/command/speckit.research.md
file.066.verdict=reviewed
file.067.path=.opencode/command/speckit.review.md
file.067.verdict=reviewed
file.068.path=.opencode/command/speckit.sanitize.md
file.068.verdict=reviewed
file.069.path=.opencode/command/speckit.session.md
file.069.verdict=reviewed
file.070.path=.opencode/command/speckit.skills.md
file.070.verdict=reviewed
file.071.path=.opencode/command/speckit.status.md
file.071.verdict=reviewed
file.072.path=.opencode/command/speckit.tasks.md
file.072.verdict=reviewed
file.073.path=.opencode/command/speckit.team.md
file.073.verdict=reviewed
file.074.path=.opencode/command/speckit.todo.md
file.074.verdict=reviewed
file.075.path=.opencode/command/speckit.tools.md
file.075.verdict=reviewed
file.076.path=.qoder/commands/speckit.analyze.md
file.076.verdict=reviewed
file.077.path=.qoder/commands/speckit.checklist.md
file.077.verdict=reviewed
file.078.path=.qoder/commands/speckit.clarify.md
file.078.verdict=reviewed
file.079.path=.qoder/commands/speckit.derive.md
file.079.verdict=reviewed
file.080.path=.qoder/commands/speckit.docs.md
file.080.verdict=reviewed
file.081.path=.qoder/commands/speckit.feedback.md
file.081.verdict=reviewed
file.082.path=.qoder/commands/speckit.goal.md
file.082.verdict=reviewed
file.083.path=.qoder/commands/speckit.history.md
file.083.verdict=reviewed
file.084.path=.qoder/commands/speckit.implement.md
file.084.verdict=reviewed
file.085.path=.qoder/commands/speckit.improve.md
file.085.verdict=reviewed
file.086.path=.qoder/commands/speckit.instructions.md
file.086.verdict=reviewed
file.087.path=.qoder/commands/speckit.interview.md
file.087.verdict=reviewed
file.088.path=.qoder/commands/speckit.measure.md
file.088.verdict=reviewed
file.089.path=.qoder/commands/speckit.plan.md
file.089.verdict=reviewed
file.090.path=.qoder/commands/speckit.requirements.md
file.090.verdict=reviewed
file.091.path=.qoder/commands/speckit.research.md
file.091.verdict=reviewed
file.092.path=.qoder/commands/speckit.review.md
file.092.verdict=reviewed
file.093.path=.qoder/commands/speckit.sanitize.md
file.093.verdict=reviewed
file.094.path=.qoder/commands/speckit.session.md
file.094.verdict=reviewed
file.095.path=.qoder/commands/speckit.skills.md
file.095.verdict=reviewed
file.096.path=.qoder/commands/speckit.status.md
file.096.verdict=reviewed
file.097.path=.qoder/commands/speckit.tasks.md
file.097.verdict=reviewed
file.098.path=.qoder/commands/speckit.team.md
file.098.verdict=reviewed
file.099.path=.qoder/commands/speckit.todo.md
file.099.verdict=reviewed
file.100.path=.qoder/commands/speckit.tools.md
file.100.verdict=reviewed
file.101.path=.specify/memory/exec-quant/records/20261109T022650325741Z-305d27ac.json
file.101.verdict=reviewed
file.102.path=.specify/memory/exec-quant/records/20261109T023419477214Z-26fe7a30.json
file.102.verdict=reviewed
file.103.path=.specify/memory/exec-quant/records/20261109T024808293296Z-6583474b.json
file.103.verdict=reviewed
file.104.path=.specify/memory/exec-quant/records/20261109T030007008075Z-8b6b0304.json
file.104.verdict=reviewed
file.105.path=.specify/memory/exec-quant/records/20261109T030942740348Z-10c58876.json
file.105.verdict=reviewed
file.106.path=.specify/memory/exec-quant/records/20261109T031303295529Z-d5f880aa.json
file.106.verdict=reviewed
file.107.path=.specify/memory/exec-quant/records/20261109T032439928949Z-5f18730f.json
file.107.verdict=reviewed
file.108.path=.specify/memory/exec-quant/records/20261109T033025424349Z-559cb7da.json
file.108.verdict=reviewed
file.109.path=.specify/memory/exec-quant/records/20261109T050941886215Z-44baddaa.json
file.109.verdict=reviewed
file.110.path=.specify/memory/exec-quant/scores/20261109T032442971294Z-e080253e.json
file.110.verdict=reviewed
file.111.path=.specify/memory/exec-quant/scores/20261109T033028117852Z-81580f88.json
file.111.verdict=reviewed
file.112.path=.specify/memory/features.md
file.112.verdict=reviewed
file.113.path=.specify/memory/features/091.md
file.113.verdict=reviewed
file.114.path=.specify/memory/feedback/20261109T022654Z-skill-create-requirements.md
file.114.verdict=reviewed
file.115.path=.specify/memory/feedback/20261109T023425Z-skill-sdd-loop-driver.md
file.115.verdict=reviewed
file.116.path=.specify/memory/feedback/20261109T024802Z-skill-create-plan.md
file.116.verdict=reviewed
file.117.path=.specify/memory/feedback/20261109T030015Z-skill-create-tasks.md
file.117.verdict=reviewed
file.118.path=.specify/memory/feedback/20261109T030951Z-skill-create-checklist.md
file.118.verdict=reviewed
file.119.path=.specify/memory/feedback/20261109T031308Z-speckit-analyze.md
file.119.verdict=reviewed
file.120.path=.specify/memory/feedback/20261109T032455Z-skill-sdd-loop-driver.md
file.120.verdict=reviewed
file.121.path=.specify/memory/feedback/20261109T033042Z-skill-sdd-loop-driver.md
file.121.verdict=reviewed
file.122.path=.specify/memory/feedback/20261109T050944Z-skill-sdd-loop-driver.md
file.122.verdict=reviewed
file.123.path=.specify/memory/session/20261015T034643Z-run-determination-skill-create-tasks-20261015t114512z-tasks.md
file.123.verdict=reviewed
file.124.path=.specify/memory/session/20261028T134545Z-run-determination-skill-sdd-loop-driver-r20261028t132000z-07.md
file.124.verdict=reviewed
file.125.path=.specify/memory/session/20261030T123430Z-run-determination-skill-sdd-loop-driver-r20261030t081645z-07.md
file.125.verdict=reviewed
file.126.path=.specify/memory/session/20261106T042740Z-run-determination-skill-create-tasks-r20261106t033959z-086a.md
file.126.verdict=reviewed
file.127.path=.specify/memory/session/20261106T075522Z-run-determination-skill-sdd-loop-driver-r20261106t033959z-08.md
file.127.verdict=reviewed
file.128.path=.specify/memory/session/20261106T094333Z-run-determination-speckit-analyze-r20261106t090000z-086a-r3.md
file.128.verdict=reviewed
file.129.path=.specify/memory/session/20261109T013904Z-run-determination-skill-sdd-loop-driver-r20261108t220214z-86.md
file.129.verdict=reviewed
file.130.path=.specify/memory/session/20261109T022648Z-run-determination-skill-create-requirements-r20261109t023000.md
file.130.verdict=reviewed
file.131.path=.specify/memory/session/20261109T023417Z-run-determination-skill-sdd-loop-driver-r20261109t023000z-au.md
file.131.verdict=reviewed
file.132.path=.specify/memory/session/20261109T024806Z-run-determination-skill-create-plan-r20261109t025000z-auto-c.md
file.132.verdict=reviewed
file.133.path=.specify/memory/session/20261109T030000Z-run-determination-skill-create-tasks-r20261109t030000z-auto.md
file.133.verdict=reviewed
file.134.path=.specify/memory/session/20261109T030907Z-run-determination-skill-create-checklist-r20261109t023000z-a.md
file.134.verdict=reviewed
file.135.path=.specify/memory/session/20261109T031300Z-run-determination-speckit-analyze-20261109t031256z.md
file.135.verdict=reviewed
file.136.path=.specify/memory/session/20261109T032435Z-run-determination-skill-sdd-loop-driver-r20261109t023000z-au.md
file.136.verdict=reviewed
file.137.path=.specify/memory/session/20261109T032942Z-run-determination-skill-sdd-loop-driver-r20261109t023000z-au.md
file.137.verdict=reviewed
file.138.path=.specify/memory/session/20261109T033017Z-run-determination-skill-sdd-loop-driver-r20261109t023000z-au.md
file.138.verdict=reviewed
file.139.path=.specify/memory/session/20261109T050936Z-run-determination-skill-sdd-loop-driver-implement-091-slice2.md
file.139.verdict=reviewed
file.140.path=.specify/shared/definitions/probe-definitions.md
file.140.verdict=reviewed
file.141.path=.specify/shared/workflow/artifact-commit-step.md
file.141.verdict=reviewed
file.142.path=.specify/skills/coaching-skills/SKILL.md
file.142.verdict=reviewed
file.143.path=.specify/skills/create-docs/SKILL.md
file.143.verdict=reviewed
file.144.path=.specify/skills/create-pages/SKILL.md
file.144.verdict=reviewed
file.145.path=.specify/skills/create-skills/SKILL.md
file.145.verdict=reviewed
file.146.path=.specify/skills/database-utils/SKILL.md
file.146.verdict=reviewed
file.147.path=.specify/skills/document-utils/SKILL.md
file.147.verdict=reviewed
file.148.path=.specify/skills/draw-diagram/SKILL.md
file.148.verdict=reviewed
file.149.path=.specify/skills/git-utils/SKILL.md
file.149.verdict=reviewed
file.150.path=.specify/skills/git-utils/assets/git-workflow-block.md
file.150.verdict=reviewed
file.151.path=.specify/skills/git-utils/references/closeout-commands.md
file.151.verdict=reviewed
file.152.path=.specify/skills/humanize/SKILL.md
file.152.verdict=reviewed
file.153.path=.specify/skills/improve-docs/SKILL.md
file.153.verdict=reviewed
file.154.path=.specify/skills/improve-skills/SKILL.md
file.154.verdict=reviewed
file.155.path=.specify/skills/internal/analyze-artifacts/SKILL.md
file.155.verdict=reviewed
file.156.path=.specify/skills/internal/archive-session/SKILL.md
file.156.verdict=reviewed
file.157.path=.specify/skills/internal/clarify-artifact/SKILL.md
file.157.verdict=reviewed
file.158.path=.specify/skills/internal/code-review/SKILL.md
file.158.verdict=reviewed
file.159.path=.specify/skills/internal/collect-evidence/SKILL.md
file.159.verdict=reviewed
file.160.path=.specify/skills/internal/create-agent/SKILL.md
file.160.verdict=reviewed
file.161.path=.specify/skills/internal/create-checklist/SKILL.md
file.161.verdict=reviewed
file.162.path=.specify/skills/internal/create-plan/SKILL.md
file.162.verdict=reviewed
file.163.path=.specify/skills/internal/create-requirements/SKILL.md
file.163.verdict=reviewed
file.164.path=.specify/skills/internal/create-tasks/SKILL.md
file.164.verdict=reviewed
file.165.path=.specify/skills/internal/create-team/SKILL.md
file.165.verdict=reviewed
file.166.path=.specify/skills/internal/create-tools/SKILL.md
file.166.verdict=reviewed
file.167.path=.specify/skills/internal/derive-architecture/SKILL.md
file.167.verdict=reviewed
file.168.path=.specify/skills/internal/implement-feature/SKILL.md
file.168.verdict=reviewed
file.169.path=.specify/skills/internal/improve-agent/SKILL.md
file.169.verdict=reviewed
file.170.path=.specify/skills/internal/improve-team/SKILL.md
file.170.verdict=reviewed
file.171.path=.specify/skills/internal/improve-tools/SKILL.md
file.171.verdict=reviewed
file.172.path=.specify/skills/internal/manage-agents/SKILL.md
file.172.verdict=reviewed
file.173.path=.specify/skills/internal/manage-constitution/SKILL.md
file.173.verdict=reviewed
file.174.path=.specify/skills/internal/manage-features/SKILL.md
file.174.verdict=reviewed
file.175.path=.specify/skills/internal/manage-feedback/SKILL.md
file.175.verdict=reviewed
file.176.path=.specify/skills/internal/manage-goal/SKILL.md
file.176.verdict=reviewed
file.177.path=.specify/skills/internal/manage-history/SKILL.md
file.177.verdict=reviewed
file.178.path=.specify/skills/internal/manage-instructions/SKILL.md
file.178.verdict=reviewed
file.179.path=.specify/skills/internal/manage-todo/SKILL.md
file.179.verdict=reviewed
file.180.path=.specify/skills/internal/memory-recall/SKILL.md
file.180.verdict=reviewed
file.181.path=.specify/skills/internal/memory-record/SKILL.md
file.181.verdict=reviewed
file.182.path=.specify/skills/internal/research-feature/SKILL.md
file.182.verdict=reviewed
file.183.path=.specify/skills/internal/review-feature-quality/SKILL.md
file.183.verdict=reviewed
file.184.path=.specify/skills/internal/review-sdd-process/SKILL.md
file.184.verdict=reviewed
file.185.path=.specify/skills/internal/run-agent/SKILL.md
file.185.verdict=reviewed
file.186.path=.specify/skills/internal/run-interview/SKILL.md
file.186.verdict=reviewed
file.187.path=.specify/skills/internal/run-skills/SKILL.md
file.187.verdict=reviewed
file.188.path=.specify/skills/internal/run-team/SKILL.md
file.188.verdict=reviewed
file.189.path=.specify/skills/internal/sanitize-materials/SKILL.md
file.189.verdict=reviewed
file.190.path=.specify/skills/internal/self-improvement/SKILL.md
file.190.verdict=reviewed
file.191.path=.specify/skills/internal/study-project/SKILL.md
file.191.verdict=reviewed
file.192.path=.specify/skills/internal/summarize-project/SKILL.md
file.192.verdict=reviewed
file.193.path=.specify/skills/merge-skills/SKILL.md
file.193.verdict=reviewed
file.194.path=.specify/skills/sdd-house-keeping/SKILL.md
file.194.verdict=reviewed
file.195.path=.specify/skills/sdd-loop-driver/SKILL.md
file.195.verdict=reviewed
file.196.path=.specify/skills/sdd-loop-driver/references/dispatch-recipes.md
file.196.verdict=reviewed
file.197.path=.specify/skills/sdd-project-setup/SKILL.md
file.197.verdict=reviewed
file.198.path=.specify/skills/ssh-utils/SKILL.md
file.198.verdict=reviewed
file.199.path=.specify/specs/083-mechanism-policy-separation/data-model.md
file.199.verdict=reviewed
file.200.path=.specify/specs/091-auto-git-closeout/checklists/2026-11-09-requirements-quality.md
file.200.verdict=reviewed
file.201.path=.specify/specs/091-auto-git-closeout/checkpoints/01-requirements.md
file.201.verdict=reviewed
file.202.path=.specify/specs/091-auto-git-closeout/checkpoints/02-clarify.md
file.202.verdict=reviewed
file.203.path=.specify/specs/091-auto-git-closeout/checkpoints/03-plan.md
file.203.verdict=reviewed
file.204.path=.specify/specs/091-auto-git-closeout/checkpoints/04-tasks.md
file.204.verdict=reviewed
file.205.path=.specify/specs/091-auto-git-closeout/checkpoints/05-checklist.md
file.205.verdict=reviewed
file.206.path=.specify/specs/091-auto-git-closeout/checkpoints/06-analyze.md
file.206.verdict=reviewed
file.207.path=.specify/specs/091-auto-git-closeout/checkpoints/07-analyze-repair.md
file.207.verdict=reviewed
file.208.path=.specify/specs/091-auto-git-closeout/checkpoints/08-analyze-round2.md
file.208.verdict=reviewed
file.209.path=.specify/specs/091-auto-git-closeout/checkpoints/09-implement.md
file.209.verdict=reviewed
file.210.path=.specify/specs/091-auto-git-closeout/contracts/closeout-declaration.contract.md
file.210.verdict=reviewed
file.211.path=.specify/specs/091-auto-git-closeout/contracts/closeout-executor.contract.md
file.211.verdict=reviewed
file.212.path=.specify/specs/091-auto-git-closeout/contracts/closeout-lifecycle.contract.md
file.212.verdict=reviewed
file.213.path=.specify/specs/091-auto-git-closeout/contracts/closeout-verification.contract.md
file.213.verdict=reviewed
file.214.path=.specify/specs/091-auto-git-closeout/coverage-baseline.txt
file.214.verdict=reviewed
file.215.path=.specify/specs/091-auto-git-closeout/data-model.md
file.215.verdict=reviewed
file.216.path=.specify/specs/091-auto-git-closeout/feature-ref.md
file.216.verdict=reviewed
file.217.path=.specify/specs/091-auto-git-closeout/goal/091-auto-git-closeout/goal.md
file.217.verdict=reviewed
file.218.path=.specify/specs/091-auto-git-closeout/notes/pre-change-measurements.md
file.218.verdict=reviewed
file.219.path=.specify/specs/091-auto-git-closeout/notes/red-first-evidence.md
file.219.verdict=reviewed
file.220.path=.specify/specs/091-auto-git-closeout/plan.md
file.220.verdict=reviewed
file.221.path=.specify/specs/091-auto-git-closeout/quickstart.md
file.221.verdict=reviewed
file.222.path=.specify/specs/091-auto-git-closeout/requirements.md
file.222.verdict=reviewed
file.223.path=.specify/specs/091-auto-git-closeout/research.md
file.223.verdict=reviewed
file.224.path=.specify/specs/091-auto-git-closeout/tasks.md
file.224.verdict=reviewed
file.225.path=.specify/specs/091-auto-git-closeout/team/091-auto-git-closeout/team.md
file.225.verdict=reviewed
file.226.path=.specify/specs/091-auto-git-closeout/test-evidence/T001-fixture-probe.txt
file.226.verdict=reviewed
file.227.path=.specify/specs/091-auto-git-closeout/test-evidence/T005-baseline-freeze.txt
file.227.verdict=reviewed
file.228.path=.specify/specs/091-auto-git-closeout/test-evidence/T006-overlap-implement-entry.txt
file.228.verdict=reviewed
file.229.path=.specify/specs/091-auto-git-closeout/test-evidence/T030-forks.txt
file.229.verdict=reviewed
file.230.path=.specify/specs/091-auto-git-closeout/test-evidence/T041-mutation-probe.py
file.230.verdict=reviewed
file.231.path=.specify/specs/091-auto-git-closeout/test-evidence/T052-dispatch-recipes.txt
file.231.verdict=reviewed
file.232.path=.specify/specs/091-auto-git-closeout/test-evidence/T054-instructions-pointer.txt
file.232.verdict=reviewed
file.233.path=.specify/specs/091-auto-git-closeout/test-evidence/T056-mirrors.txt
file.233.verdict=reviewed
file.234.path=.specify/specs/091-auto-git-closeout/test-evidence/T062-smoke.txt
file.234.verdict=reviewed
file.235.path=.specify/specs/091-auto-git-closeout/test-evidence/analyze-repair-gates.txt
file.235.verdict=reviewed
file.236.path=.specify/specs/091-auto-git-closeout/test-evidence/analyze-repair-round1.md
file.236.verdict=reviewed
file.237.path=.specify/specs/091-auto-git-closeout/test-evidence/analyze-round1-findings.md
file.237.verdict=reviewed
file.238.path=.specify/specs/091-auto-git-closeout/test-evidence/analyze-round2-findings.md
file.238.verdict=reviewed
file.239.path=.specify/specs/091-auto-git-closeout/test-evidence/analyze-round2-gates.txt
file.239.verdict=reviewed
file.240.path=.specify/specs/091-auto-git-closeout/test-evidence/baseline-failed.txt
file.240.verdict=reviewed
file.241.path=.specify/specs/091-auto-git-closeout/test-evidence/baseline-full.txt
file.241.verdict=reviewed
file.242.path=.specify/specs/091-auto-git-closeout/test-evidence/checklist-gates-2026-11-09.txt
file.242.verdict=reviewed
file.243.path=.specify/specs/091-auto-git-closeout/test-evidence/checklist-readings-2026-11-09.txt
file.243.verdict=reviewed
file.244.path=.specify/specs/091-auto-git-closeout/test-evidence/clarify-gates.txt
file.244.verdict=reviewed
file.245.path=.specify/specs/091-auto-git-closeout/test-evidence/decision-tensions-plan.json
file.245.verdict=reviewed
file.246.path=.specify/specs/091-auto-git-closeout/test-evidence/dry-run-closeout-rerun.txt
file.246.verdict=reviewed
file.247.path=.specify/specs/091-auto-git-closeout/test-evidence/dry-run-closeout.py
file.247.verdict=reviewed
file.248.path=.specify/specs/091-auto-git-closeout/test-evidence/dry-run-closeout.txt
file.248.verdict=reviewed
file.249.path=.specify/specs/091-auto-git-closeout/test-evidence/final-failed.txt
file.249.verdict=reviewed
file.250.path=.specify/specs/091-auto-git-closeout/test-evidence/final-full.txt
file.250.verdict=reviewed
file.251.path=.specify/specs/091-auto-git-closeout/test-evidence/implement-gates.txt
file.251.verdict=reviewed
file.252.path=.specify/specs/091-auto-git-closeout/test-evidence/mutations.txt
file.252.verdict=reviewed
file.253.path=.specify/specs/091-auto-git-closeout/test-evidence/overlap-check-clarify.json
file.253.verdict=reviewed
file.254.path=.specify/specs/091-auto-git-closeout/test-evidence/overlap-check-plan.json
file.254.verdict=reviewed
file.255.path=.specify/specs/091-auto-git-closeout/test-evidence/overlap-check-tasks.json
file.255.verdict=reviewed
file.256.path=.specify/specs/091-auto-git-closeout/test-evidence/plan-baseline-named-tests.txt
file.256.verdict=reviewed
file.257.path=.specify/specs/091-auto-git-closeout/test-evidence/plan-gates.txt
file.257.verdict=reviewed
file.258.path=.specify/specs/091-auto-git-closeout/test-evidence/pre-analyze-plan-driver.json
file.258.verdict=reviewed
file.259.path=.specify/specs/091-auto-git-closeout/test-evidence/pre-analyze-plan-repair.json
file.259.verdict=reviewed
file.260.path=.specify/specs/091-auto-git-closeout/test-evidence/pre-analyze-plan.json
file.260.verdict=reviewed
file.261.path=.specify/specs/091-auto-git-closeout/test-evidence/pre-analyze-requirements-post-clarify.json
file.261.verdict=reviewed
file.262.path=.specify/specs/091-auto-git-closeout/test-evidence/pre-analyze-requirements-repair.json
file.262.verdict=reviewed
file.263.path=.specify/specs/091-auto-git-closeout/test-evidence/pre-analyze-requirements.json
file.263.verdict=reviewed
file.264.path=.specify/specs/091-auto-git-closeout/test-evidence/pre-analyze-tasks.json
file.264.verdict=reviewed
file.265.path=.specify/specs/091-auto-git-closeout/test-evidence/requirements-gates.txt
file.265.verdict=reviewed
file.266.path=.specify/specs/091-auto-git-closeout/test-evidence/run-note-sandbox.txt
file.266.verdict=reviewed
file.267.path=.specify/specs/091-auto-git-closeout/test-evidence/stage-gates.txt
file.267.verdict=reviewed
file.268.path=.specify/specs/091-auto-git-closeout/test-evidence/workspace-checklist-post.json
file.268.verdict=reviewed
file.269.path=.specify/specs/091-auto-git-closeout/test-evidence/workspace-clarify-post.json
file.269.verdict=reviewed
file.270.path=.specify/specs/091-auto-git-closeout/test-evidence/workspace-requirements-post.json
file.270.verdict=reviewed
file.271.path=.specify/specs/091-auto-git-closeout/test-evidence/workspace-tasks-post.json
file.271.verdict=reviewed
file.272.path=.specify/specs/091-auto-git-closeout/verification.md
file.272.verdict=reviewed
file.273.path=.specify/state/091-auto-git-closeout.md
file.273.verdict=reviewed
file.274.path=.specify/workflow/git.md
file.274.verdict=reviewed
file.275.path=shared/definitions/probe-definitions.md
file.275.verdict=reviewed
file.276.path=shared/workflow/artifact-commit-step.md
file.276.verdict=reviewed
file.277.path=skills/external/coaching-skills/SKILL.md
file.277.verdict=reviewed
file.278.path=skills/external/create-docs/SKILL.md
file.278.verdict=reviewed
file.279.path=skills/external/create-pages/SKILL.md
file.279.verdict=reviewed
file.280.path=skills/external/create-skills/SKILL.md
file.280.verdict=reviewed
file.281.path=skills/external/database-utils/SKILL.md
file.281.verdict=reviewed
file.282.path=skills/external/document-utils/SKILL.md
file.282.verdict=reviewed
file.283.path=skills/external/draw-diagram/SKILL.md
file.283.verdict=reviewed
file.284.path=skills/external/git-utils/SKILL.md
file.284.verdict=reviewed
file.285.path=skills/external/git-utils/assets/git-workflow-block.md
file.285.verdict=reviewed
file.286.path=skills/external/git-utils/references/closeout-commands.md
file.286.verdict=reviewed
file.287.path=skills/external/humanize/SKILL.md
file.287.verdict=reviewed
file.288.path=skills/external/improve-docs/SKILL.md
file.288.verdict=reviewed
file.289.path=skills/external/improve-skills/SKILL.md
file.289.verdict=reviewed
file.290.path=skills/external/merge-skills/SKILL.md
file.290.verdict=reviewed
file.291.path=skills/external/sdd-house-keeping/SKILL.md
file.291.verdict=reviewed
file.292.path=skills/external/sdd-loop-driver/SKILL.md
file.292.verdict=reviewed
file.293.path=skills/external/sdd-loop-driver/references/dispatch-recipes.md
file.293.verdict=reviewed
file.294.path=skills/external/sdd-project-setup/SKILL.md
file.294.verdict=reviewed
file.295.path=skills/external/ssh-utils/SKILL.md
file.295.verdict=reviewed
file.296.path=skills/internal/analyze-artifacts/SKILL.md
file.296.verdict=reviewed
file.297.path=skills/internal/archive-session/SKILL.md
file.297.verdict=reviewed
file.298.path=skills/internal/clarify-artifact/SKILL.md
file.298.verdict=reviewed
file.299.path=skills/internal/code-review/SKILL.md
file.299.verdict=reviewed
file.300.path=skills/internal/collect-evidence/SKILL.md
file.300.verdict=reviewed
file.301.path=skills/internal/create-agent/SKILL.md
file.301.verdict=reviewed
file.302.path=skills/internal/create-checklist/SKILL.md
file.302.verdict=reviewed
file.303.path=skills/internal/create-plan/SKILL.md
file.303.verdict=reviewed
file.304.path=skills/internal/create-requirements/SKILL.md
file.304.verdict=reviewed
file.305.path=skills/internal/create-tasks/SKILL.md
file.305.verdict=reviewed
file.306.path=skills/internal/create-team/SKILL.md
file.306.verdict=reviewed
file.307.path=skills/internal/create-tools/SKILL.md
file.307.verdict=reviewed
file.308.path=skills/internal/derive-architecture/SKILL.md
file.308.verdict=reviewed
file.309.path=skills/internal/implement-feature/SKILL.md
file.309.verdict=reviewed
file.310.path=skills/internal/improve-agent/SKILL.md
file.310.verdict=reviewed
file.311.path=skills/internal/improve-team/SKILL.md
file.311.verdict=reviewed
file.312.path=skills/internal/improve-tools/SKILL.md
file.312.verdict=reviewed
file.313.path=skills/internal/manage-agents/SKILL.md
file.313.verdict=reviewed
file.314.path=skills/internal/manage-constitution/SKILL.md
file.314.verdict=reviewed
file.315.path=skills/internal/manage-features/SKILL.md
file.315.verdict=reviewed
file.316.path=skills/internal/manage-feedback/SKILL.md
file.316.verdict=reviewed
file.317.path=skills/internal/manage-goal/SKILL.md
file.317.verdict=reviewed
file.318.path=skills/internal/manage-history/SKILL.md
file.318.verdict=reviewed
file.319.path=skills/internal/manage-instructions/SKILL.md
file.319.verdict=reviewed
file.320.path=skills/internal/manage-todo/SKILL.md
file.320.verdict=reviewed
file.321.path=skills/internal/memory-recall/SKILL.md
file.321.verdict=reviewed
file.322.path=skills/internal/memory-record/SKILL.md
file.322.verdict=reviewed
file.323.path=skills/internal/research-feature/SKILL.md
file.323.verdict=reviewed
file.324.path=skills/internal/review-feature-quality/SKILL.md
file.324.verdict=reviewed
file.325.path=skills/internal/review-sdd-process/SKILL.md
file.325.verdict=reviewed
file.326.path=skills/internal/run-agent/SKILL.md
file.326.verdict=reviewed
file.327.path=skills/internal/run-interview/SKILL.md
file.327.verdict=reviewed
file.328.path=skills/internal/run-skills/SKILL.md
file.328.verdict=reviewed
file.329.path=skills/internal/run-team/SKILL.md
file.329.verdict=reviewed
file.330.path=skills/internal/sanitize-materials/SKILL.md
file.330.verdict=reviewed
file.331.path=skills/internal/self-improvement/SKILL.md
file.331.verdict=reviewed
file.332.path=skills/internal/study-project/SKILL.md
file.332.verdict=reviewed
file.333.path=skills/internal/summarize-project/SKILL.md
file.333.verdict=reviewed
file.334.path=templates/commands/analyze.md
file.334.verdict=reviewed
file.335.path=templates/commands/checklist.md
file.335.verdict=reviewed
file.336.path=templates/commands/clarify.md
file.336.verdict=reviewed
file.337.path=templates/commands/derive.md
file.337.verdict=reviewed
file.338.path=templates/commands/docs.md
file.338.verdict=reviewed
file.339.path=templates/commands/feedback.md
file.339.verdict=reviewed
file.340.path=templates/commands/goal.md
file.340.verdict=reviewed
file.341.path=templates/commands/history.md
file.341.verdict=reviewed
file.342.path=templates/commands/implement.md
file.342.verdict=reviewed
file.343.path=templates/commands/improve.md
file.343.verdict=reviewed
file.344.path=templates/commands/instructions.md
file.344.verdict=reviewed
file.345.path=templates/commands/interview.md
file.345.verdict=reviewed
file.346.path=templates/commands/measure.md
file.346.verdict=reviewed
file.347.path=templates/commands/plan.md
file.347.verdict=reviewed
file.348.path=templates/commands/requirements.md
file.348.verdict=reviewed
file.349.path=templates/commands/research.md
file.349.verdict=reviewed
file.350.path=templates/commands/review.md
file.350.verdict=reviewed
file.351.path=templates/commands/sanitize.md
file.351.verdict=reviewed
file.352.path=templates/commands/session.md
file.352.verdict=reviewed
file.353.path=templates/commands/skills.md
file.353.verdict=reviewed
file.354.path=templates/commands/status.md
file.354.verdict=reviewed
file.355.path=templates/commands/tasks.md
file.355.verdict=reviewed
file.356.path=templates/commands/team.md
file.356.verdict=reviewed
file.357.path=templates/commands/todo.md
file.357.verdict=reviewed
file.358.path=templates/commands/tools.md
file.358.verdict=reviewed
file.359.path=tests/contract/test_client_guard_sweep.py
file.359.verdict=reviewed
file.360.path=tests/contract/test_decision_tension_contract.py
file.360.verdict=reviewed
file.361.path=tests/contract/test_git_closeout_contract.py
file.361.verdict=reviewed
file.362.path=tests/contract/test_mechanism_policy_guard.py
file.362.verdict=reviewed
file.363.path=tests/contract/test_probe_nonentity_catalog.py
file.363.verdict=reviewed
file.364.path=tests/contract/test_review_code_composition.py
file.364.verdict=reviewed
file.365.path=tests/contract/test_review_feedback_boundary.py
file.365.verdict=reviewed
file.366.path=tests/contract/test_shared_reference_rewrite.py
file.366.verdict=reviewed
file.367.path=tests/contract/test_stage_class_wiring.py
file.367.verdict=reviewed
file.368.path=tests/fixtures/git_closeout/__init__.py
file.368.verdict=reviewed
file.369.path=tests/fixtures/git_closeout/block.py
file.369.verdict=reviewed
file.370.path=tests/fixtures/git_closeout/plan.py
file.370.verdict=reviewed
file.371.path=tests/fixtures/git_closeout/repo.py
file.371.verdict=reviewed
<!-- coverage-receipt:end -->
