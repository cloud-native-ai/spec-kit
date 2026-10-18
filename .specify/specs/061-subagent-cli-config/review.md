# Specification-Driven Development (SDD) Process Review Report: 061-subagent-cli-config 子代理 CLI 配置管理与按派发量化

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits narrative summaries of the feature's contents. It critiques the process that produced them, not the feature's business merits or its code.

## 0. Portable Project Context (Self-Contained Snapshot)

All paths in this report are absolute. The feature branch is **not pushed**, and the only remote is SSH-only, so `{REPO_URL}@<sha>` citations cannot resolve; use the absolute paths below plus the `git show` recovery commands in Appendix C.

| Field | Value |
|-------|-------|
| Requirement ID | 061 |
| Requirement Key | 061-subagent-cli-config |
| Requirement Name | 子代理 CLI 配置管理与按派发量化（Subagent CLI Config Management & Per-Dispatch Quantification） |
| Related Feature | 061 子代理 CLI 配置管理与按派发量化 |
| Repository | spec-kit |
| Repository URL | `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (SSH-only; no HTTPS web remote) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE** — `git branch -r --contains HEAD` printed nothing; HEAD is local-only. Cite absolute paths and `git show <sha>:<path>`. |
| Branch | 061-subagent-cli-config |
| Commit SHA | `c3a268f6b860fc0720a6606ad6adef02a45558fa` (short: `c3a268f6`; implementation commit `be491b33`) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-18 |
| Reviewer (Agent) | Qoder CLI — `sdd-executor` review stage |
| Environment | macOS arm64 25.6.0; bash; qodercli 1.1.73; pytest interpreter `/Users/liuqiming.lqm/project/profiles/.venv/bin/python` (pytest 9.1.1); repo `.venv` has no pytest |
| spec-kit Source Snapshot | `.specify/source.json` commit `8c9eaab612ad5f8355263c880c204ae17c84e696`, stamped `20261015T074120Z`; `pyproject.toml` version `0.0.22`; live HEAD `c3a268f6` |

### 0.1 Mechanical State at Review Time

- Feature artifacts: 33/33 task rows `[X]`, 0 open; `validate-requirements.py` `status: ok` (0 errors / 0 warnings; 253 lines scanned, 33 definition rows, 15 shared strings); `validate-tasks.py` `PASS` (0 errors / 0 warnings).
- Full-suite record consumed (not re-run): `24 failed, 3417 passed, 1 skipped`; `comm -13` and `comm -23` between `/tmp/061-baseline-failed.txt` and `/tmp/061-verify-failed.txt` are both empty.
- Generation faces re-checked read-only: `sync-mirrors.py --check` exit 0 (templates 22 / skills.external 369 / skills.internal 136 / agents 3 / scripts 109 / shared 51); `compile-embeds --check` exit 0 (73 units, zero drift); `regen-command-copies.py --check` exit 0; runtime defaults layer present and byte-equal to `templates/execution-config-defaults.yaml`.
- Commit surface: `git show --stat --name-only be491b33` lists exactly 42 files; no excluded dirty file (instructions mirrors, `records.jsonl`, `glossary.md`, session/feedback records, progress-reporting files) appears in it.
- Clause machinery: `clause_extract.py` reports `form=md-none clauses=0` for **all three** feature contracts; `account-clause-coverage.py` reports `claimed clauses (this feature): 0`.

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 252 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/requirements.md` | 27 FR / 6 SC / 4 user stories / 15 shared strings; clarified and analyze-remediated |
| plan.md | 187 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/plan.md` | 16-principle constitution check; Phase 0 decisions; mirror obligations; risks |
| tasks.md | 259 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/tasks.md` | 33 tasks in 7 phases; DoD / GATE-1..7; all rows `[X]` |
| data-model.md | 206 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/data-model.md` | 7 entities E1–E7 plus V1–V15 validation rules |
| contracts/execution-config-cli.md | 139 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/contracts/execution-config-cli.md` | C-EC-01..C-EC-15 resolver CLI contract |
| contracts/exec-quant-v2.md | 114 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/contracts/exec-quant-v2.md` | C-EQ-01..C-EQ-11 record v2 and `collect-dispatch` contract |
| contracts/dispatch-wiring.md | 113 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/contracts/dispatch-wiring.md` | C-DW-01..C-DW-11 wiring, seeding, mirror, driver re-read contract |
| quickstart.md | 235 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/quickstart.md` | 6 scenarios, per-example premises, S6 authorization gate |
| feature-ref.md | 134 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/feature-ref.md` | FR/SC → design/contract mapping, delivery surface, baseline record |
| verification.md | 186 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/verification.md` | SC status table, GATE-1..7, intentional extensions, T028/T030/T033 evidence |
| waivers.md | 14 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/waivers.md` | Checklist exemption granted at implement start |
| checklists/config-quant.md | 110 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/checklists/config-quant.md` | 36 requirements-quality items, all `[x]` after in-place rewrite |
| checklists/requirements.md | 37 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/checklists/requirements.md` | Specification quality checklist, all `[x]` |
| notes/baseline-failed.txt | 43 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/notes/baseline-failed.txt` | 24-node frozen failing baseline (header says "BEFORE any 061 source edit") |
| notes/pre-change-measurements.md | 122 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/notes/pre-change-measurements.md` | T001/T002 measurements, trap notes, re-freeze procedure |
| notes/quickstart-run.md | 204 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/notes/quickstart-run.md` | S1–S5 executed output; S6 not executed |
| notes/red-first-evidence.md | 122 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/notes/red-first-evidence.md` | red→green runs and intentional-extension process evidence |
| Analyze round 1 | 289 | `/tmp/log-061-analyze.log` | CRITICAL 0 / HIGH 4 / MEDIUM 17 / LOW 5; 4-HIGH gate failure |
| Analyze round 2 | 164 | `/tmp/log-061-analyze-r2.log` | CRITICAL 0 / HIGH 0; MEDIUM 3 / LOW 5; gate passed |
| Terminal authority brief | 85 | `/tmp/061-subagent-cli-config-brief.md` | Untracked `/tmp` scope authority cited by plan/feature-ref/feature-detail |

### 0.2 Review Method and Same-Author Disclosure

- **Same-author condition**: the artifact chain was produced by prior stage agents of the **same unattended loop**, over multiple edit passes; the review executor is a separate stage agent, but loop-level authorship is shared. The objective-analysis gate's literal firing condition (`/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/shared/workflow/objective-analysis-gate.md:15-16`) is scoped to "the agent now running the command, in the current session", which would not fire across stages. This review applied the stricter reading: **detection was delegated** to four fresh-context, read-only detectors with disjoint scopes.
- **Detection split**: A = requirements / both checklists / waivers / two analyze reports / feature registry; B = plan / data-model / three contracts / feature-ref; C = tasks / quickstart / verification / notes / recorded suite evidence; D = framework surfaces (run-agent, preflight, subagent-definitions, loop driver, review skill/template, Wrap-up engines, foreign progress-reporting files).
- **Validation**: three P0 candidates were raised (Wrap-up embed parameters; contract clause syntax; driver dispatch bypass). Each was sent to a **separate** fresh-context read-only validator that received only that finding. All three validators **downgraded** their finding to P1. Downgrade rate: **3/3 (100%)**; rejected: 0. The validation pass was executed, not vacuous.
- **Interpretation disclosed**: run-agent's anti-nesting clause forbids a third **driver/loop** layer. This review treated the review skill's mandated read-only detector/validator wave as analysis assistance, not loop nesting. The framework itself does not settle this; finding F10 records the ambiguity.
- **Not flagged by design**: deliberate `[~]` deferrals (none), mirror-by-design duplication under `.specify/`, and pre-existing baseline failures already recorded for the feature (the 7 `test_exec_quant_engine.py` nodes).

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements + first checklist committed | `54c90c29` (2026-10-18 08:19) | None |
| 2 | clarify binds Feature 061 and records 5 answers | `77ea2967` (08:28) | None |
| 3 | plan + Phase 1 design artifacts committed | `3d01bcad` (09:12) | None |
| 4 | Foreign progress-reporting guideline and test appear untracked; instructions mirrors/templates become dirty | Files created 09:14–09:15; `.specify/agents/execution/logs/061-line-state.md:12` lists them as "Not part of 061; leave untouched" | Concurrent-line interference; no isolation declaration artifact |
| 5 | tasks committed (33 rows) | `8959ade9` (09:32) | None |
| 6 | requirements quality checklist committed | `71d59574` (09:43) | None |
| 7 | analyze round 1 runs; 4 HIGH blocks the gate | `/tmp/log-061-analyze.log` metrics: 0/4/17/5 | Expected quality-gate loop |
| 8 | analyze remediation + SC-006 clarification commits | `65ceb389` (10:11), `3a62cb28` (10:12) | One bounded remediation round, per loop rule |
| 9 | implementation starts; "pre-change" baseline captured with the three new 061 files parked inside the spec dir | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/notes/pre-change-measurements.md:106-107`; engine mtime 10:36:21, test mtime 10:37:06, baseline file mtime 10:41:38 | Baseline is a reconstructed dirty-tree measurement, not a clean pre-change tree |
| 10 | generation trio runs; `compile-embeds --write` fails (no such flag), then corrected in passing; regen rewrites four foreign dirty command copies at 10:56:24 | `verification.md:120-124`; copies' mtimes 10:56:24 vs source `templates/commands/instructions.md` 09:15:04 | Premise decay + whole-tree generator write |
| 11 | analyze round 2 runs; HIGH=0, gate passes; 3 MEDIUM / 5 LOW remain | `/tmp/log-061-analyze-r2.log:19` | Convergence required two rounds |
| 12 | implement commit (42 files) | `be491b33` (11:01) | Includes requirements/plan/tasks edits during implement (M-01/M-02/L-01 fixes) |
| 13 | verification SHA recorded | `c3a268f6` (11:02) | None |
| 14 | review stage dispatched by a direct qodercli print-mode runner; log is 0 bytes while the heartbeat grows | `/tmp/run-061-review.sh`; `/tmp/log-061-review.log`; `.specify/agents/execution/logs/061-line-state.md:17` | Driver bypasses run-agent's resolver/collect path and the Visibility Contract's stream requirement |
| 15 | This review: four read-only detectors + three P0 validators | Appendix A | Same-author gate applied in the stricter cross-stage form |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 10 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 10 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 4 |
| Command Prompt | 1 |
| Automation / Scripts | 2 |
| Workflow | 5 |
| Documentation | 8 |

**P0 status**: three P0 candidates were raised and independently validated; all three were downgraded to P1 because the failures are loud, recoverable, disclosed, or outside the feature's declared change scope. Final P0 count is **0**; no P0 waiver is required. The P0 validation pass was executed, not vacuous.

## 3. Findings (Problems & Improvement Targets)

### 3.0 P0 Candidate Validation Notes

| Candidate | Original severity | Validator verdict | Reason (abridged) |
|-----------|-------------------|-------------------|-------------------|
| Wrap-up embed parameters (now F1) | P0 | downgrade → P1 | Engines raise exit 2 before any store mutation; recovery is documented one hop away; 68 feedback entries prove executors recover. Recurring toll, not corruption. |
| Contract clause syntax (now F2) | P0 | downgrade → P1 | The extractor names unparseable files; green claims would fail loudly (`green-dangling`); zero green claims is repo norm; content is manually correct. Residual: 29 unresolvable feature-ref citations and an empty machine lane. |
| Driver dispatch bypass (now F3) | P0 | downgrade → P1 | The prohibition holds, but the driver path is pre-existing and outside 061's declared change scope; T030 records the bypass; heartbeat/sentinel/stall handling mitigates; telemetry is missing, not corrupted. |

### F1 — Compiled Wrap-up embeds omit every engine's required parameters

- **Severity**: P1 *(validated: downgraded from P0)*
- **Category**: Automation / Scripts
- **Propagation surface**: every compiled `## Wrap-up` face generated from the probe registry, and the determination / exec-quant / feedback stores they feed.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.qoder/commands/speckit.review.md:25-27`; renderer `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/probe-utils.py:881-883`; handler model `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/shared/definitions/probe-definitions.md:180-187`; required-parameter checks `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/scripts/python/run-determination.py:1391,1396` and `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/scripts/python/feedback-utils.py:718,722,726`.
- **Evidence** (verbatim):

  ```
  25:1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "/speckit.review" --unit-type command`
  26:2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "/speckit.review" --unit-type command`
  27:3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "/speckit.review" --unit-type command`
  ```

  ```
  run-determination.py:1391:  raise InputError("--run-id is required: the key is (unit_id, run_id)")
  run-determination.py:1396:  raise InputError("--complexity is required: it is a caller declaration, "
  feedback-utils.py:718:     raise FeedbackError("--run-id is required.")
  feedback-utils.py:722:     raise FeedbackError("record requires a non-empty --review / --review-file.")
  feedback-utils.py:726:     "record requires --points / --points-file with at least one line "
  ```

  The generated form is produced by a fixed renderer that appends only the identity flags:
  `cli = (f"python3 {owner} --action {action} " f"--unit-id \"{unit_id}\" --unit-type {unit_type}")`. The 2026-10-18 analyze feedback record restates the defect: `Analyze wrap-up surface is under-specified: run-determination requires --run-id/--complexity and feedback-utils requires --points, but the generated Wrap-up lists only --unit-id/--unit-type.` Fourteen earlier feedback records carry the same marker.
- **Why it's a problem**: the only command line a wrap-up executor sees is wrong by construction, so every command/skill run pays a multi-round flag-discovery tax before it can record anything. The owner document deliberately keeps invocation prose out of `feedback-step.md` (`No invocation is written out here on purpose`), which makes the compiled face the sole carrier — and the carrier is incomplete.
- **Proposed fix**: make each engine expose its per-action required flags (a module-level `REQUIRED_FLAGS` map or an `--action required-flags` output), teach the probe Handler model to carry them, and have `probe-utils.py::_render_call_line` emit placeholders; add a contract test that executes every rendered engine call in a sandbox and fails on any `is required` error; then run `compile-embeds → regen-command-copies → sync-mirrors`.

### F2 — Contract clause IDs are outside the owner grammar; the machine-readable clause lane is empty

- **Severity**: P1 *(validated: downgraded from P0)*
- **Category**: Documentation
- **Propagation surface**: `/speckit.tasks` green-point validation, `account-clause-coverage.py`, `feature-ref.md` traceability, and every future `/speckit.analyze` coverage claim.
- **Location**: contract headings `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/contracts/execution-config-cli.md:9`, `.../contracts/exec-quant-v2.md:9`, `.../contracts/dispatch-wiring.md:8`; syntax owner `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/definitions/contract-clause-definitions.md:13,42,57`; extractor `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/clause_extract.py:44-51`; tasks `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/tasks.md` (0 `[green:]`); analyze claim `/tmp/log-061-analyze-r2.log:138`; mapping table `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/feature-ref.md:10-39`.
- **Evidence** (verbatim):

  ```
  ## C-EC-01 Engine identity & actions
  ## C-EQ-01 Schema v2 & value domains
  ## C-DW-01 run-agent：派发前解析并展示
  ```

  ```
  contract-clause-definitions.md:13: 它由一个 **id** 标识,形态为 `C-<数字>`,可带一级小数后缀(如 `C-3.4`)
  contract-clause-definitions.md:42: **新建契约 MUST 只用这一种形态**
  ```

  ```
  $ python3 scripts/python/clause_extract.py .specify/specs/061-subagent-cli-config/contracts/*.md
  dispatch-wiring.md       form=md-none  clauses=0
  exec-quant-v2.md         form=md-none  clauses=0
  execution-config-cli.md  form=md-none  clauses=0
  ```

  ```
  $ python3 scripts/python/account-clause-coverage.py .specify/specs/061-subagent-cli-config
  claimed clauses (this feature): 0
  ```

  The analyze round-2 report still claims `| FR → task coverage | **27/27（100%）** |` (`/tmp/log-061-analyze-r2.log:138`) and lists only `validate-requirements.py` and `validate-tasks.py` as the run read-only validators (`:5`). Spec 060 used canonical `**C-N**` (8 and 10 clauses); spec 059 hit the same `md-none` condition and documented its fallback in `tasks.md:44,232`; 061 repeats the condition without a waiver.
- **Why it's a problem**: the three contracts contain 37 clauses that no clause consumer can see. `validate-tasks.py` passes because the feature declares zero `[green:]` claims; `feature-ref.md` has 29 mapping rows carrying clause IDs (47 occurrences, 33 distinct) that cannot resolve; analyze's "27/27" is an FR-to-task row count, not clause coverage. The named fallback (`UNPARSABLE-NAMED`) fires, so this is not fully silent — but the machine lane is empty while the artifacts present themselves as traceable.
- **Proposed fix**: renumber the 061 contracts to canonical `**C-N**` (feature-wide unique, as 060 did), add per-clause FR citation groups, restore `[green: contracts/<file>.md#C-n]` claims in `tasks.md`, and require `clause_extract.py` in the plan/contract gate. Make `skills/internal/analyze-artifacts/SKILL.md` run `account-clause-coverage.py <spec-dir>` before any coverage percentage is written, and make `skills/internal/create-plan/SKILL.md` point contract authors at `shared/definitions/contract-clause-definitions.md` §3. Add a contract test that scans the newest spec's contracts for `form=md-none`.

### F3 — The driver's default dispatch shape bypasses the new resolver and uses the contract's prohibited print-mode form

- **Severity**: P1 *(validated: downgraded from P0)*
- **Category**: Workflow
- **Propagation surface**: every stage dispatch of every unattended line (including this review), the Visibility Contract, and the FR-027 merge gate.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/dispatch-recipes.md:27-57`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/definitions/subagent-definitions.md:76-85`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/run-agent/SKILL.md:67-107`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/verification.md:143-146`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/agents/execution/logs/061-line-state.md:17`; `/tmp/run-061-review.sh`.
- **Evidence** (verbatim):

  ```
  qodercli -p "<prompt>" > agent.log 2>&1 &   # PROHIBITED
  Every external subagent dispatch MUST therefore: 1. **Stream events** ...
  3. **Emit the artifact triplet** per dispatched agent
  ```

  ```
  Recipe 2: cd <project-dir> && <cli> -w <project-dir> --permission-mode auto -p "$(cat ...)"
  Recipe 3: ssh <alias> "nohup su - <run-user> -c 'bash ... > .../log-... 2>&1' < /dev/null > /dev/null 2>&1 &"
  ```

  ```
  verification.md:146: the driver's dispatch shape is **not broken** — it neither calls the new resolver nor the new collect action, and preflight ④ still accepts its existing evidence form under the new "resolved configuration" wording once a defaults layer exists. Verdict: **compatible, no fast-fail**.
  line-state:17: ④ LLM config: model=`dfmodel`, contextWindow=`1000000`, reasoning unset (uncertain, non-blocking; ...)
  ```

  At review time, `/tmp/run-061-review.sh` runs `qodercli -w "$PROJECT" --permission-mode auto --agent sdd-executor -p "$(cat "$PROMPT")"`; `/tmp/log-061-review.log` is 0 bytes while `/tmp/heartbeat-061-review.log` grows.
- **Why it's a problem**: the framework's own primary loop runs the exact buffered print-mode shape its contract marks `PROHIBITED`, and it never exercises the new `resolve → cli_args → dispatch.sh → collect-dispatch` path. T030 correctly records the bypass but then overclaims compatibility: the recorded ④ is a manual model/context probe produced before the contract commit and does not satisfy the new "resolve exit 0 + config_id" criterion. The current review prompt also pre-frames the expected answer ("确认 ... 仍兼容（T030 已记录）") rather than asking for a test.
- **Proposed fix**: route the driver's recipes through the target project's `skills/internal/create-team/scripts/dispatch.sh` (stream-json + compact filter + `.live.log`/`.jsonl`/`.status`) using the resolver's `cli_args`, then call `exec-quant.py --action collect-dispatch`; or add a narrowly scoped stage-granularity exception to the Visibility Contract with a named compensating control and a contract test. Update `skills/internal/run-agent/references/dispatch-preflight.md` row ④ and the line-state template to require the exact resolve command, exit code, and `config_id`. Separate "direct runner bypasses run-agent (not exercised)" from "run-agent path would work" in T030's wording, and change the review prompt to ask for a verdict rather than confirm one.

### F4 — Plan decisions were not written back to requirements, forcing two analyze rounds and an implement-time requirements edit

- **Severity**: P1
- **Category**: Workflow
- **Propagation surface**: the analyze quality gate and the implement stage's requirement/plan/task edits; every future spec where plan decisions change acceptance premises.
- **Location**: `/tmp/log-061-analyze.log:15-21`; `/tmp/log-061-analyze-r2.log:45`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/requirements.md:198,207`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/plan.md:127-131`.
- **Evidence** (verbatim):

  ```
  r1:13: **结论：CRITICAL/HIGH ≠ 0，analyze 质量门不通过。** 按驱动规则，应将下列 4 项 HIGH 一次性回环到对应上游阶段修复，然后重跑 analyze（同一门最多回环一轮）。
  r2:45: **残留 M-02（MEDIUM）**：`claude + none` 正向夹具必须声明 `mode: external`——因为 C-EC-06（`contracts/execution-config-cli.md:60`）规定显式 `cli` + 生效 native/virtual 会被拒收；SC-006(a)、SC-006 Source、T004、T011 未写明该夹具前提。这与第一轮 C-02（SC-001 夹具默认层 `mode: external`）同型；行为已由契约完全钉死，测试作者可确定性推出，故 MEDIUM 而非 HIGH。
  ```

  The implement commit `be491b33` edits `requirements.md` by 4 lines to add exactly that premise (`SC-006(a)` now says `该夹具 MUST 声明 mode: external`). Round 1 also shows the calibration problem in the other direction: `7 sent / 4 confirm / 2 downgrade / 1 reject` (`/tmp/log-061-analyze.log:198`).
- **Why it's a problem**: plan-time decisions changed acceptance premises but were written only to plan/contracts, so analyze had to rediscover them; one (M-02) survived round 2 as MEDIUM and was repaired during implement, after the "HIGH=0" gate had passed. The two-round analyze plus remediation commits are an avoidable process cost.
- **Proposed fix**: in `skills/internal/create-plan/SKILL.md` Phase 0/Step 2, require a writeback table row for every plan decision that changes an acceptance premise or an output value domain (decision → owning FR/SC → writeback or explicit dated reference). In `skills/internal/analyze-artifacts/SKILL.md`, require a gate pass only when zero findings require edits to requirements/plan/tasks — "deferred to implement" must not count as converged. Add a checklist dimension: "Does every plan-only normative sentence have an owning FR/SC?"

### F5 — The checklist "refresh" edited the original checklist in place, violating the new-file-per-run rule, and two `[x]` items are not backed by requirements text

- **Severity**: P1
- **Category**: Workflow
- **Propagation surface**: the checklist artifact, the waiver, the implement-stage exemption gate, and any later audit that reads the checklist as evidence of requirements quality.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/create-checklist/SKILL.md:94`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/checklists/config-quant.md:14,20,65,73,106-108`; commits `71d59574` (original) and `be491b33` (rewrite); `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/requirements.md` (absence of `--snapshot`, `/proc`, `--host-cli`, `SPECKIT_HOST_CLI`).
- **Evidence** (verbatim):

  ```
  create-checklist/SKILL.md:94: - **Each run creates a NEW file** — never overwrite an existing checklist.
  config-quant.md:106-108: Check items are `[x]` after the analyze remediation round; the boxes assert that the **requirements text** carries the answer, not that code exists.
  config-quant.md:20: - [x] CHK003 Are all inputs required for snapshot-consistent collection (`--snapshot`, the current `--config-id`, and `--run-id`) stated at requirement level...
  config-quant.md:65: - [x] CHK033 Are the dependencies on the dispatch label, snapshot path, host detection (`/proc`, `--host-cli`, `SPECKIT_HOST_CLI`), and verified qodercli flags documented as assumptions with validity dates?
  ```

  `grep -- '--snapshot' requirements.md` returns nothing; `grep 'host-cli\|SPECKIT_HOST_CLI\|/proc' requirements.md` returns nothing. The original file at `71d59574` had 36 `- [ ]` rows; `be491b33` rewrote 137 lines into the current all-`[x]` form while keeping the original header.
- **Why it's a problem**: the wrap-up followed analyze's M-03 advice to "refresh" the checklist, but that advice conflicts with the checklist skill's lifecycle rule. The rewrite erased the artifact the waiver depended on, presents a post-hoc edit as the original run's result, and asserts closure for at least two items whose cited requirement text does not exist. The boxes are therefore not trustworthy as evidence.
- **Proposed fix**: in `skills/internal/create-checklist/SKILL.md`, add a re-check mode that never edits an existing checklist: create `checklists/<domain>-recheck-<date>.md`, keep the original as a dated record, and require every `[x]` to carry a short verbatim quote from the cited requirement line; an unquoted item stays `[ ]`. Point analyze M-03 and the implement wrap-up at the recheck file, not at an in-place refresh. Correct CHK003/CHK033 or the requirements they cite.

### F6 — Command literals in task rows are not re-derived; the `compile-embeds --write` drift recurs

- **Severity**: P1
- **Category**: Template
- **Propagation surface**: every future `tasks.md` generated from plan prose, and the implement stage that executes the rows.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/tasks.md:160`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/plan.md:109`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/contracts/dispatch-wiring.md:86`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/feature-ref.md:134`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/verification.md:120-124`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md:227-231`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/feedback/backlog.md:95`.
- **Evidence** (verbatim):

  ```
  tasks.md:160: python3 scripts/python/probe-utils.py --action compile-embeds --write (expect no-op)
  verification.md:121-124: Premise correction: tasks.md/doc used `compile-embeds --write`, but the probe CLI has no `--write` flag (write is the default; `--check` verifies). The first invocation exited 2 with "unrecognized arguments: --write"; the corrected form ran successfully.
  create-tasks/SKILL.md:227-231: Factual premises embedded in ANY task row — file existence, counts, ... are governed by the **Inherited premises** ... they are hypotheses to re-measure at generation time ...
  backlog.md:95: 命令型前提无同权实测义务:create-tasks 前提枚举不含命令字面/flag(`:227-231`),任务行 --write 类字面漂移到 implement 期才暴露;... open
  ```

  The same drift was already logged on 2026-10-13 in `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/feedback/20261013T161312Z-speckit-implement.md`: `T021 task rows specified a --write flag the engine deliberately does not have — task-premise drift from plan-phase wording`.
- **Why it's a problem**: the row is marked `[X]` even though its literal command exits 2; the premise enumeration covers counts and file existence but not command flags, so plan prose is copied into tasks and only caught at execution. The recurrence and the open backlog entry prove the current control is insufficient.
- **Proposed fix**: extend `skills/internal/create-tasks/SKILL.md` § Premise verification with a command-literal bullet: every subcommand/flag in a task row MUST be re-derived by running `<tool> <action> --help` at generation time and pasting the relevant help line. Apply the same rule in `skills/internal/create-plan/SKILL.md` for plan prose copied into tasks. Correct `tasks.md:160`, `plan.md:109`, `contracts/dispatch-wiring.md:86`, and `feature-ref.md:134`; close backlog F-07.

### F7 — The baseline of record is a dirty-tree, parked-file measurement and is not reproducible from the commit

- **Severity**: P1
- **Category**: Workflow
- **Propagation surface**: GATE-1 / SC-004 and every future baseline capture; the verification's pass counts.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/notes/baseline-failed.txt:3-4`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/notes/pre-change-measurements.md:33-36,97-121`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/tasks.md:24`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/verification.md:8,16`; `/tmp/061-baseline-run.txt`.
- **Evidence** (verbatim):

  ```
  baseline-failed.txt:3-4: Date: 2026-10-18 (implementation start, BEFORE any 061 source edit; captured with the three new 061 files parked so the tree matched pre-061 reality)
  pre-change-measurements.md:106-107: The three new 061 files (engine, defaults template, US1 contract test) were parked inside the feature's spec directory for this capture, so the tree matched pre-061 reality.
  tasks.md:24: ... the untracked `tests/contract/test_progress_reporting.py` is collected. The FAILED set still has 25 names and still has 7 in `test_exec_quant_engine.py`, but it differs from the frozen record by one unrelated swap ...
  verification.md:8: baseline_passed=3288
  verification.md:16: post_change_passed=3417
  ```

  File mtimes: `scripts/python/execution-config.py` 10:36:21, `tests/contract/test_execution_config_engine.py` 10:37:06, `notes/baseline-failed.txt` 10:41:38. `/tmp/061-baseline-run.txt` records `27 failed, 3285 passed` from the earlier dirty-tree run with the 061 files present.
- **Why it's a problem**: the "BEFORE any 061 source edit" header is not literally true — the baseline was captured after 061 files were authored and then parked. The accepted baseline also absorbs an untracked foreign test (9 tests) and a dirty-instructions node, so its collection set and pass count cannot be reproduced from the commit. The differences are disclosed, but the procedure relies on manual file parking and a dirty tree.
- **Proposed fix**: in `skills/internal/implement-feature/SKILL.md` § Test runs, require the baseline to be captured in a clean `git worktree` at `baseline_commit` (or with `git status --porcelain` empty), record `pytest --collect-only -q | tail -1` and the tracked path set, and forbid "parking" feature files. At final, assert the same collection count as well as `comm -13`/`comm -23`. Record the untracked/foreign file inventory with the run.

### F8 — `DoD Status` stays `pending` while the feature is `Implemented`

- **Severity**: P1
- **Category**: Template
- **Propagation surface**: the Pre-Status-Flip Gate, the feature registry, and every review/merge consumer.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/tasks.md:39`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features/061.md:6`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features.md:69`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/tasks-template.md:52`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/shared/workflow/feature-integration.md:39-51`.
- **Evidence** (verbatim):

  ```
  tasks.md:39: **DoD Status**: pending
  features/061.md:6: **Status**: Implemented
  tasks-template.md:52: **DoD Status**: pending | green | green-with-void <!-- flip to `green` only when every DoD-N row above is satisfied.
  ```

  The Pre-Status-Flip Gate in `feature-integration.md:39-51` checks deferred conversion, zero open tasks, SC status rows, deferred registry, and void rows; it does not mention `DoD Status`. A grep found seven feature `tasks.md` files still carrying `pending`.
- **Why it's a problem**: the state machine advanced to `Implemented` while the feature's own DoD line says unfinished. No gate step or implement-feature action owns the flip, so the contradiction is structural, not a one-off typo.
- **Proposed fix**: add a seventh Pre-Status-Flip Gate item: "`DoD Status` is `green` or `green-with-void` (with the void annotation)", and an explicit flip step in `skills/internal/implement-feature/SKILL.md` Step 8. Optionally make `validate-tasks.py` warn when a `pending` DoD row coexists with an `Implemented` registry row, and backfill the seven stale files.

### F9 — The review report template cannot carry the review gate's mandatory outputs

- **Severity**: P1
- **Category**: Template
- **Propagation surface**: every `/speckit.review` report generated from the template; P0 validation and downgrade auditing.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/review-template.md:54-88,131-141`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/skills/internal/review-sdd-process/SKILL.md:116-141`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/shared/workflow/objective-analysis-gate.md:23,26`.
- **Evidence** (verbatim):

  ```
  objective-analysis-gate.md:23: the emitted finding row carries the propagation surface as its FIRST field ... and the severity is DERIVED from that field
  objective-analysis-gate.md:26: state in the report that the same-author condition held, how detection was split, and how many findings validation downgraded
  review-template.md:76: - **Severity**: [P0 | P1 | P2]
  review-template.md:141: P0 validation status is stated explicitly. When the review raised zero P0 findings, use the standard wording: "No P0 findings raised; the P0 independent-validation pass is vacuously satisfied."
  ```

  The template has no propagation-surface field, no same-author/downgrade section, no `Unvalidated Findings` appendix (required by `review-sdd-process/SKILL.md` step 5), and no count-versus-rows check. This report had to add those sections ad hoc.
- **Why it's a problem**: the gate's output contract is unenforceable when the report artifact cannot record it. Severity derivation, downgrade rate, and rejected findings become invisible, and a later reviewer cannot audit the P0 path.
- **Proposed fix**: add `- **Propagation surface**: ...` as the first finding field in both `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/review-template.md` and its `.specify/templates/review-template.md` mirror; add `## Same-Author Detection & Validation` (condition, split, downgrade count/rate, validator roster) and `## Unvalidated Findings`; add a §7 checkbox "severity/category counts equal the enumerated finding rows"; update the skill's step 4 field list and step 6; add a contract test asserting these fields exist.

### F10 — The same-author gate, the anti-nesting clause, and the stage executor's toolset contradict each other

- **Severity**: P1
- **Category**: Workflow
- **Propagation surface**: every unattended review and its P0 validation evidence; the review skill's central safeguard.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/shared/workflow/objective-analysis-gate.md:15-16`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/skills/internal/review-sdd-process/SKILL.md:98-105,120-133`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/run-agent/SKILL.md:119-126`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/agents/templates/sdd-executor.agent.md:8`.
- **Evidence** (verbatim):

  ```
  objective-analysis-gate.md:15: **Fires**: the artifacts under analysis were produced by the agent now running the command, in the current session.
  objective-analysis-gate.md:16: **Does not fire**: the artifacts predate this session, or have a different author (another agent, ...).
  run-agent/SKILL.md:123: 循环层级恒为 1：驱动者 → 阶段执行者，不存在第三层). The pre-dispatch probe extends to this obligation
  sdd-executor.agent.md:8: capability-tools: [Read, Grep, Glob, Bash, Write, Edit]
  ```

  `grep -rn "anti-nesting\|pre-dispatch\|sdd-loop-driver" .specify/scripts/python scripts/python` returns nothing; the five-family preflight contains no prompt-content scan.
- **Why it's a problem**: in the driver's separate-stage model the gate does not fire by default (the artifacts predate the review agent's session), the only remedy the review skill allows (fresh-context subagents) is a third layer the anti-nesting clause forbids, and the declared stage executor has no subagent tool. The framework's claimed pre-dispatch enforcement probe does not exist. Review quality therefore depends on an undocumented adjudication, which this review had to make.
- **Proposed fix**: extend the gate's firing condition to "the same orchestrated lineage/loop, even when each stage is a separate agent", or have the driver's review stage prompt pass the condition explicitly. Narrow the anti-nesting clause to driver/loop skills and loop logic, and explicitly permit a stage command to delegate to skills and to the gate's read-only detector/validator wave. Add a subagent tool to `sdd-executor.agent.md` or state a degraded fallback in the review skill. Implement the claimed probe as a dispatch-preflight row plus a deterministic script and a contract test, or remove the claim.

### F11 — The analyze severity rubric rates an unexecutable acceptance criterion MEDIUM, and round 1's downgrade rate signals over-rating

- **Severity**: P2
- **Category**: Command Prompt
- **Propagation surface**: the severity semantics of every future `/speckit.analyze` run; the reliability of "HIGH=0" as a convergence signal.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/references/detection-and-severity.md:83`; `/tmp/log-061-analyze-r2.log:45`; `/tmp/log-061-analyze.log:22,198-202`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/requirements.md:198`.
- **Evidence** (verbatim):

  ```
  detection-and-severity.md:83: | **HIGH** | Duplicate or conflicting requirement; ambiguous security/performance attribute; untestable acceptance criterion |
  r2:45: **残留 M-02（MEDIUM）**：... 这与第一轮 C-02（SC-001 夹具默认层 `mode: external`）同型；行为已由契约完全钉死，测试作者可确定性推出，故 MEDIUM 而非 HIGH。
  r1:198: | Validation wave | 7 sent / 4 confirm / 2 downgrade / 1 reject |
  ```

  The implement commit `be491b33` later edited `requirements.md` to add the missing `mode: external` premise to SC-006/SC-006 Source — after the round-2 gate had passed.
- **Why it's a problem**: by the skill's own table, an acceptance criterion that cannot be executed from the requirements alone is HIGH; the same class was rated MEDIUM twice because it was derivable from a contract. Downgrading fix effort is legitimate; downgrading severity is what let the gate pass with an edit still needed. Round 1's 2 downgrades + 1 rejection out of 7 shows the same calibration drift in both directions.
- **Proposed fix**: add a non-derogable rule to `detection-and-severity.md`: "A Success Criterion or acceptance scenario that cannot be mechanically satisfied from `requirements.md` alone is HIGH; derivability from a contract may reduce fix effort, never severity." Require every downgrade of an acceptance-testability finding to quote the requirement text (not a contract clause) that makes it testable. Require a rerun to report "0 findings requiring edits to requirements/plan/tasks" before calling the gate passed.

### F12 — The preflight table has no local-topology forms, and row ④ asks for topology inputs the resolver cannot accept

- **Severity**: P2
- **Category**: Documentation
- **Propagation surface**: every local-topology line's preflight evidence, and remote-topology row ④ dispatches.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/run-agent/references/dispatch-preflight.md:11-15`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/run-agent/SKILL.md:71-75`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/agents/execution/logs/061-line-state.md:14-18`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/scripts/python/execution-config.py` (argparse surface).
- **Evidence** (verbatim):

  ```
  dispatch-preflight.md:11-15: ① SSH 连通性（**本地拓扑跳过**） ... ② ssh <alias> "id <run-user>" ... ③ ssh <alias> "su - <run-user> -c '<cli> --version'" ... ⑤ ssh <alias> "cd <project-dir> && test -d .specify ..."
  run-agent/SKILL.md:71-75: The inline argument names are exactly `--mode`, `--cli`, `--model`, `--reasoning-effort`, `--context-window`, `--extra-flags`, `--log-dir`, `--quantification-method`; pass the same values the dispatch will use, including the topology declaration inputs.
  line-state:14-18: ② run identity: ok — uid=501, non-root. ... ③ subagent CLI: ok — qodercli 1.1.73, on PATH. ...
  ```

  `execution-config.py --help` accepts `--workspace-root`, `--action`, `--agent`, the configuration flags, `--host-cli`, `--format`; it has no `--alias` or `--run-user`.
- **Why it's a problem**: only row ① declares a local variant, so a local line must invent commands for ②③⑤; its "ok" evidence is not comparable with a remote line's. Row ④'s "including the topology declaration inputs" is unsatisfiable because two of the four topology elements are transport identity, not resolver inputs.
- **Proposed fix**: add a local-topology command column (or section) for ②③⑤ (`id -u`, `<cli> --version`, and the `.specify/` checks in `<project-dir>`); state that `<alias>` is unused locally. Split the declaration into configuration dimensions (project dir + mode/cli/model/...) and transport dimensions (alias/run-user, owned by ①②③); change row ④ to "inline config overrides" and add a sentence that alias/run-user are never resolver inputs.

### F13 — The waiver is stale and under-scoped

- **Severity**: P2
- **Category**: Documentation
- **Propagation surface**: the waiver file as read by the review/audit stage and any future reconstruction of why implement proceeded.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/waivers.md:3-14`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/verification.md:168-170`.
- **Evidence** (verbatim):

  ```
  waivers.md:5-6: `checklists/config-quant.md` still carries its 36 open CHK rows and the pre-remediation `Recorded Gaps` table.
  waivers.md:10-13: Waiver: proceed with implement without a blocking checklist gate. Disposition: refresh both checklists' Recorded Gaps/notes at implement wrap-up (M-03)...
  verification.md:170: **M-03**: both checklists refreshed — config-quant's 36 CHK boxes are checked...
  ```

  The current checklist has 0 `[ ]` rows and a post-remediation disposition table at `line 73`; the waiver has no closure/superseded line. The implement commit also edited `requirements.md` (4 lines), `plan.md` (6 lines), and `tasks.md` (72 lines) outside the waiver's stated checklist scope.
- **Why it's a problem**: the waiver still reads as an active exemption whose factual premise is false, and it does not disclose the upstream artifact edits made during implement. A reviewer cannot tell what was waived, what was done, or whether the disposition completed.
- **Proposed fix**: in `skills/internal/implement-feature/SKILL.md` § Checklist exemption gate, define a waiver record format with `Scope` / `Basis` / `Disposition` / `Closed (<date>, <evidence path>)`; require a closure line at wrap-up; require any upstream artifact edit made during implement to be listed as its own scope entry with the analyze finding IDs and commit SHA. Annotate this waiver as superseded by M-03 / `checklists/config-quant.md:73`.

### F14 — The "qoder defaults" literal set has seven copies and no declared owner; the leak test pins literals instead of the template

- **Severity**: P2
- **Category**: Documentation
- **Propagation surface**: the SC-006 leak test and every artifact that must move when the defaults template changes.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/requirements.md:198,229,248`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/plan.md:180`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/contracts/execution-config-cli.md:91`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/feature-ref.md:49,55`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/tasks.md:115`; `/tmp/log-061-analyze-r2.log:91`.
- **Evidence** (verbatim):

  ```
  r2:91: `qoder 默认值`字面集在 SC-006、C-EC-09、feature-ref、plan 风险 2、T011、Clarifications 六处出现。... 未来若模板值变化，需同步六处。当前不构成 Fail。
  requirements.md:229: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.
  ```

  The actual count in the authored artifacts is seven (requirements SC-006 + Clarifications, plan risk 2, contract C-EC-09, feature-ref ×2, tasks T011); the set is not registered as a Shared String, so `ref-resolvable` never checks it. `templates/execution-config-defaults.yaml` is explicitly user-editable (`data-model.md:186`), so a hardcoded test literal set stops detecting leaks of edited defaults.
- **Why it's a problem**: a test-counted literal set with seven hand copies has no owner and an already-wrong count. The requirements template's own anti-copy mechanism sits unused, and the leak test's discrimination is bounded by a user-editable template.
- **Proposed fix**: add `STR-016` for the literal set (or better, derive the set at test time from `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/execution-config-defaults.yaml`), replace the copies with `[[STR-016]]` or pointers, and make analyze's "uncounted observation" channel impossible: every systemic observation must be a numbered finding or be dropped.

### F15 — A `/tmp` file is named the feature's "terminal authority" and the analyze reports are not in-repo

- **Severity**: P2
- **Category**: Documentation
- **Propagation surface**: later sessions, reviewers, and any machine that does not share this `/tmp`; the feature's scope-adjudication provenance.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/plan.md:5`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/feature-ref.md:6`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features/061.md:46`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/requirements.md:6`; `/tmp/061-subagent-cli-config-brief.md`; `/tmp/log-061-analyze.log`; `/tmp/log-061-analyze-r2.log`.
- **Evidence** (verbatim):

  ```
  plan.md:5: ...；终态权威文档 `/tmp/061-subagent-cli-config-brief.md`
  feature-ref.md:6: **Terminal authority**: `/tmp/061-subagent-cli-config-brief.md`（已裁定范围未被静默改写）
  features/061.md:46: - 需求简报（终态权威文档）: `/tmp/061-subagent-cli-config-brief.md`
  ```

  The brief and both analyze reports exist only under `/tmp`; neither is referenced from `notes/` or `verification.md`, and none is committed.
- **Why it's a problem**: a terminal authority that disappears on reboot or temp cleanup makes every "已裁定范围未被静默改写" claim unverifiable in later phases. The same applies to the two analyze reports that justify the gate history.
- **Proposed fix**: copy the brief into `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/notes/input-brief.md` (or fold its adjudications into requirements Clarifications) and repoint the three citations; store the analyze reports under `notes/` as dated records. Add a rule to `skills/internal/create-requirements/SKILL.md` that any supplied brief is copied into the spec directory, and to `templates/feature-details-template.md` that Related Files lists only tracked in-repo paths.

### F16 — "All eight extensions are same-nodeid edits" is false: two new test methods were added after the baseline

- **Severity**: P2
- **Category**: Documentation
- **Propagation surface**: the intentional-extension disclosure, SC-004 / GATE-1 evidence, and future gate audits.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/verification.md:100`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/tasks.md:43`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_exec_quant_engine.py:414,420`; commit `be491b33`.
- **Evidence** (verbatim):

  ```
  verification.md:100: All eight extensions are same-nodeid edits; none surfaced as a new failing nodeid.
  tasks.md:43: The registered intentional extensions (T012/T013) are same-nodeid pin edits and MUST NOT surface as new nodeids.
  ```

  The commit adds two new methods to `tests/contract/test_exec_quant_engine.py`: `test_collect_rejects_agent_form` (line 414) and `test_agent_unit_type_is_a_valid_listing_choice` (line 420). The final collected delta is +129 = 127 new-file tests + 2 new methods.
- **Why it's a problem**: the gate is FAILED-nodeid-only, so the two new (green) nodes are invisible to it; the disclosure nonetheless claims they do not exist. The +2 pass delta is unexplained in `verification.md`. The gate outcome (zero new failures) still holds; the provenance claim does not.
- **Proposed fix**: add a "nodeid status (existing/new)" column to the intentional-extension table and list the two new nodes; compare `pytest --collect-only` nodeids in GATE-1 (or explicitly scope the gate to FAILED nodeids and stop claiming "same-nodeid"); reword T012 to distinguish pin edits from new tests.

### F17 — GATE-4's open-row check cannot go red; the tasks template ships the same inverted form

- **Severity**: P2
- **Category**: Template
- **Propagation surface**: every future `tasks.md` completion gate; the blind-check lesson.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/tasks.md:46`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/tasks-template.md:82`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/docs/reference/history/00-cross-cutting-lessons.md` §十二.
- **Evidence** (verbatim):

  ```
  tasks.md:46: - GATE-4: No open task rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/061-subagent-cli-config/tasks.md; true` returns 0.
  tasks-template.md:82: - GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' tasks.md` returns 0
  ```

  `grep -c` exits 1 when the count is zero (the desired state), which is why the task row appended `; true`, making the command always exit 0.
- **Why it's a problem**: the gate's only pass signal is a human reading stdout; a runner that checks the exit status would pass with open rows present. The subject (zero open rows) is true here, but the check does not prove it.
- **Proposed fix**: change the template and the task row to `test "$(grep -cE '^- \[[ >]\]' tasks.md)" -eq 0` or `! grep -qE '^- \[[ >]\]' tasks.md`, and state "exit 0 = pass". Add the §十二 mutation-drill requirement ("would this go red if the subject broke?") to gate authoring.

### F18 — The generation trio rewrote foreign dirty copies, and concurrent-line isolation has no declaration artifact

- **Severity**: P2
- **Category**: Automation / Scripts
- **Propagation surface**: every dirty workspace that runs `regen-command-copies.py` / `sync-mirrors.py`; the verification's pass counts; the U6 archive/merge closure.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/verification.md:126,183-185`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.qoder/commands/speckit.instructions.md`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/agents/execution/logs/061-line-state.md:12`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/dispatch-recipes.md:71-78`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_progress_reporting.py`.
- **Evidence** (verbatim):

  ```
  verification.md:126: regen "Regenerated command copies for 4 tools" (no command-template change)
  verification.md:183-185: pre-existing dirty files (instructions mirrors, `records.jsonl`, `glossary.md`, session/feedback records, progress-reporting guideline) were not modified by this run
  line-state:12: Foreign dirty files appeared during the run (progress-reporting guideline + instructions/mirror updates): ... Not part of 061; leave untouched and decide at U6.
  dispatch-recipes.md:71-78: 他线隔离项（并发隔离声明列出的路径）→ 保留不动，逐项登记进收尾汇总 ... 工作树归零才进入合并
  ```

  The four per-tool instruction copies (`.qoder/commands/speckit.instructions.md`, `.claude/commands/speckit.instructions.md`, `.github/prompts/speckit.instructions.prompt.md`, `.opencode/command/speckit.instructions.md`) have mtime 10:56:24, while their source `templates/commands/instructions.md` is 09:15:04 — the generator wrote them during the 061 run. No `*-isolation.md` declaration exists in `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/agents/execution/logs/`. The untracked `tests/contract/test_progress_reporting.py` (9 tests) sits in pytest's default collection path and changes the pass counts.
- **Why it's a problem**: the verification's "not modified by this run" claim is false in the file-write sense; a whole-tree generator can mutate unrelated command surfaces, and the only safeguard is explicit-path staging at commit time. U6's isolation rule keys off a "concurrent isolation declaration" that no step creates, so the closure precondition is missing.
- **Proposed fix**: give `regen-command-copies.py` and `sync-mirrors.py` an `--only <path>` scope; in `skills/internal/implement-feature/SKILL.md` § Command/template edits and the T026-style step, require a pre-run dirty inventory and assert the write delta is a subset of the feature's touched paths (or run the trio in a clean worktree). Make the isolation declaration a required artifact at first observation (`<line>-isolation.md`, path + owner per line), read by U4/U6. Correct `verification.md:183-185`, and record the untracked-file inventory with the suite run.

### F19 — T033/DoD-7 seeding evidence is assertion-only, not a pasted measurement

- **Severity**: P2
- **Category**: Documentation
- **Propagation surface**: the FR-027 runtime-precondition claim and every future seeding task.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/tasks.md:164`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/verification.md:134-139`; contrast `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/notes/quickstart-run.md:144-190`.
- **Evidence** (verbatim):

  ```
  tasks.md:164: assert `test -f .specify/agents/execution/configs/_defaults.yaml` exits 0, its bytes equal the template's, and a second invocation leaves it byte-identical ... the evidence line is recorded in `verification.md`
  verification.md:134-139: - `.specify/agents/execution/configs/_defaults.yaml` exists (exit 0 for `test -f`). - Content is byte-equal to `templates/execution-config-defaults.yaml`. - Seeding is idempotent (second invocation leaves bytes unchanged); `git check-ignore` exits 1...
  ```

  No command line or actual output is pasted; S5 in `quickstart-run.md` does paste its invocation and output.
- **Why it's a problem**: the record asserts existence, byte-equality, and idempotency without showing the invocation or output; a manual copy followed by one check would satisfy these lines. The seeded file and template share mtime 10:56:13, so provenance cannot be reconstructed from the record. The claims are true today (I re-verified byte-equality), but the evidence is not re-derivable.
- **Proposed fix**: paste the seeding invocation and output in `verification.md` § T033 (as S5 does), or cite the `tests/integration/test_init_execution_config.py` nodeids plus the `test -f`/`cmp` output. Add a general line to `skills/internal/implement-feature/SKILL.md` Gate Function: a DoD/evidence line MUST carry the command and its output, not adjectives.

### F20 — Contract text can silently lose an explicit quantification method, and two clauses duplicate the mode-derivation algorithm

- **Severity**: P2
- **Category**: Documentation
- **Propagation surface**: `execution-config.py resolve` output, the `collect-dispatch` record's `method_requested`/`method_resolved`, and the SC evidence built from them.
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/contracts/execution-config-cli.md:84,59,68`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/data-model.md:111`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/execution-config.py:452-466`.
- **Evidence** (verbatim):

  ```
  contract:84: `requested` = highest-layer explicit method; if absent or the defaults layer is skipped, `auto`.
  data-model:111: **Requested**: 最高层显式方法值；若默认层被跳过或无任何层声明 → `auto`。
  contract:68 (C-EC-07): mode derivation restated: "The mode is external when (a) ... (b) ... or (c) ..."
  contract:59 (C-EC-06): the same derivation is owned here.
  ```

  The implementation (`scripts/python/execution-config.py:452-466`) checks inline, then agent-config, then participating defaults, then `auto` — so an agent-layer explicit `qoder-settings` survives a skipped defaults layer. The contract's literal wording would set it to `auto` and then auto-resolve to `none` + warning, contradicting FR-010's no-downgrade rule.
- **Why it's a problem**: read literally, C-EC-09 silently downgrades an explicitly requested method whenever the defaults layer is skipped. The code happens to be correct, but the artifact is contradictory and untested for this corner. C-EC-06 and C-EC-07 restate the same derivation, so a future edit to one can diverge from the other — and neither is machine-parseable under the current clause syntax.
- **Proposed fix**: correct C-EC-09 to "`requested` = highest-layer explicit method; if absent → `auto`; skipping the defaults layer removes only that layer's value, never a higher layer's explicit method", and add the agent-`qoder-settings` + claude-defaults fixture as a required negative/positive case. Reduce C-EC-07 to a derived one-liner: "`requires_external` is `true` exactly when the effective `mode` is `external`; mode derivation is owned by C-EC-06."

## 4. What Worked — Preserve (Brief)

- The deterministic requirements/tasks validators run clean (`status: ok`, `PASS` 0/0) and caught structural drift cheaply.
- Red-first evidence is genuine: autouse fixtures made the new test files error on missing artifacts, and earlier vacuous exit-2 passes were explicitly tightened.
- The baseline comparison is name-level in both directions (`comm -13` and `comm -23` empty), and the seven pre-existing `test_exec_quant_engine.py` failures are reconciled node by node.
- The generation trio, mirror byte-identity, and `## Wrap-up` no-edit checks are strong, reproducible controls; the defaults seeding is tested for absent / present / user-edited / missing-source cases.
- The feature's own error paths are loud and field-specific (exit 2 with field + supported set), and the S6 real-dispatch run was correctly left authorization-gated.
- T030 recorded the driver's actual dispatch path and did not silently adapt; the bypass verdict is at least visible for this review to challenge.
- The two analyze rounds did catch the four HIGH issues and the remediation was bounded and committed.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-T1 — Teach the tasks template to carry command-literal premises.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/tasks-template.md` § Format / § Premise verification. Change: require every subcommand/flag in a task row to carry the `--help` line that proves it exists. Source: F6. Expected impact: eliminates the recurring `--write` class before execution.
- **REC-T2 — Close the DoD state machine.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/tasks-template.md:52` and `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/shared/workflow/feature-integration.md:39-51`. Change: add `DoD Status` to the Pre-Status-Flip Gate and an explicit flip step. Source: F8. Expected impact: `Implemented` can no longer coexist with `pending`.
- **REC-T3 — Make the review template carry the gate's outputs.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/review-template.md:76,131-141` and its `.specify/templates/` mirror. Change: propagation-surface-first field, same-author/downgrade section, Unvalidated Findings appendix, count-versus-rows checkbox. Source: F9. Expected impact: P0/downgrade history becomes auditable.
- **REC-T4 — Fix the open-row gate's exit status.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/tasks-template.md:82`. Change: `! grep -qE '^- \[[ >]\]' tasks.md` or `test "$(grep -c ...)" -eq 0`; state "exit 0 = pass". Source: F17. Expected impact: the gate can actually go red.

### 5.2 Command Prompt Improvements

- **REC-C1 — Make analyze run the deterministic coverage accountant.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/SKILL.md:76-90` and `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/analyze.md`. Change: run `account-clause-coverage.py <spec-dir>`, surface `clause-unparsable` / `fr-uncovered` as findings, and forbid coverage percentages unless the accountant's FR lane is empty. Source: F2, F4. Expected impact: traceability claims become machine-derived.
- **REC-C2 — Make acceptance-testability findings non-downgradable.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/references/detection-and-severity.md:83`. Change: the non-derogable HIGH rule and the requirement-text downgrade proof. Source: F11. Expected impact: "HIGH=0" becomes a reliable convergence signal.
- **REC-C3 — Require plan-decision writeback.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/create-plan/SKILL.md` Phase 0 / Step 2. Change: writeback table for every decision that changes an acceptance premise or value domain. Source: F4. Expected impact: removes the two-round analyze tax.
- **REC-C4 — Require `[green:]` claims and canonical clause IDs.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md` § From Contracts and `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/create-plan/SKILL.md` Phase 1. Change: every contract-backed verification row declares `[green: <contract>#<clause>]` or a recorded reason; contracts use `**C-N**` per `shared/definitions/contract-clause-definitions.md` §3; run `clause_extract.py` as a gate. Source: F2. Expected impact: the clause/FR lane stops being empty.
- **REC-C5 — Make checklists append-only and evidence-quoted.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/create-checklist/SKILL.md:94`. Change: new recheck file per run; every `[x]` quotes the requirement line; no in-place refresh. Source: F5. Expected impact: checklist evidence stays truthful and auditable.
- **REC-C6 — Define the waiver closure format.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` § Checklist exemption gate. Change: `Scope` / `Basis` / `Disposition` / `Closed`; list upstream artifact edits. Source: F13. Expected impact: waivers stop being stale open-ended records.

### 5.3 Automation / Script Improvements

- **REC-A1 — Render the engines' required flags.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/probe-utils.py:881-883` and `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/shared/definitions/probe-definitions.md:180-187`. Change: `REQUIRED_FLAGS` per engine/action, carried by the Handler model and rendered as placeholders; add an executable contract test. Source: F1. Expected impact: the wrap-up tax disappears across all compiled faces.
- **REC-A2 — Capture baselines in a clean worktree.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` § Test runs. Change: clean-worktree requirement, `--collect-only` count, tracked path set, untracked inventory; forbid parking. Source: F7. Expected impact: baseline and final counts become reproducible from the commit.
- **REC-A3 — Give generators a scope guard and require an isolation declaration.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/regen-command-copies.py` and `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/sync-mirrors.py`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/dispatch-recipes.md:71-78`. Change: `--only <path>`, pre-run dirty inventory, `<line>-isolation.md` artifact. Source: F18. Expected impact: foreign dirty state can no longer be silently rewritten or folded into a baseline.
- **REC-A4 — Paste seeding evidence.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md` Gate Function. Change: command + actual output, not adjectives. Source: F19. Expected impact: runtime-precondition claims become re-derivable.

### 5.4 Workflow Improvements

- **REC-W1 — Reconcile the driver with the Visibility Contract.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/dispatch-recipes.md:27-57`. Change: route through `dispatch.sh` + stream-json + resolver `cli_args` + `collect-dispatch`, or record a stage-granularity exception with a compensating control. Source: F3. Expected impact: the framework's own loop stops running the prohibited shape.
- **REC-W2 — Fix the same-author/anti-nesting/toolset contradiction.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/shared/workflow/objective-analysis-gate.md:15-16`, `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/run-agent/SKILL.md:119-126`, `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/agents/templates/sdd-executor.agent.md:8`. Change: extend the firing condition to the orchestrated lineage, narrow anti-nesting, add the subagent tool or a fallback, implement or remove the claimed probe. Source: F10. Expected impact: the review gate is executable as written.
- **REC-W3 — Separate bypass from compatibility in T030.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/verification.md:143-146` and the review-stage prompt. Change: record the exact resolve command/exit/`config_id` for row ④; state "direct runner bypasses run-agent (not exercised)" separately; ask the reviewer to test, not confirm. Source: F3. Expected impact: FR-027 evidence stops overclaiming.

### 5.5 Documentation Improvements

- **REC-D1 — Enforce the canonical clause form at authoring time.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/definitions/contract-clause-definitions.md` §3 and the contract-authoring surface in `skills/internal/create-plan/SKILL.md`. Change: a one-line MUST plus a `clause_extract.py` gate; a contract test scanning the newest spec. Source: F2. Expected impact: new contracts stay machine-readable.
- **REC-D2 — Give the qoder literal set one owner.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/requirements.md:198` and `templates/requirements-template.md:153`. Change: `STR-016` or a template-derived set; replace copies with references. Source: F14. Expected impact: the leak test tracks the actual template.
- **REC-D3 — Make terminal authorities durable.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/create-requirements/SKILL.md` § Input Contract and `templates/feature-details-template.md` § Related Files. Change: copy supplied briefs into the spec directory; forbid `/tmp` paths in tracked records. Source: F15. Expected impact: scope adjudications survive the session.
- **REC-D4 — Fix the record-law writeback and the `requested` wording.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/061-subagent-cli-config/contracts/execution-config-cli.md:84` and `data-model.md:111`; `templates/requirements-template.md` for the record-law writeback rule. Source: F4, F20. Expected impact: no explicit method is silently downgraded; plan-only laws have owning FRs.
- **REC-D5 — Keep evidence references in-repo.** Target: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/create-requirements/SKILL.md` and the feature-details template. Source: F15. Expected impact: reviewers can open what the artifacts cite.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | (none — final P0 count is zero) | — | — |
| P1 | Render the engines' required flags in compiled Wrap-up faces | `scripts/python/probe-utils.py` + `probe-definitions.md` | F1 |
| P1 | Enforce canonical clause IDs and run clause/FR coverage | `create-plan`, `create-tasks`, `analyze-artifacts`, `clause_extract.py` | F2 |
| P1 | Reconcile the driver's dispatch shape with the Visibility Contract | `dispatch-recipes.md`, `run-agent/SKILL.md`, preflight | F3 |
| P1 | Require plan-decision writeback; make analyze convergence mean zero upstream edits | `create-plan/SKILL.md`, `analyze-artifacts/SKILL.md` | F4 |
| P1 | Make checklists append-only and evidence-quoted | `create-checklist/SKILL.md` | F5 |
| P1 | Re-derive command literals in task rows | `create-tasks/SKILL.md`, `tasks-template.md` | F6 |
| P1 | Capture baselines in a clean worktree with a pinned collection set | `implement-feature/SKILL.md` § Test runs | F7 |
| P1 | Close the DoD state machine | `tasks-template.md`, `feature-integration.md` | F8 |
| P1 | Make the review template carry the gate's outputs | `review-template.md` | F9 |
| P1 | Resolve same-author vs anti-nesting vs toolset | `objective-analysis-gate.md`, `run-agent/SKILL.md`, `sdd-executor.agent.md` | F10 |
| P2 | Calibrate analyze severity for untestable acceptance criteria | `detection-and-severity.md` | F11 |
| P2 | Add local preflight forms and fix row ④ topology inputs | `dispatch-preflight.md`, `run-agent/SKILL.md` | F12 |
| P2 | Close the waiver at wrap-up and scope upstream edits | `implement-feature/SKILL.md`, `waivers.md` | F13 |
| P2 | Give the qoder literal set one owner | `requirements.md`, `requirements-template.md` | F14 |
| P2 | Move terminal authorities in-repo | `create-requirements/SKILL.md`, feature-details template | F15 |
| P2 | Disclose new nodeids, not only FAILED nodeids | `verification.md`, `implement-feature/SKILL.md` | F16 |
| P2 | Make the open-row gate able to go red | `tasks-template.md` | F17 |
| P2 | Scope the generators and require an isolation declaration | `regen-command-copies.py`, `sync-mirrors.py`, `dispatch-recipes.md` | F18 |
| P2 | Paste seeding evidence | `verification.md`, `implement-feature/SKILL.md` | F19 |
| P2 | Fix the `requested` wording and de-duplicate mode derivation | `contracts/execution-config-cli.md`, `data-model.md` | F20 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute. The repository is unpushed and SSH-only, so URL-form citations are not used; Appendix C gives `git show` recovery commands.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No unresolved template placeholder tokens remain. Bracketed forms inside quoted evidence (`[x]`, `[ ]`, `[green: ...]`, `[P0 | P1 | P2]`) are literals under discussion, not fill-in fields.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly. Final P0 count is zero; three P0 candidates were raised, independently validated, and downgraded to P1. The P0 validation pass was executed, not vacuous. No P0 waiver is required. The template's standard "no P0 findings raised; vacuously satisfied" wording does not apply because candidates were raised and validated down.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

---

## Appendix A — Same-Author Detection & Validation Log

- **Condition**: shared unattended-loop authorship across stage agents; the literal current-session gate would not fire, so the stricter cross-stage reading was applied.
- **Detectors** (all fresh-context, read-only, disjoint scopes):
  - A: requirements, both checklists, waivers, two analyze reports, feature registry.
  - B: plan, data-model, three contracts, feature-ref, clause-syntax owner and precedent specs.
  - C: tasks, quickstart, verification, notes, recorded suite evidence, implement-feature test-run owner.
  - D: run-agent, preflight, subagent-definitions, loop driver, review skill/template, Wrap-up engines, foreign progress-reporting files.
- **Validator wave** (disjoint from detection):
  - Validator 1: contract clause syntax → downgrade P0→P1.
  - Validator 2: Wrap-up embed parameters → downgrade P0→P1.
  - Validator 3: driver dispatch bypass → downgrade P0→P1.
- **Downgrade rate**: 3/3 (100%). **Rejected**: 0.
- **Detector findings merged into retained findings** (not separate defects):
  - A-F-01 (coverage instrument not invoked) → F2.
  - B-2 (analyze accepted unparseable contracts) → F2.
  - B-3 (plan has no clause-syntax gate) → F2.
  - B-4 (feature-ref ID table not semantic) → F2.
  - B-6 (literal set copies) → F14.
  - B-7 (`/tmp` authority) → F15.
  - B-8 (C-EC-06/C-EC-07 duplication) → F20.
  - C-4 (generator rewrote foreign copies) → F18.
  - D-3 (T030 preflight record pre-contract) → F3.
  - D-6/D-7 (preflight local/topology) → F12.
  - D-8 (isolation declaration) → F18.
  - A-3 (waiver stale) → F13.
  - A-4 (record-law writeback) → F4/F20.
  - A-5 (severity calibration) → F11.
  - A-6 (literal set) → F14.
  - A-7 (`/tmp` authority) → F15.
  - C-1 (preflight compatibility) → F3.
  - C-2 (baseline procedure) → F7.
  - C-3 (`--write` drift) → F6.
  - C-5 (DoD pending) → F8.
  - C-6 (new nodeids) → F16.
  - C-7 (GATE-4 blind check) → F17.
  - C-8 (T033 evidence) → F19.
  - D-4 (review template output) → F9.
  - D-5 (same-author/anti-nesting) → F10.
  - D-1 (Wrap-up) → F1.
  - D-2 (driver dispatch) → F3.
- **Dropped detector claims**:
  - The "253 lines vs 252 `wc -l`" discrepancy is not a false claim; the validator's 253 includes the trailing split element. Not retained.
  - The claim that C-EC-09's `requested` wording produces a live silent downgrade is corrected in F20: the implementation preserves agent-layer explicit methods; the defect is the contract text and the missing corner-case test, not current behavior.
- **Process anomalies surfaced by detection and integrated**: the baseline header's "BEFORE any 061 source edit" is literally false (F7); "all eight extensions are same-nodeid" is false (F16); "preflight ④ still accepts its existing evidence form" is contradicted by the new row ④ (F3); `DoD Status: pending` coexists with `Implemented` (F8); the waiver's 36-open-rows premise is false (F13); `compile-embeds --write` does not exist (F6).

## Appendix B — Unvalidated Findings

No P0 candidate was rejected; no finding in this report is unvalidated. Findings downgraded from P0 are labeled `(validated: downgraded from P0)` in place. There is no separate unvalidated appendix because the validation wave produced no rejection.

## Appendix C — Evidence Recovery Commands

Because `c3a268f6` is not reachable from any remote, recover the cited files with:

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
git show c3a268f6:.specify/specs/061-subagent-cli-config/requirements.md
git show c3a268f6:.specify/specs/061-subagent-cli-config/plan.md
git show c3a268f6:.specify/specs/061-subagent-cli-config/tasks.md
git show c3a268f6:.specify/specs/061-subagent-cli-config/verification.md
git show be491b33:scripts/python/execution-config.py
git show be491b33:scripts/python/exec-quant.py
```

The two analyze reports and the terminal brief exist only under `/tmp`:
`/tmp/log-061-analyze.log`, `/tmp/log-061-analyze-r2.log`, `/tmp/061-subagent-cli-config-brief.md`. The recorded full-suite run is `/tmp/061-verify-pytest.txt`; the failed-name lists are `/tmp/061-verify-failed.txt` and `/tmp/061-baseline-failed.txt`.
