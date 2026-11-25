# Contract — Enforcement & Migration (`role-edge-check.py --action settle`, guards, legacy, tests)

**Consumers**: `/speckit.tasks` turns each clause into task rows; `/speckit.implement` checks each clause off.
**Pinning tests**: `tests/contract/test_settlement_engine.py` (engine behavior), `tests/contract/test_settlement_migration.py` (version/legacy/refusal), `tests/contract/test_settlement_preservation.py` (preserved surfaces + mutation legs).
**Clause grammar owner**: `shared/definitions/contract-clause-definitions.md`.
**Owners reached by pointer**: `superagent-definitions.md` § Termination / § Role Edges; `shared/definitions/script-interface-definitions.md`; `.specify/skills/sdd-loop-driver/references/watch-model.md` § 3 / § 7; `scripts/python/role-edge-check.py` (its own `--help` is the interface owner for flags and exit codes).

**C-25** One deterministic, read-only settlement judgment face — *artifact-class*.

`scripts/python/role-edge-check.py` MUST gain an additive `--action settle` that reads existing carriers plus the additive attempt/end records (C2/C4) and emits one finding per attempt. It MUST remain read-only (zero write points, no temporary files, fixture tree byte-identical after a run) and MUST answer `-h`/`--version` and reject undeclared options before reading. The `report` and `query` actions and their output schemas MUST NOT change (byte-identical JSON on the same input). It MUST declare the settlement boundary inputs as named options — `--live-window N` (default 120 s), `--wait-deadline N` (default 1800 s), `--start-grace N` (default 30 s), all positive-integer seconds — and state the precedence: an attempt record's optional `wait_deadline_s` / `start_grace_s` field overrides the corresponding option for that attempt; otherwise the option value applies, else the built-in default. These are settlement-time parameters, not new carriers or roots (C-28). (FR-005, FR-006, FR-016, FR-018, FR-028, FR-033, A-6)

**C-26** Exit codes carry the three outcomes — *artifact-class*.

`--action settle` MUST use the engine's existing exit codes: `0` = every attempt judged (a correctly derived `silent-end` is a judged attempt, not a violation); `1` = settlement violations found; `2` = `unknown` findings — unreadable/unparseable evidence or a claimed attempt with no resolvable start record — naming the unreadable pointers or the missing start slot. `unknown` MUST never be represented as exit 0. (FR-007, FR-010, FR-029)

**C-27** The violation kinds are closed and additive — *artifact-class*.

The settle action MUST emit only the three settlement violation kinds owned by § Termination — `settlement-unrecorded`, `settlement-out-of-set`, `settlement-unbacked` — in addition to the four unchanged edge kinds where they apply. A new kind MUST NOT be emitted before the owner page is revised. (FR-029)

**C-28** Inputs are the existing carriers plus additive records — *artifact-class*.

The settle action MUST read: the driver four-piece + stage sidecar/spine (C1), the C2 triplet + `.attempt`/`.end`/optional `.settlement`, the C3 seat start records (E2, carrier `c3-team-seat`) + team report mapping rows, and the C4 native attempt records; it MUST NOT introduce a new root concept beyond the existing `--state-dir` / `--teams-dir` / `--logs-dir` roots. The settlement boundary inputs are C-25's `--live-window` / `--wait-deadline` / `--start-grace` options plus the optional attempt-record `wait_deadline_s` / `start_grace_s` fields; they introduce no new root. C5 and C6 contribute no direct reader: C5 is excluded and C6 is constrained to comply through C1/C2. (FR-028, FR-012, FR-017, FR-020)

**C-29** Determinism and repeated-run identity — *artifact-class*.

Two consecutive settle runs on the same unchanged input MUST produce byte-identical output (stable ordering, no clock in the compared payload). If any interval or timestamp is present, it is either input-derived or excluded from the compared portion; the test names the excluded fields explicitly. (SC-002, SC-007)

**C-30** Mutation drill is an evidence obligation — *artifact-class presence / behavior-class execution*.

The implement stage MUST run the four drills — remove/weaken silent-end detection, remove/weaken the liveness requirement, make `unknown` pass (return 0), remove the evidence-pointer requirement — and record for each drill at least one test that turns red, with the command and output under `test-evidence/`. A drill that turns nothing red is a defect of the guard, recorded as such, never softened. (FR-030)

**C-31** Every in-scope carrier has deterministic tests — *artifact-class*.

Each background-detachable carrier in the closed inventory (C1, C2, C3, C4, C6-through-runner) MUST have at least one deterministic fixture that simulates its silent-death form and asserts the settlement value and the reaction, plus a reverse fixture proving a live attempt is not misreported as `silent-end`; C5 MUST assert the exclusion and the foreground-native branch. Missing coverage for a listed carrier is a defect. (FR-031, FR-032, SC-001, SC-005, SC-008)

**C-32** Fixtures and the test entry — *artifact-class*.

New tests MUST run through `scripts/bash/run-tests.sh` (targeted set `targeted-set-v1`; on this host with `SPECKIT_PYTHON=/usr/local/bin/python3`, the measured interpreter premise), use committed fixture trees or `tmp_path` builders and event-based waits (no fixed `sleep`), and MUST NOT add a third full-suite slot. The same fixture MUST yield the same settlement on repeated runs (difference count 0). (FR-032, SC-007, A-14)

**C-33** Legacy / migration — *artifact-class content / behavior-class discharge*.

Records without `settlement_version` MUST be annotated `legacy` in the audit output, MUST NOT be counted as compliant, MUST NOT be rewritten, and MUST NOT cause a failing exit code. A legacy 5-column team-report row is exempt from the `settlement-unrecorded` predicate (C-16) — its empty-by-schema cells are absence of columns, not absence of a claim; it is annotated and exits 0. The single deterministic refusal is `unknown` (exit 2) for unreadable evidence or a missing start record; no pre-built rejection mechanism is added. The incompatible-change ledger for this feature is **empty** (FR-033's allowed-delta set is empty); any future incompatible change MUST carry a migration path or a deterministic refusal plus a test, and MUST NOT leave a silent mixed state. A test MUST assert the ledger is empty and that a versioned vs legacy fixture pair behaves as specified. (FR-034, FR-035, A-10, SC-006)

**C-34** Enforcement honesty boundary — *artifact-class*.

Behavior-class clauses MUST be named as such in the contracts and quickstart and MUST NOT be claimed as contract-test coverage. The closed behavior-class set is: FR-005 settlement-time freshness of a live check, FR-011 parent-settles-before-report, FR-023 reaction reporting, FR-025 stop-on-live recording, FR-026 no-silent-repair, FR-027 per-attempt coverage in the parent report, the "success voice" half of FR-017, and the mutation-drill execution duty of FR-030. Each is evidenced by truth-source text + review/mutation and, where possible, a reverse fixture — never by a text assertion alone. (FR-041, A-2)
