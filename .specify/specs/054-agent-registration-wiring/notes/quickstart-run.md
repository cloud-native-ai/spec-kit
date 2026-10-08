# Quickstart Run — 054 (executed 2026-10-08)

## Scenario 3 executable part — real outputs

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/ == .specify/skills/ (455 files)
ok    agents/ == .specify/agents/templates/ (2 files)
ok    scripts/ == .specify/scripts/ (107 files)
ok    shared/ == .specify/shared/ (46 files)
exit=0

$ grep -rn "<STR-001 verbatim> + SKILL retired phrases" <shipped surfaces>
STR-001 hits:
templates/commands/agents.md:0
skills/create-agent/SKILL.md:0
.qoder/commands/speckit.agents.md:0
.claude/commands/speckit.agents.md:0
.github/prompts/speckit.agents.prompt.md:0
.opencode/command/speckit.agents.md:0
SKILL phrase hits:
skills/create-agent/SKILL.md:0
.specify/skills/create-agent/SKILL.md:0

$ scripts/bash/run-tests.sh <five guard files>
============================== 35 passed in 0.17s ==============================
```

Teardown: none needed (all steps read-only).
