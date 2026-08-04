# Contract: Summary Write-Set & Read-Only Discipline

**Requirement → Feature**: `036-team-summary` → Feature 027 Team Management
**Covers**: FR-011, FR-017, FR-020, FR-021, FR-022, FR-024, plus the pre-seeded Agent-layer invariance constraint
**Pinned by**: `tests/contract/test_summary_writeset.py`
**Measures**: SC-003, SC-004, SC-007, SC-010

## Write whitelist

During the summary step, writes are permitted ONLY to:

| # | Path | Contents |
|---|------|----------|
| W-1 | `<delivery_dir>/` — `.specify/project/goal/<goal-slug>/` ([[STR-001]]) | `summary.md`, `assets/`, `data/` |
| W-2 | `.specify/memory/feedback/` | Feedback entries recorded by the invoked skill |

Any write outside W-1 and W-2 during the summary step is a violation.

## Byte-invariance set

The following MUST remain byte-identical across the summary step:

| Group | Paths |
|-------|-------|
| Team run info (team index) | `.specify/teams/**` in full — `team.md`, `STATE.md`, `run-log.jsonl`, `items.jsonl`, `runs/**`, `constraints.md` |
| Monitored targets | Any external target the team observes |
| Invoked skill | `skills/summarize-project/**` and its mirror |
| Agent layers | `.specify/agents/**` — templates, instances, and execution configs/scripts alike |
| Pre-existing project artifacts | `.specify/project/` entries outside `goal/` — `project.md` and the wbs / gantt / milestones `.puml`/`.svg`/`.png` sets left by the former `manage-project` skill (FR-036) |

- **WS-1**: Invariance binds the **summary step** specifically. The Team Supervisor's ordinary cycle writes — appending to `items.jsonl`, issuing identifiers into `STATE.md`, writing the run report — are outside this constraint and remain permitted in their own phases.
- **WS-2**: `summarize-project` MUST NOT be modified by this mechanism. Adaptation is the team side's responsibility.
- **WS-3**: The summary step MUST NOT touch any agent layer. It is a pure derivation step.
- **WS-4**: Tracked summary artifacts MUST be written only by the Team Supervisor. Sub-agents MUST NOT write them.

## Provenance admissibility

- **WS-5**: Admissible provenance is a path tracked in version control.
- **WS-6**: Inadmissible, exhaustively: `.specify/teams/.work/**` (run intermediates, git-ignored), `.specify/agents/execution/logs/**` (runtime logs, git-ignored, including the external-dispatch visibility triplet `.live.log` / `.jsonl` / `.status`), and any path outside the repository — the dispatch wrapper's default log directory is `${TMPDIR:-/tmp}/spec-kit-dispatch`, which is outside the repository and therefore inadmissible on both counts.
- **WS-7**: Admissible despite being execution-layer: `.specify/agents/execution/configs/**` and `.specify/agents/execution/scripts/**` are tracked, and may serve as provenance.
- **WS-8**: A value whose only evidence lives at an inadmissible path MUST degrade to `unknown`. It MUST NOT be backfilled from cache, conversation memory, or a prior summary. Provenance must be verifiable at read time.

## Delivery-directory invariants

- **WS-9**: The goal delivery directory MUST hold exactly one current summary. History stays in each contributing team's `runs/` and MUST NOT be migrated.
- **WS-10**: The `## 附注` annotation section of a prior summary MUST survive refresh verbatim. This is provided by the invoked skill's existing refresh behavior and MUST NOT be reimplemented.
- **WS-11**: The delivery directory is keyed on goal identity, so a **team** slug change MUST NOT relocate it; provenance paths and attribution prefixes follow the rename instead. When a team is deleted, its historical contributions MUST remain in the goal summary, annotated as no longer active, with no dangling provenance to the removed team.
- **WS-12**: A team rebinding to a different goal (`goal_slug` rewritten) MUST leave its prior contributions in the original goal directory, annotated as no longer contributing; the new goal directory receives contributions from the rebinding point onward. Contributions MUST NOT be silently migrated nor presented in both places.
- **WS-13**: Concurrent refresh of one goal directory MUST be serialized. A partially written delivery directory is a prohibited state — a refresh either lands complete or leaves the previous summary intact.

## Reader-section hygiene

- **WS-14**: The five presentation sections MUST NOT contain team-internal identifiers — agent identifiers, result-manifest paths, or run-intermediate paths. Such information belongs only to the metadata and source-declaration sections. Team **attribution** is permitted and required (FG-17), carried by team slug rather than by internal identifiers.

## Verification

```bash
# Byte-invariance across a refresh: capture, refresh, compare
G=.specify/project/goal/<goal-slug>
before=$(git status --porcelain=v1 .specify/teams skills/summarize-project .specify/agents .specify/project | sort)
# ... run the summary step ...
after=$(git status --porcelain=v1 .specify/teams skills/summarize-project .specify/agents .specify/project | sort)
# Only paths under $G/ may differ between the two snapshots.

# Pre-existing project artifacts untouched (FR-036)
git diff --exit-code -- .specify/project/project.md .specify/project/wbs.* .specify/project/gantt.* .specify/project/milestones.*

# Reader-section identifier scan
grep -nE '\.work/|parallel-result-|\.live\.log|agent-[a-z-]+-template' $G/summary.md
# Any hit outside the metadata / source-declaration sections is a WS-14 violation.
```

The invariance check is asserted as a contract test rather than by manual inspection, so that a regression surfaces as a failing test instead of a reviewer noticing a stray diff.
