# Contract — Guards, Containment Claims and Boundaries

**Feature**: 110 Context Management（上下文管理）(spec 110)
**Status**: design contract. Closed-set-claim owner: `shared/guidelines/closed-set-claims.md`;
single-run evidence owner: `shared/guidelines/single-run-evidence.md`;
test execution owner: `shared/guidelines/test-execution-efficiency.md`.

## C-040 — Five guard files, red-first, one seeded violation per checked rule

**Statement**: the feature ships `tests/contract/test_context_management_owner.py`,
`tests/contract/test_context_management_declarations.py`,
`tests/contract/test_context_management_engine.py`,
`tests/contract/test_context_management_readonly.py` and
`tests/integration/test_context_management_init.py`, authored before the implementation (Red-Green), and
run through `scripts/bash/run-tests.sh` (single entry). Every rule `--action check` can report carries its
own seeded-violation fixture under `tests/fixtures/context-management/`; each fixture carries a minimal
owner document and the four facts at its own workspace root in the framework-source shape, so
`--workspace-root` selects the audited tree and its own declaration layer drives the reading (A-17). The
fixture's **guard test** MUST go red when the rule is removed from the engine (roster-mismatch,
roster-order, unknown-layer, unknown-form, layer-form-illegal, duplicate-class, empty-layer, cap-missing,
category-column): the observable is the guard test's verdict, not the engine's finding output. A guard
that would not fail when its subject breaks is itself a defect.
**Red when**: a rule has no fixture; a fixture's guard test stays green under mutation; a guard is
skipped or muted; a fixture lacks its own declaration layer.
**Test carrier**: the five files themselves; the mutation drill is executed at implement and captured per
single-run evidence.

**Serves**: (FR-027)

## C-041 — Containment claims are decidable

**Statement**: SC-002's containment leg is a SHA-256 hash manifest over the fixture tree taken immediately
before and after each audit action in the same test run, with interpreter bytecode caches (`__pycache__`
by name) excluded, asserting identical bytes and zero new files. SC-008's containment leg takes the
implement-entry commit as its named baseline: the allowed-delta set is the file fan-out of this feature's
edits, mirrors are asserted byte-identical after the flow, and the three protected surfaces (the
super↔sub protocol's declared field / injection item set, the `## Project Context` rendering fixture
output, and `memory-utils.py --action recall` output on a populated fixture) are compared against outputs
captured at that commit for the same fixtures. The five required elements of the claim discipline are
carried per claim: baseline referent, comparison unit per artifact class, mechanically derived
allowed-delta set, complement assertion, and no undefined aggregate words.
**Red when**: determinism (A/B byte-identity) is used as containment evidence; the baseline is unnamed;
the allowed-delta set is hand-listed rather than derived from the fan-out.
**Test carrier**: `tests/contract/test_context_management_readonly.py` (hash-manifest legs);
`tests/integration/test_context_management_init.py` and the full-suite capture (SC-008).

**Serves**: (FR-027)

## C-042 — Concept-pointer and protocol-boundary guard

**Statement**: the guards pin the three concept-pointer rows as required project-layer rows and as the
declared per-structure carriers; on the repository tree each reads `present` with a resolvable source; on
a fixture with one concept-pointer layout row removed and one source unreadable, the manifest still prints
the removed row (the row set is the roster) reading `not-evaluated` with the missing-layout-row reason and
prints the unreadable source's row reading `unreachable`, the affected structure's consistency reading is
`Unobserved` (the evidence-state token; the manifest row's own presence token is one of the four absence
tokens), and no output reports agreement or `present`; the fixture's layout-versus-roster mismatch is
separately assertable as the `check` `roster-mismatch` finding (exit 1), a distinct reading that may
co-occur. The same guards assert each governed structure's slot presence resolves to a named surface: the
manifest's three project-layer rows for the root/superagent turn, the memory-recall projection and the
recovery/re-entry surface, and the pinned dispatch channels — the Documentation Map glossary entry and the
dispatch brief's reading list — for a dispatch payload. The protocol-boundary leg parses the super↔sub
protocol owner's declared item set (the seven role fields and the four injections) and asserts the set is
unchanged since the pre-change baseline; the owner document's mapping section names only existing channels.
**Red when**: an absence reads as agreement; a missing concept row is omitted; a structure's presence
surface is undeclared or does not resolve; the protocol's declared item set changes; a new field or
injection appears in a dispatch payload.
**Test carrier**: `tests/contract/test_context_management_owner.py` (package-boundary and structure legs);
`tests/contract/test_context_management_engine.py` (concept-row presence legs).

**Serves**: (FR-017, FR-027, FR-028)

## C-043 — Layer-landing guard

**Statement**: a contract test pins the owner document's three legal (category, layer) cells and the three
forbidden combinations, asserts the layout carries no category column, and asserts that every layout row's
layer and form fall inside the cell where the form is legal. The cells' allowed forms reference the form
contract (C-005), never a second value list.
**Red when**: a cell is missing or a fourth is admitted; a forbidden combination appears as a row; the
category column appears; a row's form escapes its cell.
**Test carrier**: `tests/contract/test_context_management_owner.py` (landing-cell legs);
`tests/contract/test_context_management_engine.py` (row-to-cell legs).

**Serves**: (FR-027, FR-029)

## C-044 — Existing owners are referenced, never redefined

**Statement**: the mechanism changes none of these owners' rules: the super↔sub protocol and its payload
(`shared/definitions/superagent-definitions.md` § The super↔sub Protocol); the standing `## Project
Context` rendering (`render_agents_for_tool` in `src/specify_cli/__init__.py` over the agent definitions);
memory recall (`scripts/python/memory-utils.py --action recall`); the token/cap economy
(`shared/guidelines/token-efficiency.md`); the governance documents and their generators; the destructive
action rules (`shared/guidelines/confirmation-gates.md`); the declaration layer
(`shared/definitions/harness-triple-definitions.md`, `shared/declarations/contract.yaml`); and the
re-anchoring tiers (`shared/definitions/re-anchoring-definitions.md`). The feature's edits outside its own
new files are exactly: three framework-map rows and one instructions-template section (plus their
generated copies and the append-only registration keys).
**Red when**: one of these owners is edited beyond the named rows/section/keys; a rule text is copied into
the owner document; a second cap, red line or gate appears.
**Test carrier**: `tests/contract/test_context_management_owner.py` (boundary legs); the full suite and
`git diff --stat` over the changed set.

**Serves**: (FR-005, FR-017)

## C-045 — No new command, skill, gate, store or network path

**Statement**: this version ships no `/speckit.*` command and no skill wrapper; the documented entry is the
read-only audit invocation. No store, cache, index, rendered artifact or database is created; no existing
store's schema changes and the runtime-store roster
(`shared/declarations/facts/runtime-store-layout.yaml#/statement`) is unchanged; no network access,
transmission or raw-text consumption exists anywhere in the audit path. Changing or adding a command, a
skill, a gate or a red line is out of scope.
**Red when**: a wrapper ships; a store or cache appears; a schema or the store roster changes; a network
call exists.
**Test carrier**: `tests/contract/test_context_management_readonly.py` (containment legs); review of the
changed-file set.

**Serves**: (FR-011, FR-024, FR-026)

## C-046 — Every declared member is exercised; unknown members are refused

**Statement**: every member of `context-categories`, `context-layers` and `context-forms` is exercised in
at least one test or engine action (exercised = mutating or removing the member produces an observable
difference in an assertion or an engine output); the declarations and the engine agree member-for-member;
an unknown or missing declaration member is refused with exit `2` on both actions.
**Red when**: a member is never exercised; the engine's accepted set drifts from a fact; an unknown
declaration member is accepted; a missing declaration member yields a default.
**Test carrier**: `tests/contract/test_context_management_declarations.py` (member-exercise legs);
`tests/contract/test_context_management_engine.py` (unknown-member legs).

**Serves**: (FR-018, FR-027)