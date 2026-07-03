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

## Notes

- All role agents are **supervisors** by default (`supervisor: true`), capable of orchestrating EEI (Executor-Evaluator-Improver) loops.
- Tool-specific directories (`.github/agents/`, `.qoder/agents/`, `.qwen/agents/`, `.opencode/agents/`) are symlinks to `.specify/agents/`.
- Run `/speckit.instructions` to refresh discovery metadata after adding or updating agents.
