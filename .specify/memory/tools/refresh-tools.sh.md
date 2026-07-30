# Tool Record: refresh-tools.sh

**Tool Name**: refresh-tools.sh  
**Tool Type**: `project-script`  
**Source Identifier**: scripts/bash/refresh-tools.sh  
**Tool ID**: <TOOL:.specify/memory/tools/refresh-tools.sh.md>  
**Aliases**: refresh-tools  
**Status**: Verified  
**Discovery Origin**: manual-entry  
**Last Updated**: 2026-07-30

## Scope

**Availability**: Project-level — available only within the current project workspace.  
**Typical Sources**: Scripts bundled with the project (e.g., `scripts/bash/*.sh`, `scripts/python/*.py`, `.specify/scripts/`).  
**Portability**: Tied to the project repository; not available outside the project root.  
**Source Identifier Convention**: Path relative to the project root.

## Description

Discovers the helper tools available to this workspace across three sources (system binaries, shell functions, project scripts) and emits a unified JSON inventory. This is the discovery engine behind `/speckit.tools`; it populates the inventory at `.specify/memory/tools.md` and is **not** a definition-record writer.

## Resource ID

- Canonical ID: `<TOOL:.specify/memory/tools/refresh-tools.sh.md>`
- Canonical Path: `.specify/memory/tools/refresh-tools.sh.md`

## Invocation & I/O Contract

- **Input Channel**: command-line flags
- **Invocation Mode**: non-interactive, read-only
- **Output Mode**: JSON on stdout (with `--json`); diagnostics on stderr (with `--debug`)

## Parameters

| Name | Required | Description |
|------|----------|-------------|
| `--system` | no | Query system binaries on `PATH` |
| `--shell` | no | Query shell functions in the current session |
| `--project` | no | Query project scripts under `.specify/scripts/` then `scripts/` |
| `--json` | no | Emit the unified JSON payload for the selected sources |
| `--debug` | no | Emit diagnostics to stderr while keeping stdout JSON-only |

At least one source flag must be supplied; `--format markdown` is explicitly rejected.

## Returns

| Field | Description |
|-------|-------------|
| `tools` | Flat list of discovered tools; each item carries `sourceType`, `sourceName`, `canonicalName` |
| `system_binaries` | System binaries found on `PATH` |
| `shell_functions` | Functions defined in the invoking shell session |
| `project_scripts` | `*.sh` / `*.py` scripts found under the project's script directories |

## Usage Notes

- Output is a snapshot of the invoking environment: shell functions reflect the *calling* shell, so results differ between an interactive shell and a fresh non-interactive one.
- Discovery output is advisory input for authoring a definition record — it is not itself authoritative about how a tool should be invoked.

## Examples

**Input**

```json
{ "flags": ["--project", "--json"] }
```

**Output**

```json
{ "tools": [ { "sourceType": "project", "sourceName": "scripts/bash/refresh-tools.sh", "canonicalName": "project:scripts/bash/refresh-tools.sh" } ], "project_scripts": ["..."] }
```

## Behavioral Rules

- MUST be run from the repository root directory
- MUST be invoked with at least one source flag (`--system` / `--shell` / `--project`)
- MUST NOT be used to write or edit tool definition records under `.specify/memory/tools/`
- MUST NOT be passed `--format markdown` — that form is rejected by design
- SHOULD be paired with `--json` when the output is consumed programmatically
- SHOULD be treated as a discovery snapshot only; the user confirms every field before a record reaches `Verified`

## Discovery Metadata

- **Method**: manual definition
- **Source**: project scripts directory
- **Verification Status**: verified
- **Notes**: Contract confirmed against the script's own `--help` output on 2026-07-30.
