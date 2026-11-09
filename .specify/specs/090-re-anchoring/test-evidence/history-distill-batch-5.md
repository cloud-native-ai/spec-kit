# Distillation batch 5 — five-thread extract

Scope: 18 sessions from `.specify/.tmp/history-batches/batch-5.txt` (2026-10-08 → 2026-11-10), read-only on `.specify/history/.work/` sources. Threads: **T1** agents→skills→tools · **T2** anchoring→goal→team · **T3** archive+history+session · **T4** derive+review+interview · **T5** memory+state. No session skipped (18/18).

## 5ea25dfb — 2026-10-08 — Feature 055 conflict-free stores (feedback/memory index.json → per-entry files)

- **Decisions & rationale**: per-entry `.md` is the sole record; `entries[]`/`introspections[]` derived by frontmatter scan, never persisted; `state/threshold.json` / `state/submitted-at.json` / `state/upstream-repo.json` one file per scalar (missing = default); legacy `index.json` read-only fallback, first mutating action auto-migrates + deletes + discloses `migrated: true`; `reindex` = explicit idempotent migration. Rejected alternative: keep the monolith + merge discipline — full-file rewrite was the conflict root. Memory session/knowledge refactored same round; 055 implemented in an isolated worktree to leave the active 054 session untouched. [T5]
- **Lessons/pitfalls**: engines/tests read the `.specify/` mirror — 4 failures were missing mirror sync after a late `.part`-cleanup edit; `test_c2_active_spec_feature_bindings_resolve` only greens after the features.md registration row; baseline compared on clean master (48 failed = baseline, zero new); same-second cross-branch same-unit record collision registered as Known Residual (≤ status quo). [T5]
- **Unfinished/TODO**: merge playbook for master — features.md adjacent-row conflict keeps both rows; index.json modify/delete takes deletion; 054's next wrap-up auto-migrates.
- **Key interaction flow**: 3 exploration agents → 3 user rulings (feedback+memory same round / auto-migrate on first write / lightweight Feature 055, ~8 FR) → design agent → engine+memory+consumers+tests+docs+self-migration → 3 commits; subsequent "提交代码" landed 054's demo artifacts as `7267c46a` on `054-agent-registration-wiring`.
- **User↔model conflicts**: none; design agent corrected model premises (run-determination loads index in-process; repo held 29 feedback entries). [T5]

## 06db3fb9 — 2026-10-13 — Feature 056 Probe-Handler system (1 probe ⇒ N handler)

- **Decisions & rationale**: layered probe admission — entity only if queryable / host-extensible / prose-reconciled; micro-probes stay code-first, registered only as pointer entries in a `## 非实体 probe 目录` chapter; three-layer model Probe Class×Object + HandlerBinding + Handler (six-field closed set, `h-` prefix); dispatch = compile-time generation (`probe-utils.py --action compile-embeds` → single AUTO-GENERATED `## Wrap-up` per unit); incremental MVP = five wrap-up handlers. Clarify Q1–Q6: title `## Wrap-up`; new umbrella Feature 056, 028 demoted; behavior rules frozen, wiring-reference edits allowed; kind-fixed call forms + `@point:` closed set; zero-handler units emit no section; host projects read-only. [T1]
- **Lessons/pitfalls**: engine reads `.specify/` mirror; `_table_rows` matches `## Classes`/`## Objects` literally — headings kept; hyphenated `probe-utils.py` imported via `importlib.util.spec_from_file_location` + `sys.modules` dedupe; order conflict fires only across different handlers; `splitlines()` drops the trailing blank → use `split("\n")`; BLOCKING_PATTERNS imported by path, case-sensitive; baselines need a real-registry workspace + catalog-seeded scratch; post-migration `scan_embed_units` must scan `## Wrap-up` (old `## Feedback` literal produced ~60 reconcile errors); banner fingerprint must cover the wrap-up projection only (full-set hash invalidated all banners on phase-2 rows; projection == old hash); 20 pre-existing reconcile gaps (S-layer skills embedding without rows) adjudicated correction-class and registered; naive `ls` = 26 command files vs `grep -l '^## Feedback'` = 23; test `ROOT = parents[1]` bug; exit-code pipe trap (`| tail` masks status); SC-007 baseline corrected 276 (stale memory) → measured 853 → final 413/≤853; `.git/objects` root-owned by a background root git writer blocked commits repeatedly — chown fixed, regeneration observed. [T1]
- **Unfinished/TODO**: mid-run directive (below) resolved; 056 all 38 tasks `[X]`, SC-001..008 pass, feature Implemented; commits `581f1f7a`, `b1ae7308`, `391fccd8`, `ad61b009`, `ef573d5f`, `5a6c99b7`, `c8784382`, `efa7812d`, `f5973848`, `1e9ff866`, `6a42d068`.
- **Key interaction flow**: retrospective → 1⇒N design → user "使用3 走完成SDD流程" → full requirements→clarify→plan→tasks→implement chain across 3 compactions; mid-run git-workflow directive injected between phases and landed `a85393c7`; user follow-up ruling landed `974a4f45`.
- **User↔model conflicts**: user premise "docs/git-workflow.md 不存在" falsified (file existed, mode 600) — substantive point (MAIN/PRE/DEV hard-coded as THE framing) upheld and fixed; user labeled the project "单分支开发" while measured practice = trunk + short-lived `NNN-<slug>` branches → user ruled rename menu option 3 to 临时分支 (distinct from 单分支 = never creates temp branches), closed. [T1]

## 4f60c597 — 2026-10-16 — Feature 059 exec-quant plan stage (unattended)

- **Decisions & rationale**: engine attaches to the existing wrap-up point (engine handler, order 15; zero new template faces/gates); storage `-.specify/memory/exec-quant/` dual JSONL append-only; feedback `package` reads only the feedback store, so upload exclusion is structural; duration/token carried from the same-run determination record, not re-measured; non-collectable fields explicit `not_evaluated` (no invented effort). D1: action renamed `list` → `list-records` to avoid collision with feedback's `list`. [T5][T1]
- **Lessons/pitfalls**: `_ENGINE_SIBLINGS` is an explicit tuple — a new engine must be added; `determine` requires `--run-id` (key = unit_id+run_id) and caller declarations (`--complexity`; green check must be declared verbatim); wrap-up line budget BUDGET=853 is an upper bound; run start taken from plan.md btime (no fabricated duration); Re-check row must stay pending until artifacts land; a `cd` inside a scan command drifted the workdir → rerun from repo root; glossary duplicate character fixed in passing (file intentionally uncommitted). [T5]
- **Unfinished/TODO**: next stage `/speckit.tasks` dispatched by the orchestrator (sentinel `PLAN-DONE`).
- **Key interaction flow**: unattended dispatch brief with sentinel/anomaly-line contract → Phase 0 exploration → plan + 4 Phase 1 artifacts → fresh-context constitution re-check (3 real defects fixed) → Feature 059 Draft→Planned → commit `20e14dc4` → wrap-up engines (self-reported Re-check prefill violation corrected).
- **User↔model conflicts**: none.

## 04e3f86b — 2026-10-19 — `/speckit.agents` no-argument listing

- **Decisions & rationale**: informational, non-destructive listing only — 3 templates + 4 instances, execution configs only `_defaults.yaml`; no artifact, no commit. [T1]
- **Lessons/pitfalls**: observed `framework-engineer.agent.md` mode 600 vs 644 on the other six; for larger rosters, frontmatter field extraction should go to a script (`token-efficiency` marker). [T1]
- **Unfinished/TODO**: ANOMALY — run-determination/exec-quant/feedback-record blocked by the dispatch permission classifier; wrap-up status unknown, not clean.
- **Key interaction flow**: frontmatter read of all 7 definitions → listing + contextual suggestions + capability summary (create/refine/run).
- **User↔model conflicts**: none. [T1]

## cfa3d399 — 2026-10-19 — analyze 062-humanize-command (read-only cross-artifact)

- **Decisions & rationale**: gate verdict BLOCKED — CRITICAL 0 / HIGH 2 (H-01 prompt-injection defense absent across FR/contracts/fixtures; H-02 main-language determination has no owner) / MEDIUM 15 / LOW 4; zero writes, zero commits; same-author gate not fired (artifacts predate the session, different author) → direct detection with unconditional validation wave for HIGH. [T4]
- **Lessons/pitfalls**: validation wave confirm 2 / downgrade 1 (B-01 call-syntax → MEDIUM); `[blockedBy]` is the ONLY mechanical start gate — prose phase order creates false-green surfaces (F-05/F-06); "semantic criteria deferred to rubric" pattern left main-language/number-equivalence/audience/execution-limit criteria unowned; green-claim partition program-checked C-1..C-34 exactly once; `cws-lib-bash` missing made `check-prerequisites.sh` unusable — REQUIREMENTS_DIR rebuilt from the tree without relaxing any baseline. [T4]
- **Unfinished/TODO**: upstream fix for H-01/H-02 (REQ/contracts/fixtures) then re-run analyze; B-01 call contract to be settled before fixture layout; G-01 registry stage-record lag.
- **Key interaction flow**: artifact load → passes A–G → 3 fresh-context validators → findings report with severity counts and gate conclusion.
- **User↔model conflicts**: none.

## df0d4308 — 2026-10-19 — implement 062 attempt 2 (resume after transient crash)

- **Decisions & rationale**: resume 30/33 without renumbering; keep the unplanned `.specify/scripts/python/probe-utils.py` path normalization — single-file revert experiment made `compile-embeds --check` exit 2 (`probe registry invalid`), proving the compile pipeline needs it, so it stays with a recorded deviation; frozen 71-name baseline never relaxed; commits `c7de21a0` (distribution surface), `92037f07` (fingerprint refresh `71fc61d910c6 → 7877db82c58c` + normalization), `e6696a0f` (closure); 17–19 run records intentionally uncommitted. [T1][T5]
- **Lessons/pitfalls**: `clause_extract.clause_blocks()` returns `(id, body)` tuples, not strings; `cp -i` alias no-ops while returning success → `/bin/cp -f`; `nohup ... &` misreports launcher completion → confirm via log/pid; analyze2 U-08/F-07/L-04/L-05 were already fixed in the tree; generated wrap-up calls omit `--run-id/--complexity/--review` (exit 2) — completed per prior-run convention (`complex` + honest review) and disclosed as template-generation defect; mirror sync only with `--only` pairs. [T1]
- **Unfinished/TODO**: fix the generation source of wrap-up args (carried into 063 F4).
- **Key interaction flow**: T031 quickstart S1–S8 → T032 SC-001..011 pass → T033 Planned→Implemented → 3 logical-group commits → wrap-up engines → `IMPLEMENT-DONE`.
- **User↔model conflicts**: none.

## be645516 — 2026-10-19 — checklist 063-review-p1-governance (requirements quality)

- **Decisions & rationale**: new file `checklists/requirements-quality.md` — 40 items CHK001–CHK040, 8 groups, 100% traceable; existing `checklists/requirements.md` untouched; Feature transition `Implemented → Ready for Review` N/A (Planned); commit `728ad4ea`. [T4]
- **Lessons/pitfalls**: awk numbering-validation syntax error → Python heredoc; `grep -o 'CHK###'` counted the meta note as a false duplicate → count only `^- \[ \] CHK` lines; run-determination `artifact_correctness: not_evaluated (no_baseline)` is the honest result, never fabricate a baseline. Item-level gaps found: FR-022 baseline set vs C-29/E12; FR-020 stale GATE-8 anchor; FR-026 write-boundary vs FR-009/016; FR-029 four-file enumeration vs SC-014 whole-directory; "逐字执行" vs placeholder substitution; 100% SCs without non-zero denominators. [T4]
- **Unfinished/TODO**: analyze dispatched separately by the orchestrator.
- **Key interaction flow**: same-author gate not fired (prior-stage artifacts) → direct gap-finding vs plan/tasks/contracts → generate + mechanically validate checklist → wrap-up engines → `CHECKLIST-DONE`.
- **User↔model conflicts**: none.

## f2f7adbe — 2026-10-20 — sdd-loop-driver: humanize 062 delivery + driver items 2/4 + 063 chain

- **Decisions & rationale**: full-chain driver runs (requirements→…→review); analyze round 1 HIGH=2 → one repair loop (requirements→plan→tasks) → round 2 HIGH=0; implement attempt 1 died `UnsupportedFinishReasonError` (transient), attempt 2 resumed from T031; Stop-hook + FIFO backstop adopted (PID/status/sentinel remain authoritative); SSH design: hook on run-user side, atomic `done.json` then FIFO, check-before-wait; item 2 `acc36bfd` (`watch-target.sh --hook-done/--hook-fifo`, self-test 20/20, contract 25/25); item 4 probe row `skill:sdd-loop-driver` (`aec46e5e`, `060320e5`) — its wrap-up face was already inside the 74 compile units, only the Object row was missing, so test pins stay 74; 063 C-12 ruling: refresh via `/speckit.instructions` (`a8c3c1f0`) instead of extending `generate-instructions.sh`. [T1]
- **Lessons/pitfalls**: FIFO `read < fifo` blocks in open even with `-t` → `read <> fifo`; watcher positive-evidence matrix — no `pgrep -c` counting, empty output = UNKNOWN never 0/done, `EXITED_NO_SENTINEL` must carry last line/tail/git state; contract pin "前置检查表不得自持" rejects a `ConnectTimeout` literal in the preflight table; compile→regen→sync fixed order; a hook is an early completion signal, not the completion judgment; `cws-lib-bash` destroyed by a teardown → realpath + prefix assertion before `rm -rf`, never generic variable names. [T1]
- **Unfinished/TODO**: 063 review P0=1 — implement Step-2 checklist waiver gate never executed → next-feature pre-gate (REC-063-01/02).
- **Key interaction flow**: user ordered items 2→4→3; items 2/4 merged, 063 ran six stages → implement (51/51, SC 14/14) → review (P0=1/P1=3/P2=5, 10 `REC-063` registered) → merge `cfe7947e`; then user "pull上游代码然后合并,最后进行push" → merge `005fa2b8` + archive `c45cc6aa`, pushed gitlab/github/gitee, `origin` untouched.
- **User↔model conflicts**: none; the user's explicit ordering and push authorization were followed as stated.

## 57f56b33 — 2026-11-05 — validator H-04 (082 self-explanatory integration)

- **Decisions & rationale**: verdict **downgrade** HIGH→MEDIUM. EP-002 is a mechanism/source-presence rule that the cited code does establish (`src/specify_cli/__init__.py:2503-2516`; module-dir-first `get_resource_path()` at `:1532-1539`; `pyproject.toml:32-37` force-includes `shared/` into the wheel), so `verified` is defensible; the real defect is task/closure-level — SC-005 (`requirements.md:149`) lacks a build qualifier, T029 hard-fails against the stale `/usr/local/bin/specify`, and the documented remedy `pip install -e .` (tasks.md:38, T036) is satisfiable after a documented environment mutation. [T4]
- **Lessons/pitfalls**: validator must return both `EVIDENCE_SUPPORTED` and `EVIDENCE_NOT_SUPPORTED`; Bash was denied and reads outside the workspace blocked, so the installed-tree absence rests on the artifact's own S-1/S-6 record + static code reading, not fresh observation; research.md R-5 itself contradicts the executed S-6 (no listing recorded). [T4]
- **Unfinished/TODO**: SC-005 build qualifier + a task performing the reinstall.
- **Key interaction flow**: re-read cited artifacts → trace resource resolution → judge premise vs closure defect → single verdict.
- **User↔model conflicts**: none.

## 670d17a3 — 2026-11-05 — validator H-01 (082 T006 red-first premise)

- **Decisions & rationale**: verdict **downgrade** HIGH→MEDIUM. T006's expected "STR-001 尚不存在而失败" branch is impossible — neither suite references STR-001; the "空真" fallback is a vacuous green, not a red baseline; but the red premise IS asserted unambiguously by adjacent rows (T051; "T006 captures the Red baseline into the two existing suites"), the plan rows name no suite, and the feature-ref "row 3" citation is wrong (it is `constitution.md`; guard rows are 12–13) — the "incompatible mechanism" claim is unsupported. [T4]
- **Lessons/pitfalls**: a vacuous-green ("空真") test is not a red baseline; line-numbered citations must be re-resolved before use (row 3 vs 12–13; tasks.md:111 is a separator, checkpoint at :109); pytest denied → green accepted from recorded measurements only. [T4]
- **Unfinished/TODO**: T006 wording to be tightened; new module T007 absent from the plan-owned delivery surface.
- **Key interaction flow**: artifact re-read → attempt test run (blocked) → evidence-based verdict.
- **User↔model conflicts**: none.

## 46290991 — 2026-11-09 — post-merge integrity W5 (read-only, 6 checks)

- **Decisions & rationale**: read-only audit only, no repairs; all six checks PASS with drift 0 — mirror parity 6 pairs byte-identical (templates 22, skills/external 417, skills/internal 139, agents 17, scripts 123, shared 100), regen copies clean, compile-embeds 79 units zero drift, 4 instruction symlinks resolve to `.specify/instructions.md`, HEAD `41e91f0d`, declarations parse (contract 9 keys / exclusions 73 / facts 24). [T3][T1]
- **Lessons/pitfalls**: own trailing `EXIT=0` echo corrupted the captured JSON parse — strip wrappers before parsing captured output; 18 untracked entries were concurrent W2/round-3 evidence, not merge drift. [T3]
- **Unfinished/TODO**: none (ANOMALY: none).
- **Key interaction flow**: verify check-mode flags via `--help` first → run six deterministic checks → report `integrity.md` → `W5-DONE`.
- **User↔model conflicts**: none.

## 37801781 — 2026-11-09 — VC anchoring verification (094-goal-team-parallel, D4)

- **Decisions & rationale**: VC FAIL. D4 substance PASS (FR-007/025/028 rationale recorded in T-004 + Notes; engine values `global|spec|auto` verified at `goal-utils.py:1339`; spec-local `goal/` path unchanged at `:61`); duplicate-092 handling correct (ND archive pointer keeps 092, clause ids C-92 intact). Failures are a live normative split: contracts still carry `.specify/goal` (10 lines / 9 clauses / 4 of 5 pages; `anchoring` = 0) — HIGH×5 (+5 tasks rows, 4 quickstart lines, feature-ref SC-012, data-model ×2); MEDIUM×8 (C-112 dated, features.md header 87 vs 88 rows, `team/094.../team.md` live residues, EP-002 denominator wrong, 092 identity residues); LOW×3. [T2]
- **Lessons/pitfalls**: R2's residual under-scoped the split to contracts — 15 more live hits sit outside; the tree has TWO one-level `team/team.md` files (088 and 092-non-disposable), so neither 16 nor 18 is a tree-supported denominator (probe-visible 9+8=17, all files 9+10=19). [T2]
- **Unfinished/TODO**: fix targets enumerated per hit table in `notes/analyze-round4/vc-anchoring.md`.
- **Key interaction flow**: contract-by-contract hit table (file:line | class | verdict) → PASS/FAIL verdict → `VC-DONE`.
- **User↔model conflicts**: none.

## 5a429557 — 2026-11-09 — wp01-foundation implement (094)

- **Decisions & rationale**: 15/15 rows closed; binding model (owner/owner_id/origin/lifecycle) + scope engine changes in `scripts/python/goal-utils.py`; C-20: `_render` keeps the binding block byte-identical across lifecycle/objective/criteria/targets writes; scope choices/default changed with cross-layer refusal; commits `a8965b03` (T001–T015), `26688b3d` (close-out readings); no push. [T2]
- **Lessons/pitfalls**: the plan's 46-id baseline was stale — clean implement-entry baseline measured 113 failed / 8187 passed and the plan file itself fails `LC_ALL=C sort -c`; a mid-run background baseline was contaminated by the worker's own engine edits → stopped and re-captured clean against the HEAD engine with same-command auto-restore; 085 disposal rewrites (`test_scope_resolution.py`, `test_goal_scope_engine.py`, `test_temp_goal_contract.py`, `test_temp_team_schema.py`) and the `test_run_checks.py` action-roster pin (11→13) are unowned; C-19 `reopen` clause has no implementation row. [T2]
- **Unfinished/TODO**: residuals listed in `notes/implement-wp01.md` § Residual risks, none repaired outside the package write domain.
- **Key interaction flow**: read package map/rows → red-first 12 failed → engine + binding → green 12 passed → collateral classification → evidence per row → explicit-path commits → `WP01-DONE`.
- **User↔model conflicts**: none.

## bd6dcf6f — 2026-11-09 — test-suite audit chunk 3 (read-only)

- **Decisions & rationale**: 75 modules / 903 test functions → keep 827 / rework 33 / delete-candidate 43; every delete-candidate carries a one-line reason; two unread modules explicitly closed out (no sampling left silent). [T4]
- **Lessons/pitfalls**: `INTERNAL_SKILLS` roster is 36 but the tree holds 38 (`run-skills`, `run-team` unguarded); self-referential constant assertion (`WRITE_VERBS_OF_THIS_FEATURE == ()`); vacuous `or True` in a trigger idempotency test; parametrized tests that are strict subsets of `_assert_card_contract`; exclusion test whose fixture contains no excluded files; slow-by-construction: module-scoped venv + `pip install -e` fixture (300/540s timeouts), `time.sleep(1.1)`×2 inside a git-merge test, full-suite subprocess simulators (47 KB test-only `wp_driver_sim.py`). [T4]
- **Unfinished/TODO**: none; report at `.specify/.tmp/sdd-loop/tmp/test-audit/audit-3.md`.
- **Key interaction flow**: chunk list → size/name extraction → module reads → counts → totals + top-5 delete-candidates → `AUDIT-3-DONE`.
- **User↔model conflicts**: none.

## 2e79c944 — 2026-11-09 — consolidation review G1 (11 entries)

- **Decisions & rationale**: keep 10 / archive 1 — `003-speckit-agents-command` → `.specify/archive/spec/` (revert `git checkout 6f00890e1 -- <path>`; history is the rollback); registry status judged against spec evidence, never verbatim; archive-not-delete convention sourced from the 2026-08-15 audit. [T3]
- **Lessons/pitfalls**: `features/001.md` reads Planned while `features.md` records Completed (001's Handoffs invariant now 27/29 — `measure.md`, `status.md` lack `## Handoffs`); `features/003.md` is mislabeled "Checklist Command" and points at a nonexistent spec dir; 057 treats `.specify/goal` as truth owner — retired by the 090 rename (now `.specify/anchoring/`); spec-branch numbers vs Feature IDs are offset (020→025, 028→029, 033→037, 048→049) — not mismatches. [T3][T2]
- **Unfinished/TODO**: 001/003 header repairs; 057 path refresh.
- **Key interaction flow**: inventory → registry/evidence/detail triangulation → staleness sweep → per-entry verdict table → `REV-G1-DONE`.
- **User↔model conflicts**: none.

## 3b8d316b — 2026-11-09 — consolidation review G5 (8 entries, feedback/exec-quant/probe)

- **Decisions & rationale**: all 8 keep — `041`, `059`, `068`, `072` contracts and 027's classification contract are LIVE test fixtures; deleting any breaks the suite; 041/047 are extension slices of Feature 028, not standalone Features; spec dirs offset from owners (027→028, 034→038). [T3][T1]
- **Lessons/pitfalls**: hard status contradiction — `features/056.md` header says Planned/2026-10-13 while its own Status Tracking, the registry and verification.md record Implemented 2026-10-14 (header-only repair); live-surface drift — registry row 028 and `features/028.md` still instruct `feedback-utils.py --action probes`, an action moved to `probe-utils.py` by 056 and now rejected; 027's contract still names `.specify/goal/` (090 rename). [T1][T2]
- **Unfinished/TODO**: the two stale instructions + goal path.
- **Key interaction flow**: entry inventory → feature-row mapping → verification reads → staleness grep → keep verdicts → `REV-G5-DONE`.
- **User↔model conflicts**: none.

## 111683d8 — 2026-11-09 — study-code on dsh-superagent-prototype

- **Decisions & rationale**: target repo's `.git/refs/heads/main` zeroed and `.git/index` unreadable → do NOT repair the target; verified the object DB intact (single commit `8c32a9d`) and materialized via `cp -a` with recorded provenance; default `$STUDY_DIR` parent unwritable → sanctioned `~/tmp` root; draw-diagram backend unreachable → Mermaid sketches + planned `.puml` sources + visible degradation note; target untouched (mtimes preserved). [T1][T5]
- **Lessons/pitfalls**: `--names-*` args are pytest failed-nodeid lists, not skill names — misuse self-corrected; duplicate run IDs refused → settle the prior record then re-determine; feedback points need the literal `token-efficiency` marker; superseded feedback entry disposed; `Closeout: ask` gate → records left uncommitted (7 files), no unilateral commit; doc-vs-code conflicts recorded as facts (missing `src/sources/`, `SETUP.md`, `skills/`, `scripts/`). [T5]
- **Unfinished/TODO**: close-out commit awaiting user approval; 382-entry feedback backlog.
- **Key interaction flow**: SKILL + 6 references → strip 301→120 files → outlines → deep study → `docs/overview.md` (280 lines; self-check 42 evidence paths, 29/29 anchors, 21 index rows) → wrap-up engines.
- **User↔model conflicts**: none.

## ca4d659f — 2026-11-10 — Wave 5 verification (G3 live-surface fix)

- **Decisions & rationale**: baseline `orphan-path` 736 / `not_closed.open` 899; applied 153 planned corrections across 62 files — one backticked-token rewrite per entry, target existence-verified before editing, no dated-record rewrite, no invented target; after: 736→599 and 899→762 (drop 137 = the entries actually closed); E-7 evidence written with four segments (`readings` / `paths` / `corpus` / `dispositions`). [T3]
- **Lessons/pitfalls**: `entry_id` drops the leading `.specify/` → use the baseline's `evidence_refs.path`; `:line`-suffixed tokens replace the path and preserve the suffix; engine C-703 merges same-line readings by `entry_id`, masking a second orphan token on the line — that is exactly the 16 residuals (named, left open); capture rules re-verified (mirrors ok, instructions 36804 B, pins 27/21). [T3]
- **Unfinished/TODO**: 16 residual same-line entries left open with names.
- **Key interaction flow**: fresh baseline JSONs (before/after) → plan parse → mapping validation → apply script → residual diagnosis → report → `HIST-W5-DONE`.
- **User↔model conflicts**: none.

## Per-thread index

- **T1 agents→skills→tools**: 06db3fb9 (core: probe/handler entities, shared engine, compile-embeds, git-workspace reframe), f2f7adbe (driver Stop-hook/FIFO + probe row), df0d4308 (probe-utils compile pipeline), 4f60c597 (handler attachment), 04e3f86b (agent listing), 5ea25dfb, 3b8d316b, 46290991, 111683d8.
- **T2 anchoring→goal→team**: 37801781 (D4 `.specify/goal`→`.specify/anchoring` split, team denominators), 5a429557 (goal binding/scope engine), bd6dcf6f (retired-goal pin), 2e79c944 (057 stale goal path), 3b8d316b (027 goal path).
- **T3 archive+history+session**: ca4d659f (history G3 wave), 2e79c944 (archive verdict + convention), 3b8d316b (registry/detail drift), 46290991 (session-record surface), 5ea25dfb (session store design).
- **T4 derive+review+interview**: cfa3d399 (analyze HIGH gate), 57f56b33 + 670d17a3 (validation-wave downgrades, vacuous-green/red-first discipline), be645516 (requirements-quality checklist), bd6dcf6f (test audit).
- **T5 memory+state**: 5ea25dfb (per-entry stores, derived indexes), 4f60c597 (exec-quant append-only store), df0d4308 (run-record handling), 46290991, 111683d8 (wrap-up records/close-out gate), 04e3f86b.

Sessions skipped: none (18/18 distilled).
