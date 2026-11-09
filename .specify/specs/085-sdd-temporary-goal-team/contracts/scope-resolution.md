# Contract — Scope Resolution

Owner: `scripts/python/goal-utils.py` action `resolve-scope`. Consumers: `/speckit.goal`, `/speckit.team`, `run-checks`, `sdd-route.py authorize`, `create-team`, `run-team`, `improve-team`, evidence runs lane.

- **C-001**: `resolve-scope` MUST accept `--scope global|spec|auto`, `--spec-dir <path>`, optional `--team <slug>`, and `--json`.
- **C-002**: `global` MUST resolve `goal_root=.specify/anchoring` and `team_root=.specify/teams`.
  <!-- superseded (092: scope-not-temporary; path side: `.specify/goal` → `.specify/anchoring`) -->
  <!-- prior text, retained (2026-11-09): "`global` MUST resolve `goal_root=.specify/goal` and `team_root=.specify/teams`." -->
- **C-003**: `spec` MUST resolve `goal_root=<spec-dir>/goal` and `team_root=<spec-dir>/team`.
- **C-004**: `spec` MUST require a spec directory that is under `.specify/specs/`; absent or invalid input exits 2 with a named reason.
- **C-005**: `auto` MUST resolve only when exactly one of the global or spec candidate exists; both existing exits 2 `scope-ambiguous` and names both paths.
- **C-006**: `auto` MUST NOT silently prefer global when both exist.
- **C-007**: A write operation MUST require an explicit `global` or `spec` scope; `auto` is read-only.
- **C-008**: A wrong-scope identity MUST exit 3 and MUST name the other scope as a hint; no fallback is permitted.
- **C-009**: The returned object MUST carry `scope`, `spec_dir`, `goal_root`, `team_root`, `goal_definition`, and `team_definition`.
- **C-010**: `sdd-route.py authorize` MUST resolve the team path with the same rule and MUST add `scope`/`spec_dir` to its record.
- **C-011**: `run-checks` MUST add `scope` and `spec_dir` to its payload without changing the existing `resolution` keys.
- **C-012**: Existing global behavior without `--scope`/`--spec-dir` MUST remain byte-identical.
- **C-013**: The command templates `templates/commands/goal.md` and `templates/commands/team.md` MUST expose the flags and delegate to the resolver; per-tool copies are regenerated, never hand-written.
- **C-014**: Every consumer MUST reach the same rule by the resolver or a shared `Scope` object; a second path implementation is a defect. (FR-012, FR-013, FR-014, FR-015, FR-016, FR-017)
