# Quickstart: Tier 2 Agent Support for Hermes-Agent and iFlow

**Spec**: [requirements.md](requirements.md) | **Plan**: [plan.md](plan.md)

## Scenario 1: Initialize a new project with Hermes-Agent

```bash
# Create a new project with Hermes-Agent as the AI tool
specify init my-project --ai hermes

# Verify the directory structure
ls -la my-project/.hermes/
# Expected: commands/ directory, skills symlink → .specify/skills/

ls my-project/.hermes/commands/
# Expected: speckit.requirements.md, speckit.plan.md, speckit.tasks.md, etc.

cat my-project/HERMES.md
# Expected: symlink content from .specify/instructions.md
```

## Scenario 2: Initialize a new project with iFlow

```bash
# Create a new project with iFlow as the AI tool
specify init my-project --ai iflow

# Verify the directory structure
ls -la my-project/.iflow/
# Expected: commands/ directory, skills symlink → .specify/skills/

ls my-project/.iflow/commands/
# Expected: speckit.requirements.md, speckit.plan.md, speckit.tasks.md, etc.

cat my-project/IFLOW.md
# Expected: symlink content from .specify/instructions.md
```

## Scenario 3: Add Hermes-Agent to an existing project

```bash
# Existing project already has Claude Code initialized
ls .claude/
# Already exists with commands, skills, etc.

# Add Hermes-Agent support
specify init . --ai hermes --here --force

# Verify both tools coexist
ls .claude/commands/   # Unchanged
ls .hermes/commands/   # Newly created
ls .specify/           # Core files preserved
```

## Scenario 4: Verify Tier 2 classification

```bash
# Check CLI help to see tier labels
specify init --help
# Expected output includes:
# --ai: AI assistant to use: claude, codex, qoder, copilot, opencode (Tier 1),
#        or qwen, hermes, iflow (Tier 2)

# After init, check the initialization summary output
specify init . --ai hermes --here --force
# Expected summary line: "Configured assistants: hermes (Tier 2)"
```

## Scenario 5: Multi-tool coexistence

```bash
# Initialize with three different tools sequentially
specify init . --ai claude --here --force
specify init . --ai hermes --here --force
specify init . --ai iflow --here --force

# Verify all three coexist
ls .claude/commands/ .hermes/commands/ .iflow/commands/
# All three directories have command templates

ls -la .claude/skills .hermes/skills .iflow/skills
# All three point to .specify/skills/

# Core files untouched
cat .specify/memory/constitution.md
# Constitution content preserved across all three init runs
```

## Validation Checklist

- [ ] `specify init . --ai hermes` succeeds without errors
- [ ] `specify init . --ai iflow` succeeds without errors
- [ ] `.hermes/commands/` contains expected command templates
- [ ] `.iflow/commands/` contains expected command templates
- [ ] `.hermes/skills` → `.specify/skills/` symlink works
- [ ] `.iflow/skills` → `.specify/skills/` symlink works
- [ ] `HERMES.md` exists (symlink to `.specify/instructions.md`)
- [ ] `IFLOW.md` exists (symlink to `.specify/instructions.md`)
- [ ] Tier 2 label shown in initialization summary
- [ ] Multi-tool init does not overwrite core `.specify/` files
- [ ] CLI `--help` lists hermes and iflow as Tier 2 options
