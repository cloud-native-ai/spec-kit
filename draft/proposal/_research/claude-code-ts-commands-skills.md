# Mining report: claude-code-ts — command, skill & UX systems

Source scope: `/cws_work/claude-code-ts` (large TS reimplementation of Claude Code).
Lens: ideas to evolve spec-kit into a universal SKILLS + COMMANDS + WORKFLOWS + SCRIPTS framework.

## Project snapshot

claude-code-ts is a very large, production-grade TypeScript CLI/TUI that reimplements Claude Code. Its command surface has two tiers: (1) ~150 hardcoded slash commands registered as `Command` objects in `src/commands.ts` (each a `type: 'prompt' | 'local-jsx' | 'local'` object with a `getPromptForCommand`/`load`), and (2) a filesystem-driven skill/command system (`src/skills/loadSkillsDir.ts`) that discovers markdown skills from layered sources (managed/policy, user `~/.claude/skills`, project `.claude/skills`, `--add-dir`, plugins, bundled, and MCP). Skills and slash commands are unified: a skill *is* a prompt-`Command` with frontmatter. The model invokes them through a single `Skill` tool whose description is a **character-budgeted listing** of skill name + `description`/`when_to_use` (`packages/builtin-tools/src/tools/SkillTool/prompt.ts`), while full skill bodies are loaded only on invocation (progressive disclosure). Around this sit several UX subsystems: output-styles (`src/outputStyles/`), personas/"modes" (`src/modes/`), a plugin/marketplace layer (`src/plugins/`, `src/utils/plugins/`), keybindings (`src/keybindings/`), proactive/tick autonomy (`src/proactive/`), a TF-IDF **skill-search** matcher (`src/services/skillSearch/`), and a self-evolving **skill-learning** engine that detects skill gaps and auto-drafts skills (`src/services/skillLearning/`).

## Top ideas for spec-kit

### 1. Progressive disclosure: budgeted skill *index* injected as context, full body loaded on invoke
- **Source evidence:** `packages/builtin-tools/src/tools/SkillTool/prompt.ts` (`formatCommandsWithinBudget`, `SKILL_BUDGET_CONTEXT_PERCENT = 0.01`, `MAX_LISTING_DESC_CHARS`, bundled-never-truncated partitioning); `src/commands.ts` `getSkillToolCommands`; `src/skills/loadSkillsDir.ts` `createSkillCommand.getPromptForCommand` (body loaded lazily).
- **Why it helps:** spec-kit's skills each carry a full `SKILL.md`; injecting them all bloats context. This pattern lists only `name: description - when_to_use` under a hard char budget (1% of context), reserves budget for high-priority skills, truncates the rest, and defers full bodies until invocation. It's the core mechanism that lets a *universal* framework scale to hundreds of skills/commands without context blowup.
- **Maps to spec-kit as:** infra + skill (loader/injector).
- **Value:** H · **Effort:** M.
- **Adoption sketch:** Add a `specify skills index` step that emits a compact catalog (name/description/when_to_use) into each harness's system-reminder/context, and have the invocation path read the full `SKILL.md` on demand. Reuse the char-budget + never-truncate-priority partition logic.

### 2. `when_to_use` frontmatter + a single "invoke a skill" tool prompt with BLOCKING-invocation semantics
- **Source evidence:** `packages/builtin-tools/src/tools/SkillTool/prompt.ts` (getPrompt text: "When a skill matches… this is a BLOCKING REQUIREMENT: invoke… BEFORE generating any other response"; slash-command == skill framing); `when_to_use` parsed in `src/skills/loadSkillsDir.ts` (`parseSkillFrontmatterFields`).
- **Why it helps:** spec-kit skills use `description` only. A dedicated `when_to_use` field (trigger scenarios + example phrases) plus a firm meta-prompt dramatically improves *automatic* skill selection — key for a universal assistant where the user shouldn't have to know command names. Also unifies "/command" and "skill" mentally for the model.
- **Maps to spec-kit as:** template (SKILL.md frontmatter) + infra (invocation prompt).
- **Value:** H · **Effort:** L.
- **Adoption sketch:** Add optional `when_to_use:` to SKILL.md and command frontmatter; append example trigger phrases; adopt the "blocking requirement / never mention without invoking" phrasing in each harness's skill-tool/instructions text.

### 3. Path-conditional & dynamically-discovered skills (auto-activate by files touched)
- **Source evidence:** `src/skills/loadSkillsDir.ts` — `parseSkillPaths`, `conditionalSkills`, `activateConditionalSkillsForPaths` (gitignore-style `paths:` frontmatter), `discoverSkillDirsForPaths`/`addSkillDirectories` (walk up from touched files to find nested `.claude/skills`).
- **Why it helps:** Makes skills context-aware without bloating the index: a skill with `paths: ["**/*.tf"]` only surfaces once Terraform files are touched; nested project skills load on demand. Perfect for a universal framework spanning many stacks/subdirs — spec-kit currently loads all skills unconditionally.
- **Maps to spec-kit as:** skill (frontmatter) + infra (loader).
- **Value:** H · **Effort:** M.
- **Adoption sketch:** Support `paths:` glob frontmatter; keep such skills out of the base index and inject them only after a matching file is read/edited; add upward-walk discovery for monorepo subproject skills.

### 4. Self-evolving skills: skill-gap detection → auto-draft → promote
- **Source evidence:** `src/services/skillLearning/skillGapStore.ts` (`SkillGapRecord`, `draftHits`, `draftHitSessions`, promotion gate `draftHits >= 2`, status `pending|draft|active|rejected`), `src/services/skillLearning/skillGenerator.ts` (`generateSkillDraft`, `writeLearnedSkill` → writes `SKILL.md`), `types.ts` (instincts/domains); command `src/commands/skill-learning/index.ts`.
- **Why it helps:** Directly advances the universal-framework vision: when a user repeatedly asks for something with no matching skill, the system records the gap, drafts a skill, and promotes it to active after repeated recurrence — the framework grows itself from usage.
- **Maps to spec-kit as:** agent/workflow + infra.
- **Value:** M · **Effort:** H.
- **Adoption sketch:** Start small — a `specify skills gaps` command that logs "no-skill-matched" prompts to a project store, plus a `/speckit.skillify`-style generator (see #5) triggered when a gap recurs.

### 5. `/skillify`: interactive interview that captures a session into a reusable SKILL.md
- **Source evidence:** `src/skills/bundled/skillify.ts` (full `SKILLIFY_PROMPT`: analyze session → multi-round AskUserQuestion interview → write SKILL.md with `name/description/allowed-tools/when_to_use/argument-hint/arguments/context`), `disableModelInvocation: true`.
- **Why it helps:** Lowers the authoring cost of the whole framework. spec-kit wants users to build up skills/workflows; this turns a completed ad-hoc session into a durable, parameterized skill via guided Q&A (name, steps, success artifacts, inline-vs-fork, save location, triggers). It even codifies "capture where the user corrected you."
- **Maps to spec-kit as:** command + template (authoring workflow).
- **Value:** H · **Effort:** M.
- **Adoption sketch:** Ship `/speckit.skillify` as a command template that reads session history + spec-kit's SKILL.md schema and writes to `skills/<name>/SKILL.md`. Reuse the interview structure almost verbatim.

### 6. Rich skill/command frontmatter: model, effort, context:fork+agent, hooks, allowed-tools, user-invocable/disable-model-invocation, version, argument-hint/arguments
- **Source evidence:** `src/skills/loadSkillsDir.ts` `parseSkillFrontmatterFields` + `createSkillCommand`; `src/types/command.ts` (fields `model`, `effort`, `context: 'inline'|'fork'`, `agent`, `hooks`, `skillRoot`, `paths`, `disableModelInvocation`, `userInvocable`, `version`, `argNames`).
- **Why it helps:** A universal framework needs per-skill execution policy. Standouts vs spec-kit: `context: fork` + `agent:` (run a skill as a sub-agent with its own context/token budget — unifies skills and role-agents), per-skill `model`/`effort`, per-skill `hooks`, and the `disable-model-invocation`/`user-invocable` axis (some skills are user-only, some model-only, some both).
- **Maps to spec-kit as:** template (frontmatter schema) + infra.
- **Value:** M · **Effort:** M.
- **Adoption sketch:** Extend spec-kit SKILL.md/command frontmatter with `context`, `agent`, `model`, `effort`, `allowed-tools`, `user-invocable`, `disable-model-invocation`; the fork+agent field is the bridge that unifies spec-kit's skills and role-based agents.

### 7. Variable substitution + inline shell in skill bodies (`${CLAUDE_SKILL_DIR}`, `${CLAUDE_SESSION_ID}`, `!\`cmd\``) with MCP untrusted-source guard
- **Source evidence:** `src/skills/loadSkillsDir.ts` `getPromptForCommand` (baseDir prefix, `${CLAUDE_SKILL_DIR}`/`${CLAUDE_SESSION_ID}` replacement, `executeShellCommandsInPrompt`, and the `loadedFrom !== 'mcp'` guard: "MCP skills are remote and untrusted — never execute inline shell").
- **Why it helps:** spec-kit skills bundle `scripts/` and `assets/` but must hardcode paths. `${CLAUDE_SKILL_DIR}` lets a SKILL.md reference its own bundled scripts portably, and inline `!\`...\`` injects live command output into the prompt at load time (great for "current git state" style skills). The trust-tier guard is a clean security model for a marketplace/multi-source framework.
- **Maps to spec-kit as:** infra (prompt templating) + script.
- **Value:** M · **Effort:** L.
- **Adoption sketch:** Add `${SPECIFY_SKILL_DIR}` / session-id substitution and (optionally) load-time shell injection to spec-kit's command/skill renderer; gate shell execution off for any remote/untrusted source.

### 8. Output-style system (swap the base system prompt) as file-based `.md`
- **Source evidence:** `src/outputStyles/loadOutputStylesDir.ts` (loads `.claude/output-styles/*.md`, frontmatter `name/description/keep-coding-instructions`, body becomes system prompt), `src/constants/outputStyles.ts` (built-in Explanatory/Learning styles, `keepCodingInstructions`).
- **Why it helps:** spec-kit has NO output-style system. This gives a lightweight, user-authorable way to reshape the assistant's whole voice/behavior (e.g., "SDD-strict", "teaching", "terse") without touching commands — a natural fit for a universal framework that serves different audiences.
- **Maps to spec-kit as:** infra + template.
- **Value:** M · **Effort:** L.
- **Adoption sketch:** Support `.specify/output-styles/*.md`; a `specify output-style <name>` selector that prepends the chosen prompt; `keep-coding-instructions`-style flag to append vs replace base instructions.

### 9. Persona/"modes": named bundles of system-prompt + permissions + verbosity + model
- **Source evidence:** `src/modes/types.ts` (`CCBMode`: systemPrompt, model, permissions.defaultMode, responseStyle.verbosity, UI accent), `src/modes/defaults.ts` (Default/Gentle/Dr.Sharp/Workhorse/Token-Saver/Super-AI, each with a distinct prompt + `acceptEdits` vs `default` permission + verbosity).
- **Why it helps:** A mode ties together *behavior + autonomy + model* as one switch — richer than output-styles. For spec-kit, "modes" could encode SDD phases or autonomy levels (e.g. a "Workhorse" mode with auto-accept for scaffolding vs a "Dr. Sharp" strict-review mode). This is the "interactive modes" spec-kit currently lacks.
- **Maps to spec-kit as:** infra + agent/template.
- **Value:** M · **Effort:** M.
- **Adoption sketch:** Define spec-kit modes as data (prompt + permission default + verbosity + model); expose `specify mode <slug>`; seed with SDD-oriented personas.

### 10. Built-in plugin registry with enable/disable, and a plugin marketplace layer
- **Source evidence:** `src/plugins/builtinPlugins.ts` (`registerBuiltinPlugin`, `getBuiltinPlugins` enabled/disabled split via `settings.enabledPlugins`, `{name}@builtin` id scheme, plugins bundle skills+hooks+mcpServers, `skillDefinitionToCommand`), `src/plugins/bundled/index.ts`, `src/utils/plugins/loadPluginCommands.ts` (frontmatter parsing for plugin skills).
- **Why it helps:** spec-kit has NO plugin marketplace. This shows a clean model: a *plugin* is a togglable bundle of (skills + commands + hooks + MCP servers), sourced from a named marketplace or built-in, persisted enabled-state in settings. It's the packaging/distribution story for a universal framework.
- **Maps to spec-kit as:** infra.
- **Value:** M · **Effort:** H.
- **Adoption sketch:** Define a spec-kit plugin manifest (name/version + skills/commands/scripts/agents it contributes); support enable/disable in `.specify` settings; ship first-party bundles as "built-in plugins."

### 11. TF-IDF skill-search matcher (offline intent → skill ranking)
- **Source evidence:** `src/services/skillSearch/localSearch.ts` (`SkillIndexEntry`, weighted TF with `FIELD_WEIGHT {name:3, whenToUse:2, description:1, allowedTools:0.3}`, `computeIdf`, tokenize/stem incl. CJK bigrams, stopwords), command `src/commands/skill-search/index.ts`.
- **Why it helps:** A dependency-free, local ranking that scores skills against the current prompt — used to surface/pre-select the right skill. For spec-kit this is a self-contained way to power both proactive suggestions and gap detection (#4) without an embedding service.
- **Maps to spec-kit as:** infra/script.
- **Value:** M · **Effort:** M.
- **Adoption sketch:** Port the tokenizer + weighted TF-IDF as a small Python module; index SKILL.md frontmatter; use for `specify suggest` and gap logging.

### 12. Layered source resolution + symlink-aware dedup + fail-soft loading
- **Source evidence:** `src/skills/loadSkillsDir.ts` (`getSkillsPath` per source, parallel load of managed/user/project/additional/legacy, `getFileIdentity` via `realpath` dedup, first-wins precedence, gitignore skip, `--bare` mode, plugin-only policy lock).
- **Why it helps:** spec-kit will need clear precedence when the same skill exists in user vs project vs plugin. This is a battle-tested resolution+dedup+security model (policy-managed skills, gitignored-dir skip, per-source enable flags) worth mirroring.
- **Maps to spec-kit as:** infra.
- **Value:** M · **Effort:** M.
- **Adoption sketch:** Adopt explicit source ordering (managed > user > project > plugin > bundled), realpath dedup, and per-source enable/lock flags in spec-kit's loader.

### 13. Proactive tick loop (optional autonomous continuation)
- **Source evidence:** `src/proactive/index.ts` (state machine inactive→active→paused, `shouldTick`, `setContextBlocked` to prevent tick→error runaway, `getNextTickAt` countdown), `src/proactive/useProactive.ts`.
- **Why it helps:** spec-kit has NO proactive mode. A guarded tick loop could drive long SDD workflows (spec→plan→tasks→implement) semi-autonomously, with the error-block safeguard preventing runaways.
- **Maps to spec-kit as:** infra/workflow.
- **Value:** L · **Effort:** H.
- **Adoption sketch:** Optional; likely defer. If pursued, model it as a workflow driver with the same block-on-error safeguard.

## Notable code/prompts worth copying (file paths)

- `packages/builtin-tools/src/tools/SkillTool/prompt.ts` — the entire budgeted-listing algorithm (`formatCommandsWithinBudget`) and the Skill-tool meta-prompt. Nearly copy-paste-able intent.
- `src/skills/bundled/skillify.ts` — the `SKILLIFY_PROMPT` interview script; a ready-made `/speckit.skillify` command body.
- `src/skills/loadSkillsDir.ts` — reference implementation for frontmatter parsing (`parseSkillFrontmatterFields`), conditional/dynamic skills, `${CLAUDE_SKILL_DIR}` substitution, and layered dedup.
- `src/modes/defaults.ts` — concrete persona system-prompts (Dr. Sharp / Workhorse / Token-Saver) that map cleanly to SDD modes.
- `src/services/skillSearch/localSearch.ts` — self-contained TF-IDF matcher with field weights.
- `src/services/skillLearning/skillGapStore.ts` + `skillGenerator.ts` — gap-record → draft → promote lifecycle.
- `src/constants/outputStyles.ts` + `src/outputStyles/loadOutputStylesDir.ts` — output-style schema and loader.

## Anti-patterns / what to skip

- **Do not copy `src/commands.ts`'s 150+ hardcoded imports + `feature()`-flag conditional `require()` sprawl.** It's the opposite of the file-driven, universal design spec-kit wants; keep spec-kit's commands as data/templates, not compiled-in objects. Only mine the *filtering/registration* helpers (`getSkillToolCommands`, dedup), not the giant static array.
- **Skip the deep TUI/React coupling** (`.tsx` panels, `KeybindingContext`, ink `stringWidth`) — spec-kit is a harness-agnostic CLI; the keybindings subsystem is TUI-specific and not portable to the multi-harness model.
- **Don't adopt the proactive tick loop early** — high effort, and autonomous continuation is risky without spec-kit's SDD guardrails first.
- **The `enabledPlugins`/settings-persistence + marketplace machinery is heavy** — mine the manifest *concept* (a plugin = skills+commands+hooks+mcp bundle with enable/disable) rather than the full marketplace/OAuth/remote-loading stack.
- **Analytics/telemetry plumbing** (`logEvent`, `tengu_*` events) threaded through loaders is noise for spec-kit — strip it when porting.
- **`context: fork` + `agent` is powerful but implies a sub-agent runtime** — only valuable if spec-kit commits to running skills as sub-agents; otherwise treat as future-facing frontmatter, not immediate infra.
