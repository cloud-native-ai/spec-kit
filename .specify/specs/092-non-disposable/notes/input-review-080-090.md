# Input Review — Features 080–090 cross-spec consistency (2026-11-09)

**Role**: this file is a dated **input record** for Feature 092 (Non-Disposable). It is the
validation corpus the feature must be able to *detect and repair*; it is not a spec artifact
and owns no rule. Evidence was produced read-only: deterministic gates across all 11 specs
(validate-requirements, validate-tasks, validate-decision-tensions, pre-analyze,
account-clause-coverage, closure-acceptance-check, harness-triple-check) plus three semantic
reading clusters and seven independently re-measured spot checks.

## Overall verdict

The tree compiles and its test baseline is clean, but the specs are **not one self-consistent
semantic snapshot**. Three systemic causes: (1) a later feature supersedes an earlier one and
the earlier text is never retired; (2) one fact has several owners; (3) renumbering leaves live
self-bindings.

## A. Status and verdict self-contradiction

| Sev | Finding | Evidence |
|---|---|---|
| CRITICAL | 089 is registered `Implemented` while its own closure engine says **block** (`status-claims-implemented-but-blocked`); `verification.md` has no machine-readable block (`SC-###_status=`, `smoke_*=`); **5 tasks still `- [ ]`** (T019/T081/T085/T086/T087) | `089/verification.md:3-22`; `tasks.md:30,140,278,282-284` |
| CRITICAL | 084's core invariant is false: `harness-triple-check --action coverage` reports **3 unclassified candidates**, exit 1, while the spec records `unclassified 0` | `084/requirements.md:219`; `verification.md:70` |
| HIGH | 090 registry says `Planned` although closure is `accept` (4/4 SC) | `.specify/memory/features.md:98` |
| HIGH | 089's tasks artifact fails its own structural gate: **7 errors** (`[US*]` labels in a non-story phase) | `089/tasks.md:416-425` |
| HIGH | 085 decision-tensions is `error`: `dtr-rejected-form` ×3 HIGH | `085/plan.md` |
| HIGH | 080 does not follow the post-081 common schema: **zero `**Path**` markers** (10 errors), no `smoke_command`, yet declares `Flow Class: execution`; 081's audit recorded it "not judged" and never collected it | `080/requirements.md`; `081/verification.md:46` |

## B. Supersessions never retired

| Sev | Finding | Evidence |
|---|---|---|
| HIGH | 086 C-016 still demands the runner's two carriers be **byte-identical**; 089 replaced that with a declared projection. `cmp` is non-zero — 086's live contract is false on its own carrier; the guard function is still named `…_byte_identical` | `086/contracts/runner-contract-086.contract.md:4,71-73`; `089/contracts/mirror-projection.contract.md:9-13`; `tests/contract/test_run_tests_runner_contract.py:511-537` |
| HIGH | 085 C-007 says the team lands at `.../team/team.md` and the checkpoint has **four parts**; the owner (`create-mode.md`, `checkpoint-protocol.md`) and every landed team use `team/<slug>/team.md` and **five parts** | `085/contracts/temporary-goal-team.md:11`; `085/contracts/checkpoint-and-agents.md:5,12`; `checkpoint-protocol.md:7` |
| MEDIUM | 067's runner contract still says "Serial is the default"; 086 requires parallel default; 067 was never amended | `067/contracts/runner-contract.md:11-15` |
| MEDIUM | 088's evidence-path trap: the owner says closure names land at `<spec-dir>/final-failed.txt`; that path holds the r1 reading (58), the real closure is `final-failed-r6.txt` (27) | `efficiency-model.md:91-92`; `088/final-failed.txt` vs `final-failed-r6.txt` |
| MEDIUM | Two-slot evidence paths have three spellings: owner `<spec-dir>/{baseline,final}-failed.txt`; 085 `test-evidence/full-suite-final-failed.txt`; 086 `test-evidence/{baseline,final}-failed.txt` | three `verification.md` |

## C. Renumbering residue (live references, not history)

| Sev | Finding | Evidence |
|---|---|---|
| HIGH | 089's authority file still binds `Feature ID: 086`; tasks header `Requirement ID: 086` / `Related Feature: 086`; feature-ref points at `features/086.md` (a different feature) | `089/requirements.md:12`; `tasks.md:3,5`; `feature-ref.md:7,12,78` |
| HIGH | 089 T081 is a **live instruction** to edit "features.md (086 row)" and `features/086.md` — executing it corrupts another feature's record | `089/tasks.md:278` |
| HIGH | 089's team dir is `team/086-script-interface-contract/` with `name: SDD Temporary Team 086` and `slug: 089-…`; `goal-utils run-checks 089-…` reports `team not found` | `089/team/086-…/team.md:2-4` |
| MEDIUM | 088's **eight** contracts all write `**Feature**: 087`; the main team is "SDD Temporary Team 087"; the dogfood slug is `087-reporting-dogfood` | `088/contracts/*.md:3`; `088/team/team.md:2` |

## D. Multiple owners for one fact

| Sev | Finding | Evidence |
|---|---|---|
| HIGH | 081's status machine has three owners: requirements says the template; contracts/data-model say `acceptance-hardening.md`; the owner doc says itself | `081/requirements.md:136,156`; `contracts/state-vocabulary.contract.md:17`; `shared/workflow/acceptance-hardening.md:3-12` |
| HIGH | 081's closed reason set has two owners: the requirements table itself, FR-022's schema, and tasks' Shared Strings | `081/requirements.md:165,256`; `tasks-081b.md:232` |
| HIGH | 084's "goes to yaml" criterion exists in two mutually exclusive forms in its owner doc, which claims there is only one | `harness-triple-definitions.md:41-59` vs `084/requirements.md:143` |
| HIGH | 088's reporter default cadence has two owners and two values: 15 minutes (progress-reporting) vs 30 seconds (reporting-obligations) | `create-mode.md:105,157`; `reporter.agent.md:50`; `progress-reporting.md:23`; `reporting-obligations.md:45` |
| HIGH | 090's "rule anchor eight members" has four spellings (owner §1.1 seven + 「等」, §1.2 eight, §3 eight, RULE_SET eight-but-different; two instruction surfaces still enumerate) | `re-anchoring-definitions.md:17-18,31-33,57`; `test_sdd_loop_driver_reanchor.py:37-46`; `instructions-template.md:108` |
| MEDIUM | 082 and 083 criteria are adjacent but declare no precedence | `self-explanatory-definitions.md:29-33`; `mechanism-policy-definitions.md:226-234` |

## E. Closed-set claims falsified by measurement

| Sev | Finding | Evidence |
|---|---|---|
| HIGH | 083's scope contradicts itself: FR-011 forbids touching skills outside the member table, FR-026 requires editing two of them; SC-003's byte-identity claim is therefore false | `083/requirements.md:160,186,220` |
| HIGH | 083's "baseline" has three values (`3ffeb26e` / `28662977` / `58d3dc5b`), and post_change equals baseline so the delta is unreviewable | `083/requirements.md:260`; `verification.md:11,32`; `plan.md:8` |
| HIGH | 083 claims a "first-class principle" that is absent from the constitution roster | `083/requirements.md:144`; `mechanism-policy-definitions.md:3` |
| HIGH | 089's `applicable + exempt == candidates` identity is false: **367 + 737 = 1104 ≠ 751**; no test pins the identity | `089/tasks.md:23,38`; `test-evidence/closure-check.json` |
| MEDIUM | 084 exclusion rows disagree with the tree (8 vs 38) | `084/requirements.md:203`; `contracts/migration-batches.contract.md:132` |
| MEDIUM | 087's Overview contradicts its own clarify ruling (reorganise by diagram vs keep six types + add diagram obligation) | `087/requirements.md:37` vs `:41,155,301` |

## F. Constants and counts drift (same critical number hand-written in several places)

| Sev | Finding |
|---|---|
| HIGH | Decomposition ceilings have four values: 081 `40`, 083 `60/80`, 084 `30`, script `120/160`; no owner pointer. |
| HIGH | Instructions budget chain ends at 37888 in the record but the constant is **38400**; the implement stage changed it without a raise record. |
| MEDIUM | Constitution roster copied into plans with stale counts (17/18 vs live 22 / template 21). |
| MEDIUM | Feature total arithmetic stale (76→77 vs 85); Feature 080's spec dir is registered under ID **062** with no 080 row. |
| MEDIUM | 083 skill counts disagree (15+38 vs 54 vs 16+38). |

## G. Guards with semantic gaps

| Sev | Finding | Evidence |
|---|---|---|
| HIGH | 090's ordering guard **lost its only positional comparison** in the fix round; an additive goal-first mutation stays green | `tests/contract/test_sdd_loop_driver_reanchor.py:142-153` |
| MEDIUM | `first_no = "1"; assert first_no == "1"` is a tautology | `:118-119` |
| MEDIUM | `RULE_SET` splits ① and omits ⑧, so deleting "report discipline" cannot red | `:37-46` |

## H. Path and evidence residue

- HIGH: 086 writes the mirror as `.specify/skills/external/...`, a directory that never existed.
- MEDIUM: 082 references a nonexistent session file; 085 GATE-1 points at a nonexistent `test-evidence/final-failed.txt`.
- LOW: `.specify/.tmp/086-*` historical measurement paths (legitimate history).

## What this corpus demands of Feature 092

1. A **history surface** that reads the current worktree's `.specify/{archive,derive,goal,history,memory,project,review,specs,state,teams}` — not git history — and reports: superseded-but-live text, multi-owner facts, false closed-set claims, stale constants/counts, renumber residues, unreadable status records, and deferral markers.
2. A **design-then-confirm** step in `/speckit.history`: review → plan → ask the user before executing.
3. A **no-deferral rule**: "kept though useless" and "outdated but not deleting now" must be detectable states with a mandatory disposition, not silent retention.
4. The A–H rows above are the **validation cases**: the mechanisms must reproduce these detections on this tree and, once the repair lane runs, drive them to zero.
