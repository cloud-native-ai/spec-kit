# Implementation Plan: Derivation Command

**Branch**: `048-derive-command` | **Date**: 2026-09-05 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `048-derive-command` → Feature 049 Derivation Command
**Input**: Specification from `.specify/specs/048-derive-command/requirements.md`

## Summary

`/speckit.derive` reaches an architecture by **replaying the reasoning methods of authoritative sources** rather than summarizing their conclusions. It grounds every source online (mandatory), extracts each source's way of arguing as a reusable **Reasoning Move** with named slots, accumulates those moves into a project-level library that later runs reuse and augment, builds a **derivation chain** under enforceable integrity rules C1–C7, and composes an architecture in which every element traces to a chain step. Gaps where grounded premises run out are recorded as open questions, never silently filled.

Technical approach: a **concept anchor** (`shared/definitions/derivation-definitions.md`) owns the model; a **stdlib-only engine** (`scripts/python/derive-utils.py`, six actions) owns every deterministic half — identity issuance, structural validation, dedup, link probing, counting; the **command template** (`templates/commands/derive.md`) owns the interaction and the irreducibly semantic halves — reading an argument, abstracting its inference pattern, grading provenance, naming a discriminating question. Storage is a new top-level root `.specify/derive/` holding the cross-topic move library and one archive per topic.

Direct motivation: the handed-in reading list that prompted this feature contained one dead link and one community-retitled article. Without online grounding, both become invisible holes in the chain and the output is an architecture that looks derived and is not.

## Technical Context

**Language/Version**: Python >= 3.8 (per `pyproject.toml`); engine is **stdlib only** — `argparse`, `json`, `re`, `pathlib`, `urllib.request`, `datetime`. `from __future__ import annotations` so PEP 604 signatures stay 3.8-safe (house pattern from `goal-utils.py`).
**Primary Dependencies**: none new. Agent-side online grounding uses the host's WebSearch/WebFetch tools — host capabilities, not Python dependencies. The archive availability API is reached with stdlib `urllib` only.
**Storage**: Markdown tables, git-tracked. `.specify/derive/moves.md` (single accumulating table, engine-written only) + `.specify/derive/<topic-slug>/derive.md` (one archive per topic). Column order is contractual — the engine parses positionally.
**Testing**: `pytest` with `contract` / `integration` markers (`pyproject.toml` → `[tool.pytest.ini_options]`); house runner `scripts/bash/run-tests.sh` (resolves `SPECKIT_PYTHON` → `.venv/bin/python` → `python3` → `python`). Regression judged **name-level** via `--names-out` + `comm -13`, never by count.
**Target Platform**: any host running a supported agent CLI (macOS / Linux). Pure-stdlib engine ⇒ no platform-specific code path.
**Project Type**: CLI framework / code generator (`templates/` + `scripts/` + `src/specify_cli/`).
**Performance Goals**: throughput is not the binding budget — **LLM tokens are**. Hence Summary-First projection reads of the move library (`moves-list`) instead of whole-file injection, and Program-First offloading of A1–A10/A12/A13 out of the model entirely.
**Constraints**:
- **Zero confirmation-gate headroom.** Scanner `total = 23` against a cap of `93 × 0.25 = 23.25`. One new BLOCKING match in `templates/commands/derive.md` or any new `shared/` file breaks two contract tests at once. Design consequence: the workflow is auto-execute + three-element execution report throughout (its outputs are reversible), so no gate is warranted at all.
- **Shipped-surface client neutrality.** `templates/` and `shared/` are in `SHIPPED_ROOTS`: no `Feature 0NN`, no `requirement 0NN`, no `.specify/specs/0NN-`, no real corpus URLs or titles. `KNOWN_DEBT` is empty — no allowlist to hide behind.
- **No test may touch the real network.** `probe-links` is offline-tolerant by contract (network error → `access: unknown`, exit 0) and is never invoked by a test.
- **Banned-heading sweeps.** `shared/**` and `templates/**` are substring-scanned for twelve reserved headings; this design therefore uses `## Contradiction Handling` and `## Script / Prompt Boundary`.
- **Two independent ID namespaces.** Feature ID = 049; requirement key / spec dir = 048. Offset −2 is stable across the repo (047→045, 048→046).
**Scale/Scope**: the 25th command template; 1 concept anchor (~321 lines); 1 engine (~600–900 lines); 1 new top-level `.specify/` root; 8 new test files; 6 wiring edits (probe registry, two classification lists, framework-map, glossary, features index).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.11.0):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Full flow executed: `requirements.md` (4 US / 38 FR / 6 SC / 7 shared strings) → this `plan.md` → `data-model.md` + 4 `contracts/` → `tasks.md` → implement. Nothing was built before it was specified. |
| II | Feature-Centric Development | ✅ Pass | Registered as Feature 049 in `.specify/memory/features.md` (hand-edited, header bumped 48→49) with detail file `.specify/memory/features/049.md`; requirement 048 bound to it, adjudication recorded in `feature-ref.md`. |
| III | Intent-Driven Development | ✅ Pass | The four user stories state *what the user needs and why that priority*, with Given/When/Then acceptance scenarios and no implementation leakage; the user's own words are preserved verbatim in `requirements.md` § Clarifications. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Four contracts authored before any implementation; RED tests (engine CLI surface, move-library unit, validate unit) precede the engine (tasks T019–T021 before T022); guard tests pin the concept anchor and the command surface. |
| V | AI Agent Integration Standards | ✅ Pass | The command fans out to every supported agent via `regen-command-copies.py` (no tool-specific dialect in the template); **and** the capability-degradation clause (FR-007, anchor §Capability Degradation) handles hosts that expose no online tool — the V-specific risk for a command whose core requirement is "must go online". |
| VI | Continuous Quality & Observability | ✅ Pass | `## Self-Audit` A1–A14 in every artifact; `validate` returns `errors[]` / `warnings[]` / `semanticChecksPending[]`; `stats` exposes per-run counts; feedback probe `speckit-derive-wrapup` registered; three-element execution report at wrap-up. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | This artifact is the plan stage; `tasks.md` follows via the tasks stage; feature status advances Draft → Planned here, → Implemented only when tasks are all closed and every SC has a `verification.md` row. |
| VIII | Code as the Single Source of Truth | ✅ Pass | Enforcement lives in code: the grade enum, exit codes, banned-justification literals and ID grammars are engine constants. The anchor is the *conceptual* owner; the engine holds the one pinned copy, and a drift test asserts the two lists are equal — a legitimate duplicate under Principle XIV, not a fork. |
| IX | Framework Scope Discipline (No Over-Engineering) | ⚠ Partial — see Complexity Tracking | New command surface + new stdlib engine + a **new top-level `.specify/derive/` root**. Justified row below; reuse surface is real (`sync-mirrors`, `regen-command-copies`, `feedback-utils`, `scan-confirmation-gates`, `run-tests.sh`, and the `goal-utils.py` / `sanitize-utils.py` house style). |
| X | Documentation Naming & Location Conventions | ✅ Pass | No uppercase special-name introduced; user doc lands at `docs/reference/commands/derive.md` per the one-file-per-command convention with **no** nested `README.md`/`index.md`; the new `.specify/derive/` root is registered in `shared/definitions/framework-map.md` (FR-038) so it is visible to the layout's single source of truth. |
| XI | Dogfooding (Self-Application) | ✅ Pass | Task T038 runs `/speckit.derive` on the real handed-in corpus inside this repo. The dead link and the community-retitled entry in that list become the acceptance evidence for SC-001 — the feature is validated by the exact defect that motivated it. |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuse gate honored by lookup-and-miss: no existing engine does HTTP (`docs-utils.py:broken_links()` and `sanitize-utils.py:check_dead_references()` resolve **repo-local paths only**; zero HTTP anywhere in `scripts/python/`). A Tool record `.specify/memory/tools/derive-utils.py.md` is added so the next author finds it instead of regenerating. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Directly strengthens **Learning Capture**: the accumulating move library is captured reasoning that later runs reuse rather than re-derive, and `reinforced` / `superseded` give the capture a correction path. The `## Feedback` step is embedded per the canonical convention. |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | The anchor declares in its opening lines exactly what it owns; the command template, engine docstring, glossary rows and user doc **reference** it and restate nothing. Move-library drift is closed by three mechanisms (projection-only reads, sole-writer append with dedup-refuse, and check A9 rejecting a divergent restated row). |

**Gates Status**: ⚠ One Partial — Principle IX, justified in Complexity Tracking below. No Fail rows.

**Re-check after Phase 1**: 2026-09-05 — re-checked against the landed design artifacts (`data-model.md`, 4 contracts, `quickstart.md`, `feature-ref.md`) and the corrected concept anchor. No compliance change: IX remains the only Partial. One correction was folded in during the re-check — the anchor's cross-scope identity defect (project-wide `M-<nnn>` anchoring to per-topic `S-<nnn>`) was fixed by adopting the qualified form `<topic-slug>.S-<nnn>`, which strengthens XIV (one identity grammar, no unresolvable references).

## Project Structure

### Documentation (this spec)

```text
.specify/specs/048-derive-command/
├── plan.md                     # This file
├── requirements.md             # 4 US / 38 FR / 6 SC / 7 shared strings
├── data-model.md               # Phase 1 — 7 entities + 2 state machines
├── quickstart.md               # Phase 1 — 3 walkthroughs
├── feature-ref.md              # Phase 1 — requirement→feature adjudication
├── baseline-failed.txt         # Frozen name-level test baseline (50 entries)
├── checklists/requirements.md  # Requirements-quality checklist
├── contracts/
│   ├── derivation-model.md     # Enforcement of C1–C7 / A1–A14; owns the engine's pinned banned-literal list
│   ├── derive-engine.md        # CLI surface, exit codes, JSON envelope, sole-writer rule
│   ├── derive-command-template.md  # Frontmatter, section order, scanner safety, degradation clause
│   └── move-library.md         # Table shape, ID issuance, dedup, projection-vs-copy
├── tasks.md                    # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
└── verification.md             # Implementation output (/speckit.implement)
```

No standalone `research.md` — Phase 0 findings are inlined below (internal investigation plus one external integration point).

## Phase 0: Research Review

- **R1 — Command wiring has no roster to edit.** `src/specify_cli/__init__.py` contains no command list; `generate_commands()` globs `templates/commands/*.md`. `_OBSOLETE_COMMANDS` is a *deletion* manifest — adding `derive` there would be actively wrong. Per-tool copies are generated into four existing dirs (`.claude/commands`, `.github/prompts`, `.qoder/commands`, `.opencode/command`); `.hermes`/`.codex` are absent locally and materialize at `specify init`.
- **R2 — Section order decides conformance class.** `templates/commands/sanitize.md` places `## Documentation` *before* `## Feedback` and therefore cannot satisfy `test_docs_step_injection.py` (which requires Feedback first, adjacent, Documentation citing `docs-step.md`). That is why the docs-step list is 15 while the feedback list is 18. `derive.md` uses the `research.md` order and joins **both** lists (18→19, 15→16).
- **R3 — The gate budget is exhausted.** `scan-confirmation-gates.py` reports `total: 23` against a cap of 23.25. `classify()` returns `reversible` for any BLOCKING match on a non-governance path with an action-context word nearby, and neither new file matches `GOVERNANCE_PATH_PATTERNS` — so there is no exemption path. Consequence: zero gates by design, and a guard test that imports `BLOCKING_RE` and asserts zero matches.
- **R4 — No HTTP predecessor exists.** Searched for a reusable link-liveness capability (Principle XII gate): `docs-utils.py` and `sanitize-utils.py` both resolve repo-local paths only. Lookup-and-miss is recorded; the new `probe-links` action is bounded (stdlib `urllib`, per-URL timeout, offline-tolerant, never test-invoked).
- **R5 — External integration point: the archive availability API.** The dead-link protocol's step 2 depends on a public archive availability endpoint returning JSON. **Its exact request/response contract is NOT assumed here** — it must be verified against the live service during engine implementation (task T022) and covered by the offline-tolerance test (T023) with the network path monkeypatched. If the endpoint's shape differs from expectation, the protocol's *ordering* is unaffected; only the adapter changes.
- **R6 — `update-feature-index.sh` is a live footgun.** It ends in `cat > "$FEATURE_INDEX"` and emits a **6-column** layout (dropping `Spec Path`), derives names from directory slugs, resets every status, and counts spec dirs (38) rather than feature rows (49) — while `test_c3` still passes. The features index is therefore hand-edited in this feature, and the script is **not** fixed here (out of scope; recorded as an observation for `/speckit.sanitize`).

### Source Code (repository root)

```text
templates/commands/            # + derive.md — the 25th command template (canonical prompt source)
shared/definitions/            # + derivation-definitions.md — concept anchor; edits to probe-definitions.md, framework-map.md
scripts/python/                # + derive-utils.py — six-action stdlib engine
docs/reference/commands/       # + derive.md — user-facing per-command doc (no index file in this dir)
tests/contract/                # + test_derivation_definitions.py, test_derive_command_surface.py,
                               #   test_derive_engine_contract.py; edits to the two classification lists
tests/unit/                    # + test_derive_moves.py, test_derive_validate.py
tests/integration/             # + test_derive_us1.py, test_derive_us2.py, test_derive_us3.py
.specify/memory/               # features.md row 049 + features/049.md + tools/derive-utils.py.md + glossary rows
.specify/derive/               # NEW TOP-LEVEL ROOT — moves.md (library) + <topic-slug>/derive.md (archives)
.specify/specs/048-derive-command/  # this feature's SDD artifacts
```

**Structure Decision**: extends the existing code-generator/framework shape by adding one command template, one concept anchor beside the other `*-definitions.md` files, and one engine beside the other `*-utils.py` engines. It introduces **one new top-level `.specify/` root** (`.specify/derive/`), the first since `.specify/goal/` was specified — and `.specify/goal/` has never been materialized in this repo, so there is no live instance to copy, only `goal-definitions.md` and `goal-utils.py:ARCHIVE_DIRNAME` as definitional precedent. `.specify/derive/` is git-**tracked** (unlike the gitignored `.specify/memory/sanitize/`, whose findings are re-derivable on every collect — moves are not).

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

Live pairs consulted from `scripts/python/sync-mirrors.py:MIRROR_PAIRS` (not memory): `templates`→`.specify/templates` (excludes `commands/`), `skills`→`.specify/skills` (excludes `site`), `agents`→`.specify/agents/templates`, `scripts`→`.specify/scripts` (**strict**), `shared`→`.specify/shared`.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/derive.md` | `.claude/commands/speckit.derive.md`; `.github/prompts/speckit.derive.prompt.md`; `.qoder/commands/speckit.derive.md` (+ `description:` frontmatter from `short-description`); `.opencode/command/speckit.derive.md` — all via `regen-command-copies.py`. **NO `.specify/templates/commands/` mirror (retired — that pair excludes `commands/`).** | `regen-command-copies.py --check` exit 0; each copy carries `<!-- AUTO-GENERATED from templates/commands/derive.md … -->` |
| `shared/definitions/derivation-definitions.md` | `.specify/shared/definitions/derivation-definitions.md` | `diff -q` byte-identical; `sync-mirrors.py --check` exit 0 |
| `shared/definitions/probe-definitions.md` | `.specify/shared/definitions/probe-definitions.md` | `diff -q`; `feedback-utils.py --action probes --validate` exit 0 (engine reads the **mirror**) |
| `shared/definitions/framework-map.md` | `.specify/shared/definitions/framework-map.md` | `diff -q` |
| `scripts/python/derive-utils.py` | `.specify/scripts/python/derive-utils.py` — **STRICT pair** (`strict_extras=True`): an orphan mirror file fails `--check`, so source and mirror must land in the same batch | `diff -q`; `sync-mirrors.py --check` exit 0 |
| `.specify/derive/**` | **NOT a mirror pair.** Project state, never shipped. MUST NOT be added to `MIRROR_PAIRS`. | `sync-mirrors.py --check` still exit 0 with the new root present |
| `.specify/memory/feedback/probe-map.md` | **Derived view** — rebuilt from the probe truth source by `feedback-utils.py --action map`; never hand-edited | re-running `--action map` is byte-idempotent |

## Complexity Tracking

> Filled because the Constitution Check has one Partial row.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| **IX — new stdlib engine `derive-utils.py` (~600–900 LOC)** | The Program-First discipline (`shared/guidelines/token-efficiency.md`) names pattern matching, structural validation, counting, dedup and comparison as work that MUST go to a deterministic program. A1–A10, A12 and A13 are entirely in that class. Two arguments are decisive beyond discipline: (a) an **accumulating** library with no scripted ID issuance and no dedup has no defense against two runs both writing `M-012` for different moves — which is precisely how a second source of truth is born, and the accumulating-library requirement creates that risk itself; (b) C1/C3/C5-propagation/A7 *are* the integrity claim — an unenforced integrity rule is decoration, and the whole difference between "a derivation chain" and "prose with arrows" is that the links are checked. | *Prompt-only enforcement.* Rejected: the model would be asked to self-check ~14 structural invariants across a multi-hundred-line artifact on every run — expensive in tokens, non-deterministic, and unauditable. A red self-audit that the model grades itself is not evidence. Precedent also rejects it: 047 shipped `sanitize-utils.py`, 041 shipped `goal-utils.py`, 048 shipped `site-memory.py`. |
| **IX — new top-level root `.specify/derive/`** | The user's decision was explicit: a **project-level** derivation archive (so a domain-level derivation outlives and serves many features) and an **accumulating project-level** move library. Both are cross-feature by construction, so a feature-scoped home (`.specify/specs/<key>/`) cannot hold them. Two roots for one concept would violate XIV, so the library and the archives share `.specify/derive/`. | *Reuse `.specify/memory/`.* Rejected: that root holds generic project state (constitution, features, glossary, tools, feedback); moves are the derivation domain's own accumulated instrument consumed only by `/speckit.derive` — exactly how `.specify/goal/` holds only goal-domain state. *Store per-feature.* Rejected: it would make the library un-reusable across topics, defeating the requirement. |
| **IX — `probe-links` performs HTTP** | The dead-link protocol needs link-liveness and archive-availability evidence that cannot be produced from the local repo, and FR-002 requires `verification` to carry concrete evidence rather than a bare attestation. Without a probe, the anti-fabrication rule has no unfakeable trace to point at. | *Let the agent assert liveness.* Rejected: that is the fabrication this feature exists to prevent. The action is kept deliberately narrow — stdlib `urllib` only, per-URL timeout, offline-tolerant (`access: unknown`, exit 0, never blocks), and never invoked by any test, so CI stays network-independent. It is a corroborator that leaves a trace, not a crawler. |

## Phase 1: Design Artifacts Summary

> Backfilled after the Phase 1 artifacts settled on disk (re-verified at close-out, task T039).

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 7 entities (Source Record, Reasoning Move, Derivation Step, Architecture Element, Open Question, Move Library, Derivation Archive) + 2 state machines (`access`, `confidence` with minimum-propagation) |
| Contracts | [`contracts/`](./contracts/) | 4 files: `derivation-model.md`, `derive-engine.md`, `derive-command-template.md`, `move-library.md` |
| Quickstart | [`quickstart.md`](./quickstart.md) | 3 walkthroughs: happy path with live sources; input containing a dead link + a community-retitled article; no online capability → honest degradation |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | requirement 048 → new Feature 049 adjudication (5 candidates considered and rejected) + US→FR→artifact map |
| Requirements checklist | [`checklists/requirements.md`](./checklists/requirements.md) | requirements-quality gate for this spec |
| Concept anchor | `shared/definitions/derivation-definitions.md` | Model owner: 4 record schemas + Open Question, 4-value grade set, C1–C7, A1–A14, banned-justification set, degradation rule, terminology boundaries |
| Test baseline | [`baseline-failed.txt`](./baseline-failed.txt) | 50 pre-existing failures, name-level; GATE-1 is `comm -13 baseline final` empty |

**Drift from Phase 0 expectation**: one substantive correction. The anchor as first drafted had a cross-scope identity defect — `M-<nnn>` is issued project-wide while `S-<nnn>` is issued per topic, so a move's `anchor` was unresolvable from any other topic. Fixed by adopting the qualified form `<topic-slug>.S-<nnn>` (after the `<goal-slug>.T-<nnn>` precedent). Three lesser defects were fixed in the same pass: two enum values with no producing path (`access: not-found`, `resolved_via: publisher-index`) were removed; `paywalled` and network-failure branches were added to the dead-link protocol; and move `status` was normalized from a four-value column mixing durable state with run-relative disposition into a durable two-value column (`active` / `superseded`) with the run-relative values reported by engine output instead. All four were surfaced by authoring the downstream contracts against the anchor — the drift check earned its keep.
