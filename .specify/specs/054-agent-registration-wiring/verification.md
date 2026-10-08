# Verification Log — 054-agent-registration-wiring

feature=044 Agent Metadata Portability
requirement=054-agent-registration-wiring
implemented=2026-10-08
commits=3e673e16,38c19d1e,b95b5818,fb3432e9,77e041cb,d58a600e,219811cd(review report),7267c46a(user-side sweep of demo artifacts + feedback ledger),b4f2b8cb(review roadmap fixes; carries this file — resolve the landing commit via `git log -- <spec-dir>/verification.md`)
baseline=49 pre-existing failed (captured 2026-10-08, name-level, baseline-failed.txt)
regression=comm -13 baseline current → empty at every phase boundary (Phases 2,3,4,5,6) and at the post-review re-check; final full-suite summary 2026-10-08 (post-review re-run, verbatim): `49 failed, 2609 passed, 2 skipped in 59.03s` — the 49 == the pre-existing baseline set, name-compared via comm -13 (empty)
gate_rejections=0
deferred_tasks=none

SC-001_status=pass
SC-001_value=0 hits (target 0; baseline 3 surfaces: agents.md:25 + SKILL.md:122/:127, plus 4 tool copies carried STR-001)
SC-001_note=Measured 2026-10-08: grep of both retired literal classes over source+mirrors+4 tool copies returns 0 everywhere (real output pasted in notes/quickstart-run.md); pinned by tests/contract/test_teaching_surfaces.py (11/11) with a 1-char mutation drill recorded in notes/red-first-evidence.md. F-A02 dead letter (2026-09-11, spread across three surfaces) is now closed on the code side.

SC-002_status=pass
SC-002_value=dogfood-executor seat: instantiated (placeholders resolved, team-scope set) → rendered (`rendered 3 agent(s) for qoder`, exit 0) → dispatched by registered-type semantics; seat task returned success; general-purpose carrier not used
SC-002_note=Per the Source row's named evidence form (host directory listing + dispatch record): run report .specify/teams/demo-seat-dispatch/runs/20261008T214100Z-report.md (seat dispatch surface, §1 build → §2 render trigger with real output → §3 dispatch record) + seat result 20261008T214100Z-seat-result.md (success, capacity fields verified by the dispatched seat itself). Fixture-level runtime also guarded by test_agent_chain_guards.py test_c9; wiring by test_seat_instantiation_flow.py (6/6). Honest boundary recorded in the run report: this orchestrating session's native type set predates the render, so the seat was dispatched in the external-equivalent form with the registered capacity declared in the dispatch header; native-type dispatch becomes the default in the next session (the registered type now exists in .qoder/agents/).

SC-003_status=pass
SC-003_value=manifest entry set == neutral-layer definition set (glob-derived, no hand list); foreign user files neither in manifest nor pruned
SC-003_note=tests/contract/test_agent_chain_guards.py test_c10 (correspondence) + foreign-file edge case; source-prefix mutation drill → guard red → byte-equal restore (notes/red-first-evidence.md). Scope: framework-rendered products only (render manifest), per the clarified SC-003.

SC-004_status=pass
SC-004_value=3 surfaces fixed, guards pinned, ledger closure actionable
SC-004_note=F-A02 closure conditions met: teaching surfaces corrected (T010/T011/T012), absence guards landed with mutation-drill evidence (T013), contract test suite green (35/35 across five guard files). The ledger closure action (marking the 2026-09-11 consume-log routing resolved in the feedback store) is consumption-side and actionable now — this row records the condition is met.

notes=Design rulings from /speckit.clarify (2026-10-08) all landed as planned: ruling (b) seat instantiation at team creation (FR-007), direct render-trigger execution in the create flow (FR-004), modify-time opt-in backfill (FR-014, improve-team), host-registration-surface concept owned in agent-definitions.md (FR-009). New CLI surface: `specify render-agents --ai <tool>` (render-mode tools only; annotated tools rejected with legal values). New neutral key: `team-scope` (framework-only, seat provenance, never rendered). Mid-run disclosures: T022 supported-agent-tools insert initially broke the Tier-1 sentence (caught by re-read, relocated, disclosed); chain-guard first drill form (suffix-append) was invisible to substring assertions — re-drilled with the deletion form, finding recorded.
