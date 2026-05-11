---
name: create-skills
description: This skill can create new Spec Kit Skills from user input or conversation history. Use this when the user mentions ["create a skill", "new skill", "make a skill", "skill creation", "添加技能", "创建skill", "新建skill"]
skill_id: "<SKILL:.specify/skills/create-skills/SKILL.md>"
---

# create-skills

## Goal

Create a high-quality Spec Kit Skill from explicit user input or by distilling reusable workflows from the current conversation. The expected result is a well-structured `SKILL.md` with valid frontmatter, clear trigger descriptions, appropriate resource organization, and a deterministic registry entry.

Treat Skill creation as **test-driven process documentation**: understand the intended behavior, identify where an agent would fail without the Skill, write only the reusable guidance/resources needed to close that gap, then validate with realistic prompts before reporting completion.

## Quality Bar

A good Skill is an onboarding guide for future agents, not a retrospective about one solved task. It should contain only information that materially improves future execution.

Create or update a Skill when:
- The user asks to create/save/package a reusable workflow as a Skill.
- The conversation reveals a repeatable multi-step workflow with reusable decision logic.
- The task needs specialized tools, references, templates, scripts, or project conventions that a fresh agent would not reliably infer.
- The behavior should be reused across multiple future prompts.

Do not create a Skill when:
- The request is a one-off solution with no expected reuse.
- The behavior is a standard practice already obvious to a general coding agent.
- The constraint is mechanical and should be enforced by validation, tests, scripts, or hooks instead of prose.
- The need is project-specific but belongs in existing always-on instructions rather than an on-demand Skill.

## Workflow

### 1. Determine the creation source

**Case A — User provided explicit input**

Parse intent before writing. Extract or clarify:

1. What the Skill should enable future agents to do.
2. When it should trigger, including concrete user phrases and near-miss cases.
3. The expected output or completion signal.
4. Which resources are needed: `./scripts/`, `./references/`, `./assets/`, or generated `./tools/` manifests.
5. Whether this is a new Skill or an improvement to an existing Skill.

Then parse `skill name` and `description` from the user input:

- **skill name**: A concise command-like identifier matching the project script validator: letters, digits, hyphens (`-`), and underscores (`_`) only. When inventing a name, prefer lowercase kebab-case (for example, `api-testing`) unless the user explicitly needs another valid form.
- **description**: A concise capability summary plus trigger scenarios/keywords. Format: `This skill can <capability>. Use this when the user mentions [ "keyword1", "keyword2", ... ]`.

Keep descriptions discoverable but not overloaded. Include what the Skill does and when to use it; do **not** encode the full workflow in the description, because future agents may shortcut from the description and skip the body.

If the input contains only a valid name and the Skill already exists (`.specify/skills/<name>/SKILL.md`), redirect to `improve-skills` rather than creating a duplicate.

If the description is missing, derive it from the current conversation or ask one targeted clarification question.

**Case B — User provided no input (empty arguments)**

Distill a reusable Skill from the current conversation history:

1. **Review the conversation history**: Identify recurring task patterns, explicit user intent (e.g., "save as a skill", "solidify this workflow"), multi-step operations with reuse value, and domain-specific decision logic.
2. **Distill a reusable workflow**: Extract the core task objective, key execution steps, trigger conditions/keywords, and required tools/scripts/resources.
3. **Generate Skill metadata**: Produce a concise English `name` (e.g., `data-validation`, `api-testing`) and a `description` with capability summary plus trigger keywords.
4. **Minimal clarification**: If critical information cannot be determined, ask **only one question at a time**. Prioritize: target output, scope (project vs personal), checklist vs multi-step workflow.

**Case C — User is improving an existing Skill**

If the user provides an existing Skill path, Skill name, or asks to refine/optimize/debug a Skill:

1. Preserve the existing `name`, directory, `skill_id`, and registry identity unless the user explicitly asks to rename.
2. Read the existing `SKILL.md` and any referenced resources before editing.
3. Identify the specific failure, missing trigger, inefficient step, or resource gap.
4. Prefer minimal changes that improve reusability and validation without rewriting unrelated content.
5. If the request is primarily quality improvement, redirect to `improve-skills` when that Skill exists and is more appropriate.

### 2. Determine SKILL_ROOT and metadata

- **skill name** determines `SKILL_ROOT`. Example: `name = "testing"` → `SKILL_ROOT = .specify/skills/testing/` (project-level).
- **description** must include keywords and trigger scenarios; avoid vague descriptions.

Naming guidance:
- Use lowercase kebab-case for invented names.
- Prefer action-oriented names that describe what the Skill helps do (for example, `create-api-tests`, not `api-test-guide`).
- Keep the folder name identical to `name` in frontmatter.
- Avoid special characters, spaces, parentheses, and display-name wording.

Trigger description guidance:
- Include concrete symptoms, domains, file types, commands, and user phrases that should trigger the Skill.
- Include enough near-miss specificity to avoid accidental invocation by adjacent tasks.
- Avoid vague descriptions such as “helps with testing” or “useful workflow”.
- Avoid long procedural summaries such as “first do A, then B, then C”. Put procedure in the body.

Storage location options (`SKILL_ROOT`):
- `.specify/skills/<name>/` — project-level primary (preferred)
- `.github/skills/<name>/` — compatibility entry (symlink, not primary)
- `~/.copilot/skills/<name>/` — personal-level

### 3. Obtain available tools information

Run the script to get tools available in the current project:

```bash
scripts/bash/refresh-tools.sh --mcp --system --shell --project --json
```

Reference tool manifest categories:
- **MCP Tools** → `tools/mcp.json`
- **System Tools** → `tools/system.json`
- **Shell Tools** → `tools/shell.json`
- **Project Scripts** → `tools/project.json`

Filter available tools against Skill goals for inclusion in `SKILL.md` tool references.

Only mention tools that the Skill actually needs. If a tool command has many flags, link or refer to its help output instead of copying full command documentation into `SKILL.md`.

### 4. Plan reusable contents before writing

Analyze the intended examples before drafting `SKILL.md`:

1. For each example prompt, consider how a fresh agent would solve it without the Skill.
2. Identify repeated work that should become a script, reference, asset, or checklist.
3. Choose the lowest-friction resource type:
	- `./scripts/` for deterministic or repeatedly rewritten operations.
	- `./references/` for detailed schemas, APIs, policies, examples, or long domain knowledge.
	- `./assets/` for templates, images, boilerplate, sample files, or other output inputs.
	- `./tools/` for generated tool manifests and project-tool context.
4. Keep the main body focused on routing, ordering, safety constraints, and links to resources.
5. Do not add placeholder resource directories/files except standard generated structure from project scripts.

### 5. Structure the Skill

#### SKILL.md Specification

**Frontmatter** (minimum required):

```yaml
---
name: <name>
description: <capability + trigger keywords>
---
```

Optional frontmatter (on demand):
- `argument-hint`
- `user-invocable`
- `disable-model-invocation`
- `skill_id`: deterministic identifier for discoverability

**Body** — keep concise and actionable. Must include:
- Result goal
- Key steps (executable, checkable)
- Resource references (use relative paths: `./scripts/x.py`, `./references/details.md`)
- Validation/check criteria for knowing the Skill worked
- Common mistakes or safety limits when they are non-obvious

**Size control**: Keep `SKILL.md` under 500 lines. Move large details into `./references/`.

#### Resource Directory Layout

```
${SKILL_ROOT}/
├── SKILL.md            # Required, Skill main body
├── tools/              # Tool descriptions (optional)
├── scripts/            # Executable scripts (optional)
├── references/         # Reference materials loaded on demand (optional)
└── assets/             # Static assets for outputs (optional)
```

The project creation script may create standard empty resource directories and a `tools/` manifest directory during scaffolding or refresh. Treat those as acceptable generated structure; only fail validation for unrelated documentation files, broken links, or resource directories whose checked-in contents are not needed by the Skill.

#### Progressive Disclosure

1. Discovery: Read `name` + `description`
2. After match: Read `SKILL.md` body
3. When needed: Read `scripts/`, `references/`, `assets/`

Constraints:
- `SKILL.md` recommended < 500 lines
- Reference chain at most one level (from `SKILL.md` directly to resource)
- Use relative paths uniformly (prefer `./references/...`)

#### Content NOT to include

Do not add unrelated documents: `README.md`, `INSTALLATION_GUIDE.md`, `QUICK_REFERENCE.md`, `CHANGELOG.md`, process logs, or full retrospectives.

#### Recommended Body Pattern

Use this structure unless the Skill clearly needs a smaller or domain-specific layout:

1. `## Goal` — one paragraph describing the successful result.
2. `## When to Use` — only if the trigger decision is nuanced after the Skill loads; do not rely on this section instead of a strong frontmatter description.
3. `## Workflow` — numbered executable steps.
4. `## Resources` — relative links and when to read/use each resource.
5. `## Validation` — concrete checks, commands, assertions, or review criteria.
6. `## Anti-Patterns` — mistakes future agents are likely to make.

Prefer one excellent example over many shallow examples. Avoid narrative “what happened in this session” content unless it is converted into reusable rules.

### 6. Test before finalizing

Use a lightweight RED-GREEN-REFACTOR loop adapted to the available environment:

**RED — baseline expectation**
- Create 2-3 realistic test prompts that a future user would actually ask.
- For discipline/process Skills, include at least one pressure scenario where an agent may rationalize skipping the process.
- If subagents or a test harness are available, run at least one baseline without the Skill or compare against the previous version for an update.
- If no runner is available, still write down the likely baseline failure before drafting final text.

**GREEN — minimal Skill**
- Write the smallest `SKILL.md` and resources that address the identified failures.
- Do not overfit to the test prompts; generalize the principle behind the failure.

**REFACTOR — close gaps**
- Validate with the prompts.
- If the Skill user still misses steps, adds unnecessary work, or finds loopholes, revise the Skill to close that specific gap.
- Remove instructions that increase tokens without improving outcomes.

Objective checks are preferred when possible:
- File transforms: verify expected files/fields exist.
- Code workflows: run relevant tests, linters, or project validation.
- Trigger quality: test both should-trigger and near-miss should-not-trigger prompts.
- Human-judged outputs: present clear examples and request feedback.

### 7. Incrementally clarify details

Ask **only one question per round**, waiting for user response. Prioritize:
- Target output: What should the Skill produce?
- Applicable scenarios: Under what trigger conditions?
- Resource needs: Scripts, references, templates, or toolchain?

Iterate until:
1. Frontmatter is complete (`name`, `description`)
2. Body has clear executable steps
3. Resource directories are ready as needed
4. All resource links use relative paths
5. Validation prompts/checks are defined or intentionally skipped with a reason

### 8. Register the Skill

Generate the Resource ID and persist:

- **skill_id**: `<SKILL:.specify/skills/<name>/SKILL.md>`
- **Canonical Path**: `.specify/skills/<name>/SKILL.md`

Write to `.specify/instructions.md` → `### Skills` table:
- `Skill Name`, `Skill ID`, `Description`, `Canonical Path`

Constraints:
- Do not write duplicate entries for the same `skill_id`
- Keep the list sorted and deduplicated
- Remove `None yet.` once real entries exist

### 9. Validate the Skill

Run quality checks before reporting completion. See [the quality checklist](./references/skill-creation-quality-checklist.md) for the full validation workflow.

Minimum checks:
- [ ] Frontmatter: `name` matches directory, `description` has triggers
- [ ] Body: clear steps, no vague placeholders
- [ ] Resources: relative paths, no broken links; standard generated resource directories are acceptable
- [ ] Registry: one deduplicated row in `.specify/instructions.md`
- [ ] Size: `SKILL.md` < 500 lines
- [ ] No unrelated documentation files
- [ ] Test prompts or validation criteria exist; baseline/previous-version comparison was run when feasible
- [ ] Description includes trigger scenarios but does not replace the body with a full workflow summary

### 10. Report completion

Summarize:
- Skill capabilities and directory structure
- `SKILL.md` path and `skill_id`
- Example prompts
- Validation performed and any skipped checks with reasons
- Suggested next-step customizations (e.g., add references, scripts, test prompts, or personalized trigger keywords)

## Design Principles

### Manage Degrees of Freedom

- **High freedom**: Text strategies for multi-path problems
- **Medium freedom**: Pseudocode / parameterized scripts for configurable primary paths
- **Low freedom**: Fixed scripts / steps for high-risk error-prone operations

### Discoverable Descriptions

`description` must include keywords and trigger scenarios. Avoid vague one-liners.

Balance discoverability with body loading:
- Good: states capability, task contexts, file/tool/domain cues, and user phrase examples.
- Bad: lists the complete workflow so a future agent can act from the description alone.
- Include synonyms and multilingual trigger words when the user works across languages.

### Progressive Disclosure and Token Efficiency

- Keep the most common path in `SKILL.md`; move rare, long, or domain-specific details into `./references/`.
- Keep references one level away from `SKILL.md`; avoid nested discovery chains.
- Prefer tables/checklists for scan-heavy guidance.
- Do not duplicate tool help, API docs, or examples already stored in resources.
- If a script is included, test it by running a representative case before reporting success.

### Evaluation Mindset

- A Skill is successful only if a fresh agent performs better with it than without it or better than the previous version.
- For new Skills, compare against a no-Skill baseline when feasible.
- For updates, preserve identity and compare against the old behavior when feasible.
- Capture exact agent mistakes or rationalizations from tests and address those directly.
- Generalize from feedback instead of adding brittle prompt-specific rules.

### Anti-Patterns

- Vague descriptions that fail to trigger
- Descriptions that summarize the whole workflow and let agents skip the body
- `SKILL.md` too large without splitting into `./references/`
- Directory name inconsistent with `name` in frontmatter
- Missing executable steps (only background prose)
- Inconsistent or broken resource paths
- Untested Skills with no realistic prompts, validation criteria, or stated skip reason
- Narrative session logs instead of reusable guidance
- Batch-creating multiple Skills without validating each one

## Slash Behavior Notes

Skill behavior in the `/` menu is controlled by frontmatter:
- Default: Manually invocable + auto-triggerable
- `user-invocable: false`: Not manually invocable
- `disable-model-invocation: true`: Not auto-triggerable
- Both set: Both disabled

## Continuous Improvement

1. Validate the skill with real tasks
2. Record pain points and inefficient steps
3. Revise `SKILL.md` or resource directories
4. Validate again, forming a stable iteration