# Tool Record: sanitize-utils.py

**Tool Name**: sanitize-utils.py  
**Tool Type**: `project-script`  
**Source Identifier**: scripts/python/sanitize-utils.py  
**Tool ID**: <TOOL:.specify/memory/tools/sanitize-utils.py.md>  
**Aliases**: sanitize-utils  
**Status**: Verified  
**Discovery Origin**: manual-entry  
**Last Updated**: 2026-08-20 (requirement 045 / Feature 047: initial engine)

## Scope

**Availability**: Project-level — available only within the current project workspace (framework repo and client projects alike; the engine ships in both `scripts/python/` and its `.specify/scripts/python/` mirror).  
**Typical Sources**: Scripts bundled with the project (`scripts/python/*.py`).  
**Portability**: Tied to the project repository; not available outside the project root.  
**Source Identifier Convention**: Path relative to the project root.

## Description

The framework material hygiene engine (Feature 047): runs deterministic correctness checks (dead references over material prose with fence/placeholder exemptions — docs tree reuses `docs-utils.broken_links`; index↔store bidirectional consistency for the features/feedback/evidence families; compat-symlink three-state checks conditioned on tool-surface presence; mirror drift via the sibling `sync-mirrors.py --check` plus orphan-directory and `_OBSOLETE_*` registry cross-check), gathers bounded evidence packs (git log since the material's claim date over its referenced paths + path existence) for agent-side semantic staleness/redundancy judgment, persists findings into the cumulative ledger `.specify/memory/sanitize/findings.json` (stable ID `sha1(category|target)[:12]`, lifecycle pending/resolved/dismissed, auto-resolution on non-re-detection), and executes confirmation-gated cleanup (`apply` refuses unconfirmed plans and out-of-whitelist targets with exit 2; archive moves to `.specify/archive/` preserving relative layout; failures reported honestly without rollback).

## Resource ID

- Canonical ID: `<TOOL:.specify/memory/tools/sanitize-utils.py.md>`

## Behavioral Rules

1. **Write confinement**: `collect`/`record` write ONLY the findings store (`.part` + `os.replace` atomic); `status` is zero-write; checked materials are never modified during check stages.
2. **Exit codes**: 0 success / 1 CLI error (unknown action, unreadable input) / 2 verification failure (unconfirmed plan, schema violation, out-of-whitelist target, disposition mismatch).
3. **Schema gate is all-or-nothing**: `record` rejects the entire verdicts file on any schema violation (stable-ID recomputation, enums, semantic-evidence rules, disposition↔reversibility binding, target whitelist, semantic-only detection).
4. **Scope red line**: delete/archive targets must hit the material-root whitelist; `src/`, `tests/`, `node_modules/`, `.git/` are always refused.
5. **Partial scans never auto-resolve**: `--roots` subset runs disable auto-resolution entirely (conservative C-14 rule).
6. **Evidence honesty**: semantic candidates carry only mechanically gathered claims + bounded git evidence (≤20 lines); git failure degrades the lane with a note, never fabricates.
7. **sync-mirrors lane locality**: the mirror-drift subprocess lane runs only when the workspace IS the sibling script's repository root (framework dogfood or installed client copy); otherwise it is skipped — running it against a foreign workspace would inspect the wrong tree.

## Environment Applicability

- **Verified**: Python ≥ 3.8, stdlib-only, Linux/macOS; git ≥ 2.x for the semantic evidence lane (optional — degrades with note).
- **Version differences**: none (no third-party dependencies).
- **Platform**: cross-platform; compat-symlink checks rely on `Path.is_symlink()` (Windows symlink semantics may differ — findings degrade to "replaced by regular file").
- **Fallback**: non-git environments lose only semantic staleness detection; deterministic checks run everywhere.
- **Preflight**: the command template probes `python3` + engine script presence before Stage 2.
