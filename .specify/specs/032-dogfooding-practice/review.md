<!-- Self-contained SDD process review. Audience: spec-kit framework maintainers. -->

# Specification-Driven Development (SDD) Process Review Report: Dogfooding Practice Adoption

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 032 |
| Requirement Key | 032-dogfooding-practice |
| Requirement Name | Dogfooding Practice Adoption |
| Related Feature | 036 Dogfooding Practice |
| Repository | spec-kit |
| Repository URL | https://github.com/github/spec-kit |
| Branch | 032-dogfooding-practice |
| Commit SHA | 35f05219ad65079a95679c4a298731471fcd983f (short: 35f05219) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-07-25 |
| Reviewer (Agent) | AI coding agent (Qoder CLI session) |
| Environment | Linux 5.10.134 (x86_64), bash 4.4.20, Python 3.11.11, pytest via system python3 |
| spec-kit Source Snapshot | https://github.com/github/spec-kit @ specify-cli 0.0.22 (workspace fork, commit 35f05219) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 124 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/requirements.md | Revised spec: two existing loops (A/B) made explicit, FR-004 "no new machinery" red line |
| plan.md | 100 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/plan.md | Revised plan: constitution principle + template section only; Phase 0 inlined |
| tasks.md | 195 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/tasks.md | 17 tasks, 3 stories, Tests Mode ON, all `[X]` |
| data-model.md | 52 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/data-model.md | Principle/Guidance entities + referenced (unchanged) loop mechanisms |
| contracts/dogfooding-artifacts.md | 45 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/contracts/dogfooding-artifacts.md | C-1…C-7 incl. C-4 no-new-machinery invariants |
| quickstart.md | 52 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/quickstart.md | Four drill scenarios, all on existing engine actions |
| checklists/requirements.md | 37 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/checklists/requirements.md | 16/16 quality items pass (re-validated after revision) |
| verification.md | 54 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/verification.md | Baseline/post-change parity snapshot, SC-001…004 all pass |
| feature-ref.md | 23 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/feature-ref.md | Requirement→Feature 036 mapping, 028 as referenced carrier |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | `/speckit.requirements` scaffolded spec from long conceptual input; 1 NEEDS CLARIFICATION | requirements.md Input header + checklist | None |
| 2 | Inline user answer (Option A) resolved constraint strength before `/speckit.clarify` | requirements.md Clarifications first bullet | Minor — answer recorded outside a `### Session` block (see F6) |
| 3 | `/speckit.clarify` Mode A: Feature 036 created & bound; cycle metric defined | requirements.md `### Session 2026-07-25` | None |
| 4 | `/speckit.plan` v1 designed engine extension (`--status`/`resolve`/`loop-health`) + review-command step | features.md history: "dropped feedback-utils extension & review step from initial plan" | Over-scope caught only by later user input (see F1) |
| 5 | `/speckit.tasks` v1 emitted 26 tasks against the over-scoped plan | tasks.md history (rewritten) | Downstream artifacts built on soon-invalidated design |
| 6 | User concept clarification → full manual rewrite of 7 artifacts + obsolete contract deletion | "当前理念应聚焦于框架本身…复用既有机制" (user turn); `\rm -f contracts/feedback-utils-extension.md` | **Yes** — no command supports post-tasks upstream revision (F1) |
| 7 | `rm` blocked by interactive alias during cleanup | shell output: `rm: remove regular file '...feedback-utils-extension.md'?` — file survived first attempt | Friction (F2) |
| 8 | `/speckit.implement`: TDD in 3 batches, 4 per-story commits 24e7318a→5c37a9bb | git log scoped to spec dir | None |
| 9 | quickstart CLI example rejected by engine at first real execution | `error: Invalid --unit-id; expected '/speckit.<command>' or 'skill:<name>'.` | Doc/code drift caught only by live dogfooding (F3) |
| 10 | Baseline & regression: 729→748 passed, constant 106 failed / 13 errors | verification.md `baseline_pytest=` / `post_change_pytest=` | Long-standing failure debt tolerated (F7) |
| 11 | `.venv` python missing pytest; pipe exit code masked the fallback | `.venv/bin/python: No module named pytest` after `\| tail` returned 0 | Friction (F4) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 2 |
| Automation / Scripts | 3 |
| Workflow | 1 |
| Documentation | 0 |

## 3. Findings (Problems & Improvement Targets)

### F1 — No command path for mid-lifecycle scope revision; downstream artifacts must be rewritten by hand

- **Severity**: P1
- **Category**: Workflow
- **Location**: https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/templates/commands/clarify.md (Behavior Rules); /storage/project/cloud-native-ai/spec-kit/.specify/scripts/bash/create-new-plan.sh
- **Evidence** (verbatim quote):

  ```
  - Do not modify upstream artifacts in later modes (B won't edit requirements.md; C won't edit plan.md)
  ```

  and (project instructions, Recurring Operational Lessons):

  ```
  **In-place amend ≠ re-scaffold**: `create-new-plan.sh` unconditionally overwrites `plan.md`; do NOT run overwrite scaffolding when amending existing specs.
  ```

- **Why it's a problem**: When the user re-scoped the concept *after* tasks.md existed, seven artifacts (requirements, plan, data-model, contracts, quickstart, feature-ref, tasks) plus an obsolete contract file had to be revised entirely by hand, with consistency (dropped-machinery references, FR renumbering, checklist re-validation) maintained only by agent discipline. `/speckit.clarify` explicitly forbids touching upstream files in later modes, and re-running `/speckit.plan` would destroy history via unconditional overwrite — so the prescribed flow offers no safe revision path at all.
- **Proposed fix**: Add a documented "revision protocol" to `templates/commands/clarify.md` (or a `--revise` mode note in `templates/commands/plan.md`): when upstream intent changes post-tasks, (1) amend requirements.md in place recording the directive under `## Clarifications`, (2) regenerate downstream artifacts *without* scaffolding scripts, (3) require a residual-reference sweep (grep for dropped design terms) as an exit gate.

### F2 — Interactive shell aliases (`rm -i`, `cp -i`) silently defeat non-interactive cleanup steps

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/verification.md (notes=); shell transcript of this run
- **Evidence** (verbatim quote):

  ```
  rm: remove regular file '.specify/specs/032-dogfooding-practice/contracts/feedback-utils-extension.md'? dogfooding-artifacts.md
  ```

  (the prompt consumed the next `ls` output as its answer; the file was NOT deleted and required a second pass with `\rm -f`.)

- **Why it's a problem**: The command *appeared* to run, but the deletion silently did not happen — exactly the "cp -i" trap already documented in the project instructions, now reproduced with `rm`. Any spec whose implement phase deletes or mirrors files can ship a stale artifact without noticing.
- **Proposed fix**: In `templates/commands/implement.md`, extend the setup step with a one-line shell-hygiene rule: "file removals/copies in wrap-up steps MUST use alias-proof forms (`\rm -f`, `\cp -f`, or `command rm/cp`) and verify the result (`ls` / `diff -q`)". Mirror the same line into the Recurring Operational Lessons block of `templates/instructions-template.md`.

### F3 — Generated CLI examples are not execution-verified; quickstart shipped an invalid invocation

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/templates/commands/plan.md (Phase 1 outputs); engine rejection observed at /storage/project/cloud-native-ai/spec-kit/scripts/python/feedback-utils.py line 50
- **Evidence** (verbatim quote):

  ```
  error: Invalid --unit-id; expected '/speckit.<command>' or 'skill:<name>'.
  ```

  against the quickstart draft example `--unit-id "my-product:checkout-flow"`, while the engine enforces:

  ```
  _UNIT_ID_RE = re.compile(r"^(?:/speckit\.[a-z0-9._-]+|skill:[a-z0-9._-]+)$")
  ```

- **Why it's a problem**: quickstart.md was written at plan time from intent, not from code, and the invalid example survived plan → tasks → implement until a live dogfooding drill hit the validator. Projects without such a drill would ship broken documentation.
- **Proposed fix**: In `templates/commands/plan.md` (Post-Generation Quality Gate) add one rule: "every executable command example emitted into quickstart.md/contracts MUST be either executed once against the real tool or asserted by a contract test". The same gate slots naturally next to the existing deliberation-marker sweep.

### F4 — Test interpreter ambiguity: `.venv` python lacks pytest and pipe exit codes mask the failure

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.venv/bin/python (environment); baseline run transcript of this review's spec
- **Evidence** (verbatim quote):

  ```
  /storage/project/cloud-native-ai/spec-kit/.venv/bin/python: No module named pytest
  ```

  emitted by `.venv/bin/python -m pytest -q 2>&1 | tail -5 || python3 -m pytest ...` — the `||` fallback never fired because `tail` exited 0.

- **Why it's a problem**: Every implement run pays a retry to discover the right interpreter, and the pipe-masking pattern can record an empty "baseline" without anyone noticing.
- **Proposed fix**: Add a `scripts/bash/run-tests.sh` (or a line in `templates/commands/implement.md` Setup) that resolves the interpreter once (`python3 -m pytest`, honoring `PIPESTATUS`/`set -o pipefail`) and is referenced by both baseline (T001-style) and regression tasks.

### F5 — tasks-template forces an empty Foundational phase header when a feature has no blocking prerequisites

- **Severity**: P2
- **Category**: Template
- **Location**: https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/templates/tasks-template.md (Phase 2 block); instantiated at /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/tasks.md
- **Evidence** (verbatim quote, from the instantiated tasks.md):

  ```
  ## Phase 2: Foundational (Blocking Prerequisites)

  **Purpose**: 无阻塞性前置 — 本特性纯文本交付，无共享基础设施需先行构建（Phase 1 基线即前置）

  *(no tasks)*
  ```

- **Why it's a problem**: Pure-template/governance specs (an increasingly common shape in this repo: rubric, glossary, dogfooding) have no foundational infrastructure, yet the template's fixed phase numbering pressures writers to keep a placeholder phase, which downstream tooling then has to parse around.
- **Proposed fix**: In `templates/tasks-template.md`, annotate Phase 2 with "OMIT this phase entirely when no blocking prerequisites exist — renumber subsequent phases" so generated files carry no empty scaffolding.

### F6 — First clarification answer recorded outside the `### Session` structure

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/requirements.md (`## Clarifications`)
- **Evidence** (verbatim quote):

  ```
  - Q: Dogfooding 对下游项目的约束强度（建议性 / 节点提醒 / 阻断门禁）？ → A: 建议性原则 + 评审节点提醒；不设阻断性门禁。

  ### Session 2026-07-25
  ```

- **Why it's a problem**: `/speckit.requirements` resolves its ≤3 residual questions directly but has no instruction to nest answers under a dated session heading, while `/speckit.clarify` does — producing two formats in the same section and complicating later tooling that groups clarifications by session.
- **Proposed fix**: In `templates/commands/requirements.md` step 7 (remaining-clarifications handling), instruct writing accepted answers under `### Session YYYY-MM-DD` — same convention as clarify's integration rules.

### F7 — Permanent baseline failure debt (106 failed / 13 errors) forces every spec to reason about noise

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/032-dogfooding-practice/verification.md
- **Evidence** (verbatim quote):

  ```
  baseline_pytest=729 passed, 106 failed, 13 errors, 1 skipped (pre-existing failure batch, matches long-term baseline)
  ```

- **Why it's a problem**: "Zero new failures vs baseline" discipline works, but each spec must re-measure and mentally subtract ~119 known-bad outcomes; a genuinely new failure inside an already-failing module would be invisible. The debt is acknowledged across multiple features' notes yet owned by none.
- **Proposed fix**: Open a dedicated maintenance spec to either fix or formally quarantine (e.g. `xfail` markers with reason strings) the 106+13 known failures, so future baselines are near-green and regression detection is exact.

## 4. What Worked — Preserve (Brief)

- Test-first contract batches (fail → implement → green) cleanly enforced by tasks.md ordering; three batches, zero rework.
- Contract tests as invariants: C-4 pins the FR-004 "no new machinery" red line permanently, not just for this run.
- Per-story commits (US1/US2/US3/polish) gave `/speckit.review` a reconstructable timeline.
- Live dogfooding during implement surfaced two real defects (F2, F3) that static review would have missed — the feature validated itself.
- `verification.md` structured key=value baseline/post-change snapshot made SC-004 (parity) mechanically checkable.
- User-driven scope correction (dropping the engine extension) was absorbed without losing clarify/Feature-binding history — in-place amend discipline held.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Allow omitting empty Foundational phase** — Target: https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/templates/tasks-template.md. Change: annotate Phase 2 as omittable with renumbering when no blocking prerequisites exist. Source: F5. Expected impact: less boilerplate in template-only specs; simpler downstream parsing.

### 5.2 Command Prompt Improvements

- **Execution-verify emitted CLI examples** — Target: https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/templates/commands/plan.md (Post-Generation Quality Gate). Change: require each command example in quickstart/contracts to be run once or contract-tested. Source: F3. Expected impact: eliminates doc/code drift at birth.
- **Session-structured answers in requirements** — Target: https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/templates/commands/requirements.md. Change: record inline-resolved clarifications under `### Session YYYY-MM-DD`. Source: F6. Expected impact: single clarification format across commands.
- **Alias-proof shell hygiene in implement** — Target: https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/templates/commands/implement.md. Change: mandate `\rm -f`/`\cp -f`/`command rm` + post-check for destructive/mirror steps. Source: F2. Expected impact: removes a silent-stale-artifact class.

### 5.3 Automation / Script Improvements

- **Canonical test runner** — Target: https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/scripts/bash/ (new `run-tests.sh`). Change: resolve interpreter once, `set -o pipefail`, shared by baseline and regression tasks. Source: F4. Expected impact: reproducible baselines, no masked failures.
- **Quarantine the failure debt** — Target: /storage/project/cloud-native-ai/spec-kit/tests/ (dedicated maintenance spec). Change: fix or `xfail`-mark the standing 106 failures / 13 errors. Source: F7. Expected impact: near-green baseline; exact regression detection.

### 5.4 Workflow Improvements

- **Documented mid-lifecycle revision protocol** — Change: add a "scope revision after tasks" subsection to https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/templates/commands/clarify.md: amend requirements in place, hand-regenerate downstream without scaffold scripts, finish with a residual-reference grep gate. Source: F1. Expected impact: turns today's discipline-dependent rewrite into a prescribed, checkable path.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Mid-lifecycle revision protocol | templates/commands/clarify.md | F1 |
| P1 | Alias-proof shell hygiene in implement | templates/commands/implement.md | F2 |
| P1 | Execution-verify emitted CLI examples | templates/commands/plan.md | F3 |
| P2 | Canonical test runner script | scripts/bash/run-tests.sh (new) | F4, F7 |
| P2 | Omittable Foundational phase | templates/tasks-template.md | F5 |
| P2 | Session-structured requirements answers | templates/commands/requirements.md | F6 |
| P2 | Quarantine standing test-failure debt | tests/ (maintenance spec) | F7 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `https://github.com/github/spec-kit/blob/35f05219ad65079a95679c4a298731471fcd983f/...`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
