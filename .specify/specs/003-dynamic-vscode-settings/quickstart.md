# Quickstart: Dynamic VS Code Settings

## Prerequisites

- Python 3.x installed.
- A project directory with some tech stack indicators (e.g., `pom.xml`, `pyproject.toml`).

## Usage

The script is designed to be run as part of the build process, but can be run manually.

### 1. Basic Run

```bash
python3 scripts/generate_vscode_settings.py \
  --template templates/vscode-settings.json \
  --output .vscode/settings.json \
  --root .
```

### 2. Verify Output

Check the generated file:

```bash
cat .vscode/settings.json
```

### 3. Test with Different Stacks

Create a dummy `pom.xml` to test Java detection:

```bash
touch pom.xml
python3 scripts/generate_vscode_settings.py ...
grep "java.configuration" .vscode/settings.json
rm pom.xml
```
