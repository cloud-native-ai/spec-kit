# Tool Record: sync-mirrors.py

**Tool Name**: sync-mirrors.py  
**Tool Type**: `project-script`  
**Source Identifier**: scripts/python/sync-mirrors.py  
**Tool ID**: <TOOL:.specify/memory/tools/sync-mirrors.py.md>  
**Aliases**: sync-mirrors  
**Status**: Verified  
**Discovery Origin**: manual-entry  
**Last Updated**: 2026-07-30

## Scope

**Availability**: Project-level — available only within the current project workspace.  
**Typical Sources**: Scripts bundled with the project (e.g., `scripts/bash/*.sh`, `scripts/python/*.py`, `.specify/scripts/`).  
**Portability**: Tied to the project repository; not available outside the project root.  
**Source Identifier Convention**: Path relative to the project root.

## Description

Single-source mirror sync engine (adopted from ai-website-cloner-template's sync-script fan-out pattern). Fans canonical sources out to their runtime mirrors in one command: `templates/` → `.specify/templates/`, `skills/` → `.specify/skills/`, `agents/` → `.specify/agents/`, `scripts/` → `.specify/scripts/`, `shared/` → `.specify/shared/`, then delegates per-tool command copies to `regen-command-copies.py`. Replaces the manual dual-write ritual from the Mirror-sync map.

## Resource ID

- Canonical ID: `<TOOL:.specify/memory/tools/sync-mirrors.py.md>`
- Canonical Path: `.specify/memory/tools/sync-mirrors.py.md`

## Invocation & I/O Contract

- **Input Channel**: command-line flags
- **Invocation Mode**: non-interactive; `--check` is read-only, `--write` copies files
- **Output Mode**: human-readable drift/sync report on stdout; exit code carries the verdict

## Parameters

| Name | Required | Description |
|------|----------|-------------|
| `--check` | no | Report drift only; exit 2 if any drift detected (CI gate); never writes |
| `--write` | no | Sync all mirrors from canonical sources (default when no flag given) |

## Returns

| Signal | Description |
|--------|-------------|
| exit 0 | All mirrors match (or were successfully synced in `--write` mode) |
| exit 2 | `--check` found drift (`MISS`/`DIFF` lines list each file) |
| stdout lines | `ok`/`MISS`/`DIFF`/`sync`/`note`/`skip` prefixed per-file report |

## Environment Applicability

| Field | Value |
|-------|-------|
| Verified Version | python3 3.11 (stdlib only: argparse/filecmp/shutil/subprocess) |
| Version Differences | None known; requires Python ≥3.8 (pathlib.rglob) |
| Platform | linux (verified 2026-07-30) |
| Architecture | x86_64 (verified); no architecture-specific behavior |
| Fallback | Manual dual-write + `diff -rq <src> <mirror>` per the Mirror-sync map, plus `python3 scripts/python/regen-command-copies.py` |
| Preflight Check | `python3 scripts/python/sync-mirrors.py --check` (exit 0 = clean, exit 2 = drift) |

## Usage Notes

- Direction is one-way: canonical source → mirror. Never edit the mirror expecting it to flow back.
- `skills/` at repo root may be a placeholder (only `.gitkeep`); the script detects this and skips, since `.specify/skills/` is then canonical.
- Extra files that exist only in a mirror are reported (`note`) but never deleted — archive-not-delete discipline.
- Junk entries (`__pycache__`, `node_modules`, `.DS_Store`) are ignored and never copied.

## Examples

**Input**

```json
{ "flags": ["--check"] }
```

**Output**

```text
ok    templates/ == .specify/templates/ (43 files)
MISS  .specify/scripts/python/new-script.py
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
(exit 2)
```

## Behavioral Rules

- MUST be run from within the repository (script resolves repo root from its own location)
- MUST use `--check` in CI/verification contexts; `--write` only when syncing is intended
- MUST NOT be used to push edits from a mirror back to a canonical source (one-way only)
- MUST NOT delete mirror-only files; extras are report-only
- SHOULD be run after any edit to `templates/`, `skills/`, `agents/`, `scripts/`, or `shared/`
- SHOULD replace manual `cp`+`diff` mirror rituals in commands and skills

## Discovery Metadata

- **Method**: manual definition
- **Source**: project scripts directory
- **Verification Status**: verified
- **Notes**: Verified 2026-07-30: `--check` detects injected drift (exit 2), `--write` repairs to byte-identical, clean run exits 0.
