# Tool Record: interview-utils.py

**Tool Name**: interview-utils.py  
**Tool Type**: `project-script`  
**Source Identifier**: scripts/python/interview-utils.py  
**Tool ID**: <TOOL:.specify/memory/tools/interview-utils.py.md>  
**Aliases**: interview-utils  
**Status**: Draft  
**Discovery Origin**: manual-entry  
**Last Updated**: 2026-08-06

## Scope

**Availability**: Project-level — available only within the current project workspace.  
**Typical Sources**: Scripts bundled with the project (`scripts/python/*.py`, mirrored to `.specify/scripts/python/`).  
**Portability**: Tied to the project repository; not available outside the project root.  
**Source Identifier Convention**: Path relative to the project root.

## Description

The decision-DAG engine behind `/speckit.interview` and the interview pattern (Feature 042). The command owns the conversation; this engine owns the deterministic half — dependency tracking, frontier computation, topological ordering, cycle rejection, conflict-candidate lookup, and **retraction propagation** (finding everything that transitively rested on a changed answer, reporting the artifact spans that must be rolled back, and re-opening those decisions). Graph reachability and ordering are fixed-rule computations, so they belong in a program rather than being re-derived in prose each run (Program-First / Principle XII).

State lives in a JSON sidecar beside the human-readable ledger (`interview-log.md` → `interview-log.dag.json`), so the markdown stays what a human reads while the graph stays machine-queryable.

Pattern authority: `shared/patterns/interview-pattern.md` (read-only for this engine).

## Resource ID

- Canonical ID: `<TOOL:.specify/memory/tools/interview-utils.py.md>`
- Canonical Path: `.specify/memory/tools/interview-utils.py.md`

## Invocation & I/O Contract

- **Input Channel**: command-line subcommands + flags
- **Invocation Mode**: non-interactive
- **Output Mode**: human text by default; `--json` for a machine-readable payload
- **Shared flags** (`--ledger`, `--json`) are declared per subcommand, so they follow the action name.

## Parameters

| Name | Required | Description |
|------|----------|-------------|
| subcommand | yes | One of `init`, `add`, `answer`, `defer`, `frontier`, `order`, `descendants`, `retract`, `conflicts`, `status`, `render` |
| `--ledger PATH` | yes | Path to the markdown ledger; the JSON store is its `.dag.json` sidecar |
| `init --target PATH [--mode special\|informal] [--branch NAME ...] [--force]` | — | Create the store; refuses to clobber without `--force` |
| `add --id D4 --question T [--depends-on D1 ...] [--branch NAME]` | — | Declare a decision and its premises |
| `answer <id> --decision T [--span T] [--round N]` | — | Settle a decision and record where it wrote |
| `defer <id> --reason T` | — | Mark out-of-scope (⏭) without dropping it |
| `frontier` | — | Decisions askable now, dependency-ordered |
| `order` | — | Full topological order, most-depended-on first |
| `descendants <id> [--direct]` | — | What rests on a decision, transitively unless `--direct` |
| `retract <id> [--decision T] [--apply]` | — | Propagate a changed answer; **dry-run unless `--apply`** |
| `conflicts --with T` | — | Settled decisions sharing terms with a candidate answer |
| `status` | — | Counts, stale rows, decisions missing a span, exit-gate readiness |
| `render` | — | Regenerate the markdown ledger table from the graph |

## Behavioral Rules

- **RULE-1**: IDs match `^[A-Za-z][A-Za-z0-9_.-]*$` and are **never reused** — `add` refuses an existing ID. A reused ID silently rewrites history and breaks every `dependsOn` pointing at it.
- **RULE-2**: A dependency cycle is refused at insertion time (exit `4`). A retraction walk over a cyclic graph would not terminate, and a cyclic premise set is unanswerable by construction.
- **RULE-3**: `answer` refuses a decision whose premises are not all settled (exit `4`). This is the pattern's "never ask a blocked question" rule made mechanical.
- **RULE-4**: The frontier counts **only `settled`** premises as satisfied. A `deferred` or `retracted` premise does not unblock its dependents.
- **RULE-5**: `order` breaks ties by **descendant count, descending** — the `I1` rule that widely-depended-on premises are asked first, so a late retraction costs less.
- **RULE-6**: `retract` is **dry-run by default**, reporting `descendants`, `invalidated`, and `needs_rollback` (id + span) so the blast radius is visible before anything changes. `--apply` re-opens the invalidated decisions and clears their stale spans.
- **RULE-7**: `retract` **never edits the target artifact.** It reports the spans; rolling them back belongs to the caller, which is the only party that knows how to edit that artifact.
- **RULE-8**: `conflicts` returns **candidates, not verdicts** — a shared-term filter that narrows the field so the model judges a handful of rows instead of the whole ledger. Whether two decisions truly conflict is never the engine's call.
- **RULE-9**: `descendants` is transitive by default and reports each node **once** (a diamond dependency does not duplicate). Breadth-first order means premises come before what depends on them.
- **RULE-10**: `status.exit_gate_ready` is true only when nothing is open or awaiting an answer **and** no settled decision has an unsettled premise (`stale`). The gate is mechanical; the user's confirmation still governs.
- **RULE-11**: This engine owns the `.dag.json` store and nothing else. It never writes the interview's target artifact, and `render` regenerates the markdown table from the graph rather than parsing it back.

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | ok |
| `2` | input error — invalid ID, reused ID, bad mode, or an existing store without `--force` |
| `3` | not found — missing store, unknown decision ID, or unknown premise |
| `4` | validation failed — dependency cycle, answering a blocked decision, corrupt store |

## Environment Applicability

- **Verified against**: Python 3.11 in this repository (2026-08-06), 39 unit tests in `tests/unit/test_interview_utils.py` plus a full end-to-end CLI run (init → add → order → frontier → answer → retract dry-run → `--apply` → conflicts → render). No third-party dependencies — standard library only.
- **Unverified**: other Python versions and platforms. Status stays **Draft** until exercised on the project's declared floor (`>=3.8`) in CI, and until a live interview has driven it end-to-end with a real user.

## Mirror

Canonical `scripts/python/interview-utils.py` is mirrored byte-identical to `.specify/scripts/python/interview-utils.py` by `sync-mirrors.py`. Never hand-edit the mirror.
