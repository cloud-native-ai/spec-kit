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

## Static Site (Hugo)

The documentation space is publishable, not just readable in the repo: `docs/` doubles as a
**Hugo project root**, so a reconcile run also scaffolds and maintains `docs/hugo.toml`,
`docs/layouts/`, `docs/static/css/site.css`, and `docs/.gitignore` (build output).

```bash
SC=.specify/skills/create-docs/scripts/scaffold-hugo.py
python3 $SC --action check    --root .                     # drift only, no writes
python3 $SC --action scaffold --root . --site-title "<t>"   # create/repair the site layer
python3 $SC --action build    --root .                      # -> docs/public
cd docs && hugo server                                     # local preview
```

Key properties:

- **Mounted, never copied** — Markdown is mounted into Hugo via module mounts, so `docs/`
  stays pure Markdown, keeps its repo-native relative links, and `content/` never appears on
  disk. Directory indexes stay `index.md` (mounted as `_index.md`, so sibling pages remain
  pages), and relative `.md`/image links are resolved by render hooks at build time.
- **Minimal and offline** — layouts and a single stylesheet ship with the skill; no external
  theme, no network, no asset pipeline. Absent `hugo` binary → the scaffold is still complete
  and only the build step is skipped.
- **Never clobbers** — only the `# >>> speckit:mounts` block in `hugo.toml` is machine-owned;
  layouts or config you edit are reported `kept`. A repeat run writes nothing.
- **Publish scope** is all of `docs/` (six types + `notes/` + `archive/` + media).

CI integration is delivered as **guidance**, not a generated workflow: install Hugo extended,
run it with `docs/` as the working directory, publish `docs/public`. Copy-pasteable snippet and
troubleshooting live in `.specify/skills/create-docs/references/hugo-site.md`.

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
