# Contract — Owner Document and Signal Catalog

**Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）— Spec Kit port of the closed ai-harness spec 092
**Status**: design contract. Meaning owner after implementation:
`shared/definitions/prompt-adherence-definitions.md`; value-domain owners: the five
`shared/declarations/facts/prompt-adherence-*.yaml` files. This file fixes the design the guards assert;
it is not a second definition point once the owner lands.

## C-001 — One owner document, pointer-only consumers

**Statement**: `shared/definitions/prompt-adherence-definitions.md` (installed as
`.specify/shared/definitions/prompt-adherence-definitions.md`) is the single owner of: the premise
chain, the two-layer model, the signal catalog (rows plus admission criteria), the per-row attribution,
the assumed-behavior coverage map, the blind-spot register, the reading contract's field meanings and
the feature's red lines. Every other surface that carries any of these facts points at it by path; none
restates its tables or enumerations. The framework map (`shared/definitions/framework-map.md`) gains
the owner-document row for this page.
**Red when**: a second file restates the catalog, blind-spot table or coverage map; the framework-map
owner row is missing; the owner is absent from a fresh init.
**Test carrier**: `tests/contract/test_prompt_adherence_owner.py`; `tests/integration/test_prompt_adherence_init.py`.

**Serves**: (FR-001, FR-019, FR-020)

## C-002 — Two layers, declared and bilingual

**Statement**: the host prompt layer (宿主提示层, [[STR-001]]) is the runtime-owned prompt surface — the
host system prompt plus the user's direct prompt — and is not authored by this framework; the project
rule file layer (项目规则文件层, [[STR-002]]) is the instructions surface this framework ships, whose
fact owner remains `.specify/shared/workflow/symlink-model.md`. The owner document reaches the
host-versus-project harness disambiguation in `shared/guidelines/better-harness.md` and the
instructions-surface model by reference, and its core concept lines carry the bilingual form per
`shared/guidelines/bilingual-expression.md`.
**Red when**: a layer is defined a second time; a token differs from [[STR-001]]/[[STR-002]]; a core
concept line loses its bilingual form; the referenced owners are restated instead of pointed at.
**Test carrier**: `tests/contract/test_prompt_adherence_owner.py` (layer-token and bilingual legs).

**Serves**: (FR-002)

## C-003 — Premise review: assumed behaviors and the two-way coverage map

**Statement**: the owner document decomposes the premise chain into named assumed behaviors (`AB-NN`,
dense in document order) and carries a coverage map in which every assumed behavior maps to exactly one
catalog row id or exactly one blind-spot id. The mapping is machine-checkable in both directions: every
sensor target resolves to a catalog row id, every blind-spot target resolves to a register id, every
catalog row is cited by at least one assumed behavior, and every register blind spot is cited by at
least one assumed behavior. The check is reachable as
`python3 .specify/scripts/python/prompt-adherence.py --check-coverage`, exits 0 with zero findings, and
is also driven by the owner guard.
**Red when**: an AB row is missing, duplicated, or names two targets; a target does not resolve; a
catalog row is uncited; the check exits non-zero on the delivered owner document; the check result is
only claimed, not machine-produced.
**Test carrier**: `tests/contract/test_prompt_adherence_owner.py`; the `--check-coverage` leg of
`tests/contract/test_prompt_adherence_engine.py`.

**Serves**: (FR-003)

## C-004 — Admission criteria for a signal class

**Statement**: a signal class enters the catalog only when all five conditions hold: (a) an existing
mechanism produces it at an existing lifecycle point and persists it in an existing store; (b) it
carries a machine-readable source identifier; (c) its meaning is decidable from a closed vocabulary or a
declared derivation; (d) it declares layer candidacy and strength; (e) it can express "not observable"
honestly. A signal failing (a) is listed in the blind-spot register; this feature MUST NOT synthesize it
through a new capture point.
**Red when**: a catalog row names a non-existent store or capture point; a blind spot is missing for a
purpose that fails (a); a row cannot express absence.
**Test carrier**: `tests/contract/test_prompt_adherence_owner.py` (admission-criteria section present
and each row's cells resolvable); `tests/contract/test_prompt_adherence_declarations.py` (store names
resolve through the runtime store layout).

**Serves**: (FR-004, FR-005)

## C-005 — The six catalog rows and their declared attribution

**Statement**: the initial catalog is exactly the six rows of FR-028 — `run-determination-record`
(host-prompt, indirect; classes `axis-regression`, `green-unproven`), `exec-quant-record` (project-rules,
indirect; no class), `feedback-entry` (project-rules, direct; no class; excludes the gate-observation
family), `gate-observation-record` (project-rules, direct; no class; family = the `gate:` run-identity
prefix its protocol declares), `evidence-finding` (project-rules, indirect; class `evidence-missing`),
`probe-registry-declaration` (project-rules, indirect; positive states stop at `Wired`; no class). Each
row declares its record predicate, source store and owning read surface, identity fields and timestamp
field in the machine-parsed catalog table. Instruction-reconcile observations are not a row while no
store persists them.
**Red when**: a seventh row appears; a row's layer or strength differs from this clause; a row's cells
name an undeclared store or engine; the gate family is identified by anything other than the declared
`gate:` prefix.
**Test carrier**: `tests/contract/test_prompt_adherence_owner.py` (catalog table legs);
`tests/contract/test_prompt_adherence_declarations.py` (row-id set equality).

**Serves**: (FR-004, FR-028)

## C-006 — Blind-spot register, exactly six classes

**Statement**: the initial register is exactly the six classes of FR-029 — `host-prompt-content`,
`host-rule-surfacing`, `in-turn-rule-behavior`, `anomaly-line-persistence`,
`gate-breach-and-silent-skip`, `instruction-drift-between-reconciles` — each carrying the reason no
persisted sensor observes it today and the direction an owner-sanctioned capture change would take. The
`host-prompt-content` red line (raw host and user prompt text is never read) and the
`anomaly-line-persistence` boundary (the dropped run-determination red-state producer MUST NOT be
reintroduced) are stated in the register entries. Instruction-reconcile observations stay here until an
owner-sanctioned persistence change exists.
**Red when**: a register entry lacks its reason or capture direction; a seventh class appears; the
register is not carried into every reading's coverage section.
**Test carrier**: `tests/contract/test_prompt_adherence_owner.py` (register legs);
`tests/contract/test_prompt_adherence_engine.py` (coverage section carries all six).

**Serves**: (FR-029, FR-013)

## C-007 — Red lines stated once

**Statement**: the owner document states the feature's red lines: no composite adherence score, maturity
index, ranking or cross-project comparison; no new store, capture point or record-schema change; no
reading of raw host prompts or user conversation text; no network access or automatic transmission;
host-layer observations inform framework integration only and are never packaged as feedback about the
host product; the feedback red lines (framework-only target, optional user data, zero automated
transmission) remain owned by `shared/workflow/feedback-step.md` and are referenced, not restated.
**Red when**: a red line is missing; a score-like output appears; the feedback red lines are restated
instead of referenced.
**Test carrier**: `tests/contract/test_prompt_adherence_owner.py` (red-line legs); the no-score and
no-network legs of `tests/contract/test_prompt_adherence_engine.py`.

**Serves**: (FR-025, FR-027, FR-007)