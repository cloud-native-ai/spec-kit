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

## C-43 · DG-03 — Bounded by a declared cap, with the omitted count stated

The digest MUST render at most the declared cap of entries. When it truncates it MUST state `omitted=<n>`. The cap
MUST be a declared default in the script and MUST be overridable per invocation. The ordering MUST be deterministic
(active lines first, then descending last-activity time, ties by `line_id` ascending), so the same registry always
yields the same first-N set (`FR-012`).

*Judged by*: `tests/unit/test_status_digest_unit.py` — a 12-entry fixture with cap 5 renders 5 entries and
`omitted=7`; two renders are byte-identical.

## C-44 · DG-04 — Staleness is marked with its age, never presented as current

Each entry MUST show the age of its last observed activity. An entry whose age exceeds the declared stale bound
MUST be marked stale with that age. A digest MUST NOT render a stale entry's data as current (`FR-011`,
`SC-005`).

*Judged by*: `tests/unit/test_status_digest_unit.py` — a fixture entry older than the bound is marked stale and
carries its age.

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

## C-46 · DG-06 — The guard's propositions are the named, mechanically decidable set

`--action guard` MUST judge, and report each with a **named status** (`pass` / `fail` / `not-evaluated` plus a
reason), exactly these propositions:

| Proposition | What it reads |
|-------------|---------------|
| RO-01 | the owner document declares its single-source-of-truth block and its five owned facts |
| RO-02 | scope predicate present and applied to a seeded flow sample with zero unclassifiable cases |
| RO-03 | the owner-literal scan: exactly one definition site of the long-run default in framework sources |
| RO-04 | each team roster (`.specify/teams/*/team.md` or a supplied path) carries a reporter seat or an RS-04 reason, named |
| RO-05 | a captured line set carries the four content-element labels and an explicit blocker field |
| RO-06 | a captured supervision report names every dispatched sub-flow at least once |
| RO-07 | the stall judgement's anchor resolves and no second numeric threshold set exists |
| RO-08 | a captured report contains the three transition classes and their pre-tick timing |
| RO-09 | a captured line set carries the profile field and a recorded profile switch |
| RO-10 | no captured line is interrogative or an approval request |
| RO-11 | a fixture whose tick was suppressed renders a `reporter-failure` line |
| RO-12 | the carrier value recorded in a run record is one of the two legal forms |
| RO-13 | the delivered changed-file set introduces no scheduler/timer/daemon/dependency/store/channel/registry/spine/ledger |

Each proposition MUST be decidable from files on disk with no network and no process spawn. A proposition the guard
cannot decide MUST be reported `not-evaluated` with the reason, and MUST NOT be reported `pass`.

*Judged by*: `tests/contract/test_status_digest.py` — every proposition name appears in the guard's output for a
compliant fixture, and a mutation fixture (seat removed, omission count removed) turns the matching proposition
red.
