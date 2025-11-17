# Contract: SDD Command Integration with Feature Tracking

## Purpose
Define how all existing SDD commands (`/speckit.plan`, `/speckit.tasks`, `/speckit.implement`, `/speckit.checklist`) integrate with the feature index for automatic status updates.

## Integration Requirements

All SDD commands must:

1. **Detect Feature Context**: Determine if they are running in the context of a feature
2. **Parse Feature ID**: Extract the feature ID from branch name or directory structure
3. **Update Feature Index**: Modify the corresponding feature entry in `features.md`
4. **Stage Changes**: Automatically stage `features.md` changes with `git add features.md`

## Feature ID Detection

### From Branch Name
- Pattern: `###-feature-name` (e.g., `001-user-auth`, `002-payment-processing`)
- Extract: First 3 digits as feature ID
- Validate: Must be exactly 3 digits

### From Directory Structure  
- Pattern: `.specify/specs/###-feature-name/`
- Extract: First 3 digits from directory name
- Validate: Must be exactly 3 digits

### Fallback Behavior
- If no feature context detected: Skip feature index updates
- If feature ID invalid: Log warning but continue execution
- If features.md doesn't exist: Skip updates (no feature tracking enabled)

## Status Transition Matrix

| Command | Current Status | New Status | Additional Updates |
|---------|----------------|------------|-------------------|
| `/speckit.specify` | Draft | Planned | Set `spec_path` to spec.md location |
| `/speckit.plan` | Planned | Implemented | Set `plan_path` (if tracked) |
| `/speckit.tasks` | Implemented | Implemented | No status change |
| `/speckit.implement` | Implemented | Implemented | No status change |
| `/speckit.checklist` | Implemented | Ready for Review | Set `checklist_path` and validation results |

## Implementation Pattern

Each SDD command template should include this integration logic:

```bash
# Check if feature index exists
if [ -f "features.md" ]; then
    # Extract feature ID from branch or directory
    FEATURE_ID=$(extract_feature_id)
    
    if [ -n "$FEATURE_ID" ]; then
        # Update feature status in features.md
        update_feature_status "$FEATURE_ID" "NEW_STATUS"
        
        # Stage the changes
        if command -v git >/dev/null 2>&1; then
            git add features.md
        fi
    fi
fi
```

## Error Handling

### Feature Index Update Failures
- **File not found**: Skip update (feature tracking not enabled)
- **Invalid format**: Log error but continue command execution
- **Parse errors**: Use backup parsing strategy or skip update
- **Write permissions**: Log error but continue command execution

### Git Staging Failures
- **Git not available**: Skip staging (continue without git integration)
- **Staging errors**: Log warning but continue command execution
- **No changes to stage**: Normal behavior (no error)

## Performance Requirements

- **Feature detection**: < 100ms overhead per command
- **Status updates**: < 200ms for files with up to 100 features
- **Git staging**: < 100ms for single file staging

## Validation Requirements

Each integration must be validated with:

1. **Feature context detection**: Verify correct feature ID extraction
2. **Status updates**: Verify correct status transitions in features.md
3. **Metadata updates**: Verify spec_path and other metadata is correctly recorded
4. **Git integration**: Verify changes are properly staged
5. **Error resilience**: Verify commands continue execution even if integration fails

## Backward Compatibility

- **Existing projects**: Commands work without feature index (no breaking changes)
- **New projects**: Automatic feature tracking enabled when features.md exists
- **Mixed usage**: Projects can enable/disable feature tracking at any time