---

description: "Task list for Feature 092 Non-Disposable"
---

# Tasks: Non-Disposable（不可一次性处置）

**Requirement ID**: 092
**Requirement Key**: 092-non-disposable
**Related Feature**: 092 Non-Disposable（不可一次性处置） (from `.specify/memory/features.md`)
**Input**: Design documents from `.specify/specs/092-non-disposable/`
**Prerequisites**: plan.md (required), requirements.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" plus Principle VII
(specification → plan → task → implementation) make the test rows mandatory. `plan.md` § Complexity Tracking row IV
records the partial compliance honestly: the guards for the new engine cannot be written before the engine exists, so
each guard carries a **mutation leg** (break the subject, assert red) instead of a red-first stub that would supply
the verdict it checks. A clause's green point sits on the row that **writes the artifact the clause governs** — for
the eight contracts that is the content row, and the P5 guard rows re-read those clauses without claiming them.

**Organization**: this is a governance + mechanism feature, not an app: its phases are the plan's **implement
packages P1–P8**, and each phase is independently verifiable through its own checkpoint. Package ownership
(territory) is owned by `plan.md` § Implement Package Proposal; this file does not restate it.

## Definition of Done (DoD)

- DoD-1: Every artifact in `plan.md` § Source Code (repository root) that this feature creates or edits exists and is non-empty, and every `.specify/` mirror is produced by `sync-mirrors.py`, never hand-written
- DoD-2: The guard file `tests/contract/test_non_disposable_contract.py` is green under `pytest -m contract` and carries one mutation leg per closed set and per detection class — `detection-categories` C-106 (per class), `status-and-verification` C-207 (the substituted checker), `disposition` C-307 (no batch rewrite channel), `renumber-and-supersede` C-505 (both predicate legs), `detection-engine-cli` C-606 (a path duplicated across scopes) — each leg **observed red** before its green counts. `acceptance-readability` C-803's leg is the clash-vs-consistent pair: the clash fixture lands red on its cell **and** the consistent fixture lands green, which a guard that reddens every `Planned` row would fail
- DoD-3: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/092-non-disposable/tasks.md` exits 0, and `account-clause-coverage.py --spec-dir .specify/specs/092-non-disposable` reports every one of the 62 clauses claimed (`0 error(s)`) with an empty FR lane (`FR uncovered: 0`)
- DoD-4: Every 档 I corpus entry (19: A1–A6, B1–B5, C1–C4, G1–G3) is closed **by name** on a second engine reading, and every 档 II entry (15) reaches a receiving body — read as **12** handoff markers, one per `plan.md` § Shift List row, not 15 — while its body stays untouched by this feature's diff. The two counts differ on purpose: 19 / 15 count corpus entries, 12 counts receiving bodies (C-805, § Shift List count table)
- DoD-5: `sanitize-utils.py`'s four closed sets are byte-unchanged; both constitution count pin guards are unmoved; `wc -c .specify/instructions.md` stays within `INSTRUCTIONS_BUDGET_BYTES`
- DoD-6: `verification.md` carries a status row per success criterion (20) plus the smoke record, and `closure-acceptance-check.py` is the verdict that flips the status
- DoD-7: The `D-1`…`D-8` decision rows are registered in `.specify/memory/register.md`, and the registry row for 092 sits at `Planned` with `.specify/memory/features/092.md` present

**DoD Status**: pending

## Completion Gate

- GATE-1: No NEW failure vs the recorded frozen baseline — check: `pytest -m contract` name list compared to the frozen failed node-id set by name (`comm -13` / `comm -23`), both directions empty; baseline owner: `/speckit.implement` step 6 `**Test runs**`
- GATE-2: Every mirror obligation from `plan.md` § Mirror Obligations verified — check: `python3 scripts/python/sync-mirrors.py --check` reports no new drift on the pairs this spec touches, and `diff -q` on each byte-equal pair in `plan.md` § Mirror Obligations is empty
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/092-non-disposable/tasks.md` returns 0
- GATE-4: Every `final`-path success criterion is `pass` **and** the feature's smoke record is present — check: in `.specify/specs/092-non-disposable/verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (an existing non-empty path) are all present, unless an explicit user waiver names that criterion. Condition set owner: `shared/workflow/acceptance-hardening.md` § Gates — this row carries the check, not a second schema
- GATE-5: Every contract clause is claimed by exactly one row, and the FR lane is empty **by citation or by a named declaration** — check: `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/092-non-disposable` exits 0 with an empty `UNCOVERED` list and `FR uncovered: 0`. The FR lane is **not** required to be empty by absence: the three process-grade FRs (FR-046, FR-050, FR-051) are closed by `contracts/acceptance-readability.contract.md` C-806's named declaration, and the remaining FRs by clause citation groups. A run that reaches `FR uncovered: 0` only by adding an empty citation to a clause has not met this gate — the closure must be either a real citation or the C-806 declaration, which names its three FRs explicitly
- GATE-6: The closed sets this feature is forbidden to move are byte-unchanged — check: `pytest -m contract tests/contract/test_constitution_double_landing.py tests/contract/test_fast_fail_discipline.py` plus the four-set comparison asserted by the guard

## Environment Prerequisites

- CPython ≥ 3.8 interpreter: available — probe: `/usr/bin/python3 --version` @ 2026-11-09 → `Python 3.11.0rc1`; affected phases/tasks: P2, P5, P6, P7, P8
- `pytest`: available — probe: `python3 -m pytest --version` @ 2026-11-09; the frozen failed node-id set of the contract suite is the comparison baseline (EP-002). Affected: P5, P8
- `git` CLI: available — probe: `git rev-parse --short HEAD` @ 2026-11-09 → `69c45fec`; affected: T036, T066, T110, T128, T149
- container runtime / live cluster / remote registry: none required — this feature is stdlib Python plus Markdown; no row below needs an external service, so no probe applies
- `scripts/python/sync-mirrors.py` and `scripts/python/regen-command-copies.py`: available in-repo (stdlib) — probe: `python3 scripts/python/sync-mirrors.py --help` @ 2026-11-09; affected: T059, T069, T070, T167

**A13 boundary** (owner: `shared/workflow/acceptance-hardening.md` § Gates): this section records **task-generation
probe verdicts** only. Planning-time load-bearing premises live in `plan.md` § Execution Premises (EP-001…EP-008)
and are not restated here.

## Format: `[ID] [P?] Description with file path [green: <contract>#<clause>]`

- **[P]**: can run in parallel — a different file, and no unfinished dependency
- A **blocked-by list** (written in the row's own brackets) — the row MUST NOT start until every listed row is `[X]`. The list is one or more concrete task ids, comma-separated; a pattern, a range or a placeholder is a malformed row
- **[green: <contract>#<clause>]** — the row that turns that clause green; each of the 62 clauses is claimed
  exactly once (see § Green Partition)
- Phases are the plan's packages P1–P8 (§ Organization). This feature's nine user stories are satisfied by the
  package chain; each package names the stories it serves in its own `Package` line, and no row carries a `[US]`
  label because no phase is a story phase

## Path Conventions

Single project, framework self-hosting repository. `shared/`, `scripts/`, `templates/`, `skills/` are the framework
**sources**; their `.specify/` counterparts are generated by `scripts/python/sync-mirrors.py` and MUST NOT be
hand-edited. `.specify/memory/{glossary,features,register}.md` are single-copy live governance files.

---

## Phase 1: P1 — Owner page, declaration fact and registration

**Package**: P1 (`plan.md` § Implement Package Proposal). **Serves**: US2, US5, US6 (the rule owner the rest reads).
**Checkpoint**: the owner page exists and declares what it owns; the fact loads through the single read entry; the
registry row says `Planned`; the eight decisions are registered; the corpus and the frozen baseline exist.

- [X] T001 Author § Status Readability of `shared/definitions/non-disposable-definitions.md` — the objects a status claim rests on (registry row; `verification.md` machine-block and smoke fields; `tasks.md` structure; decision-tension records), what makes each red, and the explicit statement that `requirements.md` `**Path**:` markers are judged by `validate-requirements.py`'s `path-marker` check and never by `status-unreadable` [green: contracts/acceptance-readability.contract.md#C-801]
- [X] T002 Author the closed status × verdict contradiction table in `shared/definitions/non-disposable-definitions.md` § Status Readability — seven registry values (`Draft` / `Planned` / `Implemented` / `Blocked` / `Ready for Review` / `Completed`, plus `Relocated` excluded by name with its `count: 0` reason) crossed with `accept` / `block`, the reason code only on the two completion-claim cells, empty `reasons` plus `evidence_refs` on the rest, and the three prohibitions (unknown spelling exits 2; `Completed` / `Relocated` not out of scope beyond the named exclusion; a third verdict value fails the guard) [green: contracts/acceptance-readability.contract.md#C-802]
- [X] T003 State in `shared/definitions/non-disposable-definitions.md` § Status Readability which corpus rows and fixture legs prove each cell — A3 for `Planned × accept`, A1 for `Implemented × block` and `Ready for Review × block`, a clash fixture and a separate consistent fixture for the rest — and that A3 MUST land red, not merely described [green: contracts/acceptance-readability.contract.md#C-803]
- [X] T004 State in `shared/definitions/non-disposable-definitions.md` § Status Readability that a `requirements.md` success-criterion row carrying no `**Path**:` marker is reported by `scripts/python/validate-requirements.py`'s `path-marker` check — never by `status-unreadable` — and that the engine only carries that reading as an `evidence_refs` element [green: contracts/acceptance-readability.contract.md#C-804]
- [X] T005 State the 档 II handoff marker's form (one line per receiving body, corpus id from the 档 II set, receiving feature from `plan.md` § Shift List), its count (`12` rows = `12` receiving bodies = `12` markers), and record in `team/092-non-disposable/team.md` § Handoff boundary which surface lands it — P7 cross-line write with the `forbidden` list narrowed to the marker lines, or the receiving body's own line [green: contracts/acceptance-readability.contract.md#C-805]
- [X] T006 Create the owner page skeleton at `shared/definitions/non-disposable-definitions.md` — a header declaring the entries it owns (concept, disposition set + exemption forms, detection-class closed set, review-surface definition, supersede protocol, renumber predicate face, report schema, boundary with sanitize/history, relation to the constitution) [green: contracts/detection-categories.contract.md#C-101]
- [X] T007 Author § Detection Categories of `shared/definitions/non-disposable-definitions.md` — the eight-member closed set — and the § Detection Subject rule that binds each member's predicate to a program-readable reading (file / line / field / literal / count / path / resolvable reference) [green: contracts/detection-categories.contract.md#C-102]
- [X] T008 Author the four structure classes' predicates (`superseded-live`, `multi-owner`, `orphan-path`, `renumber-live-binding`) with their evidence obligations in `shared/definitions/non-disposable-definitions.md` [green: contracts/detection-categories.contract.md#C-103]
- [X] T009 Author the four state classes' predicates (`status-unreadable`, `false-closed-set`, `stale-constant`, `deferral-marker`) with their evidence obligations in `shared/definitions/non-disposable-definitions.md` [green: contracts/detection-categories.contract.md#C-104]
- [X] T010 State in `shared/definitions/non-disposable-definitions.md` that the reviewed corpus carries no `deferral-marker` row and that the class MUST be proven by construction instead [green: contracts/detection-categories.contract.md#C-105]
- [X] T011 State the per-class mutation-leg obligation (one defect-creating leg per class plus the inverse) in `shared/definitions/non-disposable-definitions.md` [green: contracts/detection-categories.contract.md#C-106]
- [X] T012 State the "a class that finds nothing reports `count: 0` over a declared surface" rule in `shared/definitions/non-disposable-definitions.md` [green: contracts/detection-categories.contract.md#C-107]
- [X] T013 Record in `shared/definitions/non-disposable-definitions.md` that a class name outside the eight-member set is an `unknown-class` finding, never a silent extra class [green: contracts/detection-categories.contract.md#C-108]
- [X] T014 Author § Disposition Set of `shared/definitions/non-disposable-definitions.md` — four members, one owner, and the "do nothing is not a disposition" prohibition [green: contracts/disposition.contract.md#C-301]
- [X] T015 State the rejected values explicitly in `shared/definitions/non-disposable-definitions.md` (`null` / `""` / `keep` / `leave` / `none` / free text are findings, emitted as open) [green: contracts/disposition.contract.md#C-302]
- [X] T016 Author § Exemption in `shared/definitions/non-disposable-definitions.md` — the four required fields (`reason`, `expiry_kind`, `expiry_value`, `expiry_recheck`) and the rejection of a missing member or a constant-true condition [green: contracts/disposition.contract.md#C-303]
- [X] T017 Author § Exemption expiry semantics in `shared/definitions/non-disposable-definitions.md` — `on-date` / `on-review` date comparison, `on-condition` engine evaluation, and "unevaluable = `unevaluated`, never still valid" [green: contracts/disposition.contract.md#C-304]
- [X] T018 Author § Disposition Bridge in `shared/definitions/non-disposable-definitions.md` — the per-value mapping table and the unmappable table whose row count is the Cartesian product of the two closed sets [green: contracts/disposition.contract.md#C-305]
- [X] T019 Author the two explicit prohibitions (`exempt` has no material-hygiene counterpart; `dismiss` MUST NOT be read as deferred) with a named receiving surface per unmappable row, and the single adjudication rule ("the detecting engine decides the disposition vocabulary") exactly once, in `shared/definitions/non-disposable-definitions.md` [green: contracts/disposition.contract.md#C-306]
- [X] T020 Author § Disposal Pathways in `shared/definitions/non-disposable-definitions.md` — archive is a move, deletion is never a disposition, no batch rewrite channel [green: contracts/disposition.contract.md#C-307]
- [X] T021 State in `shared/definitions/non-disposable-definitions.md` the archive disposition's requirements — `archive` is a move with the source → archive mapping recorded, the superseded text is kept, and a deletion is never a disposition [green: contracts/disposition.contract.md#C-308]
- [X] T022 Author § Supersede Protocol of `shared/definitions/non-disposable-definitions.md` — the three landing faces (body / guard / evidence path) a superseding side MUST recover [green: contracts/renumber-and-supersede.contract.md#C-501]
- [X] T023 Author the mechanical detection of incomplete recovery (missing pointer, stale guard, second evidence spelling) in `shared/definitions/non-disposable-definitions.md` [green: contracts/renumber-and-supersede.contract.md#C-502]
- [X] T024 Author the supersede registry row form (superseded → superseding → disposition → evidence) in `shared/definitions/non-disposable-definitions.md` [green: contracts/renumber-and-supersede.contract.md#C-503]
- [X] T025 Author § Renumber-Face of `shared/definitions/non-disposable-definitions.md` — the four live-binding shapes and the closed history-record predicate enumeration, quoted from `scripts/python/renumber-utils.py` by pointer [green: contracts/renumber-and-supersede.contract.md#C-504]
- [X] T026 Author the owner page's history-record rule (never rewritten to suit a renumber; a rewrite is reported red) while keeping every predicate in `scripts/python/renumber-utils.py` [green: contracts/renumber-and-supersede.contract.md#C-505]
- [X] T027 Author the owner page's single-predicate rule (the engine consumes `renumber-utils.py`'s `EXCLUDED_PREFIXES` / `MACHINE_PREFIXES` / `EVIDENCE_SEGMENTS` / `DATED_RE`, never a copy) [green: contracts/renumber-and-supersede.contract.md#C-506]
- [X] T028 Author § Report Entry in `shared/definitions/non-disposable-definitions.md` — the entry fields (`entry_id`, `path`, `line`, `class`, `detection`, `state`, `disposition`, `evidence_refs`) and the two `detection` values, with the `semantic` evidence minimum stated [green: contracts/report-schema.contract.md#C-701]
- [X] T029 Author § Report Envelope in `shared/definitions/non-disposable-definitions.md` — the coverage declaration as the first block, the four reader questions, and the "no unprovable closure" rule that makes `closed` a derived value [green: contracts/report-schema.contract.md#C-702]
- [X] T030 Create `shared/declarations/facts/non-disposable-review-surface.yaml` as a `kind: closed-set` fact carrying the five required keys and the ten roots in their declared order [green: contracts/detection-engine-cli.contract.md#C-601]
- [X] T031 Register the owner page in `shared/definitions/framework-map.md` with one directory-registration row [green: contracts/detection-engine-cli.contract.md#C-602]
- [X] T032 Declare in the owner page § Engine Contract that the engine resolves every root through `scripts/python/declaration_reader.py`, that a missing or invalid declaration exits 2 naming the path or key `STR-014`, and that an undeclared sibling produces a hint only [green: contracts/detection-engine-cli.contract.md#C-603]
- [X] T033 Declare in the owner page § Engine Contract the argument set (the eight declared options and no other) and the three-valued exit-code surface with the empty-surface prohibition [green: contracts/detection-engine-cli.contract.md#C-604]
- [X] T034 Declare in the owner page § Engine Contract the sharding rule (membership a pure function of the sorted path list, disjoint union equal to the candidate set, no empty shard), deterministic serialisation, and the single mirror-projection block placement [green: contracts/detection-engine-cli.contract.md#C-605]
- [X] T035 Add the four glossary terms to `.specify/memory/glossary.md` — `Non-Disposable` / `Disposition（处置）` / `Review Surface（回顾面）` / `Exemption（豁免）` — each a pointer that restates no owner criterion
- [X] T036 Author the owner page's capture rule for the "diff against pre-change output" premises — which four readings a run MUST take before an edit (the `sync-mirrors.py --check` baseline, `wc -c .specify/instructions.md`, the two constitution pin readings, `git status --porcelain`) — in `shared/definitions/non-disposable-definitions.md` [green: contracts/four-stage-command.contract.md#C-401]
- [X] T037 Write `.specify/specs/092-non-disposable/notes/pre-change-measurements.md` with those four readings taken on this tree at generation time, recording each command and its raw output, **and** freeze `notes/baseline-failed-tests.txt` (the failed node-id name list, before any edit — the designation GATE-1 compares against, never a count) [blockedBy: T036]
- [X] T038 Create the 092 row in `.specify/memory/features.md` at status `Planned` and re-read the `Total Features` header in the same pass (the index is hand-maintained; header and rows move together) [blockedBy: T001]
- [X] T039 Create `.specify/memory/features/092.md` from `.specify/templates/feature-details-template.md` — Overview / Latest Review / Key Changes / Implementation Notes / Future Evolution Suggestions / Related Files, including the constitution-XI boundary line [blockedBy: T038]
- [X] T040 Register the eight clarify decisions `D-1`…`D-8` in `.specify/memory/register.md` as pointer-shaped rows (id → one-line meaning → authority path → status), placed where the table's existing `D-…` rows sit
- [X] T041 Create `.specify/specs/092-non-disposable/notes/measurement-corpus.md` — the 35 A–H entries with their 档 I / 档 II tier and reproduction source, read from `notes/input-review-080-090.md`
- [X] T042 Freeze `.specify/specs/092-non-disposable/coverage-baseline.txt` by redirecting `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/092-non-disposable --freeze` at the first full-tree accounting run (not the first green one) [blockedBy: T030]

**Checkpoint P1**: `declaration_reader.py --action list` loads the new fact; the owner page declares its owned
entries and carries both disposition tables; the registry row reads `Planned` with a detail file beside it; the
eight decisions are in `register.md`; `coverage-baseline.txt` exists.

---

## Phase 2: P2 — The deterministic engine

**Package**: P2 (`plan.md` § Implement Package Proposal). **Serves**: US1, US3, US5, US6, US7.
**Checkpoint**: `scripts/python/non-disposable-check.py` answers `-h`, `--help`, `--version`, rejects an undeclared
option with exit 2, scans the whole declared surface read-only, emits the coverage declaration first, and reproduces
corpus A2 and F2 on this tree.

- [ ] T043 Create the `scripts/python/non-disposable-check.py` skeleton — stdlib only, shebang, module docstring stating usage and exit codes, `from __future__ import annotations`, `main(argv=None) -> int`, `if __name__ == "__main__": sys.exit(main())`
- [ ] T044 Implement the script-interface surface in `scripts/python/non-disposable-check.py` — `-h` / `--help` / `--version` answer without acting, and the argument set is exactly `--root`, `--json`, `--scope`, `--roots`, `--emit-categories`, `--declaration`, `-h`/`--help`, `--version`, every other option exiting 2 [green: contracts/detection-engine-cli.contract.md#C-606]
- [ ] T045 Implement the three-valued exit-code surface in `scripts/python/non-disposable-check.py` (`0` = no findings over a stated non-empty surface; `1` = findings; `2` = argument/environment error) with the empty-surface prohibition [green: contracts/detection-engine-cli.contract.md#C-607]
- [ ] T046 Implement the read-through-declaration surface in `scripts/python/non-disposable-check.py` — ten roots and their order via `scripts/python/declaration_reader.py`, absent-root reporting with a reason, unregistered-sibling hint, `STR-014` for a degraded read [green: contracts/detection-engine-cli.contract.md#C-608]
- [ ] T047 Implement the zero-write guarantee in `scripts/python/non-disposable-check.py` — no repository write in any mode, and root resolution from the `.specify/scripts/python/` mirror to the parent of `.specify`
- [ ] T048 Implement `--scope` sharding in `scripts/python/non-disposable-check.py` — membership as a pure function of the sorted path list, disjoint union equal to the candidate set, no empty shard
- [ ] T049 Implement deterministic serialisation in `scripts/python/non-disposable-check.py` — entries sorted by `entry_id`, roots in declaration order, mappings sorted by key
- [ ] T050 Implement the mirror-safe projection block placement in `scripts/python/non-disposable-check.py` so `scripts/python/sync-mirrors.py` inserts exactly one projection marker before the `__main__` guard, and confirm the mirror carries it once
- [ ] T051 Implement the `status-unreadable` class in `scripts/python/non-disposable-check.py` by invoking `scripts/python/closure-acceptance-check.py --json` as a subprocess and reading `verdict` + `reasons`, carrying the checker path and the feature id in every entry's `evidence_refs` [green: contracts/status-and-verification.contract.md#C-201]
- [ ] T052 Emit the checker's verbatim reason code `status-claims-implemented-but-blocked` in `scripts/python/non-disposable-check.py`, naming the feature, and report nothing when status and verdict agree [green: contracts/status-and-verification.contract.md#C-202]
- [ ] T053 Report the **missing field names** of `verification.md` (machine-readable block, smoke fields) in `scripts/python/non-disposable-check.py`, reading the field names from the owner document [green: contracts/status-and-verification.contract.md#C-203]
- [ ] T054 Recompute a claimed closed-set identity in `scripts/python/non-disposable-check.py` and report both readings on disagreement, treating "declared but never recomputed" as its own finding [green: contracts/status-and-verification.contract.md#C-204]
- [ ] T055 Keep `scripts/python/non-disposable-check.py` free of any private reason-code table, status enum or closure ladder, and prove it by the module's own import surface [green: contracts/status-and-verification.contract.md#C-205]
- [ ] T056 Make the status reading reproducible from the entry alone in `scripts/python/non-disposable-check.py` — `evidence_refs` names the command and the feature, and the emitted state does not depend on run order or concurrency degree [green: contracts/status-and-verification.contract.md#C-206]
- [ ] T057 Make the merged `status-unreadable` emission carry every observable the contract requires — the missing field names, the recomputed closed-set readings and the checker-call identity — so no one of them is reported alone, and supply the leg that substitutes `closure-acceptance-check.py` with a stub emitting a chosen verdict (the report MUST reflect the stub, and MUST fail if the engine re-derived the verdict) [green: contracts/status-and-verification.contract.md#C-207]
- [ ] T058 Implement the eight-class judgement loop in `scripts/python/non-disposable-check.py` by reading the class set from the owner page rather than from a local literal, and emitting `unknown-class` for any class absent there
- [ ] T059 Implement the `superseded-live`, `multi-owner`, `orphan-path` and `renumber-live-binding` classes in `scripts/python/non-disposable-check.py`, each naming both sides of the defect, with one class per entry (a two-class defect is two entries, never a joined class string)
- [ ] T060 Implement the four state classes in `scripts/python/non-disposable-check.py`, including `deferral-marker`'s retention statement with no expiry condition
- [ ] T061 Implement entry evidence emission in `scripts/python/non-disposable-check.py` — `path`, `line` (1-based, `0` reserved for file-level facts), and at least one resolvable `evidence_refs` element per entry (≥ 2 for a `semantic` entry), with a duplicate `entry_id` merged and `path` normalised per `declaration_reader.normalize_path`
- [ ] T062 Implement the `multi-owner`, `orphan-path` and `renumber-live-binding` reproduction arms over the A–H corpus in `scripts/python/non-disposable-check.py`, and run the engine against the real tree to record the first coverage declaration (per-root counts, candidate total) into `.specify/specs/092-non-disposable/notes/quickstart-run.md`
- [ ] T063 Implement the per-class zero-reporting arm in `scripts/python/non-disposable-check.py` — `count: 0` accompanied by the roots searched, never an omitted class
- [ ] T064 Implement the unified `--json` and human projections of one in-memory run in `scripts/python/non-disposable-check.py` so every human-form count appears in the JSON
- [ ] T065 Implement the mandatory coverage declaration as the first block of every report (roots in declared order with presence and count, candidate total, exclusions with reasons, missing roots, unregistered siblings, declaration path and status)
- [ ] T066 Emit `unevaluated` entries and `unevaluated` shards as counted, visible states in `scripts/python/non-disposable-check.py` and include them in the not-closed totals [green: contracts/report-schema.contract.md#C-703]
- [ ] T067 Derive `closed` in `scripts/python/non-disposable-check.py` and forbid any "kept as is" / "reviewed by a human" field [green: contracts/report-schema.contract.md#C-704]
- [ ] T068 Make the four reader questions answerable from the report alone in `scripts/python/non-disposable-check.py` (what was looked at, what was found, what is proposed, what is not done) [green: contracts/report-schema.contract.md#C-705]
- [ ] T069 Generate `.specify/scripts/python/non-disposable-check.py` from `scripts/python/non-disposable-check.py` by running `python3 scripts/python/sync-mirrors.py`, and confirm the pair carries the projection marker and no new drift [green: contracts/report-schema.contract.md#C-706]
- [ ] T070 Emit a `status-unreadable` entry's verdict and reason-code spelling verbatim, plus the checker-call identity, in the machine fields of every `--json` run, asserted on the corpus A2 reading [green: contracts/report-schema.contract.md#C-707]
- [ ] T071 Verify the engine reproduces corpus A2 and `quickstart.md` § 2's two readings on this tree, recording exit codes and hit lines in `.specify/specs/092-non-disposable/notes/quickstart-run.md` [blockedBy: T062]

**Checkpoint P2**: the engine runs read-only, exits 0/1/2 meaning three different things, writes nothing, and its
coverage declaration agrees with an independent enumeration over the ten roots.

---

## Phase 3: P3 — The four-stage history seam

**Package**: P3 (`plan.md` § Implement Package Proposal). **Serves**: US1, US3.
**Checkpoint**: both seam faces name the four stages in order; review and design write nothing; a confirmation is
required before any write; unconfirmed entries are visible; evidence lands one file per run in four segments.

- [ ] T072 Add seam steps 0 / A / B to `skills/internal/manage-history/SKILL.md` naming the four stages in order — review → design（方案）→ user confirm → execute — inserted around the existing **Steps 1–6** (review as Step 0, design as Step A, confirmation as Step B, execute taking Step 6's position), leaving that list's own numbering intact [green: contracts/four-stage-command.contract.md#C-402]
- [ ] T073 Implement the zero-write reading for the review and design segments in `skills/internal/manage-history/SKILL.md` — two snapshots (`git status --porcelain=v1` full text + content hashes over the managed path set), taken before the review and after the design, required byte-identical [green: contracts/four-stage-command.contract.md#C-403]
- [ ] T074 Constrain a temporary design plan to `.specify/.tmp/` in `skills/internal/manage-history/SKILL.md`, with removal mandated by the execute segment, and prove it by a copy-tree write that stays inside that path [green: contracts/four-stage-command.contract.md#C-404]
- [ ] T075 Implement the closed three-value confirmation granularity (`group` / `item` / `none-of`, absent input resolves to `group`, no "one confirmation = execute everything") in `skills/internal/manage-history/SKILL.md` [green: contracts/four-stage-command.contract.md#C-405]
- [ ] T076 Implement the `unconfirmed` visible state in `skills/internal/manage-history/SKILL.md` — not dropped, not retried next round, not counted toward this round's closure; a partial confirmation leaves the rest visible and outside the closure count [green: contracts/four-stage-command.contract.md#C-406]
- [ ] T077 Implement the group-boundary execute ordering in `skills/internal/manage-history/SKILL.md` — start only on the confirmed set, write at group boundaries, never mid-entry [green: contracts/four-stage-command.contract.md#C-407]
- [ ] T078 Implement the four-segment evidence file contract in `skills/internal/manage-history/SKILL.md` — one file per run under `.specify/specs/<spec-dir>/test-evidence/`, segments `readings` / `paths` / `corpus` / `dispositions`, and no write to `.specify/memory/sanitize/findings.json` or `.specify/history/` [green: contracts/four-stage-command.contract.md#C-408]
- [ ] T079 Add the four-stage delegation bullet list plus the seam pointer to `templates/commands/history.md`, retaining the existing distill capability and incremental manifest [green: contracts/four-stage-command.contract.md#C-409]
- [ ] T155 In the execute segment of `skills/internal/manage-history/SKILL.md`, handle the archive disposition as `git mv` semantics with the source → archive mapping recorded, keeping the superseded text and showing a rename pair rather than a deletion [green: contracts/renumber-and-supersede.contract.md#C-507]
- [ ] T080 Regenerate the per-tool command copies from `templates/commands/history.md` with `python3 scripts/python/regen-command-copies.py`, then confirm `pytest -m contract tests/contract/test_docs_command_template.py::test_c10_runtime_copies_exist_for_every_present_tool` is green [blockedBy: T079]
- [ ] T081 Generate `.specify/skills/internal/manage-history/SKILL.md` from its source by running `python3 scripts/python/sync-mirrors.py`, confirm the pair is byte-identical, and register the two edited frozen sources in `tests/contract/test_expression_compatibility.py`'s `ALLOWED_POST_BASELINE_CHANGES` with markers **added by this change** and a reason naming Feature 092 [blockedBy: T072,T079]
- [ ] T082 Run the `quickstart.md` § 8 seam walk against a copy tree and record the two snapshots' byte comparison, the confirmation reading and the four evidence segments in `.specify/specs/092-non-disposable/notes/quickstart-run.md` [blockedBy: T080]

**Checkpoint P3**: deleting the seam from either face makes the P5 guard go red; on a copy tree, review and design
leave `git status --porcelain` byte-identical, and execute writes only after a confirmation.
- [ ] T156 Add the seam-bypass leg to `tests/contract/test_non_disposable_contract.py` and to the owner page's statement of the rule — an execute run touching a path that no confirmed design row names is red, and a confirmed-row path is green; the before/after readings are required on every edit the seam makes [green: contracts/four-stage-command.contract.md#C-410]

---

## Phase 4: P4 — The three pointer faces

**Package**: P4 (`plan.md` § Implement Package Proposal). **Serves**: US1, US2.
**Checkpoint**: one pointer line lands inside an existing `##` section of the template; the live instructions are
regenerated within budget; the compatibility files are still symlinks; no count pin moves.

- [ ] T083 Append exactly one pointer line into an existing `##` section of `templates/instructions-template.md`, adding no top-level section and no restated owner criterion
- [ ] T084 Regenerate `.specify/instructions.md` by running `scripts/bash/generate-instructions.sh`, then confirm `wc -c .specify/instructions.md` is within `INSTRUCTIONS_BUDGET_BYTES` and that `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md` are still symlinks [blockedBy: T083]
- [ ] T085 Run `pytest -m contract tests/contract/test_fast_fail_discipline.py` and confirm the top-level `##` count pin is unmoved after the regeneration [blockedBy: T084]

**Checkpoint P4**: the instructions face points at the owner page without a second definition of it, and no count
pin moves.

---

## Phase 5: P5 — The contract guard

**Package**: P5 (`plan.md` § Implement Package Proposal). **Serves**: US1–US7 (every closed set becomes falsifiable).
**Checkpoint**: the guard is green, every closed set has a mutation leg, and substituting the closure checker with a
stub makes the `status-unreadable` leg fail.

- [ ] T086 Create the contract-test group files under `tests/contract/` (`test_non_disposable_contract.py` plus one file per later clause group, so clause groups can be authored in parallel) with each file's fixture data stated in itself — the seven-face existence legs and the `deferral-marker` fixture tree
- [ ] T087 Add the mutation-leg harness to `tests/contract/test_non_disposable_contract.py` — one defect-creating copy-tree edit per class, asserting red with the expected path:line, plus the inverse asserting green
- [ ] T088 Add the engine CLI legs to `tests/contract/test_non_disposable_contract.py` — `-h`/`--help`/`--version` answer without acting and an undeclared option exits 2; every declared option is accepted and no other one is exposed
- [ ] T089 Add the read-only leg to `tests/contract/test_non_disposable_contract.py` — a `git status --porcelain` comparison around a full run is byte-identical, with a mutation leg that touches a tracked path and asserts red
- [ ] T090 Add the empty-surface, unknown-option and declaration-surface legs to `tests/contract/test_non_disposable_contract.py` — the empty candidate set is never `closed: true`, a missing declaration exits 2 naming the path, an invalid key exits 2 naming the key, an absent root is reported and excluded with a reason, and an undeclared sibling only hints
- [ ] T091 Add the sharding leg to `tests/contract/test_non_disposable_contract.py` — shards are disjoint, their union equals the candidate set, and a mutation leg duplicates one path across two scopes and asserts red
- [ ] T092 Add the determinism and projection legs to `tests/contract/test_non_disposable_contract.py` — two runs on one tree produce byte-identical `--json` after the run identifier is removed, and the `_bridge_*` block sits before the `__main__` guard
- [ ] T093 Add the disposition-set and "do nothing is not a disposition" legs to `tests/contract/test_non_disposable_contract.py`, reading the four member spellings through the owner page and asserting red when a mutation leg injects `"keep"` into a report
- [ ] T094 Add the exemption-field and expiry-evaluation legs to `tests/contract/test_non_disposable_contract.py` — each of the four fields removed in turn names the missing member, an unevaluable `on-condition` predicate lands `unevaluated`, and a passed `expiry_recheck` re-opens the entry
- [ ] T095 Add the bridge-exhaustiveness leg to `tests/contract/test_non_disposable_contract.py`, computing the expected pair count from the two sets' lengths at test time and failing on a duplicate pair
- [ ] T096 Add the prohibition and adjudication legs to `tests/contract/test_non_disposable_contract.py` — both explicit prohibitions are stated in the owner page, no bridge row contradicts them, and the adjudication rule appears exactly once
- [ ] T097 Add the pathway and archive leg to `tests/contract/test_non_disposable_contract.py` — every `archive` record carries `moved`, `irreversible` appears only where the router says so, and a wrong archive landing face is reported as a finding
- [ ] T098 Add the three-recovery leg to `tests/contract/test_non_disposable_contract.py` — a body, a guard and an evidence path recovered together are green, and two of three is red
- [ ] T099 Add the per-landing-face mutation legs to `tests/contract/test_non_disposable_contract.py` — body / guard / evidence path each asserting red on a copy tree and green after synchronised recovery
- [ ] T100 Add the supersede-registry leg to `tests/contract/test_non_disposable_contract.py` — a supersede traced only in a commit message or session record fails
- [ ] T101 Add the live-binding leg to `tests/contract/test_non_disposable_contract.py` — each of the four shapes reported red with file and line
- [ ] T102 Add the history-record leg to `tests/contract/test_non_disposable_contract.py` — an old number inside the predicate face is green, and a rewritten history record is red
- [ ] T103 Add the single-predicate leg to `tests/contract/test_non_disposable_contract.py` — the engine carries no duplicate of the four predicate literals, and a mutation leg edits the predicate module and expects the classification to move with it
- [ ] T104 Add the entry-field leg to `tests/contract/test_non_disposable_contract.py` — a duplicate `entry_id` is merged, `path` is normalised per `declaration_reader.normalize_path`, `line` is 1-based, and a `semantic` entry carries at least two evidence refs
- [ ] T105 Add the two-projection and coverage-declaration legs to `tests/contract/test_non_disposable_contract.py` — every human-form count appears in the parsed JSON, and a findings-bearing report without a declaration is invalid
- [ ] T106 Add the unevaluated-count leg to `tests/contract/test_non_disposable_contract.py` — an unparseable deterministic input and a malformed semantic shard each grow the not-closed total
- [ ] T107 Add the no-unprovable-closure leg to `tests/contract/test_non_disposable_contract.py` — a mutation leg writes `closed: true` over an open entry and asserts red
- [ ] T108 Add the four-reader-questions leg to `tests/contract/test_non_disposable_contract.py` — each answer is derivable from the report and the design face invents no fifth form
- [ ] T109 Add the mirror-generation leg to `tests/contract/test_non_disposable_contract.py` — the generated mirror carries the projection marker exactly once and the pair shows no drift
- [ ] T110 Add the vocabulary-quoting leg to `tests/contract/test_non_disposable_contract.py` — a status finding carries the verdict and the reason-code spelling verbatim plus the checker-call identity, and the consumption legs assert that substituting `closure-acceptance-check.py` with a stub returning a chosen verdict makes the report reflect the stub, that `status-claims-implemented-but-blocked` is emitted with the checker's spelling while an agreeing feature is not reported, that a missing machine-readable field is named rather than called "unreadable", that both closed-set readings are reported on disagreement, that no literal reason-code table exists in the engine module, that the evidence refs reproduce the verdict in one command, and that a concurrent run gives the same status reading
- [ ] T111 Add the four-stage ordering leg to `tests/contract/test_non_disposable_contract.py` — both faces name the stages in order, and a mutation leg deletes one stage name from one file and asserts red
- [ ] T112 Add the zero-write leg to `tests/contract/test_non_disposable_contract.py` — the two snapshots around review and design are byte-identical
- [ ] T113 Add the temporary-plan leg to `tests/contract/test_non_disposable_contract.py` — a mutation leg writes the design plan to a tracked path and asserts red
- [ ] T114 Add the confirmation-granularity and unconfirmed-visibility legs to `tests/contract/test_non_disposable_contract.py` — three values with `group` as the default and no fourth value, and a partial confirmation leaves the rest visible as `unconfirmed` and outside the closure count
- [ ] T115 Add the group-boundary and non-bypass legs to `tests/contract/test_non_disposable_contract.py` — a one-group confirmation touches no path outside that group, the mutation leg touches one and asserts red, and a path outside the confirmed design rows touched by an execute run is a violation
- [ ] T116 Add the evidence-shape and preservation legs to `tests/contract/test_non_disposable_contract.py` — one file per run in the spec's `test-evidence/`, all four segments present, the distill capability and incremental manifest still present, and `.specify/history/` stays read-only to this feature
- [ ] T117 Add the archive-is-a-move leg to `tests/contract/test_non_disposable_contract.py` — `git status --porcelain` after a repair run shows a rename pair and never a deletion
- [ ] T118 Add the four-closed-set immutability leg to `tests/contract/test_non_disposable_contract.py` — `sanitize-utils.py`'s `CATEGORIES` / `DISPOSITIONS` / `STATES` / `DETECTIONS` are byte-unchanged, and both constitution count pins are unmoved

**Checkpoint P5**: `pytest -m contract tests/contract/test_non_disposable_contract.py` is green, and each mutation
leg was observed to go red when its subject was broken.

---

## Phase 6: P6 — 档 I first-round repair

**Package**: P6 (`plan.md` § Implement Package Proposal; the tier rows are `plan.md` § A–H Corpus Mapping).
**Serves**: US4, US6, US7, US9. **Checkpoint**: all 19 档 I entries reach name-level zero on a second engine reading,
each with a four-segment evidence file; no 档 II body appears in this feature's diff.

**Carrier boundary**: these rows write bodies owned by other feature lines (080, 084–090). `team/092-non-disposable/team.md`
lists those spec trees under `forbidden`; the row is legal only as the corpus repair `plan.md` § A–H Corpus Mapping
assigns to 档 I, and every edit is a **record completion or a marker**, never a redesign (see § Adjudications 9).

- [ ] T119 Record the **before** engine reading for the 档 I scope in `.specify/specs/092-non-disposable/test-evidence/repair-corpus.md` (`--json`, exit code, per-class counts) as the first evidence segment [blockedBy: T086]
- [ ] T120 Repair A1 by completing `.specify/specs/089-script-interface-contract/verification.md` with the machine-readable per-criterion block and smoke fields, and reconciling its registry row against `closure-acceptance-check.py`'s verdict — the record's fields, not its conclusions, are what change
- [ ] T121 Repair A2 by completing `.specify/specs/084-harness-triple-structure/verification.md` so its `unclassified` claim is taken from `harness-triple-check.py --action verify` rather than asserted
- [ ] T122 Repair A3 by moving 090's registry row in `.specify/memory/features.md` from `Planned` to its closure-consistent value (closure verdict `accept`, 4/4 SC) [blockedBy: T038]
- [ ] T123 Repair A4 by completing the structural record of `.specify/specs/089-script-interface-contract/tasks.md` so its non-story-phase user-story labels and its status block agree
- [ ] T124 Repair A5 by completing the decision-tension records of `.specify/specs/085-sdd-temporary-goal-team/plan.md` to the owner's six-field form [green: contracts/acceptance-readability.contract.md#C-806]
- [ ] T125 Repair A6 by adding the post-081 common schema fields (`**Path**:` markers, `smoke_command`) to `.specify/specs/080-humanize-run-output/requirements.md` as a record completion [green: contracts/acceptance-readability.contract.md#C-807]
- [ ] T126 Repair B1 by marking `C-016` in `.specify/specs/086-efficient-test-execution/contracts/runner-contract-086.contract.md` superseded with a pointer to the 089 mirror-projection contract, keeping the old text, and retiring or replacing the `byte_identical` guard in `tests/contract/test_run_tests_runner_contract.py` in the same change
- [ ] T127 Repair B2 by following the owner in `.specify/specs/085-sdd-temporary-goal-team/contracts/temporary-goal-team.md` — its **C-007** (the team path form `.specify/specs/<NNN-slug>/team/team.md`) and **C-008** (creation timing), not a paraphrased copy — and in `contracts/checkpoint-and-agents.md`'s **C-001** (the four-part checkpoint) — with markers and pointers, old text retained
- [ ] T128 Repair B3 by marking `.specify/specs/067-*/contracts/runner-contract.md` "Serial is the default" superseded by 086's parallel default (marker + pointer, old text retained)
- [ ] T129 Repair B4 by re-pointing the evidence path in `.specify/specs/088-*/efficiency-model.md` § evidence-path to the owner spelling that exists, retaining the original text inside the disposition record
- [ ] T130 Repair B5 by choosing one owner spelling for the two-slot evidence path and adding pointer rows for the other two spellings in the same disposition record
- [ ] T131 Repair C1 by correcting the live bindings in `.specify/specs/089-script-interface-contract/requirements.md` (Feature ID), `089/tasks.md` (headers) and `089/feature-ref.md` (its binding lines) to 089
- [ ] T132 Repair C2 by correcting the live instruction in `.specify/specs/089-script-interface-contract/tasks.md` so it names the 089 registry row and `features/089.md`, and by renaming `.specify/specs/089-script-interface-contract/team/086-script-interface-contract/` to the 089 slug with `git mv` semantics, correcting its `name:` line [blockedBy: T131]
- [ ] T133 Repair C4 by correcting 088's eight contract headers, its main team name and its dogfood slug to 088
- [ ] T134 Repair G1 by adding the goal-first mutation leg to `tests/contract/test_sdd_loop_driver_reanchor.py` (asserting red when the ordering is broken)
- [ ] T135 Repair G2 by replacing the tautological `first_no` assertion in `tests/contract/test_sdd_loop_driver_reanchor.py` with an assertion that reads the actual first item
- [ ] T136 Repair G3 by completing `RULE_SET` in `tests/contract/test_sdd_loop_driver_reanchor.py` against the owner's rule anchor so deleting a rule member turns it red
- [ ] T137 Record the **after** engine reading over the same scope in `.specify/specs/092-non-disposable/test-evidence/repair-corpus.md`, with the changed-path list (`git diff --name-only` scope), the corpus entry ids and one disposition record per entry — the four segments of E-7 [blockedBy: T119]
- [ ] T138 Confirm that no 档 II receiving body (D1–D6, E1–E6, F1–F5, H1–H2) appears in the changed-path list of this feature's diff, and record that reading beside the evidence file [blockedBy: T137]

**Checkpoint P6**: the second reading shows 档 I at zero by name; each repaired entry's evidence file carries the
four segments; RK-5's check (no 档 II body touched) reads clean.

---

## Phase 7: P7 — 档 II detection and the shift list

**Package**: P7 (`plan.md` § Implement Package Proposal). **Serves**: US5, US9.
**Checkpoint**: the 15 档 II entries are detected, each receiving body carries exactly one handoff marker, and the
"zero" statistic excludes 档 II by construction.

- [ ] T139 Run the engine's `multi-owner` class over the D-row carriers (081, 084, 088, 090 and the 082/083 owners) and record the detection readings in `.specify/specs/092-non-disposable/test-evidence/shift-092.md` [blockedBy: T059]
- [ ] T140 Run the engine's `false-closed-set` class over the E-row carriers (083, 089, 084, 087) and append the readings to `.specify/specs/092-non-disposable/test-evidence/shift-092.md`
- [ ] T141 Run the engine's `stale-constant` class over the F-row carriers (the ceiling owner, `scripts/bash/generate-instructions.sh`, the copying plans, the registry, 083) and append the readings to `.specify/specs/092-non-disposable/test-evidence/shift-092.md`
- [ ] T142 Run the engine's `orphan-path` class over the H-row carriers (086's mirror spelling, 082's session file, 085's GATE-1 path) and confirm `.specify/.tmp/086-*` (H3) produces no entry as a recorded exclusion, appending the reading to `.specify/specs/092-non-disposable/test-evidence/shift-092.md`
- [ ] T143 Declare the 12 Shift List rows in the owner page § Handoff Rows (`plan.md` § Shift List face) as pointer-shaped rows naming corpus id → receiving feature → landing face, so the marker form has a single owner
- [ ] T144 Land one handoff marker line per receiving body of `plan.md` § Shift List (12 rows, the `<!-- 092 handoff: <corpus id> → <receiving feature> -->` form, placed where the defect is) and change nothing else in those bodies [blockedBy: T143]
- [ ] T145 Confirm the shift list carries one row per 档 II entry (15) and that the feature's own zero statistic counts 档 I only, recording both readings in `.specify/specs/092-non-disposable/test-evidence/shift-092.md` [blockedBy: T144]
- [ ] T146 Record the two-way coverage reading FR-056 requires in `.specify/specs/092-non-disposable/test-evidence/shift-092.md` — every corpus group has a carrier, and `deferral-marker` plus FR-023's rewrite limb are proven by construction rather than by a corpus row

**Checkpoint P7**: each 档 II receiving body carries exactly one marker, the receiving lines' owners are named, and
the feature's reported zero excludes 档 II.

---

## Phase 8: P8 — Stage verification and closure

**Package**: P8 (`plan.md` § Implement Package Proposal). **Serves**: all stories.
**Checkpoint**: the closure run, the evidence index, `verification.md` and the gate readings all exist and agree; no
`[ ]` row remains; the status flip is the closure engine's verdict, not this file's claim.

- [ ] T147 Write `.specify/specs/092-non-disposable/verification.md` from `.specify/templates/verification-log-template.md` — one status row per success criterion (20), the smoke record, `deferred_tasks=`, and the engine reading behind each row
- [ ] T148 Run the stage gates and paste the raw output into `.specify/specs/092-non-disposable/test-evidence/tasks-gates.txt` — `validate-tasks.py`, `decomposition-check.py --mode tasks`, `account-clause-coverage.py --spec-dir`, and `pytest -m contract tests/contract/test_non_disposable_contract.py`
- [ ] T149 Run the mirror verification and paste it into `.specify/specs/092-non-disposable/test-evidence/tasks-gates.txt` — `python3 scripts/python/sync-mirrors.py --check`, the `diff -q` readings for every byte-equal pair in `plan.md` § Mirror Obligations, and the `regen-command-copies.py` re-run result
- [ ] T150 Run `closure-acceptance-check.py --spec-dir .specify/specs/092-non-disposable` and record its `verdict` and `reasons` verbatim in `verification.md`; the registry status flip is written only on `accept`
- [ ] T151 Flip the 092 row of `.specify/memory/features.md` per the closure verdict and re-read the `Total Features` header in the same pass, appending a `(deferred: …)` suffix only if a `[~]` row exists [blockedBy: T147]
- [ ] T152 Update `.specify/memory/features/092.md` § Latest Review and § Key Changes with this run's measured outcome [blockedBy: T151]
- [ ] T153 Index the run's evidence files in `.specify/specs/092-non-disposable/test-evidence/INDEX.md` (one line per file, its producer row and its reading date)
- [ ] T154 Register the run's own durable identifiers (any finding `F-…`, open item `OI-…`, recommendation `REC-…` coined after this stage, plus the `F-1 (092)` row for the post-freeze clause delta) in `.specify/memory/register.md`, in the pointer shape

**Checkpoint P8**: zero open rows remain, the closure verdict is recorded verbatim, and every gate reading is on
disk with the command that produced it.

---

## Green Partition

Every one of the 62 contract clauses is claimed by exactly one row, and the partition is cut so that no contract's
clause order runs backwards against the row order (owner: `.specify/templates/tasks-template.md` § Format; machine
criterion: `validate-tasks.py`'s four green-* checks).

| Contract (clauses) | Claiming rows | Clauses |
|---|---|---|
| `detection-categories` (8) | T001–T005 (owner page § Detection Categories), T011–T013 | C-101 … C-108 |
| `disposition` (8) | T014–T021 (owner page § Disposition Set and § Disposal Pathways) | C-301 … C-308 |
| `renumber-and-supersede` (7) | T022–T027 (owner page § Supersede Protocol and § Renumber-Face), T155 (archive-as-move seam row) | C-501 … C-507 |
| `detection-engine-cli` (8) | T030–T034 (fact + owner-page § Engine Contract), T044–T046 (engine) | C-601 … C-608 |
| `status-and-verification` (7) | T051–T057 (engine status class) | C-201 … C-207 |
| `four-stage-command` (10) | T036 (capture rule), T072–T079 (seam), T156 (seam-bypass guard) | C-401 … C-410 |
| `report-schema` (7) | T028–T029 (owner page § Report Entry / § Report Envelope), T066–T070 | C-701 … C-707 |
| `acceptance-readability` (7) | T001–T005 (owner page § Status Readability — objects, contradiction table, cell proofs, the `**Path**:` mark, the 档 II marker), T124 (process-grade FRs), T125 (owner-page landing obligations) | C-801 … C-807 |

A contract's clauses are claimed in ascending order along the row order, which the `green-cross-phase` check reads:
that is why `acceptance-readability`'s five owner-page rows sit in P1 (`T001`–`T005`) while its last two sit on the
P6 rows that realise their obligation — a partition whose clause order ran backwards could not leave its contract green
at its own phase.

**Why the cut runs this way.** A `[green:]` row asserts "this row is what turns that clause green". For an
authoring obligation the row that writes the owned text is that row, so the owner-page contracts are claimed
where the text lands (P1), and the P5 guard rows re-read those clauses in prose without claiming them. For the two
contracts whose subject is a running program (`detection-engine-cli`, `status-and-verification`) and for
`report-schema` the green point sits on the engine row; the guard re-reads them. `four-stage-command` C-401 is the
capture rule and the rest are the seam; `renumber-and-supersede` C-507 is the archive landing face.

Rows T035, T037–T043, T047–T050, T058–T065, T071, T080–T123 and T126–T155, plus every `DoD` / `GATE` item, carry **no** claim: a second claim on one clause would be a
`green-clause-collision`, and a mirror generation, a corpus repair, an evidence index or a gate reading is not a
clause's green point.

## Dependencies & Execution Order

### Phase Dependencies

- **P1 (Phase 1)**: no dependency — starts immediately
- **P2 (Phase 2)**: depends on P1 — the engine reads the declaration fact and the owner page
- **P3 (Phase 3)**: depends on P1 and P2 — the seam cites the disposition vocabulary and the engine's report
- **P4 (Phase 4)**: depends on P3 — a pointer must point at something that exists
- **P5 (Phase 5)**: depends on P1–P4 — the guard guards faces that must exist
- **P6 (Phase 6)**: depends on P2, P3, P5 — the repair evidence is read against a working engine and a red-able guard
- **P7 (Phase 7)**: depends on P2 and P5 for detection; runs **concurrently with P6** — the only real parallelism inside the implement stage, and no two write packages share a path
- **P8 (Phase 8)**: last — a closure run over every other package

### Within Each Phase

- Owner-page authoring precedes every engine row that reads it
- Engine rows precede their guard rows (a mutation leg needs a subject)
- Mirror generation and command-copy regeneration follow the source edit, never precede it
- Repair rows land before the "after" reading; the "after" reading lands before the zero confirmation

### Parallel Opportunities

- The package chain P1 → P2 → P3 → P4 → P5 is serial by construction (`plan.md` § Serialization), so most
  parallelism sits **inside** a package: owner-page sections, engine class implementations, guard legs
- P6 and P7 run as two lanes once P5 is green
- The repaired bodies in P6 are separate files owned by separate feature lines: T120–T136 write disjoint paths and
  can be staffed to different executors once T119 is recorded

## Implementation Strategy

### MVP First

**MVP scope rule**: the smallest same-priority story set whose checkpoints are independently testable. The P1
stories are US1 (a report of expired carriers), US2 (every judged entry must be disposed), US3 (design before
execute), US4 (supersede recovers every landing face), US7 (status/verification readable) and US9 (the repair lane
drives the corpus to zero). An owner page without the engine is half a mechanism, and an engine without the seam
gives a report nobody can act on — so the MVP is **P1 + P2 + P3 + P4 + P5**: every P1 story through its guard. P6 and
P7 deliver US9 against the real corpus; P8 closes the line.

1. Complete P1 → `declaration_reader.py` loads the fact; the registry says `Planned`
2. Complete P2 → the engine reproduces corpus A2 and F2 on this tree, read-only
3. Complete P3 + P4 → the seam exists inside the one history entry, and the pointer faces point at it
4. Complete P5 → every closed set is falsifiable
5. **STOP and VALIDATE**: run each P1 story's checkpoint independently before starting the repair lane

### Incremental Delivery

1. P1 + P2 → a report with a coverage declaration and reproducible findings (first demonstrable value)
2. P3 + P4 → the four-stage seam inside `/speckit.history`, with a zero-write review and design
3. P5 → the mechanism becomes guardable
4. P6 + P7 → the corpus is reproduced, 档 I driven to zero, 档 II handed off
5. P8 → the closure verdict and the evidence index

### Parallel Team Strategy

The line's team (`team/092-non-disposable/team.md`) declares `stage_seats.implement.max_parallel: 8`. At that
capacity: one executor owns P1's owner page, one the declaration fact plus registration, two split P2's engine
classes, two split P5's guard legs, and P6 / P7 run as two lanes once P5 is green. No two executors write one path —
the package territory in `plan.md` § Implement Package Proposal is the partition.

---

## Notes

- `[P]` = different files, no dependency; the write-alone rule of the package territory is what makes it true
- `[green:]` is the clause's single green point — never delete a tag to silence a warning
- Each mutation leg MUST be observed going red before its green counts as evidence
- Evidence lands one file per run in `.specify/specs/092-non-disposable/test-evidence/` (Concurrent Development Safety)
- Deferral discipline: prefer `[~]` with a recorded reason over leaving a row `[ ]` for now
- 档 II bodies are read-only to this feature; a repair there belongs to the receiving line (FR-056 / FR-045)

## Adjudications and assumptions (recorded at generation time)

1. **`[green:]` tag spelling.** The generation brief writes the tag in bracket form. `validate-tasks.py` parses that
   exact form; the boilerplate line in `.specify/templates/tasks-template.md` § Format renders it as two backticked
   fragments inside a Markdown table cell, so a tag copied verbatim from that table is a *mention*, not a
   declaration. The validator's executable form is authoritative here.
2. **One row, one clause.** Every clause is claimed by exactly one row. Where a clause needs both an authoring
   surface and a guard, the row that writes the surface claims it and the guard row names the clause in prose only.
3. **The first generated file is deleted, not repaired.** The first version of this file claimed several clauses
   twice (owner page and guard) and carried 166 task rows, over `decomposition-check.py`'s 160 ceiling. Both were
   generation defects, not scope facts: the cut below keeps every work item and merges rows that described one
   artifact's two facets, landing at 149 rows.
4. **Owner-page clauses are claimed by their authoring row**, engine clauses by the engine row, and guard clauses
   (C-105, C-106, C-206, C-207, C-505) by the guard row that is their only green point.
5. **`features.md` status.** `plan.md` § Landing Checklist row 4 says the registry row lands at `Planned`, while the
   feature-integration owner (`shared/workflow/feature-integration.md` § Status State Machine) assigns
   `Draft → Planned` to `/speckit.plan` and only *maintenance* to `/speckit.tasks`. 092 has no row at all today, so
   T038 creates it at `Planned` — the two statements agree once the row exists. Recorded because a reader comparing
   the two files would otherwise read a conflict.
6. **`Total Features` header.** The index is hand-maintained, so header and rows are edited in one pass
   (`shared/workflow/feature-integration.md`); T038 and T151 re-read the header beside the row they touch and this
   file does not restate the number.
7. **`D-1`…`D-8` registration.** `plan.md` § ID Register Duty carries the eight rows as a deferred obligation; T040
   is the row of this stage that performs it, because the brief names `register.md` as one of the two登记 writes the
   tasks stage is allowed and `requirements.md` § Clarifications already holds the full statements. T154 registers
   only identifiers a later run coins.
8. **`decomposition-check.py` location.** The gate lives at `skills/external/sdd-loop-driver/scripts/`, not under
   `scripts/python/`; T148 names the path that exists.
9. **Territory vs. repair carrier.** `team/092-non-disposable/team.md` lists `.specify/specs/{085…090}-**` under
   `forbidden`, while `plan.md` § A–H Corpus Mapping assigns 19 档 I entries to this feature's P6. The two are
   reconcilable only if the forbidden list is read as "no redesign of another line's design artifacts" and the 档 I
   rows as "record completion and markers the corpus repair owns". This file follows the plan's assignment, keeps
   every repair to a record field or a marker, and discloses the tension rather than resolving it here.
10. **`D-1`…`D-8` vs. the corpus rows.** The eight clarify decisions are decisions, not findings; they carry no
    `F-`/`OI-` id and are registered in the shape the table's `D-…` rows already use.

- [ ] T157 Migrate the sibling spec-local teams that still nest the default team under its own spec slug (`085/086/087/089`) to `team/team.md`, keeping named extra teams under `team/<team-slug>/team.md`; re-run `goal-utils.py run-checks` per spec and record the before/after paths in `test-evidence/team-path-migration.txt` (the engine now resolves the default file first, so the migration is a rename, not a behavioural change).
