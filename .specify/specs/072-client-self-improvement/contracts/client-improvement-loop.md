# Contracts: Client improvement loop (C-33…C-39)

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升
**Owner**: this file owns how the self-improvement loop treats a client (`custom:`) subject: the observation source of the why segment, the fail-closed disclosure, and the preserved loop constraints. The SI-0…SI-9 step bodies, the Execution Subject criteria, and the run-determination engine are owned elsewhere and cited here, never restated.
**Pinned by**: `tests/contract/test_client_improve_loop.py` (planned)
**Measures**: SC-004

**C-33**: A client project's improvement loop reuses the existing self-improvement skill's standard path (SI-0…SI-9). No client-specific improvement flow, skill, or ledger is created. The loop's subject must pass the five Execution Subject criteria, and those criteria gain no relaxation and no client-side exemption (FR-014, SC-004).

**C-34**: For a `custom:` subject the run-determination engine has no legitimate persistence source — its source contract accepts only command and skill unit forms and returns "not persisted" with a reason for other subjects, which the engine already reports honestly instead of dropping. The why segment of a client-subject loop therefore states the disclosure "运行判定历史未评估" together with the engine's reason, verbatim (FR-015, SC-004).

**C-35**: For a `custom:` subject the why segment's observation source is the client channel — this unit's `kind: external` entries — plus the existing evidence lanes. The loop invents no source string to make a write succeed, forges no history, and never phrases "no history" as "past runs were fine" (FR-015, SC-004).

**C-36**: Widening the run-determination source contract is the engine owner's action and is outside this feature's scope. This feature creates no client-side parallel history store and no second observation engine (FR-015, FR-027).

**C-37**: The how segment keeps routing through the existing dispatch table to the existing improvers (skill, agent, tool record, team), keeps the existing degrade-to-assisted path when no improver matches, adds no improver for client subjects, and never lets the command mutate a subject directly (FR-016).

**C-38**: The loop's existing constraints are preserved verbatim: one executed falsification attempt before every dispatch; exactly one intervention ledger, kept beside the baseline evidence run; the attempt limit remains a hard limit that stops the loop and demands human intervention; and the outcome state is reported as pending until the comparison of comparable runs completes, never as improved (FR-017, SC-004).

**C-39**: When a target resolves to no unique editable definition, the loop halts at subject resolution (SI-0), reports "no unique owner", leaves the observation for a follow-up carrier, mutates no file, and assumes no ownership (FR-018, SC-004).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-33 | FR-014 | SC-004 | skill + workflow |
| C-34 | FR-015 | SC-004 | workflow disclosure |
| C-35 | FR-015 | SC-004 | why observation source |
| C-36 | FR-015, FR-027 | — | scope boundary |
| C-37 | FR-016 | — | dispatch table |
| C-38 | FR-017 | SC-004 | loop constraints |
| C-39 | FR-018 | SC-004 | SI-0 halt |
