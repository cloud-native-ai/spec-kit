# History distillation — batch 2 (18 sessions)

Source: `.specify/.tmp/history-batches/batch-2.txt`. Processed 18/18; **skipped: none**.
Dimensions per session: D=decision+rathionale (incl. abandoned), L=lesson/pitfall, U=unfinished/TODO, F=key interaction flow, C=user↔model conflict. Thread tags in brackets.

## 7896e937 — 2026-10-06 — goal `command-logic-as-classified-skills` + serial team
- D: one goal (not two); annotation names `internal`/`external` as identifiers only; criteria 0→1 ("command 中只包含该调用哪些 skill…细节都在 skill 中"); T-001..T-003 = three layers, S1→S2→S3 progression moved to team plan; boundary excludes annotation-driven differentiated handling; `focus_target` deliberately unset — a `done` target would block later runs via run-checks check 3. [T1,T2]
- L: GD-3 only lexical conjunction match — green ≠ evidence; Target restatement guard compares normalized literal equality only (`goal-utils.py:693-704`) → paraphrased restatement is a blind check; `validate` stays green through a conceptual MUST breach; Targets have no edit action (drop + new ID, IDs never reused); `goal-utils.py` has no `boundary` action, so Boundaries are create-only; `verify-territory-disjoint.py` sees only same-`goal_slug` teams → cross-goal write contention invisible; create-team seat templates not installed in host registry → all seats virtual-dispatch (`general-purpose`), no isolation. [T1,T2]
- L (audit round): 16 findings — carve-out (`templates/commands/improve.md`) missing from stage briefs; asserted pre-alignment contradicts target text (missing 输入和产出 clause); one-sided forward conflict; mirror/regen paths (`sync-mirrors.py`, `.qoder/commands/**`) outside write face; invariants "every stage" only on 2/5 gates; S2b blind (no coverage/cumulative clause); T-001 could close without verified annotations; glossary真源 pointer cycle; criteria copied twice while claiming pointer-only. [T1,T2]
- U: `boundary` engine action still missing; master commit `aefa82b5` diverged from declared short-lived-branch workflow; term confirmed later (glossary count 118). [T2,T3]
- F: goal interview → external-session audit → "全部执行" 13 fixes → user ruling "读法①不冲突" → `/speckit.instructions` no-op → commit. [T2,T3]
- C: model twice misjudged (S1⊂S3; objective excludes annotation) and retracted on user evidence; predicted restatement rejection disproven by measurement. [T2]

## 86dd0ae8 — 2026-10-12 — skill-layer install separation, five-stage serial run
- D: two-layer layout `skills/{external 17, internal 15}`; references rewritten to source form `skills/external/<n>/…` | `skills/internal/<n>/…`; G1 forbidden-path touch → verifier CONDITIONAL-PASS → Meta modify ruling authorizes layered migration; T1 closed by deleting `clarify.md` `skills:[study-project]` (by-name→by-path list = 0); new goal `post-refactor-mechanism-integrity` + T-001; F1 migration before internal copy, F2 remove stale flat copies (name-gate protects user skills), F3 upgrade-sim regression test. [T1,T2]
- L: consumer upgrade break `migrated 0 … kept 15 (nested target exists)` — function-level tests masked by "no nested" start state; `git diff BASE..HEAD` window means `confirmation_gates_sweep.py` c7 red since `09bd40a9` (+`cb483a1b`) — "pre-existing baseline" only true in A/B sense; register.md is hand-maintained with **no engine and no guard** — silent misses; 24 dispatches → 8 hit 24-turn cap, resume + Lead-takeover; `| pipe` masked regen exit 1; `cp` interactive alias silently refused overwrites; vacuous `skills/*/SKILL.md` glob (anti-vacuous sentinel added); `maxdepth 2` vs 3 validation depth; git `AM` vs `RM` pathspec artifact. [T1,T3,T5]
- U: 4 root-owned `/tmp/specify-skills-*` dirs; T-001 `pending_approval` awaiting human; register "reference⇒registration" guard proposed, not built. [T2,T5]
- F: S-B rehome → S-C toolchain → S-D tests (A=`1F/3491P`, B=`1F/3523P`, zero new) → S-E runtime verify → 2 commits `1adfa49a`+`766088f2`, push gitee/github/gitlab, `origin`=upstream not pushed. [T1,T3]
- C: none material; user corrected only via dispatch scope (no adjudications). [T2]

## a3d3ec0a — 2026-10-15 — draw-diagram interactive (iteration team) + feedback batch 5
- D: iteration threshold 0.8 / max 5 / regression 2; gen-1 converged at 0.885; adopted only after bounded convergence round (score-pass ≠ deliverable); deliverables 7 files `skills/external/draw-diagram/`, interactivity_intent (3 tiers × 8 forms, animation excluded), D7 interactive-web contract, routing tie-break `interactive-html`/`interactive-dashboard`. [T1,T2]
- L: verifier hit 12-turn cap zero artifacts → re-dispatch wider vehicle (fixed turn budget too small for execute+score); `cp` alias again silently no-op (diff caught it); summary subagent stream error but deliverable was complete → verify then continue; `.git` 57 root-owned residues, 5 object buckets — fix = mv aside → rebuild → copy blobs (lesson §二十), `.root-bak` inert but undeletable. [T1,T5]
- L (Path A): 5 bundles/77 items + local 33 = 94 dedup; 159 verdicts STILL-VALID 93/PARTIAL 21/ALREADY-FIXED 16/NOT-OURS 15/ack 14; `generate-instructions.sh` references undefined `gitignore_add_pattern`/`git_repo_root` (contract green only via env inheritance); Wrap-up embeds missing `--run-id` (15-entry cluster); `instructions.md` 33898 B over budget with no legal R1/R2 candidate; `rm` alias silently refused deletion (lesson §五 rm variant, previously only cp); introspection schema C-7 needs `(成立|…)` annotations; `--disposition open` truncation defect M-1. [T1,T3,T5]
- U: F-02 budget ruling (raise / add R3 / trim); 4 root-owned /tmp dirs. [T1]
- F: team run → package `feedback-20261015T061707Z.zip` (zero network) → commits `195f1f56`/merge `6892edef`/push ×3 → `/speckit.feedback console`≈consume → batch 5 (`4c0ef162`, then `cd78c0e6`/`455f2169`). [T3,T5]
- C: `console` read as near-miss for consume, disclosed. [T3]

## df0a6be3 — 2026-10-16 — unattended review stage, feature 059
- D: review = process critique only; same-author gate not triggered (all 9 commits predate session); P0=0 (verification wave empty), P1=4/P2=4. [T4]
- L: propagation-order doc contradicts engine — `compile-embeds` reads `.specify` mirror registry (`PROBE_DEFS_REL` L130), so documented compile-first order silently compiles stale faces; registration obligation has two owners (`feature-integration.md` vs create-requirements SKILL); implement close-out leaves corrections only in notes/ while contracts/quickstart keep wrong facts (F1, 7 instances); `_ENGINE_SIBLINGS` at L619 not L620-621; unpushed HEAD ⇒ no URL cite, use absolute paths + `git show`; `--run-id` required; exec-quant evidence flags want file paths — omit to record honest `not_evaluated`. [T1,T3,T4]
- U: F1 write-back obligation, F2 order fix, F3 ownership convergence (later features). [T1,T4]
- F: context capture → artifact load → mechanical premise checks → report → commit `0afc8a1c` (review.md only) → wrap-up. [T3,T4]
- C: none. [T4]

## 544f490f — 2026-10-19 — unattended PLAN, feature 062-humanize
- D: command classified **Simple** per 027 owner rule (a)(b)(c) → no command Wrap-up/probe unit, skill still registers `skill-humanize-wrapup`; 73 units = 23 Complex commands + 50 skills; 34 clauses C-1..C-34, FR 28/28; mirrors keep spec-local vs runtime paths distinct. [T1,T3]
- L: `compile-embeds --unit` does NOT scope — `--write` rewrites all 73 faces ⇒ relative Verify only; pre-existing baselines: mirror 209 DIFF, tests 71F/3929P, compile 73/73 old-fingerprint drift; `*.log` gitignore forced `baseline-test-run.txt` rename; blind SC count 17 vs dedup 10 (`Measurement Sources` rows matched); `extract_clauses()` returns ids, `clause_blocks()` returns bodies; sync form `sync-mirrors.py --write --only <prefix>` (repeatable); two-hats edit target is `shared/…`, not `.specify/shared/…`; Wrap-up embeds still missing `--run-id`/`--complexity`/`--review`. [T1,T3]
- U: `## Same-Author Scoring Record` placeholder noted for fill; scorer findings (mirror-touched pair line 181, delivery count) pending correction at checkpoint. [T4]
- F: setup → explore → Phase 1 artifacts → gates → same-author scorer (12 findings, all resolved as corrections) → commit `548c9b18` → `PLAN-DONE` with 3 ANOMALY lines. [T3,T4]
- C: model's initial Complex design self-corrected to Simple; disclosure kept. [T1]

## 62a1b0b1 — 2026-10-19 — tasks propagation after analyze HIGH=2, feature 062
- D: fold repairs into existing 33 rows (never renumber); 35 green claims / 35 distinct clauses, C-35 claimed once by T029; status stays Planned. [T3,T4]
- L: `validate-tasks.py` parallel-safe heuristic treats `URL/版本号` as file paths → reword to Chinese enumerations; validator warnings are adjudications, not deletions; registry counts must be program-derived (30 rules/35 clauses/FR 29/SC 11); requirements authority moved from `/tmp/sdd-humanize/brief.md` to dated record `notes/source-requirement.md`. [T3,T4]
- U: none. [T3]
- F: read brief/log → edit tasks+registry → validator PASS 0/0 → commit `c831e7ec` → `TASKS-DONE`. [T3]
- C: none; all repairs accepted. [T4]

## 99912504 — 2026-10-19 — clarify Mode A, feature 063-review-p1-governance
- D: new Feature 063 (candidates 012/028/053/056/062 don't cover F1–F8 cross-command bundle); FR-006→`create-checklist/SKILL.md`, FR-008→`implement-feature/SKILL.md` §Step 2; malformed citation group kept (silent handling would reintroduce reading dependence). [T3,T5]
- L: RP-1 near-miss typo 花括号→括号; RP-6 default completion — `/speckit.clarify` is Complex (carries Wrap-up); first `simple` call skipped and wrote nothing, same run-id rerun with `complex` is legal under E1 lock; full-width comma broke exact-match edit; engine params: `--run-id`/`--complexity`, `--points`, `--review`; feature index row reads huge → targeted reads only. [T1,T3,T5]
- U: none; commits `ea79ceda` + `c5b3d1fc` (separate `chore(archive)` precedent `5c4840db`). [T3]
- F: context → 12-class coverage scan (4 Partial/Missing) → 3 self-adjudicated questions → write-back → registry bind → validate → commit. [T3,T5]
- C: none; E1/E2 preserved as recorded. [T5]

## d01a3852 — 2026-10-20 — instructions refresh carries REC- into live file (063 C-12)
- D: `/speckit.instructions` (manage-instructions Action 5) is the content-refresh owner; `generate-instructions.sh` stays additive-only (C-2 pinned); one-line edit exactly matching template. [T1,T3]
- L: permission classifier read "do not extend" as "do not run" → documented Warning-level fallback (manual backup `instructions.md-2026-10-20-003045`, programmatic snapshot reproduction); A/B by stash: `-m contract` 45 failures identical both sides, untagged live-file subset 13 pre-existing/1 fixed/0 new; red→green C-12 test 1F/9P→12P; budget 37443/32768 B with no R1/R2 candidates → pending; E1 idempotency lock rejects artifact-correctness upsert (first record final); `--user-turn-class` belongs to `settle` not `determine`. [T1,T3,T5]
- U: budget overrun; `## Fact, Correctness & Logic Checks` 403 B behind template; C-12 docstring still says "through the generator". [T1]
- F: recall → blocked setup fallback → edit → validation → suite A/B → commit `a8c3c1f0` → `INSTRUCTIONS-DONE`. [T3,T5]
- C: none; classifier block disclosed as ANOMALY. [T3]

## c218f73c — 2026-10-28 — review+code-review integration (071) and client self-improvement (072)
- D: `/speckit.review` = fixed order process segment (`review-sdd-process`) then code segment (`code-review`), separate reports `review.md`/`code-review.md`, severities not merged; code base resolution explicit > parent of requirements first commit > trunk merge-base, head pinned; lifecycle gate `Implemented → Ready for Review` single owner (feature-details template); 072 reuses feedback store via `kind`/`slice`/`custom:owner/name` (no second engine), adds code-review 5th step `capture` (pointer only), read-only `client-metrics` (zero denominator ⇒ `not-evaluated`). [T1,T4]
- L: probe catalog reachability broken in client layout (repo-root-relative vs `.specify/` fallback) — fixed per engine doctrine + negative test; C-56 surface guard missed `.specify/memory/register.md` and skill mirrors; `git %h` abbreviation drifts 8→9 as repo grows → pin `--abbrev=8`; merge conflict resolution first pass confused remote half with HEAD (`--conflict=merge` recovery); `tmp/` reappeared because `318ad7a2e` removed the `tmp/` ignore rule — new discipline forbids repo-root tmp, scratch under `.specify/.tmp/sdd-loop/`; fast-forward exposed trunk-interaction pins: 072 guard needs FEATURE_HEAD anchor, C-5 whitelist update, C-6 "exactly one line"→"zero deletion + 7 additive". [T1,T5]
- U: REC-071-*/REC-072-* backlog; no push without authorization. [T1,T3]
- F: U0–U6 driver over two lines → review/closure → commit+merge `9b7f1d62a` → push ×3 → tmp relocation (`~/tmp/spec-kit/legacy-root-tmp-2026-10-28/`) → ff `252735f0e` + fixes `3f102dc0f` → push ×3. [T3,T5]
- C: user demanded root-cause explanation for `tmp/`; model relocated but did not delete. [T5]

## fa711d34 — 2026-11-05 — independent validator rejects H-07 (spec 082)
- D: census "two load-bearing decisions" is complete — owner threshold `.specify/shared/guidelines/decision-tension.md:86-89` (4 triggers: irreversible, cross-team, blast radius, constitution MUST) places no burden on the plan to prove per-decision negatives. [T4]
- L: the two named candidates fail all triggers — packaged `shared/` distribution is a verified premise (EP-002/T030/T033), XIX/XVIII numbering is a ratified requirements decision (A4) and measurement-derived; "not shown below threshold" is not a defect; structural validator green ≠ semantic census. [T4]
- U: none. [T4]
- F: read threshold → apply to plan → reject with `evidence_supported` / `evidence_not_supported`. [T4]
- C: none (adversarial finding rejected). [T4]

## 0f63f87a — 2026-11-05 — interview "不言自明 (Self-explanatory)" → Feature 082 full SDD chain → feedback digest
- D: rename 望文生义→不言自明/Self-explanatory; user-perspective principle, ceiling "直接看到"/floor "一个简单命令", floor suffices; SHOULD as best-practice entry; dimension order user explicit > framework rule > one at a time; truth stays in `goal.md` frontmatter, path is projection reconciled by `/speckit.sanitize` (eventual consistency); no preventive optimization; migration via reconcile + impact assessment (references/workload/compat) with user decision; deliverables split definitions/guidelines/workflow + docs pointer; two-hats output mapping (`/speckit.constitution`→constitution, `/speckit.instructions`→instructions). [T4,T5]
- L: `flow-class` declaration trailing space → `declaration-malformed`; execution-class spec needs `## Runtime Stack & Dependency Ownership`; `split-required` 53>40 with 12 FR unsplittable (8–30 FR/slice) → user-authorized framework change `TASK_CEILING`/`TASK_MAX` 40→60 (`edd18472`,`24c27f81`); T023 budget must be 1024-multiple AND ≥1024 B headroom (34816, not 33792); T024 live rebuild must follow T026 mirror sync (generator reads runtime mirrors); T031 arithmetic 65→65 not 65→68; `*.log` again forced `.txt`; `audit-test-budget.py` needs JSONL fence + per-stage `.jsonl`; plan subagent wrote `.specify/shared/` mirror while claiming not to; 120-turn caps on plan/implement/review; `sync-mirrors --only skills` misses `skills/internal`; `feedback-utils.py --action probes` no longer exists; `list --disposition open` defaults to 5 → `--limit 0` (true open = 136); introspection schema needs sequential F-ids, unique membership, one disposition line. [T1,T3,T5]
- U: `OI-082-01` `/speckit.improve` wiring open; Review P2 F2–F5 + RECs; backlog 131 open / 7 open-unverified / 5 carried-by-spec-053; 25 baseline-inherited reds. [T1,T3]
- F: 6-round interview (24 decisions) → requirements → clarify (4 Q, Feature 082, budget raise, runtime pointers) → driver U0–U6 (10 implement parts) → review P0=0/P1=1 fixed/P2=4 → closure 25F/7198P (1 baseline red→green) → ff `0ae4c3ea` → feedback Path A (11 findings F-01..F-11) → commit `543aff40`, merge `1286f37f`, push ×3. [T3,T4,T5]
- C: user authorized a framework threshold change instead of slicing; model disclosed tension D10(x)SHOULD vs D14 apply. [T1,T5]

## 63f60627 — 2026-11-09 — repair writer R1, 094-goal-team-parallel round 3
- D: archive page C-53/C-54 → C-112/C-113, namespace C-1…C-113, 113 markers = 113 ids (pages 30/24/18/20/21); GATE-6 rewritten with true pre-freeze reading (fr 43/43, clause-uncovered 599/1 beyond = 085#C-014, unparsable 115/1 parse-doubt = 067 runner-contract, delta 1); baseline re-frozen once (598→599); FR trace re-derived from task quotes (drift 0). [T2,T4]
- L: `--freeze` prints only (redirect into baseline file); upstream merge after freeze adds new names — freeze covers exactly one name, parse-doubt is not a coverage item; green-partition export contradicted rows' own tags (C-30→T067/C-54-55→T081 vs T005/T082) — corrected; territory split R1/R2 disjoint, writer runs only own-file gates. [T2,T4]
- U: 067 parse-doubt remains named warning; T015 duplicate evidence fragment flagged not touched. [T4]
- F: findings → verify anchors → edits → validate-tasks 0E/1W → freeze → post-freeze green → ledger `repair-r1.md` → `R1-DONE`. [T3,T4]
- C: none; one in-passing correction disclosed. [T4]

## 03be6910 — 2026-11-09 — fix writer W2, 094 round 4
- D: canonical Probe denominators per measured tree: probe form goal 9/team 8 = 17, full census goal 9/team 10 = 19 (two one-level team files 088/092); history dated (plan 7/7=14, tasks 8/8=16); `.specify/anchoring` paths; `Total Features` 87→88. [T2,T5]
- L: dispatch premise "9+9 per W3" was a directory count (`ls -d .specify/specs/*/team`), not a definition-file count — re-measure dispatch premises; team identity naming follows sibling convention `SDD Temporary Team <id>`; 092 residue in titles/identity lines must be swept; 44→46 ids dated correction. [T2,T3]
- U: none. [T4]
- F: read notes → measure tree → 10 edits → validate-requirements ok → fix record `notes/analyze-round4/fix-w2.md` → `W2-DONE`. [T3]
- C: none; ANOMALY on premise. [T2]

## fe7dafff — 2026-11-09 — read-only test-suite audit, chunk 1
- D: audit criteria = correctness (unfalsifiable assertions, removed surfaces, non-repeatable deps), necessity (duplicates named), slow-by-construction. [T1,T4]
- L: 1351 tests → keep 1333/rework 12/delete 6; `test_feedback_skill_conformance.py` source-side `skills/*/SKILL.md` glob matches 0 of 54 (nested layout) → green by vacuity (mirror side works); tests hashing literals they wrote; duplicate face-table checks; meta-test counting its own file's names; name promises baseline comparison it never performs. [T1]
- U: chunks 2+ not in this session; rework/delete candidates not executed here. [T4]
- F: chunk read → mechanical scan → batch reads → report `audit-1.md` → `AUDIT-1-DONE`. [T4]
- C: none. [T1]

## db0b0717 — 2026-11-09 — `/speckit.history` trainee run, gate withheld
- D: four-stage seam 回顾→设计→用户确认→执行; Step A.3 requires byte-identical before/after snapshot before Step B; inherited dated `none-of` decision for the same 861-entry set (commit `3d52ea09a`) — do not re-ask; distillation set uncovered → not guessed. [T3,T5]
- L: `collect-history.sh` tool autodetect null → identify via `QODER_CLI`/`QODER_PID`, `--tool qoder`; qoder store 104 pending sessions / ~211 MB, 0 overlap with claude-era manifest (16 entries, last 2026-08-15); 1.46 MB review JSON must be digested programmatically; seam diff attribution by mtime+git log shows external writers (trigger telemetry, coaching close-out). [T3,T5]
- U: 861 entries remain open/unconfirmed; distillation unconfirmed; wrap-up chain withheld (zero-write boundary). [T3]
- F: locate → snapshot #1 → `non-disposable-check.py --json` (861 entries: orphan 661/renumber 120/status 54/false-closed 10/deferral 16) → design → snapshot #2 mismatch → stop before Step B. [T3]
- C: none; nothing self-approved. [T3]

## 61298504 — 2026-11-09 — read-only spec consolidation reviewer G2
- D: verdicts keep 11 / merge 054→040 / archive 4 (007,008,017,022) / delete 0; archive is established convention; rollback = `git checkout c4605da6a -- <path>`. [T3,T5]
- L: registry row IDs ≠ spec dir numbers (registry 020→spec 006; detail files follow registry IDs); all 16 share top commit `c4605da6a` (2026-11-05 sanitize sweep) → git date is not a staleness signal; task counts polluted by legend text → anchor row pattern; 6/16 lack `verification.md`; 006/009 leave 10/13 tasks unchecked while registry+detail say Implemented — evidence gap, not delivery gap. [T3,T5]
- U: archive/merge actions not executed here. [T3]
- F: evidence gather → registry mapping → per-spec evidence → report `review-G2.md` → `REV-G2-DONE`. [T4,T5]
- C: none. [T5]

## 644a1597 — 2026-11-09 — review segments C+D for 094
- D: Segment C pass (P0=0/P1=1/P2=4); Segment D pass, no blocking, important=2 — consolidation left dangling normative pointers to archived 069b/092 specs, and `create`→`bind` is unreachable because `bind` requires a pre-existing binding (empirically reproduced). [T2,T4]
- L: closure claims reproducible: accept 8/8, 16/16 receipts, 34/34 bindings, 87 disposal tests, failing-set arithmetic 152−24+58=186; P1 = T016–T019 closed `[x]` with absent module/write and falsified evidence pointers (false closure, the class later fixed by repair waves); test-intent preservation verified across six rewritten 085 modules; repair-wave suite run mutated `.specify/memory/trigger/index.json` via nested-worktree self-location trap → judge committed HEAD only. [T2,T4,T5]
- U: 3 dangling evidence pointers; P2s (DoD-7 list, T079 names, mutation pointers, un-dogfooded handoff). [T4]
- F: read method → verify artifacts file-by-file → independent smoke → code diff review → single notes write `review-implementation-code.md` → `RV2-DONE`. [T4]
- C: none. [T4]

## dd3b7b4e — 2026-11-10 — Wave 2 G5 status-unreadable: BLOCKED, 0/52
- D: G5 lands BLOCKED — 0 of 52 closed (`not_closed.open` 908→908; class 52→52, entry ids unchanged); no status fixpoint for 090 (Implemented→block; Blocked/Planned/Draft→accept; Completed/Relocated false; 116 open rows arrived with the Implemented flip in `8edd955d1`). [T3,T5]
- L: class reading = registry-status × closure-verdict; 51/52 produce no verdict (checker input contract postdates them): 43 missing `**Path**:` markers (AS-01 — per C-804 that reading belongs to `validate-requirements.py`), 7 lack closure inputs, 1 (080) row keyed 062 vs dir 080; 016 scratch retrofit probe still `block` (`blocked-without-measurement-ladder: SC-005`); 17 specs would need never-taken ladder measurements, 20 would need new smoke + per-SC judgments (semantic decisions; subagents forbidden). [T3,T5]
- U: needs an engine-side C-804 decision or 51-spec schema migration — left open, not fabricated. [T3]
- F: read owner/predicate → fresh baseline → per-entry analysis → cascade probe → no tracked edits → E-7 evidence `history-execute-g5.txt` + before/after JSON → `HIST-W2-DONE`. [T3]
- C: none; Fast-Fail block surfaced instead of repairing. [T3]

---

## Per-thread index

- **T1 agents→skills→tools**: 7896e937 (command→skill goal, seat dispatch), 86dd0ae8 (two-layer skills, probe/engine), a3d3ec0a (draw-diagram skill, feedback engine), 544f490f (command classification, Wrap-up compile), d01a3852 (instructions refresh), c218f73c (review/code-review skill, feedback channel), 0f63f87a (constitution/instructions integration, engine params), fe7dafff (skill-layout test vacuity), 644a1597 (goal-utils create→bind).
- **T2 anchoring→goal→team**: 7896e937 (goal+team create, Targets/boundary), 86dd0ae8 (post-refactor goal/team, T-001), 63f60627 + 03be6910 (094 goal-team repair), 644a1597 (create→bind gap).
- **T3 archive+history+session**: 7896e937 (terminology/commit), 86dd0ae8 (register/c7, run reports), a3d3ec0a (batch consume/commits), df0a6be3 (review artifact), 544f490f/62a1b0b1 (session-stage artifacts), 99912504 (clarify records), d01a3852 (records/idempotency), c218f73c (state spine), 0f63f87a (session/introspection), 03be6910 (dated corrections), db0b0717 (history seam), 61298504 (archive consolidation), dd3b7b4e (non-disposable evidence).
- **T4 derive+review+interview**: df0a6be3 (review), c218f73c (review integration), fa711d34 (validator), 0f63f87a (interview + review), 63f60627 (analyze repair), fe7dafff (test audit), 61298504 (consolidation review), 644a1597 (review C+D).
- **T5 memory+state**: 86dd0ae8 (register mechanism), a3d3ec0a (feedback store/backlog), 99912504 (feature registry/run-determination), d01a3852 (memory-record lock), c218f73c (trigger/state), 0f63f87a (feedback digest/backlog), 61298504 (registry consistency), 644a1597 (trigger index), dd3b7b4e (status state machine), db0b0717 (manifest).
