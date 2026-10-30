---
name: fixture-trainee
description: |
  Test-fixture Trainee for the Feature 078 coaching-loop contract tests. Reads a work
  brief that asks for a release-readiness checklist and writes `checklist.md`. Not a
  framework skill and never installed. Two defects are planted in the flow below so the
  coaching records can be judged against a known ground truth: one correctness defect
  (the Rollback plan row is dropped) and one efficiency regression (the brief is re-read
  once per remaining row).
classification: external
---

# fixture-trainee

## Goal

Turn the work brief in `work.md` into `checklist.md`: one row per required item, in the
order the brief gives, with a `PENDING` status column.

## Inputs

- `work.md` — the brief. Its numbered "Required items" list is the only source of rows.
- Output path: `checklist.md`, next to `work.md`.

## Workflow

1. Read `work.md` once and collect the numbered "Required items".
2. For each item that will get a row, read `work.md` again to confirm the item's exact
   wording. (Planted efficiency regression: this is one extra read per row instead of
   reusing the list collected in step 1.)
3. Emit one row per item **except item 4**. Item 4 is assumed to be covered by item 3, so
   no row is written for it. (Planted correctness defect: the brief requires five rows,
   this flow produces at most four.)
4. Write `checklist.md` with the header `| # | item | status |` and every row's status set
   to `PENDING`.

## Output

`checklist.md` — the primary artifact. It is correct only when it has one row per item in
`work.md`'s "Required items" list, in order, with no merged or missing entries.

## Failure semantics

- `work.md` missing or unreadable: stop and report `failed`; never invent items.
- `checklist.md` cannot be written: report `failed` with the write error.
- A required item cannot be quoted: keep the row and mark its item text `UNQUOTED` rather
  than dropping the row.
