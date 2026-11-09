# History Distillation — Batch 3 (18 sessions)

Read-only extract from `.specify/history/.work/` per `batch-3.txt`. Dimensions: **D** decisions & rationale (incl. abandoned alternatives) · **L** reusable lessons/pitfalls · **U** unfinished/TODO · **F** key interaction flow · **C** user↔model conflicts. Threads: T1 agents→skills→tools · T2 anchoring→goal→team · T3 archive+history+session · T4 derive+review+interview · T5 memory+state. 0 sessions skipped; 0 work files unreadable.

## 4c000af3-3681-40cb-afe5-2dda978e74af — 2026-10-08 — todo-in-context: comment-form TODO + philosophy docs

- **D** [T1]: Extend `scripts/python/search-todo.py` beyond fenced blocks to comment forms (`#`/`//`/`--`, non-Markdown gated) with `form: fence|comment`; fences illegal inside code files. Contract D-9..D-12, C-5/C-6, FR-014..016; fixtures `db.sql`, `legacy.ts`. Dual-face philosophy: owner `shared/guidelines/todo-in-context.md` + narrative `docs/concepts/todo-in-context.md` + Documentation Map rows; guard `test_todo_in_context_wiring.py`. Collection Step 6 now removes completed blocks after execution (lifecycle gap).
- **L** [T1]: fixture `valid/src/api.py` already carried a comment-form SPECKIT TODO — comment form was the originally intended shape, implementation lagged. New shipped guideline citing `.specify/specs/020-...` tripped shipped-surface neutrality; fix = neutral “name + framework-repo spec number”. 11 of 12 full-suite failures were concurrent-session WIP; only 1 was ours. pytest failure hint can reflect stale test semantics; AND-vs-any tuple semantics misread.
- **U**: none material; 11 unrelated concurrent-session failures left untouched.
- **F**: optimize todo command + record philosophy → gap found (scanner only fences) → scope decision (dual record + discoverable) → plan → implement scanner/fixtures/template/wiring → verify → commit `c016382e` (21 files, 834+/123−) staged by explicit path.
- **C**: user expectation “usually comments” vs spec FR-004 fence-only — user intent won; spec and implementation extended to both forms.

## 6313ff57-6320-4a0f-adb8-76df86f11120 — 2026-10-12 — merge-skills provenance + six-engine draw merge

- **D** [T1,T2]: merge-skills gains committed inheritance record `references/merge-provenance.md` + frozen baselines (`coverage_probe.py --emit-baseline` / `--baseline`) + `provenance_check.py`; Phase 8 cleanup gated on record committed, not on green probe. Six `draw-*` skills merged into `draw-diagram` as `references/types/<engine>/` (five-layer model survives; L4/L5 become type dirs); commits `bb2e3575`, `a5ed1556`, `ec6ffe77`. Goal `draw-two-layer-structure` T-001 `dropped→open→done` via `goal-utils` (only legal path; `dropped→done` illegal) — never hand-edit.
- **L** [T1]: three false-greens caught by own pressure tests — bare token list not re-extractable, `#`-leading tokens parsed as comments, provenance artifacts inside own corpus match trivially. Coverage probe caught image-alt corruption (`![标题](x.png)`→`!](x.png)`) the link checker missed. Pre-existing `feedback-utils.py:1352` globbed `skills/*/SKILL.md` one level deep in a two-layer repo → `--reconcile` 31 false errors; fix → zero-gap (71 objects/49 embeds) and exposed missing `skill:self-improvement` row. `\b`-regex renamed `draw-plantuml` inside team name `draw-plantuml-optimizer`. Bare `git commit` swept a concurrent session's 23 staged files; guard printed violation but commit was chained — fixed via `git reset --soft HEAD~1` + pathspec commit `9ad5675e`. B+C forced into one atomic commit: the duplication window breaks `test_hidden_edge_two_cycle.py` (OSoT sweep).
- **U** [T2]: `command-logic-as-classified-skills` still active; team S1 3/20 batches (`run-agent`, `analyze-artifacts`, `create-checklist`); Hugo `docs/public/**` stale, six test fixtures keep old slugs, `rewrite_paths()` still flat→layered only.
- **F**: improve-skills loop → user demands merge provenance → mechanism built and pressure-tested; user invokes merge-skills on six draw skills → survey halts on governance conflict (active goal target previously dropped) → user decision → staged merge → goal archive audit (4 active: 3 closed, 1 left active) → team run resumes S1.
- **C**: merge request inverted a documented two-layer design and a dropped T-001 — model stopped for user adjudication instead of assuming; user confirmed the new direction.

## 2337ce96-fdf1-4ba3-860b-dd7b89476cd5 — 2026-10-16 — 059 exec-quant-recording requirements

- **D** [T5]: A1 unit grain = `(unit_id, unit_type, run_id)` (run-determination semantics); A2 independent store, not feedback store (feedback is friction-only, packaged submission unsuited to neutral telemetry); A3 attach to existing wrap-up probe via HandlerBinding, zero new template face/confirmation gate; A4 scoring = user manual + run-determination derivation, source-tagged; A6 parallel with run-determination, four-axis contract unchanged.
- **L** [T5]: scaffold `create-new-requirements.sh` auto-creates and switches the branch — do not recreate it. `/tmp` writes blocked by workspace boundary → pass reflection points via engine `--points`. Run-determination needs caller-declared complexity; command + inner skill record separately under one run-id.
- **U**: next stage clarify (Feature binding); feedback backlog 36 ≥ threshold 10 (non-blocking).
- **F**: dispatch → internal `create-requirements` skill → scaffold `059-exec-quant-recording` (baseline master @ `289be39d`) → 15 FR/3 US/4 SC + checklist → validator 0/0 → commit `4166a5be` → wrap-up ×2 units.
- **C**: none.

## 09e7b15b-58c5-4754-a214-28b36880d90a — 2026-10-16 — runtime model info probe + sdd-loop-driver 059 run

- **D** [T1,T5]: runtime context exposes no provider / model id / effort / context window; only host status surfaces or config carry them. Process forensics (`/proc` environ, `ss`) showed active connections to `qoder.sh` endpoints while Aliyun MaaS env vars had no active IPv4. Switched to `/sdd-loop-driver` U0–U6 for feature 059.
- **L** [T1,T5]: effort not explicitly configured; config face does not echo the effective default → record “未显式配置”, never guess. External-class skill units are intentionally absent from the probe registry (`test_probe_nonentity_catalog.py:92` asserts) — feedback record rejection is a guard, not a defect; run-determination records fine. State spine transitions must append, not replace (one accidental replace fixed). pgrep hit was an exiting process — check process tree before declaring residue. Review P0=0; P1×4 (stale facts not written back, compile-order doc contradiction, registration-duty ownership, over-surface delivery red-first collapse).
- **U**: P1×4 handed to framework maintenance line; empty-config `effort` disclosed; not pushed (master ahead 10/11).
- **F**: model-info interrogation (user interrupted) → SDD driver with 059 brief → U1 probe → per-stage dispatch/U4 → fast-forward `289be39d → 6f37e013` (262 files, +7460/−976) → wrap-up honest `not_evaluated`.
- **C**: user interrupted heap-memory inspection; no disagreement on outcomes.

## 0250abd1-c412-4471-9336-64b3aca6ef44 — 2026-10-19 — 062-humanize-command tasks

- **D** [T1]: Tests Mode ON via Principle IV + VII template-only gate → structural contract tests + E8 corpus/rubric; 33 tasks / 7 phases / 34 green claims exactly once. Green partition must be monotonic per contract ordinal to avoid cross-phase WARNs. C-7 read literally → 6-step Wrap-up for humanize (existing skills carry 5), recorded as D-T1. `cws-lib-bash` missing recorded in `## Environment Prerequisites`; baseline not relaxed (23 added failures).
- **L** [T1]: `[P]` parallel-safe false positive fixed via pointer governors (`指向`) and dropping `[P]` from T007. 48 `skill-*-wrapup` registry rows vs 73 compile units (23 complex commands + 50 skills; `sdd-loop-driver`/`sdd-project-setup` carry Wrap-up without rows — external units by design). Flat skill count overcount: `find .specify/skills -mindepth 1 -maxdepth 1` includes `internal` → 13 external via `EXTERNAL_SKILLS`. 26 command templates vs 25 docs pages (`improve` lacks a page). Wrap-up template call lacked engine-required `--run-id`; corrected per engine `--help`.
- **U**: next stages analyze/implement; 48-vs-50 registry observation recorded as D-T5, not repaired.
- **F**: dispatch → context load → premise measurement (94/3906 vs frozen 71/3929 root-caused to `cws-lib-bash`) → tasks.md design → validator PASS 0/0 → commit `e14d9a0a` → wrap-up.
- **C**: none.

## dde7a9d4-47f2-45ae-9cea-714718cba781 — 2026-10-19 — 062 analyze round 2 (quality gate)

- **D** [T4]: gate passed — CRITICAL 0 / HIGH 0; H-01 (injection defense) and H-02 (primary-language rule) fully closed; 21/21 round-1 findings resolved, 4 new MEDIUM/LOW. Same-author gate not triggered (artifacts predate session). Zero CRITICAL/HIGH → no validation wave; zero-CRITICAL/HIGH floor replaced by full-coverage mapping review (all 29 FR + 11 SC, not sampling).
- **L** [T4]: repair-round residue concentrates in index/summary lines — new enumeration items land in obligation bodies but not in Measurement Sources (U-08 SC-011), E8 range summary (F-07), structural trees (L-05). Contract header FR enumerations are a standing drift surface; shrink to a pure pointer. `check-prerequisites.sh` ran under bash despite round-1 “not runnable” — calling-context difference, disclosed, no premise falsified. Archive literal check false-miss on blank lines → verify with non-empty lines.
- **U**: U-08/F-07/L-04/L-05 suggested for implement or a later doc round; read-only stage produced no commits.
- **F**: dispatch round 2 → load round-1 delta baseline → read requirements/plan/tasks/contracts/data-model → program-derived counts (FR 29 / SC 11 / clauses 35 / tasks 33 / features 61=61) → validators → report with rerun delta → ANALYZE-DONE.
- **C**: none.

## 7362873e-e6c3-4f93-8313-d60bcd451494 — 2026-10-19 — 063-review-p1-governance plan

- **D** [T4]: Feature 063 fixes review P1 findings F1–F8 at framework-source side; canonical clause form `md-bold-closed` (`**C-N**:`), citation group = LAST parenthesized group with FR-/SC- ids (owner contract-clause-definitions §4 rule 2). Same-author delegation: constitution scorer 16/16 confirm (0 overturn), contract auditor 7 findings all repaired in-commit. Pre-change baselines frozen: 63 failed/3954 passed; 202 sync DIFF; regen clean; compile-embeds 74 units zero drift.
- **L** [T4]: subagent claims falsified by firsthand reading — “Mode 5 自省” is actually manage-feedback Path A `A3 自省`; “GATE-8” does not exist (gate ids are tasks.md-local; implement anchor = Step 9 verification-log); red-first note shape owner is `create-tasks`, not implement-feature. Legacy markers `**C-N — label**:` = `md-bold-paren`; FR ids in heading labels are mentions, not citations — all 30 clauses cited zero FRs until repaired (extractor `clause_citations()` proved it). Piped test command exit code reflects `tail`, not pytest. plan.md pre-asserted “verdicts unchanged” before delegation findings filled — anomaly caught by scorer.
- **U**: Feature 063 Draft→Planned; implementation deferred to tasks/implement; commits `2bcee2ac` (12 files), `bf88f2c6` (run records).
- **F**: dispatch → load authoritative 062 review → baseline freeze → Explore + personal verification → same-author delegation → repair 7 findings (34 clauses, re-extractor + live accountant `[fr-uncovered] pass 30/30`) → plan integrity → Feature Integration → wrap-up → PLAN-DONE.
- **C**: none user-facing; self-caught artifact pre-assertion.

## 2633f12c-6d57-43bf-8375-684b1b90989a — 2026-10-20 — 063 implement attempt 2 (resumed)

- **D** [T4]: C-12 propagation owner = `/speckit.instructions` (manage-instructions Action 5); never extend additive-only `scripts/bash/generate-instructions.sh` (user adjudication, recorded in Clarifications; test renamed `test_c12_live_instructions_received_rec_via_content_refresh`). 053 window-freeze: `C12_WINDOW_END = "cb0a190a"` closes the `test_c12_the_status_state_machine_is_untouched` window (test_c7 precedent) because the contract scopes the freeze to “本特性窗口”. C-20..C-25: engines expose `--action args-manifest` built from their own parser; renderer consumes manifests at compile time, `<UPPERCASE>` placeholders, convention line declared once in registry § Handler note; C-23 one-shot missing-arg errors; C-24 `(unit_id, run_id)` idempotency, no run-id minting. C-26 evidence records sha256; C-29 Step 0 baseline pre-flight with 4 provenance classes (`upstream repair`/`inherited`/`attributable to this feature`/`undecidable`).
- **L** [T4]: repo engines load the probe registry from the RUNTIME face `.specify/shared/definitions/probe-definitions.md` — sync must precede compile/`--reconcile`. `sync-mirrors.py --only skills` is a silent no-op (pairs are `skills/external`/`skills/internal`); `(N files)` = actually copied count. `MAX_SECTION_BYTES` 1500→2500 with dated comments: inline manifest rendering grew max face 2135 B; anti-copy intent kept by `OWNER_ONLY_LITERALS`. Stale closed-set: 056 contract/exec-quant docstring said “3 actions” while 4 had landed (`collect-dispatch`). Harness bugs: `[a-z_]+` misses `evidence_sha256` digits, blank lines don't close records, `re.search(text, re.M)` passes pos not flags. Transient NEW failures while regression runs during template edits (per-tool copies stale). Void gate items: GATE-5/DoD-4 `exit 0` premise was false at plan time (failures frozen in baseline) → void with cited measurement + inline annotation (“met with one void row”). Permission classifier blocks Bash/python bulk flip of tasks.md — use Edit per row. 42 of 63 baseline failures disappeared with mirror sync (not regressions).
- **U**: none blocking — 51/51, Feature 063 Planned→Implemented, commits `68e6b43c`, `7e738423`, `cf8c882e`, `a969e310`; not pushed; 062 zero-diff held.
- **F**: resume dispatch → C-12 align + US2 close → US3 (args-manifest renderer) → US4–US6 → Polish → Completion Gate re-validation → status flip → wrap-up engines → IMPLEMENT-DONE.
- **C**: attempt-1 fast-fail halt already adjudicated by user (C-12 mechanism); no new decision-level anomaly.

## 2b259011-1831-4073-835e-0994d88b534d — 2026-10-29 — 074 goal-team↔SDD unification (requirements→push)

- **D** [T2]: goal→team→agent sits above SDD. Authorization two layers: agent `sdd-invocation` + team `seats` AND, default `forbidden`. Routing engine `sdd-route.py` three-value `sdd/direct/adjudicate`, priority `adjudicate > sdd > direct`; missing/conflicting inputs only adjudicate, never default direct; owner `shared/definitions/sdd-routing-definitions.md`. Anti-nesting invariant narrowed, not deleted: depth-2 chain (team orchestrator → member driver host → stage executor leaf), virtual members banned, SDD-within-SDD banned. Nested SDD hands off after review; merge/push owned by outer goal/team. tasks split gate 57 > 40 → 074a (FR-001–019 + FR-025) / 074b (FR-020–024 + FR-026–028); parent tasks marked SUPERSEDED.
- **L** [T2]: root-owned `.git/objects` buckets (30, then 15 regenerated 2026-10-28 23:58) blocked `git add`; same content hash → same bucket, retry useless; U5 stall with actionable repair; persistent fix = default ACL `setfacl -R -m u:agent:rwX -m d:u:agent:rwX`. Slice specs writing parent ids as `FR-xxx` trip pre-analyze dangling refs → use `Parent FR 0xx` (checklist `FR 020` space form). F1 framework defect: `find_feature_dir_by_prefix` matches only `^([0-9]+)-`, so `074b-...` resolves to parent 074 dir — bypass via explicit target, P0 waiver. Closure regressions: confirmation-gate 27→28 from a negative sentence miscounted by the scanner; neutrality violations from shipped docs citing Feature 064/070/074; compatibility pin frozen hash missing `src/specify_cli/__init__.py`. test-budget ledger needs per-row `purpose/trigger/at/selection_basis/rc` + 6 stage E3 rows.
- **U**: F1 prefix defect recorded not fixed; Feature 074 Ready for Review pending human Completed; feedback backlog 174+; pushed fork mirrors only (`gitlab`/`github`/`gitee`), upstream `origin` untouched; final `89b7d8cab`.
- **F**: requirements (containment claims FR-026/027/SC-005/SC-008 repaired before checklist) → clarify (same-author delegation; Feature 074 bound) → sdd-loop-driver U0–U6 → permission stall ×2 → split → 074a/074b door-to-door → closure → local merge → user “更新代码再合并推送” → merge `89b7d8cab` → push three mirrors.
- **C**: “更新代码再合并推送” after Ready for Review — model followed declared git workflow, merged two remote commits; only conflict `glossary.md`, both sides kept.

## f3930139-5d2c-4252-8820-15a9c53149c7 — 2026-11-05 — validator rejects H-06 (glossary STR-002 vs STR-004)

- **D** [T4,T5]: verdict `reject` — glossary is a project-local store, not a distributed client-facing surface; existing rows cite `真源 shared/definitions/...`; C-32 allows either `STR-002`/`STR-004`; A11 governs client-facing outputs only; `glossary-utils.py validate` enforces no path form.
- **L** [T4,T5]: live store already carried the exact T043 row (`.specify/memory/glossary.md:185`) — task and contract jointly satisfiable as written. Lone `[[STR-004]]` at line 40 is an unresolved 042 Shared-String placeholder for `focus_target`, not a path. Forced split `evidence_supported` / `evidence_not_supported` makes the validator name what artifacts do NOT say.
- **U**: none (single verdict).
- **F**: read cited artifacts + glossary convention → judge → reject with file:line evidence both fields.
- **C**: none.

## d28dbd53-733f-4c57-aa62-aefa74729449 — 2026-11-06 — history-review mechanisms + 085 temporary Goal/Team

- **D** [T2,T3]: no unified history-audit command exists; capabilities are layered (goal view/validate/coordinate, review/analyze per-feature, feature registry reconcile, sanitize, summarize, sdd-house-keeping). `/speckit.history` does NOT read `.specify/specs` or `.specify/goal`; goal archive is engine-write-only and outside sanitize `MATERIAL_ROOTS`. Fusion design: temporary Goal under `.specify/specs/<NNN>/goal/`, temporary Team under `.../team/`; Goal formed after requirements U4, Team after clarify+plan U4; stage roles replace generic `sdd-executor`; `agent_concurrency_requested` default 24; per-agent worktree + 064 integration queue; maxTurns unified 500. Renumbered 084→085 because remote `gitlab/master` already had Feature 084 (“Never create duplicate Feature IDs”).
- **L** [T2]: maxTurns actually 400 (2026-11-05 policy 120→400), not 120 — corrected before planning. Disk “full”: `df` 0 vs `stat -f` ~179 GB free = ext4 root-reserved blocks; agent could not write git index. 617 root-owned files chowned to agent (reversible) before render/mirror work. Baseline attribution: reproduce failures in `aafbf5a8` worktree before claiming pre-existing (8 representative failures reproduced). Branch cleanup only after verifying fully merged / only deletions (070 worktree: 4218 deletions, no modifications).
- **U**: SC-010 partial (bounded live dogfood only; no full 8-stage driver run); code segment `not-evaluated`; pushed `24cb4edc` to three forks via renumbered `2cb68c44`/`70d2bb1e`.
- **F**: mechanism survey Q&A → fusion design (067/070/074 gap check) → `sdd-route.py` verdict `sdd` (`sdd-capability-or-contract-change`) → implementation S1–S7 → full-suite attribution → review → commit `cbbf6dda`/`55ce4508` → user requests push → renumber + `--no-ff` merge + push.
- **C**: user’s “SDD 启动即建 team” conflicted with 074’s ban on SDD creating Goal/Team — constraints surfaced; user chose spec-local temporary goal/team.

## a3a581e2-ffb3-4360-ae4b-a5cd91648a77 — 2026-11-09 — 094 repair writer R2 (anchoring vocabulary)

- **D** [T2]: adopt trunk’s live vocabulary — global store `.specify/anchoring/<slug>/goal.md` (filename still `goal.md`), spec-local `<spec>/goal/<slug>/goal.md`, teams `.specify/teams/<slug>/team.md`; engine scope values stay `global|spec|auto` (stated as fact, not redefined); FR-007/FR-025/FR-028 re-scoped with rationale in plan T-004. Page-qualified clause ids: FR-016/FR-035 → `handoff-contract#C-53`/`#C-54`; FR-043 → `unified-archive-and-migration#C-112`/`#C-113`; register row `R3-H-1…L-5@094`.
- **L** [T2]: definition-form bullets `- **FR-007**` in Notes trip the dup-id gate — use plain id form. FR-022 table row carried 5 cells in a 4-column table (real pre-existing defect, distinguished from a parser artifact by re-parsing). R1’s concurrent rename verified landed (113 markers / 113 distinct ids) before writing post-rename ids.
- **U** [T2]: contracts still name `.specify/goal/` in live clauses (C-10/C-13/C-15/C-31/C-58/C-59/C-66, `owner-rewrites:57`) — sweep unassigned in this wave (ANOMALY line).
- **F**: read findings D1–D5 → measure tree → 9-item edits → `validate-requirements.py` green (0/0; 55 definition rows) → map regeneration 43/43 → ledger `repair-r2.md` → R2-DONE.
- **C**: none; territory split left a disclosed cross-file gap instead of silent handoff.

## a07fa138-1d8c-44b4-b67c-ffeebeebc65a — 2026-11-09 — FV2 final verification (094 fix wave)

- **D** [T2]: verdict `FV2: FAIL` on 3 claim-hygiene items — `requirements.md:47` cites round-3 “goal 9 / team 9” while EP-002 now says probe 9/8=17 / census 9/10=19; `plan.md:102,104` live decision-tension fields carry superseded “2026-11-09 复测 18 条”; `register.md:192-193` status drift after closure `84d8765f`.
- **L** [T2]: named-site repair ≠ class repair — M-5 fixed exactly the three named sites but the falsified 9/9-derived denominator survived at three unnamed live lines. Clause-id extraction must target markers, not body mentions. Headline counts verified: FR 43 / SC 12 / markers 113 = 113 distinct / tasks 83 T001–T083 / packages 15+17+19+8+16+6+2=83; `features.md` 88=88=88; team YAML parses with only 4 assigned lines changed.
- **U**: the three FV2-F items open at handoff.
- **F**: read fix-wave notes → measure counts → check three M-5 sites → sweep stale counts → claim-hygiene spot checks → fragment `fv2-consistency.md` → FV2-DONE.
- **C**: none.

## 3db3e58c-a375-43ad-b3a6-fbbe1fe81fad — 2026-11-09 — test-suite audit chunk 4

- **D** [T2,T4]: 73 modules / 441 tests → keep 398 / rework 36 / delete-candidate 7. 28 goal-surface tests still read the retired global `.specify/goal/` tree (current `.specify/anchoring/<slug>/summary/`; `build-summary-input.py:1054`, `goal-utils.py:66`); 1 permanently-red red-first test `test_parallel_lines` calls the unregistered `handoff-decision` action.
- **L** [T2,T4]: tautological tests assert constants defined in their own helper (`test_c006_engine_sticky_on_update`); duplicate coverage named (`test_source_and_mirror_are_byte_identical` ≡ mirror-parity suite); slow-by-construction constructs named — 8 nested pytest subprocesses (`test_wp_mutation_drills.py`), 300 s `specify init` smoke, 50,001-record session fixture, Hugo/Docker. JUnit artifact mismatch (`tests="0"`) means no pass/fail count may be taken from it; `--durations` data did not survive.
- **U**: rework/delete candidates left to owners (audit only).
- **F**: read 73 modules → verify removed surfaces against engine → write per-test table (`audit-4.md`) → chunk totals.
- **C**: none.

## e2c7372c-116f-4ed3-b3bc-9a77f7c5006d — 2026-11-09 — consolidation review G8

- **D** [T3]: keep 4 entries (043-init-commit-stamp, 044-reduce-confirmation-flows, 090-re-anchoring, 091-auto-git-closeout). Sibling note: `092-non-disposable` → archive/merge-into 090 (83 files, no verification/closure, 116 open task rows, Status `Planned` while narrative says merged into 090).
- **L** [T3,T2]: registry spec-dir numbers offset from feature-registry numbers (spec 043→Feature 045, 044→046). “Accepted” machine block coexists with unresolved `SC-003 (full-suite) = final/fail` row. `.specify/goal → .specify/anchoring` rename still named as live by four owner surfaces (`framework-map.md`, `non-disposable-review-surface.yaml`, `non-disposable-definitions.md`, driver `SKILL.md`) — consolidation must not close 090/092 until adjudicated.
- **U**: 090/092 adjudication deferred; 092 cleanup.
- **F**: survey 4 dirs + registry rows → verification/closure evidence → stale-reference scan → `review-G8.md` → REV-G8-DONE.
- **C**: none.

## c2287715-20d7-4887-ac4c-bed79e50aab6 — 2026-11-09 — consolidation review G9

- **D** [T3]: keep 7 entries (031/032/035/045/073/088/089); mapping offset established (spec 031→row 032, 032→036, 035→040, 045→047).
- **L** [T3]: 073 requirements-only dir yet marked “Implemented”; 089 marked Implemented while `closure-suite.txt` records 111 failures vs 34-failure baseline (~77 new) and T081/T086 read “remain” in `verification.md` but “[x]” in `tasks.md`. Text-match “open task rows” false positives came from template text — verify exact rows.
- **U**: contradictions flagged to owners, none repaired here.
- **F**: structure/registry mapping → git dates → detail/verification read → evidence checks → `review-G9.md` → REV-G9-DONE.
- **C**: none.

## b3bf67dc-e96c-4026-973c-fdaaf68b66bd — 2026-11-09 — 094 artifact-segment re-review round 2

- **D** [T4,T2]: artifact segment `pass`; AF-1..AF-6 + ARC anomaly all closed; SC-010 remains `partial` with ARC reading, `final_path` stays 8/8; close-out precondition (`Planned → Ready for Review` flip + merge) unblocked.
- **L** [T4,T2]: gates reproduced on MAIN — `closure-acceptance-check.py` `verdict: accept` / `pass=8 ... fail=0`, requirements 0/0, tasks 0 err/1 disclosed warning (`T043 → T054`). T022 names a guard test that does not exist (P2 residual; module has six other tests). Package split 15+17+19+8+18+6+2=85. Unrelated working-tree changes (humanize→humanize-conclusion rename, study-code batch) disclosed, never attributed.
- **U**: P2/P3 residuals — dangling `wp07-closure-suite.log`, `§ 5.1/§ 5.3` resolving to list items not headings.
- **F**: read consolidated/process/ARC inputs → diff `19003b613..0f02c32fb` → per-AF verification → gate re-runs → `review-artifacts-round2.md` → RV-ART2-094-DONE.
- **C**: none.

## 1b96db87-ef22-40d3-a19f-f3947b12ac13 — 2026-11-10 — /speckit.history Wave 3: G4 renumber-live-binding

- **D** [T3]: of 105 `renumber-live-binding` entries, 9 live bindings corrected in place (git-verified dir renames `063→074→075`, `079→080`, `087→088`; corpus shapes C1/C4); 96 left open as legitimate owning-feature registry bindings (94 registry-backed + 2 Feature 040 refs) — rewriting them would falsify current statements. `not_closed.open` 908→899 (−9 exactly), zero additions, no other class moved.
- **L** [T3]: two-level numbering trap — spec iteration dirs vs feature registry numbers; most `**Related Feature**`/`**Feature ID**` hits are cross-namespace bindings, not renumber residue. Brief’s “909” = total-entry count (908 open + 1 unevaluated). Determinism check difference explained: the evidence file itself joins the `test-evidence` dated-record exclusion. Engine over-approximation (96/105) recorded as a framework observation, never “fixed”. Adjacent unreported residues named (e.g. 088 quickstart/research/data-model `**Feature**: 087`).
- **U**: 96 entries stay open with per-entry evidence; engine over-approximation flagged for framework maintainers.
- **F**: probe before/after (`history-w3-before.json` / `-after.json`) → classify with engine predicate → 9 edits across 8 files → `validate-tasks.py` passes → `history-execute-g4.txt` (E-7 segments) → HIST-W3-DONE.
- **C**: none.

---

## Per-thread index

- **T1 agents→skills→tools**: 4c000af3 (todo command/comment form), 6313ff57 (merge-skills provenance, six-engine draw merge, team S1 skill packages), 09e7b15b (driver skill behavior, external-unit registry), 0250abd1 (humanize command + skill wiring).
- **T2 anchoring→goal→team**: 6313ff57 (goal archive audit, team run), 2b259011 (goal/team over SDD, routing, split), d28dbd53 (temporary Goal/Team, renumber), a3a581e2 (anchoring vocabulary, page-qualified ids), a07fa138 (goal/team denominators), 3db3e58c (retired goal surface in tests), b3bf67dc (094 close-out), e2c7372c (rename owners).
- **T3 archive+history+session**: 1b96db87 (renumber wave), e2c7372c (G8 consolidation), c2287715 (G9 consolidation), d28dbd53 (history/archive mechanism survey).
- **T4 derive+review+interview**: dde7a9d4 (analyze round 2), 7362873e (063 plan + same-author delegation), 2633f12c (063 implement, void gate items), f3930139 (validator judgment), b3bf67dc (artifact re-review), 3db3e58c (suite audit).
- **T5 memory+state**: 2337ce96 (exec-quant requirements), 09e7b15b (state spine, run-determination), f3930139 (glossary store convention).

## Counts

18 sessions distilled (0 skipped). 90 dimension findings total: D 18 · L 18 · U 18 · F 18 · C 18 (aggregate sub-points exceed 90). Thread feed counts: T1 4 · T2 8 · T3 4 · T4 6 · T5 3 (multi-tagged sessions counted once per thread).
