---
description: Generate or update project instructions and compatibility symlinks, ensuring a consistent AI context across tools.
handoffs:
  - label: Scan Skills
    agent: speckit.skills
    prompt: Scan project for available tools and skills to populate the instructions.
scripts:
  sh: scripts/bash/generate-copilot.sh
---

> Note: `$ARGUMENTS` 为**可选补充输入**。当本次调用未提供任何 `$ARGUMENTS` 时，仍须按下文流程基于现有仓库分析生成或更新 `.ai/instructions.md`。

## User Input

```text
$ARGUMENTS
```

You **MUST** analyze the content of `$ARGUMENTS` to determine if it contains specific project details, overriding preferences, or partial updates.

## Outline

1. **Setup**: Run `{SCRIPT}` to ensure the basic directory structure, `.copilotignore`, and template `.ai/instructions.md` exist.
   - This script handles the "heavy lifting" of creating directories, ignoring files, and establishing symlinks for various AI tools (`.clinerules`, `.github`, `.lingma`, etc.).
   - It will only create a template `.ai/instructions.md` if one does not exist.

2. **Analyze Project Context**:
   - Read `README.md` to understand the project's purpose and existing features.
   - Inspect configuration files (`pyproject.toml`, `package.json`, `pom.xml`, `Makefile`, etc.) to determine the tech stack.
   - Check `memory/constitution.md` (if exists) to identify any mandated project rules.
   - Check `memory/feature-index.md` (if exists) for feature status reference.

3. **Update Instructions Content**:
   - Read the content of `.ai/instructions.md` (whether newly created or existing).
   - **Fill Placeholders**: Replace any bracketed placeholders (e.g., `[Brief summary...]`, `[Detected tech stack...]`) with concrete details derived from your analysis.
   - **Update Documentation Map**: Ensure the table correctly points to existing documentation files in the repository.
   - **Preserve Sections**: Do NOT remove or overwrite the `## Tools` and `## Skills` sections or their placeholder comments (`<!-- TOOLS_PLACEHOLDER -->`, `<!-- SKILLS_PLACEHOLDER -->`). These are reserved for the `skills` command.
   - **Incorporate User Input**: If `$ARGUMENTS` provided specific instructions or context, integrate them into the file.

4. **Validation**:
   - Ensure the file is well-formatted Markdown.
   - Verify that the resulting instructions clearly describe the project to a fresh AI instance.

5. **Report**:
   - Report the full path of the instructions file (`.ai/instructions.md`).
   - Confirm that symlinks for Copilot, Cline, Lingma, Trae, and Qoder have been established.
   - **Next Step**: Recommend running `/speckit.skills` to automatically populate the Tools and Skills sections.
