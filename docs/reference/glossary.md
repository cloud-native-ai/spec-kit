# Glossary Mechanism

**Feature 031.** A single project-wide glossary that anchors project vocabulary and corrects voice/dictated input (homophones, easily-confused words). It doubles as a lightweight domain-knowledge dictionary.

## What it is

- **One file per project**: `.specify/memory/glossary.md` — a human-readable Markdown table beside `constitution.md` and `features.md`.
- **Ambient**: referenced from the Documentation Map in `.specify/instructions.md`, so every `/speckit.*` command loads it as context (the same way the constitution is ambient).
- **Framework-native**: it is a documentation/prompt artifact, not a runtime service. Correction and conflict *judgment* are AI-agent behaviors; the `scripts/python/glossary-utils.py` engine only performs deterministic file operations and structural conflict detection.

## Entry shape

| Canonical | Variants | Meaning | Origin | Status |
|-----------|----------|---------|--------|--------|
| Spec Kit | speckit, spec-kit, speck it | The SDD CLI toolkit (specify-cli) | user | confirmed |

- **Canonical**: the agreed term (unique). **Variants**: homophone/confusable forms that anchor to it. **Meaning**: one-line domain definition.
- **Origin**: `auto` (proposed by the framework) or `user` (authored/confirmed manually). **Status**: `proposed` or `confirmed`.

## Lifecycle

1. **Initialize** — `/speckit.instructions` creates the glossary from `templates/glossary-template.md` if absent (non-destructive) and seeds observed domain terms, excluding common words.
2. **Correct & anchor** — any command maps recorded variants → canonical when interpreting input (primarily fixing voice dictation), surfacing each correction; ambiguous variants are deferred to the user.
3. **Enrich** — at workflow checkpoints, new project-specific terms are proposed.
4. **Resolve conflicts** — same-term/different-meaning or homophone/near-duplicate clashes are surfaced and require explicit user confirmation before writing.
5. **User precedence** — manual edits are authoritative, preserved across regenerations, and never silently overwritten.

The full protocol lives in `.specify/shared/workflow/glossary.md`.

## Engine

`python3 .specify/scripts/python/glossary-utils.py --action <init|list|validate|detect-conflict|add|remove> [options]` — stdlib-only, JSON output. `add` refuses a conflicting or user-overriding write unless `--confirmed-resolution` is supplied.
