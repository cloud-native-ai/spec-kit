# Contract — Declaration facts (C-001…C-018)

**Scope**: the eight machine-read fact entries this feature adds under `shared/declarations/facts/`, the registration
surface they must appear on, and the enumeration roots that define the scope closed set. These clauses bind
`scripts/python/concurrency-check.py`, the fact files themselves, and `tests/contract/test_concurrency_declarations.py`.

**Reading conventions**: a clause's normative sentence uses MUST / MUST NOT. `[[STR-NNN]]` refers to this spec's
Shared Strings table. A "fact" always means a file under `shared/declarations/facts/` read through
`scripts/python/declaration_reader.py`.

**Authority boundary**: the *values* are owned by the fact files. This contract owns the **shape and registration
obligations**; it never restates a member list.

---

## A. Declaration facts

- **C-001** — The feature MUST add exactly eight fact files under `shared/declarations/facts/`: `concurrency-class`,
  `serial-reason`, `effective-concurrency`, `concurrency-slot-and-reserve`, `decomposition-coverage`,
  `executor-enumeration-roots`, `concurrency-contract` and `coordinator-dispatch-verdict`. No ninth file is added,
  and no file is placed outside that directory. (FR-002, FR-031, C-016)
- **C-002** — Each fact MUST carry the mandatory keys declared by `required_fact_keys` in
  `shared/declarations/contract.yaml` and MUST use only the `block-subset/v1` YAML subset named by that file
  (`yaml_subset`): block mappings, block sequences and scalars; no flow collections other than the empty forms, no
  anchors, aliases, tags, multiple documents or block scalars. (R-2, FR-031)
- **C-003** — Each fact's `kind` MUST be one of the five members of `fact_kinds` in `contract.yaml`.
  `concurrency-class` and `executor-enumeration-roots` are `mapping`; `serial-reason` is `ordered-operator-table`;
  `effective-concurrency` is `record-schema`; `concurrency-slot-and-reserve` is `threshold`;
  `decomposition-coverage` is `mapping`; `concurrency-contract` and `coordinator-dispatch-verdict` are `mapping` as
  well (both are keyed records, not thresholds). (FR-031)
- **C-004** — `concurrency-class.yaml` MUST own the closed class member set, the class's semantic name ([[STR-002]]),
  and the per-class `obligation`, `unit_form` and `owner_anchor` fields. The decision rule that assigns a body to a
  class MUST be expressed in the fact (not in the engine) as a mapping from `(root_id, produced_shape)` to a class.
  ([[STR-001]], FR-004)
- **C-005** — `executor-enumeration-roots.yaml` MUST carry exactly five roots and MUST express each as a **pattern**,
  never as a member count. Each root MUST name its `class` and its `excluded_layers`. The spec-local
  `<spec-dir>/goal/` and `<spec-dir>/team/` layers MUST be listed under `excluded_layers` (they are 085
  projections, not roots). ([[STR-008]], FR-001, FR-032)
- **C-006** — `serial-reason.yaml` MUST group each member into exactly one of `condition-bound` or `factual`, MUST
  give each `condition-bound` member its FR-005 clause id, and MUST record declaration order as part of the value.
  `single-unit` ([[STR-009]]) and `mechanism-not-yet-landed` ([[STR-010]]) MUST be `factual` members — they
  describe "nothing to run" and "no mechanism yet", not a concurrency condition that failed. ([[STR-003]], FR-006)
- **C-007** — `effective-concurrency.yaml` MUST declare the reading fields `requested`, `effective` and
  `effective_reason`, MUST declare the value domain of `effective` as `integer | not_evaluated`, and MUST state the
  interval-overlap rule as the computation. It MUST NOT declare a second concurrency metric. ([[STR-005]], FR-008)
- **C-008** — `concurrency-slot-and-reserve.yaml` MUST own `slot_cap_default` and `verifier_reserve` and MUST
  name `wp-gate.py --slot-cap-ceiling` as the ceiling's owner by path and check id (`WG-16`). It MUST NOT carry a
  numeric ceiling of its own. (FR-014, FR-015, T-001)
- **C-009** — `decomposition-coverage.yaml` MUST declare, per stage, whether decomposition is the default, and MUST
  state the relation between its own members and the three existing state-spine keys `decomposition`,
  `decomposition_stages` and `decomposition_slot_cap`: the fact is the owner and those keys are projections. A
  fourth place that assigns "which stages decompose" is a defect. ([[STR-007]], FR-029)

## B. Registration and read surface

- **C-010** — "Registered" MUST be judged by the read behaviour of `scripts/python/declaration_reader.py`: a slug is
  registered when `--action get --fact <slug>` exits `0` with a body **and** the slug appears in the `facts` array
  of `--action list`. (EP-003, FR-031)
- **C-011** — An unregistered slug MUST be reported as `owner-unavailable`: the reader exits `1` today; the
  judgement engine MUST translate that into its own `owner-unavailable` verdict with exit code `2`. No consumer may
  default the value when the read fails. (SC-009, R-1)
- **C-012** — A fact whose `fact:` key disagrees with its file stem, or that falls outside the YAML subset, is
  `registration-invisible`: it MUST be reported rather than skipped, and the corresponding judgement MUST be red.
  (R-1, SC-009)
- **C-013** — Removing a fact from the read surface (renaming the file, changing its stem key, or making it
  unparsable) MUST make the dependent judgement report `owner-unavailable` with a named message and a non-zero exit —
  it MUST NOT silently fall back to a default. The mutation test asserts this read behaviour, not the act of
  "unregistering". (SC-009)

## C. Scope and enumeration

- **C-014** — The execution-body universe MUST be derived by enumerating the five roots' patterns at run time. A
  hand-written body list MUST NOT exist anywhere in the repository. (FR-003)
- **C-015** — The enumeration MUST have a drift guard: adding a member to a root without giving it a class MUST make
  the class check red, and removing a member from the enumeration result while keeping the assertion MUST also be
  red (double-direction). (FR-003, SC-001)
- **C-016** — `coordinator-dispatch-verdict.yaml` MUST exist and MUST carry a value from the closed set
  `{allow, forbid}` plus its `authority` and `consequence`. This feature MUST register the surface; it MUST NOT
  write a verdict the owner did not supply. ([[STR-011]], FR-021, T-004)
- **C-017** — `concurrency-contract.yaml` MUST carry the landing discipline ([[STR-006]]): which framework sources
  carry the obligation, that mirrors are regenerated and never hand-edited, and that `templates/` gains obligation
  text but no repository-specific path fact. ([[STR-006]], FR-031, FR-032)
- **C-018** — The same fact MUST be reachable from the framework source (`shared/`) and its runtime projection
  (`.specify/shared/`) by identical content; a hand edit to the projection is a defect, and the mirror check must
  report drift if the two ever differ. (R-11, Constitution XI)
