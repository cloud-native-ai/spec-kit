# Contract: Conceptual Model

**Spec**: [requirements.md](../requirements.md) | **Plan**: [plan.md](../plan.md)

Normative definitions for the redesigned Agent framework. Keywords MUST / MUST NOT / SHOULD per RFC 2119.

## C1. Three Attribute Dimensions

Every Agent MUST be describable by three orthogonal dimensions:

- **Role** — the responsibility and problem-solving perspective. MUST map to exactly one `agent-role-<role>-template.md`.
- **Stage** — one of `executor`, `evaluator`, `optimizer`. MUST use these canonical names.
- **Type** — one of `Worker`, `Meta`. MUST be derived from Stage per C3.

The dimension name **SubRole MUST NOT** appear in any live artifact. The stage name **improver MUST NOT** appear; `optimizer` MUST be used.

## C2. Organizational Structures

- **Team** (static): a Role × Stage matrix. Each row is a Role, each column is a Stage, each cell states the Type.
- **Loop** (dynamic): the runtime iteration across stages executed by a multi-agent group.

## C3. Type-follows-Stage (NORMATIVE)

| Stage | Resulting Type |
|-------|----------------|
| executor | Worker |
| evaluator | Meta |
| optimizer | Meta |

A **Meta role** (Team Supervisor) MUST be `Meta` at all stages and MUST NOT perform real project tasks.

## C4. Team Supervisor (merged)

There MUST be exactly one merged **Team Supervisor** Meta role that unifies the former "Meta-Coordinator" and "Team Supervisor" responsibilities (task coordination + team supervision). References to "Meta-Coordinator" as a separate role MUST NOT remain.

## C5. Roles Inventory

Worker roles (this iteration): Requirements Analyst, System Designer, Module Designer, Test Engineer, QA Engineer, Knowledge Manager. Meta role: Team Supervisor. UX Analyst is deferred (Decision D1) and is NOT required to have a template this iteration.

## C6. Conformance

Any Agent definition or role/stage/orchestration template MUST express Role, Stage, and Type consistently (SC-005). Any artifact violating C1–C4 is non-conformant and MUST be corrected.
