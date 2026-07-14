# Contract: Path Rewrite

**ID**: C-REWRITE | **Feature**: 029 | **Maps to**: FR-006, FR-008

## Interface

`rewrite_paths(content: str) -> str` upgrades root-relative core-asset paths to the installed
`.specify/` form when generating command files.

## Rules

- **MUST** add a rule mapping root-relative `shared/` → `.specify/shared/`, using the same
  negative-lookbehind guard as the existing `memory/`, `scripts/`, `templates/` rules.
- The guard **MUST** prevent double-prefixing an already-rewritten `.specify/shared/` path.
- The new rule **MUST** be applied wherever the existing rules run (command-body rewrite in `generate_commands`).

## Examples

```python
def rewrite_paths(content: str) -> str:
    import re
    content = re.sub(r"(?<!\.specify/)memory/", r".specify/memory/", content)
    content = re.sub(r"(?<!\.specify/)scripts/", r".specify/scripts/", content)
    content = re.sub(r"(?<!\.specify/)templates/", r".specify/templates/", content)
    content = re.sub(r"(?<!\.specify/)shared/", r".specify/shared/", content)   # NEW
    return content
```

| Input | Output |
|-------|--------|
| `shared/workflow/user-input-protocol.md` | `.specify/shared/workflow/user-input-protocol.md` |
| `.specify/shared/workflow/x.md` | `.specify/shared/workflow/x.md` (unchanged — guarded) |

## Test Mapping

- Unit test: `rewrite_paths("shared/workflow/x.md")` == `".specify/shared/workflow/x.md"`.
- Unit test: idempotence — re-running on an already-prefixed string is a no-op.
