# Specification-Driven Development (SDD) Process Review Report: /speckit.team view — 团队结构与状态只读呈现（Team View）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 103 |
| Requirement Key | `103-team-view` |
| Requirement Name | `/speckit.team view — 团队结构与状态只读呈现（Team View）` |
| Related Feature | 027 Team Management (`Implemented`; extension slice, no status regression) |
| Repository | spec-kit |
| Repository URL | remotes: `origin git@github.com:github/spec-kit.git` (upstream), `github`/`gitee`/`gitlab` carry the same project; all SSH, no HTTPS web rendering |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the branch has no upstream and nothing was pushed. Cite absolute paths plus `git show a5b81b881:<path>` instead of URLs. |
| Branch | `103-team-view` |
| Commit SHA | `a5b81b88105bce170c2bcab73c196d4e7e548c96` (short: `a5b81b881`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-24 |
| Reviewer (Agent) | Qoder SDD review stage (fresh-context stage runner; four segments executed in the fixed order, ARC last) |
| Environment | Linux x86_64 (`5.10.134-15.2.al8`), GNU bash 4.4.20, CPython 3.11.11, pytest 8.4.2 (xdist 3.8.0), git 2.43.5, Node v26.3.0; installed `specify` = `ai-harness-cli 0.0.22` (deprecated pre-rename alias — see F4) |
| spec-kit Source Snapshot | same repository at `a5b81b881` (self-hosting; framework hat) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 230 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/requirements.md` | 21 FR / 7 SC / 4 Shared Strings / A-1…A-19 / RS-001…RS-005 / EP references |
| plan.md | 168 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/plan.md` | Constitution Check 23/23, Project Structure, Mirror Obligations, EP-001…003, Inherited Blockers none |
| tasks.md | 304 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/tasks.md` | 44 rows (T001–T044), Tests Mode ON, DoD-1…8, GATE-1…5 |
| research.md | 59 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/research.md` | B-01…B-20 measurements, R-01…R-14 decisions, U-01…U-04 |
| data-model.md | 176 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/data-model.md` | E1–E9, INV-01…INV-14, Rendering Line Types, FR-021 Fixture Map (12 rows) |
| contracts/team-view-command.contract.md | 89 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/contracts/team-view-command.contract.md` | C-01…C-12 command wiring |
| contracts/view-team-skill.contract.md | 65 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/contracts/view-team-skill.contract.md` | C-13…C-23 skill contract |
| contracts/team-view-program.contract.md | 124 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/contracts/team-view-program.contract.md` | C-24…C-38 program interface |
| quickstart.md | 98 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/quickstart.md` | S-0…S-6, per-example premises + pinning test names |
| feature-ref.md | 60 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/feature-ref.md` | Feature 027 binding + 20-entry delivery surface |
| verification.md | 57 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/verification.md` | SC-001…SC-007 status rows, smoke triple, RS-005 joint acceptance |
| checklists/requirements.md, checklists/team-view.md | 39 + 83 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/checklists/` | requirement-quality checklists (outside the expected-set denominator; reviewed as support) |
| notes/red-first-evidence.md, quickstart-run.md, pre-change-measurements.md | 99 + 355 + 129 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/notes/` | red-first capture, executed quickstart scenarios, pre-change measurements (support) |
| test-evidence/ | dir | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/test-evidence/` | per-stage E3 rows, gate readings, targeted-suite outputs |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | U1 breakpoint: fresh start at requirements | base `df1b204f5`; no `103-*` branch; pre-existing dirty files = 2 (`coaching-skills/SKILL.md`, `references/trainee-resolution.md`) | No |
| 2 | requirements attempt 1 | `124f2d962`; gate refused: `requirements.md carries no § Runtime Stack & Dependency Ownership` (mandatory for execution-class) | Yes — gate correctly refused; bounded repair dispatched |
| 3 | requirements attempt 2 | `e6230672d`; RS-001…RS-005 + EP references; `pre-analyze-check --stage requirements` pass (errors=0, advisories=2) | No |
| 4 | clarify | `a873907b5`; Feature 027 bound; program path `scripts/python/team-view.py` pinned (A-16); unattended self-adjudication recorded | No |
| 5 | plan | `9b57ba59d`; 3 contracts / 38 clauses; EP-001…003 verified; gate pass errors=0, advisories=58 | No |
| 6 | tasks | `d89c91fd3`; 44 rows; one PLAN-EDIT (minor): delivery surface gains `shared/definitions/probe-definitions.md` + mirror (item 19) | Yes — mid-chain registry repair (F3) |
| 7 | checklist | `1ed62808c`; `checklists/team-view.md` 83 lines; no plan-owned touch | No |
| 8 | analyze | `test-evidence/analyze-report.md`; 0 CRITICAL / 0 HIGH / 4 MEDIUM / 2 LOW; E-02 predicts the FR-018 citation gap | Yes — MEDIUM findings left without a disposition record (F7) |
| 9 | implement P1 (T001–T010) | `6bab4a0ed`, `5ae5b3358`; baseline full run (`222 failed / 9818 passed`, rc derived from a `\| tail` pipeline); red-first capture `rc 1 · 38 failed, 1 passed, 192 errors` | Yes — baseline rc derived (F5); the full run rewrote `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` (F4) |
| 10 | implement P2–P3 | `90d178698` (P2: program wiring, skill, probe registration; 97 passed), `5f169622f` (P3: overview, routing, docs; 97 passed) | No |
| 11 | implement P4 (T032–T044) | `328847007` (error paths, quickstart run, verification, gates), `a5b81b881` (close-out evidence); second PLAN-EDIT (minor): flow-class ledger row (item 20) | Yes — second mid-chain registry repair (F3) |
| 12 | package verifications P1–P4 | fresh-context verifiers, each `VERDICT: pass` (6/6, 8/8, 7/7, 6/6) | No |
| 13 | review (this run) | base `df1b204f5`..head `a5b81b881`; triage `run` (78 changed, 7 code paths); targeted 103 passed; smoke 19 passed; ARC `accept`; code gate `allow` | No |
| 14 | machine side effect during the line | `run-determination.py` settled prior pending session records of the same units (`settled_at` filled; `pending_next_turn → no_user_input`) in 4 tracked `.specify/memory/session/*` files; left uncommitted | No — engine's documented `settle` behaviour; disclosed, not committed |

## 2. Findings Summary

Each segment keeps its own vocabulary and its own count; the three blocks below are not summed, mapped or scored together.

**Process segment** (`P0`/`P1`/`P2`, owned by `review-sdd-process`):

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 5 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 |
| Command Prompt | 0 |
| Automation / Scripts | 3 |
| Workflow | 3 |
| Documentation | 0 |

**Artifact segment** (`P0`/`P1`/`P2`): P0 = 0 · P1 = 1 · P2 = 2. **Implementation segment**: P0 = 0 · P1 = 1 · P2 = 1.

**Code segment** (six-level family, never mapped): `blocking` 0 · `important` 1 · `suggestion` 2 · `nitpick` 1 · `question` 1 · `praise` 2; gate `allow`.

**Concurrency reading**: requested 24 · effective 1 · effective_reason `single-unit` (one read-only review chain; the four segments are sequential by composition, and the code segment is one deterministic walk).

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `df1b204f5ba6ad696e7bb330a2cfb418961bb0b4` | `git-delta-review.sh base --spec .specify/specs/103-team-view` |
| Head commit | `a5b81b88105bce170c2bcab73c196d4e7e548c96` | run-start `HEAD`, fixed for this run |
| Base source | `feature-first-commit` | the resolution tier the code skill's `base` step reported |
| Renderer mode | `text` | non-interactive agent invocation; receipt header `renderer=text` |
| Changed / judged / skipped / gap files | 78 / 6 / 72 / 0 | copied field by field from the receipt block in `code-review.md` |
| Segment verdict | `not-evaluated` | the receipt's own derivation: `skipped_files > 0` earns no coverage credit; 0 gaps, 0 `blocking` |
| Gate verdict | `allow` | `report --summary --file code-review.md` → `{"blocking":0,"important":1,"suggestion":2,"nitpick":1,"question":1,"praise":2}`, `gate=allow`; the one `important` item is answered below |
| Reason, when one applies | not-evaluated: 72 legal skips (`generated` mirrors and per-tool copies; `non-code-file` docs, spec artifacts and evidence), 0 gaps; `none` for the merge gate | `code-review.md` |
| Uncommitted scope | 42 uncommitted paths were outside the review object (the 4 settled session records, the 2 pre-existing coaching-skills files, the 081 smoke evidence rewrite, this line's runtime records and the review's own evidence files); the receipt gives no conclusion over them, and the verbatim sentence with the full path list lives in `code-review.md` | `code-review.md` |
| Record | `.specify/specs/103-team-view/code-review.md` | written because triage = `run` |
| Archive | `none` | first code-segment run for this slice |

Client capture: `capture: skipped hat=framework basis=root owns framework source directories (templates/skills/shared/scripts/src/specify_cli); triage=run` — the repository is judged framework-hat, so capture does not run and no five-value token is emitted.

**Answer to the single `important` item** (required by the transition gate): **agreed** — `--spec-dir` is a declared, silently ignored option and a real FR-005 / C-13 / C-26 defect (I1). This review does not repair artifacts; the fix belongs to a bounded implement-stage repair (either forward the value to the `binding` read — the only engine read that declares `--spec-dir` — or reject the option explicitly with exit 2).

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/ (3), data-model.md, quickstart.md, verification.md, research.md, feature-ref.md, test-evidence/ — 10 members | stage rules (standard spec-stage product) ∪ `plan.md` § Project Structure (lines 81–96) |
| Coverage line | 10 / 10 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `blocked` | one P1 acceptance-honesty finding plus two P2 rows |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/103-team-view/tasks.md` | 19 | none | DoD-1 claims “FR-001…FR-021 每条都被至少一个任务行…引用”, and `.specify/features/027-team-management.md:16` repeats it as fact; at HEAD **FR-018 has 0 citing rows** while the other 20 FRs have ≥2 each (enumerated in §3 F2). The named oracle (`pre-analyze-check --stage tasks`) counts FR presence (`"fr": 21`), not citations, so the gate stays green on this defect. |
| P2 | `.specify/specs/103-team-view/plan.md` | 162 (also 43) | none | Two retrospective counts are stale: “18-entry delivery surface” while `feature-ref.md` now lists 20 entries, and Constitution row IV says the fixture forms are “mapped to four new test files” while the FR-021 Fixture Map names three (`data-model.md:161-176`). |
| P2 | `.specify/specs/103-team-view/verification.md` | 7 | none | `post_change_commit=5f169622f` is the P3 close commit, but this file itself lands with the P4 commit `328847007` (the in-line note says so); a reader recomputing the post-change delta from this pointer misses the file that carries the record. |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `df1b204f5ba6ad696e7bb330a2cfb418961bb0b4` | the resolved diff base |
| Head commit | `a5b81b88105bce170c2bcab73c196d4e7e548c96` | run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/integration/test_team_view_program.py -q --names-out .specify/specs/103-team-view/test-evidence/us4-failed.txt` | recorded verbatim from `verification.md:11` |
| Smoke exit code | `0` | re-run in this review verbatim: `19 passed in 6.45s`, rc 0 |
| Smoke evidence path | `.specify/specs/103-team-view/test-evidence/review-smoke.txt` | exists, non-empty (this run's capture; the recorded triple also points at `test-evidence/us4-green.txt`) |
| Scope and regression verdict | **scope: clean** — all 78 changed paths fall inside `feature-ref.md` § Delivery surface items 1–20 (items 19/20 are the two lifecycle registrations), this spec directory, and the two per-tool/registry mirror classes; `goal-utils.py`, create/improve/run skills and `pyproject.toml` untouched (RS-004 zero modification confirmed). **regression: clean** — feature targeted set 103 passed / 0 failed; failure-name set difference vs the 222-name entry baseline = **0 new**; `sync-mirrors.py --check` rc 0 (three scopes `ok`), `regen-command-copies.py --check` rc 0; plan-owned audit `classification=declared` (`plan.md` + `feature-ref.md`, 3 minor declarations, `undeclared=false`) | this segment's readings; evidence in `test-evidence/review-targeted.txt`, `review-failed.txt`; `git-delta-review.sh` receipt |
| Segment verdict | `blocked` | one P1 finding below |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `scripts/python/team-view.py` | 1297 | none | `--spec-dir` is declared in the closed CLI surface (C-26) with the promise “forwarded to engine reads that accept it”, but `main()` never reads `args.spec_dir`; FR-005 / C-13 / `data-model.md` E1 require a value the team archive cannot serve to be **reported**, never silently ignored. Measured: `team-view.py team-a --spec-dir /nonexistent/spec --repo-root <fixture>` → rc 0, empty stderr. |
| P2 | `scripts/python/team-view.py` | 891 | none | A declared-but-empty `config: {}` renders `config: 未声明（默认值见 …）` instead of `为空` (`config_state = None if config_entries else STATE_UNDECLARED`); FR-015's missing-state set and `data-model.md` E4 distinguish “present but zero entries” from “absent”. Measured on a fixture whose frontmatter carries `config: {}`. |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `.specify/features.md` row 027 (extension slice) |
| `final_path` record, copied verbatim (7/7) | pass 2 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 2 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/103-team-view --json` (exit 0), never recomputed here |
| Comparison verdict | `agree` | checker verdict `accept`; claim `Implemented`; `pass` bucket = 2, not 0; `completion_conditions` all true; `reasons: []` |
| Failed condition, on refusal | none — no refusal fires on this record | — |
| Fixed item, on refusal | none | `F-ACCEPTANCE` fires only when the `pass` bucket reads zero; here it reads 2 |

## Status Transition — judged once, granted pending the driver's registry write

The transition judged here is `Implemented → Ready for Review`; its four conjunctive conditions are owned by `templates/feature-details-template.md` § Canonical Status State Machine and are cited, not restated.

| Condition | Reading | Verdict |
|---|---|---|
| (a) every deferred (`[~]`) task resolved or explicitly waived | `tasks.md`: 44 closed / 0 open; `deferred_tasks=` empty in `verification.md` | satisfied |
| (b) review evidence produced | `review.md` and `code-review.md` are on disk; `test-evidence/review.jsonl` records the run | satisfied |
| (c) the current code-segment record contains no `blocking` entry | `code-review.md`: 0 `blocking`; `report --summary --file` exits 0 with `gate=allow`; the one `important` item is answered in §2.1 | satisfied |
| (d) no `final`-path criterion in `blocked` / `deferred` / `fail` without a user waiver | `final_path`: 2 `pass`, 0 in every non-pass bucket (SC-001/SC-002) | satisfied |

**The four conditions hold, so the transition is granted.** The artifact and implementation segments are `blocked` on one P1 each (A1, I1); neither P1 is one of the four conditions, so they are carried to a bounded repair rather than holding the flip. **Named limitation L-1**: this run's commit is limited to the review artifacts, so the single registry write (`features.md` 027 `Last Updated` cell + `features.md` row status + `027-team-management.md` `## Latest Review` entry carrying this review's verdicts and the transition) is left to the driver's close-out and must land there before `/speckit.seal`.

## 3. Findings (Problems & Improvement Targets)

### F1 — The requirements template omits the execution-class mandatory section the gate requires

- **Severity**: P1
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/templates/requirements-template.md:184`
- **Evidence** (verbatim excerpt; intervening template sections elided with `...`):

  ```
  ## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*
  ...
  ## Clarifications
  ```

  (the template's heading list ends here; there is no `### Runtime Stack & Dependency Ownership`. The requirements gate refused this spec: `gate pre-analyze-check (requirements): FAIL — "requirements.md carries no § Runtime Stack & Dependency Ownership" (mandatory for execution-class)`; the author's own repair note reads `A-19 需求门禁修复（attempt 2）：按 execution 类必填补齐 ### Runtime Stack & Dependency Ownership`.)

- **Why it's a problem**: every `execution`-class requirements author must discover a mandatory section that the template does not carry and hand-copy the table from an older spec; the first attempt of this spec failed the gate for exactly that reason.
- **Proposed fix**: add the section skeleton (column names only, with a pointer to `shared/workflow/acceptance-hardening.md` § Runtime Stack & Dependency Ownership, zero value-domain literals) to `templates/requirements-template.md`, so the author fills rows instead of copying a template from another spec.

### F2 — DoD-1's named oracle cannot see FR→task-row citations

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/tasks.md:19`; oracle `/storage/project/cloud-native-ai/spec-kit/.qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py`
- **Evidence** (verbatim quote):

  ```
  - DoD-1: **FR lane 完整** — FR-001…FR-021 每条都被至少一个任务行按 `pre-analyze-check.py` 认可的形态引用（`- [ ] T<NNN>` 行内出现该 id；表格单元或散文不算）。Check: … 的 summary 中 `errors=0`。
  ```

  Measured: `pre-analyze-check --stage tasks` → `decision=pass errors=0 advisories=47`, summary `"fr": 21`; per-FR citation counts over the 44 rows: FR-018 = **0**, every other FR ≥ 2.
- **Why it's a problem**: the claim is machine-unbacked — the summary counts FR presence in the artifact set, not whether a task row cites each FR — so the gate stays green while the exact defect analyze E-02 predicted went to press in the feature detail (`every FR-001…FR-021 is quoted by at least one task row`).
- **Proposed fix**: make the check citation-sensitive when `--stage tasks` (each FR id must appear inside at least one `- [ ]`/`- [X]` row; emit an error when it does not), or replace DoD-1's named oracle with one that measures citations.

### F3 — The plan stage does not register the per-unit lifecycle surfaces a new skill needs

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/feature-ref.md:54-58`; source template `/storage/project/cloud-native-ai/spec-kit/templates/plan-template.md` § Mirror Obligations
- **Evidence** (verbatim quote):

  ```
  19. `shared/definitions/probe-definitions.md` (one `skill:view-team` wrap-up Object row) + its mirror … (added at the tasks stage, 2026-11-24 — a line-level completeness repair; required by `view-team-skill.contract.md` C-22, because `compile-embeds` gives the new skill a `## Wrap-up` embed and `probe-utils.py --action probes --reconcile` rejects an embed whose unit has no probe object)

  20. `shared/definitions/flow-class-definitions.md` (one `skill:view-team` per-unit ledger row; …) … Added at the implement stage, 2026-11-24 — a registry-completeness repair of the same class as item 19, not a new capability.
  ```

- **Why it's a problem**: the plan's Mirror Obligations table covers source→mirror/copies only; the two **per-unit registries** (`probe-definitions`, `flow-class-definitions`) are discovered one stage at a time and repaired under PLAN-EDIT. Every new skill/command unit will pay the same toll, and each repair mutates a plan-owned artifact mid-chain.
- **Proposed fix**: add a “New-unit registration” row to `templates/plan-template.md` § Mirror Obligations: whenever a new skill/command unit is delivered, the plan MUST name the probe Object row and the flow-class ledger row (and their mirrors) in the delivery surface.

### F4 — The installed CLI is the renamed `ai-harness`, so the framework's own 081 smoke fails and rewrites its tracked evidence

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `/storage/project/cloud-native-ai/spec-kit/tests/integration/test_acceptance_smoke.py:100`; environment `/usr/local/bin/specify`; record `/storage/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`
- **Evidence** (verbatim quotes):

  ```
  $ specify --version
  warning: 'specify' is the deprecated pre-rename alias of 'ai-harness' and will be removed in a future release; use 'ai-harness' instead.
  ai-harness-cli 0.0.22
  ```

  A temp probe of the exact smoke command (`specify init smoke-probe --ai claude --no-git --script sh --ignore-agent-tools`, cwd `<tmp>`) exits 0 but creates `smoke-probe/.ah/` and **no** `.specify/` tree. The 081 smoke asserts `.specify/` and its three member dirs, so it fails; because it writes its evidence **before** asserting, the tracked record was rewritten during this line's baseline full run:

  ```
  -  generated: .specify/.gitignore, .specify/agents, …
  +  generated: <none>
  ```

  `baseline-failed.txt:145` contains `tests/integration/test_acceptance_smoke.py::test_acceptance_smoke`.

- **Why it's a problem**: the 222-name baseline was measured against an installed CLI that is a different product name and container layout; the framework's canonical smoke is red there by construction, and a full-suite run silently mutates another spec's tracked evidence. The stage disclosed the file change but not its cause.
- **Proposed fix**: make `scripts/bash/run-tests.sh` (or a documented preflight in the driver) detect and report this skew before measuring (installed CLI name/version vs the tree's expected container); and have the 081 smoke resolve the generated container name from the CLI it invokes instead of hard-coding `.specify/`.

### F5 — The baseline full-suite exit code was destroyed by a capture pipeline

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/test-evidence/implement-baseline.txt:12-15`
- **Evidence** (verbatim quote):

  ```
  - rc: 1 — derived, not re-measured. The capture pipeline (`| tail -40`) masked the
    runner's own exit status (its exit was `tail`'s 0); the runner's documented exit rule
    ("exit code still reflects the passes' own results") plus the observed
    `222 failed` summary make pytest exit 1 the only consistent value. No second full
    suite was run to re-capture the code (the stage budget forbids one).
  ```

- **Why it's a problem**: the exit status is the primary reading every later gate compares against; a 65-second full-suite run paid its cost and then lost its most important signal because the stage piped stdout through `tail`. The derived value is honest and unambiguous here, but the same shape can silently invert a future reading (e.g. `| tee` before an `echo`).
- **Proposed fix**: give `scripts/bash/run-tests.sh` a documented `--log <path>` mode that captures the full output and preserves the runner's own exit code; state in the runner's help that piping its output discards the verdict.

### F6 — Stage-runner heartbeats carry no run attribution, so attributed watching sees NO_SIGNAL

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.qoder/skills/sdd-loop-driver/scripts/stage-runner.sh:231`; watcher `/storage/project/cloud-native-ai/spec-kit/.qoder/skills/sdd-loop-driver/scripts/watch-target.sh:417`
- **Evidence** (verbatim quotes):

  ```
  atomic_write "$hb" "at=$(now_epoch) line=$LINE stage=$STAGE event=heartbeat"
  ```

  ```
  printf '%s' "$1" | sed -n 's/.*[[:space:]]run=\([^[:space:]]*\).*/\1/p' | head -n 1
  ```

- **Why it's a problem**: the four-piece envelope (`pid`/`status`/`log`/`heartbeat`) has no `run=` field; a watcher given `--run-id` therefore classifies live stages as `unattributed`, and this line had to fall back to legacy single-active-line watching (recorded at U4 requirements in the state spine).
- **Proposed fix**: carry `run=$RUN_ID` in the heartbeat/status envelope (stage-runner already receives the line id) and, in `watch-target.sh`, accept a heartbeat's matching `line=` as an attributed signal when `run=` is absent.

### F7 — Analyze MEDIUM findings have no disposition record between analyze and implement

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/103-team-view/test-evidence/analyze-report.md:116`
- **Evidence** (verbatim quote):

  ```
  **Gate reading**: no CRITICAL/HIGH remains open, so `/speckit.implement` is not blocked by this report; the four MEDIUM items are routing decisions for the driver (tasks-stage repair vs implement-stage absorption). Would you like concrete remediation edits for the top N issues? (Not applied automatically.)
  ```

- **Why it's a problem**: the routing decision was never recorded. E-01 was absorbed (coverage baseline landed), F-02 was absorbed by P3, E-03 partially, but **E-02 was dropped** — and it predicted exactly the false claim A1 shipped. A MEDIUM without an explicit disposition disappears between stages.
- **Proposed fix**: require a one-line disposition table per MEDIUM+ finding in the analyze report (absorbed where / deferred with reason / rejected with reason), read at implement entry and carried into the feature detail note.

### F8 — The requirements template has no Assumptions section

- **Severity**: P2
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/templates/requirements-template.md` (heading list: `## Related Feature`, `## User Scenarios & Testing`, `## Requirements`, `## Success Criteria`, `## Shared Strings`, `## Clarifications`)
- **Evidence** (verbatim quote):

  ```
  ## Clarifications
  ```

  (no `## Assumptions & Decisions` heading exists in the template; this spec carries one with A-1…A-19, and the requirements-stage feedback recorded `create-requirements 加载的模板缺 Assumptions 节`.)

- **Why it's a problem**: the create-requirements procedure expects authors to record adjudicated assumptions, but the template gives them no home; each spec invents a section shape and the adjudications become less discoverable.
- **Proposed fix**: add an optional `## Assumptions & Decisions *(adjudicated here, not asked)*` section skeleton to `templates/requirements-template.md`.

## 4. What Worked — Preserve (Brief)

- The four-conjunctive-condition status gate plus the deterministic closure checker: ARC read `accept` with zero recomputation, and the implement gate's readings re-verify at review time.
- Red-first evidence with a disclosed false-green correction (`notes/red-first-evidence.md`): a missing program made three tests exit 2 coincidentally, the assertions were tightened, and the disclosure is in the record.
- Read-only proof by construction for the new mode: path+sha256 snapshots on success, `--json` and both error paths, plus a source-level scan for write calls.
- The mirror/copy generators (`sync-mirrors.py`, `regen-command-copies.py`): three scopes `ok`, four copies green, no hand-edited mirror.
- Two fresh plan-constraint audits with explicit PLAN-EDIT declarations: the plan-owned audit reads `classification=declared`, `undeclared=false`.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Carry the execution-class mandatory section in the requirements template** — Target: `templates/requirements-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/requirements-template.md`). Change: add the `### Runtime Stack & Dependency Ownership` skeleton (columns only, pointer to the owner) and an `## Assumptions & Decisions` section. Source: F1, F8. Expected impact: the first requirements attempt stops failing the execution gate; assumption adjudications land in a named place.
- **Register per-unit lifecycle surfaces at plan time** — Target: `templates/plan-template.md` § Mirror Obligations (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/plan-template.md`). Change: add a “New-unit registration” row naming the probe Object row and flow-class ledger row for every new skill/command unit. Source: F3. Expected impact: removes two mid-chain PLAN-EDITs per new-skill feature.

### 5.3 Automation / Script Improvements

- **Make the FR-lane oracle citation-sensitive** — Target: the driver's `pre-analyze-check.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/.qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py`). Change: when `--stage tasks`, error on any FR id that appears in zero `- [ ]`/`- [X]` rows. Source: F2, A1. Expected impact: DoD-1's claim becomes machine-checked instead of asserted.
- **Preserve the runner exit code under capture** — Target: `scripts/bash/run-tests.sh` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/scripts/bash/run-tests.sh`). Change: add `--log <path>` (full capture, own exit code preserved) and a help line that piping discards the verdict. Source: F5. Expected impact: stage gates read a measured rc, not a derived one.
- **Detect installed-CLI skew before measuring** — Target: `scripts/bash/run-tests.sh` preflight (or the driver's admission check). Change: compare the installed CLI name/container against the tree's expected container and warn; resolve the container in `tests/integration/test_acceptance_smoke.py` from the invoked CLI instead of hard-coding `.specify/`. Source: F4. Expected impact: the baseline and the framework's canonical smoke stop failing for an environment reason nobody names.
- **Carry `run=` in the stage envelope** — Target: `.qoder/skills/sdd-loop-driver/scripts/stage-runner.sh` + `watch-target.sh`. Change: heartbeat/status lines carry `run=$RUN_ID`; the watcher accepts matching `line=` as an attributed alternative. Source: F6. Expected impact: attributed watching stops misreading live stages as NO_SIGNAL.

### 5.4 Workflow Improvements

- **Require a MEDIUM+ disposition table at analyze exit** — Target: `shared/workflow/acceptance-hardening.md` § Gates or the analyze report template. Change: one line per MEDIUM+ finding (absorbed / deferred with reason / rejected with reason), read at implement entry. Source: F7. Expected impact: a predicted defect like E-02 cannot vanish between stages.

(No Command Prompt or Documentation recommendations this run — those sub-sections are dropped rather than left empty. No `REC-…` identifier is coined: each recommendation is carried by its target path and source finding ids, so the register has no new durable id to record from this report.)

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Carry the mandatory runtime-stack section (and an Assumptions section) in the requirements template | `templates/requirements-template.md` | F1, F8 |
| P1 | Register per-unit lifecycle surfaces at plan time | `templates/plan-template.md` § Mirror Obligations | F3 |
| P1 | Make the FR-lane oracle citation-sensitive | driver `pre-analyze-check.py` | F2, A1 |
| P1 | Preserve the runner exit code under capture | `scripts/bash/run-tests.sh` | F5 |
| P1 | Detect installed-CLI skew before measuring | `scripts/bash/run-tests.sh`; `tests/integration/test_acceptance_smoke.py` | F4 |
| P1 | Forward or explicitly refuse `--spec-dir` (feature repair) | `scripts/python/team-view.py` | I1 |
| P2 | Carry `run=` in the stage envelope | `stage-runner.sh` / `watch-target.sh` | F6 |
| P2 | Require a MEDIUM+ disposition table at analyze exit | `shared/workflow/acceptance-hardening.md` § Gates | F7 |
| P2 | Cite FR-018 on the syncing task rows; fix the feature-detail coverage sentence | `tasks.md`; `.specify/features/027-team-management.md` | A1 |
| P2 | Refresh the two retrospective counts | `plan.md:43,162` | A2 |
| P2 | Re-point the verification log's post-change commit | `verification.md:7` | A3 |
| P2 | Distinguish declared-but-empty config from undeclared | `scripts/python/team-view.py` | I2 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary); no `REC-…` identifier was coined, so no register entry is owed by this report.
- [x] Every finding in Section 3 carries a quoted excerpt that lets the reader judge the problem without opening the source file; the artifact and implementation findings quote their measured evidence in §2.2/§2.3.
- [x] No bullet says “see attached”, “as discussed earlier”, or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status stated explicitly: **No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.**

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
