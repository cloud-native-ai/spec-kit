# Contract: Ownership Map and Zero-New-Machinery Audit

**Feature**: 087 | **Covers**: FR-018, SC-006, SC-008, SC-010
**Contract object**: the ownership relations this feature creates, and the mechanically decidable audit that it
introduced nothing it prohibits. Every clause is judged over the delivered changed-file set (`base..head` plus the
working tree at implementation time).

Clause ids are dense (`OM-01`…`OM-06`) and are cited verbatim by `/speckit.tasks`.

---

## C-47 · OM-01 — Every new fact has exactly one owner, and every consumer reaches it by path

The delivered files MUST satisfy this table. A fact appearing as a definition in two rows of the "consumer" column
is a defect.

| Fact | Owner (definition site) | Consumers (reach by path / anchor) |
|------|-------------------------|------------------------------------|
| Long-run cadence default (30 s) | `shared/guidelines/reporting-obligations.md` | the reporter Template body; the create-team schema note; `coaching-skills` § Dispatch Payload (by anchor only — C-39 forbids the literal); the digest's rendered profile summary; the guard's RO-03 scan |
| Interactive cadence default | `shared/guidelines/progress-reporting.md` | unchanged; the new owner points at it and carries no number of its own |
| Content floor (four elements) | `shared/guidelines/progress-reporting.md` § 汇报内容下限 | the new owner (by anchor), the reporter Template, this contract's C-23 (labels only) |
| Artifact triplet + execution modes | `shared/definitions/subagent-definitions.md` | the new owner, the digest's carrier resolution, the reporter Template |
| Stall threshold numbers | `skills/internal/create-team/references/patterns.md` § Monitoring → Stall Detection | the new owner (by anchor), the supervision report (row identity only) |
| Line state vocabulary | `skills/external/sdd-loop-driver/scripts/line-registry.py` (`STATE_VALUES`, `ACTIVE_STATES`) | the digest's projection (`data-model.md` E7) — quoted, never re-enumerated |
| Registry directory resolution | same engine (`resolve_registry_dir`) | the digest (C-42 restates the order because the script cannot import the engine; that restatement is the one legal duplicate and is marked as such in the script's docstring) |
| Digest cap default | `scripts/python/status-digest.py` (a declared constant) | the digest's rendered `cap=<n>` and the guard's DG-03 proposition — no other file carries the number |
| Digest stale bound default | `scripts/python/status-digest.py` (a declared constant) | the digest's rendered `stale` marker and the age it shows (`data-model.md` E5 `stale_bound`) — this row is the declaration point `SC-005`'s "declared stale bound" resolves to, and no other file carries the number |

*Judged by*: `tests/contract/test_reporting_obligations.py` — a scan set derived **from the delivered files
themselves** (the owner-literal scan's query set is extracted from what landed, not from the author's intention —
the framework's own One-Source-Of-Truth verification rule) must report exactly one definition site per row.

Requirements served: (FR-018, SC-006).

## C-48 · OM-02 — The ownership relation to pre-existing owners is declared, in one direction

Each pre-existing owner this feature touches MUST be recorded with its relation, in exactly one of four forms:
`owns` (the new owner document), `consumes` (reached by path), `amends` (a bounded edit), `preserves` (untouched
because the feature deliberately keeps its clauses). The declared set MUST be:

| Pre-existing owner | Relation |
|--------------------|----------|
| `shared/guidelines/progress-reporting.md` | `consumes` — no clause of it is rewritten (`SC-008`) |
| `shared/definitions/subagent-definitions.md` | `consumes` + one pointer line added |
| `shared/workflow/external-dispatch-recipes.md` | `consumes` + one pointer line added |
| `shared/guidelines/fast-fail.md` | `preserves` — the dispatch injection clause is referenced, never modified |
| `shared/guidelines/user-facing-comprehension.md` | `consumes` — the emitted line is a governed surface |
| `shared/guidelines/confirmation-gates.md` | `preserves` — no gate is added (measured: 27 blocking gates before and after) |
| `skills/internal/create-team/` | `extends` — roster schema note + create step + guard script |
| `skills/external/coaching-skills/SKILL.md` § Dispatch Payload | `amends` — exactly one field, one forbidden class, one return clause (`FR-019`) |

*Judged by*: `feature-ref.md` § Consuming / Consumed Owners carries the same table, and the contract test asserts
the two are consistent (no relation appears in one and not the other).

Requirements served: (FR-013, SC-008).

## C-49 · OM-03 — No new persistent store, channel or registry

The changed-file set MUST introduce:

- no new file under `.specify/state/`, `.specify/memory/`, or any registry directory;
- no new output file written by any delivered script except the reporter's own stream artifact (which is one of the
  triplet files the visibility contract already declares);
- no new environment variable that selects a store (`SPECIFY_LINE_REGISTRY_DIR` and friends are read, never
  introduced).

*Judged by*: `status-digest.py --action guard` proposition RO-13 plus a changed-path audit in
`tests/contract/test_status_digest.py`.

Requirements served: (FR-018).

## C-50 · OM-04 — No scheduler, timer, daemon or third-party dependency

The changed-file set MUST introduce:

- no process spawn in any delivered script (no `subprocess`, `os.system`, `os.exec*`, `os.fork` on a delivery
  path);
- no sleeping loop and no background thread (`threading`, `multiprocessing`, `asyncio` task loops);
- no new entry in `pyproject.toml` dependency lists (the change MAY touch nothing in that file at all).

The cadence is executed by the running flow between its own steps — the same mechanism the progress-reporting
discipline already mandates — so no scheduler is needed or permitted.

*Judged by*: `tests/contract/test_status_digest.py` — an AST-level import and call audit over every delivered
`.py` file, plus a pin on `pyproject.toml`'s dependency lists against the pre-change baseline.

Requirements served: (FR-018, SC-006).

## C-51 · OM-05 — Pre-existing behaviour is the compatibility baseline, measured by name

The feature is additive. The regression criterion is **name-level**: the pre-change node-id set of the affected
suites equals the post-change node-id set for pre-existing tests, and any renaming or removal is named and
justified.

Affected pre-existing suites (measured before the change): `tests/contract/test_progress_reporting.py`,
`tests/contract/test_coaching_dispatch_contract.py`, `tests/contract/test_agent_dispatch_mechanism.py`,
`tests/contract/test_team_territory.py`, `tests/contract/test_improve_team_presence.py`,
`tests/contract/test_team_command_routing.py`.

One suite is expected to change **by design**: `tests/contract/test_coaching_dispatch_contract.py`'s
`REQUIRED_FIELDS` tuple gains `reporting-cadence`. That change is declared here so it is not read later as a
regression; it is the amendment's own test update (`FR-019`).

*Judged by*: the implement-stage baseline/closure name-level diff, plus this clause being the declared expected
delta.

Requirements served: (FR-019, SC-008, SC-009).

## C-52 · OM-06 — The delivered set is auditable as a file list, not as a claim

`feature-ref.md` MUST enumerate the delivered paths. The audit MUST be able to answer "which of these paths is a
scheduler, a store, a channel, a registry?" by reading the list, and the answer MUST be "none".

*Judged by*: `contracts/ownership-map.contract.md` OM-03/OM-04 (C-49, C-50) plus `feature-ref.md` § Delivered
Paths, whose table is the enumerated file list this clause reads.

Requirements served: (FR-018, SC-010).
