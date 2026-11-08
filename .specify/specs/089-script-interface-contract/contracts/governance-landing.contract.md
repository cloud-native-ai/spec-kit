# Contract: Governance Landing

**Feature**: 089-script-interface-contract | **Contract file**: `contracts/governance-landing.contract.md`
**Guard carriers**: `tests/contract/test_constitution_double_landing.py` (extended),
`tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` (count pin),
`tests/contract/test_script_interface_contract.py` (owner page + ambient section clauses)
**FR coverage**: each clause carries its own trailing citation group; that group, not this header, is the owner of the mapping

The rule reaches five surfaces and must reach no sixth. Clauses below are normative; each names the guard that
must go red when it is broken.

## C-23 — Owner page: what it owns, declared at the top

`shared/definitions/script-interface-definitions.md` MUST open by declaring itself the single source of truth
and listing the five owned items: (1) the candidate and classification rule, (2) the mandatory flags and their
mandatory content, (3) the zero-side-effect boundary, (4) the unrecognized-option rejection requirement,
(5) the exemption criteria and the declared-exception register. The page MUST end with the `## Declared
Exceptions` section (C-30). Its mirror `.specify/shared/definitions/script-interface-definitions.md` MUST be
byte-identical.

(FR-001, FR-015)

## C-24 — Template principle

`templates/constitution-template.md` MUST carry a new numbered principle whose title is exactly
`Script Interface Contract (Declared, Zero-Side-Effect)`. The block MUST satisfy the house shape already asserted
for every principle in that file: `### <numeral>. <title>`; a claim sentence ending in a colon; bullets each
carrying `MUST` / `MUST NOT`; a `Rationale:` paragraph after the bullets; no line of 100 characters or more; no
residual `[UPPER_SNAKE_CASE]` placeholder. The principle body MUST be a pointer plus non-delegable rule points; it
MUST NOT reproduce the owner page's classification steps.

(FR-011)

## C-25 — Live principle, its own numeral

`.specify/memory/constitution.md` MUST carry the same title with that surface's own next free numeral (measured at
plan time: template 18 → 19, live 19 → 20). No clause, test or plan row may assert a numeral value; the guard's
matchers stay numeral-agnostic. The amendment MUST produce a Sync Impact Report block, a MINOR version bump
(1.16.0 → 1.17.0) and an updated `Last Amended` date, all three in the same change.

(FR-013)

## C-26 — Mandate-list entry

`skills/internal/manage-constitution/SKILL.md` MUST gain a sub-entry of the form
`  - **Script Interface Contract (Declared, Zero-Side-Effect)** — …` inside its `- **MUST include**` block. The
entry MUST name the owner path and carry the referenced-not-restated rule.

(FR-014)

## C-27 — Ambient section

`templates/instructions-template.md` MUST gain exactly one top-level section headed
`## Script Interface Contract`. Its body MUST be a summary of at most two sentences plus the owner path, and MUST
NOT contain `--action`, `$ARGUMENTS`, or an `<placeholder>` form. `.specify/instructions.md` MUST carry the same
top-level heading with the same body, produced by the project's instructions reconcile (never hand-written).

(FR-012)

## C-28 — Counts move with the landing, in one commit

`tests/contract/test_constitution_double_landing.py` MUST be updated to `TEMPLATE_COUNT = 19`,
`LIVE_COUNT = 20`, `COMMAND_COUNT = 12`, and its `DOUBLE_LANDING_WATCHLIST` MUST gain the new title (6 → 7).
`tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` MUST be updated to
`TPL_EXPECTED = 33`, `LIVE_EXPECTED = 34`. Both files MUST move in the same commit that lands the surfaces; a
count that stays behind is a stale pin and the guard is then red on nothing.

(FR-013, FR-014, FR-016)

## C-29 — Pointer discipline, with a banned-literal list

The four mandatory help-content labels (`usage`, `options`, the side-effect statement, the exit codes) and the
classification rule's step list MUST appear on the owner page and on **no** other surface. The other surfaces
carry a summary sentence plus the path. The guard MUST assert this with a banned-literal scan over
`templates/constitution-template.md`, `templates/instructions-template.md`, `.specify/memory/constitution.md`,
`.specify/instructions.md` and `skills/internal/manage-constitution/SKILL.md`, judged against the owner page's own
list (never a hand-typed second list).

(FR-015)

## C-30 — Declared exceptions register

`## Declared Exceptions` MUST exist on the owner page (and so on its mirror) and MUST be a table with the columns
`path`, `skill`, `unsatisfied clause`, `handling`, one row per registered script. An entry that does not
recompute MUST be an error, not a silent pass — the four recomputation limbs (path exists, under `skills/external/<skill>/`, `classification: external`, and
all four columns present) are declared in that same `## Declared Exceptions` section and are not restated here. An empty table is legal and MUST carry the literal
`none`.

(FR-020, FR-027)

## C-31 — The rule's own scope is written into the rule

The principle's and the ambient section's text MUST state that the rule applies to framework scripts, downstream
project scripts and third-party scripts alike. No surface may carry a phrase limiting the rule to this
repository. The guard MUST assert the absence of a repository-limited phrasing in the five landing surfaces.

(FR-023)

## C-32 — No new command, gate step, or engine for the landing

The landing MUST NOT add a `/speckit.*` command, a driver stage gate, a confirmation gate, or a second checker.
The only new executable artifacts in this feature are `scripts/python/script-interface-check.py` (plus its
mirror), `scripts/python/script_interface_cli.py` (plus its mirror), `scripts/bash/script-interface.sh` (plus
its mirror), and `tests/contract/test_script_interface_contract.py`.

FR-028 is a tombstone reserved by the clarification: this clause names it only so the coverage universe
accounts for the reserved number, and it carries no obligation.

(FR-021, FR-028)
