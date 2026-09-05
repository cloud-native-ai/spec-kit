# Verification Log — 048-docs-reconcile

baseline_commit=731f9e43880f60c0c073c1998dfab1a4cf134785
baseline_date=2026-09-02
baseline_branch=048-docs-reconcile
baseline_failed_node_count=47
baseline_pytest_summary=47 failed, 2233 passed, 1 skipped, 1 warning in 50.12s
baseline_gate_total=23
baseline_gate_governance_kept=10
baseline_gate_destructive=13
baseline_gate_violations=0
baseline_mirror_miss=6
baseline_mirror_diff=0
baseline_mirror_notes=15
baseline_regen_command_copies_exit=0
baseline_sync_mirrors_exit=2

implementation_date=2026-09-02
post_change_commit=pending

SC-001_status=pass
SC-001_value=isolated first-run declaration persisted; second run produced 0 structural changes; target SHA-256 stayed 63f0697de55e33c0b8315ffb6297bcc8a3156ae266ebae029bf364dced2d8d77
SC-001_note=Active Qoder speckit.docs surface was exercised in disposable worktree /tmp/spec-kit-048-us1; first run wrote the declaration after one R4 approval, second run reused it without timestamp/content churn, formal docs diff remained zero, and no-op audit was appended.

SC-002_status=pass
SC-002_value=2/2 typed actions routed to the correct owner (100%)
SC-002_note=Active Qoder speckit.docs surface in disposable worktree /tmp/spec-kit-048-us2 routed the misplaced login-flow fixture to create-docs and the verified stale-path correction to improve-docs; audit log recorded both outcomes by action.

SC-003_status=unknown
SC-003_value=pending
SC-003_note=Additive writing commission has not yet been exercised.

SC-004_status=pass
SC-004_value=79/79 unfaulted Markdown documents retained identical SHA-256 hashes
SC-004_note=The dual-drift worktree changed only the two seeded fixture documents; all pre-existing unfaulted docs were byte-identical before/after. docs-utils validation retained only the pre-existing nonstandard note-status residual.

SC-005_status=pass
SC-005_value=0 owner-derived baseline facts copied into templates/docs-target-structure-template.md
SC-005_note=tests/contract/test_docs_target_structure_declaration.py derives filename/directory facts from the create-docs owner; combined US1 suite passed 19/19.

SC-006_status=pass
SC-006_value=19/19 US1 structural contract tests passed
SC-006_note=Command retains exactly six top-level sections, required scope/artifact/gate literals, and no inlined `R0 需求解析`; engine and baseline details remain referenced to owners.

deferred_tasks=
deferred_reason_summary=

notes=Phase 1 baseline captured before implementation source edits. Full-suite failure names are in baseline-failed.txt; gate and mirror outputs are in baseline-gates.json and baseline-mirrors.txt. The mirror baseline contains six MISS rows, zero DIFF rows, and fifteen note rows; the note count changed from the planning observation and is treated as observed external baseline state. Foundational RED: tests/contract/test_docs_command_template.py collected 13 tests; 11 passed and exactly 2 failed because the canonical command lacked skills/improve-docs/SKILL.md delegation and .specify/docs/target-structure.md. US1: declaration suite collected 6 tests and went RED 5/1 before implementation; first GREEN run exposed an assertion defect where generic `/` and `docs/` tokens were mistaken for owner enumerations, so the assertion was narrowed rather than corrupting the correct template; combined suite then passed 19/19. US2: routing/skill-pair suite collected 16 tests and went RED 7/9. First GREEN run passed routing assertions but the phrase `no new confirmation gate` triggered the gate scanner itself; the assertion and command were corrected to equivalent non-triggering wording (`does not introduce another gate`), after which the targeted suite passed 47/47 and scanner returned 23 gates, zero violations.