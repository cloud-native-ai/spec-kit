# Quickstart: EEI Agent Triad

## What is the EEI Triad?

The Executor-Evaluator-Improver (EEI) triad is a quality optimization pattern for AI agents. Instead of running a task once and accepting the result, the triad iteratively improves output until a quality threshold is met.

```
┌──────────────────────────────────────────────┐
│                Orchestrator                  │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Executor │→│ Evaluator │→│ Improver  │  │
│  │          │  │           │  │          │  │
│  │ Performs  │  │ Scores    │  │ Modifies │  │
│  │ the task │  │ output    │  │ env +    │  │
│  │          │  │ & gives   │  │ executor │  │
│  │          │  │ feedback  │  │ context  │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│       ↑                           │          │
│       └───────────────────────────┘          │
│              (loop until score > threshold)  │
└──────────────────────────────────────────────┘
```

## Scenario 1: Create a Triad for Diagram Drawing

### Step 1: Define the goal

```
Goal: Draw a K8s architecture diagram scoring >90 on correctness (60%) and aesthetics (40%)
```

### Step 2: Set up the triad

The orchestrator creates three independent sub-agents:

**Executor** receives:
- Task: "Draw a K8s infrastructure diagram in PlantUML, render to PNG"
- Environment: skill reference files (howto guides, best practices, style config)
- Output directory: `output/k8s-arch/`

**Evaluator** receives:
- Artifacts: the rendered PNG file path
- Scoring dimensions: `{correctness: 0.6, aesthetics: 0.4}`
- Threshold: 90

**Improver** receives:
- Evaluator feedback: scores + specific suggestions
- Workspace: skill reference files (can edit howto guides, best practices)

### Step 3: Run the loop

```
Round 1: Executor draws → Evaluator scores 49 → Improver updates skill files
Round 2: Executor redraws (reads updated skills) → Evaluator scores 62 → Improver updates
...
Round N: Executor redraws → Evaluator scores 91 → DONE! (> 90 threshold)
```

### Step 4: Review results

The orchestrator presents:
- The best-scoring output (PNG at 91 points)
- Iteration history table showing score progression
- Summary of skill improvements made

## Scenario 2: Apply Triad to Code Review

### Setup

**Executor**: Write code implementing a feature  
**Evaluator**: Review code for correctness (50%), security (30%), style (20%)  
**Improver**: Update coding guidelines and executor instructions based on feedback  

### Expected flow

```
Round 1: Code written → Review finds SQL injection → Guidelines updated with security rules
Round 2: Code rewritten → Review finds style issues → Style guide updated
Round 3: Code refined → Review scores 92 → DONE!
```

## Scenario 3: Apply Triad to Document Writing

### Setup

**Executor**: Write technical documentation  
**Evaluator**: Score on completeness (40%), clarity (30%), accuracy (30%)  
**Improver**: Update writing guidelines and topic context  

## Scenario 4: Generate a Supervisor Role Agent via `/speckit.agents` *(Plan Amendment 2026-07-02)*

This scenario shows the unified flow: `/speckit.agents` delegates to the general-purpose `create-agent` skill to produce a **role agent that supervises its own EEI triad**.

### Flow

```
/speckit.agents "make the system-designer a supervisor that optimizes its architecture output"
      │
      ├─ command gathers project context ({{PROJECT_NAME}}, {{TECH_STACK}}, ...)
      ├─ command builds an AgentAuthoringRequest { kind: supervisor, role_slug: system-designer, ... }
      └─ command CALLS create-agent (Supervisor capability)
              │
              ├─ composes agent-role-system-designer-template.md
              │   + shared "Supervision & EEI Delegation" section (ROLE_SCOPE = system-designer)
              ├─ writes .specify/agents/system-designer.agent.md
              └─ returns AuthoringResult (artifact paths + registry entry)
```

### Result

The generated `system-designer.agent.md`, when invoked on a quality-gated task, acts as an orchestrator: it spawns Executor (drafts the architecture), Evaluator (scores on role-default dimensions), and Improver subagents from the existing `agent-subrole-*` templates and loops until threshold — all scoped to the System Designer's domain.

### Refining it later

```
/speckit.agents  →  improve-agent { target: system-designer, direction: "scores plateau at 70" }
```

`improve-agent` classifies the target, plots the trajectory, and applies a minimal fix to the responsible layer (see `improve-agent` Triad Refinement rules).

## Key Principles

1. **Context isolation**: Each sub-agent gets a fresh context per invocation — no shared memory
2. **Environment persistence**: Improver's file edits persist on disk, so the executor naturally reads the latest version
3. **Structured scoring**: The evaluator always produces per-dimension scores + weighted total + specific suggestions
4. **Convergent improvement**: The improver targets BOTH the environment (reference files) and the executor (prompt/context)
5. **Best-output tracking**: The orchestrator preserves the highest-scoring output across all iterations

## Validation Checklist

After running a triad loop, verify:

- [ ] The final score exceeds the configured threshold
- [ ] The iteration history shows monotonic or near-monotonic improvement
- [ ] No evaluator output references the executor's internal prompt (context isolation)
- [ ] All improver changes are traceable (file diffs logged)
- [ ] The executor re-read updated environment files each iteration (not cached)

## Amendment Validation Checklist (Supervisor + General-Skill Refactor)

Structural validation for the 2026-07-02 amendment (no runtime code — verified by inspecting the templates/skills/command):

**G1 — Role supervisors (T036)**
- [ ] Each of the 6 `templates/agent-role-*-template.md` carries `supervisor: true` (default-on, OQ-1) and a `role-scope:` matching its slug
- [ ] The shared section lives ONLY in `templates/agent-supervision-delegation.md` (not copied into role templates, OQ-2)
- [ ] `templates/agent-triad-orchestration-template.md` exposes a `{{ROLE_SCOPE}}` binding

**G2 — Generalized create-agent (T043)**
- [ ] `skills/create-agent/SKILL.md` Goal reads as general authoring (not "role-based only")
- [ ] A capability matrix covers role · supervisor · triad · custom
- [ ] The Supervisor capability inlines `agent-supervision-delegation.md` and binds `{{ROLE_SCOPE}}`
- [ ] Every `AgentAuthoringRequest` field from `contracts/agent-authoring-contract.md` is consumed

**G3 — Generalized improve-agent (T047)**
- [ ] `skills/improve-agent/SKILL.md` target resolution covers role · sub-role · orchestration · custom `.agent.md`
- [ ] A classify-then-route step precedes the refinement workflows

**G4 — Command delegates (T049)**
- [ ] `templates/commands/agents.md` Mode A builds an `AgentAuthoringRequest` and calls `create-agent`
- [ ] Mode B delegates custom creation to `create-agent` and updates to `improve-agent`
- [ ] No inline template-rendering block remains in either mode (contract R1)
- [ ] Runtime command `.claude/commands/speckit.agents.md` matches `templates/commands/agents.md`
