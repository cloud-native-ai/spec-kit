# Contract — Stage Agents and Turn Budgets

Owners: `skills/internal/create-agent/SKILL.md`, `src/specify_cli/__init__.py` (render mapping), `.specify/agents/.render-manifest.json`.

- **C-001**: The stage role grammar MUST be coordinator/worker/verifier/integrator; the user-named roles `sdd-requirement-analyzer`, `sdd-plan-coordinator`, and `sdd-plan-executor` MUST exist.
- **C-002**: Stage agent count and type MUST be dynamic; no fixed per-stage count is a contract.
- **C-003**: Every retained framework agent MUST carry `run-turn-budget: 500`; rendered copies MUST carry `maxTurns: 500` or `steps: 500`.
- **C-004**: The generic `sdd-executor` MUST NOT exist in sources, mirrors, rendered copies, or the render manifest after cleanup.
- **C-005**: Live references and tests MUST be updated; dated state/evidence records MUST NOT be rewritten. (FR-025, FR-026, FR-027, FR-028, FR-029, FR-030, FR-047, FR-048, FR-049, FR-050)
