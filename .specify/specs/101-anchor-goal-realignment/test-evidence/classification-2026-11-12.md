# T048 — Classification record realized as implement-time evidence (2026-11-12)

Authority: `classification.json` (`schema: 101-classification/v1`, `mapping_version: 101-mapping-v1`,
`baseline_commit: d7c9da7a3`), read verbatim; FR-035/FR-036/FR-037.
Comparison baseline: `requirements.md` § Provisional anchoring inventory (14 rows, A-5).

Method: for every directory under `.specify/anchoring/*/`, read `goal.md`'s frontmatter `status`
and count the `## Targets` table rows (`| T-NNN | …`), and detect `summary/` presence; then compare
each row against `classification.json` (`class`, `rule`, `targets`, `summary`) and against the
requirements provisional class. The classification file carries no `status` field; lifecycle is read
from the live definition (LOW-4 reading of T048).

Date: 2026-11-12. Reproduce: the reading command is recorded in
`test-evidence/classification-reading-2026-11-12.txt`.

## Per-entry readings

| # | slug | live status | Targets (live) | summary/ | class (json) | rule | Targets (json) | summary (json) | provisional (req) | deviation |
|---|------|-------------|----------------|----------|--------------|------|----------------|----------------|-------------------|-----------|
| 1 | `085-sdd-temporary-goal-team` | active | 0 | no | obsolete | FR-036(b) | 0 | false | obsolete | none |
| 2 | `086-efficient-test-execution` | active | 0 | no | anchor | FR-036(c) | 0 | false | anchor | none |
| 3 | `087-arch-diagram-docs` | achieved | 0 | no | anchor | FR-036(c) | 0 | false | anchor | none |
| 4 | `088-speckit-visualization` | active | 2 | no | action-goal | FR-036(a) | 2 | false | action-goal | none |
| 5 | `090-re-anchoring` | active | 0 | no | anchor | FR-036(c) | 0 | false | anchor | none |
| 6 | `091-auto-git-closeout` | active | 0 | no | action-goal | FR-036(a) | 0 | false | action-goal | none |
| 7 | `094-goal-team-parallel` | active | 0 | no | anchor | FR-036(c) | 0 | false | anchor | none |
| 8 | `command-logic-as-classified-skills` | active | 3 | yes | anchor | FR-036(c) | 3 | true | anchor | none |
| 9 | `draw-diagram-interactive` | active | 0 | yes | action-goal | FR-036(a) | 0 | true | action-goal | none |
| 10 | `draw-two-layer-structure` | achieved | 3 | no | anchor | FR-036(c) | 3 | false | anchor | none |
| 11 | `post-refactor-mechanism-integrity` | achieved | 1 | yes | obsolete | FR-036(b) | 1 | true | obsolete | none |
| 12 | `script-interface-contract` | active | 0 | no | anchor | FR-036(c) | 0 | false | anchor | none |
| 13 | `session-driven-self-improvement` | achieved | 0 | yes | anchor | FR-036(c) | 0 | true | anchor | none |
| 14 | `skill-layer-install-separation` | achieved | 4 | yes | anchor | FR-036(c) | 4 | true | anchor | none |

## Derived counts

- Classes: **9 anchor / 3 action-goal / 2 obsolete** — equals `classification.json` and
  `research.md` §3.
- Summary trees: **5** — `command-logic-as-classified-skills` (anchor, stays/regenerate),
  `draw-diagram-interactive` (action-goal, moves), `post-refactor-mechanism-integrity` (obsolete,
  archives with tree), `session-driven-self-improvement` (anchor, stays/regenerate),
  `skill-layer-install-separation` (anchor, stays/regenerate).
- Targets ledger: 2 (088) + 3 (command-logic) + 3 (draw-two-layer) + 1 (post-refactor) +
  4 (skill-layer) = 13 statements, all matching the classification counts.

## Deviation from the provisional baseline (FR-037)

**None.** Every one of the 14 entries keeps the class recorded in `requirements.md` § Provisional
anchoring inventory; no rule id + evidence record is owed for a deviation, and no silent re-class
occurred. Lifecycle `status` is a definition-level fact (five `achieved` entries: 087,
draw-two-layer, post-refactor, session-driven, skill-layer) and does not alter any class.

## Cross-check against the disk enumeration

- 14 entry directories counted at run time, matching `classification.json`'s 14 `entries`.
- 7 team dispositions in `classification.json` (6 × R3 + 1 × R2) — realized in T049/T057 readings.
- Engine verdict `decision=pass` is captured in the `--check` reading (T049).
