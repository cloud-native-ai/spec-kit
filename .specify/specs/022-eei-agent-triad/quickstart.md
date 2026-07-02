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
