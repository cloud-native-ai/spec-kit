# Data Model — 093-concurrency-by-default

**Owner of this document**: the entity and validation-rule shapes this feature introduces or amends. Values
themselves are **not** owned here — every closed set, threshold and enumeration is reached by path to its fact
entry (`shared/declarations/facts/*.yaml`) or its existing owner. Where this document names a member (for example
`dependency-edge`), it names it to make a rule readable and cites the fact that owns the member set.

Eleven entities (E-1…E-11), twenty-six validation rules (V-1…V-26), five state machines (SM-1…SM-5).

---

## E-1 — Declaration class (声明类别)

The class an execution body is mapped to. Closed set, owned by
`shared/declarations/facts/concurrency-class.yaml` ([[STR-001]]; semantic name [[STR-002]]).

| Field | Type | Meaning |
|---|---|---|
| `name` | string | the member name (user-facing vocabulary, not an internal enum) |
| `applies_to` | list of enumeration-root ids | which roots this class may receive members from |
| `obligation` | enum `must-concurrent` / `may-serial` | the default shape this class imposes |
| `unit_form` | string | what a concurrent unit *is* for this class (Work Package, command segment, target, seat group, setup step, record batch, command run) |
| `owner_anchor` | path + section | where the class's obligation text lives |

**Invariants**: exactly one class per execution body (FR-004); the member set is closed and grows only by
revising the fact (FR-009); a body that resolves to no member is `uncovered` and red (never a catch-all member).

## E-2 — Execution body (执行体)

One member of the scope closed set. **Derived, never hand-listed** (FR-003).

| Field | Type | Meaning |
|---|---|---|
| `body_id` | string `<root-id>/<relative-path>` | stable identity derived from the filesystem |
| `root_id` | enum, from E-10 | which enumeration root produced it |
| `class` | E-1 member | resolved by the FR-004 rule, never chosen |
| `dispatch_capability` | E-6 | whether it can create sibling executors |
| `obligation_present` | bool | whether its own text (or its pointed owner) states the class obligation |

**Invariants**: `body_id` is a projection of a path, so it changes when the path changes and never independently;
a body with `obligation_present = false` is red (SC-001).

## E-3 — Concurrent unit (并发单元)

The independently dispatchable, independently completable, independently verifiable minimum advance.

| Field | Type | Meaning |
|---|---|---|
| `unit_id` | string | deterministic, derived from source artifacts (never from dispatch order) |
| `kind` | enum `read-only` / `write` | decides whether a write domain may be non-empty |
| `write_domain` | list of **file** paths | empty for `read-only`; directory-level entries are invalid (FR-012) |
| `depends_on` | list of `unit_id` | edges whose sources must hold a `verdict=pass` |
| `bounded_by` | `{unit, count}` | the unit's budget bound |
| `executor_id` | string | who ran it |
| `verifier_id` | string | who verified it; MUST differ from `executor_id` (FR-016) |
| `dispatched_at` / `settled_at` | epoch seconds or absent | the time interval used by the effective-concurrency reading (E-5) |
| `verdict` | `pass` / `fail` / `blocked` / absent | recorded by the verifier, never by the executor |
| `evidence_ptr` | path | one pointer per verdict |

**Invariants**: a unit is *ready* only when every dependency carries `verdict=pass` **with** an `evidence_ptr`
(FR-011); a missing interval makes that run's effective concurrency `not_evaluated` (FR-008); `verdict` without
`verifier_id` is `independence-undecidable` and red.

## E-4 — Serial reason record (串行理由记录)

The named explanation attached to any non-concurrent schedule.

| Field | Type | Meaning |
|---|---|---|
| `codes` | ordered list of E-7 members | non-empty unless the shape itself is red |
| `evidence` | per-code object with a code-specific shape | resolvable, not a free string |
| `pattern` | enum `concurrent` / `serial` | the shape actually taken |
| `requested` / `effective` | integers or `not_evaluated` | the concurrency reading (E-5) |

**Invariants**: the evidence shape is decided by the code's group in `serial-reason.yaml`
(`condition-bound` codes carry a resolvable artefact; `factual` codes carry an enumerated unit set of size 0 or 1);
a `concurrent` pattern carrying serial codes, or a `serial` pattern carrying none, is
`form-reason-inconsistent` (FR-007, SC-003).

## E-5 — Concurrency reading (并发读数)

| Field | Type | Meaning |
|---|---|---|
| `requested` | integer | the declared concurrency for the run |
| `effective` | integer or `not_evaluated` | maximum overlap count of unit intervals |
| `effective_reason` | string | why `effective < min(slot_cap, ceiling, remaining budget)` |

**Invariants**: `effective` is computed **only** from the intervals of E-3 (interval-overlap maximum, not width
sum ÷ duration, not a dispatched count); if any interval is missing the value is `not_evaluated` — never a
configuration value, never a neighbouring run's number (FR-008).

## E-6 — Dispatch capability (派发能力)

[[STR-004]], owned by `shared/definitions/subagent-definitions.md` for its definition and read from each
definition's existing `capability-tools` list for its value.

| Field | Type | Meaning |
|---|---|---|
| `verdict` | enum `dispatch-capable` / `handoff-declared` / `external-process` / `incapable` | the outcome of FR-021's three-way test |
| `source` | path + anchor | where the verdict is readable |
| `handoff_to` | string or absent | the upper executor when the verdict is `handoff-declared` |

**Invariants**: a body declaring `N >= 2` units with verdict `incapable` is red; `handoff_to` is required for
`handoff-declared` and forbidden for the other three.

## E-7 — Serial reason code (串行理由码)

[[STR-003]], closed, owned by `shared/declarations/facts/serial-reason.yaml`.

| Field | Type | Meaning |
|---|---|---|
| `code` | string | the member name |
| `group` | enum `condition-bound` / `factual` | which evidence obligation applies |
| `condition` | FR-005 clause id or absent | present iff `group = condition-bound` |
| `evidence_form` | enum | the shape E-4's `evidence` must take for this code |

**Invariants**: every `condition-bound` code maps to exactly one FR-005 clause and every FR-005 clause to exactly
one code (bidirectional zero gap, FR-006); `factual` codes map to no clause and are exempt from that bijection.
The declaration order is part of the value: E-4's list sorts by it.

## E-8 — Slot and reserve (槽位与保留位)

| Field | Type | Owner |
|---|---|---|
| `slot_cap_default` | integer | `shared/declarations/facts/concurrency-slot-and-reserve.yaml` |
| `slot_cap_ceiling` | integer, runtime-resolved | `wp-gate.py --slot-cap-ceiling` (default `4`) |
| `verifier_reserve` | integer `>= 1` | the same fact as `slot_cap_default` |
| `remaining_budget` | runtime reading | the run's existing budget accounting |

**Invariant** (the only composition rule this feature adds): `effective <= min(slot_cap, ceiling, remaining budget)`,
and `effective_available = min(...) - verifier_reserve`; when `effective_available < 2` the body degrades to serial
with `budget-reserve` (FR-015).

## E-9 — Unit partition rule (单元划分规则标识)

| Field | Type | Meaning |
|---|---|---|
| `rule_id` | string | e.g. the existing `decompose-<stage>-v1` family |
| `stage` | stage name | which stage the rule serves |
| `derivation` | string | what the units are derived from |

**Invariant**: replaying the same source artifacts and the same `rule_id` yields the same unit set and the same
edge set (FR-010); an unregistered `rule_id` is red.

## E-10 — Enumeration root (枚举根)

[[STR-008]], owned by `shared/declarations/facts/executor-enumeration-roots.yaml`.

| Field | Type | Meaning |
|---|---|---|
| `root_id` | string | stable id used by E-2/E-1 |
| `pattern` | glob | the filesystem pattern (**never** a member count) |
| `class` | E-1 member | the class this root's members map to |
| `excluded_layers` | list of paths | projections that are **not** roots (notably the spec-local goal/team layer, an 085 projection) |

**Invariants**: five roots; a sixth added by editing the fact; a root whose members resolve to two classes is red
(FR-004); a count written into this entity is a defect (R-6).

## E-11 — Coordinator dispatch verdict (协调者可派发裁定)

[[STR-011]], owned by `shared/declarations/facts/coordinator-dispatch-verdict.yaml` (T-004).

| Field | Type | Meaning |
|---|---|---|
| `verdict` | enum `allow` / `forbid` | the single adjudication |
| `authority` | path + anchor | who owns the ruling |
| `consequence` | string | what each verdict obliges (`forbid` ⇒ dispatch belongs to the driver/main agent; `allow` ⇒ coordinators gain a dispatch tool) |

**Invariant**: exactly one value per repository; this feature never writes a value it did not receive from the
owner — it registers the surface and asserts the value is readable.

---

## Validation rules

| ID | Rule | FR / SC |
|----|------|---------|
| V-1 | Every enumerated body maps to exactly one E-1 member; the uncovered list is empty. | FR-001, FR-004, SC-001 |
| V-2 | Removing a body from the enumeration still leaves the check red (double-direction assertion). | FR-003, SC-001 |
| V-3 | The fact slugs in `--action list`'s `facts` array equal the `shared/declarations/facts/*.yaml` stems. | FR-002, SC-009 |
| V-4 | Every E-10 member is a pattern; no member is a count. | FR-001, R-6 |
| V-5 | E-1's member set is closed: an unknown class name aborts the run at parse time. | FR-004, FR-009 |
| V-6 | Concurrent condition: `ready >= 2` — the count is computed from E-3 readiness, never from a declaration. | FR-005(a) |
| V-7 | Concurrent condition: no unsatisfied dependency edge among the ready units. | FR-005(b) |
| V-8 | Concurrent condition: write domains pairwise disjoint **or** the body declares a write-isolation form. | FR-005(c), FR-013 |
| V-9 | Concurrent condition: host parallel probe says yes **or** the body uses the external-process form. | FR-005(d) |
| V-10 | Concurrent condition: `min(slot_cap, ceiling, remaining) - verifier_reserve >= 2`. | FR-005(e), FR-015 |
| V-11 | Every serial record carries a non-empty ordered code list drawn from E-7. | FR-006, SC-003 |
| V-12 | The condition↔code bijection has a bidirectional gap of zero. | FR-006 |
| V-13 | Each code's `evidence` matches its `evidence_form`; the shape check is per-code, not "non-empty string". | FR-007 |
| V-14 | Pattern and codes are mutually consistent: concurrent ⇒ empty codes; serial ⇒ non-empty codes. | FR-007, SC-003 |
| V-15 | `effective` is the maximum interval overlap; a missing interval yields `not_evaluated`. | FR-008, SC-006 |
| V-16 | `requested`, `effective` and `effective_reason` are all present together — never one alone. | FR-008 |
| V-17 | Unit ids, layers and dependency edges replay identically from the same inputs and rule id. | FR-010 |
| V-18 | Readiness is answered only by a recorded `verdict=pass` plus an evidence pointer. | FR-011 |
| V-19 | A write unit's write domain is a non-empty file-path set; a directory entry is red. | FR-012 |
| V-20 | A read-only unit's write domain is empty. | FR-012 |
| V-21 | Each unit's `executor_id` and `verifier_id` are both present and different; the two sets are disjoint. | FR-016 |
| V-22 | Integration order equals the declared layer-flattened order and is identical on replay. | FR-017 |
| V-23 | A unit failure leaves unrelated siblings uncancelled and dependents blocked with a recorded reason. | FR-018 |
| V-24 | Re-entry redispatches no settled unit and rebuilds no progress from session memory. | FR-019 |
| V-25 | A declared-`N>=2` body with no capability, no handoff and no external form is red. | FR-021, FR-023, SC-005 |
| V-26 | Team seats with intersecting or **undeclared** territories are red at binding time. | FR-027, spec Edge Cases |

## State machines

### SM-1 — Unit lifecycle

```text
planned --(deps all verdict=pass with evidence)--> ready --(slot available)--> dispatched
dispatched --(terminal status + sentinel)--> settled --(independent verifier)--> verified(pass|fail)
dispatched --(timeout|budget exhausted)--> failed
verified(fail) --(one retry with a material delta)--> ready | split(<depth 1>)
failed --(second failure or split-child failure)--> stage-failed
```

Rules: `settled` is not `verified`; a unit never enters `verified` from `dispatched` directly; `split` children
inherit the attempt count and are never split again (070 § 5, cited not restated).

### SM-2 — Decomposition decision per stage

```text
auto --gate admit + >=2 packages + benefit--> decomposed
auto --otherwise--> single-package(reason=not-beneficial)
on   --gate admit + >=2 packages--> decomposed
off  --never--> disabled
gate reject after one repair | gate exit 2 --> fallback(reason=gate-reject | decomposition-unavailable)
```

Rules: the decision record is written even for `disabled` (FR-029, SC-008); `mechanism-not-yet-landed` is a
*reason code on the concurrency reading*, not a decomposition decision, so it never substitutes for one.

### SM-3 — Declaration class resolution

```text
body discovered --(root lookup)--> candidate classes for root
candidate set size == 1 --> class assigned
candidate set size >  1 --> judged by produced shape (FR-004 rule)
produced shape not decidable --> uncovered  (red, no fallback member)
```

### SM-4 — Effective concurrency settlement

```text
intervals for every dispatched unit present  --> effective = max overlap (integer)
any interval missing                          --> effective = not_evaluated
effective < min(slot_cap, ceiling, remaining) --> require effective_reason
```

### SM-5 — Coordinator dispatch adjudication

```text
verdict = allow   --> coordinator definitions gain a dispatch tool; FR-021(a) satisfiable
verdict = forbid  --> dispatch responsibility belongs to the driver/main agent; FR-021(b) required
verdict absent / unreadable --> owner-unavailable (exit 2), never defaulted
```
