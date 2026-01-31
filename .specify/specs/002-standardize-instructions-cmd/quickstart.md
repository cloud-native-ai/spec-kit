# Instructions Command Quickstart

## Usage

Run the instructions command to generate or update the AI agent instructions file.

```bash
speckit instructions
```

## Prerequisites

- `templates/instructions-template.md` must exist in your project root.

## Behavior

1. **Initialization**: Creates `.ai/instructions.md` if it doesn't exist.
2. **Update**: If it exists, it upgrades the structure while preserving your content (Smart Fusion).
3. **Integration**: Creates symlinks in `.clinerules/` for compatibility with AI tools.

## Troubleshooting

- **Template Not Found**: Ensure you have copied the default template to `templates/`.
- **Fusion Errors**: Check `.ai/instructions.md.bak` for the original content if the merge looks incorrect.
