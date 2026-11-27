# Contract — Declaration Sets and Vocabularies

**Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）— Spec Kit port of the closed ai-harness spec 092
**Status**: design contract. Declaration-layer contract owner: `shared/declarations/contract.yaml`;
reader: `scripts/python/declaration_reader.py`; completeness judge:
`scripts/python/harness-triple-check.py`. This file fixes the design; the facts themselves are
implementation outputs of this feature.

## C-010 — Exactly five declaration facts, no sixth

**Statement**: the feature introduces exactly five fact files under `shared/declarations/facts/`:
`prompt-adherence-layers.yaml` (members `host-prompt`, `project-rules`), `prompt-adherence-strengths.yaml`
(`direct`, `indirect`), `prompt-adherence-signals.yaml` (the six row ids of FR-028),
`prompt-adherence-deviation-classes.yaml` (`axis-regression`, `green-unproven`, `evidence-missing`) and
`prompt-adherence-reading-status.yaml` (`complete`, `partial`, `no-data`, `not-found`). Observation
states get no sixth fact: they compose `shared/declarations/facts/evidence-seven-states.yaml` with the
`not_evaluated` literal owned by the run-determination value domains, composed at read time.
**Red when**: a sixth `prompt-adherence-*` fact appears; observation states are declared as a set; a
member differs from this clause.
**Test carrier**: `tests/contract/test_prompt_adherence_declarations.py` (file inventory and member
equality legs).

**Serves**: (FR-018)

## C-011 — Facts obey the declaration layer's own contract

**Statement**: each fact carries the required keys (`fact`, `kind`, `statement`, `consumers`,
`former_carriers`; `note` optional) of `shared/declarations/contract.yaml`, uses one of its five kinds
(all five are `closed-set`), and is read through `declaration_reader.load_fact`. Each declares
`scripts/python/prompt-adherence.py` among its consumers, so the triple check's read-point condition is
locatable in the engine source (the engine references `declaration_reader` and each slug). No value
domain is restated in engine constants or in documentation.
**Red when**: a required key is missing; a kind is outside the contract's set; the engine's read point
for a slug is not locatable; a member list is re-spelled outside the fact (the guard's copy excepted).
**Test carrier**: `tests/contract/test_prompt_adherence_declarations.py`; `harness-triple-check.py`
`verify` stays clean for the five facts.

**Serves**: (FR-018, FR-019)

## C-012 — Cross-agreement between the owner document and the declaration sets

**Statement**: the owner document's catalog table cells draw only on the declared sets: every layer cell
is a member of the layers fact, every strength cell a member of the strengths fact, every deviation-class
cell a member of the classes fact; the row-id column equals the signals fact member-for-member; the
engine's emitted reading-status values are members of the reading-status fact; emitted observation
states are members of the composed state domain. A disagreement in either direction is a finding.
**Red when**: a cell token is outside its set; the catalog's row ids differ from the signals fact; the
engine emits a status or state outside the composed domain.
**Test carrier**: `tests/contract/test_prompt_adherence_declarations.py` (bidirectional agreement legs);
`tests/contract/test_prompt_adherence_engine.py` (emitted-token legs).

**Serves**: (FR-018, FR-009)

## C-013 — Unknown tokens are hard errors

**Statement**: an unknown token in any of the five declaration sets, in the owner document's catalog,
blind-spot or coverage-map tables, or on the engine's command line aborts the run with exit 2, a
recognizable message on stderr, and no reading. No silent coercion, no guess, no default. A
record-level value outside its source engine's declared domain is not this clause's subject: C-024
lays it aside as a schema-violating record while the reading continues.
**Red when**: an unknown token is coerced, skipped, or defaulted; a reading is emitted after an unknown
token is detected.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (unknown-token rejection legs; exit
codes asserted); `tests/contract/test_prompt_adherence_declarations.py` (a doctored fact in a scratch
copy is rejected).

**Serves**: (FR-018, FR-022)

## C-014 — Observation-state composition

**Statement**: an observation state is one of the seven evidence states (`Present`, `Wired`, `Exercised`,
`Outcome-supported`, `Missing`, `Unobserved`, `Not applicable`) or `not_evaluated`. The seven names and
their order are read from `evidence-utils.py` (which reads `evidence-seven-states.yaml`); the
`not_evaluated` literal is read from `run-determination.py`'s comparison-verdict and correctness-verdict
domains. The engine carries no copy of either set.
**Red when**: a state outside the composition is emitted; the engine spells a state literal that its
source engines own; the order used for any deterministic listing differs from the declared order.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (emitted-state legs);
`tests/contract/test_prompt_adherence_declarations.py` (no sixth fact).

**Serves**: (FR-018, FR-011)

## C-015 — The not-evaluated reason taxonomy is not a sixth declaration fact

**Statement**: the reading's reason causes are closed at three — `source-unavailable`,
`no-matching-records`, `invalid-source` — and the invalid-source causes at four — `unparsable`,
`schema-violation`, `unknown-schema-version`, `invalid-timestamp`. Their **meanings** are owned by the
owner document's reading contract; their **tokens** are the engine's schema; a bidirectional contract
test pins the two faces and fails when either drifts. These vocabularies are deliberately **not**
declaration facts: FR-018 fixes the feature's declaration set at five, and inventing a sixth would
violate it. The engine also carries no adherence verdict token.
**Red when**: a fourth reason cause appears; owner and engine disagree member-for-member; a reason is
free text without a cause token; the vocabulary is moved into a sixth fact without revising the owner.
**Test carrier**: `tests/contract/test_prompt_adherence_declarations.py` (owner↔engine agreement legs);
`tests/contract/test_prompt_adherence_engine.py` (reason presence on every `not_evaluated` or
`Unobserved` row).

**Serves**: (FR-011, FR-014, FR-018)

## C-016 — Layer attribution is declared, never derived at read time

**Statement**: every observation reports its layer and strength exactly as the catalog declares them.
The reading may list direct rows and indirect rows side by side but produces no layer-level statement,
verdict or roll-up from any combination of rows, and a fixture carrying only indirect rows yields no
layer-level verdict (SC-003). Host-layer observations inform framework integration only (FR-027).
**Red when**: the engine assigns a layer or strength not in the catalog; an output line or field states
a layer-level adherence conclusion; an indirect-only input yields a verdict-shaped aggregate.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (layer-honesty legs with the
project-only and indirect-only fixtures).

**Serves**: (FR-009, FR-010, FR-027)