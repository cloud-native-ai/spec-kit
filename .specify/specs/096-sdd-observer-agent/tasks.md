# Tasks: SDD 专用观察者与线级观察记录（sdd-observer）

**Requirement ID**: 096
**Requirement Key**: 096-sdd-observer-agent
**Related Feature**: 096 SDD Observer Agent（sdd-observer 专用观察者与线级 journal）
**Input**: Design documents from `.specify/specs/096-sdd-observer-agent/`
**Prerequisites**: requirements.md (23 FR / 7 SC; 6 clarify rulings; 13 assumptions A1–A13), plan.md (22 principle checks, 5 decision tensions T-001…T-005, 8 execution premises EP-001…EP-008, Mirror Obligations table, 4 work packages), research.md (R-01…R-14), data-model.md (E-1…E-10, V-1…V-20), contracts/ (5 pages / **58 clauses**: journal-engine 13, journal-format 13, observer-lifecycle 12, observer-role 10, observer-verification 10), quickstart.md (S-0…S-7), feature-ref.md (19 delivery rows, FR→contract and SC→measurement maps)

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating (pure functions MUST have unit tests, critical flows MUST have automated regression coverage, cross-service/external contracts MUST have integration/contract tests); Principle VII is NON-NEGOTIABLE and its template-only gate applies on top, because the agent template and driver prose are structure-asserted rather than runtime-tested (plan A10 / Constitution Check row IV). This is an `execution`-class line (`flow-class-check.py --action lookup --unit-id spec:096-sdd-observer-agent` → `flow_class: execution`, read once this stage), so the runtime layers apply in addition to the template-only gate.

**Tests**: MANDATORY. Red-first captures append to the writing package's own file — `notes/red-first-evidence-wp01.md`, `notes/red-first-evidence-wp02.md` or `notes/red-first-evidence-wp03.md` (one file per package, never one shared file; command, real output, exit status per entry); execution readings land in `.specify/specs/096-sdd-observer-agent/test-evidence/`. Guard rows come BEFORE the row that turns them green, except where a row's subject is an appended assertion over an already-authored module (a later row extends the same module without re-claiming a green point).

**Organization**: grouped by the five user stories of `requirements.md` (US1–US3 Priority P1; US4–US5 Priority P2), with a Setup phase, a Foundational phase (the journal-format owner fact and the line fixture builder — every story reads them), and a Polish phase. All paths are repo-relative.

## Definition of Done (DoD)

- DoD-1: **FR lane** — every FR-001…FR-023 is quoted at line level by at least one task row. Check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --stage tasks --spec-dir .specify/specs/096-sdd-observer-agent --repo .` reports `decision: pass` with zero runtime-row findings naming an unquoted FR.
- DoD-2: **SC lane** — every SC-001…SC-007 has at least one task row and a recorded evidence pointer under `test-evidence/` or `notes/` (§ SC → row trace).
- DoD-3: **clause lane** — every `[green:]` claim resolves to a real contract and clause (`validate-tasks.py` zero `green-dangling`, zero `green-clause-collision`); all 58 clauses are claimed exactly once, and § Green Attribution records the claim map plus every mechanical warning it discloses.
- DoD-4: **tests** — the new guard modules pass through the one runner (`bash scripts/bash/run-tests.sh`); the full-suite reading has zero NEW failed ids against the implement-entry baseline (owner of the baseline capture: `/speckit.implement` Step 0).
- DoD-5: **mirrors and renders** — `python3 scripts/python/sync-mirrors.py --check` shows no NEW drift against the pre-edit baseline; the four per-tool agent copies exist and carry the fast-fail clause; `test_fast_fail_discipline.py -k "i10 or i11"` is green after the deliberate preset update.
- DoD-6: **boundaries** — `scripts/python/status-digest.py` carries zero `observer` / `journal` tokens; the digest field-set delta against `test-evidence/digest-fieldset-baseline.txt` is empty; the boundary carriers (`shared/guidelines/reporting-obligations.md`, the `STAGE_ARTIFACTS` mapping — declaration carrier `shared/declarations/facts/driver-stage-artifacts.yaml` plus the fallback table in `skills/external/sdd-loop-driver/scripts/loop-state.py` — and `shared/declarations/facts/driver-stage-sequence.yaml`) show an empty `git diff --name-only <implement-entry-base>..HEAD -- <carrier paths>` against the implement-entry base (§ Environment Prerequisites).
- DoD-7: **final-path criteria** — every SC whose `**Path**` marker reads `final` has a `pass` reading and the feature's smoke record is present (GATE-4).
- DoD-8: every premise in § Premises measured at generation time is re-measured at implement entry — the 11 count/token rows by T004 into `test-evidence/premises-entry.txt`, the three guard-baseline rows by T002 into `notes/pre-change-measurements.md`; a changed value is carried into the row that uses it, never silently inherited.

**DoD Status**: pending

## Completion Gate

- GATE-1: Full suite has zero NEW failed ids vs the implement-entry baseline — check: `git check-ignore -q .specify/.tmp && mkdir -p .specify/.tmp/096 && bash scripts/bash/run-tests.sh --names-out .specify/.tmp/096/current-names.txt` then `LC_ALL=C comm -13 <implement-entry-baseline-names> .specify/.tmp/096/current-names.txt` reports an empty delta (a re-run after the suite is mandatory before claiming the feature complete; the scratch file stays under the sanctioned repo-local root `.specify/.tmp/`, never the bare OS temp directory).
- GATE-2: Every mirror obligation of plan.md § Mirror Obligations holds — check: `python3 scripts/python/sync-mirrors.py --check` reports no NEW drift against `test-evidence/plan-mirror-baseline.txt`, and the four render copies named in T042 exist and carry the fast-fail clause.
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\] T[0-9]{3} ' .specify/specs/096-sdd-observer-agent/tasks.md` returns 0.
- GATE-4: Every Success Criterion has a status line in `verification.md`, every `final`-path success criterion is `pass`, and the feature's smoke record is present — check: in `.specify/specs/096-sdd-observer-agent/verification.md`, every Success Criterion of `requirements.md` has `SC-NNN_status=`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (a path that exists and is non-empty) are present. Condition owners: `.specify/constitution.md` § VII Workflow Gates (Pre-Status-Flip record — a status line for **every** Success Criterion; the zero-open-task conjunct is GATE-3) and `shared/workflow/acceptance-hardening.md` § Gates / § Verification Vocabulary (final-path pass, smoke-record fields) — this row carries the check, not a second schema. Disclosure: 宪法 VII 的 `verification.log` 字面由框架级统一裁定（反馈已登记：`.specify/memory/feedback/20261110T124821Z-skill-sdd-loop-driver.md`），本线按框架链执行（唯一载体 `verification.md`，即 `templates/verification-log-template.md` 与 `closure-acceptance-check.py` 的输入名）。
- GATE-5: Structure and attribution are silent — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/096-sdd-observer-agent/tasks.md` exits 0 with `0 error(s)`, and every remaining warning appears in § Green Attribution's disclosed-warnings table.
- GATE-6: The script interface contract holds on the new engine — check: `python3 scripts/python/journal-utils.py --help` and `--version` exit 0, and `python3 scripts/python/journal-utils.py --bogus-option` exits non-zero rejecting the undeclared option.
- GATE-7: The tasks-stage cross-artifact gate passes — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --stage tasks --spec-dir .specify/specs/096-sdd-observer-agent --repo .` reports `decision: pass` (missing-path advisories for paths this feature creates are expected and do not block without `--strict`).
- GATE-8: The carrier boundaries are untouched — check: `grep -cE 'observer|journal' scripts/python/status-digest.py` returns 0, and `git diff --name-only <implement-entry-base>..HEAD -- shared/guidelines/reporting-obligations.md shared/declarations/facts/driver-stage-artifacts.yaml skills/external/sdd-loop-driver/scripts/loop-state.py shared/declarations/facts/driver-stage-sequence.yaml` prints no path (`<implement-entry-base>`: § Environment Prerequisites).
- GATE-9: The contract coverage baseline holds — check: `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/096-sdd-observer-agent --corpus-root .specify/specs` exits 0 with 0 uncovered names beyond `coverage-baseline.txt` and 0 `UNCOVERED-FR` names (every FR cited from a clause citation group).

## Environment Prerequisites

Probed 2026-11-10 in the line worktree (base `c691d658a`). Every row that depends on one of these verdicts references THIS section; no row restates a verdict. Re-probe at implement entry (T004) — never cached across runs. T004 also pins the **implement-entry base** (the entry-time `git rev-parse HEAD`); DoD-6, GATE-8 and T032 compare against that named commit and none other.

- CPython interpreter for the engine and the suites: **available** — probe: `python3 --version` @ 2026-11-10 → `Python 3.11.11`; `pyproject.toml` declares `>=3.8`; affected: T008–T017, T036–T037, GATE-1, GATE-6.
- `pytest` runner: **available** — probe: `python3 -m pytest --version` @ 2026-11-10 → `pytest 8.4.2`; affected: every guard row through `scripts/bash/run-tests.sh`.
- `git` read forms (`log --format`, `cat-file -e`, `rev-parse`): **available** — probe: `git --version` @ 2026-11-10 → `git version 2.43.5`; plan EP-004 verified the read forms; affected: T007, T010, T017.
- Per-tool agent render entry: **available** — probe: `specify render-agents --help` @ 2026-11-10 lists qoder, claude, copilot, opencode; affected: T041, T042.
- External services, network, container runtime, daemon: **not required** — no probe needed; every fixture builds under `tmp_path`; affected: none.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel — different **write** targets, no dependency on an incomplete row of the same phase.
- **[Story]**: `US1`…`US5` from `requirements.md`; Setup / Foundational / Polish phases carry NO `[US]` label.
- **[blockedBy: T006,T007]**: this row MUST NOT start until every listed row is `[X]`; a row without the tag follows phase order only.
- **[green: <contract>#<clause>]**: this row is the one that turns that clause green — one row per clause, never claimed twice.
- One line per row, exact file paths, no wrapped continuations.

### Task State Sigil

`- [ ]` open · `- [>]` claimed (multi-agent only) · `- [X]` closed · `- [~]` deferred with an inline `<!-- deferred: reason -->` comment.

## Path Conventions

Two hats (plan § Mirror Obligations): `agents/`, `shared/`, `scripts/`, `skills/external/`, `tests/` are **framework sources**; `.specify/agents/templates/`, `.specify/shared/`, `.specify/scripts/`, `.specify/skills/` are their generated mirrors, never hand-edited. The four per-tool agent copies under `.qoder/`, `.claude/`, `.github/` (copilot) and `.opencode/` are render products of `specify render-agents`. `docs/` is this project's development documentation (not shipped).

### Premises measured at generation time (2026-11-10)

Every quantity below was measured this stage with the re-derivation command shown, and MUST be re-measured at implement entry — the 11 count/token rows by T004 into `test-evidence/premises-entry.txt`, the three guard-baseline rows by T002 into `notes/pre-change-measurements.md`.

| Quantity | Measured | Re-derivation | Naive form that disagrees |
|---|---|---|---|
| FR definitions | **23** | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/096-sdd-observer-agent/requirements.md` | counting every `FR-0` mention also counts cross-references inside other FRs; the definition-row form is the unit |
| SC definitions | **7** | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/096-sdd-observer-agent/requirements.md` | a prose SC mention is not a definition |
| Contract clauses | **58** = 13 + 13 + 12 + 10 + 10 | `grep -cE '^## C-[0-9]+' .specify/specs/096-sdd-observer-agent/contracts/*.md` | counting `C-N` mentions inside clause bodies inflates the total; the heading form is the unit |
| Declaration fact files on disk | **34** | `ls shared/declarations/facts/*.yaml \| wc -l` | counting `registered_facts` rows in `shared/declarations/contract.yaml` returns 2 (the 094-owned block only) |
| Shipped agent presets | **17** | `grep -c 'ROOT / "agents"' tests/contract/test_fast_fail_discipline.py` | counting `*.agent.md` under `.specify/agents/templates/` counts the mirror, not the preset tuple |
| Fast-fail bounded set | **19** | `grep -n 'assert len(bounded) == 19' tests/contract/test_fast_fail_discipline.py` → line 1624 | counting presets alone (17) omits the 2 authoring texts the bound adds |
| Driver skill H2 sections | **14** | `grep -c '^## ' skills/external/sdd-loop-driver/SKILL.md` | counting `^###` as well inflates the H2 pin |
| Driver mirror list | **9** | `sed -n '/^MIRROR_FILES = \[/,/^\]/p' tests/contract/test_sdd_loop_driver_skill.py \| grep -c '    "'` | counting the whole file's quoted paths includes `CLI_PROFILE_RELS` and feature deliverables |
| Declared stage sequence | **8** | `sed -n '/^statement:/,/^consumers:/p' shared/declarations/facts/driver-stage-sequence.yaml \| grep -c '^  - '` | counting every `- ` list item in the file also counts `consumers` / `former_carriers` |
| `status-digest.py` observer tokens | **0** | `grep -c "observer" scripts/python/status-digest.py` | a case-insensitive search could match an unrelated prose word; measure case-sensitive |
| `status-digest.py` journal tokens | **0** | `grep -c "journal" scripts/python/status-digest.py` | same trap as above |
| Driver-skill guard baseline | **25 passed** | `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` (2026-11-10) | reading the plan's old value without re-running; counts drift with upstream merges |
| Fast-fail guard baseline | **2 passed** | `bash scripts/bash/run-tests.sh tests/contract/test_fast_fail_discipline.py -q -k "i10 or i11"` (2026-11-10) | running the whole module (much slower) answers a different question |
| Mirror baseline | **exit 0** | `python3 scripts/python/sync-mirrors.py --check` (2026-11-10) | a non-zero exit here is pre-existing drift, not this feature's; compare NEW drift only |

## Package Map (implement-stage dispatch boundary)

Setup rows execute first in the main worktree (they freeze baselines and create landing points). The four packages below are the implement-stage dispatch units, executed strictly in the order declared below; row-level `[blockedBy:]` tags stay the ordering authority inside a package, package edges order between packages, and every cross-package row edge points to an earlier package.

| Package | Rows | Write domain (rows' write targets; a later package may extend an earlier package's module) | Edge |
|---------|------|----------------------------|------|
| `wp01-journal-core` | T006–T017, T036 | `shared/declarations/facts/journal-format.yaml`, `tests/fixtures/sdd-observer/`, `scripts/python/journal-utils.py`, `tests/contract/test_journal_engine.py` | after Setup (carries the Foundational rows T006–T007) |
| `wp02-observer-definition` | T018–T020, T037–T038 | `agents/sdd-observer.agent.md`, `tests/contract/test_sdd_observer_agent.py`, `tests/contract/test_fast_fail_discipline.py`, `tests/contract/test_journal_engine.py` (T037 extends wp01's module) | after wp01 |
| `wp03-driver-lifecycle` | T023–T030, T034 | `skills/external/sdd-loop-driver/SKILL.md`, `skills/external/sdd-loop-driver/references/observer-lifecycle.md`, `skills/external/sdd-loop-driver/references/stage-prompts.md`, `tests/contract/test_sdd_loop_driver_skill.py`, `tests/contract/test_sdd_observer_lifecycle.py`, `tests/fixtures/sdd-observer/failure_builder.py` (T023), `docs/reference/skills/sdd-loop-driver.md` | after wp02 |
| `wp04-release-and-evidence` | T021–T022, T031–T033, T035, T039–T047 | generated mirrors + four render copies, `.specify/features.md`, `.specify/features/096.md`, `tests/contract/test_sdd_observer_agent.py` (T031 extends wp02's module), `tests/contract/test_sdd_observer_lifecycle.py` (T032 extends wp03's module), `test-evidence/`, `notes/` | after wp03 |

**Partition check**: 13 + 5 + 9 + 15 = 42 packaged rows + 5 Setup rows = 47 total, one row per ID, no ID in two packages; the largest package holds 15 rows, under the 16-row planning target. Evidence layout: the red-first captures use one file per package (`notes/red-first-evidence-wp01.md` / `-wp02.md` / `-wp03.md`), and every other evidence file is written by rows of exactly one package (Setup's `notes/pre-change-measurements.md` is written by the sequential T002/T005), so no two packages share an evidence path.

**Declared integration order**: `wp01-journal-core → wp02-observer-definition → wp03-driver-lifecycle → wp04-release-and-evidence`, executed strictly in that order — no package pair runs concurrently. Every cross-package row edge points backwards: wp02 waits on wp01 (T018←T006, T037←T036), wp03 waits on wp01 (T023←T007) and is serialized after wp02 by this declared order, and wp04 waits on all three (T021←T017/T020, T031←T020/T029, T032←T020/T029, T035←T034, T039←T037/T038, T041←T010/T017/T019/T025/T027).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: freeze every baseline the later rows compare against, re-probe the environment once, and create the fixed evidence landing points so no later row invents a path.

- [X] T001 Create the fixed evidence landing points under `.specify/specs/096-sdd-observer-agent/notes/`: `notes/red-first-evidence-wp01.md`, `notes/red-first-evidence-wp02.md` and `notes/red-first-evidence-wp03.md` (one file per package — no shared single red-first file; one entry per red-first run: command, real output, exit status), `notes/pre-change-measurements.md` (value, re-derivation command, capture date) and `notes/quickstart-run.md` (skeleton with teardown field).
- [X] T002 [P] Re-capture the pre-edit baselines into `.specify/specs/096-sdd-observer-agent/notes/pre-change-measurements.md`: `python3 scripts/python/sync-mirrors.py --check` (expect exit 0), `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` (expect 25 passed) and `bash scripts/bash/run-tests.sh tests/contract/test_fast_fail_discipline.py -q -k "i10 or i11"` (expect 2 passed), each with its real output [blockedBy: T001].
- [X] T003 [P] Capture the SC-006 status-digest field-set baseline before the first implementation edit into `.specify/specs/096-sdd-observer-agent/test-evidence/digest-fieldset-baseline.txt` from `python3 scripts/python/status-digest.py --action digest --format json --workspace .` (sorted top-level keys plus the `all_entries[]` row keys; no timestamps or ages) [blockedBy: T001].
- [X] T004 [P] Re-probe the environment named in § Environment Prerequisites at implement entry and record the readings plus the implement-entry base (`git rev-parse HEAD`) in `.specify/specs/096-sdd-observer-agent/test-evidence/env-probe.txt`; re-measure every count/token premise of § Premises with its re-derivation command and record value, delta and command in `.specify/specs/096-sdd-observer-agent/test-evidence/premises-entry.txt`.
- [X] T005 Re-freeze the contract coverage baseline with `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/096-sdd-observer-agent --corpus-root .specify/specs --freeze > .specify/specs/096-sdd-observer-agent/coverage-baseline.txt` and record the base-sha plus any delta against the tasks-stage freeze in `notes/pre-change-measurements.md` [blockedBy: T002].

**Checkpoint**: every later row names the baseline it is compared against, the evidence landing points exist, and the environment verdicts are re-measured.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the journal-format owner fact (the only copy of every spelling) and the line fixture builder (the carrier shapes every story's tests read). A story row that reads either artifact names the foundational row in `[blockedBy:]`.

**CRITICAL**: the ordering authority is the row-level `[blockedBy:]` tag (§ Package Map) — a row may start exactly when every row it lists is `[X]`, and no phase sentence adds or removes an edge. T014 reads the format fact and lists both foundational rows; T036 reads only the fixture builder.

- [X] T006 Author `shared/declarations/facts/journal-format.yaml` (`kind: record-schema`): journal filename STR-001, the five header keys, the nine entry columns in order, the sixteen event classes with `min_persistent`, retention classes `persistent`/`runtime`, the pointer kinds, the `-` placeholder and the escaping rule; read through `scripts/python/declaration_reader.py`, with no consumer holding a second copy; `python3 scripts/python/harness-triple-check.py --action verify --repo .` gains no NEW finding (baseline: 4 advisory unclassified candidates, exit 0) [green: contracts/journal-format.contract.md#C-01] [green: contracts/journal-format.contract.md#C-02] (FR-010, FR-011, FR-012)
- [X] T007 [P] Author the line fixture builder `tests/fixtures/sdd-observer/line_builder.py`: builds a stub SDD line under a caller-provided `tmp_path` — state spine with the U0 block and an observer record section, runner quartet envelopes (`pid-*` / `status-*` / `log-*.log` / `heartbeat-*.log`), per-stage sentinel logs, checkpoints, meta envelopes and a git history; the stage list is read from `shared/declarations/facts/driver-stage-sequence.yaml#/statement`, never restated (FR-013)

**Checkpoint**: the spelling face has exactly one owner and the fixture mechanism is available to every story test.

---

## Phase 3: User Story 1 - 一条 SDD 线从启动到 review，journal 留下完整轨迹 (Priority: P1)

**Goal**: one line produces one append-only `journal.md` whose rows cover every declared stage, in order, with all nine fields and a resolvable evidence pointer.

**Independent Test**: run `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py -q -k "coverage or append or idempotent or header"` against the line fixture; the journal exists, covers every stage of the declared sequence with `stage-start` (and `stage-end` on the zero-failure fixture), every row carries nine fields with `-` placeholders, and `seq` runs 1..N in file order.

### Tests for User Story 1 (MANDATORY)

- [X] T008 [US1] Author the first slice of `tests/contract/test_journal_engine.py`: stage-coverage over the declared sequence, header five keys, single nine-column table, `seq` continuity in file order, `-` placeholders, append idempotency on unchanged carriers; confirm every case fails on the current tree and append the red runs to `notes/red-first-evidence-wp01.md` [green: contracts/observer-verification.contract.md#C-01] (FR-015, SC-001) [blockedBy: T006,T007]

### Implementation for User Story 1

- [X] T009 [US1] Implement the CLI surface of `scripts/python/journal-utils.py`: exactly the actions `append` and `check`, script-interface wiring through `script_interface_cli.configure_parser` / `guard_argv` with the ImportError fallback, the `append` flags of journal-engine C-03, and the closed exit-code set [green: contracts/journal-engine.contract.md#C-01] [green: contracts/journal-engine.contract.md#C-02] [green: contracts/journal-engine.contract.md#C-03] (FR-015) [blockedBy: T008]
- [X] T010 [US1] Implement the deterministic projection and append in `scripts/python/journal-utils.py`: write the header once, render the nine-column table, project rows from the closed carrier list (spine observer section plus the two narrow prose grammars, quartet envelopes, logs/sentinels, checkpoints, git history, meta envelopes, execution records), assign stable row identities for idempotency, continue `seq`, and escape `|` / collapse newlines [green: contracts/journal-engine.contract.md#C-04] [green: contracts/journal-engine.contract.md#C-05] [green: contracts/journal-format.contract.md#C-03] [green: contracts/journal-format.contract.md#C-04] [green: contracts/journal-format.contract.md#C-05] (FR-010, FR-011, FR-013) [blockedBy: T009]
- [X] T011 [US1] Implement the single-writer protocol (non-blocking exclusive `flock` on the journal file itself; a second writer exits 3 with `concurrent-writer-refused` and writes nothing; no lock file) and the identity check against the latest state-spine observer record section (mismatch exits 2 and appends nothing) [green: contracts/journal-engine.contract.md#C-06] [green: contracts/journal-engine.contract.md#C-07] (FR-007) [blockedBy: T010]
- [X] T012 [US1] Run the US1 slice green through the one runner and record the reading in `.specify/specs/096-sdd-observer-agent/test-evidence/us1-journal-coverage.txt` [blockedBy: T011] (SC-001)
- [X] T013 [US1] Execute the SC-001 deletion mutations in a temporary copy: delete the journal, then delete one stage's `stage-end` row, and confirm the coverage test turns red for each; record both readings in `test-evidence/sc001-mutations.txt` [blockedBy: T012] (SC-001)

**Checkpoint**: User Story 1 is fully functional and independently testable — the journal trajectory exists without the driver text, the template or the checker strictness.

---

## Phase 4: User Story 2 - 记录只有事实与证据指针，评价与建议无处可写 (Priority: P1)

**Goal**: every row is a deterministic projection of a carrier fact; the structure has no field able to carry evaluation, suggestion, causal inference, severity or recommendation, and the checker rejects anything outside the closed structure.

**Independent Test**: run `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py tests/contract/test_sdd_observer_agent.py -q` — a clean journal exits 0; the three tamper fixtures (tenth column, unknown event, free narrative), a forged pointer and an unresolvable commit each exit 1 and name the row; the template carries the verbatim prohibition.

### Tests for User Story 2 (MANDATORY)

- [X] T014 [P] [US2] Author `tests/fixtures/sdd-observer/tamper_builder.py`: three structural tamper variants (a tenth column `recommendation`, an event literal `should-improve` outside the closed set, a free narrative paragraph) plus a forged-pointer journal and an unresolvable-commit journal [green: contracts/observer-verification.contract.md#C-02] [green: contracts/observer-verification.contract.md#C-04] (FR-014, SC-002, SC-004) [blockedBy: T006,T007]
- [X] T016 [US2] Extend `tests/contract/test_journal_engine.py` with the five tamper drills, the gap drill (skip an observation window; assert exactly one `observer-gap` row naming the window start and end, and that removing the gap-writing path turns it red), persistent-pointer resolution (`path exists` / `git cat-file -e` for commits) and free-narrative rejection; confirm each fails before its implementation and append the red runs to `notes/red-first-evidence-wp01.md` [green: contracts/observer-verification.contract.md#C-07] (FR-013, FR-014, SC-002, SC-004, SC-007) [blockedBy: T014]
- [ ] T018 [US2] Author `tests/contract/test_sdd_observer_agent.py`: neutral frontmatter keys, the declared `observer` role face, the verbatim 「不评价、不建议、不推断」 sequence, read domain and write surface, three-layer binding, serial-subagent rule, forbidden capabilities and the byte-identical fast-fail clause; confirm the module fails while the template is absent and append the red run to `notes/red-first-evidence-wp02.md` (FR-001, FR-002, FR-016, FR-022, SC-004) [blockedBy: T006]

### Implementation for User Story 2

- [X] T015 [P] [US2] Implement the gap derivation in `scripts/python/journal-utils.py`: on the first append of an execution whose spine `started_at` is later than the last entry's `observed_at`, append exactly one `observer-gap` row with `event_at` = window start and `observed_at` = window end, and never fill the window with inferred events [green: contracts/journal-engine.contract.md#C-08] (FR-013, SC-007) [blockedBy: T011]
- [X] T017 [US2] Implement the `check` action in `scripts/python/journal-utils.py`: findings as `code: path:line`, data-model V-1…V-13 and V-17 (V-16 is an append-time refusal enforced by `append` under C-07, never by `check`), closed sets read from `journal-format` and stage names from the stage-sequence fact, pointer resolution, escaping and free-narrative rejection, exit `0` / `1` / `2`, strictly read-only [green: contracts/journal-engine.contract.md#C-09] [green: contracts/journal-engine.contract.md#C-10] [green: contracts/journal-engine.contract.md#C-11] [green: contracts/journal-engine.contract.md#C-12] [green: contracts/journal-engine.contract.md#C-13] [green: contracts/journal-format.contract.md#C-06] [green: contracts/journal-format.contract.md#C-07] [green: contracts/journal-format.contract.md#C-08] [green: contracts/journal-format.contract.md#C-09] [green: contracts/journal-format.contract.md#C-10] [green: contracts/journal-format.contract.md#C-11] [green: contracts/journal-format.contract.md#C-12] (FR-012, FR-014, FR-015, SC-002, SC-004) [blockedBy: T011,T016]
- [ ] T019 [US2] Author `agents/sdd-observer.agent.md`: `observer` role face with no execution/review/decision authority, neutral frontmatter (`user-invocable: false`, `disable-model-invocation: false`, `supervisor: false`, `model-tier: auto`, read/search/shell-only `capability-tools`, `skills: []`, `run-turn-budget: 500`), the verbatim 「不评价、不建议、不推断」 prohibition, read domain / write surface (journal through the engine + own execution artifacts), three-layer binding with no unmerged-feature reference, serial internal subagents with host in-process concurrency BANNED, forbidden capabilities (no driver/loop load, no SDD run hosting, no user-visible reports/questions/approval requests) and the byte-identical fast-fail clause [green: contracts/observer-role.contract.md#C-02] [green: contracts/observer-role.contract.md#C-03] [green: contracts/observer-role.contract.md#C-04] [green: contracts/observer-role.contract.md#C-05] [green: contracts/observer-role.contract.md#C-06] [green: contracts/observer-role.contract.md#C-07] [green: contracts/observer-role.contract.md#C-08] (FR-001, FR-002, FR-016, FR-022) [blockedBy: T018]
- [ ] T020 [US2] Update `tests/contract/test_fast_fail_discipline.py` deliberately: add `agents/sdd-observer.agent.md` to `FACTORY_PRESETS` (17 → 18) and raise the bounded-count assertion from 19 to 20 (`17 presets + 2 authoring texts` → `18 presets + 2 authoring texts`), with a comment naming this feature [blockedBy: T019] (FR-001)
- [ ] T021 [US2] Run the US2 slice green through the one runner and record the reading in `.specify/specs/096-sdd-observer-agent/test-evidence/us2-objectivity.txt` [blockedBy: T017,T020] (SC-002, SC-004)
- [ ] T022 [US2] Record the SC-002/SC-004/SC-007 drill readings in `.specify/specs/096-sdd-observer-agent/test-evidence/objectivity-red-legs.txt`, `test-evidence/pointer-drills.txt` and `test-evidence/gap-drill.txt` [blockedBy: T021] (SC-002, SC-004, SC-007)

**Checkpoint**: objectivity is structural and machine-decidable; the template's prohibition is pinned verbatim; the checker rejects every out-of-structure shape.

---

## Phase 5: User Story 3 - 观察者掉线不阻塞开发线，缺口仍被点名 (Priority: P1)

**Goal**: observer start failure or mid-run termination never gates a stage; the spine records the observer state and the journal names the uncovered window instead of fabricating events.

**Independent Test**: run `bash scripts/bash/run-tests.sh tests/contract/test_sdd_observer_lifecycle.py tests/contract/test_sdd_loop_driver_skill.py -q` — both failure fixtures reach the terminal stage, the spine carries `state: failed` with a reason, and a doctored stage-gate sentence that requires observer liveness turns the structural predicate red.

### Tests for User Story 3 (MANDATORY)

- [ ] T023 [P] [US3] Author `tests/fixtures/sdd-observer/failure_builder.py`: a start-failure fixture and a mid-run-kill fixture (unsettled / failed status envelope, spine observer record `state: failed` with a one-line reason), both under `tmp_path` (FR-009, FR-020, SC-003) [blockedBy: T007]
- [ ] T024 [US3] Author `tests/contract/test_sdd_observer_lifecycle.py`: entry switch, startup point, spine record key set, restart-at-stage-boundary, terminal close, non-blocking predicate, the doctored-gate red leg and the digest boundary baseline comparison; confirm the non-blocking and close assertions fail before the driver text lands and append the red runs to `notes/red-first-evidence-wp03.md` [green: contracts/observer-verification.contract.md#C-03] (FR-003, FR-004, FR-005, FR-008, FR-009, FR-020, FR-023, SC-003, SC-006) [blockedBy: T023]

### Implementation for User Story 3

- [ ] T025 [US3] Author the new H2 `## SDD Observer（观察者：启动、记录节与收束）` in `skills/external/sdd-loop-driver/SKILL.md`: `observer: on|off` entry switch (default `on`; `off` recorded as `state: disabled`), startup point after line registration and spine creation and before the first stage's U2 dispatch, instance duty (one instance per line, identity = `line_id` + spec key), the append-only observer record section whose shape the section owns, restart at stage boundaries, line-terminal close, non-blocking disclosure and scope; add one References line pointing at the new reference file [green: contracts/observer-lifecycle.contract.md#C-01] [green: contracts/observer-lifecycle.contract.md#C-02] [green: contracts/observer-lifecycle.contract.md#C-03] [green: contracts/observer-lifecycle.contract.md#C-04] [green: contracts/observer-lifecycle.contract.md#C-05] [green: contracts/observer-lifecycle.contract.md#C-06] [green: contracts/observer-lifecycle.contract.md#C-07] [green: contracts/observer-lifecycle.contract.md#C-08] [green: contracts/observer-lifecycle.contract.md#C-09] [green: contracts/observer-lifecycle.contract.md#C-10] [green: contracts/observer-role.contract.md#C-09] [green: contracts/observer-role.contract.md#C-10] (FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-020, FR-021, FR-023) [blockedBy: T024]
- [ ] T026 [P] [US3] Author `skills/external/sdd-loop-driver/references/observer-lifecycle.md`: the dispatch brief template (assignment, fast-fail injection clause, concurrency-obligation pointer, read domain, write surface, forbidden list, mandatory anomaly line in the return), the engine invocation loop and actions, gap semantics and failure semantics; the brief references no driver skill and carries no loop logic [green: contracts/observer-lifecycle.contract.md#C-11] (FR-005, FR-006, FR-008, FR-013, FR-016, FR-018, FR-019, FR-022) [blockedBy: T025]
- [ ] T027 [US3] Add exactly one pointer line in `skills/external/sdd-loop-driver/references/stage-prompts.md` § 状态脊 to the observer record-section owner in `SKILL.md` (no key copy) [green: contracts/observer-lifecycle.contract.md#C-12] (FR-004, FR-017) [blockedBy: T026]
- [ ] T028 [US3] Update `tests/contract/test_sdd_loop_driver_skill.py` deliberately: add the new H2 to `PINNED_H2_SECTIONS` immediately before the compiled `Wrap-up` section and add `references/observer-lifecycle.md` to `MIRROR_FILES` (9 → 10) [blockedBy: T026,T027] (FR-003, FR-004)
- [ ] T029 [US3] Run the US3 slice green through the one runner and record the reading in `.specify/specs/096-sdd-observer-agent/test-evidence/us3-non-blocking.txt` [blockedBy: T028] (SC-003)
- [ ] T030 [US3] Record the start-failure and mid-run-kill readings plus the doctored-gate red leg in `.specify/specs/096-sdd-observer-agent/test-evidence/sc003-non-blocking.txt` [blockedBy: T029] (SC-003)

**Checkpoint**: the observer is a recorded, disclosed non-observation — its absence changes no stage verdict.

---

## Phase 6: User Story 4 - 只读且边界一致：不新造状态面、汇报面或可见性通道 (Priority: P2)

**Goal**: the observer's declared write surface is exactly the journal plus its own execution artifacts; the state spine stays the only persistent state, the existing reporting duty and `/speckit.status` field set are unchanged, and visibility rides the existing artifact triplet.

**Independent Test**: run `bash scripts/bash/run-tests.sh tests/contract/test_sdd_observer_agent.py tests/contract/test_sdd_observer_lifecycle.py -q` — the write-surface assertions name exactly two surfaces, `status-digest.py` carries zero observer/journal tokens, the digest field-set delta against the frozen baseline is empty, and the driver text presents the observer only through the existing `--sub-flow <label>=<triplet-dir>` semantics.

### Tests for User Story 4 (MANDATORY)

- [ ] T031 [US4] Extend `tests/contract/test_sdd_observer_agent.py` with the template-side boundary assertions: exactly two write surfaces; no text grants a spine, stage-artifact, registry or glossary write path; the role face is not a stage executor, reviewer or reporter seat; the verbatim prohibition and the no-evaluation/no-suggestion/no-causal field rule hold [green: contracts/observer-verification.contract.md#C-06] (FR-016, FR-017, FR-018, FR-019, SC-006) [blockedBy: T020,T029]
- [ ] T032 [US4] Extend `tests/contract/test_sdd_observer_lifecycle.py` with the driver/digest-side boundary assertions: the observer appears only through the existing `--sub-flow <label>=<triplet-dir>` supervision projection; `status-digest.py` carries no observer/journal token; the boundary carriers (`shared/guidelines/reporting-obligations.md`, the `STAGE_ARTIFACTS` mapping — `shared/declarations/facts/driver-stage-artifacts.yaml` plus the `loop-state.py` fallback table — and `shared/declarations/facts/driver-stage-sequence.yaml`) are unchanged against the implement-entry base: an empty `git diff --name-only <implement-entry-base>..HEAD -- <the four carrier paths>` (§ Environment Prerequisites) plus the structural invariants that the mapping's stage keys equal the stage-sequence `statement` and the obligations page still carries its `## 十一 · 零新增机制` heading; the journal is not a stage artifact or U4 completion condition (FR-017, FR-018, FR-019, SC-006) [blockedBy: T020,T029]
- [ ] T033 [US4] Capture the post-implementation digest field set with the same command as T003 and compare it against `test-evidence/digest-fieldset-baseline.txt`; record the empty delta (or name every added field as a failure) in `.specify/specs/096-sdd-observer-agent/test-evidence/digest-boundary.txt` [blockedBy: T003,T031,T032] (SC-006)

### Implementation for User Story 4

- [ ] T034 [P] [US4] Update `docs/reference/skills/sdd-loop-driver.md` with one additive observer section: the mechanism sentence (observer sub-flow, journal, non-blocking) plus owner pointers — no restated key set, no new status field [blockedBy: T025] (FR-001, FR-018)
- [ ] T035 [US4] Run the US4 slice green through the one runner and record the reading in `.specify/specs/096-sdd-observer-agent/test-evidence/us4-boundaries.txt` [blockedBy: T033,T034] (SC-006)

**Checkpoint**: a reader still learns "where it is now" from the spine/digest and "what happened" from the journal — no third channel exists.

---

## Phase 7: User Story 5 - 一 spec 一专用实例，可选内部 subagent (Priority: P2)

**Goal**: one dedicated observer instance per line and one journal per spec directory; two parallel lines never share a path or an identity; the second live writer is refused; internal subagents are permitted but serial and inherit every bound.

**Independent Test**: run `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py tests/contract/test_sdd_observer_agent.py -q` — two temp lines produce two distinct journals and two distinct instance identities with zero shared paths, a second concurrent append on one journal exits 3, the first journal row precedes the first stage-completion row, and the template audit allows serial internal subagents while banning the host in-process carrier.

### Tests for User Story 5 (MANDATORY)

- [X] T036 [P] [US5] Author `tests/fixtures/sdd-observer/dual_line_builder.py`: two independent temp project roots, each with its own spec directory, state spine and state dir [green: contracts/observer-verification.contract.md#C-05] (FR-003, SC-005) [blockedBy: T007]
- [ ] T037 [US5] Extend `tests/contract/test_journal_engine.py` with first-journal-row ordering, dual-line isolation (two journals, two identities, zero shared paths) and the same-line second-writer exit-3 assertion; append the red runs to `notes/red-first-evidence-wp02.md` (FR-003, FR-007, SC-005) [blockedBy: T020,T036]
- [ ] T038 [P] [US5] Extend `tests/contract/test_sdd_observer_agent.py` with the instance-identity and subagent capability audit: the instance slug derives from `line_id`, no stage command creates an instance, internal subagents are allowed but serial only, the host in-process path is BANNED as a concurrency carrier, and no driver/loop load or SDD run hosting is permitted [blockedBy: T020] (FR-003, FR-022, SC-005)

### Implementation for User Story 5

- [ ] T039 [US5] Run the US5 slice green through the one runner and record the reading in `.specify/specs/096-sdd-observer-agent/test-evidence/us5-isolation.txt` [blockedBy: T037,T038] (SC-005)
- [ ] T040 [US5] Record the two journal paths, the two instance identities, the zero-shared-path reading and the second-writer exit-3 reading in `.specify/specs/096-sdd-observer-agent/test-evidence/dual-line-isolation.txt` [blockedBy: T039] (SC-005)

**Checkpoint**: two parallel lines cannot write into one record; one line cannot run two live observers.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: generate the mirrors and render copies, run the full suite as the one evidence opportunity, reconcile the feature registry, execute the quickstart end to end, and close the structural gates.

- [ ] T041 Generate the framework mirrors and per-tool render copies: `python3 scripts/python/sync-mirrors.py --write` for the `agents/`, `shared/`, `scripts/` and `skills/external/` pairs, then `specify render-agents --ai qoder`, `--ai claude`, `--ai copilot` and `--ai opencode` [green: contracts/observer-role.contract.md#C-01] [green: contracts/observer-verification.contract.md#C-08] (FR-001) [blockedBy: T010,T017,T019,T025,T027]
- [ ] T042 [P] Verify the generated surfaces: `python3 scripts/python/sync-mirrors.py --check` shows no NEW drift against `test-evidence/plan-mirror-baseline.txt`; `.specify/agents/templates/sdd-observer.agent.md` is byte-identical to the source; the four render copies exist and carry the fast-fail clause; record the readings in `.specify/specs/096-sdd-observer-agent/test-evidence/render-verify.txt` [blockedBy: T041] (FR-001)
- [ ] T043 Run the full suite through the one runner with `bash scripts/bash/run-tests.sh --names-out .specify/specs/096-sdd-observer-agent/test-evidence/full-suite-names.txt`; classify every failed id against the implement-entry baseline and record the reading in `.specify/specs/096-sdd-observer-agent/test-evidence/full-suite.txt` [green: contracts/observer-verification.contract.md#C-09] [green: contracts/observer-verification.contract.md#C-10] (SC-001, SC-002, SC-003, SC-004, SC-005, SC-006, SC-007) [blockedBy: T035,T040,T042]
- [ ] T044 [P] Reconcile the feature registry: refresh the `.specify/features.md` row 096 and `.specify/features/096.md` detail with the implemented artifact/test pointers and re-run the Feature Integration review — no new Feature is exposed by the task breakdown and no existing feature is invalidated [blockedBy: T043]
- [ ] T045 [P] Execute quickstart S-0…S-7 end to end against the implemented tree, including the tamper drills and teardown, and record the real output in `.specify/specs/096-sdd-observer-agent/notes/quickstart-run.md` [blockedBy: T043] (SC-001, SC-002, SC-003, SC-004, SC-005, SC-006, SC-007)
- [ ] T046 Record the SC → row → evidence trace in `.specify/specs/096-sdd-observer-agent/test-evidence/requirements-sc-map.txt`: one line per SC-001…SC-007 naming its task rows and the evidence path that discharges it [blockedBy: T045]
- [ ] T047 Close the structural gates and record them in `.specify/specs/096-sdd-observer-agent/test-evidence/tasks-stage-gates.txt`: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/096-sdd-observer-agent/tasks.md` exit 0, `pre-analyze-check.py --stage tasks` decision `pass`, `account-clause-coverage.py` exit 0 (0 uncovered beyond the frozen baseline and 0 uncited FRs), and the journal-format C-13 boundary (journal absent from `STAGE_ARTIFACTS` and every stage required-artifact set) [green: contracts/journal-format.contract.md#C-13] [blockedBy: T046] (SC-001, SC-006)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies — runs first in the main worktree.
- **Foundational (Phase 2)**: depends on Setup — provides the two rows the story rows list in `[blockedBy:]`; the tags and package edges carry the exact order.
- **US1 (Phase 3)**: after Foundational; builds the engine core (MVP start).
- **US2 (Phase 4)**: after US1's engine core (T011) and Foundational; extends the same engine and the template.
- **US3 (Phase 5)**: after Foundational; independent of US1/US2 in write domain (driver + tests), but its lifecycle test asserts the spine/engine behaviors from US1.
- **US4 (Phase 6)**: after US2's template (T020) and US3's lifecycle rows (T029).
- **US5 (Phase 7)**: after US2's template (T020) and Foundational; the engine-extension rows reuse the US1 module.
- **Polish (Phase 8)**: after US4 and US5; the mirror render (T041) is the last source-touching row.

### User Story Dependencies

- **US1 (P1)**: independent after Foundational.
- **US2 (P1)**: integrates with US1's engine (append/gap/check on the same module) but its checkpoint is independently testable.
- **US3 (P1)**: independent of US1/US2 for its driver text and failure fixtures; its non-blocking proof does not depend on the template.
- **US4 (P2)**: depends on US2 (template text) and US3 (driver text); the digest baseline is frozen in Setup.
- **US5 (P2)**: depends on US2 (template) and US1's engine identity behavior.

### Within Each User Story

- Tests MUST be authored and fail before the implementation row that turns them green.
- Engine rows follow CLI → projection/append → safety (flock/identity) → gap → check.
- Prose rows follow the guard row that asserts them.
- Story complete before moving to the next priority.

### Parallel Opportunities

- Setup: T002, T003 and T004 run in parallel after T001.
- Foundational: T006 and T007 run in parallel.
- US2: T014 (tamper fixture) and T015 (gap engine) and T018 (agent test) are independent write targets.
- US3: T026 (reference) and T027 (stage-prompts pointer) run in parallel after T025.
- US4: T034 (docs) runs in parallel with the boundary test rows.
- US5: T036 (dual-line fixture) and T038 (agent-test audit) run in parallel.
- Polish: T042, T044 and T045 can start once their blockers are closed; T043 is the single full-suite run.

These are same-phase `[P]` opportunities for a single executor; under package dispatch the package chain in § Package Map is strict.

---

## Parallel Example: Foundational + US2

```bash
# Foundational — the two blocking artifacts in parallel:
Task: "T006 Author shared/declarations/facts/journal-format.yaml"
Task: "T007 Author tests/fixtures/sdd-observer/line_builder.py"

# US2 — independent write targets after Foundational/US1:
Task: "T014 Author tests/fixtures/sdd-observer/tamper_builder.py"
Task: "T015 Implement gap derivation in scripts/python/journal-utils.py"
Task: "T018 Author tests/contract/test_sdd_observer_agent.py"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: all three P1 stories (US1 + US2 + US3) — the user's requirement is one mechanism, and each alone is half of it: US1 records but does not constrain objectivity, US2 checks a record nobody produces yet, US3 keeps alive a mechanism whose record does not exist. Per the template's MVP rule, the MVP covers all same-priority stories that only together form an independently valuable increment. US4 and US5 are the P2 boundary and cardinality properties that harden a working mechanism.

1. Complete Setup + Foundational.
2. Complete US1 → US2 → US3 (Phases 3–5) — the MVP.
3. **STOP and VALIDATE**: run each story's independent test command at its checkpoint.
4. Complete US4 and US5 (Phases 6–7).
5. Complete Polish (Phase 8) — mirrors, full suite, quickstart, registry, gates.

### Incremental Delivery

1. Setup + Foundational → baselines frozen, fixture mechanism proven.
2. US1 → a journal trajectory exists and is coverage-tested.
3. US2 → objectivity is structural and the tamper drills are red/green as designed.
4. US3 → the observer cannot block the line, and gaps are named.
5. US4 + US5 → boundaries and per-line cardinality are pinned.
6. Polish → generated surfaces, full-suite evidence, quickstart, closure.

### Parallel Team Strategy

1. Setup rows first in the main worktree; the Foundational rows (T006–T007) open `wp01-journal-core`.
2. Run `wp01-journal-core` → `wp02-observer-definition` → `wp03-driver-lifecycle` strictly in that order — each package waits for the previous one (wp02 needs wp01's T006/T036; wp03 is serialized after wp02 by the declared order so no package pair needs concurrent write access).
3. `wp04-release-and-evidence` integrates last; its evidence rows are append-only sinks and never touch source files.

---

## SC → row trace

| SC | Task rows | Evidence |
|----|-----------|----------|
| SC-001 | T008, T012, T013, T043, T045 | `test-evidence/us1-journal-coverage.txt`, `test-evidence/sc001-mutations.txt`, `test-evidence/full-suite.txt` |
| SC-002 | T014, T016, T022, T043, T045 | `test-evidence/pointer-drills.txt`, `test-evidence/objectivity-red-legs.txt` |
| SC-003 | T023, T024, T029, T030, T043, T045 | `test-evidence/sc003-non-blocking.txt` |
| SC-004 | T014, T016, T018, T019, T022, T043, T045 | `test-evidence/objectivity-red-legs.txt` |
| SC-005 | T036, T037, T038, T039, T040, T043, T045 | `test-evidence/dual-line-isolation.txt` |
| SC-006 | T031, T032, T033, T035, T043, T045, T047 | `test-evidence/digest-boundary.txt`, `test-evidence/us4-boundaries.txt` |
| SC-007 | T015, T016, T022, T043, T045 | `test-evidence/gap-drill.txt` |

## Green Attribution

Every `[green:]` claim resolves to exactly one row, and every one of the 58 contract clauses (13 + 13 + 12 + 10 + 10) is claimed exactly once. The four clauses the first analyze round recorded as deliberately unclaimed (finding E-01) are now claimed by the rows that discharge them:

| Clause | Claimed by | Why this row turns it green |
|--------|-----------|------------------------------|
| `contracts/observer-role.contract.md#C-01` | T041 | the mirror and render generation is C-01's completion step; T042 only verifies it |
| `contracts/observer-verification.contract.md#C-03` | T024 | the lifecycle test authors the non-blocking assertions and the doctored-gate red leg |
| `contracts/observer-verification.contract.md#C-05` | T036 | the dual-line fixture is the artifact C-05 names (two journals, two identities, second writer refused) |
| `contracts/observer-verification.contract.md#C-07` | T016 | the gap drill is authored in the journal-engine test extension |

**Disclosed warnings** — `validate-tasks.py` exits 0; these are the only warnings it reports:

| Warning | Rows involved | Why it stands |
|---------|---------------|----------------|
| `green-cross-phase` | T025→T041 in `contracts/observer-role.contract.md` (C-10 → C-01) | C-01's completion (mirror + render) necessarily lands after the template clause block; the claim sits on the row that turns it green, not on a row chosen to keep ordinals monotone |
| `green-cross-phase` × 2 | T016→T024 and T031→T036 in `contracts/observer-verification.contract.md` | the page's clause order (C-03 before C-04, C-05 before C-06) does not follow the delivery order (SC-004 in US2, SC-003 in US3; SC-006 in US4, SC-005 in US5), so two adjacent claim pairs run backwards in clause ordinal; re-cutting the contract's clause partition is a plan-stage change |
| `green-path-divergence` | T008/T016 in `tests/contract/test_journal_engine.py` (C-01 vs C-07) | two distinct slices of one test module; the file accumulates green points, and each row is the one that turns its own clause green |

## Notes

- `[P]` rows write different files and depend on no incomplete row of the same phase; the red-first captures use one file per package (`notes/red-first-evidence-wp01.md` / `-wp02.md` / `-wp03.md`), so no two packages share an evidence path, and the remaining `notes/` and `test-evidence/` files are write targets of a single row (Setup's `notes/pre-change-measurements.md` by the sequential T002/T005), not source write targets.
- The journal-format fact is deliberately **not** registered in `shared/declarations/contract.yaml` (plan R-05): the 094 C-86 closed-set pin stays valid and the fact is read by file through `declaration_reader`.
- The SC status-record carrier of GATE-4 is `verification.md` — the sole input name of the framework implementation chain (`shared/workflow/acceptance-hardening.md` § Gates condition 2; `templates/commands/implement.md` § Feature Integration; `scripts/python/closure-acceptance-check.py` `REQUIRED_INPUTS`; vocabulary owner `templates/verification-log-template.md`). The constitution VII literal `verification.log` is under framework-level adjudication (feedback registered, see GATE-4 Disclosure), and this line follows the framework chain: no task row writes a `verification.log`, which `.gitignore:37` (`*.log`) would exclude from the commit.
- No row adds a `/speckit.*` command, a skill directory, a scheduler, a daemon, a second registry, a second state store, a digest field, or an edit to any stage command template.
- The observer execution artifacts land in the existing `.specify/agents/execution/logs/` layout; the journal references them as runtime-retention pointers and never copies their content.
- Commit after each task or logical group; a `[~]` deferral must carry its reason as an inline `<!-- deferred: reason -->` comment, never an open `[ ]`.
