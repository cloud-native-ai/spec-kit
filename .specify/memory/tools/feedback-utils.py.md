# Tool Record: feedback-utils.py

**Tool Name**: feedback-utils.py  
**Tool Type**: `project-script`  
**Source Identifier**: scripts/python/feedback-utils.py  
**Tool ID**: <TOOL:.specify/memory/tools/feedback-utils.py.md>  
**Aliases**: feedback-utils  
**Status**: Verified  
**Discovery Origin**: manual-entry  
**Last Updated**: 2026-08-12

## Scope

**Availability**: Project-level — available only within the current project workspace.  
**Typical Sources**: Scripts bundled with the project (e.g., `scripts/bash/*.sh`, `scripts/python/*.py`, `.specify/scripts/`).  
**Portability**: Tied to the project repository; not available outside the project root.  
**Source Identifier Convention**: Path relative to the project root.

## Description

The feedback-as-files engine: persists local, unit-scoped feedback entries produced at the wrap-up of a qualifying flow (every skill; complex commands only) into `.specify/memory/feedback/` as Markdown plus a lightweight JSON index, and reports when the consolidated submission threshold is reached.

## Resource ID

- Canonical ID: `<TOOL:.specify/memory/tools/feedback-utils.py.md>`
- Canonical Path: `.specify/memory/tools/feedback-utils.py.md`

## Invocation & I/O Contract

- **Input Channel**: command-line flags (long prose passed via `--review-file` / `--points-file`)
- **Invocation Mode**: non-interactive
- **Output Mode**: JSON on stdout (default `--format text` for human-facing actions)

## Parameters

| Name | Required | Description |
|------|----------|-------------|
| `--action` | yes | One of `record`, `status`, `list`, `mark-submitted`, `reindex`, `package`, `upstream` |
| `--unit-id` | for `record` | The unit the entry belongs to, e.g. `skill:create-tools` or `/speckit.tools` |
| `--unit-type` | for `record` | `skill` or `command` |
| `--run-id` | for `record` | Stable per-run identifier; the engine no-ops on a duplicate `(unit_id, run_id)` |
| `--review` / `--review-file` | for `record` | Review prose, inline or from a file |
| `--points` / `--points-file` | for `record` | Optimization points, inline or from a file |
| `--partial` | no | Marks an aborted/partial run |
| `--feature` | no | Associated **requirement key** (e.g. `038-goal-target`); NOT the Feature registry ID |
| `--feature-id` | no | Associated **Feature registry ID** (e.g. `041`); distinct number space from `--feature` |
| `--notes` | no | `mark-submitted`: disposition summary for the batch, archived as `SUBMISSION-NOTES.md` inside the package |
| `--threshold` | no | Override the consolidated-submission threshold |
| `--format` | no | `text` or `json` |

## Returns

| Field | Description |
|-------|-------------|
| `id` | The created entry identifier |
| `path` | Path of the written feedback Markdown file |
| `duplicate` | `true` when the `(unit_id, run_id)` pair was already recorded (no-op) |
| `count_since_submission` | Entries accumulated since the last submission |
| `threshold` | Current consolidated-submission threshold |
| `should_prompt` | Whether the caller should surface the consolidated submission prompt |

## Environment Applicability

| Field | Value |
|-------|-------|
| Verified Version | python3 3.11.0rc1 |
| Version Differences | Requires Python >= 3.8 per the project's `pyproject.toml`; no version-specific flags observed |
| Platform | linux (verified); pure-Python and path-based, so no OS-specific invocation known |
| Architecture | x86_64 (verified); no architecture-specific behavior known |
| Fallback | None — this is the only writer of the feedback store; do not hand-edit `.specify/memory/feedback/` |
| Preflight Check | `python3 scripts/python/feedback-utils.py --help` (exit 0) |

## Usage Notes

- Feedback content is produced by agent self-reflection; it MUST NOT be solicited from the user.
- Pass multi-line prose via `--review-file` / `--points-file` rather than inline, to avoid shell quoting damage.
- Only prompt the user to submit when the returned `should_prompt` is `true`.

## Examples

**Input**

```json
{ "action": "record", "unit-id": "skill:create-tools", "unit-type": "skill", "run-id": "create-tools-20260730-1", "points-file": "/tmp/points.md" }
```

**Output**

```json
{ "id": "20260730T024742Z-skill-create-tools", "duplicate": false, "count_since_submission": 3, "threshold": 10, "should_prompt": false }
```

## Behavioral Rules

- MUST be run with a `--run-id` that is stable for the run, so re-invocation de-duplicates instead of double-recording
- MUST keep `--feature` (requirement key) and `--feature-id` (Feature registry ID) as distinct fields — never overload one with the other
- MUST treat `mark-submitted` as archive-then-reset: the pending batch is zipped into `packages/` (with optional `--notes` as `SUBMISSION-NOTES.md`) before the counter resets, so every reset leaves an auditable package artifact
- MUST use `scope: local` semantics — a whole-project assessment belongs to `/speckit.review`, not here
- MUST NOT solicit feedback content from the user; entries are agent self-reflection
- MUST NOT prompt for consolidated submission unless the returned `should_prompt` is `true`
- SHOULD pass multi-line review/points content via `--review-file` / `--points-file`
- SHOULD be skipped entirely in standalone mode (no `.specify/` at the workspace root)

## Discovery Metadata

- **Method**: manual definition
- **Source**: project scripts directory
- **Verification Status**: verified
- **Notes**: Contract confirmed against the script's `--help` output and a real `--action record` invocation on 2026-07-30. Re-verified 2026-08-12: sandbox round-trip confirmed `--feature-id` frontmatter, `mark-submitted` auto-packaging, and `SUBMISSION-NOTES.md` embedding; baseline feedback test suite 76/76 unchanged.
