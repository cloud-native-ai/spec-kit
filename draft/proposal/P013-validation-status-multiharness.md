# P013 — Spec Validation, Status Graph & Multi-Harness Tooling

- **Status:** Draft
- **Pillars:** Infra
- **Source projects:** OpenSpec
- **Value:** H · **Effort:** M–H · **Phase:** 1
- **Related:** [[P009]], [[P004]], [[P008]], [[P002]]

## Problem / Gap

spec-kit generates specs, plans, tasks, and delta-specs (the delta-spec workflow lives in
`draft/skills/delta-spec-change/`) but has **no runtime tooling around those artifacts**:

1. **No validation.** Nothing checks that a generated spec/plan/delta-spec is well-formed.
   Agents and humans discover structural problems only when a later stage breaks. The
   delta-spec skill *documents* rules (4-hashtag scenarios, SHALL/MUST presence,
   ADDED/MODIFIED/REMOVED conflicts) but codifies them as prose, not checks.
2. **No machine state contract.** There is no way for an agent (or CI) to ask "what is done,
   what is ready, what is blocked, and what exact command do I run next?" The flow is driven
   by a human invoking `/speckit.*` commands in order; state is implicit in which files exist.
3. **Monolithic prompts.** Guidance is baked into each command's markdown, mixing the output
   *skeleton*, the *how-to* prose, project *context*, and per-stage *rules* — so agents leak
   guidance into deliverables and teams cannot inject house style without editing commands.
4. **Brittle multi-harness generation.** Support for the 8 assistants is expressed as parallel
   per-assistant dicts (`_ASSISTANT_COMMAND_DIRS`, `_ASSISTANT_EXTENSIONS`,
   `_ASSISTANT_ARG_FORMATS`, `_ASSISTANT_TIERS`, `_SKILLS_SYMLINK_ASSISTANTS` in
   `src/specify_cli/__init__.py`). Adding a tool means editing several dicts in lockstep — a
   drift-prone pattern that will not scale toward "universal."
5. **No health command.** No one-shot "is my install/config sane, and how do I fix it" surface.

OpenSpec has mature, data-driven versions of all five. This proposal ports the *tooling*
(validation, status graph, instruction injection, adapter registry, doctor) — not OpenSpec's
delta grammar, which spec-kit already has.

## Proposal

Five Infra additions, all read-only or generation-side, none touching the `/speckit.*`
prompts themselves:

- **A. Two-layer validator** — grammar/schema layer + semantic-rule layer producing leveled
  diagnostics (`ERROR|WARNING|INFO`) with separated remediation strings; `--strict` promotes
  warnings; `--json` for agents.
- **B. `status --json` agent-state contract** — per-artifact `done`/`ready`/`blocked` (+
  `missingDeps`), backed by an **artifact dependency graph**, with a `nextSteps` array whose
  entries are *exact runnable commands*.
- **C. Per-artifact instruction injection** — an `instructions <id>` command that assembles an
  XML-tagged prompt bundle keeping **template / instruction / context / rules** as separate
  fields with explicit "do NOT include in output" markers.
- **D. Adapter-based multi-harness registry** — a tiny `ToolAdapter` protocol + registry
  replacing the parallel per-assistant dicts; one ~30-line adapter per tool.
- **E. `doctor` diagnostics** — structured `{severity, code, message, fix}` records where every
  finding carries a pasteable fix; `--json` mode.

## Design sketch

### B. Artifact graph + status contract (the spine A/C/E build on)

A declarative graph describes the SDD artifacts and their dependencies; completion is derived
purely from whether output files exist:

```python
# scripts/python/artifact_graph.py
@dataclass
class Artifact:
    id: str            # spec | plan | tasks | analyze | implement …
    generates: str     # glob for the output file(s)
    requires: list[str]
def build_order(graph) -> list[str]        # Kahn topo sort (deterministic)
def state_of(a, fs) -> str                 # done | ready | blocked
def next_steps(graph, fs) -> list[str]     # exact runnable commands
```

```
specify status [--feature NNN] [--json]
```

JSON is the agent contract:

```json
{ "artifacts": [
    {"id": "spec",  "state": "done"},
    {"id": "plan",  "state": "ready"},
    {"id": "tasks", "state": "blocked", "missingDeps": ["plan"]}
  ],
  "nextSteps": ["Run /speckit.plan for feature 007 before writing tasks"] }
```

Any agent can now drive the flow statelessly: read status → act on first `ready` → repeat.
This same graph is what a workflow engine ([[P009]]) or task-graph orchestrator ([[P004]])
consumes. Policy functions (`state_of`, `next_steps`) stay pure so text and JSON renderers
share them.

### A. Two-layer validator

```python
# scripts/python/spec_validate.py
@dataclass
class ValidationIssue:
    level: str      # ERROR | WARNING | INFO
    path: str
    message: str    # diagnosis
    guide: str      # remediation (kept separate, composable)
    line: int | None = None
@dataclass
class ValidationReport:
    valid: bool
    items: list[ValidationIssue]
    summary: dict   # counts by level
```

Layer 1 (grammar): heading structure, required sections, delta-spec 4-hashtag scenarios.
Layer 2 (semantic): SHALL/MUST presence (with header-vs-body detection for targeted fixes),
ADDED/MODIFIED/REMOVED cross-section conflict checks. Diagnosis strings live apart from
`GUIDE_*` remediation strings (so the same fix hint is reused across errors).

```
specify validate [item] [--all] [--strict] [--json] [--concurrency N]
```

`--strict` promotes WARNING→ERROR; `--json` emits `{items, summary, valid, root}`. This gives
agents a self-check loop and makes the already-drafted delta-spec workflow verifiable.

### C. Per-artifact instruction injection

```
specify instructions <artifact> [--feature NNN] [--json]
```

Assembles an XML-tagged bundle from four *separate* fields, in a fixed injection order
(context → rules → template), each marked so the agent never leaks guidance into output:

```
<artifact id="spec" output=".specify/specs/007-…/spec.md">
  <project_context note="do NOT include in output"> … </project_context>
  <rules note="do NOT include in output"> … per-stage constraints … </rules>
  <dependencies> plan: done </dependencies>
  <template> … output skeleton … </template>
  <success_criteria> … </success_criteria>
  <unlocks> tasks </unlocks>
</artifact>
```

`context` and `rules[id]` come from an optional `.specify/config.yaml` (light customization:
global context + per-artifact rules), so teams inject house style without editing commands.
This is a clean prompt pattern spec-kit's skills ([[P002]]) can reuse directly.

### D. Adapter-based multi-harness registry

Replace the parallel dicts in `src/specify_cli/__init__.py` with one protocol + registry:

```python
# scripts/python/harness_adapters.py
class ToolAdapter(Protocol):
    tool_id: str
    def file_path(self, command_id: str) -> str          # nested vs flat, dir, extension
    def format_file(self, content: CommandContent) -> str # frontmatter/TOML/companion file

class BaseAdapter:                # covers the common md + $ARGUMENTS + frontmatter case
    ...                           # most tools need almost no code

REGISTRY: dict[str, ToolAdapter] = {
    "claude": BaseAdapter("claude", dir=".claude/commands", ext="md", arg="$ARGUMENTS"),
    "qwen":   QwenAdapter(),      # TOML + {{args}}
    "copilot": CopilotAdapter(),  # .github/prompts, .prompt.md companion
    "opencode": OpencodeAdapter(),# command-name dialect rewrite
    …
}
```

Adding a harness = one adapter object, not edits across five dicts. A single
`escape_yaml_value` helper centralizes frontmatter escaping (applied uniformly — avoid
OpenSpec's inconsistency). Directory-presence auto-detection (which harnesses are installed)
stays, reading from the registry. This is the single highest-leverage change for the universal
goal: spec-kit's ~8 tools via brittle dicts → an abstraction OpenSpec scaled to 29 cleanly.

### E. `doctor` diagnostics

```
specify doctor [--json]
```

```python
@dataclass
class Diagnostic:
    severity: str   # error | warning | info
    code: str       # e.g. missing_command_coverage, broken_skills_symlink
    message: str
    fix: str        # pasteable command
```

Checks install completeness (reuse `compute_command_coverage` / `audit_capability_matrix`
already in `__init__.py`), skills-symlink health (`.github/skills → .specify/skills`), and
config validity. Exit 0 for healthy-with-findings, exit 1 only for hard failures. The
`{severity, code, message, fix}` taxonomy becomes the pattern for *all* spec-kit error
reporting.

### Cross-cutting: dual human/JSON + JSON purity

Every new command supports `--json`, emitting exactly one parseable document to stdout with
empty stderr (write side effects before the final print). A pytest helper
`assert_json_only(result)` enforces it — the contract that makes agent orchestration robust.

## Source evidence

- Data-driven artifact DAG + filesystem-derived state (topo sort, ready/blocked, cycle
  detection) → `_research/openspec.md` idea #1
  (`src/core/artifact-graph/graph.ts` `getBuildOrder`/`getNextArtifacts`/`getBlocked`,
  `schema.ts` cycle detection, `state.ts`+`outputs.ts`).
- `status --json` with `nextSteps` as runnable commands, pure policy functions →
  `_research/openspec.md` idea #3 (`src/commands/workflow/status.ts`,
  `src/core/change-status-policy.ts` `buildNextSteps`).
- Two-layer validator, leveled issues, separated remediation, header-vs-body SHALL/MUST →
  `_research/openspec.md` idea #4 (`src/core/validation/validator.ts`, `types.ts`,
  `constants.ts` `VALIDATION_MESSAGES`/`GUIDE_*`, `src/commands/validate.ts` flags).
- Per-artifact instruction injection with template/instruction/context/rules separation +
  XML "do NOT include" markers → `_research/openspec.md` idea #2
  (`src/core/artifact-graph/instruction-loader.ts`, `src/commands/workflow/instructions.ts`
  `printInstructionsText`); light config tier → idea #8 (`openspec/config.yaml`,
  `src/core/project-config.ts`).
- Adapter registry replacing per-assistant dicts → `_research/openspec.md` idea #5
  (`src/core/command-generation/{types,generator,registry}.ts`, `adapters/{gemini,codex,opencode}.ts`,
  `yaml.ts` `escapeYamlValue`); explicit contrast with spec-kit's
  `_ASSISTANT_COMMAND_DIRS`/`_ASSISTANT_EXTENSIONS`/`_ASSISTANT_ARG_FORMATS` in
  `src/specify_cli/__init__.py`.
- `doctor` structured `{severity, code, message, fix}` → `_research/openspec.md` idea #7
  (`src/commands/doctor.ts`, `src/core/relationship-health.ts` `makeStoreDiagnostic`).
- Dual human/JSON purity convention + test helper → `_research/openspec.md` idea #9
  (`test/cli-e2e/basic.test.ts` `expectJsonOnlyOutput`).
- spec-kit surfaces reused: `draft/skills/delta-spec-change/references/delta-format.md`
  (rules to codify), `compute_command_coverage`/`audit_capability_matrix` in `__init__.py`,
  `scripts/bash/check-prerequisites.sh` (existing prerequisite/`--json` pattern to align with).

## Adoption plan

All additions are read-only or generation-side and ship in `draft/` / new scripts; the
`/speckit.*` prompts are untouched.

1. **Adapter registry (D).** Refactor the per-assistant dicts into `ToolAdapter` objects +
   registry behind the existing generation code. Pure internal refactor with identical output
   — verify byte-equivalence against current generation before/after. Highest leverage, no
   user-visible change.
2. **Artifact graph + status (B).** Add `artifact_graph.py` and `specify status`; ship a
   built-in graph mirroring spec-kit's current stages. State = "does the output file exist."
3. **Validator (A).** Add `spec_validate.py` + `specify validate`; codify the delta-spec rules
   the skill already documents. Wire as an optional self-check; agents/CI call `--json`.
4. **Instructions (C).** Add `specify instructions <artifact>` + optional `.specify/config.yaml`
   (context + per-artifact rules); skills loop over `status` ready set and call it per artifact.
5. **Doctor (E).** Add `specify doctor` reusing existing coverage checks; adopt the
   `{severity, code, message, fix}` shape project-wide over time.

Standardize `--json` + `assert_json_only` across all five as they land.

## Risks & mitigations

- **Adapter refactor regressions.** The dicts encode subtle per-harness quirks (TOML args,
  Copilot companion files, opencode dialect). Mitigate with a golden-file test: generate all
  harness outputs before and after and assert byte-equivalence; migrate one tool at a time.
- **Validator false positives frustrate users.** Ship rules as WARNING first (only known-hard
  breakage as ERROR); `--strict` is opt-in; every issue carries a `guide` remediation.
- **Graph/state drift from reality.** Derive state solely from file existence (no separate
  state store to desync); add a `doctor` check for graph/output-path mismatches.
- **Prompt-guidance leakage.** The XML "do NOT include in output" markers and template/context
  separation are the mitigation; validate deliverables don't contain the markers.
- **Scope temptation.** Skip OpenSpec's worksets/stores and animated welcome screen (flagged
  out-of-scope in the mining report); ship the read-only engine first, defer schema-fork UX.

## Value / Effort rationale

**Value H:** this is the fastest, lowest-risk path to real framework maturity — it makes
spec-kit's artifacts *verifiable* (validator), makes the flow *agent-drivable* (status graph +
runnable nextSteps), makes prompts *composable and leak-free* (instruction injection), and
makes multi-harness support *scalable* (adapter registry) instead of drift-prone dicts. The
status graph is the substrate [[P009]] and [[P004]] both build on.

**Effort M–H:** the artifact graph, validator, and doctor are self-contained Python ports of
well-understood OpenSpec code (~150 lines each); the adapter refactor is mechanical but must
be regression-proofed against current output. No new runtime and no prompt changes keep the
risk low, which — together with the high leverage — is why this is Phase 1.
