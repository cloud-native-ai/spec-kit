# Agent Index

This file tracks all agents in the Spec Kit workspace. Agents are stored as `.agent.md` files in `.specify/agents/`.

## Active Agents

| Name | Description | Path | Status |
|------|-------------|------|--------|
| Requirements Analyst | Analyzes and clarifies requirements, translating business needs into structured specifications. | `.specify/agents/requirements-analyst.agent.md` | Active |
| System Designer | Designs system-level architecture and implementation approaches from requirements. | `.specify/agents/system-designer.agent.md` | Active |
| Module Designer | Designs and implements detailed module-level changes within interface boundaries. | `.specify/agents/module-designer.agent.md` | Active |
| Test Engineer | Designs, writes, and executes tests validating implementations against specifications. | `.specify/agents/test-engineer.agent.md` | Active |
| QA Engineer | Validates integrated system quality against architecture and requirements. | `.specify/agents/qa-engineer.agent.md` | Active |
| Knowledge Manager | Manages project documentation, decision records, and knowledge assets. | `.specify/agents/knowledge-manager.agent.md` | Active |

## Role Workflow Chain

```
Requirements Analyst → System Designer → Module Designer → Test Engineer → QA Engineer
                                                         ↑                     ↓
                                                         └── feedback loop ────┘
                                                                                    ↓
                                                              Knowledge Manager (all roles)
```

## Multi-Agent Orchestration Modes

All orchestration is accessed through the unified `/speckit.agents` command, which uses intent recognition to automatically route to the correct pattern via the `organize-agents` skill.

### Parallel Dispatch
- **Use when**: Multiple independent tasks can be executed simultaneously
- **Pattern**: Territory isolation → Parallel dispatch → Result aggregation
- **Trigger**: `/speckit.agents` with intent signals like "并行", "parallel", "同时执行"

### Serial Chain
- **Use when**: Tasks have sequential dependencies (stage N output feeds stage N+1)
- **Pattern**: DAG definition → Topological execution → Progress tracking
- **Trigger**: `/speckit.agents` with intent signals like "串行", "pipeline", "阶段"

### Team Loop
- **Use when**: Complex deliverables need iterative quality improvement by a team
- **Pattern**: Team Supervisor (Meta role, coordination + quality gate) + Workers → Self-iterating quality loop (two layers; the former separate Meta-Coordinator is merged into the Team Supervisor)
- **Trigger**: `/speckit.agents` with intent signals like "团队", "闭环", "自迭代"

### Decision Guide
| Scenario | Recommended Mode |
|----------|------------------|
| Independent tasks, no shared state | Parallel Dispatch |
| Sequential phases with dependencies | Serial Chain |
| Quality-critical, needs iteration | Team Loop |
| Mix of independent + dependent | Serial Chain with parallel stages |

## Notes

- All role agents are **supervisors** by default (`supervisor: true`), capable of orchestrating EEI (Executor-Evaluator-Optimizer) loops.
- Tool-specific directories (`.github/agents/`, `.qoder/agents/`, `.qwen/agents/`, `.opencode/agents/`) are symlinks to `.specify/agents/`.
- Run `/speckit.instructions` to refresh discovery metadata after adding or updating agents.
