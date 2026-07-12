# Memory System (memory-as-files)

Spec Kit keeps a dynamic, file-based memory layer alongside the static memory assets
(`constitution.md`, `features.md`, `features/<ID>.md`, `tools.md`). It records the
non-derivable takeaways of conversations that happen **through** Spec Kit commands and
skills, so later sessions can build on prior decisions, preferences, and working state.

The design borrows the "memory as files" idea from
[agentscope-ai/ReMe](https://github.com/agentscope-ai/ReMe) but intentionally omits the
heavy parts: there is **no vector store** — retrieval uses a plain local JSON index with
keyword/tag scoring.

## Scope boundary

This memory only records LLM conversations that are **driven by a Spec Kit command or
skill** — not arbitrary chat. Because Spec Kit is scaffolding (it cannot intercept raw
model turns), the agent writes memory deliberately while executing a command/skill. The
engine enforces the boundary: every `record` must carry a `--source` of the form
`/speckit.<command>` or `skill:<name>`, and any other source is rejected.

## Layout

```
.specify/memory/
  session/            # short-term / working memory (append-only)
    <UTC-ts>-<slug>.md
    index.json
  knowledge/          # long-term / distilled memory (upsert by slug)
    <slug>.md
    index.json
```

- **session** — ephemeral working context of a current effort (progress, in-flight state).
  Safe to prune.
- **knowledge** — durable, cross-session knowledge (stable preferences, conventions,
  lasting decisions). Re-recording the same title updates the existing entry.

Each entry is a Markdown file with YAML frontmatter (`id, scope, source, feature, tags,
title, created, session_id, summary`) plus a body. The per-scope `index.json` mirrors the
metadata + summary so search never has to open every file.

### What NOT to store

Never store anything derivable from project state — code, architecture, file layouts, git
history, or anything already in the constitution / features / tools registries. Memory is
only for **non-derivable** context.

## Engine: `memory-utils.py`

The engine is a shared, standard-library-only script at
`.specify/scripts/python/memory-utils.py` (source: `scripts/python/memory-utils.py`).

| Action | Purpose |
|--------|---------|
| `record` | Write one entry to `session` or `knowledge`; updates the index. Requires a valid `--source`. |
| `recall` | Search by `--query` keywords + `--tags` / `--source` / `--feature` / `--since` filters; ranks by keyword overlap and recency. |
| `list` | List the most recent entries in a scope (no query). |
| `prune` | Bound short-term memory via `--max-entries` and/or `--max-age-days`. |
| `reindex` | Rebuild `index.json` from files if it is lost or stale. |

Example:

```bash
# capture a decision to short-term memory
python3 .specify/scripts/python/memory-utils.py --action record \
  --scope session --source "/speckit.plan" \
  --title "Chose JWT auth" --tags "decision,auth" --feature "012-auth" \
  --content "User picked JWT over sessions; API must stay stateless."

# recall it later
python3 .specify/scripts/python/memory-utils.py --action recall \
  --scope all --query "jwt auth" --limit 5
```

`record`, `prune`, and `reindex` always print JSON. `recall` and `list` print human-readable
text by default; pass `--format json` for machine parsing.

## Skills

Two skills wrap the engine for agent use:

- **memory-record** — the capture half. Invoked during/after a `/speckit.*` command or skill
  to distill and persist a takeaway. Chooses `session` vs `knowledge` and sets the correct
  `--source`.
- **memory-recall** — the retrieval half. Invoked at task start (or mid-task) to pull
  relevant entries and fold them into working context.

Both reference the engine as `${SKILL_WORKDIR}/.specify/scripts/python/memory-utils.py` and
operate on the memory store under `${SKILL_WORKDIR}/.specify/memory/`.
