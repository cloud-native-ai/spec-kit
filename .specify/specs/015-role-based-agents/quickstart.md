# Quickstart Validation: Role-Based Agent Templates

**Spec**: 015-role-based-agents | **Date**: 2026-06-17

## Prerequisites

- Spec Kit installed (`specify` CLI available)
- A project initialized with `specify init`
- `.specify/agents/` directory exists

## Scenario 1: Generate all role-based agents (US1 - P1)

**Steps**:
1. Run `/speckit.agents` with no arguments in an initialized project
2. Verify six agent files are created under `.specify/agents/`:
   - `requirements-analyst.agent.md`
   - `system-designer.agent.md`
   - `module-designer.agent.md`
   - `test-engineer.agent.md`
   - `qa-engineer.agent.md`
   - `knowledge-manager.agent.md`
3. Verify each agent file has valid YAML frontmatter with `name`, `description`, `tools`, `user-invocable: true`
4. Verify each agent body contains project-specific context (not `{{PLACEHOLDER}}` variables)
5. Verify existing agents (e.g., `code-reviewer.agent.md`) are untouched

**Expected**: Six role-based agents generated with project-aware content; existing agents preserved.

## Scenario 2: Legacy templates removed (US2 - P1)

**Steps**:
1. Verify `templates/agent-common-template.md` does NOT exist
2. Verify `templates/agent-knowledge-template.md` does NOT exist
3. Verify `templates/agent-plan-template.md` does NOT exist
4. Verify `templates/agent-research-template.md` does NOT exist
5. Verify six `templates/agent-role-*-template.md` files exist
6. Run `/speckit.agents` and verify it uses role templates, not type templates

**Expected**: Old capability-based templates removed; new role-based templates in place.

## Scenario 3: Workflow handoffs (US3 - P2)

**Steps**:
1. Open `requirements-analyst.agent.md` — verify Downstream section references System Designer
2. Open `system-designer.agent.md` — verify Upstream references Requirements Analyst, Downstream references Module Designer and QA Engineer
3. Open `module-designer.agent.md` — verify Upstream references System Designer, Downstream references Test Engineer
4. Open `test-engineer.agent.md` — verify Upstream references Module Designer, Downstream references Module Designer (feedback) and QA Engineer
5. Open `qa-engineer.agent.md` — verify Upstream references System Designer and Test Engineer, Downstream references Requirements Analyst
6. Open `knowledge-manager.agent.md` — verify Upstream and Downstream reference all roles

**Expected**: Complete handoff chain traceable through all six agents.

## Scenario 4: Regeneration with backup (FR-008a)

**Steps**:
1. Generate role-based agents via `/speckit.agents`
2. Manually edit `system-designer.agent.md` (add a custom line)
3. Re-run `/speckit.agents`
4. Verify `system-designer.agent.md.bak` exists with the customized content
5. Verify `system-designer.agent.md` contains the freshly generated content
6. Verify a warning was displayed about the backup

**Expected**: Customized agent backed up before overwrite; warning shown to user.

## Scenario 5: Dynamic context injection (US4 - P2)

**Steps**:
1. Run `/speckit.agents` in a Python project with `src/` layout
2. Verify Module Designer agent references actual modules under `src/`
3. Verify QA Engineer agent references constitution principles
4. Verify System Designer agent references the feature index
5. Run `/speckit.agents` in a different project (e.g., Node.js)
6. Compare generated agents — project-specific sections should differ

**Expected**: Generated agents contain real project context, not generic placeholders.

## Scenario 6: Custom agent creation (backwards compatibility)

**Steps**:
1. Run `/speckit.agents create a security auditor agent`
2. Verify a custom `security-auditor.agent.md` is created in `.specify/agents/`
3. Verify the custom agent does NOT use a role-based template
4. Verify existing role-based agents are untouched

**Expected**: Custom (non-role) agent creation still works alongside role-based generation.

## Scenario 7: Symlink compatibility

**Steps**:
1. Generate role-based agents
2. Verify `.github/agents/` symlinks to `.specify/agents/`
3. Verify role-based agents are visible through the symlink
4. Verify agents work when invoked via tool-specific paths

**Expected**: All symlink-based discovery paths see the generated role-based agents.
