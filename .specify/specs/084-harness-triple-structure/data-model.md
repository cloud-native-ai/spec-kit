# Data Model — 084 Harness 三重结构（markdown + yaml + script）

**Date**: 2026-11-05 | **Spec**: `.specify/specs/084-harness-triple-structure/requirements.md`

Three stored entities (`contract.yaml`, one file per fact, one file per exclusion reason) and five derived quantities.
Nothing else is stored: a unit's disposition, a unit's completeness state and a read point are **recomputed from the
stored files on every run** (`.specify/instructions.md` § Concurrent Development Safety: 派生索引即读即建). The stored
set is closed and grows only by revising `contract.yaml`'s key set, which is the file this model calls E-3.

Vocabulary discipline: the literal values (`complete` / `pending` / the three exclusion reasons / the six reason
templates) are **not restated here** — they are owned by `contract.yaml` (value domains) and by `requirements.md`
§ Shared Strings (the reason templates). This file references them by `[[STR-NNN]]` or by contract key name only.

---

## E-1 — Fact Declaration（一条事实一件文件）

**Identity**: the file path — `shared/declarations/facts/<fact-slug>.yaml`. `<fact-slug>` is the fact's grounded name
(kebab-case, `^[a-z0-9]+(-[a-z0-9]+)*$`); it MUST equal the `fact` key and the filename stem. There is no second
numbering namespace (a slug is not a `FR-`, not a `STR-`, not a `T-`).

| Field | Cardinality | Content | Validation |
|-------|-------------|---------|------------|
| `fact` | required | the slug | equals the filename stem; matches the kebab-case grammar |
| `kind` | required | one value from E-3's `fact_kinds` | membership in the contract's closed five-value set |
| `statement` | required | the machine-read value: scalar, sequence, or mapping | block subset only (E-3 `yaml_subset`); non-empty |
| `consumers` | required | sequence of repo-relative paths: engine paths that MUST read the fact, and carrier paths that point at it | every entry resolves after E-9 normalization; non-empty; disjoint from `former_carriers` |
| `former_carriers` | required | sequence of repo-relative paths that used to carry the literal | every entry resolves; MUST NOT overlap `consumers` |
| `note` | optional | human-readable remark (e.g. the authority-order correction recorded when two faces had already drifted) | prose; never read by a judgement |

Rules that are properties of the entity, not of a run:

- **R-1 one fact, one file.** Two files claiming the same slug is the duplicate-declaration finding, never resolved by
  filename order or mtime.
- **R-2 the value lives only here.** `statement` is the fact's only normative copy; a carrier may point at
  `<path>#/<key-path>` and MUST NOT restate the value (the mechanical reading is the reused `duplicate-fact` label).
- **R-3 migration provenance.** When the faces disagreed before migration, the value taken follows the authority order
  owned by `shared/definitions/harness-triple-definitions.md` and the correction is written in `note`.

## E-2 — Exclusion Record（按理由一词一文件）

**Identity**: the path *and* the row — `shared/declarations/exclusions/<reason>.yaml`, where `<reason>` is the
filename form of one of E-3's `exclusion_reasons`. One file per reason, at most three; a new unit appends a row and
MUST NOT reorder existing rows (the conflict surface the dual-writer test acknowledges).

| Field | Content | Validation |
|-------|---------|------------|
| `unit` | the unit's markdown carrier path (E-4 identity) | resolves after E-9 normalization; unique across all three files |
| `carrier` | the engine or asset the unit does reach, when the reason is `no-machine-fact` / `no-harness-asset` | resolves; may be empty only for a reason the contract marks carrier-free |
| `anchor` | the resolvable in-tree evidence for the reason (file path plus a locatable line or section) | MUST resolve; an unresolvable anchor is the `[[STR-012]]` finding, never a warning |

**R-4 exactly one disposition per unit.** A candidate unit is in scope because at least one declaration names its
carrier path, or it is out of scope because exactly one exclusion row names it — never both, never neither. This is
what makes `by-owner-decree` a *unit*-level reason (a fact-level carve-out belongs in the owner documents and in
§ Non-Goals, not as a second exclusion row for the same unit).

## E-3 — Layer Contract（`shared/declarations/contract.yaml`）

The single owner of every machine-read value domain of this feature. It is the only aggregated file the layer is
allowed to hold, because it carries **domains**, not processing state.

| Key | Content |
|-----|---------|
| `schema` | the declaration-layer schema identifier |
| `yaml_subset` | the allowed-subset identifier (the subset grammar itself is owned by `harness-triple-definitions.md`) |
| `fact_kinds` | the closed five-value set |
| `completeness_states` | the closed two-value set |
| `exclusion_reasons` | the closed three-value set |
| `exit_codes` | the three exit codes with their meaning |
| `required_fact_keys` / `required_exclusion_keys` | the mandatory key sets |
| `gate_call_sites` | the call-site roster (E-8) |

**R-5 the contract is not a second copy.** Every value in it appears exactly once repo-wide; markdown owners reference
it, scripts read it through E-7's single entry point. A contract key that restates a value already owned elsewhere is a
duplicate, not a declaration.

## E-4 — Flow Unit（derived identity, never stored）

Identity = the unit's markdown carrier path. Membership is recomputed by the candidate screen: the three carrier
surfaces (`templates/commands/*.md`, `skills/{external,internal}/*/SKILL.md`, `shared/workflow/*.md`) whose text
contains at least one reference to a framework-internal deterministic engine. `shared/definitions/*.md` is explicitly
not a unit (it owns facts; it does not get a disposition).

Counts are a **reading**, not a schema: the measured surface sizes at plan time are recorded in `research.md` § R4 and
`test-evidence/plan-readings.txt`; nothing in the implementation may hard-code them.

## E-5 — Unit Disposition（derived: in-scope | excluded | unclassified）

Derived by reverse projection, in this order: (1) a declaration names the unit's carrier path in `consumers` or
`former_carriers` ⇒ in-scope; (2) else an exclusion row names the unit ⇒ excluded, carrying that row's reason;
(3) else unclassified ⇒ the `[[STR-013]]` finding naming the unit. Step order is part of the contract because a
contradictory pair (both a declaration and an exclusion naming one unit) must resolve to a *finding*, not to whichever
file the reader happened to open first.

## E-6 — Layer Completeness State（derived binary）

| Value | Condition |
|-------|-----------|
| `complete` | three conditions conjunctively: (a) each of the unit's facts has exactly one declaration passing the schema and subset checks; (b) the unit's carrier holds a pointer, and the reused `duplicate-fact` reading for that fact is zero hits; (c) at least one engine named in `consumers` has a locatable read point |
| `pending` | anything else, named by the closed reason set; a missing read point is `[[STR-009]]` |

**R-6 the false-green red line.** A declaration file existing is **not** evidence for (a): (a) is a per-fact verdict
from the run, and (c) failing keeps the state at `pending` even when (a) and (b) are green.

**Read point (derived, part of (c))**: the consumer engine's source text references the single read entry point (E-7)
and references the fact's slug. This is a textual locator, decidable by a program, and explicitly **not** a proof of
semantics — the contract says so in one sentence so nobody reads a green (c) as "the engine is correct".

State transitions: only two, and neither is stored — `pending → complete` when the three conditions start holding, and
`complete → pending` when any of them stops holding (a carrier edit that reintroduces the literal, a declaration losing
its read point). There is no third state, no timestamp, and no per-unit status field anywhere.

## E-7 — Shared Read Entry（the one parser）

`scripts/python/declaration_reader.py` — importable by sibling engines (the script's own directory is `sys.path[0]` for
every `python3 scripts/python/<name>.py` invocation, in this repo and in a client project's `.specify/scripts/python/`),
and callable as a CLI for humans. It owns: reading `contract.yaml`, reading one fact, reading the exclusion rows,
normalizing paths (E-9), and refusing the subset violations (E-8's `declaration-outside-subset` reason). Sibling
precedent for an importable underscore-named module: `scripts/python/clause_extract.py`.

**R-7 single source of the parser.** A consumer that implements its own subset parser is a finding, not a style
problem: it is the exact mechanism (two copies of the same rule) this feature exists to remove.

## E-8 — Finding（closed six, instance form）

A finding is `(template, argument(s))`, rendered by substituting placeholders into the template verbatim — the
templates and their instance form are owned by `requirements.md` § Shared Strings (six templates, one of them taking
two arguments joined by `@`). No finding carries free text. Exit codes: `0` no finding, `1` at least one finding,
`2` input error or degraded wiring; the three meanings are owned by E-3's `exit_codes`.

The degraded-wiring class (a client project without the declaration layer) is an **exit-2 input-error label**, not a
seventh finding: the six-value set of `requirements.md` FR-017 is closed, and an input error is not a judgement about a
declaration.

## E-9 — Path normalization（the three-form problem）

The same declaration file exists in three forms (framework source, this repo's byte-identical mirror, a client project
copy whose text was rewritten to the `.specify/` form on the way in — see `research.md` § R3). Resolution rule: strip
**one optional leading `.specify/`** from a path value, then resolve against the repo root. Both forms therefore name
the same object, and a declaration written in source form is valid in all three copies. A path that still does not
resolve is the `[[STR-012]]` finding (for an anchor) or an input error (for a contract-level path).

## E-10 — Gate Call Site（contract-owned roster）

| Call site | What it does |
|-----------|--------------|
| `pre-analyze-check.py` with `--triple-structure` (stages requirements / plan / tasks) | delegates once to the checker's verify action and forwards each finding line verbatim under one check name; **off by default**, so the host's existing behavior and its closed four-name finding set are untouched |
| `tests/contract/test_harness_triple_structure.py` | pins the contract itself: the six reasons verbatim, the three exit codes, the subset rejection, the dual-writer paths, the coverage three-state readings |

Degradation at a call site: checker absent, or the declaration layer absent in the tree ⇒ exit-2 label plus an
explicit annotation, never an exception and never a pass.

---

## Fixture set (declarative inputs the rules are proved on)

One directory per feature, under `tests/fixtures/harness-triple-structure/`:

| Fixture | Proves |
|---------|--------|
| `positive/` | a small tree where every candidate is declared or excluded ⇒ exit 0, zero findings |
| `negative-<reason>/` (one per reason template) | the six reasons, each emitted verbatim with its exit code |
| `subset-violation/` | a declaration using a construct outside the subset ⇒ the subset reason, no best-effort parse |
| `dual-writer/` | two branches each adding one fact file ⇒ two distinct paths; coverage exits 0 on both trees |
| `legacy-project/` | no declaration layer at all ⇒ exit 2 with the degradation annotation, no traceback |
| `screen-boundary/` | a carrier that only mentions a script path in prose ⇒ enters the candidate set (conservative side) and is retired by one exclusion row |

Each negative fixture carries its expected `(exit code, reason instance)` as data, so the test compares strings instead
of re-deriving the template.
