# Phase 0 Research — Speckit 框架可视化（Speckit Framework Visualization）

**Feature**: 087 | **Date**: 2026-11-06 | **Stage base**: `56f3f881`
**Method note**: every reading below was **measured against the working tree on 2026-11-06**, not recalled. Where a
document and the tree disagreed, the measurement is quoted and the document is treated as stale (constitution
VIII). Each reading carries the command that produced it so a later reviewer can re-measure instead of trusting
this file.

**Reading-id namespace (disambiguation, not a second vocabulary)**: the `RO-nn` headings **in this file** are
*research readings* — a Phase 0 numbering of measured observations, closed at `RO-15`. They are **not** the guard
propositions, whose `RO-01`…`RO-13` namespace is owned by `contracts/reporting-obligations.contract.md` C-01…C-13.
The two namespaces share a spelling and nothing else; a reference that means a guard proposition says so and cites
the contract, and a reference that means a reading cites this file.

## RO-01 — The repository is the framework source, and every delivery path is mirrored by an existing engine

`python3 scripts/python/sync-mirrors.py --check` → `EXIT=0`;
`OK: all per-tool command copies match the source templates.`;
`ok` for every pair: `templates/` == `.specify/templates/` (22 files), `skills/external/` == `.specify/skills/`
(415), `skills/internal/` == `.specify/skills/internal/` (138), `agents/` == `.specify/agents/templates/` (16),
`scripts/` == `.specify/scripts/` (121), `shared/` == `.specify/shared/` (94).

*(Post-delivery reading, added at implement Part 6 — `test-evidence/polish-mirror-check.txt` § 3: the same six pairs
read `ok` with `EXIT=0`, at `templates/` 22, `skills/external/` 415, `skills/internal/` 139, `agents/` 17,
`scripts/` 122, `shared/` 95. The four increments are the four new framework-source files; the reading above is left
as the pre-change measurement it is, not rewritten into the post-change one.)*

**Consequence**: the baseline drift is **zero**, so every mirror obligation in `plan.md` can state "no NEW drift"
as a passable criterion instead of an absolute "all green" that a future unrelated drift would fail. The pair
mapping is not uniform and matters for path shapes: `skills/external/<name>/` → `.specify/skills/<name>/` (the
`external/` component is dropped), `agents/` → `.specify/agents/templates/` (the subtree is renamed). `scripts/` is
the only **STRICT** pair (a file present on one side only FAILS `--check`).

## RO-02 — The progress-reporting channel already exists, owns the interactive default, and is contract-pinned

`shared/guidelines/progress-reporting.md` (96 lines) owns: the default interval (**15 分钟**, line 23), its anchor
(task start, not last report), the override precedence (user instruction > project instruction file > file
default), the four-element content floor (§ 汇报内容下限), the measured-figures rule, the atomic-step deferral
rule, "reporting is not a gate", the dispatch-payload injection clause (§ 子代理与委托（派发时注入）), and two
"不引入机制" clauses (lines 27 and 96) that already forbid a timer, a background reporting channel, a persisted
report artifact and an extra process.

`tests/contract/test_progress_reporting.py` pins the owner doc, the instructions ambient section and the mirror.

**Consequence**: the new owner must not touch that literal or restate the content floor; it adds a **second,
declared profile** selected by one condition and reaches the floor by section anchor. Requirements A10 and FR-020
already fix this; the measurement confirms the constraint is real (the literal and the pinned test both exist).

## RO-03 — The subagent model already owns the three modes and the visibility carrier

`shared/definitions/subagent-definitions.md` (134 lines): § Three Execution Modes is a 3-row table whose
`Progress visibility` column states, for mode 3 (external), "**Not automatic** — MUST follow the Visibility
Contract below"; § External Dispatch Visibility Contract point 3 fixes the artifact triplet
(`<label>.live.log`, `<label>.jsonl`, `<label>.status`) and point 4 fixes liveness monitoring by `.live.log`
growth; § Dispatch-Time Governance Obligation already names the dispatch-payload channel for the fast-fail clause
and declares "the clause's owner literal … is defined once in `.specify/shared/guidelines/fast-fail.md`
§ 子代理派发注入; this section MUST reference it and MUST NOT restate it".

**Consequence**: FR-013's "same way the fast-fail clause and the progress obligation already are" has a precedent
with a real anchor. The new owner's reporting obligation rides that same channel; `subagent-definitions.md` gains
**one pointer line**, not a second copy of the duty. No fourth mode and no second carrier is needed: mode 1 renders
natively, mode 2 is inline in the visible session, and mode 3's declared stream artifact is the carrier — so
FR-014's "no mode is left without a surface" is already true and only needs to be *stated* as a duty.

## RO-04 — Team creation already has a roster schema, a create procedure and deterministic helper scripts

`skills/internal/create-team/SKILL.md` (258 lines) + `references/create-mode.md`: the team schema is a YAML
frontmatter block with `members[]` (`agent`, `role`, `lifecycle`, plus `territory` / `blockedBy`), `seats` (074a
per-seat SDD policy), `stage_seats` (085), `territory` (team level), `config`, and the four pattern blocks.
`references/create-mode.md` step 4 already says a roster row carries "**responsibility** (stage, territory,
`blockedBy`, reporting duty)". `skills/internal/create-team/scripts/` already ships three deterministic helpers
(`match-team-preset.py`, `verify-territory-disjoint.py`, `dispatch.sh`).

**Consequence**: D3 is supported by the schema as it stands — "reporting duty" is already named as a roster-row
concern, so a reporter seat is a member row with `role: reporter`, not a schema widening. D4 is supported by the
directory precedent: a stdlib-only `validate-roster.py` beside `verify-territory-disjoint.py` is the house form,
and the create procedure (step 6) already has a place to call it.

**Measured absence**: no script today validates a roster against any obligation — `verify-territory-disjoint.py`
checks territory disjointness only. So the guard is genuinely new work, not a redirection.

## RO-05 — Tool-record lookup (Tool Reuse gate) — no Tool covers a current-state digest

`ls .specify/memory/tools/` shows the shipped Tool records; they cover shell/git/memory/feedback/history utility
families. Reading `.specify/shared/workflow/tool-reuse-gate.md`'s criterion (a capability worth repeating,
pre-verified, environment-specific invocation), a current-state digest is a **read of this framework's own state
shapes**, not a reusable environment capability.

**Consequence**: authoring `scripts/python/status-digest.py` is the expected outcome under constitution XII
("Where no Tool exists, writing the code is the expected outcome"). Premise EP-002.

## RO-06 — The line registry is the only owner of line state, and its entry fields are enough for a digest

`python3 skills/external/sdd-loop-driver/scripts/line-registry.py --action list --all --format json` returned, per
entry: `branch`, `line_id`, `project_dir`, `run_id`, `stage`, `state`, `updated_at` (plus nullable fields not set
in every entry). The engine's own header documents its file layout:
`$REGISTRY/<line_id>.json` (atomic replace), `<line_id>.lock`, `manifests/<line_id>.json`,
`<line_id>.driver.lock`, `reservations/<line_id>.<stage>.json`. `STATE_VALUES` (line 55) is the closed 8-value set
`{active, waiting, stalled, completed, orphaned, stale, closed, blocked}`; `ACTIVE_STATES = {active, waiting}` is
the engine's own "currently running" predicate.

`resolve_registry_dir()` (line 146) resolves, in order: `$SPECIFY_LINE_REGISTRY_DIR`, `$XDG_STATE_HOME/spec-kit/lines`,
`~/.local/state/spec-kit/lines`.

**Consequence**: the digest needs **no new query surface** — a read-only listing plus the per-entry fields already
exists, and the engine's own `ACTIVE_STATES` defines "running" so the digest does not invent a second predicate.
The registry lives **outside the repository** by default, which is why the digest must resolve the directory the
same way and never hardcode `.specify/state/`.

**Correction to the requirements' wording (disclosed, not silently applied)**: requirements `RS-004` and A11 describe
the digest's input as "`.specify/state/` 下的状态脊与逐条状态文件". Measured, the line registry — the authoritative
per-line state — is at `$REGISTRY` **outside** the repository, while `.specify/state/` holds the *spine documents*
one of which carries the fenced loop-state block. Both are read-only inputs and neither is a new store, so the FR
(`FR-011`: "read state artifacts") is satisfiable as written; the plan records the real resolution order and does
**not** treat `.specify/state/` as the registry. This is a factual correction of an inherited premise, recorded here
per the fast-fail disclosure duty rather than repaired inside `requirements.md` (the plan stage must not edit the
upstream spec).

## RO-07 — The runner's four-piece evidence gives per-line liveness without a second detector

`skills/external/sdd-loop-driver/scripts/run-stage.sh` writes "the four-piece evidence (PID + start token, atomic
status, log, heartbeat) and projects runner_pid/cli_pid into the Line Registry". `watch-target.sh`'s header states
its signal discipline: "completion = exact sentinel last line (necessary) or exit record rc=0; liveness = pid file +
kill -0 …; progress = log tail; heartbeat proves the runner shell is alive. **Absence … is never completion.**"

**Consequence**: the digest's "age of last observed activity" has a real source (the status file's mtime and the
heartbeat's mtime, both of which the registry entry points at), and the "absence is not completion" rule the
requirements state for the reporter is the *same* rule the watcher already implements — so the owner references it
rather than restating it.

## RO-08 — The stall threshold numbers already have one owner, and it is a table

`skills/internal/create-team/references/patterns.md` § Parallel Dispatch → **Monitoring → Stall Detection** is a
3-row table: "No manifest created | 60s after dispatch | Alert Lead", "Manifest stuck at `in-progress` | 120s with
no file changes | Flag as stalled", "Empty output | Manifest exists but deliverables empty | Flag as incomplete".
`grep` over `shared/`, `templates/`, `skills/` finds no second numeric table for the same purpose.

**Consequence**: FR-009's "declared stall threshold, not a per-run guess" is satisfiable by **referencing this
table**, and the owner document must cite it by path and section rather than copy the numbers. Premise EP-005.

## RO-09 — The coaching skill's dispatch payload is a genuine closed set with a contract test

`skills/external/coaching-skills/SKILL.md` § Dispatch Payload (lines 150–184) opens with "The payload is a closed
field set; anything not listed below is forbidden", lists **7** fields (`trainee`, `workdir`, `work`, `instruction`,
`return-contract`, `anomaly-line`, `fast-fail-clause`, `confirmation-relay` — 8 rows, 7 of which the test pins plus
`workdir`), then lists four forbidden content classes, the single-dispatch cardinality, the return handling and the
transport record.

`tests/contract/test_coaching_dispatch_contract.py` pins `REQUIRED_FIELDS = ("trainee", "work", "instruction",
"return-contract", "anomaly-line", "fast-fail-clause", "confirmation-relay")` and runs a payload validator over one
compliant payload plus four counterexamples.

**Consequence**: FR-019's amendment is exactly one field plus one forbidden-content clause plus one return-handling
clause, and the same change must add the field to that test's tuple — otherwise the test goes red for the wrong
reason (it would report a missing field the skill legitimately gained). Premise EP-006. Note the skill dispatches
**exactly one** subagent per run, which requirements § Edge Cases already reads into scope via FR-002's
"keeps one or more asynchronous delegations past their dispatch".

## RO-10 — The team-creation entry is one skill with four pattern sections; the reporter seat must not be pattern-specific

`skills/internal/create-team/SKILL.md` routes all four patterns (parallel / serial / iteration / continuous) through
one create procedure and one schema. The `Summary Refresh` gate order and the `Hard Constraints` block apply to all
four.

**Consequence**: the seat obligation and its guard must be stated **once, pattern-generic**, and the two escape
paths (FR-006's recorded reason, FR-021's runtime omission) must be expressible in the schema. A per-pattern
statement would be four copies of one rule — the drift the one-source principle exists to prevent.

## RO-11 — The 30-second literal has no definition site today; the 15-minute literal has exactly the ones already known

- `grep -rn "30 秒\|30 seconds" shared/ templates/ skills/ agents/` → **2 hits, both unrelated prose**:
  `skills/external/draw-diagram/references/types/plantuml/references/howto/19-salt-diagram.md:12` and
  `skills/external/improve-skills/references/skill-slimming-principles.md:73`. Neither is a reporting interval.
- `grep -rn "15 分钟\|15 minutes" --include=*.md shared/ templates/ .specify/instructions.md` → 3 hits:
  `shared/guidelines/progress-reporting.md:23`, `:24` (the selection rationale) and
  `templates/instructions-template.md:128` + its mirror `.specify/instructions.md:140` (the ambient reachability
  reminder the pinned test already sanctions).

**Consequence**: designating the new owner as the single definition site of the long-run default creates **no
duplicate** (EP-008), and SC-006's literal scan has a precise, measured baseline: today the pattern matches 0
framework-source *interval* definitions, so the post-change assertion is "exactly 1 definition site + the two
unrelated prose hits which the guard whitelists by path". Writing the scan as "0 hits anywhere" would be a claim
the tree already falsifies.

## RO-12 — Adding one command template fans out through an existing generator to the tool directories that exist

`src/specify_cli/__init__.py:796` `_ASSISTANT_COMMAND_DIRS` configures 6 tools (`copilot`, `claude`, `hermes`,
`opencode`, `qoder`, `codex`). `scripts/python/regen-command-copies.py::_tool_dirs()` writes **only** the tool
directories that exist in this repo; on 2026-11-06 those are `.claude/commands`, `.github/prompts`,
`.opencode/command`, `.qoder/commands` (no `.hermes/`, no `.codex/`). `--check` exits 0 today.

**Consequence**: EP-007 holds and `plan.md` § Mirror Obligations names the 4 real copy paths rather than 6
configured ones — naming 6 would be a file-count claim the tree contradicts.

## RO-13 — Two existing validators already implement the digest's exit-code and output conventions

`python3 scripts/python/validate-decision-tensions.py --spec <spec> [--json]` prints per-check `[label] pass|fail (n)`
lines then `N error(s), M warning(s)`; `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py
--spec-dir <dir> --stage <stage> [--json-out <path>]` prints a one-line verdict then a JSON line, and exits 0 on
pass / non-zero on findings or input error. `python3 scripts/python/gate-check.py <paths>` uses `0` / `1` / `2`.

**Consequence**: D10's `0` / `1` / `2` for `--action guard` follows an established three-value convention, so the
new script introduces no new exit-code vocabulary. The digest's `3` for "nothing active" is the only new value and
is declared by the requirements (FR-011, SC-005), not invented here.

## RO-14 — The framework's own tool surface has no current-state reading command today

`ls templates/commands/` → 26 command templates; `ls .qoder/commands/` shows their per-tool copies. None of the 26
is a "what is running right now" reading (`session` manages session memory records, `review` judges artefacts,
`analyze` judges cross-artefact consistency, `history` distils conversations).

**Consequence**: the digest entry is genuinely new user-facing surface (which is why T-002 is recorded as a
load-bearing tension: it is cross-team, adding a `speckit.*` name to 4 copy trees), and the name must be chosen by
the naming order — `status` describes what the command answers, and it imitates the sibling shape
`speckit.<verb|noun>.md`.

## RO-15 — The confirmation-gate scanner is green at 27 blocking gates, which bounds what the new command may do

`python3 .specify/scripts/python/scan-confirmation-gates.py --summary` →
`blocking confirmation gates: 27 / destructive: 20 / governance_kept: 7 / violations (reversible gates still blocking): 0`.

**Consequence**: the new command and the reporter seat must add **zero** blocking confirmation gates — the digest is
a read-only renderer and the reporter is a read-and-emit role, so neither needs one. A future reviewer can re-run
this scan and expect **the same 27**, which is a passable criterion (an increment is a defect).

## Resolved unknowns (Phase 0 exit)

| # | Unknown carried from the spec | Resolution | Where it lands |
|---|-------------------------------|------------|----------------|
| U-1 | Where does the obligation's owner document live? | `shared/guidelines/reporting-obligations.md` (the `shared/guidelines/<topic>.md` sibling form, and the store requirements A10 already named) | `plan.md` D1 / T-001; contract RO-01 |
| U-2 | What is the reporter Template's path and capability shape? | `agents/reporter.agent.md`, mirror `.specify/agents/templates/reporter.agent.md`; `capability-tools` limited to read + write-own-stream; no dispatch/authorize/retry/terminate tool | `plan.md` D2; contract RS-01…RS-07 |
| U-3 | Where does the seat obligation attach in the roster? | A `members[]` row with `role: reporter`, plus a declared `reporting-reason` key for the two recorded-reason escape paths | `plan.md` D3; contract RS-02, RS-05 |
| U-4 | What is the digest's command + script name and exit-status set? | `/speckit.status` (`templates/commands/status.md`) + `scripts/python/status-digest.py`; statuses `0` rendered / `3` nothing active / `2` input error (guard action: `0`/`1`/`2`) | `plan.md` D8, D10; contract DG-01, DG-05 |
| U-5 | What are the coaching payload's exact added field and clauses? | exactly one field `reporting-cadence`, one forbidden-content class, one return-handling clause, plus the test tuple update | `plan.md` D5; contract MV-06…MV-08 |

## Unknowns that remain, with why they are not blocking

| # | Unknown | Why the plan can proceed |
|---|---------|--------------------------|
| R-1 | Whether a real multi-minute team run can be staged inside this unattended run for SC-001's live evidence | SC-001 states its own path as `final`; the plan provides the fixture shape in `quickstart.md` scenario C and `contracts/status-report.contract.md`, so `/speckit.implement` can measure it. Whether a given host console captures the line is an execution-time fact, not a design fact |
| R-2 | Which concrete host will serve SC-009's dogfood run | `requirements.md` RS-003 declares "at least one supported host" and records host + version into `test-evidence`; the plan does not pin a host, so no plan fact depends on the answer |
| R-3 | The digest's exact default entry cap value | The cap is a declared default **inside the script** and overridable per invocation (D9). The value is chosen at implementation time and measured by the guard; no other artifact restates it, so choosing it later creates no drift |
