# Feature Reference — 102-line-registry-registration

**Bound Feature**: 088 — Speckit 框架可视化（Speckit Framework Visualization）, registered as **slice row 102**.
**Binding basis**: 088 owns `shared/guidelines/reporting-obligations.md` § 九 · 当前态摘要契约, the only contract this feature extends (A-14). Parent row status stays `Completed`; 102 is the row that moves.
**Parent detail**: `.specify/features/088-speckit-visualization.md`.

## How this plan maps to Feature 088

| Plan element | Feature 088 element it serves | Direction |
|--------------|-------------------------------|-----------|
| Owner-doc criterion (C-01…C-04) | § 九 digest contract | append one criterion — no rewrite of the contract |
| Wrapper `line-run.sh` | § 九's "reads state artifacts" premise | supplies the missing carrier so a long task can enter the registry |
| Scanner | § 九's freshness and explicit-emptiness claims | makes "unregistered ⇒ invisible" mechanically visible |
| `status.md` sentence | the thin-entry / single-renderer rule | restates nothing; pins registry-only reading |
| Ambient bullet | `## Progress Reporting Discipline` | one pointer so every session sees the duty |
| run-team wiring | § 八 three modes / two carriers | the executor carries the duty with it |

The feature does **not** change the digest's action set, exit codes, rendering or `[[STR-006]]`; it does not add a second parser, renderer, registry or status spine.

## Delivery surface (SC-009's allowed delta)

Authored framework sources:

1. `scripts/bash/line-run.sh` (new)
2. `scripts/python/line-registration-scan.py` (new)
3. `shared/guidelines/reporting-obligations.md` (edit, § 九 + 判定边界 ownership line)
4. `skills/internal/run-team/SKILL.md` (edit, §5 / §6 / §7)
5. `templates/commands/status.md` (edit, Delegation section)
6. `templates/instructions-template.md` (edit, one bullet)

Tests (new):

7. `tests/contract/test_line_run_contract.py`
8. `tests/contract/test_line_registration_scan.py`
9. `tests/contract/test_line_registration_wiring.py`
10. `tests/integration/test_line_run_behavior.py`
11. `tests/integration/test_line_registration_scan_live.py`

Generated mirrors and copies (never hand-edited):

12. `.specify/scripts/bash/line-run.sh`
13. `.specify/scripts/python/line-registration-scan.py`
14. `.specify/shared/guidelines/reporting-obligations.md`
15. `.specify/skills/internal/run-team/SKILL.md`
16. `.specify/templates/instructions-template.md`
17. `.claude/commands/speckit.status.md`
18. `.github/prompts/speckit.status.prompt.md`
19. `.qoder/commands/speckit.status.md`
20. `.opencode/command/speckit.status.md`
21. `.specify/instructions.md` (refreshed through `/speckit.instructions`; timestamped backups `.specify/instructions.md-*` are git-ignored and MUST NOT be committed)

This spec directory:

22. `.specify/specs/102-line-registry-registration/**`

Lifecycle registration:

23. `.specify/features.md` (102 row `Draft → Planned`)
24. `.specify/features/088-speckit-visualization.md` (plan note for the slice)

**Explicitly outside the delta**: `scripts/python/status-digest.py`, the engine `line-registry.py`, `scripts/bash/generate-instructions.sh`, `skills/internal/create-team/**`, `pyproject.toml`, and the two pre-existing untracked files `.specify/scripts/line-registry.py` / `.specify/scripts/stage-runner.sh` (neither committed nor reverted, FR-023).
