---
id: "20260726T075125Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-code-review-20260726"
scope: "local"
feature: "code-review"
partial: false
created: "2026-07-26T07:51:25Z"
summary: "Rebuilt skills/code-review from a frontmatter-less design document into a contract-style SpecKit skill centered on git-delta: proper SKILL.md (frontmatter, 4-phase workflow skeleton, strict requiremen"
---

## Review
Rebuilt skills/code-review from a frontmatter-less design document into a contract-style SpecKit skill centered on git-delta: proper SKILL.md (frontmatter, 4-phase workflow skeleton, strict requirements, canonical Feedback), extracted deterministic logic into scripts/git-delta-review.sh (fixed set -e arithmetic-increment kills, grep -c double-output, unquoted focus, EOF-abort on read; aligned severity to 6-level blocking..praise taxonomy; added tests-first ordering, size guard, report --summary merge gate; removed serve subcommand that violated the bash-only constraint), and moved methodology/setup detail into references/. Runtime-validated end-to-end in a scratch repo with a delta stub; mirrored to .specify/skills byte-identically.

## Optimization Points
- Pre-edit, check target skill directory ownership/permissions: this run hit a root-owned skills/code-review dir (container-created) that blocked all writes; the workaround (mv aside + recreate) works but leaves root-owned litter requiring sudo cleanup. A permission preflight step in the identify-target phase would surface this earlier.
