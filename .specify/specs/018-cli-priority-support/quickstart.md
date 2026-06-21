# Quickstart: CLI Priority AI Tool Support

**Spec**: [requirements.md](requirements.md) | **Plan**: [plan.md](plan.md)
**Created**: 2026-06-21

## Prerequisites

- Python 3.8+
- `specify-cli` installed (`uv tool install specify-cli` or `pipx install specify-cli`)
- At least one Tier 1 CLI tool installed (recommended: Claude Code, Codex CLI, or Qoder CLI)

## Scenario 1: Initialize a New Project with Codex CLI (P1 — MVP)

```bash
# Initialize with Codex CLI explicitly
specify init my-project --ai codex

# Verify .codex/ directory was created
ls -la my-project/.codex/commands/

# You should see 15 speckit.* command files:
# speckit.agents.md  speckit.analyze.md  speckit.checklist.md  ...
```

**Expected output**: `specify init` creates `.codex/commands/` with all Speckit command templates, plus the standard `.specify/` core directory. The result summary shows "Created: .codex/commands/" and a "CODEX_HOME" environment variable setup step.

## Scenario 2: Verify Tier Classification in Init Menu (P2)

```bash
# Run init without --ai to see interactive menu
specify init my-project

# The interactive menu should display tools in this order:
# → Claude Code        (Tier 1)
#   Codex CLI           (Tier 1)
#   Qoder CLI           (Tier 1)
#   GitHub Copilot      (Tier 1)
#   opencode            (Tier 1)
#   Qwen Code           (Tier 2)
```

**Expected behavior**: Tier 1 tools appear at the top of the selection menu. Qwen Code appears last with a "(Tier 2)" label.

## Scenario 3: Multi-Tool Coexistence (P2 — Tier System)

```bash
# Start with Claude Code
specify init my-project --ai claude
cd my-project

# Add Codex CLI support to the same project
specify init . --ai codex --force

# Add Qoder CLI support
specify init . --ai qoder --force

# Verify all three tool directories exist
ls -d .claude .codex .qoder

# Verify core .specify/ was not overwritten
cat .specify/memory/constitution.md | head -1
# Should still show the original constitution header
```

**Expected behavior**: Each tool gets its own configuration directory. The `.specify/` core content is preserved (reused, not overwritten). The init summary reports "Preserved: .specify/memory, .specify/templates, ..."

## Scenario 4: Deep Capability Adaptation — Command Template Variants (P3)

```bash
# Initialize with each Tier 1 tool and verify command template format

# Claude Code uses $ARGUMENTS
specify init project-claude --ai claude
head -5 project-claude/.claude/commands/speckit.requirements.md
# Should contain "$ARGUMENTS" as the argument placeholder

# Codex CLI uses $ARGUMENTS
specify init project-codex --ai codex
head -5 project-codex/.codex/commands/speckit.requirements.md
# Should contain "$ARGUMENTS" as the argument placeholder

# Qwen Code (Tier 2) uses {{args}}
specify init project-qwen --ai qwen
head -5 project-qwen/.qwen/commands/speckit.requirements.toml
# Should contain "{{args}}" as the argument placeholder
```

**Expected behavior**: Each tool's command templates use the tool's native argument format. The workflow semantics (command names, descriptions, execution flow) remain identical across all tools.

## Scenario 5: Capability Matrix Audit (P3)

```bash
# After initializing with multiple tools, run the support-surface audit
# (This is a programmatic check, not a user-facing CLI command)

python -c "
from specify_cli import audit_capability_matrix
from pathlib import Path
result = audit_capability_matrix(Path('my-project'))
for entry in result['entries']:
    status = '✅' if entry['status'] == 'pass' else '❌'
    print(f'{status} {entry[\"tool_key\"]:12} {entry[\"dimension\"]:20} {entry[\"status\"]}')
print(f'Tier 1 pass rate: {result[\"summary\"][\"tier1_pass_rate\"]}%')
"
```

**Expected output**: All Tier 1 tools pass all 6 dimensions. Tier 2 (Qwen Code) passes `initialization` and `command_templates` at minimum.

## Scenario 6: Constitution Amendment Verification (P2 — Governance)

```bash
# After implementation, verify the constitution includes Codex CLI and tier classification
grep -A 5 "Principle V" .specify/memory/constitution.md

# Should show:
# "Only support officially approved AI agents: Claude Code, Codex CLI,
#  GitHub Copilot, Qwen Code, opencode, and Qoder"
# And a tier classification sub-bullet
```

## Scenario 7: CLI Installation Verification in Init Summary (P3)

```bash
# Init with Codex CLI when it's not installed (for testing)
specify init test-project --ai codex --ignore-agent-tools

# The result summary should include:
# "Attention required: Codex CLI not detected. Install from: https://..."
# Plus the CODEX_HOME environment variable setup guidance
```

**Expected behavior**: Even when the CLI tool is not installed, project assets are created. The init summary prominently displays installation guidance.
