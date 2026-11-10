# Specification-Driven Development (SDD) Process Review Report: SDD 专用观察者与线级观察记录（sdd-observer）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

- **Review run**: `/speckit.review` round 3 — 过程 → 产物 → 实现 → 代码四段固定顺序 + Acceptance Reality Check（非第五段）。base `b3da3a26d` → run-start head `15fd648c5`（run-start `HEAD`，固定于本轮）。
- **Rotation**: 上一份 `review.md` 已归档为 `review-20261110T161639Z.md`（slice-id 归档名 `review-096-sdd-observer-agent.md` 已被 round 1 占用；既有归档路径从不覆盖，故取时间戳回退形式）；代码段记录由 `git-delta-review.sh start` 轮转为 `code-review-20261110T161257Z.md`。
- **Judgement**: `Implemented → Ready for Review` = **allowed**（四条件全满足；ARC `accept`；claimed status `Implemented`）。状态转换由本轮 review（状态机的 owner）写回两个载体，写入发生在两份记录落盘之后（见 `### 2.4`）。命名门禁结果：`gate=allow`。
- **Round-2 repair 复核**: **F7（状态翻转）** — 两个状态载体均读 `Implemented`（`.specify/features.md:102`、`.specify/features/096.md:6`）；pre-flip checker 载荷已入证（`claimed_status: Planned`、`verdict: accept`，`review-repair-r2-closure-acceptance.txt` step 1），post-flip 载荷 `claimed_status: Implemented`、`final_path` pass 4 / total 4；顺序为 checker → `verification.md` → 状态写，符合 owner 要求的门序。**F2（脊同步）** — loop-state 读 `stage: review` / `attempt: 2`，最后一条 Stage Record 标题为 `review（review-repair r2 …）`，二者一致；analyze round 5 / implement / review round 1 / r1 / round 2 / r2 六条记录已按证据回填；round-3 analyze 记录缺口照实留白（未补造）。残留：loop-state 文本仍写「review-repair r2 进行中」，而 r2 已于 `15fd648c5` 关闭——属 driver 所有的阶段内文案更新，不影响 `stage` 与末条记录的一致性判据，如实披露。
- **并发读数**: `requested=24`（本线 U0 声明）/ `effective=1` / `effective_reason=representable unit set size 1`（本轮仅一个 P0 待校验单元；四段为组合 owner 声明的固定顺序，不属可并行单元集）。

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 096 |
| Requirement Key | 096-sdd-observer-agent |
| Requirement Name | SDD 专用观察者与线级观察记录（sdd-observer） |
| Related Feature | 096 SDD Observer Agent（sdd-observer 专用观察者与线级 journal） |
| Repository | spec-kit（worktree `096-sdd-observer-agent`） |
| Repository URL | 已配置 `gitee` / `github` / `gitlab`（均 `cloud-native-ai/spec-kit`，SSH 形式）；`origin` 指向上游 `github/spec-kit` |
| Reachability of COMMIT_SHA | **UNRESOLVABLE** — `git branch -r --contains HEAD` 为空：HEAD 未推送到任何跟踪远端分支。本报告不使用 URL 引用，统一用绝对路径 + `git show 15fd648c5:<path>` 取回 |
| Branch | 096-sdd-observer-agent |
| Commit SHA | 15fd648c5fc9aef157a88e06ff6dbc3af491a7fe（short: 15fd648c5） |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent` |
| Review Date | 2026-11-11 |
| Reviewer (Agent) | Qoder（SDD review round 3；git user: Qiming Liu (John)） |
| Environment | Linux x64；CPython 3.11.11；pytest 8.4.2；git 2.43.5 |
| spec-kit Source Snapshot | 本 worktree @ 15fd648c5（`journal-utils.py` 自报版本 0.0.22） |
| State spine (outside worktree) | `/storage/project/cloud-native-ai/spec-kit/.specify/state/096-sdd-observer-agent.md`（只读引用） |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 253 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/requirements.md` | 23 FR / 7 SC（4 final / 3 supporting）；observer 角色、生命周期、journal 客观性与边界；AF-3 修复后 `:181` 读九类 |
| plan.md | 278 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/plan.md` | 22 项宪法检查；5 decision tensions；8 premises；4 工作包；`:38` 已 pin v1.19.1；`§ Project Structure` 已列 `verification.md` |
| tasks.md | 400 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/tasks.md` | 47 行依赖有序任务，47/47 关闭；GATE-1 读 DEFERRED（11 名带 owner）；DoD 7/8 + 1 deferred |
| data-model.md | 164 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/data-model.md` | 10 实体 / 20 校验规则（V-1…V-20） |
| contracts/（5 文件） | 375 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/contracts/` | 58 条款：role / lifecycle / format / engine / verification |
| quickstart.md | 102 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/quickstart.md` | S-0…S-7 八场景；r2 已将陈旧前提刷新到已实现树 |
| research.md | 102 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/research.md` | R-01…R-14 实测记录 |
| feature-ref.md | 111 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/feature-ref.md` | 19 交付行、FR/SC 映射、重叠裁定 |
| verification.md | 64 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/verification.md` | 7 条 `SC-NNN_status=` 全 pass（final 4/4）、`RS-003_joint_acceptance=pass`、单一 smoke 三元组；状态叙事记录 checker-first 顺序 |
| test-evidence/ | 目录 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/test-evidence/` | 门禁读数与证据收录（含本轮 `review-r3-smoke.txt`、`review-r3-gates.txt`、`review-r3-arc.txt`） |
| review.md | 本文件 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/review.md` | 本报告（上一份归档 `review-20261110T161639Z.md`） |
| code-review.md | 本记录 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/code-review.md` | 代码段记录（含覆盖率回执；上一份归档 `code-review-20261110T161257Z.md`） |

## 1. Process Execution Timeline

从 `git log b3da3a26d..HEAD`（48 个提交）与状态脊重建；时间线只取有提交/产物锚的事件。

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements 完成 | `32c26f3c0`（requirements + checklist + test-evidence + glossary） | none |
| 2 | clarify 完成 | `7d3e34183` | none |
| 3 | plan 完成 | `79a650f45`；plan.md:38 以 v1.19.0 渲染 Constitution Check | none（版本 pin 已由 r2 修为 v1.19.1） |
| 4 | tasks 完成 | `492353de4`；GATE-4 声明 `verification.md` 载体 | none |
| 5 | checklist 完成 | `38377e3ae` | none |
| 6 | analyze rounds 1–2 | `07cf28816`、`60c78e773`；round 2 检出 1 CRITICAL + 3 HIGH | gate 未过 |
| 7 | analyze repairs r3/r4 + rounds 3/4 | `32e83b95e` → `14a7da094`；`05491c0a7` → `4c34b2c1f`；open HIGH W13-17（`verification.log` vs `.gitignore` vs 框架链） | gate 未过 |
| 8 | **宪法修订 v1.19.0 → v1.19.1** | `34ea3eb76`；Sync Impact Report: "Version change: 1.19.0 → 1.19.1 (PATCH; carrier correction, 2026-11-10)" | **deviation**：运行中修订治理文档（见 F4） |
| 9 | analyze repair r5 + round 5 | `e2b248bfd` → `dee7e2976` / `c9b86e7fa`；C0/H0 门禁通过 | none（5 轮才过） |
| 10 | implement setup + wp01–wp04 | `ac9ca879b` … `ed4dd1e6b`（13 个实现/证据提交）；47/47 行关闭 | **deviation**：`verification.md` 未产出，Feature 停在 `Planned`（F1 / F7 的线级症状） |
| 11 | state spine 记录 | 当时最后一条 Stage Record 停在 analyze round 4；loop-state 仍是 `stage: requirements` / `attempt: 0` | **deviation**：单一持久状态过期（F2） |
| 12 | review round 1 | `86f3a546a`；四段 + ARC 判定 refused；2 P0 / 2 P1 / 2 P2，代码记录 1 blocking / 1 important / 1 suggestion | gate 未过 |
| 13 | review-repair r1 | `262f30bde`；写 `verification.md`、修 anomaly 投影与 owner 块解析、对齐 GATE-1 口径；closure checker 复跑 `accept` | **deviation**：审查门所需产物由 review 之后的修复轮补出（F1 行级症状） |
| 14 | review round 2 | `0d0b3c2f5`；r1 四项修复复核通过；ARC `accept`；转换仍 refused（from-state `Planned`）；process P0 3（F1 / F2 / F7）各经独立校验器 confirm | gate 未过（状态机 from-state） |
| 15 | review-repair r2 | `b2b5e0015`；**F7**：按 checker-first 顺序落 `Planned → Implemented`（`verification.md` 状态叙事 + 两个载体）；**F2**：状态脊回填（loop-state + 六条阶段记录 + 框架观察节）；F5 / AF-3…AF-7 与 quickstart/DoD 陈旧行就地修复 | none（round-2 发现按处置落地） |
| 16 | pre-flip 证据补录 | `15fd648c5`；`review-repair-r2-closure-acceptance.txt` 追加 step-1 载荷（`claimed_status: Planned`、`verdict: accept`），与 flip 提交中的处置记录互为佐证 | none（证据完整性补录；随附披露） |
| 17 | review round 3（本次） | ARC `accept`（pass 4/4）；代码段 `gate=allow`（0 blocking / 0 important / 1 praise）；F7 / F2 修复锚点复核通过；转换 **allowed** → 状态写回两载体 | none |

## 2. Findings Summary

> 本节汇总的是**过程段**（`review-sdd-process`）的 findings。产物段与实现段各自在 `### 2.2` / `### 2.3` 给出自己的逐条表，代码段在独立的 `code-review.md`；四段结论不合并、不折算、不评分。

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 1 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 3 |
| Documentation | 0 |

**Same-author gate**: **not fired** — the artifacts under review predate this session and were authored by earlier stage sessions, so independent authorship already supplies fresh context; detection was direct. **P0 validation**: the single open P0 (F1, carried from round 2) was re-confirmed by a fresh-context, read-only independent validator that received only the finding, its anchors and the quoted evidence — `confirm` 1 / `downgrade` 0 / `reject` 0 (downgrade rate 0/1). Round-2 P0s F2 and F7 are **closed** this round by verified anchors (see the header block and `### 2.4`); they no longer appear in the counts above.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | `git-delta-review.sh base --spec .specify/specs/096-sdd-observer-agent` |
| Head commit | 15fd648c5fc9aef157a88e06ff6dbc3af491a7fe | run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | the resolution tier the code segment reported |
| Renderer mode | text | the code record's header marker (`renderer: text`) |
| Changed / judged / skipped / gap files | 177 / 11 / 166 / 0 | copied field by field from the receipt block in `code-review.md` |
| Segment verdict | not-evaluated | C-37（`skipped_files=166>0` 时不得记 `pass`；`blocking_entries=0` → `not-evaluated`）。非结论不阻断状态转换 |
| Gate verdict | **allow**（代码合入门禁）· 状态转换 **allowed**（四条件全满足，见 `### 2.4`） | `report --summary --file code-review.md` → `gate=allow`, exit 0（0 blocking / 0 important / 1 praise） |
| Reason, when one applies | none — triage 值为 `run`；段裁决 `not-evaluated` 是 C-37 跳过规则的结果，不是适用性失败 | `code-review.md` |
| Uncommitted scope | 14 个未提交路径未计入评审对象：12 个 `.specify/memory/` 运行记录、运行前已存在的未跟踪 `checkpoints/` 目录、本轮两个证据文件（`review-r3-smoke.txt`、`review-r3-gates.txt`）— disclosed, never concluded over | `git status --porcelain` at receipt time; the same sentence lives in `code-review.md` |
| Record | .specify/specs/096-sdd-observer-agent/code-review.md | written (triage = run) |
| Archive | .specify/specs/096-sdd-observer-agent/code-review-20261110T161257Z.md | rotated by `start` |

代码段四短语约束：本次以 `renderer: text` 运行，记录与结论均未声称可视化评审已完成。代码路径自 round-2 head `262f30bde` 起零变化（`git diff --stat 262f30bde..15fd648c5 -- '*.py' '*.yaml' '*.sh'` 为空）；本轮对引擎与三个契约测试模块重新通读，fixtures 与两个既有测试的 pin 更新逐项复核，零 blocking / 零 important / 一条 praise。**客户采集**：本仓为框架帽（spec-kit 源码树，非客户项目），`capture` 步不运行——结论以帽子判据为依据，不取五值闭集中任何一项。

### 2.2 Artifact Review Segment

Artifacts: 10 / 10   missing: none

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md, test-evidence/ | union of the stage rules (Canonical Status State Machine: every SC has a `verification.md` status row) and `plan.md` § Project Structure (which declares research.md, feature-ref.md and test-evidence/) |
| Coverage line | 10 / 10 | present members / expected members |
| Missing members | none | — |
| Segment verdict | pass | 本段零 open finding；round-2 的 AF-3…AF-7 全部经锚点复核确认已修复 |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| — | — | — | — | （无 open finding） |

**Round-2 产物修复复核（本段）**: **AF-3** `requirements.md:181` 已读「承载九类信息（类别见 FR-011）」；**AF-4** `plan.md:38` 已 pin `(v1.19.1)`；**AF-5** `tasks.md:33` GATE-4 披露改为「已由 v1.19.1 修订（commit `34ea3eb76`，2026-11-10）裁定为 `verification.md`」，`:379` 的 Notes 残句同步；**AF-6** `plan.md:147` 文档树新增 `verification.md # Implement close — one SC status row per criterion + smoke record (GATE-4 input)`；**AF-7** `.specify/features.md:102` 的 Last Updated 文本已改写。残留 grep（`由框架级统一裁定` / `under framework-level adjudication` / `v1.19.0`（plan）/ `承载八类`）在所需产物集上无匹配（exit 1）；计数一致性：FR 23 / SC 7 / 条款 58 / SC 状态行 7 / `smoke_command=` 恰一处；`validate-requirements.py` → `status: ok`、0 error / 0 warning；`validate-tasks.py` → 0 error / 4 warning（既有披露集）；`pre-analyze-check.py --stage tasks` → `decision=pass`。证据：`test-evidence/review-r3-gates.txt`。

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base |
| Head commit | 15fd648c5fc9aef157a88e06ff6dbc3af491a7fe | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | `git-delta-review.sh base` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py tests/contract/test_sdd_observer_agent.py tests/contract/test_sdd_observer_lifecycle.py tests/contract/test_sdd_loop_driver_skill.py -q` | recorded verbatim |
| Smoke exit code | 0 | the integer the command returned（77 passed + 1 serial，25 s） |
| Smoke evidence path | .specify/specs/096-sdd-observer-agent/test-evidence/review-r3-smoke.txt | exists, non-empty（含命令行、全量输出、退出码、耗时） |
| Scope and regression verdict | scope: pass with disclosure — 区间内新增提交为 round-2 评审记录（`0d0b3c2f5`）、review-repair r2（`b2b5e0015`）与 pre-flip 证据补录（`15fd648c5`），逐项可追溯到评审发现 F7 / F2 / F5 / AF-3…AF-7 与本轮 review 周期，属同一变更线内的评审/修复工作，无无主工作；code paths unchanged since `262f30bde`。regression: pass for the feature modules — 四个 096 模块 77 passed + 1 serial，exit 0；全量套件 delta 仍按 GATE-1 读 **DEFERRED**（11 名均带 owner，零 096 模块 id），照实引用、不重新解释 | segment's own reading |
| Segment verdict | pass | the finding rows below are this segment's record (none) |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| — | — | — | — | （无实现段 finding：正确性、范围与回归三项均按上表读 pass） |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written before this judgement) | Implemented | `.specify/features/096.md` `**Status**`（与 `.specify/features.md` 096 行一致；checker 的 `claimed_status_source` 解析为仓库注册表） |
| `final_path` record, copied verbatim (7/7) | pass 4 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 4 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/096-sdd-observer-agent --json`（exit 0，`verdict: accept`，`reasons: []`；证据 `test-evidence/review-r3-arc.txt`），never recomputed here |
| Comparison verdict | agree | checker `accept` 与 claim `Implemented` 一致；两条拒绝条件均不成立（verdict 非 `block`；claim 非 `Implemented`/`Ready for Review` 且 pass 为零），`F-ACCEPTANCE` 不触发 |
| Failed condition, on refusal | none | 转换未拒绝 |
| Fixed item, on refusal | none | `F-ACCEPTANCE` 未触发 |

**Status transition judgement**: `Implemented → Ready for Review` is **allowed**. 四个合取条件在本树读为：(a) 零 deferred task —— `tasks.md` 的 `[~]` 行为 0、`verification.md` 的 `deferred_tasks=` 为空，checker `tasks.deferred=0`、`tasks.open=0`；(b) 评审证据已产出 —— 本报告 + `code-review.md` + `test-evidence/review-r3-smoke.txt` + `review-r3-gates.txt` + `review-r3-arc.txt`；(c) 当前代码记录零 `blocking` —— `report --summary` 读 `blocking_entries=0`、`gate=allow`；(d) 无 `final` 路径判据处于 `blocked` / `deferred` / `fail` —— checker `final_path` pass 4 / total 4。判断时点为四段完成之后、两份记录均已落盘（`review.md`、`code-review.md`），ARC 先于翻转运行。据此本轮把状态写回两个载体为 `Ready for Review`：`.specify/features.md` 096 行与 `.specify/features/096.md` `**Status**`；此前 claimed status 保持 `Implemented` 未降级、未改写。The unattended disposition is not triggered (no refusal).

## 3. Findings (Problems & Improvement Targets)

### F1 — The review gate reads an artifact that the implement stage is assigned but not enforced to produce, and this line's stage plan reviews before closure

- **Severity**: P0
- **Category**: Workflow
- **Location**: `templates/commands/implement.md:50`; `.specify/state/096-sdd-observer-agent.md:31`; `.specify/specs/096-sdd-observer-agent/verification.md:1-11`
- **Evidence** (verbatim quote):

  ```
  - **Outputs**: every task `[X]` or honestly `[~]`, the `## Completion Gate` re-validated against the current tree, `verification.md` populated, phase-boundary commits landed.
  ```

  ```
  - 阶段计划：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure → 合并 master`
  ```

  ```
  Recorded 2026-11-10 by the review-repair r1 pass (review finding AF-1), discharging
  GATE-4 / DoD-7 of tasks.md.
  ```

- **Why it's a problem**: the review's Acceptance Reality Check runs `closure-acceptance-check.py`, whose `REQUIRED_INPUTS` include `verification.md`, while `/speckit.implement`'s output contract assigns that file to the implement stage without a mechanism that fails the stage when it is missing. A line whose stage plan reviews before closure therefore gets a structurally undecidable gate the first time implement closes without the file — this line's round-1 ARC exited 2 and the artifact appears only in the review-repair r1 commit. The line-level symptom is repaired; the ordering/enforcement conflict that produced it remains open at framework level (independently re-confirmed this round).
- **Proposed fix**: add an implement-stage row that writes `verification.md` and runs `python3 scripts/python/closure-acceptance-check.py --spec-dir <spec>` before review, and make the implement-stage close fail when the file is absent (or move review after closure in the driver stage sequence — the two orders cannot both hold).

### F3 — The implement-entry full-suite baseline was not captured; GATE-1 still reads DEFERRED

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/096-sdd-observer-agent/tasks.md:20` (DoD-4), `:30` (GATE-1), `:40-56` (§ GATE-1 DEFERRED set)
- **Evidence** (verbatim quote):

  ```
  This line took no Step 0 capture; its same-day reconstructed baseline leaves a literal 11-id delta, so GATE-1 reads **DEFERRED** — every one of the 11 ids is named with its owner in § GATE-1 DEFERRED set and is never re-labelled as "zero NEW".
  ```

- **Why it's a problem**: a baseline that was never captured cannot be created retroactively, so the closed-set gate stays undecidable for the life of the line. The 11-id delta is disclosed with named owners and contains zero 096 module id, but "zero NEW failed ids" still has no baseline to compare against; every later line pays the same toll unless Step 0 capture is enforced.
- **Proposed fix**: make `/speckit.implement` Step 0 capture `bash scripts/bash/run-tests.sh --names-out <baseline>` before the first edit and make GATE-1 compare against that file; keep the DEFERRED reading with its named owners where a shared store keeps the baseline unstable.

### F4 — A machine-read path literal in the constitution conflicted with `.gitignore` and the implementation chain, surfacing only at analyze round 4

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/constitution.md:3` (Sync Impact Report); `.specify/specs/096-sdd-observer-agent/test-evidence/analyze-merged-r4-2026-11-10.md`
- **Evidence** (verbatim quote):

  ```
  - Version change: 1.19.0 → 1.19.1 (PATCH; carrier correction, 2026-11-10)
  ```

  ```
  round-4 未过 —— 1 条 open HIGH（W13-17）
  ```

- **Why it's a problem**: the plan-stage Constitution Check rendered 22 Pass rows against a constitution whose record carrier (`verification.log`) is excluded by `.gitignore` and unread by every machine consumer. The conflict survived requirements, plan, tasks and three analyze rounds, then forced an in-line constitutional amendment and a fifth analyze round. A plan-stage check that verifies only principle prose cannot catch a machine-read path that no chain reads. (The constitution is now v1.19.1 and this line's conflict is resolved; the gate gap is the open part.)
- **Proposed fix**: add a plan-stage gate row — "every record carrier this plan names is (a) committable under the repository's ignore rules and (b) read by a named machine consumer" — and render the Constitution Check against the live version.

### F6 — `specify render-agents` refreshes unrelated agent copies as a side effect

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/096-sdd-observer-agent/tasks.md:266` (T041); `.claude/agents/reporter.md`; `.github/agents/reporter.agent.md`; `.opencode/agents/reporter.md`; `.qoder/agents/reporter.agent.md`
- **Evidence** (verbatim quote):

  ```
  - [X] T041 Generate the framework mirrors and per-tool render copies: `python3 scripts/python/sync-mirrors.py --write` for the `agents/`, `shared/`, `scripts/` and `skills/external/` pairs, then `specify render-agents --ai qoder`, `--ai claude`, `--ai copilot` and `--ai opencode` …
  ```

  ```
  +<!-- 092 handoff: D4 — 周期数值的唯一 owner 是 `.specify/shared/guidelines/reporting-obligations.md` § 二（长跑档 30 s）；上一行只抵达 `progress-reporting.md` 的交互档缺省与内容下限，该行保留不改、仅作历史记录。参见 092 D4，2026-11-09。 -->
  ```

- **Why it's a problem**: a feature-scoped render obligation silently changes four files owned by another feature. The delta stays small here, but the pattern means every feature that renders agents can carry another feature's pending render drift, making the slice's scope claim unverifiable from the diff.
- **Proposed fix**: add a per-agent filter to `specify render-agents` (e.g. `--agent sdd-observer`) or declare the refreshed copies in the plan's Mirror Obligations table and verify them by name; do not let an unlisted copy change inside a feature delta.

## 4. What Worked — Preserve (Brief)

- The F7 disposition holds the required gate order: checker on the final edited tree (`claimed_status: Planned`, `verdict: accept`) → verdict written into `verification.md` → status written to both carriers; both payloads are on file and the post-flip reading is `claimed_status: Implemented`, `final_path` 4/4.
- The F2 backfill makes the spine self-consistent where it matters: loop-state `stage: review` and the last Stage Record heading agree, six records cite their evidence basis, and the pre-existing round-3 analyze gap was left visible rather than invented.
- The P2 cleanup is verifiable: residue greps are empty across the required artifact set, `validate-requirements.py` is 0/0, `validate-tasks.py` keeps 0 errors with only the four disclosed warnings, and `pre-analyze-check.py --stage tasks` reads `decision=pass`.
- The journal engine and its drills are unchanged since round 2 and still carry their red legs (mutation-driven coverage test, flock refusal, anomaly-after-sentinel, gap drill); this round's smoke re-ran them green.
- Evidence discipline in `test-evidence/` remains strong: every gate reading named its command, exit status and file, and the round-3 evidence set is three self-describing captures (`review-r3-smoke.txt`, `review-r3-gates.txt`, `review-r3-arc.txt`).

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Implement-stage verification carrier with enforcement** — Target: `templates/commands/implement.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/templates/commands/implement.md`) § Feature Integration, and `templates/tasks-template.md`. Change: make `verification.md` a required implement-stage output row, fail the stage close when it is absent, and state that a DoD row may not defer it to a later stage. Source: F1. Expected impact: review and implement stop disagreeing about when the acceptance record exists.

### 5.2 Command Prompt Improvements

- None beyond F1's implement-template row; the review prompt already states the ARC clause correctly.

### 5.3 Automation / Script Improvements

- **Implement Step 0 baseline capture** — Target: `skills/internal/implement-feature/SKILL.md` Step 0. Change: capture the full-suite name list before the first edit and make `tasks.md` GATE-1 compare against that file. Source: F3. Expected impact: the closed-set gate becomes decidable without post-hoc reconstruction.
- **Per-agent render filter** — Target: the `specify render-agents` CLI entry in `src/specify_cli/__init__.py`. Change: add a per-agent selector so a feature renders only the templates it owns; or record every refreshed copy in the plan's Mirror Obligations. Source: F6. Expected impact: feature deltas stop carrying other features' render drift.

### 5.4 Workflow Improvements

- **Plan-stage carrier committability check** — Target: `templates/plan-template.md` / `skills/internal/create-plan/SKILL.md`. Change: add the record-carrier check from F4 as a plan gate row and render the Constitution Check against the live version. Source: F4. Expected impact: path literals that no machine reads, or that `.gitignore` excludes, are caught before analyze.
- **Framework-side close guards (carried observations)** — Targets: `skills/external/sdd-loop-driver/SKILL.md` § 状态脊 (stage-close guard comparing loop-state `stage` with the last Stage Record heading) and `skills/internal/implement-feature/SKILL.md` (status-write enforcement at implement close). Change: fail the respective stage close when the guard reads a mismatch. Source: the round-2 F2 / F7 findings, now line-level closed and carried as named framework observations in the state spine. Expected impact: a stale spine or an un-flipped status becomes detectable at the stage where it occurs, not two review rounds later.

### 5.5 Documentation Improvements

- None open — the v1.19.1 residue and the plan-tree gap are verified fixed (AF-3…AF-7).

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Produce and enforce `verification.md` at implement close; judge the review gate after it exists | `templates/commands/implement.md`, `templates/tasks-template.md` | F1 |
| P1 | Capture the implement-entry suite baseline in Step 0 | `skills/internal/implement-feature/SKILL.md` Step 0 | F3 |
| P1 | Add the plan-stage carrier committability gate | `templates/plan-template.md`, `skills/internal/create-plan/SKILL.md` | F4 |
| P2 | Scope `render-agents` per agent | `src/specify_cli/__init__.py` | F6 |
| P2 | Land the driver-side spine/status close guards (carried observation) | `skills/external/sdd-loop-driver/SKILL.md`, `skills/internal/implement-feature/SKILL.md` | round-2 F2 / F7 (line-level closed) |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target lacks a repo-relative form.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] **P0 validation status is stated explicitly.** F1 (carried) was re-confirmed by a fresh-context, read-only independent validator that received only the finding, its anchors and the quoted evidence (`confirm` 1 / `downgrade` 0 / `reject` 0). Round-2's other two P0s (F2, F7) are closed by verified anchors this round and are excluded from the counts.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
