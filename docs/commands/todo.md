# `/speckit.todo` — Todo Command

Find and manage marked TODO blocks in your workspace.

## Overview

The `/speckit.todo` command operates in two modes:

- **Collection mode** (default): Scans workspace text files for fenced `SPECKIT TODO` blocks and outputs a consolidated list with source context.
- **Insertion mode** (`--insert`): Parses a user description and inserts a conforming `SPECKIT TODO` block at a specified location in a target file.

## Collection Mode

Run without arguments to discover all marked TODO blocks:

```
/speckit.todo
```

The scanner (`search-todo.sh`) finds any fenced code block whose opening fence line contains the exact substring `SPECKIT TODO` (case-sensitive). Each block is reported with:

- **Source file** and line range
- **Block content** (raw, preserved)
- **Context heading** (nearest Markdown heading above the block)
- **Prologue / Epilogue** (paragraph-boundary context around the block)

### Output Formats

- **Key:value** (default): Human-readable `BRANCH:`, `REPO_ROOT:`, `BLOCK[i]:` lines
- **JSON** (`--json`): Machine-readable single-line JSON object per contract schema

### Exclusion Rules

By default, the scanner excludes:
- `.git/`, `.svn/`, `node_modules/`, `.venv/`, `venv/`
- `__pycache__/`, `dist/`, `build/`, `target/`
- `.idea/`, `.vscode/`, `.DS_Store`, `Thumbs.db`
- Files larger than 16 MB
- Binary / non-UTF-8 files

Use `--no-default-excludes` to disable built-in excludes, and `--exclude <pattern>` to add custom patterns.

## Insertion Mode

Use `--insert` to add a SPECKIT TODO block to a specific file:

```
/speckit.todo --insert src/lib/auth.py
```

The command validates that the target file exists and is writable before inserting. It does NOT create files and does NOT modify content outside the inserted block.

## Safety

- **Malformed blocks** (unclosed fences, nested markers) are reported with source location but excluded from execution planning.
- **Batching**: When more than 10 valid TODO blocks are found, they are split into batches of at most 5 groups each, presented sequentially for review.
- **Safety veto**: TODO blocks requesting destructive operations (e.g., `rm -rf /`) or secret exposure are rejected.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Argument error |
| 2 | Repository root undefined |
| 3 | Scan I/O error |

## Related

- [Quickstart](quickstart.md) — End-to-end walkthrough
- [Specification](../.specify/specs/020-speckit-todo-command/requirements.md)
- [Data Model](../.specify/specs/020-speckit-todo-command/data-model.md)
- [CLI Contract](../.specify/specs/020-speckit-todo-command/contracts/search-todo-cli.md)