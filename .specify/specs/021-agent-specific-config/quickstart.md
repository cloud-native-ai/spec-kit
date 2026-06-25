# Quickstart: Agent-Specific Configuration

**Spec**: [requirements.md](./requirements.md)  
**Date**: 2026-06-25

## What This Feature Does

After implementation, commands like `/speckit.agents` and skills like `browser-utils` automatically detect which AI agent is executing them and adapt their guidance accordingly. Claude Code gets Claude Code-specific tool recommendations; Copilot gets Copilot-specific patterns; unknown agents get generic guidance that still works.

## Scenario 1: Running `/speckit.agents` from Claude Code

**Before** (current behavior):
```
User runs /speckit.agents from Claude Code.
The command template provides generic guidance about agent creation.
It references tool patterns that may not match Claude Code's capabilities.
```

**After** (with agent-specific config):
```
User runs /speckit.agents from Claude Code.
Step 1: Template detects Claude Code as the executing agent.
Step 2: Loads Claude Code-specific guidance inline:
  - Use Agent tool for subagent delegation (not shell-based workarounds)
  - Prefer Edit tool for file modifications (not Write for small changes)
  - Use Bash tool with --timeout for long-running operations
Step 3: If execution hits an agent-specific obstacle, generates a feedback
  document at .specify/memory/feedback/agents-claude-code-2026-06-25T14-30-00.md
```

## Scenario 2: Running `browser-utils` Skill from Qoder

**Before**:
```
User runs browser-utils from Qoder.
SKILL.md references Claude Code's Bash tool and Read tool for screenshots.
Qoder doesn't have these tools — user must manually translate.
```

**After**:
```
User runs browser-utils from Qoder.
Step 1: SKILL.md detects Qoder as the executing agent.
Step 2: Loads ${SKILL_HOME}/references/qoder-guide.md:
  - Use direct shell commands instead of Bash tool
  - Screenshots saved to /tmp; open with system image viewer
  - No background task support — run Playwright synchronously
Step 3: No obstacles → no feedback document generated.
```

## Scenario 3: Running from an Unrecognized Agent

```
User runs /speckit.skills from an agent that Spec Kit doesn't recognize.
Step 1: Template cannot identify the agent from available signals.
Step 2: Falls back to generic guidance (existing behavior, unchanged).
Step 3: Optionally logs a note: "Agent not identified. Consider creating
  a reference document for your agent to enable tailored guidance."
No errors. No degraded functionality.
```

## Scenario 4: Feedback Loop with improve-skills

```
1. User runs browser-utils from Claude Code.
2. Claude Code hits an obstacle: WebFetch doesn't support file:// URLs.
3. Feedback document generated:
   .specify/memory/feedback/browser-utils-claude-code-2026-06-25T15-00-00.md
4. Later, user runs /speckit.improve-skills browser-utils.
5. improve-skills discovers the feedback document.
6. improve-skills analyzes the obstacle and suggests updating the Claude Code
   reference guide to add a workaround for file:// URLs.
```

## File Locations After Implementation

```
templates/commands/agents.md              # + Agent-Specific Configuration section (inline)
templates/commands/skills.md              # + Agent-Specific Configuration section (inline)
templates/commands/tools.md               # + Agent-Specific Configuration section (inline)

skills/browser-utils/SKILL.md             # + Agent-Specific Configuration section
skills/browser-utils/references/
  ├── claude-code-guide.md                # NEW
  └── copilot-guide.md                    # NEW

skills/create-agent/SKILL.md              # + Agent-Specific Configuration section
skills/create-agent/references/           # NEW directory
  ├── claude-code-guide.md                # NEW
  └── copilot-guide.md                    # NEW

skills/improve-agent/SKILL.md             # + Agent-Specific Configuration section
skills/improve-agent/references/          # NEW directory
  ├── claude-code-guide.md                # NEW
  └── copilot-guide.md                    # NEW

skills/improve-skills/SKILL.md            # + Agent-Specific Configuration section
skills/improve-skills/references/
  ├── claude-code-guide.md                # NEW
  └── copilot-guide.md                    # NEW

.specify/memory/feedback/                 # NEW directory (empty at launch)
  └── .gitkeep
```
