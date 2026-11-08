# Contract — Guard Tests

**Feature**: 090-re-anchoring | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)

The four test modules that make the discipline falsifiable, and the one assertion that is still missing.
`FR-010`; `SC-001`…`SC-004`.

## C-1 — Two guards belong to this feature and are named as such

`tests/contract/test_reanchoring_contract.py` (five faces, pointers — `re-anchoring-faces.contract.md`) and
`tests/contract/test_sdd_loop_driver_reanchor.py` (checkpoint part 5, tiers, verdict, minimal shape —
`direction-audit.contract.md`) are this feature's guard surface. Their docstrings MUST describe the defect they guard,
not the mechanism they check.

## C-2 — Two pre-existing guards carry the counting face

`tests/contract/test_constitution_double_landing.py` and `tests/contract/test_fast_fail_discipline.py` are not this
feature's tests, but they carry `FR-010`'s count face (`governance-landing.contract.md` C-4, C-5). Their pins MUST
move in the same commit as the principle.

## C-3 — Guards are pure reads

Every guard listed here MUST read files and assert; none may spawn a subprocess, write a file, or require network. This
keeps the four modules runnable in ~0.2 s and inside EP-001.

## C-4 — A guard must red when its subject breaks

Each clause a guard asserts MUST have a demonstrated failure mode: deleting the surface, renaming the title, or
dropping the part must make the module fail. `test_constitution_double_landing.py`'s C-10 mutation probe already does
this for the watchlist; the Re-Anchoring guards inherit the same obligation.

## C-5 — The face guards do not assert ordering

`test_reanchoring_contract.py` asserts presence and pointers. It MUST NOT be read as evidence for
`direction-audit.contract.md` C-6 (rule-first ordering), because presence of `Q1` is not ordering.

## C-6 — `test_sdd_loop_driver_reanchor.py` asserts structure, not order

It asserts that part 5 exists, that T0/T1/T2 appear, that the three verdict values appear and that the full-reload ban
is stated. It carries no assertion on the order of the five questions.

## C-7 — The ordering assertion (OPEN — this feature's remaining gap)

A guard MUST be added to `tests/contract/test_sdd_loop_driver_reanchor.py` that reds when the audit stops asking the
rules first. Acceptance form:

- **Red control**: with `Q1` reworded to ask the goal, the new assertion MUST fail; with the landed text it MUST pass.
- **Not satisfiable by the existing greens**: neither "the literal `Q1` appears" nor "three verdicts appear" counts —
  both already pass on a goal-first rewrite, which is precisely why the gap survived.
- **Same test**: the rule-order assertion and the "verdict/action precedes the goal restatement" assertion live in one
  test function, per the clarify C-4 tightening of `SC-002`.

**Status**: OPEN. This is the single compliance gap this plan carries (`plan.md` § Complexity Tracking row IV). It is
task work with a red-first obligation, never a plan-time claim.

## C-8 — The baseline is measured, never assumed green

An acceptance run MUST compare against the measured pre-change failure set, not against "green": the contract suite
holds a pre-existing red set (`plan.md` EP-003). The criterion is **no NEW failure** for the four modules named in C-1
and C-2.
