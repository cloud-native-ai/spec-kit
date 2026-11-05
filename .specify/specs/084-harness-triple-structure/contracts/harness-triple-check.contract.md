# Contract — `scripts/python/harness-triple-check.py`

**Feature**: 084 Harness 三重结构 | **Date**: 2026-11-05
**Value-domain owner**: `shared/declarations/contract.yaml` (three exit codes; the six reason templates are owned by
`requirements.md` § Shared Strings and referenced here as `[[STR-NNN]]`). This document owns the **action surface and
the judging algorithm** only.

## Clauses

- **C-026** The engine is one file, `scripts/python/harness-triple-check.py`, standard library only, Python `>= 3.8`,
  and **read-only**: it opens no write point of any kind. Its only outputs are stdout/stderr and, when asked, one JSON
  report path given by `--json-out`.
- **C-027** It takes exactly three actions, selected by `--action`: `coverage`, `verify`, `lookup`. Any other value is
  an input error (exit 2). No action runs checks belonging to another action.
- **C-028** Common argument: `--repo <path>` (default: the repository root resolved from the script's own location by
  walking up to the directory that contains `scripts/python/`, never by matching a bare `.specify` component).
  `--format text|json` and `--json-out <path>` are available on all three actions.
- **C-029** **`--action coverage`** recomputes the candidate set on the tree and prints, per candidate: the unit path,
  its disposition (in-scope / excluded-with-reason / unclassified), and — for an in-scope unit — the completeness state
  with the facts it is judged on. It is deterministic: two consecutive runs on one tree print byte-identical output.
- **C-030** Candidate screen: a unit carrier is one of `templates/commands/*.md`, `skills/{external,internal}/*/SKILL.md`,
  `shared/workflow/*.md`. A carrier enters the candidate set when its text contains a reference to a framework-internal
  deterministic engine — a token of the form `scripts/python/<name>.py` or `skills/<layer>/<name>/scripts/<file>`.
  `shared/definitions/*.md` is not a unit and gets no disposition. The screen is a text test on purpose; its
  conservative side is accepted and retired by an exclusion row, never by a second "does it really call it" judgement.
- **C-031** Disposition derivation order is fixed: a declaration naming the unit's carrier path (in `consumers` or
  `former_carriers`) ⇒ in-scope; else an exclusion row naming the unit ⇒ that reason; else `[[STR-013]]`. A unit named by
  both a declaration and an exclusion row is reported as a finding, never resolved by precedence of file order.
- **C-032** **`--action verify`** judges declaration completeness only: subset conformance, required keys, duplicate
  declarations, exclusion-row shape and anchor resolvability, coverage of the candidate set, both-direction consistency
  between declarations and carriers, and residual literals via the reused `duplicate-fact` reading. It MUST NOT re-judge
  any criterion already owned by `validate-requirements.py`, `validate-tasks.py`, `gate-check.py`, `flow-class-check.py`
  or `doc-consistency-check.py`.
- **C-033** Both-direction consistency (part of `verify` and of the coverage reading): every path in a fact's
  `consumers` is actually referenced by that fact's carrier or engine side, and every carrier that references the fact
  is named in `consumers`. The two directions are counted separately so a one-sided green cannot pass.
- **C-034** **`--action lookup`** answers one question without reading raw declarations: `--unit-id <carrier path>`
  prints that unit's disposition plus the slugs and kinds of the facts it is judged on; `--fact <slug>` prints that
  fact's declaration summary (kind, consumers, former carriers, completeness verdict). Exactly one of the two selectors
  is required; both or neither is an input error.
- **C-035** Findings are the closed six of `requirements.md` FR-017, each emitted **verbatim from its template** after
  placeholder substitution; the instance form (separator characters, argument grammar) is owned by that file's § Shared
  Strings and MUST NOT be re-spelled here or in a consumer.
- **C-036** Exit codes: `0` no finding; `1` at least one finding; `2` input error or degraded wiring. A finding is never
  downgraded to a note and never batched into a single "N problems" line.
- **C-037** Degraded wiring: when the declaration layer is absent from the tree under judgement (the legacy client
  project case), the engine prints an explicit exit-2 input-error label naming the missing directory and MUST NOT raise,
  MUST NOT print a traceback, and MUST NOT exit 0.
- **C-038** No model judgement, no network, no subprocess, no environment-dependent branch: the same tree and the same
  declaration set always produce the same verdict. Time, hostname, user and locale MUST NOT appear in the output.
- **C-039** The engine never writes into the tree it judges, and never rewrites a declaration. A run leaves the tree
  byte-identical (checked by comparing a git-status reading before and after in the test module).
- **C-040** Call sites are exactly two — the gate host's opt-in delegation and the contract test (`data-model.md`
  § E-10). No new stage, no new driver phase, no scheduled job.
- **C-041** Every finding has a negative fixture that asserts exit code plus the verbatim instance, and every action has
  at least one positive fixture asserting exit 0 with zero findings. A fixture without its expected pair is not a
  fixture.

## Example invocations (route (b): not executed at plan time)

The engine does not exist on this branch, so none of these was run. Each line is pinned by the contract test named
below; the premises column lists what a later stage must re-measure rather than inherit.

| Example | Pinned by | Premises |
|---------|-----------|----------|
| `python3 scripts/python/harness-triple-check.py --action coverage` | `tests/contract/test_harness_triple_structure.py` (coverage three-state cases) | the engine exists at that path and is mirrored to `.specify/scripts/python/`; exit 0 requires every candidate to be declared or excluded, which is only true **after** batch 1 lands |
| `python3 scripts/python/harness-triple-check.py --action verify --json-out <path>` | same module (reason fixtures) | `--json-out` writes one report and nothing else; the report schema is this contract's, not a separate file's |
| `python3 scripts/python/harness-triple-check.py --action lookup --unit-id shared/workflow/feedback-step.md` | same module (lookup cases) | the unit path resolves on the tree under judgement; the printed summary names slugs and kinds only, never the values |
| `python3 scripts/python/harness-triple-check.py --action lookup --fact <fact-slug>` | same module | the slug belongs to a declaration that exists in the fixture, not to a hard-coded list |
