# Research — Feature 090 Re-Anchoring

**Feature**: 090-re-anchoring | **Date**: 2026-11-09 | **Plan**: [plan.md](plan.md)

Phase 0 answers one question: *what does the pre-landed tree actually contain, and does it match the settled
requirements?* This feature's implementation exists before its spec chain, so research here is **measurement**, not
design. Every reading below was taken on 2026-11-09 against `/cws_data/cloud-native-ai/spec-kit`.

## R1 — Per-surface numbering differs legitimately

`grep -cE '^### [IVXLC]+\. '` reports **21** principles in `templates/constitution-template.md` and **22** in
`.specify/memory/constitution.md`. The live roster carries 13 project-specific principles the template does not, so the
same rule sits at `XXI` in the template (`templates/constitution-template.md:389`) and `XXII` live
(`.specify/memory/constitution.md:490`). `FR-002` constrains the title and the pointer, not the numeral; forcing them
equal would break each document's self-consistency. Recorded as clarify A2 and `governance-landing.contract.md` C-1.

## R2 — Six pointer sites, zero restatement

`grep -rn re-anchoring-definitions.md` outside the spec directory returns the owner page and six consumers:

| Consumer | Anchor |
|----------|--------|
| `skills/internal/manage-constitution/SKILL.md` | `:264` (mandate entry body) |
| `templates/constitution-template.md` | `:408` |
| `.specify/memory/constitution.md` | `:509` |
| `templates/instructions-template.md` | `:108` |
| `.specify/instructions.md` | `:120` |
| `shared/definitions/agent-definitions.md` | `:107` |

Each is a path reference. None copies the tier table or the five-question list, which is `FR-001`'s pointer
obligation and `re-anchoring-faces.contract.md` C-7.

## R3 — The counting pins moved in one batch, and are recomputable

`tests/contract/test_constitution_double_landing.py` carries `TEMPLATE_COUNT = 21` (`:75`), `LIVE_COUNT = 22` (`:80`)
and `COMMAND_COUNT = 14` (`:84`), each with a `# stale-pin update (2026-11-09, 090)` comment.
`DOUBLE_LANDING_WATCHLIST` gained `"Re-Anchoring (不忘初心 · 温故而知新)"` as its ninth entry, and
`test_fast_fail_discipline.py::test_x15` pins `len(entries) == 9`. Critically, `test_x13` **derives** its three expected
values from the artifacts (template roster, live roster, generator `- **MUST include**` block) rather than restating
numerals, so the "same batch" claim can be recomputed after any later amendment without editing a foreign feature's
guard.

## R4 — The gap is ordering, not presence

The protocol states the rule-first object explicitly (`checkpoint-protocol.md:43`: "The audit's primary object is the
RULES, not the goal"), Q1 asks the rules with the eight-rule set inline (`:47`), and the minimal shape prints
`- Q1 rules:` (`:102`). What is missing: no test in `tests/` asserts that ordering. `test_reanchoring_contract.py`
asserts presence; `test_sdd_loop_driver_reanchor.py` asserts part 5, the tiers, the verdicts and the full-reload ban.
A goal-first rewrite of Q1 would leave both green. This is the clarify C-4 tightening of `SC-002` and the single
compliance gap carried by this plan (`contracts/guard-tests.contract.md` C-7).

## R5 — Same-author delegation was unavailable, and that is disclosed

The canonical gate (`.specify/shared/workflow/objective-analysis-gate.md`) delegates fresh-context scoring to
read-only subagents when the scored artifacts were written by the same agent in the same chain. This stage worker has
no dispatch authority, so the Constitution Check reports what it measured and escalates the one Partial row to
Complexity Tracking instead of marking it Pass. The degraded evidence path is stated in `plan.md` § Phase 0 item 6; a
silent pass is the failure this disclosure prevents.

## R6 — The baseline is red before this stage touches anything

`/usr/bin/python3 -m pytest tests/contract/ -q` on the untouched tree:
`49 failed, 6368 passed, 2 skipped in 486.38s` (raw capture:
`test-evidence/plan-contract-baseline-raw.txt`). The failures span 22 modules — 25 in
`test_run_tests_runner_contract.py` alone, one each in `test_confirmation_gates_sweep.py`,
`test_acceptance_premises.py`, `test_neutrality_budget.py` and others. Two sit in
`test_fast_fail_discipline.py`, the module this feature edits:

| Failure | Measured detail | Bearing on this feature |
|---------|-----------------|-------------------------|
| `test_g9_total_equals_frozen_baseline` | `gate total moved from the frozen 23 to 27` | The gate-scan budget is frozen at 23 with zero headroom; unrelated to the four Re-Anchoring guards, which all pass |
| `test_i11_channel_two_mirrors_and_per_tool_copies` | `.qoder/agents/sdd-analysis-worker.agent.md` clause is not byte-identical to the `rewrite_paths` rendering of the owner literal | A rendered per-tool copy carries the un-rewritten `shared/…` form; a pre-existing projection defect, not a Re-Anchoring face |

Consequence: "the suite is green" is unpassable and MUST NOT be written as an acceptance criterion. The only honest
criterion is **no NEW failure** for the four modules in `contracts/guard-tests.contract.md` C-1/C-2, judged against the
name-level baseline captured in the evidence file.

## R7 — The guards are cheap and self-contained

The four modules together: `2 failed, 129 passed in 1.92 s` (the two failures are the pre-existing R6 entries). They
read files and assert; none spawns a subprocess or touches the network, which is what makes EP-001 hold and keeps
`SC-001`/`SC-004` checkable at every stage rather than only at closure.

## R8 — Runtime versions were re-measured, not inherited

`requirements.md` RS-002 requires re-checking the pin before any closure comparison. Measured today:
`/usr/bin/python3 --version` → `Python 3.11.0rc1`; `/usr/bin/python3 -m pytest --version` → `pytest 9.0.3`;
`pyproject.toml:5` → `requires-python = ">=3.8"`. The `PATH` `python3` resolves to a profile virtualenv **without**
pytest (`No module named pytest`), so every command in `quickstart.md` pins `/usr/bin/python3`. That trap is recorded
here rather than discovered at implement time.

## R9 — The requirements artifact has two validator defects, carried to the requirements owner (RESOLVED 2026-11-09)

**Resolved** — both defects were repaired at their owner (`requirements.md`) by commit `ce108516`: SC-001…SC-004 now end with an inline `**Path**: final` marker, and the `### Measurement Sources & Collection Methods` section exists (its four `**SC-00N Source**` lines are what the two decision-tension records resolve against). Evidence: `/usr/bin/python3 .specify/scripts/python/validate-requirements.py .specify/specs/090-re-anchoring/requirements.md` → 0 errors, and `validate-decision-tensions.py` no longer reports `expected-sacrifice-unmapped`. The original finding is preserved below as the dated record; its present-tense wording is read as the state at plan time, not as a live claim.

`validate-requirements.py .specify/specs/090-re-anchoring/requirements.md` reports four `path-marker` errors: `SC-001`
…`SC-004` carry no `**Path**` marker (`final` / `supporting`), which the owner (`shared/workflow/acceptance-hardening.md`
§ Closure Verdict) requires. Sibling specs state it inline, e.g.
`.specify/specs/089-script-interface-contract/requirements.md:255` ends the criterion line with `**Path**: final`.

`requirements.md` also carries no `### Measurement Sources & Collection Methods` section, which
`validate-decision-tensions.py` reads to resolve a tension record's `expected_sacrifice`. Consequence: this plan's two
records cite `SC-002 Source` / `SC-004 Source` in the owner's `<SC-NNN> Source ↓` grammar, and the validator reports
two `expected-sacrifice-unmapped` findings **until that section exists**. Both defects live in the requirements stage's
artifact and are therefore carried as follow-ups (`feature-ref.md` § 7 F-1, F-2), not repaired by a plan write into
another stage's territory.
