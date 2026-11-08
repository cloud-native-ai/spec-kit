# Data Model — Feature 089 脚本接口契约（Script Interface Contract）

**Feature**: 089-script-interface-contract | **Date**: 2026-11-06 | **Plan**: [plan.md](./plan.md)

This feature stores no runtime data. Its entities are the artifacts and verdicts the contract makes
machine-decidable, and its validation rules are the conditions a guard or the checker asserts. Each entity
names its carrier (the file or program that holds it); each rule names the contract clause that enforces it
(`contracts/script-interface-criteria.contract.md` C-1…C-13, `contracts/contract-checker-cli.contract.md`
C-14…C-22, `contracts/governance-landing.contract.md` C-23…C-32, `contracts/mirror-projection.contract.md`
C-33…C-38).

## Entities

### E-1 — Candidate

The unit of judgement: one file the candidate screen found.

| Field | Meaning | Carrier |
|-------|---------|---------|
| `path` | repo-relative path | engine output (`--json` `candidates[]`) |
| `discovered_by` | `tracked` · `walk-only` | engine (`source` cell of the screen report) |
| `ignored` | whether `git check-ignore` matched it (ignored ⇒ not a candidate) | engine |
| `language` | `bash` · `python` | engine (extension) |

Rules: V-1 (screen), V-2 (coverage assertion). Relationship: E-1 1—1 E-2 (every candidate gets exactly one
class), E-1 0—1 E-5 (a candidate may be registered as a declared exception).

### E-2 — Classification

The sandbox verdict that decides whether the contract applies.

| Field | Meaning | Carrier |
|-------|---------|---------|
| `applicable` | `true` · `false` | engine (`--json` `candidates[].applicable`) |
| `basis` | one of the closed set below | engine |
| `evidence` | marker line / observed effect (bash) or import/exit observation (python) | engine (`candidates[].evidence`) |
| `projected` | `true` when the candidate is a mirror copy whose same-path source is declared as projected | engine |

`basis` closed set: `entry-point-marker` (bash marker fired) · `entry-point-side-effect` (python produced an
effect outside the interpreter's import machinery) · `no-entry-point` (marker never fired) ·
`imported-only` (python: importable module with no effect) · `projected-mirror` (a mirror copy with a same-path
source; class inherited from that source, obligation carried by the bridge) · `mirror-unpaired` (a mirror copy
with no same-path source — 73 skills-side copies, 81 across `.specify/`) · `declared-exception`
(registered in E-5 and recomputed true).

Rules: V-3 (bash), V-4 (python), V-5 (both uses ⇒ applicable), V-6 (mirror).

### E-3 — Contract verdict (four conclusions per applicable candidate)

| Field | Meaning | Carrier |
|-------|---------|---------|
| `help` | `-h` and `--help` both exit 0 with non-empty output | engine |
| `help_content` | the four mandated labels present: `usage`, `options`, side-effect statement, exit codes | engine |
| `version` | `--version` exits 0 and prints `<script-name> <framework-version>` on one line | engine |
| `unknown_rejected` | an undeclared `-*` token exits non-zero, exits before the main action, prints an error and usage | engine |
| `zero_side_effect` | the sandbox fingerprint is unchanged across the three flag runs and one unknown-option run | engine |

Rules: V-7 (help content), V-8 (version source), V-9 (rejection), V-10 (zero side effect), V-11 (help wins).

### E-4 — Check report

| Field | Meaning |
|-------|---------|
| `schema` | `script-interface-check/1` |
| `mode` | `full` · `files` · `emit-rule` · `check-projection` |
| `source` | `tracked` · `walk-only` |
| `root` | the resolved repository root |
| `candidates` / `applicable` / `exempt` / `violations` | counts |
| `exemptions[]` | `path`, `basis`, `evidence` — one row per exempt candidate, never a bare path list |
| `exceptions[]` | `path`, `skill`, `recomputed` (`true`), `unsatisfied_clause` |
| `findings[]` | `message`, `paths[]` |
| `projection[]` | declared mirror pairs and their projection kind |
| `rule` | emitted only under `--emit-rule`: `labels`, `flag_forms`, `separator`, `version_line`, `version_source`, `exempt_basis`, `findings`, `exceptions` (eight keys) |
| `elapsed_ms` | measured, never estimated |

Rules: V-12 (report completeness), V-13 (exit codes).

### E-5 — Declared exception

| Field | Meaning | Carrier |
|-------|---------|---------|
| `path` | the script | owner page `## Declared Exceptions` table, one row per script |
| `skill` | the skill directory that ships it | same |
| `unsatisfied` | the clause that cannot be met without rewriting upstream | same |
| `handling` | the reduced obligation actually satisfied | same |
| `recomputed` | checker recomputation result (never stored in the page) | engine |

Rules: V-14 (recomputation), V-15 (not-in-page ⇒ ordinary candidate).

### E-6 — Owner page (the single definition point)

| Field | Meaning |
|-------|---------|
| `owns` | the five declared items, listed at the top of the page |
| `rule` | the classification rule, in the same vocabulary `--emit-rule` emits |
| `exceptions` | the E-5 table |
| `mirror` | `.specify/shared/definitions/script-interface-definitions.md`, byte-identical |

Rules: V-16 (pointer discipline), V-17 (rule/page agreement).

### E-7 — Governance landing

| Field | Meaning | Carrier |
|-------|---------|---------|
| `template_principle` | the new principle on `templates/constitution-template.md` | that file |
| `live_principle` | the same title on `.specify/memory/constitution.md`, its own next numeral | that file |
| `mandate_entry` | the `- **<title>** — …` entry inside `- **MUST include**` | `skills/internal/manage-constitution/SKILL.md` |
| `ambient_section` | `## Script Interface Contract` | `templates/instructions-template.md` + `.specify/instructions.md` |
| `counts` | `TEMPLATE_COUNT` / `LIVE_COUNT` / `COMMAND_COUNT` / watchlist length | `tests/contract/test_constitution_double_landing.py` |
| `section_counts` | `TPL_EXPECTED` / `LIVE_EXPECTED` | `tests/contract/test_fast_fail_discipline.py` |

Rules: V-18 (title equality across surfaces), V-19 (counts move with the landing), V-20 (ambient section shape).

### E-8 — Evidence snapshot

| Field | Meaning |
|-------|---------|
| `tree` | the sandbox copy root (outside the measured tree) |
| `status` | `git status --porcelain` output |
| `hashes` | `sha256` of every `*.sh` / `*.py` in the measured tree |
| `specify_manifest` | file list and hashes under `.specify/` |
| `before` / `after` | the two snapshots; equality is the zero-side-effect assertion |

Rule: V-10.

## Validation rules

| ID | Rule (decidable) | Clause |
|----|------------------|--------|
| V-1 | Candidates = `git ls-files '*.sh' '*.py'` minus `git check-ignore` matches; with git unavailable the walk result is the candidate set and the report says `source=walk-only`. | C-1 |
| V-2 | Every `*.sh` / `*.py` in the work tree is a candidate or is ignored; anything else is `candidate-not-collected`, exit 1. | C-2 |
| V-3 | bash is applicable iff the modified copy, run as a script with a declared option, emits the marker that the patch placed after the recognized-option trigger. | C-3 |
| V-4 | python is applicable iff running it with a declared action produces an effect outside the interpreter's import machinery. | C-4 |
| V-5 | Applicability is monotone in evidence: a file that both is imported/sourced and executes on direct run is applicable. | C-5 |
| V-6 | A mirror copy with a same-path source inherits that source's class and carries its declared projection; a mirror copy with **no** same-path source (`mirror-unpaired`: 73 skills-side copies, 81 across `.specify/`) is judged on its own run semantics like any other candidate. The candidate set is never de-duplicated by path; only the probe count may be. | C-6 |
| V-7 | An applicable file's `--help` output contains `usage`, `options`, a side-effect statement and exit codes — as four labels, not as one blob. | C-7 |
| V-8 | `--version` prints exactly `<script-name> <framework-version>`; the version is read from `pyproject.toml` at run time and equals the value in that file; no literal appears in any script. | C-8 |
| V-9 | An undeclared `-*` token exits non-zero, produces its output before the main action, and never reaches a write. | C-9 |
| V-10 | The before/after snapshot pair of the four flag runs is identical (status, hashes, `.specify/` manifest). | C-10 |
| V-11 | With `--help` and a write-triggering option both present, the help path wins regardless of order. | C-11 |
| V-12 | `--json` carries per-candidate rows and the totals; no exempt candidate is a bare path without a basis. | C-18 |
| V-13 | Exit `0` iff `violations == 0` and no structural finding; `1` for any violation or structural finding; `2` for argument/environment errors. | C-17 |
| V-14 | Every row in `## Declared Exceptions` recomputes true (path exists, under `skills/external/<skill>/`, that `SKILL.md` says `classification: external`); a failing limb is `exception-unverifiable`, exit 1. | C-30 |
| V-15 | A third-party candidate absent from the page is judged as an ordinary candidate, never auto-exempted. | C-12 |
| V-16 | No surface other than the owner page carries the four mandatory help-content labels or the classification rule's step list. | C-29 |
| V-17 | `--emit-rule` output and the owner page agree on the label set and the class vocabulary (set equality, both directions). | C-21 |
| V-18 | The principle title is identical on the template and the live roster; numerals are per-surface and pinned by nothing. | C-24, C-25 |
| V-19 | Adding the principle + ambient section raises `TEMPLATE_COUNT` 18→19, `LIVE_COUNT` 19→20, `COMMAND_COUNT` 11→12, watchlist 6→7, `TPL_EXPECTED` 32→33, `LIVE_EXPECTED` 33→34 in the same commit. | C-28 |
| V-20 | The ambient section carries a summary (≤ 2 sentences), the owner path, and zero engine-invocation forms (`--action`, `$ARGUMENTS`, `<placeholder>`). | C-27 |
| V-21 | The owner page lists the five owned items at its top and declares itself the single source. | C-23 |
| V-22 | A mirror script equals `source + declared projection`; re-projecting is idempotent (running twice changes nothing). | C-34, C-35 |
