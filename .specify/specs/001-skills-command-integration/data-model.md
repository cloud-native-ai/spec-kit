# Data Model: Skills Command Integration

## Entities

### Skill
Represents a modular capability package that extends the spec-kit framework.

**Fields:**
- `name` (string): Unique identifier for the skill, following naming conventions (alphanumeric, hyphens, underscores only)
- `description` (string): Brief description of what the skill does and when to use it
- `directory_path` (string): File system path where the skill is stored (`.github/skills/{name}/`)
- `status` (enum): Current status of the skill (active, archived, deprecated)

**Validation Rules:**
- Name must match regex pattern: `^[a-zA-Z0-9_-]+$`
- Name must be unique within the project
- Description must be non-empty and provide clear usage context

### SkillDirectory
File system structure that defines a complete skill.

**Components:**
- `SKILL.md`: Required file containing YAML frontmatter and markdown instructions
- `scripts/`: Optional directory for executable code (bash, python, etc.)
- `references/`: Optional directory for documentation and reference material
- `assets/`: Optional directory for output templates and resources

**Relationships:**
- Each Skill has exactly one SkillDirectory
- SkillDirectory belongs to exactly one Skill

### SkillSpecification
Source documentation that defines how skills should be structured and what capabilities they provide.

**Fields:**
- `source_location` (string): Path to specification source (speckit documentation)
- `last_updated` (timestamp): When the specification was last modified
- `version` (string): Version of the specification format

**Relationships:**
- Multiple Skills can reference the same SkillSpecification
- SkillSpecification can be used to refresh multiple Skills

## State Transitions

### Skill Lifecycle
- **Created**: New skill directory structure initialized with template
- **Active**: Skill is available for use in the framework
- **Updated**: Skill refreshed from latest specification
- **Archived/Deprecated**: Skill marked as no longer recommended for use

### SkillDirectory Operations
- **Initialize**: Create standard directory structure with SKILL.md and resource directories
- **Validate**: Verify directory structure matches expected pattern
- **Refresh**: Update SKILL.md content based on current specification
- **Cleanup**: Remove unnecessary files or directories

## Validation Rules from Requirements

From Functional Requirements:
- **FR-004**: Skill names validated against naming conventions (alphanumeric, hyphens, underscores only)
- **FR-005**: Standard skill directory structure must include SKILL.md, scripts/, references/, assets/
- **FR-006**: SKILL.md must contain proper YAML frontmatter with name and description fields
- **FR-007**: System handles missing `.github/skills/` directory by creating it automatically