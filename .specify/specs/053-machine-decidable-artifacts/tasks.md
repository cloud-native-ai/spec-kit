# Tasks: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Requirement ID**: 053
**Requirement Key**: 053-machine-decidable-artifacts
**Related Feature**: 053 机器可判定的制品命题(Machine-Decidable Artifact Propositions)
**Input**: Design documents from `.specify/specs/053-machine-decidable-artifacts/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), research.md, data-model.md, contracts/ (×7, 182 clauses), quickstart.md (12 scenarios), feature-ref.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" matched the deterministic keyword scan at `constitution.md:73` (`grep -nE 'MUST|MANDATORY|Test-First|TDD|Contract-Driven'`); Principle VII's **template-only gate does NOT excuse this feature** — 053 ships executable runtime code (2 new scripts + 2 script edits per `feature-ref.md` § 交付面清单 rows 1,2,4,5), so red-first contract tests and unit tests for pure functions are mandatory, and every new-behavior test MUST fail before its subject exists.

**Organization**: Tasks are grouped by user story; each story phase is independently implementable and testable. Within each story: Tests (red-first) → Implementation → Evidence.

## Definition of Done (DoD)

- DoD-1: Zero `[ ]`/`[>]` rows remain; deferred work is `[~]` with a recorded reason (never silent)
- DoD-2: Tests-Mode-ON obligations honored — every new check item has a counter-sample, `clause_extract.py` has unit tests, all 7 contracts have a pinning suite, and every red-first test's failing output is pasted into `notes/red-first-evidence.md`
- DoD-3: Every SC-001…SC-012 from requirements.md has a status line in `verification.md` (or `[~]` + `deferred_reason` — never a fabricated pass rate)
- DoD-4: Every Mirror Obligation row of plan.md § Mirror Obligations has a landed write AND a verify, with per-pair criterion as that table states — **relative for the three pre-dirty pairs** (`scripts/python`, `skills`, `templates`), **absolute** for the three single `skills/create-team/…` files, `templates/tasks-template.md`, the `shared/*` pairs and the per-tool command copies. (2026-10-03 订正 R2-H9:本行原先写「every other pair absolute」,而当时表里根本没有 `templates` 对那一行——该对改前 EXIT=2 / 2 DIFF,读侧范围小于 T023 写侧范围)
- DoD-5: Landing hygiene — every file landed by this feature has zero `BLOCKING_RE` hits; gate total stays **23** / violations **0**; `templates/` new content has zero repo-name hits; `scan-confirmation-gates.py` diff empty within the recorded SHA window
- DoD-6: Full suite has zero NEW failures vs the implement-owned frozen name-level baseline (`comm -13` route: `templates/commands/implement.md:64` step 6 `**Test runs**` bullet owns capture; this file does not restate its path) — 2026-10-03 订正(F-16):本行原先把采集路径委托给**运行时镜像里那个已退役的 commands 目录**(该目录不存在——templates 镜像对明确排除 `commands/`,见 `sync-mirrors.py:72` 与本 spec plan.md 的镜像表说明),而 GATE-1 的 `<implement-owned baseline>` 只能经本行锚定,故一个门曾挂在一条死路径上;此处按坐标记录而不复写那条死路径本身
- DoD-7: Self-hosting — this very file passes the tooling it builds: `validate-tasks.py` exits 0 on it with zero green-* findings, and the accountant's uncovered sets are empty beyond the frozen baseline **paired with a non-empty claimed count** for this feature's own artifacts (the plan's dogfooding obligation: 053's own clauses and FRs sit OUTSIDE the baseline面 by T026's exclusion, so they can be claimed but never exempted; the clause/FR counts themselves are re-derived that run, never cited here — volatile measurements per DoD-9)
- DoD-8: The 4 "obligation-with-landing" gaps closed at plan time have their landed counterparts: Tool record `.specify/memory/tools/goal-utils.py.md`, `docs/reference/commands/{team,requirements,tasks}.md`, and both `skills/create-team/references/*` files
- DoD-9: Volatile measurements re-derived at implement start per the re-freeze rule; no artifact cites a number whose owning command has not been re-run this run

**DoD Status**: pending

## Completion Gate

- GATE-1: Zero NEW test failures — check: `bash .specify/scripts/bash/run-tests.sh --names-out <spec-dir>/current-failed.txt -q tests/` then `comm -13 <(sort -u <implement-owned baseline>) <(sort -u <spec-dir>/current-failed.txt)` prints nothing
- GATE-2: Mirror pairs clean per their own criteria — check: `python3 scripts/python/sync-mirrors.py --check --only scripts/python` (relativity vs `notes/pre-change-measurements.md`'s recorded DIFF list: `trigger-utils.py` pre-existed) and `--only` each of `shared/definitions shared/guidelines shared/constants templates/tasks-template.md` returns EXIT=0; AND `--only skills` judged **relatively** against T002's recorded 30-name DIFF list (pair pre-dirty, EXIT=2) while `--only skills/create-team/references/execution-guide.md`, `.../references/goal.md` and `.../scripts/build-summary-input.py` each return EXIT=0 **absolutely** (byte-identical pre-change, measured 2026-10-03) (`/speckit.analyze` E-04); AND `--only templates` judged **relatively** against T002's recorded list (pair pre-dirty: EXIT=2 with **2** DIFFs — `proactive-trigger-seed.json` and `skills-template.md`; this feature writes neither file, but T023's `--write --only templates` is pair-scoped and syncs them anyway, so the read side MUST cover the write side — R2-H9). The per-pair pre-dirty counts and their reconciliation to the whole-tree total are owned by plan.md § Mirror Obligations' 全树 paragraph — this row does not restate them.
- GATE-3: Per-tool command copies current — check: `python3 scripts/python/regen-command-copies.py --check` EXIT=0 (pre-change state measured EXIT=0 on 2026-10-02; the 052-era "large pending regen" note is superseded — do not re-inherit it)
- GATE-4: No open work — check: `grep -cE '^- \[[ >]\]' .specify/specs/053-machine-decidable-artifacts/tasks.md` returns 0
- GATE-5: verification.md covers every SC — check: `comm -23 <(grep -oE 'SC-[0-9]{3}' .specify/specs/053-machine-decidable-artifacts/requirements.md | sort -u) <(grep -oE 'SC-[0-9]{3}' .specify/specs/053-machine-decidable-artifacts/verification.md | sort -u)` prints nothing
- GATE-6: Gate budget neutral and scanner untouched — check: `python3 scripts/python/scan-confirmation-gates.py --summary` shows `total 23 / violations 0` AND `git diff <BASE>..HEAD -- scripts/python/scan-confirmation-gates.py` empty with BASE = the implement-start SHA recorded in `notes/pre-change-measurements.md` (named explicitly so the 052 GATE-3 void — unanchored window — is not repeated)
- GATE-7: Self-validation of this file — check: `python3 scripts/python/validate-tasks.py .specify/specs/053-machine-decidable-artifacts/tasks.md` EXIT=0, zero `green-*` labels in output, and its `[green:]` claims cover **every clause of this feature's own contracts** (clause count re-derived from `contracts/*.md` in the same run, never cited here — DoD-9) — **contract clauses ONLY**: FRs are not a claim target, their coverage is GATE-8's separately-sourced universe (`contracts/green-point-claim.md` C-9…C-11 + FR-016/FR-026; `/speckit.analyze` F-05), see T045/T046
- GATE-8: Coverage accounting green — check: `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/053-machine-decidable-artifacts` → relational sentinel holds (parsed + named == total scanned, the script prints all three) and `LC_ALL=C comm -13 .specify/specs/053-machine-decidable-artifacts/coverage-baseline.txt <(live uncovered)` empty — the path is spelled out because a bare repo-root name makes this gate error as written (F-15), and **`LC_ALL=C` is load-bearing** (2026-10-04 T027 measurement: the names are codepoint-sorted while glibc collation ignores `#`/`/`/`.`, so under `en_US.UTF-8` the baseline's two header lines sort after digit-initial names, `comm` prints `file 1 is not in sorted order` and then echoes all 665 live names as the delta where the true delta is 182 — a wrong verdict that still looks like output; the same run under `LC_ALL=C` gives 182 with empty stderr, agreeing with the script's own locale-independent set difference) — **and** its paired positive companion printed non-empty: this feature's own claimed-clause count > 0. The FR side is reported as an empty set, but note the measured asymmetry (2026-10-03): all 48 of this feature's FRs are already cited from clause 引用组 before any task runs, so FR-emptiness is NOT a red-capable witness on its own — that lane's falsifiability is supplied by C-18's counter-sample (delete one `(FR-nnn)` from a copy of a contract → the accountant MUST name exactly that FR and exit non-zero), which GATE-9 counts. **Absent baseline ⇒ non-zero exit naming the path** (C-21): a gate MUST NOT be made green by its own missing input. The baseline面 excludes this feature's own spec dir (T026), which is what makes the clause-side emptiness falsifiable: with 053's own items inside the baseline, claims landing in T045 could never turn this gate red (`/speckit.analyze` F-07/F-18/R2-H8)
- GATE-9: Evidence completeness — check **per subject, never as one aggregate**, where a subject is every checker this feature creates OR extends: its counter-sample count ≥ that subject's **newly added check units**, and a unit is one of three co-equal kinds — a check label, an exit tier, a verdict vocabulary item (key rule: SC-011; fields: `data-model.md` E-6 `subject`/`breaks`). Both sides come from named owners, so the gate is computable: the **new subset** is enumerated per subject in `data-model.md` § 标签集 (D-5), the **full** label set stays owned by that module's docstring, and per-contract extras are owed by `green-path-divergence` paired (C-27) and `run-checks` one per exit tier (C-18). Derive both sides by command in the same run and paste the per-subject pairs — a typed total is forbidden here, and so is using the full docstring count as the denominator (it counts labels that predate this feature: `validate-tasks.py` carries 6 today and gains 4, so its floor is 4, not 10). The previous form failed both ways: its `≥14 (US1 5 + US2 4 + US3 3 + US4 2 + US5 3)` contradicted its own printed breakdown (17), and its replacement keyed the whole rule on "each NEW checker", which left 3 of its 5 subjects outside the domain and one subject's docstring holding an action roster rather than a label set (`/speckit.analyze` E-02, round-2). Scenario-12 residue probes all 0 WITH their planted positive control run once (a probe that cannot go red proves nothing)
- GATE-10: US1 checker works on reality — check: `python3 scripts/python/validate-requirements.py` on three real existing specs exits 0 each, and each of the four broken copies exits 1 naming exactly its own class (4/4, zero cross-masking)

## Environment Prerequisites

Single landing point for probe conclusions (re-probe on every rerun — never cached); per-phase notes below reference this section only.

- **python ≥ 3.8**: available — probe: `python3 --version` → `3.11.11` @ 2026-10-02; affected: all phases
- **pytest + canonical runner**: available — probe: `python3 -c "import pytest"` → `8.4.2` @ 2026-10-02; `run-tests.sh --names-out` proven in 3 invocations this session (output form: sorted bare names, stderr prints `# failed-name list written: … (N entries)`)
- **External environment (docker/network/cluster/hardware)**: none — this feature is stdlib + local git only; affected: none
- **Real terminal-state goal for SC-007**: partial — probe: `ls -d .specify/goal/*/` → 1 (`draw-two-layer-structure`); `ls -d .specify/teams/*/` → 6 teams + hidden `.work/` (naive `find -type d` counts 7 — the two disagree because `.work` is dot-hidden; say "6 + .work"); the bound goal's terminal status is not established; affected: US4 evidence row — construct the scenario in a repo copy per `contracts/run-checks.md` C-28 rather than mutating real definitions or fabricating a verdict
- **Pre-change mirror drift**: `sync-mirrors.py --check --only scripts/python` → EXIT=2 with `DIFF .specify/scripts/python/trigger-utils.py` (pre-exists this feature) @ 2026-10-02; `shared/definitions`, `shared/guidelines`, `shared/constants`, `templates/tasks-template.md`, `templates/commands` all EXIT=0 @ 2026-10-02; **`skills` pair added 2026-10-03 after `/speckit.analyze` found it missing from plan.md's table** → `--only skills` EXIT=2 with **30** DIFFs (all pre-existing) while the three files T034/T041 write (`create-team/references/execution-guide.md`, `create-team/references/goal.md`, `create-team/scripts/build-summary-input.py`) are each `--only <file>` EXIT=0; whole-tree `--check` = 33 DIFFs (plan.md's first draft said 3). Affected: GATE-2's criteria and DoD-4's per-pair forms
- **Re-freeze timing**: `notes/pre-change-measurements.md`, `coverage-baseline.txt`, and the implement-owned test baseline are frozen measurements — re-capture at implement start per implement.md step 6/8; a row whose re-capture differs MUST carry the new value

## Format: `[ID] [P?] [Story] Description`

- **[P]** different files, no incomplete dependencies; **one line per task** (row-format contract: `templates/commands/tasks.md:155`, machine-enforced by validate-tasks.py itself); `[blockedBy: …]` gates `/speckit.implement`'s topological order
- Path convention for this repo (code-generator shape): sources at root (`scripts/python/`, `shared/`, `templates/`), runtime mirrors at `.specify/` (generated, never hand-edited), tests at `tests/contract/`
- Evidence landing points (fixed, not re-invented per run): `notes/red-first-evidence.md`, `notes/quickstart-run.md`, `notes/pre-change-measurements.md` — created under `.specify/specs/053-machine-decidable-artifacts/notes/` (dir exists; two plan-phase files already in it)

## Task State Sigil

`[ ]` open · `[>]` claimed (multi-agent only) · `[X]` closed with evidence · `[~]` deferred with `<!-- deferred: reason -->` + `verification.md deferred_tasks=` entry. A run is complete at zero `[ ]`/`[>]`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create evidence landing files and capture the re-measurable pre-change baselines once, in one place.

- [X] T001 [P] Initialize evidence landing files `notes/red-first-evidence.md`, `notes/quickstart-run.md`, `notes/pre-change-measurements.md` in `.specify/specs/053-machine-decidable-artifacts/notes/` (dir already exists per plan), each headed by its purpose line and capture date
- [X] T002 Record implement-start baseline facts into notes/pre-change-measurements.md by RUNNING each: `python3 scripts/python/scan-confirmation-gates.py --summary` (expected 23/13/10/0 — paste real), `git rev-parse HEAD` (the BASE SHA for GATE-6), `grep -c 'sub.add_parser' scripts/python/goal-utils.py` (→ 9), docstring-extraction labels of validate-tasks.py (→ the 6: blockedBy, dod-format, id-unique, parallel-safe, row-format, story-labels — trap form: raw `grep -c 'parallel-safe' scripts/python/validate-tasks.py` counts every mention, not the check set, and yields a different number; the authoritative derivation is `re.findall(r'^  ([A-Za-z][A-Za-z-]*)\s{2,}', module.__doc__, re.M)` as `tests/contract/test_validate_tasks_parallel_safety.py:312` does), and the census baseline via the command inside notes/clause-form-census.md run FROM REPO ROOT (→ excl-053 (110, 508); volatile totals MUST NOT be pasted — re-derive per row), noting per that file that a wrong cwd returns (0, 0) silently; AND the mirror pre-change name lists — `python3 scripts/python/sync-mirrors.py --check --only <pair>` over `scripts/python shared/definitions shared/guidelines shared/constants templates/tasks-template.md templates/commands templates skills`, storing every `DIFF`/`MISS` path (2026-10-03: `skills` AND `templates` MUST be in this list — both pairs are already EXIT=2 pre-change (`skills` 30 DIFFs, `templates` 2) and GATE-2's relativity criteria for them have no other source; the third pre-dirty pair is `scripts/python` with 1)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The clause-syntax owner and its executable counterpart — US2's clause resolution and US3's accountant both consume them, so they block story work.

**⚠️ CRITICAL**: No user story phase can start until this phase is complete.

- [X] T003 [P] Author shared/definitions/contract-clause-definitions.md declaring itself the sole owner of contract clause syntax (per `contracts/clause-coverage.md` C-1…C-4 against it): the six-form table with per-form regex, one canonical form for NEW contracts + legacy forms recognized read-only, zero `BLOCKING_PATTERNS` hits in its wording (pre-verify each candidate line against `BLOCKING_RE` before landing — budget headroom is 0, patterns 17), and the canonical pointer line to `shared/guidelines/user-facing-comprehension.md` without restating its class table
- [X] T004 [P] Write unit tests tests/contract/test_clause_forms.py for the to-be-built shared extractor (pure functions MUST have unit tests per Principle IV): each of the six forms extracted by name, the four `.md` forms mutually exclusive (measured same-file co-occurrence = 0 on 2026-10-02), the `md-bold-paren` case from 031's rubric-section.md (10 clauses the closed-bold regex alone would silently drop), OpenAPI detected via `paths:` method keys and MUST NOT probe for a literal `operations:` key, assertions-form via `^\s+- id:`, and the yaml `013-…/portable-skill-creation.openapi.yaml` misnomer (named `.openapi.yaml`, parsed as `yaml-assertions`, 6 ids) — suite MUST be red first: paste output into notes/red-first-evidence.md
- [X] T005 Implement scripts/python/clause_extract.py per tests/contract/test_clause_forms.py [blockedBy: T003,T004]: stdlib-only (no PyYAML — plan D-2; parse-form comment cites gate-check.py:48 hand-parse precedent), exposing `extract_clauses(path) -> list[ClauseId]` and `resolvable(path, clause_id) -> bool`, its module docstring carrying the STR-008 Program-First attribution line and the label enumeration in the `^  label  description` docstring body (contracts/checker-form.md C-5 contract: the SAME extraction regex as T002's), and any parse-doubt `.yaml` falling back to named-unparseable rather than guessed (C-13)
- [X] T006 Sync mirrors for Phase 2 files and verify per plan criteria: `python3 scripts/python/sync-mirrors.py --write --only shared/definitions && python3 scripts/python/sync-mirrors.py --write --only scripts/python` then `--check --only shared/definitions` EXIT=0 and `--check --only scripts/python` showing no NEW DIFF beyond trigger-utils.py's recorded pre-existing one [blockedBy: T003,T005]

**Checkpoint**: Owner doc + extractor exist; US2/US3 can resolve clause ids; US1/US4/US5 could proceed regardless but phase order is sequential here.

---

## Phase 3: User Story 1 - requirements.md 的结构性命题由检查器判定 (Priority: P1) 🎯 MVP

**Goal**: `validate-requirements.py` judges the four structural proposition classes (FR-006…FR-011) with counter-samples, is wired into `/speckit.requirements` step 7, and retires the transitional awk copy (FR-012…FR-014).

**Independent Test**: run the new checker read-only on three real specs → exit 0 each; run it on four broken copies (one per class) → exit 1 each naming exactly its own class (SC-001 4/4); `grep` the taxonomy file → transitional copies 0.

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T007 [P] [US1] Write tests/contract/test_checker_form.py pinning all 33 clauses of contracts/checker-form.md (clause recount at capture 2026-10-02 via `grep -cE '^\*\*C-[0-9]+\*\*' .specify/specs/053-machine-decidable-artifacts/contracts/checker-form.md` → 33; line-count==occurrence-count here because the clause pattern is line-anchored): label-set equality with docstring extraction, exit-code table pins per C-22/C-23 (label pin and exit pin in SEPARATE test functions), read-only write-point scan C-13 (expect 0 write points in the new scripts), json-keys-with-verdict-array C-7/C-8, mirror/packaging C-30…C-32 — red until T009 lands: paste into notes/red-first-evidence.md
- [X] T008 [US1] Write tests/contract/test_requirements_checker.py pinning all 29 clauses against contracts/requirements-checker.md (recount 2026-10-02 → 29), including the five labels `id-contiguous|doc-order|ref-resolvable|marker-count|dup-id`, the C-6 example `FR-7` vs `FR-007` judged a format violation (never normalized), C-12/C-28 mention-vs-reference AND CommonMark N-backtick-run code-span rules with the planted self-test string ("写在 ```` ``` ```` 围栏内的 (FR-020)"), C-29 pair-dedup counting, C-17 marker regex with negative lookbehind, and C-15 reverse `Consumed by` consistency — red first: paste into notes/red-first-evidence.md

### Implementation for User Story 1

- [X] T009 [US1] Implement scripts/python/validate-requirements.py: docstring per C-4/C-5 (STR-008 attribution + five-label body), four checks per FR-006…FR-011, exit table 0/1/2 with the fourth state ("empty or skeleton-only") as a `status` value not a code (D-6), `--json` including per-check verdict array and human tail line `N error(s), N warning(s)` (STR-003), read-only [blockedBy: T007,T008]
- [X] T010 [US1] Evidence: run the checker on requirements.md of this spec plus two other real specs (exit 0, paste full output) and on the four broken copies built by quickstart.md scenario 3's commands run VERBATIM (each exits 1 naming exactly its class; SC-001), writing all outputs plus the FR-043 real-artifact run into notes/red-first-evidence.md [blockedBy: T009]
- [X] T011 [P] [US1] Wire the call into templates/commands/requirements.md step 7 (measured @ 2026-10-02: the Quality Validation block sits at :62-66) per contracts/requirements-checker.md C-18/C-19: invoke after spec write, STOP on any ERROR, present checker output verbatim, keep checklist pass/fail update after clarification write-back (FR-013); then `python3 scripts/python/regen-command-copies.py` and verify the 4 per-tool copies of speckit.requirements each contain the new line
- [X] T012 [P] [US1] Edit shared/guidelines/requirements-guidelines.md § Validation Process (real heading is `### Validation Process` at :50 under `## Specification Quality Validation` — verify, do not assume a `## Validation Process` heading; naive `grep '^## Validation Process'` returns nothing) adding "counts and reference resolution derive from the checker, never hand-typed" and the post-write-back timing, WITHOUT claiming an existing count-set owner (the taxonomy's pointer to "the full count set" is a dangling ownership claim already escalated as plan A-1 — do not inherit it into this file)
- [X] T013 [US1] Pay the FR-014 debt in ONE commit: remove from shared/constants/clarify-taxonomy.md the transitional awk block (lines 108-112, discriminators measured 2026-10-02: `ORDER BREAK: %s after %s` ×1, `Until that validator ships` ×1, `shares one implementation` ×1) and the sentence, re-point the invariant at validate-requirements.py, AND amend BOTH pinning tests `test_c4_extraction_is_definition_anchored_and_history_excluded` (:311, whose `:324` message literally asserts the block IS present) and `test_c4_shared_implementation_with_the_requirements_validator_is_declared` (:336) in tests/contract/test_clarify_semantic_completeness.py to assert the NEW state — trap note: `grep -c 'def test_c4'` finds THREE functions (:288, :311, :336) but only :311 and :336 pin the block (:288 verified not to); rewriting :288 would break an unrelated assertion [blockedBy: T009]
- [X] T014 [US1] Sync mirrors for US1 files (`sync-mirrors.py --write --only scripts/python --only shared/guidelines --only shared/constants` then `--check` each: scripts/python judged relative per Environment Prerequisites, others EXIT=0) and run `python3 scripts/python/test… none — verify by re-running the two amended test files green: python3 -m pytest -q tests/contract/test_clarify_semantic_completeness.py tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` [blockedBy: T009,T012,T013]
- [X] T015 [US1] Landing hygiene for this phase: run `python3 scripts/python/scan-confirmation-gates.py --summary` (total MUST still be 23) and a BLOCKING_RE zero-hit pass over every file US1 touched incl. the 4 regenerated copies; fix wording, never budgets (FR-045) [blockedBy: T011,T014]
- [X] T016 [US1] [blockedBy: T015] Story checkpoint per Independent Test: T010's runs green, mirrors green, hygiene green — record the outcome line in notes/red-first-evidence.md

**Checkpoint (MVP)**: US1 independently delivered — the requirements-side proposition is machine-judged and the transitional copy is gone.

---

## Phase 4: User Story 2 - 绿点归属声明面 (Priority: P1)

**Goal**: `[green: <contract>#<clause>]` becomes a parseable surface (FR-015…FR-021) with four checks in validate-tasks.py, EXPECTED_CHECKS grown 6→10 in the same commit, and the D-7 write-classification collision fixed structurally.

**Independent Test**: validator on a tasks.md with consistent claims exits 0 with zero WARN; the fenced/悬空/cross-phase/collision counter-samples each report exactly their class; the D-7 pair (positional same-path control still WARNs; green-tag shared-contract does NOT).

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T017 [P] [US2] Write tests/contract/test_green_point_claim.py pinning all 27 clauses of contracts/green-point-claim.md (recount 2026-10-02 → 27): four-tuple parse, ERROR vs WARN severities, C-14 warn-only exits 0, C-17 the two collisions reported separately, and the C-21/C-24 pair — the shared-contract two-`[P]`-rows case MUST NOT warn while the same-write-path control MUST warn (anti-vacuity for the very fix) [blockedBy: T005] — red first: paste into notes/red-first-evidence.md

### Implementation for User Story 2

- [X] T018 [P] [US2] Add the declaration surface to templates/tasks-template.md inside the Format section beside the blockedBy-tag definition line (measured @ 2026-10-02: that definition sits at template :104; the template itself holds no single-line rule — that is owned by templates/commands/tasks.md:155, reference it, do not restate it) with the STR-001 literal tag `[green: <contract>#<clause>]`, project-neutral wording (grep repo names → 0) [blockedBy: T017]
- [X] T019 [US2] Implement in scripts/python/validate-tasks.py: extract green claims BEFORE `_classify_paths` sees the row (structural orthogonality per C-22 — do NOT extend POINTER_GOVERNOR's closed governor-word list), resolve clause existence via scripts/python/clause_extract.py (C-11), add `green-dangling` (ERROR) + `green-cross-phase` (WARN, comparing the existing monotonic `order` counter :171/:181 — there is NO numeric phase index; precedent :229-233) + `green-clause-collision` + `green-path-divergence` (test-path × differing green points, mechanizing the prose obligation at templates/commands/tasks.md:197), docstring label body extended to 10 labels [blockedBy: T017,T018] — **(2026-10-04 实跑扩了一处上游缺口,已回写)**: landing this row exposed that FR-020 named only fenced blocks while the house rule it is an instance of (FR-009, and `requirements-checker.md` C-28's CommonMark N-backtick-run clause) also excludes **inline code spans** — T018's row must *name* the tag to define it, and the first implementation parsed that mention as a claim on a contract file literally named `<contract>`, so 053's own tasks.md failed its own GATE-7; fixed in the subject by routing the declaration view through the existing `clause_extract.strip_code_spans` (not by making T018's row dodge the literal, which would leave no document able to name its own markup), and written back to FR-020 + C-8 + `## Clarifications` → Session 2026-10-04, pinned in both directions (`test_c8b…` mentions excluded, `test_c8c…` an unclosed span still declares)
- [X] T020 [US2] Same commit as T019: extend EXPECTED_CHECKS (:75-82) and any docstring-shape assertions in tests/contract/test_validate_tasks_parallel_safety.py 6→10 and add the new-tier exit assertions to test_c5_exit_code_table (:346) without altering existing tier semantics (contracts/checker-form.md C-25/C-26) [blockedBy: T019]
- [X] T021 [US2] Point the prose self-check at templates/commands/tasks.md:197 (verbatim obligation measured present ×1 @ 2026-10-02) at the new `green-path-divergence` check instead of manual diligence — one criterion, not two — then `regen-command-copies.py` and verify the 4 speckit.tasks copies carry the change
- [X] T022 [US2] Evidence: run validator over 053's own tasks.md AFTER this phase and paste: exit 0 today is IMPOSSIBLE (this file contains no `[green:]` claims yet — claims land in T045), so paste the counter-sample battery from quickstart scenario 5's seven samples each hitting exactly one label, into notes/red-first-evidence.md [blockedBy: T019,T020] — **(2026-10-04 前提被实跑推翻,已回写)**: this row's "exit 0 today is IMPOSSIBLE" is false — measured after US2 landed, `python3 scripts/python/validate-tasks.py` on this very file gives `PASS … 0 error(s), 0 warning(s)` EXIT=0, and the row's reasoning was backwards (a file carrying no claims exits 0 *because* nothing can fail on it, which is the expected verdict rather than an impossible one); the row's actual intent — the battery, since this feature's own claims only arrive at T045 — ran 7/7 with each sample hitting exactly its own label and residue 0 (`/speckit.analyze` F-25 measured the same exit)
- [X] T023 [US2] Sync mirrors + hygiene: `sync-mirrors.py --write --only scripts/python --only templates` … `--check --only templates/tasks-template.md` EXIT=0, scripts/python relative-criterion vs pre-change list; scanner total still 23; templates repo-name grep 0 [blockedBy: T019,T021]

**Checkpoint**: green-point ownership is parsed, four checks live, EXPECTED_CHECKS=10 pinned; US3's claimed-subset input now exists.

---

## Phase 5: User Story 3 - 覆盖核算 (Priority: P2)

**Goal**: the accountant prints uncovered sets as relational set differences over owner-declared forms (FR-022…FR-028), with the FR-027 frozen name-level baseline; 053's own contracts join the scanned surface (re-measured live 2026-10-02: total files 117, volatile — NEVER paste as a premise, re-derive at implement start).

**Independent Test**: minimal 3-clause contract with 2 claims → exactly the 1 uncovered printed with `UNCOVERED:` prefix;补 claims → empty + non-zero companion; relational sentinel holds on the full-tree scan; only-new-uncovered items block.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T024 [P] [US3] Write tests/contract/test_clause_coverage.py pinning all 27 clauses of contracts/clause-coverage.md (recount 2026-10-02 → 27): relational sentinel (parsed+named==scanned-total, MUST NOT pin a literal total), collapsible name list, `.yaml` explicit disposition, C-15 zero-clause-parseable file named (never silently covered), C-25 baseline discipline via `comm -13`, and MUST-NOT-copy of the broken `scan-confirmation-gates.py --baseline` shape (nested-key trap; plan A-3) [blockedBy: T005] — red first: paste evidence

### Implementation for User Story 3

- [X] T025 [US3] Implement scripts/python/account-clause-coverage.py: single entry, read-only, `--spec-dir` + `--json` + collapsible `--list-named`, clause universe via clause_extract.py, claims = `[green:]` targets restricted to **contract files + clause ids** (FR-015/FR-016 — a claim aimed at a non-contract file IS `green-dangling`, and no task row may designate a second target form in prose, which is exactly what FR-021 forbids; the earlier "(this row DESIGNATES that convention)" wording is removed per `/speckit.analyze` F-05), FR-universe from requirements.md (`FR-\d+` definition lines OUTSIDE code spans — the C-28/C-29 rules from T008 apply to this script too) with its **claimed side taken from each clause's 引用组** (C-2's three-part rule: block = marker line to the next marker OR next section heading, whichever first; group = the block's last parenthetical containing an FR/SC id, tolerating one nesting level and expanding `FR-a…FR-b` ranges; ids outside the group are mentions, not citations — FR-009), NOT from `[green:]` — the rule itself is declared by FR-026 and judged by C-18, this row only implements it, clause-uncovered and FR-uncovered reported as two separate sections with two separate sources (FR-026), exit 0 only when both empty-beyond-baseline with companions non-zero [blockedBy: T019,T024]
- [X] T026 [US3] Freeze `.specify/specs/053-machine-decidable-artifacts/coverage-baseline.txt` at the **first full-tree accounting run after T025** — NOT at the first *green* one: green would require the baseline while the baseline requires a run, which is circular (C-21 触发条, `/speckit.analyze` F-18; the same instant is what `data-model.md` E-3c `frozen_at` and FR-027 § 基线面 name), **over the corpus EXCLUDING this feature's own spec dir** (FR-027 § 基线面 → the `excl-053` census basis, so 053's own clauses sit outside the baseline permanently and can be claimed but never exempted; the file holds clause names, so the FR lane has no baseline at all — that gap is recorded as `research.md` **A-7**, not decided here): uncovered clause NAMES sorted one-per-line + header recording owner-form-set, BASE SHA, the excluded corpus selector and the C-2 extraction-rule version (C-23: two counts from different owner-declarations are incomparable otherwise; a baseline that includes this feature's own items makes GATE-8 green whether or not any claim ever lands — F-07); the accountant MUST exit non-zero while this file is absent (C-21) [blockedBy: T025]
- [X] T027 [US3] Evidence: run the accountant on the full tree and on quickstart scenarios 6/7 inputs; paste the three-number relational output (re-derive totals live, do not cite this row's numbers) and one `comm -13` delta proof into notes/quickstart-run.md [blockedBy: T026]
- [X] T028 [P] [US3] Counter-samples for C-13/C-15 and the misnomer: a stream-style `.yaml` copy falls back to named (not guessed-zero), a parseable-but-zero-clause `.md` is named with companion incremented, the `013-…` misnamed yaml resolves via content not extension — all in temp dirs, residue 0 after [blockedBy: T025]
- [X] T029 [US3] Sync mirrors + hygiene for US3 files (scripts/python relative-criterion; scanner total 23) [blockedBy: T025,T027]

**Checkpoint**: coverage is printed, not claimed; 053's own contracts are in the denominator.

---

## Phase 6: User Story 4 - run-checks (Priority: P2)

**Goal**: `goal-utils.py` gains action `run-checks` emitting the five-check JSON verdict in one call (FR-029…FR-034), reusing the existing EXIT_* constants' meanings with `blocked`=5, zero-write, first CLI exposure of `preview_target_check`/`resolve_effective_target`.

**Independent Test**: one call → 5 checks with fields per C-9; checksum of `.specify/goal/`+`.specify/teams/` byte-equal before/after; blocked exit 5 / input-error 2 / unparsable 4 mutually distinguishable; no-target run yields ②③④ `not-evaluated` while ①⑤ evaluate.

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T030 [P] [US4] Write tests/contract/test_run_checks.py pinning all 28 clauses of contracts/run-checks.md (recount 2026-10-02 → 28): closed exit-table pin in the `test_trigger_engine.py:48` + `:292` + `:392/:395` shape (EXIT_CODES dict, per-action loop, CLOSED roster assert — note `goal_utils.EXIT` currently has ZERO test imports, measured 2026-10-02), zero-write via byte checksum, C-7 target-less wrapper semantics, C-10 in its CORRECTED satisfiable form (≥1 name outside the verdict vocabulary — `goal-binding` — plus pinned per-check name→possible-verdict mapping; MUST NOT assert disjointness: 4 of 5 names ARE verdict literals at source :643/:660/:665/:669), C-14 `not-evaluated` constant defined once, C-15 `rejected` untouched (source :935/:968 hit count unchanged before/after), `read:` help-label first word [blockedBy: T001] — red first: paste evidence

### Implementation for User Story 4

- [X] T031 [US4] Implement in scripts/python/goal-utils.py: `EXIT_BLOCKED = 5`, subparser `run-checks` with `read:`-first help, thin wrapper (no `--target` → resolve via :679, ②③④ `not-evaluated`, ①⑤ evaluated), reuse `preview_target_check` :626 verbatim for per-target checks, emit through `_emit` :1004, extend docstring action roster (:16-30) and exit-code table (:32) in the SAME commit (contracts/run-checks.md C-24); existing four EXIT constants' values byte-unchanged [blockedBy: T030]
- [X] T032 [US4] Extend the hardcoded action tuple in tests/contract/test_goal_definition.py (:249-251, the 9-tuple ending `"migrate", "targets"`) to include `run-checks` so the new action is pinned, not silently unguarded (C-23) [blockedBy: T031]
- [X] T033 [US4] Add the ONE invocation form to templates/commands/team.md five-check block (measured @ 2026-10-02: block at :114-119 names all five but contains NO CLI invocation line — that assembly gap is the recorded backlog item this closes); keep :96/:98's 0/2 branches valid; `regen-command-copies.py` + verify 4 speckit.team copies [blockedBy: T031]
- [X] T034 [P] [US4] Update the doc/skill surfaces that describe the five checks so no second criterion survives: docs/reference/commands/team.md (:68,:70), skills/create-team/references/execution-guide.md (:27,:30), skills/create-team/references/goal.md (:45) — each points at the `run-checks` invocation
- [X] T035 [P] [US4] Update the Tool record .specify/memory/tools/goal-utils.py.md:39 (measured: lists 6 subcommands `create/validate/list/status/criteria/migrate` against the then-9-action binary; go to 10 incl. `run-checks`) + its exit-code list incl. 5 — Principle XII: a stale authoritative record outranks model knowledge downstream (T031)
- [X] T036 [US4] Evidence: run `run-checks --json` on the real bound team (`.specify/goal/` holds exactly 1 goal; teams 6+.work) + a temp-copy team for blocked/unparsable/input tiers + a constructed no-target case; if no real terminal-state goal exists, follow Environment Prerequisites and notes the unavailability honestly per C-28 — MUST NOT fabricate a verdict; paste all runs into notes/quickstart-run.md [blockedBy: T031,T032,T033,T034,T035]
- [X] T037 [US4] Sync mirrors + hygiene for US4 files (scripts/python relative; team.md copies regen; scanner total 23; PLUS `--only skills` — T034 writes `skills/create-team/references/{execution-guide.md,goal.md}`, whose `.specify/skills/` mirrors are byte-identical pre-change, so sync them and verify per-file EXIT=0; the pair as a whole stays relational against T002's recorded 30-name DIFF list) [blockedBy: T036]

**Checkpoint**: one call answers "is this team run-blocked", machine-readably, without touching a byte.

---

## Phase 7: User Story 5 - 判据主体指代形 (Priority: P3)

**Goal**: `[subjects: <glob>]` makes a criterion's subject set derived at parse time (FR-035…FR-038), with two distinguishable empty/failure states, a decidable conflict rule, and an explicit second-parser disposition.

**Independent Test**: same subject set written two ways; add/remove a member in a temp copy → reference form's set moves, enumeration's does not (SC-009); all existing goal definitions parse identically before/after compared by name (SC-010, with its ≥1-count companion).

### Tests for User Story 5 (MANDATORY) ⚠️

- [X] T038 [P] [US5] Write tests/contract/test_criterion_subject.py pinning all 19 clauses of contracts/criterion-subject.md (recount 2026-10-02 → 19): both failure states distinguishable, `SUBJECT EMPTY:` prefix, brace-expansion co-occurrence conflict, V-32 honesty boundary asserted as a documented limitation, V-34 anti-vacuity (goal count ≥1 companion), and the C-14 second-parser disposition test (build-summary-input.py:354-391 re-parses by design — its :356-360 comment proves intent; test asserts whichever disposition the owner doc records) [blockedBy: T001] — red first: paste evidence

### Implementation for User Story 5

- [X] T039 [P] [US5] Add the reference-form section to shared/definitions/goal-definitions.md (verified @ 2026-10-02: NO glob/dir-reference form exists there — grep returns nothing; 137 lines, 9 headings — ADD a section, touch no existing one): `[subjects: <glob>]` semantics, repo-root-relative globbing, the two failure states, conflict rule + its stated undecidable boundary, and the build-summary-input disposition (T041's decision written as normative text) [blockedBy: T038]
- [X] T040 [US5] Implement parsing in scripts/python/goal-utils.py per T038: derive member set at parse time; missing path → distinguishable error; empty derivation → `SUBJECT EMPTY:`; brace co-occurrence → conflict error; pure-enumeration criteria parse EXACTLY as before (FR-038) — run SC-010 name-level before/after over all existing goal definitions WITH the ≥1-count companion (V-34) [blockedBy: T031,T038,T039] — T031 is a blocker because both rows write `scripts/python/goal-utils.py`; without this edge the tags did NOT encode the serialization the Dependencies section claims (2026-10-03, `/speckit.analyze` F-06)
- [X] T041 [US5] Execute the second-parser disposition chosen in T039 inside skills/create-team/scripts/build-summary-input.py (understand `[subjects:]` locally — cross-tree import is forbidden by its own :356-360 comment — or leave it and record the divergence consequence where users will see it); MUST NOT solve by adding the import [blockedBy: T039]
- [X] T042 [US5] Evidence: SC-009 two-way demo in a temp skills-copy (add/remove member → one set moves, one does not), counter-samples for both failure states and the conflict, all into notes/quickstart-run.md [blockedBy: T040,T041]
- [X] T043 [US5] Sync mirrors + hygiene (shared/definitions absolute-OK per pre-change list; scripts/python relative; `--only skills/create-team/scripts/build-summary-input.py` absolute per the pre-change EXIT=0 recorded by T002 — the pair as a whole is relative, 30 pre-existing DIFFs; goal-definitions.md is also inside the gate-scan surface AND named by test_goal_targets_engine.py:296 AUTHORITY — verify that suite stays green; scanner total 23) [blockedBy: T039,T040]

**Checkpoint**: subject sets are derived, not retyped; the repo's own history (:36/:37 six→seven rewrite churn) is the cautionary exhibit.

---

## Phase 8: Polish & Cross-Cutting Concerns

- [ ] T044 [P] Write and run tests/contract/test_neutrality_budget.py pinning all 19 clauses of contracts/neutrality-budget.md (recount 2026-10-02 → 19): budget 23 triple-form + meta-pin warning, templates neutrality grep per-file, closed two-channel trigger set, no new state machines, name-level comparison forms only
- [ ] T045 Retro-fit `[green:]` claims into the rows of .specify/specs/053-machine-decidable-artifacts/tasks.md generated mechanically from feature-ref.md's FR→clause table — **182 clause claims over 7 contract docs only** (the "+ 48 FR claims onto requirements.md#FR-NNN" half is DROPPED per `/speckit.analyze` F-05: FR-015/FR-016 make the claim surface contract-only, and FR coverage is the accountant's separately-sourced universe under FR-026 — see T025), and the placement rule this row previously lacked: each contract's FULL clause set is claimed by the row that pins that contract (T007/T008/T017/T024/T030/T038/T044), so every clause is claimed exactly once and the generated set is deterministic rather than invented per clause, keeping every row single-line and its existing state sigil intact — the claims were inert text before US2 landed; they are parseable now
- [ ] T046 Self-hosting acceptance: `python3 scripts/python/validate-tasks.py` this tasks.md → exit 0 with zero findings; `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/053-machine-decidable-artifacts` → clause-uncovered and FR-uncovered both empty **and both non-trivially so**: this feature's own items are outside coverage-baseline.txt by construction (T026's exclusion), so the run MUST also print the positive companions — 053's own claimed-clause count == its own clause count and 053's own FRs each cited from ≥1 clause 引用组 (C-2's rule), both counts re-derived this run, never pasted (C-21's paired criterion; the FR-side emptiness is red-capable only through C-18's delete-one-citation counter-sample, which GATE-9 must show — R2-H8) — Feature 053 must pass the tools it exists to build (DoD-7) [blockedBy: T045]
- [ ] T047 Run quickstart.md end-to-end — all 12 scenarios, teardown steps to the same standard as setup, real outputs appended to notes/quickstart-run.md; scenarios 3/5/6/8/9/10's previously-unrunnable halves become runnable now [blockedBy: T046]
- [ ] T048 [P] Volatile-number sweep: grep every artifact this feature owns for census/label/clause counts written as literals, re-derive each with its declared command (re-freeze rule from Environment Prerequisites), correct any that moved — MUST NOT leave a stale literal citing a moved measurement [blockedBy: T047]
- [ ] T049 [P] Full-suite name-level regression per GATE-1 (capture owned by implement step 6 — this row only runs the comparison), then `verification.md` completed: all 12 SC status lines, deferred list, DoD Status line, gate re-validation evidence — the Pre-Status-Flip Gate (`.specify/shared/workflow/feature-integration.md`) belongs to `/speckit.implement`, this row prepares its artifact, it does not flip Feature status [blockedBy: T047,T048]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: none — start immediately
- **Foundational (Phase 2)**: after Setup; BLOCKS US2/US3 (clause resolution) and every mirror-touching phase
- **US1 (Phase 3)**: after Foundational; independent of US2-US5 — 🎯 MVP
- **US2 (Phase 4)**: after Foundational; blocked by T005 (resolution) and its own red tests
- **US3 (Phase 5)**: blocked by US2 (T019 — claims must exist to count claimed) and T005
- **US4 (Phase 6)**: after Foundational; fully file-disjoint from US1/US2/US3/US5 (its own rows in goal-utils.py; US5 shares that file — see cross-story note)
- **US5 (Phase 7)**: after Foundational; shares scripts/python/goal-utils.py with US4 → serialize T040 after T031
- **Polish (Phase 8)**: after all desired stories

### Cross-story note (file conflict, not story dependency)

T031 (US4) and T040 (US5) both edit `scripts/python/goal-utils.py`: they MUST NOT run in parallel; order T031 → T040. The `[blockedBy]` tags encode this.

### Parallel Opportunities

- Phase 2: T003 ∥ T004; Phase 3: T007 ∥ T008; T011 ∥ T012; Phase 6: T034 ∥ T035; Phase 8: T048 ∥ T049 (different files)
- After Foundational, the four stories US1/US2/US4/US5 may proceed in parallel by different workers EXCEPT the T031/T040 file serialization; US3 starts only after US2's T019

## Parallel Example: Foundational + US1 tests

```bash
# Task: "T003 author shared/definitions/contract-clause-definitions.md"   &
# Task: "T004 write tests/contract/test_clause_forms.py (red)"             — different files, no shared target
# Task: "T007 write tests/contract/test_checker_form.py"                   &
# Task: "T008 write tests/contract/test_requirements_checker.py"            — two new files, zero overlap
```

## Implementation Strategy

### MVP First

MVP scope rule applied: US1 alone is P1 AND independently checkpointed → **MVP = Phase 1 + 2 + 3 (US1)**. US2 is the second P1 increment (formalizes an existing prose duty; together they close the self-reporting gap end-to-end).

1. Setup → Foundational → US1 → STOP, run the four broken-copy battery (T010) → MVP demo: the requirements side is machine-judged, transitional copy retired
2. US2 → green claims + 4 checks; EXPECTED_CHECKS 6→10 green
3. US3 → accountant + baseline; 053's own surface counted
4. US4 → run-checks; US5 last (P3)
5. Polish → self-hosting (T046) is the capstone proof

### Stop Rules

Any GATE red → fix forward as a task; 3 consecutive failed re-validations of the same gate with no newly closed item → STOP and escalate (implement step 8). `[~]` over silent `[ ]`.

## Notes

- Feature list review at generation time (tasks-phase duty): no new/deprecated Feature discovered beyond the two candidates already parked in features/053.md § Future Evolution (exit-code-table owner; contract-migration wave); Feature 053 stays `Planned` — status transitions are owned downstream
- Claims added by T045 make this file self-referential by design; that is the point, not an accident to prune
- One-time premise trap ledger for implement: `^awk ` (unanchored) missed the taxonomy block once; `--only … | tail; $?` yields tail's code; MIRROR_PAIRS greps noisy, introspects to 5; team-dir count 6 vs 7 hidden `.work`; three test_c4 functions but two pin the block
