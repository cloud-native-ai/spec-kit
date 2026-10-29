# Specification-Driven Development (SDD) Process Review Report: 076 决策反题与反指标契约（Decision Tension Record）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command
> prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents.
> If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 076 |
| Requirement Key | `076-decision-tension-contract` |
| Requirement Name | 决策反题与反指标契约（Decision Tension Record） |
| Related Feature | 076 决策反题与反指标契约（Decision Tension Record） |
| Repository | spec-kit |
| Repository URL | `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (single remote, named `gitlab`, SSH only — `git remote -v`) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` returns empty (the whole branch is unpushed). Cite absolute paths plus `git show <sha>:<path>`; no `blob/` URL can resolve, and the only remote is SSH, so no web rendering exists either |
| Branch | `076-decision-tension-contract` |
| Commit SHA | `0bddad68d87a1a5c88cf927d1fdfedbeb29daf40` (short: `0bddad68`) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-29 |
| Reviewer (Agent) | Qiming, Liu |
| Environment | macOS (darwin, arm64), bash; `python3` 3.9.6 (system) and `/Users/liuqiming.lqm/project/profiles/.venv/bin/python` (pytest 9.1.1 — the repo `.venv` has no pytest); `git 2.54.0`; `git-delta` **absent** → code segment ran `renderer: text`; `CWS_LIB_BASH_HOME` unset by default (see F12) |
| spec-kit Source Snapshot | this repository at `0bddad68` (the framework source tree and the `.specify/` runtime tree are the same checkout) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 286 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/requirements.md` | 26 FR / 8 SC / 5 user stories / 4 shared strings, plus a six-ruling Clarifications section |
| plan.md | 275 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/plan.md` | Constitution Check, the feature's own two-record `## Decision Tensions` pilot, project structure |
| research.md | 244 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/research.md` | R-1…R-11 decisions with rejected alternatives |
| data-model.md | 181 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/data-model.md` | E1–E8 entities, R1–R6 validation rules, six state migrations |
| contracts/ (8 files) | 240 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/contracts/` | 34 clauses across owner / anchor / measurement / channel / quartet / ADR / validator / mirrors |
| tasks.md | 350 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/tasks.md` | 27 tasks, 9 DoD rows, 7 gates, measured premises, clause partition |
| quickstart.md | 139 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/quickstart.md` | S1–S5 executable scenarios |
| verification.md | 120 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/verification.md` | Baseline + 8 sha256-bound evidence rows + 8 SC blocks |
| feature-ref.md | 65 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/feature-ref.md` | Delivery-surface reference for Task 4's `Related Files` |
| checklists/readiness-2026-10-29.md | 186 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/checklists/readiness-2026-10-29.md` | 37 readiness items: 27 pass / 10 fail |
| checklists/requirements.md | 44 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/checklists/requirements.md` | Requirements-quality checklist (earlier stage, kept as history) |
| notes/red-first-evidence.md + notes/* | 4 files | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/notes/` | Four-field red-first log, pre-change measurements, quickstart run log, SC-002/SC-003 snapshots |
| test-evidence/ (60 files) | — | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/test-evidence/` | One archived output per gate run, per red-first run and per guard mutation |
| code-review.md | — | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/code-review.md` | Code segment record (this run) |
| review-probes.txt | 123 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/test-evidence/review-probes.txt` | The four read-only probes that back F1/F2/F3 and the code segment's column-0 quartet finding |

A fifth stage artifact — `review.md`, this document — is written by the review stage itself.

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Feature registered, then `requirements` run and committed in three passes | `ac63fe8c` (registration) → `da7256e1` → `1b426e1a` → `0518c7ef` | Yes — the feature was bound to its Feature at requirements time instead of at `clarify` (declared as Assumption A4 in `requirements.md:43`); the scaffold's branch action was suppressed by invoking `create-new-requirements.sh` from outside the repo (Assumption A1, `requirements.md:40`) |
| 2 | `clarify` — six rulings, no user in the loop | `2c208998`, `80d26698`; `requirements.md:272-287` | Yes — unattended run: the agent ruled on all six points and recorded candidate readings, cost and rejected alternative per ruling. Detection marked `(detected: direct read, subagent unavailable)` |
| 3 | `plan` | `246eba85`; `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md` | Yes — `create-new-plan.sh` exited 1 on `CWS_LIB_BASH_HOME` unset, so the plan was filled in place (recorded in `.specify/memory/features/076.md` § Last Updated (plan)) |
| 4 | `tasks` | `920e0f8d`; `tasks.md`, `coverage-baseline.txt` | No, but note: zero `[P]` rows, argued as a measurement ("all test rows append to one red-first log") — `tasks.md:303` |
| 5 | `checklist` — readiness audit, 27 pass / 10 fail | `cde66c0b`; `checklists/readiness-2026-10-29.md` | No |
| 6 | `analyze` #1 → 4 HIGH ⇒ implement blocked | no artifact; recorded only in `.specify/state/076-decision-tension-contract.md` § analyze #1 | **Yes** — the four HIGH findings were ruled on by `objective-analysis-gate.md` rule 7 ("direct-read") because the validation subagent wave failed on `qodercli` SDK auth; no analyze report file exists (F11) |
| 7 | `analyze` #1 remediation (16 findings) | `16a44ea0` | No |
| 8 | `analyze` #2 → 0 CRITICAL / 0 HIGH, 4 MEDIUM / 3 LOW | no artifact; state spine § analyze #2 | Yes — same no-report condition |
| 9 | `analyze` #2 remediation (7 findings) | `8a5f7aea` | No |
| 10 | `analyze` #3 → 0 CRITICAL / 0 HIGH, 1 MEDIUM / 4 LOW | no artifact; state spine § analyze #3 | Yes — same no-report condition |
| 11 | Micro-remediation (5 findings) | `d4479500` | No |
| 12 | `implement` full-suite baseline: 6514 passed / 39 failed / 7 skipped | `75216750`; `verification.md:9-11` | No — the 39 failures are pre-existing and were neither fixed nor masked, as required by the stage brief |
| 13 | Implement P1 (T001–T007) incl. an adjudicated anomaly | `c69dbb81`; `test-evidence/anomaly-c11b-guideline-pointer.txt` | **Yes** — adding `shared/guidelines/decision-tension.md` tripped Feature 051's complement assertion; the adjudication added an instruction-surface pointer rather than editing 051's contract, and classified the `templates/instructions-template.md` edit as `PLAN-EDIT: substantive` |
| 14 | Implement P2 (T008–T013) | `b99b3670`, `4c532433` | No |
| 15 | Implement P3 (T014–T020) | `3c1a288c` | No |
| 16 | Implement P4 (T021–T027) + status flip | `84de4ddf`, `7d3ebb58` | **Yes** — T027's and DoD-8's "status stays `Planned`" contradicted the state-machine owner; the contradictory sentence was ruled void and annotated in place at three sites (F9) |
| 17 | Implement wrap-up (records, feedback, state spine) | `0bddad68` | No |
| 18 | Review (this run) — process segment, then code segment | this report + `code-review.md` + `test-evidence/review-probes.txt` | No — the order and the two-file output follow `templates/commands/review.md` |

Workflow shapes worth recording, because they shaped the findings: the whole lifecycle ran
unattended, so every "ask the user" surface became an agent ruling recorded as an Assumption; the
subagent layer was unavailable at two separate moments (step 2 detection, step 6 validation), so two
of the framework's independent-evidence mechanisms degraded to direct read in the same feature.

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 5 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 6 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 |
| Command Prompt | 1 |
| Automation / Scripts | 2 |
| Workflow | 4 |
| Documentation | 3 |

**P0 validation status**: F1 is this report's only P0. No subagent dispatch surface existed in this
run's tool set, so the P0 finding was validated by the documented fallback — a direct bounded re-read
of the same lines plus a fresh executable probe written to
`test-evidence/review-probes.txt` § P-1 — and carries the marker
`(validated: direct re-read, subagent unavailable)`. One P0 reached validation, zero were downgraded,
zero rejected.

**Same-author condition**: **did not hold.** The artifacts under review were produced by an earlier
session's driver and its stage subagents (run id `r20261029T172918Z-076a`); this review is a fresh
context. Detection therefore ran as a single direct pass, which is the independent path the gate
exists to obtain — and the gate rule 6 report is vacuous here rather than favourable: there is no
downgrade rate to report because there was no delegated detection wave to downgrade.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `ac63fe8c474357b4230b1f8a7ac2408f6cc12b2d` | the resolved diff base |
| Head commit | `0bddad68d87a1a5c88cf927d1fdfedbeb29daf40` | the run-start `HEAD`, fixed for the run |
| Base source | `explicit` (the explicit SHAs this run passed are the pair the script's own `feature-first-commit` tier resolves; both statements are true of the same range) | `git-delta-review.sh baseline/triage`, recorded receipt |
| Renderer mode | `renderer: text` | `git-delta` is absent on this host (`which delta` → rc=1); the skill's fallback path was used, no installer was run |
| Changed / judged / skipped / gap files | 135 / 12 / 123 / 0 | copied from the record's `<!-- coverage-receipt -->` block, never recomputed |
| Segment verdict | `blocked` | the record's receipt block |
| Gate verdict | `blocking-unresolved` | `report --summary --file code-review.md` → exit 1, `gate=deny`, `blocking_entries=1` |
| Reason, when one applies | one `blocking` entry (owner omits the grammar its own validator enforces); five `important` entries remain unanswered | record body |
| Uncommitted scope | none at review start — `git status --short` was empty; the two report files and the probe file are this run's own output, not code | measured before the run |
| Record | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/code-review.md` | written (`triage=run`) |
| Archive | `none` | first run of the code segment for this feature |

This subsection carries the verdict and the pointers only: no opinion body, no per-severity item
count. The findings themselves live in the record named above and are read there.

### 2.2 Status Gate — `Implemented → Ready for Review` (judged once, after both segments)

| # | Condition (owner: `templates/feature-details-template.md` § Canonical Status State Machine) | Verdict | Evidence |
|---|-------------------------------------------------------------------------------------------|---------|----------|
| 1 | Every deferred (`[~]`) task is resolved or explicitly waived | **met** | `tasks.md`: 27 `[X]`, 0 `[~]`, 0 `[ ]`; `verification.md` `deferred_tasks=` empty |
| 2 | Review evidence has been produced | **met** | `review.md` (this file) and `code-review.md` both on disk, plus `test-evidence/review-probes.txt` |
| 3 | The current code-segment record contains no `blocking` entry | **NOT met** | `code-review.md`: 1 `blocking` entry, `gate=deny`, `blocking_entries=1` |

**Outcome: the transition is refused — status stays `Implemented`; the named refusal literal is
`blocking-unresolved`.** No user waiver exists (this run is unattended, and a driver's or
orchestrator's confirmation is not a user ruling), so the run halts and reports rather than flipping.
The five `important` entries are recorded and await the author's answer, one by one; none of them
blocks, and none of them was answered in this run because no author turn occurred inside it.

## 3. Findings (Problems & Improvement Targets)

### F1 — The record grammar has no normative home outside a plan-artifact

- **Severity**: P0 *(validated: direct re-read, subagent unavailable)*
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/guidelines/decision-tension.md:12-28`
  (enforcing code: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/validate-decision-tensions.py:126`;
  the grammar's only written form: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/data-model.md:46`)
- **Evidence** (verbatim quote):

  ```
  ## 记录形态：六字段 + 记录标识（封闭集）

  一条记录由封闭的六字段与一个记录标识构成，字段名逐字如下：

  | 字段 | 内容 |
  |------|------|
  | `decision` | 一句话点名被选中的一极 |
  ```

  and, from `templates/plan-template.md:73-74`:

  ```
  Every record is carried by a level-3 sub-section whose heading begins with `T-NNN`
  (e.g. `### T-001 — <one-line title>`), and its six fields are written in the owner's shape.
  ```

- **Why it's a problem**: FR-001 makes this file the owner of "六字段 DTR 的**输出形态**", but the
  owner states field *names and content*, never the line syntax the checker requires
  (`- **<field>**:`, bold name, colon; plus two indented `- pole_a:` / `- pole_b:` lines). A plan
  author who writes exactly what the owner and template describe is rejected. Measured
  (`test-evidence/review-probes.txt` § P-1): exit 1, `dtr-record-incomplete: missing field label(s):
  decision, antithesis, binding_constraints, discriminating_evidence, expected_sacrifice,
  revision_trigger` — a false rejection *and* a wrong diagnosis, since all six were written. The
  grammar survives today only in the plan-owned `data-model.md:32-48`, which belongs to one feature;
  one-source-of-truth forbids a later feature's data-model from restating it, so the grammar has no
  durable surface, and the next spec's author inherits the defect.
- **Proposed fix**: add the line-grammar block to `shared/guidelines/decision-tension.md`
  § 记录形态 (a fenced six-line example plus one sentence on the pole indentation), and make
  `tests/contract/test_decision_tension_contract.py` build one fixture record **from the owner's
  example verbatim** and assert exit 0, so owner and checker cannot drift.

### F2 — The `N/A` rule is fail-open: one flat sentence satisfies four "per-trigger" justifications

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/validate-decision-tensions.py:295-318`
- **Evidence** (verbatim quote, `validate-decision-tensions.py:310-313`):

  ```
  unjustified = [
      trigger for trigger in LOAD_BEARING_TRIGGERS
      if not any(trigger in line and len(line.strip()) - len(trigger) >= 2 for line in block)
  ]
  ```

  Measured (`review-probes.txt` § P-2): a one-line
  `N/A — 不可逆、跨团队、高爆炸半径、与宪法原则相关四类触发均不成立。` returns exit 0 with zero
  findings.
- **Why it's a problem**: the "bare `N/A` is a missing record" rule is the load-bearing half of the
  fail-closed design (FR-011 (a), US4, SC-003): the detector is forbidden to decide whether a
  load-bearing decision exists, so the *shape* of `N/A` carries the whole burden. Both declaring
  documents are stricter than the program —
  `templates/plan-template.md:76-78` says "write the literal `N/A` plus **one line per trigger**
  explaining why that trigger does not hold", and
  `skills/internal/analyze-artifacts/references/detection-and-severity.md:105` says "a bare `N/A`
  carrying no **one-line justification per load-bearing trigger**". The program accepts one line that
  merely names the four triggers, so an author can satisfy the high-severity gate without justifying
  anything.
- **Proposed fix**: require one line per trigger — the trigger's justification must be on a distinct
  line whose non-trigger remainder is a non-trivial sentence — and add the flat-sentence fixture to
  the validator contract suite as an inverse sample.

### F3 — Two of the six validator labels have no defect class, hence no severity, in the analyze channel

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/references/detection-and-severity.md:99-107`
- **Evidence** (verbatim quote):

  ```
  Three defect classes, each **HIGH**. The value domain is HIGH or 0 — there is **no advisory or
  downgrade tier**, and the detector MUST NOT be asked to decide whether the plan holds a
  load-bearing decision: a missing record is judged fail-closed.
  ```

  followed by a three-row table whose label column names only `dtr-section-missing`,
  `dtr-record-incomplete`, `dtr-rejected-form` and `expected-sacrifice-unmapped`.
- **Why it's a problem**: `dtr-anchor` and `dtr-tension-id` are live labels with no row. Measured
  (`review-probes.txt` § P-3): a plan whose section exists but is not the direct successor of
  `## Constitution Check` returns exactly `[dtr-anchor] fail (1)`, exit 1, no other label. A detector
  rendering only the table's classes has nothing to attach that finding to and can report **0 HIGH
  for a plan the program rejects** — the same fail-open shape the channel was created to close, now
  one layer up in the mapping. The channel's own claim of a closed "HIGH or 0" domain is what makes
  this a defect rather than an omission.
- **Proposed fix**: extend the table to all six labels (add "Misplaced section — `dtr-anchor`" and
  "Record identifier malformed, duplicated or skipped — `dtr-tension-id`", both HIGH), and add a
  contract assertion that the table's label column equals the validator's `LABELS` tuple as a set.

### F4 — SC-002 / SC-003 are closed by an artifact the asserting test itself writes

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_decision_tension_contract.py:1025-1053`
- **Evidence** (verbatim quote, the snapshot writer's own docstring):

  ```
  """Archive one SC-003 analyze-channel snapshot; SC-003's HIGH count reads only these files.

  The channel is a declared detection pass, not a program, so the run that produces its report is
  this test: the snapshot carries the program's verdict verbatim (exit code, per-label counts,
  record count) under the channel's four defect classes. Rendering is deterministic, so a re-run
  refreshes it instead of accumulating near-duplicates.
  """
  ```

  against the measurement source it is supposed to satisfy, `requirements.md:245`:

  ```
  - **SC-002 Source**: analyze 报告中的严重度列与条目计数；四类夹具各一次运行的报告快照。
  ```

- **Why it's a problem**: the acceptance criterion asks for an *analyze report*'s severity column;
  what exists is a file written by the test, whose headline `HIGH findings: N` is a sum the test
  computes from the same label counts it then asserts. Evidence and assertion share one author, so
  the claim "the analyze channel reports 1 HIGH" was never observed through `/speckit.analyze` at
  all — the narrative layer, which is the only thing that turns a label into a HIGH finding, was
  never executed. The implement stage disclosed this honestly (`verification.md:87`: "the
  `/speckit.analyze` narrative layer was not produced by a full skill run and no SC depends on it"),
  but disclosure does not restore the missing observation; "no SC depends on it" is true only because
  the SC's own evidence was redefined to something the test can produce.
- **Proposed fix**: make the channel's severity mapping a program — a `--channel-report` mode on
  `validate-decision-tensions.py` that emits findings with class and severity — and have the test
  assert that output. The snapshot then records a program's verdict instead of a template the test
  fills in.

### F5 — Ten checklist failures never get a closure record

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/checklists/readiness-2026-10-29.md` (summary table and ten `[ ]` rows)
- **Evidence** (verbatim quote, the checklist's own summary):

  ```
  | Verdict | Count |
  |---------|-------|
  | pass | 27 |
  | fail | 10 |
  | total | 37 |
  ```

  and one of the ten, CHK004: `- [ ] CHK004 [Clarity, Measurability] Is a decidable judge named for
  the semantic admissibility and rejection criteria … — **fail** … — **Handoff**: `/speckit.plan`.`
- **Why it's a problem**: the checklist stage gate is "清单文件落盘 + 记账", which was satisfied — and
  then the ten gaps were inherited by tasks and fixed inside `/speckit.analyze`'s remediation rounds.
  Nothing records that. `grep -c 'CHK0'` over `tasks.md` and `contracts/*.md` returns **0**, so no
  task, contract or artifact claims any of the ten; the only mapping from a CHK id to a closing task
  is prose in `.specify/state/076-decision-tension-contract.md`. A checklist whose fail rows are
  never dispositioned cannot be read as an audit: the next reader sees ten open gaps beside a feature
  that shipped, and has no way to tell "closed" from "ignored".
- **Proposed fix**: give the checklist file a disposition column (or a handoff section) whose rows
  the artifact that closes a gap must fill — `/speckit.analyze` and `/speckit.implement` should cite
  the CHK id they close, and the checklist stage gate should require `fail` rows to be addressed or
  explicitly deferred, not merely counted.

### F6 — A pointer assertion that resolves from the authoring file's own directory cannot see its consumer

- **Severity**: P1
- **Category**: Template
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/plan-template.md:65`
  (assertion: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_decision_tension_contract.py:351`)
- **Evidence** (verbatim quote, template line 65):

  ```
  threshold: [`shared/guidelines/decision-tension.md`](../shared/guidelines/decision-tension.md).
  ```

  and the assertion that guards it:

  ```
          target = (TEMPLATE.parent / link.group(1)).resolve()
  ```

- **Why it's a problem**: `../shared/...` is correct relative to `templates/` and to the mirror
  `.specify/templates/`, but the artifact that will actually carry this section is an instantiated
  `plan.md` under `.specify/specs/<key>/`, where the same link resolves to
  `.specify/specs/shared/guidelines/decision-tension.md` — a path that does not exist. The test
  resolves from `TEMPLATE.parent`, the single base at which the defect cannot appear, so FR-009's
  "指针路径可解析" is a guarded assertion that cannot go red for its subject. This is the framework
  pattern to fix, not just the literal: a template's pointers are authored for its *consumer's*
  directory, and a test that resolves them from the template's directory silently blesses a dead
  link in every instantiated plan.
- **Proposed fix**: in `templates/plan-template.md` use the repo-root form the rest of the template
  already uses (`` `.specify/shared/guidelines/decision-tension.md` ``, cf. lines 5 and 37), and in
  the contract test resolve the pointer from a fixture instantiated under
  `.specify/specs/<fixture-key>/plan.md` rather than from `TEMPLATE.parent`.

### F7 — `post_change_commit=` cannot be filled by the run that writes the log

- **Severity**: P2
- **Category**: Template
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/templates/verification-log-template.md:38`
  (what the run wrote: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/verification.md:17-22`)
- **Evidence** (verbatim quote, template):

  ```
  implementation_date=[YYYY-MM-DD]
  post_change_commit=[GIT_SHA_AT_RUN_END]
  ```

  and what the implement stage actually wrote, with its reason:

  ```
  # Tree this segment (part 4/4) builds on: the P3 commit. This segment's own commit hash is reported
  # in the implement wrap-up report; verification.md is written before that commit exists, so no
  # self-referential hash is invented here.
  segment_base_commit=3c1a288c
  post_change_commit=3c1a288c
  ```

- **Why it's a problem**: `GIT_SHA_AT_RUN_END` does not exist when the log is written — the log is
  part of the end state whose SHA it is supposed to name. Every run meets the same contradiction, so
  the field either gets a wrong SHA or gets hand-reasoned around; this run chose the latter, honestly
  and at the cost of a field whose name no longer means what the template says. A field that cannot
  be filled invites a fabricated value in a less careful run.
- **Proposed fix**: replace the key with `post_change_tree=` plus a `post_change_commit_pointer=`
  that names the wrap-up report and the branch, or have a wrap-up step rewrite the field after the
  commit exists (the same step already knows the SHA).

### F8 — The feature detail's `## Latest Review` carrier was stale for the whole feature

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features/076.md:29-31`
- **Evidence** (verbatim quote):

  ```
  ## Latest Review

  尚无。立项日 2026-10-29，等待 `/speckit.requirements` 起跑。
  ```

- **Why it's a problem**: `templates/feature-details-template.md` § Canonical Status State Machine
  names this entry as one of the two verifiable carriers for the review conclusions, and the tasks
  file gives T027 "Feature 集成复核" the job of updating the detail. Eight stages later the section
  still says the requirements stage has not started, so the carrier that a reader would consult for
  "what did the last review say" answers with a pre-history placeholder. The rest of the detail file
  was updated diligently (five `Last Updated (…)` blocks), which makes the staleness *look* like a
  content choice rather than an omission.
- **Proposed fix**: give the section an owner in the stage that writes it (the review stage already
  writes it) and have `/speckit.feature`'s reconcile treat a placeholder left standing past
  `implement` as drift; at minimum, delete the "等待 … 起跑" sentence at registration time so the
  section never claims a state that has passed.

### F9 — Three artifacts copied a status-machine fact and all three copied it wrong

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/tasks.md:6,25,269`
- **Evidence** (verbatim quote, tasks.md line 6, the header the tasks command generated):

  ```
  **Related Feature**: Feature 076 — 决策反题与反指标契约（Decision Tension Record）, status `Planned`（tasks 阶段不推进状态机；`Implemented` 属 `/speckit.implement`）
  ```

  against DoD-8 in the same file: `Feature 076 状态保持 `Planned`。` — and against the owner row
  (`templates/feature-details-template.md` § Canonical Status State Machine): `| Planned |
  Implemented | /speckit.implement |`.
- **Why it's a problem**: line 6 quotes the owner correctly, DoD-8 and T027 restate it incorrectly,
  and the contradiction survived tasks, checklist and three analyze rounds to be discovered by the
  last task of the implement run. The cost is not the one-line fix; it is that a self-contradicting
  DoD is a DoD nobody can satisfy, so the honesty of the whole gate set became a judgement call at
  the moment of the status flip. The root is the tasks template asking the planner to write the
  feature's current status into a task file at all — a fact with an owner, restated at a second site.
- **Proposed fix**: in `templates/tasks-template.md`, drop the "status `X`" clause from the
  Related-Feature line and require a pointer (`status: see `.specify/memory/features.md``), and stop
  emitting DoD rows about status transitions — the state machine owns them.

### F10 — An SC's own count does not match its measurement source, and survived three analyze rounds

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/requirements.md:233` (SC-001) versus `:244` (its measurement source)
- **Evidence** (verbatim quote, SC-001):

  ```
  - **SC-001**: 在含 1 条承重决策的夹具计划上，[[STR-001]] 章节存在、该记录六字段齐备且 `tension_id`
    唯一按序，确定性校验器返回 0；六个反向输入（删去任一字段——六字段逐一各跑一次、置
    `expected_sacrifice: none`（[[STR-002]]）、写入不可判定措辞、重复 `tension_id`、`tension_id`
    跳号、`expected_sacrifice` 指向不存在的测量来源）各返回 1。
  ```

  and its measurement source:

  ```
  - **SC-001 Source**: … 十二次运行（1 合规 + 删除一类按六字段逐一各一次 + 其余五个反向输入各一次）
  ```

- **Why it's a problem**: "六个反向输入" is followed by a parenthetical that enumerates 6 + 5 = 11,
  and the measurement source says 12 runs. The two numbers can be reconciled only by reading "六个"
  as "six *classes*, one of which expands to six runs" — a reading nothing states. A criterion whose
  count has to be interpreted is a criterion whose pass cannot be checked by counting, and this one
  went through three analyze rounds and a readiness audit unchanged because each half is plausible
  in isolation.
- **Proposed fix**: state the count in one place only (the measurement source) and have the SC text
  cite it, or write SC-001 as "every inverse input returns 1" without a cardinal — a count restated
  in prose is exactly the second definition point the framework forbids elsewhere.

### F11 — `/speckit.analyze` leaves no artifact, so its verdicts are unreviewable afterwards

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.qoder/commands/speckit.analyze.md:40`
- **Evidence** (verbatim quote):

  ```
  A read-only run that produced no artifact skips this step and says so in one line rather than
  creating an empty commit.
  ```

  Observed consequence: three analyze runs (4 HIGH → blocked; then 0 HIGH twice) exist only as prose
  in `.specify/state/076-decision-tension-contract.md`; `ls .specify/specs/076-decision-tension-contract/`
  shows no analyze report.
- **Why it's a problem**: analyze is the stage that decides whether implementation may start, and it
  is the only gate whose verdict leaves nothing behind. This review had to accept "4 HIGH closed" and
  "0 CRITICAL / 0 HIGH" on the strength of a narrative in the state spine — the one artifact the
  read-only design deliberately does not commit. Every later reader, and every rerun-delta
  comparison, is in the same position; the "rerun delta when a prior report exists" feature of the
  skill has nothing to compare against when reports are never written.
- **Proposed fix**: specify a durable analyze report path (`.specify/specs/<key>/analyze-<UTC>.md`)
  in the command and skill, and make the wrap-up commit it — a read-only pass over artifacts can
  still write its own report, exactly as this review writes `review.md`.

### F12 — Framework bash scripts hard-require an undeclared environment variable

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/scripts/bash/check-prerequisites.sh` (dependency guard)
- **Evidence** (verbatim output of the command's own declared prerequisite, run first thing this stage):

  ```
  $ bash .specify/scripts/bash/check-prerequisites.sh --json --require-spec --include-spec --include-plan --include-tasks
  Error: CWS_LIB_BASH_HOME environment variable is not set.
  Dependency check failed. Initializing dependencies are required.
  ```

  The same variable stopped `create-new-plan.sh` during the plan stage (`features/076.md` § Last
  Updated (plan): "`create-new-plan.sh` 因 `CWS_LIB_BASH_HOME` 未设置退出 1").
- **Why it's a problem**: two stages of one feature were blocked at their first command by a variable
  that neither `templates/commands/*.md` nor the skills declare as a prerequisite, and that the
  framework never tells you how to set. Recovery is local knowledge (the sibling checkout
  `cloud-native-tools/cws-lib-bash`), so the same feature pays the tax twice and a fresh machine pays
  it at every stage. The gate is real (the scripts genuinely need the library) — the omission is the
  declaration.
- **Proposed fix**: have the guard print the expected value and the resolution rule (one line), add
  `CWS_LIB_BASH_HOME` to the `## Environment Prerequisites` block that commands emit, and let the
  script fall back to a discovery order (env var → `../cws-lib-bash` sibling → exit with the
  instruction) instead of failing on the first check.

## 4. What Worked — Preserve (Brief)

- Red-first log with four mandatory fields per group (`notes/red-first-evidence.md`), and guard
  slices explicitly excluded from red-first claims instead of being dressed as one.
- Closed-set containment claims measured against a **literal** baseline commit (`ac63fe8c`) and
  asserted by delta **equality** — a rewrite shows up as remove + add (scenario G).
- Mirror discipline honoured end to end: seven pairs, byte-identical, produced by `sync-mirrors.py`,
  with `--check` compared against a pre-change baseline rather than against exit 0.
- `verification.md` binds every `pass` to an archived file by sha256; all eight recomputed this run
  and all eight match.
- The feature's own `plan.md` is a real pilot of its own mechanism (two records, six fields, costs
  resolvable to declared measurement sources) — the template change was exercised before it shipped.
- Anomaly adjudication left a written trail instead of a silent patch: Feature 051's complement
  assertion, the instruction-surface pointer, and the status-flip correction each have an evidence
  file or an inline correction note.
- No `[P]` rows, with the reason given as a measurement (single red-first log write point) rather
  than left as an omission.
- 39 pre-existing suite failures neither fixed nor masked; the budget (baseline once, targeted sets
  between, closure after review) was respected — this run added no full-suite invocation.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Add the record grammar to the owner and validate it from the owner's example** — Target:
  `shared/guidelines/decision-tension.md` § 记录形态; `tests/contract/test_decision_tension_contract.py`
  (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/guidelines/decision-tension.md`).
  Change: paste the six-line fenced example (field bullets + the two indented pole lines) into the
  owner, then build one fixture record from that example verbatim and assert exit 0. Source: F1.
  Expected impact: the capability becomes usable from its own documentation, and owner/checker drift
  becomes a red test.
- **Stop emitting status facts and un-fillable keys from templates** — Target:
  `templates/tasks-template.md` (Related-Feature status clause, status DoD rows) and
  `templates/verification-log-template.md` (`post_change_commit=`). Change: point at
  `.specify/memory/features.md` instead of restating the status; replace `GIT_SHA_AT_RUN_END` with a
  post-commit pointer or a wrap-up rewrite step. Source: F9, F7. Expected impact: removes two
  classes of self-contradicting artifact (a DoD nobody can satisfy; a key nobody can fill).
- **Author template pointers for the consumer's directory, and resolve them there** — Target:
  `templates/plan-template.md` + the contract-test pattern that guards pointer resolvability.
  Change: repo-root pointer form, and resolve from a fixture instantiated under
  `.specify/specs/<key>/`. Source: F6. Expected impact: pointer assertions start observing the path a
  real plan will take.

### 5.2 Command Prompt Improvements

- **Give analyze a durable report** — Target: `templates/commands/analyze.md` (+ the skill's report
  format section). Change: name an output path, commit it in the wrap-up, and let rerun deltas
  compare against it. Source: F11, F4. Expected impact: the gate whose verdict starts implementation
  becomes reviewable, and a rerun has something to diff.
- **Close the checklist loop in the stages that follow it** — Target: `templates/commands/analyze.md`
  and `templates/commands/implement.md`. Change: require each CHK id a remediation closes to be cited
  by that artifact. Source: F5. Expected impact: a checklist's fail rows stop being decorative.

### 5.3 Automation / Script Improvements

- **Tighten the `N/A` shape to one justification per trigger** — Target:
  `scripts/python/validate-decision-tensions.py::na_verdict`. Change: one distinct line per trigger
  with a non-trivial remainder; add the flat-sentence fixture as an inverse sample. Source: F2.
  Expected impact: the fail-closed gate stops accepting a sentence that justifies nothing.
- **Make the channel severity a program, not a table a test fills in** — Target:
  `scripts/python/validate-decision-tensions.py` (a `--channel-report` mode) and
  `skills/internal/analyze-artifacts/references/detection-and-severity.md` § I. Change: emit class +
  severity per finding, cover all six labels, and have the SC-002/SC-003 evidence record that output.
  Source: F3, F4. Expected impact: severity mapping is deterministic, drift-guarded, and independently
  observed.
- **Declare and self-heal the bash library dependency** — Target: `.specify/scripts/bash/*.sh`
  dependency guard and the `## Environment Prerequisites` block that commands emit. Change: print the
  expected value plus a discovery order before failing. Source: F12. Expected impact: two blocked
  stage-starts per feature disappear.

### 5.4 Workflow Improvements

- **Keep the feature detail's `## Latest Review` honest from the start** — Target:
  `templates/feature-details-template.md` (`## Latest Review`) + `/speckit.feature`'s reconcile.
  Change: seed it empty of claims, treat a pre-history placeholder left past `implement` as drift.
  Source: F8. Expected impact: one carrier stops answering with a stale sentence.
- **Make "one line per trigger" checkable end to end** — Target: the `N/A` rule's three sites
  (template, channel doc, checker). Change: state it once (owner) and cite it from the other two.
  Source: F2. Expected impact: one rule, one wording, one assertion.

### 5.5 Documentation Improvements

- **Map every validator label to a channel class** — Target:
  `skills/internal/analyze-artifacts/references/detection-and-severity.md` § I. Change: six rows,
  one per label, and pin the label set by importing the checker's `LABELS`. Source: F3. Expected
  impact: no finding can be silently dropped between the program and the detector.
- **State counts once** — Target: `076-decision-tension-contract/requirements.md` SC-001 as the
  example, and the requirements-quality checklist as the guard. Change: cardinal only in the
  measurement source; SC prose cites it. Source: F10. Expected impact: a recount stops being able to
  disagree with itself.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Record grammar into the owner, validated from the owner's example | `shared/guidelines/decision-tension.md` + contract test | F1 |
| P1 | One justification per trigger; flat-sentence inverse sample | `scripts/python/validate-decision-tensions.py` | F2 |
| P1 | Channel table covers all six labels; label set pinned by import | `skills/internal/analyze-artifacts/references/detection-and-severity.md` | F3 |
| P1 | Channel severity emitted by a program; SC-002/SC-003 evidence records it | `validate-decision-tensions.py` + the contract suite | F4, F3 |
| P1 | Checklist fail rows closed by the artifact that closes them | `templates/commands/analyze.md`, `implement.md` | F5 |
| P1 | Pointers authored for the consumer and resolved from it | `templates/plan-template.md` + pointer assertion | F6 |
| P2 | Drop status facts and un-fillable keys from templates | `templates/tasks-template.md`, `verification-log-template.md` | F9, F7 |
| P2 | Durable analyze report | `templates/commands/analyze.md` | F11 |
| P2 | `## Latest Review` never carries a passed-state placeholder | `templates/feature-details-template.md` | F8 |
| P2 | Cardinal stated once | requirements SC-001 / requirements checklist guard | F10 |
| P2 | Declare and self-heal the bash library dependency | `.specify/scripts/bash/*` prerequisites | F12 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a
  parenthetical supplement; no target needed an `external` marking.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without
  opening the source file; F2, F3, F10 and F12 additionally carry the measured output inline, and
  all four executable probes are archived verbatim in `test-evidence/review-probes.txt`.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside
  this document.
- [x] No unfilled placeholder tokens remain. The single bracketed token in the report —
  `[GIT_SHA_AT_RUN_END]` — sits inside F7's verbatim quote of the template row being criticized, and
  is evidence, not an omission.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one
  source finding ID.
- [x] P0 validation status is stated explicitly in §2: one P0, validated by the documented
  subagent-unavailable fallback (direct re-read plus a fresh probe), zero downgraded, zero rejected.
- [x] **Deliberate deviation from the handoff's id family**: this report coins **no `REC-…`
  identifiers**. The stage brief restricts this run's writes to `review.md`, `code-review.md` and the
  stage's own evidence, so a durable identifier coined here could not be registered in
  `.specify/memory/register.md` in the same commit as the ID Register rule requires. Recommendations
  therefore carry self-describing titles and the roadmap's target/source columns for
  cross-referencing; if the driver wants the register rows, they are the eleven roadmap titles above.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

## 9. Disposition (author turn, 2026-10-29)

> Appended by the review-remediation round. §3 is left byte-identical on purpose: a finding is a
> dated observation, and rewriting it would erase what was found. This section records what each
> finding received. Nothing here re-states a verdict — the code segment's gate is re-measured by the
> next review run, not by this note.

### 9.1 Repaired in this round

| Finding | Repair | Where the repair lives |
|---------|--------|------------------------|
| F1 (P0) | The owner now carries the line grammar the validator enforces: one `- **<field>**:` line per field, the two two-space-indented `pole_a` / `pole_b` sub-lines, the `### T-NNN` carrier, and one copy-pasteable complete record. A contract test extracts that example **verbatim** and requires exit 0, so owner and checker cannot drift. | `shared/guidelines/decision-tension.md` § 记录形态 → `### 记录行文法（校验器强制的形态）`; `tests/contract/test_decision_tension_contract.py::test_owner_example_passes_the_validator_verbatim` |
| F2 (P1) | The `N/A` rule is now per trigger: each trigger must own a **distinct line** whose remainder, once the trigger name and punctuation are removed, is still a sentence (≥8 chars); a line naming two or more triggers justifies none. Measured: the flat sentence, a two-trigger line and a two-character remainder all exit 0 under the previous rule and exit 1 now. | `scripts/python/validate-decision-tensions.py::na_verdict` / `_justified_trigger`; inverse samples `test_flat_sentence_na_justifies_no_trigger`, `test_per_trigger_na_needs_one_trigger_and_a_reason_per_line` |
| F3 (P1) | The channel table now covers all six labels — `dtr-anchor` (misplaced section) and `dtr-tension-id` (identifier malformed / duplicated / skipped) each own a class at HIGH. The guard imports the validator's `LABELS` and asserts set equality with the table's label column, so neither a seventh label nor a dropped row can pass. | `skills/internal/analyze-artifacts/references/detection-and-severity.md` § I; `test_defect_classes_fail_closed_no_advisory`, scenario G |
| F4 (P1) | The severity mapping is now a program output, not a table a test fills in: every finding carries `severity=HIGH`, every label carries `HIGH` or `0` (the declared HIGH-or-0 domain), and the aggregate `channel.high` is printed in both the human and `--json` forms. All seven `notes/analyze-sc003/` snapshots are re-rendered from that output and carry a per-label severity column; SC-002/SC-003 read `channel.high`. The disclosure that the `/speckit.analyze` narrative layer was never run end to end is retained. | `validate-decision-tensions.py` (`CHANNEL_VALUE_DOMAIN`, per-check / per-finding severity, `channel` block); `write_analyze_snapshot`; `verification.md` SC-002/SC-003 notes + refreshed sha256 |
| F5 (P1) | A `## Closure` block now maps all ten `fail` rows to their analyze disposition (A-01…A-11 in `16a44ea0`, the carried A-12 plus A-17…A-22 in `8a5f7aea`, A-23…A-27 in `d4479500`), the FR / contract clause / task that closes each, and the assertion that holds it. The original ten rows are untouched. | `checklists/readiness-2026-10-29.md` § Closure |
| F6 (P1) | The template pointer is authored for its consumer: `.specify/shared/guidelines/decision-tension.md`, read from the repository root (the form the rest of the template already uses). The assertion now derives its base from an instantiated plan at `.specify/specs/<key>/plan.md` and asserts the plan-directory-relative form is dead — the base at which the old defect could not appear is no longer used. | `templates/plan-template.md` § Decision Tensions; `test_template_is_pointer_not_copy_and_path_resolves` (`consumer_plan`, `pointer_base`) |

### 9.2 Corrected (fact errors), not repaired as written

- **F9 — tasks.md status sites.** The finding's title ("three artifacts … all three copied it wrong")
  over-counts: `tasks.md:6` quotes the state-machine owner **correctly** (a tasks-stage file does not
  advance the status); DoD-8 and T027 were the two that restated it wrongly, and the implement stage
  already left a dated correction on both (the owner's rule plus the measured flip to `Implemented`).
  What was missing is the third site, added here: line 6 gains a pointer to the live owner
  (`.specify/memory/features.md`) and the same dated trace, because a status fact restated in a task
  file goes stale the moment the stage advances. No task row, count or clause was changed.
  → `tasks.md` lines 6 / DoD-8 / T027.
- **F10 — SC-001's cardinal.** Recounted against the file: the parenthetical enumerates **six
  inverse-input classes**, and the first class ("删去任一字段——六字段逐一各跑一次") expands to six
  runs; 6 + 5 = 11 inverse runs, plus the compliant run = 12, which is exactly what
  `SC-001 Source` states ("十二次运行（1 合规 + 删除一类按六字段逐一各一次 + 其余五个反向输入各
  一次）"). The arithmetic in the finding (6 + 5 = 11 against a stated 12) is the error, not the
  criterion: the two numbers reconcile, and the expansion is stated in the text. `requirements.md`
  is therefore unchanged — the review round's own constraint forbids editing it, and there is
  nothing to correct. What remains valid in F10 is the stylistic advice (a cardinal restated in SC
  prose is a second definition point), which is a requirements-template improvement, not a defect
  in this criterion. → no artifact change; this paragraph is the trace.

### 9.3 Not implemented

Disposition: F7 (P2) accepted-for-roadmap — `templates/verification-log-template.md`'s
`post_change_commit=` cannot be filled by the run that writes the log; replacing it with a
post-commit pointer is a template-wide change outside this feature's scope.
Disposition: F8 (P2) accepted-for-roadmap — `templates/feature-details-template.md`'s
`## Latest Review` placeholder and `/speckit.feature`'s reconcile are framework surfaces.
Disposition: F11 (P2) accepted-for-roadmap — a durable analyze report path belongs to
`templates/commands/analyze.md` and the analyze skill, not to this feature.
Disposition: F12 (P2) deferred — declaring `CWS_LIB_BASH_HOME` and adding a discovery order touches
the first command of every stage; it needs an environment-prerequisite decision (which sibling
layout to probe, and what the guard prints) that this round's scope cannot settle.
