# Specification-Driven Development (SDD) Process Review Report: 主动触发机制 (Proactive Flow Trigger)

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.
>
> **Reviewer disclosure**: the reviewing agent is the same agent that executed `/speckit.implement` for this feature. Every P0-grade claim was therefore dispatched to an independent read-only validator receiving only the finding and its anchored evidence. One finding was **downgraded** (F1, P0→P1) and one was **rejected outright** (see §3.1 Unvalidated Findings) — the validator showed the rejected claim rested on the narrowest possible reading of an ambiguous phrase and had overlooked that a relative pytest path makes the repository root follow the invocation tree.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 050 |
| Requirement Key | 050-proactive-flow-trigger |
| Requirement Name | 主动触发机制 (Proactive Flow Trigger) |
| Related Feature | 050 Proactive Flow Trigger(主动触发机制) — status `Implemented` |
| Repository | spec-kit |
| Repository URL | `git@github.com:github/spec-kit.git` (`remote.origin.url`) — **see F5: this is the upstream, not the fork that holds these commits** |
| Actual fork remotes | `github` → `git@github.com:cloud-native-ai/spec-kit.git`; also `gitee`, `gitlab` |
| Branch | 050-proactive-flow-trigger |
| Commit SHA | 6ca6de43f31bcddf1b25a5aec883acb525624cc8 (short: 6ca6de43) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-09-08 |
| Reviewer (Agent) | Qiming Liu (John) <john.liuqiming@linux.alibaba.com> |
| Environment | Linux 5.10.134-15.2.al8.x86_64 x86_64; Python 3.11.11; pytest 8.4.2 |
| spec-kit Source Snapshot | specify-cli 0.0.22 (installed wheel predates this branch; working tree is the source of truth here) |
| Reachability of COMMIT_SHA | **None** — `git branch -r --contains HEAD` returns empty; the branch was never pushed to any remote |

### Artifact Inventory

All paths relative to `/storage/project/cloud-native-ai/spec-kit/.specify/specs/050-proactive-flow-trigger/`.

| Artifact | Lines | Path | One-line Summary |
|----------|------:|------|-------------------|
| requirements.md | 328 | `requirements.md` | 26 FR / 15 SC / 4 user stories, four clarification rounds |
| plan.md | 247 | `plan.md` | Technical context, Constitution Check 13 Pass / 1 Partial (XIV), Phase 0 findings D-1…D-10, Mirror Obligations |
| data-model.md | 300 | `data-model.md` | 7 entities, 2 state machines, controlled vocabulary (13 situations / 9 stages / 12 signals), 32 validation rules V1…V6 |
| contracts/trigger-section.md | 48 | `contracts/trigger-section.md` | 12 clauses: instructions-section shape and full agent-path coverage |
| contracts/trigger-engine.md | 84 | `contracts/trigger-engine.md` | 23 clauses: engine envelope, closed CLI enumerations, per-turn semantics, promotion safety |
| contracts/seed-derivation.md | 49 | `contracts/seed-derivation.md` | 10 clauses: seed schema, provenance, drift detection |
| contracts/discipline-doc.md | 53 | `contracts/discipline-doc.md` | 16 clauses: discipline-doc sections and wording safety |
| quickstart.md | 269 | `quickstart.md` | 6 end-to-end walkthrough scenarios |
| feature-ref.md | 94 | `feature-ref.md` | Feature 050 binding and FR→contract mapping |
| checklists/requirements.md | 91 | `checklists/requirements.md` | 16/16 items complete |
| tasks.md | 393 | `tasks.md` | 51 tasks / 7 phases, DoD-1…DoD-8, GATE-1…GATE-8, plus an appended corrections section |
| verification.md | 138 | `verification.md` | SC-001…SC-015 status rows, baseline/post-change counters, deferred-task registry |
| baseline-failed.txt | 44 | `baseline-failed.txt` | Frozen name-level failure baseline (42 own + 1 externally attributed) |
| baseline-gates.json | 189 | `baseline-gates.json` | Frozen environment/gate values, 13-anchor precheck, external-attribution record |

## 1. Process Execution Timeline

Commits are story/task-grouped, so git history supports per-phase attribution; no degradation to working-tree reconstruction was needed for the implementation phase. The design phase, however, has **no commit trace at all** (see F2).

| # | Step / Event | Evidence | Deviation from prescribed flow? |
|---|--------------|----------|---------------------------------|
| 1 | `/speckit.requirements` + two clarification rounds | `requirements.md` internal date 2026-09-07; feedback entries `20260907T093812Z`, `20260907T115039Z`, `20260907T132729Z-speckit-clarify` | None, but **left uncommitted** |
| 2 | `/speckit.plan` | `plan.md` header: `**Branch**: 050-proactive-flow-trigger \| **Date**: 2026-09-07`; feedback entry `20260907T170938Z-speckit-plan` | None, but **left uncommitted** |
| 3 | `/speckit.tasks` | `tasks.md` 51 tasks; feedback entry `20260907T173807Z-speckit-tasks` | None, but **left uncommitted** |
| 4 | `/speckit.analyze` + authorized remediation | feedback entry `20260907T183023Z-speckit-analyze`; 37 findings, contract clauses 47→61 | None, but **left uncommitted** |
| 5 | **All of steps 1–4 committed in one lump by `/speckit.implement`** | commit `02e1b441` (2026-09-08 13:33) `docs(050-proactive-flow-trigger): commit design artifacts from requirements/clarify/plan/tasks/analyze runs`; `git log --diff-filter=A` shows requirements.md, plan.md, data-model.md, quickstart.md, contracts/*, checklists/* **all first added by this commit** | **Yes — F2** |
| 6 | Phase 1 Setup: baselines frozen | commit `9c84941f` (13:33); `baseline-failed.txt` 42 names; `baseline-gates.json` gates 23/0, probes 73, anchors 13/13 | None |
| 7 | Phase 2 Foundational: discipline doc RED→GREEN | commit `48e0f9ee` (13:45); 44 contract assertions; gate total held at 23 | None |
| 8 | Phase 3 US1: instructions section + 2 missing symlinks | commit `e1000fe9` (14:03); `_check_instructions` hermes/opencode `fail`→`pass` | **Discovered quickstart scenario 1's premise was false — F4** |
| 9 | Phase 4 US2: all 8 test files written RED, then the engine implemented once | commit `f6c74a5a` (15:23); 1480-line engine, 13-rule seed, 313 tests | **Yes, deliberate — F3** (consolidated the single-file engine instead of three scheduled edit cycles) |
| 10 | Mid-run governance change, separate commit | commit `61813fbf` (15:57) `docs(guidelines): add Ask-Record-Repeat philosophy and make the two-hats rule reachable` | Out-of-feature scope, correctly isolated |
| 11 | Phase 5 US3 walkthroughs delegated to three subagents | commit `a3b7ee67` (17:24); SC-005/006/009/010/15 evidence | None |
| 12 | Phases 6–7, Completion Gate, status flip | commit `2c726325` (23:24); 8 gates re-validated; DoD `green` with one annotated void clause | **Yes — F1** (invented a disposition the protocol does not define) |
| 13 | Wrap-up records | commit `6ca6de43` (23:32); glossary 77→81 terms, feedback recorded | None |
| 14 | One regression failure attributed externally | `baseline-failed.txt` header + `baseline-gates.json.externalAttribution`: a parallel session kept scaffolding git-ignored `.specify/skills/.migration-backups/layout-int-*` dirs during the run | Handled per the command's external-provenance axis |

Wall-clock span 13:33 → 23:32 with two user interruptions (an efficiency review at ~1h45m, then the governance-change request). The mechanical write gate required by `/speckit.implement` step 6 was first run in Phase 6 — four phases after it became applicable (**F6**).

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 6 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 |
| Command Prompt | 5 |
| Automation / Scripts | 0 |
| Workflow | 1 |
| Documentation | 1 |

No P0 survived validation. The single P0 candidate was downgraded to P1 (F1) because the validator established that three existing reason-recording channels make the state expressible in substance, and because `DoD Status` is parsed by no script and pinned by no contract test.

## 3. Findings (Problems & Improvement Targets)

### F1 — No disposition exists for a Definition-of-Done row whose premise is factually false

- **Severity**: P1 `(validated: downgraded from P0)`
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/tasks-template.md#L52`; `/storage/project/cloud-native-ai/spec-kit/.specify/templates/verification-log-template.md#L22`; instance at `/storage/project/cloud-native-ai/spec-kit/.specify/specs/050-proactive-flow-trigger/tasks.md` DoD-8 and §Implementation-Period Corrections C-1
- **Evidence** (verbatim):

  ```
  .specify/templates/tasks-template.md:52
  **DoD Status**: pending | green   <!-- flip to `green` only when every DoD-N row above is satisfied -->
  ```

  ```
  The DoD-8 row as originally generated (recoverable: git show f6c74a5a:.specify/specs/050-proactive-flow-trigger/tasks.md, line 24)
  - DoD-8: Tool 记录 `.specify/memory/tools/trigger-utils.py.md` 已建,且 `.specify/memory/tools.md` 与 `.specify/tools/*.json` 经 `refresh-tools.sh` **再生**(未手改派生清单)
  ```

  The `tools.md` half is unsatisfiable, verified independently by the validation subagent: `bash scripts/bash/refresh-tools.sh --json` prints usage and exits 1 (all three `QUERY_*` flags false ⇒ `usage`, script lines 278–280); no code in `scripts/`, `src/` or `.specify/scripts/` writes `.specify/memory/tools.md` by literal or fragment-built path; the file is a 1984-line MCP index whose `## System Binaries` / `## Shell Environment` / `## Project Scripts` sections (lines 1977/1980/1983) hold one description line each; and `git show 15b13dba:.specify/memory/tools.md` — the revision that added it — already had that exact structure, so the claim was never true rather than merely stale.

- **Why it's a problem**: `DoD Status` is binary and conditioned on *every* row being satisfied, so a row that cannot be satisfied leaves only two honest-looking options: report `green` while a row is unmet, or block a finished feature on an impossible requirement. The validator correctly notes the state is expressible in substance through adjacent channels (`waivers.md`, `[~]` + `<!-- deferred: -->`, the SC `deferred_reason` field), and that `DoD Status` is machine-parsed by nothing — so this is a vocabulary and fidelity defect rather than a corrupted state. It still cost real judgement mid-run: the disposition used here (record as **void**, annotate the `green` inline, surface prominently) was invented on the spot and is not reproducible by another agent.
- **Proposed fix**: In `.specify/templates/tasks-template.md`, widen line 52 to `**DoD Status**: pending | green | green-with-void` and add a one-line rule beneath the DoD list: a row whose premise is measurably false is **void**, not unmet — voiding requires cited measurement, an inline annotation on the DoD Status line, and (when the false premise lives in a framework artifact) a correction entry naming every surface that repeats it. Mirror the term in `.specify/templates/verification-log-template.md`'s status vocabulary so SC rows can express it too.

### F2 — Upstream commands leave the spec directory entirely uncommitted; only `/speckit.implement` cleans up

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md#L71` (the rule exists here and nowhere upstream); artifacts under `/storage/project/cloud-native-ai/spec-kit/.specify/specs/050-proactive-flow-trigger/`
- **Evidence** (verbatim):

  ```
  templates/commands/implement.md:71 (step 8)
  The spec dir MUST NOT be left *entirely* uncommitted when validation completes — an uncommitted
  implementation leaves no per-task audit trail and breaks `/speckit.review`'s git-based history
  reconstruction. Do not report the Definition of Done as "met" while the whole feature is uncommitted.
  ```

  ```
  $ git log --diff-filter=A --format='%h %ad %s' --date=format:'%m-%d %H:%M' -- .specify/specs/050-proactive-flow-trigger/requirements.md
  02e1b441 09-08 13:33 docs(050-proactive-flow-trigger): commit design artifacts from requirements...
  ```

  The same `02e1b441` commit is the first-add commit for `plan.md`, `data-model.md`, `quickstart.md`, every `contracts/*.md` and `checklists/requirements.md`. Yet `plan.md`'s own header reads `**Date**: 2026-09-07`, and four separate feedback entries (`…T093812Z-speckit-requirements`, `…T115039Z-speckit-requirements`, `…T132729Z-speckit-clarify`, `…T170938Z-speckit-plan`, `…T173807Z-speckit-tasks`, `…T183023Z-speckit-analyze`) show six upstream command runs across two days.

- **Why it's a problem**: The rule is enforced only at the *end* of the lifecycle, by the one command that did not create the risk. Five command runs produced ~1,200 lines of design artifacts that existed only in the working tree — one `git checkout`, one failed stash, or one parallel session away from loss. It also defeats the rule's own stated purpose: `/speckit.review`'s step-2 history reconstruction cannot attribute any design artifact to the command that produced it, because they all share one implement-phase commit. This review's §1 timeline had to reconstruct steps 1–4 from feedback-entry timestamps and internal document dates instead of commit traces.
- **Proposed fix**: Move the commit obligation upstream into each artifact-producing command (`templates/commands/requirements.md`, `plan.md`, `tasks.md`, `clarify.md`, `analyze.md`) as a wrap-up step alongside their existing Feedback and Documentation steps, each committing only its own artifact. Keep implement's step-8 sentence as the backstop, reworded to note that finding an uncommitted spec dir is itself a reportable upstream deviation.

### F3 — Two verification tasks claim the same test file with contradictory green points

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/050-proactive-flow-trigger/tasks.md#L150` and `#L177`; generator is `/storage/project/cloud-native-ai/spec-kit/templates/commands/tasks.md`
- **Evidence** (verbatim):

  ```
  tasks.md:150
  - [X] T027 [US2] 验证:`python3 -m pytest tests/contract/test_trigger_seed_derivation.py tests/contract/test_trigger_engine.py tests/unit/test_trigger_utils_units.py -q` 全绿 [blockedBy: T020,T024,T026]
  ```

  ```
  tasks.md:177
  - [X] T035 [US3] 验证:`python3 -m pytest tests/integration/test_trigger_promotion.py tests/integration/test_trigger_telemetry.py tests/contract/test_trigger_engine.py -q` 全绿(C-16…C-18 由 T017 已写就,此处随实现转绿) [blockedBy: T034]
  ```

  Both rows require `tests/contract/test_trigger_engine.py` to be **全绿** (fully green). T027 sits at the end of Phase 4 (US2); T035 sits at the end of Phase 5 (US3) and states in the same breath that clauses C-16…C-18 only "随实现转绿" (turn green with the implementation) *there*. Those clauses cover `record`, `reset` and `config` — actions T031/T032 implement in Phase 5.

- **Why it's a problem**: As written the pair is unsatisfiable in the prescribed order: at T027 the file cannot be fully green because three of its clauses test Phase-5 actions that do not exist yet, and at T035 T027 has already been signed off. The executing agent resolved it by front-loading the whole engine into Phase 4 against all eight RED test files, which satisfied both rows but was **not** the schedule `/speckit.tasks` produced (three separate edit-mirror-verify cycles for one file). That is a better outcome, yet it was reached by overriding the plan rather than by the plan being correct — the next agent may instead tick T027 against a partially-green file.
- **Proposed fix**: In `templates/commands/tasks.md`, add a generation rule: when one test file is named by verification tasks in more than one phase, its clauses must be partitioned across those tasks (each row naming the clause range it is responsible for), or the file must be assigned to a single phase with the later rows referencing it read-only. Add a self-check that flags any test path appearing in two verification rows with different green points.

### F4 — The quickstart's "cannot be executed yet" disclaimer covers only part of the file, implicitly vouching for the rest

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/050-proactive-flow-trigger/quickstart.md#L7`; generator is `/storage/project/cloud-native-ai/spec-kit/templates/commands/plan.md`
- **Evidence** (verbatim):

  ```
  quickstart.md:7
  > **CLI 示例的有效性钉桩**:引擎在本阶段尚未实现,故下列每条示例**无法被执行验证**。它们全部由
  > `contracts/trigger-engine.md` 的 C-9(action 封闭枚举,11 项)、C-10(flag 封闭集)、C-11(标识符格式)钉住,
  > 并由 `tests/contract/test_trigger_engine.py` 以"解析本文件代码块 → 逐条校验 action / flag / 标识符"
  > 的方式机械断言(见该契约末节)。
  ```

  The disclaimer is scoped to `引擎`(the engine) examples. Scenario 1's example was not an engine call and was therefore implicitly vouched for:

  ```
  quickstart.md scenario 1, as originally written
  TMP=$(mktemp -d) && cd "$TMP" && git init -q .
  specify init --here --ai qoder --force --ignore-agent-tools
  # ① 5 个声明文件(_INSTRUCTIONS_FILE_MAP 去重后的值)
  for p in CLAUDE.md AGENTS.md HERMES.md .github/copilot-instructions.md .opencode/instructions.md; do ...
  ```

  Executed during implementation, that produced: `init exit_code : 0`, the template and discipline doc shipped byte-identical — and `.specify/instructions.md` **did not exist**, all 8 symlinks `MISS`, `_check_instructions` `fail` for all six tool keys. `src/specify_cli/__init__.py` contains no generator invocation at all; its only mention of the file (line 985) is an entry in the `_CORE_SPECIFY_ASSETS` preservation list.

- **Why it's a problem**: A precise, well-reasoned disclaimer about one class of examples created false confidence about the others. The failure mode is expensive because it *looks* like an implementation defect: an agent following scenario 1 would see 8 MISS results against a contract demanding 8 OK and start debugging correct code. It cost four investigation calls to attribute, and the correction had to be written back into the artifact (`quickstart.md` now carries an `实现期订正` block).
- **Proposed fix**: In `templates/commands/plan.md`'s quickstart generation guidance, require that every scenario's commands be **executed at authoring time** wherever the tooling already exists, and that any example which could not be executed carry its own per-example marker rather than relying on a file-level disclaimer. Where an example depends on a multi-step pipeline (`init` then `/speckit.instructions`), the scenario must show every step — a scenario that omits a required step is wrong even when each shown command works.

### F5 — The review report's own portability mechanism produces unresolvable citations in a fork

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `/storage/project/cloud-native-ai/spec-kit/templates/commands/review.md` (step 1 "capture REPO_URL"; step 5 and the Goal section requiring `{REPO_URL}@{COMMIT_SHA}` references); template `/storage/project/cloud-native-ai/spec-kit/.specify/templates/review-template.md#L28` and `#L77`
- **Evidence** (verbatim):

  ```
  templates/commands/review.md, Goal section
  1. Be readable standalone — embedded evidence, absolute paths or `{REPO_URL}@{COMMIT_SHA}` references
  ```

  ```
  .specify/templates/review-template.md:77
  - **Location**: [ABS_PATH or [REPO_URL]/blob/[COMMIT_SHA_FULL]/relative/path#Lstart-Lend]
  ```

  Measured on this repository:

  ```
  $ git config --get remote.origin.url
  git@github.com:github/spec-kit.git
  $ git config --get remote.github.url
  git@github.com:cloud-native-ai/spec-kit.git
  $ git branch -r --contains HEAD
  (empty)
  ```

- **Why it's a problem**: `origin` is the **upstream** project, not the fork where this work lives, and `COMMIT_SHA` is not reachable from any remote. A citation rendered as `git@github.com:github/spec-kit.git/blob/6ca6de43…/tasks.md#L52` resolves to a repository that does not contain that commit — the report would look self-contained and be silently unresolvable, which is worse than an obviously-local path. The template offers `blob/` URL syntax that also assumes an HTTPS web remote; all four remotes here are SSH. This report therefore uses absolute paths plus git-recoverable references (`git show <sha>:<path>`) throughout, which is a workaround the command does not sanction.
- **Proposed fix**: In `templates/commands/review.md` step 1, capture **all** remotes plus the push-tracking branch, and run `git branch -r --contains HEAD`; when that is empty, the command must state in §0 that commit-anchored citations are unresolvable and fall back to absolute paths with `git show <sha>:<path>` recovery instructions. In `.specify/templates/review-template.md`, add a `Reachability of COMMIT_SHA` row (this report added one ad hoc) and make the `Location` field's fallback order explicit: absolute path first, URL only when the commit is confirmed pushed.

### F6 — The mechanical write gate is per-phase-optional and its omission is undetectable

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md#L51` (step 6, "Mechanical write gate"); gate definition `/storage/project/cloud-native-ai/spec-kit/.specify/gate.yaml`
- **Evidence** (verbatim):

  ```
  templates/commands/implement.md, step 6
  - **Mechanical write gate**: if `.specify/gate.yaml` exists, run
    `python3 .specify/scripts/python/gate-check.py <planned-write-paths>` before each phase's edits.
    Exit 2 (DENY) → do NOT write, report the rule and escalate; exit 1 (CONFIRM) → ask the user
    before writing; exit 3 (gate unreadable) → surface the problem, do not silently proceed.
    The gate verdict is mechanical — never argue around it in prose.
  ```

  `.specify/gate.yaml` has existed since commit `4b836652` and its `confirm` list includes `.specify/memory/constitution.md` and `pyproject.toml`. In this run the gate was first invoked during Phase 6 — four phases and roughly 5,900 authored lines after it became applicable. Retroactive checking showed every path written would have returned `allow`, so the outcome was harmless.

- **Why it's a problem**: A gate whose invocation depends on the agent remembering it each phase is a gate that gets skipped on the phase where it matters. Nothing in the run's observable output distinguishes "gate ran and allowed" from "gate never ran", so the omission is invisible to the progress report, to `/speckit.review`, and to any later reader. Had a phase targeted the constitution — which this run came close to, since the user's request was initially framed as adding three principles — the write would have happened first and the `confirm` requirement been discovered afterwards.
- **Proposed fix**: In `templates/commands/implement.md` step 6, require the gate verdict to be **echoed in the phase's first progress report** (paths checked, exit code, any `confirm`/`deny` rows), making omission visible in the artifact trail. Strengthen further by having step 7's evidence-backed-closure gate treat a phase with no recorded verdict as unclosed.

### F7 — The verification log's status vocabulary is wider than the DoD row that consumes it

- **Severity**: P2
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/verification-log-template.md#L22` and `#L52` versus the generated `DoD-7` row in `/storage/project/cloud-native-ai/spec-kit/.specify/specs/050-proactive-flow-trigger/tasks.md#L23`
- **Evidence** (verbatim):

  ```
  .specify/templates/verification-log-template.md:22
  - `status` is one of: pass | fail | partial | deferred | unknown.
  ```

  ```
  tasks.md:23 (as generated)
  - DoD-7: `verification.md` 为 **SC-001…SC-015** 逐条记录 `pass` 或 `deferred`(附因)
  ```

- **Why it's a problem**: The template invites five values; the DoD row accepts two. An agent following the template honestly will at some point write `partial` — which is the *most accurate* value for a criterion whose mechanical half passes and whose specified measurement condition was not met — and then fail DoD-7. That is exactly what happened here: SC-011 was first recorded `partial` and had to be reclassified to `deferred` during the Completion Gate pass. The reclassification was defensible (the criterion's stated condition genuinely was not met) but it was a judgement call forced by a vocabulary mismatch, not by the evidence.
- **Proposed fix**: Reconcile the two owners. Either narrow `.specify/templates/verification-log-template.md` line 22 to the values DoD rows accept, or — better — have `templates/commands/tasks.md` generate DoD-7 from the template's actual vocabulary rather than restating a subset, so the two cannot drift. Add a one-line note in the template that `partial` must still satisfy whatever the consuming DoD row admits.

### F8 — A false operational claim propagated to seven surfaces and no test asserts it

- **Severity**: P2
- **Category**: Documentation
- **Location**: owner `/storage/project/cloud-native-ai/spec-kit/shared/definitions/tool-definitions.md#L36`; copies at `templates/instructions-template.md#L132`, `templates/tools.md#L14`, `templates/commands/tools.md#L103`, `skills/create-tools/SKILL.md#L65`, `skills/improve-tools/SKILL.md#L53`, and the generated `.specify/instructions.md#L147`
- **Evidence** (verbatim):

  ```
  shared/definitions/tool-definitions.md:36
  Note also: `.specify/memory/tools.md` (singular file) is the **discovery inventory** regenerated by
  `refresh-tools.sh`; `.specify/memory/tools/` (directory) holds the **definition records**.
  Only the directory is authoritative.
  ```

  ```
  templates/instructions-template.md:132   (identical claim, ambient — every agent loads it)
  Note also: `.specify/memory/tools.md` (file) is the discovery inventory regenerated by
  `refresh-tools.sh`; `.specify/memory/tools/` (directory) holds the authoritative definition records.
  ```

  Measured false four ways (see F1's evidence): the script exits 1 standalone, nothing writes the file, the file is an MCP index, and it was born that way.

- **Why it's a problem**: This is Principle XIV's rule of thumb failing loudly rather than quietly — correcting one fact requires editing six framework files. It survived because the claim is *prose about a mechanism*, and no contract test asserts that a documented regeneration actually occurs; the drift-detection pattern this very feature built for seed provenance (open the named source, assert the claimed content is still there) is precisely the missing guard. Because one copy is ambient, every agent inherits the false model, and two agents this run acted on it: `/speckit.tasks` generated DoD-8 from it (F1) and the implementing agent tried the documented command and had to diagnose why it failed.
- **Proposed fix**: Fix the owner (`shared/definitions/tool-definitions.md` §on discovery) to state the real mechanism — `.specify/tools/{system,shell,project}.json` are the regenerated inventories, written by `generate-instructions.sh:39-41`; `.specify/memory/tools.md` is a hand-maintained MCP index — then convert the other six surfaces to pointer-shaped references. Add a contract test asserting that every path a doc names as "regenerated by X" is actually written by X, which is the general guard this class of drift needs.

### F9 — Shell-hygiene guidance covers alias traps but not exit-code traps in verification chains

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md#L55` (step 6, "Shell hygiene (alias-proof)")
- **Evidence** (verbatim):

  ```
  templates/commands/implement.md, step 6
  - **Shell hygiene (alias-proof)**: destructive/mirror file operations MUST use alias-proof forms
    (`\rm -f`, `\cp -f`, or `command rm/cp`) and MUST verify the result afterwards (`ls` / `diff -q`) —
    interactive aliases (`rm -i`, `cp -i`) silently swallow non-interactive deletes/copies while
    appearing to succeed.
  ```

  Observed in this run: a verification chain of the form `… && grep -c 'telemetry.jsonl' <staged-list> && git commit -q -m "…"` printed `0` for the grep and then stopped. `grep -c` exits 1 when the count is zero, so the `&&` chain aborted **before the commit**. The intended check passed (the count legitimately was 0) and the failure was silent — no error, just a missing commit discovered on the next `git log`.

- **Why it's a problem**: The existing bullet addresses commands that *appear to succeed while doing nothing*. This is the mirror image: a command that *succeeds semantically* while aborting everything after it. Both are silent, and both are common in verification chains, which by nature test for absence and therefore routinely produce zero counts.
- **Proposed fix**: Extend the same bullet in `templates/commands/implement.md` with one clause: in an `&&` chain, never place a command whose legitimate result is a zero count or empty match (`grep -c`, `grep -q`, `comm`, `diff -q`) before a command that must run; use `;` or an explicit `|| true`, and verify the chain's tail actually executed.

## 3.1 Unvalidated Findings

Per `/speckit.review` step 4.5, rejected findings are recorded here rather than silently dropped.

### R1 — "T045 is unexecutable as written" — REJECTED by independent validation

- **Claimed severity**: P1 · **Category**: Command Prompt · **Location**: `tasks.md#L218`
- **Claim as diagnosed**: T045 tells the agent to edit a `## Handoffs` section "在临时副本上" (on a temporary copy) yet then to "恢复原文件" (restore the original file), which was read as contradictory; and because `tests/contract/test_trigger_seed_derivation.py` resolves `ROOT = Path(__file__).resolve().parents[2]`, a temporary copy of a single template file was claimed to be invisible to the test, making the required failure unobservable.
- **Validator verdict**: `reject`. Quoting the validator: *"「临时副本」has a coherent reading — a throwaway copy/worktree of the **repo**, not a loose copy of one file — under which 「恢复原文件」 is exactly consistent… That is not hypothetical: `verification.md:61` records that the experiment ran in a throwaway `git worktree` at /tmp/drift-exp."* On the second half: *"the row's pytest argument is itself a **relative** path, so ROOT follows the tree you invoke from. Copy/worktree the repo, edit that tree's template, run the same command there: the executed test's `__file__` is inside the copy and C-7 fails with ruleId + `provenance.file` + `missing flow` (lines 252–262 emit precisely those three)."*
- **Why it is retained here**: the claim was wrong on both halves, and the reason it looked plausible is itself worth recording — the diagnosing agent had just *used* a full worktree to perform the experiment, then described the task row as if it prescribed a single-file copy. The validator also noted the narrow reading makes `恢复原文件` vacuous, which is internal evidence against that reading. **Residual, at most a wording nit**: `临时副本` could be written `临时仓库副本(worktree)` to foreclose the narrow reading. Not carried as a finding.

## 4. What Worked — Preserve (Brief)

- **Name-level regression baselines** (`run-tests.sh --names-out` + `comm -13`) made "zero new failures" a mechanical claim at six phase boundaries instead of count archaeology; the frozen 42-name baseline plus one externally-attributed entry stayed meaningful across ten hours and two interruptions.
- **The external-provenance attribution axis** in implement step 6 let a parallel session's git-ignored scaffolding be recorded as evidence rather than consuming the retry budget or being "fixed" by deleting another session's work.
- **Frozen-value references instead of hardcoded literals** — gates compared against `baseline-gates.json` rather than `23`, so the assertion survives legitimate project-side movement.
- **Contract-per-file test layout** preserved `[P]` parallel eligibility across four stories and kept one 1,480-line engine from serializing four test files.
- **Provenance-bearing derived data plus drift detection** proved its worth: the guard was demonstrated live for both anchor kinds with a negative control, so "not vacuously true" is now evidenced rather than assumed.
- **The five mechanical Pre-Status-Flip Gate checks** turned a status advance into something auditable, and caught that `deferred_tasks=` needed registering.
- **Independent validation of findings** (step 4.5) changed the report materially: one downgrade with two citation-scope corrections, one outright rejection. On a self-review this is the only thing standing between evidence and self-justification.
- **Delegation of walkthroughs** kept hundreds of lines of command output out of the review agent's context while returning measured digests; two subagents strengthened their briefs unprompted (pre-loading a counter before corrupting state; measuring after every one of 60 appends).

## 5. spec-kit / SDD Improvement Recommendations

Targets are given as absolute paths because the `{REPO_URL}@{COMMIT_SHA}` form is unresolvable for this branch (F5). All live in the framework source tree, so per the two-hats rule they must be edited there and ride publish → install → init; editing the `.specify/` copies would not reach any downstream project.

### 5.1 Template Improvements

- **Add a `void` disposition to DoD Status** — Target: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/tasks-template.md#L52`. Change: widen to `pending | green | green-with-void`, and add a rule that voiding a row requires cited measurement, an inline annotation, and a correction entry naming every surface repeating the false premise. Source: F1. Expected impact: removes the fudge-or-block dilemma whenever a generated DoD row inherits a false claim from framework docs.
- **Reconcile the SC status vocabulary with DoD-7** — Target: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/verification-log-template.md#L22` and `#L52`. Change: either narrow the vocabulary or make `templates/commands/tasks.md` derive DoD-7 from it. Source: F7. Expected impact: an honest `partial` no longer fails the DoD, removing a forced reclassification judgement call.
- **Add a commit-anchored-reachability row to the review template** — Target: `/storage/project/cloud-native-ai/spec-kit/.specify/templates/review-template.md#L28`. Change: add `Reachability of COMMIT_SHA` and make the `Location` fallback order explicit at `#L77` (absolute path first; URL only when the commit is confirmed pushed). Source: F5. Expected impact: review reports stop emitting citations that look portable and are not.

### 5.2 Command Prompt Improvements

- **Move the spec-dir commit obligation upstream** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/commands/{requirements,plan,tasks,clarify,analyze}.md`, wrap-up section beside their existing Feedback and Documentation steps. Change: each command commits its own artifact; keep `templates/commands/implement.md#L71` as backstop, reworded so that discovering an uncommitted spec dir is itself a reportable upstream deviation. Source: F2. Expected impact: design artifacts gain per-command audit trails, and `/speckit.review` step 2 can reconstruct the design phase from commits instead of feedback timestamps.
- **Partition test files claimed by two phases** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/commands/tasks.md`. Change: add a generation rule that a test path appearing in verification rows of more than one phase must have its clauses partitioned per row, plus a self-check flagging the collision. Source: F3. Expected impact: removes unsatisfiable acceptance pairs for single-file components shared by several stories — a shape that recurs whenever a house engine serves multiple stories.
- **Require per-example execution marking in quickstart scenarios** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/commands/plan.md`, quickstart guidance. Change: execute every scenario whose tooling already exists at authoring time; mark any unexecuted example individually rather than under one file-level disclaimer; require multi-step pipelines to show every step. Source: F4. Expected impact: prevents walkthroughs that fail for reasons unrelated to the implementation and get misattributed to it.
- **Make the write gate's verdict part of the phase record** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md#L51`. Change: require the gate verdict (paths, exit code, any confirm/deny rows) to be echoed in the phase's first progress report, and have step 7 treat a phase with no recorded verdict as unclosed. Source: F6. Expected impact: converts an easily-skipped instruction into an observable artifact.
- **Extend shell hygiene to exit-code traps** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md#L55`. Change: one clause forbidding zero-count-capable commands (`grep -c`, `grep -q`, `comm`, `diff -q`) before a must-run command in an `&&` chain. Source: F9. Expected impact: prevents silently skipped commits and verifications.
- **Capture all remotes and push state in review step 1** — Target: `/storage/project/cloud-native-ai/spec-kit/templates/commands/review.md`, step 1. Change: record every remote plus the tracking branch, run `git branch -r --contains HEAD`, and when empty declare citations unresolvable and fall back to absolute paths with `git show <sha>:<path>` recovery. Source: F5. Expected impact: the report's self-containment claim becomes true rather than aspirational, especially in forks — the common case for this project.

### 5.3 Automation / Script Improvements

- **Assert that documented regeneration actually happens** — Target: new contract test beside `/storage/project/cloud-native-ai/spec-kit/tests/contract/test_one_source_of_truth.py`. Change: for every documentation claim of the form "`<path>` is regenerated by `<script>`", assert the script (or its documented caller) writes that path. Source: F8. Expected impact: this is the general guard for the class of drift that produced F1, F8 and the seven-surface propagation; the seed-provenance drift test built in this feature is the working precedent for its shape.
- **Have `refresh-tools.sh` fail loudly on a no-source invocation, or accept a default** — Target: `/storage/project/cloud-native-ai/spec-kit/scripts/bash/refresh-tools.sh#L278-L280`. Change: either document the required source flag in the usage text as mandatory-with-no-default more prominently, or support a bare `--json` meaning "all three sources", since three separate documents describe the bare invocation. Source: F8, F1. Expected impact: removes the trap that made DoD-8 unsatisfiable.

### 5.4 Workflow Improvements

- **Treat an uncommitted upstream artifact as a lifecycle defect, not a cleanup task** — Target: `/storage/project/cloud-native-ai/spec-kit/.specify/shared/workflow/feature-integration.md`. Change: add to the integration protocol that each phase-transition command is responsible for committing the artifact it produced, so the spec dir is never wholly uncommitted between phases. Source: F2. Expected impact: the risk window shrinks from "the whole design phase" to "one command run".
- **Record the void-clause disposition as a house pattern** — Target: `/storage/project/cloud-native-ai/spec-kit/.specify/shared/workflow/feature-integration.md` §Pre-Status-Flip Gate. Change: add a sixth check — any DoD row reported void must carry measurement and an annotation, and a void row does not by itself block the flip but must be surfaced in the wrap-up. Source: F1. Expected impact: the next agent inherits a disposition instead of inventing one under time pressure.

### 5.5 Documentation Improvements

- **Correct the `tools.md` claim at its owner and convert six copies to pointers** — Target: owner `/storage/project/cloud-native-ai/spec-kit/shared/definitions/tool-definitions.md#L36`; copies at `templates/instructions-template.md#L132`, `templates/tools.md#L14`, `templates/commands/tools.md#L103`, `skills/create-tools/SKILL.md#L65`, `skills/improve-tools/SKILL.md#L53`. Change: state the real mechanism (`.specify/tools/{system,shell,project}.json` regenerated via `generate-instructions.sh:39-41`; `.specify/memory/tools.md` is a hand-maintained MCP index), then reduce each copy to a pointer. Source: F8, F1. Expected impact: stops propagating a false operational model to every agent through the ambient surface, and removes the false premise that made DoD-8 unsatisfiable.
- **Document the two-step initialization pipeline** — Target: `/storage/project/cloud-native-ai/spec-kit/docs/tutorials/quickstart.md` and `docs/reference/cli/`. Change: state plainly that `specify init` distributes resources but does not render `.specify/instructions.md` or create any symlink, and that `/speckit.instructions` (running `generate-instructions.sh`) is the required second step. Source: F4. Expected impact: this is the single most likely first-run stumble for a new user, and it currently appears nowhere outside feature 050's corrected scenario 1.

## 6. Priority Roadmap

| Order | Action | Findings | Effort | Rationale |
|------:|--------|----------|--------|-----------|
| 1 | Correct the `tools.md` claim at its owner and reduce six copies to pointers | F8, F1 | S | It is ambient, it is false, and it already generated an unsatisfiable DoD row. Every future feature inherits it. |
| 2 | Add the `void` disposition to DoD Status and to the flip gate | F1 | S | Small template edit; removes a fudge-or-block dilemma that will recur wherever docs and reality disagree. |
| 3 | Move the spec-dir commit obligation upstream into the five artifact-producing commands | F2 | M | Highest structural payoff: restores per-command audit trails and makes `/speckit.review` step 2 work as designed. |
| 4 | Capture all remotes and push-reachability in review step 1; add the template row | F5 | S | Restores the truth of the report's own self-containment promise; this project is a fork, so it applies every time. |
| 5 | Partition test files claimed by two phases in `/speckit.tasks` | F3 | M | Recurs for any single-file engine serving multiple stories — the house's dominant engine shape. |
| 6 | Require per-example execution marking in quickstart scenarios; document the two-step init pipeline | F4 | M | Prevents misattributed implementation failures and the most likely first-run stumble. |
| 7 | Make the write-gate verdict part of the phase record | F6 | S | Cheap; converts an easily-skipped instruction into an observable artifact. |
| 8 | Reconcile the SC status vocabulary with DoD-7 | F7 | S | Removes a forced reclassification judgement call. |
| 9 | Extend shell hygiene to exit-code traps; make `refresh-tools.sh` bare `--json` loud or defaulted | F9, F8 | S | Two small guardrails against silent no-ops. |

## 7. Self-Containment Check

- Every finding quotes its evidence inline, with file and line anchors. ✅
- All locations are absolute paths, because `{REPO_URL}@{COMMIT_SHA}` is unresolvable for this branch: `remote.origin.url` is the upstream `git@github.com:github/spec-kit.git` and `git branch -r --contains HEAD` is empty (F5). Git-recoverable references (`git show <sha>:<path>`) are given where a since-edited line is cited. ✅
- No reliance on local-only resources beyond the repository itself; the two ephemeral walkthrough roots (`/tmp/…`) are named only as provenance and no finding depends on their contents. ✅
- Findings are process-scoped: none judges whether proactive triggering is a worthwhile feature. ✅
- Rejected finding retained in §3.1 rather than dropped. ✅
- Validation status is visible on every affected row: F1 carries `(validated: downgraded from P0)`; R1 carries the validator's `reject` with quoted reasoning. ✅
- Known limitation, stated rather than hidden: the reviewer executed the implementation under review. Mitigations were independent validation of the P0 candidate and of one strong P1, and preferring evidence anchored on files this run did not edit (`templates/`, `.specify/templates/`, `src/`) over files it did.

## 8. Feedback

Recorded separately via the feedback engine at wrap-up (`unit_id=/speckit.review`, `scope: local`), covering this review run's own operation rather than the project-wide assessment above.
