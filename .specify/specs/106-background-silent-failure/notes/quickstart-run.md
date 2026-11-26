# Quickstart Run — S-0…S-7 (T033, spec 106)

Executed 2026-11-26 on branch `106-background-silent-failure` (post-T031), from the
repository root. Every block below quotes the real output of the command above it.
Scratch trees live under the sanctioned, git-ignored `.specify/.tmp/`; teardown is
recorded at the end.

**In-passing correction surfaced by this run (disclosed)**: S-2/S-3 on the live carrier
exposed that the settle engine's C1 pid reader accepted only the bare-integer fixture
shape, while the live `stage-runner.sh` writes `pid=<n> start=<ticks> at=… line=… stage=…
event=pid` (the watcher's own reader accepts exactly that shape first, then a bare
integer). Measured before the fix: `.specify/state` + `.specify/teams` +
`.specify/agents/execution/logs` → `summary attempts=114 violations=0 unknown=112`,
exit **2** — every real stage was a fabricated detection defect instead of a mapped
verdict, contradicting C-13 ("C1 keeps its evidence and only maps verdicts"). The fix
(`scripts/python/role-edge-check.py` `_load_c1_attempt`: `pid=` line first with its
`start=` token as `pid_start_ticks`, bare integer as fallback, anything else still
`unreadable`) was pinned by two new legs in `test_settlement_engine.py`
(`test_c1_reads_the_drivers_pid_line_format`,
`test_c1_pid_line_start_token_detects_pid_reuse`) and the mirror regenerated. Measured
after: the same roots → `summary attempts=114 violations=0 unknown=0`, exit **0**.

---

## S-0 — read the single owner (reading)

`shared/definitions/superagent-definitions.md` line 62 carries the verbatim heading
`**Termination.**` — the section owns the closed seven-value set, the per-value evidence
requirement, the reactions, the version/legacy rule and the three settlement violation
kinds. No other surface reached in this run restates them (the scope guard in S-7 scans
for exactly that).

## S-1 — C2 subprocess silent death (real run)

Command form and measured output:

```text
launcher pid=966182
--- .attempt record (written before the CLI launched) ---
{"settlement_version": 1, "attempt_id": "demo-kill", "carrier": "c2-subprocess", "parent_identity": "root", "started_at": "2026-11-26T03:05:05Z", "pid": 966182, "contract": "superagent-definitions.md § Termination", "pid_start_ticks": 2459856744}
recorded wrapper pid=966182 (launcher pid matches: yes)
fake CLI pid=966199
.end absent before the kill (as expected)
wrapper reported exit rc=137 (SIGKILL, no trap ran)
process-group members left: 0
--- log dir after the SIGKILL ---
demo-kill.attempt
demo-kill.jsonl
demo-kill.live.log
--- settle judgment ---  (rc 0)
  "verdict": "silent-end", "class": "terminal",
  evidence: demo-kill.attempt (start) + demo-kill.end (lack, absent) + demo-kill.status (lack, absent)
  "detail": "pid-gone", "violations": []
summary attempts=1 violations=0 unknown=0
```

Two command-form adaptations, disclosed (scenario intent — “dispatch a fake CLI that
blocks, SIGKILL the wrapper, judge the attempt” — is unchanged):

1. `DISPATCH_CLI_FLAGS="-c 'sleep 300'"` is word-split by the shell before dispatch.sh
   sees it (the literal quotes reach `sh` as separate words), so the quoted form cannot
   block; a four-line blocking fake CLI (stdin-held, `/proc`-free) was used instead —
   the same technique the carrier tests drive the shipped script with.
2. All paths were passed absolute: `dispatch.sh` `cd`s into the workdir, so relative
   log/prompt paths only survive when the workdir is the repository root (the literal
   quickstart command uses `.`; the demo workdir is its own scratch directory).

The wrapper was killed as a process group (`kill -9 -- -<pid>`); the group ended
empty (0 members left), the fake CLI and its pipeline included.

## S-2 — C1 verdict mapping

Run-now part:

```text
$ bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test | tail -1
SELF-TEST: 39 passed, 0 failed

$ grep -oE '"(DONE|RUNNING|ANOMALY|FAILED|DEAD|TIMEOUT|INCOMPLETE|NO_SIGNAL)"' <baseline copy> | tr -d '"' | sort -u
ANOMALY DEAD DONE FAILED INCOMPLETE NO_SIGNAL RUNNING TIMEOUT
$ grep -oE '^EXIT_[A-Z_]+=[0-9]+' <baseline copy> | cut -d= -f2 | sort -n -u
0 2 10 11 12 13 14 15 16
$ grep -oE '[A-Z][A-Z0-9_]*-DONE' test-evidence/watch-help-baseline.txt | sort -u
STAGE-DONE
```

Settle part (now executable):

```text
$ role-edge-check.py --action settle --state-dir tests/fixtures/settlement/c1-state …
attempt demo-line-implement carrier=c1-fork verdict=failed class=terminal consistent=true legacy=false
summary attempts=1 violations=0 unknown=0          (rc 0 — exit=0 terminal without a completion claim = incomplete)

$ … --state-dir <dead-stage variant: sidecar + dead pid, no status record>
attempt qs-dead-implement carrier=c1-fork verdict=silent-end class=terminal consistent=true legacy=false
summary attempts=1 violations=0 unknown=0          (rc 0)
```

Full eight-token mapping is pinned by
`test_settlement_engine.py::test_c1_mapping_function_covers_all_eight_tokens`; the live
carrier shapes (pid line with `start=` token, status line, log tail, heartbeat) are
pinned by the two new C1 legs named in the correction note above.

## S-3 — team seat settlement on the real roots

```text
$ role-edge-check.py --action settle --teams-dir .specify/teams \
    --logs-dir .specify/agents/execution/logs --state-dir .specify/state --format text
attempt background-silent-failure-analyze-final carrier=c1-fork verdict=failed …
…
summary attempts=114 violations=0 unknown=0        (rc 0; 115 output lines)
```

Value distribution (JSON reading of the same run):
`failed 110` (109 `incomplete` absent a U4 claim + 1 `non-zero-terminal`),
`anomaly 1` (`background-silent-failure-clarify`, `anomaly-signal` — its log tail is the
recorded `ANOMALY:` line), `running 1` (`background-silent-failure-implement-p4`,
`live-check` — this executing attempt's consumer process is alive at settlement time),
`silent-end 2` (`decision-governance-analyze-r4`/`-r5`, `start-grace-expired`).
The team report rows contributed no violation; the two fixture-level C3 readings (5-column
legacy annotated / 7-column clean audit) are in S-4 and the carriers module.

## S-4 — legacy vs versioned audit

```text
$ … --logs-dir tests/fixtures/settlement/legacy/logs
attempt legacy-run carrier=c2-subprocess verdict=completed class=terminal consistent=true legacy=true
summary attempts=1 violations=0 unknown=0          (rc 0 — annotation, not a refusal)

$ … --logs-dir tests/fixtures/settlement/versioned/logs
attempt versioned-run carrier=c2-subprocess verdict=completed class=terminal consistent=true legacy=false
summary attempts=1 violations=0 unknown=0          (rc 0)
```

Pinning test: `test_settlement_migration.py::test_legacy_annotated_not_compliant` (and
the seven sibling legs).

## S-5 — green run of the settlement judgment modules

```text
$ SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
    tests/contract/test_settlement_engine.py tests/contract/test_settlement_carriers.py -q
57 passed in 6.47s                                  (rc 0)
```

Mutation evidence: `test-evidence/mutation-drill.md` (four drills red 3/4/3/1, restored
byte-identically; T026 meta-mutation included).

## S-6 — preserved surfaces

```text
$ bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test | tail -1
SELF-TEST: 39 passed, 0 failed

$ sha256sum skills/external/…/watch-target.sh .specify/…/test-evidence/watch-target-fbab7a45c.sh
955ddf7820a80cb3afad5af25877f2f8d7093e4fb08c46ec59dfe948ec3f2479  (both — identical)

$ python3 scripts/python/scan-confirmation-gates.py --root . --json | head -3
{ "total": 30, …    (EP-005: the frozen ==27 equality was already red at base — live 31;
                     this feature measures zero NEW hits on touched files, owner page 0 ≤ 1)

$ role-edge-check.py --action report --state-dir …/qs-probe/state --teams-dir … --logs-dir … --registry-dir …/none
{… "summary": {"edges": 0, "executors": 0, "violations": 0, "conflicts": 0}}   (rc 0)
probe tree removed: yes
```

## S-7 — mirrors, copies and the six-module battery

```text
$ .venv/bin/python scripts/python/sync-mirrors.py --check
ok six pairs, byte-identical; rc 0
$ .venv/bin/python scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.   (rc 0)

$ SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
    tests/contract/test_settlement_contract_definitions.py tests/contract/test_settlement_engine.py \
    tests/contract/test_settlement_carriers.py tests/contract/test_settlement_migration.py \
    tests/contract/test_settlement_preservation.py tests/contract/test_settlement_scope.py -q
100 passed in 23.48s                                (rc 0)
```

No third full-suite slot was consumed (the two-slot ledger is unchanged; this battery is
targeted).

## Teardown

- `rm -rf .specify/.tmp/settlement-demo` — the only tree S-1/S-4 created; removed.
- `.specify/.tmp/qs2` (S-2 dead-stage scratch) and `.specify/.tmp/s3-text.txt` (S-3
  capture) removed.
- `.specify/.tmp/sdd-loop/tmp/background-silent-failure/qs-probe` — removed inside S-6
  and verified absent.
- Nothing outside `.specify/.tmp/` was touched by the demo commands; the read-only
  settle/report runs left the repository tree unchanged (`git status` shows only the
  intended P4 edits).
