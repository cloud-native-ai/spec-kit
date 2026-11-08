# Contract — Re-Anchoring Faces

**Feature**: 090-re-anchoring | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)

The five human-facing surfaces that must simultaneously exist and point at one owner. Each clause names the path, the
anchor, and the assertion a guard can make. `FR-001`…`FR-003`, `FR-008`, `FR-009`; `SC-001`.

## C-1 — The owner page exists and declares what it owns

`shared/definitions/re-anchoring-definitions.md` MUST exist and MUST carry, in its first screen, an `Owner（唯一所有者）`
declaration naming the three things it owns: the concept definitions, the reload tiers, and the agent-side obligation.
It MUST delegate the executable procedure to `sdd-loop-driver/references/checkpoint-protocol.md` § Direction audit by
path, and MUST NOT restate that procedure.

## C-2 — The owner page carries both concepts, the tiers and the three verdicts

The page MUST contain the literals `不忘初心`, `温故而知新`, `规则锚`, `T0`, `T1`, `T2`, `on-track`,
`correction-applied`, `decision-needed`. Asserted by
`tests/contract/test_reanchoring_contract.py::test_owner_document_carries_both_concepts_and_the_tiers`.

## C-3 — Both constitution surfaces carry the principle, with the same title

`templates/constitution-template.md` and `.specify/memory/constitution.md` MUST each carry the heading title
`Re-Anchoring (不忘初心 · 温故而知新)`. The numeral is **not** part of the proposition: the template holds it as `XXI`
and the live roster as `XXII`, because the live roster carries project-specific principles the template does not.

## C-4 — Both instruction surfaces carry the ambient section and the owner pointer

`templates/instructions-template.md` and `.specify/instructions.md` MUST each carry a section headed
`## Re-Anchoring (不忘初心 · 温故而知新)` whose body names `.specify/shared/definitions/re-anchoring-definitions.md`.
The live file is produced from the template by `scripts/bash/generate-instructions.sh`; the only admissible edit to
that script for this feature is raising `INSTRUCTIONS_BUDGET_BYTES`.

## C-5 — The agent obligation is declared on the neutral template

`shared/definitions/agent-definitions.md` MUST carry a `## Re-Anchoring Obligation` section naming the owner page and
stating the two duties (restate the anchor at entry; after each core step re-read the rules first and record the
verdict). It MUST also state that the dispatcher carries the anchor summary into every subagent brief.

## C-6 — The constitution generator mandates the principle

`skills/internal/manage-constitution/SKILL.md` MUST carry a `- **<Title>** — …` sub-entry for the principle inside its
`- **MUST include**` block, and the sub-entry MUST point at the owner page.

## C-7 — Every consumer is a pointer, never a copy

No consumer surface (C-3…C-6) may restate the tier table or the five questions. A consumer MAY name the rule in one
sentence; the criteria, the tier cost table and the question list live only in the owner page or the checkpoint
protocol.

## C-8 — The owner page introduces no machinery

The owner page MUST state that the discipline's carriers are the existing state spine, checkpoints, assignment brief and
fast-fail channel, and MUST NOT define a store, a ledger, a score or a schedule.
