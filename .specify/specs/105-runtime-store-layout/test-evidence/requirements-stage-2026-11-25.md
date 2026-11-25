# Requirements Stage Record — 105-runtime-store-layout

- **Stage**: requirements · attempt 1 · 2026-11-25
- **Line / run**: `runtime-store-layout` / `r20261125T022857Z-06dd`
- **Baseline commit**: `23938f22e` (branch `master`); feature branch `105-runtime-store-layout`
- **Assignment**: create the next numbered requirements spec + its requirements-quality checklist via `/speckit.requirements`, treating `.specify/.tmp/sdd-loop/tmp/runtime-store-layout/brief-requirements.md` as the feature description.
- **Execution class**: direct; no subagents dispatched; no state-spine writes; no user questions.

## Artifacts produced

| Artifact | Path |
|---|---|
| Requirements spec | `.specify/specs/105-runtime-store-layout/requirements.md` |
| Requirements-quality checklist | `.specify/specs/105-runtime-store-layout/checklists/requirements.md` |
| Validator capture (verbatim) | `.specify/specs/105-runtime-store-layout/test-evidence/requirements-validator.txt` |
| Pre-analyze gate capture (verbatim) | `.specify/specs/105-runtime-store-layout/test-evidence/pre-analyze-requirements.json` |
| This record | `.specify/specs/105-runtime-store-layout/test-evidence/requirements-stage-2026-11-25.md` |

## Baseline measurements (dated; re-measurable)

- `ls .specify/memory/` at `23938f22e`: 12 child directories — `coaching`, `evidence`, `exec-quant`, `feedback`, `housekeeping`, `knowledge`, `renumber`, `retention`, `session`, `todo`, `tools`, `trigger`.
- Engine-declared extra stores: `sanitize/` (`sanitize-utils.py`), `migrate/receipts/` (`src/specify_cli/__init__.py`), legacy `draft/` (`sanitize-utils.py` material roots), legacy `git-workflow.md` (superseded; not a store).
- `git ls-files .specify/memory | wc -l` = **2963** tracked paths (before migration).

## Deterministic gate results

| Gate | Command | Verdict |
|---|---|---|
| Flow-class read | `flow-class-check.py --action lookup --unit-id "spec:105-runtime-store-layout"` | `flow_class: execution`, `flow_type: -`, `source: declaration`, `marker: null`, `neutral: false`, rc 0 |
| Requirements validator | `validate-requirements.py .specify/specs/105-runtime-store-layout/requirements.md` | `status: ok`, 0 error / 0 warning, 304 lines, 34 definition rows (26 FR + 8 SC), 6 shared strings, exit 0 |
| Pre-analyze gate (self-check) | `pre-analyze-check.py --stage requirements --spec-dir .specify/specs/105-runtime-store-layout` | `decision=pass errors=0 advisories=29 waived=0`; every advisory is `missing-path` naming a new top-level store root that the implementation creates (expected creation target) |
| Quality checklist | `.specify/specs/105-runtime-store-layout/checklists/requirements.md` | 16/16 pass; no iteration consumed |

## Adjudications carried into the spec

- Memory namespace (A-2): `session` + `knowledge` remain the memory system and move to top-level; `.specify/memory/` is retired as a container with a tombstone row; "memory" is a system name, not a directory name.
- Every baseline child is classified with exactly one disposition (Store Inventory, 17 rows incl. the container and the legacy non-store file); no child stays by inertia.
- Migration/refusal contract (A-6/A-7/A-8): install/upgrade surfaces own the one-time migration; both-present is a deterministic refusal; no runtime dual-path fallback; archive-first + per-run receipts.
- Temporary memory + dynamic injection preserved: the session-tier behavior and the dispatch payload contract are unchanged; only store roots change.
- Tools domain consolidation (A-5): `.specify/tools/` holds canonical `*.md` records plus generated `*.json` inventories; the blanket ignore rule narrows to generated artifacts only.
- Feature binding deferred to `/speckit.clarify` (A-13).

## Concurrency reading

- `requested=1` · `effective=not_evaluated` (settled by the orchestrator) · `effective_reason=single-unit`.
- Single leaf execution; no dispatch, no fan-out.

## Anomaly line

- ANOMALY: `.git/config` became root-owned (`0600`) mid-run at 2026-11-25T10:35Z (host IDE git integration wrote it), which blocked every git command for the run user. Repaired in passing: `sudo -n chown agent:agent .git/config` restored the pre-anomaly ownership; file content unchanged (verified read), no repository data touched. Correction, disclosed here.

## Re-anchoring record

- After scaffold: `on-track`.
- After validator error repair (citation reverse-consistency): `correction-applied`.
- After git-config repair: `correction-applied`.
