# P002 — Skill System Evolution

- **Status:** Draft
- **Pillars:** Skills
- **Source projects:** claude-code-ts, superpowers, claw-code-agent
- **Value:** H · **Effort:** M · **Phase:** 1
- **Related:** [[P001]], [[P003]], [[P010]]

## Problem / Gap

spec-kit's skill system works well at today's scale (a dozen skills under `skills/`, each a
full `SKILL.md`), but it does not scale to the *universal skill library* the framework is
aiming at. Three structural limits are already visible:

1. **No progressive disclosure.** Every skill carries a complete `SKILL.md` (the
   `git-workflow` skill alone is ~490 lines). Discovery relies on the agent noticing the
   Resource Registry table in `.specify/instructions.md` and on long keyword lists embedded
   in each `description`. As the library grows to dozens or hundreds of skills, injecting
   even the descriptions unbudgeted will crowd out the working context, and injecting bodies
   is impossible.
2. **Discovery is keyword-stuffing, not intent-matching.** Skills encode triggers by packing
   bilingual keyword arrays into `description` (see `skills/git-workflow/SKILL.md` line 4).
   There is no dedicated *trigger* field the agent can reason over, and no single mechanism
   that says "before acting, check whether a skill applies."
3. **All skills load unconditionally, always.** A Terraform or database skill is as present
   in a docs-only session as in its native context. There is no way to scope a skill to the
   files in play, and no way to capture a good ad-hoc session into a reusable skill without
   hand-authoring from scratch.

The result: the skill system is authorable but not *scalable* or *self-selecting*. P002
addresses the mechanics of scale; [[P003]] supplies the concrete new skills that will exercise
them; [[P001]]'s SessionStart hook is the injection vehicle.

## Proposal

Evolve the skill system along five independently-adoptable axes, all expressed as
frontmatter/loader/template changes — no change to the `/speckit.*` flow:

1. **Budgeted skill-index injection + lazy body loading.** A compact, character-budgeted
   catalog (`name` · `description` · `when_to_use`) is injected as context; full `SKILL.md`
   bodies are read only when a skill is actually invoked.
2. **`when_to_use` frontmatter + one "invoke-skill" convention.** A dedicated trigger field
   plus a short, calm meta-instruction ("when a skill matches, load and follow it before
   proceeding") that unifies how skills are selected.
3. **Path-conditional / auto-discovered skills.** A `paths:` glob field keeps stack-specific
   skills out of the base index until a matching file is touched; nested `.specify/skills/`
   directories are discovered on demand.
4. **`/skillify` (session → skill capture).** A meta-skill/command that interviews the user
   about a just-completed session and emits a spec-compliant `SKILL.md`.
5. **Optional self-evolving skill-learning.** A lightweight gap log that records
   "no-skill-matched" prompts and, on recurrence, proposes a `/skillify` draft.

## Design sketch

### 1. Budgeted skill index (infra + generator)

Add a generator that emits a catalog from skill frontmatter. It is produced by (or for)
[[P001]]'s SessionStart hook and injected once per session/clear/compact.

```
.specify/skills/_index.md          # generated, machine-maintained
```

```markdown
<!-- SPECIFY-SKILL-INDEX v1 (budget: ~1% of context) -->
- git-workflow — three-tier branch sync. Use when: branch sync, rebase, release flow.
- systematic-debugging — root-cause-first debugging. Use when: a test/behavior is wrong…
- brainstorming — pre-spec design dialogue. Use when: a vague idea needs shaping…
  [+ 40 more · full bodies load on invoke]
```

Budget algorithm, ported in spirit from claude-code-ts
`packages/builtin-tools/src/tools/SkillTool/prompt.ts` (`formatCommandsWithinBudget`,
`SKILL_BUDGET_CONTEXT_PERCENT = 0.01`, `MAX_LISTING_DESC_CHARS`):

- List `name` + a truncated `description`/`when_to_use` per skill under a hard char budget.
- Partition into **never-truncate** (first-party/pinned) and **truncatable** (the rest);
  spend budget on the priority partition first, truncate the tail, and append a
  "N more skills — full bodies load on invoke" footer.
- The full `SKILL.md` is read only at invocation time — the loader already resolves canonical
  paths via `skill_id` (`<SKILL:.specify/skills/<name>/SKILL.md>`), so lazy loading is a read,
  not a new mechanism.

A small Python module under `scripts/python/` (e.g. `build_skill_index.py`) parses frontmatter
and writes `_index.md`; no runtime dependency is added.

### 2. `when_to_use` frontmatter + invoke convention (template)

Extend the SKILL.md frontmatter schema (documented in `docs/skills/`, enforced by
`create-skills`/`improve-skills`) with an optional trigger field:

```yaml
---
name: systematic-debugging
description: |
  Root-cause-first debugging discipline…
when_to_use: >
  A test fails, a behavior is wrong, or output is unexpected — before attempting a fix.
  Trigger phrases: "why is this failing", "flaky test", "it works locally", "regression".
skill_id: "<SKILL:.specify/skills/systematic-debugging/SKILL.md>"
---
```

`when_to_use` is the field the index and the invoke convention reason over; the existing
keyword lists can move here verbatim. Add one calm line to the bootstrap skill / instructions
(not coercive superpowers phrasing): *"Before acting on a request, scan the skill index; if a
skill's `when_to_use` matches, read and follow its `SKILL.md` first."* This gives a single
"invoke-skill" mental model that also covers `/speckit.*` commands.

Add `when_to_use` as a column to the Resource Registry **Skills** table in
`.specify/instructions.md` so the catalog and the registry stay aligned.

### 3. Path-conditional & auto-discovered skills (frontmatter + loader)

```yaml
---
name: database-utils
when_to_use: SQL schema or migration work.
paths: ["**/*.sql", "**/migrations/**", "**/alembic/**"]
---
```

- Skills with `paths:` are **omitted from the base index** and surfaced only after a matching
  file is read/edited (gitignore-style globs).
- Nested `.specify/skills/` under a subproject are discovered by walking up from touched files
  (monorepo support), mirroring claude-code-ts `parseSkillPaths` / `conditionalSkills` /
  `discoverSkillDirsForPaths` in `src/skills/loadSkillsDir.ts`.

This keeps the index lean while making skills context-aware — the base catalog only lists
always-relevant process skills.

### 4. `/skillify` — session → skill capture (command + meta-skill)

Ship a draft command that turns a finished session into a durable skill, reusing the interview
structure of claude-code-ts `src/skills/bundled/skillify.ts` (`SKILLIFY_PROMPT`).

```
templates/commands/skillify.md            # command wrapper (draft)
draft/skills/skillify/SKILL.md            # interview methodology
```

Command frontmatter, matching the existing style (`templates/commands/skills.md`):

```yaml
---
description: Capture the current session into a reusable spec-compliant SKILL.md.
handoffs:
  - label: Update Instructions
    agent: speckit.instructions
    prompt: Register the newly captured skill in the Resource Registry.
    send: true
scripts:
  sh: scripts/bash/create-new-skill.sh --json $ARGUMENTS
---
```

Interview outline (one question at a time): skill name → `when_to_use` triggers → the steps
that worked → success artifacts / verification → inline-vs-fork → save location →
where the user corrected the agent (captured as guardrails). Output is written through the
existing `create-skills` scaffold so directory layout and `${SKILL_HOME}`/`${SKILL_WORKDIR}`
conventions are automatic. This lowers authoring cost, which is the real bottleneck for a
growing library.

### 5. Optional self-evolving skill-learning (infra, deferred within Phase 1)

A minimal, provider-free gap log — not the full claude-code-ts engine:

```
.specify/skills/_gaps.jsonl               # {prompt, ts, matched:false}
```

Modeled on `src/services/skillLearning/skillGapStore.ts` (record → `draftHits >= 2` promotion
gate). When a request matches no skill, append a record; when a similar gap recurs, suggest
`/skillify`. Ranking can reuse a small TF-IDF port of
`src/services/skillSearch/localSearch.ts` (field weights `name:3, when_to_use:2,
description:1`) if fuzzy matching is wanted later. This axis is optional and can land last.

## Source evidence

- Budgeted listing + lazy bodies → `/cws_work/claude-code-ts/packages/builtin-tools/src/tools/SkillTool/prompt.ts` (`formatCommandsWithinBudget`, `SKILL_BUDGET_CONTEXT_PERCENT`, never-truncate partition); lazy body load in `src/skills/loadSkillsDir.ts` (`createSkillCommand.getPromptForCommand`).
- `when_to_use` + invoke-before-acting convention → `packages/builtin-tools/src/tools/SkillTool/prompt.ts` (skill-tool meta-prompt); `src/skills/loadSkillsDir.ts` (`parseSkillFrontmatterFields`); superpowers `skills/using-superpowers/SKILL.md` and the `description: "Use when…"` convention across its skills; claw-code-agent `src/bundled_skills.py` (`when_to_use` + `allowed_tools`).
- Path-conditional / auto-discovery → `src/skills/loadSkillsDir.ts` (`parseSkillPaths`, `conditionalSkills`, `activateConditionalSkillsForPaths`, `discoverSkillDirsForPaths`).
- `/skillify` interview → `/cws_work/claude-code-ts/src/skills/bundled/skillify.ts` (`SKILLIFY_PROMPT`, `disableModelInvocation`).
- Skill-learning / gap store → `src/services/skillLearning/skillGapStore.ts`, `skillGenerator.ts`; TF-IDF matcher `src/services/skillSearch/localSearch.ts`.
- spec-kit targets to extend → `skills/git-workflow/SKILL.md` (keyword-in-description pattern), `.specify/instructions.md` Resource Registry (Skills table), `templates/commands/skills.md`, `scripts/bash/create-new-skill.sh`, `docs/skills/`.

## Adoption plan

**Phase 1 (this proposal), landed in `draft/` first, no `/speckit.*` change:**

1. Add `when_to_use` as an optional frontmatter field; document it in `docs/skills/` and teach
   `create-skills`/`improve-skills` to emit it. Migrate existing keyword lists into it
   (non-breaking — `description` still works).
2. Add `scripts/python/build_skill_index.py` that emits `.specify/skills/_index.md` under a
   char budget. Ship a `when_to_use` column in the Resource Registry Skills table.
3. Wire the index into [[P001]]'s SessionStart injection (index only; bodies stay lazy).
4. Support `paths:` globs + nested-dir discovery in the loader; keep such skills out of the
   base index.
5. Ship `/speckit.skillify` as a draft command + `draft/skills/skillify/`.
6. (Optional, last) `_gaps.jsonl` gap log + recurrence-triggered `/skillify` suggestion.

Each step is reversible and additive; the current unconditional-load behavior remains the
fallback until the index is deliberately promoted out of `draft/`.

## Risks & mitigations

- **Truncation hides a needed skill.** Mitigate with the never-truncate priority partition for
  first-party/process skills and an always-present "N more — load on invoke" footer; the full
  registry in `.specify/instructions.md` remains the exhaustive source.
- **Stale index.** `_index.md` is generated, never hand-edited; regenerate on
  `/speckit.instructions` and in the SessionStart hook so it cannot drift silently.
- **Over-strong invoke phrasing backfires.** Keep the convention calm and advisory, consistent
  with spec-kit's "user instructions take precedence" model — no "BLOCKING / no choice"
  language from the source projects.
- **Path-conditional skills never surface.** Provide an explicit `/speckit.skills` listing that
  shows conditional skills too, so they are discoverable on demand.
- **Skill-learning noise / privacy.** Gap log is opt-in, local-only, prompt-text-truncated, and
  gitignored by default; promotion is a *suggestion*, never automatic write.

## Value / Effort rationale

**Value H.** Progressive disclosure is the single mechanism that lets the skill library scale
past a dozen entries without context blowup — a precondition for [[P003]] and the universal-
framework goal. `when_to_use` + the invoke convention directly raise automatic-selection
quality, and `/skillify` attacks the authoring bottleneck.

**Effort M.** The budget algorithm, frontmatter parsing, path-conditional logic, and the
skillify interview all have near-copy-paste references in claude-code-ts and superpowers. The
work is a Python index generator, additive frontmatter, loader tweaks, and one command
template — no runtime, no new dependency, no change to the `/speckit.*` pipeline. The optional
skill-learning axis is the only H-effort piece and is explicitly deferrable.
