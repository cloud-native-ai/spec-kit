# Quickstart: Agent Skill Enablement

**Feature**: 026 — Agent Skill Enablement
**Spec**: [requirements.md](./requirements.md) · **Plan**: [plan.md](./plan.md)

This quickstart shows how to verify that the seven built-in role agents are skill-enabled.
It maps directly to the user stories in `requirements.md`.

## Prerequisites

- A Spec Kit workspace with agents installed under `.specify/agents/` and skills under
  `.specify/skills/`.
- `pytest` available (`pytest -m contract`).

## Scenario 1 — Each agent declares role-relevant skills (US1, US3)

1. Open any built-in agent, e.g. `agents/requirements-analyst.agent.md`.
2. Confirm the frontmatter includes a `skills:` list, e.g.:

   ```yaml
   skills: [draw-plantuml, memory-recall, memory-record, think-skills]
   ```

3. Confirm the body contains a `## Skill Enablement` section with the shared preference
   protocol and a `| Skill | When to use |` table matching the declared skills.
4. Repeat for the other six agents; confirm the section format and protocol text are
   identical (only the skill table differs).

**Expected**: All 7 agents declare ≥1 role-relevant skill and share one consistent format
(SC-001, SC-005).

## Scenario 2 — Agents prefer skills for covered operations (US1)

1. Ask the **System Designer** to produce an architecture diagram.
   - **Expected**: it uses the `draw-plantuml` skill rather than hand-writing diagram markup.
2. Ask the **Module Designer** to assess the current project structure before a change.
   - **Expected**: it uses the `analysis-project` skill.
3. Ask the **Test Engineer** to run an end-to-end web check.
   - **Expected**: it uses the `browser-utils` skill.

**Expected**: The declared, role-matched skill is invoked for the covered operation (SC-003).

## Scenario 3 — Graceful fallback (US1, edge cases)

1. Ask an agent to perform an operation with no matching skill (e.g. a plain textual summary).
   - **Expected**: the agent completes it directly, without inventing or forcing a skill.
2. Simulate a skill being unavailable.
   - **Expected**: the agent degrades to direct execution and surfaces the failure rather than
     stalling.

## Scenario 4 — No dangling skill references (US2)

Run the contract test:

```bash
pytest -m contract tests/contract/test_agent_skill_enablement.py -q
```

**Expected**: green. Every declared skill resolves to an installed
`.specify/skills/<slug>/SKILL.md`, every agent declares ≥1 skill, no agent declares a
non-declarable skill (`sdd-workflow`, `create-agent`, `improve-agent`, `create-skills`,
`improve-skills`, `organize-agents`), and each agent has a `## Skill Enablement` heading
(SC-002).

## Scenario 5 — No regression (US, FR-011)

```bash
pytest -m contract tests/contract/test_shipped_agent_presets.py -q
```

**Expected**: green. Existing frontmatter fields (`name`, `description`, `model`, `tools`,
`maxTurns`) and supervision/role-scope wiring are intact (SC-004).

## Done

When all five scenarios pass, the feature satisfies its Success Criteria and is ready for
`/speckit.tasks`.
