# Data Model — 106-background-silent-failure（Phase 1）

**Rule owner**: `shared/definitions/superagent-definitions.md` § Termination owns the settlement value set and the per-value evidence requirement. This page owns the record shapes the feature introduces or extends and the invariants the engine enforces; it MUST NOT restate the owner's value/evidence table.

## E1 — Settlement Verdict（结算判定）

| Field | Type | Rule |
|-------|------|------|
| `value` | enum | Closed set owned by § Termination: `completed`, `failed`, `anomaly`, `cancelled`, `running`, `silent-end`, `unknown` (STR-001 / STR-002 are the last two literals) |
| `class` | enum | `terminal`, `non-terminal`, `detection-defect` — owned by § Termination |
| `evidence` | list of pointers | One or more evidence paths/objects; per-value requirement owned by § Termination |
| `derived_at` | ISO-8601 | The settlement-time reading; `running` is invalid without a fresh check at this moment |

A value outside the closed set is `settlement-out-of-set` (E6) — never coerced.

## E2 — Dispatch Attempt（派发尝试记录）

One file per attempt, `<label>.attempt` (JSON object) in the carrier's existing evidence directory.

| Field | Type | Rule |
|-------|------|------|
| `settlement_version` | integer | `1` for every record this feature writes (FR-034) |
| `attempt_id` | string | Equal to the dispatch `label`; unique per attempt; a retry is a new label (FR-009) |
| `carrier` | enum | `c1-fork`, `c2-subprocess`, `c3-team-seat`, `c4-native` (C5/C6 write no attempt record) |
| `parent_identity` | string | The dispatch edge's parent label/root identity |
| `started_at` | ISO-8601 | Recorded before execution starts (C2: before the CLI launches; C3: before seat hand-off — or the same label's existing C1/C2 start evidence when the seat is dispatched through them; C4: before hand-off) |
| `pid` | integer, optional | Process carriers only (C2 wrapper shell; C1 from the pid file) |
| `pid_start_ticks` | integer, optional | `/proc/<pid>/stat` field 22 where available; used for pid-reuse detection |
| `wait_deadline_s` | integer, optional | Per-attempt wait deadline in seconds for pid-less settlement; overrides the settle `--wait-deadline` option (C-25); positive integer |
| `start_grace_s` | integer, optional | Per-attempt start grace in seconds; overrides the settle `--start-grace` option (C-25); positive integer |
| `contract` | string | Pointer literal `superagent-definitions.md § Termination` |

Existing carriers that already record equivalent facts (C1 four-piece, `exec-quant` dispatch records) are **not** duplicated; the engine reads them at their existing paths (E7).

## E3 — Termination Record（终止记录）

`<label>.end` (JSON object), written by the carrier.

| Field | Type | Rule |
|-------|------|------|
| `settlement_version` | integer | `1` |
| `attempt_id` | string | Matches E2 |
| `exit` | integer, optional | Process exit code when a clean exit was observed |
| `signal` | string, optional | The trap-captured signal (`TERM` / `INT` / `HUP`); absent under SIGKILL |
| `ended_at` | ISO-8601 | When the record was written |
| `completion` | enum | `declared` when the carrier itself declares completion (C1 sentinel path), else `absent`; the **independent verification** is E4, not this field |

A missing E3 is not itself a verdict: the engine combines E2 + liveness + deadline (E6 derivation).

## E4 — Completion Declaration / Independent Verification（完成声明与独立核验）

The parent-side verification that upgrades a success terminal record to `completed` (FR-002).

| Field | Type | Rule |
|-------|------|------|
| `mechanism` | enum | `u4` (driver U4 verification — C1), `team-verification` (report `## Verification` — C3), `five-element` (run-agent uplink — C4), `return-record` (the parent verifies a declared-equivalent return — C2's read slot: the child's returned artifact pointers, recorded in the parent-written `<label>.settlement` claim) |
| `evidence` | list of pointers | Must be non-empty; each pointer must resolve |
| `verified_at` | ISO-8601 | Recorded after the verification actually ran |

Mechanism ↔ carrier is closed: `u4` → C1, `return-record` → C2, `team-verification` → C3, `five-element` → C4; C6 settles only through a compliant C1/C2 runner, and no other pairing constitutes completion evidence. The verification evidence is recorded on the claim surface (E5) by the parent — never by the engine and never by `dispatch.sh` — and a missing claim blocks `completed` (INV02), not verdict derivation.

No E4 → a success terminal record settles as `failed` (incomplete), never `completed`.

## E5 — Settlement Claim（结算主张）

A recorded settlement on a claim-bearing surface; two shapes exist because two carriers already have a place to write it.

| Field | Type | Rule |
|-------|------|------|
| `surface` | enum | `attempt-file` (`<label>.settlement`, in the same existing evidence directory as E2/E3 — no new root; written **only by the parent** after its independent verification, never by `dispatch.sh`, never by the engine) or `team-report-row` (`## Execution Detail` row, written by the team run) |
| `attempt_id` / `label` | string | Matches E2 / the dispatched seat label |
| `value` | enum | E1 value (STR-003 `end_state` is the column name on the team report) |
| `evidence` | list of pointers | Required for `completed`; required for `silent-end` to name disappearance + absence evidence |
| `settlement_version` | integer, optional | Absent = **legacy claim**: annotated `legacy`, never counted as compliant, never rewritten, and not judged by any E7 predicate (so it contributes no exit 1) (FR-034, INV08) |
| `claimed_at` | ISO-8601 | When the claim was written |

## E6 — Settlement Finding（判定发现）

The engine's per-attempt row; the only place a derived verdict and a claim audit meet.

| Field | Type | Rule |
|-------|------|------|
| `attempt_id` | string | Unique within one run of the engine |
| `verdict` | E1 | Derived from evidence; claims are audited **against** it, never substituted for it |
| `evidence` | list of `{pointer, kind}` | `kind` ∈ `start` / `live` / `terminal` / `lack` / `claim` / `unreadable` |
| `claim` | object, optional | The E5 snapshot the audit compared against |
| `consistent` | boolean | False when a claim disagrees with evidence (e.g. `completed` claim with no E4) |
| `legacy` | boolean | True when the claim/record carries no `settlement_version` (E5) |
| `unknown_cause` | enum, optional | Present only when `verdict` = `unknown`: `unreadable` or `start-record-missing` (FR-007) |
| `violations` | list of E7 | Zero when the attempt is cleanly settled |

## E7 — Settlement Violation（结算违例，closed）

| Kind | Predicate |
|------|-----------|
| `settlement-unrecorded` | A versioned claim-bearing slot exists with no value (team-report row missing `end_state`/`evidence`; claim file missing `value`); a legacy 5-column row is exempt and only annotated `legacy` (INV08) |
| `settlement-out-of-set` | A recorded value on a version-bearing record is outside E1's closed set |
| `settlement-unbacked` | A recorded value on a version-bearing record lacks its required positive evidence (covers: `completed` without E4; `running` without a settlement-time live check; `silent-end` without start-record + disappearance + absence of all four terminal evidences) |

**Legacy scope**: all three predicates apply only to **version-bearing** records (a claim or record carrying `settlement_version`); a versionless record is annotated `legacy` (E6) and judged by none of them, so it alone never contributes exit 1 (INV08) — the `settlement-unrecorded` row's 5-column exemption is this scope's table-level instance.

`unknown` is **not** a violation kind: unreadable evidence produces E6 rows with `kind: unreadable` and `unknown_cause: unreadable`; a claimed attempt with no resolvable start record produces a `start`-slot `lack` row with `unknown_cause: start-record-missing`; either way the engine exits 2 (the single deterministic refusal, FR-007), and the legacy annotation never suppresses that refusal. The four edge kinds (`self-dispatch`, `dangling-parent`, `unbacked-role-claim`, `depth-inconsistent`) remain closed at the same page and are untouched.

## E8 — Carrier Evidence Map（载体证据映射，C1…C6 closed）

| ID | Attempt/claim carrier | Evidence the engine reads | Attempt record written by |
|----|----------------------|---------------------------|---------------------------|
| C1 | driver stage (fork) | `pid-`, `status-`, `log-`, `heartbeat-<line>-<stage>`; stage sidecar `prompt-*.md.meta.json`; U4/`last_verdict` pointer from the spine/checkpoints | stage-runner (existing four-piece; no new file) |
| C2 | `dispatch.sh` subprocess | existing `.live.log` / `.jsonl` / `.status` + new `.attempt` / `.end` + optional parent-written `.settlement` claim | `dispatch.sh` (attempt/end only; the `.settlement` claim belongs to the parent, E5) |
| C3 | team run report | `## Execution Detail` mapping row + `## Verification` + the seat's E2 `<label>.attempt` (carrier `c3-team-seat`, `started_at` before hand-off) or the same label's existing C1/C2 start evidence | `run-team` seat dispatch (no duplicate when dispatched through C1/C2); the report row remains the E5 claim surface, not the start record |
| C4 | native host subagent | `.attempt` in the existing dispatch log dir + return record / five elements | `run-agent` |
| C5 | virtual | none — excluded; no detachable edge | none |
| C6 | direct recipes | only through a compliant runner (C1/C2 evidence) or foreground-terminal | none extra |

A carrier not in this table is outside the closed inventory (FR-012) and is a specification change, not a silent addition.

## E9 — Reaction Record（反应记录）

| Field | Type | Rule |
|-------|------|------|
| `action` | enum | `report` / `retry` / `stop` (A-8; closed) |
| `attempt_id` | string | The attempt being reacted to |
| `reason` | string | Required; for retry it must name the diagnosis or the user ruling (fast-fail) |
| `new_attempt_id` | string, optional | Required for `retry`; a **new** label, never reused (FR-009/FR-024) |
| `evidence_kept` | list of pointers | Old attempt's evidence that must remain readable after the retry |
| `stopped_while_running` | boolean | `true` only for a live attempt stopped under the existing discipline — record `running` + live evidence + stop reason, never `silent-end` (FR-025) |

## Invariants (INV-series)

- **INV01** A settlement value comes from E1's closed set; nothing coerces an out-of-set value (V: `settlement-out-of-set`).
- **INV02** A `completed` verdict requires E3 success **and** E4 with non-empty resolvable evidence; exit 0 alone is not completion.
- **INV03** A `running` verdict requires a live check performed at settlement time (pid alive, not zombie, start ticks match; or fresh heartbeat; or log growth within the C-25 settlement live window (`--live-window`); or open return channel). A stale reading is not `running`.
- **INV04** `silent-end` requires all three: E2 start record present (C3: the seat's E2 record or the same label's C1/C2 start evidence), execution subject gone (process carriers: recorded pid absent — disappeared, or never appeared within C-25's `--start-grace` / the attempt's `start_grace_s`; for pid-less carriers: the C-25 wait-deadline input — `--wait-deadline`, or the attempt's `wait_deadline_s` — passed with the settlement-time live check finding no live signal), and all four terminal evidences (completed/failed/anomaly/cancelled) absent.
- **INV05** `unknown` is produced only from unreadable/unparseable evidence or from a claimed attempt with no resolvable start record, names the unreadable pointers or the missing start slot with its finding label (`unreadable` / `start-record-missing`), and the engine exits 2 — never 0.
- **INV06** `cancelled` requires an explicit parent-side cancellation record written under the existing destructive-action discipline; process death or a dropped connection is never inferred as cancellation.
- **INV07** Each attempt has one unique label; a retry is a new attempt with a new label; the old attempt's evidence is kept and its late return is never consumed as the current result.
- **INV08** `legacy` records (no `settlement_version`) are annotated `legacy`, never counted as compliant, never rewritten, and not judged by any of E7's three violation predicates — so a legacy record alone never causes exit 1; a 5-column row's absent cells are absent columns, not an unrecorded claim. The exit-2 `unknown` refusal (INV05) is a detection defect, not a judgment, and applies regardless of version.
- **INV09** The engine is read-only: zero write points, no temporary files, and a fixture tree is byte-identical after a run (AST + hash legs).
- **INV10** The same input yields byte-identical `settle` output across consecutive runs (deterministic ordering; no clock in the compared payload).
- **INV11** Existing `.status` line format, sentinel literals, watcher verdict tokens/exit codes and the four-piece names are unchanged (extraction equality vs `fbab7a45c`).
- **INV12** Settlement never widens destructive authority: the engine does not kill, retry, delete evidence, rewrite reports or push; a stop on a live attempt records `running` + stop reason.

## State transitions

```text
attempt started (E2)
  ├─ terminal record: exit≠0 ─────────────────────────────► failed
  ├─ terminal record: exit=0 + explicit anomaly line ─────► anomaly
  ├─ terminal record: exit=0 + sentinel/declaration
  │     ├─ E4 verified ──────────────────────────────────► completed
  │     └─ E4 absent ────────────────────────────────────► failed (incomplete)
  ├─ terminal record: exit=0, no completion declaration ──► failed (incomplete)
  ├─ cancellation record (parent, under gate discipline) ─► cancelled
  ├─ no terminal record + live evidence at settlement ────► running
  └─ no terminal record + subject gone / deadline passed
        + start record + all terminal evidences absent ──► silent-end
unreadable evidence anywhere ─────────────────────────────► unknown (unreadable; exit 2, never a pass)
claimed attempt with no resolvable start record ─────────► unknown (start-record-missing; exit 2)
```

An exit-0 termination carrying an explicit anomaly line is `anomaly`; the incomplete-failure rows apply only when no anomaly marker is present.

A retry starts a **new** `attempt started` transition with a new `attempt_id`; the previous row keeps its verdict.
