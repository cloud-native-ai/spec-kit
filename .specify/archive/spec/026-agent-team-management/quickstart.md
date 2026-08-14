# Quickstart: Agent Team Management

**Feature**: 027 Team Management | **Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

This walkthrough validates the three `/speckit.team` modes and the single-agent ↔ team separation.

## Prerequisites

- `specify init` completed; `.specify/agents/` populated with the seven role agents.
- `/speckit.team` command installed; `create-team` + `improve-team` skills installed.

## 1. Create a team (mode: create)

```text
/speckit.team 组织一个团队，用系统架构师、模块设计师和测试工程师串行完成 X 功能
```

Expected:
- Intent classified as **create** → routed to `create-team`.
- Pattern inferred: **serial** (sequenced roles).
- A roster is proposed (system-designer → module-designer → test-engineer) and, on confirmation, persisted to `.specify/teams/x-feature-team.team.md` with a Static Structure matrix and a Dynamic Structure (DAG + handoff).

**Verifies**: US1, FR-001, FR-004, FR-007.

## 2. Modify the team (mode: modify)

```text
/speckit.team 给 x-feature-team 增加一个 QA 工程师做质量门禁
```

Expected:
- Intent classified as **modify** → routed to `improve-team`.
- The existing `.team.md` loads; a `qa-engineer` member is added; the rest of the team is unchanged; `updated` date bumped.
- A change report lists the single edit and its rationale.

**Verifies**: US2, FR-008, FR-009, SC-005.

Negative check:

```text
/speckit.team 优化 nonexistent-team
```

Expected: "team not found" + an offer to create it (FR-010).

## 3. Run the team (mode: run) — preview → confirm → execute

```text
/speckit.team 运行 x-feature-team
```

Expected sequence:
1. **Static Structure** printed — Role × Stage × Type matrix of the roster (agent, role, Worker/Meta, persistent/temporary).
2. **Dynamic Structure** printed — pattern = serial; DAG stage order; an execution flow diagram.
3. **Confirmation gate** — the run does **not** start until the user explicitly confirms.
4. On confirm → serial orchestration executes (file-path-only handoff, DAG validated); on decline → nothing executes.

**Verifies**: user planning input (3 modes + preview/confirm), FR-017, command contract § Run-mode.

## 4. Separation of concerns

- `/speckit.agents 组织一个团队…` → directed to `/speckit.team` (team ops not served by the single-agent command). **Verifies** US3, FR-003.
- Inspect `skills/create-agent/SKILL.md` → no Conceptual Model section, no `triad`/`team-supervisor` modes. **Verifies** FR-011, FR-013, SC-003, SC-006.
- Repo search for `organize-agents` in active paths → zero hits. **Verifies** FR-006, SC-004.

## 5. Guard tests

Run `pytest -m contract` — the M7 guard tests (zero dangling reference, single Conceptual Model, single-agent purity, command routing, skill presence) pass.
