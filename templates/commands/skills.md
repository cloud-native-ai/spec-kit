---
description: Create Agent Skills
handoffs:
  - label: Update Instructions
    agent: speckit.instructions
    prompt: Update project instructions so the new skill is discoverable.
    send: true
scripts:
  sh: scripts/bash/create-new-skill.sh --json $ARGUMENTS
---

> Note
>
> - Argument Format: `<name> - <description>` (e.g., `testing - Unit testing utils`)
> - Or use flags: `--name <name> --description <desc>`

## User Input

```text
$ARGUMENTS
```

## Outline

Goal: Interactively guide the user to create a high-quality SpecKit Skill, ensuring all necessary components are properly structured and documented.

Primary workflow:
1. Extract reusable workflow from the current conversation
2. Clarify only when the workflow is still unclear
3. Iterate draft → review weak points → refine until finalized

## Specification

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── tools/            - Availiable tools
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields that AI Agent reads to determine when the skill gets used, thus it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded AFTER the skill triggers (if at all).

#### Bundled Resources (optional)

##### Tools (`tools/`)

Project specific tools documentation can be found in `tools/`, created by `refresh-tools.sh`.
- [MCP Tools](tools/mcp.md)
- [System Tools](tools/system.md)
- [Shell Tools](tools/shell.md)
- [Project Scripts](tools/project.md)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by AI Agent for patching or environment-specific adjustments

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform AI Agent's process and thinking.

- **When to include**: For documentation that AI Agent should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when AI Agent determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output AI Agent produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables AI Agent to use files without loading them into context

### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain the information needed for an AI agent to do the job at hand. It should not contain auxilary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc. Creating additional documentation files just adds clutter and confusion.

### Design Principles

#### Set Appropriate Degrees of Freedom

Match the level of specificity to the job/task's fragility and variability:

- High freedom (text-based instructions): Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.
- Medium freedom (pseudocode or scripts with parameters): Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.
- Low freedom (specific scripts, few parameters): Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of AI Agent as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

#### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by AI Agent (Unlimited because scripts can be executed without reading into context window)

#### Progressive Disclosure Patterns

Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat. Split content into separate files when approaching this limit. When splitting out content into other files, it is very important to reference them from SKILL.md and describe clearly when to read them, to ensure the reader of the skill knows they exist and when to use them.

**Key principle:** When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details (patterns, examples, configuration) into separate reference files.

**Pattern 1: High-level guide with references**

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

AI Agent loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.

**Pattern 2: Domain-specific organization**

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When a user asks about sales metrics, AI Agent only reads sales.md.

Similarly, for skills supporting multiple frameworks or variants, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When the user chooses AWS, AI Agent only reads aws.md.

**Pattern 3: Conditional details**

Show basic content, link to advanced content:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

AI Agent reads REDLINING.md or OOXML.md only when the user needs those features.

**Important guidelines:**

- **Avoid deeply nested references** - Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md.
- **Structure longer reference files** - For files longer than 100 lines, include a table of contents at the top so AI Agent can see the full scope when previewing.

### Skill Planning & Strategy (Official Workflow Aligned)

#### Step A: Extract from Conversation First

Before asking new questions, review the current conversation history and extract a reusable workflow whenever possible.

Extract at minimum:

- The step-by-step process being followed
- Decision points and branching logic
- Quality criteria or completion checks

If a clear workflow can be extracted, use it as the default draft baseline and only ask follow-up questions for missing or high-risk gaps.

#### Step B: Clarify if Needed

If no clear workflow emerges from conversation context, ask focused clarification questions to establish a minimal working workflow:

- What outcome should this skill produce?
- Is this workspace-scoped or personal?
- Should this be a quick checklist or a full multi-step workflow?

Use one question at a time and prefer recommended defaults.

#### Step C: Iterate

Iterative loop:

1. Draft the skill and save it
2. Identify the most ambiguous/weak parts and ask targeted follow-ups
3. Refine and repeat until stable
4. Finalize by summarizing outputs, example prompts, and suggested related customizations

#### Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

#### Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

#### Editing Best Practices (SKILL.md)

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of AI Agent to use. Include information that would be beneficial and non-obvious to AI Agent. Consider what procedural knowledge, domain-specific details, or reusable assets would help another AI Agent instance execute these tasks more effectively.

**Learn Proven Design Patterns**

Consult these helpful guides based on your skill's needs:

- **Multi-step processes**: See references/workflows.md for sequential workflows and conditional logic
- **Specific output formats or quality standards**: See references/output-patterns.md for template and example patterns

These files contain established best practices for effective skill design.

**Frontmatter**

Write the YAML frontmatter with `name` and `description`:

- `name`: The skill name
- `description`: This is the primary triggering mechanism for your skill, and helps AI Agent understand when to use the skill.
  - Include both what the Skill does and specific triggers/contexts for when to use it.
  - Include all "when to use" information here - Not in the body. The body is only loaded after triggering, so "When to Use This Skill" sections in the body are not helpful to AI Agent.
  - Example description for a `docx` skill: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when AI Agent needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"

Do not include any other fields in YAML frontmatter.

**Body**

Write instructions for using the skill and its bundled resources.

## Execution Steps

1.  **Initialize or Refresh**:
    - Execute `{SCRIPT}` to create basic structure.
    - Parse JSON output.
    - **Case 1: Refresh Only** (Input was empty or invalid format):
        - Output includes `"status": "refreshed"`.
        - Action: Display the message from `{SCRIPT}` output.
        - **STOP**. (Do not proceed to step 2).
    - **Case 2: Created Skill**:
        - Output includes `"SKILL_DIR"`.
        - Parse `SKILL_DIR`, `SKILL_NAME`, `SKILL_DESCRIPTION`.
        - Confirm success: "Created skill backbone at `SKILL_DIR`."

2.  **Extract from Conversation (Default Path)**:
    - Review current conversation history first.
    - Extract and draft:
      - Reusable step-by-step process
      - Decision points and branching logic
      - Quality criteria / completion checks
    - If extraction is strong enough, proceed directly to draft without broad discovery questions.

3.  **Clarify if Needed (Fallback Path)**:
    - Trigger this only when extraction is weak, ambiguous, or missing key decisions.
    - **Constraint**: Ask **EXACTLY ONE** question at a time. Wait for user response before proceeding.
    - Preferred clarifications:
      - Outcome: "What concrete result should this skill produce?"
      - Scope: "Workspace-scoped or personal?"
      - Format: "Quick checklist or full multi-step workflow?"
    - Then refine trigger description and constraints as needed:
      - Trigger intent/keywords/scenarios (for frontmatter `description`)
      - Critical rules/constraints (compliance/prohibitions/specific libraries)

4.  **Iterative Drafting & Refinement**:
    - Draft/update `SKILL.md` and save.
    - Identify the most ambiguous or weak parts.
    - Ask targeted follow-up questions only for those weak parts.
    - Repeat until the skill is coherent and actionable.

5.  **Tailored Implementation**:
    - **Update SKILL.md Details**:
      - Replace `{{DESCRIPTION}}` in frontmatter with finalized trigger description.
      - Fill `## Overview` with finalized outcome.
      - Fill `## Workflow / Instructions` with extracted/refined process.
      - If constraints exist, append a `## Constraints` section or integrate into workflow.
      - *Note*: If `## Applicable Scenarios` (or the legacy `## 适用场景`) section exists in the template, verify if it adds value beyond the Frontmatter. If not, remove it to reduce context.
    - **Scaffold Resources**:
      - Detect and confirm resource strategy, then create placeholders in `scripts/`, `references/`, or `assets/` with context-aware comments.
      - Detection hints:
        - Logic/Automation/API calls -> **Scripts**
        - Documentation/Schema/Policy -> **References**
        - Templates/Boilerplate -> **Assets**
        - System Commands -> **Tools**
    - **Update Links**:
      - Update the `## Available Tools & Resources` section in `SKILL.md` to link to the newly created scaffold files (e.g., add `- [Rotate Script](scripts/rotate_pdf.py)` under `### Scripts`).
    - **Import Files**:
      - Ask: "Do you have existing files to import for these resources?"
      - If yes, guide user to copy them to the valid paths.

6.  **Completion**:
    - Summarize what the skill produces and the structure created.
    - Suggest example prompts to try the skill.
    - Propose related customizations to create next.
    - Output the link to `SKILL.md`.

## Continuous Improvement

After using the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again
