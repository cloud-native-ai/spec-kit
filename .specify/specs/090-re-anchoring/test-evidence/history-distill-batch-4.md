# History distillation — batch 4

Source: `.specify/.tmp/history-batches/batch-4.txt` (18 sessions). Read-only on `.specify/history/`;
this extract is the only write. Threads: **T1** agents→skills→tools · **T2** anchoring→goal→team ·
**T3** archive+history+session · **T4** derive+review+interview · **T5** memory+state.

## 9c57a1ed — 2026-10-08 — goal `session-driven-self-improvement` → team → achieved; ID Register
- **Decisions**: goal created via a 9-round interview, narrowed to “只建立 improve 流程, not perform improvement”; zero Targets (kept the 2026-09-16 “no phases in Goal” ruling); criteria = one unified `运行判定` over token/耗时/制品正确性/满意度, plus `achieved` as a deliberate human judgment. B1 name `运行判定 (Run Determination)` (avoid 断言/评估/判据/verdict/信号); B2 correctness split — only 制品正确性 (name-level failed-set difference empty + every green carries red-first/mutation evidence); B3 satisfaction rule kept minus the hedge. OI-1 `green_unproven` → `not_evaluated`; OI-9 finally `engine_nonzero_exit` only (the per-turn telemetry has a closed seven-key schema and cannot express an unresolved red).
- **Team**: serial; S1 contract 68,894 B → S2 engine `scripts/python/run-determination.py` (1,698 lines) + 1,742-line test (193 pass) → S3 passive wiring / S3b critique / S4 active → S5 verifier. Final run landed S3 (instructions 32,674/32,768, 94 B headroom), S4 `templates/commands/improve.md` (112-line thin shell) and S4-2 `skills/self-improvement/SKILL.md` (102 lines, first `classification: internal`); goal set `achieved` through `goal-utils.py`; team left read-only.
- **Critique-and-self-critique**: user overruled routing it to a separate spec (“适合当前的goal高度契合”); GD-3 confirmed it is a component. Landed `docs/concepts/critique-and-self-critique.md` (54 lines) + `shared/guidelines/critique-and-self-critique.md` (81 lines) and workflow step `SI-3C — Critique Before Dispatch` (after SI-3, before SI-4 — not between SI-1/SI-2, where no proposals exist). Output = one falsification attempt per proposed change, not a concern list.
- **Cross-goal collision**: `verify-territory-disjoint.py` compares write×write only; `forbidden` is never subtracted (`build-summary-input.py:608-609`), so two writers can hold one file while both reports are clean. Resolved by a `forbidden` entry plus territory narrowing; the schema-sanctioned resolution is machine-invisible.
- **ID Register**: user demanded all durable IDs live in one file → `## ID Register` ambient section in `templates/instructions-template.md` + `.specify/memory/register.md` backfilled (D1–D9, B1–B4, S1–S5/S3b, OI-1…OI-9, D-A/D-B, T-001…T-003, SI-0…SI-9, F-…), pointer rows only.
- **Agent-registration gap**: `render_agents_for_tool` is reachable only from `src/specify_cli/__init__.py:2283` (the `specify` CLI); the loader reads only `.specify/agents/{templates,instances}/`; `templates/commands/agents.md:25` still teaches retired symlinks; no Qoder IDE agent adaptation. `general-purpose` is the correct fallback; F-A02 dead letter had spread from the skill into the command template. The 054 spec (B1) was deferred to the backlog.
- **Lessons**: `interview-utils.py render` writes to stdout (use `--out`); YAML breaks on `确认门[禁控]` inside an unquoted flow scalar; `cp`/`mv`/`rm` aliased interactive silently no-op; whole-file staging carried a concurrent session's bytes (`70721de7` took 418 B); a full A/B overlapped a concurrent landing (7 new reds, 6 race-only); patch `.orig` files were copied by sync-mirrors; D-B was voided by one grep before dispatch (contract §5.0 already legal), which is the critique discipline working.
- **Key flow**: goal interview (D1↩D7) → team create → halted run (B1–B4) → S1 contract/S2 engine → feedback digest (17 entries) → S3b critique docs → S4 shell → S3/S4-2/S5 → goal `achieved`.
- **Unfinished**: 054 spec (B1) not authored; B2/B3 backlog verification not dispatched; `0206e021` not pushed; final wrap-up changes uncommitted.
- Tags: T1 T2 T5

## 8b32d7cd — 2026-10-12 — team run `command-logic-as-classified-skills`; init migration; sanitize lane
- **Decisions**: serial 5-seat team (team-supervisor Meta = sole canonical writer + regen engines; skill-author
  patches workspace-only; structure-aligner native; contract-checker independent verdict). Goal-based branch, all
  3 Targets open. S1 landed 20/20 skill packages in `skills/internal/` + `classification:` on 25 legacy SKILL.md
  (internal 14 / external 11; `self-improvement` untouchable; `coverage.allow` kept workspace per B2d). S2a/S2b
  46/46 judged, 8 patches (`archive-session` description, `draw-diagram` ungated `.specify` call, `manage-agents`
  stale `skill_id`). S3 thinned 25 command templates to frontmatter + lifecycle + thin delegation (−2,368 lines;
  agents.md 13001→3804 B); 123 contract failures were drift-guards pinning fat templates → rerouted, never weakened.
  Migration approach: add a sanitize lane rather than manual cleanup — C-22 legacy skill dirs (`LEGACY_SKILL_NAMES`
  33, archive not delete; apply `delete` refuses non-empty dirs), C-22 legacy `git-workflow.md`/`.specify/tools/`,
  C-23 flat-vs-`internal/` duplicates → archive, C-10 extended to `.qoder/skills`/`.claude/skills`.
  init gaps: xuanji-images `.specify/git-workflow.md`→`docs/git-workflow.md`, `.specify/tools/`→`.specify/memory/tools/`,
  user skills untouched; profiles orphan `analysis-project` manual archive + `safe.directory`; per-tool `specify init
  --here --force --ai <tool>`.
- **Lessons/pitfalls**: tests in `tests/contract/` without `@pytest.mark.contract` are never selected by `-m contract`
  (1532 deselected) — 23 S3 residues hid there; full marking proposed as its own campaign. `cp` aliased `cp -i`
  silently blocked overwrite (use `\cp -f`). cwd drifted into feature dirs; re-run from repo root. S0 ruling cited a
  `skills: [study-project]` frontmatter already gone — re-verify rulings against current text. Summary check-coherence
  WARN CG-ID "123" was a test-count false positive.
- **Unfinished/TODO**: `/speckit.docs` reconcile (command pages still describe fat templates); T-001/T-002/T-003
  `done` toggles with user; full contract-marker sweep (filed in feedback).
- **Key flow**: goal-based team run → 4×5 parallel skill-author batches → independent contract-checker gates →
  Meta landing + sync/regen → S2a/S2b → S3 thinning → A/B contract diff → report/ledger/summary refresh.
- **Conflicts**: user pushed against nothing here, but a C2 commit without pathspec swept another session's staged
  files; not pushed — `git reset --soft` + pathspec redo, disclosed. Divergence: rebased 8 commits onto gitlab/master
  `5c4bc367`, pushed three mirrors `5c4bc367..23617b8a`, origin read-only. Commits `3c61f7a3`, `a7b076e7`.
- Tags: T1 T2 T5

## 6fbbb89d — 2026-10-16 — 059 clarify (exec-quant recording)
- **Decisions**: Feature 059 unregistered → created `features.md` row + `features/059.md` Draft (Total 57→58);
  Related Feature binds to 059 itself (028/055/056 screened, no sibling). Engine name locked `exec-quant.py` (A5,
  zero collisions) so plan cannot reopen it. Coverage Resolved 2 / Clear 10 / Deferred 0 / Outstanding 0; validator
  exit 0; commit `c9a1e646` (4 files). FR-003 order contradiction fixed in passing (after the run-determination handler).
- **Lessons**: same-author gate does not fire when the artifact predates the session (`4166a5be`). Compiled Wrap-up
  faces lacked `--run-id/--complexity/--review`; supplied manually — fix belongs to the probe compile layer (feedback).
  Run determination recorded all four axes honestly as `not_evaluated`.
- **Unfinished/TODO**: `features.md` missing row 054 (noticed, out of scope); template parameter gap.
- **Key flow**: read brief + spec → same-author check → taxonomy scan → closed-question adjudication → registry
  backfill → commit → wrap-up engines (record `cp-…T031228Z`, feedback 37/10).
- **Conflicts**: none; upstream deviation disclosed (requirements session had not registered the feature).
- Tags: T1 T5

## 34080ca9 — 2026-10-19 — unified watch model + driver entry routing guard
- **Decisions**: root cause of false timeout — `pgrep -c` prints `0` then exits 1, so `$(pgrep -c …) || echo 0`
  yields `0\n0` and numeric compare fails. Completion is positive evidence only: exit record → sentinel → PID →
  heartbeat; silence/disappearance/pgrep-zero are not completion. State machine
  DONE/INCOMPLETE/ANOMALY/FAILED/DEAD/TIMEOUT/NO_SIGNAL/RUNNING with single destination U4/U5. Mechanism ladder:
  long-poll window (default) → host notification (supplement only; must not end driver session) → interval polling;
  window expiry returns RUNNING, only stage deadline yields TIMEOUT. Liveness via PID file + `kill -0` (start ticks,
  PID reuse, zombie); `pgrep` boolean fallback only. `scripts/watch-target.sh` (read-only, `--once`, `--self-test`
  16 cases; 4/4 e2e mock; 55 contract tests). Runner keeps pid/status/log/heartbeat + atomic exit record.
- **Lessons/pitfalls**: user conflict “为什么没有按照sdd流程进行,我是用的是sdd-loop-driver技能” — the model loaded
  `improve-skills` and edited directly, skipping U0–U6. Root cause was a missing entry-routing guard, fixed in the
  skill: U0 default resolution (cwd with `.specify/` → current repo; no remote params → local direct drive;
  authority = entry + docs/ + constitution), U0.5 self-check, Hard Requirement 7 (process not replaceable; only
  explicit “skill-maintenance-only, no SDD” exception), first action must be the U0 declaration; fresh-context
  read-only stress test confirmed. Unexpected staged snapshot (`A`/`MM`) from the first run — inspect before commit.
- **Unfinished/TODO**: `skill:sdd-loop-driver` has no probe object → embedded Wrap-up errors `no probe object for
  unit`; feedback filed, not fixed in this change. Field-level gain (idle turns, false-timeout rate) pending a real run.
- **Commits**: `1030da9a` (model + routing guard), `9f2f7ba5` (run records); skill-shape 4779/5000.
- Tags: T1 T3

## 3e8cf04f — 2026-10-19 — 062 checklist (requirements quality)
- **Decisions**: produced `checklists/requirements-quality.md`, 40 items CHK001–CHK040, 100% traceable, commit
  `f2fe4027`. Captured requirement-quality gaps: undefined tone/audience/output path/coverage confirmation; unmeasured
  terms (明显减少/严格可推出/轻微润色/主语言/可区分); zero-input call, extension conflict, partial-write cleanup, path
  equivalence, frontmatter-only Markdown, prompt injection; FR conflicts (FR-003 quote preservation, FR-006 vs FR-009,
  FR-002 vs FR-005, FR-015, protected-element drift, “all supported tools” vs four measured copies).
- **Lessons**: `check-prerequisites.sh --json` hard-fails on the known missing `cws-lib-bash`; resolve paths manually
  without relaxing baselines. The traceability regex anchored on bracket start was itself a blind check (0/40 false
  negative) — fix the check, not the artifact. Compiled Wrap-up faces again lacked engine args; supplied
  `062-humanize-command-checklist-20261019`.
- **Key flow**: load skill + artifacts → prerequisite script fails on `cws-lib-bash` → manual path resolution → fresh-context gap pass (20 candidates) → 40-item checklist → structural self-check (regex fixed) → commit `f2fe4027` → wrap-up engines.
- **Unfinished/TODO**: none stage-side; feature stayed `Planned`, registry untouched.
- **Conflicts**: none; three in-passing corrections disclosed.
- Tags: T1 (command-surface only; checklist domain otherwise off-thread)

## da741035 — 2026-10-19 — 062 humanize implement (aborted mid-T031)
- **Decisions**: 33 tasks / 7 phases. `humanize` is a **Simple** command (027 rule) → the template carries no `## Wrap-up`; the skill carries `skill-humanize-wrapup` plus the first skill-side `h-docs-sync-eval`. The 0/40 checklist was seen and a waiver recorded because the dispatch brief pre-granted autonomy — the same 0/40 state later became 063's P0 F1. Tests Mode red-first; E8 corpus of 12 samples + rubric + two fresh-context reviewers + deterministic `diff_protected.py`.
- **Re-freeze**: `cws-lib-bash` restored 2026-10-19 15:58; full run 71 failed / 3929 passed name-identical to the frozen baseline. Mirror count read 113 vs the frozen 209 — the relative criterion was judged against the pre-change capture; 1 inherited NEW (`manage-feedback`).
- **Differ bugs**: frontmatter leaked into new-sentence detection; number blanking was not length-preserving; newlines swallowed; a URL `?` was read as a sentence terminator → `_BLANK_KEEP = set(string.punctuation) | {"\n"}`. Fixture corrections (not weakening): s09 gained an EN sentence (78/98); s10's window basis corrected from 12k to a 4k host (≈2,136 tokens > 2,000).
- **Probe compile**: compile-embeds reads the **mirror** registry, so a stale mirror engine emitted `.specify/.specify/...` on all 73 faces. Correct order = registry pair sync → source-engine compile → regen → feature-scoped sync; new units need a bare seed heading. Fingerprint `71fc61d910c6`→`7877db82c58c`; 74 units; pins updated (SIMPLE 3→4, EXTERNAL 13→14, “74 units”).
- **Honesty**: s11 was claimed PASS without execution → self-caught, executed, 补正记录. T016 reviewers both FAILed T-audience (annotations covered only the heading; one over-entailed sentence) → repair loop + third reviewer 翻案. Silent `str.replace` checkbox failures → assert-guarded marks.
- **Key flow**: waiver → T001 re-freeze → E8 corpus/rubric/differ (three bug-fix rounds) → red-first T002 (8 red/2 green) → skill/template → E8 rewrites → tone matrix repair loop → Phase 6 registration → T026 full A/B (65/3950 zero-new) → T030 fresh-workspace battery → T031 started, session died.
- **Unfinished**: the session aborted at T031 (quickstart S1–S8 live run) — T031–T033 remain; Feature 062 stayed `Planned` in this transcript even though T026/T030 closed with 65 failed / 3950 passed zero-new.
- Tags: T1 T5

## 26ca6503 — 2026-10-19 — 063 tasks (review P1 governance)
- **Decisions**: Tests Mode ON per Constitution IV. Never-cache re-freeze reproduced 63 failed / 3954 passed,
  set-equal to the plan freeze (`git diff` empty). First coverage freeze for 063: 497 lines, base `bf88f2c63857`
  (FR-004 dogfooded before its implementation). tasks.md: 51 tasks / 8 phases; 34 `[green:]` claims exactly once.
  Validator 0 err / 0 warn after: W1 drop `[P]` on T002 (read-vs-write same file as peer), W2 split C-8/9/10 into a
  separate pin file (one green point per test file), W3 de-path prose `assumption/decision`. D-T1 moved C-19 into
  US6/T041 to keep clause ordinals ascending per contract; D-T2 moved C-25 recompile to Polish T044 blockedBy
  T027+T032 to prevent re-drift. Commit `4a1204ba`.
- **Lessons**: validate-tasks flags write-vs-pointer pairs among `[P]` peers, not just write/write; a file-as-a-whole
  may hold exactly one green point.
- **Unfinished/TODO**: anomaly returned to orchestrator (decision-class): quickstart S6 literal `--complexity standard`
  is rejected by `run-determination.py` (closed domain `complex|simple`); left unfixed because plan artifacts are out
  of the tasks stage's scope.
- Tags: T4 T5

## f556a5f4 — 2026-10-20 — 063 review (SDD process review)
- **Decisions**: P0 F1 — implement Step-2 checklist exemption gate never fired (40 unchecked / 11 Gap-tagged /
  0 recheck / 0 waivers / no gate trace) while the feature flipped Implemented; confirmed by an independent
  read-only subagent (0/1 downgraded). P1: F2 frozen plan premise falsified (additive-only generator pinned by
  `test_instructions_section_propagation` → attempt-1 halt, mid-run amendment procedure undefined); F3 born-false
  GATE-5/DoD-4 premises; F4 baseline shrink unbookkept (63→21, 42 ghost names). P2: F5 stale `post_change_commit`;
  F6 falsified quickstart literals remain committed; F7 budget residuals dead-lettered; F8 cited 061 REC ids never
  registered; F9 reactive state-pin amendment. REC-063-01..10 written; report + register rows in same commit
  `708b1ab5`; correction commit `5a12778c` (eight→nine dispatches).
- **Lessons**: trust mechanical counts over narrated ones (11 vs “10 Gap”), per objective-analysis-gate rule 8.
  Unpushed HEAD makes reachability UNRESOLVABLE — report uses absolute paths + `git show` recovery, not URLs.
  Shell cwd persisted after `cd` into the spec dir; prefix repo-root cd. `register.md` had 0 REC- rows despite
  cited ids — forward-only seam.
- **Unfinished/TODO**: none for the stage; F1 mechanism fix became later work.
- Tags: T4 T5

## 8ac9bcc5 — 2026-11-02 — 078 bilingual-expression driver run; renumbered 079
- **Decisions**: full 8-stage chain + closure. The requirements dispatch first hit the 40-turn budget (scaffold only) → U5 retry with a 120-turn executor. Plan decomposition recorded `single-package`; implement split into 4 ≤8-task segments (19 tasks / 35 clauses). Deliverables: owner `shared/guidelines/bilingual-expression.md`, ambient section in `templates/instructions-template.md`, `scripts/python/bilingual-expression-check.py` (scan/coverage/census; exit 0/1/2), `tests/contract/test_bilingual_expression.py` (16 legs); REC-078-01..03 registered.
- **Closure**: baseline 21 failed / 6811 passed; first closure 24/6826 → 3 new failures from the ambient section (neutrality, pointer, section-count guards). Root cause: `[[STR-001]]` written into distributed text instead of the literal path, and `.specify/specs/078-` inside the owner doc triggered C-57. Fix `4e23dad2`; in-slot rerun 21/6829 zero new. E3 value `review-targeted` was outside the closed set → changed to `ran`.
- **User test-speed suggestions** were parked to `.specify/memory/todo/20261030-suite-speed-optimizations.md` and deliberately not implemented mid-run (protects baseline comparability); ranked xdist-on-contract and sleep removal highest, CLI contract tests keep real subprocesses.
- **Number collision**: `gitlab/master` was 49 commits ahead and already held another Feature 078 (`078-coaching-skills`). User ruled renumber local to **079**: 28 files, line-symmetric 250/250; colliding `T-001…T-004` and `REC-078-01..03`; merge `8d0e0106` resolved registry conflicts as a union, Total Features 74→75; three mirrors fast-forwarded, origin untouched.
- **Framework feedback filed**: 40-turn budget too small; structure gate scans all spec dirs (boilerplate noise); checklist `reader=not-applicable`; `validate-tasks` shared read-path false positive; E2 `seq`/E3 `status` closed domains absent from the dispatch block; analyze has no read-only E3; `generate-instructions.sh` never refreshes section bodies; `[[STR-]]` leaked into a distributed template.
- Tags: T3 T5 (T1 for template/tests)

## 6799e41f — 2026-11-05 — independent validator H-02 (082 SC-006)
- **Verdict**: downgrade HIGH→LOW. `requirements.md:150` SC-006 says “真实树上同一组测试全绿”; its Source (`:162`) plus US4 Scenario 1 bound “同一组测试” to the three mutation suites (double-landing, instructions propagation, mirror parity). The red node `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` (pin 23 vs live 27) belongs to Feature 050, not to those suites → no logical contradiction. `tasks.md:29` GATE-1 carries the exception while `requirements.md` never does — a clarity/completeness gap already captured as CHK014/CHK015, not HIGH untestability.
- **Evidence honesty**: bash was not permitted, so “currently red” rests on recorded executed evidence and test/baseline source, not a run the validator performed; the plan's pin citation `:361` sits near, not on, the equality assertion at `:365`. The return format forced separate `evidence_supported` / `evidence_not_supported`.
- **Key flow**: read cited artifacts → attempt the named test (tool denied) → verify red-ness from recorded evidence + test/baseline source → bound “同一组测试” via SC Source + US4 → downgrade.
- **Lesson**: an independent validator must state what it could not observe; a finding's paraphrase can be broader than the artifact text.
- Tags: T4

## 9857e730 — 2026-11-07 — 087/088 speckit visualization + `/speckit.measure`
- **Decisions**: driver ran the full chain; analyze took 4 rounds to GATE GREEN (C0/H0/M0/L3). The “same gate, one bounded loop per run; second round with C/H not cleared → stop” discipline produced a U5 stall with the four-element handoff; the user authorized rounds 3–4. F-07 CRITICAL was an owned-fact enumeration divergence (5 vs 8) introduced by a plan fix; F-01 HIGH was RO mapping drift.
- **`SDD Analysis Worker` missing** from the host: `display-color: teal` rejected by the Qoder config loader (`qodercli agents list` 1 error); fixed to `cyan` in source→mirror→render order (`ae6d6b19`), 24 active. The session's agent-type table is snapshotted at start, so round 4 used a read-only `SDD Stage Verifier` and recorded the degradation; `general-purpose` was not used again.
- **Feature Blocked** on SC-001/SC-002 partials; the user added efficiency info + `/speckit.measure`. SDD routing verdict = sdd. The unit-semantics conflict (“列表单位来自各面自身状态源” vs the user's “每个步骤”) was ruled per-step `(unit_id, unit_type)`; requirements corrected, PLAN-EDIT minor `6be09c3a`.
- **`measure.py`** (stdlib, read-only; `--since/--window` left-closed right-open; per-unit median/min/max/count/token sum; `--cap`; four exclusion classes; exit 0/2/3/1) + `templates/commands/measure.md` + four copies. Probe registry lacked `speckit-status-wrapup` and the `h-docs-sync-eval` binding → templates missed `## Documentation`; fixed `d41d0ced` (235 generated files).
- **Pseudo-completion caught**: the tasks revision had T055–T078 marked `[x]` before implementation → mechanically corrected. The checklist wrap-up accounting was skipped → the driver reran the three steps as a sanctioned exception.
- **Unblocking**: SC-002 real dogfood team with exactly one `role: reporter` seat (`validate-roster.py` exit 0, RO-04 pass); SC-001 real >90 s run (437.97 s) + reporter 20 lines at 30 s cadence. Closure r6 27 baseline failures / 7698 passed / 0 new; accept 10/10; master `7300d44d`.
- **Push collision**: remote held `086-efficient-test-execution` + `087-arch-diagram-docs`; local 087 renamed **088**, 9 conflicts resolved, cross-feature pins fixed (C-50 vs 086's `[dev]`; remote 087 C-019 vs the new commands); pushed `be29670d..018ca7f0` to three mirrors; final 27 failed / 7881 passed / 0 merge-new.
- **Lessons**: frozen-pin increments (commands 27→29, 79 probe units, flow-class 83/83) surface only via a full A/B; remote 086 changed runner/marker behaviour (“1 passed, 7909 deselected”); Part 3 wrote to `$HOME/.cache/` (temp-dir violation) and was cleaned.
- **Unfinished**: REC-A1 (per-tool renderer `rewrite_paths`, test_i11) and REC-W1/W4 registered as deferred.
- Tags: T1 T2 T5

## 866a72f0 — 2026-11-09 — VA verification (094 goal-team-parallel)
- **Decisions**: H-1 verified — contract clause marker form is `- **C-NNN**:`; 113 markers / 113 distinct,
  contiguous C-1…C-113, per-page 30/24/18/20/21; archive backfill = C-112/C-113, handoff keeps C-53/C-54;
  113 green tags, 0 duplicate (page, clause) pairs. H-2 verified — GATE-6 measured truth matches an independent
  post-freeze run; baseline delta exactly +1 `085-sdd-temporary-goal-team/contracts/checkpoint-and-agents.md#C-014`,
  −0 (one-time re-freeze, no gate weakening). VA: PASS; repairs `84d8765f` + `2c704003` (HEAD).
- **Lessons/anomaly**: tasks.md:483 claims the 42/42 pre-analyze reading is “kept verbatim” at
  `test-evidence/analyze-repair2-gates-requirements.txt`, but that file reads 43/43 and has no pre-analyze section;
  the fr:42 record actually lives in `test-evidence/pre-analyze-tasks-analyze-repair.json`. Non-blocking, pointer only.
- Tags: T2 T5

## 6d387867 — 2026-11-09 — FV1 verification (094 D4 anchoring fix wave)
- **Decisions**: at `aeadddd2`, 0 live normative `.specify/goal` hits in contracts/tasks/quickstart/feature-ref/
  data-model; 28 dated keeps + 90 dated-note quotations remain per the D5 keep list. All 9 listed contract lines now
  `.specify/anchoring`; `goal.md` filename and spec-local store unchanged; C-112 dated count 6 reproduces (6/12 live).
  feature-ref 43 FR entries / 43 distinct; `features.md` 88 rows / 88 distinct. Gates: requirements 0/0; coverage
  113 claimed, 599/0-beyond, FR 43/43; tasks 0 err / 1 disclosed warn; tensions 0/0; pre-analyze ×3 (fr 43/sc 12/
  tasks 83; advisories 101→98); decomposition 43/83.
- **Verdict**: FV1 FAIL — registry status stale: `features/094.md:66` + `features.md:101` say the anchoring wave is
  “进行中, 下一阶段 = 修复集成 + 门复跑” while the same commit's state spine records it complete.
- **Lessons**: the VB-1 defect class recurs at the integration boundary (W2 authored “W1/W2 进行中” pre-integration;
  the same-commit state update did not refresh the registry row).
- Tags: T2 T5

## 5fea4a1e — 2026-11-09 — test-suite audit chunk 0
- **Decisions**: 78 modules (73 test + 5 helpers), 1,081 test functions → keep 1,016 / rework 53 /
  delete-candidate 12; 13 slow-by-construction (9× `time.sleep(1.1)` in `test_client_metrics.py`); recorded full run
  8,351 tests / 165 failures / 46 s; chunk 0 had 0 failures. Delete candidates: `test_checker_form.py`
  `test_c15_c18_counter_samples_exist_one_per_new_check` (tautology — greps own source for a string supplied by the
  assertion), `test_agent_skill_enablement.py::test_union_is_subset_of_declarable_installed` (duplicate),
  `test_ask_record_repeat.py` mirror-parity duplicates of `test_mirror_parity_suite.py`, `test_closed_set_claims.py::
  test_runtime_mirrors_match_sources` (covered by MIRROR_PAIRS), `test_agent_dispatch_mechanism.py::
  test_c35_parity_map_complete` (pins frozen 060 artifact).
- **Anomaly**: `test_directory_governance.py::test_framework_map_registers_the_runtime_roots` asserts the retired
  `.specify/goal/<slug>/` root while `shared/definitions/goal-definitions.md:180` records the rename to
  `.specify/anchoring/`; `shared/definitions/framework-map.md:12` is stale — green only because doc and test are
  stale together.
- **Lessons**: chunk lists are zero-padded (`chunk-00.txt`); self-referential assertions (source-grep of a literal the
  assertion itself introduces) cannot fail.
- Tags: T1 (tests/skills surfaces)

## 1f5f64d1 — 2026-11-09 — G7 consolidation review
- **Decisions**: 12 entries → keep 10, merge 069a/069b into 069, archive 0, delete 0. 075 is an evolutionary spec
  bound to Feature 058 by design (not a missing registry row). Registry rows are huge; parse ID/status/links only.
- **Anomaly**: 070 review gate says closure stays blocked until F1/F2 are fixed or waived, while its verification.md
  claims the closure gate unblocked and merged at `ca8040f5`; no record resolves F1/F2 (waiver-070 covers only
  SC-001/SC-002).
- **Lessons**: check stale `.specify/goal` contract references and retired vocabulary when judging staleness;
  evolutionary-spec binding is a legitimate no-registry-row pattern.
- Tags: T3 T5

## 208e88b8 — 2026-11-09 — G3 consolidation review
- **Decisions**: 9 entries → keep 7, merge `092` → `090-re-anchoring`, archive `085` (gated on 094 closing),
  delete 0. Revert note convention: `git checkout <sha-before-deletion> -- <path>`.
- **Lessons**: spec-dir numbers and registry IDs are separate sequences — `features/037.md` is “Docs Command”
  (spec 033), not `037-goal-registry`; map by spec path. 090 rename is `.specify/goal` → `.specify/anchoring`.
- **Anomaly**: registry row 090 reads `Implemented` and claims it absorbed 092, while the tree holds 116 open rows of
  092's 158-row slice, 62 unparseable ND clauses, a 197-row task graph over the 160 ceiling, and a verification still
  certifying “tasks.md (39 rows, all closed)” — the status/verdict contradiction Non-Disposable exists to detect.
- Tags: T2 T3

## af6d3fc1 — 2026-11-10 — coaching-skills trainee run of `/speckit.status`
- **Decisions**: `status-digest.py --action digest` exit 0; 8 registry lines, all stale, none active (exit 3 =
  nothing-running not hit). Run determination persisted (4 axes `not_evaluated`, `trigger_feedback=false`); feedback
  count 379; threshold notice suppressed because composition needs `should_prompt` AND the routing bit. Closeout
  policy `ask`: sequence presented, nothing executed; model 临时分支(trunk-based); push targets
  `github`/`gitlab`/`gitee`, `origin` excluded as read-only upstream; a record-only run has no `NNN-<slug>` so the
  feature-branch name needs the user's decision.
- **Lessons/anomaly**: digest header lacks the resolved registry directory; 074's label/derived-state contradiction
  is silently split (state=stalled but activity label=running). Wall clock 113–172 s, under the 15-min ceiling.
- **Unfinished/TODO**: closeout choice open by design (policy `ask`); no commit/push.
- Tags: T1 T5

## 38ebae8c — 2026-11-10 — history Wave 4 (G3 orphan-path, 736 entries)
- **Decisions**: probe found 736 `orphan-path` entries (`not_closed.open` 899). Classified all: live-surface 153 /
  dated record 198 / genuinely removed 385 (39 declared runtime stores, 22 example paths). The live bucket (153)
  exceeds the wave's 150 bound → stop after classification; 0 fixes applied, 0 claimed; `not_closed.open` stayed 899.
  Full per-entry plan written for the next run.
- **Artifacts**: `history-w4-before.json`/`-after.json` byte-identical (digest `e4e9acc8…`), `history-execute-g3.txt`
  with four E-7 segments + 153-row plan + 736-row disposition. Capture Rule readings: mirrors byte-identical,
  instructions 36804 B, constitution pins 27/21.
- **Lessons**: `.tmp` worktree noise is not a live target; basename-only matching is too noisy — build suffix-based
  relocation matching; analyzed-workspace convention paths must not be rewritten. Renames confirmed:
  `humanize`→`humanize-conclusion`, `export-session`→`archive-session`, `goal/`→`anchoring/`, docs six-type reorg.
- **Anomaly**: 4 `030-summarize-project` entries cite the analyzed workspace's `docs/overview.md` convention, not a
  repo path — left open with that reason.
- Tags: T3

## Per-thread index

- **T1 agents→skills→tools**: 9c57a1ed (skills/commands/agent registration), 8b32d7cd (S1–S3 skill/command
  campaign), 34080ca9 (driver watch + routing guard), da741035 (probe compile/command), 3e8cf04f (checklist
  command surface), 5fea4a1e (test audit of skills tests), af6d3fc1 (coaching trainee), 6fbbb89d (template
  param gap), 9857e730 (status/measure commands, reporter agent)
- **T2 anchoring→goal→team**: 9c57a1ed (goal/team lifecycle → achieved), 9857e730 (reporter seat; goal/team
  visualization), 8b32d7cd (goal-based team run; goal/→anchoring in migration), 866a72f0 (094),
  6d387867 (094 anchoring wave), 208e88b8 (092→090 merge; 090 rename)
- **T3 archive+history+session**: 38ebae8c (history Wave 4), 208e88b8 (consolidation), 1f5f64d1 (consolidation),
  34080ca9 (session watch model), 8ac9bcc5 (driver session + feature renumber)
- **T4 derive+review+interview**: 26ca6503 (063 tasks), f556a5f4 (063 review; 10 RECs), 6799e41f (082 P0/H
  validator)
- **T5 memory+state**: 9c57a1ed (register, run-determination, feedback store), 6fbbb89d (059/exec-quant),
  26ca6503 (frozen baselines), f556a5f4 (register seam), 866a72f0 (coverage baseline truth), 6d387867
  (registry currency), 1f5f64d1 (070 status), 208e88b8 (090 status), af6d3fc1 (status digest),
  8b32d7cd (migration stores), da741035 (baselines/mirrors), 9857e730 (measure/exec-quant),
  8ac9bcc5 (test baselines/registries)
