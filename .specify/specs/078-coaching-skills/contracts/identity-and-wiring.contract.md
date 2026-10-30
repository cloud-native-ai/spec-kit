# Contract: Identity and Wiring

**Scope**: the rename `think-skills` → `coaching-skills` across its eight identity coordinates, the closed wiring surface, the derived faces that are regenerated rather than edited, the upgrade path, the frozen test updates, and the history boundary.

**Literal authority**: `coaching-skills` (STR-001), `think-skills` (STR-002), `skill:coaching-skills` (STR-003), `skill-coaching-skills-wrapup` (STR-004), `skills/external/coaching-skills/SKILL.md` (STR-005) are owned by [`../requirements.md`](../requirements.md) § Shared Strings.

## C-1 Eight Identity Coordinates

| Coordinate | New value |
|------------|-----------|
| Source directory | `skills/external/coaching-skills/` |
| frontmatter `name` | `coaching-skills` |
| `skill_id` / Resource ID canonical path | `<SKILL:.specify/skills/coaching-skills/SKILL.md>` / `.specify/skills/coaching-skills/SKILL.md` |
| Runtime unit id | `skill:coaching-skills` |
| flow-class ledger row | `skill:coaching-skills` \| `execution` \| `behavior-oracle` \| (no neutral flag) \| new one-line rationale |
| probe Object row | `skill-coaching-skills-wrapup` \| `skill-wrapup` \| `skill:coaching-skills` \| `wrap-up` |
| `/speckit.skills` route row | points at `skills/external/coaching-skills/SKILL.md`, call form `coaching-skills <trainee-name|trainee-path> <work>` |
| description triggers | 教练 / 陪练 / 观察执行 / 预期 vs 实际 / 执行偏差 / 微调建议 / coaching, plus the explicit call form |

Trigger rule: triggers that promise a side-effect-free mental simulation only (“thought experiment”, “思想实验”, “不要真的执行”) MUST NOT survive, because the skill dispatches a real subagent. Triggers that express “predict first, then look at the real execution” may stay.

## C-2 Hand-Edited Source Files (closed set, 19)

| # | File | Change |
|---|------|--------|
| 1 | `skills/external/coaching-skills/SKILL.md` | New body (renamed from `skills/external/think-skills/SKILL.md`, rewritten to the coach loop) |
| 2 | `skills/external/coaching-skills/references/prompt-templates.md` | Renamed; expectation-phase fragments retained, observation/deviation templates added |
| 3 | `templates/commands/skills.md` | Route row + call form for the modify family |
| 4 | `agents/skill-verifier.agent.md` | `skills:` list |
| 5 | `agents/structure-adjuster.agent.md` | `skills:` list |
| 6–9 | `skills/internal/create-agent/templates/agent-capacity-{module-designer,requirements-analyst,system-designer,test-engineer}-template.md` | `skills:` list line **and** the capability-table row whose description states the old “simulate” meaning |
| 10 | `skills/internal/run-skills/SKILL.md` | modify-family pointer list |
| 11 | `shared/definitions/flow-class-definitions.md` | Ledger row, ledger version, change record |
| 12 | `shared/definitions/probe-definitions.md` | Probe Object row (id + handler unit) |
| 13 | `src/specify_cli/__init__.py` | `_OBSOLETE_SKILLS` entry; the historical comment restated without the old literal (C-6) |
| 14 | `docs/reference/agents/command-and-skills.md` | `skills:` example list |
| 15 | `docs/tutorials/quickstart.md` | Skill list entry (description updated, not just renamed) |
| 16 | `tests/contract/test_expression_compatibility.py` | Frozen roster + retired-path register (C-7) |
| 17 | `tests/contract/test_migration_distribution.py` | Frozen skill roster |
| 18 | `tests/contract/test_skill_layer_visibility_guards.py` | Frozen external roster + count assertion |
| 19 | `tests/contract/test_run_skills_wiring.py` | Frozen rosters + route-table needle |

Additionally, `shared/definitions/framework-map.md` gains the `.specify/memory/coaching/` row required by the new run directory (Constitution XVII). This is an addition, not a rename coordinate, and it introduces no occurrence of the old name.

## C-3 Derived Faces — Regenerated, Never Hand-Edited

| Derived face | Regeneration entry |
|--------------|--------------------|
| `.specify/skills/coaching-skills/**` | `python3 scripts/python/sync-mirrors.py --write --only skills/external` |
| `.specify/skills/think-skills/**` (removal) | **Explicit deletion** — `sync-mirrors.py` never deletes extras (archive-not-delete) |
| `.specify/shared/definitions/*.md` | same mirror entry, `--only shared` |
| `.specify/agents/templates/*.agent.md` | same mirror entry, `--only agents` |
| Per-tool command copies (`.claude/commands`, `.github/prompts`, `.opencode/command`, `.qoder/commands`) | `python3 scripts/python/regen-command-copies.py` (fan-out from `templates/commands/`) |
| Per-tool agent copies (`.qoder/agents/*.agent.md`; siblings via the same renderer) | `.venv/bin/specify render-agents --ai qoder` (and the other render tools when their directories are present) |
| Compiled `## Wrap-up` block in the skill body | `python3 scripts/python/probe-utils.py --action compile-embeds` |
| `.specify/memory/feedback/probe-map.md` | `python3 scripts/python/probe-utils.py --action map` |

## C-4 Upgrade Path

- The old directory name enters `src/specify_cli/__init__.py` `_OBSOLETE_SKILLS`.
- `cleanup_obsolete_framework_assets()` skips a path that is a symlink or absent and removes an entity directory. That is exactly the required behaviour: the entity directory is deleted, a user-authored symlink of the same name survives.
- No change to the cleanup code is required; the entry alone activates it.

## C-5 Route and Discovery Consistency

- The `/speckit.skills` route table keeps five rows; only the modify-family row changes name and gains the two-parameter call form.
- The skill keeps `classification: external` and stays under `skills/external/`.
- The description advertises the new call form so a reader who never saw the old skill can invoke it.

## C-6 Residual Rule

- Inside the closed wiring surface (C-2 plus C-3 derived faces), the old literal appears **exactly once**: the `_OBSOLETE_SKILLS` tuple entry.
- Consequence for `src/specify_cli/__init__.py`: the historical comment that currently spells the old name (inside the OBSOLETE-ASSET-REGISTRY region) is restated without the literal — it keeps the rename-chain meaning and points at Feature 078 instead of repeating the token.
- Historical records are outside the surface: `.specify/specs/**`, `.specify/memory/evidence/**`, `.specify/memory/features*/**`, `reviews/`, `eval-baseline/`, and run/feedback records archived under the old unit id.

## C-7 Frozen Baseline Tests

- All four test files are updated explicitly, each carrying a dated note with the reason (2026-10-30, Feature 078 rename).
- Counts stay consistent with the directory: 52 skills (15 external + 37 internal), 27 command templates, 49 hash-manifest skills.
- The hash manifest of 069a is a dated record and is not rewritten. `test_expression_compatibility.py` gains a retired-path register mapping the old manifest path to the new one with date and reason, so the C-5 “no new skill” assertion stays decidable instead of degrading into an empty assertion (see plan T-001).
- No test count may change silently; a change without its date-and-reason note fails review.

## C-8 Verifiable Surface

After implementation the following commands are the verification surface for SC-006 / SC-008. Each is expected to be run once against the real tree during `/speckit.implement`, and their outputs recorded in that stage's evidence:

```bash
python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "skill:coaching-skills"
python3 .specify/scripts/python/flow-class-check.py --action check
python3 scripts/python/probe-utils.py --action probes --validate
python3 scripts/python/probe-utils.py --action compile-embeds --check
python3 scripts/python/sync-mirrors.py --check
python3 scripts/python/regen-command-copies.py --check
python3 scripts/python/scan-confirmation-gates.py --summary
git grep -n "think-skills" -- <closed surface paths>
```

The `git grep` line is a template: the closed surface is enumerated in C-2 and C-3, and the expected result is one hit (the `_OBSOLETE_SKILLS` entry).
