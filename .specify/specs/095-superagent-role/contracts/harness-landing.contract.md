# Contract — Harness Landing & Zero-Second-Mechanism Audit

**Status**: design contract (Feature 095) · Owners referenced, not restated: `shared/definitions/superagent-definitions.md` ([[STR-004]]); budget owner `scripts/bash/generate-instructions.sh` (`INSTRUCTIONS_BUDGET_BYTES`); pointer discipline `shared/guidelines/one-source-of-truth.md`.

## C-1. Instruction pointer section (FR-033)

`templates/instructions-template.md` gains exactly one new top-level section:

- Heading: `## Super Agent (相对逻辑角色)` — placed **between** `## Spec Kit Framework Map` and `## Spec Kit Runtime & Symlink Model`.
- Content (pointer form only): one sentence stating super agent is a relative logical role on a dispatch edge; the owner path `.specify/shared/definitions/superagent-definitions.md`; one sentence declaring that a dispatch granting dispatch duty physically carries the `role-transition` injection list.
- Size budget: **target ≤ 600 B** including heading. The live-file headroom is whatever the owner's budget mechanism reports at generation time — this contract does not carry the budget literal or the headroom number.
- MUST NOT contain: any byte count, any budget number, any copied rule text, any table.
- Degradation path (only legal disposition when the generator's report says `over`): shrink the section to a one-line pure pointer (~200 B). Raising the budget is out of scope (A7).

`.specify/instructions.md` is produced by running `scripts/bash/generate-instructions.sh` — never hand-edited. The generator's whole-section reconcile injects the missing section in template order.

**Section-count pin obligation**: `tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` pins the top-level `##` counts and requires a same-commit bump. The commit that adds the section MUST raise `TPL_EXPECTED` and `LIVE_EXPECTED` by `+1` each; adding the section without the pin bump turns that test red.

## C-2. Definition pointer lines (FR-032)

- `shared/definitions/agent-definitions.md`: one pointer line naming [[STR-004]] as the owner of the role concept (not a fourth layer).
- `shared/definitions/subagent-definitions.md`: one pointer line + one boundary sentence ("the parent-side role is owned there; this page owns the child side").
- `shared/definitions/framework-map.md`: one pointer row for the new owner page.
- None of these files gains rule text; `better-harness.md` is unchanged (clarify ruling).
- `agent-definitions.md` MUST NOT contain a second subagent definition after this change (guarded by the definitions contract test).

## C-3. Zero second mechanism (FR-035, SC-008)

The change set MUST show, by structural assertion:

1. **No new persistence root** — no new directory that stores state; only documentation, one engine file, tests and fixtures.
2. **No new registry** — no second index/store of executions or edges.
3. **No second renderer** — `status-digest.py` remains the only digest renderer.
4. **No second dispatcher/scheduler/queue**.
5. **Judgement face is read-only** — zero write points (engine contract C-6).
6. **Owner rules not copied** — concurrency, reporting and authorization rule text stays at its owner; the new surfaces carry pointers.

The audit is a test, not a prose claim: `tests/contract/test_superagent_zero_mechanism.py` scans the change-set file list and the new/changed sources for the six assertions; injecting a second store path or renderer turns it red.

## C-4. Budget verification

`scripts/bash/generate-instructions.sh`'s budget report is the judge: its `BUDGET:` line ends `(within|over)`, and its log line prints `Instructions size: <n> B (budget <b> B, <m> B headroom)`. The live-file criterion is `within` on the `BUDGET:` line, with a positive headroom in the log line. This contract's only number is the C-1 section size target.

## C-5. Guarding tests

- `tests/contract/test_instructions_budget_superagent_section.py`: section exists between the two fixed neighbours; pointer form (no budget literal, no copied rules); generated live file carries the section; budget report `within` (asserted by re-running the report path or by the live-size check that already exists in `tests/contract/test_instructions_size_budget.py`).
- `tests/contract/test_superagent_zero_mechanism.py`: the six C-3 assertions.
- `tests/contract/test_superagent_definitions.py`: owner page both sides + pointer-only discipline + nine-item list + depth-vs-license-chain sentence.

## C-6. Command examples

> **Premises / execution status (per example)**: the template section does **not exist yet**; the generator exists and its budget mechanism is measured today (2026-11-10): the budget is owned by `INSTRUCTIONS_BUDGET_BYTES` in `scripts/bash/generate-instructions.sh`, and the live/template sizes were captured in `test-evidence/plan-stage-evidence.md`. The `within` expectation below is pinned by the guarding tests (route: contract-test pinning); `/speckit.tasks` MUST run the generator once during implementation and paste its full budget report into `test-evidence/`. Premises: the generator is run from repo root and reconciles `.specify/instructions.md` from `.specify/templates/instructions-template.md` (mirror), not from the framework source directly — so the template mirror must be synced before generation.

```bash
python3 scripts/python/sync-mirrors.py --write --only templates/instructions-template.md
bash scripts/bash/generate-instructions.sh
```

Expected after implementation (pinned, not assumed now): the report's `BUDGET:` line ends `within`; the log line shows a positive headroom; the per-section table carries one row for `## Super Agent (相对逻辑角色)`; the live file contains the section.
