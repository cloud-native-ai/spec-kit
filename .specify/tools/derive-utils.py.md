# Tool Record: derive-utils.py

**Tool Name**: derive-utils.py  
**Tool Type**: `project-script`  
**Source Identifier**: scripts/python/derive-utils.py  
**Tool ID**: <TOOL:.specify/memory/tools/derive-utils.py.md>  
**Aliases**: derive-utils  
**Status**: Draft  
**Discovery Origin**: manual-entry  
**Last Updated**: 2026-09-05 (requirement 048 / Feature 049: engine conformed to its contract; record rewritten against the landed code)

## Scope

**Availability**: Project-level — available only within the current project workspace (framework repo and client projects alike; the engine ships in `scripts/python/` and its `.specify/scripts/python/` mirror).  
**Typical Sources**: Scripts bundled with the project (`scripts/python/*.py`, mirrored to `.specify/scripts/python/`).  
**Portability**: Tied to the project repository; not available outside the project root.  
**Source Identifier Convention**: Path relative to the project root.

## Description

The derivation engine behind `/speckit.derive` (Feature 049 / requirement 048). It owns the deterministic half of the Derivation model — monotonic identity issuance for the project-level move library, structural validation of a derivation archive against the chain-integrity and self-audit rule sets, two-level (exact + slot-isomorphic) dedup on append, bounded link-liveness probing that leaves an unfabricable evidence trace, and counting/distribution reporting. The command owns interaction and every semantic judgment: reading a source's actual argument, abstracting its inference shape into a move, grading provenance, naming a discriminating question, deciding which termination condition fired, and attesting the two semantic audit checks. Fixed rules live in the program, not in the model (Program-First / Constitution Principle XII).

**Concept authority (read-only)**: `shared/definitions/derivation-definitions.md` — the six record schemas, the provenance grades, chain rules C1–C7, the self-audit set A1–A16, the closed banned-justification literal set and the capability-degradation rule are defined there. This record describes engine *behavior* and re-defines none of the model.

**File contracts (cited, never restated)**:

| Contract | Owns |
|---|---|
| `.specify/specs/048-derive-command/contracts/derive-engine.md` | CLI form, flag table, envelope, exit codes, write authority, per-action payload schemas |
| `.specify/specs/048-derive-command/contracts/derivation-model.md` | enforcement face of C1–C7 and the audit set, `normalize_text`, the warning set, degradation (the 048 contract predates the criterion layer; A15/A16 are defined in the anchor) |
| `.specify/specs/048-derive-command/contracts/move-library.md` | `moves.md` physical form, identity issuance, dedup, `status` state machine, small-file threshold |

## Resource ID

- Canonical ID: `<TOOL:.specify/memory/tools/derive-utils.py.md>`
- Canonical Path: `.specify/memory/tools/derive-utils.py.md`

## Invocation & I/O Contract

- **Input Channel**: command-line flags (`--action` + per-action flags) and JSON spec files passed by path via `--file`. No stdin.
- **Invocation Mode**: non-interactive.
- **Output Mode**: exactly one JSON object on stdout by default (`--format json`, `ensure_ascii=False`, indent 2); `--format text` renders a human-readable summary (error/warning/note lines carrying `rule`/`code`/`locator`, the audit projection, a one-line count summary) from the **same** internal result — the two formats never compute separately.
- **Envelope**: every response, in every action and on every exit path, carries exactly these nine top-level keys — `ok`, `action`, `workspaceRoot`, `generatedAt`, `errors[]`, `warnings[]`, `semanticChecksPending[]`, `notes[]`, `payload{}`. **All action-specific data lives inside `payload`**; there is no flat per-action object. The four list keys are always arrays, never `null`. `semanticChecksPending` is `["A11", "A14"]` on `validate` and `[]` on the other five actions (they do no self-audit). `generatedAt` is UTC `%Y-%m-%dT%H:%M:%SZ`; `workspaceRoot` is the resolved absolute path. Schema: `contracts/derive-engine.md` §4.
- **Configuration**: storage locations are module constants (RULE-2); the engine reads no environment variable, config file, or artifact field to locate them. Environment is read for one purpose only — naming a SOCKS egress proxy in a `probe-links` note (RULE-18).

### The six actions

| action | required | optional | writes | payload key set |
|---|---|---|---|---|
| `init` | `--slug <topic-slug>` | `--force`, `--max-steps <int>` | `.specify/derive/<slug>/derive.md`; `moves.md` **only if absent** | `slug`, `archivePath`, `movesPath`, `created[]`, `clobbered`, `backupPath`, `maxSteps`, `terminationCondition` |
| `validate` | **exactly one** of `--file <path>` / `--slug <slug>` | `--max-steps <int>` | zero | `file`, `topic`, `degraded`, `sources{}`, `steps{}`, `moves{}`, `elements{}`, `openQuestions{}`, `audit{engine,semantic}` |
| `moves-list` | — | `--name-contains`, `--status`, `--anchor` | zero | `total`, `returned`, `projection`, `filters{}`, `librarySize{lines,bytes}`, `fullReadAllowed`, `moves[]` |
| `moves-add` | `--file <json>` | — | **only** `moves.md` (RULE-4) | `requested`, `appended`, `deduped`, `superseded`, `issued[]`, `dispositions[{moveId,disposition}]`, `duplicates[{requestIndex,normalizedForm,existingMoveId}]` |
| `probe-links` | `--file <json>` | — | zero | `probed`, `online`, `degraded`, `results[{url,access,resolvedVia,httpStatus,snapshotTs,error,evidence}]` |
| `stats` | — | `--file <path>` **or** `--slug <slug>` (either, or neither) | zero | `moves{total,byStatus,duplicateIds,duplicateForms}`, `dispositions{new,reused,reinforced}`, `archives{total,topics[]}`, `lastRun` |

Per-action payload semantics, including which grouping keys are always the full enum: `contracts/derive-engine.md` §5.

## Parameters

| Name | Required | Description |
|------|----------|-------------|
| `--action` | yes | exactly one of `init`, `validate`, `moves-list`, `moves-add`, `probe-links`, `stats` (argparse `choices`) |
| `--workspace-root` | no | workspace root, default `.`; a value resolving to a directory named `.specify` is lifted to its parent, so the mirror can be invoked in place |
| `--format` | no | `json` (default) \| `text` |
| `--slug` | for `init`; alternatively for `validate` / `stats` | topic slug; grammar `^[A-Za-z0-9][A-Za-z0-9_.\-]*$` — the identity grammar `goal-utils.py` uses, deliberately not a second one. **The flag is `--slug`; there is no `--topic`** (that was the pre-conformance name) |
| `--file` | for `moves-add` / `probe-links`; alternatively for `validate` / `stats` | `validate` / `stats`: archive path. `moves-add`: JSON object `{"moves": [{...}]}`. `probe-links`: JSON object `{"urls": ["<url>", ...]}` |
| `--force` | no | `init`: re-scaffold over an existing archive. The current content is **kept** as `derive.md.bak` in the same directory; `payload.clobbered` is `true` and `payload.backupPath` names it. `--force` never touches `moves.md` |
| `--max-steps` | no | derivation step budget; must be a positive integer. Two-level resolution only: explicit flag > `DEFAULT_MAX_STEPS = 12`. The budget declared in the artifact's `## Termination` does **not** participate — it is a report, cross-checked (RULE-14) |
| `--name-contains` | no | `moves-list`: case-insensitive substring filter on `name` |
| `--status` | no | `moves-list`: `active` \| `superseded` — the durable library enum. A run-relative disposition (`new` / `reused` / `reinforced`) is rejected with exit 2 |
| `--anchor` | no | `moves-list`: filter value, grammar-validated against `^S-\d{3,}$` **or** `^<topic-slug>\.S-\d{3,}$`. Matching is exact against the stored cell items, and stored anchors are always qualified, so a bare `S-<nnn>` filter is accepted but can never match (`returned: 0`, exit 0) |

**There is no `--timeout`** (nor `--limit`, `--offline`, `--dry-run`). The probe timeout is the module constant `PROBE_TIMEOUT_SECONDS = 10`, and offline behavior is automatic degradation (RULE-18), not a switch.

**`moves-add` input** (all-or-nothing; any violation → exit 2 with **zero writes**):

```json
{"moves": [{
  "name": "<label>",
  "inferenceForm": "<inference shape with `backticked` named slots>",
  "prevents": "<the failure mode this move prevents>",
  "appliesWhen": "<applicability condition AND an over-application guard>",
  "anchor": "<topic-slug>.S-<nnn>[, <topic-slug>.S-<nnn> ...]",
  "intent": "new | reuse | reinforce | supersede",
  "existingMoveId": "M-<nnn>   (required by reuse / reinforce / supersede)"
}]}
```

Keys are **camelCase**. There is no `topic` key — the engine reads `moves` only, which is exactly why `anchor` must arrive already qualified (RULE-9).

## Behavioral Rules

- **RULE-1 — the anchor owns the model.** Schemas, the grade set, C1–C7, A1–A16, the banned-justification literals and the degradation rule come from `shared/definitions/derivation-definitions.md`. The engine holds *pinned copies* of the literals (`BANNED_JUSTIFICATIONS`) and of the small-file threshold (RULE-19); a drift test asserts each pinned copy equals its owner. Never treat this record, or the engine's constants, as the definition.
- **RULE-2 — paths are constants.** `ARCHIVE_DIRNAME = ".specify/derive"`, `MOVES_FILENAME = "moves.md"`, `ARCHIVE_FILENAME = "derive.md"`. Nothing relocates the store: no environment variable, config file, or artifact field is consulted.
- **RULE-3 — `.specify/derive/` is deliberately NOT a `sync-mirrors.py` mirror pair.** It is project runtime state (same class as `.specify/goal/` and `.specify/specs/`), never shipped framework material. Registering it in `MIRROR_PAIRS` would make `specify init`'s additive copytree push one project's move library into every downstream project. `sync-mirrors.py --check` must stay green with the root present. Rationale and clause: `contracts/move-library.md` §7.
- **RULE-4 — `moves.md` has exactly one writer, and it writes atomically.** `moves-add` is the only code path that opens the library for writing. `init` may *create* it once when missing (prose header + engine marker + column header + separator, zero data rows) and never rewrites an existing one — not even under `--force`. `validate` / `moves-list` / `probe-links` / `stats` are zero-write, and `validate` is zero-write on the archive too (RULE-11). Every library write goes to `<moves.md>.part` first, then `os.replace` — a crash leaves the previous library intact, never a half-written one; an `OSError` on write is reported as exit 2, `code: library-write-failed`.
- **RULE-5 — the library's physical form is pinned and hand edits are detected, never repaired.** Title line `# Reasoning Move Library`, the engine-written marker comment, the header `| move_id | name | inference_form | prevents | applies_when | anchor | status |` and the separator `|---------|------|----------------|----------|--------------|--------|--------|` are literals the engine compares against; `anchor` cells are `, `-separated and qualified-only (RULE-9). `validate` and `stats` re-check these invariants independently of write-time discipline and report `moves-library-hand-edited` with a sub-cause. The engine never auto-fixes, re-sorts or renumbers — repair is a human edit followed by `validate`, or a legitimate `moves-add`. Literal forms: `contracts/move-library.md` §1.
- **RULE-6 — dedup is two-level, and refusing is the success path.** Level 1 is the exact normalized `inference_form`; level 2 is the *slot-isomorphic* form — backticked tokens and standalone single uppercase letters both collapse to `<SLOT>`, because a slot name carries no semantics and the same shape written with different slot letters is one move. Normalization itself is `normalize_text` (NFKC → casefold → drop Unicode `P*`/`S*` and ZWSP/BOM → collapse whitespace → empty becomes `None`); there are no similarity thresholds and no edit distance. On a hit the engine writes **no new row**, returns the existing id in `duplicates[].existingMoveId`, increments `deduped`, and records the disposition as `reinforced` when the request brought a fresh anchor or `reused` when it did not. **Exit code 0** — refusal is success, not an error. Never dedup on `name`. Clause: `contracts/move-library.md` §3.
- **RULE-7 — `intent` says what this run does; `status` says what the library holds.** `new` appends (or dedups into `reinforced`/`reused`); `reuse` writes nothing and only reports a disposition; `reinforce` grows the existing row's `anchor` in place and requires at least one anchor the row does not already carry (else exit 2, `code: reinforce-without-new-anchor`); `supersede` migrates the row's durable `status` to `superseded`. The last three require `existingMoveId`. `superseded` is **terminal**: only `active → superseded` is legal, a superseded row can never be reused, reinforced or revived, and citing one in an artifact is an A9 error. Need the shape again? `moves-add` writes a **new** row. The run-relative triple `new` / `reused` / `reinforced` is payload output and must never appear in the library's `status` column. State machine: `contracts/move-library.md` §4.
- **RULE-8 — identity issuance is split by writer.** `M-<nnn>` is the only engine-issued identity: `moves-add` issues it **project-wide**, monotonic at `max(existing) + 1`, zero-padded to at least three digits, never reused, never renumbered. `S-<nnn>`, `D-<k>`, `A-<k>` and `Q-<k>` are **written by the agent** into the archive; the engine validates their grammar and monotonicity but does not issue them, because issuance is only meaningful on a file the engine solely writes. `S-` matches `^S-\d{3,}$` — three **or more** digits, so `S-1000` is legal and `S-99` is not; its cross-topic qualified form matches `^<topic-slug>\.S-\d{3,}$`. `D-` / `A-` / `Q-` match `^(D|A|Q)-\d{1,}$` and are compared numerically, never lexicographically. Clause: `contracts/derive-engine.md` C-27.
- **RULE-9 — anchors in the library must be qualified, and a bare reference is refused.** The library is project-wide while `S-<nnn>` is per-topic, so a bare `S-003` stored in a library row could not be resolved from any later topic. `moves-add` carries **no topic** (see the input schema under Parameters), so it cannot qualify a bare reference itself — it refuses the whole request with exit 2, `code: input-schema`, rather than guessing a slug. Anchors are stored `, `-separated, sorted by slug segment then `S-` number, and only ever grow: the engine unions existing with fresh.
- **RULE-10 — library invariants gate appends, and the refusal is exit 2.** Before issuing anything, `moves-add` validates the *existing* library; if any invariant fails it refuses the entire request with exit **2** (`EXIT_INPUT_ERROR`), `code: moves-library-hand-edited` and a note explaining that it will not renumber its way past the damage. This is an input conflict, not a validation verdict — `validate` and `stats` report the same damage as exit **4** because there the artifact/library *is* the subject. The invariants checked: id grammar, duplicate id, non-monotonic id, `status` outside the durable two-value enum, empty `inference_form`, two rows sharing a slot-isomorphic form, unqualified `anchor`, missing marker/header/separator literals.
- **RULE-11 — the self-audit is a two-pass loop, because `validate` is zero-write.** A1–A10, A12, A13 and A15 are **derived** from `errors[]` (each A row maps a closed set of error codes; zero hits → `pass`), and the artifact's own `## Self-Audit` rows must equal those derived values or the engine reports rule `A0`, `code: audit-result-diverges`. Consequences worth knowing before you call it: a freshly scaffolded archive carries `pending` in all sixteen rows and therefore does **not** validate clean — it exits 4 with thirteen `audit-result-diverges` errors. The converging sequence is: run `validate` → transcribe `payload.audit.engine` into the A1–A10/A12/A13/A15 rows → set A11, A14 and A16 to `attested` with a checkable `method` sentence → run `validate` again. A11/A14/A16 are agent attestations the engine never judges `pass`; their result is closed to `attested` / `not-attested` / `pending`, and `pending` is a to-do, not a failure. A `method` cell that is empty, `engine` or `n/a` draws the `attestation-method-degenerate` warning.
- **RULE-12 — read the verdict from `ok` and the exit code, not from the audit table.** Not every error code is mapped into an A row: a step carrying two moves (`move-count-not-one`), a confidence outside the enum, a non-reciprocal `contested-with`, a derivation under `DERIVATION_MIN_CODEPOINTS = 40`, or a conclusion identical to a source title rejects the file with exit 4 while `payload.audit.engine` reads `pass` for all twelve rows. The audit table is the A-check projection; `ok` is the verdict.
- **RULE-13 — engine-computed fields are not agent-assertable.** `title_mismatch` is recomputed from normalized titles and a stated value that disagrees is an A1 error; a mismatch is a **two-title** assertion, so an empty `resolved_title` computes to `false` plus an `unresolved-title` warning — absence of evidence is not evidence of retitling. `access: unknown` forces `grade: unverified`. `verification` must be ≥ `VERIFICATION_MIN_CODEPOINTS = 16` codepoints and outside the closed bare-attestation set (`verified`, `checked`, `已核实`, `-`, …); a cell with no recognizable evidence token (URL, three-digit HTTP status, snapshot timestamp, `search: …` / `result #n`) is a **warning**, not an error — the reject list is the hard floor. Thresholds and the token set: `contracts/derivation-model.md` §6.
- **RULE-14 — the budget is the flag, and the declaration is cross-checked.** Effective budget = explicit `--max-steps` > `DEFAULT_MAX_STEPS = 12`; a non-positive value is exit 2. More steps than budget is an error (hitting a budget is reported, never silently truncated); exactly at budget is the `step-budget-reached` warning. The artifact's `- steps: <n> / <budget>` line is parsed and compared — a divergence in either number is `step-budget-diverges`, because the engine's count is authoritative and the declared line is the run's self-report, never a second source of truth. `- condition: a|b` is required.
- **RULE-15 — one error per fact; the warning set is closed.** Errors are deduped by `(rule, locator)`, so one defect that several rules would each flag surfaces once; warnings are not deduped. The `warn()` call raises if the code is outside the closed six (`secondary-sole-anchor`, `unresolved-title`, `verification-evidence-token-absent`, `step-budget-reached`, `attestation-method-degenerate`, `degraded-run`), so a seventh warning code cannot be shipped by accident.
- **RULE-16 — a degraded run is honest, and faking a chain is rejected.** When the source table is non-empty, *every* row is `unverified`, *every* `verification` normalizes equal to `no-online-capability`, there are zero `D-` steps and no element carries a statement, then `validate` exits **0** with `payload.degraded == true`, a `degraded-run` warning and a note beginning `no-online-capability:` — and `payload.steps.total` / `.anchorable` are both 0. Add a single step under those conditions and it flips to exit 4 (`premise-grade-ineligible`, both per-step and section-level), `degraded` flips to `false`, and the `degraded-run` warning disappears. Partial degradation is never treated as degradation: one non-`unverified` row runs the full rule set.
- **RULE-17 — `_http_get` is the single transport seam, and no test may call it against the real network.** All network I/O in the module goes through `_http_get(url, timeout) -> (status | None, body | error)`; it is the only place a request is made, which is what makes "no test touches the network" mechanically assertable rather than a promise. Unit tests monkeypatch it; contract tests assert the seam is unique and that every `probe-links` test file carries the patch. Per URL the engine runs the first two Dead-Link Protocol steps only — direct fetch, then the archive availability API — and the third (attribution search) is the agent's action, never the engine's. It fetches one URL plus at most one availability query: it is a corroborator, not a crawler, and it never caches a body. Clause: `contracts/derive-engine.md` §7.
- **RULE-18 — a network failure is not a dead link.** Any transport exception (DNS failure, timeout, TLS error, connection refused) degrades that one result to `access: "unknown"` with the exception class and message in `error` / `evidence`, and the whole action still returns **exit 0** with `payload.online == false`, `payload.degraded == true` and a degradation note. The engine emits `dead` only on a definitive HTTP 404 from the origin; `dead` as a *judgment* after the attribution search also misses belongs to the agent. **SOCKS proxy**: stdlib `urllib` has no SOCKS support, and this project's own runtime depends on `httpx[socks]` for exactly that reason — so in an environment exporting `ALL_PROXY` / `HTTPS_PROXY` / `HTTP_PROXY` as a `socks5://` (or `socks4://`) URL, *every* probe degrades to `unknown` and the engine adds a note naming the offending variable. `probe-links` returning all-`unknown` in a proxied environment is **expected** and is NOT evidence that the sources are dead; ground them with the host agent's own fetch/search tool and cite that evidence in the `verification` column.
- **RULE-19 — the small-file threshold is a pinned copy, and the engine returns a verdict, not a number.** `SMALL_FILE_MAX_LINES = 100` and `SMALL_FILE_MAX_BYTES = 10240` are pinned copies of the threshold owned by `shared/guidelines/token-efficiency.md`, kept equal by a drift test. `moves-list` reports `librarySize{lines,bytes}` and the boolean `fullReadAllowed` (both conditions satisfied) so the caller's read-escalation decision is a program verdict; the engine never restates the threshold values in its output. Over the threshold, the `moves-list` projection is the mandatory read path — it is always a summary-first projection (`payload.projection == true`), seven fields per row, never the library's raw text.
- **RULE-20 — no-clobber on `init`.** An existing archive is refused with exit 2 plus a hint pointing at amend-in-place; `--force` re-scaffolds and keeps the previous content as `derive.md.bak`, reporting `clobbered: true` and `backupPath`. `--force` with a non-existent topic is just a normal create (`clobbered: false`). `init` never touches an existing library, never goes online, never issues an `M-`, and never fills in an audit result.

### Divergences found against the contracts — and how each was resolved

The conformance pass reproduced eight engine-vs-contract divergences against the landed code. **All eight are now closed.** Five were engine defects and were fixed in the engine; three were contract clauses that were themselves wrong, unsatisfiable, or contradicted a sibling clause, and were amended in the contract with the reason recorded inline. They are listed here as a resolution record so the next agent does not re-chase them.

| # | Divergence as found | Resolution | Side changed |
|---|---|---|---|
| 1 | `validate` payload carried a `topic` key that C-19 does not list | key removed; the slug is recoverable from `file` | engine |
| 2 | Usage errors exited **2** with bare argparse text and no JSON, so `EXIT_USAGE = 1` was unreachable | a `_Parser` subclass raises `_UsageError` instead of exiting; `main()` catches it and emits the envelope with `action: null` at exit **1** | engine |
| 3 | `urllib.request.quote` was called outside `_http_get`, violating C-30/C-33(a)'s source scan | replaced with a local RFC 3986 `_percent_encode` (verified byte-equivalent to `quote(safe="")` on ASCII, punctuation, spaces and CJK), so the seam keeps its contracted **two-parameter** signature and no transport-library reference exists outside it | engine |
| 4 | A3 (`resolved-title-not-cited`) was enforced on `premises` only, though C-23 and the anchor's Title-Mismatch Protocol extend the duty to `leads` | now enforced on both | engine |
| 5 | `probe-links` emitted `resolvedVia: ""` on transport failure — outside the enum | emits `null`; C-22 amended to `resolvedVia: str\|null`, because a probe that never ran resolved nothing and `null` is the honest value | both |
| 6 | The run-relative `move_id \| disposition` table that C-23 and SC-003 read could not coexist with a clean `validate`: any line matching `^\| M-\d{3,} \|` was treated as a restatement row, so contiguous rows gave exit 4 (`unmarked-move-copy`) while interleaving projection markers broke the table's contiguity and made `stats` read all-zero dispositions | a line is a restatement **only if it actually carries the library's columns**; a row with fewer cells than the move record copies nothing from the library and is the disposition log `stats` reads | engine |
| 7 | Two library clauses unimplemented: `anchor-removal-refused` (C-20) and the C-4/C-8 row-shape checks | row-shape and ordering checks **implemented** (exactly seven non-empty cells, no blank or non-table lines between rows, exactly one trailing newline). `anchor-removal-refused` proved **unreachable by construction** — the input schema has no removal verb and the write is union-only — so C-20 was amended to state the guarantee as structural and reserve the code for a future explicit-removal input | both |
| 8 | A dedup hit with no fresh anchor reported `reused` where C-21 literally required `reinforced` | the engine was right and C-21 contradicted move-library C-19 ("`reinforced` without a new anchor *is* `reused`"); C-21 amended to require a genuinely new anchor for `reinforced` | contract |

## Exit Codes

`ok == true` ⟺ exit code 0, on every path. There is no "ok: true with exit 4" combination available to disguise a failure.

| Code | Constant | Meaning |
|------|----------|---------|
| `0` | `EXIT_OK` | success — **including** zero findings, zero filter hits (`moves-list`), a dedup refusal (RULE-6), a degraded run (RULE-16), and `probe-links` with every URL offline (RULE-18) |
| `1` | `EXIT_USAGE` | unknown or missing `--action`, or a flag the action does not accept. Emitted as a JSON envelope with `action: null` and code `usage-error`, never as bare argparse text |
| `2` | `EXIT_INPUT_ERROR` | invalid or missing `--slug`; `--slug` and `--file` both given or both missing where one is required; non-positive `--max-steps`; missing `--file`; input file unparseable or not a JSON object; empty/non-list `moves` or `urls`; `moves-add` schema violation including an unqualified anchor (all-or-nothing, zero writes); `--status` outside the durable enum; `--anchor` grammar failure; illegal `intent` transition (`illegal-status-transition`, `reinforce-without-new-anchor`); `init` against an existing archive without `--force`; library unfit to append to (`moves-library-hand-edited` via `moves-add`, RULE-10); library write failure |
| `3` | `EXIT_NOT_FOUND` | archive not found (`validate`, `stats`), or `--file` names a file that does not exist (`moves-add`, `probe-links`) |
| `4` | `EXIT_INVALID` | `validate` / `stats` produced a non-empty `errors[]` — any mechanical C1–C7 or A-check violation, including the A0 audit-table divergences and library invariants observed on the read path |

## Environment Applicability

- **Verified against**: Python 3.9.6 on macOS (darwin) in this repository, 2026-09-05 — all six actions re-exercised end to end on scratch workspaces after the conformance rewrite (`init` → `init --force` with `.bak` → `moves-add` two new moves → slot-isomorphic dedup refusal → bare-anchor refusal → hand-edited-library refusal → `moves-list` filtered projection → `probe-links` fully degraded behind a SOCKS proxy → `validate` fresh-scaffold exit 4 → two-pass convergence to exit 0 → community/unverified premise rejection → degraded-run exit 0 and its step-added flip to exit 4 → `stats` with and without a target).
- **Unverified**: the project's declared floor (Python `>= 3.8`) under CI, and Linux. **Status: Draft** — promotion to Verified needs invocation evidence on those environments, not a re-read of this record.
- **Dependencies**: standard library only (`argparse`, `datetime`, `json`, `os`, `re`, `sys`, `unicodedata`, `urllib.request`, `urllib.error`, `pathlib`). `from __future__ import annotations` keeps the PEP 604 signatures 3.8-safe (house pattern from `goal-utils.py`), and the one place a runtime `dict | dict` union would have been natural is written out explicitly for the same reason. A third-party import is a contract failure.
- **Version differences**: none known — no third-party surface. `response.status` is read with a `getcode()` fallback for older HTTP response objects.
- **Platform**: cross-platform, no platform-specific code path. Network egress is the only environment sensitivity: a SOCKS-only proxy makes every probe degrade to `access: unknown` (RULE-18), which is named in a note rather than silently absorbed.
- **Fallback**: `probe-links` is the sole action that leaves the machine; the other five are fully offline. A host with no online capability at all still gets a usable engine — the artifact records the degradation and validates clean with zero steps (RULE-16).
- **Preflight**: the command template probes `python3` + engine presence (three-state probe convention) and the host's online capability before stage 2.

## Mirror

Canonical `scripts/python/derive-utils.py` is mirrored byte-identical to `.specify/scripts/python/derive-utils.py` by `sync-mirrors.py`. The pair is **strict** (`("scripts", ".specify/scripts", True, set())`), so the new engine acquired its mirror automatically and an orphan mirror file fails `--check`: source and mirror must land in the same batch. Never hand-edit the mirror. The engine tolerates being invoked from the mirror in place (RULE-2 / `--workspace-root` lifting). By contrast the data root it writes, `.specify/derive/`, is **not** a mirror pair (RULE-3).
