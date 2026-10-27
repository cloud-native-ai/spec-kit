# Specification-Driven Development (SDD) Process Review Report: Review 命令与代码评审技能的组合与治理

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 071 |
| Requirement Key | `071-review-code-integration` |
| Requirement Name | Review 命令与代码评审技能的组合与治理（Review × Code-Review Composition） |
| Related Feature | 071 Review 命令与代码评审技能的组合与治理（Review × Code-Review Composition） |
| Repository | `spec-kit` |
| Repository URL | `git@gitee.com:cloud-native-ai/spec-kit.git`, `git@github.com:cloud-native-ai/spec-kit.git`, `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (from `git remote -v`). `origin` is `git@github.com:github/spec-kit.git` — the UPSTREAM project, which holds none of these commits |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — nothing was pushed. Cite absolute paths plus `git show <sha>:<path>`; no URL citation in this report resolves |
| Branch | `master` |
| Commit SHA | `9b45a1b25159c1ff5d92cea8e8e1d3549e8887d5` (short: `9b45a1b2`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-27 |
| Reviewer (Agent) | SDD executor subagent (unattended loop, stage `review`, run `r20261027T061144Z-a3ec`) — a different agent and a different session from the one that wrote the artifacts under review |
| Environment | Linux 5.10.134-15.2.al8.x86_64; bash 4.4.20; git 2.43.5; python 3.11.11; `delta` present at `/home/agent/.cargo/bin/delta`; stdout is **not** a TTY |
| spec-kit Source Snapshot | `/storage/project/cloud-native-ai/spec-kit` @ `9b45a1b2` (self-hosting: the framework sources and the `.specify/` runtime are in one tree), `specify-cli` 0.0.22 |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 308 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/requirements.md` | 28 FR / 7 SC / 5 user stories / 10 shared strings, with the Q1–Q9 adjudications in `## Clarifications` |
| plan.md | 299 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/plan.md` | Design, constitution check (16/16), mirror obligations, risks R-01…R-16, change log |
| tasks.md | 404 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/tasks.md` | 36 rows across Setup/Foundational/US1–US5/Polish, DoD-1…DoD-7, per-row `[green:]` clause claims |
| data-model.md | 217 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/data-model.md` | 13 entities, validation rules V1–V35 |
| research.md | 231 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/research.md` | R1–R14 repository measurements (exit-code alphabet, TTY rule, timestamp form, pin authorization) |
| quickstart.md | 168 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/quickstart.md` | 8 scenarios A–H, each with premises and a recorded execution status |
| contracts/ (6 files) | 366 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/contracts/` | 74 clauses C-1…C-74 (+ amendment logs) across orchestration, skill, receipt, gate, feedback, tests/docs |
| checklists/ (2 files) | 360 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/checklists/` | `requirements.md` 16/16; `review-composition.md` 40 items (13 PASS / 27 FAIL, all dispositioned) |
| notes/ (6 files) | 1557 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/notes/` | Red-first evidence per group, quickstart run log, remediation worklists, pre-change measurements |
| verification.md | 101 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/verification.md` | SC-001…SC-007 status rows (5 `pass` bound to hashed evidence, 2 honest `partial`) |
| code-review.md (this run's code record) | 778 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/code-review.md` | Code segment: 9 opinions over the 11 code paths + coverage receipt + answers |
| feature detail | 84 | `/storage/project/cloud-native-ai/spec-kit/.specify/memory/features/071.md` | `## Latest Review` per-stage entries and the status cell under review here |

## 1. Process Execution Timeline

Reconstructed from `git log` scoped to `REQUIREMENTS_DIR` (20 commits, all attributable by message prefix and by the artifact set each one touches).

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Requirements stage lands spec + feature registration | `8d18265b`, `c3a28d91` (wrap-up) | No. One deviation, disclosed in the spec's Assumptions: the scaffold's branch switch was suppressed (an unattended stage subagent may not switch branches) |
| 2 | Clarify adjudicates the cross-segment boundaries | `0d2d2d66`, `884e7a86` | No |
| 3 | Plan lands 6 contracts / 73 clauses | `4932c2b1`, `ac2d1821` | No |
| 4 | Checklist stage; later found to have been **omitted from the feature-detail record** and back-filled | `89daf845`, `ee4e5070`; detail's note "此前本登记面漏记该阶段，于 2026-10-27 的修复轮补记" | Yes — the `## Latest Review` carrier was not updated by the stage that ran; repaired later by a different stage |
| 5 | Analyze gate **FAIL**: `GATE: CRITICAL=0 HIGH=6` (32 findings) | `771720db`, `8b556933`, `test-evidence/analyze-report.md` | Not a deviation; the gate worked |
| 6 | One authorized upstream repair round: requirements → plan → tasks | `14a1c6ec`, `2c42bbbe`, `fc007019` | No. Clause ids preserved, the single new obligation appended as C-74 rather than inserted |
| 7 | Analyze re-run clears the gate | `30391ec3`, `test-evidence/analyze-rerun-report.md` | No |
| 8 | Implement part 1 consumes the E2 baseline slot (5983 passed / 26 pre-existing failures) | `b7f0cadc`; `test-budget` ledger row 1 | No |
| 9 | Implement parts 2–7a land the six contract groups, the mirrors and the doc surface | `a6625f32` … `f02d9a0b` | No |
| 10 | Implement part 7b runs the quickstart band and writes the verification log | `9b45a1b2` | **Yes** — the commit touches `verification.md`, `tasks.md` and `notes/`, and does **not** touch `features.md` or `features/071.md`; the status flip and the part-7b `## Latest Review` entry never landed (F4) |
| 11 | Code-segment probe of the documented non-interactive path | `test-evidence/review-code-probes.txt` (this run) | Yes — the documented step 4 cannot run as written on this repository (F1) |
| 12 | Review stage (this run): process segment + code segment, one fixed order | `review.md` (this file), `code-review.md`, `test-evidence/review-code-*.txt` | No, apart from the in-passing repair recorded in F4 |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 1 |
| Automation / Scripts | 2 |
| Workflow | 3 |
| Documentation | 2 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `e57052efa1c16871da4e24a56eabf7402b6fd87e` (`e57052ef`) | the resolved diff base |
| Head commit | `9b45a1b25159c1ff5d92cea8e8e1d3549e8887d5` (`9b45a1b2`) | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code segment reported |
| Renderer mode | `renderer: text` | the code record's header marker (a renderer is installed, stdout is not a TTY, so the two-condition rule selected text mode) |
| Changed / judged / skipped / gap files | 169 / 11 / 158 / 0 | copied field by field from the coverage receipt block |
| Segment verdict | `not-evaluated` | one of the four closed values the `code-review` skill owns |
| Gate verdict | `allow` (exit 0, 0 `blocking`, 5 `important` — every `important` item answered in the record) | the merge-gate verdict source; the refusing literal `blocking-unresolved` was not produced |
| Reason, when one applies | `skipped_files` = 158 > 0, so the segment verdict MUST NOT be `pass` (contracts/coverage-receipt.md C-37); the 158 are the non-code files of the delta, each carrying the legal reason `non-code-file`, and a legal skip earns no coverage credit | mandatory reason for a `not-evaluated` result |
| Uncommitted scope | 5 uncommitted paths were **not** part of the review object and no conclusion is issued over them: `test-evidence/review-code-probes.txt`, `review-code-receipt.txt`, `review-code-start.txt`, `review-context.txt`, `review-prereq.json` — the same sentence is written inside `code-review.md` | disclosed, never concluded over |
| Record | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/code-review.md` | written because the triage value was `run` |
| Archive | `none` | this run's archive path; `none` on a first run |

This subsection carries the verdict and the pointers only: no opinion body, no per-severity item count. The findings themselves live in `code-review.md` and are read there (9 opinions: 5 `important`, 2 `suggestion`, 1 `question`, 1 `praise`).

## 3. Findings (Problems & Improvement Targets)

### F1 — The documented non-interactive step 4 cannot run as written, and its base disagrees with the record header

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `skills/internal/code-review/SKILL.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/SKILL.md`), § 非交互路径（Agent / CI：四步，不是三步）step 4; the underlying resolver is `skills/internal/code-review/scripts/git-delta-review.sh` `cmd_receipt`
- **Evidence** (verbatim quote):

  ```
  4. `receipt --review-file <record>` — 写出覆盖率回执与段裁决；随后用 `report --summary --file <record>` 取合入门禁判决。
  ```

- **Why it's a problem**: `receipt` re-resolves the range itself and takes no `--spec`, so it falls through the feature tier to the trunk tier while `start --spec` wrote the feature tier into the same record's header. Measured on this repository: header `base=e57052ef` (`base_source=feature-first-commit`) versus `receipt` without a range `base=926836e0` (`base_source=trunk-merge-base`). Three consequences, all silent: (a) the documented command exits `2` here, because the wider range contains 24 binary blobs and C-41 refuses to write unmeasurable line counts, so the "completely non-interactive" path stops exactly where an agent needs it; (b) when it does run, the record carries two ranges; (c) the process report copies base/head from the resolved range and the four counts from the block (FR-011), so a reader who recomputes `git diff base..head` from the header gets a different file set than the counts describe. This is the decision-class item the implement stage deliberately left unrepaired, and it needed adjudication rather than a fix: **ruling — the record header is authoritative, so `receipt` must inherit base/head from the record it is given** (justification: C-21 requires that a reader can recompute the range from the header alone; C-74 makes the block the single source of the counts; FR-011 puts both in one subsection — that triple only holds if the two ranges are the same range). Until the script inherits, the documented invocation must carry `--spec <feature-dir>`. **P level: P1** — not P0, because the divergence is visible in the record's own two fields and recomputation exposes it; not P2, because every composed review on an agent-driven host pays it.
- **Proposed fix**: in `cmd_receipt`, read `base`/`head` from the target record's header when they are present and only resolve otherwise; make `SKILL.md` step 4 show the range (`--spec <feature-dir>`) and pin both the header string and the documented line in a contract test so the two cannot drift again.

### F2 — The trunk tier trusts `refs/remotes/origin/HEAD`, which is the upstream fork's tip in this very repository

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `skills/internal/code-review/scripts/git-delta-review.sh` `resolve_trunk` (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh`); the requirement it implements is `requirements.md` FR-004
- **Evidence** (verbatim quote):

  ```
      if git_has_ref refs/remotes/origin/HEAD; then
          printf '%s' "refs/remotes/origin/HEAD"; return 0
      fi
  ```

- **Why it's a problem**: FR-004's closed trunk order is 显式 `--trunk` > 可解析的 `refs/remotes/origin/HEAD` > `main` > `master` > `not-evaluated`, and FR-004 forbids guessing outside it. On this repository `origin` is `git@github.com:github/spec-kit.git` — the UPSTREAM project — while the work lives on three differently-named remotes. `refs/remotes/origin/HEAD` therefore resolves to `926836e0`, an upstream merge commit **1180 commits and 4399 files behind** `HEAD`. The process skill's own §1 warns about exactly this fork trap ("In a fork, `origin` is often the UPSTREAM project"), so the same repository carries the warning and the defect in two different files. A tier that is "closed" but picks a remote the work does not live on is not a deterministic tier; it is a guess with a rule-shaped justification.
- **Proposed fix**: resolve the trunk from the remote that actually contains `HEAD` (`git branch -r --contains HEAD`, first match), and only then from the local default branch; or require `--trunk` whenever no local default branch exists. Amend FR-004's second tier in the same change, and add a contract test over a fixture repository whose `origin` is a decoy remote.

### F3 — A complete code review of a docs-bearing slice is recorded `not-evaluated` forever

- **Severity**: P1
- **Category**: Workflow
- **Location**: `requirements.md` FR-014 (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/requirements.md`); implemented by `contracts/coverage-receipt.md` C-33 / C-37
- **Evidence** (verbatim quote):

  ```
  跳过计数大于 0 时段裁决 MUST NOT 为 [[STR-006]]，只能为 [[STR-007]]（当前记录含 `blocking` 条目时）或 [[STR-002]]（其余情形）。
  ```

- **Why it's a problem**: measured on this feature, the honest run judges 11 code paths and carries 158 non-code files as legal `non-code-file` skips, which yields `skipped_files=158` and therefore `not-evaluated` — even though every code path in the delta was read. The rule was written for focus-driven partial review (C-37's stated case), and it is correct there; applied to "this file is not code", it fuses two different facts into one verdict. The consequence inverts the feature's own purpose: `pass` becomes reachable only by claiming the 158 markdown/JSON files as `reviewed` — the misrepresentation FR-015 exists to forbid — and the framework's normal feature shape (code + docs) can never produce a passing code segment. The verdict stops discriminating between "reviewed nothing" and "reviewed everything that was code".
- **Proposed fix**: amend FR-014 and C-33 so the receipt's file set may be the code-path subset with the non-code remainder disclosed as a separate count that does not void a pass (keep the gap semantics unchanged), or add a third per-file verdict value (`not-code`) that neither earns nor voids coverage. Whichever is chosen, keep C-74's single-source rule: the report and the feature detail keep copying one block.

### F4 — The implement stage closed without its status flip and without its `## Latest Review` entry, and nothing noticed

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/memory/features.md` row 071 and `.specify/memory/features/071.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/memory/features/071.md`); the rule is `templates/feature-details-template.md` § Canonical Status State Machine
- **Evidence** (verbatim quote):

  ```
  **Status**: Planned
  ```

  and, in the same file, `当前：`Planned`（requirements、plan 与 tasks 均已完成…）` — while `tasks.md` carries `**DoD Status**: met at part 7b` and all 36 rows `[X]`.

- **Why it's a problem**: the state machine's row is `| Planned | Implemented | \`/speckit.implement\` |`, and the implement stage satisfied its DoD (zero `[ ]`, zero `[~]`, one `verification.md` row per SC) — but the part-7b commit `9b45a1b2` touches `verification.md`, `tasks.md` and `notes/` only. Two carriers were therefore left stale by the stage that owned them, and nothing detected it: no gate, test or script reads the live status value, so the omission survived the implement closure, the T035/T036 sweeps and the DoD self-assessment. It is the same failure class as the missing part-7a evidence row (F6) — a bookkeeping duty with no reader — and it lands on the next stage's desk: `/speckit.review` judges `Implemented → Ready for Review`, and the state it was handed was `Planned`. **In-passing repair, disclosed**: this run recorded the implement closure (`Planned → Implemented`, with its own `## Latest Review` entry naming `9b45a1b2` and the two `partial` criteria) before judging the review gate, because the recorded intent has exactly one reading — the transition is mandatory once the DoD is met — and leaving the chain `Planned → Ready for Review` would skip a legal row. The finding stays open: the check that would have caught it does not exist.
- **Proposed fix**: add a deterministic status-consistency check (features.md status vs `tasks.md` open rows vs `verification.md` SC rows vs the newest review record) and call it from the implement stage's closure step; make the implement command's E3 record carry the status flip, so the two cannot be written by different parts of the same stage.

### F5 — quickstart F's skip selector matches nothing in this repository

- **Severity**: P2
- **Category**: Documentation
- **Location**: `quickstart.md` § Scenario F (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/quickstart.md`)
- **Evidence** (verbatim quote):

  ```bash
  bash skills/internal/code-review/scripts/git-delta-review.sh receipt \
    --review-file .specify/specs/071-review-code-integration/code-review.md \
    --skip-with-reason "src/legacy/**" --reason size-guard-focus-not-reviewed
  ```

- **Why it's a problem**: this repository has no `src/legacy/` — it is a Python + markdown framework — so the literal command selects nothing, reports `skipped_files=0`, and returns `verdict=pass`, which is the opposite of the scenario's stated expectation (`skipped_files > 0`, verdict not `pass`). The scenario is correct in form and unusable as written; the implement stage had to substitute a repository-shaped selector to demonstrate the behaviour it documents. A quickstart whose literal command cannot be pasted is a fixture-value defect, and it is the second one in this feature (the receipt command lines' missing range is F1).
- **Proposed fix**: use a selector that exists here (`docs/**` was the substitute that worked) and add a one-line rule to the quickstart template: every literal selector must be validated against the repository at write time.

### F6 — A stage-status store with a missing row and no reader

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `test-evidence/implement-stage-status.jsonl` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/test-evidence/implement-stage-status.jsonl`)
- **Evidence** (verbatim quote):

  ```
  {"stage":"implement","substage":"part7b-polish-closure",...}
  ```

  Rows exist for `part1-setup-foundational`, `part2-us1-composition`, `part3-us2-code-segment-core`, `part4-us3-coverage-receipt`, `part5-us4-status-gate-ownership`, `part6-us5-feedback-boundary` and `part7b-polish-closure` — seven rows for eight parts. `part7a` has none.

- **Why it's a problem**: the file is append-only, one row per implement part, and no gate, test or script reads it, so a missing row is indistinguishable from a part that did not run until someone counts. The implement stage disclosed the gap honestly and declined to back-fill it (a back-filled row would record a run that part did not perform) — the right call, and also the point: an unread store accumulates exactly this kind of silent hole. It is worth deciding whether the file is evidence or ceremony.
- **Proposed fix**: either give the store a reader (a closure check that asserts one row per part, or that reads `substage` values against `tasks.md`'s part grouping) or retire it and let `tasks.md` plus git carry the same fact.

### F7 — SC-001 cannot be satisfied by the stage that owns its evaluation

- **Severity**: P2
- **Category**: Workflow
- **Location**: `requirements.md` SC-001 (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/requirements.md`)
- **Evidence** (verbatim quote):

  ```
  **SC-001**: 在一个有已提交代码 delta 的特性上运行一次 `/speckit.review`，同一份过程报告内可同时读到过程段按严重度的计数与代码段裁决与回执计数…
  ```

- **Why it's a problem**: the criterion's subject is a `/speckit.review` run, so the implement stage — which must record a status for every SC before it may flip to `Implemented` — can never do better than `partial`, and it correctly wrote `partial` with the missing half named. That is honest, and it also means the verification log's vocabulary is being used to encode "not my stage", which no reader can distinguish from "not done". A criterion authored for a later stage should say so, or be split; otherwise every feature whose SCs name a downstream flow carries permanent partials and the log loses its ability to flag real shortfalls.
- **Proposed fix**: split SC-001 into (a) a deterministic two-carrier equality the implement stage can assert and (b) the composed-run observation, and mark (b) with the stage that owns it; add the same "evaluable by which stage" column to the verification-log template.

### F8 — The size-guard thresholds exist twice, once as prose

- **Severity**: P2
- **Category**: Documentation
- **Location**: `skills/internal/code-review/SKILL.md` Phase 1 step 1 and `skills/internal/code-review/scripts/git-delta-review.sh` `size_guard`
- **Evidence** (verbatim quote):

  ```
  1. **粒度守门**：运行 `${SKILL_HOME}/scripts/git-delta-review.sh diff --stat`。脚本内置 size guard——变更 >400 行警告拆分，>800 行强烈警告。
  ```

  against the script's `if [[ "$lines" -gt 800 ]]` / `elif [[ "$lines" -gt 400 ]]`.

- **Why it's a problem**: code is the owner of a threshold it enforces, and the skill body restates both literals. Nothing makes them drift *today*; nothing prevents it either, and a reader who edits one has no signal to edit the other. This is the smallest instance of the class the framework's own One Source Of Truth discipline names — a fact with two homes where a pointer would do.
- **Proposed fix**: keep the numbers in `size_guard` and have `SKILL.md` say the script owns them and cites the subcommand; the same treatment for any other numeric literal the skill body repeats from the script.

## 4. What Worked — Preserve (Brief)

- **Analyze gate → one authorized repair round → clause ids preserved, the single new obligation appended as C-74 rather than inserted.** The renumbering discipline is what let three stages repair the same spec without invalidating 73 `[green:]` claims.
- **Red-first evidence per contract group, with four fields each (command line, real output, exit code, failure count).** 24/24 fields present across six groups; a group that could not go red was a reportable finding, not a footnote.
- **Evidence binding by hash**: `verification.md` refuses a `pass` that is not bound to an existing, non-empty artifact whose SHA-256 matches (`verification-evidence-binding.txt`, 5/5 OK).
- **Honest partials**: SC-001 and SC-006 record `partial` with the missing half named rather than being rounded up — SC-001's composed-run half belongs to the review stage (F7), and SC-006's full-suite name diff is the driver's closure slot, which the implement stage's test budget excluded on purpose; both remainders name an owner instead of hiding behind a `pass`.
- **One banner entity for the code segment.** Nine subcommands (`base`/`triage`/`start`/`note`/`receipt`/`report`/`diff`/`review` plus `--help`) live in one existing script — no new engine, no resident process, no network path.
- **The two-condition renderer rule, demonstrated live in this run**: a renderer is installed and stdout is not a TTY, and the record is marked `renderer: text` — the rule is about the ability to render *and* a terminal, not about binary presence.
- **The throwaway-repo harness** (`tests/fixtures/review_git_repo.py`): framework-root write refusal, empty `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM`, inherited `GIT_*` stripped, `DELTA_BIN` defaulting to a non-existent path, three delta shapes from one state. This is what keeps the applicability and receipt assertions from passing on host luck.
- **The receipt block as a parsed grammar** rather than prose: the contract test reads it with a real parser (`parse_receipt`), so a drift in the closed name set or the counting identity goes red mechanically.

## 5. spec-kit / SDD Improvement Recommendations

### 5.3 Automation / Script Improvements

- **REC-071-01 — `receipt` inherits its range from the record it is given** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (`cmd_receipt`) and `skills/internal/code-review/SKILL.md` step 4 (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/`). Change: read `base`/`head` from the record header when present, resolve only otherwise; document the composed step as `receipt --review-file <record> --spec <feature-dir>` until then; pin the documented line and the header string in one contract test. Source: F1. Expected impact: the non-interactive path runs as written on any repository, and a record can no longer carry two ranges.
- **REC-071-02 — resolve the trunk from the remote that holds `HEAD`** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (`resolve_trunk`) plus `requirements.md` FR-004's second tier. Change: prefer the first remote whose `--contains HEAD` is non-empty (or the local default branch) over a blind `refs/remotes/origin/HEAD`; add a contract test over a fixture repository with a decoy `origin`. Source: F2. Expected impact: the base tier becomes deterministic on fork-shaped repositories, which is the framework's own shape.
- **REC-071-04 — give `implement-stage-status.jsonl` a reader or retire it** — Target: `templates/commands/implement.md` (the E3 record discipline) and a closure check under `scripts/python/`. Change: assert one row per part, or drop the store. Source: F6. Expected impact: a missing row fails a check instead of waiting for a human to count.

### 5.4 Workflow Improvements

- **REC-071-05 — separate "not code" from "not reviewed" in the coverage receipt** — Target: `requirements.md` FR-014 and `contracts/coverage-receipt.md` C-33/C-37 (owner texts; the feature's copies are under `.specify/specs/071-review-code-integration/`). Change: allow the receipt's file set to be the code-path subset with the non-code remainder disclosed as its own count, or add a `not-code` per-file verdict that neither earns nor voids coverage; keep C-74's single-source rule intact. Source: F3. Expected impact: a complete review of a code + docs feature can be reported as a pass, and the shortest route to `pass` stops being a false claim.
- **REC-071-03 — a status-consistency check at stage closure** — Target: `scripts/python/` (new check) called from `templates/commands/implement.md`. Change: compare `features.md` status against `tasks.md` open rows, `verification.md` SC rows and the newest review record; fail closed. Source: F4. Expected impact: a stage can no longer close with its own two carriers stale, which is what happened here.
- **REC-071-06 — make each success criterion name the stage that evaluates it** — Target: `requirements.md` SC-001 and the verification-log template's SC row shape. Change: split SC-001 into an implement-evaluable half and a composed-run half; add an "evaluated by" field. Source: F7. Expected impact: `partial` stops encoding "not my stage", so a real shortfall stays visible.

### 5.5 Documentation Improvements

- **REC-071-07 — quickstart selectors must be repository-shaped** — Target: `quickstart.md` § Scenario F (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/071-review-code-integration/quickstart.md`) plus a one-line rule where quickstarts are authored. Change: replace `src/legacy/**` with a selector that exists here (`docs/**`), and require every literal selector to be validated at write time. Source: F5. Expected impact: the literal command demonstrates the documented behaviour instead of the opposite.
- **REC-071-08 — the skill cites the script for the size-guard thresholds** — Target: `skills/internal/code-review/SKILL.md` Phase 1 step 1. Change: drop the `>400` / `>800` literals and point at `git-delta-review.sh diff --stat`. Source: F8. Expected impact: one home for a threshold the code enforces, and no silent drift.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | `receipt` inherits its range from the record | `skills/internal/code-review/scripts/git-delta-review.sh` + `SKILL.md` | F1 |
| P1 | Trunk tier resolves from the remote that holds `HEAD` | `resolve_trunk` + `requirements.md` FR-004 | F2 |
| P1 | Separate "not code" from "not reviewed" | `requirements.md` FR-014 + `contracts/coverage-receipt.md` | F3 |
| P1 | Status-consistency check at stage closure | `scripts/python/` + `templates/commands/implement.md` | F4 |
| P2 | A reader for the stage-status store, or retire it | `templates/commands/implement.md` + `scripts/python/` | F6 |
| P2 | Each SC names its evaluating stage | `requirements.md` SC-001 + verification-log template | F7 |
| P2 | Repository-shaped quickstart selectors | `quickstart.md` § Scenario F | F5 |
| P2 | Skill cites the script for the thresholds | `skills/internal/code-review/SKILL.md` | F8 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target needed an `external` marking.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

Also stated explicitly, because it is a condition of this run rather than a property of the report: the same-author detection gate at the skill's step 4 **did not fire** — the artifacts under review were written by a different agent in a different session, so no detection had to be delegated to fresh-context subagents. Had a P0 been raised, this run could not have delegated its validation (the executing agent has no subagent dispatch capability) and would have had to substitute a direct evidence re-read marked as such.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
