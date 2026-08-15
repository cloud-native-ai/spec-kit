# Specification-Driven Development (SDD) Process Review Report: Feedback 机制的 Probe 化重构（反馈插点 + 切片定向 + 三模式管理命令 + 外部 probe）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. Sections that describe the feature instead of identifying a process gap MUST be deleted.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 041 |
| Requirement Key | 041-refactor-feedback-probe |
| Requirement Name | Feedback 机制的 Probe 化重构（反馈插点 + 切片定向 + 三模式管理命令 + 外部 probe） |
| Related Feature | 028 Feedback Mechanism |
| Repository | spec-kit |
| Repository URL | https://github.com/cloud-native-ai/spec-kit (push remote `github`; note the `origin` remote points at upstream `github.com:github/spec-kit.git` — SHAs cited here exist on the cloud-native-ai remotes) |
| Branch | master (work delivered on branch `041-refactor-feedback-probe`, merged) |
| Commit SHA | bc3301dd1168741ec668ad4b6d85a1cdda6acc7f (short: bc3301dd) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-08-15 |
| Reviewer (Agent) | Qoder agent (command tester, clean context) |
| Environment | Linux, bash, python3 >= 3.8, pytest; specify-cli 0.0.22 |
| spec-kit Source Snapshot | self-hosting: the reviewed templates/commands/scripts live in this repository @ bc3301dd (version 0.0.22 per pyproject.toml) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 275 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/requirements.md | 21 FR / 8 SC / 6 stories for the probe-ified feedback mechanism; two clarify rounds recorded |
| plan.md | 128 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/plan.md | Plan with Constitution check (IX Partial justified), mirror obligations, phase design |
| tasks.md | 275 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/tasks.md | 34 tasks (all [X]), tests-first, 6 completion gates |
| data-model.md | 88 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/data-model.md | 6 entities: Probe Class/Object, External Probe, System Slice, Feedback Entry, Probe Map |
| contracts/engine-cli.md | 61 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/contracts/engine-cli.md | Engine CLI contract: 6 new actions + record/list extensions |
| contracts/entry-schema.md | 43 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/contracts/entry-schema.md | Entry frontmatter extension (probe/kind/slice/disposition) |
| contracts/feedback-command.md | 38 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/contracts/feedback-command.md | Three-mode command behavior contract |
| contracts/probe-registry.md | 68 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/contracts/probe-registry.md | Truth-source format and reconcile invariants |
| quickstart.md | 75 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/quickstart.md | End-to-end drill for the three modes |
| feature-ref.md | 23 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/feature-ref.md | Requirement 041 → Feature 028 binding and mapping |
| checklists/requirements.md | 56 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/checklists/requirements.md | Requirements-stage quality checklist (created before round-2 revision) |
| verification.md | 51 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/verification.md | Baseline vs post-change record, SC-001..008 all pass, incident notes |
| embed-inventory.txt | 54 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/embed-inventory.txt | Snapshot of the 49 implicit embed points (pre-delivery) |
| baseline-failed.txt | 38 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/baseline-failed.txt | 38 pre-existing failing tests, recorded before any engine edit |
| verification-scratch/ (6 files) | 64 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/verification-scratch/ | Per-SC evidence transcripts (sc-001/003/005/007-mode12/008, t031-t032) |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | 2026-08-14: requirements authored; two clarify rounds (Feature binding; Class/Object two-layer; round-2 rewrote Story 4 into three modes, added Story 6 + FR-018~021 + SC-007/008) | requirements.md `## Clarifications` (Sessions 2026-08-14, 2 rounds) | None |
| 2 | 2026-08-14: plan + Phase 1 artifacts (data-model, contracts ×4, quickstart, feature-ref); Constitution check 12 Pass + IX Partial (justified in Complexity Tracking) | plan.md `## Constitution Check` | None |
| 3 | 2026-08-14: tasks.md — 34 tasks, Tests Mode ON, DoD-1..6, GATE-1..6 | tasks.md `## Completion Gate` | None |
| 4 | 2026-08-15 commit fd4cba1d: first commit carries the whole spec artifact set + T001–T008 (baseline 38 failures recorded; probe truth source; US1 reconcile green) | `git log` scoped to the spec dir; first touching commit is fd4cba1d | Minor: requirements/plan/tasks authored 08-14 entered git history only with the first implementation batch — the approved spec baseline was never pinned at its own lifecycle point |
| 5 | 2026-08-15 commit 00aaeabb: T009–T015 (US2 map idempotence, US3 slice filters); MVP stop-and-validate | commit subject `feat(feedback): 041 probe map + 切片定向引擎扩展 (T009-T015)` | None |
| 6 | 2026-08-15 commit 5c74b0d5: T016–T021 (US4 command + cleanup). T021 first QA run omitted `--workspace-root`; engine self-location anchored the real store and `package`+`cleanup` misfired on it; recovered via `git restore`; rerun with the explicit flag passed | verification.md Notes (quoted in F1) | Yes: QA accident with real-store mutation (→ F1) |
| 7 | 2026-08-15 commit d6f87204: T022–T025 (US5 migration). 140 legacy entries all disposed as delete after the T024 user stop point; `migration-log.md` 140 rows (row count re-verified during this review) | commit d6f87204; /storage/project/cloud-native-ai/spec-kit/.specify/memory/feedback/migration-log.md | None (stop point honored) |
| 8 | 2026-08-15 commit fa9a70a8: T026–T030 (US6 external probes; package exclusion content-stream verified) | commit fa9a70a8; verification-scratch/sc-008.txt | None |
| 9 | 2026-08-15 commit f38e28dd: T031–T034 polish (mirror final check, suite rerun, tool-record refresh, verification.md, Feature 028 ledger) | commit f38e28dd | Residual: canonical docs left stale (→ F2), plan scale figure stale (→ F4) |
| 10 | 2026-08-15 (this review, HEAD bc3301dd): completion gates re-run read-only — `sync-mirrors.py --check` exit 0; open-task count 0; SC-001..008 present; `probes --reconcile` → "Probe registry reconciled zero-gap: 3 classes, 50 internal + 0 external objects, 50 embeds"; measured embeds 19 command templates + 31 skills = 50 | gate re-run outputs captured during this review | None |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 1 |
| Automation / Scripts | 2 |
| Workflow | 2 |
| Documentation | 2 |

Note on validation (per review command §4.5): F1 was initially drafted as P0 and was confirmed/downgraded by an independent read-only validation subagent (verdict: `downgrade` to P1 — evidence verbatim, mechanism real, incident real, but hazard confined to cross-project invocations with multiple recovery paths). No findings were rejected; no Unvalidated Findings appendix is needed.

## 3. Findings (Problems & Improvement Targets)

### F1 — Destructive engine actions can silently target the real store when run from a scratch project (validated: downgraded from P0)

- **Severity**: P1 (validated: downgraded — independent validator confirmed evidence and mechanism; P0 definition not met because normal single-project use is unaffected and recovery paths exist)
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/scripts/python/feedback-utils.py#L119-L141 (mirror: /storage/project/cloud-native-ai/spec-kit/.specify/scripts/python/feedback-utils.py); incident record: /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/verification.md (Notes)
- **Evidence** (verbatim quote):

  ```
  Priority: explicit CLI argument > script self-location (an engine copy
  installed under ``*/.specify/scripts/`` anchors its parent project) >
  nearest CWD ancestor containing ``.specify/`` > CWD itself. Self-location
  must outrank the walk-up: ...
  ```

  ```
  事故与恢复:T021 首跑漏 --workspace-root 致引擎自定位锚定真实库(package+cleanup 误触)→ git restore 完整恢复,重跑显式传参通过——证实 resolve_workspace_root 自定位优先级高于 CWD,QA 脚本必须显式传参
  ```

- **Why it's a problem**: During this feature's own sanctioned QA drill, `package` + `cleanup` (which calls `entry_file.unlink()`) executed against the real repository store instead of the scratch project, because self-location outranks the CWD walk-up and no warning is emitted when the two disagree. The engine behavior is unchanged, and the "always pass `--workspace-root`" rule lives only in this feature's verification log — future QA agents will not read it.
- **Proposed fix**: In `scripts/python/feedback-utils.py` `resolve_workspace_root` (or a wrapper used by destructive actions `package`/`cleanup`/`migrate-legacy`): when no explicit `--workspace-root` was given and the self-located root differs from the CWD-anchored root, print a prominent warning naming both roots; for the three destructive actions, additionally require an explicit `--workspace-root` (or an explicit override flag) instead of silently proceeding. Record the rule in `shared/workflow/feedback-step.md` or the quickstart QA guidance, not only in a per-feature verification log.

### F2 — Stale complex-command count "13" survives in two canonical files after 041 moved it to 19

- **Severity**: P1
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/instructions.md#L23 (Documentation Map, Feedback System row; symlinked to AGENTS.md/CLAUDE.md/QODER.md); /storage/project/cloud-native-ai/spec-kit/shared/workflow/feedback-step.md#L5-L6 (mirror: .specify/shared/workflow/feedback-step.md)
- **Evidence** (verbatim quote):

  ```
  ## Feedback step on all skills + 13 complex commands (4 simple excluded)
  ```

  (instructions.md, Feedback System row)

  ```
  This file is the single source of
  truth for the `## Feedback` step that every qualifying unit embeds. Skills embed it
  as their final workflow section; the 13 **complex** command templates embed it at
  their wrap-up / Git-commit-prompt stage.
  ```

  (feedback-step.md) — while the correctly updated reference doc says:

  ```
  As of requirement 041 this yields **19 complex** command
  ```

  (/storage/project/cloud-native-ai/spec-kit/docs/reference/skills/feedback.md#L28). Measured during this review: 19 `templates/commands/*.md` + 31 `skills/*/SKILL.md` embed `## Feedback` (50 total, matching `probes --reconcile`).

- **Why it's a problem**: The instructions file is the canonical AI guidance loaded by every supported agent, and `feedback-step.md` is the canonical step embedded across 52 units; both contradict the reference doc and the probe truth source. T029 edited `feedback-step.md` for probe attribution but left the stale count; `/speckit.implement`'s documentation step did not catch either residue. Hardcoded counts that must be edited in N places are exactly the drift class the probe truth source was built to eliminate.
- **Proposed fix**: Correct both files (13 → 19), and replace the hardcoded count with a reference to the derived source (e.g. "all complex command templates — enumerate via `feedback-utils.py --action probes --format json`"), so the count can no longer drift; add the two paths to the delivery checklist that `/speckit.implement` walks (or regenerate instructions.md at delivery).

### F3 — verification.md test-count self-report is internally inconsistent (three different totals in one line)

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/verification.md#L21
- **Evidence** (verbatim quote):

  ```
  post_change_new_contract_tests=27 (registry 14 + cli 13[map5+filter/dispose5+cleanup3... 见测试文件] + entry-schema 6 + command-template 6 — 按文件计 4 文件 42 用例全绿)
  ```

  The same line asserts 27, a per-file sum of 39 (14+13+6+6), and "42 用例全绿". Measured during this review, the four pinned files contain 14 + 20 + 6 + 6 = 46 test functions (the cli file may have grown after 041, but 27 ≠ 39 ≠ 42 is a contradiction inside one sentence regardless).

- **Why it's a problem**: verification.md is the audit artifact DoD-4 and GATE-1 point at; hand-written counts that contradict themselves undermine the credibility of the whole log, and nothing in the workflow catches it because the numbers are typed, not derived.
- **Proposed fix**: Make the verification template/command require machine-derived counts: paste the output of `pytest --collect-only -q tests/contract/test_feedback_probe_*.py | tail -1` (or `grep -c "def test_"` per file) instead of hand-summing; the same rule should apply to every numeric claim in verification.md (the rest of this file's numbers — 50 embeds, 140 rows, 13 actions — all re-verified correct during this review).

### F4 — plan.md scale line says "5 new engine actions" but 6 shipped (dispose is an action, not a flag)

- **Severity**: P2
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/plan.md#L23; contradiction at verification.md#L20 and contracts/engine-cli.md#L18-L19
- **Evidence** (verbatim quote):

  ```
  新增 1 个命令模板 ×6 工具副本、1 个定义文件、5 个新引擎动作 + record/list 旗标扩展
  ```

  vs. contract text:

  ```
  C-2.5 新动作 `dispose`(FR-011 的 setter,与 C-2.4 过滤器配对):`--action dispose --id <entry-id> --to processed|ignored`
  ```

  and the verification record:

  ```
  post_change_engine_actions=13 (+dispose/cleanup/probes/map/migrate-legacy/probe-inject)
  ```

  (7 existing + 6 new = 13; `dispose` is an action per its own contract.)

- **Why it's a problem**: The plan's Scale/Scope figures are the reference maintainers quote when judging whether a change was over-scoped; they were never reconciled at delivery, so plan, contract, and verification now tell three different stories about the same delivered surface.
- **Proposed fix**: Either correct plan.md at delivery wrap-up (a one-line errata in `## Notes` is enough), or stamp plan.md as "frozen at plan time; see verification.md for delivered counts" so readers know which document owns the numbers.

### F5 — Requirements quality checklist still certifies the pre-revision spec shape (17 FR / 6 SC vs delivered 21 FR / 8 SC)

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/checklists/requirements.md (Requirement Completeness section); compare requirements.md after round-2 integration
- **Evidence** (verbatim quote):

  ```
  - [x] Requirements are testable and unambiguous
    - 17 条 FR 全部为可判定断言(四要素非空校验、双向对账零缺漏、无归属新条目数为 0、零差异重建等)。
  - [x] Success criteria are measurable
    - SC-001~006 全部为数值/可判定
  ```

  while requirements.md `## Clarifications` round 2 records: "新增 Story 6(外部 probe);FR-008/009/010 重写…新增 FR-018~021(外部 probe 组)…新增 SC-007/008" — i.e. 21 FR and 8 SC at sign-off.

- **Why it's a problem**: The checklist is the recorded quality gate for the spec, but the spec changed shape after the gate ran and the gate artifact was never re-validated; a future auditor reading the checklist would certify a spec that no longer exists. The workflow has no "re-run the requirements checklist after a clarify revision" step.
- **Proposed fix**: Add to the clarify/revision flow: whenever a revision round adds/removes FRs or SCs, the requirements checklist must be re-executed (or annotated with a "re-certified after round N" line); alternatively derive the counts in the checklist from requirements.md instead of typing them.

### F6 — requirements.md `Status` field is a dead signal: "Draft" persists after full delivery

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/041-refactor-feedback-probe/requirements.md#L5; systemic across /storage/project/cloud-native-ai/spec-kit/.specify/specs/
- **Evidence** (verbatim quote):

  ```
  **Status**: Draft
  ```

  in a spec whose tasks.md records `**DoD Status**: green`, whose verification.md records `SC-001_status=pass` through `SC-008_status=pass`, and which shipped in commits fd4cba1d..f38e28dd. Measured across the repo: 40 of 41 spec directories still read `**Status**: Draft`; only 037-goal-registry reads `Implemented`.

- **Why it's a problem**: The field is template-mandated, filled once at creation, and never advanced by any lifecycle step — so it carries no information and teaches readers to ignore spec metadata. Feature status lives (correctly) in features.md, making the requirements-level Status pure cargo-cult.
- **Proposed fix**: Either add a delivery step (in `/speckit.implement` wrap-up or the verification writing task) that advances `**Status**: Draft → Implemented` in requirements.md, or remove the field from the requirements template so there is one status authority (features.md) instead of two.

### F7 — No-argument prerequisite resolution silently picks the highest-numbered spec on non-spec branches

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/scripts/bash/common.sh#L55-L85 (`find_feature_dir_by_prefix`; mirror: scripts/bash/common.sh)
- **Evidence** (verbatim quote):

  ```
    # Extract numeric prefix from branch (e.g., "004" from "004-whatever")
    if [[ ! $branch_name =~ ^([0-9]+)- ]]; then
      # If branch doesn't have numeric prefix, fall back to latest spec directory.
      local latest_feature=""
      local highest=0
  ```

  This review ran on branch `master` and was silently resolved to `041-refactor-feedback-probe` (the highest number present) with no warning emitted.

- **Why it's a problem**: `/speckit.review` (and implement/plan/tasks) with no arguments relies on this rule; on a shared branch with 41 candidate specs, the resolved target changes the moment anyone scaffolds spec 042 — a reviewer can unknowingly review the wrong feature, and the resolution rule is documented only in a code comment.
- **Proposed fix**: In `check-prerequisites.sh` JSON output (or the review command's step 1), emit and surface a resolution note whenever the fallback path fires — e.g. `"RESOLUTION": "fallback: highest-numbered spec (branch 'master' has no NNN- prefix)"` — and have the command print it before proceeding; optionally require confirmation when more than one implemented spec exists.

### F8 — Review command mandates a P0 validation subagent with no degraded-mode fallback

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/commands/review.md#L54-L60 (generated copies: .claude/commands/, .qoder/commands/, .github/prompts/, .opencode/command/)
- **Evidence** (verbatim quote):

  ```
  Every **P0** finding MUST be confirmed by an independent read-only validation subagent before it enters the report:
  ```

  The section defines confirm/reject/downgrade handling but no behavior for agents that have no subagent capability (the framework supports six agent CLIs across two tiers, not all of which can spawn isolated validators).

- **Why it's a problem**: On subagent-capable hosts the step works (this review exercised it: one validator agent, verdict `downgrade`); on hosts without the capability the instruction is unsatisfiable, so an agent will either skip validation silently or refuse to print P0 findings — both degrade the report without any recorded reason. It also cost one failed orchestration attempt in this very run before a working validator path was found.
- **Proposed fix**: Add one fallback sentence to templates/commands/review.md §4.5, e.g. "If the host provides no subagent mechanism, apply the strict rule instead: downgrade every would-be P0 to P1 with a `(validated: self, no subagent host)` note and list it in the Unvalidated Findings appendix."

## 4. What Worked — Preserve (Brief)

- Story-grouped commit discipline held exactly: 6 commits mapping cleanly onto T001–T008 / T009–T015 / T016–T021 / T022–T025 / T026–T030 / T031–T034 — review could attribute every artifact to a task range from `git log` alone.
- Baseline-first testing: 38 pre-existing failures recorded before any edit; gates compare by name, so "zero new failures" was checkable rather than vibes.
- Machine-reconciled invariants (`probes --reconcile` 50↔50, `sync-mirrors --check` exit 0) re-verified green by this review days after delivery — the truth-source design works.
- Evidence committed with the spec (verification-scratch/, baseline-failed.txt, embed-inventory.txt): a clean-context reviewer could re-verify SC claims offline.
- The T024 user stop point (migration plan confirmation) was honored and recorded before 140 deletions ran.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Advance or remove the requirements Status field** — Target: https://github.com/cloud-native-ai/spec-kit/blob/bc3301dd1168741ec668ad4b6d85a1cdda6acc7f/templates/requirements-template.md (status field) and the implement/verification wrap-up steps in templates/commands/implement.md. Change: add a delivery step advancing `Status: Draft → Implemented`, or drop the field (features.md is the status authority). Source: F6. Expected impact: removes a dead metadata signal duplicated across 41 specs.

### 5.2 Command Prompt Improvements

- **Degraded-mode fallback for P0 validation** — Target: https://github.com/cloud-native-ai/spec-kit/blob/bc3301dd1168741ec668ad4b6d85a1cdda6acc7f/templates/commands/review.md (section 4.5). Change: one fallback clause for hosts without subagent capability (mandatory downgrade + appendix listing), then re-run `regen-command-copies.py`. Source: F8. Expected impact: review reports stay trustworthy on all six supported agent CLIs.

### 5.3 Automation / Script Improvements

- **Guard destructive actions against cross-store misfire** — Target: https://github.com/cloud-native-ai/spec-kit/blob/bc3301dd1168741ec668ad4b6d85a1cdda6acc7f/scripts/python/feedback-utils.py (`resolve_workspace_root` + action dispatch for package/cleanup/migrate-legacy). Change: warn when self-located root ≠ CWD-anchored root; require explicit `--workspace-root` for destructive actions in that state. Source: F1. Expected impact: eliminates the demonstrated real-store-mutation accident class for every downstream QA/demo drill.
- **Surface fallback spec resolution** — Target: https://github.com/cloud-native-ai/spec-kit/blob/bc3301dd1168741ec668ad4b6d85a1cdda6acc7f/scripts/bash/check-prerequisites.sh (and common.sh `find_feature_dir_by_prefix`). Change: emit a `RESOLUTION` field + stdout note when the no-prefix fallback picks the highest-numbered spec; commands print it before proceeding. Source: F7. Expected impact: no-arg invocations on shared branches can no longer silently target the wrong spec.

### 5.4 Workflow Improvements

- **Machine-derived counts in verification logs** — Change: verification writing (task T034 pattern / implement wrap-up) must paste collector output (`pytest --collect-only -q ... | tail -1`, `grep -c`, `wc -l`) for every numeric claim instead of hand-summing; add a self-consistency read-back before saving. Source: F3. Expected impact: verification.md becomes a trustworthy audit artifact by construction.
- **Re-certify the requirements checklist after revision rounds** — Change: clarify/integration rounds that add or remove FRs/SCs must re-run (or annotate) checklists/requirements.md with "re-certified after round N". Source: F5. Expected impact: the quality-gate record always describes the spec that was actually approved.

### 5.5 Documentation Improvements

- **Kill the hardcoded "13 complex commands" count at its two remaining sites** — Target: https://github.com/cloud-native-ai/spec-kit/blob/bc3301dd1168741ec668ad4b6d85a1cdda6acc7f/.specify/instructions.md (Feedback System row, regenerate via /speckit.instructions) and https://github.com/cloud-native-ai/spec-kit/blob/bc3301dd1168741ec668ad4b6d85a1cdda6acc7f/shared/workflow/feedback-step.md (replace the literal with a pointer to `probes --action probes --format json` as the derived enumeration). Source: F2. Expected impact: the count can no longer drift across canonical files; agents stop reading a contradictory number.
- **Freeze or reconcile plan.md scale figures at delivery** — Target: plan.md `## Technical Context` Scale/Scope line (per-spec artifact; convention-level fix in templates/commands/implement.md docs step). Change: delivery wrap-up adds a one-line errata when delivered counts diverge from plan-time figures. Source: F4. Expected impact: plan/contract/verification stop telling three different stories about delivered scope.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Guard destructive actions against cross-store misfire (warn + require explicit root) | scripts/python/feedback-utils.py | F1 |
| P1 | Fix + de-hardcode the complex-command count in instructions.md and feedback-step.md | .specify/instructions.md, shared/workflow/feedback-step.md | F2 |
| P1 | Machine-derived counts in verification logs | implement wrap-up / verification writing step | F3 |
| P2 | Surface fallback spec resolution in check-prerequisites.sh | scripts/bash/check-prerequisites.sh, scripts/bash/common.sh | F7 |
| P2 | Degraded-mode fallback for P0 validation subagent | templates/commands/review.md §4.5 | F8 |
| P2 | Advance or remove requirements Status field | templates/requirements-template.md + implement wrap-up | F6 |
| P2 | Re-certify requirements checklist after revision rounds | clarify/revision workflow | F5 |
| P2 | Freeze/reconcile plan scale figures at delivery | templates/commands/implement.md docs step (convention) | F4 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `https://github.com/cloud-native-ai/spec-kit/blob/bc3301dd1168741ec668ad4b6d85a1cdda6acc7f/...`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
