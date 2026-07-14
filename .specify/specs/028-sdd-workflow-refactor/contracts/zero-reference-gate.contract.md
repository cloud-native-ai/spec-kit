# Contract: Zero-Reference Gate

**ID**: C-GATE | **Feature**: 029 | **Maps to**: FR-010, FR-011, SC-001

## Interface

The final acceptance gate: no live `sdd-workflow` reference remains anywhere in active source.

## Rules

- A repository-wide search for the token `sdd-workflow` **MUST** return zero matches across active
  source: `src/`, `scripts/`, `templates/`, `skills/`, `agents/`, `docs/` (except excluded paths),
  `pyproject.toml`, and the regenerated `.specify/` mirror.
- The following paths are **excluded** (legitimately retain the token as historical/spec content):
  - `docs/summary/03-sdd-workflow-refactor-proposal.md`
  - `.specify/specs/028-sdd-workflow-refactor/**` (this spec, plan, contracts, tasks, verification)
  - `docs/history/**`
- No rewritten reference may resolve to a missing file (no runtime dead link).

## Verification Command

```bash
grep -rn "sdd-workflow" . \
  --exclude-dir=.git --exclude-dir=.venv --exclude-dir=docs/history \
  | grep -v "docs/summary/03-sdd-workflow-refactor-proposal.md" \
  | grep -v ".specify/specs/028-sdd-workflow-refactor/"
# Expected: no output (exit non-zero from grep = success for the gate)
```

## Test Mapping

- Integration test: run the gate command; assert empty result set (excluding the excluded paths).
- Integration test: enumerate all `shared/workflow/*` references in generated artefacts; assert each target file exists.
