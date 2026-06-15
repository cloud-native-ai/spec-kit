# Quickstart: Agent Framework Refactor

**Spec**: 014-agent-framework-refactor | **Date**: 2026-06-15

## Prerequisites

- Spec Kit CLI installed (`specify` available in PATH)
- A Git repository initialized
- At least one AI tool configured (Claude Code, Copilot, Qoder, Qwen, or opencode)

## Scenario 1: Initialize a Project with Bundled Agents

```bash
# Create a new project with Claude Code
specify init --here

# Verify agents were installed
ls -la .specify/agents/
# Expected: bundled .agent.md files + references/ directory

# Verify symlink was created
ls -la .github/agents
# Expected: symlink → ../../.specify/agents

# Verify agent is accessible through symlink
cat .github/agents/code-reviewer.agent.md
# Expected: same content as .specify/agents/code-reviewer.agent.md
```

**Pass criteria**: `.specify/agents/` contains bundled agents, `.github/agents` is a symlink pointing to `.specify/agents/`.

## Scenario 2: Create a New Agent via `/speckit.agents`

```
# In an AI tool session, run:
/speckit.agents Create a code review agent for Python files

# Verify the agent was created at the canonical location
ls .specify/agents/code-reviewer.agent.md

# Verify workspace files were created (first-time only)
ls .specify/agents/AGENTS.md .specify/agents/MEMORY.md .specify/agents/SOUL.md .specify/agents/USER.md

# Verify the agent is visible through tool-specific symlink
ls .github/agents/code-reviewer.agent.md
# Should resolve through the directory symlink
```

**Pass criteria**: Agent file exists in `.specify/agents/`, workspace files were scaffolded, agent is discoverable via `.github/agents/` symlink.

## Scenario 3: Shared References

```
# Create two agents that share reference material

/speckit.agents Create a code reviewer agent that uses coding standards
# Creates: .specify/agents/code-reviewer.agent.md
# Creates: .specify/agents/references/coding-standards.md

/speckit.agents Create a security auditor agent that also uses coding standards
# Creates: .specify/agents/security-auditor.agent.md
# References existing: .specify/agents/references/coding-standards.md (no duplicate)

# Verify single copy of shared reference
find .specify/agents/references -name "coding-standards.md" | wc -l
# Expected: 1
```

**Pass criteria**: Both agents reference the same file in `references/`; no duplicate copies.

## Scenario 4: Re-init Preserves User Agents

```bash
# Create a custom agent first
# (via /speckit.agents in an AI tool session)

# Re-run init
specify init --here

# Verify user agent was NOT overwritten
cat .specify/agents/my-custom-agent.agent.md
# Expected: user's original content preserved

# Verify bundled agents were merged
ls .specify/agents/
# Expected: both user agents and bundled agents present
```

**Pass criteria**: User-created agents survive `specify init`; bundled agents are added alongside.

## Scenario 5: Migration from Existing Regular Directory

```bash
# Simulate: project has a regular .github/agents/ directory (not a symlink)
mkdir -p .github/agents
echo "old agent" > .github/agents/legacy-agent.agent.md

# Run init
specify init --here

# Verify migration happened
cat .specify/agents/legacy-agent.agent.md
# Expected: contains "old agent" (migrated from .github/agents/)

# Verify .github/agents is now a symlink
ls -la .github/agents
# Expected: symlink → ../../.specify/agents
```

**Pass criteria**: Existing content migrated to `.specify/agents/`, regular directory replaced with symlink.

## Scenario 6: Multiple Tools Configured

```bash
# Init with Claude Code
specify init --here

# Verify all tool-specific symlinks point to the same canonical directory
readlink .github/agents    # → ../../.specify/agents
readlink .qoder/agents     # → ../../.specify/agents  (if qoder configured)
readlink .qwen/agents      # → ../../.specify/agents  (if qwen configured)

# All resolve to the same canonical directory
```

**Pass criteria**: Multiple tool directories all symlink to `.specify/agents/`.

## Validation Checklist

- [ ] `specify init` copies bundled agents to `.specify/agents/`
- [ ] `specify init` creates directory-level symlinks for the configured tool
- [ ] `/speckit.agents` writes to `.specify/agents/`, not tool-specific directories
- [ ] `/speckit.agents` creates workspace files (AGENTS.md, MEMORY.md, SOUL.md, USER.md) on first run
- [ ] References are shared in `.specify/agents/references/`
- [ ] Existing user agents survive `specify init`
- [ ] Regular directories at symlink targets are migrated before replacement
- [ ] Agents are discoverable through tool-specific symlinks
