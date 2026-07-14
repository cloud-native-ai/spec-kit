# Feedback System (feedback-as-files)

Spec Kit keeps a distributed, **local-scope** feedback layer alongside the memory layer
(`session/`, `knowledge/`). At the wrap-up of a *qualifying* flow — the same lifecycle
point where flows already prompt for a Git commit — the executing agent reflects on the
just-completed run against the unit's declared purpose and records concrete, unit-scoped
optimization points. Once enough accumulate, it raises a single consolidated prompt
inviting the user to submit the collected feedback to the Spec Kit developers.

The engine reuses the proven memory-as-files pattern (`memory-utils.py`): a stdlib-only
`feedback-utils.py` writes Markdown entries plus a local `index.json`. There is **no
database and no vector store**.

## Feedback Trigger Policy

Feedback attaches only to long-running, qualifying flows — never to trivial ones:

- **All skills** carry a `## Feedback` step by default (a skill without it is
  non-conformant; `create-skills` validates it and `improve-skills` repairs it).
- **Complex commands only** carry the step. A command is *complex* iff it (a) invokes
  scripts/CLI tools, (b) produces an artifact consumed by another flow, or (c) consumes
  another flow's artifact. This yields **13 complex** commands and **4 simple** ones.
- **Simple commands** — `agents`, `constitution`, `feature`, `team` — carry **no** step
  (they delegate authoring to skills, which already carry feedback).
- **Trivial/short flows never trigger it**, preserving execution efficiency.

The authoritative classification lives in the feature's
`contracts/command-classification.md`; the canonical step text lives at
`.specify/skills/sdd-workflow/references/feedback-step.md`.

| Command | Class | Command | Class |
|---------|-------|---------|-------|
| requirements | Complex | instructions | Complex |
| clarify | Complex | tools | Complex |
| plan | Complex | skills | Complex |
| tasks | Complex | todo | Complex |
| implement | Complex | agents | Simple |
| analyze | Complex | constitution | Simple |
| checklist | Complex | feature | Simple |
| review | Complex | team | Simple |
| research | Complex | | |

## Layout

```
.specify/memory/feedback/
  <YYYYMMDDTHHMMSSZ>-<unit-slug>.md   # one file per recorded run
  index.json                          # store metadata + entry mirror
  .gitkeep                            # keeps the store dir version-tracked
```

Each entry is Markdown with YAML frontmatter (`id, unit_id, unit_type, run_id, scope,
feature, partial, created, summary`) plus a body with `## Review` and
`## Optimization Points` (≥1 bullet, or the explicit no-op line). Every entry is
`scope: local`. The `index.json` mirrors each entry plus `threshold`,
`count_since_submission`, and `submitted_at`.

## Engine (`feedback-utils.py`)

```bash
python3 .specify/scripts/python/feedback-utils.py --action <action> [options]
```

| Action | Purpose |
|--------|---------|
| `record` | Write one entry; idempotent per `(unit_id, run_id)`; increments the count on a new entry. |
| `status` | Read counters; `should_prompt = count_since_submission >= threshold`. |
| `list` | List recent entries (filters: `--unit-id`, `--unit-type`, `--since`, `--limit`). |
| `mark-submitted` | Reset `count_since_submission` to 0 and stamp `submitted_at` (entries are kept). |
| `reindex` | Rebuild `index.json` from entry files; preserves `submitted_at`. |

- `--unit-id` must match `^(?:/speckit\.[a-z0-9._-]+|skill:[a-z0-9._-]+)$` (else exit code 2).
- A `record` with an empty `--review` or empty `--points` exits with code 2.

## Threshold behavior

Entries accumulate across runs. The threshold defaults to **10** (overridable via
`--threshold` or `SPECKIT_FEEDBACK_THRESHOLD`, persisted into the index). When
`count_since_submission >= threshold`, `record`/`status` return `should_prompt: true`,
and the agent surfaces a **single** consolidated prompt. On confirmation, `mark-submitted`
resets the counter. Below threshold, no prompt appears.

## Dedup & partial runs

- **Dedup**: `record` is keyed by `(unit_id, run_id)`; a repeat is a no-op returning
  `duplicate: true` without incrementing the count. Nested command→skill invocations each
  record their own scope but never double-count the same unit+run.
- **Partial runs**: an aborted/failed run either records nothing or records with
  `--partial`; the `## Review` then begins with `**Partial run** — `.

## Distinction from `/speckit.review`

`/speckit.review` remains the sole **global**, whole-project process report. Local
Feedback Entries are bound to a single unit + run (`scope: local`) and MUST NOT duplicate
that global perspective — they complement it. Even the `review` command's own wrap-up
records only a *local* self-review of that run, kept distinct from the global report it
produces.
