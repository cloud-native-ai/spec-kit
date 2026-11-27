# Contract — Owner Document, Layout Table and Concept-Pointer Slot

**Feature**: 110 Context Management（上下文管理）(spec 110)
**Status**: design contract. Bilingual-expression owner: `shared/guidelines/bilingual-expression.md`;
one-source-of-truth owner: `shared/guidelines/one-source-of-truth.md`; the evidence-state domain:
`shared/declarations/facts/evidence-seven-states.yaml#/statement`.

## C-001 — One owner document for the whole context model

**Statement**: `shared/definitions/context-management-definitions.md` (installed at
`.specify/shared/definitions/context-management-definitions.md`) is the single owner of the
context-management concept. It owns: the umbrella term and its bilingual definition site; the two
categories; the three layers; the five materialization forms; the layer landing contract; the one context
layout table; the composition protocol; the closed trigger set; the composer roles; the concept-pointer
slot; the presence vocabulary (all five tokens, `present` included, defined once here); and the red lines.
Every other surface reaches these meanings by path reference and MUST NOT restate them.
**Red when**: a second document declares the model, a layout row set, or a trigger set; the owner document
carries an entry duplicated from another owner instead of a pointer.
**Test carrier**: `tests/contract/test_context_management_owner.py` (heading and ownership legs);
`tests/contract/test_context_management_declarations.py` (value-domain separation).

**Serves**: (FR-001)

## C-002 — Bilingual definition sites carry the fixed literal forms

**Statement**: the owner document carries the definition sites for the umbrella term and for each category
and layer, using the literals `Context Management(上下文管理)` ([[STR-001]]), `Invariant(不变)` ([[STR-002]]),
`Variable(可变)` ([[STR-003]]), `System(系统级)` ([[STR-004]]), `Project(项目级)` ([[STR-005]]) and
`Task(任务级)` ([[STR-006]]) verbatim; the machine tokens `invariant` / `variable`, `system` / `project` /
`task` are the declaration-owned value domains. Other surfaces cite the terms and point here; they do not
re-declare either face.
**Red when**: a definition site is missing or paraphrased; a machine token drifts from its declaration;
a second surface enumerates the value domain.
**Test carrier**: `tests/contract/test_context_management_owner.py` (definition-site legs);
`tests/contract/test_context_management_declarations.py` (token-domain legs).

**Serves**: (FR-001, FR-002, FR-003)

## C-003 — Terminology boundaries are stated once, by pointer

**Statement**: the owner document states the boundary between this concept and four neighbours, each by
pointer to its owner: the standing `## Project Context` block (a rendered artifact owned by the agent
render path — `render_agents_for_tool` in `src/specify_cli/__init__.py` over the agent definitions under
`agents/`); the super↔sub dispatch payload (owned by `shared/definitions/superagent-definitions.md` § The
super↔sub Protocol); the ambient instructions layer and its Documentation Map (owned by
`templates/instructions-template.md` and its generator `scripts/bash/generate-instructions.sh`); and the
model context window (not a framework artifact). The table states the distinction only; it neither
redefines a neighbour nor copies its rules.
**Red when**: the boundary table is missing a neighbour; a boundary row restates a neighbour's rule text.
**Test carrier**: `tests/contract/test_context_management_owner.py` (boundary-table legs).

**Serves**: (FR-001, FR-005)

## C-004 — The layout table is the single home of the row data

**Statement**: the owner document carries one machine-parsed layout table whose fixed column set is
`class id | layer | form | source | owner | cap reference`. The table is the single home of the per-row
data; no second layout data file exists. The class-id column is the projection of the machine roster
whose membership and order `context-classes.yaml` owns (C-010, C-015); the table must match it
row-for-row and a mismatch is an audit finding. The row roster is the eighteen classes of FR-004, and
the table carries no category column (the category is derived from the layer, C-006).
**Red when**: a row-level field (source, form, owner, cap) is duplicated in the fact layer or another
document; the class-ids column diverges from the roster without a finding; a category column appears;
the roster drops or adds a class outside an owner revision.
**Test carrier**: `tests/contract/test_context_management_owner.py` (table shape and roster legs);
`tests/contract/test_context_management_engine.py` (parser legs).

**Serves**: (FR-004, FR-007, FR-029)

## C-005 — The five forms and their legality matrix

**Statement**: the closed form set is `pointer`, `read-in-full`, `bounded-index`, `runtime-discovery`,
`inline-digest` (domain owned by `context-forms.yaml`). Legality by layer: system — `runtime-discovery`,
`pointer`; project — `read-in-full`, `pointer`, `bounded-index`; task — `bounded-index`, `pointer`,
`inline-digest`. The owner document states the matrix once; the engine enforces it; a row outside its
layer's set is a finding.
**Red when**: a form token outside the domain appears; a layer's allowed set drifts from this clause; the
matrix is enforced only by review.
**Test carrier**: `tests/contract/test_context_management_engine.py` (matrix and seeded-violation legs);
`tests/contract/test_context_management_declarations.py` (form-domain legs).

**Serves**: (FR-006, FR-009)

## C-006 — The layer landing contract: three legal cells, three forbidden combinations

**Statement**: the owner document declares exactly three legal (category, layer) cells — `invariant` ×
`system` (runtime discovery or constraint-owner pointers; never authored, never persisted), `invariant` ×
`project` (read-in-full governance baseline with zero copied bytes, plus pointers and bounded indexes from
`.specify/`), `variable` × `task` (bounded indexes, pointers and the inline-digest fallback, discarded at
task end; carried by the dispatch brief and the `task-delta` refresh on dispatch edges) — each stating its
definition, its carriers, its allowed forms by reference to C-005, and its content-versus-pointer rule.
The three other combinations (`invariant` × `task`, `variable` × `system`, `variable` × `project`) are
named as forbidden and appear in no layout row. The category is derived from the layer and is never a
layout column.
**Red when**: a cell is missing or merged; a fourth combination is admitted; allowed forms are restated as
a second value list instead of referencing C-005; a row's layer and form fall outside their cell.
**Test carrier**: `tests/contract/test_context_management_owner.py` (landing-cell legs);
`tests/contract/test_context_management_engine.py` (row-to-cell legs against the matrix).

**Serves**: (FR-002, FR-003, FR-029)

## C-007 — Concept-pointer slot: pointer-only triple, four governed structures, honest absence

**Statement**: concept consistency is carried by one non-omittable pointer-only triple — `glossary` →
`.specify/glossary.md`; `definitions` → the concept-definition owner documents under the installed
`shared/definitions/` tree as a bounded index; `explanations` → `.specify/skills.md` / `.specify/tools.md`
plus the project's explanation-type documentation reached through the Documentation Map. The triple is
carried by the project-layer rows `project-vocabulary`, `concept-definitions` and `concept-explanations`.
The slot is required in the closed structure set — a root/superagent turn, a subagent dispatch payload
with its temporary-memory package, a memory-recall projection, and a recovery/re-anchoring re-entry
surface — and the owner document declares, per structure, the slot's carrier and pointer form, mapping
onto existing channels only (on dispatch edges: the existing `authority_ref` pointer field, the child's
ambient Documentation Map glossary row and the dispatch brief's reading list). Every structure's slot
presence is observable through a named surface, never declarative-only: the manifest's three project-layer
rows serve the root/superagent turn, the memory-recall projection and the recovery/re-entry surface (their
carrier is the composing session's baseline rows), and the dispatch payload is read through the pinned
channels — the Documentation Map glossary entry and the brief's reading list — plus the protocol-boundary
assertion. A definition's meaning is never copied into context. A missing or unresolvable entry reads one
of the absence tokens in the manifest — an entry whose layout row is missing reads `not-evaluated` (the
manifest's row set is the roster, C-015/C-033), an entry whose declared source is missing or unreadable
reads `absent` / `unreachable` — and a consistency claim derived from that structure reads `Unobserved`,
never `present` and never agreement.
**Red when**: the triple is carried by content instead of pointers; a structure in the closed set lacks a
declared carrier or a named presence surface; absence is reported as agreement or `present`; the mapping
adds a payload field, injection, cap, identifier or self-check item.
**Test carrier**: `tests/contract/test_context_management_owner.py` (slot and structure legs);
`tests/contract/test_context_management_engine.py` (concept-row presence legs);
the package-boundary leg in `tests/contract/test_context_management_owner.py` (C-042).

**Serves**: (FR-028)