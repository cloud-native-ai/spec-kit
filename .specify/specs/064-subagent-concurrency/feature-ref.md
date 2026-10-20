# Feature Reference — 064

**Requirement key**: `064-subagent-concurrency`
**Bound Feature**: **Feature 064** — Subagent 并发归属、CLI 能力档案与生命周期解耦（Subagent Concurrency, CLI Profiles, and Lifecycle Decoupling）
**Status at plan**: Draft → **Planned**（`/speckit.implement` 才可进入 Implemented）
**Spec**: `.specify/specs/064-subagent-concurrency/requirements.md`

## 1. Mapping to the Feature Index

| Dimension | Mapping |
|-----------|---------|
| Feature row | `.specify/memory/features.md` row `064` (Draft → Planned at this plan) |
| Feature detail | `.specify/memory/features/064.md` (Latest Review / Key Changes / Implementation Notes already seeded by requirements+clarify; plan appends the design decision pointer) |
| Related features | 058 (loop U0–U6, state spine, sentinels, watcher verdict/exit codes — referenced, not redefined); 061 (`CAPABILITY_MATRIX` — dispatch eligibility owner); 063 (in-flight; CLI-profile provisional scope adjudicated into 064, stream-json/nohup retained there as dependency) |

## 2. Delivered Surface (planned)

| Path | Change | Purpose |
|------|--------|---------|
| `skills/external/sdd-loop-driver/scripts/line-registry.py` | **new** (Python stdlib-only) | Registry/lease/reservation/identity/queue/ownership/resources/archive engine |
| `skills/external/sdd-loop-driver/scripts/watch-target.sh` | extended | Attribution flags (`--line-id/--run-id/--meta`), foreign/stale-run/unattributed filtering, self-test cases; verdicts/exit codes unchanged |
| `skills/external/sdd-loop-driver/SKILL.md` | extended | New H2 `CLI Capability Profiles`; concurrency/lifecycle pointers; envelope/Registry entry points |
| `skills/external/sdd-loop-driver/references/cli/index.md` + `qodercli.md` + `claude.md` + `codex.md` + `opencode.md` + `hermes.md` | **new** | CLI behaviour knowledge (8 dimensions, known/unknown, provenance) |
| `references/dispatch-recipes.md` | extended | Envelope-carrying runner, CLI child PID, reservation-before-dispatch, detach (setsid/nohup), integration protocol pointer |
| `references/stage-prompts.md` | extended | U0.5 registration, U2 profile consult/dispatch record, U4/U5 CLI observation, U6 closure, ingress rules, reattach program |
| `references/watch-model.md` | extended | Attribution layer reference; verdict state machine text unchanged (owner remains §3 + code) |
| `shared/definitions/probe-definitions.md` (+ `.specify` mirror) | one row | Probe Object `skill-sdd-loop-driver-cli-profile` |
| `docs/reference/skills/sdd-loop-driver.md` | extended | Concurrency/lifecycle + CLI profiles entry (references only) |
| `tests/unit/test_line_registry_engine.py` | **new** | Pure-function unit coverage |
| `tests/contract/test_line_registry_contract.py` | **new** | LR-01…LR-13 |
| `tests/contract/test_line_envelope_contract.py` | **new** | EN-01…EN-16 |
| `tests/contract/test_workspace_isolation_contract.py` | **new** | WI-01…WI-21 |
| `tests/contract/test_lifecycle_detach_reattach.py` | **new** | LC-01…LC-18 |
| `tests/contract/test_sdd_loop_driver_cli_profiles.py` | **new** | CLP-01…CLP-17 + Probe Object + docs/mirrors |
| `tests/contract/test_sdd_loop_driver_skill.py` | updated | Pinned H2 set gains `CLI Capability Profiles`; mirror test covers new files |
| `tests/integration/test_two_line_isolation.py` | **new** | Two-line same-sentinel, foreign events, no-line message, no process scan |
| `tests/integration/test_worktree_integration_queue.py` | **new** | Two write lines, overlap/disjoint, `git fsck`, deterministic replay, runtime/mirror once |
| `tests/integration/test_session_kill_reattach.py` | **new** | Detached survival, reattach running/done/dead, zero redispatch |

No new command, skill, daemon, external service, runtime dependency, or model API.

## 3. FR Coverage (68/68)

| FR range | Owning contract clauses |
|----------|-------------------------|
| FR-001…FR-007 | LR-01…LR-13 |
| FR-008…FR-017 | EN-01…EN-16 (FR-016 → EN-15; FR-017 → EN-16/LR-13) |
| FR-018…FR-032 | WI-01…WI-21 |
| FR-033…FR-045 | CLP-01…CLP-17 (FR-044 → CLP-17 + `notes/063-overlap-adjudication.md`) |
| FR-046…FR-059 | LC-01…LC-18 (FR-058 → LC-17/LR-08; FR-059 → LC-18) |
| FR-060…FR-068 | NG-01…NG-13（FR-065 → LR-08/LC-17；FR-067 → NG-13；FR-065 不由 NG 条款承载） |

## 4. Success Criteria Coverage

| SC | Evidence plan |
|----|---------------|
| SC-001 | `test_two_line_isolation` — event attribution diff list is empty; both lines' completion verdicts correct (2/2 = 100%) |
| SC-002 | Ingress fixture — exactly one question per unidentified message; PATH-stub `ps`/`pgrep` invocation count 0; post-answer routing correctness 100% (ambiguous-stop counts as a correct terminal outcome, not an error; correctness = correct outcomes / answered messages) |
| SC-003 | Foreign monitor/PID fixture — state transition count 0; 100% tagged `foreign`; `stale-run`/`unattributed` rows in `test_en_04_classification` and the two-line integration file prove the other non-own classes are also not consumed |
| SC-004 | `test_worktree_integration_queue` — `git fsck --no-dangling` exit 0; commit SHAs present in `git rev-list --all`; overlap rejection 100%; replay comparison = byte-identical `integration-plan` JSON plus identical ordered line_id list |
| SC-005 | `test_session_kill_reattach` — survival 100%, reattach 100%, redispatch 0, branch outcome matches evidence; `orphaned`, `stalled(remote-unreachable)` and `dead` outcomes covered by `test_lc_13_orphan_check_uses_line_evidence`, `test_lc_09_remote_unreachable_not_dead`, and the integration dead branch |
| SC-006 | Profile content check + `feedback-utils.py --action list --contains "cli-profile:qodercli"`; simulated mismatch → exactly 1; no new fact → zero new feedback |
| SC-007 | Existing contract suites + push-stub count 0 + watcher exit-code pin |
| SC-008 | Test matrix + three mutation drills each turning ≥1 test red |
| SC-009 | `test_lr_12_concurrent_registration` — N=12 writers plus an interleaved reader; parse rate 100%, lost 0, duplicate 0, no half-written JSON observed during writes |
| SC-010 | U6 fixture — active residue 0; worktree retained when unmerged; `--once` executed; duplicate start 0 |

## 5. 063 Overlap

Authoritative adjudication: `notes/063-overlap-adjudication.md`. Summary: 064 owns CLI capability profiles (files, schema, observation, probe object, tests); 063 retains throughput work (stream-json default, nohup runner) as a dependency; 063 MUST delete its provisional `FR-044…FR-049` / `CP-01…CP-10` and its `README.md` schema-owner design when merging. No duplicate owner.

## 6. Non-Goals Preserved

No automatic push; no deletion of uncommitted work; no sentinel/watcher verdict/exit-code change; no daemon/external dependency/model API; no cross-machine multi-user coordination beyond the minimal remote fields; no replacement of 061's `CAPABILITY_MATRIX` or 063's throughput scope.
