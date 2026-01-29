---
description: Create or update an Agent Skill in .github/skills/ with context-aware scaffolding.
---

> Note: `$ARGUMENTS` should contain the skill name and a brief description. e.g. "testing - A skill for running unit tests"

## Goal

Create a new Agent Skill directory structure or update an existing one, injecting relevant project context.

## Execution Steps

### 1. Input Parsing
- Extract `SKILL_NAME` and `DESCRIPTION` from `$ARGUMENTS`.
- If arguments are missing or unclear, ask the user to provide them.
- Standardize `SKILL_NAME`: lowercase, hyphens only (e.g., `web-testing`).

### 2. Context Gathering (Targeted Enrichment)
- Scan `.specify/memory/feature-index.md` for active or implemented features.
- If the skill relates to specific features (e.g., "testing" skill relates to functionality in recent specs), read those `spec.md` files to extract relevant guidelines or context (e.g., "Testing" section).
- Summarize this context as "Project Constraints & Guidelines".

### 3. Skill Scaffolding
Define path: `.github/skills/<SKILL_NAME>/`
Check if directory exists.

**Case A: New Skill (Directory missing)**
1. Create directory `.github/skills/<SKILL_NAME>/`.
2. Create `SKILL.md` with:
   - YAML Frontmatter:
     ```yaml
     ---
     name: <SKILL_NAME>
     description: <DESCRIPTION>
     ---
     ```
   - Body:
     ```markdown
     # Skill Instructions

     [Insert DESCRIPTION]

     ## Project Context
     [Insert summarized Project Constraints & Guidelines]

     ## Capabilities
     - [ ] Define step-by-step procedures here
     - [ ] Link to scripts or resources
     ```

**Case B: Existing Skill (Directory exists)**
1. Read existing `SKILL.md`.
2. Do NOT overwrite.
3. Append a new section at the end of the file:
   ```markdown
   
   ### Spec Context Updates [YYYY-MM-DD]
   
   **Context from recent features**:
   [Insert summarized Project Constraints & Guidelines]
   ```

### 4. Validation
- Output the location of the created/updated skill.
- Verify `SKILL.md` has correct YAML frontmatter.

## Report
Confirm creation/update of the skill and suggest next steps (e.g., "Add scripts to the skill directory").
