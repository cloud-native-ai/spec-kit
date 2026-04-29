> Note
>
> - Argument Format: `<name> - <description>` (e.g., `testing - Unit testing utils`)
> - Or use flags: `--name <name> --description <desc>`

## User Input

```text
$ARGUMENTS
```

You **MUST** analyze the user input in `$ARGUMENTS` to extract the two core elements of a Skill: `name` and `description`.

1. *name*: A concise command-like identifier using only letters, digits, hyphens (`-`), and underscores (`_`). Must follow standard programming variable naming conventions and contain no special characters.
2. *description*: A brief statement of what the Skill does, followed by a list of trigger keywords. Format: `This skill can <capability>. Use this when the user mentions [ "keyword1", "keyword2", ... ]`.

### Input Classification & Processing Strategy

**Check the user input**: Determine whether `$ARGUMENTS` is empty or contains only whitespace.

- **Case A: User provided input**  
  Extract `name` and `description` from the input following the rules above, then proceed to [Step 1](#step-1-determine-skill_root-and-metadata).

- **Case B: User provided no input (empty arguments)**  
  This **MUST** be interpreted as: **create a Skill from the current conversation history**. Execute the following:

  1. **Review the conversation history**: Analyze the current session's user–AI interactions to identify:
     - Recurring task patterns or workflows
     - Explicit user intent such as "save as a skill", "create a skill", "solidify this workflow"
     - Multi-step operations with clear reuse value
     - Domain-specific expertise or decision logic

  2. **Distill a reusable workflow**: Extract from the conversation:
     - Core task objective (what it does)
     - Key execution steps (how to do it)
     - Trigger conditions and keywords (when to use it)
     - Required tools, scripts, or resources (what it needs)

  3. **Generate Skill metadata**: Based on the distilled results, produce:
     - `name`: A concise English identifier (e.g., `data-validation`, `api-testing`)
     - `description`: A capability summary plus trigger keyword list

  4. **Minimal clarification**: If critical information cannot be determined from the conversation, ask **only one question at a time**. Prioritize:
     - "I noticed we discussed [topic] — would you like to turn this workflow into a Skill?"
     - "What is the primary output or goal of this Skill?"

  5. **Confirm and proceed**: Once the user confirms, continue with [Step 1](#step-1-determine-skill-root-and-metadata) through the full workflow.

## Outline

Goal: Help users create or refine high-quality SpecKit Skills within the current conversation context, ensuring structured specifications, clear triggers, reusable resources, and a deterministic reusable `skill_id` for each skill.

Main workflow:
1. Prioritize distilling reusable workflows from the current conversation
2. Only ask minimal clarifying questions when necessary (one question at a time)
3. Iteratively refine `SKILL.md` and supporting resources until ready for use

## Skill Specification

### 1) SKILL_ROOT and Basic Structure

**SKILL_ROOT** is the root directory where a Skill resides. The main body of a Skill is `${SKILL_ROOT}/SKILL.md`, and all other resource directories are resolved relative to `SKILL_ROOT`.

Typical structure:

```
${SKILL_ROOT}/
├── SKILL.md            # Required, Skill main body
├── tools/              # Tool descriptions (relative to SKILL_ROOT, optional)
├── .specify/scripts/            # Executable scripts (relative to SKILL_ROOT, optional)
├── references/         # Reference materials loaded on demand (relative to SKILL_ROOT, optional)
└── assets/             # Static assets for outputs (relative to SKILL_ROOT, optional)
```

**Storage location**: `SKILL_ROOT` can be in any of the following paths (project-level or personal-level):

- `.specify/skills/<name>/` (project-level primary directory)
- `.github/skills/<name>/` (compatibility entry, does not host primary copy)
- `.agents/skills/<name>/`
- `.claude/skills/<name>/`
- `~/.copilot/skills/<name>/`
- `~/.agents/skills/<name>/`
- `~/.claude/skills/<name>/`

All subsequent resource references use paths relative to `SKILL_ROOT` (prefer `./.specify/scripts/x.py` form).

### 2) `SKILL.md` Specification

#### Frontmatter

Minimum required:

- `name` (required, recommended to match directory name)
- `description` (required, describes "what it does + when to trigger")

Optional (on demand, following official behavior):

- `argument-hint`
- `user-invocable`
- `disable-model-invocation`

Note: This project defaults to `name` and `description` as core trigger metadata; only introduce optional fields when truly needed.

#### Body

Body contains only execution instructions, no redundant background. Must include:

- Result goal
- Key steps (executable, checkable)
- Resource references (use relative paths, e.g., `./.specify/scripts/x.py`)

### 3) Resource Directory Usage Guidelines

#### `tools/`

The `tools/` directory under the Skill root describes the tools available to this Skill. Project-level tool manifests come from the JSON generated by `.specify/scripts/bash/refresh-tools.sh`:

- [MCP Tools JSON](tools/mcp.json)
- [System Tools JSON](tools/system.json)
- [Shell Tools JSON](tools/shell.json)
- [Project Scripts JSON](tools/project.json)

#### `.specify/scripts/`

Used for high-repetition, deterministic tasks (Python/Bash, etc.).

- Applicable: Writing repetitive logic, or operations that are error-prone and need stable reproducibility
- Value: Saves tokens, executable, reusable

#### `references/`

Used for on-demand document knowledge (e.g., schemas, APIs, policies).

- Applicable: High information volume but not needed every time
- Principle: Put details in `references/`, keep `SKILL.md` only for navigation and core workflow
- Large file recommendation: Provide search hints in `SKILL.md`; add a table of contents for reference files exceeding 100 lines

#### `assets/`

Used for resources needed by outputs but unnecessary in context (templates, images, fonts, boilerplate projects, etc.).

### 4) Context Loading and Size Control

Use progressive loading:

1. Discovery phase: Read `name` + `description`
2. After match: Read `SKILL.md` body
3. When needed: Then read `.specify/scripts/`, `references/`, `assets/`

Constraints:

- `SKILL.md` recommended < 500 lines
- Reference chain should be at most one level (from `SKILL.md` directly to resource)
- Resource paths use relative paths uniformly (prefer `./`)

### 5) Content NOT to Include in a Skill

A Skill only retains content needed for task execution; do not add unrelated documents:

- `README.md`
- `INSTALLATION_GUIDE.md`
- `QUICK_REFERENCE.md`
- `CHANGELOG.md`
- Other process review / test record appendices

## Design Principles

### 1) Manage Degrees of Freedom

- High freedom: Text strategies, suitable for multi-path problems
- Medium freedom: Pseudocode / parameterized scripts, suitable when there's a primary path but configurability needed
- Low freedom: Fixed scripts / fixed steps, suitable for high-risk error-prone operations

### 2) Discoverable Descriptions

`description` must include keywords and trigger scenarios; avoid vague descriptions.

### 3) Anti-Patterns

- Vague descriptions that fail to trigger
- `SKILL.md` too large without splitting
- Directory name inconsistent with `name`
- Missing executable steps

## Planning Strategy (Official Workflow Aligned)

### Step A: Distill First, Then Ask

First distill from the current conversation:

- Reusable steps
- Decision branches
- Quality checkpoints

If distillation is sufficient, proceed directly to draft.

### Step B: Clarify When Necessary

Only ask when critical information is missing, and **one question at a time**. Prioritize:

- What is the target output?
- Is the scope workspace or personal?
- Is a checklist or a complete multi-step workflow needed?

### Step C: Iterate to Convergence

1. Draft and save
2. Identify the weakest point
3. Ask a targeted question and revise
4. Produce a usable version (including example prompts and follow-up customization suggestions)

## Execution Steps

The core workflow for creating a Skill is as follows:

### Step 1: Determine SKILL_ROOT and Metadata

Parse `skill name` and `description` from user input:

- **skill name** determines the `SKILL_ROOT` path. For example, with `name = "testing"` and a project-level storage location, `SKILL_ROOT = .github/skills/testing/`.
- **description** describes "what it does + when to trigger" and must include keywords and trigger scenarios; avoid vague descriptions (see Design Principles point 2).

If input information is insufficient, proceed to Step 3 for clarification.

### Step 2: Obtain Available Tools Information

Run the script to get the tools available in the current project/workspace, providing a basis for the Skill's resource orchestration:

- Run `refresh-tools.sh` (or equivalent) to refresh and output JSON.
- Reference tool manifest categories:
  - **MCP Tools** → [mcp.json](tools/mcp.json)
  - **System Tools** → [system.json](tools/system.json)
  - **Shell Tools** → [shell.json](tools/shell.json)
  - **Project Scripts** → [project.json](tools/project.json)

Use the following command to get the tool manifest as needed:

```bash
.specify/scripts/bash/refresh-tools.sh --json
```

After obtaining the tool list, filter available tools against Skill goals as reference for tool references in `SKILL.md`.

### Step 3: Incrementally Clarify Skill Details

Fill in the information needed for `SKILL.md` through questioning. **Ask only one question per round**, waiting for user response before continuing.

Prioritize:

- **Target output**: What should the Skill ultimately produce?
- **Applicable scenarios**: Under what trigger conditions should this Skill be loaded?
- **Resource needs**: Are scripts, references, templates, or a fixed toolchain needed?

Iteratively revise `SKILL.md` until:

1. Frontmatter is complete (`name`, `description`)
2. Body contains clear executable steps
3. Resource directories (`tools/`, `.specify/scripts/`, `references/`, `assets/`) are ready as needed
4. All resource links use paths relative to `SKILL_ROOT`

### Step 4: Register Resource ID and Write to Instructions

Generate the Resource ID for `SKILL.md` and persist it:

- **Canonical ID (`skill_id`)**: Workspace-relative path of `.specify/skills/<name>/SKILL.md`.
- **Canonical Path**: Workspace-relative path of `${SKILL_ROOT}/SKILL.md`.

Write the following into the `## Resource Registry` → `### Skills` section of `.specify/instructions.md`:

- `Skill Name`
- `Skill ID`
- `Description`
- `Canonical Path`

Constraints:

- Entry field names reference `.specify/templates/skills-template.md`.
- Do not write duplicate entries for the same `skill_id`.
- Keep the list sorted and deduplicated; remove `- None yet.` once real entries exist.

### Completion

- Summarize Skill capabilities and directory structure.
- Provide example prompts.
- Suggest optional next-step customizations.
- Output the `SKILL.md` path (i.e., `SKILL_ROOT/SKILL.md`) and `skill_id`.

## Slash Behavior Notes

Skill behavior in the `/` menu is controlled by frontmatter:

- Default: Manually invocable + auto-triggerable
- `user-invocable: false`: Not manually invocable but auto-triggerable
- `disable-model-invocation: true`: Manually invocable but not auto-triggerable
- Both set simultaneously: Both disabled

## Continuous Improvement

1. Validate the skill with real tasks
2. Record pain points and inefficient steps
3. Revise `SKILL.md` or resource directories
4. Validate again, forming a stable iteration