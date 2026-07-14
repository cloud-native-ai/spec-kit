# Contract: `feedback-utils.py` Engine CLI

**Feature**: 028 Feedback Mechanism | **Type**: CLI contract (stdlib-only Python engine)

The engine is a shared, standard-library-only script at `scripts/python/feedback-utils.py`, mirrored to `.specify/scripts/python/feedback-utils.py`. It is patterned on `memory-utils.py`. Skills and complex commands invoke it at wrap-up via:

```bash
python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action <action> [options]
```

## Global options

| Option | Default | Notes |
|--------|---------|-------|
| `--action` | (required) | One of `record`, `status`, `list`, `mark-submitted`, `reindex`. |
| `--workspace-root` | CWD | Store resolves to `<root>/.specify/memory/feedback/`. |
| `--format` | `text` | `record`, `status`, `mark-submitted`, `reindex` ALWAYS emit JSON; `list` emits text unless `--format json`. |

## Action: `record`

Writes one Feedback Entry and updates the index. Idempotent per `(unit-id, run-id)`.

| Option | Required | Constraints |
|--------|----------|-------------|
| `--unit-id` | Yes | MUST match `^(?:/speckit\.[a-z0-9._-]+|skill:[a-z0-9._-]+)$`. Invalid → exit code `2`. |
| `--unit-type` | Yes | `skill` \| `command`. |
| `--run-id` | Yes | Opaque per-run token; dedup key. |
| `--review` / `--review-file` | Yes (one of) | Prose review of the run. |
| `--points` / `--points-file` | Yes (one of) | One optimization point per line; a single no-op line is valid. |
| `--partial` | No | Flag; marks entry as covering a partial/failed run. |
| `--feature` | No | Feature key/ID. |
| `--threshold` | No | Override store threshold (default 10; env `SPECKIT_FEEDBACK_THRESHOLD` also honored). |

**Behavior (MUST)**
- Reject invalid `--unit-id`, empty `--review`, or empty `--points` with a non-zero exit and a stderr message.
- If an entry already exists for `(unit_id, run_id)`, MAKE NO CHANGES and return `{"duplicate": true, ...}` with the existing path; do NOT increment `count_since_submission`.
- On a new entry: write `<created-ts>-<unit-slug>.md`, append to `index.json`, increment `count_since_submission` by exactly 1.

**Output (JSON)**: `{ "id", "path", "duplicate": bool, "count_since_submission": int, "threshold": int, "should_prompt": bool }`.

## Action: `status`

Read-only. Returns store counters used to decide the consolidated prompt.

**Output (JSON)**: `{ "count_since_submission": int, "threshold": int, "should_prompt": bool, "total_entries": int, "submitted_at": string|null }`.

`should_prompt` MUST equal `count_since_submission >= threshold`.

## Action: `list`

Lists recent entries (most recent first). Options: `--limit` (default 5), `--unit-id`, `--unit-type`, `--since`. Text output by default; JSON with `--format json`.

## Action: `mark-submitted`

Records that the accumulated feedback was submitted. MUST set `count_since_submission := 0` and `submitted_at := now`. Does NOT delete entries. Output: `{ "submitted_at", "reset_from": int }`.

## Action: `reindex`

Rebuilds `index.json` from the on-disk `*.md` entries if the index is lost/stale. Preserves `submitted_at`; recomputes `count_since_submission` as the number of entries with `created > submitted_at` (or all entries when never submitted). Output: `{ "reindexed": int }`.

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success. |
| `2` | Validation error (bad `--unit-id`, missing required input, unknown action). |
