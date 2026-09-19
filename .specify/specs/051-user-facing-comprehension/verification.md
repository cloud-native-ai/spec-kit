# Verification Log — 051-user-facing-comprehension

<!--
  Populated by /speckit.implement across two runs:
    run 1 (2026-09-18) — MVP scope chosen by the user: Phase 1 Setup + Phase 2 US1 (13 of 63 tasks).
    run 2 (2026-09-18 → 2026-09-19) — the remaining 50 rows: US2, US3, US4, US5, Polish.
  This is the FINAL log: all 9 Completion Gate items were re-validated against the current tree
  (not trusted from task state) and all 9 pass, so the Pre-Status-Flip Gate was run and Feature 051
  moves Planned → Implemented. Two SCs stay `deferred` because both require reviewers who did not
  build this feature and cannot be self-administered by the implementing agent.
-->

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=925badb60860fdbbb8a5fade24cecb01627fbc6f
baseline_commit_superseded=710c7179fc1896d85b5d7d0c8ad52719af18f558
baseline_commit_superseded_reason=orphaned by the rebase onto gitlab/master; not an ancestor of HEAD, so it no longer delimits this feature's changes
baseline_date=2026-09-18
baseline_branch=051-user-facing-comprehension

# Baseline counters. Source of record: notes/pre-change-measurements.md (frozen by T001),
# which carries the command that re-derives each value.
baseline_truth_doc_count=0
baseline_guideline_count=11
baseline_template_h2_count=17
baseline_live_h2_count=18
baseline_template_guideline_pointers=7
baseline_live_guideline_pointers=8
baseline_reader_baseline_declaration_files=3
baseline_rule_sources_carrying_pointer=0
baseline_gate_total=23
baseline_gate_destructive=13
baseline_gate_governance_kept=10
baseline_contract_failed=26
baseline_contract_passed=1924
baseline_blocking_patterns=17
baseline_docs_space_counts=2/1/1/0 (interview.md / feedback.md / requirements.md / tracked files under docs/public)

# -- /speckit.implement results --

implementation_date=2026-09-19
implementation_span=2026-09-18 (Setup, US1–US4) through 2026-09-19 (US5, Polish)
post_change_commit=aa29c7116c99bd79addacfbdb122fc992e5e7356
post_change_commit_note=aa29c711 is the last implementation commit (US5, T040–T054). This log and the status flip land in the Phase 7 commit that immediately follows it, so no SHA recorded here can name its own commit. Earlier SHAs 82d95e2d and 8e634e8c were orphaned by the rebase onto gitlab/master.
post_change_scope=Phase 1 Setup + Phases 2–6 (US1–US5) + Phase 7 Polish; 60 of 63 rows closed, 3 deferred
post_change_tasks_closed=60
post_change_tasks_deferred=3
post_change_tasks_open=0

post_change_truth_doc_count=1
post_change_guideline_count=12
post_change_template_h2_count=18
post_change_live_h2_count=19
post_change_template_guideline_pointers=8
post_change_live_guideline_pointers=9
post_change_reader_baseline_declaration_files=2
post_change_rule_sources_carrying_pointer=8
post_change_gate_total=23
post_change_gate_destructive=13
post_change_gate_governance_kept=10
post_change_contract_failed=26
post_change_contract_passed=2042
post_change_blocking_patterns=17
post_change_docs_space_counts=1/0/0/0 (all three hand-written restatements fell; docs/public still 0 tracked files)

# -- Success Criteria evaluation --
# Tally: 12 pass / 4 partial / 2 deferred / 0 fail / 0 unknown.

SC-001_status=deferred
SC-001_value=0 of 13 governance-kept gates carry a wording obligation at baseline; sample review not administered
SC-001_note=Everything the review needs is in place — the truth doc's mechanical criteria (whitelist/blacklist/floor/ceiling plus the five verdict questions), and the 13 prompts enumerated in confirmation-gates.md's governance-kept list — so the sample is ready to take. The criterion is a human sampling review by a reader who has not opened the repo this session, which the implementing agent cannot supply without fabricating it.
SC-001_deferred_reason=T060 marked [~]: needs a reviewer who did not implement this feature; a single session cannot supply one. Unblocks when such a reviewer samples the 13 prompts against the mechanical criteria.

SC-002_status=partial
SC-002_value=rule decidable and landed (blacklist item 1); the one named user-facing instance converged; surface-wide count NOT asserted in CI
SC-002_note=Blacklist item 1 ("engine/script/function internal call form where a user-facing path exists") makes the violation decidable, and T041 converged the instance research named — feedback-step.md's submission notice now points at `/speckit.feedback package` rather than the raw `feedback-utils.py` path, with C-10's rewrite obligation guarding it. Measured on the 9 governed rule-source files, 6 engine-call forms remain in prose (feedback-step.md:144, clarify.md:20, reporting-playbook.md:91/305/308, glossary.md:43); all 6 sit inside agent-executed numbered steps, not inside a user-facing message, which is exactly the partition the blacklist draws. **Gap, named rather than absorbed**: SC-002's Source specifies a contract test that executes the count in CI, and no task row in tasks.md owns building it — a task-breakdown omission, not a design choice. A raw prose count is not the SC's count until a test traverses the 11-class enumeration to separate reader-facing lines from agent-facing steps.
SC-002_deferred_reason=Not deferred work but an unbuilt assertion; the follow-up is recorded below as followup_4.

SC-003_status=pass
SC-003_value=truth docs = 1 (target 1); content-form restatements under shared/ + templates/ + skills/ = 0 (target 0)
SC-003_note=Both halves measured and guarded. First half: discipline-doc C-1/C-2/C-3 green, `ls -1 shared/guidelines/*.md | wc -l` = 12 with exactly one comprehension doc, C-3 drill-proven to catch a rename. Second half: surface-pointers C-13's single-source scan is green inside the 67-case run, using needles taken from the rule bodies themselves (whitelist condition, blacklist condition, floor items, ceiling constraint, mechanical verdict questions, the seven H2 section names) and exempting only the truth doc, machine copies and test-pinned literals. C-13's needle set was re-keyed once after its first version went vacuously green against the truth doc's own brand-new phrasings — the falsifiable form was proven by measuring 2 files before convergence and 0 after (notes/red-first-evidence.md). Scope limit restated where the number is claimed: this is a literal scan, so "0" means zero literally-identifiable restatements, not all 38 researched sites individually verified — those are covered by C-6/C-9/C-10/C-11 and by T041–T049's row-level assertions.

SC-004_status=pass
SC-004_value=8 of 8 rule-source files carry exactly 1 pointer line; independent second rule copies = 0
SC-004_note=GATE-8 re-run this session prints `1` for all eight files (confirmation-gates.md, feedback-step.md, interview-pattern.md, clarify.md, requirements-guidelines.md, proactive-trigger.md, reporting-playbook.md, glossary.md). FR-016's full-batch requirement holds — no staged transition state exists. C-2 pins the confirmation-gates.md pointer to the header ownership block so one line covers classes ①②⑩⑪ instead of four per-section pointers. The two stranded implementations are resolved in the same batch: interview-pattern.md's four comprehension rules converged to a pointer while its two pattern-specific rules (`:125-126`) stay verbatim, and reporting-playbook.md §1.7's blacklist was promoted into the truth doc (see SC-014). C-12(a)/(b)/(c) supply the mechanical distinction that made `:309` decidable — a text may *refer to* the blacklist but must not *restate its category enumeration*, and the reference must carry no repo path, or C-1's "exactly one line" would turn red at the convergence point.

SC-005_status=partial
SC-005_value=both charter landing points landed and guarded; plan-template.md diff = 0 lines; downstream bootstrap drill not executed
SC-005_note=Constitution template went 11 → 13 principles (`### XII. One Source of Truth` backflowing STR-006, `### XIII. User-Facing Comprehension`), the command's MUST-include list went 5 → 7, and the live project charter took `### XV. User-Facing Comprehension` at version 1.11.0 → 1.12.0 under explicit user approval (CONFIRM-tier gate verdict). plan-template.md shows 0 changed files vs BASE_SHA, and its dynamic-enumeration instruction is intact, so both principles reach the `plan` gate's Constitution Check without any edit there — this is what makes the zero-change constraint and the "appears in the dynamic enumeration" requirement simultaneously satisfiable. What is missing is SC-005's Source: the end-to-end drill in a blank directory (init + `/speckit.constitution` + `/speckit.plan`).
SC-005_deferred_reason=The drill is quickstart scenario 5c, deferred with T034: the installed `specify` CLI is a non-editable site-packages 0.0.22, so init renders the installed package's templates rather than this tree, and reinstalling globally needs user consent. FR-026's acceptance evidence is T033's mechanical check instead.

SC-006_status=deferred
SC-006_value=judging instrument present and guarded; agreement rate not measured (needs >=20 messages across >=5 surface classes, 2 non-communicating reviewers)
SC-006_note=discipline-doc C-13 is green on the instrument: five verdict questions spanning both the jargon side and the context side, plus the explicit goal form ("two independent reviewers applying the criteria to the same message reach the same verdict; disagreement means the criteria need fixing"). The baseline this SC replaces — judgement resting entirely on reviewer intuition — is gone. The double-blind test itself is a human activity requiring two reviewers who did not build this feature.
SC-006_deferred_reason=T061 marked [~]: two independent reviewers cannot be supplied by one session, and inventing an agreement rate would violate the observation red line against fabricated numbers.

SC-007_status=partial
SC-007_value=suggestion-line form unchanged (1 insertion into proactive-trigger.md, the pointer; `## Suggestion Shape`'s one-line rule verbatim); before/after length distribution not sampled
SC-007_note=The regression this SC guards against is structurally prevented: the truth doc's ceiling section carries the single-line constraint **by path reference** ("其形态真源为 `.specify/shared/guidelines/proactive-trigger.md`,本文档只引用不复述"), so adopting the discipline adds no wording to the suggestion line. `git diff BASE --stat -- shared/guidelines/proactive-trigger.md` = `1 file changed, 1 insertion(+)`, and that insertion is the pointer GATE-8 counts, leaving `:47`'s "一条建议 = **一行非阻塞提示**" untouched. SC-008's adjudication also closes the conflict in the conservative direction: a suggestion that cannot carry its floor facts in one line is a signal the suggestion should not fire, not a reason to relax the single-line cap.
SC-007_deferred_reason=SC-007's Source additionally asks for a sampled length-distribution comparison before and after; no sampling baseline was captured pre-change, so the comparison cannot be reconstructed after the fact. Recorded rather than estimated.

SC-008_status=pass
SC-008_value=2 of 2 named conflicts adjudicated; blank surface classes = 0
SC-008_note=discipline-doc C-12 green. Both of FR-012's named conflicts carry an explicit adjudication order — floor vs the non-blocking single-line cap (different surface classes, not folded; the cap binds only class ⑥ and exempts nothing else) and floor vs summary-first — plus the accepted cost of clarify R2-Q3=A written as "length unbounded, form bounded". No class is left in a "both readings defensible" state.

SC-009_status=pass
SC-009_value=5 of 5 surfaces guarded; 96 contract cases across the four new files; neutrality and single-source assertions both present
SC-009_note=Coverage per SC-009's enumeration: truth doc (`test_user_facing_comprehension_doc.py`, C-1…C-18 + gate-neutrality), mirror parity (C-3 byte-identity on the `shared` and `skills` pairs, re-checked by GATE-2's scoped `--check`), ambient section (`test_user_facing_comprehension_section.py`, C-1…C-11), charter template and charter command MUST-include list (`test_constitution_double_landing.py`, C-1…C-13 with the named two-entry watchlist). The four files collect 67 + 10 + 19 = 96 cases, all green. Mutation-style effectiveness was demonstrated rather than assumed for the clauses where a vacuous pass was plausible: C-3 (temp renamed copy), ambient C-11 (both halves deleted in turn), C-10 (tmp_path copies with anti-vacuity assertions in both directions), C-13 (measured 2 files before convergence, 0 after). Five assertion defects were found and fixed in the double-landing test during T024 — including a missing `re.M` that made the title set silently empty, i.e. a guard that could never fail (notes/red-first-evidence.md).

SC-010_status=pass
SC-010_value=0 leaks across all three shipped surfaces under the canonical needle set
SC-010_note=Measured this session against the same `FORBIDDEN_NAMES` the tests pin (`spec-kit`, `specify-cli`, `specify_cli`, `cloud-native-ai`): truth doc 0, `templates/constitution-template.md` 0, `templates/commands/constitution.md` 0. discipline-doc C-15 and ambient-section C-9 assert it in CI. One wider ad-hoc regex (`/speckit\.`) hits `constitution.md:203`'s Handoffs line; that line predates BASE_SHA, is untouched by this feature (verified by diff), and `/speckit.*` names are the framework's own user-facing command names — deliberately outside `FORBIDDEN_NAMES`, since banning them would make every command template self-violating.

SC-011_status=pass
SC-011_value=0 new executables outside tests/contract (GATE-9 = 0)
SC-011_note=GATE-9 re-run in its stated `--name-only` form returns 0, and the stricter union form (tracked diff vs BASE_SHA ∪ `git ls-files --others --exclude-standard`, 112 changed paths total) also returns 0 outside `tests/contract/`. No jargon lint, wording scorer, maturity report generator, tracking ledger or registry was added; FR-033's design-avoidance route held. The stated form's two traps are documented in the gate row itself — `--stat` makes the extension regex match nothing, and asserting "filtered count == 0" rather than "every hit is under tests/contract/" keeps an empty result distinguishable from a pass.

SC-012_status=pass
SC-012_value=gate total 23 → 23; destructive 13 → 13; governance_kept 10 → 10; violations 0 → 0; baseline delta total -70 unchanged
SC-012_note=Scenario 3 re-run this session: both scanner invocations return character-identical numbers to the pre-change output, EXIT=0 both times. Achieved by design avoidance, not by widening the scanner — every line added inside scan scope (`shared/`, `templates/commands/`, `skills/`) was verified to carry 0 `BLOCKING_RE` hits, and gate-neutrality C-2/C-3 assert that in CI. The scanner itself is untouched: `BLOCKING_PATTERNS` 17, `POLICY_DOCS` `['shared/patterns/reconcile-pattern.md', 'shared/patterns/interview-pattern.md']`, `SELF_REL` `shared/guidelines/confirmation-gates.md` — all three verbatim as expected, including the corrected 17 (the requirements phase had mis-recorded 18). Headroom was 0 throughout (cap = 93 × 0.25 = 23.25, pinned as equality by `test_proactive_trigger_section.py`), so any single added blocking hit would have broken two contract tests at once.

SC-013_status=pass
SC-013_value=1 assertion now covers the generalized wording rule; unguarded surfaces for it = 0
SC-013_note=`test_confirmation_gates_execution_report.py` went 9 → 10 cases (all green). The added `test_doc_carries_comprehension_discipline_pointer` asserts both the header **position** (the pointer sits in the ownership block beside the existing single-line-reference rule, never inside `:7-52`'s criteria sections) and **exactly one** occurrence, closing the gap FR-034 named — the pre-existing `:44-46` case asserted only `非阻塞` and `自动传输`, never `用户视角途径`. C-4 additionally freezes all five criteria sections by SHA-256, extracted **by heading** rather than by line number so T017's insertion cannot silently move the assertion onto different text. C-5 keeps the execution-report three要素 owned by confirmation-gates.md, with the truth doc reaching it by path — the two sides of one obligation, each asserted from its own file.

SC-014_status=pass
SC-014_value=blacklist enumeration + reader-facing rewrite mapping promoted into the truth doc; independent blacklist copies = 0
SC-014_note=T046 promoted §1.7's category enumeration (tier codes, honesty/gate numbers, statistic-scope IDs, engine field names, data-layer identifiers, script names) and its rewrite mapping (`unknown-schedule` → 「无计划日期,无法判定延期」, `delayed` → 「逾期 N 天」, `progress_pct=null` → 「进度未量化」) into blacklist item ②'s instance-source block, making them framework-referenceable instead of skill-internal. The original site converged to a pointer in the same batch. C-12(c)'s count is derived from the truth doc's own category literals rather than from purpose or section names, which is what makes it falsifiable: measured **1 file / 12 hits before** the rewrite and **0 after**, recorded in notes/red-first-evidence.md. C-12's two carve-outs hold — `reporting-playbook.md:309`'s landing gate and `project-overview.md:51`'s `无内部黑话` checklist item are landing checks, not blacklist definitions, and both are preserved (the former with its parenthetical enumeration replaced by a path-free reference, per C-12(a)/(b)).

SC-015_status=pass
SC-015_value=2 of 2 watchlist principles present on both sides (100%); mutation-proven to fail on deletion from either side
SC-015_note=`DOUBLE_LANDING_WATCHLIST` carries STR-003 and STR-006; C-10 asserts each title appears in `templates/constitution-template.md`'s `### <num>. <title>` set **and** in `templates/commands/constitution.md`'s `**MUST include** a principle for "<name>"` set, matching by full title rather than by Roman numeral. Effectiveness is demonstrated on `tmp_path` copies, not assumed: deleting either principle from either side makes the clause fail, with anti-vacuity assertions in both directions so a pass cannot come from an empty set. The full-roster form (traversing every template principle) was measured as unimplementable during planning and corrected to the named watchlist under FR-035 — recorded here so the narrower scope reads as a decision, not an oversight. Baseline was 0 principles guarded and 0 hits for STR-006 in both files.

SC-016_status=pass
SC-016_value=0 regressions across all five named checkpoints; contract failure set is equal to the frozen baseline in both directions
SC-016_note=Checkpoint by checkpoint: (1) interview-pattern.md's two pattern-specific rules (`每问一决策` / `问 what 不问 whether`) remain verbatim, asserted by C-7, and the truth doc does not absorb them; (2) its embedded-contract non-droppable list now includes the pointer entry, asserted by C-8 — the list did **not** contain Comprehension rules before, so without this addition a host narrowing could legally drop the pointer; (3) clarify's existing form adjudication is unchanged (R2-Q3=A's accepted cost is written into the truth doc, not into clarify.md); (4) summarize-project still produces a compliant report — its own suite runs 118 passed with the single failure `test_summary_four_patterns.py::test_full_chain_per_pattern[serial]` confirmed present in the pre-change baseline, i.e. pre-existing and not caused by this feature; (5) scanner counts unchanged (SC-012). Suite level: `comm -13` **and** `comm -23` against `baseline-failed.txt` are both empty at 26 failed / 2042 passed, so nothing new failed and nothing healed for an unexplained reason. The three related existing suites SC-016's Source names (`test_confirmation_gates_*`, `test_scan_confirmation_gates`, `test_instructions_section_propagation`) are inside that set and green.

SC-017_status=pass
SC-017_value=dangling pointers = 0 on both instruction surfaces; 9 runtime targets resolve, 0 MISSING; remainder accounted for in subset semantics
SC-017_note=ambient-section C-11 traverses every guideline pointer on BOTH surfaces (template 8 unique targets, live 9) and asserts both halves of the delivery window — the runtime copy a reader opens under `.specify/shared/guidelines/` and the framework source that regenerates it. C-11(b)'s remainder assertion derives the full set from `shared/guidelines/*.md` (12 files) and asserts "full set − pointed-to set ⊆ the three named pointer-less guidelines", in subset semantics, so deleting any pointer fails while adding one does not. The ambient section carries FR-038's recovery route in normative prose ("should the owner document be missing from a project, it ships with the framework: refresh the project instructions to restore it together with its mirror copy"). Drill-proven in **both** directions: removing either copy makes the clause fail naming the missing half. The drill also found that C-11's first version resolved pointers against the framework source tree only, and therefore passed with the runtime copy deleted — the exact blind-check shape this feature kept uncovering in its own guards (notes/red-first-evidence.md's amendment).

SC-018_status=partial
SC-018_value=1 global baseline + 2 registered class overrides = 3 (<= 3) under by-class counting; 4 under by-line counting
SC-018_note=discipline-doc C-13 (exactly one global baseline), C-18(a) (2 registered override entries — classes ⑦ and ⑧, cap 2) and C-18(b) (no unregistered declaration anywhere in `shared/`, `templates/`, `skills/`) are all green. C-18(b) went green because the unregistered fourth site — `templates/commands/requirements.md:82`, class ⑦'s command-side twin — was converged by **deleting the copy**, per the one-source-of-truth repair direction ("remove the copy; do not correct the number"). That copy had already drifted from its owner (it had dropped `not developers`), which is the concrete cost this SC exists to prevent; a third unregistered copy in `docs/reference/commands/requirements.md` was found and converged by T049. Declaration files therefore went 3 → 2. The override column is declared in the truth doc as the sole counting source, and the doc deliberately carries no separate number. **Open user decision, not silently resolved**: SC-018 says "至多 2 **处**类级覆盖", and 处 reads as either class or line. By class (what C-18(a) implements, and what the truth doc's column declares) the total is 3 and the criterion holds; by line it is 4, and SC-018 would then need restating as ≤4 or the two `requirements-guidelines.md` sites merged.
SC-018_deferred_reason=Not deferred work but an unresolved counting interpretation; the implemented reading is documented and the alternative's cost is stated rather than absorbed. Recorded in the 第五轮 Clarifications block as awaiting user confirmation.

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=T034,T060,T061
deferred_reason_summary=All three are human/environment-dependent, not skipped engineering. T034 (quickstart scenario 5c, downstream bootstrap drill): the installed `specify` CLI is a non-editable site-packages 0.0.22, so init renders the installed package's templates rather than this tree, and a global reinstall needs user consent — FR-026's acceptance evidence is T033's mechanical check instead. T060 (SC-001 sampling review) and T061 (SC-006 double-blind agreement test) both require reviewers who did not build this feature; a single session cannot supply them, and fabricating a pass rate would violate the observation red line against invented numbers. Each row carries its reason inline as an evidence-cited `<!-- deferred: … -->` comment.

# -- Completion Gate re-validation (run against the current tree, not trusted from task state) --

gate_1_new_test_failures_vs_baseline=PASS (comm -13 empty AND comm -23 empty; 26 failed / 2042 passed; set-equal to baseline-failed.txt)
gate_2_mirror_and_regen=PASS (① scoped --check EXIT=0 on shared/templates/skills-summarize-project/agents/scripts; ② regen-command-copies --check EXIT=0; ③ 0 new MISS/DIFF lines vs the frozen set)
gate_3_gate_budget=PASS (blocking confirmation gates: 23; violations: 0)
gate_4_scanner_and_zero_change_surfaces=PASS (0 files changed vs BASE_SHA across scripts/, .specify/scripts/, src/specify_cli/, templates/plan-template.md)
gate_5_unclosed_task_rows=PASS (0 rows at `[ ]` or `[>]`; 60 `[X]` + 3 `[~]` = 63)
gate_6_validate_tasks=PASS (exit 0, 0 errors, 0 warnings)
gate_7_sc_status_lines=PASS (18 lines, this file)
gate_8_eight_pointer_files=PASS (all 8 files print exactly 1)
gate_9_no_new_executables=PASS (0, in both the stated tracked-diff form and the stricter union-with-untracked form)

# 9 of 9 gates pass. Every check above was re-executed against the working tree in this session;
# none was inferred from task-checkbox state. GATE-5 and GATE-8 were the two that failed at the
# MVP checkpoint and are the two that the US2–US5 work closed.

# -- Named follow-ups (recorded, NOT fixed inside this feature) --

followup_1=The confirmation-gate budget (total 23 / cap 23.25 / headroom 0) has NO owner document. `shared/guidelines/confirmation-gates.md`'s 99 lines never mention it; the threshold lives only in two contract tests and in two feature indexes' prose. Suggested landing: that document's `## 回流约束` section. Cross-feature — belongs to the gate-governance owner, not to 051.
followup_2=`AGENTS.md` / `templates/instructions-template.md` claim the `Total Features` count is "maintained by `scripts/bash/update-feature-index.sh`", which contradicts the script's actual behaviour: `:150` is `cat > "$FEATURE_INDEX"` (full overwrite) and `:164` emits a 6-column header that destroys the live index's `Spec Path` column. The script is unusable as described; either fix it or delete it. Target document = the Feature Index row in `templates/instructions-template.md` and its generated mirrors. This feature hand-edited the index for exactly this reason and never ran the script.
followup_3=Upstream drift, not this feature's: `.specify/skills/improve-skills/scripts/redline-check.py` differs from its source, and the blob comparison in notes/pre-change-measurements.md § ③ shows the divergence is present in `gitlab/master` itself. It is the sole remaining `DIFF` line and the reason whole-tree `sync-mirrors.py --check` exits 2.
followup_4=SC-002's CI-executed count assertion (its Source names a contract test) has no owning task row in tasks.md. Either build the test — traversing the 11-class enumeration so agent-facing steps are excluded from the count by construction — or amend SC-002's Source to state that the criterion is decidable-but-manually-applied. Recorded as a task-breakdown omission found during verification.
followup_5=`templates/feature-details-template.md:70` states the `Planned → Implemented` transition condition as "`verification.md` records a `SC-NNN_status=pass|deferred` row for every Success Criterion". That is the exact anti-pattern `.specify/templates/verification-log-template.md:22-26` names and forbids: the log template OWNS the status vocabulary (`pass | fail | partial | deferred | unknown`) and says any DoD row or **gate** constraining SC statuses must draw from that set, not a narrower subset. As written, four honest `partial` rows make a legally-satisfied transition read as unmet, forcing the executor either to reclassify honestly-partial criteria or to override the state machine. This feature hit it live and resolved it by correcting its own DoD-11 (same wording) and recording the deviation here rather than editing another owner's framework template — `templates/` is inside `scan-confirmation-gates.py`'s `SCAN_ROOT_FILES`, whose integer headroom is 0. Target document = `templates/feature-details-template.md` § Canonical Status State Machine, plus every generated mirror of it.

# -- Free-form notes --

post_change_rebase=rebased onto gitlab/master (925badb6) then master fast-forwarded; the feature branch sits 4 commits ahead of master, 0 behind upstream; 6 index.json conflicts resolved by `feedback-utils.py --action reindex` (the engine rebuilds the index from entry files, which is the correct route for a JSON index), 1 additive table-row conflict in skills/draw-diagram/SKILL.md resolved by keeping both rows; nothing pushed at any point
post_change_rebase_consequence=the rebase orphaned the originally frozen BASE_SHA (710c7179), which made `git diff BASE..HEAD` sweep in upstream commits and caused two gates to blame upstream's files on this feature. BASE_SHA was re-frozen to gitlab/master (925badb6) and the re-freeze was verified to be strictly tighter, not a relaxation — see notes/pre-change-measurements.md § ①'s supersession table.
notes=Scope was set by the user twice: MVP (Setup + US1) for run 1, then "rebase onto master and finish the remaining work" for run 2, with phase-boundary commits pre-authorized and one CONFIRM-tier gate verdict (the `.specify/memory/constitution.md` amendment) explicitly approved. **Six defects were found in this feature's own guards during the run, five of them one shape** — a verification command that returns an answer which is not about the proposition it was written to judge: (1) gate-neutrality C-5/C-6 derived their change set from `git diff <sha>`, which cannot see untracked files, so during the run window they were blind to exactly the artifacts they exist to judge; (2) discipline-doc C-3 compared two literals inside the test file and never looked at the tree, leaving "MUST NOT be renamed" unasserted; (3) ambient-section C-11 resolved pointers against the framework source tree while readers resolve the runtime copy, so SC-017's own drill passed with the runtime copy deleted; (4) C-14 measured the whole class-table section instead of the rule-source column, so it contradicted C-18 over a path the contract had already ruled on; (5) the double-landing test's missing `re.M` made its title set silently empty — a guard that could never fail; (6) C-13's first needle set was keyed to the truth doc's own brand-new phrasings and went vacuously green (XPASS under `strict`, which is what surfaced it). Every one was found by **executing** a check rather than reading it, and each was then drill-proven able to fail. The class and both countermeasures (mutation drill, anti-vacuity sentinel) were written up as § 十二 of `docs/reference/history/00-cross-cutting-lessons.md` and into the ambient instructions, so the lesson outlives this feature. Two sequencing defects in tasks.md were also corrected by annotation rather than by quietly overriding the schedule: C-18(b)'s green point was T012 (US1) while the work satisfying it was assigned to T043 (US5), so that half of T043 was front-loaded into US1 and both rows record the falsified premise; and a phantom `[P]` conflict arose from an annotation naming another task's file. Three-way partition of the pointers test file across US2/US4/US5 was resolved by removing the `xfail(strict=True)` markers once each story's clauses actually went green, so no marker outlived its purpose. Left untouched and reported as an upstream deviation: `skills/draw-diagram/` in-flight work (committed separately by user decision during the merge step) and the improve-skills drift at followup_3.
