# Quickstart: Validating the Agent Framework Redesign

**Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

This walkthrough validates the refactor against the Success Criteria. Run from repo root.

## 1. Terminology is unified (SC-002, SC-009)

```bash
# Expect 0 matches in LIVE files (exclude specs/CHANGELOG/draft)
grep -rliE "subrole|improver" \
  --include="*.md" --include="*.py" --include="*.sh" . \
  | grep -vE "/\.specify/specs/|CHANGELOG|/draft/|/features/019\.md"
```

Expected: **no output**. `.specify/agents/*.agent.md` MUST NOT appear (SC-009).

## 2. Templates canonicalized (SC-003)

```bash
ls skills/create-agent/templates/agent-stage-*.md        # 3 stage templates present
ls skills/create-agent/templates/agent-role-team-supervisor-template.md  # merged supervisor
ls templates/ | grep -iE "^agent-" || echo "OK: no agent-* in top-level templates/"
ls .specify/templates/ | grep -iE "^agent-" || echo "OK: no stale agent-* in .specify/templates/"
```

Expected: stage/role templates present; **no** `agent-subrole-*`, `agent-role-meta-coordinator-*`, or top-level/`.specify` `agent-*` duplicates.

## 3. Reference integrity (SC-004)

```bash
# No lingering references to old names anywhere live
grep -rE "agent-subrole-|meta-coordinator" \
  skills/ templates/ docs/ tests/ .specify/agents/ .specify/skills/ \
  | grep -viE "/features/019\.md" || echo "OK: no dangling old references"
pytest -q                    # existing suite + new deprecated-term guard must pass
```

## 4. Conceptual model expressed (SC-005)

- Open any `agent-role-*-template.md` and confirm it states **Role**, applicable **Stage(s)**, and **Type** per the [conceptual-model contract](./contracts/conceptual-model-contract.md).
- Confirm the Team matrix in `data-model.md` matches `docs/agents/design.md`.

## 5. Single entry & scenarios (SC-001, SC-006)

- Confirm `/speckit.agents` is the only agent command:

```bash
ls .qoder/commands/ .github/prompts/ | grep -iE "agent" # only speckit.agents(.md/.prompt.md)
```

- Invoke `/speckit.agents` with each intent and confirm routing per the [command contract](./contracts/agents-command-contract.md):
  - "create a system-designer agent" → `create-agent`
  - "run these agents in parallel" → `organize-agents` (parallel)
  - "run a team loop until quality ≥ 0.85" → `organize-agents` (team-loop, Team Supervisor + Workers)
- Ambiguous input (e.g. "agents") → command lists capabilities and asks for intent (FR-019).

## 6. Docs coherent (SC-007)

- Review `docs/agents/{design.md,eei-triad-pattern.md,multi-agent-orchestration.md}` and `docs/commands/agents.md`: terminology unified, model consistent with `design.md`.

## 7. Cross-project research delivered (SC-008)

- Confirm `.specify/specs/023-agent-framework-redesign/research.md` exists, covers each in-scope `/cws_work/*` sibling project (one agent per project), and that ≥1 redesign decision cites it.
