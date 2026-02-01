# Feature Reference: Skills Command Integration

## Feature Details
- **Feature ID**: 003
- **Name**: Skills Command Integration
- **Status**: Implemented
- **Specification**: [.specify/specs/001-skills-command-integration/spec.md](spec.md)
- **Implementation Plan**: [.specify/specs/001-skills-command-integration/plan.md](plan.md)

## Key Capabilities
1. **Refresh Existing Skills**: Execute `/speckit.skills` without parameters to synchronize all installed skills with current speckit documentation
2. **Create New Skills**: Execute `/speckit.skills "<name> - <description>"` to generate new skill directories with proper structure

## Related Files and Directories
- **Skill Storage**: `.github/skills/`
- **Command Template**: `templates/commands/skills.md`
- **Skill Template**: `templates/skills-template.md`
- **Bash Scripts**: `scripts/bash/create-new-skill.sh`, `scripts/bash/refresh-skills.sh` (to be created)
- **Feature Documentation**: `.specify/memory/features/003-skills-command-integration.md`

## Integration Points
- **Specification-Driven Development Workflow**: Integrates as a core command in the SDD workflow
- **AI Agent Support**: Compatible with approved AI agents (GitHub Copilot, Qwen Code, opencode)
- **Existing Command Patterns**: Follows established patterns from other speckit commands like `/speckit.specify`

## Validation Requirements
- Skill names must follow naming conventions (alphanumeric, hyphens, underscores only)
- Skill directory structure must include SKILL.md, scripts/, references/, assets/
- SKILL.md must contain proper YAML frontmatter with name and description
- Error handling must provide clear, actionable feedback for invalid inputs

## Success Metrics
- Refresh operation completes in under 10 seconds
- New skill creation completes in under 5 seconds  
- 95% of valid skill creation attempts succeed without manual intervention
- Error messages enable 90% of users to correct input on first retry