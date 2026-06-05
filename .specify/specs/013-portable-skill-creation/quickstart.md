# Quickstart: Portable Skill Creation

## Scenario 1: Create a new skill (post-change)

```bash
# Create a new skill
scripts/bash/create-new-skill.sh --json --name "my-new-skill" --description "A portable skill"

# Verify: no tools/ directory created
ls .specify/skills/my-new-skill/
# Expected: SKILL.md  scripts/  references/  assets/
# NOT expected: tools/

# Verify: SKILL.md has no tool-manifest references
grep -c "refresh-tools\|tools/system.json\|tools/shell.json\|tools/project.json" \
  .specify/skills/my-new-skill/SKILL.md
# Expected: 0
```

## Scenario 2: Refresh an existing skill (post-change)

```bash
# Refresh skill metadata (skill_id only, no tool manifests)
scripts/bash/create-new-skill.sh --refresh-only --name "create-skills" --json

# Verify: existing tools/ directory (if any) is untouched
# Verify: skill_id is present in frontmatter
grep "skill_id" skills/create-skills/SKILL.md
# Expected: skill_id: "<SKILL:.specify/skills/create-skills/SKILL.md>"
```

## Scenario 3: Cross-environment portability

```bash
# 1. Create a skill in environment A
scripts/bash/create-new-skill.sh --json --name "portable-demo"

# 2. Copy the skill directory to environment B (different machine, no refresh-tools.sh)
cp -r .specify/skills/portable-demo/ /other/machine/.specify/skills/portable-demo/

# 3. The skill works on environment B without errors
# Because SKILL.md contains no environment-specific tool references
```

## Scenario 4: Existing skill with user-authored tools/ directory

```bash
# A skill that already has a manually created tools/ directory
ls .specify/skills/custom-skill/tools/
# Expected: user-authored files remain untouched

# Running refresh-only does NOT delete or modify tools/
scripts/bash/create-new-skill.sh --refresh-only --name "custom-skill" --json
ls .specify/skills/custom-skill/tools/
# Expected: same files as before, unchanged
```

## Running contract tests

```bash
# Run all contract tests
pytest -m contract tests/contract/test_portable_skill_creation.py -v

# Run alongside existing skill tests
pytest -m contract tests/contract/ -v
```
