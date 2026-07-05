# P004 — Task Graph & Parallel Worktree Orchestration

- **Status:** Draft
- **Pillars:** Workflow/Process · Scripts
- **Source projects:** learn-claude-code, intellegix-code-agent-toolkit, claude-code-ts
- **Value:** H · **Effort:** M–H · **Phase:** 2
- **Related:** [[P005]], [[P006]], [[P007]], [[P009]]

## Problem / Gap

spec-kit's unit of execution is `templates/tasks-template.md` — a *flat markdown checklist*
grouped into phases, with `[P]` parallel hints and prose dependency notes ("Dependencies &
Execution Order"). It is excellent for humans and adequate for a single agent working top to
bottom, but it has four structural limits:

1. **Dependencies are prose, not data.** "User Story 2 may integrate with US1" and "Services
   before endpoints" live in narrative sections a machine cannot reliably query. There is no
   way to ask *"which tasks are ready right now?"* without an LLM re-reading and re-reasoning
   over the whole file every time.
2. **No auto-unblock.** Completing `T012` does not mechanically make `T014` (which "depends on
   T012, T013") ready — a human or the agent must re-derive readiness by hand.
3. **State is fragile under compaction.** The checklist is the only record of progress. When
   the host agent compacts or restarts mid-`/speckit.implement`, in-flight status ("who owns
   T014, is it half-done?") is lost. This is the same durability gap [[P007]] addresses for
   context.
4. **`[P]` is a hint with no execution lane.** spec-kit says tasks *can* run in parallel but
   ships no isolation: two parallel agents editing the same working tree collide. The draft
   `subagent-driven-development` skill dispatches fresh subagents per task but keeps them all
   in one working tree, so genuinely parallel writes are unsafe.

The research repos converged on the same answer: promote the checklist to a **file-based task
graph** and bind each concurrent task to an **isolated git worktree lane**.

## Proposal

Introduce an *optional, additive* task-graph layer that sits **beside** `tasks.md`, never
replacing it. `tasks.md` remains the human-authored, human-readable source; a small script
derives a machine-readable graph from it (and syncs status back). Three capabilities:

1. **Task graph** — one JSON object per task under `.specify/specs/<KEY>/.tasks/`, carrying an
   explicit `blockedBy` edge list. A `task_graph.py` script answers `ready` / `blocked` / `done`
   and, on completing a task, **auto-unblocks** its dependents. This is the coordination
   backbone every other capability reads from.
2. **Worktree lanes** — each task that runs concurrently is bound by `id` to a git worktree
   (`git worktree add`). A `worktree-lane.sh` helper allocates, tracks, and tears down lanes
   (`keep` / `remove`), with crash recovery reconstructed from an append-only `events.jsonl`.
3. **Coordinator/worker dispatch + sequential merge** — a coordinator reads the graph, fans
   ready tasks out to worker lanes, then merges completed lanes back **one at a time** behind a
   `pre-merge` rollback tag so a bad merge is trivially revertible.

Everything is plain files any host agent can read; nothing runs a daemon. The coordinator is a
*skill + script convention*, driven by the host's own Agent/Task tooling, consistent with the
guiding principle that spec-kit steers a harness rather than being one.

## Design sketch

### File layout (all under the existing per-feature root)

```
.specify/specs/<KEY>/
  tasks.md                     # unchanged, human source of truth
  .tasks/
    index.json                 # graph metadata + fast ready/blocked cache
    T012.json  T013.json ...   # one file per task
    events.jsonl               # append-only lifecycle log (crash recovery)
```

### Task JSON schema (`.tasks/T014.json`)

```json
{
  "id": "T014",
  "subject": "Implement OrderService in src/services/order.py",
  "story": "US1",
  "phase": "Phase 3: User Story 1",
  "status": "blocked",            // ready | in_progress | blocked | done | deferred
  "parallel": false,              // mirrors the [P] marker
  "blockedBy": ["T012", "T013"],  // DAG edges; [] => root
  "files": ["src/services/order.py"],
  "owner": null,                  // agent/lane id once claimed
  "worktree": null,               // lane path once bound (see below)
  "sigil": "[ ]",                 // mirrors tasks.md task state
  "updated": "2026-07-06T10:00:00Z"
}
```

Status maps 1:1 onto the existing task sigils so the two views never diverge:
`[ ]`→`ready|blocked|in_progress`, `[X]`→`done`, `[~]`→`deferred` (honoring the deferral
discipline already in `templates/tasks-template.md`).

### `scripts/python/task_graph.py` — CLI surface

```
task_graph.py build   <KEY>          # parse tasks.md -> .tasks/*.json (derive blockedBy from
                                     #   "(depends on T012, T013)" spans + phase ordering)
task_graph.py ready   <KEY>          # list tasks whose blockedBy are all done  (JSON)
task_graph.py blocked <KEY>          # list still-blocked tasks + their blockers
task_graph.py claim   <KEY> <TID> <OWNER>   # ready -> in_progress, set owner
task_graph.py done    <KEY> <TID>    # -> done; auto-unblock dependents; flip tasks.md [X]
task_graph.py defer   <KEY> <TID> --reason  # -> deferred; flip tasks.md [~]; append reason
task_graph.py status  <KEY>          # counts + DoD rollup (feeds P006 completion gate)
```

`build` is deterministic parsing, not an LLM step: it reads task rows, extracts `depends on
T0xx` spans and cross-phase ordering (Foundational blocks all stories, etc.), and writes the
graph. `done` is the linchpin — it clears the completed id from every dependent's `blockedBy`,
promoting newly-unblocked tasks to `ready`, then rewrites the matching `tasks.md` checkbox so
the human view stays authoritative.

### Auto-unblock (pseudo-flow)

```
on done(T):
    T.status = "done"; T.sigil = "[X]"; append_event("task_done", T)
    for D in tasks where T in D.blockedBy:
        D.blockedBy.remove(T)
        if D.blockedBy == []: D.status = "ready"; append_event("unblocked", D)
    rewrite index.json cache; patch tasks.md row for T
```

### Worktree lanes — `scripts/bash/worktree-lane.sh`

```
worktree-lane.sh add    <KEY> <TID>   # git worktree add .specify/specs/<KEY>/.wt/<TID> \
                                       #   -b wt/<KEY>/<TID>  ; bind in T<TID>.json.worktree
worktree-lane.sh list   <KEY>          # lanes + bound task + branch (from index.json)
worktree-lane.sh keep   <KEY> <TID>    # detach lane, leave branch for later merge
worktree-lane.sh remove <KEY> <TID>    # git worktree remove + delete branch (teardown)
worktree-lane.sh recover <KEY>         # reconcile .wt/ vs events.jsonl after a crash
```

Lanes live under `.specify/specs/<KEY>/.wt/<TID>/`, respecting the existing per-feature
isolation boundary (do not scatter worktrees at repo root). Each lifecycle step appends to
`events.jsonl` (`lane_add`, `task_claim`, `task_done`, `lane_merge`, `lane_remove`) so
`recover` can rebuild live state purely from disk — no in-memory orchestrator state survives a
restart, and none needs to.

### Coordinator/worker dispatch + sequential merge

A `task-graph-orchestration` skill (draft/skills/) instructs the host:

```
1. task_graph.py build <KEY>
2. loop:
     ready = task_graph.py ready <KEY>
     if not ready and no in_progress: break            # done or blocked
     for T in ready (respect [P]; cap concurrency N):
        if T.parallel: worktree-lane.sh add <KEY> T ; dispatch worker with cwd=lane
        else:          dispatch worker in main tree (serialize write-heavy work)
        task_graph.py claim <KEY> T <worker-id>
3. as each worker returns a completion report (P006 gate must pass first):
        task_graph.py done <KEY> T
        git tag pre-merge/<KEY>/<T>                     # rollback anchor
        git merge --no-ff wt/<KEY>/<T>                  # SEQUENTIAL, one lane at a time
        on conflict/failure: git reset --hard pre-merge/<KEY>/<T> ; reopen T ; log
        worktree-lane.sh remove <KEY> T
```

Two rules borrowed directly from the sources: **read-only work parallelizes; write-heavy work
serializes** (claude-code-ts coordinator), and **merges are sequential behind a rollback tag**
(intellegix `orchestrator-multi`). An *appropriateness gate* refuses lanes for small or tightly
coupled task sets and falls back to the plain single-tree SDD loop — parallelism is opt-in and
justified, never default.

### Relationship to existing artifacts

- Extends, does not replace, `templates/tasks-template.md` — the checklist stays canonical.
- Feeds [[P006]]: `task_graph.py status` is the natural input to the completion gate.
- Feeds [[P005]]: the autonomous loop claims from `ready` instead of being told task numbers.
- The dispatch skill builds on `draft/skills/subagent-driven-development` (per-task fresh
  subagent, two-verdict review) — it adds the graph + lanes, keeping SDD's review gate.

## Source evidence

- **File-based DAG with `blockedBy` + auto-unblock** → `learn-claude-code`
  `agents/s07_task_system.py` (`TaskManager.create/update/_clear_dependency`, lines 47–116),
  `docs/en/s07-task-system.md`; mining report `_research/learn-claude-code.md` idea #1.
- **Worktree-per-task, control-plane/execution-plane binding, `events.jsonl` + crash recovery**
  → `learn-claude-code` `agents/s12_worktree_task_isolation.py` (`EventBus.emit` 82–118,
  `TaskManager.bind_worktree` 183, `index.json`); `_research/learn-claude-code.md` idea #2.
- **Coordinator/worker dispatch, read-parallel/write-serialize, `<task-notification>` results**
  → `claude-code-ts` `src/coordinator/coordinatorMode.ts`, `src/coordinator/workerAgent.ts`;
  `_research/claude-code-ts-agent-core.md` idea #2.
- **Territory splitting, appropriateness gate, sequential `--no-ff` merge behind a
  `pre-merge` rollback tag** → `intellegix` `commands/orchestrator-multi.md` (justification
  matrix 43–53, merge/rollback 674–753), `automated-loop/multi_agent.py`
  (`WorkSplitter.split_for_agents`); `_research/intellegix-loop-orchestration.md` idea #4.
- **Autonomous claim-from-board loop** → `learn-claude-code` `docs/en/s11-autonomous-agents.md`
  (`scan_unclaimed_tasks`); `_research/learn-claude-code.md` idea #4 (deferred to [[P005]]).

## Adoption plan

**Phase A — graph, read-only (draft).** Ship `scripts/python/task_graph.py` with `build`,
`ready`, `blocked`, `status`. Emit `.tasks/*.json` as a *derived cache* on top of an unchanged
`tasks.md`. Prove the graph matches the checklist on the existing specs under
`.specify/specs/` (e.g. `022-eei-agent-triad`). No behavior change to `/speckit.*`.

**Phase B — status sync.** Add `claim`, `done`, `defer` with round-trip to `tasks.md` sigils
and `verification.md` deferral fields. A draft `task-graph-orchestration` skill teaches a host
to run `/speckit.implement` off the graph *as an alternative mode*, selected explicitly.

**Phase C — worktree lanes.** Ship `worktree-lane.sh` + `events.jsonl` + `recover`, reconciled
with the existing three-tier `git-workflow` skill (lanes are short-lived feature branches, not
a fourth tier). Wire the coordinator/worker + sequential-merge flow, gated by the
appropriateness check.

**Promotion.** Only after Phases A–C are exercised on real features and [[P006]]'s completion
gate is in place does `/speckit.tasks` optionally emit the graph alongside `tasks.md`, and
`/speckit.implement` optionally consume it. Until promoted, everything lives in `draft/` and
the main flow is untouched.

## Risks & mitigations

- **Two sources of truth drift (`tasks.md` vs `.tasks/`).** Mitigation: `tasks.md` is
  canonical; the graph is a *derived* view. Every state-changing command patches `tasks.md` in
  the same call; a `task_graph.py verify` diff detects drift and refuses to proceed.
- **`build` mis-parses prose dependencies.** Mitigation: deterministic extraction of explicit
  `depends on T0xx` spans + phase-order rules only; anything ambiguous is emitted as a root
  task with a `needs_review` flag rather than a guessed edge. Encourage authors to keep the
  `(depends on …)` convention already shown in the template.
- **Worktree sprawl / leaked lanes after crashes.** Mitigation: `events.jsonl` + `recover`
  reconstruct and prune; `worktree-lane.sh list` surfaces orphans; lanes are namespaced under
  the feature dir for easy bulk cleanup.
- **Merge conflicts between parallel lanes.** Mitigation: split by the `files` field so lanes
  own disjoint paths; serialize merges behind `pre-merge` tags; on conflict, hard-reset and
  reopen the task rather than hand-resolving mid-run.
- **Over-parallelization on coupled work.** Mitigation: appropriateness gate defaults to the
  single-tree SDD loop unless tasks are provably independent.
- **Scope creep toward a runtime.** Mitigation: scripts + skills + files only; the host owns
  the loop. No daemon, no long-lived process (per `_research` anti-patterns).

## Value / Effort rationale

**Value: H.** The task graph is the substrate the rest of the roadmap reads from — [[P005]]'s
autonomous loop, [[P006]]'s completion gate, and [[P009]]'s workflow engine all become far
simpler once "what's ready?" is a file query instead of an LLM re-read. Worktree lanes unlock
genuinely safe parallel implementation, spec-kit's most-requested execution capability.

**Effort: M–H.** The graph script and status round-trip are moderate, self-contained Python
over an existing, well-structured template (M). Worktree lanes plus crash recovery and the
sequential-merge coordinator add real integration surface with git and the host's dispatch
tooling (H). Phasing (read-only graph → sync → lanes) lets value land early while the
higher-effort orchestration matures in `draft/`.
