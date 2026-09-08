# Verification Log — 050-proactive-flow-trigger

<!--
  Populated during the /speckit.implement run per .specify/templates/verification-log-template.md.
  Shape is key=value + per-SC three-field rows so /speckit.review, /speckit.analyze and CI can
  derive pass-rates programmatically without grepping prose.
  status ∈ {pass | fail | partial | deferred | unknown}. `unknown` = producing task not yet run.
-->

# -- Baseline (recorded once, BEFORE any /speckit.implement work changed the tree) --

baseline_commit=c3bc955d
baseline_date=2026-09-08
baseline_branch=050-proactive-flow-trigger

# Counters frozen by T002 into baseline-gates.json; restated here so the SC rows
# below have their comparison values in one place.
baseline_confirmation_gates_total=23
baseline_confirmation_gates_violations=0
baseline_gate_budget_cap=23.25
baseline_gate_integer_headroom=0
baseline_probe_internal_objects=73
baseline_probe_external_objects=0
baseline_complex_commands=19
baseline_simple_commands=4
baseline_docs_step_injections=16
baseline_suite_failed=42
baseline_suite_passed=2496
baseline_suite_skipped=1
baseline_instructions_h2_sections=15
baseline_instructions_symlinks_created=6
baseline_declared_agent_paths=5
baseline_hermes_path_generated=no
baseline_opencode_path_generated=no
baseline_check_instructions_passing_keys=4
baseline_seed_anchor_verified=0

# -- /speckit.implement results --

implementation_date=2026-09-08
post_change_commit=61813fbf

post_change_confirmation_gates_total=23
post_change_confirmation_gates_violations=0
post_change_probe_internal_objects=73
post_change_complex_commands=19
post_change_simple_commands=4
post_change_docs_step_injections=16
post_change_instructions_h2_sections=16
post_change_instructions_symlinks_created=8
post_change_hermes_path_generated=yes
post_change_opencode_path_generated=yes
post_change_check_instructions_passing_keys=6
post_change_seed_anchor_verified=13

# -- Run notes --

notes=T013 found and corrected a quickstart scenario-1 premise defect: `specify init` never writes .specify/instructions.md nor any symlink (src/specify_cli/__init__.py has no generator call; its line 985 mention is only a _CORE_SPECIFY_ASSETS preservation entry). The real pipeline is two steps (init then /speckit.instructions). Scenario 1 was amended and re-run green; the defect was in the verification premise, not in the implementation.
notes=Phases 5 walkthroughs (T036) were executed by three delegated subagents working in independent mktemp roots; each returned measured readings and each independently confirmed the repo stayed clean and no .specify/memory/trigger/ appeared in it (the two-hats path-resolution trap). Their evidence is transcribed verbatim into the SC rows below.
notes=Mid-run governance change landed as its own commit (61813fbf), NOT inside feature 050: a new Ask/Record/Repeat philosophy doc plus a reachable Two Hats ambient section, prompted by the reachability gap that the resolve_root defect exposed. Feature 050's positional contract (trigger section immediately after Documentation Map) was re-asserted green after that change.
notes=One regression-suite failure during Phase 2 was attributed to EXTERNAL provenance (a parallel session scaffolding git-ignored .specify/skills/.migration-backups/layout-int-* dirs). Evidence and reasoning recorded in baseline-gates.json `externalAttribution` and in baseline-failed.txt's header. The assertion was NOT loosened and the dirs were NOT deleted.

# -- Success Criteria (all 15, seeded per template instruction) --

SC-001_status=pass
SC-001_value=8/8 agent instruction paths created and resolving to .specify/instructions.md; 6/6 _check_instructions tool keys pass; divergent copies = 0
SC-001_note=Produced by T013 (automated) + T015 (manual walkthrough of quickstart scenario 1). Fresh mktemp root, `specify init --here --ai qoder --force --ignore-agent-tools` then the root's own shipped `.specify/scripts/bash/generate-instructions.sh`. All of CLAUDE.md, AGENTS.md, HERMES.md, .github/copilot-instructions.md, .opencode/instructions.md, QODER.md, .qoder/project_rules.md, .claude/project_rules.md are symlinks whose realpath is the one canonical .specify/instructions.md, so semantic sameness is structural (one file, eight links) rather than a content comparison — divergent copies cannot exist. Each of the 8 read through its link reports heading=1 pointer=1. Regression: before T011 HERMES.md and .opencode/instructions.md were MISS and hermes/opencode returned `fail`; both now pass. The shipped discipline doc is byte-identical to the working-tree source. Pinned by trigger-section.md C-1/C-10/C-12 (tests/contract/test_proactive_trigger_section.py, 16 tests green with the existing propagation guard).

SC-002_status=pass
SC-002_value=0 enumeration copies (0 command names of 25, 0 skill names of 34, 0 `skills/` paths, 0 parameter structures)
SC-002_note=Produced by T015 via cross-text check against the authoritative rosters, and pinned by trigger-section.md C-5. Rosters were derived, not assumed: 25 command names from templates/commands/*.md and 34 skill directory names from skills/. All three surfaces checked (templates/instructions-template.md, its .specify mirror, and the regenerated live .specify/instructions.md) — each reports 0 hits for every command name, 0 for every skill name, 0 for `skills/`, and 0 for the closed parameter-pattern set (`--<long-option>`, `$ARGUMENTS`, `<placeholder>`). Section body is 9 lines (limit 25) with 0 `### ` subheadings, so nothing is hidden in a subsection that additive reconcile would fail to propagate. Invocation forms are supplied by the engine at runtime, never enumerated in the instructions file.

SC-003_status=pass
SC-003_value=15/15 states correct = 100.0% accuracy (target >=90%); 14/14 suggestions carried an exact copy-ready invocation = 100%; command names the user had to recall = 0
SC-003_note=Produced by T028 on a cold-start mktemp root. The required >=6 lifecycle states were covered 15 times over — the full named-situation set plus the no-match case: only-requirements->s02 /speckit.plan; unresolved-clarification->s01 /speckit.clarify; clarified-unplanned->s02; plan-ready-no-tasks->s04 /speckit.tasks; tasks-ready+checklist-absent->s05 /speckit.checklist; tasks-ready+open-tasks->s06 /speckit.implement; implementing->s07 /speckit.analyze; implemented+deferred->s08 /speckit.review; no-feature-index->s03 /speckit.feature; no-constitution->s13 /speckit.constitution; feedback-threshold->s09 /speckit.feedback package; introspection-pending->s10 /speckit.feedback introspect; docs-drift->s11 /speckit.docs; instructions-stale->s12 /speckit.instructions; and unrelated-turn->no situation, no suggestion. Human correctness judgement: every resolved situationId and every suggested flow matched the intended next step for its state, including the two deliberately-confusable pairs (s05 vs s06 by checklist-absent, s03 vs s13 by which registry is absent). Note the s05/s06 pair exercised V1.6 most-specific-first: passing both open-tasks and checklist-absent resolved to s05, passing only open-tasks resolved to s06.

SC-004_status=pass
SC-004_value=irrelevant suggestions over 20 unrelated turns = 0; repeat suggestions within one session after the first = 0
SC-004_note=Part 1 produced by T028 (quickstart scenario 3): 20 fresh-session turns at `--stage non-feature` with no signals produced 0 suggestions, and status reported suggested=0 / visibleOutputCount=0 / escalated=0 over turns=20. Part 2 produced by T028 and pinned by trigger-engine.md C-20: five consecutive turns in ONE session on an unchanged state produced a suggestion on turn 1 and `payload.suppressed=true` with suggestion=null on turns 2-5, so the repeat count is 0. The suppression is structural (session-keyed lastSuggestion compared on situationId AND ruleId), not a rate limit, which is what makes the zero reproducible rather than incidental.

SC-005_status=pass
SC-005_value=destructive rule r-006: promoted=false and autoExecute=false on 10/10 consecutive acceptances (measured at 10, stronger than the >=5 floor); reversible control r-001 promoted on turn 3 and returned autoExecute=true on turn 4
SC-005_note=Produced by T036 deliverable 1 (quickstart scenario 4), executed by a delegated subagent in an independent mktemp root. r-006 was accepted across 10 distinct sessions sd1-sd10, all resolving situationId s06 with suppressed=false, so all 10 were genuine hits rather than suppressed no-ops. After every turn: promotion.promoted=false, state=active, destructiveExempt=true, and that turn's assess returned autoExecute=false. Final state confirmationClass="destructive" (never recomputed by the engine), promotion={consecutive:10, threshold:3, promoted:false}, stats={hits:10, accepted:10}, promoted rules in the index = []. The CONTROL is what makes this meaningful: the reversible r-001 accepted on sr1-sr3 went consecutive 1->2->3, promoted=true, state=promoted on turn 3, and the next hit sr4 returned autoExecute=true. Without that control a constant-false bug would look identical to a correct safety guard. Zero-tolerance criterion met. Also pinned by trigger-engine.md C-17 in both tests/contract/test_trigger_engine.py and tests/integration/test_trigger_promotion.py.

SC-006_status=pass
SC-006_value=part 1: consecutive 2->0 on a single decline, promoted false, state active, resetBy resolves to a real stored eventId. part 2: index.json byte-identical across a real generate-instructions.sh run (sha256 12cf771d...bb08cc both sides)
SC-006_note=Part 1 produced by T036 deliverable 2: consecutive=2 before, 0 after one declined response; promotion.resetBy=20260908T084921Z-03 was confirmed present in index.json events[] (3 events) and to reference the actual declined event (ruleId r-001, situationId s01, response declined) — so the reset is traceable, not just a zeroed counter. A supplementary run demoted a genuinely PROMOTED r-001: consecutive 3->0, promoted true->false, state promoted->active, resetBy present among 14 events. Part 2 produced by T036 deliverable 3, the half no earlier task covered: after promoting r-001 (consecutive=3, promoted=true, state=promoted, 3 events), the workspace was made to look like an installed project and the repo's real `scripts/bash/generate-instructions.sh` was executed inside it (exit 0). index.json sha256 was identical before and after, diff -q and cmp both reported byte-identical, and index.json's mtime (16:51:40.483) predated the generator run (16:51:49) — direct proof the generator never wrote the trigger store. Post-run r-001 still consecutive=3/promoted=true/state=promoted with 3 events. This is the mechanism-level guarantee behind FR-018's "the off state survives regeneration": instructions and learning state are separate surfaces.

SC-007_status=unknown
SC-007_value=
SC-007_note=Producing task T043 (US4 manual walkthrough, quickstart scenario 6) not yet run — Phase 6.

SC-008_status=unknown
SC-008_value=part 1 measured green at every phase boundary so far: gate total 23, violations 0, cap 23.25
SC-008_note=Producing task T050 (part 2: count of events where a suggestion blocked or deferred the user's current request) not yet run. Part 1 — new gate-scan violations = 0 and total within the existing contract cap — has held at every phase boundary and after the mid-run governance change (total 23 == the T002 frozen value, violations 0, cap 23.25 from the 044 baseline x 25%, integer headroom 0). The row stays open until T050 lands the intrusion half.

SC-009_status=pass
SC-009_value=suggestions produced while disabled = 0/5; auto-executions while disabled = 0/5; still 0/5 after a second generate-instructions.sh run; config.enabled still false post-regeneration
SC-009_note=Produced by T036 deliverable 4, deliberately sequenced AFTER r-001 had been promoted — that ordering is what makes the test meaningful, since a promoted rule is exactly the case where "it was approved before" could wrongly keep auto-executing. `config --enabled false` reported changed=["enabled=False"] while promotedRules still listed ["r-001"], i.e. the promotion survived but was inert. Five fresh-session turns sg1-sg5 that would otherwise hit r-001 all returned enabled=false, situationId=null, suggestion=null; r-001's hits stayed at 3, confirming no phantom assessments. The generator was then re-run and five further turns sg6-sg10 again produced 0 suggestions and 0 auto-executions, with config.enabled still false and index.json byte-identical (sha256 73da4d62...). Both halves of FR-018 met: no suggestions and no auto-execution, and the off state is not overwritten by instructions regeneration. Pinned by tests/integration/test_trigger_promotion.py.

SC-010_status=pass
SC-010_value=all three breakages: exit code 0, zero-byte stderr with no traceback, ok=true, warnings=["state-unreadable"], payload.degraded="suggest-only", rule set rebuilt from seed at 13 rules with every promotion.consecutive=0; session interruptions = 0
SC-010_note=Produced by T036 deliverable 5, the three-state degradation walkthrough no earlier task covered. Breakages constructed independently: (1) index.json deleted; (2) index.json overwritten with the literal `{not json`; (3) schemaVersion rewritten 1 -> 999999 as valid JSON. Each workspace was first init-ed AND given one normal turn plus an accepted record, leaving promotion.consecutive=1 — so the observed reset to 0 is a genuine reset rather than a trivially-zero fresh state, which is the detail that makes this evidence rather than a tautology. Under all three the degraded assess still resolved situationId=s01 and returned a full suggestion for r-001 (/speckit.clarify), so the mechanism kept working in suggest-only mode instead of going dark. Telemetry was still appended (2 rows, the degraded turn's row carrying assessed=true), so the measurement denominator survives degradation too. Session continuity: immediately after the degraded call a fresh-session assess returned exit 0, ok=true, warnings=[] with no degraded key and a full suggestion — the mechanism self-recovered and the session was never interrupted. Zero-tolerance on session interruption met. Pinned by trigger-engine.md C-8 (three parametrized cases) in tests/contract/test_trigger_engine.py.

SC-011_status=partial
SC-011_value=constructed measurement over 20 turns: escalationPct 0.0% <= probeBudgetPct 20%, budgetOver=false, visibleOutputCount=0, suggested=0, turns=20, rows=20. Separate 10-turn probe run: escalated=2, escalationPct=20.0 == 2/10*100, turns=10 distinct from rows=15
SC-011_note=The mechanical half is measured and passes: T028's 20 fresh-session unrelated turns gave escalation rate 0.0% against the 20% budget with 0 visible output, and T036 deliverable F confirmed the ratio arithmetic (2 escalations over 10 session turns = 20.0%, budgetOver=false at exactly the budget) and that `turns` (session-scoped) is genuinely distinct from `rows` (window-bounded file) — 10 vs 15 in a mixed workspace. Marked PARTIAL rather than pass because SC-011 specifies "a continuous stretch of >=20 turns of ORDINARY WORK", and every turn measured so far was constructed for the walkthrough, not ordinary work. T050's dogfood run is the named producer of the live-session half and has not run. DENOMINATOR CAVEAT recorded honestly per data-model.md V4.5: telemetry rows are written only when assess is called, so the denominator is assessment invocations, not raw user turns — a turn whose assessment was skipped entirely leaves no trace and therefore cannot be counted. This metric cannot prove that every turn was assessed; that half needs session-side observation.

SC-012_status=pass
SC-012_value=suggestions emitted before compliance declaration = 0 when --compliance-done is passed; omitting the flag reports errors=["ordering-violation"] and the telemetry row still records suggested=true with complianceDone=false
SC-012_note=Produced by T028. The ordering contract is measurable rather than aspirational because the engine refuses to infer it: assess WITHOUT --compliance-done returned errors=["ordering-violation"], and the same call WITH the flag returned errors=[] — while both still produced their suggestion and their telemetry row, so the violation is reported honestly instead of suppressing the turn. Rows where a declared-compliant turn still violated: 0. The single-pass ("同一趟") half is structural rather than telemetry-observable: the trigger section sits in the instructions template immediately after the Documentation Map resident directive and immediately before `## Fact, Correctness & Logic Checks (Input Sanity)`, which is asserted positionally by trigger-section.md C-3 (tests/contract/test_proactive_trigger_section.py) and re-asserted after the mid-run governance change added two later sections. One analysis pass, compliance first, flow selection continuing in it. T050 will add the live-session confirmation.

SC-013_status=pass
SC-013_value=13/13 seed rules locatable in existing framework text = 100% (11 via anchorKind=handoffs, 2 via owning-section); cold-start first-day suggestion produced with 0 accumulated learning records
SC-013_note=Provenance half produced by T003 (mechanical pre-flight before the seed was written) and re-proved by T019's own self-check plus tests/contract/test_trigger_seed_derivation.py C-6/C-7: for all 13 rules the provenance.file exists, the anchor section exists, the quote is a verbatim whitespace-normalized substring of it, and the rule's flow name still appears in it. Breakdown by FR-022's two source classes: 11 handoffs-kind (requirements.md x3, clarify.md, tasks.md, checklist.md, implement.md x2, sanitize.md, docs.md, feature.md) and 2 owning-section (shared/workflow/feedback-step.md Threshold prompt protocol; templates/commands/feedback.md Outline). Cold-start half produced by T028 on a fresh mktemp root: init reported 13 rules / 13 situations / learned=0 / accumulated_hits=0 with default config, and the very first assess on a brand-new project returned a complete suggestion (/speckit.clarify, situationId s01, autoExecute=false) with a rationale — first-day value with zero learning history, which is what FR-022 requires. T043 will add the drift-detection controlled experiment (6a).

SC-014_status=pass
SC-014_value=100% agreement — 21 independent sessions across 3 constructed states, each resolving to exactly 1 distinct situationId
SC-014_note=Produced by T028, exceeding the >=5-session requirement. Three states were each assessed in 7 independent sessions (distinct session identifiers, so no session-level suppression could carry an answer over): requirements-unclear+needs-clarification resolved to s01 in 7/7; tasks-ready+open-tasks resolved to s06 in 7/7; non-feature with no signals resolved to no situation in 7/7 (the correct answer, not a failure). 21 sessions total, 1 distinct identity per state, so the agreement rate is 100%. This is the precondition for FR-010's consecutive counting being well defined — if the same state could resolve differently across sessions the counter would be counting noise. The anti-pattern discriminator also holds by construction: identity is derived from the coarse (stage, signals) pair against a closed 13-entry vocabulary, never from an artifact state fingerprint, so the promotion trigger rate is not structurally pinned at 0. Pinned by trigger-engine.md C-12 (test_c12_resolution_is_repeatable).

SC-015_status=pass
SC-015_value=append-then-truncate invariant held on 60/60 appends at window 50 (max observed 50, never exceeded); rule set byte-identical across rotation (sha256 975c7f80...30cfd7 both sides); consecutive survived a shrink to window 1; rotate left index.json byte-identical (sha256 7cf0ba03...5c50e4)
SC-015_note=Produced by T036 deliverable 6 (quickstart scenario 5). Part A is the half that distinguishes a real invariant from a cleanup routine: with window 50, the file was measured after EVERY one of 60 fresh-session appends and the maximum observed at any point was 50 — counts rose 1..50 through turn 50 then pinned at 50 for turns 51-60. Bounding therefore holds after each append, not merely after an explicit rotate; a design that only trimmed on rotate would pass part B and fail here. Part B: rotate reported rowsBefore=50 rowsAfter=50 window=50 indexTouched=false. Part C is the zero-loss discriminator: r-001 was first genuinely promoted (consecutive 1->2->3, promoted=true, state=promoted, 3 events), the rule set was captured, then 60 more turns plus rotate, and the recaptured rule set was byte-identical (same sha256, sorted-key dump so ordering could not mask a difference) with r-001 still consecutive=3/promoted=true/state=promoted and 3 events. Any difference would have meant promotion counters were recomputed from telemetry rows — the exact defect this criterion exists to catch. Part D: shrinking to window 1 truncated telemetry to 1 line while r-001 kept consecutive=3 and state=promoted. Part E: rotate left index.json byte-identical, not even the `updated` timestamp moving, confirming V4.4 (rotate never writes the index). Pinned by tests/integration/test_trigger_telemetry.py.
