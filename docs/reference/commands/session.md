# `/speckit.session`

Export AI agent CLI sessions into **user-named directories** — the export-side answer to a naming problem the host CLIs cannot solve: sessions carry only auto-generated IDs, with no official rename mechanism. Exporting copies a session's raw records into a directory whose name you choose, plus a description document that makes the session searchable and skimmable.

- **Source of truth**: `templates/commands/session.md`
- **Engine**: `skills/archive-session/scripts/export.py` (stdlib-only, network-free)
- **Feature**: 043 Session Export · **Requirement**: `039-session-export`

## What it does, in one paragraph

`/speckit.session export --name <bundle-name>` locates the current (or an explicitly specified) session of the AI agent CLI you are running in, copies its raw records — main transcript, sub-agent logs, state directories, oversized tool results, and request IDs where extractable — into `.session-export/<bundle-name>/`, and writes a session description document: `session-meta.json` (deterministic meta extracted by the engine) plus `SESSION.md` (meta section + a structured summary the exporting agent fills in faithfully from the records). The host's session storage is read-only throughout.

## Usage

```text
/speckit.session export --name <bundle-name> [--session <id>] [--tool <name>] [--verify <text>]
```

| Argument | Meaning |
|----------|---------|
| `--name` | **Required.** The bundle directory name — naming is the point of this command, so it is never auto-generated. Safe path segment: first character alphanumeric, remaining `[A-Za-z0-9_.-]`. |
| `--session` | Explicit session ID instead of auto-detection. |
| `--tool` | Explicit tool, skipping detection. One of the six supported names below. |
| `--verify` | A distinctive recent user utterance; confirms (or relocates) the chosen session. The agent fills this itself. |

The command previews the export (tool, session ID, target path, estimated size), asks for confirmation, then delegates to the engine. If the target directory already exists, the default is refusal; overriding requires an explicit interactive confirmation at that gate — there is no bypass flag.

## Supported tools (exactly six)

| Tool | Session storage | Exportability |
|------|-----------------|---------------|
| `claude-code` | `~/.claude/projects/**.jsonl` | ✅ |
| `codex-cli` | `~/.codex/sessions/**` | ✅ |
| `qoder-cli` | `~/.qoder/projects/**.jsonl` | ✅ |
| `opencode` | `~/.local/share/opencode/opencode.db` | ✅ |
| `copilot` | probe-style adapter | ⚠ declared "storage not detected" until a real store is probed |
| `hermes` | probe-style adapter | ⚠ declared "storage not detected" until a real store is probed |

Exit codes: `0` ok · `2` invalid arguments (missing/bad `--name`, same-name conflict) · `3` no matching session · `4` no usable tool (includes the probe declarations) · `5` IO/SQLite error.

## The description document

Each bundle carries `SESSION.md`: a deterministic **元信息** section (tool, session ID, model, workspace, time window, size counts, snapshot flag) and a **结构化总结** section — 任务脉络 / 关键决策 / 产物清单 — written by the exporting agent from the raw records, never invented. Oversized records (over the frozen budget thresholds) degrade to a skeleton summary with the reason declared. A still-running session is summarized as of the snapshot moment.

## Team-run traceability

Name bundles by dispatch label (`<team-slug>--<run-stamp>--<member-role>`) so `/speckit.team` run reports' mapping tables can reference exported dispatched-member sessions — closing the traceability chain from dispatch to raw conversation.

## Boundaries

- Read-only toward host session storage; records are copied, never moved or mutated.
- The bundle's version-control fate is yours — the command never edits `.gitignore`.
- Not related to Spec Kit's memory session layer (`.specify/memory/session/`) — a different concept.

## See also

- `.specify/specs/039-session-export/requirements.md` — the requirement (degraded route from session renaming)
- `skills/archive-session/SKILL.md` — engine invocation contract and support matrix
- `docs/reference/commands/team.md` — run-mode dispatch whose sessions this exports
