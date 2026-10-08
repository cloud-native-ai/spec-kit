# TODO-in-Context

A todo list on the side and the code it refers to drift apart: the list says
one thing, the code says another, and every reader — human or agent — has to
reconcile them by hand. TODO-in-Context closes the gap by embedding the todo
*at the code location it refers to*, as a marked block.

## The marker: two forms, one meaning

A SPECKIT TODO block takes the form its host file can legally carry:

- **Fenced form** in Markdown files — a fenced block whose opening fence line
  contains `SPECKIT TODO`.
- **Comment form** in source files — a run of consecutive line comments
  (`#`, `//`, `--`) whose first line's payload starts with `SPECKIT TODO`.
  A fenced block inside source code would be a syntax error, which is exactly
  why the comment form exists.

The exact detection semantics are owned by the scanner contract
(`.specify/specs/020-speckit-todo-command/contracts/search-todo-cli.md`,
rules D-1..D-12); `/speckit.todo` finds both forms, reports each block with
its surrounding context, and plans the work.

## Why embedding beats listing

1. **Context completes the intent.** The block only needs to state the
   short intent. The surrounding code, adjacent comments, and section
   headings complete it: a terse "remove this once migration completes"
   sitting above `legacyLogin()` is unambiguous in place, ambiguous on a
   list. When the wording alone admits two readings, the context settles
   it before a human has to be asked.
2. **Other flows perceive it early.** A marker is a declared future change.
   An agent refactoring near a marker knows the ground is about to shift;
   a reviewer knows why a region looks half-finished. The perception rules
   (do not silently remove; take it into account; report what you passed
   over) are owned by `.specify/shared/guidelines/todo-in-context.md`.

## Lifecycle

```
insert (placed at the element it refers to)
  → perceive (other workflows read it as declared intent)
    → collect (/speckit.todo scans, groups, plans)
      → execute (bounded, reviewable batches)
        → remove (the landed change + git history is the record)
```

A completed block is removed in the same step that lands the work — a stale
marker would send the next collection run re-planning finished work. Ideas
with no code touchpoint belong in the park store
(`.specify/memory/todo/`) instead; the two mechanisms meet when a parked
idea is promoted into an inserted block.

## Where each rule lives

| Surface | Role |
|---------|------|
| `.specify/shared/guidelines/todo-in-context.md` | Single source of truth: form ownership, interpretation, perception obligations, lifecycle |
| `.specify/specs/020-speckit-todo-command/contracts/search-todo-cli.md` | Scanner detection semantics (D-1..D-12, C-1..C-6) |
| `/speckit.todo` command (`templates/commands/todo.md`) | The four operational modes: list, collect, insert, park |

> **Related**: [spec-driven.md](./spec-driven.md) explains why written
> specifications lead implementation; TODO-in-Context is the same inversion
> applied one level down — intent is written where implementation lives.
