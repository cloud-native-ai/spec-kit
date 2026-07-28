# /speckit.docs

Standardize and manage the project documentation space as a single reconcile engine.

## When to Use

- Bootstrap a standard documentation skeleton on a new project.
- Converge an existing, drifted `docs/` tree back toward the desired state (full sweep).
- Reorganize one document or triage a raw material dump into the right doc types.
- Operate the `docs/notes/` lifecycle (expire / archive / renew / confirmed deletion).

## Syntax

```text
/speckit.docs                    # full sweep over the managed space
/speckit.docs <path-or-target>   # single-target directional reconcile
/speckit.docs <raw material>     # fan-out intake: triage into doc types
```

`/speckit.docs` is a chat instruction, not a terminal command.

## Desired State (baseline)

- **Thin root layer** — uppercase special names with fixed semantics (filename IS semantics), each ≤ one screen:
  `README.md` (indexes all of `docs/`) · `ARCHITECTURE.md` (summary of concepts + decisions) · `CONTRIBUTING.md` (summary of contribute) · `CHANGELOG.md` (self-contained timeline). Registry is extensible; ordinary docs use lowercase kebab-case.
- **Thick `docs/` layer** — `concepts/ tutorials/ tasks/ reference/ decisions/ contribute/` (formal, archive-not-delete) + `notes/` (temporary, lifecycle-constrained).
- **ADR** — `docs/decisions/NNNN-slug.md`, append-only, status Proposed / Accepted / Deprecated / Superseded by.
- **Notes lifecycle** — frontmatter (`title/created/expires/status/target/tags`, default TTL 60 days); state machine draft → expired → (renew | confirmed delete) and draft → archived (merged into `target`).

## Execution Flow

1. **Scope resolution**: full sweep / single target / fan-out / bootstrap.
2. **R0–R6 reconcile loop** (per `shared/patterns/reconcile-pattern.md`): observe snapshot → desired state → diff through the tolerance band → dry-run plan with per-item opt-out → tiered convergence → verify + residual report.
3. **Tiered gates**: safe local writes auto-execute (never clobber); moves/archives/restructures require plan confirmation; the formal zone is archive-only (`docs/archive/`); notes deletion requires explicit human confirmation.

## Deterministic Engine

```bash
python3 .specify/scripts/python/docs-utils.py --action scan --root .
python3 .specify/scripts/python/docs-utils.py --action expire --root .
python3 .specify/scripts/python/docs-utils.py --action clean [--yes] --root .
python3 .specify/scripts/python/docs-utils.py --action archive-check --root .
python3 .specify/scripts/python/docs-utils.py --action stats --root .
python3 .specify/scripts/python/docs-utils.py --action validate --root .
python3 .specify/scripts/python/docs-utils.py --action audit --root . --scope <s> --summary <text>
```

`validate` covers the deterministic dimensions: reserved-name case/misuse, one-screen threshold for root entries, broken relative links, ADR numbering continuity, notes frontmatter completeness.

## Output Artifacts

| Artifact | Location | Always produced |
|----------|----------|-----------------|
| Observation snapshot | inline in chat | yes |
| Dry-run plan | `.specify/docs/plans/` | when moves/archives are proposed |
| Audit log | `.specify/docs/audit/` | yes — even a no-op run records "all dimensions within tolerance" |
| Residual report | inline in chat | yes |

## Tool Support

Distributed like every other `/speckit.*` command to all supported AI tools (Claude Code, Codex CLI, Qoder CLI, GitHub Copilot, opencode, Qwen Code, Hermes Agent, iFlow CLI) via the standard command-generation path.

## Related

- Engine contract: `.specify/specs/033-docs-command/contracts/docs-utils-cli.md`
- Reconcile pattern: `shared/patterns/reconcile-pattern.md` (mirrored at `.specify/shared/patterns/`)
- Docs-sync step convention: `shared/workflow/docs-step.md`
