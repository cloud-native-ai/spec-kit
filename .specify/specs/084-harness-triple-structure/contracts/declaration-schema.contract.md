# Contract — Declaration Layer Schema（`shared/declarations/`）

**Feature**: 084 Harness 三重结构 | **Date**: 2026-11-05
**Owner of the value domains this contract references**: `shared/declarations/contract.yaml` (E-3). This document
names keys and shapes; it MUST NOT become a second copy of any value domain. Where a literal appears below it is
`[[STR-NNN]]`, owned by `requirements.md` § Shared Strings.

- **DS-01** The declaration layer is the directory `shared/declarations/` in the framework source, with exactly three
  members: `contract.yaml`, `facts/`, `exclusions/`. Any other member at that level is outside this contract.
- **DS-02** `contract.yaml` is the only aggregated file. It owns: `schema`, `yaml_subset`, `fact_kinds`,
  `completeness_states`, `exclusion_reasons`, `exit_codes`, `required_fact_keys`, `required_exclusion_keys`,
  `gate_call_sites`. A consumer reads these keys; it MUST NOT inline any of their values.
- **DS-03** A fact declaration is one file per fact at `facts/<fact-slug>.yaml`. `<fact-slug>` matches
  `^[a-z0-9]+(-[a-z0-9]+)*$` and equals both the `fact` key and the filename stem. No second identifier namespace is
  introduced for facts.
- **DS-04** `required_fact_keys` (as declared in `contract.yaml`) are present in every fact file. `note` is the only
  optional key. An unknown top-level key is an input error, not a forward-compatible extension.
- **DS-05** `consumers` and `former_carriers` are disjoint, and every entry resolves after path normalization (DS-10).
  `consumers` means "must read this fact"; `former_carriers` means "used to carry this literal, must now be a pointer".
  Conflating them is a schema violation because it destroys the residual-literal reading.
- **DS-06** An exclusion record is a row inside `exclusions/<reason>.yaml`, where `<reason>` is one of
  `contract.yaml`'s `exclusion_reasons` written as the filename. At most one file per reason, at most as many files as
  there are reasons. Rows carry `unit`, `carrier`, `anchor`; `unit` is unique across all reason files.
- **DS-07** An exclusion `anchor` MUST resolve in the tree. An unresolvable anchor is the `[[STR-012]]` finding with
  exit 1 — never a warning, and never silently dropped as "no longer applicable".
- **DS-08** **YAML subset** — allowed: block mappings, block sequences, scalars (plain / single- / double-quoted),
  comments, two-space indentation; `[]` and `{}` only as empty values. Forbidden: anchors and aliases, explicit tags,
  multiple documents, block scalars (literal `|` and folded `>`), and every flow collection. A forbidden construct is
  the `[[STR-010]]` finding; a best-effort parse that "mostly works" is a contract violation, not a lenient success.
- **DS-09** The subset grammar has one implementation — the shared read entry (`contracts/shared-reader.contract.md`).
  A second parser anywhere (including a consumer engine) is `SR-07`'s violation.
- **DS-10** **Path values** are written in source form (no `.specify/` prefix). Resolution strips exactly one optional
  leading `.specify/` before resolving against the repo root. Reason: `specify init` rewrites source-form references to
  the `.specify/` form while copying (`research.md` § R3), so one file has three physical copies with two textual forms.
- **DS-11** `shared/declarations/`, `facts/`, `exclusions/` are registered in `shared/definitions/framework-map.md` in
  the same change that creates them, with kebab-case names and a one-line meaning each (Directory Governance).
- **DS-12** No aggregated ledger, index, manifest or cache file is created at any level. Unit dispositions are derived
  by reverse projection on every run (Concurrent Development Safety: 派生索引即读即建).

## Worked shape (illustrative, not a value domain)

The block below shows the *shape* of a fact file. Every literal value in it is illustrative only; the authoritative
values live in the migration batches (`contracts/migration-batches.contract.md`) and in `contract.yaml`.

```yaml
fact: <fact-slug>
kind: <one of contract.yaml fact_kinds>
statement: <scalar, sequence, or mapping>
consumers:
  - scripts/python/<engine>.py
  - shared/workflow/<carrier>.md
former_carriers:
  - shared/workflow/<carrier>.md
note: <optional human-readable remark>
```

## Verification (per-example premises)

No command in this contract was executed at plan time: the layer and its checker do not exist yet on this branch.
Route (b) applies, per example, with the premises each one rests on:

| Example | Pinned by | Premises to re-measure, not inherit |
|---------|-----------|--------------------------------------|
| subset rejection (DS-08) | `tests/contract/test_harness_triple_structure.py` negative fixture `subset-violation/` | the subset identifier is a `contract.yaml` key; the finding text is the `[[STR-010]]` template verbatim; the exit code is `1` for a finding and `2` for an unreadable/invalid input — the boundary between them is measured by the fixture, not assumed |
| unresolvable anchor (DS-07) | same module, negative fixture for the anchor reason | `anchor` grammar (path plus a locatable line or section); the tree used by the fixture |
| path normalization (DS-10) | same module, one case per textual form (source form and `.specify/` form) | `rewrite_paths()` in `src/specify_cli/__init__.py` still rewrites `shared/`, `scripts/`, `skills/…` on copy — re-read it if it changes |
