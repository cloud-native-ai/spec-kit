# /speckit.team

The single entry point for **all team operations** — create, modify, run, and view agent teams. `/speckit.team` is the multi-agent analogue of `/speckit.agents`: it recognizes your intent and routes it to the owning team skill. Single-agent authoring lives in `/speckit.agents`; team operations live here.

## When to Use

- When you want to **create** a team — organize several agents into a collaborative structure (parallel / serial / iteration / continuous)
- When you want to **run** an existing team (the preview is disclosure, then execution)
- When you want to **modify or optimize** an existing team (add/remove members, tune thresholds, repartition territories)
- When you want a **read-only view** of one team's structure and status (six information groups), or an overview of every team

## Conceptual Model

A **team** has two structures (defined once in `skills/internal/create-team/references/conceptual-model.md`):

- **Static structure** — a **Role × Stage × Type** roster (who participates, in what role, at what stage, Worker or Meta).
- **Dynamic structure** — the collaboration **pattern** (parallel / serial / iteration / continuous) with its parallelism / DAG / iteration / operating settings and an execution flow. Each pattern encodes a priority: **parallel** = 效率优先 (throughput), **serial** = 质量优先 (quality, verified handoffs), **iteration** = 目标收敛 (converge then stop), **continuous** = 长期运营 (operate on a cadence).

An `iteration`/`continuous` team MUST include **exactly one** Team Supervisor (Meta role); a `parallel`/`serial` team MAY use one as the Lead / quality gate.

Persistent teams own a directory `.specify/teams/<slug>/` — the definition lives at `.specify/teams/<slug>/team.md` (Markdown + YAML frontmatter, no per-tool symlink) and per-run reports accumulate under `.specify/teams/<slug>/runs/`. A **continuous** team additionally owns tracked operating-spine files — `constraints.md`, `STATE.md`, `run-log.jsonl` (see [`docs/teams/continuous-operations.md`](../teams/continuous-operations.md)).

## Syntax

```text
/speckit.team                      # infer intent from context
/speckit.team view [team-slug]     # read-only view: no slug = overview, slug = six groups
/speckit.team [intent]             # natural-language intent → routed to the matching mode/skill
```

## Modes → Intent Routing

`/speckit.team` exposes **four modes**:

| Mode | Recognized intent | Skill |
|------|-------------------|-------|
| **create** | "组织一个团队", "创建团队", "build a team" | `create-team` |
| **modify** | "调整团队", "优化 team", "improve/adjust team" | `improve-team` |
| **run** | "运行团队", "执行团队", "run/execute team" | `run-team` |
| **view** | "查看团队", "展示团队", "团队状态", "概览", "overview", "status", "show" | `view-team` |

The command **delegates to skills** and never renders templates inline. On ambiguous or unsupported intent it reports the four recognized capabilities (create / modify / run / view) and requests the missing intent — it never guesses silently, and it executes no mode until the intent resolves. A `modify`/`run`/`view` targeting a team that does not exist reports **"team not found"** and offers to `create` it.

### Anchor-based creation (create with an archived anchor)

When the input names an anchor that is already archived under `.specify/anchoring/<slug>/` (exact slug match, confirmed with you), create runs the **anchor-based branch** instead of re-eliciting the anchor as free text:

1. **Load & restate** — the definition (objective, criteria, lifecycle, existing Targets) is loaded via the `goal-utils.py` engine and restated for your confirmation. A dangling name stops with the verbatim error prefix `goal 未定义:` and points to `/speckit.anchor create`; a terminal anchor (`achieved`/`abandoned`) is refused outright.
2. **Four-element analysis** — dimension, criteria coverage (missing criteria declared, never invented), existing Targets, and single-team achievability, each with rationale. The conclusion is advisory: you adjudicate single-team vs decomposition.
3. **Decomposition proposal (optional)** — on the decomposition path, a proposal set is drafted (outcome-form statements, no criteria restatement), each statement dry-run validated by `goal-utils.py targets <slug> --check` (zero writes) before presentation; one merged confirmation lands them per-statement via the existing `targets --add` authorization surface. The team side never writes `anchor.md`.
4. **One team per Target (N teams : 1 Anchor)** — each open Target gets a team: all declare the same `anchor_slug`, each carries `focus_target: T-<nnn>` (its default focus), slugs derive as `<anchor-slug>-t<nnn>` with uniqueness checks, and a pairwise-disjoint territory proposal is verified by `skills/internal/create-team/scripts/verify-territory-disjoint.py` before landing — known overlaps are disclosed and handed to `/speckit.anchor coordinate`, never landed silently.

Concepts (Anchor / Target / binding) are defined once in `.specify/shared/definitions/anchor-definitions.md`; decomposition is owned by `skills/internal/create-team/references/conceptual-model.md`.

## Run Mode: preview → execute (disclosure, not a gate)

The **run** mode delegates to the `run-team` skill. It loads the team, renders both structures, and then executes directly — the preview is disclosure, not a blocking gate (`shared/guidelines/confirmation-gates.md`); **continuous** loops are the exception and keep their tiered gates.

1. **Load** the team from `.specify/teams/<slug>/team.md`.
2. **Render Static Structure** — the Role × Stage × Type roster matrix.
3. **Render Dynamic Structure** — the pattern, its parallelism/DAG/loop settings, and an execution flow diagram.
4. **Disclose, then execute** — the preview discloses the resolved anchor, both structures, the Target assignment and the summary decision, and orchestration then runs directly (territory validation for parallel, DAG no-cycle + per-handoff verification for serial, max-iteration cap for iteration, and — for **continuous** — read `constraints.md` + budget + kill-switch and run exactly **one cycle** at the declared maturity level with an independent verifier at L2+; file-path-only handoff throughout).
5. **Report** — after execution, a dated report is written to `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md` (anchor, timing, result summary, process detail). Run intermediates stay in the git-ignored `.specify/teams/.work/<slug>/`; deliverables go only to their declared target paths.

### Target-focused runs (`--target`)

```text
/speckit.team run <team-slug> --target T-001
```

A run MAY focus on one authorized **Target** (scope slice) of the bound anchor — see [`/speckit.anchor`](anchor.md) → Targets for the authorization side. The parameter is validated in preview, before execution: dangling references stop with a pointer to `/speckit.anchor targets --add`; cross-anchor references and terminal anchors are refused; a **terminal-state Target** (`done`/`dropped`) stops for the **review bifurcation** — verify by hand: if it is genuinely done, the run ends with a report; if the evidence contradicts, reopen it via `/speckit.anchor targets <slug> --set open --id <T-nnn>` and re-issue the run. There is no terminal-execution bypass. The preview discloses `本次 Target: T-<nnn> — <statement>(open)` (or `本次 Target: 无(对 anchor 整体运行)` when omitted), the report carries `**Target 指派**: …`, and new ledger entries carry `target_ref`. The assignment never rebinds the team, never changes identity resolution, and never moves the summary delivery directory; without `--target` the whole flow is byte-equivalent to the pre-038 behavior. **All five preview checks are available as one machine-readable, zero-write call** — `python3 scripts/python/goal-utils.py run-checks <team-slug> [--target <T-<nnn>>] --json` — whose exit code IS the verdict (`0` pass / `2` bad argument / `3` no such team / `4` definition unusable / `5` blocked), with a per-check `not-evaluated` value for any check whose precondition did not hold. The five checks, their judgment order and the meaning of each verdict are owned by the `/speckit.team` command reference and the engine; this page names the call rather than restating a second criterion.

**Default focus (`focus_target`, 042).** A team created through the anchor-based branch may declare `focus_target: T-<nnn>` in its frontmatter — the team's default focus Target. Resolution order is **explicit `--target` > `focus_target` > none**: a run without `--target` resolves to the declared Target and discloses the source with the `(团队默认)` marker (`本次 Target: T-003 — <statement>(open)(团队默认)`); an explicit `--target` always overrides; teams without the field behave exactly as before (byte-equivalent). `focus_target` is a prefill of `--target` — not a write-scope claim and not a binding change; the five preview checks apply unchanged to the resolved value (a terminal default Target is intercepted the same way; re-focus via `improve-team`, reopen via `/speckit.anchor`).

## View Mode

`/speckit.team view [team-slug]` is a **strictly read-only** presentation: it writes no
definition, run report, ledger, summary, anchor, registry or state file, dispatches no seat
and registers no run line. The mode delegates to the `view-team` skill, whose deterministic
reader is `scripts/python/team-view.py`; the command renders nothing itself.

- **No slug = overview** — one row per team in the archive, sorted by slug ascending, with
  slug / name / pattern / lifecycle / bound-anchor identity / updated / latest run.
- **One slug = six information groups** — identity & binding, static structure, dynamic
  structure, persistence inventory, recent run state, archive references; every missing
  fact is labelled (`缺失` / `为空` / `不可读` / `未记录`), never filled with a fabricated
  value.
- **Exact slug match only** — a near-miss is never resolved by prefix or fuzzy match. An
  unknown slug reports **"team not found"**, the available slugs (bounded, with an omitted
  count) and a `/speckit.team create` suggestion.
- **Corrupt definition** — a directory that exists but whose `team.md` is missing,
  unreadable or unparseable is reported as `定义损坏` with its exact path; it is never
  reported as "not found".
- **Not a run preview** — the five-check preflight and the `blocked` verdict belong to
  `run-team`. View presents persisted state and binding facts only; a reader who wants the
  run judgement goes to `/speckit.team run`. `--target` carried by view is a
  mode/parameter conflict and is reported, never silently dropped or rerouted.

### Run-report recognition and degradation semantics

- **Recognition is closed and parseable** — a file under `runs/` is a run report when its
  name starts with a valid UTC timestamp in one of exactly five forms (`YYYYMMDDThhmmssZ`,
  `YYYYMMDDThhmmZ`, `YYYY-MM-DDThh:mm:ssZ`, `YYYY-MM-DDThh-mm-ssZ`,
  `YYYY-MM-DDThhmmssZ`) and the remainder matches `(?:-[0-9a-f]{4})?-(?:report|stage)\.md`;
  a stamped file with any other remainder is an **auxiliary artifact**; a file with no
  parseable leading stamp is **unrecognized residue**. The grammar and the fixed
  classification order are owned by
  `.specify/specs/108-team-view-degradation/contracts/report-recognition.contract.md`
  (C-201 / C-202).
- **Latest = the maximum parsed timestamp** — the latest run report is the report with the
  largest parsed UTC instant (name-ascending on ties); the reader never falls back to an
  older report because a file does not match a narrow template. When a readable `runs/`
  directory also holds residue, the latest determination is unprovable: the output shows
  the residue count with bounded examples and the view adds the degradation reason
  `report-recognition-uncertain`.
- **Missing or empty history alone never degrades** — `缺失` / `为空` (and the file-level
  states `不可读` / `未记录`) never change the exit code by themselves.
- **Exit 5 meaning and the closed reason set** — exit `5` means "rendering produced, but a
  required fact group is unreadable or the latest run is undeterminable". The degradation
  reason set is exactly `{engine-degraded, report-recognition-uncertain}`; every active
  reason is named individually in the trailing `降级（degraded）` block. The reason ids and
  the exit mapping are owned by
  `.specify/specs/108-team-view-degradation/contracts/team-view-program.contract.md`
  (C-104) — this page cites the owner and never restates a second definition.
- **Repair pointers are presented, never executed** — an unreadable binding or a `goal`
  key needing normalization renders its named state together with the sanctioned repair
  entries `/speckit.team modify` (definition repair) and the engine write face
  `goal-utils.py bind` / `goal-utils.py migrate`; the view itself writes nothing and
  executes no repair.

## Collaboration Patterns

Four patterns; the anchor decides which fits. The first three are **bounded** (run once and stop); `continuous` is **unbounded** (operates on a cadence). Pick with the decision tree in [`docs/teams/orchestration.md`](../teams/orchestration.md).

- **parallel** (效率优先) — independent Workers dispatched together with disjoint write territories
- **serial** (质量优先) — an ordered DAG chain where each stage's output feeds the next via file-path-only handoff, with a simple verification between each step and its predecessor
- **iteration** (目标收敛) — Workers + exactly one **Team Supervisor** (Meta role) iterate to a quality threshold, then deliver and stop
- **continuous** (长期运营) — runs on a cadence; each cycle reads constraints + budget, acts, independently verifies, scores, critiques, and updates a cross-run state spine (maturity L1→L2→L3; see [`docs/teams/continuous-operations.md`](../teams/continuous-operations.md))

## Output Artifacts

| Artifact | Location | Git |
|----------|----------|-----|
| Team definition | `.specify/teams/<slug>/team.md` | tracked |
| Item ledger (all patterns) | `.specify/teams/<slug>/items.jsonl` | tracked, append-only |
| Continuous operating spine (continuous only) | `.specify/teams/<slug>/{constraints.md,STATE.md,run-log.jsonl}` | tracked |
| Run reports (per execution) | `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md` | tracked |
| **Anchor summary** (per anchor, not per team) | `.specify/anchoring/<slug>/summary/` (`summary.md` + `assets/` + `data/`) | tracked |
| Deliverables (standard output) | declared target path (real project path) | tracked |
| Run intermediates | `.specify/teams/.work/<slug>/` | git-ignored |

## Anchor Summary

A team's execution flow periodically produces an **anchor-level summary** — the team treated
as a project — by driving the `summarize-project` skill. Output is **dual-indexed**:

| Index | Path | Answers |
|-------|------|---------|
| **team** | `.specify/teams/<team-slug>/` | how is this team running |
| **anchor** | `.specify/anchoring/<anchor-slug>/summary/` | how far has this anchor progressed |

The anchor directory holds the single complete summary and aggregates **every** team that
declares the same `anchor_slug`, so an anchor outlives any individual team's rebuild or rename.
The team directory keeps run information only.

### Trigger boundaries

| Pattern | Boundary |
|---------|----------|
| `continuous` | end of every Nth cycle (phase 9 SUMMARIZE, after REPORT) |
| `iteration` | after each generation's DECIDE phase |
| `serial` | after each stage handoff verification passes |
| `parallel` | after cross-verification and result aggregation |
| all | terminal summary on anchor met / converged / halt / manual stop |

Gates are evaluated in a fixed order — **budget → cadence → material** — and every run
records the outcome in its report:

```text
Summary: produced | skipped(cadence) | skipped(budget) | declined(no-material)
```

That line is mandatory: it is what makes "not observed" distinguishable from "observed,
no progress". The run-mode preview discloses the summary decision, the resolved anchor
identity, and the target directory before execution, so the cost is known up front.

### Configuration

```yaml
anchor_slug: my-anchor     # frontmatter — the ANCHOR's identity; distinct from `slug`
config:
  summary:
    enabled: true         # omit the whole block and the summary is still enabled
    every: 5              # per N boundaries; continuous defaults to 5, bounded patterns 1
    interactive: false
```

`anchor_slug` is optional: a team that omits it falls back to its own slug as an *inferred*
anchor identity, so pre-existing teams need no migration. Editing the anchor prose never moves
the delivery directory, because identity is declared rather than derived. Concurrent
refreshes of one anchor serialize into a single atomic write.

Details: `skills/internal/create-team/references/summary-mapping.md`.

## Companion Skills

- `create-team` — define a team (static + dynamic structure), persist it, and execute it (parallel / serial / iteration / continuous)
- `improve-team` — apply targeted, evidence-based, structure-preserving edits to an existing team
- `run-team` — run an existing team: five-check preview, structure render, present & execute, run report
- `view-team` — read-only view: six information groups for one team, or an overview of every team

## Prerequisites

- `specify init` (project initialized); `.specify/agents/{templates,instances}/` populated with the agents that become team members

## Next Steps

- Run [`/speckit.instructions`](instructions.md) to refresh discovery metadata
