# Quickstart Run — 054 (executed 2026-10-08; re-run with verbatim commands 2026-10-08 after review F2)

## Scenario 3 executable part — verbatim commands and real outputs

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/ == .specify/skills/ (455 files)
ok    agents/ == .specify/agents/templates/ (2 files)
ok    scripts/ == .specify/scripts/ (107 files)
ok    shared/ == .specify/shared/ (46 files)
exit=0

$ grep -rc "Tool-specific directories are symlinks" templates/commands/agents.md skills/create-agent/SKILL.md .qoder/commands/speckit.agents.md .claude/commands/speckit.agents.md .github/prompts/speckit.agents.prompt.md .opencode/command/speckit.agents.md
templates/commands/agents.md:0
skills/create-agent/SKILL.md:0
.qoder/commands/speckit.agents.md:0
.claude/commands/speckit.agents.md:0
.github/prompts/speckit.agents.prompt.md:0
.opencode/command/speckit.agents.md:0
exit=1 (1 = zero total matches, expected)

$ grep -rc "Per-file symlinked into every officially supported tool" skills/create-agent/SKILL.md .specify/skills/create-agent/SKILL.md
skills/create-agent/SKILL.md:0
.specify/skills/create-agent/SKILL.md:0
exit=1 (1 = zero total matches, expected)

$ grep -rc "recreates a \*\*per-file\*\* symlink for each" skills/create-agent/SKILL.md .specify/skills/create-agent/SKILL.md
skills/create-agent/SKILL.md:0
.specify/skills/create-agent/SKILL.md:0
exit=1 (1 = zero total matches, expected)

$ scripts/bash/run-tests.sh tests/contract/test_render_trigger_cli.py tests/contract/test_teaching_surfaces.py tests/contract/test_seat_instantiation_flow.py tests/contract/test_agent_surface_docs.py tests/contract/test_agent_chain_guards.py
============================== 35 passed in 0.17s ==============================
```

Teardown: none needed (all steps read-only).
