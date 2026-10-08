# `/speckit.todo` — Todo Command

Find and manage marked TODO blocks in your workspace.

## Overview

The `/speckit.todo` command embeds todos **at the code or document location they refer to** and operates in four modes:

- **List mode** (default, no arguments or `--list`): read-only enumeration of every TODO item — workspace `SPECKIT TODO` blocks and parked ideas — then stop.
- **Collection mode** (`--collect`): scan blocks, group them with recalled context into a reviewable plan, execute it in bounded batches, and remove completed blocks.
- **Insertion mode** (`--insert`): insert a conforming TODO block into a target file at a specified location.
- **Park mode** (`--park`): store a free-floating idea (no code touchpoint) in `.specify/memory/todo/` without committing to it.

The underlying discipline — context-completed interpretation, early perception by other workflows, and the insert → perceive → collect → execute → remove lifecycle — is owned by [TODO-in-Context](../../concepts/todo-in-context.md).

## Marker Forms

The scanner (`search-todo.py`) finds two forms of the marker:

| Form | Files | Shape |
|------|-------|-------|
| **Fenced** | Markdown-family (`.md`, `.markdown`, `.mdown`, `.mkd`, `.mdx`) | Fenced block whose opening fence line contains the exact substring `SPECKIT TODO` |
| **Comment** | All other eligible text files (source code, configs, no-extension files) | A run of consecutive same-token line comments (`#`, `//`, `--`) whose first line's payload starts with `SPECKIT TODO` |

A fenced block inside a source file is a syntax error, which is why the comment form exists. Each block is reported with `form`, source file and line range, content, context heading (Markdown files only), and prologue/epilogue context (blank-line or paragraph bounded). Exact detection rules: D-1..D-12 and C-1..C-6 in the [CLI contract](../../../.specify/specs/020-speckit-todo-command/contracts/search-todo-cli.md).

## Collection Mode

```
/speckit.todo --collect
```

The command consumes scanner output summary-first, recalls prior run outcomes and user preferences from project memory (`memory-recall`), groups blocks by module/theme/order into work items, and presents the plan for review. Context completion applies: a terse or ambiguous block is interpreted first from its surrounding context (adjacent code and comments, heading, file structure); only when two readings survive does the run ask the user.

Execution auto-proceeds per batch (at most 5 groups per batch when more than 10 blocks are found), stops on any failed task, and **removes each completed block in the same step** — the landed change plus git history is the record.

## Insertion Mode

```
/speckit.todo --insert src/lib/auth.py
```

The command validates that the target file exists and is writable before inserting. It chooses the form by target file type (fenced for Markdown, comment for source files — never a fence in code), places the block at the element the TODO refers to, and preserves all surrounding content. It does NOT create files and does NOT modify anything outside the inserted block.

## Park Mode

```
/speckit.todo --park <idea>
```

Free-floating ideas — worth remembering, no code touchpoint yet — are stored verbatim in `.specify/memory/todo/` as one file per idea with status `parked`. Later runs promote them (into an inserted block or a requirement spec), retire them after the destination lands, or drop them on explicit veto.

## Output Formats

- **Key:value** (default): `BRANCH:`, `REPO_ROOT:`, `BLOCK[i]:` lines ending with `:form <fence|comment>`
- **JSON** (`--json`): single-line JSON object per the contract schema (§4.2); every block entry carries `form`

### Exclusion Rules

By default, the scanner excludes `.git/`, `.svn/`, `node_modules/`, `.venv/`, `venv/`, `__pycache__/`, `dist/`, `build/`, `target/`, `.idea/`, `.vscode/`, `.DS_Store`, `Thumbs.db`, files larger than 16 MB, and binary/non-UTF-8 files. Use `--no-default-excludes` to disable built-in excludes and `--exclude <pattern>` to add custom patterns.

## Safety

- **Malformed blocks** (unclosed fences, nested markers) are reported with source location but excluded from execution planning. The comment form has no closing syntax and is structurally never malformed.
- **Batching**: More than 10 valid blocks split into batches of at most 5 groups each, presented sequentially.
- **Safety veto**: Blocks requesting destructive operations (e.g., `rm -rf /`) or secret exposure are rejected from planning.
- **Bounded removal**: Only blocks whose task was executed and verified are removed; failed or unverified tasks leave their block in place.

## Memory & Framework Integration

- **Memory recall (planning)**: prior TODO-run outcomes and durable preferences are recalled before grouping — previously vetoed or deferred blocks are not re-proposed, and recorded grouping conventions apply.
- **Memory record (wrap-up)**: non-trivial runs persist outcomes (executed/deferred/vetoed and why) via the `memory-record` skill.
- **Summary-first scanner consumption**: counters + projected digest first; full block content only for the group being planned (token-efficiency discipline).
- **Glossary**: user input passes through the project glossary's homophone/confusable correction before mode detection.
- **Optional Git commit**: after execution, the command offers a `commit-template.md`-based commit, executed only on explicit approval.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Argument error |
| 2 | Repository root undefined |
| 3 | Scan I/O error |

## Related

- [TODO-in-Context](../../concepts/todo-in-context.md) — the discipline this command implements
- [Quickstart](../../tutorials/quickstart.md) — End-to-end walkthrough
- [Specification](requirements.md)
- [Data Model](../../../.specify/specs/020-speckit-todo-command/data-model.md)
- [CLI Contract](../../../.specify/specs/020-speckit-todo-command/contracts/search-todo-cli.md)
