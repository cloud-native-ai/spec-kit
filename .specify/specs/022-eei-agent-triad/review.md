# Specification-Driven Development (SDD) Process Review Report: EEI Agent Triad (Executor-Evaluator-Improver)

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 022 |
| Requirement Key | 022-eei-agent-triad |
| Requirement Name | EEI Agent Triad (Executor-Evaluator-Improver) |
| Related Feature | 019 Agents Command |
| Repository | spec-kit |
| Repository URL | https://github.com/cloud-native-ai/spec-kit (divergent fork; `origin` nominally points upstream to https://github.com/github/spec-kit) |
| Branch | 022-eei-agent-triad |
| Commit SHA | 0bf2a9a8811097b170ece5df01be897a5c14813e (short: 0bf2a9a) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-07-02 |
| Reviewer (Agent) | Claude Opus 4.8 (claude-opus-4-8), invoked via `/speckit.review` in Claude Code CLI |
| Environment | Linux 5.10.134-15.2.al8.x86_64 (x86_64); bash; Python 3.11.11. This feature is template/prompt engineering — no runtime language/toolchain is exercised. |
| spec-kit Source Snapshot | https://github.com/cloud-native-ai/spec-kit @ 0bf2a9a8811097b170ece5df01be897a5c14813e (this review runs *inside* the spec-kit repo itself; the reviewed templates/commands/scripts are this same tree). NOTE: commit 0bf2a9a is currently local-only (not yet pushed to `gitee`/`github`/`gitlab` remotes — `git branch -r --contains 0bf2a9a` returns only `*/master`), so absolute filesystem paths below are authoritative; blob URLs at the fork will resolve only after this branch is pushed. |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 172 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/requirements.md | 12 FRs / 6 SCs / 5 user stories for the EEI triad pattern; Clarifications resolved Feature binding to 019 |
| plan.md | 120 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/plan.md | Constitution Check table, project structure, Phase 0 findings inlined (no research.md) |
| tasks.md | 149 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/tasks.md | 31 tasks across 8 phases; T008/T013 marked `[~]` deferred |
| data-model.md | 128 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/data-model.md | 9 conceptual entities (Triad, Iteration, ScoringConfig, …) + state transitions |
| contracts/triad-protocol.md | 126 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/contracts/triad-protocol.md | Input/Output/Constraint tables per sub-agent + orchestrator responsibilities |
| quickstart.md | 107 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/quickstart.md | 3 usage scenarios + key principles + validation checklist |
| checklists/requirements.md | 36 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/checklists/requirements.md | Spec-quality checklist, all boxes ticked |
| verification.md | 55 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/verification.md | Baseline/post-change counts + per-SC status; `post_change_commit=pending` |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Baseline snapshot taken before implement | verification.md line 6: `baseline_commit=3b5a21d180c4339c34f38303e2a3a18f7c395053` | None — matches `/speckit.implement` baseline convention |
| 2 | `/speckit.requirements` produced the spec | requirements.md exists with FR/SC/user-story structure | None |
| 3 | `/speckit.clarify` bound the spec to a feature | requirements.md line 173: `Q: Which existing Feature should this spec belong to? → A: Feature 019 (Agents Command)` | None |
| 4 | `/speckit.plan` produced plan + design docs | plan.md Constitution Check table; data-model.md; contracts/triad-protocol.md; quickstart.md | Minor: `research.md` intentionally skipped — plan.md line 57: `No standalone research.md — findings inlined below` |
| 5 | `/speckit.tasks` produced 31 tasks | tasks.md with 8 phases | None |
| 6 | `/speckit.implement` created templates + docs | templates/agent-subrole-{executor,evaluator,improver}-template.md; templates/agent-triad-orchestration-template.md; docs/eei-triad-pattern.md all present | None (files exist) |
| 7 | Both automated-test tasks deferred | tasks.md T008/T013 `[~]`; verification.md line 50: `deferred_tasks=T008,T013` | Deviation: Test-First mandate (tasks.md line 9 `Tests Mode: ON`) satisfied by deferral, not by tests. See F2. |
| 8 | Feature committed with unrelated changes bundled in | `git show --stat f261cea` lists `skills/draw-plantuml/SKILL.md`, `.../howto/00-semantic-analysis.md` (~540 lines) alongside the EEI feature | Deviation: commit boundary not feature-scoped. See F5. |
| 9 | verification.md left with stale field | verification.md line 17: `post_change_commit=pending` | Deviation: post-change commit never backfilled. See F6. |
| 10 | Prior friction: verification artifact renamed off `.log` | Repo history commit `ddc3655 refactor: rename verification.log to verification.md to avoid .gitignore exclusion` | Deviation (already remediated): artifact was silently gitignored. See F1. |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 3 |
| Command Prompt | 2 |
| Automation / Scripts | 0 |
| Workflow | 2 |
| Documentation | 0 |

## 3. Findings (Problems & Improvement Targets)

### F1 — "Verification Log" naming invites a `.log` filename that `.gitignore` silently swallows

- **Severity**: P1
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/templates/verification-log-template.md (H1) and /storage/project/cloud-native-ai/spec-kit/.gitignore#L40
- **Evidence** (verbatim quote):

  ```
  # verification-log-template.md, line 1
  # Verification Log — [REQUIREMENTS_KEY]
  ```
  ```
  # .gitignore, line 40
  *.log
  ```
  Repo history: `ddc3655 refactor: rename verification.log to verification.md to avoid .gitignore exclusion`

- **Why it's a problem**: The template is named `verification-log-template.md` and its H1 reads "Verification Log", steering writers toward a `verification.log` output — which the repo-wide `*.log` rule silently untracks, causing the SC-tracking artifact to vanish from version control. A dedicated cleanup commit (`ddc3655`) already proves this bit someone; the latent trap remains for the next writer.
- **Proposed fix**: In `.specify/templates/verification-log-template.md` (and its packaged twin `templates/verification-log-template.md`), add a top-of-file comment: `OUTPUT FILENAME MUST be verification.md — never verification.log (.gitignore excludes *.log)`. Optionally add `!verification*.md` is unnecessary, but consider adding a negative guard comment near `.gitignore` line 40.

### F2 — Test-First gate is forced ON for a no-runtime-code feature, then satisfied by 100% test deferral

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/tasks.md#L9, /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/plan.md#L33, and the generator /storage/project/cloud-native-ai/spec-kit/templates/commands/tasks.md
- **Evidence** (verbatim quote):

  ```
  # tasks.md, line 9
  **Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates tests BEFORE implementation; contract test for triad protocol required)
  ```
  ```
  # tasks.md, line 56 (and T013 line 61)
  - [~] T008 [US1] Write contract test ... <!-- deferred: pytest contract test not applicable to template/prompt feature; validated structurally -->
  ```
  ```
  # plan.md, line 33
  | IV | Test-First & Contract-Driven Implementation | ✅ Pass | Contract defined for triad orchestration protocol; test scenarios in US1-US5 acceptance criteria |
  ```

- **Why it's a problem**: The workflow forces "Tests Mode: ON" and marks the Constitution's Test-First principle "✅ Pass" at plan time, but every executable test task (T008, T013) is then deferred as "not applicable to template/prompt feature." The gate rubber-stamps a principle the feature structurally cannot satisfy, so the compliance signal is meaningless for this class of feature and there is no sanctioned path to declare "tests N/A — no runtime code."
- **Proposed fix**: In `templates/commands/tasks.md` and `templates/plan-template.md`, add an explicit "Tests N/A (documentation/template/prompt feature — no runtime code)" determination with a required one-line justification, so Principle IV is recorded as *justified-N/A* rather than *Pass-then-deferred*. Wire the same option into the Constitution Check row so the ✅/N/A distinction is visible.

### F3 — Generated tasks.md drops the `[X]`/`[~]` checkbox-state legend, leaving `[~]` undefined in the artifact

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/tasks.md#L55-L58 (generated) vs. /storage/project/cloud-native-ai/spec-kit/templates/tasks-template.md#L64-L70 (source)
- **Evidence** (verbatim quote):

  ```
  # generated tasks.md, lines 55-58 — the ENTIRE state legend present in the file
  ## Format: `[ID] [P?] [Story] Description`

  - **[P]**: Can run in parallel (different files, no dependencies)
  - **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
  ```
  ```
  # templates/tasks-template.md, line 68 — legend that was NOT carried into the generated file
  - `- [~]` — **Deferred**. Task is intentionally handed off to the user (or to a later phase). Reasons must be recorded in `verification.md` ...
  ```

- **Why it's a problem**: The source template defines `[ ]`/`[X]`/`[~]` as first-class states, but the `/speckit.tasks` instantiation kept only the `[P]`/`[Story]` legend. The generated file then uses `[~]` on T008/T013 with no in-file definition — a reader (or a downstream tool author) cannot tell from the artifact alone what `[~]` means.
- **Proposed fix**: In `templates/commands/tasks.md`, require the generator to copy the checkbox-state legend block (`templates/tasks-template.md` lines 65-70) verbatim into every generated `tasks.md`, immediately under the `## Format:` header.

### F4 — Packaged (`templates/`, `skills/`) and runtime (`.specify/`) trees drift; new sub-role templates never reached `.specify/templates/`

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/ vs /storage/project/cloud-native-ai/spec-kit/.specify/templates/
- **Evidence** (verbatim quote):

  ```
  # ls .specify/templates/agent-subrole-*.md .specify/templates/agent-triad-*.md
  ls: cannot access '.specify/templates/agent-subrole-*.md': No such file or directory
  ls: cannot access '.specify/templates/agent-triad-*.md': No such file or directory
  ```
  ```
  # git show --stat f261cea (relevant rows) — feature edited packaged skills only, not runtime twins
   skills/create-agent/SKILL.md                       |  46 ++++
   skills/improve-agent/SKILL.md                      |  34 +++
   templates/agent-subrole-executor-template.md       |  47 ++++
   ...
  ```

- **Why it's a problem**: The four new EEI templates and the create-agent/improve-agent updates landed in the packaged trees (`templates/`, `skills/`) but not in the runtime trees (`.specify/templates/`, `.specify/skills/`) that this project's own agents actually load. The same commit *did* mirror `draw-plantuml` to both `skills/` and `.specify/skills/`, so mirroring is done manually and inconsistently. Nothing in the SDD flow reconciles the two trees, so the project dogfoods stale runtime copies until a manual reinstall.
- **Proposed fix**: Add a `scripts/bash/sync-runtime.sh` (mirror `templates/`→`.specify/templates/`, `skills/`→`.specify/skills/`) and reference it as a post-implement step in `templates/commands/implement.md`; or add a self-containment check to `/speckit.implement` that fails when a file created under `templates/`/`skills/` has no counterpart under `.specify/`.

### F5 — No `/speckit.*` step defines a feature-scoped commit boundary; unrelated changes bundled into the feature commit

- **Severity**: P2
- **Category**: Workflow
- **Location**: commit f261cea (`git show --stat`), /storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md
- **Evidence** (verbatim quote):

  ```
  # git show --stat f261cea — non-feature files inside the EEI feature commit
   .specify/skills/draw-plantuml/SKILL.md             |  47 +++-
   .../references/howto/00-semantic-analysis.md       | 271 +++++++++++++++++++++
   skills/draw-plantuml/SKILL.md                      |  47 +++-
   .../references/howto/00-semantic-analysis.md       | 271 +++++++++++++++++++++
  ```

- **Why it's a problem**: The EEI feature commit `f261cea` also carries ~540 lines of unrelated `draw-plantuml` skill work. `/speckit.review` Step 2 reconstructs the timeline via `git log` scoped to the feature directory; bundled commits defeat that reconstruction and make per-feature diffing unreliable. No SDD command owns the commit boundary, so isolation depends entirely on operator discipline.
- **Proposed fix**: Add an optional "Finalize" step to `templates/commands/implement.md` that stages only paths under `REQUIREMENTS_DIR` plus the files it created/edited during the run and commits them with a `feat(<REQUIREMENTS_KEY>): …` message, or document a mandatory feature-isolated-commit rule in `docs/git-workflow.md` and cross-link it from the implement command.

### F6 — `verification.md` template ships a `post_change_commit=pending` field that is structurally impossible to fill in-run and is left stale

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/verification.md#L17, source /storage/project/cloud-native-ai/spec-kit/.specify/templates/verification-log-template.md
- **Evidence** (verbatim quote):

  ```
  # verification.md, lines 15-17
  implementation_date=2026-07-02
  post_change_commit=pending
  ```

- **Why it's a problem**: `post_change_commit` cannot be known while the implement run is still producing the very changes that will be committed (chicken-and-egg), so it is predictably left as `pending`. A field that is always stale trains readers to ignore the log and pollutes any tool that parses it for the implementing commit SHA.
- **Proposed fix**: In `templates/verification-log-template.md`, either drop `post_change_commit` or relabel it `post_change_commit=<filled by post-commit hook / speckit.review>` and have `/speckit.review` (which already has `COMMIT_SHA_FULL`) backfill it, so the field has an owner instead of dangling.

### F7 — Plan template's code-centric Technical Context forces repeated `N/A` for template/prompt features (cargo-cult fields)

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/022-eei-agent-triad/plan.md#L12-L18, source /storage/project/cloud-native-ai/spec-kit/templates/plan-template.md
- **Evidence** (verbatim quote):

  ```
  # plan.md, lines 12-18
  **Language/Version**: N/A — this is a template/prompt engineering feature, not runtime code
  ...
  **Performance Goals**: N/A — template rendering is near-instantaneous
  ```

- **Why it's a problem**: The `plan-template.md` Technical Context block assumes a runtime-code feature (Language/Version, Performance Goals, Scale/Scope, Storage), so a template/prompt feature must fill several fields with hand-written `N/A` justifications. This is leftover boilerplate the writer has to translate/neutralize every time spec-kit itself (or any doc-only feature) is the subject.
- **Proposed fix**: In `templates/plan-template.md`, mark the code-specific Technical Context fields explicitly optional and add a one-line "Feature Type" selector (`runtime-code` | `template/prompt` | `documentation`) that governs which fields are required, so doc/template features skip the code fields instead of stamping `N/A`.

## 4. What Worked — Preserve (Brief)

- Baseline-before-implement capture (`baseline_commit=…` in verification.md) gives `/speckit.review` a clean before/after anchor — keep it.
- Per-SC status schema (`SC-NNN_status=pass|partial|deferred`) in the verification log is machine-parseable and was fully populated — preserve the enum discipline.
- `[~]` deferral with an inline `<!-- deferred: reason -->` comment plus a `deferred_tasks=` registry made skipped work auditable rather than silent — keep this dual-recording.
- `/speckit.clarify` recorded the Feature-binding decision inline (requirements.md Clarifications) rather than in a side channel — preserve.
- The plan gracefully documented the intentional `research.md` omission instead of leaving a dangling reference — preserve that "explain the skip" habit.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Guard the verification artifact against `*.log`** — Target: /storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md (and `.specify/templates/verification-log-template.md`). Change: add a header comment mandating `verification.md` output and warning that `*.log` is gitignored. Source: F1. Expected impact: eliminates a silent version-control loss trap for every future spec.
- **Give `post_change_commit` an owner or remove it** — Target: /storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md. Change: drop the field or mark it as backfilled by `/speckit.review`. Source: F6. Expected impact: no more permanently-stale `pending` fields.
- **Feature-type-aware Technical Context** — Target: /storage/project/cloud-native-ai/spec-kit/templates/plan-template.md. Change: add a Feature Type selector and make code-specific fields optional. Source: F7. Expected impact: doc/template features stop stamping `N/A` across four fields.

### 5.2 Command Prompt Improvements

- **Sanctioned "Tests N/A" path** — Target: /storage/project/cloud-native-ai/spec-kit/templates/commands/tasks.md and /storage/project/cloud-native-ai/spec-kit/templates/plan-template.md (Constitution Check). Change: allow a justified Tests-N/A determination for no-runtime-code features instead of forcing Tests Mode ON then deferring. Source: F2. Expected impact: the Test-First gate carries real signal for template/prompt features.
- **Carry the checkbox-state legend into generated tasks.md** — Target: /storage/project/cloud-native-ai/spec-kit/templates/commands/tasks.md. Change: require verbatim copy of the `[ ]`/`[X]`/`[~]` legend into each generated file. Source: F3. Expected impact: `[~]` is self-documenting in every tasks.md.

### 5.3 Workflow Improvements

- **Runtime/packaged tree sync** — Change: add `scripts/bash/sync-runtime.sh` and an implement-time self-containment check that flags any `templates/`/`skills/` file lacking a `.specify/` counterpart (Target: /storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md). Source: F4. Expected impact: the project stops dogfooding stale runtime copies.
- **Feature-scoped commit boundary** — Change: add a Finalize/commit step to /storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md (or a mandatory rule in /storage/project/cloud-native-ai/spec-kit/docs/git-workflow.md) that commits only feature-scoped paths. Source: F5. Expected impact: `/speckit.review` and `/speckit.analyze` get reliable per-feature diffs.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Guard verification artifact against `*.log` gitignore trap | templates/verification-log-template.md + .gitignore | F1 |
| P1 | Add sanctioned "Tests N/A" path for no-runtime-code features | templates/commands/tasks.md + templates/plan-template.md | F2 |
| P2 | Carry `[X]`/`[~]` legend into generated tasks.md | templates/commands/tasks.md | F3 |
| P2 | Sync packaged↔runtime trees + implement-time check | templates/commands/implement.md + scripts/bash/sync-runtime.sh | F4 |
| P2 | Define feature-scoped commit boundary | templates/commands/implement.md + docs/git-workflow.md | F5 |
| P2 | Fix/retire stale `post_change_commit` field | templates/verification-log-template.md | F6 |
| P2 | Feature-type-aware Technical Context in plan | templates/plan-template.md | F7 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `{REPO_URL}/blob/{COMMIT_SHA}/...` (absolute paths used; commit is local-only, noted in Section 0).
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
