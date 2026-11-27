# Contract — Audit Engine, Determinism and Distribution

**Feature**: 110 Context Management（上下文管理）(spec 110)
**Status**: design contract. Script-interface rule owner:
`shared/definitions/script-interface-definitions.md`; mirror pairs: `scripts/python/sync-mirrors.py`;
framework map: `shared/definitions/framework-map.md`; instructions generator:
`scripts/bash/generate-instructions.sh`.

## C-030 — One documented entry, two actions, no wrapper

**Statement**: the entry is `scripts/python/context-audit.py` (installed at
`.specify/scripts/python/context-audit.py`), a single-file Python-stdlib read-only script. `--action check`
runs the layout integrity reading; `--action manifest --layer <system|project|task>` prints one layer's
rows. Flags: `--workspace-root PATH`, `--json` (both actions), `-h`/`--help` (identical body), `--version`.
No `/speckit.*` command and no skill wrapper ships in this version; the documented invocation is the only
entry.
**Red when**: a second entry point or action appears; a flag differs; obtaining a manifest requires an LLM
step or a hand-composed query.
**Test carrier**: `tests/contract/test_context_management_engine.py` (CLI-surface legs);
`tests/integration/test_context_management_init.py` (installed-copy entry leg).

**Serves**: (FR-021, FR-026)

## C-031 — Script interface contract satisfied

**Statement**: the engine answers `-h` and `--help` (identical body) with usage, options, side effects
(`none`) and exit-code meanings; `--version` prints one machine-readable identity line derived at run time
from the nearest `pyproject.toml` through the house helper (`scripts/python/script_interface_cli.py`), with
`unknown` an allowed form when no reachable `pyproject.toml` exists; every flag is answered before any
read; an undeclared option exits `2` before any action, including after a bare `--`. The closed usage-error
set: an unknown option (incl. after bare `--`) exits `2` before any action; `manifest` without `--layer` or
with a `--layer` outside the domain exits `2`; `--layer` combined with `check` exits `2`; an unresolvable
workspace root or a missing owner document / declaration layer exits `2`.
**Red when**: a required flag content is missing; a version literal lives in the source; an unknown option
reaches an action or exits `0`; a usage-error case exits `1`.
**Test carrier**: `tests/contract/test_context_management_engine.py` (interface legs);
`scripts/python/script-interface-check.py` stays green for the new engine.

**Serves**: (FR-021)

## C-032 — `check` verifies the layout and reports findings deterministically

**Statement**: `--action check` parses the owner document's layout table and the four facts — the engine's
declared input reads (C-012); every layout row's declared sources remain metadata-only (C-034, C-035). Its closed
rule set: `roster-mismatch` (a layer's class set differs from the roster), `roster-order` (membership equal
but in-layer order differs), `unknown-layer`, `unknown-form`, `layer-form-illegal` (the matrix),
`duplicate-class`, `empty-layer` (the finding names the side — roster or layout — and the layer),
`cap-missing` (a bounded-index row without a cap reference), `category-column` (a header outside the fixed
six columns, judged by the header alone). Every finding names the file, the row and the violated rule.
The `unknown-layer` and `unknown-form` rules apply to **layout-table** tokens: such a token is a finding,
never an input error. A member of a **declaration fact** outside its domain is the input error of C-016
(exit `2`), never a finding. Exit `0` clean, `1` findings, `2` usage, unreadable input or an unknown or
missing declaration member.
**Red when**: a rule is missing or silently passes; a finding lacks file/row/rule; a declaration-layer
unknown member exits `1` instead of `2`; a layout-table unknown token exits `2` or is defaulted instead of
producing its finding; two runs on an unchanged tree differ.
**Test carrier**: `tests/contract/test_context_management_engine.py` (check legs and one seeded-violation
fixture per rule; the four named fixtures are unknown-layer, unknown-form, roster-mismatch and
layer-form).

**Serves**: (FR-009, FR-021, FR-022)

## C-033 — `manifest` prints one layer's rows with source, form, presence and cap

**Statement**: `--action manifest --layer <layer>` prints, per roster class of the layer in roster order —
the roster declared by `context-classes.yaml` is the row set, not the current layout rows: class id,
layer, form, resolved source(s), presence token and reason (on absence), and cap reference. A roster class
whose layout row is missing still prints, its form / source(s) / cap fields reading `—` and its token
`not-evaluated` with the reason naming the missing layout row (E-10, FR-028); the layout-versus-roster
mismatch itself is C-032's `roster-mismatch` finding — a separate reading that may co-occur. Presence
follows the form's witness: standing paths (resolving, readable, non-empty by actual type), or a bounded
read-only probe for `runtime-discovery` rows. The JSON form carries the same fields with ordered keys
(`action`, `layer`, `rows` with `class`/`layer`/`form`/`sources`/`token`/`reason`/`cap`, `counts`,
`source_reading`) and per-token counts; the text form ends with one `source-reading: <digest>` line over
the printed layer's declared sources. Exit `0` whenever a manifest is emitted (absence rows included),
`2` on usage or declaration failure. No timestamps, no host values and no document content enter the
output; a resolved root appears only as a workspace-relative path.
**Red when**: a roster class's row is omitted; an absence row lacks its reason; a host value or timestamp
enters the output; absences exit non-zero; the text and JSON faces disagree.
**Test carrier**: `tests/contract/test_context_management_engine.py` (manifest legs; the
missing/empty/unreadable fixture and the all-present fixture);
`tests/integration/test_context_management_init.py` (fresh-init absence lines).

**Serves**: (FR-006, FR-007, FR-020, FR-021)

## C-034 — The audit is honest and never substitutes for composition

**Statement**: the engine performs no semantic task selection, no relevance ranking and no content reading
of **audited sources** — the sources the layout rows declare; its only content reads are the declared
inputs (the owner document's layout table and the four facts, C-012/C-032) plus the `--version` identity
source (C-031). Relevance stays with the composing agent. A broken source appears as a presence reading with a
reason, never as a skipped row. The engine never reports `present` for a source it did not evaluate and
never claims agreement beyond pointer presence and resolvability.
**Red when**: the engine ranks, selects or reads an audited source's content; a broken source vanishes; an
unevaluated row reads `present`.
**Test carrier**: `tests/contract/test_context_management_engine.py` (honesty legs);
review of the engine source against this clause.

**Serves**: (FR-022, FR-028)

## C-035 — Read-only, offline and private

**Statement**: no audit action writes any file, creates a directory or cache, or opens a network socket;
the reading consumes only audited sources' paths, metadata and presence states, and never raw user text or
conversation content; the only content reads are the declared inputs of C-012/C-032 and the `--version`
identity source of C-031. The existing feedback red lines and confirmation gates stay unchanged and unreferenced by any new
gate.
**Red when**: any action writes; a socket is opened; an audited source's content is consumed; a new gate or red line
appears.
**Test carrier**: `tests/contract/test_context_management_readonly.py` (hash-manifest containment,
zero-new-files and socket-guard legs); `tests/integration/test_context_management_init.py`
(network-blocked run).

**Serves**: (FR-024)

## C-036 — Distribution rides publish → install → init and lands map rows

**Statement**: the owner document, the four facts (with their four registration keys in
`shared/declarations/contract.yaml`), the engine and the framework-map edit are framework sources that ride
the existing flow: `sync-mirrors.py` projects `shared → .specify/shared`, `scripts → .specify/scripts` and
`templates → .specify/templates`; the `specify init` flow installs the `shared/`, `scripts/` and
`templates/` trees into a client project; mirrors are generated, never hand-edited. The framework map gains
three rows: the owner document, the four context value-domain facts (one directory entry), and the audit
entry with its documented invocation.
**Red when**: a mirror differs from its source; a fresh init fixture lacks one of the artifacts; a
framework-map row is missing or does not resolve.
**Test carrier**: `tests/integration/test_context_management_init.py`;
`python3 scripts/python/sync-mirrors.py --check` compared against the baseline in
`test-evidence/mirror-baseline-plan.txt`.

**Serves**: (FR-023)

## C-037 — One ambient section, summary plus pointer, inside the generator's budget

**Statement**: `templates/instructions-template.md` gains one top-level section headed
`## Context Management(上下文管理)`, propagated into the live `.specify/instructions.md` by
`scripts/bash/generate-instructions.sh`'s additive section reconcile. The section states baseline-once /
task-per-selection, the pointer-not-content rule and the absence-names-the-gap rule, and points at the
owner document and the audit entry. It carries no layout table, no class roster and no cap literal. The
generator's `BUDGET:` report is the judge of its size under the existing constant; the budget is not
raised and no existing section is trimmed — a section that does not fit is an anomaly to surface, not a
silent escalation.
**Red when**: the section is absent from either surface; it carries a table, a roster or a cap literal;
it exceeds the generator's budget and the plan silently raises the constant or trims sections instead of
surfacing the anomaly.
**Test carrier**: `tests/contract/test_context_management_owner.py` (ambient-section legs);
`tests/contract/test_instructions_section_propagation.py` stays green.

**Serves**: (FR-025)