# Verification Log — 049-docs-reconcile

baseline_commit=731f9e43880f60c0c073c1998dfab1a4cf134785
baseline_date=2026-09-02
baseline_branch=048-docs-reconcile (renumbered to 049-docs-reconcile during upstream merge on 2026-09-06)
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

implementation_date=2026-09-05
post_change_commit=phase commits a4c379ee,d56fa466,7968bda2; final polish commit contains this verification log
completion_gates=GATE-1 through GATE-8 pass on 2026-09-05
final_open_tasks=0
final_deferred_tasks=0
final_success_criteria=7 pass / 0 partial / 0 fail / 0 deferred
post_targeted_contract_passed=99
post_full_suite_failed_nodes=47
post_full_suite_passed=2257
post_full_suite_skipped=1
post_new_failures_vs_baseline=0
post_resolved_failures_vs_baseline=0
post_gate_total=23
post_gate_governance_kept=10
post_gate_destructive=13
post_gate_violations=0
post_mirror_miss=6
post_mirror_diff=0
post_new_mirror_drift=0
post_docs_validation_new_findings=0
post_docs_validation_preexisting_findings=1
post_upstream_merge_commit=cc344fcac377935fecd94416d2b52bd49ca35e12
post_upstream_merge_targeted_passed=334
post_upstream_merge_failed_nodes=43
post_upstream_merge_passed=2495
post_upstream_merge_skipped=1
post_upstream_merge_new_failures=0
post_upstream_merge_resolved_baseline_failures=4
merge_requirement_renumber=048-docs-reconcile -> 049-docs-reconcile (upstream reserved 048-derive-command)

SC-001_status=pass
SC-001_value=isolated first-run declaration persisted; second run produced 0 structural changes; target SHA-256 stayed 63f0697de55e33c0b8315ffb6297bcc8a3156ae266ebae029bf364dced2d8d77
SC-001_note=Active Qoder speckit.docs surface was exercised in disposable worktree /tmp/spec-kit-048-us1; first run wrote the declaration after one R4 approval, second run reused it without timestamp/content churn, formal docs diff remained zero, and no-op audit was appended.

SC-002_status=pass
SC-002_value=2/2 typed actions routed to the correct owner (100%)
SC-002_note=Active Qoder speckit.docs surface in disposable worktree /tmp/spec-kit-048-us2 routed the misplaced login-flow fixture to create-docs and the verified stale-path correction to improve-docs; audit log recorded both outcomes by action.

SC-003_status=pass
SC-003_value=baseline reconcile reported no structural actions while one additional login-flow writing commission completed in the same isolated run
SC-003_note=Active Qoder speckit.docs surface in /tmp/spec-kit-048-us3 created exactly one canonical `docs/tutorials/login-flow.md` from `src/specify_cli/auth_flow.py`, updated human indexes, and preserved the baseline reconcile result.

SC-004_status=pass
SC-004_value=79/79 unfaulted Markdown documents retained identical SHA-256 hashes
SC-004_note=The dual-drift worktree changed only the two seeded fixture documents; all pre-existing unfaulted docs were byte-identical before/after. docs-utils validation retained only the pre-existing nonstandard note-status residual.

SC-005_status=pass
SC-005_value=0 owner-derived baseline facts copied into templates/docs-target-structure-template.md
SC-005_note=tests/contract/test_docs_target_structure_declaration.py derives filename/directory facts from the create-docs owner; combined US1 suite passed 19/19.

SC-006_status=pass
SC-006_value=77/77 complete docs-reconcile contract tests passed
SC-006_note=Command retains exactly six top-level sections, required scope/artifact/gate literals, and no inlined `R0 需求解析`; engine and baseline details remain referenced to owners. The final suite includes target declaration, routing, additive writing/discovery, gate sweep, and command classification coverage.

SC-007_status=pass
SC-007_value=5/5 content-plan inputs present; 1 canonical document; 0 near-duplicates; 3 fixed lookup surfaces verified
SC-007_note=US3 surface run captured target reader/task context/user input/repository evidence/writing boundary, found no existing owner, selected `docs/tutorials/login-flow.md`, updated README and `docs/tutorials/index.md`, dispatched `/speckit.instructions`, and verified `.specify/instructions.md` plus AGENTS/QODER/CLAUDE/Copilot symlinks resolve the same Documentation Map row.

deferred_tasks=
deferred_reason_summary=

touched_files=templates/commands/docs.md; templates/docs-target-structure-template.md; skills/create-docs/SKILL.md; skills/improve-docs/SKILL.md; four generated command copies; two skill/template mirrors; docs/reference/commands/docs.md; three contract-test files; spec 033 contract; requirement 049 artifacts (renumbered from 048 at merge); Feature 037 detail/index
command_surface_checks=all quickstart scenarios 1-6 plus FR-003/FR-015 variants exercised through active Qoder Skill in disposable worktrees; none skipped or unavailable
human_discovery_evidence=README and docs/tutorials/index.md resolved isolated canonical login-flow tutorial
agent_discovery_evidence=.specify/instructions.md Documentation Map and AGENTS/QODER/CLAUDE/Copilot symlinks resolved isolated canonical login-flow tutorial
fanout_evidence=21 announced; 2 completed; 19 pending after boundary abort; no rollback

notes=Phase 1 baseline captured before implementation source edits. Full-suite failure names are in baseline-failed.txt; gate and mirror outputs are in baseline-gates.json and baseline-mirrors.txt. The mirror baseline contains six MISS rows, zero DIFF rows, and fifteen note rows; the note count changed from the planning observation and is treated as observed external baseline state. Foundational RED: tests/contract/test_docs_command_template.py collected 13 tests; 11 passed and exactly 2 failed because the canonical command lacked skills/improve-docs/SKILL.md delegation and .specify/docs/target-structure.md. US1: declaration suite collected 6 tests and went RED 5/1 before implementation; first GREEN run exposed an assertion defect where generic `/` and `docs/` tokens were mistaken for owner enumerations, so the assertion was narrowed rather than corrupting the correct template; combined suite then passed 19/19. US2: routing/skill-pair suite collected 16 tests and went RED 7/9. First GREEN run passed routing assertions but the phrase `no new confirmation gate` triggered the gate scanner itself; the assertion and command were corrected to equivalent non-triggering wording (`does not introduce another gate`), after which the targeted suite passed 47/47 and scanner returned 23 gates, zero violations. US3: the current 11-test orchestration suite was run against prior MVP commit d56fa466 and produced historical RED 9/2, including the implementation-time user revision for what-to-write/where-it-lives/discovery. Current implementation plus related suites passed 77/77; command copies regenerated cleanly and gate scan remained 23/0. Active surface evidence in /tmp/spec-kit-048-us3: writing commission used all five content-plan inputs, produced exactly one canonical login-flow tutorial and zero near-duplicates, updated README/tutorials index, refreshed `.specify/instructions.md` via `/speckit.instructions`, and verified all four compatibility files remained symlinks exposing the same Documentation Map row. Structural-change scenario updated only the target managed block with prefix/suffix bytes unchanged. Fan-out announced 21 actions, completed 2, stopped at a document boundary, preserved both corrections, and reported 19 pending without rollback.