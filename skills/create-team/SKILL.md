---
name: create-team
description: Create and run an agent team — organize multiple agents into a collaborative structure (parallel dispatch, serial chain, or self-iterating team loop), persist it as a reusable team, and execute it behind a preview→confirm gate. Use when the user mentions ["创建团队", "组织一个团队", "组建团队", "运行团队", "执行团队", "编排", "并行", "串行", "团队", "闭环", "new team", "build a team", "run team", "pipeline", "parallel", "chain", "team loop", "多agent协作", "agent协同"]
skill_id: "<SKILL:.specify/skills/create-team/SKILL.md>"
---

# create-team

## Goal

Create and run an **agent team**: organize multiple Agents into a **collaborative structure** (static roster + dynamic execution pattern — parallel dispatch, serial chain, or self-iterating team loop), persist it as a reusable `.specify/teams/<slug>.team.md`, and **execute** it behind a preview→confirm gate. This skill owns both **defining** a team and **running** it, and is the single source of truth for the multi-agent Conceptual Model (see `references/conceptual-model.md`).

## Conceptual Model

The multi-agent Conceptual Model (Role × Stage × Type + Team/Loop, the Team Supervisor Meta role, and the static/dynamic structure split) is defined once, authoritatively, in `references/conceptual-model.md`. Read it before defining or running a team; do not re-define it elsewhere.

## Team Definition & Persistence (create mode)

Produce a team from a user goal and (unless one-shot) persist it as `.specify/teams/<slug>.team.md`.

1. **Select the pattern** via the Pattern Selection decision tree below (independent → parallel; sequenced → serial; iterative-quality → team-loop).
2. **Build the roster (static structure)** — a Role × Stage × Type matrix. If the user did not supply members, **propose** them from the goal: prefer existing agents under `.specify/agents/`, otherwise temporary stage/worker templates from `templates/`. A **team-loop team MUST include exactly one Team Supervisor** (Meta role).
3. **Build the pattern config (dynamic structure)** — parallelism + territories (parallel), DAG `blockedBy` edges + file-path-only handoff (serial), or quality dimensions + threshold + max_iterations + regression_limit (team-loop).
4. **Confirm** the proposed roster + pattern with the user, then persist the `Team` to `.specify/teams/<slug>.team.md` using the schema below (skip persistence only for an explicit one-shot run).

### Persisted `.team.md` schema

Stored at `.specify/teams/<slug>.team.md` (no per-tool symlink — framework-internal):

```markdown
---
name: <display name>
slug: <kebab-slug>
description: <goal / purpose>
pattern: parallel | serial | team-loop
created: YYYY-MM-DD
updated: YYYY-MM-DD
members:
  - agent: <slug-or-template-id>
    role: <role>
    lifecycle: persistent | temporary
    # territory: [...]        # parallel
    # blockedBy: [...]        # serial
config:
  # pattern-specific block (parallelism / DAG / loop settings)
---

## Static Structure
<Role × Stage × Type matrix table for this team's roster>

## Dynamic Structure
<pattern description, parallelism/DAG/loop settings, and the execution flow diagram>
```

- `slug` MUST be unique within `.specify/teams/`; it also names the file.
- `members` MUST resolve to `.specify/agents/<slug>.agent.md` or a temporary stage/worker template; unresolved members are surfaced as broken references.
- `config` MUST match `pattern`.

## Execution (run mode)

`/speckit.team run <slug>` loads a persisted team and executes it behind the mandatory **preview → confirm → execute** gate:

1. **Load** the team from `.specify/teams/<slug>.team.md`.
2. **Render Static Structure** — the roster as a Role × Stage × Type matrix (agent, role, Worker/Meta, persistent/temporary).
3. **Render Dynamic Structure** — the `pattern`, its parallelism/DAG/loop settings, and an execution flow diagram (textual/mermaid/PlantUML showing dispatch/handoff/loop edges).
4. **Confirmation gate** — present both structures and require explicit user confirmation. On decline, stop without executing. On confirm, orchestrate per pattern using the engine defined in the pattern sections below, preserving the Hard Constraints (territory validation before parallel dispatch; DAG no-cycle before serial; mandatory max-iteration cap for team loops; file-path-only handoff; context isolation; idempotent execution).

## Pattern Selection (Decision Tree)

Analyze the user's intent and task characteristics to select the right pattern:

```
1. Are sub-tasks independent with no shared mutable state?
   → YES: Parallel Dispatch
   → NO: Continue to Q2

2. Do tasks form a strict sequence (output of A feeds input of B)?
   → YES: Serial Chain
   → NO: Continue to Q3

3. Does the deliverable need iterative quality improvement by a team?
   → YES: Team Loop
   → NO: Consider Serial Chain with parallel stages
```

| Scenario | Pattern | Signals |
|----------|---------|---------|
| Independent tasks, no shared state | Parallel Dispatch | "并行", "同时", "independent", "parallel" |
| Sequential phases with dependencies | Serial Chain | "阶段", "串行", "pipeline", "chain", "依次" |
| Quality-critical, needs iteration | Team Loop | "团队", "闭环", "自迭代", "quality loop" |
| Mix of independent + dependent | Serial Chain with parallel stages | "先…再分别…" |

---

## § Parallel Dispatch Pattern

Dispatch **multiple independent agents** in parallel to maximize throughput when the task decomposes into non-overlapping sub-tasks.

### When to Use

- Task naturally decomposes into **2+ independent sub-tasks**
- Sub-tasks have **no shared mutable state** (no file overlap)
- Throughput is a priority (wall-clock time reduction)
- Tasks are embarrassingly parallel (separate modules, independent reviews)

### When NOT to Use

- Sub-tasks have **strong sequential dependencies**
- Multiple agents need to **modify the same file**
- Fewer than 2 independent sub-tasks
- Task requires **iterative refinement** on shared artifacts

### Territory Division

Territory division is the **deterministic, conflict-free** assignment of file/directory scopes to each child agent.

**Rules:**

1. **Extract Domains**: Parse task into discrete sub-task domains with clear deliverables.
2. **Map to File Sets**: For each domain, enumerate READ and WRITE file sets.
3. **Zero Write Overlap**: No two agents may have overlapping WRITE sets.
4. **Read Overlap Allowed**: Multiple agents MAY read the same files.
5. **Shared File Prohibition**: Files that multiple agents might WRITE go to a **Forbidden Write List** — only the Lead modifies these after aggregation.

**Territory Manifest:**

```
Territory: agent-<N>
  Task: <one-line brief>
  Write Scope: [files/dirs this agent may create or modify]
  Read Scope: [files/dirs this agent may read]
  Forbidden: [shared files this agent MUST NOT modify]
```

**Validation Checklist:**

- [ ] Every file in any Write Scope appears in exactly ONE agent's Write Scope
- [ ] Forbidden Write List contains all files referenced by 2+ agents' potential writes
- [ ] Each agent has at least one file in its Write Scope
- [ ] No circular dependencies between territories

### Dispatch Protocol

**Key principle**: Issue all sub-agent calls in ONE response block — sequential dispatch defeats the purpose.

Per-Agent Payload:

| Field | Content |
|-------|---------|
| `task_brief` | One-paragraph task with clear deliverable |
| `territory` | Write Scope + Read Scope |
| `forbidden_files` | Files this agent MUST NOT modify |
| `output_convention` | Where to write results and status |
| `model_hint` | Suggested model tier (light / standard / heavy) |

Context Isolation Rules:
- NO conversation history passed to child agents
- NO other agent's task briefs shared
- NO intermediate results from other agents visible
- Child agents receive only their territory manifest

### Monitoring

Monitor each agent's output manifest at `<output_dir>/.parallel-result-<agent-id>.md`.

**Stall Detection:**

| Condition | Threshold | Action |
|-----------|-----------|--------|
| No manifest created | 60s after dispatch | Alert Lead |
| Manifest stuck at `in-progress` | 120s with no file changes | Flag as stalled |
| Empty output | Manifest exists but deliverables empty | Flag as incomplete |

**Recovery Options**: Wait (extend timeout) | Nudge (re-issue) | Terminate (Lead takes over) | Reassign (fresh agent)

### Result Aggregation

1. Collect each agent's completion manifest
2. Verify deliverables exist at declared paths
3. Flag territory violations
4. Detect contradictory outputs → trigger Lead resolution
5. Generate Final Report

**Final Report:**

```markdown
# Parallel Dispatch Report
## Summary
- Agents dispatched: <N>
- Successful: <count> | Partial: <count> | Failed: <count>

## Agent Results
| Agent | Task | Status | Output Paths | Notes |
|-------|------|--------|--------------|-------|

## Conflicts Detected
[list or "None"]

## Aggregated Deliverable
[final merged output description]
```

---

## § Serial Chain Pattern

Orchestrate Agents in a **serial chain** (DAG-based pipeline) where each stage's output feeds into the next stage's input.

### When to Use

- Task has **multiple phases with clear dependencies**
- A **pipeline of specialized roles** must collaborate in sequence
- **Quality gates** between stages ensure standards before proceeding
- Work spans **multiple sessions** and needs persistent progress tracking

### When NOT to Use

- All tasks are **independent** → use Parallel Dispatch
- A single Agent can complete the task alone
- No clear stage boundary exists
- Task is purely **iterative refinement** → use Team Loop

### Workflow Definition

**1. Derive Stages from Intent:**
- Stage sequence: distinct phases
- Agent assignments: which role handles each phase
- Dependency graph: which stages depend on which
- Outputs: what each stage produces

**2. Generate AgentWorkflow JSON:**

```json
{
  "workflow_id": "<kebab-case-id>",
  "name": "<Human-readable name>",
  "stages": [
    {
      "stage_id": "...",
      "agent_kind": "...",
      "task": "...",
      "inputs_from": ["..."],
      "outputs": ["..."],
      "blockedBy": ["..."],
      "quality_gate": "..."
    }
  ],
  "handoff_protocol": "file-path-only",
  "progress_file": ".specify/workflow-progress-<workflow_id>.md"
}
```

**3. Validate DAG (No Cycles):**
- Build adjacency list from `blockedBy` edges
- Detect cycles using topological sort
- If cycle → report path and ask user to resolve

### Stage Execution Protocol

```
For each stage in topological order:
1. CHECK: All blockedBy stages completed? (read progress file)
2. BUILD CONTEXT: Gather upstream output paths from inputs_from
3. INVOKE: Spawn subagent with agent_kind role
4. VALIDATE: Check outputs exist; run quality_gate if defined
5. RECORD: Update progress file
6. UNLOCK: Mark downstream stages as unblocked
```

### Failure Recovery

| Strategy | When to Use | Action |
|----------|-------------|--------|
| **halt** | Critical failure | Stop, report, preserve state |
| **retry** | Transient failure | Re-invoke (max 2 retries) |
| **improve** | Quality gate failed | Invoke improve-agent on output |
| **skip** | Optional stage | Mark skipped, continue pipeline |

### Progress Tracking

Write to `.specify/workflow-progress-<id>.md`:

```markdown
# Workflow Progress: <name>
**Workflow ID**: <id>
**Status**: in-progress | completed | failed | halted

## Stage Progress
| Stage | Agent | Status | Started | Completed | Output Path |
|-------|-------|--------|---------|-----------|-------------|

## Handoff Log
- [timestamp] stage_A → stage_B: Passed `<path>`
```

### Cross-Session Resume

1. Check if progress file exists
2. Parse stage table to determine state
3. Present status summary: "Workflow X is N/M complete. Resume?"
4. Continue from first non-completed stage

---

## § Team Loop Pattern

Orchestrate a **multi-Agent team** forming a self-iterating closed-loop system with two layers: a **Team Supervisor** (strategy + coordination, the single Meta role) and **Workers** (execution). The former Meta-Coordinator is merged into the Team Supervisor.

### When to Use

- Task requires **continuous quality improvement** through iteration
- Complex deliverables need **multiple specialized roles** collaborating
- **Automated quality gate control** is desired
- Task is too large or multi-faceted for a single Agent

### When NOT to Use

- Simple single-direction tasks with no feedback loop
- No clear quality standard or scoring criteria
- A single Agent can complete the task in one pass
- Purely sequential with no iteration → use Serial Chain
- Tasks are independent with no shared goal → use Parallel Dispatch

### Architecture

```
USER / GOAL
     │
     ▼
TEAM SUPERVISOR (Meta role — Strategy + Coordination Layer)
  • Define quality dimensions & thresholds
  • Decompose tasks; select & dispatch Workers
  • Monitor progress, adapt strategy
  • Score team output (multi-dimensional)
  • Decide: accept / improve / halt
     │
     ▼
WORKER AGENTS (Execution Layer)
  • requirements-analyst, ux-analyst, system-designer
  • module-designer, test-engineer
  • qa-engineer, knowledge-manager
```

### Team Initialization

1. **Define Team Goal**: Goal statement, deliverables, quality expectations
2. **Select Workers**: Choose from preset roles or create custom agents
3. **Configure Team Supervisor**: Task decomposition strategy, dispatch pattern, team roster, quality dimensions + weights, threshold (default: 0.8), max iterations (default: 5), regression limit (default: 2)

### Self-Iteration Loop

```
INITIALIZE:
  iteration = 0, best_score = 0, consecutive_regressions = 0

LOOP (iteration in 1..max_iterations):

  PHASE 1 — COORDINATE:
    Team Supervisor decomposes goal, assigns sub-tasks, selects dispatch strategy

  PHASE 2 — EXECUTE:
    Workers execute assigned sub-tasks, write deliverables
    Team Supervisor monitors, handles failures, consolidates results

  PHASE 3 — EVALUATE:
    Team Supervisor scores output on each quality dimension
    Compute weighted_total, record in history

  PHASE 4 — DECIDE:
    IF weighted_total >= threshold → STOP (Success)
    IF iteration >= max_iterations → STOP (Max Reached)
    IF consecutive_regressions >= regression_limit → STOP (Regression)
    IF weighted_total > best_score → update best

  PHASE 5 — IMPROVE (if continuing):
    Team Supervisor generates improvement feedback, adjusts strategy,
    and triggers improve-agent on weak areas
```

### Convergence Detection

| Condition | Check | Action |
|-----------|-------|--------|
| **Quality Met** | weighted_total >= threshold | Accept — deliver best output |
| **Max Iterations** | iteration >= max_iterations | Stop — report best with warning |
| **Diminishing Returns** | consecutive_regressions >= regression_limit | Halt — restore best, warn user |

### Final Report

```markdown
# Team Loop Report
## Outcome
**Status**: Converged | Max Reached | Regression Halted
**Final Score**: [weighted_total] / 1.0
**Total Iterations**: [count]

## Score Breakdown
| Dimension | Weight | Final Score | Trend |
|-----------|--------|-------------|-------|

## Iteration History
| Round | Score | Delta | Strategy | Key Changes |
|-------|-------|-------|----------|-------------|

## Deliverables
[File paths of best-scoring iteration's outputs]

## Lessons Learned
[Summary of effective strategies]
```

---

## Shared Protocols

### File Handshake Protocol

All patterns use **file-path-only** communication:
- Agents write deliverables to designated paths
- Downstream agents receive ONLY file paths (not content)
- Never paste file content between agents — saves 50%+ tokens

### Progress Tracking

- Parallel: manifest files at `<output_dir>/.parallel-result-<agent-id>.md`
- Serial: progress file at `.specify/workflow-progress-<id>.md`
- Team Loop: iteration history embedded in final report

### Model Selection Guidance

| Sub-task Type | Examples | Recommended Tier |
|---------------|----------|-----------------|
| **Deterministic** | Template filling, format conversion | Light (fast, cheap) |
| **Judgment** | Code review, scoring, standard implementation | Standard |
| **Deep Synthesis** | Architecture design, novel algorithms | Heavy (high capability) |

### Hard Constraints

- **Territory validation MUST pass** before parallel dispatch
- **DAG validation (no cycles)** before serial chain starts
- **Max iterations MUST be set** for team loops (default: 5, max: 10)
- **File-path-only handoff** — never paste content between agents
- **Context isolation** — each agent invocation is a fresh subagent
- **Idempotent execution** — stages/iterations can be re-run safely

---

## Agent-Specific Configuration

### Step 1: Identify Executing Agent

| Agent | Detection Signals |
|-------|-------------------|
| **Claude Code** | Tools include `Agent`, `Edit`, `Bash`, `Read`; `.claude/` directory exists |
| **GitHub Copilot** | Running in VS Code Copilot Chat context |
| **Qoder CLI** | `.qoder/` directory exists; `AGENTS.md` instructions loaded |
| **opencode** | `.opencode/` directory exists |
| **Qwen Code** | `QWEN.md` instructions loaded; `.qwen/` directory exists |

### Step 2: Load Agent-Specific Guidance

Check if a guide exists at:

```
${SKILL_HOME}/references/<agent-slug>-guide.md
```

If the guide exists, apply agent-specific tool mappings for orchestration (e.g., Claude Code uses `Agent` tool, Copilot uses `@workspace` delegation).

### Step 3: Capture Execution Feedback

If you encounter an agent-specific obstacle, generate feedback at:

```
.specify/memory/feedback/create-team-<agent-slug>-<YYYY-MM-DDTHH-MM-SS>.md
```

```markdown
# Agent Execution Feedback

**Source**: create-team
**Agent**: <agent-slug>
**Timestamp**: <ISO-8601>
**Outcome**: <success | success-with-workaround | partial-failure | full-failure>

## Obstacle
[Description of the agent-specific issue encountered]

## Workaround Applied
[What was done to work around the issue, if anything]

## Suggested Improvement
[Specific change to the skill or reference document that would prevent this issue]
```

Only generate feedback when a genuine agent-specific obstacle was encountered.

## Feedback

At the end of a substantial run of this skill, perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/skills/sdd-workflow/references/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this run reached a meaningful wrap-up. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against this skill's declared purpose and produce a short review plus ≥1 concrete, skill-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this skill's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id`; if a parent flow already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "skill:create-team" --unit-type skill \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
6. **Consolidated submission prompt.** If the returned `should_prompt` is `true`, surface a single consolidated prompt inviting the user to submit collected feedback to the Spec Kit developers; on confirmation run `--action mark-submitted`. Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.
