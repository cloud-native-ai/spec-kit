# Contract — Settlement Contract (owner page `shared/definitions/superagent-definitions.md` § Termination)

**Consumers**: `/speckit.tasks` turns each clause into task rows; `/speckit.implement` checks each clause off.
**Pinning test**: `tests/contract/test_settlement_contract_definitions.py` (artifact-class text/structure pins against the owner page and its pointers).
**Clause grammar owner**: `shared/definitions/contract-clause-definitions.md` (canonical `**C-NN**` form).
**Owners reached by pointer (never restated here)**: `superagent-definitions.md` § The Relative Role / § Role Edges / § The super↔sub Protocol / § Role-Transition Injection; `subagent-definitions.md` § Three Execution Modes / § External Dispatch Visibility Contract; `.specify/skills/sdd-loop-driver/references/watch-model.md` § 2–3; `shared/guidelines/fast-fail.md`; `shared/guidelines/confirmation-gates.md`.

**Design input for the owner table**: `requirements.md` § Settlement Evidence Matrix and A-3 / A-7 / A-8 / A-10. After implementation the owner page is the single source; every other surface references it.

**C-01** The closed settlement value set is owned here — *artifact-class*.

§ Termination MUST declare exactly one closed set of seven settlement values — `completed`, `failed`, `anomaly`, `cancelled`, `running`, `silent-end`, `unknown` — and MUST classify them as terminal (`completed`, `failed`, `anomaly`, `cancelled`, `silent-end`), non-terminal (`running`) and detection-defect (`unknown`). The two literals `silent-end` and `unknown` are the spec's Shared Strings STR-001 / STR-002 and MUST appear verbatim. No other surface may carry a second value table. (FR-001, A-3)

**C-02** Every value carries a positive-evidence requirement — *artifact-class content / behavior-class discharge*.

§ Termination MUST carry one row per settlement value naming the positive evidence required for that value and the readings that explicitly do **not** constitute it. The rows MUST cover at least: completion = success terminal record **and** independent verification, where the independent-verification mechanism is a closed four-value set — `u4`, `team-verification`, `five-element`, `return-record` (E4 of the data model) — and no mechanism outside it constitutes completion evidence; failure = non-zero terminal record, named failure return, or exit 0 without the required completion evidence **and without an explicit anomaly signal**; anomaly = explicit anomaly signal **with** terminal evidence, and an exit-0 termination carrying an explicit anomaly signal settles `anomaly` (the incomplete-failure reading applies only when no anomaly marker is present); running = a live check performed at settlement time; silent-end = start record + subject gone + all four terminal evidences absent, where for pid-less carriers "the declared wait deadline passed with no return and no live signal" substitutes for the disappearance test (C-25's `--wait-deadline` option, or an attempt's `wait_deadline_s` field); unknown = the unreadable/unparseable pointer set **or** a claimed attempt with no resolvable start record (finding label `start-record-missing`); cancelled = an explicit parent-side cancellation record. (FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, A-7)

**C-03** `silent-end` is an explicit terminal state, not a fallback — *artifact-class*.

§ Termination MUST state that `silent-end` is a named abnormal terminal state for "terminated with no conclusion" and that it MUST NOT be folded into `completed` or `failed`, nor reported as still running; for carriers without a pid it is "the declared wait deadline (C-25's `--wait-deadline` option, or an attempt's `wait_deadline_s` field) passed with no return and no live signal" — the same value's no-pid branch, not a second value. (FR-006, A-7)

**C-04** `unknown` is a detection-defect state, never an ending — *artifact-class*.

§ Termination MUST state that `unknown` is produced only in two readable cases — (a) evidence is unreadable/unparseable, naming the unreadable pointers, or (b) a claimed attempt has no resolvable start record, naming the missing start slot — each carrying its finding label (`unreadable` / `start-record-missing`), that it is not an ending, and that it carries the same "do not claim success" reaction as `silent-end`. (FR-007, FR-010)

**C-05** Attempts and labels — *artifact-class*.

§ Termination MUST preserve the existing rule that each retry is a new dispatch attempt with a new label, the old attempt's artifacts are kept, and a stale attempt's late return is never consumed as the current result. (FR-009, FR-005)

**C-06** Start record or `unknown`; the return channel is not liveness evidence — *artifact-class content / behavior-class discharge*.

§ Termination MUST require that the parent record the attempt identity, carrier, parent identity, start time, optional `wait_deadline_s` / `start_grace_s` and (process carriers) pid into the existing dispatch log directory (the `--logs-dir` root) as the additive `<label>.attempt` record before or at dispatch — C1 reuses its existing four-piece instead of writing a duplicate, and the additive file is FR-033-permitted, not a new storage root — and MUST state that an attempt with no start record cannot prove it existed and settles as `unknown` with the finding label `start-record-missing`, never `completed`. It MUST state that the return channel (including the seven-field `return_channel`) is a child-initiated uplink whose silence is neither liveness nor completion. (FR-010)

**C-07** The parent settles before it reports — *artifact-class content / behavior-class discharge*.

§ Termination MUST require the parent to settle every attempt it opened before its own externally visible completion report, and MUST state that a report which leaves any attempt unsettled is incomplete and cannot claim success. (FR-011, FR-027)

**C-08** Reaction is report / retry / stop, never silent repair — *artifact-class content / behavior-class discharge*.

§ Termination MUST name the three reactions and their constraints: `silent-end`/`unknown` are surfaced as an abnormal report (what was found, why it matters, intermediate artifacts, optional dispositions) and are not re-dispatched as an ordinary failure without a named diagnosis or user ruling; retries are new attempts/new labels with the old evidence kept; stopping a **live** attempt is recorded as `running` + live evidence + stop reason, never as `silent-end`; no silent repair (no fabricated terminal records, no backfilled return fields, no rewritten `.status`/reports/evidence, no deleted evidence, no consumption of stale returns). Stopping/cancelling keeps the existing destructive-action discipline and adds no gate. (FR-023, FR-024, FR-025, FR-026, A-8)

**C-09** Cancellation is explicit only — *artifact-class*.

§ Termination MUST state that `cancelled` comes only from a parent-side explicit cancellation record produced under the existing discipline; process death, early exit or a dropped connection MUST NOT be inferred as cancellation. (FR-008)

**C-10** Contract version and legacy are additive — *artifact-class*.

§ Termination MUST declare the additive field `settlement_version` (STR-004) on every new settlement-bearing record, and MUST state that records without it are annotated `legacy` in settlement/audit output, are never reported as compliant, are never rewritten, and that the annotation alone does not produce a failing exit code. (FR-034, A-10)

**C-11** Virtual and native boundaries — *artifact-class*.

§ Termination MUST state that virtual dispatch is excluded from background settlement (no detachable edge; the parent is the executor) while unfinished virtual work MUST NOT be reported `completed`; and that when the host offers no background native form, the mode is foreground-terminal — the tool return is the termination event and no settlement edge is created. (FR-018, FR-019, A-4, A-5)

**C-12** The violation set is extended additively and closed — *artifact-class*.

§ Role Edges MUST keep its four closed edge violation kinds unchanged, and § Termination MUST declare a closed settlement violation set of exactly three kinds — `settlement-unrecorded`, `settlement-out-of-set`, `settlement-unbacked` — carried by the same owner page. A fourth edge kind or a fourth settlement kind MUST NOT be emitted before a page revision; the settlement judgment face is the same page's engine (`role-edge-check.py`). (FR-028, FR-029, FR-038, A-6)
