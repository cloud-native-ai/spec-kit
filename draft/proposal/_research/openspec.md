# OpenSpec — Mining Report for spec-kit

Source project: `/cws_work/OpenSpec` (TypeScript, `openspec` CLI). Scope of this
report: everything BEYOND the already-ported delta-spec workflow — validation/status
tooling, the artifact dependency graph, the data-driven forkable schema system,
per-artifact config/context injection, the multi-harness install/update engine, the
interactive dashboard/doctor/worksets, and testing patterns.

## Project snapshot

OpenSpec is a mature, data-driven Spec-Driven-Development CLI built on Commander.js +
`@inquirer` + `zod`. Its defining architectural bet is that the SDD *process itself is
data*: a declarative `schema.yaml` defines an artifact DAG (proposal → specs → design →
tasks + an `apply` phase), and a generic TypeScript engine (`ArtifactGraph`, resolver,
instruction-loader) interprets it — topologically ordering artifacts, deriving
"done/ready/blocked" state purely from which output files exist on disk, and emitting
per-artifact LLM prompts that fuse the schema's template + instruction with the project's
`config.yaml` context + rules. On top of this sit: a two-layer validator (Zod grammar +
semantic rules) with leveled issues and remediation-carrying diagnostics; a universal
command-generation engine that renders one source-of-truth workflow into skill+command
files for ~29 AI tools via a tiny per-tool adapter interface; version-marker-based
idempotent install/update with profile/delivery drift detection; and a rich set of
read-only surfaces (`status --json`, `validate --json`, `doctor`, `view` dashboard) where
every human view has a parallel machine-readable JSON view. spec-kit today is essentially
a scaffolder/installer (a 2200-line `specify_cli` with parallel per-assistant dicts and
markdown-prompt commands); it has no runtime spec-validation, no artifact graph, no
data-driven pipeline, and no structured diagnostics — which is exactly where OpenSpec's
tooling can level it up toward a universal framework.

## Top ideas for spec-kit

### 1. Data-driven, forkable pipeline schema (`schema.yaml` + artifact DAG)
- **Idea**: Replace spec-kit's hardcoded, command-per-stage flow with a declarative
  `schema.yaml` that lists artifacts (`id`, `generates`, `template`, `instruction`,
  `requires`) plus a terminal `apply` phase. A generic engine interprets it: topo-sort the
  DAG, derive completion from file existence, and drive the agent stage-by-stage. This is
  THE structural idea that turns spec-kit from a fixed SDD tool into a configurable
  universal framework — any team can add/reorder/remove stages by editing YAML, and the
  same agent harness works with any custom pipeline.
- **Source evidence**: `/cws_work/OpenSpec/schemas/spec-driven/schema.yaml`;
  `/cws_work/OpenSpec/src/core/artifact-graph/types.ts` (Zod `SchemaYamlSchema`,
  `ArtifactSchema`, `ApplyPhaseSchema`); `/cws_work/OpenSpec/src/core/artifact-graph/graph.ts`
  (`getBuildOrder` Kahn topo sort, `getNextArtifacts`, `getBlocked`);
  `/cws_work/OpenSpec/src/core/artifact-graph/schema.ts` (duplicate-id, dangling-ref,
  DFS cycle-path detection); `/cws_work/OpenSpec/src/core/artifact-graph/state.ts` +
  `outputs.ts` (filesystem-derived completion via glob).
- **Why it helps**: Unifies SKILLS + COMMANDS + WORKFLOWS under one declarative spine.
  Makes the "process" a first-class, versionable, shareable artifact. Enables custom SDD
  variants (e.g., add a `research` or `security-review` stage) without code changes.
- **Maps to spec-kit as**: infra + template (a `schema.yaml` format) + workflow.
- **Value**: H — **Effort**: H.
- **Adoption sketch**: Define a `SchemaYaml` dataclass + YAML loader in `specify_cli`; port
  `ArtifactGraph` (topo sort, ready/blocked, cycle detection ~150 lines Python); ship a
  built-in `spec-driven` schema mirroring spec-kit's existing stages; add `specify status`
  and `specify instructions` (idea #2) that read it. State = "does the output file exist".

### 2. Per-artifact instruction injection (`instructions <id> --json`) with template/instruction/context/rules separation
- **Idea**: A command that, for a given artifact, assembles an LLM-ready prompt bundle:
  the schema `template` (output skeleton), the schema `instruction` (how-to prose), the
  project `context` (global background), the per-artifact `rules`, resolved dependency
  status, and the exact output path. Crucially it keeps these as *separate fields* and
  emits an XML-tagged prompt with explicit "do NOT include in output" markers so the agent
  never leaks guidance into the deliverable.
- **Source evidence**: `/cws_work/OpenSpec/src/core/artifact-graph/instruction-loader.ts`
  (`generateInstructions`, `ArtifactInstructions` interface, documented injection order
  context→rules→template); `/cws_work/OpenSpec/src/commands/workflow/instructions.ts`
  (`printInstructionsText` XML block: `<artifact>`, `<project_context>`, `<rules>`,
  `<dependencies>`, `<output>`, `<template>`, `<success_criteria>`, `<unlocks>`).
- **Why it helps**: Gives every agent tool a uniform, deterministic way to fetch "what to
  write next and exactly how", instead of baking all guidance into monolithic command
  prompts. The context/rules/template separation is a clean prompt-engineering pattern
  spec-kit's skills can adopt directly.
- **Maps to spec-kit as**: command + script + infra.
- **Value**: H — **Effort**: M.
- **Adoption sketch**: `specify instructions <artifact> --change <name> [--json]`; render
  the XML-tagged text for agent consumption; workflow skills loop over `status` ready set,
  call this per artifact, write to the returned path.

### 3. `status --json` as the agent state contract (ready/blocked/done + nextSteps)
- **Idea**: A `status` command that reports each artifact's state (`done`/`ready`/`blocked`
  with `missingDeps`), sorted topologically, plus `applyRequires`, resolved artifact paths,
  and a machine-readable `nextSteps` array whose entries are *exact runnable commands*
  ("Run `openspec instructions specs --change X --json` before writing that artifact").
- **Source evidence**: `/cws_work/OpenSpec/src/commands/workflow/status.ts`
  (`StatusOptions`, `printStatusText`, JSON shape); `formatChangeStatus` in
  `/cws_work/OpenSpec/src/core/artifact-graph/instruction-loader.ts`;
  `/cws_work/OpenSpec/src/core/change-status-policy.ts` (pure `buildNextSteps`,
  `buildActionContext`, `summarizePlanningHome` — policy decoupled from presentation).
- **Why it helps**: Turns the workflow into a stateless loop any agent can drive:
  read status → act on first ready artifact → repeat. The "next step is a copy-pasteable
  command" pattern is what makes multi-tool agent orchestration reliable.
- **Maps to spec-kit as**: command + infra.
- **Value**: H — **Effort**: M.
- **Adoption sketch**: `specify status [--change] [--json]`; text mode shows a progress
  header + per-artifact indicator lines; JSON mode is the agent contract. Keep policy
  functions pure so both renderers share them.

### 4. Two-layer spec validator with leveled, remediation-carrying diagnostics
- **Idea**: A `validate` command that runs (a) a grammar/schema layer and (b) a semantic
  rule layer, producing a flat list of `{level: ERROR|WARNING|INFO, path, message, line?}`
  + a rollup `summary` + a single `valid` bool. `--strict` promotes warnings to failures.
  Diagnosis strings are kept separate from composable remediation (`GUIDE_*`) strings, and
  errors are context-enriched (e.g., detect SHALL/MUST placed in a header vs body and give
  a targeted fix). Bulk mode with a bounded-concurrency pool.
- **Source evidence**: `/cws_work/OpenSpec/src/core/validation/validator.ts` (two-layer
  arch, `convertZodErrors`, `validateChangeDeltaSpecs` set-intersection conflict checks,
  `enrichTopLevelError`, `buildMissingShallOrMustMessage`);
  `/cws_work/OpenSpec/src/core/validation/types.ts` (`ValidationIssue`, `ValidationReport`);
  `/cws_work/OpenSpec/src/core/validation/constants.ts` (tunable thresholds +
  `VALIDATION_MESSAGES` with separated `GUIDE_*` remediation);
  `/cws_work/OpenSpec/src/commands/validate.ts` (flags `--all/--strict/--json/--concurrency`,
  JSON `{items, summary, version, root}` shape, "did you mean" suggestions).
- **Why it helps**: spec-kit has ZERO runtime validation of the specs/deltas it generates.
  A validator gives agents a self-check loop and gives humans actionable errors. Directly
  strengthens the already-ported delta-spec workflow by making its output verifiable.
- **Maps to spec-kit as**: command + script + infra.
- **Value**: H — **Effort**: M/H.
- **Adoption sketch**: `specify validate [item] [--all] [--strict] [--json]`; port the
  leveled-issue contract; validate delta-spec grammar (4-hashtag scenarios, SHALL/MUST
  presence, ADDED/MODIFIED/REMOVED cross-section conflicts) — the delta skill already
  documents these rules, so codify them as checks.

### 5. Adapter-based multi-harness command/skill generation engine
- **Idea**: Replace spec-kit's parallel per-assistant dictionaries with a proper adapter
  abstraction. A tiny `ToolCommandAdapter` interface (`toolId`, `getFilePath(id)`,
  `formatFile(content)`) plus a registry renders one tool-agnostic `CommandContent` /
  `SkillTemplate` into N tool-specific formats (YAML frontmatter, TOML, `.prompt.md`,
  nested vs flat filenames, absolute/global paths for Codex, command-name dialect
  rewriting for opencode/pi). Adding a tool = one ~30-line adapter, not edits across 6
  dicts.
- **Source evidence**: `/cws_work/OpenSpec/src/core/command-generation/types.ts`
  (`ToolCommandAdapter`, `CommandContent`); `.../generator.ts` (pure
  `generateCommand(content, adapter)`); `.../registry.ts` (`CommandAdapterRegistry` static
  Map of 26 adapters); `.../adapters/{claude,cursor,gemini,codex,opencode,github-copilot}.ts`
  (concrete transforms — Gemini TOML, Codex absolute path, opencode `/opsx:`→`/opsx-`);
  `.../yaml.ts` (`escapeYamlValue` centralized frontmatter escaping);
  `/cws_work/OpenSpec/src/core/config.ts` (`AI_TOOLS` registry with per-tool `skillsDir`);
  `/cws_work/OpenSpec/src/core/available-tools.ts` (directory-presence auto-detection).
  Contrast with spec-kit's current `_ASSISTANT_COMMAND_DIRS` / `_ASSISTANT_EXTENSIONS` /
  `_ASSISTANT_ARG_FORMATS` parallel dicts in `src/specify_cli/__init__.py:130-175`.
- **Why it helps**: This is the single most important area for the "universal framework"
  goal. spec-kit supports ~8 tools via brittle parallel dicts; OpenSpec's abstraction
  scales to 29 cleanly and centralizes format quirks (YAML escaping, arg placeholders).
- **Maps to spec-kit as**: infra (a refactor) + agent/tool support.
- **Value**: H — **Effort**: M.
- **Adoption sketch**: Define a Python `ToolAdapter` protocol (`file_path`, `format_file`)
  and a registry; migrate the current dicts into per-tool adapter objects; keep a single
  `escape_yaml_value` helper; a base adapter covers the common md+frontmatter case so most
  tools need almost no code.

### 6. Version-marker idempotency + profile/delivery drift-based selective update
- **Idea**: Stamp every generated file with a `generatedBy: <version>` frontmatter field;
  `update` compares the embedded version (and desired workflow "profile"/"delivery" set)
  against current to decide *per tool* whether regeneration is needed, and prunes files for
  workflows no longer selected. Idempotency for fully-owned files is just full overwrite;
  the version stamp is the only state needed.
- **Source evidence**: `/cws_work/OpenSpec/src/core/shared/skill-generation.ts`
  (`generatedBy` emit); `/cws_work/OpenSpec/src/core/shared/tool-detection.ts`
  (`extractGeneratedByVersion` regex, `needsUpdate` logic);
  `/cws_work/OpenSpec/src/core/update.ts` (smart selective update + pruning helpers);
  `/cws_work/OpenSpec/src/core/profile-sync-drift.ts` (desired-vs-actual file drift);
  `/cws_work/OpenSpec/src/core/init.ts` (`delivery: skills|commands|both`).
- **Why it helps**: spec-kit's refresh/init already has a capability matrix
  (`audit_capability_matrix`) but no per-file version tracking; this gives clean "which
  tools are stale" upgrades and safe pruning when a team changes which workflows they use.
- **Maps to spec-kit as**: infra + script.
- **Value**: M — **Effort**: M.
- **Adoption sketch**: Add `generated_by` to generated command/skill frontmatter; in
  `refresh`, diff embedded vs package version per tool; prune deselected-workflow files.

### 7. `doctor` diagnostics with structured `{severity, code, message, fix}` records
- **Idea**: A read-only health command that reports config/relationship problems as
  structured diagnostics where *every finding carries a pasteable `fix` command*. Human
  mode prints sections with `Fix:` lines; `--json` emits the raw records. Exit 0 for
  "healthy-with-findings", exit 1 only for hard resolution failures.
- **Source evidence**: `/cws_work/OpenSpec/src/commands/doctor.ts` (`printDiagnosticLines`,
  section rendering); `/cws_work/OpenSpec/src/core/relationship-health.ts`
  (`inspectRelationships`, `makeStoreDiagnostic`, error codes like `root_pointer_invalid`,
  `pointer_declarations_inert`); reused by `context` command too.
- **Why it helps**: Gives users (and agents) a one-shot "is my spec-kit install/config
  sane, and how do I fix it" surface. The structured-diagnostic taxonomy (code + fix) is a
  reusable pattern for ALL spec-kit error reporting, not just doctor.
- **Maps to spec-kit as**: command + infra.
- **Value**: M — **Effort**: M.
- **Adoption sketch**: `specify doctor [--json]`; define a `Diagnostic` dataclass; check
  install completeness (spec-kit already computes coverage via `compute_command_coverage`),
  symlink health, config validity — each finding gets a `fix` string.

### 8. Two-tier customization: light `config.yaml` (context + per-artifact rules) vs heavy `schema fork`
- **Idea**: Offer two customization tiers. Light: an `openspec/config.yaml` with a global
  `context` block (injected into every artifact) and a `rules` map keyed by artifact id
  (per-stage constraints) — customizes agent behavior without touching structure. Heavy:
  `schema fork <source>` deep-copies a schema (yaml + templates) into the project layer and
  renames it for editing, resolved via 3-layer shadowing (project > user > package).
- **Source evidence**: `/cws_work/OpenSpec/openspec/config.yaml` (context + per-artifact
  rules example); `/cws_work/OpenSpec/src/core/project-config.ts` (`ProjectConfigSchema`,
  resilient per-field `safeParse`, `validateConfigRules` warns on unknown artifact ids);
  `/cws_work/OpenSpec/src/commands/schema.ts` (`fork`/`init`/`validate`/`which`
  subcommands, kebab-case validation, `copyDirRecursive`);
  `/cws_work/OpenSpec/src/core/artifact-graph/resolver.ts` (project>user>package shadowing).
- **Why it helps**: Lets teams inject house style / tech-stack context and per-stage rules
  (spec-kit's `config.yaml` `rules.specs`, `rules.tasks`, `rules.design` are great concrete
  examples) without forking, then graduate to full pipeline forking when needed. Maps
  perfectly onto spec-kit's existing per-project `.specify/memory` + constitution idea but
  makes it structured and injected.
- **Maps to spec-kit as**: template + infra + command.
- **Value**: M/H — **Effort**: M.
- **Adoption sketch**: Add a `.specify/config.yaml` (`schema`, `context`, `rules`); inject
  `context`+`rules[id]` in the instructions command (#2); add `specify schema fork/init` for
  the heavy path once #1 exists.

### 9. Universal "dual human/JSON output + JSON-purity" convention
- **Idea**: Make *every* command support `--json`, and enforce (via a test helper) that
  JSON mode emits exactly one parseable document to stdout with empty stderr — no spinners,
  logs, or progress bleeding into machine output. Order side-effecting writes before the
  final JSON print so failures still yield one valid document.
- **Source evidence**: `/cws_work/OpenSpec/src/core/list.ts` (parallel `--json`);
  `/cws_work/OpenSpec/test/cli-e2e/basic.test.ts` (`expectJsonOnlyOutput` asserts
  exitCode 0, empty stderr, `JSON.parse` succeeds across list/status/instructions);
  `/cws_work/OpenSpec/src/commands/context.ts` (write-before-print discipline).
- **Why it helps**: Agent tools consume spec-kit via subprocess; clean JSON is the contract
  that makes orchestration robust across all harnesses.
- **Maps to spec-kit as**: infra + convention (+ test).
- **Value**: M — **Effort**: L/M.
- **Adoption sketch**: Standardize a `--json` flag + `emit_json()` helper; add a pytest
  helper `assert_json_only(result)`.

### 10. Console dashboard (`view`) + reusable progress-bar primitive
- **Idea**: A one-shot styled dashboard grouping changes into Draft/Active/Completed (state
  derived from task-checkbox progress) with a progress bar per active change and a summary
  block. Not a live TUI — just a rich single render, trivial to reproduce with Python
  `rich`.
- **Source evidence**: `/cws_work/OpenSpec/src/core/view.ts` (`ViewCommand`,
  `displaySummary`, `createProgressBar`, status-derivation from task progress);
  `/cws_work/OpenSpec/src/core/list.ts` (`formatRelativeTime`, aligned columns).
- **Why it helps**: Gives users an at-a-glance project state; pairs with the DAG/status
  work to visualize pipeline progress.
- **Maps to spec-kit as**: command.
- **Value**: L/M — **Effort**: L.
- **Adoption sketch**: `specify dashboard` using `rich` Panels/Progress; derive status from
  the tasks checklist parser spec-kit already implies.

### 11. Centralized interactivity gate + declarative command registry
- **Idea (a)**: A single `is_interactive()` gate with precedence flag → env override → CI →
  TTY, plus a dedicated env var tests set everywhere to force non-interactive.
  **Idea (b)**: A single declarative `COMMAND_REGISTRY` (name, description, flags,
  positionals, dynamic value sources) that feeds BOTH shell-completion generation AND
  command help/descriptions.
- **Source evidence**: `/cws_work/OpenSpec/src/utils/interactive.ts` (`isInteractive`
  precedence); `/cws_work/OpenSpec/src/core/completions/command-registry.ts` (single source
  for completions + `doctor`/`workset` descriptions);
  `/cws_work/OpenSpec/src/core/completions/factory.ts` (per-shell generator/installer
  factory, zsh/bash/fish/powershell).
- **Why it helps**: Removes scattered TTY checks; one registry avoids description drift and
  gives free shell completion — nice polish for a universal CLI.
- **Maps to spec-kit as**: infra + script.
- **Value**: L/M — **Effort**: M.
- **Adoption sketch**: Add `is_interactive()` helper + `SPECIFY_INTERACTIVE=0`; if pursuing
  completions, build a registry data structure (Typer gives some completion for free).

## Notable code/prompts worth copying (file paths)

- **Artifact-graph engine (port to Python nearly 1:1)**:
  `/cws_work/OpenSpec/src/core/artifact-graph/graph.ts` (Kahn topo sort with sorted queues
  for determinism, `getNextArtifacts`, `getBlocked`), `schema.ts` (DFS cycle-path
  reconstruction), `state.ts` + `outputs.ts` (filesystem-derived completion, glob support).
- **The XML-tagged per-artifact prompt template**:
  `/cws_work/OpenSpec/src/commands/workflow/instructions.ts` `printInstructionsText` — the
  `<artifact>…<project_context (do NOT include)>…<rules>…<template>…<success_criteria>`
  structure is a directly reusable prompt pattern.
- **Validation contract + remediation separation**:
  `/cws_work/OpenSpec/src/core/validation/types.ts`, `constants.ts` (`VALIDATION_MESSAGES`
  with separate `GUIDE_*` fix snippets), `validator.ts` `buildMissingShallOrMustMessage`
  (header-vs-body detection).
- **Adapter pattern**: `/cws_work/OpenSpec/src/core/command-generation/types.ts`,
  `generator.ts`, `registry.ts`, `adapters/gemini.ts` (TOML), `adapters/codex.ts` (global
  absolute path), `adapters/opencode.ts` (command dialect rewrite), `yaml.ts`
  (`escapeYamlValue`).
- **The default schema + templates as a concrete example to mirror**:
  `/cws_work/OpenSpec/schemas/spec-driven/schema.yaml` and
  `/cws_work/OpenSpec/schemas/spec-driven/templates/{proposal,spec,design,tasks}.md`;
  `/cws_work/OpenSpec/openspec/config.yaml` (context + per-artifact rules example).
- **Structured diagnostics**: `/cws_work/OpenSpec/src/core/relationship-health.ts`
  (`makeStoreDiagnostic`, `{severity, code, message, target, fix}`),
  `/cws_work/OpenSpec/src/commands/doctor.ts` rendering.
- **Testing harness**: `/cws_work/OpenSpec/test/helpers/run-cli.ts` (spawn real built CLI,
  force non-interactive env), `test/helpers/fs-snapshot.ts` (`snapshotDirectory` for
  "changes nothing" assertions), `test/helpers/fake-tool.ts` (fake opener that logs
  invocation), `test/cli-e2e/basic.test.ts` (`expectJsonOnlyOutput`),
  `/cws_work/OpenSpec/vitest.setup.ts` (build-once + force-exit teardown),
  `/cws_work/OpenSpec/vitest.config.ts` (`pool: 'forks'` for cwd isolation).

## Anti-patterns / what to skip

- **Do NOT re-port the delta-spec workflow** — already in
  `draft/skills/delta-spec-change/`. The content zod schemas in
  `/cws_work/OpenSpec/src/core/schemas/*.schema.ts` and the delta parser overlap with what
  spec-kit already has; only mine the *validator's* error-reporting/remediation patterns,
  not the delta grammar itself.
- **Worksets** (`/cws_work/OpenSpec/src/core/worksets.ts`, `src/commands/workset.ts`) and
  the **stores/registry** subsystem (`src/core/store/*`, `relationship-health` store bits)
  are a heavy, OpenSpec-specific multi-repo "personal working view" feature. Interesting
  but out of scope for spec-kit's universal-framework goal — skip unless multi-repo
  planning becomes a target. (The `{severity,code,message,fix}` diagnostic pattern is worth
  keeping; the store machinery is not.)
- **The animated ASCII welcome screen** (`src/ui/welcome-screen.ts`, `ascii-patterns.ts`)
  is polish with real complexity (raw-mode stdin, ANSI cursor redraw). Low value for the
  framework goal; skip or reduce to a static banner.
- **Inconsistent YAML escaping**: some OpenSpec adapters use `escapeYamlValue`, others do
  naive interpolation (github-copilot, amazon-q, codex, codebuddy). If porting the adapter
  pattern, apply the shared escaper *uniformly* — don't replicate the inconsistency.
- **Legacy markers**: the `<!-- OPENSPEC:START/END -->` managed-block markers in
  `config.ts` are legacy (only used by `legacy-cleanup.ts`); the current design owns whole
  files and overwrites them. Don't adopt marker-splicing — full-file ownership + a
  `generated_by` version stamp is the cleaner model.
- **`schema` command is marked experimental** in OpenSpec (prints a warning). Treat the
  fork/init UX as a v2 concern; ship the read-only engine (status/instructions/validate)
  first, add authoring commands later.
