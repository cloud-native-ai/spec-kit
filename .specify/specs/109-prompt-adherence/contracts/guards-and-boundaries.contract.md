# Contract — Guards, Containment Claim and Boundaries

**Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）— Spec Kit port of the closed ai-harness spec 092
**Status**: design contract. Containment-claim discipline owner:
`shared/guidelines/closed-set-claims.md`; guard-runner: `scripts/bash/run-tests.sh`;
mirror check: `scripts/python/sync-mirrors.py --check`.

## C-040 — The guard roster

**Statement**: the feature ships these guards, authored red-first: (1) owner-document guard
(`tests/contract/test_prompt_adherence_owner.py`) — owner declaration, bilingual forms, catalog and
blind-spot tables, coverage-map two-way check, framework-map row; (2) declaration guard
(`tests/contract/test_prompt_adherence_declarations.py`) — five facts present with the required keys,
membership equality, cross-agreement with the owner document, owner↔engine reason agreement, unknown-token
rejection, degradation exits; (3) engine guard (`tests/contract/test_prompt_adherence_engine.py`) — CLI
surface, fixture readings over all six rows and every allowed state, determinism, scope and window
arithmetic, duplicates, invalid sources, privacy, layer honesty, exit codes; (4) read-only guard
(`tests/contract/test_prompt_adherence_readonly.py`) — the containment claim of C-041; (5) init fixture
(`tests/integration/test_prompt_adherence_init.py`) — fresh init contains the mechanism, the installed
entry answers `--version`, the bare invocation on a fresh project emits explicit `not_evaluated` lines
with exit 0 under a socket-blocked interpreter, and mirror parity holds. Every member of every new closed
set is exercised by at least one test (SC-007). Fixtures are declarative seed sets under
`tests/fixtures/prompt-adherence/`; contract files carry the `contract` marker, the init file carries the
`integration` marker, and every guard runs through `scripts/bash/run-tests.sh` — no new runner, no
`slow` / `serial` requirement.
**Red when**: a roster member is absent; a closed-set member has no exercising test; a guard exists but
would not go red when its subject breaks.
**Test carrier**: the roster itself, run through `scripts/bash/run-tests.sh`; the full-suite run shows no
new failures (SC-009).

**Serves**: (FR-024)

## C-041 — The read-only containment claim (decidable)

**Statement**: the claim — a reading changes nothing under the managed store roots — is decided as
follows. **Baseline referent**: a hash manifest captured by the test itself immediately before the
reading invocation in the same working tree (path, SHA-256 of bytes, size per file). **Comparison unit**:
every file under the roots derived from `shared/declarations/facts/runtime-store-layout.yaml#/statement`
— one root per declared store name, projected as `.specify/<store-name>/` (the fact carries no per-store
`root` key; the projection is documented by the fact itself) — byte-level, plus the root path sets
themselves. **Allowed diff set**: none — derived mechanically from the engine's zero write points, so
the set is empty by construction. **Declared exclusion**: interpreter bytecode caches (`__pycache__/`,
`*.pyc`) are excluded; the exclusion is named here, not left implicit. **Complement assertions**: after
a per-run reading and a longitudinal reading, every root is byte-identical to the baseline and no new
file appears (`allowed delta: none`; zero new files). Determinism is a **separate** claim (C-023) judged
by run-A/run-B equality — neither claim is used to prove the other.
**Red when**: any store-root byte changes; a new file appears under a root; the baseline is not captured
by the test; determinism is cited as containment evidence or vice versa; a root outside the declared
projection is claimed.
**Test carrier**: `tests/contract/test_prompt_adherence_readonly.py`.

**Serves**: (FR-006, FR-024, SC-002)

## C-042 — Closed-set claims in this spec are decidable

**Statement**: every stability or containment statement this feature makes names its baseline referent,
its comparison unit and its allowed-diff source, and carries both the complement assertion (byte
identity outside the set) and the structural invariant (inside the set). Unfalsifiable aggregates
("unaffected", "the rest") are not used as acceptance semantics.
**Red when**: a claim lacks a referent or a comparison unit; an aggregate word carries acceptance
meaning.
**Test carrier**: review of this clause set plus the guard roster's executability (C-040).

**Serves**: (FR-024)

## C-043 — Pure consumer: no existing owner changes

**Statement**: this version changes no existing store schema, red line, flow or engine behavior. The
feedback red lines, the run-determination record schema and value domains, the evidence seven-state
domain, the probe registry, the measure report's contract, the runtime store layout and the decision
governance surface remain owned exactly where they are; the new mechanism only reads. A need discovered
for a new field is an open item for that owner, never a patch here.
**Red when**: an existing engine's record schema or value domain is edited; a red line is weakened; a
new capture point appears.
**Test carrier**: the full suite (existing owner guards stay green);
`tests/contract/test_prompt_adherence_declarations.py` (no schema-carrying fact edited).

**Serves**: (FR-005, FR-007)

## C-044 — No score, no ranking, no comparison

**Statement**: the mechanism produces closed-state observations, counts by state and coverage. It never
produces a composite adherence score, a maturity index, a ranking or a cross-project comparison, and any
future score is a new decision outside this feature.
**Red when**: a numeric roll-up or ordering by "adherence" appears; two projects, agents or users are
compared.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (no-verdict and no-ranking legs).

**Serves**: (FR-025)

## C-045 — Baseline honesty

**Statement**: the feature's first dated baseline reading (C-035) reports explicit unobserved rows and
never claims improvement; a later improvement claim requires comparable before/after evidence under the
evidence discipline.
**Red when**: the baseline is summarized without its unobserved rows; an improvement is claimed without
comparable evidence.
**Test carrier**: the baseline feedback entry (dated record) plus the audit-replay leg of
`tests/contract/test_prompt_adherence_engine.py`.

**Serves**: (FR-026)

## C-046 — Host observations stay framework-integration input

**Statement**: host-layer observations inform this framework's integration decisions only. They are never
packaged as feedback about the host product, and the feedback target stays the framework itself. The
framework's feedback red lines are referenced from their owner, not restated here.
**Red when**: a host-layer observation is routed into a feedback package aimed at the host product; the
feedback target widens.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (layer-honesty legs, host-row output
carries no product-directed statement); review of the baseline entry's target.

**Serves**: (FR-027)