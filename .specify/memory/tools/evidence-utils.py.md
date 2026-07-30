# Tool Record: evidence-utils.py

**Tool Name**: evidence-utils.py  
**Tool Type**: `project-script`  
**Source Identifier**: scripts/python/evidence-utils.py  
**Tool ID**: <TOOL:.specify/memory/tools/evidence-utils.py.md>  
**Aliases**: evidence-utils  
**Status**: Verified  
**Discovery Origin**: manual-entry  
**Last Updated**: 2026-07-30

## Scope

**Availability**: Project-level — available only within the current project workspace.  
**Typical Sources**: Scripts bundled with the project (e.g., `scripts/bash/*.sh`, `scripts/python/*.py`, `.specify/scripts/`).  
**Portability**: Tied to the project repository; not available outside the project root.  
**Source Identifier Convention**: Path relative to the project root.

## Description

The evidence-lane orchestrator: gathers normalized `findings.json` evidence for a target unit across five lanes (session / project / assets / runs / feedback), lists and retrieves prior evidence runs, and compares a baseline run against a current one to decide whether an intervention produced an observable change.

## Resource ID

- Canonical ID: `<TOOL:.specify/memory/tools/evidence-utils.py.md>`
- Canonical Path: `.specify/memory/tools/evidence-utils.py.md`

## Invocation & I/O Contract

- **Input Channel**: command-line flags
- **Invocation Mode**: non-interactive, read-only with respect to the observed target
- **Output Mode**: JSON on stdout

## Parameters

| Name | Required | Description |
|------|----------|-------------|
| `--action` | yes | One of `doctor`, `collect`, `list`, `latest`, `compare` |
| `--target` | for `collect` / `latest` | The observed unit, e.g. `skill:create-tools` |
| `--lanes` | no | Lane selection, e.g. `all` or a comma-separated subset |
| `--since` / `--until` | no | Observation window bounds |
| `--depth` | no | `quick` or `normal` |
| `--platform` | no | Restrict to one agent platform |
| `--limit` | no | Cap the number of listed runs |
| `--max-age-days` | no | Freshness bound when reusing a prior run |
| `--baseline` / `--current` | for `compare` | Run IDs to compare |

## Returns

| Field | Description |
|-------|-------------|
| `runId` | Identifier of the evidence run |
| `path` | Directory holding `findings.json` for the run |
| `lanes` | Per-lane status (`available` / `partial` / unavailable) |
| `evidenceCount` | Number of normalized evidence items collected |
| `findingsDigest` | Content digest of the emitted findings |
| `found` | `false` from `--action latest` when no prior run exists for the target |

## Usage Notes

- Evidence carries an `evidenceState` per item; `Unobserved` means "not seen", which is **not** the same as "defect found".
- `--action latest` returns `{"found": false}` rather than failing when a target has no prior run — check that before assuming evidence exists.
- Findings are privacy-redacted and carry no verdict fields; interpretation is the caller's job.

## Examples

**Input**

```json
{ "action": "collect", "target": "skill:create-tools", "lanes": "all" }
```

**Output**

```json
{ "runId": "ev-20260730-022019-create-tools", "path": ".specify/memory/evidence/ev-20260730-022019-create-tools", "lanes": { "session": "available", "runs": "partial" }, "evidenceCount": 7 }
```

## Behavioral Rules

- MUST be run from the repository root directory, or with an explicit `--workspace-root`
- MUST treat `Unobserved` evidence as "not observed", never as a confirmed defect to fix
- MUST NOT derive improvement conclusions from counting signals alone
- MUST NOT write to the observed target; the engine only writes under `.specify/memory/evidence/`
- SHOULD reuse a fresh prior run via `--action latest` before paying for a new `--action collect`
- SHOULD use `--action compare` with a recorded baseline before claiming an intervention worked

## Discovery Metadata

- **Method**: manual definition
- **Source**: project scripts directory
- **Verification Status**: verified
- **Notes**: Contract confirmed against the script's `--help` output and real `--action latest` / `--action collect` invocations on 2026-07-30.
