Use Agent Skills in VS Code
Agent Skills are folders of instructions, scripts, and resources that GitHub Copilot can load when relevant to perform specialized tasks. Agent Skills is an open standard that works across multiple AI agents, including GitHub Copilot in VS Code, GitHub Copilot CLI, and GitHub Copilot coding agent.

Unlike custom instructions that primarily define coding guidelines, skills enable specialized capabilities and workflows that can include scripts, examples, and other resources. Skills you create are portable and work across any skills-compatible agent.

Key benefits of Agent Skills:

Specialize Copilot: Tailor capabilities for domain-specific tasks without repeating context
Reduce repetition: Create once, use automatically across all conversations
Compose capabilities: Combine multiple skills to build complex workflows
Efficient loading: Only relevant content loads into context when needed
Note
Agent Skills support in VS Code is currently in preview. Enable the 
chat.useAgentSkills

 setting to use Agent Skills.
Agent Skills vs custom instructions
While both Agent Skills and custom instructions help customize Copilot's behavior, they serve different purposes:

Expand table
Feature	Agent Skills	Custom Instructions
Purpose	Teach specialized capabilities and workflows	Define coding standards and guidelines
Portability	Works across VS Code, Copilot CLI, and Copilot coding agent	VS Code and GitHub.com only
Content	Instructions, scripts, examples, and resources	Instructions only
Scope	Task-specific, loaded on-demand	Always applied (or via glob patterns)
Standard	Open standard (agentskills.io)	VS Code-specific
Use Agent Skills when you want to:

Create reusable capabilities that work across different AI tools
Include scripts, examples, or other resources alongside instructions
Share capabilities with the wider AI community
Define specialized workflows like testing, debugging, or deployment processes
Use custom instructions when you want to:

Define project-specific coding standards
Set language or framework conventions
Specify code review or commit message guidelines
Apply rules based on file types using glob patterns
Create a skill
Skills are stored in directories with a SKILL.md file that defines the skill's behavior. VS Code supports two types of skills:

Project skills, stored in your repository: .github/skills/ (recommended) or .claude/skills/ (legacy, for backward compatibility)
Personal skills, stored in your user profile: ~/.copilot/skills/ (recommended) or ~/.claude/skills/ (legacy, for backward compatibility)
To create a skill:

Create a .github/skills directory in your workspace.

Create a subdirectory for your skill. Each skill should have its own directory (for example, .github/skills/webapp-testing).

Create a SKILL.md file in the skill directory with the following structure:

Markdown

---
name: skill-name
description: Description of what the skill does and when to use it
---

# Skill Instructions

Your detailed instructions, guidelines, and examples go here...
Optionally, add scripts, examples, or other resources to your skill's directory.

For example, a skill for testing web applications might include:

SKILL.md - Instructions for running tests
test-template.js - A template test file
examples/ - Example test scenarios
SKILL.md file format
The SKILL.md file is a Markdown file with YAML frontmatter that defines the skill's metadata and behavior.

Header (required)
The header is formatted as YAML frontmatter with the following fields:

Expand table
Field	Required	Description
name	Yes	A unique identifier for the skill. Must be lowercase, using hyphens for spaces (for example, webapp-testing). Maximum 64 characters.
description	Yes	A description of what the skill does and when to use it. Be specific about both capabilities and use cases to help Copilot decide when to load the skill. Maximum 1024 characters.
Body
The skill body contains the instructions, guidelines, and examples that Copilot should follow when using this skill. Write clear, specific instructions that describe:

What the skill helps accomplish
When to use the skill
Step-by-step procedures to follow
Examples of the expected input and output
References to any included scripts or resources
You can reference files within the skill directory using relative paths. For example, to reference a script in your skill directory, use [test script](./test-template.js).

Example skills
The following examples demonstrate different types of skills you can create.

Example: Web application testing skill
Example: GitHub Actions debugging skill
How Copilot uses skills
Skills use progressive disclosure to efficiently load content only when needed. This three-level loading system ensures you can install many skills without consuming context:

Level 1: Skill discovery

Copilot always knows which skills are available by reading their name and description from the YAML frontmatter. This metadata is lightweight and helps Copilot decide which skills are relevant to your request.

Level 2: Instructions loading

When your request matches a skill's description, Copilot loads the SKILL.md file body into its context. Only then do the detailed instructions become available.

Level 3: Resource access

Copilot can access additional files in the skill directory (scripts, examples, documentation) only as needed. These resources don't load until Copilot references them, keeping your context efficient.

This architecture means skills are automatically activated based on your prompt—you don't need to manually select them. You can install many skills, and Copilot will load only what's relevant for each task.

Use shared skills
You can use skills created by others to enhance Copilot's capabilities. The github/awesome-copilot repository contains a growing community collection of skills, custom agents, instructions, and prompts. The anthropics/skills repository contains additional reference skills.

To use a shared skill:

Browse the available skills in the repository
Copy the skill directory to your .github/skills/ folder
Review and customize the SKILL.md file for your needs
Optionally, modify or add resources as needed
Tip
Always review shared skills before using them to ensure they meet your requirements and security standards. VS Code's terminal tool provides controls for script execution, including auto-approve options with configurable allow-lists and tight controls over which code runs. Learn more about security considerations for auto-approval features.

Agent Skills standard
Agent Skills is an open standard that enables portability across different AI agents. Skills you create in VS Code work with multiple agents, including:

GitHub Copilot in VS Code: Available in chat and agent mode
GitHub Copilot CLI: Accessible when working in the terminal
GitHub Copilot coding agent: Used during automated coding tasks
Learn more about the Agent Skills standard at agentskills.io.


How to create custom Skills
How to create custom Skills
Updated over a week ago
Skills are available for users on Pro, Max, Team, and Enterprise plans. This feature requires code execution to be enabled. Skills are also available in beta for Claude Code users and for all API users using the code execution tool.

Custom Skills let you enhance Claude with specialized knowledge and workflows specific to your organization or personal work style. This article explains how to create, structure, and test your own Skills.

 

Skills can be as simple as a few lines of instructions or as complex as multi-file packages with executable code. The best Skills:

Solve a specific, repeatable task

Have clear instructions that Claude can follow

Include examples when helpful

Define when they should be used

Are focused on one workflow rather than trying to do everything

 

Creating a Skill.md File
Every Skill consists of a directory containing at minimum a Skill.md file, which is the core of the Skill. This file must start with a YAML frontmatter to hold name and description fields, which are required metadata. It can also contain additional metadata, instructions for Claude or reference files, executable scripts, or tools.

 

Required metadata fields
name: A human-friendly name for your Skill (64 characters maximum)

Example: Brand Guidelines

description: A clear description of what the Skill does and when to use it.

This is critical—Claude uses this to determine when to invoke your Skill (200 characters maximum).

Example: Apply Acme Corp brand guidelines to presentations and documents, including official colors, fonts, and logo usage.

 

Optional Metadata Fields
dependencies: Software packages required by your Skill.

Example: python>=3.8, pandas>=1.5.0

The metadata in the Skill.md file serves as the first level of a progressive disclosure system, providing just enough information for Claude to know when the Skill should be used without having to load all of the content.

 

Markdown Body
The Markdown body is the second level of detail after the metadata, so Claude will access this if needed after reading the metadata. Depending on your task, Claude can access the Skill.md file and use the Skill.

 

Example Skill.md
Brand Guidelines Skill

## Metadata
name: Brand Guidelines
description: Apply Acme Corp brand guidelines to all presentations and documents

## Overview
This Skill provides Acme Corp's official brand guidelines for creating consistent, professional materials. When creating presentations, documents, or marketing materials, apply these standards to ensure all outputs match Acme's visual identity. Claude should reference these guidelines whenever creating external-facing materials or documents that represent Acme Corp.

## Brand Colors

Our official brand colors are:
- Primary: #FF6B35 (Coral)
- Secondary: #004E89 (Navy Blue)
- Accent: #F7B801 (Gold)
- Neutral: #2E2E2E (Charcoal)

## Typography

Headers: Montserrat Bold
Body text: Open Sans Regular
Size guidelines:
- H1: 32pt
- H2: 24pt
- Body: 11pt

## Logo Usage

Always use the full-color logo on light backgrounds. Use the white logo on dark backgrounds. Maintain minimum spacing of 0.5 inches around the logo.

## When to Apply

Apply these guidelines whenever creating:
- PowerPoint presentations
- Word documents for external sharing
- Marketing materials
- Reports for clients

## Resources

See the resources folder for logo files and font downloads.
 

Adding Resources
If you have too much information to add to a single Skill.md file (e.g., sections that only apply to specific scenarios), you can add more content by adding files within your Skill directory. For example, add a REFERENCE.md file containing supplemental and reference information to your Skill directory. Referencing it in Skill.md will help Claude decide if it needs to access that resource when executing the Skill.

 

Adding Scripts
For more advanced Skills, attach executable code files to Skill.md, allowing Claude to run code. For example, our document skills use the following programming languages and packages:

Python (pandas, numpy, matplotlib)

JavaScript/Node.js

Packages to help with file editing

visualization tools

Note: Claude and Claude Code can install packages from standard repositories (Python PyPI, JavaScript npm) when loading Skills. It’s not possible to install additional packages at runtime with API Skills—all dependencies must be pre-installed in the container.

 

Packaging Your Skill
Once your Skill folder is complete:

Ensure the folder name matches your Skill's name.

Create a ZIP file of the folder.

The ZIP should contain the Skill folder as its root (not a subfolder).

Correct structure:

my-Skill.zip

  └── my-Skill/

      ├── Skill.md

      └── resources/

 

Incorrect structure:

my-Skill.zip

  └── (files directly in ZIP root)

 

Testing Your Skill
Before Uploading
1. Review your Skill.md for clarity

2. Check that the description accurately reflects when Claude should use the Skill

3. Verify all referenced files exist in the correct locations

4. Test with example prompts to ensure Claude invokes it appropriately

 

After Uploading to Claude
1. Enable the Skill in Settings > Capabilities.

2. Try several different prompts that should trigger it

3. Review Claude's thinking to confirm it's loading the Skill

4. Iterate on the description if Claude isn't using it when expected

 

Note for Team and Enterprise plans: To make a skill available to all users in your organization, see Provisioning and managing Skills for your organization.

 

Best Practices
Keep it focused: Create separate Skills for different workflows. Multiple focused Skills compose better than one large Skill.

 

Write clear descriptions: Claude uses descriptions to decide when to invoke your Skill. Be specific about when it applies.

 

Start simple: Begin with basic instructions in Markdown before adding complex scripts. You can always expand on the Skill later.

 

Use examples: Include example inputs and outputs in your Skill.md file to help Claude understand what success looks like.

 

Test incrementally: Test after each significant change rather than building a complex Skill all at once.

 

Skills can build on each other: While Skills can't explicitly reference other Skills, Claude can use multiple Skills together automatically. This composability is one of the most powerful parts of the Skills feature.

 

Review the open Agent Skills specification: Follow the guidelines at agentskills.io, so skills you create can work across platforms that adopt the standard.

 

For a more in-depth guide to skill creation, refer to Skill authoring best practices in our Claude Docs.

 

Security Considerations
Exercise caution when adding scripts to your Skill.md file.

Don't hardcode sensitive information (API keys, passwords).

Review any Skills you download before enabling them.

Use appropriate MCP connections for external service access.