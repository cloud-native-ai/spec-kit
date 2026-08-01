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

- **Runtime-mode gate first**: every skill's `## Feedback` step begins with a
  runtime-mode gate (see `shared/workflow/runtime-mode.md`). Skills also ship to
  standalone agent applications (QoderWork, Wukong, OpenClaw, …) whose working
  directory has no `.specify/` — there the entire Feedback step is skipped (no
  engine, no store, no prompt). Commands only run inside Spec Kit projects, so the
  gate never fires for them.
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
`.specify/shared/workflow/feedback-step.md`.

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
| `list` | List recent entries (filters: `--unit-id`, `--unit-type`, `--since`, `--limit` — `0` = no limit; `--contains <text>` case-insensitive substring over entry summary + body, engine-side read, summary-level output). |
| `mark-submitted` | Reset `count_since_submission` to 0 and stamp `submitted_at` (entries are kept). Local bookkeeping only — NOT an upload. |
| `reindex` | Rebuild `index.json` from entry files; preserves `submitted_at` and `upstream_repo`. |
| `package` | Zip pending entries into `packages/` for **manual** delivery; source files untouched; no network access. |
| `upstream` | Show (or `--set`) the upstream repo URL used for manual delivery guidance. |

- `--unit-id` must match `^(?:/speckit\.[a-z0-9._-]+|skill:[a-z0-9._-]+)$` (else exit code 2).
- A `record` with an empty `--review` or empty `--points` exits with code 2.

### Token-efficiency self-assessment (Feature 040)

The canonical Reflect step (`.specify/shared/workflow/feedback-step.md`) includes a token-efficiency self-assessment: at wrap-up the agent checks for avoidable token spend (whole-file dumps of machine-managed data, LLM doing fixed-rule work, repeated reads). Findings are recorded as optimization points carrying the stable literal `token-efficiency`, retrievable in one query via `--action list --contains token-efficiency --limit 0` and consumed by the evidence feedback lane (recurrence signals) for improve-* flows. Discipline rules live in `.specify/shared/guidelines/token-efficiency.md` (single source; qualitative/proxy metrics only — no fabricated token counts).

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

## Positioning & Red Lines

Four facts govern the whole mechanism (canonical statement in
`.specify/shared/workflow/feedback-step.md` § *Positioning & Red Lines*):

1. **Target = the Spec Kit framework itself** (templates, commands, skills, scripts, docs)
   — never the LLM, the agent CLI/harness, or the user's project code.
2. **User data, fully optional** — the user may ignore the prompt, leave entries
   unprocessed forever, or delete the store; nothing blocks or nags because of it.
3. **Zero automated transmission** — the engine performs no network operations; the only
   transmission paths are the user manually sending a packaged zip or the user committing
   feedback files to their own git repo. `mark-submitted` is local bookkeeping.
4. **Local workaround value** — before a Spec Kit update lands, past entries document how a
   recurring issue was worked around.

## Processing side: package → manual send

When `count_since_submission >= threshold`, the consolidated prompt offers three choices:
**package** / **skip this time** / **stop prompting** (raise the threshold). Packaging is
the processing path:

```bash
python3 .specify/scripts/python/feedback-utils.py --action package
```

- Zips all pending entries (those recorded after the last `submitted_at`; `--all` for the
  full store) into `.specify/memory/feedback/packages/feedback-<ts>.zip`, plus a
  `MANIFEST.md` (entry list, time range, spec-kit version, install source). **Source
  entry files are never modified.**
- Prints the detected **upstream repo** and manual-send guidance. Detection priority:
  the user-configured `upstream_repo` in `index.json` > PEP 610 install metadata
  (`direct_url.json`, i.e. the git URL this custom spec-kit build was installed from) >
  none (then run `--action upstream --set <repo-url>` once). GitHub → attach the zip to
  an issue; GitLab → issue attachment or an MR to the feedback intake directory.
- The agent **never sends the zip** — delivery is entirely the user's manual action.
  After the batch is dealt with (sent or deliberately discarded), run `mark-submitted`.

The `packages/` directory is not git-ignored: like the entries, a zip is user data, and
whether to commit it is the user's call.

## Workaround lookup

Hit a recurring problem before a fix ships? Check whether an earlier run recorded a
workaround:

```bash
python3 .specify/scripts/python/feedback-utils.py --action list --unit-id "/speckit.plan"
```

Read-only; never gates execution.

## Distinction from `/speckit.review`

`/speckit.review` remains the sole **global**, whole-project process report. Local
Feedback Entries are bound to a single unit + run (`scope: local`) and MUST NOT duplicate
that global perspective — they complement it. Even the `review` command's own wrap-up
records only a *local* self-review of that run, kept distinct from the global report it
produces.

## Dogfooding: this system is Loop A

The feedback system is the carrier of the framework's **Dogfooding Loop A** (Constitution
Principle XI): every project using the framework feeds real-use friction back upstream
through the existing chain — record → threshold prompt → package → **manual** submission —
with zero automatic transmission. Downstream projects also reuse this same engine as part
of **Loop B** to run a use→feedback→iterate loop for their own product (see the
`## Dogfooding Practice` section delivered into each project's instructions file). No
Dogfooding-specific actions, steps, or storage exist — identification over invention.
