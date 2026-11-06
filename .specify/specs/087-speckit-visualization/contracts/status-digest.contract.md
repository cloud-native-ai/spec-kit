# Contract: Current-State Digest and Guard

**Feature**: 087 | **Covers**: FR-011, FR-012, FR-017, FR-022
**Contract object**: (a) the thin command `templates/commands/status.md` (entry `/speckit.status`) and its
generated per-tool copies; (b) the deterministic script `scripts/python/status-digest.py` with two actions;
(c) their shared reading of existing state.

Clause ids are dense (`DG-01`…`DG-06`) and are cited verbatim by `/speckit.tasks`.

---

## C-41 · DG-01 — One command, one script, two actions, one reading

The entry MUST be a thin command template (`templates/commands/status.md`) that delegates to
`scripts/python/status-digest.py` and carries no logic of its own. The script MUST implement exactly two actions:

- `--action digest` — render the bounded current-state summary;
- `--action guard` — judge the mechanically decidable propositions of the obligation and return named statuses.

Both actions MUST share the same reader functions for state (one reading backs both, per `FR-022`). A second
parser or a second renderer is a defect.

*Judged by*: `tests/contract/test_status_digest.py` — the script exposes both actions; the command template contains
no rendering logic (it names the script path and the delegated action).

Requirements served: (FR-017, FR-022).

## C-42 · DG-02 — The digest is a projection of state that already has an owner

The digest MUST read:

- the line registry entries resolved exactly as
  `skills/external/sdd-loop-driver/scripts/line-registry.py` resolves them (`$SPECIFY_LINE_REGISTRY_DIR`, then
  `$XDG_STATE_HOME/spec-kit/lines`, then `~/.local/state/spec-kit/lines`);
- the per-entry runner triplet paths the entry declares (`status_path` / `log_path` / `heartbeat_path`) for the age
  of last observed activity;
- `<spec-dir>/test-evidence/*.jsonl` only for a stage-row rendering when the entry's line has a spec directory.

It MUST NOT read the spine's Markdown body to recover fields the registry already carries, and it MUST NOT write
anything (`data-model.md` E7; `research.md` RO-06).

*Judged by*: `tests/unit/test_status_digest_unit.py` — a fixture registry is read, and the script is asserted to
open no file for writing.

Requirements served: (FR-011, FR-022).

## C-43 · DG-03 — Bounded by a declared cap, with the omitted count stated

The digest MUST render at most the declared cap of entries. When it truncates it MUST state `omitted=<n>`. The cap
MUST be a declared default in the script and MUST be overridable per invocation. The ordering MUST be deterministic
(active lines first, then descending last-activity time, ties by `line_id` ascending), so the same registry always
yields the same first-N set (`FR-012`).

*Judged by*: `tests/unit/test_status_digest_unit.py` — a 12-entry fixture with cap 5 renders 5 entries and
`omitted=7`; two renders are byte-identical.

Requirements served: (FR-012).

## C-44 · DG-04 — Staleness is marked with its age, never presented as current

Each entry MUST show the age of its last observed activity. An entry whose age exceeds the declared stale bound
MUST be marked stale with that age. A digest MUST NOT render a stale entry's data as current; the bound's declared
default lives in `scripts/python/status-digest.py` (ownership row in
`contracts/ownership-map.contract.md` C-47), and no other file carries the value (`FR-011`, `SC-005`).

*Judged by*: `tests/unit/test_status_digest_unit.py` — a fixture entry older than the bound is marked stale and
carries its age.

Requirements served: (FR-011, SC-005).

## C-45 · DG-05 — A closed exit-status set, and an explicit "nothing running" state

`--action digest` exit statuses, closed:

| Status | Meaning |
|--------|---------|
| `0` | a digest was rendered (an explicit "nothing running" rendering is **not** this status) |
| `3` | nothing active — the declared "nothing active" status, with the explicit `nothing-running` rendering |
| `2` | input error (unreadable registry directory, unparsable entry, bad arguments) |

`--action guard` exit statuses, closed, following the framework's existing convention (`flow-class-check.py`,
`pre-analyze-check.py`): `0` = zero findings, `1` = at least one finding, `2` = input error.

An empty entry set MUST render `nothing-running` with status `3`; it MUST NOT render an empty digest with status
`0` (`SC-005`).

*Judged by*: `tests/unit/test_status_digest_unit.py` — three fixtures (active, empty, unreadable) assert the three
statuses and the `nothing-running` literal.

Requirements served: (FR-011, SC-005).

## C-46 · DG-06 — The guard's propositions are the named, mechanically decidable set

`--action guard` MUST judge, and report each with a **named status** (`pass` / `fail` / `not-evaluated` plus a
reason), exactly the thirteen propositions `contracts/reporting-obligations.contract.md` C-01…C-13 defines. That
file is the propositions' **single owner**; this table is a consumer of it. Each row below names the proposition by
id and states only **what this guard reads** on disk to decide it — it MUST NOT restate what the proposition
asserts, because a second statement of the subject is what constitution XIV forbids.

| Proposition | What this guard reads |
|-------------|-----------------------|
| RO-01 | the owner document's single-source-of-truth block and its owned-fact list |
| RO-02 | a seeded flow sample classified by the owner's predicate (zero unclassifiable cases) |
| RO-03 | the owner-literal scan over the framework sources (one definition site) |
| RO-04 | the roster paths in `FR-006`'s population only (`.specify/teams/*/team.md` plus every path supplied with `--roster`); zero paths supplied ⇒ `not-evaluated` with that reason |
| RO-05 | a captured line set: the four content-element labels plus an explicit blocker field |
| RO-06 | a captured supervision report: one row per dispatched sub-flow |
| RO-07 | the owner document: the threshold anchor resolves, and no second numeric threshold set exists |
| RO-08 | a captured line set: the three transition classes and their pre-tick stamps |
| RO-09 | a captured line set: the profile value recorded per line and the recorded profile switch |
| RO-10 | a captured line set: interrogative / approval-request verbs |
| RO-11 | a fixture whose tick was suppressed: the `reporter-failure` line |
| RO-12 | a run record's carrier value against the two legal forms |
| RO-13 | the delivered changed-file set: scheduler / timer / daemon / dependency / store / channel / registry / spine / ledger sites |

The proposition **ids and their subjects** are owned by C-01…C-13 only. `SC-005`'s (C-44/C-45), `FR-009`'s stall
judgement (RO-07), `FR-020`'s profile fields (RO-09) and `FR-012`'s cap/omitted count (RO-13) are named by their
owning clauses and are **not** propositions of their own; where a proposition reads a value those FRs define, the
owning clause of that value is the one that pins it.

Each proposition MUST be decidable from files on disk with no network and no process spawn. A proposition the guard
cannot decide MUST be reported `not-evaluated` with the reason, and MUST NOT be reported `pass`.

*Judged by*: `tests/contract/test_status_digest.py` — every proposition name appears in the guard's output for a
compliant fixture, and a mutation fixture (seat removed, second cadence literal seeded) turns the matching
proposition red.

The guard's id set MUST equal the C-01…C-13 id set exactly: a fourteenth proposition, or a second id for one of the
thirteen, is a defect. The trigger mechanics are not propositions — `FR-020`'s profile selection is pinned by
`contracts/status-report.contract.md` C-30 and read by `RO-09`, and `FR-016`'s failure line is pinned by C-29 and
read by `RO-11` — so no trigger gets a slot of its own.

Requirements served: (FR-017, FR-022).
