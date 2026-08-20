# /speckit.docs

Standardize and manage the project documentation space as a single reconcile engine.

> Architecture: `/speckit.docs` is a thin dispatch layer. All engine semantics (desired-state baseline, scope resolution, reconcile loop, tiered gates, authoring flow, notes automation) live in the **`create-docs` skill** (`.specify/skills/create-docs/SKILL.md`), which the command loads and executes with its arguments. The skill is equally usable standalone (e.g. a knowledge-manager agent invoking it directly).

## When to Use

- Bootstrap a standard documentation skeleton on a new project.
- Converge an existing, drifted `docs/` tree back toward the desired state (full sweep).
- Reorganize one document or triage a raw material dump into the right doc types.
- Author new documents from a writing commission — the command places each document per the taxonomy and enforces all naming/format norms.
- Operate the `docs/notes/` lifecycle (expire / archive / renew / confirmed deletion).

## Syntax

```text
/speckit.docs                    # full sweep over the managed space
/speckit.docs <path-or-target>   # single-target directional reconcile
/speckit.docs <raw material>     # fan-out intake: triage into doc types
/speckit.docs <writing request>  # authoring: create new compliant documents
```

`/speckit.docs` is a chat instruction, not a terminal command.

## Desired State (baseline)

- **Thin root layer** — uppercase special names with fixed semantics (filename IS semantics), each ≤ one screen:
  `README.md` (indexes all of `docs/`) · `ARCHITECTURE.md` (summary of concepts + decisions) · `CONTRIBUTING.md` (summary of contribute) · `CHANGELOG.md` (self-contained timeline). These are **Reserved Filenames** (like reserved keywords, constitution Principle X): each registers semantics + location and may appear ONLY there — user documents must not reuse them; directory indexes elsewhere are `index.md`, never a nested `README.md`. Registry is extensible; ordinary docs use lowercase kebab-case.
- **Thick `docs/` layer** — `concepts/ tutorials/ tasks/ reference/ decisions/ contribute/` (formal, archive-not-delete) + `notes/` (temporary, lifecycle-constrained).
- **ADR** — `docs/decisions/NNNN-slug.md` (+ `index.md` + `template.md`), append-only, status Proposed / Accepted / Deprecated / Superseded by.
- **Notes lifecycle** — frontmatter (`title/created/expires/status/target/tags`, default TTL 60 days); state machine draft → expired → (renew | confirmed delete) and draft → archived (merged into `target`).

## Execution Flow

1. **Scope resolution**: full sweep / single target / fan-out / authoring / bootstrap.
2. **R0–R6 reconcile loop** (per `shared/patterns/reconcile-pattern.md`): observe snapshot → desired state → diff through the tolerance band → dry-run plan with per-item opt-out → tiered convergence → verify + residual report.
3. **Tiered gates**: safe local writes auto-execute (never clobber); moves/archives/restructures require plan confirmation; the formal zone is archive-only (`docs/archive/`); notes deletion requires explicit human confirmation.
4. **Authoring scope** (writing commission in arguments): parse the request → place each document in its taxonomy home → confirm an inline writing plan (path, type, title, outline) → write documents that comply with the baseline (lowercase kebab-case names, reserved-name blocking, ADR numbering + index registration, notes frontmatter, one-screen root entries, local style conventions, never clobber) → `validate` + index updates + audit log. If the topic is already covered, the command proposes updating the existing document instead of creating a near-duplicate.

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

`validate` covers the deterministic dimensions: reserved-name case/misuse/misplacement, one-screen threshold for root entries, broken relative links, ADR numbering continuity, notes frontmatter completeness.

## Static Site (optional, not part of this command)

Publishing the space as a static site is an **optional** capability layered on top of the
structure, owned by the `create-pages` skill — a documentation space is complete and valid
without it. `/speckit.docs` never scaffolds, mounts, or builds a site; it only skips the
site-tooling directories (`layouts/`, `static/`, `public/`, `resources/`, `themes/`,
`archetypes/`) so they are never triaged as content or archived.

`create-pages` offers two modes: **CI-deployed pages** (`<docs>/hugo.yaml` + platform
pipeline) and **in-place mount site** (`<docs>/hugo.toml`, Markdown mounted rather than
copied, build output in `<docs>/public/`). Details, commands, and CI guidance live in
`.specify/skills/create-pages/SKILL.md` and its `references/hugo-site.md`.

A move that adds or removes a documentation directory can stale an existing site's mounts —
a reconcile run reports that as a `create-pages` follow-up instead of repairing it.

## Output Artifacts

| Artifact | Location | Always produced |
|----------|----------|-----------------|
| Observation snapshot | inline in chat | yes |
| Dry-run plan | `.specify/docs/plans/` | when moves/archives are proposed |
| Audit log | `.specify/docs/audit/` | yes — even a no-op run records "all dimensions within tolerance" |
| Residual report | inline in chat | yes |

## Tool Support

Distributed like every other `/speckit.*` command to all supported AI tools (Claude Code, Codex CLI, Qoder CLI, opencode, Hermes Agent, GitHub Copilot) via the standard command-generation path.

## Related

- Engine contract: `.specify/specs/033-docs-command/contracts/docs-utils-cli.md`
- Reconcile pattern: `shared/patterns/reconcile-pattern.md` (mirrored at `.specify/shared/patterns/`)
- Docs-sync step convention: `shared/workflow/docs-step.md`
