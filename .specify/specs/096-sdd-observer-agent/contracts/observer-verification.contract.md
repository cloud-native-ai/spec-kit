# Contract — Observer Verification（验收映射与反例）

Scope: the test modules, fixtures and mutation drills that discharge SC-001…SC-007. Requirements: SC-001…SC-007, FR-001, FR-003, FR-007, FR-009, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020.

## C-01 — SC-001 coverage fixture

Fixture `tests/fixtures/sdd-observer/` builds a stub SDD line (stage sequence read from `shared/declarations/facts/driver-stage-sequence.yaml#/statement`; never restated) with real driver bookkeeping shapes: state spine, runner quartet envelopes, a sentinel-bearing log per stage, checkpoints and a git history. The contract test asserts the journal covers every declared stage with a `stage-start` row, and — on a zero-failure fixture — a `stage-end` row per stage; deleting the journal or one stage's end row turns the test red.

(SC-001, FR-015)

## C-02 — SC-002 pointer resolution and the forgery drill

Every persistent pointer in the fixture journal resolves. A forged row pointing at a nonexistent path and a row carrying an unresolvable commit both make `check` exit `1` with the row named. The drill record lands in `test-evidence/`.

(SC-002, FR-014)

## C-03 — SC-003 non-blocking fixtures

Two fixtures: (a) observer start failure; (b) observer killed mid-run. In both, the simulated line reaches its terminal stage, the spine records `state: failed` with a reason, and no stage verdict text depends on the observer. The red leg: a doctored driver-text sample in which a stage gate requires observer liveness MUST make the structural predicate fail — proving the predicate has teeth.

(SC-003, FR-009, FR-020)

## C-04 — SC-004 objectivity red legs

Three tamper fixtures each make `check` exit `1`: (a) a row with a tenth column `recommendation`; (b) an event literal outside the closed set; (c) a free narrative paragraph in the body. The agent-template test pins the verbatim 「不评价、不建议、不推断」 prohibition.

(SC-004, FR-013)

## C-05 — SC-005 startup order and dual-line isolation

Fixture asserts the first journal row's `observed_at` precedes the first stage-completion row; two parallel lines (two spines, two spec dirs) produce two journals and two instance identities; a second concurrent append on one journal exits `3`.

(SC-005, FR-003, FR-007)

## C-06 — SC-006 boundary structural assertions

(a) The observer template declares exactly the two write surfaces; (b) no observer text grants a path that writes the spine or stage artifacts; (c) `status-digest.py` carries no observer/journal token; (d) a field-set baseline captured before the first implementation commit is stored under `test-evidence/` and the contract test compares the current digest field set against it (empty delta); (e) the driver presents the observer only through the existing `--sub-flow <label>=<triplet-dir>` semantics.

(SC-006, FR-016, FR-017)

## C-07 — SC-007 gap drill

A fixture skips an observation window (an execution settles, the next starts later per the spine record) and asserts one `observer-gap` row naming the window start and end; removing the gap-writing path makes the test red.

(SC-007, FR-013)

## C-08 — Declaration and mirror drift guards

`journal-format.yaml` passes the declaration layer (`harness-triple-check.py` schema checks; reader-completeness read point present in the engine). The skill mirror set (`sync-mirrors.py --check`) and the agent mirror show no NEW drift against the pre-edit baseline in `test-evidence/plan-mirror-baseline.txt`. The four per-tool agent copies exist and are render-produced.

(FR-001, FR-019)

## C-09 — Boundary assertions that must not change

`status-digest.py` is not modified; `shared/guidelines/reporting-obligations.md` is not modified; `references/stage-prompts.md` gains one pointer line only; no new command, skill directory, scheduler, daemon or registry exists; `STAGE_ARTIFACTS` mapping and the stage sequence declaration are unchanged.

(FR-017, FR-018, FR-019)

## C-10 — Test execution through the one runner

Every suite invocation in this feature goes through `bash scripts/bash/run-tests.sh` (targeted selection allowed); the two full-run budget slots stay as the driver declares (implement entry and post-review). No direct interpreter-level test CLI is used.

(SC-001…SC-007)
