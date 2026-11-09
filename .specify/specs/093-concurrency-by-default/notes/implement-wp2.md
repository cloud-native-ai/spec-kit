# Implement — WP2-engine (feature 093-concurrency-by-default)

**Package**: `WP2-engine` (`tasks.md` § Work Packages) — rows **T021–T025, T030–T033, T051–T056,
T074–T077, T095–T097, T109, T113, T119, T138** (26 rows).
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-wp2`, branch `093-wp2`, based on `7ec5cc05`.
**Date**: 2026-11-09. **Mode**: one detached fork executor, serial, no subagents, no push.
**Test entry**: `bash scripts/bash/run-tests.sh <paths> -q` only (FR-036; xdist default).

**Outcome**: **25 of 26 rows closed; T025 closes one of its two gates** — its `script-interface-check`
half is green, and its `pytest tests/unit/test_concurrency_check_engine.py -q` collect half cannot
close in this isolated worktree because that module is **WP4's deliverable** (`tests/unit/…`, rows
T015/T136). Recorded as the row's open half, not fabricated green.

## Commits (oldest first)

| Commit | Rows | Subject |
|---|---|---|
| `27ef0433` | T021–T025 | the engine skeleton: interface, five-action dispatch, repo resolution, envelope |
| `51ab545e` | T030–T033 | classify: five-root enumeration, class resolution, obligation read, measured block |
| `e557ce2b` | T051–T056 | serial-reason: closed-vocabulary validation, evidence forms, bijection, envelope wiring |
| `2c47774d` | T074–T077 | reading: interval-overlap, not_evaluated tri-state, tri-field judgement, bound recomputation |
| `e0c58d34` | T095–T097 | capability: three-way test, coordinator verdict fail-closed, mismatch detail fields |
| `767776f8` | T109 + T113 + T119 | block-subset record read, coverage action, goal-target partition under the slot cap |
| `aac8834e` | T138 | validate-tasks `[green:]` marker reading, its contract test, and the F-093-015 pointer repair |
| _(this commit)_ | wrap-up | this record + the final smoke evidence |

## Per-row closure

| Row | Status | Evidence / reading |
|---|---|---|
| T021 | closed | C-019 green — `--help` exit 0 with the four labels, `--version` exit 0, `--bogus-opt` exit 2 before any action (`wp2-t021-t025.txt`) |
| T022 | closed | C-020 green — the `--help` positional block lists exactly `{classify,serial-reason,reading,coverage,capability}`; a sixth action exits 2; every action reaches its dispatch |
| T023 | closed | C-021 green — `default_repo()` = the worktree root on this branch (literal `scripts/python` component, `.specify` stripped only when directly above `scripts/`); no ancestor walk; `--record` on a non-record action exits 2; a record-judging action without `--record` exits 2 |
| T024 | closed | C-022 green — envelope keys `action/checked_at/decision/findings/measured`; every finding carries `code`+`subject`; `checked_at` ISO-8601 UTC |
| T025 | **partially closed** | `script-interface-check.py --files …` → `candidates=1 applicable=1 exempt=1 violations=0`, exit 0. Collect half: `tests/unit/test_concurrency_check_engine.py` is WP4's (T015/T136), absent in this worktree; the row's literal positional form exits 2 (`--files` is the declared selector, WP1 correction) |
| T030 | closed | C-023 green — 118 bodies across the five roots measured live: skills 54 (internal 38 + external 16), commands 29, agents 17, teams 12, anchoring 6; counts reported as measured, never compared to a stored copy; zero root/class literals in the engine |
| T031 | closed | C-024 green — live tree: 0 `uncovered`, 0 `ambiguous`, 0 `class-disagreement`; fixtures: a root with no rule row → `uncovered`, two same-shape rows → `ambiguous`, both fail (`wp2-t030-t033.txt`) |
| T032 | closed | C-025 mechanism green on fixtures (`body-text` / `owner-anchor` / `both` / `none` reported distinctly; `none` → `obligation-missing`). Live tree: 107 `obligation-missing` — the truthful pre-WP3 reading (T034–T036 author the anchors, T040 places the pointers) |
| T033 | closed | measured carries per-root `member_count`/`by_base`/`member_ids` and per-body class/obligation detail, all derived from the enumeration |
| T051 | closed | every code drawn from the fact's closed set, duplicates refused, declared order enforced, and the count reported as `codes_declared` — never as concurrency (`wp2-t051-t056.txt`) |
| T052 | closed | per-code evidence forms judged (dependency-edge / write-conflict / host-probe / budget-readings / unit-set); a bare string (including `.`) rejected for every code |
| T053 | closed | `code-unknown` (and `code-duplicate`) name the offending string; the finding is tagged `kind: inconsistency` |
| T054 | closed | simplicity/speed/cleanliness in the code list or a reason-like field → `prose-reason-not-a-code` with the closed vocabulary named |
| T055 | closed | one finding per offending code; each names the record code, its FR-005 condition (when condition-bound) and an evidence pointer into the record |
| T056 | closed | condition↔code bijection both ways; a mutated fact fixture yields `bijection-gap` naming both sides; the live fact is zero-gap |
| T074 | closed | C-031 green — max interval overlap: `[100,140) [120,180) [130,150)` → 3; touching intervals `[100,140) [140,180)` → 1 (settle-before-dispatch tie-break); integer only (`wp2-t074-t077.txt`) |
| T075 | closed | C-032 green — a missing interval yields the literal `not_evaluated` and names the unit; a concurrency claim then fails, a serial claim may pass |
| T076 | closed | C-033 green — any absent triple member → `reading-incomplete`; an `effective` below `min(...)` with an empty reason is also `reading-incomplete` |
| T077 | closed | C-034 green — bound recomputed from the slot fact + `wp-gate.py`'s declared `--slot-cap-ceiling` default (4) minus the verifier reserve (1) → available 3; `--ceiling 6` override reported as its own source; the engine carries no numeric ceiling |
| T095 | closed | C-037 green on a verdict-bearing fixture — `dispatch-capable` / `handoff-declared` / `external-process` / `incapable` all classified from the existing `capability-tools` key only; no new frontmatter key (C-038) |
| T096 | closed | C-039 green — live tree (`decision_state: unadjudicated`) → `owner-unavailable`, exit 2, no default; the absent-fact fixture does the same; a readable verdict is reported verbatim |
| T097 | closed | mismatch findings carry `kind: inconsistency`, `compared` (both statements) and `record`; the envelope carries `verdict` (verbatim when adjudicated, null otherwise); both C-040 forms judged |
| T109 | closed | records are parsed by `declaration_reader.parse_subset`: a JSON record and an anchored YAML record both exit 2 `record-outside-subset` (`wp2-t109-t113-t119.txt`) |
| T113 | closed | C-063 green — goal targets partitioned into packages bounded by `min(slot_cap, ceiling) − verifier_reserve` (ceiling 4 → available 3 → 5 open targets = `[3,2]`); < 2 → serial with the code named in the slot fact's `degradation_rule`; a one-target goal is not partitioned |
| T119 | closed | C-035/C-036 green — all 8 stages resolve from the fact (`analyze` = `on` with its `concurrency_source`; the rest `auto`/covered-by-default); an unknown stage and an `off` stage without a named decision both `coverage-undeclared`; the fact↔spine relation is reported per spine; a competing authored rule → `fourth-source`, fail |
| T138 | closed | marker reading on three surfaces (rule block, emitted message, `--help`), totality phrasings absent, behaviour preserved (subset passes / double claim warns as marker / dangling errors), 093's own partition 37 claims / 0 double / 0 dangling, mirror byte-identical, dead F-093-015 pointer re-pointed; red 4 failed → green 9 passed, neighbour suite 16 passed (`wp2-t138.txt`) |

## Test readings (red-first where a `[green:]` row declares it)

- **T021–T024 (C-019…C-022)**: red = engine absent (exit 2 file-not-found; `candidate-not-collected`)
  → green = interface probes in `wp2-t021-t025.txt`.
- **T030–T033 (C-023…C-025)**: red = stub `not-implemented` (exit 1) → green = live enumeration +
  three mutation fixtures (`wp2-t030-t033.txt`).
- **T051–T056 (C-027…C-030)**: red = stub → green = a 13-record matrix exercising every branch
  (`wp2-t051-t056.txt`).
- **T074–T077 (C-031…C-034)**: red = stub → green = a 9-record matrix + bound arithmetic
  (`wp2-t074-t077.txt`).
- **T095–T097 (C-037…C-040)**: red = stub → green = live fail-closed reading + verdict-bearing
  fixture + both mismatch forms (`wp2-t095-t097.txt`).
- **T109/T113/T119**: red = stub coverage → green = subset rejections, live coverage, fourth-source
  and goal-partition fixtures (`wp2-t109-t113-t119.txt`).
- **T138**: red = the new contract test against the pre-edit validator (4 failed / 5 passed, exit 1)
  → green = 9 passed, exit 0; parallel-safety neighbour 16 passed (`wp2-t138.txt`).
- **Final smoke** (`wp2-engine-smoke.txt`): classify fail (107 obligation-missing, WP3 pending) ·
  coverage pass · serial-reason pass · reading pass (effective 3) · capability owner-unavailable
  exit 2 · interface gates exit 0 · 25 contract-neighbour tests passed.

## Design decisions taken under implement-time latitude

1. **Finding-code vocabulary.** The contracts name `code-unknown`, `bijection-gap` and
   `form-reason-inconsistent`; rows T053/T054/T056/T097 use the word "inconsistency" for
   record-level inconsistencies. The engine emits the **contract's specific names** and tags those
   findings `kind: "inconsistency"` with `compared` + `record` fields, so both readings are
   machine-readable.
2. **Evidence-form key shapes** (C-029 fixes the forms, not the key names): `dependency-edge`
   → `{predecessor, verdict_ptr}`; `write-conflict` → `{paths: [file-level paths]}`; `host-probe`
   → `{probe, landing}`; `budget-readings` → `{before: {slots, budget}, after: {slots, budget}}`;
   `unit-set` → `{units: [], missing_mechanism?}`. Pointer fields must resolve inside `--repo`
   (framework source or `.specify/` mirror). These are recorded here once so WP4's contract modules
   and the integrator can adjudicate any divergence.
3. **Capability dispatch-tool set**: `agent` / `task` / `subagent` / `dispatch` / `spawn_agent`, or
   any tool name containing `dispatch`. STR-004's definition owner is WP3 (T099); this set is the
   engine's one executable spelling and is re-openable in one place.
4. **Verdict gate**: `coordinator-dispatch-verdict.yaml` is present but `unadjudicated`; its own
   note says a consumer must read that as "no verdict readable" → `owner-unavailable` exit 2. The
   live-tree capability reading is therefore exit 2 by design (F-093-003 owns the ruling).
5. **Coverage `off`** requires a `decision`/`decision_reason` field on the fact's stage row; absent
   → `coverage-undeclared`. No stage carries `off` today.
6. **Fourth-source surface**: every `.specify/state/*.md` spine is the projection surface (one per
   feature line, each run-scoped), never "a fourth place". The scan covers
   `shared/ skills/ templates/ agents/ docs/reference/ .specify/{skills,shared,templates,memory}`
   plus `.specify/instructions.md`; tests and fixtures are assertions, not rule sources.
7. **Goal partition**: goal targets carry no dependency edges (`goal-definitions.md` § Target
   Decomposition), so ≥ 2 open targets are chunked by `min(slot_cap, ceiling) − verifier_reserve`;
   under 2 the goal stays serial with the code read from the slot fact's `degradation_rule`.
8. **`not-applicable`** is reserved for input errors on the envelope (with exit 2), which keeps
   C-022's "never read as green" property true at both the envelope and the exit code.

## Corrections disclosed (Fast Fail, correction-class — repaired in passing)

1. **Block-subset scalars are strings.** The declaration reader returns every scalar as `str`; the
   reading action's first matrix passed by accident until `requested`/`effective` were coerced with
   `numeric_reading`. Fixed, and the matrix re-pinned (the `reading-three` mismatch now fails).
2. **`tracked_files` must not inherit a parent checkout's index.** A fixture under this worktree is
   inside a git repository, so a bare `git ls-files` returned nothing for it and the fourth-source
   scan went blind. Fixed by comparing `rev-parse --show-toplevel` with the given root and falling
   back to the walk.
3. **T025/GATE-5 positional form** (`script-interface-check.py <path>`) exits 2; the declared
   selector is `--files` (WP1's correction — followed here).
4. **Write-domain vs row text (T138).** The package map's `write_domain` names three files, but
   T138's row text requires the F-093-015 re-point in `templates/tasks-template.md` and its mirror.
   Those two paths are in no other package's domain, so writing them creates no conflict; the row
   was executed as written and the deviation is disclosed here (and in the final ANOMALY line).

## Residual risks

- **classify's live decision is `fail`** until WP3 lands the class-obligation anchors (T034–T036)
  and the pointer placement (T040). C-024 is green (0 uncovered/ambiguous); C-025's mechanism is
  green on fixtures. The verifier should re-run `classify` after WP3 integration.
- **T025's collect half** waits on WP4's `tests/unit/test_concurrency_check_engine.py`; the gate is
  re-runnable after integration.
- **WP4's contract modules** (`test_concurrency_*.py`) were authored concurrently from the same
  contracts; finding-code names and evidence key shapes may differ from the engine's choices
  (recorded in § Design decisions 1–2). The integrator adjudicates any mismatch; the engine is one
  file and the vocabulary is not dispatched elsewhere.
- **Live capability exits 2** until the F-093-003 owner ruling lands; that is the intended
  fail-closed window, not a defect.
- **Obligation presence is a text-token test** (class name / anchor path / fragment). A body that
  merely mentions the phrase passes; WP3's systematic placement makes the signal meaningful, and an
  anchor that fails to resolve is always reported with its reason.
- **Fourth-source detection is a line-assignment heuristic** over the declared surfaces; a rule
  expressed only in prose without a `key:` line would not be detected — the closed surface set is
  stated in the engine and in § Design decisions 6.

## Register / write-domain note

No new durable identifier was coined by WP2; nothing outside the declared write domain plus the
mirror-regenerated projections (`templates/tasks-template.md` mirror, `.specify/scripts/python/*`)
and the mandated evidence/record files was written. No push; no subagents; no additional worktrees.
