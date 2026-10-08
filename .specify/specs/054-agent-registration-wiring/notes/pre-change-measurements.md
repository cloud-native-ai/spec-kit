# Pre-Change Measurements — 054-agent-registration-wiring

Frozen 2026-10-08 at tasks generation (never-cache: re-capture at /speckit.implement start if the tree has advanced).

## Test baseline (name-level)

- Command: `scripts/bash/run-tests.sh tests/contract/ --names-out .specify/specs/054-agent-registration-wiring/baseline-failed.txt`
- Real output (verbatim tail): `49 failed, 2574 passed, 2 skipped in 58.52s` + `# failed-name list written: ... (49 entries)`
- baseline-failed.txt: 49 entries; first three: `test_agent_skill_enablement.py::…[qa-engineer]`, `[requirements-analyst]`, `[test-engineer]`
- Regression criterion: zero NEW failures — `comm -13 baseline current` empty. The 49 are pre-existing reds (agent-skill-enablement, neutrality-budget, no-nested-skills classes), not caused by this feature.

## STR-001 retired literal (grep, source + tool copies)

- Command: `grep -rn "Tool-specific directories are symlinks" templates/commands/agents.md skills/create-agent/SKILL.md .qoder/commands/speckit.agents.md`
- Real hits (2026-10-08): `templates/commands/agents.md:25` and `.qoder/commands/speckit.agents.md:19` (both carry the sentence verbatim); zero hits in skills/create-agent/SKILL.md — the SKILL carries a DIFFERENT retired wording (two distinct literal classes; the C-7 guard pins both).

## SKILL.md retired phrases (verbatim, sed)

- Command: `sed -n '122p;127p' skills/create-agent/SKILL.md`
- :122 table row: `| **persistent** | … | Per-file symlinked into every officially supported tool's agent config directory on initialization (FR-010/012) |`
- :127 paragraph head: `On initialization the CLI (re)creates a **per-file** symlink for each *.agent.md* under .specify/agents/{templates,instances}/ inside every officially supported tool's agent config dir — e.g. .qoder/agents/<slug>.agent.md → ../../.specify/agents/templates/<slug>.agent.md …`

## Mirror baseline

- Command: `python3 scripts/python/sync-mirrors.py --check`
- Real output (exit 0): `OK: all per-tool command copies match the source templates.` + `ok templates/ (22) / skills/ (455) / agents/ (2) / scripts/ (107) / shared/ (46)`
- Criterion: no NEW drift on the pairs this spec touches.

## Neutral-layer state

- Command: `ls .specify/agents/instances/`
- Real output: empty (no instances) — the gap this feature closes. `.specify/agents/templates/` holds the 2 shipped Meta agents; `.qoder/agents/` holds their 2 rendered copies.
