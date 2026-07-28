# Notes — 临时文档区

> ⚠️ No stability guarantee. Content here may be deleted, moved, or rewritten at any time. Formal knowledge lives in the typed directories.

## Rules

1. Every note MUST carry frontmatter (template below); `expires` is required (default: created + 60 days).
2. Overdue notes are marked `expired` by the engine and must be resolved: merge into the `target` formal doc (→ `archived`), renew (`expires` extended, back to `draft`), or delete after human confirmation (notes zone only).
3. `archived` notes keep a destination annotation and may be removed later once the target is stable.

## Frontmatter template

```yaml
---
title: "<one-line title>"
created: YYYY-MM-DD
expires: YYYY-MM-DD
status: draft
target: ""
tags: []
---
```

## Lifecycle automation

```bash
python3 scripts/python/docs-utils.py --action scan --root .
python3 scripts/python/docs-utils.py --action expire --root .
python3 scripts/python/docs-utils.py --action clean [--yes] --root .
python3 scripts/python/docs-utils.py --action archive-check --root .
python3 scripts/python/docs-utils.py --action stats --root .
```

## What belongs here / not

- ✅ research notes, option comparisons, meeting takeaways, immature design ideas, debugging findings.
- ❌ user-facing guides (→ `tasks/`/`tutorials/`), stable architecture (→ `concepts/`), decisions (→ `decisions/` as ADR).
