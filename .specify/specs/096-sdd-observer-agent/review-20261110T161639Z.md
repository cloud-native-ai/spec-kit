# Specification-Driven Development (SDD) Process Review Report: SDD 专用观察者与线级观察记录（sdd-observer）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

- **Review run**: `/speckit.review` round 2 — 过程 → 产物 → 实现 → 代码四段固定顺序 + Acceptance Reality Check（非第五段）。base `b3da3a26d` → run-start head `262f30bde`。
- **Rotation**: 上一份 `review.md` 已归档为 `review-096-sdd-observer-agent.md`；代码段记录由 `git-delta-review.sh start` 轮转为 `code-review-20261110T155402Z.md`。
- **Judgement**: `Implemented → Ready for Review` = **refused**（from-state 仍为 `Planned`；`Planned → Ready for Review` 不是状态机中的转换）。命名拒绝字面：`blocking-unresolved`。claimed status 保持 `Planned`，未降级、未改写。
- **Round-1 修复复核**: AF-1（`verification.md`）、IM-1（anomaly 投影）、IM-2（owner 块解析）、AF-2（GATE-1 口径）四项全部在 `262f30bde` 落地并在本树复核通过；本轮新发现/承继的未决项见 §3 与 §2.2。
- **并发读数**: `requested=24`（本线 U0 声明）/ `effective=3` / `effective_reason=representable unit set size 3`（三个 P0 校验单元一波并行；低于有效槽位 5）。四段本身按组合 owner（`shared/workflow/acceptance-hardening.md` § Review Composition）的固定顺序执行，不属串行理由码场景。

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 096 |
| Requirement Key | 096-sdd-observer-agent |
| Requirement Name | SDD 专用观察者与线级观察记录（sdd-observer） |
| Related Feature | 096 SDD Observer Agent（sdd-observer 专用观察者与线级 journal） |
| Repository | spec-kit（worktree `096-sdd-observer-agent`） |
| Repository URL | 已配置 `gitee` / `github` / `gitlab`（均 `cloud-native-ai/spec-kit`，SSH 形式）；`origin` 指向上游 `github/spec-kit` |
| Reachability of COMMIT_SHA | **UNRESOLVABLE** — `git branch -r --contains HEAD` 为空：HEAD 未推送到任何跟踪远端分支。本报告不使用 URL 引用，统一用绝对路径 + `git show 262f30bde:<path>` 取回 |
| Branch | 096-sdd-observer-agent |
| Commit SHA | 262f30bdeef601a41efd230c14317445a5da1fc8（short: 262f30bde） |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent` |
| Review Date | 2026-11-10 |
| Reviewer (Agent) | Qoder（SDD review round 2；git user: Qiming Liu (John)） |
| Environment | Linux x64；CPython 3.11.11；pytest 8.4.2；git 2.43.5 |
| spec-kit Source Snapshot | 本 worktree @ 262f30bde（`journal-utils.py` 自报版本 0.0.22） |
| State spine (outside worktree) | `/storage/project/cloud-native-ai/spec-kit/.specify/state/096-sdd-observer-agent.md`（只读引用） |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 253 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/requirements.md` | 23 FR / 7 SC（4 final / 3 supporting）；observer 角色、生命周期、journal 客观性与边界 |
| plan.md | 277 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/plan.md` | 22 项宪法检查、5 decision tensions、8 premises、4 工作包；§ Project Structure 未列 `verification.md` |
| tasks.md | 400 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/tasks.md` | 47 行依赖有序任务，47/47 关闭；GATE-1 读 DEFERRED（11 名带 owner）；DoD 6/8 + 2 deferred |
| data-model.md | 164 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/data-model.md` | 10 实体 / 20 校验规则（V-1…V-20）；E-6 anomaly 行已按修复口径更新 |
| contracts/（5 文件） | 375 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/contracts/` | 58 条款：role / lifecycle / format / engine / verification |
| quickstart.md | 102 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/quickstart.md` | S-0…S-7 八场景 |
| research.md | 102 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/research.md` | R-01…R-14 实测记录 |
| feature-ref.md | 111 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/feature-ref.md` | 19 交付行、FR/SC 映射、重叠裁定 |
| verification.md | 56 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/verification.md` | 7 条 `SC-NNN_status=` 全 pass（final 4/4）、`RS-003_joint_acceptance=pass`、smoke 三元组；由 review-repair r1 落盘 |
| test-evidence/ | 目录 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/test-evidence/` | 门禁读数与证据收录（含本轮 `review-r2-smoke.txt`） |
| review.md | 本文件 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/review.md` | 本报告（上一份归档 `review-096-sdd-observer-agent.md`） |
| code-review.md | 718 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/.specify/specs/096-sdd-observer-agent/code-review.md` | 代码段记录（含覆盖率回执；上一份归档 `code-review-20261110T155402Z.md`） |

## 1. Process Execution Timeline

从 `git log b3da3a26d..HEAD`（45 个提交）与状态脊重建；时间线只取有提交/产物锚的事件。

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements 完成 | `32c26f3c0`（requirements + checklist + test-evidence + glossary） | none |
| 2 | clarify 完成 | `7d3e34183` | none |
| 3 | plan 完成 | `79a650f45`；plan.md:38 以 v1.19.0 渲染 Constitution Check | none（版本 pin 见 F5） |
| 4 | tasks 完成 | `492353de4`；GATE-4 声明 `verification.md` 载体 | none |
| 5 | checklist 完成 | `38377e3ae` | none |
| 6 | analyze round 1 | `07cf28816`；merge 报告 39 findings = CRITICAL 0 / 4 validated HIGH / 26 MEDIUM / 8 LOW | gate 未过 |
| 7 | analyze round 2 | `60c78e773`；1 CRITICAL + 3 HIGH | gate 未过 |
| 8 | analyze repair r3 + round 3 | `32e83b95e` → `14a7da094` | gate 未过 |
| 9 | analyze repair r4 + round 4 | `05491c0a7` → `4c34b2c1f`；open HIGH W13-17（`verification.log` vs `.gitignore` vs 框架链） | gate 未过 |
| 10 | **宪法修订 v1.19.0 → v1.19.1** | `34ea3eb76`；Sync Impact Report: "Version change: 1.19.0 → 1.19.1 (PATCH; carrier correction, 2026-11-10)" | **deviation**：运行中修订治理文档（见 F4） |
| 11 | analyze repair r5 + round 5 | `e2b248bfd` → `dee7e2976` / `c9b86e7fa`；C0/H0 门禁通过 | none（5 轮才过） |
| 12 | implement setup | `ac9ca879b`；基线/落点固化（implement-entry base `c9b86e7fa`） | none |
| 13 | implement wp01–wp04 | `50cdd6cb5` … `ed4dd1e6b`（13 个实现/证据提交）；47/47 行关闭 | **deviation**：`verification.md` 未产出，Feature 停在 `Planned`（见 F1 / F7） |
| 14 | state spine 记录 | 最后一条 Stage Record 是 analyze round 4；loop-state 仍是 `stage: requirements` / `attempt: 0`；无 r5 / implement 记录 | **deviation**：单一持久状态过期（见 F2） |
| 15 | review round 1 | `86f3a546a`；四段 + ARC 判定 `Implemented → Ready for Review` **refused**（`blocking-unresolved`）；2 P0 / 2 P1 / 2 P2，代码记录 1 blocking / 1 important / 1 suggestion | gate 未过 |
| 16 | review-repair r1 | `262f30bde`；写 `verification.md`、修 anomaly 投影与 owner 块解析、对齐 GATE-1 口径；closure checker 复跑 `accept` | **deviation**：审查门所需产物由 review 之后的修复轮补出（F1 的行级症状，framework gap 未关） |
| 17 | review round 2（本次） | ARC `accept`（pass 4/4）；代码段 `gate=allow`（0 blocking / 0 important / 1 praise）；r1 四项修复复核通过；状态转换仍 refused（from-state `Planned`） | gate 未过（状态机 from-state） |

## 2. Findings Summary

> 本节汇总的是**过程段**（`review-sdd-process`）的 findings。产物段与实现段各自在 `### 2.2` / `### 2.3` 给出自己的逐条表，代码段在独立的 `code-review.md`；四段结论不合并、不折算、不评分。

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 3 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 2 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 4 |
| Documentation | 1 |

**Same-author gate**: **not fired** — the artifacts under review predate this session and were authored by earlier stage sessions, so independent authorship already supplies fresh context; detection was direct. **P0 validation**: every P0 (F1, F2, F7) was confirmed by a fresh-context, read-only independent validator that received only the finding, its anchors and the quoted evidence — `confirm` 3 / `downgrade` 0 / `reject` 0 (downgrade rate 0/3).

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | `git-delta-review.sh base --spec .specify/specs/096-sdd-observer-agent` |
| Head commit | 262f30bdeef601a41efd230c14317445a5da1fc8 | run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | the resolution tier the code segment reported |
| Renderer mode | text | the code record's header marker (`renderer: text`) |
| Changed / judged / skipped / gap files | 171 / 11 / 160 / 0 | copied field by field from the receipt block in `code-review.md` |
| Segment verdict | not-evaluated | C-37「跳过不计覆盖信用」：`skipped_files=160>0`，段裁决不得记 `pass`；`blocking_entries=0`。非结论不阻断状态转换 |
| Gate verdict | allow（代码合入门禁）· 转换拒绝字面 `blocking-unresolved`（按状态机第 6 条记录于本节） | `report --summary --file code-review.md` → `gate=allow`, exit 0（0 blocking / 0 important / 1 praise）；转换拒绝的原因为 from-state（见 §2.4） |
| Reason, when one applies | none — triage 值为 `run`；段裁决 `not-evaluated` 是 C-37 跳过规则的结果，不是适用性失败 | `code-review.md` |
| Uncommitted scope | `.specify/specs/096-sdd-observer-agent/checkpoints/`（未跟踪目录，运行前已存在，非本切片产物）、`.specify/specs/096-sdd-observer-agent/test-evidence/review-r2-smoke.txt`（本轮实现段冒烟证据，回执时尚未提交）— disclosed, never concluded over | `git status --porcelain` at receipt time; the same sentence lives in `code-review.md` |
| Record | .specify/specs/096-sdd-observer-agent/code-review.md | written (triage = run) |
| Archive | .specify/specs/096-sdd-observer-agent/code-review-20261110T155402Z.md | rotated by `start` |

代码段四短语约束：本次以 `renderer: text` 运行，记录与结论均未声称可视化评审已完成。round-1 的 1 blocking / 1 important / 1 suggestion 已由 `262f30bde` 修复并在本轮复核：`_last_anomaly()` 与 `read_spine()` 的两处契约用例都有红腿（`test-evidence/review-repair-r1-red-green-probe.txt`），本轮冒烟全绿。本轮记录零 blocking / 零 important。

### 2.2 Artifact Review Segment

Artifacts: 10 / 10   missing: none

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md, test-evidence/ | union of the stage rules (Canonical Status State Machine: every SC has a `verification.md` status row) and `plan.md` § Project Structure (which declares research.md, feature-ref.md and test-evidence/) |
| Coverage line | 10 / 10 | present members / expected members |
| Missing members | none | — |
| Segment verdict | blocked | the finding rows below are this segment's record (all P2; none is a transition condition) |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P2 | .specify/specs/096-sdd-observer-agent/requirements.md | 181 | none | **AF-3** — Key Entities「记录条目」仍写「承载八类信息」，与 FR-011:142 的「九类」矛盾（历轮 carried over）；改为九类并引用 FR-011。 |
| P2 | .specify/specs/096-sdd-observer-agent/plan.md | 38 | none | **AF-4** — Constitution Check 渲染注记仍写 `(v1.19.0)`，实际宪法为 v1.19.1；更新版本 pin。 |
| P2 | .specify/specs/096-sdd-observer-agent/tasks.md | 33 | none | **AF-5** — GATE-4 披露句仍称 `verification.log` 字面「由框架级统一裁定」，该裁定已于 v1.19.1 完成；改为「已裁定为 verification.md（commit 34ea3eb76）」。 |
| P2 | .specify/specs/096-sdd-observer-agent/plan.md | 132-150 | none | **AF-6** — § Project Structure 的 Documentation 树没有列出 `verification.md`（全文亦未提及该产物），为后来 DoD-7 的延后留下缺口；把该成员加入树并声明其产出阶段。 |
| P2 | .specify/features.md | 102 | none | **AF-7** — 096 行 Last Updated 文本仍写「`verification.md` 与 Planned→Implemented 翻转归 closure 阶段 Pre-Status-Flip Gate（GATE-4）」，而 `verification.md` 已于 `262f30bde` 落盘；该句对 `verification.md` 的一半已过期。 |

**Round-1 修复复核（本段）**: AF-1（`verification.md` 缺失，P0）→ **fixed**：文件存在，7 条 SC 状态行齐全，smoke 三元组齐备，closure checker `accept`；AF-2（GATE-1 口径，P1）→ **fixed**：DoD-4（tasks.md:20）与 GATE-1（tasks.md:30）现以同一个两步判据表述，读数照实记 DEFERRED。AF-3…AF-6 维持 open（P2），本轮新增 AF-7（P2）。

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base |
| Head commit | 262f30bdeef601a41efd230c14317445a5da1fc8 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | `git-delta-review.sh base` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py tests/contract/test_sdd_observer_agent.py tests/contract/test_sdd_observer_lifecycle.py tests/contract/test_sdd_loop_driver_skill.py -q` | recorded verbatim |
| Smoke exit code | 0 | the integer the command returned（77 passed + 1 serial，26 s） |
| Smoke evidence path | .specify/specs/096-sdd-observer-agent/test-evidence/review-r2-smoke.txt | exists, non-empty（含命令行、全量输出、退出码、耗时） |
| Scope and regression verdict | scope: pass with disclosure — 区间内两个提交在本切片实现之后（`86f3a546a` 评审记录、`262f30bde` review-repair r1）；后者改 `journal-utils.py` 与契约测试，逐项追溯到 FR-012（anomaly 事件类）与引擎/owner 形状契约，属评审发现的修复而非无主工作；`verification.md` 与 DoD-7 由该提交补出。regression: pass for the feature modules — 四个 096 模块 77 passed + 1 serial，exit 0；全量套件 delta 仍按 GATE-1 读 **DEFERRED**（11 名均带 owner，零 096 模块 id），照实引用、不重新解释 | segment's own reading |
| Segment verdict | pass | the finding rows below are this segment's record (none) |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| — | — | — | — | （无实现段 finding：正确性、范围与回归三项均按上表读 pass） |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | Planned | `.specify/features/096.md` `**Status**`（与 `.specify/features.md` 096 行一致） |
| `final_path` record, copied verbatim (7/7) | pass 4 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 4 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/096-sdd-observer-agent --json`（exit 0，`verdict: accept`，`reasons: []`），never recomputed here |
| Comparison verdict | agree | checker `accept`；claim `Planned` 位于证据之后而非之前；两条拒绝条件均不成立（verdict 非 `block`；claim 非 `Implemented` / `Ready for Review`），`F-ACCEPTANCE` 不触发 |
| Failed condition, on refusal | none at ARC | ARC 本身不拒绝；转换拒绝来自状态机 from-state（见下） |
| Fixed item, on refusal | none | `F-ACCEPTANCE` 未触发 |

**Status transition judgement**: `Implemented → Ready for Review` is **refused**. 命名失败条件：**from-state 是 `Planned`，不是 `Implemented`** —— `Planned → Ready for Review` 不是状态机中的转换；该特性必须经由 `Implemented` 重新进入，而 `Planned → Implemented` 的 owner 是 `/speckit.implement`（本轮 review 不能代为落状态）。转换的四个合取条件本身在本树读为：(a) 零 `[~]` 任务行 → 满足；(b) 评审证据已产出（本报告）→ 满足；(c) 当前代码记录零 `blocking` → 满足；(d) 无 `final` 路径判据处于 `blocked` / `deferred` / `fail`（4/4 pass）→ 满足。The claimed status stays `Planned`. The unattended disposition is halt-and-report; the named refusal literal recorded in `### 2.1` and in this run's conclusion is `blocking-unresolved`.

## 3. Findings (Problems & Improvement Targets)

### F1 — The review gate reads an artifact that this line's stage plan places after review

- **Severity**: P0
- **Category**: Workflow
- **Location**: `.specify/specs/096-sdd-observer-agent/verification.md:1-11`; `templates/commands/implement.md:50`; `/storage/project/cloud-native-ai/spec-kit/.specify/state/096-sdd-observer-agent.md:31`; commit `262f30bde`
- **Evidence** (verbatim quote):

  ```
  **Outputs**: every task `[X]` or honestly `[~]`, the `## Completion Gate` re-validated against the current tree, `verification.md` populated, phase-boundary commits landed.
  ```

  ```
  - 阶段计划：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure → 合并 master`
  ```

  ```
  Recorded 2026-11-10 by the review-repair r1 pass (review finding AF-1), discharging
  GATE-4 / DoD-7 of tasks.md.
  ```

- **Why it's a problem**: the review's Acceptance Reality Check reads `verification.md`, and `/speckit.implement`'s own output contract says the implement stage populates that file; this line's stage plan ran `review` before `closure` and its implement stage closed without the file. Round 1's ARC was therefore structurally undecidable (checker exit 2), and the gate became evaluable only after a repair pass the plan never scheduled. The line-level symptom is repaired (`262f30bde`); the ordering conflict that produced it is not.
- **Proposed fix**: add an implement-stage row that writes `verification.md` and runs `python3 scripts/python/closure-acceptance-check.py --spec-dir <spec>` before review (or move review after closure in the driver stage sequence — the two orders cannot both hold). At framework level, make plan/tasks generation reject a stage plan whose review gate precedes the artifact that gate reads.

### F2 — The state spine contradicts the line it is supposed to record

- **Severity**: P0
- **Category**: Automation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/096-sdd-observer-agent.md:7` (`stage: requirements`), `:11` (`attempt: 0`), `:13` (`last_verdict: U0 entry written; requirements dispatching`), `:23` (`state: stalled`), `:124` (last `## Stage Record —` is analyze round 4), `:141` (tail `next stage: implement（analyze 门 round-4 未过…）`)
- **Evidence** (verbatim quote):

  ```
  stage: requirements
  attempt: 0
  last_verdict: U0 entry written; requirements dispatching
  ```

  ```
  state: `stalled`（U5；reentry-required）
  ```

  ```
  next stage: implement（analyze 门 round-4 未过：W13-17 为决策项，须先处置）
  ```

- **Why it's a problem**: the spine is the driver's only persistent state and the journal's primary carrier. It reports "stalled at requirements, attempt 0" while the worktree's 45-commit delta covers analyze round 5, implement wp01–wp04 (47/47 rows closed), review round 1 and review-repair r1. A reentry that reads the spine would restart at requirements; an observer projecting from the spine would record a false state. The r1 repair pass explicitly left spine carriage to the driver, so the divergence persisted through a repair cycle.
- **Proposed fix**: append the missing Stage Records (analyze round 5, implement, review round 1, review-repair r1) and refresh the loop-state block; add a driver-side close guard that compares the loop-state `stage` with the last Stage Record heading and fails the close when they disagree.

### F7 — The claimed status never left `Planned`, although all four `Planned → Implemented` conditions now hold

- **Severity**: P0
- **Category**: Workflow
- **Location**: `.specify/features.md:102`; `.specify/features/096.md:6`; `templates/commands/implement.md:58-59`; `scripts/python/closure-acceptance-check.py` output
- **Evidence** (verbatim quote):

  ```
  **Status**: Planned
  ```

  ```
  "claimed_status": "Planned",
  "verdict": "accept",
  "final_path": { "pass": 4, "total": 4, ... }
  ```

  ```
  the status claim is a gate product, never a stage self-assessment … (1) run the checker on the tree to be claimed …, (2) copy its `verdict` and emitted reasons into `REQUIREMENTS_DIR/verification.md`, (3) only then write the registry row / detail status.
  ```

- **Why it's a problem**: `/speckit.implement` owns `Planned → Implemented` and must land either `Implemented` (checker `accept`) or `Blocked` (checker `block`). This line landed neither: the implement close deferred the flip to a closure stage that has not run, so the working tree now satisfies all four conditions (checker `accept`, pass 4/4; zero open task rows; smoke green) while both registry carriers still read `Planned`. The review run's `Implemented → Ready for Review` transition consequently has no legal from-state — a status-quality defect on the line, not a quality defect of the feature.
- **Proposed fix**: run the implement close (status flip) now that the checker returns `accept` for this tree, or make the driver's implement-stage close enforce the status write (either `Implemented` or `Blocked`) so a stage cannot end with the status untouched. Do not make the review write `Planned → Implemented`; that transition's owner is `/speckit.implement`.

### F3 — The implement-entry full-suite baseline was not captured; GATE-1 still reads DEFERRED

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/096-sdd-observer-agent/tasks.md:20` (DoD-4), `:30` (GATE-1), `:40-52` (§ GATE-1 DEFERRED set)
- **Evidence** (verbatim quote):

  ```
  This line took no Step 0 capture; its same-day reconstructed baseline leaves a literal 11-id delta, so GATE-1 reads **DEFERRED** — every one of the 11 ids is named with its owner in § GATE-1 DEFERRED set and is never re-labelled as "zero NEW".
  ```

- **Why it's a problem**: round 1's AF-2 repair aligned the criterion (both DoD-4 and GATE-1 now state the same two-step test) but could not create the missing baseline. The gate remains undecidable as a closed-set claim: the 11-id delta is disclosed with named owners, and zero 096 module id is in it, but "zero NEW failed ids" still has no baseline to compare against.
- **Proposed fix**: make `/speckit.implement` Step 0 capture `bash scripts/bash/run-tests.sh --names-out <baseline>` before the first edit and make GATE-1 compare against that file; if a shared trigger store keeps the baseline unstable, isolate the store or keep the DEFERRED reading with its named owners.

### F4 — A machine-read path literal in the constitution conflicted with `.gitignore` and the implementation chain, surfacing only at analyze round 4

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/constitution.md:1-10` (Sync Impact Report); `.specify/specs/096-sdd-observer-agent/test-evidence/analyze-merged-r4-2026-11-10.md`
- **Evidence** (verbatim quote):

  ```
  - Version change: 1.19.0 → 1.19.1 (PATCH; carrier correction, 2026-11-10)
  - Modified principles: VII. Workflow Gates — the Pre-Status-Flip Gate's status-line carrier is corrected from `verification.log` to `verification.md`
  ```

  ```
  round-4 未过 —— 1 条 open HIGH（W13-17）
  ```

- **Why it's a problem**: the plan-stage Constitution Check rendered 22 Pass rows against a constitution whose record carrier (`verification.log`) is excluded by `.gitignore` and unread by every machine consumer. The conflict survived requirements, plan, tasks and three analyze rounds, then forced an in-line constitutional amendment and a fifth analyze round. A plan-stage check that verifies only principle prose cannot catch a machine-read path that no chain reads.
- **Proposed fix**: add a plan-stage gate row — "every record carrier this plan names is (a) committable under the repository's ignore rules and (b) read by a named machine consumer" — and render the Constitution Check against the live version (the v1.19.0 pin is a symptom).

### F5 — Stale version and adjudication text after v1.19.1

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/096-sdd-observer-agent/plan.md:38`; `.specify/specs/096-sdd-observer-agent/tasks.md:33`
- **Evidence** (verbatim quote):

  ```
  Rendered by enumerating every `### <numeral>. <name>` heading of `.specify/constitution.md` (v1.19.0) in file order
  ```

  ```
  Disclosure: 宪法 VII 的 `verification.log` 字面由框架级统一裁定（反馈已登记：`.specify/memory/feedback/20261110T124821Z-skill-sdd-loop-driver.md`），本线按框架链执行（唯一载体 `verification.md` …）
  ```

- **Why it's a problem**: the amendment already happened (v1.19.1, commit `34ea3eb76`); the plan still pins v1.19.0 and the tasks still describe the carrier question as awaiting a ruling. The carrier instruction in the same sentence is still correct, so this is drift, not a behavior defect — but it is exactly the kind of stale fact that makes later readers distrust the artifacts.
- **Proposed fix**: update the plan's version pin to v1.19.1 and rewrite the GATE-4 disclosure as "v1.19.1 已裁定为 `verification.md`（commit `34ea3eb76`）".

### F6 — `specify render-agents` refreshes unrelated agent copies as a side effect

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/096-sdd-observer-agent/tasks.md:248` (T041); `.claude/agents/reporter.md`; `.github/agents/reporter.agent.md`; `.opencode/agents/reporter.md`; `.qoder/agents/reporter.agent.md`
- **Evidence** (verbatim quote):

  ```
  +<!-- 092 handoff: D4 — 周期数值的唯一 owner 是 `.specify/shared/guidelines/reporting-obligations.md` § 二（长跑档 30 s）；上一行只抵达 `progress-reporting.md` 的交互档缺省与内容下限，该行保留不改、仅作历史记录。参见 092 D4，2026-11-09。 -->
  ```

- **Why it's a problem**: a feature-scoped render obligation silently changes four files owned by other features. The delta stays small here, but the pattern means every feature that renders agents can carry another feature's pending render drift, making the slice's scope claim unverifiable from the diff.
- **Proposed fix**: add a per-agent filter to `specify render-agents` (e.g. `--agent sdd-observer`) or declare the refreshed copies in the plan's Mirror Obligations table and verify them by name; do not let an unlisted copy change inside a feature delta.

## 4. What Worked — Preserve (Brief)

- The journal engine's closed-structure + single declaration owner design is real: `journal-format.yaml` holds every spelling, the engine reads it through `declaration_reader`, and the tamper/gap/dual-line/single-writer drills are genuine red/green tests rather than prose assertions.
- The round-1 repair landed with red-first discipline: `_last_anomaly()` and the whitespace-stripping owner-block parse each carry a contract case with a reproducible red leg (`review-repair-r1-red-green-probe.txt`), and the repaired tree's closure checker reads `accept`.
- `verification.md` now makes GATE-4 decidable: 7 SC status rows with evidence pointers, one joint-acceptance row for `RS-003`, and a single smoke triple whose evidence path exists and is non-empty.
- Evidence discipline in `test-evidence/` is strong: every gate reading names its command, exit status and file, and the GATE-1 baseline reconstruction is disclosed as a deviation rather than hidden.
- The analyze repair loop produced traceable dispositions (r3/r4/r5) and recorded the constitutional carrier correction with a user ruling, so the amendment is auditable.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Implement-stage verification carrier** — Target: `templates/commands/implement.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/templates/commands/implement.md`) § Feature Integration, and `templates/tasks-template.md`. Change: make `verification.md` a required implement-stage output row and state that a DoD row may not defer it to a later stage; the review's ARC reads it before any status flip. Source: F1. Expected impact: review and implement stop disagreeing about when the acceptance record exists.

### 5.2 Command Prompt Improvements

- None beyond F1's implement-template row; the review prompt already states the ARC clause correctly.

### 5.3 Automation / Script Improvements

- **State-spine close guard** — Target: `skills/external/sdd-loop-driver/SKILL.md` § 状态脊 + the driver's stage-close script. Change: at every stage close, append the Stage Record and refresh the loop-state block in the same step; fail the close when `stage` and the last Stage Record heading disagree. Source: F2. Expected impact: a stale spine becomes detectable at the moment it occurs, not at review.
- **Implement Step 0 baseline capture** — Target: `skills/internal/implement-feature/SKILL.md` Step 0. Change: capture the full-suite name list before the first edit and make `tasks.md` GATE-1 compare against that file. Source: F3. Expected impact: the closed-set gate becomes decidable without post-hoc reconstruction.
- **Status write enforced at implement close** — Target: `skills/internal/implement-feature/SKILL.md` (Pre-Status-Flip Gate step) and the driver's implement-stage close. Change: fail the stage close when the registry row and the detail status were not written after the checker returned a verdict. Source: F7. Expected impact: a line cannot end implement with the status untouched and no legal from-state for review.
- **Per-agent render filter** — Target: the `specify render-agents` CLI entry in `src/specify_cli/__init__.py`. Change: add a per-agent selector so a feature renders only the templates it owns; or record every refreshed copy in the plan's Mirror Obligations. Source: F6. Expected impact: feature deltas stop carrying other features' render drift.

### 5.4 Workflow Improvements

- **Plan-stage carrier committability check** — Target: `templates/plan-template.md` / `skills/internal/create-plan/SKILL.md`. Change: add the record-carrier check from F4 as a plan gate row and render the Constitution Check against the live version. Source: F4, F5. Expected impact: path literals that no machine reads, or that `.gitignore` excludes, are caught before analyze.

### 5.5 Documentation Improvements

- **Refresh the v1.19.1 residue** — Target: `plan.md:38`, `tasks.md:33` inside this spec. Change: update the version pin and rewrite the carrier disclosure as a completed ruling. Source: F5. Expected impact: the spec no longer contradicts the constitution it cites.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Produce `verification.md` at implement close and judge the review gate after it exists | `templates/commands/implement.md`, `templates/tasks-template.md` | F1 |
| P0 | Make the state spine self-consistent at every stage close | `skills/external/sdd-loop-driver/SKILL.md` § 状态脊 | F2 |
| P0 | Enforce the status write at implement close (`Implemented` or `Blocked`) | `skills/internal/implement-feature/SKILL.md`, driver stage close | F7 |
| P1 | Capture the implement-entry suite baseline in Step 0 | `skills/internal/implement-feature/SKILL.md` Step 0 | F3 |
| P1 | Add the plan-stage carrier committability gate | `templates/plan-template.md`, `skills/internal/create-plan/SKILL.md` | F4 |
| P2 | Refresh v1.19.1 residue and the plan tree | this spec's `plan.md`, `tasks.md` | F5 |
| P2 | Scope `render-agents` per agent | `src/specify_cli/__init__.py` | F6 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target lacks a repo-relative form.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] **P0 validation status is stated explicitly.** F1, F2 and F7 were each confirmed by a fresh-context, read-only independent validator that received only the finding, its anchors and the quoted evidence; all three returned `confirm` (no reject, no downgrade). The artifact P0 from round 1 (`AF-1`) is closed by an existence measurement (file present, checker `accept`), and round 2 raised no new artifact or implementation P0.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
