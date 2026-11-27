# Contract — Declaration Domains and the Reader

**Feature**: 110 Context Management（上下文管理）(spec 110)
**Status**: design contract. Declaration-layer owner: `shared/declarations/contract.yaml`;
read entry: `scripts/python/declaration_reader.py`.

## C-010 — Four declaration facts own the machine value domains

**Statement**: four fact files under `shared/declarations/facts/` carry the closed domains, each written
in the declaration subset and carrying the required keys (`fact`, `kind`, `statement`, `consumers`,
`former_carriers`; `note` optional), mirrored to `.specify/shared/declarations/facts/`:

- `context-categories.yaml` — `kind: closed-set`; statement `invariant`, `variable`.
- `context-layers.yaml` — `kind: closed-set`; statement `system`, `project`, `task`, in composition order.
- `context-forms.yaml` — `kind: closed-set`; statement `pointer`, `read-in-full`, `bounded-index`,
  `runtime-discovery`, `inline-digest`.
- `context-classes.yaml` — `kind: mapping`; statement maps each layer to its ordered class ids, the roster
  the owner document's layout table matches row-for-row.

`consumers` names `scripts/python/context-audit.py` and the declarations guard; `former_carriers` is empty
because no earlier artifact carried these domains. Each fact registers in `shared/declarations/contract.yaml`
through the append-only flat block precedent (the 093/105 `<slug>: <path>` form), one key per slug,
before any consumer reads it.
**Red when**: a fifth domain file appears; a fact omits a required key or carries a member outside its
declared value; the classes mapping's order differs from the layout order; a fact is consumed without its
registration key.
**Test carrier**: `tests/contract/test_context_management_declarations.py` (fact-shape, registration and
membership legs).

**Serves**: (FR-018)

## C-011 — The domains are closed sets with one owner each

**Statement**: each domain is a closed set; membership, order and cardinality live only in its fact file.
The owner document names the tokens and their meanings; the engine validates every table cell against the
facts; the guards pin the three faces (facts, owner document, engine) member-for-member. The layer
domain's order is the composition order (`system → project → task`); the class mapping's per-layer order
is the layout's row order within that layer.
**Red when**: a token is defined in a second place; a member is added to prose but not to its fact; the
domains' orders disagree between the faces.
**Test carrier**: `tests/contract/test_context_management_declarations.py` (member-for-member legs);
`tests/contract/test_context_management_engine.py` (domain-consumption legs).

**Serves**: (FR-002, FR-003, FR-009, FR-018)

## C-012 — Every read goes through the shared declaration reader

**Statement**: the engine reads the four facts through `declaration_reader.load_fact` in process; it
implements no second YAML parser and carries no copy of a domain member. The owner document and these four
facts are the engine's declared input reads; the no-content boundary of C-034/C-035 binds the audited
sources, not this declaration layer. The layer root is the audited
workspace's own declaration layer: `<workspace-root>/shared/` when that framework-source layer (the owner
document plus the four `context-*.yaml` facts) is present, else `<workspace-root>/.specify/shared/`
(installed shape), where the workspace root is `--workspace-root` or the nearest ancestor holding
`.specify/`. One rule serves the framework source tree, a client project or fresh init tree, and a seeded
fixture carrying its own owner document and facts; running without `--workspace-root` inside an install
resolves the workspace root to that install, so engine, owner document and facts still pair. A workspace
root with no declaration layer under it is the input error of C-016, never a fallback to another root.
**Red when**: a fact value is hard-coded in the engine; a second parser appears; a read falls back to a
root outside the resolved layer root.
**Test carrier**: `tests/contract/test_context_management_declarations.py` (read-point locator legs);
`tests/contract/test_context_management_engine.py` (reader-consumption legs).

**Serves**: (FR-018, FR-021)

## C-013 — No numeric bound is declared anywhere in this feature's artifacts

**Statement**: the four facts carry no numeric bound field; the engine defines no threshold of its own;
every `bounded-index` row cites the cap owner path plus section, and every content-bearing row
(`read-in-full`, `inline-digest`) cites the same section as its exception owner
(`shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First)). The repository scan asserts that no new
numeric cap literal lands in this feature's artifacts.
**Red when**: a numeric bound field appears in a fact; the owner document or the engine states a cap
value; a bounded-index row cites no cap owner.
**Test carrier**: `tests/contract/test_context_management_declarations.py` (no-bound-field leg);
`tests/contract/test_context_management_engine.py` (cap-reference resolution leg).

**Serves**: (FR-019)

## C-014 — The presence vocabulary is defined once; `Unobserved` is reached by pointer

**Statement**: the five presence tokens — positive `present`, absence `absent` / `unreachable` / `empty` /
`not-evaluated` — have no prior framework owner in this repository, so this feature defines all five
exactly once, in the owner document. Every other surface cites the owner and MUST NOT restate the
definitions; no sixth token may be coined. Every absent or unusable source reports one of the four absence
tokens with a reason; a silent omission and an invented default are defects. A consistency claim derived
from an absent slot reads `Unobserved` under its evidence-state owner
(`shared/declarations/facts/evidence-seven-states.yaml#/statement`), never `present` and never agreement.
**Red when**: a presence token is defined in a second place; a sixth token is coined; an absence row omits
its reason; a consistency claim reads `present` with no evaluation behind it.
**Test carrier**: `tests/contract/test_context_management_owner.py` (definition-site leg);
`tests/contract/test_context_management_engine.py` (presence-vocabulary legs).

**Serves**: (FR-020, FR-028)

## C-015 — The roster agreement is machine-checked row-for-row

**Statement**: `context-classes.yaml`'s per-layer ordered ids are the single home of roster membership
and order; the owner document's layout table carries one row per roster id and is the single home of the
per-row data (`source`, `form`, `owner`, `cap reference`), its class-id column being the roster's
projection. `--action check` verifies that each layer's rows appear in exactly the declared order, that no
class id is missing or extra, and that no class id repeats across layers. A mismatch is one finding naming
the file, row and violated rule.
**Red when**: the roster and the table can diverge without a finding; the check compares sets but not
order; a missing or extra class id passes.
**Test carrier**: `tests/contract/test_context_management_engine.py` (roster-mismatch and order legs);
`tests/contract/test_context_management_declarations.py` (roster-consumption leg).

**Serves**: (FR-004, FR-018)

## C-016 — An unknown or missing declaration member is refused, never defaulted

**Statement**: a missing or unreadable declaration fact, or a member inside a declaration fact outside
its closed set (the categories, layers, forms and the classes roster alike), is an **input error**: both
actions refuse it with exit `2`, emit no partial verdict and guess no default. A pre-migration project
without the declaration layer is an input error, not a degraded pass. **Boundary**: an unknown layer or
form token in the owner document's layout table is a record-level defect, not an input error — `check`
reports it as the `unknown-layer` / `unknown-form` finding (C-032) with exit `1`, and the engine never
defaults it into a legal token.
**Red when**: an unknown declaration member is mapped to a default; a missing fact yields an empty roster;
the declaration-layer exit code drifts from `2`; a layout-table unknown token is treated as an input error
instead of its finding.
**Test carrier**: `tests/contract/test_context_management_declarations.py` (unknown-member legs);
`tests/contract/test_context_management_engine.py` (unknown-declaration-member and unknown-layout-token legs).

**Serves**: (FR-018, FR-021)