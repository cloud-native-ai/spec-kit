# Behavior-Class Evidence — clause halves with no independent artifact (FR-023)

Feature: 104-agents-run · Date: 2026-11-24 · Evidence owner route: FR-023
(`requirements.md`): behavior-class clauses are evidenced by **truth-source text (the pointer
parts pinned by contract tests) + review + the SC-006 mutation drill** — never by claiming that a
contract test covers the runtime behaviour itself.

This file records that route clause by clause. It adds no assertion and replaces no test: the
five contract modules pin presence of the truth-source text; they do **not** exercise a live
dispatch, a live return, a live probe or a live reading.

## Evidence route (declared once for all rows)

| Route leg | What it supplies | Where it lives |
|-----------|------------------|----------------|
| Truth-source text (pinned) | the skill/definition text that would have to be read and followed at runtime | `tests/contract/test_agents_run_skill_wiring.py` (presence pins), `tests/contract/test_agents_run_command_contract.py`, `tests/contract/test_agents_run_docs_contract.py` |
| Review | a reviewing pass reads the same text plus this feature's change set and judges coherence | `/speckit.review` (downstream of this implement stage) |
| SC-006 mutation drill | proves the pinned text is load-bearing: removing a pointer turns its check red and exact restoration turns it green | `test-evidence/mutation-drill.md` (4/4; M3 is the one that fires on a behavior-class clause's text half, C-12) |

Honesty boundary: a green contract module means "the text that governs the behaviour is present
and unaltered", not "the behaviour happened". No row below claims otherwise.

## Clauses and their behavior halves

| Clause | Behavior half (what only execution can show) | Truth-source text (pinned) | Extra evidence |
|--------|----------------------------------------------|----------------------------|----------------|
| C-11 (FR-007) | the presentation actually shown before a dispatch discloses the superagent/root relation, child label and return channel, and stops nothing (disclosure, not gate) | SKILL § Run Mode presentation paragraph; pinned by `test_c11_presentation_discloses_the_role_relation` | review |
| C-12 (FR-008) | the outgoing payload physically carries the seven role fields at dispatch time | SKILL § Dispatch "Role-edge downlink (seven fields, by pointer)"; pinned by `test_c12_downlink_names_the_seven_role_fields` | mutation drill **M3** (deleting the paragraph turns C-12 red; exact restore turns it green) |
| C-13 (FR-008) | the payload physically carries the four pre-existing injections (fast-fail clause verbatim, concurrency duty, reporting duty, re-anchoring digest) | SKILL § Dispatch "Four pre-existing injections (by pointer)"; pinned by `test_c13_four_injections_travel_by_pointer` | review |
| C-15 (FR-010) | a real return carries the five uplink elements; an incomplete return is refused by the parent, not backfilled | SKILL § Report "Five-element uplink (owner by pointer)" + the incomplete rule; pinned by `test_c15_uplink_requires_the_five_return_elements` and the US5 incomplete-return leg | review |
| C-16 (FR-011) | labels are unique per run at runtime; a retry is a new attempt with the old triplet retained; a stale late return is attributed, never consumed as current | SKILL § Dispatch/Report child-label convention; pinned by `test_c16_child_label_reuses_the_dispatch_convention`; engine-side fixture: `tests/contract/test_agents_run_multi_child_edges.py` (two labels → two edges; label collapse → one edge; retry keeps both triplets) | fixture reading + review |
| C-18 (FR-016) | the probe is actually invoked only for SDD-driver assignments and a refusal names the failing half, the source paths and the seat slug | SKILL § Pre-dispatch probe "Applicability" + refusal shape; pinned by `test_c18_sdd_probe_applicability_is_narrowed` | review |
| C-19 (FR-017) | the concurrency reading triple is actually recorded per run (`single-unit`; `not_evaluated` where an interval is absent; never `0`, never estimated); one run never fans out | SKILL § Scope boundary paragraph; pinned by `test_c19_run_stays_a_single_unit_and_records_the_reading` | review |

## FR-to-clause map (the six behavior-class FRs)

- FR-007 → C-11 (presentation disclosure)
- FR-008 → C-12 / C-13 (payload content: seven fields; four injections)
- FR-010 → C-15 (return completeness and the incomplete rule)
- FR-011 → C-16 (runtime label uniqueness, retry-as-new-attempt, stale-return attribution)
- FR-016 → C-18 (probe applicability execution and refusal shape)
- FR-017 → C-19 (reading recording, `single-unit`, `not_evaluated`)

## What would falsify a row

A row's truth-source leg is falsified if its pinned text is removed (the mutation drill shows the
guard mechanism firing for C-12; the same check shape covers the other rows). A row's behavior leg
is falsified only by an observed live run that contradicts the text — for this feature those runs
are the quickstart scenarios S-1…S-6, which are chat instructions executed in the user's agent,
not shell-runnable; their reading is the review's, and none of them is claimed here as executed.
