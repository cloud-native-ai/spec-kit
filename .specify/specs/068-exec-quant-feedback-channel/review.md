# Specification-Driven Development (SDD) Process Review Report: 执行量化数据反馈回传与汇总（Exec-Quant Feedback Channel）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 068 |
| Requirement Key | 068-exec-quant-feedback-channel |
| Requirement Name | 执行量化数据反馈回传与汇总（Exec-Quant Feedback Channel） |
| Related Feature | 068 执行量化数据反馈回传与汇总（Exec-Quant Feedback Channel） |
| Repository | spec-kit |
| Repository URL | Fork situation: `origin` = `git@github.com:github/spec-kit.git` (the UPSTREAM, holds none of these commits). Remotes that carry this work (all SSH-only): `github` = `git@github.com:cloud-native-ai/spec-kit.git`, `gitlab` = `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`, `gitee` = `git@gitee.com:cloud-native-ai/spec-kit.git`. |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — the HEAD commit is unpushed and all remotes are SSH-only (no HTTPS web blob URLs renderable). Cite absolute paths + `git show <sha>:<path>` recovery. Example: `git show d23a50e3:.specify/specs/068-exec-quant-feedback-channel/tasks.md` on any clone that later receives the branch. |
| Branch | 068-exec-quant-feedback-channel |
| Commit SHA | d23a50e387b4c41d417c05e1fc05a96822057454 (short: d23a50e3) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-10-22 |
| Reviewer (Agent) | SDD Executor — host-native subagent, fresh-context dispatch of the unattended `/speckit.review` stage (line `speckit-068-execquant-feedback`); not the authoring session of any artifact under review |
| Environment | Linux 5.10.134-15.2.al8.x86_64; Python 3.11.11; pytest 8.4.2 (canonical runner `scripts/bash/run-tests.sh`); bash; git 2.x |
| spec-kit Source Snapshot | This repository IS the spec-kit framework source (self-hosting repo, "two hats"): version 0.0.22 (`pyproject.toml`) @ d23a50e3, unpushed |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 277 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/requirements.md | 19 FR / 6 SC / 4 US, 059-revision table, 11 clarify rulings, 2 shared strings |
| plan.md | 131 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/plan.md | 16/16 constitution self-score, mirror obligations, test strategy, phase 0/1 summaries |
| research.md | 207 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/research.md | Decisions D1–D14 with file:line dated measurements of both engines and stores |
| data-model.md | 137 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/data-model.md | Entities E1–E8 (existing records untouched; payload/manifest/envelope/summary shapes) |
| contracts/ (4 files) | 276 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/contracts/ | 31 clauses C-1…C-31: package-layout 9, intake 8, aggregate 6, compatibility-security 8 |
| quickstart.md | 132 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/quickstart.md | 6 scenarios, route-a live vs route-b contract-pinned verification split |
| feature-ref.md | 63 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/feature-ref.md | Feature binding + FR 19/19, SC 6/6 mapping tables |
| checklists/ (3 files) | 164 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/checklists/ | Domain checklist CHK001–040 + report with 10 findings + generic spec checklist |
| tasks.md | 337 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/tasks.md | 30 tasks T001–T030 in 4 US phases + polish, 9 gates, coverage map, test budget |
| verification.md | 263 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/verification.md | SC-001…006 matrix with evidence SHA bindings + T030 gate table + status flip record |
| coverage-baseline.txt | 497 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/coverage-baseline.txt | Frozen uncovered-clause list, base-sha 7912b29d, 168 files (85 parsed + 83 named) |
| baseline-failed.txt | 84 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/baseline-failed.txt | E2 full-suite baseline failing nodeids (4467 passed / 84 failed) |
| notes/ (3 files) | 1257 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/notes/ | pre-change-measurements (281), quickstart-run (144), red-first-evidence (832) |
| test-evidence/ (16 files) | — | /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/test-evidence/ | Per-stage E3 status rows + frozen/full/regression/final test logs + review-targeted log |

## 1. Process Execution Timeline

Reconstruct what actually happened during this feature's SDD lifecycle. Capture deviations from the prescribed `/speckit.*` flow, ad-hoc artifacts, manual workarounds, and concrete friction moments. Order chronologically. This section is the raw material for Section 3 — keep it factual, not editorial.

All 25 commits recovered via `git log --oneline -- .specify/specs/068-exec-quant-feedback-channel/`; the commit series is story/task-grouped (one commit per stage or implement segment), so the per-segment attribution below is commit-traced, not inferred. Where an event left no in-repo trace (turn-budget exhaustion, driver bookkeeping), the row says so and names the local-only record that holds it.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Branch `068-exec-quant-feedback-channel` created from master 7f9033ec before any artifact existed | `git reflog show 068-exec-quant-feedback-channel` → "7f9033ec …@{2026-10-22 14:35:12 +0800}: branch: Created from HEAD" | No — single write line as declared |
| 2 | requirements stage: spec + checklist + evidence committed | 981c037f (14:40:33 +0800) | No |
| 3 | clarify stage committed, then immediate repair: two live normative headings containing "修订" were being skipped by the pre-analyze history filter, so FR-015…FR-018 were reported dangling; headings renamed to satisfy the gate | 32fe15c8 + repair 2a523e6b (diff: `-#### 边界腿——修订后的安全边界与非回归（US4）` → `+#### 边界腿——变更后的安全边界与非回归（US4）`) | Yes — gate-driven artifact rename (artifact bent to fit the tool, see F7) |
| 4 | plan stage: plan/research/data-model/contracts ×4/quickstart/feature-ref landed; feature Draft → Planned | b732731c | Yes — quickstart baseline claim drift corrected in passing (400eca59) |
| 5 | tasks attempt 1 ANOMALY: all four contracts were written as `## C-PL-01`-style headings; the clause extractor reports that form as `md-none` (zero usable clauses), so green claims could not resolve. No artifacts committed from this attempt | `git show b732731c:.specify/specs/068-exec-quant-feedback-channel/contracts/package-layout.md` → `## C-PL-01 载荷采集（read-only sweep）`; `.specify/scripts/python/clause_extract.py` FORMS includes `"md-none"` | Yes — stage aborted on a tooling-form mismatch the plan-stage gate had passed (see F1) |
| 6 | Contract clause ids canonicalized to C-1…C-31; tasks stage then landed 30 tasks with gates green | 0f8ad232 + 7912b29d | Yes — repair commit inside the stage |
| 7 | tasks U4 corrections: coverage-baseline frozen and 3 missing contract citation groups (C-8/C-25/C-26) added, because GATE-7 first ran with no baseline file (495 uncovered / 3 FRs uncovered) | d0ba5050; `coverage-baseline.txt` header `base-sha: 7912b29d2539` | Yes — gate forced the stage to produce an artifact it had scheduled for implement (see F8) |
| 8 | checklist stage: 40-item domain checklist, 10 findings recorded docs-only; command-template wrap-up engine steps not executed (disclosed in report) | b11f007e; `checklists/report-exec-quant-feedback-20261022.md` § Boundary & Process Notes | Yes — see F11 |
| 9 | analyze attempt 1: 1 HIGH (F-01 — identity_key included content_hash, making the conflict branch dead code) → remediation synced 5 artifact surfaces; attempt 2 clean | a24cbf72 (`--stat`: contracts/intake-contract.md, data-model.md, requirements.md, research.md, tasks.md) + N-01 sync 4480ba7e | No — analyze working as designed; but the sync list missed the feature-detail registry (see F5) |
| 10 | implement part 1: E2 full-suite baseline frozen (4467 passed / 84 failed, 273 s); T001–T003 closed | 47cd37e8 + GATE-9 scoping 55766ad5 | Yes — audit gate could not exit 0 before review, so tasks GATE-9 was pre-scoped to the expected future-stage gap (see F2) |
| 11 | implement part 2 (US1 packaging leg): 20 unit + 17 contract tests red-first, then implementation; the executing subagent exhausted its 120-turn budget at final bookkeeping — code/tests/evidence were complete and only T009 marking/commit remained, which the driver completed. One existing 059 structural pin (`test_packaging_is_structurally_excluded`) contradicted the adjudicated boundary revision and was rewritten in the same batch | 6aac1b6b (1317 insertions: engine +336, new tests +771); `notes/red-first-evidence.md` § 实现期修正记录; the budget event itself is recorded only in the run line's local state spine (external to repo) and `skills/external/sdd-loop-driver/references/dispatch-recipes.md` line 29 | Yes — two deviations: driver-finished bookkeeping (F3) and cross-feature pin revision inside a feature batch (F6) |
| 12 | implement parts 3a–3c (US2 intake leg): 16+20 red-first, then 109 green; scripts mirror sync rewrote 26 drifted mirrors while only feedback-utils.py was the feature target — 25 collateral mirrors appeared in the worktree and were restored by the driver; one false-green assertion corrected and disclosed | 5462b531, db0371a0, 0afdcc8e; `notes/red-first-evidence.md` § T011 ("该 1 例通过属**假绿**…归因 = 断言面缺陷…修正后断言…更名为 `test_missing_package_flag_exit_2`") | Yes — collateral mirror churn (F4) |
| 13 | Human checkpoint: efficiency review requested; line parked at part 3b; resumed ~5 min later | run line's local state spine (external to repo): "user checkpoint: 2026-10-22T08:25Z … user resumed: 2026-10-22T08:30Z" | Yes — human pause mid-implement (unattended line, orchestrator-approved) |
| 14 | implement parts 4a–4c (US3 aggregate leg): 23+6 red-first, then 31+6 green; action-set guards (`ACTIONS_CLOSED_SET`, probe expected set, `FEEDBACK_ALLOWED`) amended in the same batch — one of which (`FEEDBACK_ALLOWED += ingest-exec-quant`) was owed from the US2 segment and was discovered already red at 4b's adjacency patrol; mirror churn restored again | 523c8e75, 2c54fc4b, 1b1603dc; `notes/red-first-evidence.md` § 4b 断言修正 #4 ("该项为 **US2 段（db0371a0）欠下的同批修订**，4b 邻接巡检时发现其红（非本段引擎改动引入，HEAD 即红）") | Yes — owed pin amendment left the tree red across segments 3b→4b (F6); churn (F4) |
| 15 | implement part 5 (US4 boundary/compat guards): 11 + 6 guard tests green; 24-file name-level regression 2 failed/545 passed with zero new failing nodeids vs frozen baseline | d2fd6270; `test-evidence/log-current-post-impl-names.txt` | No |
| 16 | implement parts 6a/6b (polish): docs/skills/shared/template sources + 4 feature mirrors + 4 per-tool copies committed (108 collateral mirrors restored); quickstart scenarios 0–5 live-run with /tmp fixtures; SC matrix + gate table written; feature 068 flipped Planned → Implemented; one in-passing repair disclosed (quickstart legacy-member probe compared whole-stream bytes, fixed probe-side) | ea2883bf, 1088d4ca, d23a50e3; `notes/quickstart-run.md`; verification.md §T030 | Yes — in-passing probe repair disclosed per TDD discipline; final 24-file rerun 547 passed / 0 failed (`log-final-post-sync-names.txt`, 0 bytes) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 6 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 0 |
| Automation / Scripts | 3 |
| Workflow | 6 |
| Documentation | 1 |

**Validation status (objective-analysis-gate + review-sdd-process §5)**: No P0 findings raised; the P0 independent-validation pass is vacuously satisfied. Same-author condition: the artifacts were authored by earlier dispatches of the same unattended line, while this reviewer is a fresh-context dispatch — the gate's strict firing condition (same session) does not hold, and detection was performed by direct read of the committed tree. No validation subagent dispatch tool exists in this run; had any P0 been raised, rows would carry `(validated: direct re-read, subagent unavailable)` per the documented fallback. All findings below are P1/P2, which skip validation by rule; the two rows repaired in passing during this review are marked as such inline.

**Merge verdict**: **PASS — merge-ready from the process-quality standpoint.** The artifact chain is internally consistent, evidence-complete (SHA-bound), gate-clean at implement close (GATE-1…GATE-8 PASS; GATE-9 pass under its declared implement-stage criterion), and the committed tree re-verified green at review open (85/85 targeted, rc=0). No P0 process defect blocks merge. The E2 full-suite closure-slot name-level comparison is open **by design** (tasks.md § Test Budget: "该槽属 review/closure 阶段，implement MUST NOT 预先消耗") and is owned by the post-review closure stage; the six P1 findings are framework-side follow-ups for spec-kit sources, not feature-merge blockers.

## 3. Findings (Problems & Improvement Targets)

> List **only** problems, friction, ambiguities, and concrete improvement targets. Each finding MUST include an inline quoted excerpt of the offending text and a concrete proposed fix. Order by severity (P0 → P1 → P2), then by category. Drop any finding that lacks evidence — vague complaints are not actionable.

### F1 — Plan-stage gate passes `md-none` contracts; clause-syntax mismatch surfaces one stage later as an ANOMALY

- **Severity**: P1
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py (clause handling at `definitions()`; no form check exists in the file)
- **Evidence** (verbatim quote):

  ```
  git show b732731c:.specify/specs/068-exec-quant-feedback-channel/contracts/package-layout.md
  → "## C-PL-01 载荷采集（read-only sweep）"

  .specify/scripts/python/clause_extract.py (FORMS tuple) → "md-none"

  grep -c "md-none" skills/external/sdd-loop-driver/scripts/pre-analyze-check.py → 0

  tasks.md § Notes (post-repair): "契约条款使用规范 `C-1`…`C-31`（`clause_extract.py` 实测 31 条 md-bold-closed）"
  commit 0f8ad232 "fix(068-exec-quant-feedback-channel): canonicalize contract clause ids for coverage"
  ```

- **Why it's a problem**: The plan stage declared its gate green while all four contracts used heading ids (`C-PL-01`) that the clause machinery classifies `md-none` — zero extractable clauses. The mismatch was caught only when the tasks stage tried to pin green claims to clauses, costing a full stage ANOMALY, an uncommitted attempt, and a repair commit (0f8ad232) that rewrote 31 clause ids across four files. Every downstream consumer (coverage baseline, `[green:]` claims, `account-clause-coverage.py`) inherited the churn. The tool that would have caught it (`clause_extract.py`) exists; the plan-stage gate simply never invokes its form verdict.
- **Proposed fix**: In `pre-analyze-check.py`, run `clause_extract.form_of()` over every `contracts/*` file when the stage is `plan` (or later) and emit an error on `form=md-none` or zero extracted clauses; alternatively have the plan-stage U4 checklist run `python3 scripts/python/clause_extract.py <contracts/*.md>` and fail on `md-none`. Either surfaces the mismatch at the stage that created it.

### F2 — `audit-test-budget.py --stage-check implement` counts the future `review` stage in its denominator, so the implement gate cannot exit 0

- **Severity**: P1
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/audit-test-budget.py (docstring lines 12–14; `E3_STAGES` line 34)
- **Evidence** (verbatim quote):

  ```
  audit-test-budget.py docstring: "per-stage ``stage-status`` completeness over the
  full applicable-stage denominator (a missing or empty evidence file stays in the
  denominator and reports ``unknown``)."
  audit-test-budget.py line 34: E3_STAGES = ("clarify", "plan", "tasks", "checklist", "analyze", "review")

  tasks.md GATE-9: "implement 期判据 = 输出 `slots=baseline:1 closure:0` 且唯一 error 为
  `review: stage evidence file missing`（review 证据由 review 阶段落盘，属预期未来阶段）；
  最终 closure 审计在 review 后以 `--stage-check closure` 要求 exit 0"

  verification.md §T030: "`status=fail`，reason = `review: stage evidence file missing`——
  唯一 error 恰为预期未来阶段项，判据内判定 **PASS（implement 期）**"
  ```

- **Why it's a problem**: A stage gate whose canonical result cannot be exit 0 forces every implement run to hand-interpret a red exit as "the right red" — exactly the reading-a-green-check-as-evidence hazard the fast-fail discipline names. The workaround (declaring the sole error "expected" in two artifacts) is now copy-paste boilerplate every future feature must reproduce, and a genuinely missing earlier-stage evidence file hides behind the same red exit.
- **Proposed fix**: Make `--stage-check <stage>` require stage-status completeness only for stages at or before `<stage>` (the checked stage's own prefix), or add an explicit `--allow-future-stages review,closure` flag so the implement-stage invocation is green by construction and any other missing evidence file still fails.

### F3 — TDD-heavy implement segments exhaust the 120-turn budget; the second budget raise in a row did not converge

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/dispatch-recipes.md (line 29; owner `agents/sdd-executor.agent.md` line 10)
- **Evidence** (verbatim quote):

  ```
  dispatch-recipes.md:29: "**默认预算**：阶段执行子代理的 `run-turn-budget` 为 **120**
  （owner：`agents/sdd-executor.agent.md`；2026-10-22 由 40 上调，依据：065a implement
  阶段 30 个任务在 40 回合耗尽）。预算变更属 source change，必须同步 agent 模板、
  `.specify/agents/templates/` 镜像与各工具 render。"

  commit 6aac1b6b --stat (the segment that exhausted the budget): "7 files changed,
  1317 insertions(+), 21 deletions(-)" — engine +336, two new test files +771

  notes/red-first-evidence.md § T004/§ T005: 20 + 17 red-first cases recorded, then
  § T006/T007/T008 绿证据 "37 passed in 0.19s"
  ```

- **Why it's a problem**: The US1 segment (2 test files with 37 cases + a 328-line engine implementation + red-first evidence capture) exhausted the 120-turn budget at final bookkeeping; the code/tests/evidence were complete and only task marking/commit remained for the driver to finish (event recorded in the line's local state spine — external to the repo; the budget text itself and the segment's commit size are the in-repo traces). Raising the budget (40 → 120 for 065a) treats the symptom; two consecutive features have now hit the ceiling, which means segment sizing — not the number — is wrong.
- **Proposed fix**: In `dispatch-recipes.md`, add a segment-sizing rule: split TDD-heavy segments at the test-writing/implementation boundary (test-authoring sub-segment, then implementation+green sub-segment), or size `run-turn-budget` per segment from the task row count × measured turns-per-TDD-row rather than a stage-wide constant.

### F4 — Scope-level `sync-mirrors --only scripts` rewrites all drifted mirrors in the scope; the file-level capability the script already has was not prescribed

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md (task-row prescriptions; secondary: /storage/project/cloud-native-ai/spec-kit/scripts/python/sync-mirrors.py `--only` implementation)
- **Evidence** (verbatim quote):

  ```
  scripts/python/sync-mirrors.py argparse help: "--only PATH  restrict the run to this
  repo-relative path prefix (repeatable); skips the regen-command-copies delegation
  unless a prefix targets templates/commands/"

  tasks.md T014 (as executed): "`python3 scripts/python/sync-mirrors.py --write --only
  scripts` 后 `--check` 复查…"

  notes/red-first-evidence.md § T021: "附带改动：`--only scripts` 写入同时重写了 25 个
  继承漂移镜像（T001 基线内既有 DIFF 的字节收敛）；按派发纪律仅提交
  `.specify/scripts/python/exec-quant.py`，其余 25 个留工作树由驱动统一还原（与 3c 段
  同模式），镜像本体零手改。"

  implement-stage-status.jsonl part 4c `changed_paths`: lists all 25 collateral
  .specify/scripts/* mirror files alongside the one intended mirror
  ```

- **Why it's a problem**: The script already accepts file-level prefixes (`--only scripts/python/feedback-utils.py` restricts the sync to that pair — `pair_subprefixes()` implements sub-prefix scoping), but the generated task rows prescribed the scope-level flag, so each of the three mirror-sync tasks (T014, T021, T027) dragged 25–108 collateral mirror rewrites into the worktree that the driver then had to restore. The zero-NEW-drift criterion held both times, but the pattern is one driver mistake away from committing unintended mirror drift, and it polluted every segment's `changed_paths` evidence.
- **Proposed fix**: In `create-tasks/SKILL.md` (and the plan template's Mirror Obligations guidance, `templates/commands/plan.md`), prescribe the minimal `--only <file-or-pair-prefix>` for each sync task row — the exact paths the feature edited are known at task-generation time. Optionally, `sync-mirrors.py --write` prints a collateral count ("N files outside your --only prefix will also be rewritten") so a scope-level invocation is at least visible at execution time.

### F5 — Analyze F-01 remediation synced five artifact surfaces but missed the durable feature-detail registry, leaving a contradicted identity-key formula in `.specify/memory/features/068.md`

- **Severity**: P1
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/memory/features/068.md (§ Implementation Notes, first bullet)
- **Evidence** (verbatim quote):

  ```
  requirements.md FR-008: "content_hash 仅用于同身份内容比较、MUST NOT 进入 identity_key"

  contracts/intake-contract.md C-13: "`identity_key = sha256(source_project ␟ unit_id ␟
  unit_type ␟ run_id ␟ collected_at)`（␟ = `\x1f` 分隔；五元组不含内容；D6）。"

  .specify/memory/features/068.md (stale, still at HEAD): "identity key =
  source_project+unit_id+unit_type+run_id+collected_at+canonical 内容哈希"

  commit a24cbf72 --stat (the F-01 remediation): touched exactly
  contracts/intake-contract.md, data-model.md, requirements.md, research.md, tasks.md —
  features/068.md is absent. The committed unit test
  `tests/unit/test_feedback_intake_exec_quant.py::test_identity_key_excludes_content_f01`
  pins the corrected behavior.
  ```

- **Why it's a problem**: This is the canonical same-author defect class the objective-analysis gate exists for — a correction landed in five places and not in the sixth, because the author knows the intended reading and supplies it silently at each copy. A maintainer reading the durable feature registry (the file that outlives the spec directory) would reason against a six-component identity key that the shipped code, contract, and test all contradict. *(Repaired in passing during this review — correction-class: FR-008/C-13/test/clarify session record exactly one intent, the fix is one local line, no downstream premise depends on the stale wording; disclosed here and in the wrap-up. The finding is retained for the process gap.)*
- **Proposed fix**: In the analyze stage's owner (`skills/internal/analyze-artifacts/SKILL.md`, remediation-sync section), require every remediation to enumerate its **durable surfaces** — `.specify/memory/features/<ID>.md` and `.specify/memory/features.md` alongside the spec-directory artifacts — and verify the sync list against a grep for the corrected fact, so a missed copy fails the re-run instead of surviving into the registry.

### F6 — Cross-feature test-pin revisions ride inside feature batches; one owed amendment left the tree red for a full segment

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/notes/red-first-evidence.md (§ 实现期修正记录; § 4b 断言修正 #4); recurrence context: register row REC-063-10 (open)
- **Evidence** (verbatim quote):

  ```
  notes/red-first-evidence.md § 实现期修正记录 (part 2): "059 的结构钉「feedback 引擎源
  零 `exec-quant` 字面引用」。该断言与本特性已裁决的边界修订正面相抵…按 owner SKILL §
  TDD 「断言与已裁决需求相抵 → 修断言并引用裁决」处置：该钉改写为修订后边界的结构形态
  `test_packaging_quant_coupling_is_read_only`"

  notes/red-first-evidence.md § 4b 断言修正 #4: "`tests/contract/test_exec_quant_engine.py`
  的 `ACTIONS_CLOSED_SET` 与 `tests/contract/test_probe_engine_action_sets.py` 的
  exec-quant 期望集 += `aggregate`（双向精确钉零放松）；同文件 `FEEDBACK_ALLOWED` +=
  `ingest-exec-quant`——该项为 **US2 段（db0371a0）欠下的同批修订**，4b 邻接巡检时发现
  其红（非本段引擎改动引入，HEAD 即红），按同一先例就地补齐并披露。"

  register REC-063-10 (open): "跨特性状态钉封闭窗口规则：特性域状态钉（窗口钉/封闭集/
  字节预算）**创作时**必须声明封闭规则；修订他特性之钉须按 REC-063-08 载体登记日期行"
  ```

- **Why it's a problem**: The adjudication and disclosure were correct (the 059 pin contradicted a requirement-level boundary revision), but the discipline that would make this routine is still missing: neither pin carried the closure-rule declaration REC-063-10 requires, the pin rewrites are buried as hunks inside feature commits (6aac1b6b, 2c54fc4b) rather than separately attributable rows, and the owed `FEEDBACK_ALLOWED` amendment sat un-instantiated from db0371a0 (08:20Z) until 4b (08:58Z) — a window where HEAD was red on an existing guard suite, which breaks bisectability and any concurrent flow's gate reads.
- **Proposed fix**: In `skills/internal/implement-feature/SKILL.md` (TDD/adjacent-guard section), add: (a) a pin-revision rule — when a segment's implementation requires amending another feature's closed-set pin, the amendment lands in the **same segment** that creates the debt (never carried across segments) and the commit message names the pin + the adjudicating requirement row; (b) a pointer to REC-063-10's register-row obligation so each amendment also carries its dated register line, closing the loop with the already-open 063 recommendation.

### F7 — `SKIP_HEADING` treats any heading containing "修订" as history, so live normative sections get skipped and artifacts must rename themselves to pass

- **Severity**: P2
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py (line 34–35)
- **Evidence** (verbatim quote):

  ```
  pre-analyze-check.py:34-35:
  SKIP_HEADING = re.compile(
      r"(?i)repair record|repair log|history|changelog|修订|变更记录|修复记录")

  commit 2a523e6b (the repair):
  -### 对 059 的修订关系（显式声明，无静默矛盾）
  -#### 边界腿——修订后的安全边界与非回归（US4）
  +#### 边界腿——变更后的安全边界与非回归（US4）
  ```

- **Why it's a problem**: A bare-word substring match ("any heading containing 修订 is a dated/history section") caused the gate to drop FR-015…FR-018 — the live boundary requirements of this very feature — and report them as dangling IDs. The artifact was renamed (losing the more accurate "修订后的" wording, which is semantically load-bearing for a spec that revises a predecessor's FR) purely to satisfy a false-positive filter. Any future spec with a normative heading containing 修订/变更记录 will trip the same trap.
- **Proposed fix**: Restrict the history-skip in `pre-analyze-check.py` to headings that carry a date or record marker (e.g. require a `\d{4}-\d{2}-\d{2}` token or an explicit 修订记录/变更历史 compound), so live sections containing the bare word stay in the analyzed set.

### F8 — Tasks-stage coverage gate depends on a baseline file the stage does not produce until forced, creating a duplicate freeze obligation

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/tasks.md (GATE-7 and T002 as generated); owner: /storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md
- **Evidence** (verbatim quote):

  ```
  tasks.md GATE-7 (as generated): "check: `python3 .specify/scripts/python/
  account-clause-coverage.py .specify/specs/068-exec-quant-feedback-channel` exit 0，
  输出 claimed clauses 31 / FR uncovered 0 / uncovered beyond baseline 0"

  tasks.md T002 (as generated, an implement-Setup task): "冻结契约覆盖基线：…`--freeze >
  .specify/specs/068-exec-quant-feedback-channel/coverage-baseline.txt`"

  coverage-baseline.txt header: "base-sha: 7912b29d2539" (the tasks-stage commit —
  the freeze content originates from the tasks-stage window)

  commit d0ba5050 "fix(068-exec-quant-feedback-channel): complete contract citation
  groups and freeze coverage baseline" (the U4 correction that made GATE-7 pass)
  ```

- **Why it's a problem**: GATE-7 compares live coverage against `<spec-dir>/coverage-baseline.txt`, but that file was scheduled to be created by T002 during implement Setup — so the tasks stage's own gate could not pass at validation time: the first run reported 495 uncovered / 3 FRs uncovered, and U4 had to generate the frozen baseline itself (d0ba5050). The baseline header's `base-sha: 7912b29d2539` (the tasks-stage commit) confirms the freeze happened in the tasks-stage window, while tasks.md still carried T002 as an implement task executing the same freeze — one artifact, two scheduled obligations.
- **Proposed fix**: In `create-tasks/SKILL.md`, make the baseline freeze a tasks-stage obligation (performed during U4 before GATE-7 runs, not an implement Setup row), or make GATE-7's baseline-dependent assertion explicitly conditional with a pointer to the implement task that will satisfy it. One owner, one execution.

### F9 — verification.md records the wrong branch; the closure-consumed record misdirects the merge

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/verification.md (Run header, lines 3–4)
- **Evidence** (verbatim quote):

  ```
  verification.md: "**Run**: 2026-10-22 · Python 3.11.11 / pytest 8.4.2 · canonical runner
  `scripts/bash/run-tests.sh` · branch `master`"

  git reflog show 068-exec-quant-feedback-channel:
  "7f9033ec 068-exec-quant-feedback-channel@{2026-10-22 14:35:12 +0800}: branch: Created from HEAD"
  "981c037f 068-exec-quant-feedback-channel@{2026-10-22 14:40:33 +0800}: commit: docs(068-…): add requirements spec…"

  git log master --oneline -1 → "7f9033ec" (master never moved; all 25 feature commits
  are on the feature branch)

  tasks.md header, correct: "**Branch**: `068-exec-quant-feedback-channel`（单写线，trunk master）"
  ```

- **Why it's a problem**: Every feature commit landed on branch `068-exec-quant-feedback-channel` (created 14:35:12, before the first artifact commit), but the verification record — the artifact the closure/merge stage consumes — states `branch master`. The value was evidently carried over from the run line's trunk declaration instead of measured. tasks.md got it right, so the two feature artifacts disagree about where the work lives. *(Recorded as a finding only; verification.md is implement-stage output outside this review's explicit commit list — the closure stage should correct the header before merging.)*
- **Proposed fix**: Make the verification-log step capture the branch mechanically (`git branch --show-current`) — in `skills/internal/implement-feature/SKILL.md`'s verification-log instructions and the verification-log template (`templates/verification-log-template.md`) — so the Run header cannot inherit an unmeasured trunk name.

### F10 — The `Status: Draft` field in requirements.md is dead weight that misleads standalone readers

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/requirements-template.md (Status header field; instances in every spec directory)
- **Evidence** (verbatim quote):

  ```
  grep -m1 "^\*\*Status\*\*" across the three newest specs:
  .specify/specs/059-exec-quant-recording/requirements.md:**Status**: Draft
  .specify/specs/067-loop-efficiency-hardening/requirements.md:**Status**: Draft
  .specify/specs/068-exec-quant-feedback-channel/requirements.md:**Status**: Draft

  .specify/memory/features.md row 068 (same date): "…| Implemented | …"
  ```

- **Why it's a problem**: The spec's own Status header says Draft while the feature registry says Implemented — and no lifecycle command ever updates it, so it is guaranteed-stale on every spec that progresses. This is exactly the drift shape One Source Of Truth forbids: a second, unmaintained copy of a fact whose owner is the feature registry. A standalone reader of requirements.md (the self-contained audience the templates target) gets the wrong lifecycle signal.
- **Proposed fix**: In `templates/requirements-template.md`, either delete the Status field or replace its value with a fixed pointer line ("Status: owned by `.specify/memory/features.md` → this spec's Feature row") so the header can no longer assert a competing, unmaintained status.

### F11 — Command-template wrap-up engine steps are contractually absent from unattended dispatch briefs, so the deviation repeats every stage

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/068-exec-quant-feedback-channel/checklists/report-exec-quant-feedback-20261022.md (§ Boundary & Process Notes); owner surfaces: `templates/commands/*.md` wrap-up blocks + the orchestrator's dispatch contract (`skills/external/sdd-loop-driver/references/dispatch-recipes.md`)
- **Evidence** (verbatim quote):

  ```
  checklists/report-exec-quant-feedback-20261022.md: "命令模板 Wrap-up 的
  run-determination / exec-quant / feedback-record 引擎步骤本阶段未执行——无人值守
  派发 brief 的产物契约（清单 + E3 证据 + 报告 + 显式路径提交）未含这些运行时记录
  步骤，且相关运行时存储属本线禁改/禁提交面；偏离在此显式披露，由编排者裁定是否补录。"

  templates/commands/review.md § Wrap-up (steps 1–3): "1. Run Determination —
  `python3 .specify/scripts/python/run-determination.py --action determine …`
  2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect …`
  3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record …`"
  ```

- **Why it's a problem**: The plan, tasks, and checklist stages of this line all skipped the wrap-up engine steps their command templates mandate, each disclosing the same reason: the dispatch brief's product contract omits them and the runtime stores are on the line's forbidden-write list. This review inherits the identical conflict (the review brief neither lists the steps nor un-forbids the stores), so the deviation is now four stages deep and each report re-litigates it. A step that is always waived by contract should not keep masquerading as a template obligation — the disagreement should be resolved once, in the owner documents.
- **Proposed fix**: In `dispatch-recipes.md` (unattended dispatch contract), state explicitly whether the wrap-up engine steps are executor-owned or orchestrator-owned for unattended lines; if orchestrator-owned, annotate the wrap-up blocks in the affected command templates (`templates/commands/*.md`) with a one-line condition ("unattended lines: run by the orchestrator at line closure, not per stage") so the executor's deviation is a documented hand-off instead of a per-run disclosure.

## 4. What Worked — Preserve (Brief)

- Frozen-baseline discipline: three pre-implementation baselines (mirror drift, clause coverage, E2 failing names) made every "zero NEW" criterion mechanically checkable (`notes/pre-change-measurements.md`, `coverage-baseline.txt`, `baseline-failed.txt`).
- Red-first evidence with per-test attribution (`notes/red-first-evidence.md`): every failure classified subject-vs-assertion, including a disclosed false-green correction (argparse usage-text coincidence) — the "green check is a claim" rule practiced, not just stated.
- Name-level baseline comparison (`comm -13`) as the regression criterion: survived expected mirror-fix failures disappearing without weakening the zero-new-failures guarantee.
- Mirror Obligations with a relative criterion ("zero NEW drift vs recorded baseline", never absolute green) — correctly predicted which inherited failures would collapse at sync time.
- Per-segment E3 stage-status rows carrying `selection_basis` + `sufficiency` (`test-evidence/implement-stage-status.jsonl`): closure can audit what was run and why without re-deriving it.
- Objective-analysis-gate fallback honesty: same-author degradations consistently marked `(detected: direct read, subagent unavailable)` in plan and checklist outputs.

## 5. spec-kit / SDD Improvement Recommendations

> Group by target subsystem. Each recommendation MUST name the exact file or section in the spec-kit repo to change and cross-reference the source finding ID(s).
>
> **Target path form**: the **repo-relative path is the PRIMARY form** (`templates/...`, `skills/...`, `scripts/...` — it resolves on any checkout). An absolute path MAY follow only as a parenthetical supplement. A target with no repo-relative form MUST be marked `external` with its reason.

### 5.1 Template Improvements

- **REC-068-10 — Retire or pointer-ize the requirements Status field** — Target: `templates/requirements-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/requirements-template.md`). Change: delete the `**Status**:` header field or replace its value with a fixed pointer to the Feature registry row (`.specify/memory/features.md`), eliminating the guaranteed-stale second copy. Source: F10. Expected impact: standalone spec readers stop receiving a wrong lifecycle signal; one fewer drift surface per spec.

### 5.3 Automation / Script Improvements

- **REC-068-01 — Add a clause-form check to the plan-stage gate** — Target: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`). Change: when `--stage` is `plan` or later, run `clause_extract.form_of()` over every `contracts/*` file and error on `form=md-none` or zero clauses (alternative: plan U4 checklist invokes `scripts/python/clause_extract.py` per contract). Source: F1. Expected impact: clause-syntax mismatch dies at the stage that created it; no more tasks-stage ANOMALY + 31-id rewrite rework.
- **REC-068-02 — Make the test-budget audit stage-check-aware** — Target: `skills/external/sdd-loop-driver/scripts/audit-test-budget.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/audit-test-budget.py`). Change: `--stage-check <stage>` requires stage-status completeness only for stages at or before `<stage>` (or an explicit `--allow-future-stages` flag), so the implement-stage audit can exit 0 by construction. Source: F2. Expected impact: no more hand-interpreted "right red" gates; a genuinely missing earlier-stage evidence file becomes the only red.
- **REC-068-07 — Date-marker-gate the history-skip filter** — Target: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`, `SKIP_HEADING`). Change: require a date/record marker in a heading before skipping it as history, instead of the bare `修订` substring. Source: F7. Expected impact: live normative sections containing the word survive gate analysis; artifacts stop renaming themselves to fit the tool.
- **REC-068-04a — Collateral-rewrite visibility in sync-mirrors writes** — Target: `scripts/python/sync-mirrors.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/scripts/python/sync-mirrors.py`). Change: `--write` prints the count of files outside the requested `--only` prefix that will also be rewritten (supporting role; the primary fix for F4 is prescription-side, REC-068-04). Source: F4. Expected impact: a scope-level invocation becomes visible at execution time instead of surfacing as 25–108 surprise worktree files.

### 5.4 Workflow Improvements

- **REC-068-03 — Split TDD-heavy segments at the test/implementation boundary** — Target: `skills/external/sdd-loop-driver/references/dispatch-recipes.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/dispatch-recipes.md`; budget owner `agents/sdd-executor.agent.md`). Change: add a segment-sizing rule that splits test-authoring from implementation+green phases (or sizes `run-turn-budget` per segment from task rows × measured turns-per-TDD-row) instead of raising the stage-wide constant again. Source: F3. Expected impact: implement segments stop exhausting the budget at bookkeeping; the driver no longer finishes subagents' closing work.
- **REC-068-04 — Prescribe minimal-scope `--only` prefixes for mirror-sync task rows** — Target: `skills/internal/create-tasks/SKILL.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md`; mirrored guidance in `templates/commands/plan.md` Mirror Obligations). Change: each mirror-sync task row carries the file/pair-level `--only` prefix for exactly the files the feature edits — the capability already exists in `scripts/python/sync-mirrors.py`. Source: F4. Expected impact: mirror-sync tasks stop dragging 25–108 collateral rewrites through the worktree; segment diffs stay scoped.
- **REC-068-05 — Remediation sync lists must enumerate durable registry surfaces** — Target: `skills/internal/analyze-artifacts/SKILL.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/SKILL.md`, remediation-sync section). Change: every analyze remediation's sync list includes `.specify/memory/features/<ID>.md` and `.specify/memory/features.md`, verified by a grep for the corrected fact across those surfaces. Source: F5. Expected impact: corrected decisions stop surviving in the durable registry with pre-correction wording.
- **REC-068-06 — Pin-revision attribution rule for implement segments** — Target: `skills/internal/implement-feature/SKILL.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md`, TDD/adjacent-guard section). Change: amendments to other features' closed-set/structural pins land in the same segment that creates the debt (never carried across segments), name the pin + adjudicating requirement row in the commit, and carry the dated register row per open REC-063-10. Source: F6. Expected impact: no HEAD-red windows on existing guard suites between segments; pin rewrites stay attributable in history.
- **REC-068-08 — Give the coverage baseline one owner and one execution point** — Target: `skills/internal/create-tasks/SKILL.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md`, baseline guidance; interacts with GATE-7 generation in `templates/commands/tasks.md`). Change: either freeze `coverage-baseline.txt` during the tasks stage before GATE-7 runs (removing the implement-Setup T002 row) or make GATE-7's baseline assertion explicitly deferred with a pointer to the implement task. Source: F8. Expected impact: no forced U4 baseline generation, no duplicate freeze obligation per contract feature.
- **REC-068-09 — Capture the branch mechanically in verification records** — Target: `skills/internal/implement-feature/SKILL.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md`, verification-log step) + `templates/verification-log-template.md`. Change: the Run header's branch value is produced by `git branch --show-current` at record time, never carried from a trunk declaration. Source: F9. Expected impact: closure/merge consumes a measured branch name; feature artifacts stop disagreeing about where the work lives.
- **REC-068-11 — Resolve wrap-up engine-step ownership for unattended lines once** — Target: `skills/external/sdd-loop-driver/references/dispatch-recipes.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/dispatch-recipes.md`) + a one-line condition in the wrap-up blocks of `templates/commands/*.md`. Change: declare whether run-determination/exec-quant/feedback-record steps are executor- or orchestrator-owned for unattended lines, and annotate the templates so a documented hand-off replaces the per-stage disclosure. Source: F11. Expected impact: the same deviation stops being re-disclosed at every stage; runtime-record writes get an owner that is actually authorized to make them.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | (none — no P0 findings raised) | — | — |
| P1 | REC-068-01 clause-form gate at plan | `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` | F1 |
| P1 | REC-068-02 stage-aware audit denominator | `skills/external/sdd-loop-driver/scripts/audit-test-budget.py` | F2 |
| P1 | REC-068-03 TDD segment sizing | `skills/external/sdd-loop-driver/references/dispatch-recipes.md` | F3 |
| P1 | REC-068-04 minimal-scope mirror `--only` prescription (+ REC-068-04a visibility) | `skills/internal/create-tasks/SKILL.md`; `scripts/python/sync-mirrors.py` | F4 |
| P1 | REC-068-05 remediation sync covers durable registries | `skills/internal/analyze-artifacts/SKILL.md` | F5 |
| P1 | REC-068-06 pin-revision attribution | `skills/internal/implement-feature/SKILL.md` | F6 |
| P2 | REC-068-07 dated-marker history-skip | `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` | F7 |
| P2 | REC-068-08 coverage-baseline single owner | `skills/internal/create-tasks/SKILL.md` | F8 |
| P2 | REC-068-09 mechanical branch capture | `skills/internal/implement-feature/SKILL.md` + `templates/verification-log-template.md` | F9 |
| P2 | REC-068-10 retire/pointer-ize Status field | `templates/requirements-template.md` | F10 |
| P2 | REC-068-11 wrap-up ownership for unattended lines | `skills/external/sdd-loop-driver/references/dispatch-recipes.md` + `templates/commands/*.md` | F11 |

**Top 3 by expected payoff**: REC-068-01 (kills a whole rework class at the earliest gate), REC-068-03 (stops the recurring segment-overrun pattern that already consumed two budget raises), REC-068-04 (removes the largest recurring worktree-pollution and mis-commit risk).

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. *(No `external` targets — all targets are repo-relative.)*
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document. *(Two events — the turn-budget exhaustion in F3/timeline row 11 and the human checkpoint in row 13 — name the run line's local state spine as their only record; that file lives outside the repo and is identified by absolute path in §0's reviewer row area for recovery: `/home/agent/.local/state/spec-kit/lines/speckit-068-execquant-feedback/state-spine.md`. Each row says explicitly that no in-repo trace exists for that event.)*
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: "No P0 findings raised; the P0 independent-validation pass is vacuously satisfied." (§2). *(Supplementary disclosure: no validation-subagent dispatch tool exists in this run, so any P0 would have used the documented fallback `(validated: direct re-read, subagent unavailable)`; moot at P0=0.)*

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.



