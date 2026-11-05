# Data Model: Self-Explanatory Framework Integration

**Feature**: 082-self-explanatory-integration | **Date**: 2026-11-05 | **Plan**: [plan.md](./plan.md)

This feature has no runtime data store. Its "entities" are the artifacts the integration must produce
and keep consistent, and its "validation rules" are the decidable conditions a guard asserts. Each
entity names the artifact that carries it; each rule names the contract clause that enforces it.

## Entities

### E-1 — Principle entry (constitution)

| Field | Meaning | Carrier |
|-------|---------|---------|
| `title` | `STR-001` verbatim — `Self-Explanatory Structure (不言自明)` | `templates/constitution-template.md`, `.specify/memory/constitution.md` |
| `numeral` | the next free numeral **on that surface** (template and live roster differ in size) | same |
| `claim` | one sentence ending in a colon, between the heading and the first bullet | same |
| `bullets` | 3–6 logical bullets, each carrying `MUST` / `MUST NOT` | same |
| `rationale` | one `Rationale:` paragraph of 1–4 sentences, one blank line after the bullets | same |
| `pointer` | `STR-004` (runtime path) as the definition target; the framework-source owner `STR-002` stays the framework's own location | both |
| `mandate entry` | a `- **<title>** — …` sub-entry inside the generator's `- **MUST include**` block | `skills/internal/manage-constitution/SKILL.md` |

Relationships: E-1 is the *same title* appearing on three surfaces (template, live, mandate list) — a
set-membership relation, never a numeral relation (see V-4).

### E-2 — Instructions ambient section

| Field | Meaning | Carrier |
|-------|---------|---------|
| `heading` | `## Self-Explanatory Structure (不言自明)` — top-level, so the generator's section reconcile can see it | `templates/instructions-template.md` |
| `summary` | at most two sentences restating the principle in the reader's terms | same |
| `pointer` | `STR-004` (runtime path), resolvable in a client project | same |
| `live twin` | the same heading and body, injected verbatim by the generator | `.specify/instructions.md` |
| `mirror twin` | byte-identical copy of the template | `.specify/templates/instructions-template.md` |

### E-3 — Owner documents and their mirrors

| Entity | Source | Mirror | Role |
|--------|--------|--------|------|
| E-3a concept owner | `shared/definitions/self-explanatory-definitions.md` | `.specify/shared/definitions/self-explanatory-definitions.md` | single source of truth for the concept's meaning, ceiling/floor, authority/projection, dimension order |
| E-3b practice owner | `shared/guidelines/self-explanatory.md` | `.specify/shared/guidelines/self-explanatory.md` | how to apply the principle |
| E-3c optimization workflow | `shared/workflow/best-practice-optimization.md` | `.specify/shared/workflow/best-practice-optimization.md` | orchestration and output mapping |

Relationship: each pair is byte-identical by construction (`sync-mirrors.py`); the mirror is a
machine-regenerated copy, i.e. one of Constitution XIV's three legitimate duplicates.

### E-4 — Budget constant and its report

| Field | Meaning | Carrier |
|-------|---------|---------|
| `INSTRUCTIONS_BUDGET_BYTES` | the single definition point of the byte ceiling | `scripts/bash/generate-instructions.sh` |
| `BUDGET:` line | `<size> <budget> <over|within>` printed on every generation | same |
| section table | per-section `live B / tmpl B / delta / placeholder / project-owned` rows | same |
| `mirror twin` | byte-identical copy of the script | `.specify/scripts/bash/generate-instructions.sh` |

### E-5 — Glossary entry

| Field | Meaning | Value for this feature |
|-------|---------|------------------------|
| `canonical` | the term's canonical form | `STR-003` — `不言自明 (Self-explanatory)` |
| `variants` | retired/synonym forms | `望文生义` (retired name only) |
| `origin` | provenance | `auto` |
| `status` | confirmation state | `proposed` |
| `store` | the single glossary file | `.specify/memory/glossary.md` |

### E-6 — Contract guards

| Guard | Subject | Carrier |
|-------|---------|---------|
| double landing | E-1 across template / live / mandate list, by title set | `tests/contract/test_constitution_double_landing.py` |
| instructions propagation | E-2 template → live injection; template-side mutation must fail | `tests/contract/test_instructions_section_propagation.py` |
| mirror parity | E-3 and E-4 pairs, table derived from `MIRROR_PAIRS` | `tests/contract/test_mirror_parity_suite.py` |
| glossary mechanism | E-5 store schema and init round-trip | `tests/contract/test_glossary_mechanism.py` |
| docs links | E-7 page's referenced paths resolve | existing suite convention (see C-27) |

### E-7 — Documentation page

| Field | Meaning | Carrier |
|-------|---------|---------|
| `path` | lowercase kebab-case page under the concepts area | `docs/concepts/self-explanatory.md` |
| `pointer rows` | table mapping layer → owner path | same |
| `history note` | one line recording the retired name | same |

Constraint: the page is a pointer page — it states the principle in one glance and links the owners; it
does not re-derive the owner's definitions (V-16).

### E-8 — Traceability record

| Field | Meaning | Carrier |
|-------|---------|---------|
| `feature` | 082 | `.specify/memory/features.md`, `.specify/memory/features/082.md` |
| `follow-up` | `OI-082-01` — wiring `/speckit.improve` to the optimization workflow | `.specify/memory/register.md` |
| `stage evidence` | the E-3 `stage-status` row + baseline measurements | `test-evidence/` |

## Validation rules

Each rule is decidable — a program, a grep, or a class/ID comparison decides it — and names the
contract clause that asserts it.

| ID | Rule | Enforced by |
|----|------|-------------|
| V-1 | The principle title `STR-001` is present in the template roster, the live roster, and the generator mandate list — as a **set member**, never as a substring | C-1, C-5, C-7 |
| V-2 | No test, template, or plan row pins a roman numeral for the new principle; matchers accept roman or arabic | C-4 |
| V-3 | The template roster and the live roster take their own next free numerals; the live numeral differs from the template numeral by the roster-size difference | C-3 |
| V-4 | The principle block satisfies the house shape: claim sentence ending in a colon, 3–6 `MUST` bullets, no line ≥ 100 chars, one blank line before a 1–4-sentence `Rationale:` | C-2 |
| V-5 | The principle carries the runtime owner pointer `STR-004` and the reference-not-restate obligation | C-6 |
| V-6 | The principle carries the no-new-machinery limit clause | C-6 |
| V-7 | The principle body contains none of the owner's section text (no verbatim copy of the definition) | C-20 |
| V-8 | The principle block produces zero `BLOCKING_RE` hits | C-8 |
| V-9 | The mandate list carries a `- **STR-001** — …` sub-entry with the truth-document anchor and the referenced-not-restated rule | C-5 |
| V-10 | The live constitution contains the principle **and** its version advanced above the baseline `git show HEAD:.specify/memory/constitution.md` reading, with a Sync Impact Report naming the new principle in the head window | C-9 |
| V-11 | The instructions template carries a top-level `## STR-001` section whose body contains `STR-004` | C-11 |
| V-12 | The section's body is at most two summary sentences plus the pointer; it contains none of the owner's section bodies | C-20, C-21 |
| V-13 | The generator, run on a fixture whose live file already carries custom sections, injects the missing section and leaves every existing section byte-identical | C-13 |
| V-14 | Removing the section from the **template** makes the propagation assertion fail without reference to the live file | C-14 |
| V-15 | After regeneration, the live instructions file contains the section and `CLAUDE.md` / `QODER.md` / `AGENTS.md` remain symlinks resolving to `.specify/instructions.md` | C-15, C-16 |
| V-16 | The docs page's referenced owner paths exist in both the source tree and the mirror tree | C-27 |
| V-17 | Each of the three source/mirror pairs is byte-identical and `sync-mirrors.py --check` exits 0 | C-22, C-23 |
| V-18 | The live instructions size is `<= INSTRUCTIONS_BUDGET_BYTES - 1` after injection, and the constant's raise is recorded with its reason | C-17, C-18 |
| V-19 | The glossary store has exactly one canonical entry for the term (`STR-003`), the retired name appears only as a variant, and the status is `proposed` | C-29, C-30 |

## State transitions

### T-A — Feature status: `Draft → Planned`

Triggered by this plan stage. The transition requires `plan.md`, `data-model.md`, `contracts/`,
`quickstart.md`, `feature-ref.md` to exist and the Constitution Check to carry no unjustified Fail —
both hold. `Planned → Implemented` belongs to `/speckit.implement` and MUST NOT be reached here.

### T-B — Glossary entry: `proposed → confirmed`

Triggered by the user's confirmation, not by this feature. The entry lands `proposed` and stays there
until a user-authored confirmation exists (Assumption A6). No automated path may flip it.

## Volume

8 entities, 19 validation rules, 2 state transitions, 33 contract clause ids across 4 files
(C-1…C-34 with C-19 present: 34 ids, of which C-20 and C-21 are defined once and
referenced from two files), 6 mutation legs. No entity carries a collection that grows per run — every artifact is a single owner file, which
keeps this feature outside the concurrent-writer hazard the framework's storage discipline names.
