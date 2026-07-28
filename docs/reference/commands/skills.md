# /speckit.skills

Manage specialized AI agent skills — create new skills or refresh and modernize existing ones.

## When to Use

- To create a new reusable skill for a specialized workflow
- To refresh and modernize an existing skill to comply with the current spec
- When you need to validate skill structure and registry consistency
- After creating skills that need to be discoverable by AI agents

## Syntax

```text
/speckit.skills [argument]
```

| Input | Behavior |
|-------|----------|
| `"name - description"` | Create a new skill |
| `"existing-skill-name"` | Modernize and improve an existing skill |
| No arguments | Infer target from conversation context |

## Execution Flow

### Step 1: Parse Target Skill

Extracts the target skill name from the arguments. The name must be a concise command-like identifier using letters, digits, hyphens, and underscores.

### Step 2: Check Target Existence

Determines whether `.specify/skills/<name>/SKILL.md` already exists.

### Step 3: Route to Correct Workflow

**If the skill does NOT exist** → delegates to `create-skills`:
- Parses explicit input or distills from conversation
- Minimal clarification questions
- Scaffolds SKILL.md structure, resource directories
- Registers the skill and reports completion
- **Propagates the skill to built-in agents**: analyzes the 7 built-in role agents, proposes which ones the new skill is role-relevant to, and (after confirmation) adds the skill to those agents' `skills:` frontmatter and `## Skill Enablement` table (see [Agent propagation](#agent-propagation-create-path))

**If the skill ALREADY exists** → delegates to `improve-skills` with a two-phase pass:

1. **Phase A — Spec-compliance modernization (mandatory)**:
   - Canonical path validation (`.specify/skills/<name>/SKILL.md`)
   - Directory layout check (`scripts/`, `references/`, `assets/`)
   - Frontmatter fields validation (`name`, `description`, `skill_id`)
   - Path convention enforcement (`${SKILL_HOME}` / `${SKILL_WORKDIR}`)
   - Legacy idiom migration (bare relative paths → `${SKILL_HOME}/...`)
   - Registry consistency in `.specify/instructions.md`
   - Hygiene (size limits, reference chain depth)

2. **Phase B — User-requested refinement**:
   - Evidence collection from execution history
   - Root-cause analysis
   - Minimal targeted changes
   - Validation

### Step 4: Validate and Report

- Confirms frontmatter is valid and canonical path matches
- Verifies Skills registry in `.specify/instructions.md`
- Reports created/updated paths, `skill_id`, and registry edits
- Lists which modernization items required edits vs. were already compliant
- (Create path) Lists which built-in agents the skill was propagated to

## Agent propagation (create path)

When a **new** skill is created, `/speckit.skills` wires it into the built-in role agents so they prefer it for role-relevant work (Feature 026 Skill Enablement convention):

1. Skips non-declarable skills (reference-only/meta: `create-agent`, `improve-agent`, `create-skills`, `improve-skills`, `create-team`, `improve-team`).
2. Analyzes the 7 built-in role agents (`requirements-analyst`, `system-designer`, `module-designer`, `test-engineer`, `qa-engineer`, `knowledge-manager`, `ux-analyst`) against the skill's capability and triggers.
3. Proposes a `Agent | Skill | When to use` table and waits for confirmation.
4. On confirm, adds the canonical slug to each matched agent's `skills:` frontmatter and a row to its `## Skill Enablement` table, in both `agents/<slug>.agent.md` and `.specify/agents/<slug>.agent.md`. Generator templates are not modified.

If no agent is role-relevant, propagation is skipped (no forced use).

## Skill Directory Structure

```
.specify/skills/<name>/
├── SKILL.md         # Required — skill definition
├── scripts/         # Executable scripts (optional)
├── references/      # On-demand reference docs (optional)
└── assets/          # Output templates / static assets (optional)
```

## Path Conventions

| Variable | Purpose | Example |
|----------|---------|---------|
| `${SKILL_HOME}` | Skill's on-disk directory (post-symlink) | `${SKILL_HOME}/scripts/init.sh` |
| `${SKILL_WORKDIR}` | Runtime working directory (user's project root) | `${SKILL_WORKDIR}/output.md` |

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Skill definition | `.specify/skills/<name>/SKILL.md` |
| Skill scripts | `.specify/skills/<name>/scripts/` |
| Registry update | `.specify/instructions.md` → Skills section |
| Agent skill enablement (create path) | `agents/<slug>.agent.md` + `.specify/agents/<slug>.agent.md` |

## Prerequisites

- (Optional) Run [`/speckit.instructions`](instructions.md) if skill behavior depends on project context

## Next Steps

- Run [`/speckit.instructions`](instructions.md) to update project instructions so the skill is discoverable
