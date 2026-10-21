# Requirements Quality Checklist: Snapshot Contract & Cross-Artifact Consistency — Feature 065 / Slice 065a

**Purpose**: Validate the quality, clarity and completeness of the 065a requirements and their cross-artifact consistency before implementation. Every item is a question about the requirement/design text; no item requires running the engine.
**Created**: 2026-10-21
**Feature (Requirement Scope)**: [065a-state-awareness](../requirements.md) — Feature 065
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md), [tasks.md](../tasks.md), [contracts/](../contracts/)

**Note**: This is a **new** checklist. The existing `checklists/requirements.md` quality checklist is intentionally left untouched. `plan.md` and `tasks.md` are consulted only to expose missing, ambiguous or untraceable requirements — not to grade implementation steps.

**Focus**: read-only boundary and `--out`; evidence/verdict semantics; interruption-form slice ownership; `--probe` and `not-dispatched`; contract↔FR/SC↔task traceability and cross-slice boundaries.
**Depth**: Standard · **Audience**: Spec Kit framework maintainer / sdd-loop-driver author
**Traceability**: 37/37 items carry at least one FR/SC/contract-clause anchor or an explicit `[Gap]` / `[Conflict]` / `[Ambiguity]` marker.
**Cap**: 37 items (soft limit 40).

## 1. Read-Only Boundary and the `--out` Exception

- [ ] CHK001 - Is the snapshot's read-only boundary stated as a closed list of forbidden effects (state spine, four-piece signals, Registry, worktree, process signals, commits) rather than a general "read-only" adjective? [Completeness, FR-001, SA-4]
- [ ] CHK002 - Is the read-only guarantee paired with an observable audit definition (which paths or metadata are compared before and after), or is "MUST NOT write" left without a measurement definition? [Measurability, FR-001, T003, T029]
- [ ] CHK003 - Is the `--out` exception fully specified — canonical target boundary (relative paths, symlinks, a `spec_dir` outside `repo`), same-envelope content, atomic write — in the requirements, or only in LS-10? [Traceability, FR-001, SA-4, LS-10]
- [ ] CHK004 - Is "unreadable evidence source" distinguished from "unreadable required input"? FR-003 maps an unreadable source to `missing`, while FR-012 maps an unreadable required input to exit 2. [Conflict, FR-003, FR-012, LS-06]

## 2. Evidence and Verdict Semantics

- [ ] CHK005 - Are `present|missing|na` defined by mutually exclusive criteria, including the never-dispatched case where an evidence source is not expected at all? [Clarity, FR-003, Q2, SN-03, IA-03]
- [ ] CHK006 - Is value-level `unknown` explicitly separated from the status enum and paired only with `present`, with `null` as the sole missing value? [Consistency, FR-003, Q2, SN-03, SN-04]
- [ ] CHK007 - Does the requirements text define the full `watch_verdict` three-state mapping (verdict obtained / unavailable / no active target), and map FR-005's `watch=unavailable` notation to concrete fields? [Completeness, FR-005, Q5, SN-07, LS-15]
- [ ] CHK008 - Is the derived-mapping owner unambiguous, and is the watcher-vs-derived invariant stated once? FR-004 says the mapping is defined by the FR-043 owner document, while data-model §2.2 and IA-06 name FR-004 as the owner; the invariant is repeated in FR-004, SN-08 and IA-05. [Conflict, FR-004, FR-043, IA-06, SN-08]
- [ ] CHK009 - Is the spine-state enum — including `reentry-required` — and the participation of `running`/`retrying`/`done` in the derived ladder consistent with the 058 owner reference, or explicitly declared non-authoritative? [Consistency, FR-004, A-18, stage-prompts owner]
- [ ] CHK010 - Is "无终态" in FR-004 rule (5) and "终态证据" in IA-08 defined by a closed evidence set (exit record, sentinel, spine terminal state)? [Ambiguity, FR-004, IA-08]
- [ ] CHK011 - Are contradictory combinations — sentinel present with `exit≠0`, and sentinel present with a live process and an `ANOMALY:` last line — covered by FR-004/IA-14, or left to implementation precedence? [Edge Case, FR-004, FR-007, IA-14]
- [ ] CHK012 - Is FR-007's "INCOMPLETE semantics" for sentinel-present/artifact-missing distinguished from a literal `loop_state=INCOMPLETE`, given FR-004 can retain FAILED/DEAD, and is `false_completion` defined as the inverse of `artifacts-without-completion`? [Ambiguity, FR-007, FR-004, IA-10, SN-13]
- [ ] CHK013 - Is "same input" in SC-002 defined when the snapshot may call a live watcher or read a moving git HEAD, so two runs are actually comparable? [Ambiguity, SC-002, SN-14]
- [ ] CHK014 - Do FR-005's watcher-unavailable triggers (`ssh 255`, host timeout, script missing) and the `remote-unreachable` interruption form have disjoint definitions, so transport failure is not misclassified? [Consistency, FR-005, FR-009, IA-12]
- [ ] CHK015 - Is the consistency field's name stable — `spine.consistent` in FR-003/SN-05 versus A-3's `spine_consistent` — and is its null/unknown semantics stated? [Consistency, A-3, FR-003, SN-05]

## 3. Interruption Forms and Slice Ownership

- [ ] CHK016 - Is the eight-form closed set declared once with per-form slice ownership, and is 065a's six-form subset plus the vocabulary-only guarantee for the two 065b forms explicit in the requirement body, not only in a clarify note? [Completeness, FR-009, Q1, IA-01]
- [ ] CHK017 - Is the vocabulary-only guarantee for the two 065b forms operationalized (never emitted by 065a, fields and `missing`/`unknown` semantics reserved), or is it unverifiable prose? [Clarity, FR-009, Q1, IA-01]
- [ ] CHK018 - Is FR-012's "all interruption forms" and "concurrent lock and refusal paths" wording reconciled with LS-18's slice-cumulative `--self-test` scope (including the not-implemented refusal envelope in 065a)? [Conflict, FR-012, Q1, LS-18]
- [ ] CHK019 - Is `check-spine` assigned to exactly one downstream slice? feature-ref §2 and plan.md assign 065b, the current execution directive groups it with 065c, and LS-02's `owner=065b|065c` leaves the per-action pairing implicit. [Conflict, LS-02, feature-ref §2, plan.md]
- [ ] CHK020 - Is the salvage-gate mutation drill correctly scoped? 065a evaluates the salvage gate (IA-16), but FR-046's drill deferral sends the salvage drill to 065c. [Consistency, FR-046, IA-16, T026]
- [ ] CHK021 - Is the parent C-area action rule for `stale-signal` (stale and cannot isolate → stop) represented, deferred, or explicitly excluded in 065a's read-only action matrix? [Gap, IA-14, SA-1, FR-009]
  - CHK021 disposition: covered-by requirements.md SA-1 (stale-signal isolation/stop execution deferred to 065c; 065a only emits stale_signals/interruptions)
- [ ] CHK022 - Is `unwatched` defined as "no fresh watchbeat" even when a watcher verdict is present, and is that distinct from watcher-unavailable? [Ambiguity, FR-010, FR-011, IA-08]

## 4. `--probe` and `not-dispatched`

- [ ] CHK023 - Are both `--probe` JSON shapes defined in the requirement body with required/optional keys, shape discrimination, and unknown-field handling, or only in clarify/contract? [Completeness, FR-002, Q3, LS-11]
- [ ] CHK024 - Does FR-002's "probe takes precedence" conflict with LS-13's exit-2 mutual exclusion, and are all probe rejection conditions traceable to FR-002? [Conflict, FR-002, Q3, LS-12, LS-13]
- [ ] CHK025 - Is probe freshness authority defined (probe-provided freshness authoritative, no local recomputation), and is that consistent with SC-002 determinism? [Clarity, LS-11, SC-002]
- [ ] CHK026 - Is the `not-dispatched` predicate's placement before FR-004 rule (6) normative in the requirements, so a never-dispatched line cannot be classified `NO_SIGNAL`? [Consistency, A-14, Q4, IA-03]
- [ ] CHK027 - Does an explicit `--stage` count as dispatch evidence for `not-dispatched`, or is it intent only? IA-03 lists a Registry `stage` but not `--stage`. [Ambiguity, IA-03, LS-07]
- [ ] CHK028 - Is the `missing` vs `na` status mapping specified for a never-dispatched line (four-piece, watchbeat, artifacts, commits) versus a dispatched line with absent files? [Ambiguity, FR-003, IA-03, SN-03]
- [ ] CHK029 - Is the stage-resolution source order complete? Registry is the only stage source after `--stage`, so the "Registry missing but spine/four-piece readable" edge case cannot locate stage-scoped evidence without guessing. [Gap, FR-002, Edge Cases, LS-07]
  - CHK029 disposition: covered-by contracts/loop-state-cli.md C-7 and contracts/interruption-and-action.md C-35/C-36 (--stage → Registry; both absent → stage=null/unknown; Registry missing continues evaluation; dispatched-with-missing-spine → stop)

## 5. Cross-Artifact Traceability and Slice Boundaries

- [ ] CHK030 - Is there an explicit traceability chain from every contract clause (LS/SN/IA/AM) and every sliced FR/SC to tasks/tests, beyond DoD-3's assertion that each clause has a landing? [Traceability, Gap, FR-012, FR-046, AM-01, DoD-3, tasks.md §Requirement Coverage Map]
  - CHK030 disposition: covered-by tasks.md §Requirement Coverage Map + coverage-baseline.txt (accountant: claimed clauses 60, FR 25/25, baseline 495)
- [ ] CHK031 - Is the plan-stage artifact set (AM-02/AM-03) traceable to both the U4 owner list and the plan-owned set, including the conditional `research.md`? [Traceability, FR-006, AM-03, efficiency-model §3.1]
- [ ] CHK032 - Does the checklist-stage mapping encode U4's "newly added checklist file" requirement, or can a pre-existing `checklists/` directory satisfy completeness? [Gap, FR-006, AM-02, AM-05]
  - CHK032 disposition: covered-by contracts/stage-artifact-map.md C-54 (checklist requires a file added/modified since stage_base_commit; pre-existing files do not count)
- [ ] CHK033 - Is "提交齐备" in IA-14 row 5 defined for `commit_required=false` and an unknown commit baseline, so a DONE analyze stage maps to `verify` rather than falling through? [Gap, IA-14, AM-04, AM-08, AM-10]
  - CHK033 disposition: covered-by contracts/interruption-and-action.md C-46 rows 5/6 and contracts/stage-artifact-map.md C-57 (commit_required=false → verify; unknown baseline → verify only for DONE)
- [ ] CHK034 - Is FR-010's driver write-side deferral to 065b stated in the requirements themselves, not only in plan §Slice Landing Notes, so the slice is not judged incomplete for an unimplemented write obligation? [Traceability, FR-010, plan.md]
- [ ] CHK035 - Is the `recover`/`check-spine` refusal envelope's `owner` field unambiguous (one owner per action) and consistent with the slice allocation? [Consistency, LS-02, feature-ref §2]
- [ ] CHK036 - Is the Feature 065 registry-status rule consistent? requirements §Related Feature forbids rewriting the registered status, while plan §Disclosed Deviations and feature-ref §1 record a Draft→Planned transition. [Conflict, requirements §Related Feature, plan.md, feature-ref §1]
- [ ] CHK037 - Is "no new daemon or external dependency" quantified by a concrete dependency/inventory check, so SC-005's zero count is measurable? [Measurability, FR-041, SC-005]

## Notes

- **Gate substitution**: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` accepts only `requirements`, `plan` and `tasks` stages; `--stage checklist` is not a supported choice. The exact command was attempted and rejected, then the checklist was checked by (a) a structure self-check (sequential CHK numbering, item count, question form, traceability ratio) and (b) the closest formal cross-artifact gate, `--stage tasks`, which scans `checklists/*.md` as formal artifacts. Both results are recorded under `test-evidence/checklist-*`.
- **Same-author gate**: the requirements, clarify, plan and tasks artifacts predate this checklist session, so the same-author condition in `.specify/shared/workflow/objective-analysis-gate.md` does not fire; no fresh-context delegation was required.
- **Findings are questions, not edits**: items that expose an upstream conflict (for example CHK008, CHK019, CHK024, CHK036) are recorded here for a later clarify/analyze decision. No requirements, plan, tasks or contract file was modified in this stage.
- **Answering**: mark an item `[x]` when the requirement text (or a ratified clarification) answers it. A "no" answer is a gap to be fixed upstream, not an implementation task.
