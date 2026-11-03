# Contract — Artifact Schemas (the four structured artifacts)

**Status**: designed (this stage); implemented by `/speckit.implement`
**Owner of the schemas**: `shared/workflow/acceptance-hardening.md`. This contract states **where each schema must live**, **what it must be parseable as**, and **the one-source duty** that keeps it from being copied.

## `Path` marker on Success Criteria

- **AS-01**: `requirements.md` SC definition lines MUST carry `**Path**: final` or `**Path**: supporting` as the last token, exactly once per line, for every SC.
- **AS-02**: `scripts/python/validate-requirements.py` MUST judge the marker as a sixth check label named `path-marker`, reported with file and line, and it MUST keep its existing five labels' meanings unchanged.
- **AS-03**: An `execution`-class feature MUST carry ≥1 `final`-path SC; an `expression`-class feature MUST NOT be required to produce one.
- **AS-04**: Any consumer that cannot parse the marker MUST fail as an input error (exit `2`), never as a judgement about the feature.

## Runtime Stack & Dependency Ownership (requirements)

- **AS-05**: `requirements.md` of an `execution`-class feature MUST carry the table with the fixed column set `ID | Capability | Form | Owner | Pin | Joint acceptance | FR` and rows `RS-NNN`.
- **AS-06**: `Form` MUST be drawn from `in-scope` / `signed-contract` / `user-waived`; an `expression`-class feature MAY use `not-required` with a stated reason.
- **AS-07**: `in-scope` MUST satisfy three separately judgeable obligations — (1) its `FR` cell is non-empty and resolves to an FR **defined in this spec**; (2) at least one `tasks.md` row quotes that FR; (3) `verification.md` carries a joint-acceptance row naming that `RS-NNN`. The judgements align with the closed reason set and MUST NOT grow it: a missing or unresolvable `FR` cell is an **input error (exit 2)** — a defect of the artifact, never a `block` about the feature — while a missing task row or a missing joint-acceptance row is `runtime-dependency-not-owned: RS-NNN` ([[STR-011]]), the same reason as the prose-only case. `signed-contract` MUST carry contract path, measured pin and a named joint-acceptance owner or command; a pin recorded from a run transcript is valid only while re-reading its `--version` reproduces it, so at a baseline comparison a mismatch between the freshly read `pytest --version` / `git --version` and the recorded pin makes **that comparison invalid** (input error, exit 2) and MUST NOT be read as new failures (obligation owner: `requirements.md` FR-023). `user-waived` MUST cite the user ruling and the residual risk.
- **AS-08**: A capability whose provider is external to this repository MUST NOT be recorded `in-scope`; a capability that has only prose and no row MUST be reported as `runtime-dependency-not-owned: RS-NNN` ([[STR-011]]; the canonical spelling is owned by `requirements.md` § Shared Strings).

## Execution Premises and Inherited Blockers (plan)

- **AS-09**: `plan.md` of an `execution`-class feature MUST carry `§ Execution Premises` with the fixed column set `ID | Premise | Evidence | Status | Decision`, `Status` drawn from `verified` / `unverified` / `falsified`, and `Decision` present and drawn from `resolve-in-scope` / `fallback` / `user-waiver` whenever `Status` is `falsified`.
- **AS-10**: `plan.md` MUST carry `§ Inherited Blockers`, whose rows name `<feature>:<row>` for every extracted dependency record and disposition it as `resolved` / `inherited` / `not-applicable` with evidence. The three dispositions' obligations are owned by `requirements.md` FR-011; the one this contract points at is `inherited`: it MUST name a runtime-reachable `Carrier` (a task row of the same slice plus its test module, or a mandatory gate) and that carrier MUST NOT be a deferrable `supporting`-path SC. A missing, unresolvable, or deferrable-carrier `inherited` row is judged exactly as an undisposed row, under the same reason (`inherited-blocker-undisposed: <feature>:<row>`, [[STR-013]]) — the closed set does not grow.
- **AS-11**: Every FR that consumes a runtime capability MUST cite a premise ID; a known negative conclusion MUST NOT be recorded as an out-of-scope note instead of a `falsified` premise.
- **AS-12**: The A13 boundary MUST be stated once in the owner and referenced: plan premises = planning-time facts; plan inherited blockers = dependency-inherited records; `tasks.md` § Environment Prerequisites = task-generation probe verdicts (each with probe command and ISO date). The same fact in two of the three carriers is a defect; the second occurrence MUST be converted into a pointer.

## One-source duty for the new schemas

- **AS-13**: The column names, value domains and thresholds of AS-01…AS-12 MUST appear in exactly one place — the owner document — and every template, command, skill and driver doc MUST reach them by path plus section anchor.
- **AS-14**: A guard test MUST mechanically derive the literal set from the owner's tables and assert that, across `templates/` and `shared/`, the number of non-owner occurrences equals an explicit exemption list (zero un-exempted hits). The exemption list MUST be enumerated in the test, never inferred.
- **AS-15**: The plan skeleton for these two tables lives in `templates/plan-template.md` (so every future plan has the columns), while the schema semantics stay in the owner; the skeleton MUST NOT carry the domains or the invalid-row rules.

## Traceability

| FR | Clauses | Test |
|---|---|---|
| FR-001 | AS-01…AS-04 | `tests/contract/test_requirements_checker.py`, `test_closure_acceptance_check.py` |
| FR-009 | AS-05…AS-08 | `tests/contract/test_acceptance_premises.py` |
| FR-010 | AS-09, AS-11 | `tests/contract/test_acceptance_premises.py` |
| FR-011 | AS-10 | `tests/contract/test_acceptance_premises.py` |
| FR-012 | AS-08, AS-09, AS-10 | `tests/contract/test_acceptance_premises.py` (four findings through `pre-analyze-check.py`) |
| FR-019 | AS-12, AS-13 | `tests/contract/test_acceptance_premises.py` |
| FR-022 | AS-13, AS-14, AS-15 | `tests/contract/test_acceptance_schema_ownership.py` (SC-009 ④) |
| FR-023 | AS-07 (a transcript-recorded pin is valid only while re-reading it reproduces it; a mismatch invalidates the comparison as an input error) | `tests/contract/test_acceptance_premises.py` (pin-validity case) |
| FR-025 | AS-14 (deterministic verdict only), `contracts/gate-wiring.contract.md` GW-08 | `tests/contract/test_acceptance_premises.py` |
