# 092 measurement corpus — the 35 A–H entries (T041)

Source: `.specify/specs/092-non-disposable/notes/input-review-080-090.md` (the A–H review, 2026-11-09).
Tier and reproduction source are read from `.specify/specs/092-non-disposable/plan.md` § A–H Corpus Mapping,
which owns both the per-entry expansion and the tier column. This note is the **flat list** a repair run
reads while working: one row per entry, with the reading that reproduces it. It restates no predicate — the
owner page § Detection Categories owns those.

Counts: A 6 · B 5 · C 4 · D 6 · E 6 · F 5 · G 3 · H 3 = **35**; 档 I **19** (A1–A6, B1–B5, C1–C4, G1–G3),
档 II **15** (D1–D6, E1–E6, F1–F5, H1–H2), excluded **1** (H3).

| ID | Sev | Class | Tier | What reproduces the reading |
|----|-----|-------|------|-----------------------------|
| A1 | CRITICAL | `status-unreadable` | I | 089 `verification.md` gains the machine-readable per-SC block + smoke record; the registry row is reconciled against `closure-acceptance-check.py`'s verdict |
| A2 | CRITICAL | `false-closed-set` | I | 084's `unclassified 0` claim is completed (the reading is taken from the engine, not the claim); `harness-triple-check.py --action verify` is the reproduction used by `quickstart.md` § 1 |
| A3 | HIGH | `status-unreadable` | I | 090's registry row moves `Planned` → its closure-consistent value (closure is `accept`, 4/4 SC); the contradiction is what the check reports |
| A4 | HIGH | `status-unreadable` | I | 089 `tasks.md` structural errors (`[US*]` labels in a non-story phase) are completed as records so the status block and the task structure agree |
| A5 | HIGH | `status-unreadable` | I | 085 `plan.md` decision-tension records are completed to the owner's six-field form (`dtr-rejected-form` ×3) |
| A6 | HIGH | `status-unreadable` | I | 080 gains the post-081 common schema fields (`**Path**:` markers, `smoke_command`) — a record completion, not a conclusion change |
| B1 | HIGH | `superseded-live` | I | 086 `contracts/runner-contract-086.contract.md` § C-016 gains the superseded marker + pointer to `089/contracts/mirror-projection.contract.md`; the guard `tests/contract/test_run_tests_runner_contract.py` `…_byte_identical` is retired or replaced in the same change |
| B2 | HIGH | `superseded-live` | I | 085 `contracts/temporary-goal-team.md` / `checkpoint-and-agents.md` follow the owner (`create-mode.md`, `checkpoint-protocol.md`): `team/<slug>/team.md` and the five-part checkpoint |
| B3 | MEDIUM | `superseded-live` | I | 067 `contracts/runner-contract.md` "Serial is the default" is superseded by 086's parallel default: marker + pointer, old text retained |
| B4 | MEDIUM | `orphan-path` | I | 088 `efficiency-model.md` § evidence-path names `final-failed.txt` while the closure reading is `final-failed-r6.txt`; by clarify OI-3 the file exists → `superseded-live`/`correct`, the original text retained in the disposition record |
| B5 | MEDIUM | `orphan-path` | I | the two-slot evidence path has three spellings (owner, 085, 086): one owner spelling + pointers; the other two become pointers in the disposition record |
| C1 | HIGH | `renumber-live-binding` | I | 089 `requirements.md:12` `Feature ID: 086`, `tasks.md:3,5` headers, `feature-ref.md:7,12,78` → 089 |
| C2 | HIGH | `renumber-live-binding` | I | 089 `tasks.md` T081's live instruction to edit "features.md (086 row)" / `features/086.md` → the 089 row |
| C3 | HIGH | `renumber-live-binding` | I | 089 `team/086-script-interface-contract/` directory name and `name: SDD Temporary Team 086` → the 089 slug (a directory rename, `git mv` semantics) |
| C4 | MEDIUM | `renumber-live-binding` | I | 088's eight contract headers `**Feature**: 087`, the main team name and the dogfood slug → 088 |
| D1 | HIGH | `multi-owner` | II | 081 `requirements.md:136,156` + `contracts/state-vocabulary.contract.md:17`; the owner is `shared/workflow/acceptance-hardening.md` — the repair is 081's own body |
| D2 | HIGH | `multi-owner` | II | 081's closed reason set: one owner (the owner doc's seven-member set), the requirements table and `tasks-081b.md:232` become pointers — 081's body |
| D3 | HIGH | `multi-owner` | II | `harness-triple-definitions.md:41-59` vs `084/requirements.md:143`: two mutually exclusive forms of the "goes to yaml" criterion — the owner doc's body |
| D4 | HIGH | `multi-owner` | II | 088's reporter cadence 15 min vs 30 s across `create-mode.md`, `reporting-obligations.md`, `progress-reporting.md` — 088's body |
| D5 | HIGH | `multi-owner` | II | 090's "rule anchor eight members" four spellings (`re-anchoring-definitions.md` §1.1/§1.2/§3, `RULE_SET`) — 090's body |
| D6 | MEDIUM | `multi-owner` | II | 082 / 083 adjacent criteria with no declared precedence (`self-explanatory-definitions.md`, `mechanism-policy-definitions.md`) — the two owners' bodies |
| E1 | HIGH | `false-closed-set` | II | 083 `requirements.md:160,186,220` scope self-contradiction (FR-011 vs FR-026) — 083's body |
| E2 | HIGH | `false-closed-set` | II | 083's three "baseline" values and `post_change == baseline` — 083's plan/verification bodies |
| E3 | HIGH | `false-closed-set` | II | 083's "first-class principle" absent from the roster — 083's body |
| E4 | HIGH | `false-closed-set` | II | 089's `applicable + exempt == candidates` identity (`367 + 737 ≠ 751`, tasks `:23,38`) — 089's body |
| E5 | MEDIUM | `false-closed-set` | II | 084 exclusion rows 8 vs 38 (`requirements.md:203` vs `contracts/migration-batches.contract.md:132`) — 084's bodies |
| E6 | MEDIUM | `false-closed-set` | II | 087 Overview contradicts its own clarify ruling (`requirements.md:37` vs `:41,155,301`) — 087's body |
| F1 | HIGH | `stale-constant` | II | the decomposition ceilings: **value owner measured** = `decomposition-check.py` `FR_CEILING`/`TASK_CEILING` (pinned to `admission-check.py` by `test_sdd_loop_driver_gates.py:67-68`), already pointed at from `efficiency-model.md:300`; the remaining hits are dated records and delivered bodies that quoted a then-current value (`080/077/079/069b/069/082`) → shift to those lines, **not** rewritten here |
| F2 | HIGH | `stale-constant` | II | `scripts/bash/generate-instructions.sh:100` declares `38400` under a reason block deriving `37888`, with two self-contradicting subtractions — a delivered script body, shift to it (the 090 review already carries the same defect) |
| F3 | MEDIUM | `stale-constant` | II | constitution roster counts copied into plans (17/18 vs live 22 / template 21) — each copying body |
| F4 | MEDIUM | `multi-owner` | II | feature-total arithmetic stale (76→77 vs 85) and 080's spec dir registered under ID 062 — the registry's own body |
| F5 | MEDIUM | `stale-constant` | II | 083's skill counts disagree (15+38 vs 54 vs 16+38) — 083's body |
| G1 | HIGH | `superseded-live` (guard side) | I | 090's ordering guard lost its only positional comparison: `tests/contract/test_sdd_loop_driver_reanchor.py` gains the additive goal-first mutation leg (asserts red) — a first-round repair |
| G2 | MEDIUM | `superseded-live` (guard side) | I | the `first_no = "1"` / `assert first_no == "1"` tautology is replaced by an assertion that reads the actual first item; the class is `superseded-live`, not `deferral-marker` — a guard that asserts a constant against itself cannot red when the subject moves, which is the superseded-body-asserted-by-a-live-guard shape C-104 defines. `deferral-marker` stays reserved for retention wording with no expiry condition (C-105 / C-106) and is proven by construction only |
| G3 | MEDIUM | `superseded-live` (guard side) | I | `RULE_SET` omits ⑧ and splits ①, so deleting "report discipline" cannot red — the set is completed against the owner's rule anchor |
| H1 | HIGH | `orphan-path` | II | 086 writes the mirror as `.specify/skills/external/...` (a directory that never existed) — 086's body |
| H2 | MEDIUM | `orphan-path` | II | 082's nonexistent session file; 085 GATE-1's nonexistent `test-evidence/final-failed.txt` — those bodies |
| H3 | LOW | — (recorded exclusion) | excluded | `.specify/.tmp/086-*` historical measurement paths are **legitimate history** (FR-020's third legitimate duplicate); registered as an exclusion, never as a finding |

## Raw source rows (group by group)

### A. Status and verdict self-contradiction

- `A1` — **CRITICAL** — 089 is registered `Implemented` while its own closure engine says **block** (`status-claims-implemented-but-blocked`); `verification.md` has no machine-readable block (`SC-###_status=`, `smoke_*=`); **5 tasks still `- [ ]`** (T019/T081/T085/T086/T087)
  - evidence: `089/verification.md:3-22`; `tasks.md:30,140,278,282-284`
- `A2` — **CRITICAL** — 084's core invariant is false: `harness-triple-check --action coverage` reports **3 unclassified candidates**, exit 1, while the spec records `unclassified 0`
  - evidence: `084/requirements.md:219`; `verification.md:70`
- `A3` — **HIGH** — 090 registry says `Planned` although closure is `accept` (4/4 SC)
  - evidence: `.specify/memory/features.md:98`
- `A4` — **HIGH** — 089's tasks artifact fails its own structural gate: **7 errors** (`[US*]` labels in a non-story phase)
  - evidence: `089/tasks.md:416-425`
- `A5` — **HIGH** — 085 decision-tensions is `error`: `dtr-rejected-form` ×3 HIGH
  - evidence: `085/plan.md`
- `A6` — **HIGH** — 080 does not follow the post-081 common schema: **zero `**Path**` markers** (10 errors), no `smoke_command`, yet declares `Flow Class: execution`; 081's audit recorded it "not judged" and never collected it
  - evidence: `080/requirements.md`; `081/verification.md:46`

### B. Supersessions never retired

- `B1` — **HIGH** — 086 C-016 still demands the runner's two carriers be **byte-identical**; 089 replaced that with a declared projection. `cmp` is non-zero — 086's live contract is false on its own carrier; the guard function is still named `…_byte_identical`
  - evidence: `086/contracts/runner-contract-086.contract.md:4,71-73`; `089/contracts/mirror-projection.contract.md:9-13`; `tests/contract/test_run_tests_runner_contract.py:511-537`
- `B2` — **HIGH** — 085 C-007 says the team lands at `.../team/team.md` and the checkpoint has **four parts**; the owner (`create-mode.md`, `checkpoint-protocol.md`) and every landed team use `team/<slug>/team.md` and **five parts**
  - evidence: `085/contracts/temporary-goal-team.md:11`; `085/contracts/checkpoint-and-agents.md:5,12`; `checkpoint-protocol.md:7`
- `B3` — **MEDIUM** — 067's runner contract still says "Serial is the default"; 086 requires parallel default; 067 was never amended
  - evidence: `067/contracts/runner-contract.md:11-15`
- `B4` — **MEDIUM** — 088's evidence-path trap: the owner says closure names land at `<spec-dir>/final-failed.txt`; that path holds the r1 reading (58), the real closure is `final-failed-r6.txt` (27)
  - evidence: `efficiency-model.md:91-92`; `088/final-failed.txt` vs `final-failed-r6.txt`
- `B5` — **MEDIUM** — Two-slot evidence paths have three spellings: owner `<spec-dir>/{baseline,final}-failed.txt`; 085 `test-evidence/full-suite-final-failed.txt`; 086 `test-evidence/{baseline,final}-failed.txt`
  - evidence: three `verification.md`

### C. Renumbering residue (live references, not history)

- `C1` — **HIGH** — 089's authority file still binds `Feature ID: 086`; tasks header `Requirement ID: 086` / `Related Feature: 086`; feature-ref points at `features/086.md` (a different feature)
  - evidence: `089/requirements.md:12`; `tasks.md:3,5`; `feature-ref.md:7,12,78`
- `C2` — **HIGH** — 089 T081 is a **live instruction** to edit "features.md (086 row)" and `features/086.md` — executing it corrupts another feature's record
  - evidence: `089/tasks.md:278`
- `C3` — **HIGH** — 089's team dir is `team/086-script-interface-contract/` with `name: SDD Temporary Team 086` and `slug: 089-…`; `goal-utils run-checks 089-…` reports `team not found`
  - evidence: `089/team/086-…/team.md:2-4`
- `C4` — **MEDIUM** — 088's **eight** contracts all write `**Feature**: 087`; the main team is "SDD Temporary Team 087"; the dogfood slug is `087-reporting-dogfood`
  - evidence: `088/contracts/*.md:3`; `088/team/team.md:2`

### D. Multiple owners for one fact

- `D1` — **HIGH** — 081's status machine has three owners: requirements says the template; contracts/data-model say `acceptance-hardening.md`; the owner doc says itself
  - evidence: `081/requirements.md:136,156`; `contracts/state-vocabulary.contract.md:17`; `shared/workflow/acceptance-hardening.md:3-12`
- `D2` — **HIGH** — 081's closed reason set has two owners: the requirements table itself, FR-022's schema, and tasks' Shared Strings
  - evidence: `081/requirements.md:165,256`; `tasks-081b.md:232`
- `D3` — **HIGH** — 084's "goes to yaml" criterion exists in two mutually exclusive forms in its owner doc, which claims there is only one
  - evidence: `harness-triple-definitions.md:41-59` vs `084/requirements.md:143`
- `D4` — **HIGH** — 088's reporter default cadence has two owners and two values: 15 minutes (progress-reporting) vs 30 seconds (reporting-obligations)
  - evidence: `create-mode.md:105,157`; `reporter.agent.md:50`; `progress-reporting.md:23`; `reporting-obligations.md:45`
- `D5` — **HIGH** — 090's "rule anchor eight members" has four spellings (owner §1.1 seven + 「等」, §1.2 eight, §3 eight, RULE_SET eight-but-different; two instruction surfaces still enumerate)
  - evidence: `re-anchoring-definitions.md:17-18,31-33,57`; `test_sdd_loop_driver_reanchor.py:37-46`; `instructions-template.md:108`
- `D6` — **MEDIUM** — 082 and 083 criteria are adjacent but declare no precedence
  - evidence: `self-explanatory-definitions.md:29-33`; `mechanism-policy-definitions.md:226-234`

### E. Closed-set claims falsified by measurement

- `E1` — **HIGH** — 083's scope contradicts itself: FR-011 forbids touching skills outside the member table, FR-026 requires editing two of them; SC-003's byte-identity claim is therefore false
  - evidence: `083/requirements.md:160,186,220`
- `E2` — **HIGH** — 083's "baseline" has three values (`3ffeb26e` / `28662977` / `58d3dc5b`), and post_change equals baseline so the delta is unreviewable
  - evidence: `083/requirements.md:260`; `verification.md:11,32`; `plan.md:8`
- `E3` — **HIGH** — 083 claims a "first-class principle" that is absent from the constitution roster
  - evidence: `083/requirements.md:144`; `mechanism-policy-definitions.md:3`
- `E4` — **HIGH** — 089's `applicable + exempt == candidates` identity is false: **367 + 737 = 1104 ≠ 751**; no test pins the identity
  - evidence: `089/tasks.md:23,38`; `test-evidence/closure-check.json`
- `E5` — **MEDIUM** — 084 exclusion rows disagree with the tree (8 vs 38)
  - evidence: `084/requirements.md:203`; `contracts/migration-batches.contract.md:132`
- `E6` — **MEDIUM** — 087's Overview contradicts its own clarify ruling (reorganise by diagram vs keep six types + add diagram obligation)
  - evidence: `087/requirements.md:37` vs `:41,155,301`

### F. Constants and counts drift (same critical number hand-written in several places)

- `F1` — **HIGH** — Decomposition ceilings have four values: 081 `40`, 083 `60/80`, 084 `30`, script `120/160`; no owner pointer.
- `F2` — **HIGH** — Instructions budget chain ends at 37888 in the record but the constant is **38400**; the implement stage changed it without a raise record.
- `F3` — **MEDIUM** — Constitution roster copied into plans with stale counts (17/18 vs live 22 / template 21).
- `F4` — **MEDIUM** — Feature total arithmetic stale (76→77 vs 85); Feature 080's spec dir is registered under ID **062** with no 080 row.
- `F5` — **MEDIUM** — 083 skill counts disagree (15+38 vs 54 vs 16+38).

### G. Guards with semantic gaps

- `G1` — **HIGH** — 090's ordering guard **lost its only positional comparison** in the fix round; an additive goal-first mutation stays green
  - evidence: `tests/contract/test_sdd_loop_driver_reanchor.py:142-153`
- `G2` — **MEDIUM** — `first_no = "1"; assert first_no == "1"` is a tautology
  - evidence: `:118-119`
- `G3` — **MEDIUM** — `RULE_SET` splits ① and omits ⑧, so deleting "report discipline" cannot red
  - evidence: `:37-46`

### H. Path and evidence residue

- (H list item) — HIGH: 086 writes the mirror as `.specify/skills/external/...`, a directory that never existed.
- (H list item) — MEDIUM: 082 references a nonexistent session file; 085 GATE-1 points at a nonexistent `test-evidence/final-failed.txt`.
- (H list item) — LOW: `.specify/.tmp/086-*` historical measurement paths (legitimate history).
