# Contract: Team Project Form Generator

**Requirement → Feature**: `036-team-summary` → Feature 027 Team Management
**Artifact**: `skills/create-team/scripts/build-summary-input.py` → `<delivery_dir>/data/project-input.yaml` ([[STR-004]])
**Covers**: FR-001…FR-011, FR-023, FR-025, FR-027, FR-029
**Pinned by**: `tests/contract/test_summary_form_generator.py`, `tests/integration/test_summary_four_patterns.py`

## Interface

```
build-summary-input.py (--goal <goal-slug> | --team <team-slug>) [--out <path>] [--baseline <iso8601>] [--json]
```

| Option | Required | Semantics |
|--------|----------|-----------|
| `--goal <goal-slug>` | one of | Aggregate every team that declares this `goal_slug` ([[STR-006]]) |
| `--team <team-slug>` | one of | Convenience: resolve that team's goal identity, then aggregate that goal's full team set — a team never summarizes in isolation |
| `--out <path>` | no | Form destination; defaults to `<delivery_dir>/data/project-input.yaml` where `delivery_dir` is `.specify/project/goal/<goal-slug>/` |
| `--baseline <iso8601>` | no | Baseline date; defaults to the latest ledger event `ts` across the aggregated teams |
| `--json` | no | Emit a machine-readable generation report on stdout, including the resolved goal identity, whether it is explicit or inferred, and the contributing team list |

Exit codes: `0` form written; `3` refusal — no execution material across the whole goal (maps to `declined(no-material)`); `2` input error — unknown slug, unresolvable goal, unreadable team artifacts.

## Input surface (exhaustive)

The generator reads ONLY these paths, for **every** team belonging to the resolved goal. Reading anything else is a contract violation.

| Path | Consumed for |
|------|--------------|
| `.specify/teams/*/team.md` (frontmatter `goal_slug` only) | Goal membership discovery — scanning frontmatter to find every team sharing the goal |
| `.specify/teams/<team>/team.md` (frontmatter + `## Goal`) | `project`, `people`, `milestones`, `config.summary` |
| `.specify/teams/<team>/items.jsonl` | `work_items`, `phases`, `coverage` |
| `.specify/teams/<team>/runs/*-report.md` | Historical backfill only (FR-025), via the fixed Report contract sections |
| `.specify/teams/<team>/run-log.jsonl` | Cycle enumeration for `phases` (continuous only) |
| `.specify/agents/{templates,instances}/<slug>.agent.md` (frontmatter `name`) | `people.owner_name`; instance wins on filename collision |

## Normative rules

- **FG-1**: Generation MUST be deterministic. Two runs over identical inputs MUST produce byte-identical forms. No large-language-model transcription of run-report prose is permitted.
- **FG-2**: The generator MUST NOT read `.specify/teams/.work/**`, `.specify/agents/execution/logs/**`, or any path outside the repository.
- **FG-3**: Context consumed MUST NOT grow linearly with run count. Run reports are consumed by targeted section extraction, never whole-file ingestion.
- **FG-4**: Every emitted status and progress value MUST carry a `source` resolving to a tracked path. A value without provenance MUST be omitted rather than defaulted.
- **FG-5**: `project.repos` MUST be emitted empty. Repository derivation stays opt-in and is not used by this mechanism.
- **FG-6**: `project.baseline_date` MUST be supplied explicitly. The generator MUST NOT rely on the invoked skill reading the system clock.
- **FG-7**: All seven entities MUST be either populated from a defined team-side source or emitted empty with a corresponding `sources` declaration recording the absence. Silent omission is a violation.
- **FG-8**: The `coverage` block MUST be emitted on every run, with `candidate_total`, `excluded`, `granularity_truncated`, `unattributed`, and `source_label`. A report containing a work-breakdown diagram without a coverage declaration fails the upstream CG-COVERAGE gate.
- **FG-9**: Completed and archived items MUST remain present in the data layer. Presentation-level aggregation is expressed through `coverage.granularity_truncated`, keeping breakdown-diagram node counts within the upstream threshold of 15 nodes at depth ≥2.
- **FG-10**: Identifiers MUST follow `contracts/items-ledger.contract.md` §Identifier issuance. Non-ASCII titles MUST NOT be emitted as identifiers.
- **FG-11**: The generator MUST NOT write anywhere except `--out` and its parent `data/` directory.
- **FG-12**: When a team has no ledger and no run reports, the generator MUST exit 3 without writing a form. Goal success criteria alone MUST NOT be used to manufacture a form that appears complete.
- **FG-13**: Goal identity MUST be resolved as: `team.md` frontmatter `goal_slug` when present (`explicit`), otherwise the team's own slug (`inferred`, recorded in `inferred_fields` with a non-empty basis and surfaced in report metadata). Identity MUST NOT be derived from goal prose, so editing the goal text MUST NOT relocate the delivery directory.
- **FG-14**: Aggregation MUST cover **every** team declaring the resolved goal identity, not only the triggering team. A team that did not trigger this refresh MUST still contribute its ledger, so its prior work items never disappear from the summary.
- **FG-15**: Work-item and phase identifiers MUST be namespaced by contributing team at fold time (`<team-slug>.TI-0007`, `<team-slug>.PH-0002`). This is mandatory, not cosmetic: `entity_ids` is a global namespace enforced by primary key, and two teams' independently issued `TI-0001` values collide — measured, the load is rejected with exit 3 and the message `item_id='TI-0001' 在本实体内重复 —— DDL 约束 PRIMARY KEY`. Prefixed identifiers were measured to load cleanly. Team ledgers themselves MUST keep unprefixed identifiers so team-side issuance never depends on goal topology.
- **FG-16**: Phases MUST be namespaced per team (`phase_name` carrying the team slug). Teams under one goal may run different collaboration patterns whose phase units differ, so merging them into a single ordered sequence would assert an ordering that does not exist.
- **FG-17**: Every work item MUST be attributable to its producing team by machine. The `<team-slug>.` identifier prefix and the `source` provenance path both carry this attribution; neither may be dropped. Attribution MUST NOT be surfaced through team-internal identifiers forbidden by FR-022.
- **FG-18**: Concurrent refreshes of one goal delivery directory MUST be serialized into a single successful refresh. A half-written delivery directory is a prohibited failure state; the suppressed refresh MUST record its outcome in its own run report per the trigger contract.

## Per-pattern phase and work-item semantics (FR-002)

| Pattern | `phases` unit | `work_items` unit |
|---------|---------------|-------------------|
| `continuous` | cycle | tracked `STATE.md` entries, via the ledger |
| `iteration` | generation | per-generation variant tasks + adopted improvements |
| `serial` | stage | per-stage deliverables |
| `parallel` | dispatch batch | territories |

## Downstream invocation

The generated form is consumed by the unmodified `summarize-project` pipeline. The following sequence is **execution-verified** against a form derived from the real `cws-workspace-cluster` team (2026-08-04):

```bash
S=skills/summarize-project/scripts
python3 $S/validate-project-input.py --input <dir>/data/project-input.yaml --json   # exit 0, status=ready
python3 $S/project-db.py --db <dir>/data/project.db --load <dir>/data/project-input.yaml  # exit 0
python3 $S/project-db.py --db <dir>/data/project.db --check                          # exit 0, 状态 ok
python3 $S/progress-engine.py --db <dir>/data/project.db                             # exit 0
```

Observed guarantees from that execution, which the generator relies on rather than reimplementing:

| Observation | Consequence |
|-------------|-------------|
| `missing_required: []` with only team-derived fields | R-tier is satisfiable with zero manual form editing (SC-001, SC-002) |
| An identifier containing a space was rejected with exit 3 and a readable constraint reason | Identifier grammar is enforced upstream by DDL (FG-10) |
| `project.progress.progress_pct = null` with an explanatory `reason` | Zero-percent fabrication is prevented upstream (FR-006) |
| `gantt.bar_count = 0`, `has_planned_dates = false` | Absent schedule material suppresses the Gantt chart upstream (FR-023) |
| Phase aggregation reported 2 children for a 3-child phase | `unknown` items are excluded from aggregation (FR-006) |

`--load` is used rather than `--update`: cumulative state is authoritative in the ledger, so rebuilding the derived database loses nothing and keeps the summary reproducible from tracked artifacts alone.

## Invocation mode

The invoked skill defaults to four interactive per-layer confirmation gates. Team-triggered generation is automated, so the skill MUST be invoked in non-interactive mode with that fact recorded in the report's metadata section.
