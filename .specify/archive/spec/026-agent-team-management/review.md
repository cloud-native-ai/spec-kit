# Specification-Driven Development (SDD) Process Review Report: Agent Team Management

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 026 |
| Requirement Key | 026-agent-team-management |
| Requirement Name | Agent Team Management |
| Related Feature | 027 Team Management |
| Repository | spec-kit |
| Repository URL | https://github.com/github/spec-kit (configured remote: `git@github.com:github/spec-kit.git`) |
| Branch | 026-agent-team-management |
| Commit SHA | 51b91aa6301e8b960d0661f70afc19e10798d771 (short: 51b91aa) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-07-13 |
| Reviewer (Agent) | Qoder SDD review agent (for Qiming Liu / John) |
| Environment | Linux; /bin/bash; Python >=3.8; pytest (markers `contract`/`integration`); Node fallback shell |
| spec-kit Source Snapshot | This repo IS spec-kit — `specify-cli` version 0.0.22 @ commit 51b91aa (working tree DIRTY: feature artifacts staged/untracked, not committed) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 171 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/requirements.md | FR-001…FR-017, SC-001…SC-007, Shared Strings, clarifications |
| plan.md | 240 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/plan.md | Filled plan (L1–114) **plus a full unfilled template appended (L115–240)** |
| data-model.md | 119 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/data-model.md | Team/TeamMember/TeamConfiguration + `.team.md` schema + template-relocation table |
| tasks.md | 220 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/tasks.md | 33 tasks (T001–T033) across 6 phases, all marked `[X]` |
| quickstart.md | 68 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/quickstart.md | create → modify → run walkthrough + separation checks |
| verification.md | 68 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/verification.md | Baseline/post-change counters + SC-001…SC-007 pass records |
| feature-ref.md | 21 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/feature-ref.md | Requirement 026 ↔ Feature 027 linkage record |
| checklists/requirements.md | 39 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/checklists/requirements.md | Spec quality checklist (all boxes ticked) |
| contracts/team-command-contract.md | 48 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/contracts/team-command-contract.md | `/speckit.team` 3-mode + run preview→confirm gate |
| contracts/create-team-skill-contract.md | 50 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/contracts/create-team-skill-contract.md | create-team inputs/outputs |
| contracts/improve-team-skill-contract.md | 43 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/contracts/improve-team-skill-contract.md | improve-team targeted-edit contract |
| contracts/team-migration-contract.md | 63 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/contracts/team-migration-contract.md | M1–M7 rename/extract/relocate + guard tests |

## 1. Process Execution Timeline

Reconstructed from artifact self-reports and working-tree/`git` state (see Deviation column — the intended git-based reconstruction was **not possible** because the feature was never committed).

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | `/speckit.requirements` + `/speckit.clarify` | checklists/requirements.md: `**All clarifications resolved** in Session 2026-07-13`; requirements.md § Clarifications lists 3 Q&A | None |
| 2 | `/speckit.plan` (Phase 0/1) | plan.md L1–114 filled; data-model.md, contracts/, quickstart.md, feature-ref.md present | **Yes** — plan.md L115–240 is the raw unfilled template appended after the real plan (see F3) |
| 3 | `/speckit.tasks` | tasks.md T001–T033, `**Tests Mode**: ON` | None |
| 4 | `/speckit.implement` | tasks.md all `[X]`; verification.md `implementation_date=2026-07-13`, `post_change_commit=working-tree` | **Yes** — no commit produced; `git log -- <spec dir>` returns empty (see F5) |
| 5 | Guard-suite run | verification.md: `Guard suite: the 10 Feature-027 M7/US test files … all pass (79 passed)` | Partial — guard scope narrower than the SC-004 claim it certifies (see F1) |
| 6 | Self-declared DoD | tasks.md: `**DoD Status**: met` | **Yes** — DoD-3/DoD-6 not actually met in active tree (see F1, F2, F6) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 2 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 2 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 1 |
| Automation / Scripts | 4 |
| Workflow | 3 |
| Documentation | 0 |

## 3. Findings (Problems & Improvement Targets)

### F1 — "Zero dangling references" (SC-004) is certified by a guard whose scope is narrower than the criterion it verifies

- **Severity**: P0
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_no_organize_agents_refs.py and /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/verification.md
- **Evidence** (verbatim quote):

  verification.md certifies:
  ```
  post_change_organize_agents_active_refs=0
  SC-004_value=git grep organize-agents across active tree = 0 (was 42 across 10 files); tests/contract/test_no_organize_agents_refs.py green
  ```
  But the guard deliberately narrows "active tree":
  ```
  ACTIVE_DIRS = ["skills", "templates", "docs", "agents", "src", "memory"]
  Deliberately excluded:
    - `tests/` — test modules reference the literal string in assertions (like this one).
    - `.specify/` — runtime mirror (regenerated on install) ...
  ```
  A repo-wide search over active, non-spec-archive paths still finds live references:
  ```
  .specify/memory/features.md:1
  .specify/memory/features/019.md:1
  .specify/memory/features/027.md:5
  .specify/skills/organize-agents/SKILL.md:5
  tests/scenarios/agents-command/single-entry-routing-scenario.md:13
  ```

- **Why it's a problem**: SC-004's own wording requires zero references in "documentation, registries, skill bodies, symlinks". `.specify/memory/features.md` IS a registry and `tests/scenarios/.../single-entry-routing-scenario.md` IS an active (non-archived) test asset — both are excluded by the guard's `ACTIVE_DIRS`, so the guard reports green while the criterion is unmet. The verification record then over-certifies (`=0`) a claim that is false at the SC-004 scope. This is exactly the "drift risk / single-source-of-truth" failure the review is meant to catch.
- **Proposed fix**: Either (a) tighten the guard in test_no_organize_agents_refs.py to also scan `.specify/memory/` and `tests/scenarios/` (allow-listing only files that must retain the literal, e.g. the guard test itself), or (b) amend SC-004 in the requirements template to define "active tree" precisely and list the excluded paths, so the certified scope and the criterion match. Prefer (a).

### F2 — Task T026 marked `[X]` Closed but the edit was never performed; nothing in the process detects it

- **Severity**: P0
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/tasks.md and /storage/project/cloud-native-ai/spec-kit/tests/scenarios/agents-command/single-entry-routing-scenario.md
- **Evidence** (verbatim quote):

  tasks.md claims the scenario was updated:
  ```
  - [X] T026 [P] [US3] Update `tests/scenarios/agents-command/single-entry-routing-scenario.md` — remove team routing from the `/speckit.agents` scenario
  ```
  tasks.md defines `[X]` as:
  ```
  - `- [X]` — **Closed**. Fully executed and verified.
  ```
  But the file still routes team operations to the old skill (13 occurrences), e.g.:
  ```
  138:- I3: "Organize a parallel dispatch of three reviewers" → orchestration / organize-agents
  179:- [ ] Organize (parallel / serial / team-loop) routes to `organize-agents`
  180:- [ ] Execute (team / loop) routes to `organize-agents`
  ```

- **Why it's a problem**: A task sigil that means "Fully executed and verified" was applied to work that was not done. Because the SC-004 guard (F1) excludes `tests/`, no automated gate catches the omission, and this same scenario contradicts FR-003/SC-002 (team ops must NOT be served by `/speckit.agents`). Trusting `[X]` becomes unsafe, which undermines the whole tasks-tracking discipline.
- **Proposed fix**: In `.specify/templates/commands/implement.md` (and/or `tasks.md` template), require each `[X]` closure to cite the verifying evidence (test id, grep result, or diff) and add a lightweight closeout check that greps for each task's named target file before allowing DoD "met". Then actually perform T026 and re-run.

### F3 — `/speckit.plan` left the entire unfilled plan template appended after the real plan

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/plan.md#L115-L240
- **Evidence** (verbatim quote):

  The real plan ends at L114, then the raw template restarts with placeholder tokens:
  ```
  114:N/A — no Constitution Check violations.
  115:# Implementation Plan: [SPEC]
  116:
  117:**Branch**: `[###-spec-name]` | **Date**: [DATE] | **Spec**: [link]
  ...
  167:| I | [PRINCIPLE_1_NAME] [NON-NEGOTIABLE?] | ✅ Pass / ❌ Fail / ⚠ Partial | [one-line evidence: file or section] |
  ```

- **Why it's a problem**: The plan artifact contains two `# Implementation Plan` headings and a full block of `[PLACEHOLDER]` tokens — an internally contradictory, half-template document. Downstream readers (and any tool that parses plan sections) see duplicated/placeholder content; it is a concrete drift/boilerplate defect produced by the plan step itself.
- **Proposed fix**: In `.specify/templates/commands/plan.md`, make the fill step overwrite the template body rather than append, and add a post-write assertion that no `[UPPER_SNAKE]` placeholder token and no duplicate top-level `# Implementation Plan` heading remain. Remove L115–240 from this plan.md now.

### F4 — SC-004 guard scans the shipped default `memory/`, not the canonical runtime `.specify/memory/`

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_no_organize_agents_refs.py#L27
- **Evidence** (verbatim quote):

  ```
  ACTIVE_DIRS = ["skills", "templates", "docs", "agents", "src", "memory"]
  ```
  The live registry that still carries the stale name lives under `.specify/memory/`, not `memory/`:
  ```
  .specify/memory/features.md:1
  ```

- **Why it's a problem**: Per the project's own instructions, "the canonical project memory lives at `.specify/memory/`". The guard checks the in-package default `memory/` (constitution/features shipped with the CLI) while the authoritative live index it should protect is `.specify/memory/`. Registry drift in the file agents actually read goes undetected.
- **Proposed fix**: Add `.specify/memory` to the guard's scanned roots (or replace `memory` with `.specify/memory` when the runtime dir exists), consistent with the canonical-path rule in `.specify/instructions.md`.

### F5 — Feature was implemented but never committed; git-based process reconstruction is impossible

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/verification.md#L20 and `git log`/`git status`
- **Evidence** (verbatim quote):

  verification.md:
  ```
  post_change_commit=working-tree
  ```
  `git status --short` shows the whole spec staged/untracked, none committed:
  ```
  A  .specify/specs/026-agent-team-management/plan.md
  AM .specify/specs/026-agent-team-management/tasks.md
  ?? .specify/specs/026-agent-team-management/verification.md
  ```
  `git log --oneline -- .specify/specs/026-agent-team-management/` returns **no output**.

- **Why it's a problem**: The `/speckit.review` command §2 prescribes reconstructing the timeline "From `git log` scoped to REQUIREMENTS_DIR" — that yields nothing here, so deviations/friction cannot be traced from history. More broadly, a completed implement step with zero commits means there is no per-task audit trail, defeating the traceability the SDD workflow depends on.
- **Proposed fix**: In `.specify/templates/commands/implement.md`, add an explicit "commit after each task or logical group" gate (tasks.md already recommends it in Notes but nothing enforces it) and have `/speckit.implement` refuse to mark DoD "met" while the spec dir is entirely uncommitted. Alternatively, `/speckit.review` should fall back to working-tree diffs and state clearly when no commits exist.

### F6 — Stale `.specify/skills/organize-agents` install mirror ships alongside the renamed skill

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/skills/organize-agents/SKILL.md
- **Evidence** (verbatim quote):

  verification.md acknowledges it:
  ```
  The tracked .specify/skills/ install mirror still contains a stale organize-agents copy and lacks create-team/improve-team; this mirror is refreshed by package install and is deliberately outside the zero-dangling guard scope ...
  ```
  Directory listing confirms the canonical tree renamed but the mirror did not:
  ```
  skills/            -> create-team, improve-team   (renamed OK)
  .specify/skills/   -> organize-agents             (stale; no create-team/improve-team)
  ```

- **Why it's a problem**: `.specify/skills/` is the directory tools actually load at runtime (the canonical install location per `.specify/instructions.md`). Leaving it holding the old `organize-agents` skill and missing `create-team`/`improve-team` means the running framework is out of sync with the just-shipped feature until a manual reinstall — a silent behavioral gap the guard was explicitly told to ignore.
- **Proposed fix**: Make `/speckit.implement` (or `/speckit.instructions`) regenerate `.specify/skills/` from `skills/` as part of the migration, and add a parity check (canonical `skills/` set == `.specify/skills/` set) to the guard suite so mirror drift fails CI.

### F7 — `check-prerequisites.sh --include-*` reports an incomplete AVAILABLE_DOCS list

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/scripts/bash/check-prerequisites.sh (and mirror `.specify/scripts/bash/check-prerequisites.sh`)
- **Evidence** (verbatim quote):

  Script output:
  ```
  "AVAILABLE_DOCS":["requirements.md","plan.md","data-model.md","contracts/","quickstart.md","tasks.md"]
  ```
  Yet these tracked artifacts also exist in the same dir and are omitted:
  ```
  .specify/specs/026-agent-team-management/checklists/requirements.md
  .specify/specs/026-agent-team-management/feature-ref.md
  .specify/specs/026-agent-team-management/verification.md
  ```

- **Why it's a problem**: Downstream commands (like this review) that rely on AVAILABLE_DOCS to decide which artifacts to load will silently skip `checklists/`, `feature-ref.md`, and `verification.md`. The enumeration is a hardcoded allow-list rather than a directory scan, so any new artifact type is invisible.
- **Proposed fix**: In check-prerequisites.sh, enumerate AVAILABLE_DOCS by scanning REQUIREMENTS_DIR for known artifact names/dirs (add `checklists/`, `feature-ref.md`, `verification.md`) or switch to a glob-based listing.

### F8 — Requirement-ID vs Feature-ID offset (026 vs 027) creates recurring cross-reference confusion

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/026-agent-team-management/verification.md#L1 and tasks.md#L5-L9
- **Evidence** (verbatim quote):

  The same feature is addressed by two different numbers in adjacent lines:
  ```
  verification.md:  # Verification Log — 026-agent-team-management
  tasks.md:         # Tasks: Agent Team Management
  tasks.md:         **Requirement ID**: 026
  tasks.md:         **Related Feature**: 027 Team Management
  ```

- **Why it's a problem**: This is the first feature where the requirement key (026) and the bound feature ID (027) diverge (a new feature was minted). Artifacts, filenames, and test descriptions mix "026" and "027" freely; a reader can easily cite the wrong number (e.g., search `features/026.md` and find nothing). The offset is by design but the templates give no consistent, prominent disambiguation.
- **Proposed fix**: Have `/speckit.plan`/`/speckit.tasks` stamp a single standard header line in every generated artifact, e.g. `Requirement 026-agent-team-management → Feature 027 Team Management`, and reference features as `Feature 027` (never bare `027`) in template prose.

## 4. What Worked — Preserve (Brief)

- Shared Strings table (`STR-001…STR-004`) + `[[STR-NNN]]` citation convention in requirements.md — makes literal drift auditable.
- data-model.md § Template Classification: an explicit stay/move table per file — unambiguous migration source of truth.
- Test-First guard tests authored before implementation (T003/T006/…/T022 gated ahead of impl) — the mechanic is sound where scoped correctly.
- verification.md baseline/post-change counter format — honest enough to self-disclose the stale `.specify/skills/` mirror.
- Constitution Check rendered as one row per principle with per-artifact evidence.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Command Prompt Improvements

- **Strip template body on plan fill** — Target: /storage/project/cloud-native-ai/spec-kit/.specify/templates/commands/plan.md. Change: replace-in-place instead of appending, and assert no residual `[UPPER_SNAKE]` tokens / no duplicate `# Implementation Plan` heading after write. Source: F3. Expected impact: eliminates half-template plan artifacts across all future specs.
- **Enforce commit + evidence-backed task closure at implement/DoD** — Target: /storage/project/cloud-native-ai/spec-kit/.specify/templates/commands/implement.md. Change: block DoD "met" while the spec dir is entirely uncommitted; require each `[X]` to cite verifying evidence. Source: F2, F5. Expected impact: restores trust in `[X]` sigils and enables git-based review.

### 5.2 Automation / Script Improvements

- **Align the dangling-reference guard scope with SC-004** — Target: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_no_organize_agents_refs.py. Change: scan `.specify/memory/` and `tests/scenarios/` (allow-list only the guard's own file); add a `skills/` ↔ `.specify/skills/` parity assertion. Source: F1, F4, F6. Expected impact: guards stop over-certifying; registry/mirror drift fails CI.
- **Directory-scan AVAILABLE_DOCS** — Target: /storage/project/cloud-native-ai/spec-kit/scripts/bash/check-prerequisites.sh. Change: enumerate artifacts by scanning REQUIREMENTS_DIR (include `checklists/`, `feature-ref.md`, `verification.md`). Source: F7. Expected impact: downstream commands load the full artifact set.

### 5.3 Workflow Improvements

- **Standard requirement→feature header stamp** — Change: `/speckit.plan`/`/speckit.tasks` emit one canonical `Requirement <key> → Feature <id> <name>` line in every artifact; reference features as `Feature NNN`. Source: F8. Expected impact: removes 026/027-style cross-reference confusion.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Align dangling-reference guard scope with SC-004 (add `.specify/memory/`, `tests/scenarios/`) | /storage/project/cloud-native-ai/spec-kit/tests/contract/test_no_organize_agents_refs.py | F1, F4 |
| P0 | Evidence-backed task closure + close the actually-open T026 edit | /storage/project/cloud-native-ai/spec-kit/.specify/templates/commands/implement.md; tests/scenarios/agents-command/single-entry-routing-scenario.md | F2 |
| P1 | Strip template body on plan fill; remove plan.md L115–240 | /storage/project/cloud-native-ai/spec-kit/.specify/templates/commands/plan.md | F3 |
| P1 | Enforce commit gate before DoD "met" | /storage/project/cloud-native-ai/spec-kit/.specify/templates/commands/implement.md | F5 |
| P1 | Regenerate `.specify/skills/` + parity check | /storage/project/cloud-native-ai/spec-kit/.specify/skills/; guard suite | F6 |
| P2 | Directory-scan AVAILABLE_DOCS | /storage/project/cloud-native-ai/spec-kit/scripts/bash/check-prerequisites.sh | F7 |
| P2 | Requirement→feature header stamp | plan/tasks command templates | F8 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute, or written as `[REPO_URL]/blob/[COMMIT_SHA_FULL]/...`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
