# Continuous Operations — the Long-Lived Team Form

The **continuous** pattern is a team that runs forever on a cadence instead of converging once
and stopping. It exists for work that **arrives continuously** (CI failures, new PRs/issues,
dependency updates) or for a **quality that must be kept up long-term**.

Because a continuous team can run **unattended and repeatedly**, it carries a full operating
discipline — the essence of *Loop Engineering* applied to the team domain: start in a
report-only mode, earn trust with evidence, and only then grant automation.

> **This is the doc-level companion.** The normative single source of truth is
> [`operating-loops.md`](../../skills/create-team/references/operating-loops.md); when the two
> disagree, that reference wins. For how continuous relates to the other three patterns, see
> [orchestration.md](./orchestration.md); for the concept model see
> [`conceptual-model.md`](../../skills/create-team/references/conceptual-model.md).

---

## iteration vs continuous — which one?

| | **iteration** (converge) | **continuous** (operate) |
|---|---|---|
| Goal semantics | one-time: raise X from A to B, **stop when met** | ongoing: **maintain / keep improving** a quality, or process **an unending stream** of work |
| Lifecycle | bounded: ends at `threshold` / `max_iterations` | unbounded: runs on a **cadence**; each run is one bounded cycle |
| Stop condition | met / cap / consecutive regression | **this run** is bounded by budget/circuit-breaker/kill-switch; **the whole team** is retired by a human |
| Risk surface | single, reversible | repeated, possibly unattended → **must have guardrails** |

**Decision**: if the goal says "持续 / 不断 / 长期维持 / 每天 / keep running / keep improving", or
the work **arrives continuously** → `continuous`. Otherwise → `iteration`.

> **Core creed (from Loop Engineering): do not skip the report stage.** The value of an operating
> loop is not that it edits things automatically from day one — it is that it first calibrates its
> judgment at low risk, then earns automation level by level.

---

## Maturity Levels: L1 → L2 → L3 (no skipping)

Every continuous team runs at a **maturity level**, recorded in `config.maturity`. It **must start
at L1** and graduate only after meeting the gate for the next level.

| Level | Meaning | Allowed actions | Required guardrails |
|-------|---------|-----------------|---------------------|
| **L1 — report** | Discover + triage + score + write state, **change no deliverable** | read, evaluate, write `STATE.md` and run report | state spine + budget |
| **L2 — assist** | Make a **minimal, well-scoped** change per item, **independently verified**, produce a draft for human review | L1 + minimal change (≤ `max_attempts` per item) + independent verification | L1 + constraints file + independent verifier + worktree/workspace isolation + attempt cap |
| **L3 — unattended** | May run unattended, stopping only at boundary violations | L2 + auto-land within the allowed scope | L2 + full blacklist + explicit **human handoff points** + kill-switch + validated metrics |

### Graduation Gate (L1→L2 example; L2→L3 is the same, stricter)

Only `improve-team` may change `config.maturity`, and only with evidence:

1. Ran at L1 for **≥ 2 cadence cycles**, with a High-Priority **false-positive rate < 20%**
   (read from the cumulative Post-Run Critique in `STATE.md`).
2. Independent verifier + workspace isolation have been proven on **human-triggered** changes.
3. The constraints file (path blacklist, build/test commands, attempt cap) is fully written.
4. No unresolved boundary/budget incidents.

> **Cautionary tale (`why-we-killed-ci-sweeper`)**: jumping straight to auto-fix, running the
> verifier in the same session as the implementer, having no branch allowlist, and having no
> budget → 8M tokens burned in 48h, and 1 of 11 PRs broke a production config. Those four failures
> are exactly what the L1 gate + independent verifier + constraints file + budget circuit-breaker
> are built to prevent.

---

## Cadence

`config.cadence` declares the repeat rhythm — e.g. `1d` (daily), `2h` (denser during active
periods), or `cron: 0 8 * * 1-5` (weekday mornings only). High-frequency cadences (PR/CI-style,
`5–15m`) **must** early-exit in sub-seconds when there is no actionable work.

A continuous team's single `run` executes **one cycle**; repetition is driven externally
(a human `/speckit.team run`, cron, or CI).

---

## The Operating Guardrails

### Constraints file (read at the start of every cycle, binding)

A continuous team keeps a **binding** constraints file at `.specify/teams/<slug>/constraints.md`,
which the Team Supervisor reads and enforces at the **very start** of each cycle. It covers at least:

- **Path blacklist** — never touch `.env`/`.env.*`, `auth/`, `payments/`, `secrets/`,
  `credentials/`, or the project's declared core/infrastructure files.
- **Push / merge gate** — never auto-merge to trunk without human approval; open a draft PR first.
- **Attempt cap** — at most **3** fix attempts per item, then escalate to a human (mechanical:
  record each attempt in a workspace ledger and check the count before retrying).
- **Change discipline** — fix **one** problem per cycle; never opportunistically refactor
  unrelated code; never disable a test to make a gate go green.
- **Communication** — state what will be done before acting; never silently close an issue/PR.

### Budget + circuit-breaker + kill-switch

`config.budget` declares per-day / per-cycle caps. The Supervisor checks it at **both** the start
and end of a cycle:

```yaml
budget:
  max_cycles_per_day: <n>
  max_tokens_per_day: <n>
  max_subagents_per_cycle: <n>
  on_80pct: report-only     # ≥80% of daily budget → this cycle drops to report-only
  on_100pct: halt           # ≥100% or kill-switch → exit now, one line into STATE.md
kill_switch: <flag/label>   # e.g. loop-pause-all
```

- **No actionable work** → early-exit at minimal cost (no sub-agents), logging `no-op`.
- **≥ 80%** of daily budget → switch to **report-only** (temporarily equivalent to L1).
- **≥ 100%** or kill-switch active → **exit immediately**, leaving one line in `STATE.md`.
- Never exceed `max_subagents_per_cycle`.

### Independent verifier (Maker/Checker, mandatory at L2+)

This is `iteration`'s evaluator, hardened per Loop Engineering. At L2 and above, any deliverable
change must pass an **independent verifier**:

- **Independent** — a **separate sub-agent**, never the same session/instance as the implementer (`executor`).
- **Default REJECT** — the stance is "reject unless the evidence is sufficient".
- **Actually runs the checks** — runs the tests/gates itself; does **not** trust the implementer's
  "tests pass" claim; reports the command + result snippet.
- **Three verdicts** — `APPROVE | REJECT | ESCALATE_HUMAN` (can't run tests / medium-high risk → escalate).
- **Scope check** — only relevant files changed, no blacklisted paths, no unrelated edits, no
  cheating (disabled tests / commented-out assertions).

Mapping: `executor` (Worker) proposes a change → `evaluator` (Meta, independent verifier) rules →
`optimizer` (Meta) gives direction only if the loop continues. The implementer **may not** self-certify as done.

### State spine (cross-run memory)

A continuous team maintains **cross-cycle persistent memory** at `.specify/teams/<slug>/STATE.md`
(distinct from the one-per-run `runs/<ts>-report.md`). Every cycle updates it and **prunes**
resolved items:

```markdown
# Team State — <slug>
Last cycle: <ISO-8601>   Maturity: L1|L2|L3   Cadence: <...>

## High Priority (being handled or awaiting a human)
- [ ] <one-line description> — action/status; attempt count n/max

## Watch List (monitored, no action yet)
- <one-line description>

## Recent Noise (looked at this cycle, judged not worth acting on)
- <one-line description>

## Post-Run Critique (appended each cycle; the graduation evidence)
- <cycle time>: false-positives=<n>; noisy items; one improvement for next time
```

### Post-Run Critique + run-log

- **End of every cycle** — append a Post-Run Critique line to `STATE.md` (false positives,
  duplicate items, downgraded/dropped items, one improvement for next time). This is the evidence
  source for the graduation gate.
- **Run-log** — append one structured line to `.specify/teams/<slug>/run-log.jsonl` for
  observability and budget accounting:

```json
{"cycle":"<ISO8601>","maturity":"L1","items_found":<n>,"actions_taken":<n>,"escalations":<n>,"tokens_estimate":<n>,"outcome":"no-op|report-only|fix-proposed|escalated|halted"}
```

- The **full run report** still follows the create-team Report contract at
  `runs/<UTC-timestamp>-report.md` (one per cycle).

---

## Directory Layout (continuous extension)

`iteration`/`parallel`/`serial` teams hold only `team.md` + `runs/`. A **continuous** team
additionally owns these tracked operating-spine files (durable, not run intermediates):

```
.specify/teams/<slug>/
├── team.md            # definition (includes continuous config)
├── constraints.md     # binding constraints (read every cycle)
├── STATE.md           # cross-run state spine
├── run-log.jsonl      # structured run log (append-only)
└── runs/              # one full report per cycle
```

Run intermediates still go to the git-ignored `.specify/teams/.work/<slug>/`.

---

## Config Skeleton (written into `team.md` frontmatter)

```yaml
pattern: continuous
config:
  maturity: L1                     # must start at L1
  cadence: 1d
  verifier: independent            # mandatory at L2+
  max_attempts_per_item: 3
  quality_dimensions: [...]        # Σ weights = 1.0
  threshold: 0.8                   # per-cycle deliver/accept threshold (L2+)
  budget: { max_cycles_per_day: 1, max_tokens_per_day: 100000, max_subagents_per_cycle: 0, on_80pct: report-only, on_100pct: halt }
  kill_switch: loop-pause-all
  constraints_file: .specify/teams/<slug>/constraints.md
  state_spine: .specify/teams/<slug>/STATE.md
  run_log: .specify/teams/<slug>/run-log.jsonl
```

> At L1, `max_subagents_per_cycle: 0` (report-only, no workers dispatched). When graduating to L2,
> `improve-team` raises it and fills in `constraints.md` and the independent verifier.

---

## Per-Cycle Execution Flow (the Supervisor follows this on `run`)

```
1. READ     read constraints.md + budget + kill-switch; kill-switch or ≥100% → exit now
2. BUDGET   sum today's spend; ≥80% daily cap → drop this cycle to report-only
3. TRIAGE   discover & prioritize source work (CI/PR/issue/quality gap); nothing actionable → early-exit (no-op)
4. ACT      L1: write STATE only; L2+: minimal change per item (≤ max_attempts_per_item)
5. VERIFY   L2+: independent verifier (separate sub-agent, default REJECT, actually runs tests)
6. SCORE    score against quality_dimensions (measured against the goal)
7. CRITIQUE append a Post-Run Critique line to STATE.md; append one line to run-log.jsonl
8. REPORT   write runs/<UTC-timestamp>-report.md; update STATE.md Last cycle + prune resolved items
```

---

## Failure Modes (first-class citizens)

| Failure | Mitigation |
|---------|-----------|
| Jumping straight to L2/L3 auto-fix | Force L1 start + graduation gate |
| Verifier in the same session as implementer → rubber-stamping | Independent sub-agent + default REJECT + actually runs tests |
| No budget → runaway token burn | Budget + circuit-breaker + kill-switch |
| Triage generates noise | Add a Noise section to STATE; tighten rules; use false-positive rate as the graduation criterion |
| State file grows without bound | Prune resolved/closed items every cycle |
| Unrelated refactor / disabling tests to pass a gate | Constraints file: "one change per cycle, never disable tests" |
| Repeatedly re-processing the same flaky item | `max_attempts_per_item` + escalate to a human when exceeded |

---

## Related Documents & Traceability

- The four patterns and how to choose among them: [orchestration.md](./orchestration.md)
- Team concept, directory layout, authoritative-source index: [overview.md](./overview.md)
- **Normative single source of truth**: [`operating-loops.md`](../../skills/create-team/references/operating-loops.md)
- One-time vs continuous optimization goals: [`optimization-goals.md`](../../skills/create-team/references/optimization-goals.md)
- Graduating a team's maturity (the `improve-team` edit): [`goal-editing.md`](../../skills/improve-team/references/goal-editing.md)
