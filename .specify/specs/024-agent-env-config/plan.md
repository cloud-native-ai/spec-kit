# Implementation Plan: Unified Env-Var Agent Configuration

**Branch**: `024-agent-env-config` | **Date**: 2026-07-12 | **Spec**: [requirements.md](./requirements.md)
**Input**: Specification from `.specify/specs/024-agent-env-config/requirements.md`

## Summary

Reframe the `agent-setup` skill around a **unified environment-variable** configuration model: the user exports one canonical set of skill-layer variables for the three core inputs (API key, base URL, model); the skill validates them, reads them, performs a **secondary assignment** into each tool's native variable names, and persists the result into each tool's **own configuration file**. Scope is the six API-key-configurable CLIs — `claude`, `codex`, `qwen`, `qoder`, `iflow`, `opencode` (Copilot/Hermes excluded per clarification). Implementation extends the existing Bash script `skills/agent-setup/scripts/config-agent.sh`, reusing its per-tool config writers behind a new three-step flow (check → read → write) with fail-fast validation, no-partial-writes, idempotency, and secret redaction.

## Technical Context

**Language/Version**: Bash (POSIX-friendly, `bash` ≥ 4) for the skill script; Python 3.11 only for test harness (pytest, matching repo).  
**Primary Dependencies**: coreutils; `python3` (already used by `config-agent.sh` for JSON merge). No new runtime deps.  
**Storage**: Per-tool config files under `$HOME` (JSON/TOML/dotenv); no database.  
**Testing**: `pytest` with markers `contract` and `integration` (per `pyproject.toml`), invoking the Bash functions via subprocess against a temp `HOME`; mirrors existing `tests/contract/test_agent_specific_config_skills.py` pattern.  
**Target Platform**: Linux/macOS developer shells.  
**Project Type**: Framework skill (single Bash script + references + SKILL.md); not the `specify` Python CLI.  
**Performance Goals**: Configure-all completes well under 1 minute (SC-001); operations are file writes only.  
**Constraints**: Fail-fast with zero partial writes (FR-004); idempotent writes (FR-013); never print secrets (FR-014); preserve unrelated existing settings (FR-008).  
**Scale/Scope**: Fixed set of 6 tools; 3 required unified vars + 1 conditionally-required Anthropic URL.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design element traces to FR-001..FR-015 in `requirements.md`; contracts derived from FRs. |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 022 (AI Tools Support); `features/022.md` updated with an Evolution + Plan-phase note. |
| III | Intent-Driven Development | ✅ Pass | Plan states WHAT/WHY (unified inputs → per-tool persistence) before HOW; multi-step check→read→write. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | `contracts/` defines the env contract + per-tool file targets; `/speckit.tasks` will sequence tests before writers. |
| V | AI Agent Integration Standards | ✅ Pass | Only officially supported agents; six in scope are all official; unknown tools rejected (FR-015); Copilot/Hermes intentionally out of scope (they lack an API-key model). |
| VI | Continuous Quality & Observability | ✅ Pass | Structured per-tool report (FR-010), idempotency (FR-013), secret redaction (FR-014), YAGNI (extend existing script, no new deps), SKILL.md/docs updated. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Requirements → clarify → this plan → tasks → implement; feature index re-evaluated. |

**Gates Status**: ✅ All gates pass.

**Re-check after Phase 1**: 2026-07-12 — Re-evaluated against generated `data-model.md`, `contracts/`, and `quickstart.md`. No regressions; all rows remain ✅ Pass. Complexity Tracking remains N/A.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/024-agent-env-config/
├── plan.md              # This file
├── data-model.md        # Phase 1 — entities: unified input set, tool profile, report
├── quickstart.md        # Phase 1 — set env vars → configure all / single tool
├── contracts/           # Phase 1
│   ├── unified-env-contract.md    # canonical variable names, validation, exit codes, redaction
│   └── tool-config-targets.md     # per-tool file path + format + secondary-assignment map
├── checklists/requirements.md     # (from /speckit.requirements)
├── requirements.md
├── tasks.md             # Phase 2 (/speckit.tasks — NOT created here)
└── verification.md      # Implementation output (/speckit.implement)
```

No standalone `research.md` — Phase 0 findings inlined below (fully resolvable from the existing skill, `docs/agent-tools/`, and constitution).

### Source Code (repository root)

```text
skills/agent-setup/scripts/config-agent.sh   # extend: add unified-env validate/read/apply flow + qwen/codex persistence fixes
skills/agent-setup/SKILL.md                  # reframe workflow around unified env vars + 6-tool scope
skills/agent-setup/references/               # add unified-variables.md; update supported/available tuples framing
tests/contract/                              # new: SKILL.md/contract structure tests for unified model
tests/integration/                           # new: behavioral tests — apply into temp HOME, idempotency, fail-fast, redaction
```

> Canonical mirror: `.specify/skills/agent-setup/` reflects `skills/agent-setup/` via the package install/symlink model; edit the `skills/…` source.

**Structure Decision**: Extends the existing Bash-based `agent-setup` skill in place. It adds a unified-env-var configuration flow (`config_agent_env_validate` + `config_agent_env_apply`) layered on top of the existing per-tool config writers, rather than introducing a new skill or a Python component. New files are limited to one reference doc and the test files; no new top-level directory.

## Phase 0: Research Review (inlined)

**Decision 1 — Unified variable set (skill-layer canonical names).**
`AGENT_API_KEY`, `AGENT_MODEL`, `AGENT_BASE_URL` are required; `AGENT_ANTHROPIC_BASE_URL` is required only when `claude` is in the target set.
- Rationale: Five of six tools speak the OpenAI-compatible protocol and share one endpoint form; `claude` speaks the Anthropic-compatible protocol whose endpoint path differs. A single base URL cannot serve both, and generic path derivation across providers is brittle. Exposing an explicit Anthropic URL variant is the correct, non-brittle resolution of FR-011 and keeps the three core concepts (key/URL/model) intact — the Anthropic URL is a protocol-specific *variant* of "URL", not a new input concept.
- Alternatives rejected: (a) single `AGENT_BASE_URL` with computed suffixes — brittle, provider-specific; (b) fully per-tool inputs — defeats the "one-time convenient config" value.

**Decision 2 — Persist to each tool's own config file (fixes qwen/codex gaps).**
The prior script left `qwen` and the `codex` key as shell exports only (not persisted). Persistence targets are fixed as in `contracts/tool-config-targets.md`: `qwen` → `~/.qwen/.env`; `codex` → `~/.codex/config.toml` plus API key in `~/.codex/auth.json`. Others keep their existing JSON/TOML targets.
- Rationale: FR-007 requires durable persistence in each tool's native file, not ephemeral env exports.

**Decision 3 — Flow, atomicity, idempotency, redaction.**
Three ordered steps: (1) `validate` all required unified vars (present, non-empty, URL scheme sane) → on any failure, report every offender and write nothing (FR-004); (2) `read` values into locals; (3) `apply` per target tool — secondary-assign to native names, create dirs, merge-write preserving unrelated keys (FR-008), emit per-tool status. Writers are deterministic (idempotent, FR-013). The API key value is never echoed; logs show variable names only (FR-014).

**Decision 4 — Reuse & scope.**
Reuse existing `_config_agent_write_claude/codex/qoder/iflow/opencode`; update `_config_agent_write_qwen` and `_config_agent_write_codex` for file persistence. Restrict the tool registry for this flow to the six in scope; reject unknown tool names listing supported tools (FR-015). Provider four-tuple concepts (idealab/bailian) are superseded on the input side by the unified variables; existing list/install/start helpers remain unchanged.

## Complexity Tracking

N/A — no Constitution gate violations.
# Implementation Plan: [SPEC]

**Branch**: `[###-spec-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Specification from `.specify/specs/[REQUIREMENTS_KEY]/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

<!--
  ACTION REQUIRED for /speckit.plan:
  Do NOT hard-code principle names here. Instead, read `.specify/memory/constitution.md`,
  enumerate every heading matching `### <roman-or-arabic-numeral>. <name>` (e.g.
  `### I. Template-First Architecture`, `### IV. Test-First Development`), and render
  ONE row in the table below per principle in the exact order they appear in the
  constitution. Include the principle's NON-NEGOTIABLE / MANDATORY annotation verbatim
  when present. This avoids the drift documented in the constitution's Sync Impact Report.

  Each row must contain:
  - Principle (verbatim heading without the leading `### N.`)
  - Compliance ("✅ Pass" / "❌ Fail" / "⚠ Partial — see Complexity Tracking")
  - Evidence (one-line citation pointing at the design artefact that demonstrates compliance)
-->

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | [PRINCIPLE_1_NAME] [NON-NEGOTIABLE?] | ✅ Pass / ❌ Fail / ⚠ Partial | [one-line evidence: file or section] |
| II | [PRINCIPLE_2_NAME] [NON-NEGOTIABLE?] | ✅ Pass / ❌ Fail / ⚠ Partial | [...] |
| ... | [continue for every principle declared in constitution.md] | | |

**Gates Status**: [✅ All gates pass / ❌ Specific gate failures with justification — list failing principle numbers and link to Complexity Tracking row]

**Re-check after Phase 1**: [Date and short note when the post-design re-check was run; copy the same table refreshed against the design artefacts]

## Project Structure

### Documentation (this spec)

```text
.specify/specs/[REQUIREMENTS_KEY]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command) — see note below
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

<!--
  research.md conditional guidance:
  Produce `research.md` as a standalone file when Phase 0 research exceeds ~50 lines
  or involves external source evaluation (API docs, vendor comparisons, benchmark data).
  When Phase 0 findings are brief (< 50 lines) and fully resolvable from internal
  investigation (project docs, constitution, existing code), inline them into plan.md
  under the `## Phase 0: Research Review` heading and note in this tree:
  "No standalone research.md — findings inlined below."
-->

### Source Code (repository root)
<!--
  ACTION REQUIRED:
  Document ONLY the directories actually changed or created by THIS spec, with a
  one-line purpose per directory. Do NOT invent a generic layout, and do NOT paste
  a "Single project / Web / Mobile" stub if it does not reflect this project.

  Examples of valid shapes (see `.specify/templates/examples/structure-*.md` if
  shipped, otherwise infer from the repo):
    - Single application:           src/, tests/
    - Web app:                      backend/, frontend/
    - Mobile + API:                 api/, ios/ or android/
    - Library / SDK:                src/<package>/, examples/, tests/
    - Monorepo:                     packages/<name>/, apps/<name>/
    - Container-image factory:      images/, script/snippets/, script/build/
    - Code generator / framework:   templates/, scripts/, src/<package>/

  If your project does not match any of these, document what is true. The goal is
  evidence-faithful structure, not adherence to a fixed taxonomy.
-->

```text
[REPLACE THIS BLOCK with the real directories changed by this spec, one line per dir,
 each followed by `# <one-line purpose>`. Keep it terse — do not enumerate every file.]
```

**Structure Decision**: [Name the shape this spec actually lands in (e.g. "extends the
existing container-image factory by adding two new snippets under
`script/snippets/docker/config/users/` and weaving them into 19 daemon images") and
reference the real directories captured above. Explicitly note any new top-level dir.]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**
> If no violations, explicitly write "N/A" and remove the table.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
