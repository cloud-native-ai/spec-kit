# Data Model: Dynamic VS Code Settings

## Entities

### 1. Project Context
Represents the detected characteristics of the target project.

| Field | Type | Description |
|-------|------|-------------|
| `root_dir` | Path | The root directory of the project to analyze. |
| `tech_stack` | Set<String> | Detected technologies (e.g., `{'java', 'python'}`). |
| `has_constitution` | Boolean | Whether `memory/constitution.md` exists. |
| `has_feature_index` | Boolean | Whether `memory/feature-index.md` exists. |

### 2. Settings Template
The source configuration file.

| Field | Type | Description |
|-------|------|-------------|
| `content` | String (JSONC) | The raw content of `templates/vscode-settings.json`, potentially containing comments. |

### 3. Generated Settings
The final configuration object to be written.

| Field | Type | Description |
|-------|------|-------------|
| `settings` | Dictionary | The parsed and merged key-value pairs for VS Code settings. |

## Data Flow

1. **Input**: Read `templates/vscode-settings.json`.
2. **Process**: 
   - Strip comments from Template.
   - Parse into Dictionary.
   - Detect Project Context (scan `root_dir`).
   - **Merge**: Inject specific keys into Dictionary based on `tech_stack`.
3. **Output**: Write Dictionary to `.vscode/settings.json` as standard JSON.
