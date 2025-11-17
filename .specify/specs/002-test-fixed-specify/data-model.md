# Data Model: Feature Management

## Feature Entity

Represents a single capability or functionality in the system.

### Attributes

| Attribute | Type | Description | Validation Rules |
|-----------|------|-------------|------------------|
| `id` | string | Sequential three-digit identifier (e.g., "001", "002") | Must be exactly 3 digits, sequential based on existing features |
| `name` | string | Short name (2-4 words) describing the feature | 2-50 characters, alphanumeric + spaces/hyphens only |
| `description` | string | Brief summary of the feature's purpose and scope | 10-500 characters, required |
| `status` | enum | Current implementation status | Must be one of: "Draft", "Planned", "Implemented", "Ready for Review" |
| `spec_path` | string | Path to specification file | Must be relative path starting with `.specify/specs/`, or "(Not yet created)" |
| `last_updated` | timestamp | When the feature entry was last modified | ISO 8601 format (YYYY-MM-DD) |

### State Transitions

The `status` attribute follows a strict lifecycle:

```
Draft → Planned → Implemented → Ready for Review
```

- **Draft**: Initial state when feature is created via `/speckit.feature`
- **Planned**: Set by `/speckit.specify` when specification is created
- **Implemented**: Set by `/speckit.plan` and maintained by `/speckit.implement`
- **Ready for Review**: Set by `/speckit.checklist` when quality checks pass

### Relationships

- **FeatureIndex**: Each Feature belongs to exactly one FeatureIndex (the `features.md` file)

## FeatureIndex Entity

Represents the project-level registry of all features.

### Attributes

| Attribute | Type | Description | Validation Rules |
|-----------|------|-------------|------------------|
| `last_updated` | timestamp | When the index was last modified | ISO 8601 format (YYYY-MM-DD) |
| `total_features` | integer | Total number of features in the index | Must match actual count of Feature entries |
| `features` | array<Feature> | Collection of all Feature entities | Must contain all features in the project |

### Relationships

- **Feature**: Contains zero or more Feature entities

## Data Storage Format

The data model is persisted in a Markdown table format in `features.md`:

```markdown
# Project Feature Index

**Last Updated**: November 17, 2025
**Total Features**: 2

## Features

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
| 001 | User Authentication | Add email/password and OAuth2 login | Planned | .specify/specs/001-user-auth/spec.md | 2025-11-17 |
| 002 | Payment Processing | Implement credit card and PayPal payments | Draft | (Not yet created) | 2025-11-17 |
```

### Validation Rules for Storage Format

1. **Table Header**: Must contain exactly the columns: ID, Name, Description, Status, Spec Path, Last Updated
2. **ID Format**: Must be exactly 3 digits with leading zeros (001, 002, ..., 999)
3. **Status Values**: Must be one of the four allowed values
4. **Spec Path**: Must either be "(Not yet created)" or a valid relative path starting with `.specify/specs/`
5. **Last Updated**: Must be in YYYY-MM-DD format
6. **Total Features**: Must match the actual number of table rows

## Orphaned Feature Handling

When a feature specification file is deleted but the feature entry remains in `features.md`:
- The entry is marked as "orphaned" but not automatically removed
- The `spec_path` field shows "(Orphaned - spec file deleted)"
- Status remains unchanged to preserve historical tracking

## Concurrency Handling

- Multiple processes writing to `features.md` simultaneously will cause git merge conflicts
- Users must manually resolve conflicts during git merge operations
- No locking mechanism is implemented (rely on git's built-in conflict detection)