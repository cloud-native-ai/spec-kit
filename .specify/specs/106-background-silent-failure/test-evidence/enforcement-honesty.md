# Enforcement Honesty Boundary — US5 (T032, spec 106)

Rule owner: `shared/definitions/superagent-definitions.md` § Termination. Pinning
clause: `contracts/enforcement-and-migration.contract.md` C-34 (behavior-class clauses
are named as such and MUST NOT be claimed as contract-test coverage; FR-041, A-2).

This record separates two kinds of evidence and never mixes them:

1. **Machine readings** — things the contract modules actually assert and that would go
   red if the asserted surface broke (subject to the T025 mutation record, which proves
   the settlement guards *can* go red).
2. **Behavior-class register** — the closed set of clauses C-34 names. Each is discharged
   by truth-source text plus review / mutation evidence (and a reverse fixture where one
   exists), and **none is claimed as machine coverage**. A text pin in a contract module
   pins wording, not behavior, and is labeled as a text pin wherever cited.

The register below follows C-34's closed enumeration; C-34 owns the membership and the
count — this file does not extend, narrow or re-count it.

## 1. US5 turn-green and machine readings

| Reading | Command | Real output |
|---------|---------|-------------|
| Migration module green | `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_migration.py -q` | rc **0**, `8 passed in 6.30s` |
| Legacy fixture audit | `role-edge-check.py --action settle … --logs-dir tests/fixtures/settlement/legacy/logs` | rc **0**; `legacy-run` `verdict=completed`, `legacy=true`, `claim.settlement_version=null`, `violations=[]` |
| Versioned fixture audit | same, `…/versioned/logs` | rc **0**; `versioned-run` `verdict=completed`, `legacy=false`, `claim.settlement_version=1`, `violations=[]` |
| Mirrors | `.venv/bin/python scripts/python/sync-mirrors.py --check` | rc **0** — six pairs byte-identical (templates 23 / skills/external 394 / skills/internal 139 / agents 20 / scripts 132 / shared 116 files); **0 new** drift members vs the T001 baseline |
| Command copies | `.venv/bin/python scripts/python/regen-command-copies.py --check` | rc **0**, `OK: all per-tool command copies match the source templates.` |
| Rendered surfaces | `specify render-agents --ai qoder` | rc **0**, `rendered 25 agent(s) for qoder; unmapped intents on 25 agent(s)` |
| Touched pair byte-equality | `cmp` on engine, owner, subagent-definitions and recipes source↔mirror | rc **0** each |

The only files changed for US5 outside the spec tree are the three docs pages (T030, no
mirror) and the generator-produced surfaces (T031). No source of truth was edited by
hand to fake a reading.

## 2. Behavior-class register (C-34 closed set)

| # | Clause (as C-34 names it) | Truth-source text (owner locus) | Discharge evidence | Machine coverage claim |
|---|---------------------------|---------------------------------|--------------------|------------------------|
| 1 | FR-005 — settlement-time freshness of a live check | owner § Termination, `running` positive-evidence row: “A live check performed at settlement time …”; negative row: “a stale reading; ‘it was alive last time’; a check that was not performed” | reverse fixtures exist for the *branches* (live pid, zombie, pid-reuse: `test_settlement_carriers.py`), and T025 drill 2 removed the liveness requirement and turned 4 tests red; the wall-clock freshness intent itself is review evidence | **not claimed** — the branch behavior is muted-tested, the “performed now, not stale” intent is behavior-class |
| 2 | FR-010 — parent writes the attempt record; return-channel silence is neither liveness nor completion | owner § Termination, “Start record or `unknown`; the return channel is not liveness evidence”; `run-agent/SKILL.md` § C4 native settlement obligation (“Attempt record before hand-off”, “Wait deadline”) | the *writing* half is machine-tested through the real `dispatch.sh` (`.attempt` before launch, TERM/INT/HUP `.end`); the “silence is not evidence” half is review plus the stale-return reverse leg (`test_retry_is_a_new_label_and_the_old_attempt_keeps_its_value` asserts the old attempt keeps `claim: None` when a stale return appears) | **partially claimed** — record writing and stale-return non-consumption are asserted; the parent-side reading discipline is behavior-class |
| 3 | FR-011 — parent settles before it reports | owner § Termination, “The parent settles before it reports”; `run-agent/SKILL.md` § Reaction obligations, “Settle before reporting” | text + review of the reaction block; the ordering is an agent-behavior duty with no machine oracle | **not claimed** |
| 4 | FR-023 — reaction reporting (item by item, no aggregate success voice) | `run-agent/SKILL.md` § Reaction obligations, “Per-attempt reporting”; owner § Reactions | T021 reaction drill (`test-evidence/reaction-drill.md`): both attempts appear as separate uplink entries with values and evidence counts; review of the report wording | **not claimed** — the drill observes the consequence, the duty is behavioral |
| 5 | FR-024 — retrying `silent-end`/`unknown` requires a named diagnosis or the user's ruling | `run-agent/SKILL.md` § Reaction obligations, “Retry precondition” | text + review; no scripted actor exercises an ordinary re-dispatch by default | **not claimed** (text pin only where a test quotes the sentence) |
| 6 | FR-025 — stopping a live attempt records `running` + live evidence + reason | owner § Reactions “stop” bullet; `run-agent/SKILL.md` § Reaction obligations, “Stop” | the engine half is machine-tested (`running` requires a live check; T025 drill 2); the recording act is review evidence | **not claimed** — engine derivation is muted-tested, the recording discipline is behavioral |
| 7 | FR-026 — no silent repair (no fabricated terminal record, no backfill/rewrite/delete, no stale-return consumption) | owner § Reactions; `run-agent/SKILL.md` § Reaction obligations, “No silent repair” | engine-side guards are machine-tested (zero-write runs with tree-hash equality in T028/T021; AST scan forbidding write/kill/delete/push in `test_settlement_scope.py`); the parent-agent side is review; T026's meta-mutation proves the scan can go red | **partially claimed** — engine read-only behavior is asserted; agent conduct is behavior-class |
| 8 | FR-027 — every opened attempt is covered in the parent report | `run-agent/SKILL.md` § Reaction obligations, “Per-attempt reporting” / “unsettled … 未结算” | T021 reaction drill record; review | **not claimed** |
| 9 | FR-017 “success voice” half — no aggregate success tone may cover a non-success attempt | `skills/internal/create-team/SKILL.md` § Report; `run-agent/SKILL.md` § Reaction obligations | wording pinned by text pins in `test_settlement_carriers.py`; the rhetorical duty is review evidence | **not claimed** — text pin only |
| 10 | FR-030 — the mutation-drill execution duty | `contracts/enforcement-and-migration.contract.md` C-30 | `test-evidence/mutation-drill.md`: four drills each turned named tests red (3 / 4 / 3 / 1 failing nodes), every mutation restored byte-identically (sha256 + empty `git diff`); the T026 meta-mutation adds a fifth red proof for the scope guard | **not claimed as product coverage** — the drill is its own execution evidence |

Reading of the register: items 2, 6 and 7 have one half each that is genuinely
machine-tested (record writing, engine derivation, engine read-only), and those halves
are named as such; none of the ten items is presented as fully machine-covered, and no
contract test is described as proving any behavior-class clause end to end.

## 3. Boundary against the other C-34 sentence

“Behavior-class clauses MUST be named as such in the contracts and quickstart”: the
contract file labels the C-34 set, and `quickstart.md` S-1/S-3/S-5 mark their behavioral
expectations (“after implementation …”) rather than presenting them as asserted
outcomes. This record is the third surface: the itemized register above, with its
per-item machine-coverage verdict.
