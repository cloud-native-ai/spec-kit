# Tool Record: trigger-utils.py

**Tool Name**: trigger-utils.py  
**Tool Type**: `project-script`  
**Source Identifier**: scripts/python/trigger-utils.py  
**Tool ID**: <TOOL:.specify/memory/tools/trigger-utils.py.md>  
**Aliases**: trigger-utils  
**Status**: Draft  
**Discovery Origin**: manual-entry  
**Last Updated**: 2026-09-08 (requirement 050: initial record, authored against the landed engine)

## Scope

**Availability**: Project-level — available only within the current project workspace (framework repo and client projects alike; the engine ships in `scripts/python/` and its `.specify/scripts/python/` mirror).  
**Typical Sources**: Scripts bundled with the project (`scripts/python/*.py`, mirrored to `.specify/scripts/python/`).  
**Portability**: Tied to the project repository; not available outside the project root.  
**Source Identifier Convention**: Path relative to the project root.

## Description

The proactive flow trigger engine (spec 050 — Proactive Flow Trigger): the deterministic half of the proactive-trigger mechanism — situation identity resolution, rule matching, consecutive counting, threshold promotion, telemetry, rotation, and evidence aggregation for rule tuning. Every semantic judgment (whether to adopt a tuning proposal, which situation a missed manual flow belongs to) stays with the agent and is handed back through `semanticJudgmentPending` (Program-First / Constitution Principle XII).

Design boundaries that are **contractually enforced, not stylistic** — what this tool will and will not do:

- The engine **never executes a flow**. `autoExecute` inside a suggestion is advice for the agent (C-21); no flow name is hard-coded in the engine — flows are seed data.
- **No network capability is imported** (C-19); all state is project-local. The only subprocess is a local `feedback-utils.py --action status` call inside probe P4.
- **Without `--probe`, no artifact file is opened** (C-13); probes emit bounded summaries, never artifact bodies.
- The engine **degrades instead of failing** on unreadable state (C-8): a blank state is rebuilt from the seed with a `state-unreadable` warning, and `assess` downgrades to `degraded: "suggest-only"`.

**Discipline owner (read-only)**: `.specify/shared/guidelines/proactive-trigger.md` — the situation vocabulary, promotion semantics, telemetry retention window, and tuning protocol are defined there; this record describes engine *behavior* and re-defines none of the model. Contract: `.specify/specs/050-proactive-flow-trigger/contracts/trigger-engine.md` (clause references C-n / V-n / E-n below point into the spec's contract set).

**Paradigm sources**: `derive-utils.py` (camelCase envelope, atomic write, graded exit codes). Threshold semantics are **isomorphic to `feedback-utils.py`'s** — the same priority-chain shape (explicit > environment > stored > default), with a different env var name (`SPECKIT_TRIGGER_THRESHOLD` vs `SPECKIT_FEEDBACK_THRESHOLD`) — deliberately re-implemented locally rather than imported, because `scripts/` is mirrored as independent STRICT copies and a cross-engine import would couple two separately mirrored files.

## Resource ID

- Canonical ID: `<TOOL:.specify/memory/tools/trigger-utils.py.md>`
- Canonical Path: `.specify/memory/tools/trigger-utils.py.md`

## Invocation & I/O Contract

- **Input Channel**: command-line flags (`--action` + the closed C-10 flag set). No stdin.
- **Invocation Mode**: non-interactive.
- **Output Mode**: exactly one JSON object on stdout by default (`--format json`, `ensure_ascii=False`, indent 2); `--format text` renders a bounded human summary (≤ 60 lines) from the **same** envelope — the two formats never compute separately.
- **Envelope (C-3)**: every response, in every action and on every exit path, carries exactly these nine camelCase top-level keys — `ok`, `action`, `workspaceRoot`, `generatedAt`, `errors[]`, `warnings[]`, `semanticJudgmentPending[]`, `notes[]`, `payload{}`. The four list keys are always arrays, never `null`. `ok` ⟺ exit 0 with empty `errors[]`, with **one contractual exception**: an `assess` that reports `ordering-violation` keeps `ok: true` at exit 0 (SC-012 — the turn still produced its telemetry; the violation is a reportable fact, not a failed call). The sibling of derive-utils' `semanticChecksPending` is deliberately named `semanticJudgmentPending` here. A parser-level usage error emits the envelope with `action: "unknown"` and `workspaceRoot: "."`, never bare argparse text.
- **Closed code set (C-22)**: `errors[]` / `warnings[]` carry codes from the engine's pinned set — `ordering-violation`, `state-unreadable`, `threshold-below-floor`, `vocabulary-out-of-range`, `no-prior-assess`, `rule-not-found`, `proposal-not-found`, `identifier-malformed`, `seed-unreadable`, `telemetry-unwritable` (plus `input-error: <exc>` on an unhandled `OSError`). Owner: contract C-22 / the engine's `CODES` constant.
- **State store**: `.specify/memory/trigger/` under the resolved workspace root.
  - `index.json` — **tracked** learning state (config, situations, rules, events, lastSuggestion, proposals, manualInvocations). Written atomically: `<path>.part` then `os.replace` (C-6 / V6.5), never half-written.
  - `telemetry.jsonl` — **git-ignored** per-turn churn (V6.9): `init` appends `.specify/memory/trigger/telemetry.jsonl` to the workspace root's `.gitignore` when absent. Append-then-truncate keeps the window bound after every write (V4.3, default `telemetryWindow: 200`).
  - Root resolution (C-7): explicit `--workspace` > engine self-location (fires only on a literal `.specify` component of the engine's own resolved path — the two-hats guard) > nearest `.specify` ancestor of CWD > CWD. A `--workspace` value resolving to a directory named `.specify` is lifted to its parent.
- **Seed**: `proactive-trigger-seed.json`, sought at `<root>/.specify/templates/` then `<root>/templates/`, falling back to the engine repo's `templates/`. The seed owns the situation vocabulary instances and the initial rules (including every flow name and invocation); `init` is idempotent — a seed refresh updates `rationale`/`invocation` wording but **never reverts a user's tuning** (V2.3).
- **Payload bounds (C-15)**: an `assess` payload rendered over 60 lines / 2000 chars is trimmed to its five identity keys with a note; snapshots and probe items are capped at 200 chars — artifact bodies never enter the store (V3.3).

### The eleven actions

Closed enumeration (C-9, argparse `choices`): `init`, `assess`, `record`, `record-manual`, `status`, `rules`, `reset`, `config`, `tune`, `tune-apply`, `rotate`.

| action | required | optional | writes | payload highlights |
|---|---|---|---|---|
| `init` | — | — | `index.json`; `.gitignore` (entry only when absent) | `created`, `situations`, `rules`, `config` |
| `assess` | `--stage` (to resolve a situation) | `--signal` (repeatable), `--session`, `--turn-id`, `--probe`, `--compliance-done` | `telemetry.jsonl` (exactly one row — **only `assess` writes telemetry rows**, V4.5) + `index.json` (rule stats, `lastSuggestion`) | `sessionId`, `turnId`, `stage`, `signals`, `situationId`, `suggestion{ruleId,flow,invocation,rationale,autoExecute}`, `suppressed`, `visibleOutput`, `enabled` (+ `reason`, `degraded`, `probes`) |
| `record` | `--rule`, `--response` | `--session` | `index.json` (event newest-first, stats, promotion) | `eventId`, `ruleId`, `response`, `consecutive`, `promoted`, `state`, `destructiveExempt` |
| `record-manual` | `--flow` | `--session` | `index.json` (`manualInvocations`) | `recorded`, `missed`, `flow`, `sessionId`, `turnId`, `suggested`, `situationId`, `ts` |
| `status` | — | `--session`, `--threshold` | zero | `config`, `ruleCountByState`, `promotedRules`, `pendingProposals`, `telemetry{rows,window,turns,escalated,suggested,visibleOutputCount,escalationPct,probeBudgetPct,budgetOver}` (C-23) |
| `rules` | — | — | zero | `rules[]` (full dump, sorted by id), `count` |
| `reset` | exactly one of `--rule` / `--all` | — | `index.json` | `reset[]`, `clearedSuppression`, `userResetAt` |
| `config` | — | `--threshold`, `--enabled`, `--window`, `--probe-budget`, `--min-sample` | `index.json`; telemetry truncation on `--window` | `config`, `changed[]`, `promotedRules` |
| `tune` | — | `--min-sample` | `index.json` (`proposals`) | `proposals[]`, `created`, `minSample`, `missedFlows` |
| `tune-apply` | `--proposal`, `--reason` | — | `index.json` | `proposal`, `ruleId`, `ruleState` |
| `rotate` | — | — | **only** `telemetry.jsonl` (truncate to window; `index.json` never touched — FR-009a / V4.4) | `rowsBefore`, `rowsAfter`, `window`, `indexTouched` |

## Parameters

The closed flag set (C-10 / C-14) — there are no flags beyond these:

| Name | Required | Description |
|------|----------|-------------|
| `--action` | yes | one of the eleven actions above (argparse `choices`, C-9) |
| `--format` | no | `json` (default) \| `text` |
| `--workspace` | no | workspace root override (C-7); a value resolving to a directory named `.specify` is lifted to its parent |
| `--stage` | for a situation match in `assess` | controlled-vocabulary stage token; out-of-range → `vocabulary-out-of-range`, exit 4. The vocabulary is a closed set pinned by the engine (`STAGES`) and owned by the discipline doc — never restated here |
| `--signal` | no | `assess`: repeatable controlled-vocabulary signal token (`SIGNALS`, same ownership) |
| `--session` | no | session id, grammar `^s[0-9A-Za-z-]{1,32}$`, default `sdefault`; scopes suppression, telemetry and `record`'s prior-assess requirement |
| `--turn-id` | no | `assess`: grammar `^<sessionId>-[0-9]{2,4}$` (V2.5); auto-derived from the session's telemetry row count when omitted |
| `--probe` | no | `assess`: escalate to probes P1–P5 (feature-artifact presence, open-clarification marker count, tasks.md checkbox counts, feedback-engine threshold fields, instructions-vs-template heading drift) — summaries only, each ≤ 200 chars; without it no artifact file is opened (C-13) |
| `--compliance-done` | no | `assess`: the caller **declares** that the same-pass compliance checks ran before the suggestion (V4.1); defaults to False on purpose — a suggestion emitted without it reports `ordering-violation` (still exit 0, `ok: true`) |
| `--rule` | for `record`; one reset target | rule id, grammar `^r-[0-9]{3}$` |
| `--response` | for `record` | `accepted` \| `declined` \| `ignored` (closed set); accepted increments `consecutive`, declined and ignored both reset it to 0 (V3.1/V3.2) |
| `--flow` | for `record-manual` | name of a flow the user ran by hand; when the session's latest telemetry turn was not a suggestion, it is recorded as missed-suggestion evidence and a binding question goes to `semanticJudgmentPending` (FR-015) |
| `--threshold` | no | `record` / `status` / `config`: explicit level of the threshold chain (see Behavioral Rules); a resolved value below the floor 2 is rejected by `config` with `threshold-below-floor`, exit 1 (V6.3) |
| `--enabled` | no | `config`: `true\|1\|yes\|on` / `false\|0\|no\|off`; re-enabling clears session suppression (V6.8) |
| `--window` | no | `config`: `telemetryWindow`; changing it immediately re-truncates `telemetry.jsonl` |
| `--probe-budget` | no | `config`: `probeBudgetPct` — the escalation budget `status` reports against (`budgetOver`) |
| `--min-sample` | no | `tune` (per-call) / `config` (stored): small-sample guard, default 5; rules below it are skipped **and named in notes**, never silently dropped (FR-017) |
| `--proposal` | for `tune-apply` | proposal id, grammar `^p-[0-9]{3}$` |
| `--reason` | for `tune-apply` | non-empty ratification reason; missing → exit 1 |
| `--all` | one reset target | `reset`: all rules, and clears `lastSuggestion` suppression so the first turn after a reset shows evidence (V6.8) |

The config key set is closed (E6): `enabled`, `threshold`, `telemetryWindow`, `probeBudgetPct`, `minSample` (defaults `true`, `3`, `200`, `20`, `5`). `tune`'s emission criteria are **contract constants, not config keys**: decline-rate ≥ 0.50 → `suppress`, ignore-rate ≥ 0.50 → `tighten`, missed invocations ≥ 2 → `add-rule`; proposal kinds are `tighten`/`suppress`/`add-rule`/`extend-vocabulary`, states `proposed`/`ratified`/`applied`/`rejected`.

## Behavioral Rules

- MUST treat this engine as the deterministic half only: it never executes a flow — `autoExecute` in a suggestion is advice for the agent (C-21), and flow names live in the seed data, not in the engine
- MUST declare the same-pass compliance ordering explicitly with `--compliance-done` when the caller has done it; a suggestion emitted without the declaration reports `ordering-violation` — a fact to fix in the calling flow, not a reason to discard the turn (telemetry is still written, `ok` stays `true`)
- MUST treat the stage/signal vocabulary as a closed set: expansion goes through the user-approval channel (`extend-vocabulary` proposal) only — the engine never coins a situation on the fly, and out-of-range tokens exit 4
- MUST keep `record` behind a prior `assess` in the same session: with no `lastSuggestion` entry it refuses with `no-prior-assess` (exit 2) rather than storing a half-formed event (V3.4)
- MUST treat a `destructive` confirmation class as never earning auto-execution, whatever the consecutive count (C-17 zero tolerance); promotion requires `consecutive >= threshold`, where `accepted` increments and `declined`/`ignored` reset to 0, and promotions are re-judged under the current threshold whenever it changes (V5.4)
- MUST resolve the threshold through the chain explicit `--threshold` > env `SPECKIT_TRIGGER_THRESHOLD` > stored config > default 3, with floor 2 — isomorphic to `feedback-utils.py`'s chain (different env var name); an unusable environment value downgrades silently to the next level and never breaks a turn
- MUST treat `tune` output as **proposals, not decisions**: adoption is a semantic judgment returned via `semanticJudgmentPending`, and only `tune-apply` with an explicit `--reason` ratifies and applies one — ratification and application are separately dated (SM-2), and for `add-rule`/`extend-vocabulary` the authoring of rule text and situation binding is handed back to the agent
- MUST pass `--workspace` explicitly when invoking a copy of the engine on behalf of a project other than the one its CWD resolves in; self-location fires only on a literal `.specify` component of the engine's own resolved path (two-hats guard), and the fall-through order is `--workspace` > self-location > nearest `.specify` ancestor > CWD (C-7)
- MUST NOT hand-edit `.specify/memory/trigger/index.json` or `telemetry.jsonl`: index writes are atomic (`.part` + `os.replace`), telemetry is append-then-truncate to the window, `rotate` is the telemetry-only maintenance path, and `init` is the idempotent seed reconciler (it preserves local tuning, V2.3)
- MUST NOT expect artifact bodies anywhere in the store or output: without `--probe` no artifact file is opened at all (C-13), and probe items, snapshots and payloads are size-bounded (200-char items; 60-line/2000-char assess payload, trimmed with a note)
- SHOULD read digests, not raw state: `status` for config/rule-state/telemetry digest with the budget verdict (C-23), `rules` for the full rule dump — never inject `index.json` into agent context (Summary-First)
- SHOULD reuse this engine instead of writing ad-hoc trigger-state code (Principle XII): counting, promotion, suppression, tuning and rotation are all behind the closed eleven-action enumeration

## Exit Codes

Graded exit codes (C-5), mirroring the `derive-utils.py` paradigm:

| Code | Constant | Meaning |
|------|----------|---------|
| `0` | `EXIT_OK` | success — **including** an assess with no situation match, a session-suppressed assess (V6.7/C-20: same session + situation + rule as the last suggestion), an idempotent `tune-apply` on an already-applied proposal, and an assess carrying `ordering-violation` (`ok` stays `true`, SC-012) |
| `1` | `EXIT_USAGE` | parser-level usage errors (unknown/missing `--action`, bad `--response` value, unknown flag) emitted as a JSON envelope with `action: "unknown"`, never bare argparse text; `reset` with neither `--rule` nor `--all`; `config` threshold resolving below the floor (`threshold-below-floor`); `tune-apply` with a missing/empty `--reason` |
| `2` | `EXIT_INPUT_ERROR` | `init` with a missing/unreadable/malformed seed (`seed-unreadable`); `record` with no prior assess in the session (`no-prior-assess`); any unhandled `OSError` (`input-error: <exc>`) |
| `3` | `EXIT_NOT_FOUND` | `rule-not-found` (`record`, `reset --rule`), `proposal-not-found` (`tune-apply`) |
| `4` | `EXIT_INVALID` | identifier or vocabulary violations: `identifier-malformed` (rule/proposal/session/turn-id grammar, non-boolean `--enabled`, non-integer config values), `vocabulary-out-of-range` (stage/signal outside the closed sets) |

## Environment Applicability

| Field | Value |
|-------|-------|
| Verified Version | python3 3.11.11 — 2026-09-08 scratch-workspace round-trip in this repository: `init` (seed 13 situations / 13 rules installed, `.gitignore` entry appended in the scratch root only) → `assess` (situation resolved, suggestion with `autoExecute` advice) → `record --response accepted` (consecutive/promotion math, event id grammar) → re-`assess` (`session-suppressed`) → `record` without prior assess (exit 2) → `status` telemetry digest → `rotate` (`indexTouched: false`) → error paths (exit 4 vocabulary, exit 3 rule-not-found, exit 1 usage envelope with `action: "unknown"`); nine-key camelCase envelope confirmed on every path |
| Version Differences | Requires Python >= 3.8 per the project's `pyproject.toml`; `from __future__ import annotations` keeps the PEP 604 signatures 3.8-safe (house pattern); the declared floor is **unverified** |
| Platform | linux (verified); standard library only (`argparse`, `datetime`, `json`, `os`, `re`, `subprocess`, `sys`, `pathlib`) — a third-party import is a contract failure (C-19); no OS-specific invocation known |
| Architecture | x86_64 (verified); no architecture-specific behavior known |
| Fallback | None — this is the only writer of `.specify/memory/trigger/`; do not hand-edit the store |
| Preflight Check | `python3 scripts/python/trigger-utils.py --help` (exit 0) |

**Status: Draft** — this record was authored against the landed source and one scratch round-trip, not against field invocation evidence. Promotion to Verified needs real agent-turn usage (and the declared Python floor exercised), not a re-read of this record; a `Draft` record does not satisfy the reuse gate and its `/speckit.tools` invocation is blocked by design (`.specify/shared/definitions/tool-definitions.md` § Edge Cases).

## Mirror

Canonical `scripts/python/trigger-utils.py` is mirrored byte-identical to `.specify/scripts/python/trigger-utils.py` by `sync-mirrors.py` — the pair is **strict** (`("scripts", ".specify/scripts", True, set())`), so the engine acquired its mirror automatically and an orphan mirror file fails `--check`: source and mirror must land in the same batch. Never hand-edit the mirror. The engine tolerates being invoked from the mirror in place: self-location fires only on the literal `.specify` path component (C-7 two-hats guard). By contrast the data root it writes, `.specify/memory/trigger/`, is project runtime state, **not** a mirror pair — of which `index.json` stays tracked while `telemetry.jsonl` is git-ignored (V6.9).
