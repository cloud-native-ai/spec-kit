# Tasks: 元技能治理：机制/策略分离与技能引用归一化（Meta-Skill Governance）

**Requirement ID**: 082
**Requirement Key**: `082-mechanism-policy-separation`
**Related Feature**: 082 元技能治理：机制/策略分离与技能引用归一化（from `.specify/memory/features.md`)
**Input**: Design documents from `.specify/specs/082-mechanism-policy-separation/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), research.md, data-model.md, contracts/ (4 files), quickstart.md, feature-ref.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is MUST-level — `pytest` MUST-rows in `.specify/memory/constitution.md` § IV; plus Principle VII "Template-only features" gate, which for this doc-feature means **structural** contract tests on artifact content rather than runtime unit/integration tests). The carriers are fixed by name in `contracts/guard-and-measurement.contract.md` GM-01 (6 modules) and GM-11 (5 modules + 1 test-only helper); GM-07 additionally requires one negative-case assertion per module. Red-first shape is pinned there: every new module goes red as **artifact-missing**, never as an import or collection error. The `skill-reference` side is green from its first authoring row because its matrix rows are authored by the same row that runs them (T031's own note).

**Organization**: Tasks are grouped by user story so each story is independently implementable and testable. **One package, no slices** — plan.md § D8: 30 FR / 9 SC under `fr_ceiling=60`, natural task estimate ≈ 36 under `task_ceiling=80`, `decomposition-check.py --mode plan` → `decision=proceed` (re-measured at generation, § Environment Prerequisites).

**Two capabilities, one file set**: `create-skills` / `improve-skills` / `merge-skills` each carry **two** landing points — the mechanism/policy judgement (US1–US3) and the skill-reference coordinate (US5). Each such `SKILL.md` is rewritten **once**, satisfying both landings in that one row; no file is scheduled twice. `coaching-skills` and `run-skills` carry only the skill-reference landing (US5).

## Definition of Done (DoD)

- DoD-1: `shared/definitions/mechanism-policy-definitions.md` and `shared/definitions/skill-reference-definitions.md` exist as the **only** owners of their facts, each declaring up front what it owns and does not own; no consumer restates an acceptance-form list, a normalisation order, a failure table, a symptom table or the membership table
- DoD-2: The three `included` meta-skills (`create-skills`, `improve-skills`, `merge-skills`) each carry **one** mechanism/policy judgement line plus an owner-path reference at its existing step, and each passes on a correctly layered sample without demanding additions
- DoD-3: The five consumers (`run-skills`, `create-skills`, `improve-skills`, `merge-skills`, `coaching-skills`) each declare only their own parameter names and carry **exactly one** reference to the owner's **framework-source** path; `coaching-skills` and `run-skills` carry **zero** mechanism/policy literals
- DoD-4: The eleven contract modules and the one test-only helper exist under `tests/contract/`, the normalisation matrix lives at `tests/fixtures/skill-reference/normalization-matrix.json`, and every module carries at least one negative-case assertion (GM-07)
- DoD-5: SC-001…SC-009 each have their declared carrier in place: the six test-borne criteria green on the final tree, the three sample-borne criteria recorded in `test-evidence/` (SC-001 / SC-002 / SC-005), and no criterion claimed beyond what its reading supports
- DoD-6: Both regeneration entries are re-run and their `--check` exits 0 with **zero new drift**; `regen-command-copies.py --check` proves the command surface is unchanged (27 templates, zero per-tool copy change)
- DoD-7: The frozen-hash registration in `tests/contract/test_expression_compatibility.py` carries exactly the five registration points D7 names (four new keys + one updated existing key), with the hash list, `WIRING_SKILLS` and every assertion left intact
- DoD-8: `.specify/memory/glossary.md`, `.specify/shared/definitions/framework-map.md` and `CHANGELOG.md` each carry their single registration line; no second classification data file, no second gate script, no new directory root, no new environment variable and no new `/speckit.*` command was introduced
- DoD-9: The targeted set's failure-name difference against the recorded baseline is empty and every new module is green; no pre-existing failure was folded into this feature's verdict
- DoD-10: Every `final`-path success criterion reads `pass` in `verification.md` and the feature's smoke record is present, or the unmeasurable one is disclosed with its reason rather than folded into `green`

**DoD Status**: pending

## Completion Gate

- GATE-1: The eleven new contract modules green — check: `env -u PYTHONPATH bash scripts/bash/run-tests.sh -q tests/contract/test_mechanism_policy_owner_doc.py tests/contract/test_mechanism_policy_ownership.py tests/contract/test_mechanism_policy_skill_wiring.py tests/contract/test_mechanism_policy_guard.py tests/contract/test_mechanism_policy_missing_policy.py tests/contract/test_mechanism_policy_decidability.py tests/contract/test_skill_reference_grammar.py tests/contract/test_skill_reference_matrix.py tests/contract/test_skill_reference_consumers.py tests/contract/test_skill_reference_command_surface.py tests/contract/test_skill_reference_failures.py`
- GATE-2: Targeted-set failure names are a subset of the recorded baseline — check: `env -u PYTHONPATH bash scripts/bash/run-tests.sh -q --names-out /tmp/082-head-names.txt <the 12 modules recorded in test-evidence/plan2026-11-05-baseline.txt>` then `comm -13 <baseline names set> /tmp/082-head-names.txt` prints nothing
- GATE-3: No new drift on either regeneration entry — check: `python3 scripts/python/sync-mirrors.py --check` and `python3 scripts/python/regen-command-copies.py --check` both exit 0, with `shared/` pair `ok` and zero changed command copies
- GATE-4: Every changed path inside SC-003's comparison unit is registered — check: `git diff --name-status 3ffeb26e..HEAD -- skills/ templates/commands/` lists only paths present in `data-model.md` § GM-03 rows 1–8
- GATE-5: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/082-mechanism-policy-separation/tasks.md` returns 0
- GATE-6: The mechanism/policy judgement did not leak into the excluded members — check: `grep -rcE 'mechanism-policy-definitions|Mechanism / policy separation|mechanism-in-policy|policy-in-mechanism' skills/external/coaching-skills skills/internal/run-skills` returns 0 for **every** file it lists (recursive: each `SKILL.md` plus that skill's `references/**`); the scanned file count is printed, never only the zero. Scope owner: `contracts/skill-wiring.contract.md` SW-05 (M-08 alignment) — the recursive form is the same denominator as T027's `skills/**/SKILL.md` scan, widened to the two excluded members' own `references/`
- GATE-7: The skill reference is sourced from the framework root, never the mirror — check: `grep -rc '\.specify/shared/definitions/skill-reference-definitions\.md' skills/**/SKILL.md skills/internal/run-skills/SKILL.md` reports 0, while each of the five consumers carries exactly one `shared/definitions/skill-reference-definitions.md`
- GATE-8: Every `final`-path success criterion is `pass` and the smoke record is present — check: in `verification.md`, each criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (an existing, non-empty path) are all present. A `final`-path criterion in `blocked` / `deferred` / `fail` fails this gate unless an explicit user waiver names that criterion. Condition set owner: `shared/workflow/acceptance-hardening.md` § Gates — this row carries the check, not a second schema
- NOTE (not a gate, applies to GATE-8): GATE-8 is the template's `final`-path gate. Its `smoke_command=` / `smoke_exit_code=` / `smoke_evidence_path=` fields are written by `/speckit.implement`'s acceptance flow, which has not run at this stage; if that flow turns out not to write them for this feature, GATE-8's premise is measurably false and `/speckit.implement` MUST record the void per the template's `green-with-void` rule rather than leaving the gate silently unmet. This row is a note about the next stage, not a second gate.

## Environment Prerequisites

Probe verdicts are this section's to own. Planning-time premises stay in `plan.md` § Execution Premises (EP-001…EP-007) and dependency-inherited records stay in `plan.md` § Inherited Blockers; each verdict below carries the probe command that produced it and the date it was run, and is restated nowhere else.

- EP-001 — Python 3 + pytest + git runner — **available** — probe: `env -u PYTHONPATH .venv/bin/python --version` @ 2026-11-05 (plan-time reading recorded in `test-evidence/plan2026-11-05-baseline.txt`: `Python 3.14.6`, `pytest 9.2.0`, `git version 2.54.0 (Apple Git-157)`); affected tasks: T028–T036, T040, T041
- EP-002 — a supported agent host able to load and run a meta-skill flow — **available** (host availability only; the host name + version string are still uncollected at plan time) — probe: this stage itself ran as a native sub-agent on the same host, and the requirements / clarify / plan / tasks stages all executed in it @ 2026-11-05; affected tasks: T043, T044
- EP-003 — the three edited `SKILL.md` files already exceed the `skill-shape.py` 5000 controllable-token budget **before** this feature — **available** (debt, not an outage) — probe: `python3 skills/external/improve-skills/scripts/skill-shape.py <skill>` @ 2026-11-05 per `plan.md` § EP-003 → exit 10 on `create-skills` ≈ 5354 / `improve-skills` ≈ 5584 / `merge-skills` ≈ 5096; affected tasks: T040
- EP-004 — SC-003's comparison unit is non-empty, enumerable, and drift-free against the baseline — **available** — probe: `git ls-tree -r --name-only 3ffeb26e -- skills/ templates/commands/ | wc -l` → `575` (548 skills + 27 templates) @ 2026-11-05; the working tree's own `git status --porcelain` for these two roots was non-empty at generation time (the concurrent implementation's uncommitted edits), which is the state SC-003 measures **against** the baseline, not drift in the baseline; affected tasks: T033, T041
- EP-005 — both regeneration entries are drift-free before any edit — **available** — probe: `python3 scripts/python/sync-mirrors.py --check` @ 2026-11-05 → six pairs all `ok` (`templates 22` / `skills-external 409` / `skills-internal 138` / `agents 3` / `scripts 119` / `shared 63`); `python3 scripts/python/regen-command-copies.py --check` → `OK: all per-tool command copies match the source templates`, rc 0; affected tasks: T001, T039
- EP-006 — "zero new scripts" is deliverable because every decidable part already has a carrier — **available** — probe: `ls tests/contract/ | grep -cE 'mechanism_policy|skill_reference'` → `0` (eleven new modules, no new `scripts/` file) @ 2026-11-05; affected tasks: T028–T038
- EP-007 — the skill-reference landing premises — **partial**: (b) and (c) verified at plan time (the 14-line probe closes the command-vs-path collision and the `.md` non-stripping rule), (a) **unverified** (no installed-state sample yet) — probe: `cmp shared/definitions/skill-reference-definitions.md .specify/shared/definitions/skill-reference-definitions.md` @ 2026-11-05 → identical, which proves the mirror exists but not that a source path resolves from an installed layout; affected tasks: T042 (the single closing task — the whole row takes the weakest of its three premises, so it stays `unverified` until then)

**A13 boundary** (owner: `shared/workflow/acceptance-hardening.md` § Gates — a pointer, not a second rule): this section records **task-generation probe verdicts** only, each with its probe command and an ISO date. A planning-time load-bearing premise belongs to `plan.md` § Execution Premises; a record inherited from a dependency feature belongs to `plan.md` § Inherited Blockers. The same fact written into two of the three carriers is a defect: the second occurrence MUST become a pointer (`see § Environment Prerequisites`), never a copy.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US5)
- **[blockedBy: T001,T002]**: explicit dependency tag — this task MUST NOT start until every listed task is `[X]`
- **Green-point attribution is deliberately absent from every row.** The tag `[green: <contract>#<clause>]` binds a row to a clause id, and clause ids are only machine-resolvable when the contract declares one of the six forms owned by `shared/definitions/contract-clause-definitions.md`. This feature's four contracts all carry their clauses as headings (`## OD-01 — …`, `## SW-01 — …`, `## GR-01 — …`, `## GM-01 — …`), which that owner classifies as `md-none`, so `validate-tasks.py` rejects every such claim as `green-dangling`. The claim was dropped rather than the contract re-formed: re-forming four committed contracts is a change to `contracts/`, which is outside this stage's commit boundary and outside its mandate (the canonical `**C-N**` marker form also cannot express an `OD-`/`SW-`/`GR-`/`GM-` id without renaming every clause everywhere it is cited — `data-model.md`, `plan.md`, `feature-ref.md` and the contracts' own traceability tables). The workaround of quoting the tag in a fenced block would satisfy the validator while leaving the claim invisible to the coverage accountant, i.e. it would remove the evidence of the conflict rather than the conflict. FR-to-carrier coverage is carried instead by explicit FR id mentions inside each row's description and by the DoD / GATE / measurement rows; see `## Notes` for the disclosure line this leaves open.
- Include exact file paths in descriptions

### Task State Sigil

`- [ ]` open; `- [>]` claimed (multi-agent runs only); `- [X]` closed and verified; `- [~]` deferred with a recorded reason in `verification.md` (`deferred_tasks=`). A run is complete when zero `[ ]` / `[>]` rows remain.

## Path Conventions

Single project at repository root. This feature is a **doc-feature** (`plan.md` § Project Structure): the deliverables are Markdown owner documents, skill bodies and structural contract tests. Framework sources (`shared/`, `skills/`, `tests/`) are edited; `.specify/` holds only generated mirrors and MUST NOT be hand-edited. Phase shape therefore follows the doc-feature taxonomy — author-section → wiring → structural test → mirror-parity → registration and measurement — instead of models/services/endpoints.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: freeze the pre-change readings this feature's claims are measured against, and confirm the two owner starting points. No story work can be measured before these readings exist.

- [x] T001 Capture the pre-change readings into `.specify/specs/082-mechanism-policy-separation/notes/pre-change-measurements.md`, each with its probe command and its real output: (a) `python3 scripts/python/sync-mirrors.py --check` and `python3 scripts/python/regen-command-copies.py --check` (the zero-drift baseline, EP-005); (b) `git ls-tree -r --name-only 3ffeb26e -- skills/ templates/commands/ | wc -l` → 575 (the SC-003 denominator); (c) `ls shared/definitions/mechanism-policy-definitions.md` → absent, and `ls shared/definitions/skill-reference-definitions.md` → present (the two owners' starting states differ: one is new, one is a to-be-finalised draft); (d) `grep -rc "skill-reference-definitions" skills/` → 8 reference strings, all `.specify/` mirror paths (the SR-05 rewrite population); (e) `ls tests/contract/ | grep -cE "mechanism_policy|skill_reference"` → 0; (f) the three `skill-shape.py` readings of EP-003. The plan-stage readings already recorded in `test-evidence/plan2026-11-05-baseline.txt` are cited where they exist, and re-taken here rather than inherited
- [x] T002 [blockedBy: T001] Confirm the frozen-hash registration surface in `tests/contract/test_expression_compatibility.py` and record the confirmation in `.specify/specs/082-mechanism-policy-separation/notes/pre-change-measurements.md` under a "frozen registration" heading: read `ALLOWED_POST_BASELINE_CHANGES` and record its exact key set, confirm `RENAMED_SKILL_REL` still names `skills/external/coaching-skills/SKILL.md` and that `_retired_skill_register` therefore requires that directory to keep existing, confirm `skills/internal/run-skills/SKILL.md` is already a key (the Feature 078 routing pointer that T040 must **update**, never duplicate), and confirm `WIRING_SKILLS` is exactly `create-docs` / `humanize`. The reading feeds T040's five registration points; this row writes nothing into the module

**Checkpoint**: the measurement baseline and the registration surface are on record; every later claim has a comparator.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: land the two owner documents. Every story phase below either writes into an owner document or asserts against one, so nothing story-level can start first.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T003 Author `shared/definitions/mechanism-policy-definitions.md` § Terminology and § Boundary Test (OD-02, OD-03) — the two canonical words written verbatim bilingual (`机制 (Mechanism)` / `策略 (Policy)`), the boundary test stated as one binary question (does this text change when the runtime environment is swapped?), the two observable directions, the explicitly non-deciding factors (file name, directory name, language, length, medium), the two derived member tables (mechanism side floors: judgement rules, algorithms, step order, reusable methods, the skill definition body, `references/`, `scripts/` logic, `assets/` templates; policy side floors: user-named directory, current working directory, `.specify/` runtime paths, input source, output location and shape, runtime-mode binding, with path values reached by pointer to `${SKILL_HOME}` / `${SKILL_WORKDIR}`), the "logic vs parameters-and-locations" ruling, and the paragraph-splitting rule for mixed content
- [x] T004 Author `shared/definitions/mechanism-policy-definitions.md` § Misplacement Symptoms and § Archival Rules (OD-04, OD-05) — two three-column symptom tables with at least two observable expressions each and corrections that name the other side's landing class (not just "should be fixed"); mechanism-in-runtime floors (a judgement rule living in a user-directory run note, an algorithm branch living in a `.specify/` note file); policy-in-mechanism floors (absolute path or user-directory name in skill prose, a `references/` line defaulting output to one concrete directory); the archival rule as one statement per side, the pointer-not-copy relation to `shared/guidelines/directory-governance.md`, and the `.specify/state/` edge-case ruling (the writing **action's rule** is mechanism, the **root** is policy and is owned there)
- [x] T005 Author `shared/definitions/mechanism-policy-definitions.md` § Consumption Contract and § Meta-layer Membership (OD-06, OD-07) — the fixed prompt shape (which policy item is missing, named in user-recognisable words; why it is needed now; how the user can supply it) with a copyable skeleton of a title line plus three fields plus one example marked write-side or read-side; the missing-policy vs environment-error split with distinguishable wording and follow-up actions; the before-any-side-effect declaration and the no-half-product rule; the two prohibitions (no mechanism default standing in for policy, no silent default location including the working directory); the standalone form; then the membership section with the C1 predicate quoted verbatim as the sole basis, the closed table `| 流程 | 产出 | 裁定 | 理由/接线位置 |`, `included` exactly `create-skills` / `improve-skills` / `merge-skills`, `excluded` exactly `coaching-skills` / `run-skills` each with a reason that hits the same predicate plus the "real rewriting still goes through improve-skills" channel, `/speckit.skills` on its own row marked command-surface, and the predicate-change consequence sentence
- [x] T006 Author `shared/definitions/mechanism-policy-definitions.md` § Boundaries, § Worked Examples, § Change Log and the head ownership declaration (OD-01, OD-08, OD-09, OD-10) — head lines 1–12 carrying the literal `single source of truth`, `MUST NOT`, the seven owned fact groups each with a landing section, and the four explicitly-not-owned facts with their owner paths; the neighbour table with at least the six named owners; a closed worked-example set of **at least 12 items**, each with a 1–3 line snippet, a standard answer from {mechanism, policy, to-be-clarified}, and a one-line basis citing only the boundary-test criterion, covering both content classes, both misplacement classes and the boundary cases (script parameter, template heading, `.specify/` note, bilingual sentence) and marked as SC-001 / SC-005's sole denominator; the change-log table with its first row naming this feature's landing date and FR group
- [x] T007 [blockedBy: T001] Finalise `shared/definitions/skill-reference-definitions.md` against GR-01…GR-06 and GR-08–GR-10 **without rewriting what already satisfies them** — the draft is in the working tree, so this row verifies and closes gaps rather than re-authoring: head lines 1–12 naming the four owned fact groups (accepted forms, normalisation order and output shape, disambiguation, failure semantics) and the two not owned (position ladder → `skills/internal/run-skills/SKILL.md` § 1; mirror generation → `scripts/python/sync-mirrors.py`); the accepted-forms table with all six forms; the **normalisation order rewritten to form determination → trim and one paired wrapper quote → one `skill:` label → one `@` or `/` prefix (accepting `@/name`) → `SKILL.md` / trailing `/` → channel test → three-valued output**, i.e. NP-3/NP-4 before NP-6; the output shape carrying name-or-path-and-layer with no stripped prefix or suffix, the paired report of raw plus normalised plus decision class, the two-pass case rule with multi-hit closing as a failure, and the explicit form-determination step; the channel test as one criterion (does the residual contain `/`), `.md` explicitly not stripped with "omitting the extension is a settlement convention, not a normalisation step"; disambiguation rules (a)–(d) each with an example input and the layer-not-path-literal criterion for (c); the four-row failure table with per-class required report items, fail-closed semantics, mutual exclusivity, and the CLI-form `@name` ruling; the boundary section (no position ladder inlined, no other owner's rule literals) and the zero-new-machinery section. Record the verification outcome in the same commit. Cross-capability, so it carries no story label
- [x] T008 [blockedBy: T007] Record the FR-027 starting-point verification as evidence in `.specify/specs/082-mechanism-policy-separation/test-evidence/fr-027-starting-point-verification.txt` — a per-document comparison table (owner document, and each of the five consumer `SKILL.md` input/parsing sections) listing for each whether it satisfies FR-019…FR-026 and what exactly is missing, plus the closed gap list with one row per gap and the task that closes it. The three gaps measured at plan time are carried in as starting rows and must each be re-checked against the tree rather than copied: the normalisation order producing only NAME/PATH with no FAILURE, the eight mirror-path reference strings, and the zero `tests/` coverage. A row that re-checks a plan-time gap and finds it already closed records that finding with its probe output

**Checkpoint**: both owners exist with their required sections; every consumer-side row below can now reference a real path, and every structural assertion has a real subject.

---

## Phase 3: User Story 1 - 作者在新建技能时被强制区分两层，误置当场被拦下 (Priority: P1) 🎯 MVP

**Goal**: `create-skills` delivers a mechanism/policy judgement at its existing closing validation, locating a misplacement by file and line and refusing to report completion, while a correctly layered skill passes silently.

**Independent Test**: in a sandbox, drive `create-skills` to create a skill whose body hard-codes an environment path; observe the judgement naming that line and the correction direction before completion, then re-run on a correctly layered skill and observe the pass branch with no additions demanded. Neither run touches any existing skill.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL for artifact-missing reasons, never as import or collection errors (GM-01 / GM-11 red-first shape).**

- [ ] T009 [P] [US1] Author `tests/contract/test_mechanism_policy_skill_wiring.py` (SW-01…SW-03 half) — assert the `create-skills` § 6 `Minimum checks` list carries exactly one item containing the literal `Mechanism / policy separation` after its previous last item, that the item contains a judgement sentence covering **both** sides, an anchor to `./references/mechanism-policy-check.md` and an owner-path reference, that the item inlines no table row from the owner (the maximum permitted inline is one keyword phrase per misplacement class), that `skills/external/create-skills/references/mechanism-policy-check.md` exists and stays within its step budget, and that the same module will later carry the `improve-skills` / `merge-skills` legs. Include a negative case that deletes the judgement item in a `tmp_path` copy and asserts the module's own assertion function turns red
- [ ] T010 [P] [US1] Author `tests/contract/test_mechanism_policy_owner_doc.py` legs for OD-02…OD-06 and OD-09 — the assertions: the two canonical words appear verbatim bilingual, the boundary test is phrased as a binary question with no middle tier, each symptom table has at least two rows with a correction pointing at a landing class, the prompt shape carries all three required fields plus a skeleton and one marked example, the missing-policy and environment-error branches are textually distinguishable, the before-any-side-effect declaration exists, the worked-example set parses into at least 12 items each with a snippet, an answer from the closed three values and a basis citing only the boundary test, and the set is marked as the sole SC-001 / SC-005 denominator. Include a negative case that removes one worked-example answer in a `tmp_path` copy and asserts the parse assertion turns red

### Implementation for User Story 1

- [ ] T011 [US1] [blockedBy: T005,T009,T010] Rewrite `skills/external/create-skills/SKILL.md` for **both** landings in one pass — (i) append one checklist item after the existing last item of § 6 `Minimum checks` containing the literal `Mechanism / policy separation`, one executable judgement sentence covering both misplacement sides, a short anchor to `./references/mechanism-policy-check.md` and the owner source-path reference; (ii) at § 2's writability pre-flight and immediately before the writes in § 7 and § 8, add the read-judge-stop reference to the owner's § Consumption Contract rather than any prompt wording of its own. No judgement table, no full symptom table, no second rule set, no new step number, no new gate
- [ ] T012 [US1] [blockedBy: T009] Author `skills/external/create-skills/references/mechanism-policy-check.md` — at most 12 lines of judgement steps plus, for each of the two misplacement classes, the localisation method (how to find candidate lines, how to read the quotation), the two correction categories and the owner path. It MUST NOT restate the owner's symptom table, MUST NOT add a new rule, and MUST NOT be a second judgement owner

**Checkpoint**: US1 is independently observable — a sandbox creation run is judged, located and stopped or passed.

---

## Phase 4: User Story 2 - 改进技能时，被引用的运行环境文件先与技能正文对账再判改进方向 (Priority: P1)

**Goal**: `improve-skills` reconciles a skill's referenced environment files with its body at the survey step and offers "policy source missing or ambiguous" as an improvement candidate, never inheriting a hard-coded value as a default; batch mode runs the judgement once.

**Independent Test**: take a test skill referencing an external input file but hard-coding its default path, run `improve-skills`, and observe the candidate list carrying "policy source missing" with the direction "have the user supply it at run time"; run a correctly layered skill through the same flow and observe no new candidate relative to the pre-change baseline.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T013 [P] [US2] Extend `tests/contract/test_mechanism_policy_skill_wiring.py` with the `improve-skills` legs — assert § 2 carries one added survey question that reads the referenced environment files together with the body and answers "where does the policy take its value"; that § 3's candidate categories contain `policy source missing or ambiguous` with the freeze discipline unchanged; that the candidate carries the prohibition on inheriting a hard-coded value plus the direction "let the policy come from the user or the environment at run time"; and that the batch-mode statement lives in `./references/loop-playbook.md` with only a pointer in the body. Include a negative case that moves the candidate category's literal in a `tmp_path` copy and asserts the assertion function turns red

### Implementation for User Story 2

- [ ] T014 [US2] [blockedBy: T013] Rewrite `skills/external/improve-skills/SKILL.md` for **both** landings in one pass — (i) append the survey question at the end of § 2 and the `policy source missing or ambiguous` candidate category at § 3 with its prohibition and direction; (ii) declare the `Target identifier` parameter as a parameter only and add the owner source-path reference, with no second rule set. One judgement line plus one owner path; no new step, no new gate
- [ ] T015 [P] [US2] Edit `skills/external/improve-skills/references/loop-playbook.md` — in the batch section, add one statement that the mechanism/policy judgement runs once for the whole batch and is not repeated per skill, with the body keeping only a pointer. No second judgement, no new section

**Checkpoint**: US2 is independently observable — a hard-coded default produces a candidate, a layered skill produces none, and a batch run judges once.

---

## Phase 5: User Story 3 - 消费侧：策略缺失时以统一形态提示，而不是猜 (Priority: P2)

**Goal**: every consuming flow stops before any side effect when policy is missing or ambiguous, asking through the owner's single prompt shape and never substituting a mechanism default or a silent default location; with both layers present, behaviour is byte-identical to before.

**Independent Test**: run a test skill that takes no output directory and carries no default, observe one prompt naming the missing item and no file written anywhere; supply the parameter and observe normal output; then verify a fully specified input produces no prompt at all.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T016 [P] [US3] Author `tests/contract/test_mechanism_policy_missing_policy.py` — in `tmp_path`, build a fake skill directory and a fake run directory, then assert: the owner's check is textually a read-judge-stop three-step with no write action in it; with the policy path missing, the `tmp_path` snapshot is identical before and after across the full file set with content hashes and directory set (not mtime); with the policy path supplied, the produced artifact hashes equal the recorded baseline hashes for the same input. Include a negative case that injects a write into the check text in a `tmp_path` copy and asserts the zero-write assertion turns red
- [ ] T017 [P] [US3] Extend `tests/contract/test_mechanism_policy_skill_wiring.py` with the side-effect-before-check legs — assert each named wiring point precedes its side effect in `create-skills` (the § 2 pre-flight and the § 7 / § 8 writes), `improve-skills` (§ 7 edit) and `merge-skills` (§ 7 decommission), that each names the owner's Consumption Contract by path, that none restates prompt wording of its own, and that the missing-policy and environment-error wordings are distinguishable at every point. Include a negative case that reorders one wiring point after its side effect in a `tmp_path` copy and asserts the ordering assertion turns red

### Implementation for User Story 3

- [ ] T018 [US3] [blockedBy: T016,T017] Close the consumption-side wiring across the three included meta-skills — re-read the four wiring points already added by T011 / T014 / T020 against OD-06 and correct any drift in place: the prompt reference is a path reference to the owner's Consumption Contract, the read-judge-stop order holds, the stop leaves no half product, and the two error classes keep distinct wording. This row closes gaps only; it introduces no new wording owner and no second prompt template

**Checkpoint**: US3 is independently observable — missing policy stops with one prompt and zero writes; supplied policy behaves as before.

---

## Phase 6: User Story 4 - 同族元技能与元命令的成员裁定是封闭的、可复算的 (Priority: P2)

**Goal**: the membership ruling and its predicate are closed, recomputable by a third party, and paired with an exclusion reason per excluded member; the command surface is declared as a wiring position and left unchanged.

**Independent Test**: hand the membership table to a second person and have them apply only its predicate to any skill under `skills/external/`; their verdict matches the table, including each exclusion reason.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T019 [P] [US4] Author `tests/contract/test_mechanism_policy_ownership.py` — assert the membership table parses to exactly three `included`, two `excluded` and one command-surface row with the C1 predicate quoted verbatim; that each exclusion reason hits the same predicate and names the improve-skills channel; that the `included` set equals the skill directories implied by the allowed-difference set registered in `data-model.md` § GM-03 rows 1–8; and that the six named neighbour owners' rule literals do not appear in the owner document (including `dogfooding-definitions.md` § 1's own definition, which MUST remain unrewritten). Include a negative case that adds a fourth `included` row in a `tmp_path` copy and asserts the closed-set assertion turns red
- [ ] T020 [US4] [blockedBy: T019] Author `tests/contract/test_mechanism_policy_guard.py` — the SC-003 closed-set guard, carrying all five declaration requirements and reporting its compared-file count in the `compared=575` shape so that a guard which compared nothing cannot pass silently: read the baseline tree from the literal `3ffeb26e` (never from a "current" variable), compare both families of the comparison unit path by path with `git cat-file blob 3ffeb26e:<path>` against the working tree, assert the changed-path set from `git diff --name-status 3ffeb26e..HEAD -- skills/ templates/commands/` falls only inside the registered allowed set, and scan this feature's own contracts and `data-model.md` for undefined aggregate words used as comparison scope. Include the reverse case: copy a complement file into `tmp_path`, change one byte, and assert the guard turns red. The full green reading belongs to T041; this row lands the guard and its negative case
- [ ] T021 [US4] [blockedBy: T019] Author `tests/contract/test_mechanism_policy_decidability.py` — assert the worked-example set is machine-parsable into per-item records with snippet, answer and basis, that every answer is one of the three closed values, that every basis cites only the boundary-test criterion and introduces no new rule, and that the set is the only place this feature enumerates examples (scanning `contracts/` and `data-model.md` for a second copy). Include a negative case that appends a basis citing an undefined rule in a `tmp_path` copy and asserts the assertion function turns red

### Implementation for User Story 4

- [ ] T022 [US4] [blockedBy: T005,T019] Prove the command surface is untouched and record it — run `python3 scripts/python/regen-command-copies.py --check`, confirm zero changed copies across the four per-tool trees, confirm `templates/commands/skills.md` is byte-identical to the baseline blob, and record both readings with their commands in `.specify/specs/082-mechanism-policy-separation/notes/pre-change-measurements.md` under a "command surface" heading. If the template must change, stop and report rather than editing it

**Checkpoint**: US4 is independently observable — a third party reproduces the membership verdict and the command surface proves itself unchanged.

---

## Phase 7: User Story 5 - 元技能用一个确定的语法识别「这次操作的是哪个技能」 (Priority: P1)

**Goal**: one owner document owns how a meta-skill names its target; the five consumers declare only their own parameters and reference it by framework-source path; normalisation yields exactly one of command-surface / skill / failure, reported paired with the raw input.

**Independent Test**: feed the same reference inputs (six accepted forms, case variants, a `/speckit.*` command name, a zero hit, an out-of-ladder path) to each consumer's parsing section and check every one reports the raw identifier, the normalised identifier and the hit path with the same normalised result; then diff each consumer's body against the owner to confirm none restates the order or the failure table.

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T023 [P] [US5] Author `tests/fixtures/skill-reference/normalization-matrix.json` — the single matrix, organised in three disjoint segments `surface` / `normalize` / `failure`, starting from the fourteen-line clarify probe and extended to cover every form SC-006 names, with at least 12 rows overall; each row carrying `raw`, the form it exercises, `expect.outcome` from the closed three, `expect.normalized`, and for failure rows `expect.failure_class` from the closed four plus the required report items. Rows for `dual-layer` MUST use two genuinely different layers, never a source-and-mirror pair
- [ ] T024 [P] [US5] Author `tests/contract/skill_reference_matrix.py` — the single executable implementation of the normalisation, stdlib only (`json`, `pathlib`, `re`), a pure function from (raw string, form) to the three-valued outcome with the normalised identifier and the paired-report fields, importing nothing from the repository and carrying assertions and I/O nowhere at module level. It is a test helper, not a pytest module, not a gate, and it MUST NOT be placed under `scripts/`. Steps in NP-1…NP-8 order with NP-3/NP-4 strictly before NP-6
- [ ] T025 [US5] [blockedBy: T024] Author `tests/contract/test_skill_reference_grammar.py` — assert the owner's head declares the four owned fact groups and both not-owned facts with owner paths and each declaration has a landing section; the accepted-forms table has all six rows literal-equal to `data-model.md` E-8 and is declared closed; the normalisation step set maps one-to-one onto NP-1…NP-8 with NP-3/NP-4 ordered before NP-6; the output shape is the closed three values with no fourth; the paired report carries raw plus normalised plus decision class; the two-pass case rule closes a multi-hit as a failure. Include a negative case that swaps two normalisation steps in a `tmp_path` copy and asserts the ordering assertion turns red
- [ ] T026 [P] [US5] Author `tests/contract/test_skill_reference_matrix.py` — recompute every matrix row through `skill_reference_matrix.py` and compare both the decision class and the paired raw-plus-normalised shape; the denominator is the fixture's own row count and MUST be at least 12; print a `rows=N matched=N failed=0` reading; any single mismatch fails with the row named, never "the rest passed". Include a negative case that changes one row's expected value in a `tmp_path` copy and asserts the comparison turns red
- [ ] T027 [P] [US5] Author `tests/contract/test_skill_reference_consumers.py` — the five-consumer wiring plus the containment scan: each of the five `SKILL.md` files carries exactly one reference to the framework-source owner path and only declares its own parameters; reference strings prefixed `.specify/shared/definitions/` are zero across all of them; then scan every `SKILL.md` under `skills/` (source tree; mirrors excluded from the denominator and proved separately) counting hits of normalisation-step or failure-table literals, with the three permitted classes named as constants and counted separately, and report every hit with path and line number plus the scanned file count. Include a negative case that rewrites one consumer's source-path reference back to the mirror path in a `tmp_path` copy and asserts the assertion function turns red
- [ ] T028 [P] [US5] Author `tests/contract/test_skill_reference_command_surface.py` — at least two positive rows (`speckit.skills` bare and `/speckit.skills`) normalising to `command-surface` and pointing at `templates/commands/skills.md`, plus at least one negative row (a command-shaped name that is not a command, or the mirror form of a dot-name) proving the ruling is not "anything with a dot or a slash is a command". Include a negative case that flips one expected class in a `tmp_path` copy and asserts the assertion function turns red
- [ ] T029 [P] [US5] Author `tests/contract/test_skill_reference_failures.py` — one assertion per failure class (zero-hit, out-of-ladder, unreadable, dual-layer), each also asserting the report carries both the raw and the normalised identifier, plus a mutual-exclusion assertion that an out-of-ladder input is never reported as zero-hit and an unreadable directory is never reported as out-of-ladder. The `dual-layer` case is built from two different layers in `tmp_path`, never from a source-and-mirror pair. Include a negative case that relabels one failure class in a `tmp_path` copy and asserts the exclusion assertion turns red

### Implementation for User Story 5

- [ ] T030 [US5] [blockedBy: T007,T027] Rewrite `skills/external/merge-skills/SKILL.md` for **both** landings in one pass — (i) after § 5's no-loss gate add the pre-judgement on whether the merge changes the two layers' distribution, plus one verification item in § 8 that reuses `create-skills` § 6's judgement rather than copying it, plus the before-decommission check of § 7 pointing at the owner's Consumption Contract; (ii) declare the `Source` / `Target` parameters in the Input Contract with a **single** owner source-path reference covering both. No copied acceptance-form list, no copied failure table, no new record table
- [ ] T031 [US5] [blockedBy: T027] Rewrite `skills/internal/run-skills/SKILL.md` with the skill-reference landing only — declare the `Target` parameter in the Input Contract and add a step 0 to § 1 stating normalise-by-owner then disclose the raw identifier and the decision class. Zero mechanism/policy literals. § 1's position ladder (steps 1–4) and its trust-boundary paragraph MUST stay byte-identical to the baseline, and step 0 MUST NOT describe the normalisation order itself
- [ ] T032 [P] [US5] [blockedBy: T027] Rewrite `skills/external/coaching-skills/SKILL.md` with the skill-reference landing only — declare its own parameter in § Inputs, add one parsing line in § 2 and a § Nested section, each by source-path reference to the owner. Zero mechanism/policy literals; the § Improvement Plan channel sentence that says real rewriting still goes through `improve-skills` MUST NOT be rewritten
- [ ] T033 [P] [US5] [blockedBy: T030,T031] Edit `skills/external/merge-skills/references/provenance-record.md` — allow the capability row's "how to verify" column to state the row's layer attribution, without adding a column and without adding a second record table
- [ ] T034 [US5] [blockedBy: T007] Record the per-consumer reference-string audit that T035 converts: for each of the five consumer `SKILL.md` files, list every reference string to the owner with its current path form and the landing section it sits in, into `.specify/specs/082-mechanism-policy-separation/notes/pre-change-measurements.md` under a "reference coordinates" heading, so the rewrite's population is recorded before it is edited rather than asserted after
- [ ] T035 [US5] [blockedBy: T034] Convert all eight reference strings across the five consumer `SKILL.md` files from the mirror path to the framework-source path, then prove the population closed — the readable form is file plus string content, never a line number, since line numbers drift with editing; the population is measured at T001(d) and re-measured here, and the count after the rewrite MUST be zero mirror-path strings and exactly one source-path reference per consumer

**Checkpoint**: US5 is independently observable — the same input produces the same three-valued answer at all five consumers, and none of them restates the grammar.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: the registration lines, the frozen-hash registration, the two regeneration entries, the sample-borne measurements, the gate reading and the feature-level closure — work that spans both capabilities and belongs to no single story.

- [ ] T036 [P] Verify the mirror obligations for the twelve mirrored files and that FR-016 still holds after the binary ships — run `python3 scripts/python/sync-mirrors.py` then `python3 scripts/python/sync-mirrors.py --check`, confirm every pair reports `ok` with zero new drift against T001(a)'s reading, and confirm the `shared/` pair reflects both owner documents. Both `--check` runs exiting 0 is also this feature's RS-004 joint-acceptance reading (FR-016), since the two generators are in-scope runtime of this repository; alongside them, confirm FR-016's no-second-form boundary is still observable in the tree — exactly one classification file (`shared/definitions/mechanism-policy-definitions.md`, no parallel copy), exactly one machine gate (guarded by `tests/contract/test_expression_compatibility.py`, no second gate introduced), and no new directory root outside the mirrored six pairs. No file-count assertion may be pinned; the reading is recorded as measured
- [ ] T037 [P] Verify the command surface stayed closed after the full rewrite set — re-run `python3 scripts/python/regen-command-copies.py --check`, confirm zero changed copies and that all 27 command templates are byte-identical to the baseline, and record the reading next to T022's so the two are comparable
- [ ] T038 [blockedBy: T011,T014,T030,T031,T032,T035] Add the five frozen-hash registration points to `tests/contract/test_expression_compatibility.py` — four new keys for `skills/external/{create-skills,improve-skills,merge-skills,coaching-skills}/SKILL.md`, each with a reason naming its FR group and markers drawn from that skill's own newly added literals, plus an **update** to the existing `skills/internal/run-skills/SKILL.md` key extending its reason to cover the skill-reference wiring and folding in the new wiring line's unique literal. The hash list, `WIRING_SKILLS` and every assertion stay intact; no key is duplicated, deleted or skipped, and no `references/` file is registered since the frozen list does not cover them
- [ ] T039 [P] [blockedBy: T001] Add the three registration lines — `.specify/memory/glossary.md` gains one entry `机制/策略分离 (Mechanism–Policy Separation)` with origin `user` and status `proposed`; `.specify/shared/definitions/framework-map.md` gains both owner file names inside its existing shared-definitions row, with no new row and no new directory; `CHANGELOG.md` gains one entry naming the two owners, the meta-skill judgement and reference lines, the eleven contract modules and the matrix fixture. `framework-map.md` has no framework-source counterpart, so it is a registration in place, not a mirror drift
- [ ] T040 [P] [blockedBy: T011,T014,T030,T031,T032] Record the before and after `skill-shape.py` controllable-token readings for every edited `SKILL.md` and a `redline-check.py` reading for each, into `.specify/specs/082-mechanism-policy-separation/test-evidence/skill-shape-before-after.txt` with the command and both numbers per file plus the delta; the before readings come from T001(f) and MUST NOT be re-measured as if they were the before. Where a file was already over budget before this feature (see § Environment Prerequisites), the record states that the delta is the measurement and that exit 0 was never the criterion
- [ ] T041 [P] [blockedBy: T020,T024,T035,T038] Record the SC-003 reading in `.specify/specs/082-mechanism-policy-separation/test-evidence/sc-003-<date>.txt` — one real run of `test_mechanism_policy_guard.py` pasted verbatim, carrying the compared-file count, the complement size, the allowed-in-unit count and a zero frozen-mismatch reading, plus the `git diff --name-status 3ffeb26e..HEAD -- skills/ templates/commands/` output proving every changed path is registered. The enclosed count argument must be recomputable from the pasted output alone
- [ ] T042 [P] [blockedBy: T028] Record the SC-008 reading in `.specify/specs/082-mechanism-policy-separation/test-evidence/sc-008-<date>.txt` — the positive rows reporting `command-surface` and their command target, and the negative row reporting a non-command for a command-shaped input, pasted verbatim from one run
- [ ] T043 [P] [blockedBy: T026] Record the SC-006 reading in `.specify/specs/082-mechanism-policy-separation/test-evidence/sc-006-<date>.txt` — the per-row recomputation output plus the `rows=N matched=N failed=0` line, with N equal to the matrix's own row count and at least 12
- [ ] T044 [P] [blockedBy: T027] Record the SC-007 reading in `.specify/specs/082-mechanism-policy-separation/test-evidence/sc-007-<date>.txt` — the five consumers' single-reference readings, the per-class permitted-hit counts, every hit with path and line number, and the scanned file count
- [ ] T045 [P] [blockedBy: T029] Record the SC-009 reading in `.specify/specs/082-mechanism-policy-separation/test-evidence/sc-009-<date>.txt` — the four failure assertions' output with each class's paired report visible, plus the mutual-exclusion assertion's output
- [ ] T046 [blockedBy: T006] Record the SC-001 double-judge reading in `.specify/specs/082-mechanism-policy-separation/test-evidence/sc-001-<date>.txt` — two fresh-context read-only judges answering the closed worked-example set using the owner document alone, with the set snapshot, both verdict sets and the agreement rate. A disagreement is a decidability finding about the owner document, not a judge error, and is recorded as such
- [ ] T047 [P] [blockedBy: T006] Record the SC-005 reader reading in `.specify/specs/082-mechanism-policy-separation/test-evidence/sc-005-<date>.txt` — one reader who did not take part in this feature answering the **same** closed set from the owner document alone, with the correct count against the full set size. This shares SC-001's denominator and MUST NOT create a second question set
- [ ] T048 [blockedBy: T011,T014,T030] Record the SC-002 host reading in `.specify/specs/082-mechanism-policy-separation/test-evidence/sc-002-<date>.txt` — one supported host, the two misplacement samples and the two correctly layered samples driven before and after the change, with the host name and version string verbatim, the input draft paths, the output text, and a per-sample verdict table. Detection is 100% and false positives are 0; if the version string cannot be collected the reading says so rather than omitting the column
- [ ] T049 [P] [blockedBy: T016] Record the SC-004 supporting reading in `.specify/specs/082-mechanism-policy-separation/test-evidence/sc-004-<date>.txt` — one host transcript of a missing-policy run producing the prompt with zero files written and a supplied-policy run producing byte-identical output, with host name and version
- [ ] T050 [blockedBy: T036,T037,T038,T041] Record the SC-003 complement reading for the mechanism/policy side and close the measurement set — one real run of `test_mechanism_policy_guard.py` alongside `test_mechanism_policy_ownership.py` showing the allowed-difference set matches the `included` member set with an empty difference, appended to T041's file so both readings sit in one place
- [ ] T051 [blockedBy: T036,T037,T038,T039,T040,T041,T042,T043,T044,T045,T046,T047,T048,T049,T050] Run the closure gates and record them verbatim in `.specify/specs/082-mechanism-policy-separation/test-evidence/final-gates.txt` — GATE-1 through GATE-7 each run in its turn with its exit code, plus `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/082-mechanism-policy-separation --stage tasks --repo .` and `python3 scripts/python/validate-tasks.py .specify/specs/082-mechanism-policy-separation/tasks.md`. The targeted-set failure-name difference is computed as a set difference against the recorded baseline, never as an absolute all-green claim; a pre-existing failure is attributed, not absorbed and not hidden
- [ ] T052 [blockedBy: T051] Record the closing run determination and the feature-level statement in `.specify/specs/082-mechanism-policy-separation/verification.md` — every SC-001…SC-009 row with its status derived from that criterion's own reading, the four run quantities with an unevaluated one stated as not evaluated, every `final`-path criterion reading `pass`, the smoke command / exit code / evidence path, and any deferred row listed in `deferred_tasks=`. A criterion whose reading is missing is written as not evaluated, never as fine

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies; T001 first, T002 after it
- **Foundational (Phase 2)**: depends on Setup; **blocks every story phase**. T003–T006 build the mechanism/policy owner section by section; T007 finalises the skill-reference owner; T008 records the FR-027 verification after T007
- **User Stories (Phases 3–7)**: all depend on Phase 2. Once it closes they may run in parallel if staffed, or in priority order
- **Polish (Phase 8)**: registration and mirror rows (T036–T040) need the story rows they register; the measurement rows (T041–T049) each need the module or owner they read; T050 needs T036–T041; T051 needs all of them; T052 closes

### User Story Dependencies

- **US1 (P1)**: after Phase 2 — needs the owner's § Misplacement Symptoms and § Consumption Contract only. No dependency on another story
- **US2 (P1)**: after Phase 2 — independent of US1; both edit different files (`improve-skills` vs `create-skills`)
- **US3 (P2)**: after Phase 2 — its one implementation row closes wiring points that US1 / US2 / US5 create, so it follows them within the ticket even though its test rows are independent
- **US4 (P2)**: after Phase 2 — the membership ruling lives entirely in the owner document plus its own guard modules
- **US5 (P1)**: after Phase 2 — the largest story; independent of US1–US4 except where the same three `SKILL.md` files carry both landings, which each row handles in one pass

### Within Each User Story

- Tests before implementation, red for artifact-missing reasons, never as import or collection errors
- The owner document section before the consumer that references it
- The consumer body edit and its own reference file in the same pass
- The negative-case assertion in the same module as the assertion it guards

```text
Phase 1  T001 ─ T002
Phase 2  T003 ─ T004 ─ T005 ─ T006        (mechanism/policy owner, section by section)
         T007 ─ T008                       (skill-reference owner, finalise then verify)
Phase 3  T009,T010 ─ T011 ─ T012           (US1)
Phase 4  T013 ─ T014 ─ T015                (US2)
Phase 5  T016,T017 ─ T018                  (US3)
Phase 6  T019,T020,T021 ─ T022             (US4)
Phase 7  T023,T024,T025,T026,T027,T028,T029 ─ T034 ─ T030,T031,T032 ─ T033 ─ T035  (US5)
Phase 8  T036,T037,T038,T039,T040 ─ T041..T050 ─ T051 ─ T052
```

### Parallel Opportunities

- Phase 1: T001 then T002 (one file)
- Phase 2: T003 → T004 → T005 → T006 run in order because they write one owner document; T007 is a different file and can run alongside the mechanism/policy chain
- US1 tests (T009, T010) in parallel; in US2, T013 then T014 / T015; in US5, T023–T029 are seven different files and run together
- The five consumer bodies (T030, T031, T032, and the `create-skills` / `improve-skills` halves already landed as T011 / T014) touch five different files, so they parallelise by file; T035 must follow all of them since it converts the reference strings across the same five files
- Phase 8 measurement rows T042–T045 and T047 / T049 are independent evidence files and run together once their producers are green

---

## Parallel Example: User Story 5

```bash
# Seven different files, no mutual dependency:
Task: "Author the normalization matrix in tests/fixtures/skill-reference/normalization-matrix.json"
Task: "Author the test-only normalization implementation in tests/contract/skill_reference_matrix.py"
Task: "Author the owner-shape assertions in tests/contract/test_skill_reference_grammar.py"
Task: "Author the matrix recomputation in tests/contract/test_skill_reference_matrix.py"
Task: "Author the five-consumer wiring and containment scan in tests/contract/test_skill_reference_consumers.py"
Task: "Author the command-surface pair in tests/contract/test_skill_reference_command_surface.py"
Task: "Author the four failure classes in tests/contract/test_skill_reference_failures.py"
```

---

## Implementation Strategy

### MVP First

**MVP scope rule applied**: this feature has **three P1 stories** (US1, US2, US5) and they together form the independently valuable increment — a mechanism/policy judgement that reaches only new assets, without the improvement channel or the reference grammar, leaves both existing skills and the target-selection step uncovered, and the three share the same meta-skill surface. The MVP is therefore **US1 + US2 + US5**; US3 and US4 are P2 and land after.

1. Complete Phase 1 (Setup) and Phase 2 (Foundational) — both owners exist
2. Complete US1 + US2 + US5 — the three P1 stories
3. **STOP and VALIDATE**: run each P1 story's independent test; a new skill is judged and located, an existing skill's hard-coded default becomes a candidate, and one reference input yields one three-valued answer at all five consumers
4. Then US3 (consumption-side stop) and US4 (membership + command surface)
5. Close Phase 8: registration, mirrors, measurements, gates

### Incremental Delivery

1. Setup + Foundational → both owners on disk, both regeneration baselines frozen
2. US1 → creation-time judgement works → demo
3. US2 → the improvement channel reaches existing skills → demo
4. US5 → target naming is one grammar → demo (the three P1s are now complete)
5. US3 → missing policy stops before any write
6. US4 → the membership ruling is recomputable; the command surface proves itself unchanged
7. Phase 8 → registration lines, both `--check` readings, the nine criterion readings, the closure gates

### Parallel Team Strategy

With two workers: one takes the mechanism/policy chain (Phase 2's T003–T006, then US1 / US2 / US3 / US4), the other takes the skill-reference chain (T007–T008, then US5's T023–T034). The two chains meet at four points only — T011 / T014 / T030 carry both landings and each is a single row, T034 converts the reference strings in files the first worker has already edited, and T038 registers the frozen hashes for all five. Those four are sequencing constraints, not shared write targets, so no file is edited by two workers at the same time.

---

## Notes

- `[P]` marks different files with no dependencies on incomplete tasks; the validator's parallel-safety verdict has been adjudicated by actual write targets, not by prose
- Every new contract module is a **structural** contract test on artifact content (Constitution VII's template-only gate): it asserts headings, literals, byte equality and parsability, never "does this paragraph mean mechanism or policy" — that semantic judgement belongs to the sample-borne criteria (GM-02)
- Red-first shape is part of the contract: a module goes red because its subject artifact is missing, never because an import or collection fails
- The skill-reference side's matrix module goes green at authoring: the matrix rows are authored by T023 and the recomputation by T026 in the same story, and a stale-expectation matrix would be circular evidence. This departure from strict red-first is stated here rather than left implicit
- Deferral discipline: a row handed to a later run is marked `[~]` with its reason in `verification.md`; leaving it `[ ]` blocks completion and hides the handoff
- Commit after each logical group; never commit `.specify/` mirrors as source, and never push in this run
