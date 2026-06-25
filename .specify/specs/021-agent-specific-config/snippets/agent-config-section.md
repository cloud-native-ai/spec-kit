# Canonical Agent-Specific Configuration Section

> This snippet defines the three-step structure added to each target file.
> For COMMANDS: Steps 1 and 3 are identical; Step 2 uses inline guidance.
> For SKILLS: Steps 1 and 3 are identical; Step 2 uses ${SKILL_HOME}/references/ pointer.

## Agent-Specific Configuration

### Step 1: Identify Executing Agent

Before executing the main workflow, identify which AI agent is running this command/skill. Use the following detection signals:

| Agent | Detection Signals |
|-------|-------------------|
| **Claude Code** | System prompt contains "Claude Code"; tools include `Agent`, `Edit`, `Bash`, `Read`; `.claude/` directory exists |
| **GitHub Copilot** | Running in VS Code Copilot Chat context; `.github/copilot-instructions.md` loaded; tools include `workspace edit`, `@terminal` |
| **Qoder CLI** | `.qoder/` directory exists; `QODER.md` instructions loaded |
| **opencode** | `.opencode/` directory exists |
| **Qwen Code** | `QWEN.md` instructions loaded; `.qwen/` directory exists |
| **Codex CLI** | `.codex/` directory exists |
| **Hermes Agent** | `.hermes/` directory exists |
| **iFlow** | `.iflow/` directory exists |

If you can confidently identify your agent from these signals, proceed to Step 2 with the identified agent slug. If you cannot identify your agent, skip Step 2 and proceed directly with the standard workflow.

### Step 2: Load Agent-Specific Guidance

[FOR COMMANDS — inline subsections per agent here]
[FOR SKILLS — read ${SKILL_HOME}/references/<agent-slug>-guide.md if it exists]

### Step 3: Capture Execution Feedback

If you encounter an agent-specific obstacle during execution (e.g., a tool call is unavailable, output format doesn't match expectations, a workaround was needed for an agent limitation), generate a feedback document at:

```
.specify/memory/feedback/<command-or-skill-name>-<agent-slug>-<YYYY-MM-DDTHH-MM-SS>.md
```

The feedback document MUST contain:

```markdown
# Agent Execution Feedback

**Source**: <command-or-skill-name>
**Agent**: <agent-slug>
**Timestamp**: <ISO-8601>
**Outcome**: <success-with-workaround | partial-failure | full-failure>

## Obstacle
[Description of the agent-specific issue encountered]

## Workaround Applied
[What was done to work around the issue, if anything]

## Suggested Improvement
[Specific change to the command/skill template or reference document that would prevent this issue]
```

Only generate feedback when a genuine agent-specific obstacle was encountered — do not generate feedback for issues unrelated to agent differences.
