# Contract: Install Copy

**ID**: C-INSTALL | **Feature**: 029 | **Maps to**: FR-004, FR-005, FR-012, SC-003, SC-004, SC-005

## Interface

The `shared/` directory is a packaged core asset copied into the workspace at `init`.

## Rules

- **MUST** add `"shared" = "specify_cli/shared"` to `[tool.hatch.build.targets.wheel.force-include]` in `pyproject.toml`, alongside `memory`/`scripts`/`templates`/`skills`/`agents`.
- **MUST**, during `init`, copy `resource_path / "shared"` into `.specify/shared` using `shutil.copytree(..., dirs_exist_ok=True)`, mirroring the `skills`/`agents` copy blocks in `src/specify_cli/__init__.py`.
- The copy block **MUST** be guarded by `if (resource_path / "shared").exists():`.
- After a fresh `init`, `.specify/shared/workflow/` **MUST** contain all ten reference documents.
- **MUST** add `".specify/shared"` to `_CORE_SPECIFY_ASSETS` so re-init preserves it (retained core asset).
- Re-running `init` over an existing workspace **MUST NOT** overwrite or delete `.specify/shared/workflow/`.

## Examples

```python
# init copy (new block, shape matches skills copy at ~L1267)
if (resource_path / "shared").exists():
    shared_dest = project_path / ".specify" / "shared"
    shared_dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(resource_path / "shared", shared_dest, dirs_exist_ok=True)
```

```python
_CORE_SPECIFY_ASSETS = [
    ".specify/memory",
    ".specify/templates",
    ".specify/scripts",
    ".specify/skills",
    ".specify/agents",
    ".specify/shared",          # NEW
    ".specify/instructions.md",
]
```

## Test Mapping

- Contract test: force-include contains `shared`; init copies `shared/workflow/*` into `.specify/shared/workflow/`.
- Integration test: fresh init → 10 docs present; re-init → directory unchanged (retained).
