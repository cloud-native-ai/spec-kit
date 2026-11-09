# Spec consolidation ledger — 2026-11-09

Owner: this file (dated record). Rollback = git history: every move below is revertible with
`git checkout <sha-before-this-commit> -- <path>` (or `git mv` back). Archive-not-delete is the house
discipline; nothing was hard-deleted despite the user's deletion authorization, because every reviewer
verdict for these entries was archive/merge.

| Entry (spec dir) | Verdict | Reference target | Notes |
|---|---|---|---|
| 003-speckit-agents-command | archive | Feature 019 (spec dir bound by reference, not by its prefix) | numbering-collision entry; see review-G1 |
| 007-skill-install-layout | archive | Feature 013 child (historical) | review-G2 |
| 008-create-skills-skill | archive | Feature 013 child (historical) | review-G2 |
| 017-consolidate-draft-skills | archive | Feature 013 child (historical; complete 50/50) | review-G2 |
| 022-eei-agent-triad | archive | Feature 019 child (retired EEI vocabulary) | review-G2 |
| 046-browser-site-memory | archive | Feature 048 (row already `Relocated`) | review-G4 |
| 066-loop-state-awareness-a | archive | superseded by 065a (banner-archived 2026-10-22) | review-G6 |
| 092-non-disposable | merge | absorbed into 090-re-anchoring (merge note § W3) | review-G3/G8 |
| 069a-flow-classification-docs-gates | merge | 069 (decomposition-gate slice) | review-G7 |
| 069b-isomorphism-migration-metrics | merge | 069 (decomposition-gate slice) | review-G7 |

Deferred: `085-sdd-temporary-goal-team` — archive gated on 094 closing (review-G3).
Not executed: any hard delete; any entry the reviewers marked keep.
| 054-agent-registration-wiring | merge | 040-agent-metadata-portability (Feature 044 child) | review-G2 |
