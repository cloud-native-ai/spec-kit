# Quickstart: Project Glossary Mechanism

**Feature**: 031 Glossary Mechanism | **Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

This walks through the glossary lifecycle end-to-end. Each step maps to a user story and its acceptance scenarios.

## 1. Initialize the glossary (User Story 1)

Run instruction generation on a project:

```bash
# via the /speckit.instructions command (chat), or the underlying script:
scripts/bash/generate-instructions.sh
```

Expected:
- `.specify/memory/glossary.md` now exists (created from `templates/glossary-template.md` if it was absent).
- It contains the title, authoring-rule preamble, and a `| Canonical | Variants | Meaning | Origin | Status |` table.
- Observed project-specific terms (e.g. `Spec Kit`, `constitution`, feature names) appear as `auto` / `proposed`; common words do not.
- The generated `.specify/instructions.md` (and its symlinks `CLAUDE.md`, `QWEN.md`, …) list a **Glossary** row in the Documentation Map → the glossary is now ambient for every agent.

Verify:
```bash
python3 scripts/python/glossary-utils.py --action validate
python3 scripts/python/glossary-utils.py --action list
```

## 2. Correct voice/dictated input (User Story 2)

With an entry like `Canonical=Spec Kit | Variants=speckit,spec-kit`, dictate a request that a speech-to-text layer garbled to a variant, e.g. "update the *spec kit* readme" arriving as "update the *speck it* readme".

Expected:
- Any `/speckit.*` command interprets it as the canonical `Spec Kit`.
- The agent surfaces the correction (traceable) so you can override it.
- If the garbled word could map to two canonical terms, the agent asks instead of guessing.

## 3. Progressive enrichment with conflict prompt (User Story 3)

During `/speckit.plan` (or another checkpoint), a new term `glossary` emerges. Suppose the glossary already has `Canonical=Glossary` meaning something different, or a homophone.

Expected:
- The agent proposes the new term.
- Because it collides, the agent presents the conflict (candidate + colliding entry + kind) and asks you to resolve (`keep-existing` / `replace` / `merge-variant` / `add-distinct` / `defer`).
- Nothing is written until you confirm.

Simulate the detection:
```bash
python3 scripts/python/glossary-utils.py --action detect-conflict --canonical "Glossary" --variants "glosary"
# → {"conflict": true, "kind": "...", "collidesWith": ["Glossary"]}
```

## 4. Manual edit with user precedence (User Story 4)

Open `.specify/memory/glossary.md` and edit a row directly (set `Origin=user`), then re-run instruction generation.

Expected:
- Your edited row is preserved byte-for-byte (non-destructive re-init).
- A later `auto` proposal for the same term does NOT overwrite your value without explicit confirmation.

## Acceptance mapping

| Step | User Story | Key FRs | Success Criteria |
|------|-----------|---------|------------------|
| 1 | US1 | FR-001, FR-002, FR-003, FR-013, FR-015 | SC-001, SC-005 |
| 2 | US2 | FR-005, FR-006, FR-007 | SC-002 |
| 3 | US3 | FR-004, FR-008, FR-009 | SC-003 |
| 4 | US4 | FR-010, FR-011, FR-012, FR-014 | SC-004 |
