# Feature Detail: History Command

**Feature ID**: 030  
**Name**: History Command  
**Description**: Distill Claude Code and Qoder CLI sessions into an incremental theme knowledge base with review-confirmed execution.
**Status**: Implemented  
**Created**: 2026-07-14  
**Last Updated**: 2026-11-22

## Overview

Long-running projects accumulate large amounts of context inside AI-tool conversation history that is never captured anywhere durable. `/speckit.history` turns that history into a maintained knowledge base: it identifies the current tool and project, extracts the de-noised transcript of each past session, and distills each into five dimensions of long-term value — **关键决策与理由 (decisions & rationale, incl. abandoned alternatives)**, **可复用经验/踩坑 (reusable lessons/pitfalls)**, **未完成/待办 (unfinished/TODO)**, **关键交互流程 (key interaction flow)**, and **用户↔模型的冲突/分歧点 (user↔model conflicts)** — then aggregates them by theme into `.specify/history/`.

It is deliberately **tool-aware** (session history lives in different places per tool) and **incremental** (a manifest records which sessions were already distilled, so re-runs only process new ones and merge into existing docs, rather than re-summarising everything).

## Latest Review

2026-11-22 implementation audit: `STORE_RESOLVERS` supports both Claude Code and Qoder CLI. `manage-history` owns theme aggregation and a four-stage review → design → user confirmation → execution flow; historical Claude-only text and Qoder future-work entries are stale.

## Key Changes

1. **`scripts/python/history-utils.py`** — deterministic engine with `locate`, de-noised `extract`, and incremental manifest handling. `STORE_RESOLVERS` currently supports Claude Code and Qoder CLI; unsupported tools return an honest unsupported result rather than guessing a store.
2. **`scripts/bash/collect-history.sh`** — thin wrapper (models `refresh-tools.sh`): sources `common.sh`, resolves repo root, prefers the `.specify/scripts/python` runtime copy, pins `--project`, forwards args.
3. **`templates/commands/history.md`** — the command template (models `research.md`): frontmatter `scripts.sh` → `collect-history.sh --json`; six-step Outline (identify tool → extract → distill per session via parallel subagents → theme aggregation → manifest update → report); canonical `## Feedback` and `## Handoffs` sections.
4. **Runtime mirrors** — `.specify/scripts/{python,bash}/` copies + generated command files for the four tool dirs present in this repo (`.claude/commands`, `.github/prompts`, `.qoder/commands`, `.opencode/command`), produced via the same transform the CLI generator uses (`rewrite_paths`, `{SCRIPT}` substitution, frontmatter dropped).
5. **Docs & registry** — `docs/reference/commands/history.md`; `.gitignore` excludes `.specify/history/.work/` (the `.md` docs and `.manifest.json` are tracked); this feature entry.

## Implementation Notes

- The command was built directly rather than through a dedicated requirements cycle, so its Spec Path remains `-`.
- Summarization and theme derivation are AI work; locate, extraction, and incremental tracking belong to the deterministic engine.
- The four-stage execution flow writes dated evidence and requires user confirmation before applying designed dispositions.
- Earlier Claude-only verification results are dated history; current source and tests include the Qoder resolver.

## Future Evolution Suggestions

- Add `STORE_RESOLVERS` adapters for Codex CLI and opencode when their local session formats are deliberately supported.
- Optionally emit structured knowledge entries into `.specify/memory/knowledge/` in addition to the human-readable documents.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/030-history-command.md`
- Command Template: `templates/commands/history.md`
- Engine: `scripts/python/history-utils.py`; wrapper: `scripts/bash/collect-history.sh`
- Skill: `skills/internal/manage-history/SKILL.md`
- Docs: `docs/reference/commands/history.md`

## Status Tracking

- **Implemented**: engine, wrapper, command template, runtime mirrors, docs, and registry entry in place; end-to-end verified against Claude Code history. (current)
- **Future**: additional per-tool adapters; memory-record integration; contract tests.
