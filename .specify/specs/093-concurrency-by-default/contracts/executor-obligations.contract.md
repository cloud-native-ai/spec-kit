# Contract — Executor obligations (C-041…C-062)

**Scope**: the obligation every execution body carries, the text that carries it, and the shared strings that
make it recognisable to program and reader alike. These clauses bind the owner documents and the shared string
table; they do not bind any single program.

---

## A. The obligation itself

- **C-041** — Every execution body MUST carry, in its own text, an obligation to consider concurrency first and to
  run serially only with a named reason code. The obligation MUST be expressible in one paragraph and MUST be
  carried by the body that executes, not only by a centre document. (FR-001, FR-002)
- **C-042** — The obligation MUST be three-part and each part MUST be separately checkable: (1) partition the work
  into units; (2) dispatch the units concurrently when the class and the capability allow; (3) otherwise record the
  serial reason code and its evidence. A body carrying only two parts is `obligation-incomplete`. (FR-002)
- **C-043** — The obligation MUST NOT require a body to know the slot cap, the ceiling, the budget formula or any
  other tuning value at authoring time; those are read at execution time from their owners. (Constitution XIV,
  FR-015)
- **C-044** — The obligation MUST apply at every grain: a single skill or command body, a goal slice, a team, and a
  loop stage. A writer that satisfies the obligation for one grain and not another is `grain-gap`. (FR-003)

## B. Class obligation text

- **C-045** — The class obligation for `concurrent-by-default` MUST state that serial execution requires a reason
  code from the closed set and MUST NOT state that concurrency is optional. (FR-005)
- **C-046** — The class obligation for `partition-required` MUST state that a single-unit execution is itself a
  serial shape requiring a factual reason code (the `single-unit` string), not a silent default. ([[STR-009]],
  FR-005)
- **C-047** — The class obligation for `serial-only` MUST name the host or dependency condition that forces
  serial and MUST NOT be assignable to a body merely because concurrency was inconvenient. (FR-004, FR-005)
- **C-048** — The obligation text for each class MUST be owned by exactly one anchor named in
  `concurrency-class.yaml`; a second copy of that text elsewhere is a projection and MUST be marked as such.
  (Constitution XIV, C-004)

## C. Serial reason codes

- **C-049** — The code set MUST be closed. Each code MUST carry: its identifier, its one-line meaning, its
  evidence form, and the FR-005 clause it discharges. A code without a condition or a condition without a code MUST
  be reported, not tolerated. (FR-006, C-028)
- **C-050** — The code list MUST distinguish factual codes (the unit set has size 0 or 1) from dependency codes (a
  real predecessor edge), from conflict codes (an intersecting write set), from host codes (the environment cannot
  run units in parallel), from budget codes (the reserve is exhausted). (FR-007)
- **C-051** — A budget code MUST NOT be accepted when the remaining budget was never measured in that run; "we
  were probably near the limit" is not evidence. (FR-007, FR-010)
- **C-052** — A host code MUST NOT be accepted as reusable: it MUST be accompanied by a landing point recording the
  environment in which it was observed, so a later run on a capable host cannot inherit it. (FR-007)
- **C-053** — The obligation MUST forbid treating "one agent is simpler" as a code. Simplicity is not in the closed
  set and MUST be reported as `code-unknown`. (FR-006)

## D. Shared strings

- **C-054** — Every shared string in [[STR-001]]…[[STR-011]] MUST have exactly one owner and MUST be written
  identically everywhere it appears; an occurrence with different spelling, case or punctuation is a defect.
  (FR-012)
- **C-055** — The string table MUST be registered in the declaration layer as a closed set, so a new string is a
  registered change and not an ad-hoc invention. (FR-012, C-011)
- **C-056** — The strings MUST be used in their declared role only: a reason code is not a class name, a class name
  is not a capability verdict. Cross-role use is `string-misused`. (FR-012)

## E. Declaration-equals-execution

- **C-057** — An execution body's declaration MUST be falsifiable against a run record. A body that declares
  concurrency MUST emit at least the dispatched unit ids and their intervals; a body that cannot emit them MUST
  declare serial and say why. (FR-023, SC-005)
- **C-058** — The obligation MUST require the body to report its own `requested` / `effective` /
  `effective_reason` triple at wrap-up, and MUST require `not_evaluated` where the intervals are absent rather than
  an optimistic number. (FR-008, [[STR-005]], C-032)
- **C-059** — A coordinator that plans parallel packages MUST emit the packages and MUST state the execution shape
  actually achieved; the shape "partition ready, execution serial" MUST be a named disclosure, never a silence.
  (FR-024, R-10)
- **C-060** — The red-first obligation: the plan phase MUST name, for each decidable clause in this contract set,
  the test module that goes red when the implementation is missing. A clause with no named red-first module is
  `unguarded`. (FR-030, plan Constitution Check row IV)

## F. Carry into the artifacts that execute

- **C-061** — The obligation MUST be present in the templates used to author new execution bodies, so a body
  authored after this feature inherits it without the author remembering. (FR-026)
- **C-062** — The obligation MUST NOT be duplicated into each of the per-agent command copies by hand; a copy is a
  projection and MUST be regenerated from its source. (R-11, Constitution XIV, FR-032)
