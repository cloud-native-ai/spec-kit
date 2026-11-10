# Quickstart — Super Agent Role (095)

**Audience**: a framework maintainer who wants to answer "who is whose super agent", watch a fan-out, or wire a dispatch payload. Reader baseline inherited from the `Readers` / `Reading scenario` fields in `requirements.md` frontmatter (global baseline reader per `shared/guidelines/user-facing-comprehension.md`).

> **Execution status (applies per example below)**: this feature is in the plan stage — the engine, the digest fields and the payload wiring **do not exist yet**. Every command below is pinned by the guarding contract test named beside it (deferred-execution route per `/speckit.plan`'s Post-Generation Quality Gate); `/speckit.tasks` re-runs each one during implementation and records the reading in `test-evidence/`. Premises per example are stated with the example.

## Scenario 1 — Ask who is whose super agent

Premises: `scripts/python/role-edge-check.py` exists with `--action query`, `--parent`, `--child` and the exit codes of `contracts/role-edge-engine.contract.md`; a fixture tree exists under `tests/fixtures/superagent-role/root-a-b/`. Pinned by `tests/contract/test_role_edge_engine.py`.

```bash
python3 scripts/python/role-edge-check.py --action query \
  --parent root --child A \
  --state-dir tests/fixtures/superagent-role/root-a-b/state \
  --teams-dir tests/fixtures/superagent-role/root-a-b/teams \
  --logs-dir tests/fixtures/superagent-role/root-a-b/logs \
  --registry-dir tests/fixtures/superagent-role/root-a-b/registry
```

What you learn: whether an edge `root → A` exists, A's role set (on this fixture: `["subagent","superagent"]` — A also parents B), and both depths (root 0, A 1, B 2 via the full report). The full model is `--action report` with the same roots.

## Scenario 2 — See the role view in the existing digest

Premises: the role fields have been added to `status-digest.py`; the `nothing-running` / `omitted` / stale semantics are unchanged (measured today on this tree). Pinned by `tests/contract/test_status_digest_roles.py`.

```bash
python3 .specify/scripts/python/status-digest.py --action digest
python3 .specify/scripts/python/status-digest.py --action digest --format json
```

What you learn: each executor row shows identity, parent edge, role set, depth, state, age and stale flag; a truncated list declares `omitted=<n>`; an idle system renders `nothing-running` rather than an empty list.

## Scenario 3 — Grant dispatch duty and carry the injection

There is no command for this scenario — it is a payload-writing obligation owned by the dispatch surfaces (`run-agent` injection block, team Per-Agent Payload, driver stage envelope; see `contracts/role-transition-payload.contract.md` § C-11). After implementation, the payload carrying dispatch duty contains the literal `role-transition` plus the nine pointer items; the existing pre-dispatch self-check blocks a payload missing it. Pinned by `tests/contract/test_role_transition_payload.py`.

## Scenario 4 — Verify the harness landing is inside budget

Premises: the template section has been added; the generator is run from repo root; the template mirror is synced first. Measured before the edit: budget 38,400 B, live 37,454 B, headroom 946 B (2026-11-10). Pinned by `tests/contract/test_instructions_budget_superagent_section.py`.

```bash
python3 scripts/python/sync-mirrors.py --write --only templates/instructions-template.md
bash scripts/bash/generate-instructions.sh
```

What you learn: the generator's budget report shows its `BUDGET:` line ending `within` plus a positive headroom in the `Instructions size:` log line, and its per-section table shows the new `## Super Agent (相对逻辑角色)` row. If the report says `over`, the only legal fix is shrinking the section to a one-line pointer (never raising the budget).

## Where things live

| Thing | Path |
|-------|------|
| Role model owner | `.specify/shared/definitions/superagent-definitions.md` |
| Judgement engine | `scripts/python/role-edge-check.py` (source) / `.specify/scripts/python/role-edge-check.py` (runtime) |
| Digest view | `scripts/python/status-digest.py` |
| Payload wiring | run-agent / create-team / sdd-loop-driver surfaces listed in `contracts/role-transition-payload.contract.md` |
| Fixtures | `tests/fixtures/superagent-role/` |
| Guards | `tests/contract/test_role_edge_engine.py`, `test_role_transition_payload.py`, `test_status_digest_roles.py`, `test_superagent_definitions.py`, `test_instructions_budget_superagent_section.py`, `test_superagent_zero_mechanism.py` |
