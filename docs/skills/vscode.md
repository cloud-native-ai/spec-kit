# Using Agent Skills in VS Code Copilot

Agent Skills are collections of instructions, scripts, and resources that GitHub Copilot can load when relevant to perform specialized tasks. Agent Skills is an open standard applicable to multiple AI agents, including GitHub Copilot in VS Code, GitHub Copilot CLI, and GitHub Copilot coding agents.

Unlike Custom Instructions, which primarily define coding guidelines, Skills enable specialized capabilities and workflows that include scripts, examples, and other resources. The Skills you create are portable and work across any Skills-compatible agent.

## Core Advantages

*   **Copilot Specialization**: Tailor capabilities for domain-specific tasks without repeating context.
*   **Reduce Repetition**: Create once and automatically use across all conversations.
*   **Capability Composition**: Combine multiple Skills to build complex workflows.
*   **Efficient Loading**: Only relevant content is loaded into context when needed.

> **Note**: Agent Skills support in VS Code is currently in preview. You may need to enable the `chat.useAgentSkills` setting to use them.

## Agent Skills vs. Custom Instructions

Both can customize Copilot's behavior, but serve different purposes:

| Feature | Agent Skills | Custom Instructions |
| :--- | :--- | :--- |
| **Purpose** | Teach specialized capabilities and workflows | Define coding standards and guidelines |
| **Portability** | Universal across VS Code, Copilot CLI, Copilot Agent | VS Code and GitHub.com only |
| **Content** | Instructions, scripts, examples, and resources | Instructions only |
| **Scope** | Task-specific, loaded on demand | Always applied (or via glob patterns) |
| **Standard** | Open standard (agentskills.io) | VS Code-specific |

**Usage Comparison:**

*   **Agent Skills**: Create reusable capabilities (e.g., testing, deployment workflows) with supporting scripts or examples.
*   **Custom Instructions**: Define project-specific code style, framework conventions, or commit message formats.

## Creating Skills

Skills are stored in directories with a `SKILL.md` file.

### Storage Locations

*   **Project-Level Skills** (Recommended): The primary copy is stored in the workspace's `.specify/skills/` directory.
*   **GitHub-Compatible Entry Point**: `.github/skills/` serves only as a compatibility entry point mapped to the primary copy and does not host primary content.
*   **User-Level Skills** (Recommended): Stored in the `~/.copilot/skills/` directory of the user profile.

### Directory Structure

Each Skill should have its own subdirectory. For example, to create a Skill called `webapp-testing`:

1.  Create directory `.specify/skills/webapp-testing/`
2.  Create the `SKILL.md` file within it.
3.  (Optional) Add scripts, templates, or example files.

Example structure:
```text
.specify/skills/webapp-testing/
├── SKILL.md           # Defines Skill behavior and metadata
├── test-template.js   # Template file
└── examples/          # Example scenarios
```

### SKILL.md File Format

`SKILL.md` is a Markdown file with YAML frontmatter.

**Frontmatter**

```yaml
---
name: skill-name
description: Description of what the Skill does and when to use it
---
```

*   `name` (Required): Unique identifier, lowercase, using hyphens (e.g., `webapp-testing`).
*   `description` (Required): Describes the Skill's functionality and usage scenarios. Copilot uses this description to decide when to load the Skill.

**Body**

Contains detailed instructions, guidelines, and examples for Copilot to follow when using the Skill.

```markdown
# Skill Instructions

Write detailed instructions here...

You can reference files within the directory, e.g.: [Test Script](./test-template.js).
```

## How Copilot Uses Skills

Skills use a Progressive Disclosure mechanism, loading content only when needed:

1.  **Skill Discovery**: Copilot reads the names and descriptions of all available Skills.
2.  **Instruction Loading**: When a user request matches a Skill description, Copilot loads the body of `SKILL.md`.
3.  **Resource Access**: Copilot reads supporting files (scripts, examples) only when it needs to reference them.

## Best Practices

*   **Stay Focused**: Create separate Skills for different workflows rather than one massive all-in-one Skill.
*   **Clear Descriptions**: Descriptions are critical for Copilot to determine when to invoke a Skill.
*   **Use Examples**: Include input/output examples in `SKILL.md`.
*   **Security**: Exercise caution when adding scripts and avoid hardcoding sensitive information.

---
For more information, refer to the Agent Skills open standard: [agentskills.io](https://agentskills.io).
