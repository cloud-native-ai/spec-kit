# /speckit.history

Summarize the **current AI tool's** past conversations **for the current project** into a durable, theme-aggregated knowledge base under `.specify/history/`. Extracts long-term value (not verbatim transcripts) and runs incrementally.

## When to Use

- To capture hard-won context from many past sessions before it is forgotten
- When onboarding a teammate (or your future self) to *why* things were built the way they were
- Periodically, to keep a living record of decisions, pitfalls, and open TODOs
- After a burst of exploratory work, to distill it into reusable knowledge

## Syntax

```text
/speckit.history [--full] [theme focus | date range | topic hint]
```

- `--full` — reprocess **all** sessions and regenerate the knowledge base (ignore the incremental manifest).
- Optional focus/hint — narrow which sessions to emphasize.

## Execution Flow

1. **Identify tool & project** — Self-identifies the executing agent (per `shared/workflow/agent-configuration.md`) and runs `collect-history.sh` to locate the tool-specific session store. If the tool isn't supported yet, it reports where its history lives and stops cleanly.

2. **Extract clean sessions** — Runs the engine to de-noise each session (strips tool calls / injected blocks) into `.specify/history/.work/<sid>.txt`, and returns an inventory. Already-distilled sessions (tracked in a manifest) are skipped unless `--full`. Trivial/meta sessions are skipped and noted.

3. **Distill each session** — For each selected session, extracts five dimensions of long-term value (large sessions are delegated to parallel subagents):
   1. 关键决策与理由 (decisions & rationale, incl. abandoned alternatives)
   2. 可复用经验 / 踩坑 (reusable lessons / pitfalls)
   3. 未完成 / 待办 (unfinished / TODO)
   4. 关键交互流程 (key interaction flow)
   5. 用户 ↔ 模型的冲突/分歧点 (user↔model conflicts: `用户主张 X;模型原本 Y;最终 Z`)

4. **Theme aggregation** — Groups sessions into themes and generates/updates the knowledge base (merges into existing docs; only regenerates wholesale under `--full`).

5. **Update manifest** — Records distilled session ids so future runs are incremental.

6. **Report** — Summarizes tool/project detected, sessions distilled vs skipped, themes created/updated, and output location.

## Output Structure

```
.specify/history/
├── README.md                    # index: theme table + reading order + meta-conclusions
├── 00-cross-cutting-lessons.md  # lessons/pitfalls recurring across sessions
├── NN-<theme-slug>.md           # one file per theme, organized by the five dimensions
├── .manifest.json               # tracked: which sessions were distilled (incremental)
└── .work/                       # git-ignored scratch: de-noised transcripts
```

## Output Artifacts

| Artifact | Location | Tracked |
|----------|----------|---------|
| Theme knowledge base | `.specify/history/*.md` | yes |
| Incremental manifest | `.specify/history/.manifest.json` | yes |
| De-noised transcripts (scratch) | `.specify/history/.work/` | no (git-ignored) |

## Tool Support

| Tool | Status | Session store |
|------|--------|---------------|
| Claude Code | ✅ Supported | `~/.claude/projects/<encoded-project-path>/*.jsonl` |
| Codex / Qoder / opencode / Copilot / Hermes / … | ⏳ Not yet | Reported by the command; extraction is pluggable via `STORE_RESOLVERS` in `scripts/python/history-utils.py` |

## Prerequisites

- Have existing conversation history with the current tool for this project (the command distills the past; it does not create it).

## Next Steps

- Invoke `memory-record` to persist key distilled knowledge into long-term project memory.
- Run [`/speckit.constitution`](constitution.md) or [`/speckit.instructions`](instructions.md) if the distilled history surfaces conventions worth codifying.
