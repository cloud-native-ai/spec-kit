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
post_change_commit=PENDING_FINAL

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
notes=T044/DoD-8 correction C-1: `.specify/memory/tools.md` is NOT a regenerated inventory (nothing in the repo writes it; it is a 1984-line MCP index born with three placeholder sections in 15b13dba), and `refresh-tools.sh --json` exits 1 because it requires a source flag. The Tool record and `.specify/tools/*.json` regeneration were completed; the tools.md clause is VOID, not skipped. The same false claim is repeated in seven framework surfaces and is reported for a separate fix. See tasks.md §Implementation-Period Corrections C-1.
notes=Phase 6/7 walkthroughs were delegated: the drift-detection controlled experiment (T043 6a / T045) ran in a throwaway `git worktree` at /tmp/drift-exp so the live repo's command templates were never modified, and was removed afterwards; the Tool record (T044) was authored by a subagent that ran the mechanical write gate first and checked for brittle count assertions before adding a file.
notes=Mid-run governance change landed as its own commit (61813fbf), NOT inside feature 050: a new Ask/Record/Repeat philosophy doc plus a reachable Two Hats ambient section, prompted by the reachability gap that the resolve_root defect exposed. Feature 050's positional contract (trigger section immediately after Documentation Map) was re-asserted green after that change.
notes=One regression-suite failure during Phase 2 was attributed to EXTERNAL provenance (a parallel session scaffolding git-ignored .specify/skills/.migration-backups/layout-int-* dirs). Evidence and reasoning recorded in baseline-gates.json `externalAttribution` and in baseline-failed.txt's header. The assertion was NOT loosened and the dirs were NOT deleted.

# -- Deferred task registry (Pre-Status-Flip Gate item 4) --

deferred_tasks=T050
deferred_T050_reason=requires >=20 turns of ordinary work with the mechanism live; this session was building the mechanism, so its turns are not genuine samples. 3 real turns were recorded and yielded live evidence for SC-004(2) suppression, 0 ordering-violations, 0 silence-violations, 0.0% escalation, and the V6.9 tracking boundary.
deferred_SCs=SC-008 (part 2 only), SC-011

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
SC-004_value=irrelevant suggestions over 20 unrelated turns = 0; repeat suggestions within one session after the first = 0; confirmed live: dogfood turns 2 and 3 suppressed after turn 1 suggested
SC-004_note=Part 1 produced by T028 (quickstart scenario 3): 20 fresh-session turns at `--stage non-feature` with no signals produced 0 suggestions, and status reported suggested=0 / visibleOutputCount=0 / escalated=0 over turns=20. Part 2 produced by T028 and pinned by trigger-engine.md C-20: five consecutive turns in ONE session on an unchanged state produced a suggestion on turn 1 and `payload.suppressed=true` with suggestion=null on turns 2-5, so the repeat count is 0. The suppression is structural (session-keyed lastSuggestion compared on situationId AND ruleId), not a rate limit, which is what makes the zero reproducible rather than incidental. LIVE CONFIRMATION (T050 dogfood, this repository's own store): turn simp050-01 suggested s07/r-007 with visibleOutput=true; turns simp050-02 and simp050-03, same session and unchanged state, both recorded suggested=false and visibleOutput=false. The mechanism suppressed its own repeat advice during the very session that built it.


SC-005_status=pass
SC-005_value=destructive rule r-006: promoted=false and autoExecute=false on 10/10 consecutive acceptances (measured at 10, stronger than the >=5 floor); reversible control r-001 promoted on turn 3 and returned autoExecute=true on turn 4
SC-005_note=Produced by T036 deliverable 1 (quickstart scenario 4), executed by a delegated subagent in an independent mktemp root. r-006 was accepted across 10 distinct sessions sd1-sd10, all resolving situationId s06 with suppressed=false, so all 10 were genuine hits rather than suppressed no-ops. After every turn: promotion.promoted=false, state=active, destructiveExempt=true, and that turn's assess returned autoExecute=false. Final state confirmationClass="destructive" (never recomputed by the engine), promotion={consecutive:10, threshold:3, promoted:false}, stats={hits:10, accepted:10}, promoted rules in the index = []. The CONTROL is what makes this meaningful: the reversible r-001 accepted on sr1-sr3 went consecutive 1->2->3, promoted=true, state=promoted on turn 3, and the next hit sr4 returned autoExecute=true. Without that control a constant-false bug would look identical to a correct safety guard. Zero-tolerance criterion met. Also pinned by trigger-engine.md C-17 in both tests/contract/test_trigger_engine.py and tests/integration/test_trigger_promotion.py.

SC-006_status=pass
SC-006_value=part 1: consecutive 2->0 on a single decline, promoted false, state active, resetBy resolves to a real stored eventId. part 2: index.json byte-identical across a real generate-instructions.sh run (sha256 12cf771d...bb08cc both sides)
SC-006_note=Part 1 produced by T036 deliverable 2: consecutive=2 before, 0 after one declined response; promotion.resetBy=20260908T084921Z-03 was confirmed present in index.json events[] (3 events) and to reference the actual declined event (ruleId r-001, situationId s01, response declined) — so the reset is traceable, not just a zeroed counter. A supplementary run demoted a genuinely PROMOTED r-001: consecutive 3->0, promoted true->false, state promoted->active, resetBy present among 14 events. Part 2 produced by T036 deliverable 3, the half no earlier task covered: after promoting r-001 (consecutive=3, promoted=true, state=promoted, 3 events), the workspace was made to look like an installed project and the repo's real `scripts/bash/generate-instructions.sh` was executed inside it (exit 0). index.json sha256 was identical before and after, diff -q and cmp both reported byte-identical, and index.json's mtime (16:51:40.483) predated the generator run (16:51:49) — direct proof the generator never wrote the trigger store. Post-run r-001 still consecutive=3/promoted=true/state=promoted with 3 events. This is the mechanism-level guarantee behind FR-018's "the off state survives regeneration": instructions and learning state are separate surfaces.

SC-007_status=pass
SC-007_value=identification hit rate 2/2 = 100% (high-decline rule AND missed situation both identified, each with metric+value+sampleSize); rule-set changes without approval = 0; under-sampled rules wrongly proposed = 0
SC-007_note=Produced by T043 (quickstart scenario 6), run as a real walkthrough on a scratch root. 6b injected a noisy rule: r-001 declined on 6 fresh sessions giving declineRate 1.0, which tune identified as p-001 kind=suppress with evidence {metric:declineRate, value:1.0, sampleSize:6}. 6c injected a missed-suggestion history: /speckit.history invoked by hand twice on turns whose telemetry showed suggested=false, identified as p-002 kind=add-rule with evidence {metric:missedInvocations, value:2, sampleSize:2}. Both identifications carry evidence and sample size, so the 100% hit rate is on evidence-bearing proposals, not bare detections. FR-016 zero-change: capturing `rules --format json` before and after a tune run compared NOT equal=False — tune alone changed nothing. 6e approval chain: `tune-apply --proposal p-001 --reason ...` moved SM-2 to state=applied with ratifiedAt, appliedAt and reason all populated, wrote rule tuning {ratifiedAt, evidenceRef=p-001#declineRate, suppressedBy=p-001}, set rule state=suppressed, and a subsequent assess on that situation returned 'no suggestion (no-active-rule)' — the write-back took real effect. Small-sample guard (third clause): r-002 given only 2 declines (hits=2 < minSample=5) at the SAME declineRate 1.0 was NOT proposed and was named in notes as 'small-sample guard: r-002 skipped (hits=2 < minSample=5)'; re-running with --min-sample 2 DID propose it, which is the discriminator proving the guard rather than the evidence was the blocker. Judgement stayed with the agent: semanticJudgmentPending carried 2 items ('adopt suppress for r-001?', 'which situation should /speckit.history bind to?'). 6a drift-detection half: see SC-013.


SC-008_status=deferred
SC-008_deferred_reason=needs >=20 turns of ordinary work with the mechanism live; only 3 build-session turns available (same constraint as T050)
SC-008_value=part 1 (gate budget) measured green at every boundary: total 23 == frozen 23, violations 0, cap 23.25. part 2 (blocked-or-deferred event count) = 0 observed but over only 3 dogfood turns, not a representative sample
SC-008_note=Part 1 is fully satisfied and was re-measured at every phase boundary and after the mid-run governance change: scan-confirmation-gates total 23 equals the T002 frozen value, violations 0, within the cap of 23.25 that tests/contract/test_confirmation_gates_sweep.py derives from the 044 baseline (18 assertions green). The two new shipped surfaces (the trigger section and the discipline doc) contribute zero BLOCKING_PATTERNS hits, which is what kept the integer headroom at 0 intact. Part 2 — counting events where a suggestion blocked or deferred the user's current request — is DEFERRED with T050: it needs sustained ordinary use, and only 3 dogfood turns were available in the build session. Observed 0 over those 3 turns, and the structural guarantee is strong (trigger-engine.md C-21: the engine never executes a flow, so preemption is impossible on the engine side; the agent-side yield duty is carried by discipline-doc C-12), but 3 turns is not a sample. Unblocking condition: >=20 turns of ordinary work with the mechanism live, then count blocked/deferred events.


SC-009_status=pass
SC-009_value=suggestions produced while disabled = 0/5; auto-executions while disabled = 0/5; still 0/5 after a second generate-instructions.sh run; config.enabled still false post-regeneration
SC-009_note=Produced by T036 deliverable 4, deliberately sequenced AFTER r-001 had been promoted — that ordering is what makes the test meaningful, since a promoted rule is exactly the case where "it was approved before" could wrongly keep auto-executing. `config --enabled false` reported changed=["enabled=False"] while promotedRules still listed ["r-001"], i.e. the promotion survived but was inert. Five fresh-session turns sg1-sg5 that would otherwise hit r-001 all returned enabled=false, situationId=null, suggestion=null; r-001's hits stayed at 3, confirming no phantom assessments. The generator was then re-run and five further turns sg6-sg10 again produced 0 suggestions and 0 auto-executions, with config.enabled still false and index.json byte-identical (sha256 73da4d62...). Both halves of FR-018 met: no suggestions and no auto-execution, and the off state is not overwritten by instructions regeneration. Pinned by tests/integration/test_trigger_promotion.py.

SC-010_status=pass
SC-010_value=all three breakages: exit code 0, zero-byte stderr with no traceback, ok=true, warnings=["state-unreadable"], payload.degraded="suggest-only", rule set rebuilt from seed at 13 rules with every promotion.consecutive=0; session interruptions = 0
SC-010_note=Produced by T036 deliverable 5, the three-state degradation walkthrough no earlier task covered. Breakages constructed independently: (1) index.json deleted; (2) index.json overwritten with the literal `{not json`; (3) schemaVersion rewritten 1 -> 999999 as valid JSON. Each workspace was first init-ed AND given one normal turn plus an accepted record, leaving promotion.consecutive=1 — so the observed reset to 0 is a genuine reset rather than a trivially-zero fresh state, which is the detail that makes this evidence rather than a tautology. Under all three the degraded assess still resolved situationId=s01 and returned a full suggestion for r-001 (/speckit.clarify), so the mechanism kept working in suggest-only mode instead of going dark. Telemetry was still appended (2 rows, the degraded turn's row carrying assessed=true), so the measurement denominator survives degradation too. Session continuity: immediately after the degraded call a fresh-session assess returned exit 0, ok=true, warnings=[] with no degraded key and a full suggestion — the mechanism self-recovered and the session was never interrupted. Zero-tolerance on session interruption met. Pinned by trigger-engine.md C-8 (three parametrized cases) in tests/contract/test_trigger_engine.py.

SC-011_status=deferred
SC-011_deferred_reason=the criterion specifies >=20 turns of ORDINARY work with the mechanism live; only 3 live dogfood turns were available in the build session, and the 20-turn measurement was constructed for the walkthrough rather than incidental to real work. Unblocks after >=20 ordinary turns, then read escalationPct from `status`.
SC-011_value=constructed: escalationPct 0.0% <= budget 20% over 20 turns, visibleOutputCount=0. arithmetic verified separately: escalated=2/turns=10 -> 20.0%, turns(10) != rows(15). live dogfood: 3 turns, escalated 0, escalationPct 0.0%, 1 visible output on 1 suggestion, 0 silence violations
SC-011_note=The mechanical half passes on three independent measurements. (a) T028's 20 fresh-session unrelated turns: escalation rate 0.0% against the 20% budget, visibleOutputCount 0, suggested 0. (b) T036 deliverable F confirmed the ratio arithmetic (2 escalations over 10 session turns = 20.0%, budgetOver=false at exactly the budget) and that `turns` (session-scoped) is genuinely distinct from `rows` (window-bounded file): 10 vs 15 in a mixed workspace. (c) Live dogfood in this repository's own store over 3 turns: escalated 0, escalationPct 0.0%, budgetOver false, suggested 1, visibleOutputCount 1, and 0 rows violating V4.2 (suggested=false with visibleOutput=true). Marked DEFERRED (not partial) because DoD-7 admits only pass|deferred and, more importantly, because SC-011 specifies a continuous stretch of >=20 turns of ORDINARY WORK and the live sample is 3 turns — the 20-turn measurement was constructed for the walkthrough rather than incidental to real work. T050 is the named producer of the live half and is deferred. DENOMINATOR CAVEAT recorded honestly per data-model.md V4.5: telemetry rows exist only when assess is called, so the denominator is assessment invocations, not raw user turns — a turn whose assessment was skipped leaves no trace and cannot be counted. This metric therefore cannot prove that every turn was assessed; that half requires session-side observation.


SC-012_status=pass
SC-012_value=suggestions emitted before compliance declaration = 0 when --compliance-done is passed; omitting the flag reports errors=['ordering-violation'] and the row still records suggested=true with complianceDone=false; live dogfood ordering violations = 0/3
SC-012_note=Produced by T028 and confirmed live by T050. The ordering contract is measurable rather than aspirational because the engine refuses to infer it: assess WITHOUT --compliance-done returned errors=['ordering-violation'], and the same call WITH the flag returned errors=[] — while both still produced their suggestion and their telemetry row, so the violation is reported honestly instead of suppressing the turn. Rows where a declared-compliant turn still violated: 0. Live dogfood: all 3 turns in this repository's store passed --compliance-done and 0 rows have suggested=true with complianceDone=false. The single-pass ('同一趟') half is structural rather than telemetry-observable: the trigger section sits in the instructions template immediately after the Documentation Map resident directive and immediately before `## Fact, Correctness & Logic Checks (Input Sanity)`, asserted positionally by trigger-section.md C-3 and re-asserted by test_proactive_trigger_section_position_is_undisturbed after the mid-run governance change added two later sections.


SC-013_status=pass
SC-013_value=13/13 seed rules locatable in existing framework text = 100% (11 via anchorKind=handoffs, 2 via owning-section); cold-start first-day suggestion produced with 0 accumulated learning records
SC-013_note=Provenance half produced by T003 (mechanical pre-flight before the seed was written) and re-proved by T019's own self-check plus tests/contract/test_trigger_seed_derivation.py C-6/C-7: for all 13 rules the provenance.file exists, the anchor section exists, the quote is a verbatim whitespace-normalized substring of it, and the rule's flow name still appears in it. Breakdown by FR-022's two source classes: 11 handoffs-kind (requirements.md x3, clarify.md, tasks.md, checklist.md, implement.md x2, sanitize.md, docs.md, feature.md) and 2 owning-section (shared/workflow/feedback-step.md Threshold prompt protocol; templates/commands/feedback.md Outline). Cold-start half produced by T028 on a fresh mktemp root: init reported 13 rules / 13 situations / learned=0 / accumulated_hits=0 with default config, and the very first assess on a brand-new project returned a complete suggestion (/speckit.clarify, situationId s01, autoExecute=false) with a rationale — first-day value with zero learning history, which is what FR-022 requires. T043 will add the drift-detection controlled experiment (6a).

SC-014_status=pass
SC-014_value=100% agreement — 21 independent sessions across 3 constructed states, each resolving to exactly 1 distinct situationId
SC-014_note=Produced by T028, exceeding the >=5-session requirement. Three states were each assessed in 7 independent sessions (distinct session identifiers, so no session-level suppression could carry an answer over): requirements-unclear+needs-clarification resolved to s01 in 7/7; tasks-ready+open-tasks resolved to s06 in 7/7; non-feature with no signals resolved to no situation in 7/7 (the correct answer, not a failure). 21 sessions total, 1 distinct identity per state, so the agreement rate is 100%. This is the precondition for FR-010's consecutive counting being well defined — if the same state could resolve differently across sessions the counter would be counting noise. The anti-pattern discriminator also holds by construction: identity is derived from the coarse (stage, signals) pair against a closed 13-entry vocabulary, never from an artifact state fingerprint, so the promotion trigger rate is not structurally pinned at 0. Pinned by trigger-engine.md C-12 (test_c12_resolution_is_repeatable).

SC-015_status=pass
SC-015_value=append-then-truncate invariant held on 60/60 appends at window 50 (max observed 50, never exceeded); rule set byte-identical across rotation (sha256 975c7f80...30cfd7 both sides); consecutive survived a shrink to window 1; rotate left index.json byte-identical (sha256 7cf0ba03...5c50e4)
SC-015_note=Produced by T036 deliverable 6 (quickstart scenario 5). Part A is the half that distinguishes a real invariant from a cleanup routine: with window 50, the file was measured after EVERY one of 60 fresh-session appends and the maximum observed at any point was 50 — counts rose 1..50 through turn 50 then pinned at 50 for turns 51-60. Bounding therefore holds after each append, not merely after an explicit rotate; a design that only trimmed on rotate would pass part B and fail here. Part B: rotate reported rowsBefore=50 rowsAfter=50 window=50 indexTouched=false. Part C is the zero-loss discriminator: r-001 was first genuinely promoted (consecutive 1->2->3, promoted=true, state=promoted, 3 events), the rule set was captured, then 60 more turns plus rotate, and the recaptured rule set was byte-identical (same sha256, sorted-key dump so ordering could not mask a difference) with r-001 still consecutive=3/promoted=true/state=promoted and 3 events. Any difference would have meant promotion counters were recomputed from telemetry rows — the exact defect this criterion exists to catch. Part D: shrinking to window 1 truncated telemetry to 1 line while r-001 kept consecutive=3 and state=promoted. Part E: rotate left index.json byte-identical, not even the `updated` timestamp moving, confirming V4.4 (rotate never writes the index). Pinned by tests/integration/test_trigger_telemetry.py.
