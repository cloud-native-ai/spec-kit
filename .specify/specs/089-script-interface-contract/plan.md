# Implementation Plan: 脚本接口契约（Script Interface Contract）

**Branch**: `089-script-interface-contract` | **Date**: 2026-11-06 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `089-script-interface-contract` → Feature 089 脚本接口契约（Script Interface Contract）
**Input**: Specification from `.specify/specs/089-script-interface-contract/requirements.md` (31 FR / 12 SC / 9 clarify rulings / 10 assumptions; requirements + clarify both U4-pass)

## Summary

The incident is one line of behaviour: a script with no argument parsing treated `--help` as ordinary input and
performed its write action. The fix is a governance rule plus the machinery that keeps the rule true — not a
document that says scripts should have `--help`.

This plan delivers four things and nothing else:

1. **One owner page** (`shared/definitions/script-interface-definitions.md`) that owns the candidate rule,
   the mandatory flag content, the zero-side-effect boundary, the unrecognised-option obligation, and the
   exemption/exception criteria — plus its `## Declared Exceptions` register.
2. **Five governance landings** that point at that page: the constitution template's new principle, the
   instructions template's new ambient section, this repository's live constitution (MINOR bump + Sync Impact
   Report + Last Amended), the `manage-constitution` mandate list, and the doubled count pins in the existing
   guards.
3. **One checker** — `scripts/python/script-interface-check.py` — that screens candidates from two
   machine-readable sources, classifies each by **running it** in a sandbox, and reports four conclusions per
   applicable script; consumed by one new contract test (`pytest -m contract`), with no new gate step.
4. **The backfill of this repository's applicable scripts**, delivered through generators rather than
   hand-edits: one bash guard block inlined into every applicable `.sh` by an idempotent script, one
   `--version` surfaced on every applicable `.py` through a shared helper module plus a declared mirror
   projection, and the existing CLI surfaces (`argparse` plus the two hand-rolled `sys.argv` readers) kept
   byte-compatible.

The design's load-bearing choice is that **nothing is a hand-maintained list**: not the candidate set, not the
applicable set, not the exception set, not the mirror's projected set. Each is derived by a rule a program
executes and a test can falsify by mutation — which is what makes SC-003, SC-008, SC-009, SC-010, SC-011 and
SC-012 measurable at all.

## Technical Context

**Language/Version**: Python `>=3.8` (declared in `pyproject.toml`; the checker and its helper are
standard-library-only files, so the floor is real), bash 4+ (all framework scripts; the guard uses only `case`,
`for`, `"$@"`), Markdown for the owner page and the four governance surfaces.
**Primary Dependencies**: none new. Reuses `scripts/python/sync-mirrors.py` (mirror projection),
`scripts/bash/generate-instructions.sh` (live instructions reconcile — invoked only through a scratch copy),
`scripts/python/regen-command-copies.py` (per-tool command copies, unaffected), `pytest` (`contract` marker).
**Storage**: no runtime store. Artifacts are repository files: the owner page + its mirror, two templates + this
repository's two live governance files, four generator surfaces (three Python/bash helper modules and one
`.sh` guard block template), one engine + mirror, one contract test, and the spec-local `test-evidence/`.
**Testing**: `pytest` (`tests/contract/test_script_interface_contract.py`, `pytestmark = pytest.mark.contract`).
Tests Mode = **ON**: every guarded behaviour is specified red-first. Interpreter measured 2026-11-06: the venv on
`PATH` has no `pytest`; `/usr/bin/python3` has `pytest 9.0.3` + `yaml` + `httpx` and collects 4 303 contract
tests in 11.85 s. The runner (`scripts/bash/run-tests.sh`) reads `SPECKIT_PYTHON` first, so every budget-slot
command pins `SPECKIT_PYTHON=/usr/bin/python3`.
**Target Platform**: any host that runs the framework's scripts — macOS and Linux for the repository itself;
`specify init` projects for the distribution leg (their `.specify/` copy is what runs, and it carries the
projection from C-36).
**Project Type**: SDD framework / code generator (packaged `templates/`, `shared/`, `skills/`, `scripts/`, plus a
`pytest` suite) — the "container-image factory" analogue: the deliverable is files that fan out to consumers.
**Performance Goals**: the checker's own probe phase MUST stay inside a soft budget of 900 s on this repository
(737 candidates, one sandbox worktree); measured anchors: `git worktree add --detach` < 2 s, cheap probes tens of
ms each. The budget is a finding when it trips, never a silent pass (criteria contract C-13).
**Constraints**: no `-h`/`--version` surface may change an existing declared option, JSON payload, or exit code
(FR-018); no new `/speckit.*` command, no driver stage gate, no confirmation gate, no second checker; no hand
edit under `.specify/`; the incident script `generate-instructions.sh` is never invoked without arguments from
this feature's runs against the live tree.
**Scale/Scope**: 737 candidates (71 `.sh`, 666 `.py`), measured split `.specify/` 146 · `tests/` 449 · `skills/`
87 · `scripts/` 51 · `src/` 3 · `install.sh` 1; 207 files carry an `__main__` block, 459 do not; 16 skill-level
`.sh` files. Deliverables: 1 owner page + 1 mirror, 4 governance surfaces + 2 live files, 1 engine + 1 mirror,
2 helper modules (one Python, one bash), 1 test file, 1 projection rule inside `sync-mirrors.py`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.16.0, 19 principles, in file order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every deliverable maps to an FR row (see § Implementation Slicing); no code is designed that no FR names. |
| II | Feature-Centric Development | ✅ Pass | Feature 089 row + detail exist and are materialized; this stage advances `Draft → Planned` in `features.md` and `features/086.md` and records a Feature-list review (see `feature-ref.md`). |
| III | Intent-Driven Development | ✅ Pass | The nine settle-points are recorded upstream in `requirements.md` § Clarifications; the three load-bearing rulings this stage adds are recorded as `T-001…T-003`, and the four corrections this stage cannot make itself are declared as `PLAN-EDIT` items rather than silently chosen. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON; `contracts/` carries C-1…C-38; each slice names its red-first assertion; the mutation legs are named (M-1…M-6 in `contracts/script-interface-criteria.contract.md` carriers). |
| V | AI Agent Integration Standards | ✅ Pass | No agent rendering surface changes: `agents/`, `specify render-agents`, and the per-tool command copies are untouched (C-32). The ambient instructions section is the only agent-facing file, and it is generator-produced. |
| VI | Continuous Quality & Observability | ✅ Pass | The checker's `--json` payload (C-18) and the `elapsed_ms` field are the measurement; SC-001…SC-012 each name a collection source; no number is invented (see § Success Criteria Measurement). |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan respected; `tasks.md` is explicitly not created here; status ceiling `Planned`. |
| VIII | Code as the Single Source of Truth | ✅ Pass | Every repository fact in this plan was measured this stage and is recorded with its command in `research.md`; three requirements readings are corrected by measurement rather than repeated (`PLAN-EDIT` F-1…F-4). |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One engine, one test file, one helper per language, one projection rule. No new command, gate, daemon, store, scheduler, or second classification mechanism. The checker is the declared sibling shape of `scan-confirmation-gates.py`. |
| X | Documentation Naming & Location Conventions | ✅ Pass | New files: `shared/definitions/script-interface-definitions.md` (kebab-case, `-definitions.md` sibling convention), `scripts/python/script-interface-check.py`, `scripts/python/script_interface_cli.py`, `scripts/bash/script-interface.sh`, `tests/contract/test_script_interface_contract.py`. No ALL-CAPS name is introduced. |
| XI | Dogfooding (Self-Application) | ✅ Pass | The rule is delivered in the framework sources and reaches this repository through the same projection/reconcile paths a client project uses; no `.specify/` file is hand-edited (C-33). |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | `sync-mirrors.py` owns projection, `generate-instructions.sh` owns the live instructions, `manage-constitution` owns the live constitution; no throwaway regeneration script is introduced (the backfill script is a one-shot generator recorded in `test-evidence/`, not a new named engine). |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | The change targets Task Understanding (a script answers "what do you do and what do you write") and Controlled Execution (read-only intent stays read-only); the evidence discipline is the `--json` verdict, not a claim. |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | The owner page owns the five items and every other surface carries a pointer (C-23, C-29); the banned-literal list is read out of the owner page, never retyped. |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | `quickstart.md` states premises per scenario and gives measured output; the plan defines `candidate`, `applicable`, `exempt`, `declared exception` at first use and reaches everything else by path. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Four measured contradictions with the requirements are surfaced as `ANOMALY` / `PLAN-EDIT` items (F-1…F-4) instead of being repaired by rewriting the spec; the mirrored-files projection is disclosed as a scope decision with its reversal path (T-002). |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory is created. `.specify/specs/089-script-interface-contract/` already exists; the sandbox uses `.specify/.tmp/` (sanctioned root, git-ignored) and is removed on exit. |
| XVIII | Grounded Naming | ✅ Pass | `Script Interface Contract (Declared, Zero-Side-Effect)` follows the sibling title form (user instruction → project convention → sibling imitation), and `definitions/` vs `guidelines/` was decided by the stated convention in A3. Engine/helper names follow `scan-confirmation-gates.py` / `common.sh` siblings. |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | The user's view decides the surfaced shape: `--help` answers "what does this do and what does it write" at the floor of one command; the five governance landings are projections of one page rather than five definitions. |

**Gates Status**: ✅ All gates pass — no `❌ Fail`, no `⚠ Partial`, so Complexity Tracking is `N/A`.

**Re-check after Phase 1** (2026-11-06, after `data-model.md`, `contracts/*` ×4, `quickstart.md`,
`feature-ref.md` landed): the same 19 rows re-read against the design artifacts. One row was re-examined in
depth — XIV (One Source of Truth) because five surfaces will quote one title, now backed by C-29's banned-literal
list plus C-21's rule/page agreement; the twentieth row is correctly absent, because the feature *adds* a principle
and the roster grows in the same change that this table is written (C-28's count pin). No row changed verdict.

## Decision Tensions

*Owner of the record shape and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md`.*

### T-001 — Classify by running the file, not by reading it

- **decision**: A script's applicability is decided by executing it in a sandbox copy and observing whether its own code acts; the source text is never the criterion.
- **antithesis**: Decide from source shape — a bash file with top-level executable statements, a Python file with an `if __name__ == "__main__":` block — which needs no sandbox, no worktree copy and no per-file run, and is therefore ~737 file reads instead of ~737 sandboxed executions; it is better whenever the classification must stay sub-second and the files are known to be small.
- **binding_constraints**:
  - pole_a: The exemption must be mechanically decidable and must not be reachable by a source-shape coincidence — measured: `scripts/bash/common.sh` has a top-level dependency check (source shape says "script", behaviour says "library", exit 1 with no action) and `scripts/python/declaration_reader.py` carries a `__main__` block while serving as an imported module.
  - pole_b: The check runs on every commit and its cost is paid by whoever commits; a per-file sandbox run trades time for correctness on 737 files.
- **discriminating_evidence**: Run `python3 scripts/python/script-interface-check.py --json` on this repository and read `candidates[]`: `common.sh` and `declaration_reader.py` carry `applicable=false` with a marker-absence / import-only evidence string, while `scripts/bash/generate-instructions.sh` carries `applicable=true` with a marker hit. Binary per file, and the mutatio​n in M-2 flips `declaration_reader.py` to `applicable=true` after a real action is added to its `__main__` block.
- **expected_sacrifice**: SC-003 Source ↓ a full run costs a sandbox worktree plus one execution per applicable file (budget 900 s, measured anchor in `research.md` R3); a timeout becomes a finding rather than a fast pass.
- **revision_trigger**: If two consecutive full runs exceed the 900 s budget after cheap probes are exhausted, or if a probe produces a false classification on a file whose behaviour is identical to an already-classified sibling → reopen and introduce a per-file declarative override (a named table), with the sandbox run kept as the auditor of that table.

### T-002 — A declared mirror projection instead of byte equality

- **decision**: `.specify/` copies of the scripts that need a mirror-side flag surface are generated as `source + declared projection`; the projection rule lives in `sync-mirrors.py` and is asserted by `--check`.
- **antithesis**: Keep byte equality for every mirror and put the whole flag surface in the source; it preserves the one-line mental model "mirror == source", keeps `test_mirror_parity_suite.py` untouched, and is better whenever the source can carry the surface without changing its own semantics — which is true for every script whose mirror and source run under the same interpreter root.
- **binding_constraints**:
  - pole_a: Measured: a bridge appended to a mirrored file never runs (`sys.exit(main())` comes first), a bridge inserted before the `__main__` block is erased by the next projection, and pasting a CLI into every library module contradicts FR-026's exemption (a module that acts on direct run is applicable, not exempt).
  - pole_b: `test_mirror_parity_suite.py` derives its parameters from `MIRROR_PAIRS`; a second, differently-shaped rule means a second way for mirror drift to hide, and "the mirror differs from the source on purpose" is exactly the sentence that hides drift.
- **discriminating_evidence**: `python3 scripts/python/sync-mirrors.py --check` after a simulated re-projection of `scripts/python/declaration_reader.py` into its mirror, then `python3 .specify/scripts/python/declaration_reader.py --version`: exit 0 and a version line under the projection rule, exit 2 and `unrecognized arguments` under the equality rule (both measured during this phase in a scratch worktree).
- **expected_sacrifice**: SC-003 Source ↓ the mirror pair list loses its "byte-identical" reading for the declared rows; the criterion becomes executable ("`mirror == project(source)`") and a reader must consult one rule to know which pairs are projected.
- **revision_trigger**: If a second feature needs a third projection kind, or if any projected pair is ever observed to diverge from `project(source)` in a completed run → reopen and either fold the projection into the sources' shared library path or retire the projection in favour of a single generated launcher per language.

### T-003 — Land the rule on this repository's constitution now, as a MINOR bump

- **decision**: This feature amends `.specify/memory/constitution.md` (1.16.0 → 1.17.0, new principle, Sync Impact Report, Last Amended) as part of its own commit.
- **antithesis**: Land the principle in the framework template only and let a separate `/speckit.constitution` run amend the live constitution; it keeps the amendment path single-owned by `manage-constitution`, and it is better whenever several governance changes are queued and the live roster's version history should record them together.
- **binding_constraints**:
  - pole_a: FR-013 requires the live principle, the Sync Impact Report, the MINOR bump and the Last Amended date in the same change; SC-005 measures all three in one commit, and the double-landing guard compares the template against the live roster.
  - pole_b: `manage-constitution` owns the amendment procedure and the versioning policy; a feature that hand-writes a version line is a second author of the same fact.
- **discriminating_evidence**: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --stage plan --spec-dir .specify/specs/089-script-interface-contract` plus `git diff --stat -- .specify/memory/constitution.md` on the implementation commit: the constitution appears in the same commit as the template, and the double-landing test's `LIVE_COUNT` moves from 19 to 20 in that commit. Binary.
- **expected_sacrifice**: SC-005 Source ↓ the live constitution's history gains a commit authored by a feature rather than by a dedicated governance run; the cost is that the amendment's rationale must be complete inside this feature's commit, not in a later one.
- **revision_trigger**: If `manage-constitution`'s own contract test starts rejecting the shape of this principle block, or if a second governance amendment lands in the same release with a conflicting version bump → reopen and move the live-constitution leg into a dedicated `/speckit.constitution` follow-up, leaving the template leg here.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/089-script-interface-contract/
├── plan.md              # this file
├── research.md          # Phase 0 rulings R1–R13 (measured anchors, rejected alternatives)
├── data-model.md        # Phase 1: E-1…E-8 entities, V-1…V-22 rules
├── contracts/           # Phase 1: 4 files, C-1…C-38
│   ├── script-interface-criteria.contract.md
│   ├── contract-checker-cli.contract.md
│   ├── governance-landing.contract.md
│   └── mirror-projection.contract.md
├── quickstart.md        # Phase 1: S-0…S-8, executed where this stage could execute them
├── feature-ref.md       # Phase 1: binding, delivery surface, Feature-list review
├── requirements.md      # upstream (not edited by this stage)
├── checklists/          # upstream
├── checkpoints/         # stage checkpoints 01/02 (+03 written by the driver)
├── goal/                # temporary goal (Feature 085)
├── test-evidence/       # stage gate evidence
└── tasks.md             # /speckit.tasks output — NOT created here
```

### Source Code (repository root)

```text
shared/definitions/script-interface-definitions.md      # NEW: owner page (rule + ## Declared Exceptions)
shared/definitions/framework-map.md                     # EDIT: register the new owner page in the shared row
templates/constitution-template.md                      # EDIT: new principle (next numeral after XVIII)
templates/instructions-template.md                      # EDIT: new ambient `## Script Interface Contract` section
.specify/memory/constitution.md                         # LIVE: new principle + Sync Impact Report + v1.17.0 + date
.specify/instructions.md                                # LIVE: regenerated by generate-instructions.sh
skills/internal/manage-constitution/SKILL.md            # EDIT: MUST-include entry (11 → 12)
scripts/python/script-interface-check.py                # NEW: the checker (screen + classify + report)
scripts/python/script_interface_cli.py                  # NEW: shared --version helper (VersionAction, pyproject read)
scripts/bash/script-interface.sh                        # NEW: the bash guard block body (sourceable)
scripts/python/sync-mirrors.py                          # EDIT: declared projection rule + check-mode assertion
scripts/bash/generate-instructions.sh                   # EDIT: guard block + raised INSTRUCTIONS_BUDGET_BYTES
scripts/bash/*.sh (other applicable)                    # EDIT: guard block, generated (13 files measured)
scripts/python/*.py (applicable)                        # EDIT: --version wiring (36 files measured)
skills/**/scripts/*.sh, *.py (applicable)               # EDIT: same, through their owning skill's source tree
tests/contract/test_script_interface_contract.py        # NEW: guard (pytest.mark.contract)
tests/contract/test_constitution_double_landing.py      # EDIT: counts 19/20/12 + watchlist 6 -> 7
tests/contract/test_fast_fail_discipline.py             # EDIT: TPL_EXPECTED 33 / LIVE_EXPECTED 34
.specify/shared/, .specify/scripts/, .specify/skills/   # MIRROR: regenerated only, never hand-edited
.specify/templates/                                     # MIRROR of the two edited templates
```

**Structure Decision**: This is the framework-source shape (`templates/`, `shared/`, `scripts/`, `skills/` edited;
`.specify/` regenerated), and it creates no new top-level directory. The new executables sit where their siblings
already sit: the checker beside `scan-confirmation-gates.py`, the Python helper in the same directory so every
mirrored copy can import it by sibling path, the bash guard beside `common.sh`. The spec-local artifacts stay
under the existing `.specify/specs/089-script-interface-contract/`.

### Mirror Obligations *(mandatory — this feature touches every mirrored surface)*

**Baseline drift measured before the edit** (2026-11-06, this tree):
`python3 .specify/scripts/python/sync-mirrors.py --check` → exit **0**;
`ok templates/ (22 files)`, `ok skills/external/ (415)`, `ok skills/internal/ (138)`, `ok agents/ (16)`,
`ok scripts/ (121)`, `ok shared/ (94)`, and `OK: all per-tool command copies match the source templates.`
There is **no pre-existing drift**, so every Verify cell below reads "no NEW drift" against a clean baseline.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/script-interface-definitions.md` (new) | `.specify/shared/definitions/script-interface-definitions.md` via `sync-mirrors.py` | `sync-mirrors.py --check` prints no NEW `MISS`/`DIFF` on the `shared` pair; `cmp` on the pair is identical |
| `templates/constitution-template.md` | `.specify/templates/constitution-template.md` via `sync-mirrors.py` | same, `templates` pair; and `tests/contract/test_constitution_double_landing.py` green with the raised counts |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` via `sync-mirrors.py` | same, `templates` pair; `test_fast_fail_discipline.py::test_a7…` green with `TPL_EXPECTED=33` |
| `skills/internal/manage-constitution/SKILL.md` | `.specify/skills/internal/manage-constitution/SKILL.md` via `sync-mirrors.py` | same, `skills/internal` pair; mandate count reads 12 |
| `scripts/python/script-interface-check.py` (new), `scripts/python/script_interface_cli.py` (new) | `.specify/scripts/python/…` via `sync-mirrors.py` | same, `scripts` pair |
| `scripts/bash/script-interface.sh` (new) | `.specify/scripts/bash/script-interface.sh` via `sync-mirrors.py` | same, `scripts` pair |
| `scripts/python/*.py` (applicable, edited in place) | `.specify/scripts/python/*.py` — **projected** (`python-version-bridge`) | `sync-mirrors.py --check` asserts `mirror == project(source)`; `python3 .specify/scripts/python/<name>.py --version` exits 0 and prints the source's version |
| `scripts/python/sync-mirrors.py` (edit) | `.specify/scripts/python/sync-mirrors.py` — projected (it is itself an applicable script) | same; plus `--check-projection` green |
| `scripts/bash/*.sh` (applicable, edited in place) | `.specify/scripts/bash/*.sh` — **projected** (`bash-version-guard`) | `sync-mirrors.py --check` asserts `mirror == project(source)`; `bash .specify/scripts/bash/<name>.sh --help` exits 0 |
| `skills/**/scripts/*.sh|*.py` (applicable, edited in place) | `.specify/skills/<skill>/scripts/…` and, for `skills/internal/<skill>/`, `.specify/skills/internal/<skill>/scripts/…` via `sync-mirrors.py` | same; classification of the mirror rows reads `projected-mirror` |
| `tests/contract/*.py` (edited + new) | none | not a mirrored path (`tests/` is not in `MIRROR_PAIRS`) |
| `.specify/memory/constitution.md`, `.specify/instructions.md` | none — these files *are* the live target | live files are the destination, never a mirror; the instructions file is produced by the generator |

**Do not forget**: `.specify/scripts/` has 146 candidates of its own; the mirror side is judged, not skipped
(FR-024(d)), and **73** of the 87 `.specify/skills/` script copies have no literal same-path source because the
runtime skill directory names differ (81 across all of `.specify/` once the 8 fixture stubs under
`.specify/specs/075-…/notes/` are counted) — that is expected, must not be "de-duplicated" by path lookup, and is
what C-6's `mirror-unpaired` basis exists for.

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The candidate screen's two sources agree on this tree, so a coverage finding would mean a genuinely new file. | `git ls-files '*.sh' '*.py'` → 737; work-tree walk → 737; untracked-and-not-ignored → 0 (measured 2026-11-06) | verified | — |
| EP-002 | A sandbox copy of the repository can be created and removed cheaply enough to probe every applicable candidate. | `git worktree add --detach` in `.specify/.tmp/086-probe/` completed in < 2 s; worktree removed and `git worktree list` back to one entry (measured this stage) | verified | — |
| EP-003 | A `pytest` interpreter with the suite's dependencies is reachable, and the runner honours `SPECKIT_PYTHON`. | `/usr/bin/python3 -m pytest --version` → 9.0.3; `-m contract --collect-only -q` → 4 303 collected in 11.85 s; `run-tests.sh` `resolve_python` reads `SPECKIT_PYTHON` first; the `PATH` venv has no pytest (measured this stage) | verified | — |
| EP-004 | The bash side can be judged without a full bash CLI framework: `case`/`for "$@"` inside the script suffices for all four obligations incl. `--` handling. | guard-block probe on `generate-instructions.sh` in the scratch worktree: `--help`/`-h`/`--version` exit 0, `--bogus` exit 2, `.specify/instructions.md` hash unchanged (measured this stage) | verified | — |
| EP-005 | `pyproject.toml` is reachable from every script's own directory in the framework tree, and the version read equals its `version` field. | copy-tree probe: `sync-mirrors.py <version>` tracked a `pyproject.toml` edit `0.0.22 → 9.9.9 → 0.0.22` (measured this stage) | verified | — |
| EP-006 | A generated bridge inside a `.specify/` mirror survives re-projection **only** under the new projection rule. | measured twice: bridge after `__main__` never runs (exit 2); bridge before `__main__` works (exit 0) but a simulated re-projection erased it (exit 2) — research.md R6 | falsified | resolve-in-scope (the projection rule in `sync-mirrors.py`, T-002) |
| EP-007 | A python `--version` written as a top-level `action="version"` survives every CLI shape in this repository, including required subparsers. | `goal-utils.py` uses `add_subparsers(required=True)`; a top-level version action is rejected at exit 2 when `--version` is the first token (measured: `sync-mirrors.py --version` → `unrecognized arguments`, exit 2 before the fix) | falsified | resolve-in-scope (a custom `VersionAction` on the top parser **and** every subparser — research.md R4; measured green in the copy tree) |

## Inherited Blockers

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `082`: `.specify/memory/features/082.md`, `.specify/specs/082-self-explanatory-integration/verification.md`
- `085`: `.specify/memory/features/085.md`, `.specify/specs/085-sdd-temporary-goal-team/verification.md`
- `081`: `.specify/memory/features/081.md`
- `064`: `.specify/memory/features/064.md`
- `069`: `.specify/memory/features/069.md`

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | `082:SC-006_status` | inherited | `gate:GATE-4` | this-slice | 082's row reads `partial`. The double-landing guard suite is extended here (18/19/11/6 -> 19/20/12/7) and GATE-4 re-runs it, so the carrier genuinely carries the guard's continuation; the `partial` value itself is 082's own evidence-binding state, not a measurement this feature can lift. |
| 2 | `082:deferred_tasks` | not-applicable | — | — | Extracted set yields no row: `deferred_tasks=` is empty at `082-self-explanatory-integration/verification.md:139`; the row is recorded so the extraction is visibly empty rather than unread. |
| 3 | `085:SC-010_status` | not-applicable | — | — | 085's row reads `partial` and its own `SC-010_blocked_at` is `no full 8-stage driver run with LLM stage agents`. That acceptance object is the end-to-end LLM stage chain; this feature ships a read-only checker and a contract test and never dispatches a stage agent, so nothing here can move 085's row and no carrier may claim to. Recorded so the extraction is visibly judged rather than skipped; the blocker stays with 085's own `SC-010_unblock`. |

## Complexity Tracking

N/A — the Constitution Check has no `❌ Fail` and no `⚠ Partial` row.

## Phase 0: Research Review

Recorded in [research.md](./research.md) as R1–R13, each with the decision, the rejected alternative and a measured
anchor. The load-bearing rulings: **R1** one engine whose rule is declared as data (`--emit-rule`); **R2** the
two-source screen plus a coverage assertion that cannot pass on an empty scan; **R3** classification by sandbox
execution, with three source-shape counter-examples measured; **R4** `<script-name> <framework-version>` read at
run time, with the required-subparsers trap measured; **R5** the bash guard's shape, fixed by `getopts`/`source`
ordering counter-examples; **R6** the mirror projection, proved necessary by two failing alternatives; **R7**
`tests/` classified by run semantics, not by path; **R8** the exception register and the measured `classification:`
correction; **R9** owner-page scope and the sibling-derived title; **R10** one ambient section plus the budget
raise; **R11** four explicit non-green failure paths; **R12** wiring into the existing `pytest -m contract` surface;
**R13** the mirror scope with a reversal path.

## Risks & Known Traps

Each entry is a measured fact about this repository, not a guess; the implementation stage re-measures before it
relies on any of them.

1. **`scripts/bash/generate-instructions.sh` is the incident itself, and the escaped write is not where a naive
   guard looks.** It has no argument parsing; a zero-argument run reconciles `.specify/instructions.md`. Three
   measured facts (quickstart S-5, on a `git clone` at `23c7a83b`): (a) `--help` today already exits **0** and
   writes nothing, so a probe that only diffs `instructions.md` cannot distinguish "the guard works" from "the
   script was harmless" — the probe needs a **discriminating red control**; (b) the un-flagged run on a *healthy*
   file is also a no-op (the reconcile writes only when a section is `missing or stripped`), which is why a damaged
   copy, not a healthy one, is the control — on a damaged copy it injects and the hash changes; (c) the write that
   escapes unconditionally is the **`.gitignore`** edit (`gitignore_add_pattern` at lines 66 and 216), reached even
   when the instructions file itself is untouched. Consequence: SC-002's snapshot pair names **both** files, and the
   red control is the damaged-copy run, not the healthy one. This feature never invokes the script against the live
   tree; the tasks stage reaches it through a scratch copy and checks the diff on the copy. `--help` is the first
   acceptance object (FR-019).
   **Scratch-tree precondition:** the copy must be a real git work tree (`git clone`) — a tree built by copying
   tracked files is not one, and `git status` there reports `fatal: not a git repository` — and it must not live
   under `/tmp`, which is `noexec` on this host and fails at the nested `refresh-tools.sh` call with exit 126.
2. **`goal-utils.py` silently ignores `--scope` / `--spec-dir` placed before the subcommand.** Measured in the
   file's own comment block: argparse lets the subparser overwrite what the top level set. The `--version` action
   must therefore be attached to the parser **and** every subparser (R4), and the guard's help text must say that
   options go after the action — otherwise the new surface inherits the same silent misread.
3. **`refresh-tools.sh`'s `*)` branch calls `usage()` and then continues.** "It printed usage" is not evidence that
   it rejected the option; the checker's `unknown_rejected` limb must assert a non-zero exit **and** that the main
   action did not run (C-9), never merely "usage text appeared".
4. **`getopts` is not usable for this contract**: it stops at `--` and does not consume or reject unknown long
   options. The guard must be a `case` loop over `"$@"` with an internal `--` terminator (C-9, R5).
5. **A top-level `action="version"` is rejected at exit 2 on a command with required subparsers** — measured on
   `sync-mirrors.py` and reasoned from `goal-utils.py`'s `add_subparsers(required=True)`. The `VersionAction`
   subclass must be registered on the top parser and on every subparser.
6. **`-h` is already merged with `--help` in seven scripts** (`check-prerequisites.sh`, `create-new-plan.sh`,
   `create-new-requirements.sh`, `create-new-skill.sh`, `create-new-tools.sh`, `implement-plan.sh`,
   `research-project.sh`). The guard must not create a second `-h` branch there; it must reuse the merged arm, and
   no script uses `-h` for another meaning (measured: zero).
7. **The instructions file is at 33 357 B against a 34 816 B budget** (1 459 B headroom). One ambient section plus
   its heading must fit, or the budget constant moves by the smallest multiple of 1024 that leaves ≥ 1024 B. The
   generator's own comment records the rule; the commit body records old/new/measured/reason.
8. **`goal-utils.py`'s argparse quirk is a warning about this feature's own deliverables**: a new flag on an
   existing engine must be asserted position-independently by a test, or it inherits the same silent-ignore class.
9. **Two python scripts carry no `argparse` and read `sys.argv` directly** — `clause_extract.py`,
   `gate-check.py`; three further files (`validate-decision-tensions.py`, `validate-falsification-quartet.py`,
   `validate-requirements.py`) import `argparse` and simply pass `sys.argv[1:]` to `parse_args`, so they are
   ordinary `argparse` users, not hand-rolled parsers. Measured: `clause_extract.py --help` exits **2** with
   `--help: not a file` — the exact "read-only intent became an action" shape of the incident, in a second
   engine. The guard must therefore cover the two `argparse`-free readers as well as register on every parser
   and subparser of the `argparse` users; `validate-decision-tensions.py` is the validator this feature's
   own tension records are checked with, so it is in the guard's own critical path.
10. **The `PATH` python3 has no `pytest`** while `/usr/bin/python3` does. Every test command in this feature pins
    `SPECKIT_PYTHON=/usr/bin/python3`, and any subprocess a test spawns must inherit it.
11. **`tests/` is 449 of 737 candidates** (447 `.py` + 2 `.sh`). A directory-level exemption is forbidden and
    would be invisible; the measured shape (441 `.py` without a `__main__` block, 6 with one — 5 under
    `tests/fixtures/` plus `tests/contract/test_migration_distribution.py` — `conftest.py` importing pytest) is
    what the classification must reproduce file by file.

## Implementation Slicing

| Slice | Scope | Exit evidence |
|-------|-------|---------------|
| S0 | Baseline: mirror check, candidate counts, pytest reachability, incident-script hash | `test-evidence/plan-baseline.txt` (mirror exit 0, 737 candidates, `SPECKIT_PYTHON` reading) |
| S1 | Owner page + `## Declared Exceptions` + mirror + `framework-map.md` registration | `sync-mirrors.py --check` clean on the `shared` pair; owner-page guard clauses (C-23, C-30) green |
| S2 | Checker: screen + `--emit-rule` + `--json` + exit codes; classification and four-conclusion probes; sandbox lifecycle | `script-interface-check.py --json` runs; `--emit-rule` agrees with a full run; C-13 degraded paths exercised |
| S3 | Contract test: red-first rows for C-1…C-22, mutation legs M-1…M-6 | `pytest -m contract tests/contract/test_script_interface_contract.py` green after S2; each M-leg fails without its subject |
| S4 | Governance landings: template principle, ambient section, live constitution (v1.17.0 + Sync Impact Report + Last Amended), mandate entry, count pins | `test_constitution_double_landing.py` + `test_fast_fail_discipline.py::test_a7…` green with 19/20/12/7 (from 18/19/11/6) and 33/34 (from 32/33); `git show --stat` on the constitution |
| S5 | bash backfill through the generator: `script-interface.sh` guard block, inlined into every applicable `.sh`; projection rule for the mirror copies | `script-interface-check.py --json` reports `help`/`version`/`unknown_rejected` true for every applicable `.sh`; `generate-instructions.sh --help` leaves the file hash unchanged |
| S6 | python backfill: `script_interface_cli.py` + `--version` wiring on every applicable `.py`, incl. the two `argparse`-free readers (`clause_extract.py`, `gate-check.py`); projection bridge for mirrors | same, for every applicable `.py`; `--version` single-source assertion after a copy-tree `pyproject.toml` edit (SC-011) |
| S7 | Instructions reconcile on a scratch copy: raise `INSTRUCTIONS_BUDGET_BYTES` if needed and regenerate the live file | scratch-copy generator run; live `.specify/instructions.md` diff shows exactly the one new section; `test_a7…` green |
| S8 | Closure evidence: full check run, exemption list with per-file bases, SC-001…SC-012 collection | `test-evidence/` files named per SC (see § Success Criteria Measurement) |

If the tasks stage returns `split-required`, split into `086a` (S0–S4: rule + checker + governance) and `086b`
(S5–S8: backfill + closure), following the 074a/074b precedent.

## Success Criteria Measurement

| SC | Measurement source (all land in `test-evidence/`) | Slot |
|----|---------------------------------------------------|------|
| SC-001 | Full checker run (`--json`) + the sandbox snapshot pair before/after the four flag runs, for every applicable script | closure |
| SC-002 | `sha256sum` of `.specify/instructions.md` **and** `.gitignore` before/after `generate-instructions.sh --help` on a cloned scratch tree, plus the damaged-copy red control that proves the pair discriminates (Risks 1a–1c) | one-shot, S5 |
| SC-003 | `--json` summary: `candidates` / `applicable` / `exempt` / `violations=0`, `exemptions[]` each with `basis` + `evidence` | closure |
| SC-004 | `specify init` in a clean temp dir → generated constitution contains the principle title, generated `instructions.md` contains the ambient heading; file fragments captured | one-shot, S4/S7 |
| SC-005 | `git show` of the amendment commit: version line 1.16.0 → 1.17.0, Sync Impact Report block, `Last Amended` date | one-shot, S4 |
| SC-006 | `test_constitution_double_landing.py` + mandate-entry count assertion, exit 0 | targeted, S4 |
| SC-007 | Before/after capture of the existing declared calls (one representative call per script family), `diff` empty except added flag paths | one-shot, S5/S6 |
| SC-008 | Mutation M-1: delete one compliant script's help arm in a scratch tree, assert the check goes red and names it; repeated over the applicable set | closure |
| SC-009 | `touch probe.sh` on a scratch tree → `candidate-not-collected` exit 1; add it to that tree's `.gitignore` → green, no naming | one-shot, S2 |
| SC-010 | M-2 (bash library + guard + action → applicable), M-3 (python module's `__main__` removed → stays exempt), M-4 (python module given a real action → applicable) | one-shot, S6 |
| SC-011 | Edit the copy tree's `pyproject.toml` version, re-run every applicable `--version`, diff; plus a zero-hit scan for a version-shaped literal in script bodies | one-shot, S6 |
| SC-012 | Three exception-register mutations on a scratch tree (a forged row with a missing path, an injected row whose skill does not declare `classification: external`, and the empty-register baseline) with the exit code and `exceptions[]` read | one-shot, S2 |

## Phase 1: Design Artifacts Summary

Counts below were taken from the files on disk after they landed, not pre-written.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](./research.md) | R1–R13 |
| Data model | [`data-model.md`](./data-model.md) | 8 entities (E-1…E-8) + 22 validation rules (V-1…V-22) |
| Contracts | [`contracts/`](./contracts/) | 4 files: `script-interface-criteria.contract.md` (C-1…C-13), `contract-checker-cli.contract.md` (C-14…C-22), `governance-landing.contract.md` (C-23…C-32), `mirror-projection.contract.md` (C-33…C-38) — 38 clauses |
| Quickstart | [`quickstart.md`](./quickstart.md) | 9 scenarios (S-0…S-8) |
| Feature ref | [`feature-ref.md`](./feature-ref.md) | binding, delivery surface, Feature-list review, disclosed rulings |

Drift from the Phase 0 expectation: the contract set is **four** files rather than the three the brief named,
because the mirror projection rule (C-33…C-38) is a distinct executable obligation whose falsification path
(T-002) is not the governance surfaces'. Nothing in the Phase 0 design predicted fewer.
