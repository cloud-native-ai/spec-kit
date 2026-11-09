# Contract — Existing semantics disposal (C-079…C-092)

**Scope**: what happens to every statement that already exists in the tree and now disagrees with this feature.
Each existing restatement MUST be resolved to exactly one disposition: value moved to its owner, text replaced by a
pointer, text removed, or text kept with a dated record. There is no fifth disposition and no "leave it for now".

---

## A. Disposition taxonomy

- **C-079** — Each pre-existing concurrency statement MUST be assigned exactly one disposition from {`owner-moved`,
  `pointer`, `removed`, `dated-record`} and MUST carry its evidence path. An unassigned statement is
  `disposition-missing`. (FR-018, T-001)
- **C-080** — A `pointer` disposition MUST leave a sentence that reaches the owner by path; deleting the statement
  without a pointer is `dangling-reference`. (Constitution XIV)
- **C-081** — A `dated-record` disposition MUST carry the date and the reason it is a record rather than a live
  statement; a dated record without a date is `record-undated`. (Constitution XIV duplicate conditions)

## B. The four slot-cap restatements

- **C-082** — The numeric slot cap MUST live in `concurrency-slot-and-reserve.yaml` and nowhere else; the three
  prose sites that currently restate it MUST become pointers. (R-3, C-009, C-065)
- **C-083** — The ceiling that bounds the slot cap MUST remain owned by `wp-gate.py`'s declared default; the fact
  file records the pointer to that owner and MUST NOT copy the number. (C-008, C-034)
- **C-084** — The spine's `decomposition_slot_cap` MUST be recorded as a run-scoped projection of the fact, and the
  spine MUST say so; a spine copy presented as an independent source is `restatement`. (C-009)

## C. Declaration-layer statements

- **C-085** — Every fact this feature registers MUST declare its `kind` from the existing five-member set; a sixth
  kind is a contract revision and MUST NOT be introduced silently. (R-2, C-003)
- **C-086** — Existing declaration keys MUST NOT be renamed; where this feature needs a new reading of an existing
  key, it earns a new fact and the old key stays. A rename is `breaking-change` and requires the revision path.
- **C-087** — Each new fact file MUST be registered in `shared/declarations/contract.yaml` in the same change that
  creates it, so `declaration_reader.py --action list` reports it. An unregistered file is invisible and is
  `unregistered`. (C-011)

## D. Templates and generated copies

- **C-088** — A template that must change MUST change in `templates/` and be mirrored; editing `.specify/templates/`
  alone is `mirror-only` and will be overwritten on refresh. (R-11, Constitution XI)
- **C-089** — The per-agent command copies MUST be regenerated, not hand-edited; a hand edit to `.claude/commands/` or
  `.qoder/commands/` is `hand-edited-copy`. (C-062)
- **C-090** — Retiring `.specify/templates/commands/` (already retired) MUST NOT be reversed by this feature; a
  reintroduced copy is `retired-path-revived`. (R-11)

## E. Adjacent semantics left untouched

- **C-091** — Feature 064's write lines, worktree and integration queue; Feature 070's work-package gate; Feature
  086's test-execution efficiency; Feature 092's goal/team parallelism MUST NOT be redefined. Where this feature
  needs their numbers it MUST reference their owners. (FR-019, feature-ref.md adjudication, F-093-001)
- **C-092** — Where an adjacent feature's file-level delivery surface and this feature's surface would collide, the
  collision MUST be recorded in `feature-ref.md` with the two file paths and the resolution, and MUST NOT be
  resolved by silent overwrite. (F-093-001, F-093-002)
