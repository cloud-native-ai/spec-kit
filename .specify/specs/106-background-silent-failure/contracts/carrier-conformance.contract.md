# Contract — Carrier Conformance (C1…C6, additive evidence, preserved surfaces)

**Consumers**: `/speckit.tasks` turns each clause into task rows; `/speckit.implement` checks each clause off.
**Pinning tests**: `tests/contract/test_settlement_carriers.py` (carrier surfaces), `tests/contract/test_settlement_scope.py` (closed inventory, zero second mechanism, no second value table).
**Clause grammar owner**: `shared/definitions/contract-clause-definitions.md`.
**Owners reached by pointer**: `superagent-definitions.md` § Termination; `subagent-definitions.md` § Three Execution Modes / § External Dispatch Visibility Contract; `.specify/skills/sdd-loop-driver/references/watch-model.md` § 2–3 / § 9; `skills/internal/create-team/SKILL.md` § Report; `shared/workflow/external-dispatch-recipes.md`.

**C-13** C1 keeps its evidence and only maps verdicts — *artifact-class presence / behavior-class consumption*.

The driver stage dispatch MUST keep `stage-runner.sh`'s four-piece (`pid-`, `status-`, `log-`, `heartbeat-<line>-<stage>`) and `watch-target.sh`'s judgments, exit codes, sentinel literals and `--self-test` unchanged. The feature consumes them and maps: `DONE → completed`, `FAILED → failed`, `ANOMALY → anomaly`, `INCOMPLETE → failed (incomplete)`, `DEAD → silent-end`, `NO_SIGNAL → silent-end`, `TIMEOUT`/`RUNNING → running` when a settlement-time live check holds, else `silent-end` (TIMEOUT with a dead subject and no terminal record). `DONE` remains a candidate that the driver's U4 verification completes; a versioned claim MUST name its U4 evidence pointer. (FR-014, FR-002, A-9)

**C-14** C2 writes additive start/termination evidence — *artifact-class*.

`skills/internal/create-team/scripts/dispatch.sh` MUST write `<label>.attempt` before launching the CLI (attempt id, carrier `c2-subprocess`, parent identity, `started_at`, `pid` = wrapper shell, `pid_start_ticks` where `/proc` is available, `settlement_version: 1`), and `<label>.end` on normal exit and on TERM/INT/HUP traps (`exit`, `signal`, `ended_at`, `settlement_version: 1`). The existing `.live.log` / `.jsonl` / `.status` names and the `.status` line format (`<label> exit=<code>`) MUST remain byte-compatible; the script keeps its `-h`/`--version` guard and undeclared-option rejection. SIGKILL is not trappable and is the intended `silent-end` fixture. (FR-015, FR-016, A-9)

**C-15** C2 settlement follows evidence — *artifact-class content / behavior-class discharge*.

The settlement rules for C2 MUST be: success terminal record **and** verified return → `completed`; non-zero terminal record → `failed`; exit 0 without a completion declaration → `failed` (incomplete); no terminal record + recorded pid gone (or never appeared within the start grace) → `silent-end`; unreadable evidence → `unknown`. (FR-016)

**C-16** C3 records per-seat settlement — *artifact-class*.

The run-report contract (`skills/internal/create-team/SKILL.md` § Report) MUST extend the `## Execution Detail` mapping table with additive `end_state` (STR-003) and `evidence` columns for new reports (7 columns total), and MUST require `## Verification` to declare settlement coverage. The legacy 5-column header MUST remain accepted by the engine and MUST parse as legacy. A row with an empty `end_state`/`evidence` is `settlement-unrecorded`; a `completed` claim without an evidence pointer is `settlement-unbacked`. The report MUST NOT close in a success voice when a seat is `silent-end`/`unknown` (behavior-class, evidenced by review/mutation, not a prose parser). (FR-017, FR-041)

**C-17** C4 leaves a parent-side attempt record — *artifact-class content / behavior-class discharge*.

`skills/internal/run-agent/SKILL.md` MUST require: an attempt record written into the existing dispatch log directory before a native background hand-off (carrier `c4-native`, same E2 shape); settlement on return (five elements complete → verify and settle; missing any element → `failed` (incomplete), not consumed; host error → `failed`); declared wait deadline passed with no return and no live signal → `silent-end`; and, when the host provides no background form, an explicit foreground-terminal declaration with no settlement edge. (FR-018, FR-010)

**C-18** C5 virtual exclusion is written, not implied — *artifact-class*.

`shared/definitions/subagent-definitions.md` § Three Execution Modes MUST state that virtual dispatch cannot detach from the session, that the parent is the executor and no orphan edge exists, that virtual is therefore excluded from background settlement, and that unfinished virtual work MUST NOT be reported `completed`, with a pointer to the settlement owner. (FR-019, A-4)

**C-19** C6 recipes become per-value dispositions — *artifact-class*.

`shared/workflow/external-dispatch-recipes.md` MUST restrict background recipes to (a) a compliant runner/wrapper that produces termination evidence or (b) an explicitly foreground-terminal form (return = termination). The single ambiguous stall sentence MUST be replaced by per-settlement-value dispositions: no sentinel and subject gone/no termination record → `silent-end` (`unknown` when unreadable); no sentinel but subject alive → `running`. (FR-020)

**C-20** The read-only wave settles each validator — *artifact-class presence / behavior-class discharge*.

Recipe 7 (and its result contract) MUST state that each validator attempt is settled and that a missing status/verdict marks that validator `failed` (incomplete) and re-asked under the existing rule — it MUST NOT disappear from the wave result; the settlement owner is referenced by pointer. (FR-021)

**C-21** The observer stays optional — *artifact-class*.

No probe class, handler binding or observer dependency is added; the owner text MUST state that an observer may record settlement facts but MUST NOT be the only settlement carrier, and that a line without an observer still settles. (FR-022)

**C-22** The carrier inventory is closed — *artifact-class*.

The C1…C6 inventory is a closed list. Every dispatch entry (the `/speckit.agents` and `/speckit.team` command templates, the SDD driver stage dispatch, the direct external recipes) and every definition carrying dispatch duty (`run-agent`, `run-team`, `create-team`, `sdd-loop-driver`, the four SDD coordinator templates) MUST reference the same settlement owner; leaf executor templates MUST NOT gain a second settlement logic; no skill/command/template/document/test may carry a second value table, a second evidence matrix or a carrier-private judgment copy. (FR-012, FR-013, A-6)

**C-23** All new surfaces are additive; the preserved set has an empty allowed delta — *artifact-class*.

Existing sentinel literals, watcher judgments/exit codes/`--self-test`, the five-element uplink, the seven-field downlink, the destructive-action discipline and its frozen budget, and the two-slot test budget MUST remain unchanged; every new field/file is additive; the allowed-delta set for all of them is empty. Measurement: an extractor over `watch-target.sh` + its `--help`/`--self-test` output yields three sets (verdict tokens, exit codes, sentinel literals) that equal the `fbab7a45c` baseline member-for-member; the complement assertion is "member difference is empty". (FR-033, SC-003, A-9)

**C-24** Zero second mechanism — *artifact-class*.

The feature MUST NOT add a scheduler, daemon, queue, registry, notification channel, storage root or child list. Attempt records reuse the existing dispatch log directory (already ignored), team settlement rides the existing run report, C1 rides the existing four-piece and sidecar/spine, and the judgment rides the existing engine. (FR-038, A-6, A-13)
