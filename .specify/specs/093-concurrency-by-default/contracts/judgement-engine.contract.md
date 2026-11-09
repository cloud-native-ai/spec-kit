# Contract — Judgement engine (C-019…C-040)

**Scope**: `scripts/python/concurrency-check.py` — the one program that turns the declaration facts into verdicts.
It is read-only over the repository, standard-library only, and writes nothing except the file named by
`--json-out`. These clauses bind the engine, its unit test module and its contract module.

**Why an engine and not prose**: FR-030 requires every decidable assertion to have a check that goes red when the
implementation is missing. A judgement that lives only in prose cannot fail; a judgement that lives in two engines
will disagree with itself. One engine, one exit taxonomy, one JSON envelope.

---

## A. Interface

- **C-019** — The engine MUST answer `-h` / `--help` and `--version` without acting, MUST reject an undeclared
  option with exit `2` and a recognisable error, and MUST use the exit taxonomy `0` = pass, `1` = a documented
  check failed, `2` = input or environment error. It has no other exit code. (Constitution XXI, RS-004 analogue)
- **C-020** — The engine MUST expose exactly five read-only actions: `classify` (map bodies to classes),
  `serial-reason` (judge a serial record), `reading` (judge a concurrency reading), `coverage` (judge per-stage
  decomposition coverage), `capability` (judge dispatch capability). A sixth action MUST NOT be added without a
  clause revision.
- **C-021** — Every action MUST accept `--repo <root>` (default: resolved from the engine's own location by a
  literal `.specify` or repository-root component, never by walking up to the nearest ancestor containing
  `.specify/`), `--record <file>` for the three record-judging actions (`serial-reason`, `reading`, `capability`)
  and no record flag for `classify` / `coverage`, plus `--json-out <file>` (the only write). An action invoked
  without its declared record flag exits `2`. (Constitution XI path trap, F-093-002 family, Constitution XXI)
- **C-022** — The engine's JSON envelope MUST carry `action`, `decision` (`pass` / `fail` / `owner-unavailable` /
  `not-applicable`), `findings` (a list of `{code, subject, message, evidence_ptr}`), `measured` (the numbers the
  decision rests on) and `checked_at` (ISO-8601 UTC). A `not-applicable` decision MUST be distinguishable from a
  `pass` in the envelope and MUST NOT be read as green by a caller. (R-8 style)

## B. Class judgement (`classify`)

- **C-023** — `classify` MUST build the body universe by enumerating the roots from
  `executor-enumeration-roots.yaml` and MUST resolve each body's class through the decision rule carried by
  `concurrency-class.yaml`. No class name, root pattern or decision branch may be hard-coded in the engine. (C-004,
  C-005, FR-004)
- **C-024** — A body whose `(root, produced_shape)` resolves to zero members MUST be reported as `uncovered` and
  MUST make the decision `fail`. A body that resolves to two members is `ambiguous` and is also `fail`. There is no
  catch-all member. (FR-004, SC-001)
- **C-025** — The engine MUST read each body's obligation presence from the body's own text or from the
  `owner_anchor` named by its class, and MUST report `obligation-missing` for a body whose class obligation is
  nowhere readable. (SC-001, FR-001)
- **C-026** — `measured` MUST report the member counts per root **as measured**, not compared against a stored
  constant. (R-6)

## C. Serial-reason judgement (`serial-reason`)

- **C-027** — The judged input is a record carrying `pattern`, an ordered `codes` list and a per-code `evidence`
  object. The engine MUST reject a code outside `serial-reason.yaml`'s member set as `code-unknown`. (FR-006, FR-009)
- **C-028** — The engine MUST verify the condition↔code bijection both ways against the FR-005 clause ids carried by
  the fact, and MUST report `bijection-gap` naming each side of the gap when either direction is short. (FR-006)
- **C-029** — Evidence shape is judged **per code**, from the `evidence_form` declared in the fact: a
  `dependency-edge` record needs a resolvable predecessor id plus a completion verdict pointer; a `write-conflict`
  record needs a resolvable intersecting path set; a `host-no-parallel` record needs a probe reading and its landing
  point; a `budget-reserve` record needs the before/after slot and budget readings; a factual code needs the
  enumerated unit set of size 0 or 1. A free-form non-empty string MUST NOT satisfy any of these.
  (FR-007, FR-011, FR-013)
- **C-030** — The engine MUST report `form-reason-inconsistent` when `pattern=concurrent` carries a non-empty code
  list or `pattern=serial` carries an empty one, and MUST NOT accept the record. (FR-007, SC-003)

## D. Reading judgement (`reading`)

- **C-031** — `effective` MUST be computed as the **maximum overlap count** of the units' `[dispatched_at,
  settled_at]` intervals. Auxiliary aggregates (mean concurrency, deployed count, declared configuration) MUST NOT
  be accepted as substitutes. (FR-008, T-002)
- **C-032** — If any dispatched unit's interval is missing, `effective` MUST be reported as the literal
  `not_evaluated`, and the decision MUST NOT be `pass` for a claim that asserts concurrency. (FR-008, SC-006)
- **C-033** — `requested`, `effective` and `effective_reason` MUST be judged together: a record with one or two of
  them present is `reading-incomplete`. An `effective` below `min(slot_cap, ceiling, remaining budget)` MUST carry a
  named reason. (FR-008)
- **C-034** — The engine MUST recompute the bound from `concurrency-slot-and-reserve.yaml` plus the ceiling read
  from `wp-gate.py`'s declared default (or an explicit `--ceiling` given at call time) and MUST report the two
  operands it used. It MUST NOT carry a numeric ceiling of its own. (FR-014, T-001, C-008)

## E. Coverage judgement (`coverage`)

- **C-035** — `coverage` MUST report, per stage, the coverage decision resolved from
  `decomposition-coverage.yaml` plus the run-scoped spine keys, and MUST report `coverage-undeclared` for a stage
  that is neither covered nor explicitly disabled with a recorded reason. ([[STR-007]], FR-029, SC-008)
- **C-036** — The engine MUST report the relation it observed between the fact and the three spine keys
  (`decomposition`, `decomposition_stages`, `decomposition_slot_cap`) and MUST fail when a fourth source of
  "which stages decompose" is readable. (FR-029)

## F. Capability judgement (`capability`)

- **C-037** — `capability` MUST read each agent definition's existing `capability-tools` frontmatter list and MUST
  judge FR-021's three-way test: a dispatch tool present ⇒ `dispatch-capable`; an explicit handoff declared in the
  body ⇒ `handoff-declared`; an external-process form declared ⇒ `external-process`; otherwise `incapable`.
  ([[STR-004]], FR-021, FR-022)
- **C-038** — The engine MUST NOT introduce a new frontmatter key. The verdict is a *judgement of the existing
  field*, and the eight existing contract modules that assert on that field MUST remain green. (R-5, FR-022)
- **C-039** — The engine MUST read the coordinator verdict from
  `shared/declarations/facts/coordinator-dispatch-verdict.yaml` and MUST report `owner-unavailable` (exit `2`) when
  it is absent, never an assumed default. ([[STR-011]], C-016, T-004)
- **C-040** — `capability` MUST report the statement-by-statement inconsistency shape as a finding rather than
  resolving it: a body declaring `N >= 2` units while its `capability-tools` lacks a dispatch tool and no handoff is
  declared is `declaration-execution-mismatch`, and a run record showing all units with the same `executor_id` and
  zero interval overlap is `declaration-execution-mismatch` as well. Both are `fail`. (FR-016, FR-023, SC-005, R-14)
