# Data Model — Feature 090 Re-Anchoring

**Feature**: 090-re-anchoring | **Date**: 2026-11-09 | **Plan**: [plan.md](plan.md)

This feature stores no runtime data and introduces no store. Its "entities" are the artifacts and verdicts the
discipline makes machine-checkable; each entity names its **carrier** (the file that holds it) and the **validation
rules** a guard or the protocol asserts. Clause identifiers refer to the four contract pages under `contracts/`.

## Entities

### E-1 — Direction anchor（方向锚）

The entry-time record an agent keeps across compactions. Two halves, both required.

| Field | Meaning | Carrier |
|-------|---------|---------|
| `task_anchor` | goal verbatim, non-goals, acceptance authority, stage plan, decision gates | state spine `direction_contract`; subagent brief |
| `rule_anchor` | the operating rules in force: unattended / no approval request / U4 → next stage / spine before acting / workspace guard / fast-fail / gate discipline / budget | state spine `driver_contract`; subagent brief |
| `next_action` | the named next step | state spine `next_action` |

Rules: V-1 (both halves present), V-2 (persisted, never conversation-only). Relationship: E-1 1—N E-2 (one anchor
supports many audits).

### E-2 — Core step

The trigger of an audit. A closed set of four: stage U4, package boundary, checkpoint, subagent return.

| Field | Meaning | Carrier |
|-------|---------|---------|
| `kind` | one of the four literals above | owner page § 1.2 |
| `position` | stage / package / checkpoint id | checkpoint file |

Rules: V-3 (closed set — an audit trigger outside it is not an E-2). Relationship: E-2 1—1 E-3.

### E-3 — Reload tier

How much of the anchor is re-read at an E-2.

| Field | Value | Cost | Trigger |
|-------|-------|------|---------|
| `T0` | `driver_contract` + `direction_contract` + `next_action` (or the brief's anchor digest) | ≈1 KB | every core step |
| `T1` | driver `SKILL.md` Hard Requirements + the checkpoint protocol | ≈5 KB | stage boundary, detected compaction, after a subagent turn-limit stall, two consecutive same-direction drifts |
| `T2` | the full manual plus one reference | on demand | dispatch form unclear, or a stall is being handled |

Rules: V-4 (tier chosen by position, not by preference), V-5 (a full reload at every tool call is forbidden).

### E-4 — Audit verdict

The three-valued outcome.

| Field | Meaning | Carrier |
|-------|---------|---------|
| `value` | `on-track` · `correction-applied` · `decision-needed` | checkpoint `§ 5 Direction audit` |
| `evidence` | a path or a reading per question | checkpoint |
| `surfaced` | `true` only for `decision-needed` | checkpoint / fast-fail channel |

Rules: V-6 (closed over three values), V-7 (only `decision-needed` is surfaced; the other two are recorded and the loop
continues), V-8 (the verdict is a statement — it never ends with a question to the user).

### E-5 — Rule face

One of the surfaces that must carry the rule. Closed set of six:

| # | Face | Path |
|---|------|------|
| 1 | Owner page | `shared/definitions/re-anchoring-definitions.md` |
| 2 | Constitution (template) | `templates/constitution-template.md` |
| 3 | Constitution (live) | `.specify/memory/constitution.md` |
| 4 | Instructions (template) | `templates/instructions-template.md` |
| 5 | Instructions (live) | `.specify/instructions.md` |
| 6 | Agent obligation | `shared/definitions/agent-definitions.md` |

Plus the protocol face `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` § 5, which carries the
executable procedure rather than the concept.

Rules: V-9 (all faces present), V-10 (every non-owner face points at the owner). Relationship: E-5 1—N E-6.

### E-6 — Guard assertion

One falsifiable proposition about an E-5 face or the protocol face.

| Field | Meaning | Carrier |
|-------|---------|---------|
| `module` | the contract test module | `tests/contract/` |
| `test` | the test function name | module |
| `clause` | the contract clause it enforces | `contracts/*.md` |
| `red_control` | how the assertion was shown to fail | module docstring / evidence |

Rules: V-11 (every clause a guard cites exists in a contract page), V-12 (every guard reds when its subject breaks).

## Validation rules

| ID | Rule | Enforced by |
|----|------|-------------|
| V-1 | The anchor carries both halves; a task-only anchor is incomplete | `direction-audit.contract.md` C-4; owner page § 1.1 |
| V-2 | The anchor is persisted (spine or brief), never conversation-only | owner page § 1.1; `agent-definitions.md` |
| V-3 | An audit trigger is one of the four core-step kinds | owner page § 1.2 |
| V-4 | The tier is chosen by position (T0 default, T1 at boundaries, T2 on ambiguity) | `direction-audit.contract.md` C-8 |
| V-5 | A full reload at every tool call is forbidden | C-8; `test_sdd_loop_driver_reanchor.py::test_reload_tiers_are_bounded` |
| V-6 | The verdict is one of exactly three values | C-5; same module |
| V-7 | Only `decision-needed` is surfaced | C-5; `agent-definitions.md` |
| V-8 | The audit is a statement, never an approval request | C-7; driver `SKILL.md` HR14 |
| V-9 | All six faces plus the protocol face exist | `re-anchoring-faces.contract.md` C-1…C-6; `test_reanchoring_contract.py` |
| V-10 | Every consumer face is a pointer, never a copy | C-7; `test_reanchoring_contract.py::test_both_instruction_surfaces_carry_the_ambient_section` |
| V-11 | Every guard cites an existing contract clause | `guard-tests.contract.md` C-1, C-2 |
| V-12 | Every guard reds when its subject breaks | C-4; `test_constitution_double_landing.py` C-10 probe as the precedent |

## State transitions

The only state machine this feature touches is the checkpoint's own, and it is unchanged:

```text
checkpoint opened -> parts 1..4 drafted -> part 5 audit answered (tier + five questions + verdict)
   verdict = on-track            -> record, continue
   verdict = correction-applied  -> record the correction and its disclosure, continue
   verdict = decision-needed     -> record, surface via fast-fail, halt at the anomaly point
```

An audit never mutates the anchor it read: a `correction-applied` verdict changes the *work*, and a `decision-needed`
verdict changes nothing until the decision returns.

## What this model deliberately does not contain

No store, no index, no ledger, no scoring schema, no scheduler. E-1 is carried by the state spine that already exists,
E-2/E-3/E-4 by the checkpoint file that already exists, E-5 by governance files that already exist, and E-6 by the
pytest modules that already exist. Adding a persisted aggregate over E-4 is the exact second-mechanism failure
`plan.md` T-002 rejects.
