# History distill — batch 6 (18 sessions)

Source: `.specify/.tmp/history-batches/batch-6.txt` (1,146,498 bytes). Read-only session store;
no commits; no subagent spawns. Threads: T1 agents→skills→tools · T2 anchoring→goal→team ·
T3 archive+history+session · T4 derive+review+interview · T5 memory+state.

---

## e059c728 — 2026-10-09 — Feature 054 agent-registration-wiring end-to-end SDD + 055 merge readiness

**Decisions & rationale**
- Design ruling (user): option (b) — `create-team` instantiates seats via `create-agent`; abandoned (a) init-installed frames (conflicts with `{{PLACEHOLDER}}` rejection at `src/specify_cli/__init__.py:303-307`) and (c) `seat_kind` discriminator.
- Trigger mechanism: narrow CLI subcommand `specify render-agents --ai <tool>` delegating the existing renderer — uv/pipx isolation refutes in-script import; `init` re-run too heavy. [T1]
- Qoder IDE/CLI share `${project}/.qoder/agents/` (verified via `docs.qoder.com/extensions/subagent`) → `_AGENT_METADATA_MAPPING` needs no IDE row. [T1]
- Contract clauses must use canonical `**C-N**` bold form; one green-claim row per test file (green-path-divergence remedies `partition`/`blockedBy` are not implemented).
- Feature binding: 054 → Feature 044 (renderer is 044's deliverable).

**Lessons / pitfalls**
- Concurrent-session commit pollution: `git add <paths> && git commit` commits the WHOLE index; 09bd40a9 absorbed 52 foreign staged files. Fix: `git commit -m msg -- <paths>`. User ruled "一起提交" (keep as-is). [T3]
- Substring assertions are immune to suffix-append mutations (`seat instantiationz`); use deletion-form mutations; grep marker words first (`team-scoped` substring matched `team-scope` → vacuous green).
- Installed CLI `/usr/local/bin/specify` 0.0.22 lacks new subcommands → Two Hats deployment-time lag; teaching surfaces reach downstream only after publish/install.
- `merge-tree` does not report modify/delete conflicts — a real merge is required (055 vs 054 `feedback/index.json`).
- Pre-written "Post-Design Re-check"/Phase-1 counts = anticipatory claims; backfill only after artifacts land.
- Root-owned `feedback/state/` (root:root 755) recurs — needs `sudo chown`.
- `mark-submitted` packs before writing state → crashes leave orphan zips; `packages/*.zip` is outbound-only (root `.gitignore`, not committed).

**Unfinished / TODO**
- 054/055 merged and branches deleted at session end; feedback zip `feedback-20261008T140841Z.zip` left for manual delivery; local master 25–26 commits ahead of gitee/gitlab, unpushed.

**Key flow**: requirements → clarify (4 bundled rulings, 09bd40a9) → plan (16/16 via fresh-context subagent; 8c2ad699) → tasks (validator 10 err→0; 6f7ea28c) → implement long-run (31/31; M1–M6 mutation drills) → review (13 findings; F1 P0 → dogfood demo team `demo-seat-dispatch`/`dogfood-executor`) → roadmap fixes (b4f2b8cb) → worktree cleanup (055 branch preserved) → 054↔055 merge experiment (13/13 store tests) → merge verify (48 passed) → branch deletion.

**Conflicts**: detector found wrap-up commit pollution; user adjudicated keep-together. Review validator corrected SC-003 "4 tools" → "two directories".

## 75ced50f — 2026-10-14 — /speckit.goal create `draw-diagram-interactive` + goal-based team create

**Decisions**: "dynamic" redefined as interaction result (explicitly NOT animation/video), recorded as boundary; one success criterion (drawable interactive chart, usually HTML); targets skipped; team slug derived; iteration pattern, 3 temporary seats, `skill-verifier` template reused; canonical write only by Meta supervisor; zero writes to goal.md from the team branch. [T2]

**Lessons**: both wrap-up engines (`run-determination.py`, `feedback-utils.py`) require `--run-id`; threshold notice needs BOTH `should_prompt` and run-determination routing bit; goal-based branch decision is engine-driven (`goal-utils.py list --json`), disclosed not gated.

**TODO**: run `/speckit.instructions` to sync discoverability; first team run pending.

## 26940d66 — 2026-10-16 — /speckit.tasks for 059-exec-quant-recording (unattended)

**Decisions**: Tests Mode ON (Principle IV); Foundational phase omitted (engine spine folded into US1, `blockedBy` links); `[green:]` tags NOT used — contracts carried prose headings (clause_extract md-none/0) and the tag would dangle; inline text partition instead; 059 stays Planned. [T5]

**Lessons**: generation-time premise re-measure: `_ENGINE_SIBLINGS` at L619 (plan said L620-621); budget test = 853-line cap counted by H2 non-empty lines; feedback engine needs repeated `--points` plus `--review` body. Validator PASS 0/0 first try; commit 94f344a1 (tasks.md only).

**Exact artifacts**: `.specify/specs/059-exec-quant-recording/tasks.md` (16 tasks), `notes` evidence scaffold.

## 08e0989e — 2026-10-19 — /speckit.requirements for 062-humanize-command

**Decisions**: 4 user stories (2×P1, 2×P2), 28 FR / 10 SC / 3 Shared Strings / 19 edge cases; `Related Feature` left `Need clarification` per protocol (clarify owns binding); commit `898aa02e`. [T3]

**Lessons**: validator `validate-requirements.py` status ok (244 lines/38 definition rows); checklist 16/16; run records (session/exec-quant/feedback) stay out of the stage commit.

## b15cd656 — 2026-10-19 — /speckit.clarify repair round 1 for 062 (analyze gate HIGH=2)

**Decisions**: H-01 → FR-029 + SC-011 (prompt-injection defense); H-02 → FR-013/SC-003 main-language owner rule; B-01 full CLI syntax in FR-018; U-01..U-07, F-01/F-02, L-01..L-03 written into `## Clarifications` (5 Q&A groups) + FR/Edge/Assumptions; D-01 source requirement archived verbatim to `notes/source-requirement.md` (diff-verified; only trailing newline added by fence). [T3]

**Lessons**: "archived verbatim" is a claim → program-diff it; append-only Clarifications block (2→7 rows); validator 0/0 (264 lines/40 def rows/4 shared strings); commit `173c897d`.

## d22e136f — 2026-10-19 — /speckit.review for 062-humanize-command (SDD process review)

**Decisions**: 8 findings, P0=0 / P1=6 / P2=2 after 4/4 P0-candidate downgrades (gate rule 6 reports the rate). F1 citation-group paren charset undeclared (`clause_extract.parentheticals()` ASCII-only, `scripts/python/clause_extract.py:125-140`) + coverage lane `account-clause-coverage.py` has zero invokers; F2 no stage accountable for checklist items, `/speckit.analyze` checklist-blind (`grep` 0 hits), CHK005 pre-figured H-01 by ≤19 min; F3 review→improvement dead letter (RECs unregistered; `feedback-step.md:79-81` scope guard); F4 compiled Wrap-up faces omit required flags (10/10 command units failed); F5 `tasks.md:281` D-T2 superseded premise (carrier list closed); F6 sample claims unbound to evidence (`verification.md:180` s11); F7 re-freeze duty producer-side only; F8 GATE-7 vs GATE-1 misbinding. [T4]

**Lessons**: commit reachability check — `origin` is upstream `github/spec-kit`, `git branch -r --contains HEAD` empty → §0 UNRESOLVABLE + `git show <sha>:<path>`; validators get only the finding; evidence snapshot at diagnosis time; counts enumerated; `run-determination` `(unit_id, run_id)` idempotency locks under-measured records; registry status conflict: `features/062.md:72` demands Ready-for-Review but `shared/workflow/feature-integration.md` has no `/speckit.review` row (thrown back as ANOMALY).

**Commits**: `d2f0e510`, `1b13595e`. **Conflicts**: two adjudication-class ANOMALY lines thrown back, not smoothed.

## 6b6a829d — 2026-10-19 — /speckit.analyze for 063-review-p1-governance (read-only)

**Decisions**: CRITICAL=0/HIGH=0 gate satisfied; 5 MEDIUM + 3 LOW; 40-item checklist gaps NOT upstream-return (precision deliberately delegated to contracts); F1–F8 → 30/30 FR, 34/34 clauses, 34 green tags on 14 rows, zero collisions; same-author gate not fired. [T4][T1]

**Lessons**: green-tag `grep -c` line count ≠ row count (3 format-doc lines inflate); `[P]` measured 24 vs recorded 25 (T002 self-declares "不并行"); F4 reproduces live at run start (missing `--run-id`/`--complexity`); read-only stage = no commits, wrap-up records left uncommitted for orchestrator archival.

## 840faac8 — 2026-10-20 — Concurrent-safe stores: exec-quant per-entry files + instructions rule

**Decisions**: `records/<UTC-microsec>-<8rand>.json` / `scores/` one file per entry, atomic temp+rename, legacy `.jsonl` read-only fallback (no migration); evidence `index.json` → derived-on-read (deleted); single-owner exceptions retained: `trigger/index.json`, `history/.manifest.json`, `teams/<slug>/{items,run-log,STATE}`, `feedback/cleanup|migration-log.md`, canonical registries. New `## Concurrent Development Safety` section landed byte-identically in `templates/instructions-template.md`, `.specify/templates/...`, `.specify/instructions.md` (symlinks follow). [T5][T3]

**Lessons**: neutrality-budget gate has zero headroom (26 baseline at clean HEAD); mirror/action-set guards; git workflow = temp-branch: branch → `--no-ff` merge to `master` → push `gitlab`/`github`/`gitee`, never `origin`. Commits `aadcaf6b`, `d2a5c738`; 338 targeted tests pass.

## aae40c3f — 2026-11-05 — Read-only VALIDATOR, finding H-01 (feature 082)

**Verdict**: confirm HIGH. `tasks.md:77` T006 expects two existing suites to be red pre-landing; both are green (static evidence; Bash denied) and plan-owned text (`quickstart.md:157-162`, `test-evidence/plan-stage-checks.md:109`) says they pass vacuously; the real red-first mechanism is a new test module per `plan.md:49,67-74` + `research.md:117-119`, placed only in tasks T007/T029/T039; `[green: ...#C-1]` attribution anomalous; GATE-1 (`tasks.md:29`) owns the only permitted pre-existing red (`test_proactive_trigger_section.py`). [T4]

**Lessons**: validators must return both `evidence_supported` and `evidence_not_supported`; static-only verification is a weaker path and must be stated; finding overstated "new module" (actually existing instructions module).

## 94c3fd85 — 2026-11-05 — Read-only VALIDATOR, finding H-05 (082 clause C-20/C-21)

**Verdict**: downgrade HIGH→MEDIUM. Two headings parse to id `C-20` (`mirror-distribution.contract.md:12` vs pointer stanza `constitution-double-landing.contract.md:94`); clause-syntax owner scopes uniqueness per file (`shared/definitions/contract-clause-definitions.md:13`); the real break is the pointer stanza violating the file's one-to-one `C-N`↔test promise (`:8`); the rule stays reachable as C-11; the accountant never resolves cross-file and the implement gate never runs it. [T4]

**Lessons**: legacy `md-heading` clause form lets a pointer stanza become a clause (new contracts must use `md-bold-closed`); `(file, id)` is the accountant's identity, so duplicate ids split the universe.

## ebbbcf14 — 2026-11-09 — Post-merge audit worker W4: stale `.specify/goal` surface

**Findings**: 630 lines / 276 tracked files; LIVE 150 (framework 56, tests 33, docs 4, memory registries 22, team defs 35); own line 092 = 129; retired vocabulary 284 lines, live-stale few; engine `ARCHIVE_DIRNAME = ".specify/anchoring"` (`goal-utils.py:59`) with no legacy fallback; `build-summary-input.py:1054` writes anchoring while integration tests still assert goal (stale tests). [T2]

**Anomaly**: `specs/093-concurrency-by-default` and `state/093-*` absent from merged tree (only trace `.specify/state/092-goal-team-parallel.md:63`); `092` double-booked with `specs/092-non-disposable` → renumber to 094 must resolve both.

## cf3fe393 — 2026-11-09 — Fork verification worker VB for 094 (analyze round 4)

**Verdict**: VB: FAIL (all LOW). Six gates green (validate-requirements, account-clause-coverage fr 43/43, validate-tasks 0/1 disclosed, decision-tensions 7/0, pre-analyze ×3, decomposition 43/83); all M/L closures verified closed; open: registry still says "repair round 3 进行中" (`features.md:101`, `features/094.md:59`), `tasks.md:483` points at wrong evidence file, `research.md:115` "44 ids" vs 46, renumber residue incl. `.specify/.tmp/s092/` fixture roots. [T2][T3]

**Anomaly**: D4 write-home vocabulary split wider than declared — task rows T037/T073/T081, quickstart, data-model still prescribe `.specify/goal/` while FR-007/plan say `.specify/anchoring/`, and C-31 states the old path as normative.

## a9bcef84 — 2026-11-09 — Coaching trainee run: `/speckit.status` (no-arg)

**Outcome**: digest printed verbatim, exit 0; wrap-up: run-determination `skipped: simple-unit`; exec-quant record written (`records/20261109T114523532976Z-5945721e.json`); feedback skipped (trivial); threshold not surfaced; closeout strategy `ask` → sequence presented, nothing executed (receipt none, no commit/merge/push; targets github/gitlab/gitee, `origin` excluded). [T5]

**Anomaly (in-passing repair)**: captured output in bare `/tmp` (violates temp-directory-discipline); files deleted once recorded.

**Lesson**: interactive no-arg digest; `status-digest.py` exit 3 = "nothing-running" is a correct answer, not failure. Registry gap: active 093/094 lines were never registered in the Line Registry.

## dc1d9296 — 2026-11-09 — Read-only test-suite auditor, chunk 2

**Results**: 1,267 tests / 75 modules → 1,238 keep / 19 rework / 10 delete-candidate; wall 297.7 s (92 s in three real-tree full scans). Top delete candidates: `test_non_regression_064.py::test_ng_13_planned_test_matrix_present` (test-about-tests), `ng_08_mirror_no_new_drift` (duplicates `test_scripts_distribution_parity.py`, 3 subprocess runs), `test_sanitize_retention_lane.py::test_retention_action_set_is_closed` (duplicate args-manifest), one-source-of-truth mirror parity family (duplicate of `test_mirror_parity_suite.py`), `ng_03_migration_content_preserved` (completed-feature pin). [T5][T4]

**Product defect found**: `test_scope_resolution.py` drives retired `--scope global/spec`; engine closed set is now `goal/teams/auto` but `sdd-route.py` still calls the old value (19 tests correctly detect it). Tautologies: `... or True`, `f(x) == f(x)`. Parallel flake: `test_c15_the_engine_writes_nothing_inside_the_repository` (whole-repo git status + SHA-256 sweep under `-n auto`).

**Anomaly**: concurrent run wrote tracked `.specify/memory/trigger/index.json` at 19:48:54 (session `sman-2`).

## 302477d1 — 2026-11-09 — Consolidation reviewer G4 (9 spec entries)

**Verdicts**: keep 8 | merge 0 | archive 1 (`046-browser-site-memory`) | delete 0; rollback note = git history. [T3][T5]

**Findings**: only 2/9 entries bind to matching registry IDs (`051`, `079`); `030-summarize-project` has no registry row at all; registry numbering offset from spec-dir numbering (029→row 031, 080→row 062, 027←036, 037←049, 043←039, 048←046); the 2026-08-13 `export-session → archive-session` rename never reached registry row 043, `features/043.md`, or spec 039.

## 2a7e498f — 2026-11-09 — Acceptance reality check (ARC) for 094

**Verdict**: ACCEPT sustained at `19003b613`; closure `final_path pass=8 blocked=0`; gates reproduce recorded readings; SC-003 16 receipts (8 goal + 8 teams) verified end-to-end, SC-002 4 passed, SC-010 guard 44 passed. [T4][T3]

**Anomaly**: SC-010 claimed `pass` overclaims — its own post-disposal contract reading exits 1 with 86 failing ids (51 new vs 46-id baseline) against "whole contract suite all green"; no ratified narrowing (R1/R2 cover SC-003/SC-001) → honest status `partial`. Registry `Planned` acceptable only pre-transition; `Planned → Implemented` is owed before review can record Ready-for-Review (no `Planned → Ready for Review` transition exists).

## a4475aa8 — 2026-11-10 — improve study-code (coaching optimization run), P-1..P-4 applied

**Decisions**: `$STUDY_DIR` fallback ladder (default → `.specify/.tmp/study-code/` → `~/tmp/study-code/`, chosen root recorded in `strip-manifest.md`); Step-1 source-integrity preflight (`git fsck --no-dangling` + refs/index readability; on failure `cp -a` materialize + record commit hash); UML backend degradation branch explicit (3 fallback outputs + note format). [T1]

**Gates**: shape 2528→2782/5000 (+254), redline PASS, contract suite 3 failed/80 passed with failure NAMES identical to baseline, `sync-mirrors` write+check exit 0 (426 files byte-identical); added commands runtime-validated on healthy and corrupted scratch repos.

**Anomaly**: pre-existing merge in progress (`.git/MERGE_HEAD` = `2344a1036`) plus concurrent `hist-wave1` fork writing the same tree — `.specify/skills/internal/create-team/SKILL.md` flipped `UU` → `M.` mid-run; left untouched.

## 48099f17 — 2026-11-10 — Giant multi-line session: sdd-* archiving, 091 closeout, fork model, test governance, 093/094, history five-thread wave

**Decisions & rationale**
- sdd-* artifacts: `sdd-house-keeping` reports → `.specify/memory/housekeeping/<UTC-ts>-<mode>.yaml`; `sdd-loop-driver` local briefs → `<repo>/.specify/.tmp/sdd-loop/tmp/<line_id>/`; `sdd-project-setup` unchanged; root YAMLs `git mv`ed; guard tests added. [T1][T5]
- Git closeout (feature 091): `.specify/workflow/git.md` gains `Closeout` + `Closeout remotes` (default `ask`); `shared/workflow/artifact-commit-step.md` gains Close-out step → `git-utils` scope-A `closeout` operation; one receipt per run; stop on first failure, no force-push. [T3][T5]
- **Fork model mandatory**: qodercli is single-process/single-CPU; internal in-process subagents under concurrency are a stability-bad option (host restart killed all four, CPU saturation). Carriers: fork = `stage-runner.sh` + `qodercli -w <repo> --permission-mode auto -p` (stdin, stream-json, pid/status/heartbeat/live-log, sentinel last line, detached) or subprocess for heterogeneous CLIs. 192 cores. 093 carries the correction (FR-034 analysis N workers, FR-035 fork/subprocess). [T1][T2]
- Test entry: ALL framework test runs MUST use `scripts/bash/run-tests.sh` (xdist `-n <effective> --dist load`); raw `python3 -m pytest` forbidden (FR-036 + guard `test_test_entry_guard.py`). [T1][T5]
- >10 s tests (8 measured) → opt-in `slow` marker (user choice over deletion); full suite measured 8184 passed / 46.08 s (parallel) vs 10+ min bare single-process.
- 092→094 renumber (trunk owns 092 = Non-Disposable pointer; 094 archived rename); `.specify/goal`→`.specify/anchoring` reconciliation; registry 093 = **Blocked** on closure block (block never becomes completed). [T2][T3]
- Consolidation: archive-not-delete into `.specify/archive/specs/` + `CONSOLIDATION-LEDGER.md` (11 dirs: 003, 007, 008, 017, 022, 046, 054, 066, 069a, 069b, 092). [T3]
- History five-thread campaign: Step B = `group`; G2 false-closed-set CLOSED 10/10 (`22913ad01`, open 918→908); G4 9 live bindings fixed, 96 kept open by owner-page judgement (`1acc58bad`); G1 BLOCKED — exemption mechanism never consumed by `class_deferral_marker` and E-3 fact shape conflicts with declaration schema (P1/P2 probes); G5 BLOCKED 0/52 — closure-verdict input contract postdates 51 dated specs, refused to fabricate measurement ladders (`ce5d38f67`); G3 736 classified (153 live-fixable / 583 dated-or-removed) (`513c05be6`), Wave 5 fixing live set. [T3][T4][T5]
- `status-digest.py`: `--format auto|text|json|table`; TTY→table, non-TTY kv byte-identical (088 feature; +3 tests). [T5]
- `coaching-skills`: command-type Trainee supported; `<work>` OPTIONAL; executor kind resolved by scanning BOTH lists, leading `/` is not a discriminator; cross-kind ambiguity fails closed; details in `references/trainee-resolution.md` + `nested-runs.md` (C-1/C-1b tests). [T1]
- `study-code`: 5 steps strip-repo / outline-code / outline-docs / deep-study / report (indexable report with anchors + lookup guide); moved internal→external. [T1]
- dsh-superagent-prototype subtraction: 95 files / 21,756 deletions (commit `a27b07f`, rollback `8c32a9d`); root-owned repo → `sudo git -c safe.directory`, never global config.

**Lessons / pitfalls**
- Detached forks survive host restart; in-process agents do not. Monitor dedup glob `status-*.seen` self-matched → empty event chain; use a separate `.seen` dir.
- Worktree presence contaminates tree-scanning tests (isomorphism duplicates) — clean before closure runs; `merge-tree` misses modify/delete; mirror conflicts resolved by projecting source then `sync-mirrors --check`.
- `[green:]` has two conflicting structural definitions (`F-093-004`); `goal-utils.py` actions unowned by any row produced cross-package red tests (package-graph gap → `enginefix` + T084/T085).
- Parallel lines must be worktree-isolated: 092 tasks commit landed on the 093 branch. Stage by explicit pathspec (broad `git add` risked in-flight fork artifacts).
- `run-tests.sh` tail captured the serial mini-pass — capture full log and grep the parallel summary. Bulk string replacement missed Path-join forms (`ROOT/"skills"/...`).
- R-36a pre-existing 16 ids A/B-proven and excluded from GATE-1; review fix loop via 3 worktree packages integrated zero-conflict.

**Unfinished / TODO**
- Five-thread distillation 119 qoder sessions → `05-agents-skills-tools.md` … `09-memory-state.md` + README/00/manifest (this batch is part of it).
- G1/G5 mechanism repair (exemption channel wiring; dated-record class ruling; E-3 fact vs schema).
- 093 line Blocked (SC-006 `not_evaluated`, closure block); slow-test opt-in + audit deletion triage pending; L-03 team-name residual; all commits unpushed at session end (`513c05be6` + waves).

---

## Per-thread index

| Thread | Sessions |
|---|---|
| **T1 agents→skills→tools** | e059c728 (render-agents, registration chain, seats); 6b6a829d (F1–F8 targets); a4475aa8 (study-code improvement); 48099f17 (fork model, test-entry rule, coaching executor kind, study-code 5 steps, sdd-* curation) |
| **T2 anchoring→goal→team** | 75ced50f (goal+team create); ebbbcf14 (goal→anchoring rename audit); cf3fe393 (D4 vocabulary split); 48099f17 (092→094 renumber, registry Blocked, 093/094 lines) |
| **T3 archive+history+session** | e059c728 (commit pollution, 055 merge, feedback packaging); 08e0989e (session records); b15cd656 (source-requirement dated archive); d22e136f (review registry gap); 840faac8 (history manifest single-owner); cf3fe393 (registry statuses); 302477d1 (consolidation, export-session rename); 2a7e498f (registry transition); 48099f17 (closeout, archive-not-delete, history waves, manifests) |
| **T4 derive+review+interview** | d22e136f (review, validator discipline); 6b6a829d (analyze gate); aae40c3f + 94c3fd85 (finding validators); dc1d9296 (test audit); 2a7e498f (ARC overclaim); 48099f17 (review fix waves, closure verdicts, history Step A/B) |
| **T5 memory+state** | 26940d66 (exec-quant record); 840faac8 (per-entry stores, derived index); a9bcef84 (status/records/closeout ask); cf3fe393 (registry drift); 302477d1 (registry numbering); 48099f17 (state spines, trigger/index.json, exec-quant, retention) |

**Coverage**: 18/18 sessions distilled; 0 skipped.

**Anomaly line**: no anomaly — all 18 work files read in full (large sessions 48099f17 and e059c728 read in chunks); no truncation, no skipped session.
