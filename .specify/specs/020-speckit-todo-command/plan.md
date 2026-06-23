# Implementation Plan: Speckit Todo Command (Feature 025)

**Branch**: `020-speckit-todo-command` | **Date**: 2026-06-23 | **Spec**: [requirements.md](./requirements.md)  
**Input**: Specification from `.specify/specs/020-speckit-todo-command/requirements.md`

## Summary

Implement `/speckit.todo` as a Spec Kit chat-prompt command that (a) delegates TODO discovery to a new pure-bash scanner `.specify/scripts/bash/search-todo.sh`, (b) extracts fenced `SPECKIT TODO` blocks with paragraph-boundary context from eligible text files, (c) clusters related blocks into reviewable work groups, (d) batches outputs (valid count > 10 → batches of ≤ 5), and (e) auto-executes the generated plan after explicit user confirmation.

Technical approach: a single pure-bash scanner (augmented with a small `awk` program for the multiline fence state machine) that emits structured JSON on stdout for downstream AI consumption. The chat prompt (`speckit.todo.prompt.md`) consumes the JSON, applies safety gates (malformed-block exclusion per FR-007, destructive/secret/out-of-scope veto), renders a reviewable plan (FR-010), and executes task groups batch-by-batch after confirmation.

## Technical Context

**Language/Version**: Bash ≥ 4.0 (associative-array support; matches every other `.specify/scripts/bash/*.sh`), POSIX `awk`, `find`, GNU/coreutils.  
**Primary Dependencies**: No new runtime dependencies. Script is self-contained and reuses `common.sh` helpers.  
**Storage**: N/A — read-only filesystem scan; JSON emitted to stdout.  
**Testing**: `pytest` with `contract` and `integration` markers; shell fixtures under `tests/fixtures/todo-workspaces/` (valid / malformed / empty / negative / oversized).  
**Target Platform**: Linux and macOS (matching Spec Kit's existing bash-script support matrix).  
**Project Type**: Single — extends existing Spec Kit layout (`.github/prompts/`, `.specify/scripts/bash/`, `.specify/memory/`, `tests/`). No subproject split.  
**Performance Goals**: ≤ 10 s end-to-end scan for workspaces of up to 10 000 files; ≤ 50 ms per file on average for a 500-file workspace.  
**Constraints**: No network I/O. No external LLM/HTTP calls from the scanner. JSON output must be well-formed on UTF-8 files and must fail closed on partial-binary inputs (report, do not crash). Output must be deterministic (stable block order = file-then-line).  
**Scale/Scope**: One user, one workspace; up to ~10 000 scanned files and unbounded count of ordinary TODO comments (all ignored except `SPECKIT TODO` fenced blocks).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered dynamically from `.specify/memory/constitution.md`, one row per numbered principle, in file order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every plan task traces back to FR-001…FR-012; acceptance scenarios are represented by contract tests in `contracts/search-todo-cli.md` (happy / malformed / empty / no-op / batching / exclusion / out-of-scope veto). |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 025 `Todo Command` (already present in `.specify/memory/features.md`); Feature detail at `.specify/memory/features/025.md` records Phase 1 key changes; no duplicate feature IDs created. |
| III | Intent-Driven Development | ✅ Pass | The prompt template (`speckit.todo.prompt.md`) expresses user intent in natural language; `search-todo.sh` only performs discovery — grouping, plan synthesis, and execution remain agent-driven, preserving the "what/why before how" layering. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | `contracts/search-todo-cli.md` locks the scanner's CLI surface (flags, exit codes, JSON schema); pytest fixtures under `tests/fixtures/todo-workspaces/` cover every acceptance scenario (SC-001…SC-005). |
| V | AI Agent Integration Standards | ✅ Pass | The prompt is agent-agnostic (no provider-locked API); it is compatible with every Tier 1 and Tier 2 supported agent listed in Principle V (Copilot, Claude Code, Codex, Qoder, opencode, Qwen, Hermes, iFlow). |
| VI | Continuous Quality & Observability | ✅ Pass | Script writes structured diagnostics to stderr (malformed blocks, excluded files, scan_time); JSON counters (`total_blocks`, `malformed_blocks`, `excluded_files_count`) support observability; YAGNI honored — filtering-by-category and machine-readable output for downstream automation are deferred to Future Evolution (see `features/025.md`). |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Current artifact is Phase 2 of 7; downstream `/speckit.tasks`, `/speckit.implement`, `/speckit.review` will operate against this plan without re-planning. |

**Gates Status**: ✅ All gates pass. No complexity-tracking violations.

**Re-check after Phase 1**: 2026-06-23 — table re-evaluated against `data-model.md`, `contracts/search-todo-cli.md`, and `quickstart.md`. All seven principles remain ✅ Pass; no new Fail/Partial rows emerged.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/020-speckit-todo-command/
├── plan.md                          # This file
├── requirements.md                  # Phase input (already present)
├── checklists/requirements.md       # Spec quality checklist (already present)
├── data-model.md                    # Phase 1 output
├── quickstart.md                    # Phase 1 output
└── contracts/
    └── search-todo-cli.md           # Phase 1 output — CLI contract for search-todo.sh
```

No standalone `research.md` — Phase 0 findings are brief and fully resolved from internal project investigation, so they are inlined below under "Phase 0: Research Review & Context".

### Source Code (repository root) — directories touched by THIS spec

```text
.github/prompts/                     # NEW: speckit.todo.prompt.md (chat prompt for the command)
.specify/scripts/bash/               # NEW: search-todo.sh (scanner script)
.specify/memory/
├── features.md                      # UPDATE: Feature 025 Last Updated date
└── features/
    └── 025.md                       # UPDATE: record Phase 1 key change
tests/
├── fixtures/todo-workspaces/        # NEW: fixture workspaces for contract tests (valid / malformed / empty / negative / oversized)
└── contract/                        # NEW: test_search_todo_script.py (CLI contract tests)
```

**Structure Decision**: "Single project extending the existing Spec Kit layout." The feature adds one prompt file under `.github/prompts/` and one bash script under `.specify/scripts/bash/`, plus contract tests and fixtures. No new top-level directory, no subproject split, no new binary entrypoint — the `/speckit.todo` command is purely an AI-chat prompt invoked via `/speckit.todo` in chat, never directly from the shell.

## Complexity Tracking

N/A — all seven constitution principles pass; no justifications required.

---

## Phase 0: Research Review & Context

> No standalone `research.md`. Findings below are from internal project investigation and are inlined here.

### Findings inlined

1. **Existing-script patterns to mirror**: `create-new-plan.sh` and `create-new-requirements.sh` both (a) use `common.sh` for repo-root discovery and `get_feature_paths`, (b) support `--json` and `--help`/`-h`, (c) emit either multiline key:value (default) or single-line JSON (via printf, no jq dependency), and (d) never depend on external language runtimes. `search-todo.sh` will mirror all four conventions.

2. **Command pattern to mirror**: `.github/prompts/speckit.analyze.prompt.md` is the closest read-only-scan command; `.github/prompts/speckit.plan.prompt.md` is the closest review-gate-and-execute command. The new `/speckit.todo` prompt merges these two patterns: scan-then-plan-then-execute-after-confirmation.

3. **Tool-registration decision**: `/speckit.tools` (Feature 016) defines a "project script" tool type with records under `.specify/memory/tools/<name>.md`. `search-todo.sh` fits this category; its tool record will be generated at implement phase (out of scope for this plan). The prompt does **not** register the tool itself — it only invokes the script.

4. **Marker ambiguity resolved (`/speckit.clarify` Q2)**: any fenced block whose opening fence line contains the substring `SPECKIT TODO` (case-exact, anywhere on the line) matches. The awk state machine toggles on the first fence line whose body contains `SPECKIT TODO` and remains inside the block until the next matching closing triple-backtick fence.

5. **Context boundary resolved (`/speckit.clarify` Q3)**: paragraph-boundary — upward to nearest blank line or Markdown section heading, downward to next blank line or Markdown section heading.

6. **Execution semantics resolved (`/speckit.clarify` Q4)**: scan → plan → display → user-confirmation gate → auto-execute each batch sequentially.

7. **Batching resolved (`/speckit.clarify` Q5)**: valid block count > 10 triggers batching; each batch ≤ 5 blocks; batches are rendered and confirmed sequentially.

### Technical decisions derived

- **Scanner language**: pure bash + awk (no Python, no ripgrep, no jq). Reasoning: matches every existing `.specify/scripts/bash/*` script, no new runtime dependency, and awk elegantly handles the multiline fence state machine.
- **Ignore rules**: reuse `common.sh`'s default exclusion list (binary extensions, `.git/`, `.venv/`, `node_modules/`, `__pycache__/`, `.specify/specs/*/contracts/fixtures/`, `.specify/specs/*/checklists/`). Override via `--exclude <pattern>` (repeatable) and `--no-default-excludes` (opt into full-workspace scan).
- **JSON output**: hand-emitted via bash + printf (pattern from `create-new-requirements.sh` and `create-new-plan.sh`); no jq dependency. Escaping helper in `common.sh` handles JSON-string values (newlines, quotes, backslashes).
- **Block ordering**: deterministic — blocks are enumerated in (file-path ASC, opening-line ASC) order.
- **Malformed detection**: a `SPECKIT TODO` opening fence with no matching closing fence before end-of-file is reported to stderr and as a `malformed` entry in the JSON.
- **Out-of-scope veto**: implemented entirely at the chat-prompt layer (not the scanner). The scanner reports raw block content. The prompt applies rules to reject TODO content that requests destructive operations, secret exposure, or out-of-scope work.

## Phase 1: Design & Contracts

The Phase 1 implementation produces three artifacts (paths relative to `REQUIREMENTS_DIR`):

### 1.A `data-model.md`

Entities, fields, relationships, validation rules, and state transitions. Key entities:

- `TodoBlock` — a single valid fenced `SPECKIT TODO` block including source file path, opening/closing line numbers, raw content, context heading, prologue, and epilogue.
- `MalformedBlock` — a malformed opening fence recorded with file path, opening line, reason, and content snippet.
- `TodoGroup` — a cluster of one or more `TodoBlock` entries sharing file or topic affinity.
- `TodoPlan` — the ordered collection of `ExecutionBatch` entries to be reviewed and executed.
- `ExecutionBatch` — a bounded slice of the `TodoPlan` (≤ 5 groups) with explicit review-and-confirmation gate.

State transitions: `discovered → grouped → planned → executed | deferred | rejected`.

### 1.B `contracts/search-todo-cli.md`

CLI contract for `.specify/scripts/bash/search-todo.sh`. Locks:

- Invocation: `search-todo.sh [--json] [--help] [--root <path>] [--exclude <pattern>]... [--no-default-excludes] [<path>]`
- Exit codes: `0` success; `1` argument error; `2` repo-root discovery failure; `3` scan I/O error.
- JSON output schema (when `--json`), line-oriented key:value output otherwise.
- Malformed / empty / oversized behaviors (FR-007, FR-012, FR-011).
- Fixture-based contract tests under `tests/contract/test_search_todo_script.py`.

### 1.C `quickstart.md`

End-to-end walkthrough for a new Spec Kit user:

1. Embed one `SPECKIT TODO` fenced block into an eligible text file.
2. Run `/speckit.todo` in chat.
3. Review the generated plan (see grouped work, source references, safety notes, validation expectations).
4. Confirm execution.
5. Observe the planned task group being executed against the workspace.

### 1.D Post-Generation Quality Gate

After the three Phase 1 artifacts are written, each is reviewed to ensure:

- No internal-deliberation markers ("Wait—", "Actually,", "On second thought", "Let me reconsider", "re-reading:", "Hmm,", "I think", "I realize", "To be clear:", "For the avoidance of doubt" followed by reasoning) appear in contract files.
- All statements are declarative or normative (MUST, MUST NOT, SHOULD).
- JSON schemas, flag tables, exit-code tables, and error-message strings contain only concrete values.
- Every contract assertion traces back to at least one FR or Acceptance Scenario.

## Phase 2: Task Breakdown (downstream)

Deferred to `/speckit.tasks`. This plan provides the input surface; `/speckit.tasks` will decompose into atomic tasks.
