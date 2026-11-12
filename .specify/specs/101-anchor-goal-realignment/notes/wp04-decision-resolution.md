# WP-04 decision resolution — cleanup residue and the SC-005 reading

## The anomaly (from WP-04 T048–T057, 2026-11-12; checkpoint 16)

The applied tree still carried retired tokens / dead paths the declared C-46 table could not
reach, while the feature's own guards (FR-047 / FR-058 / FR-066) require them gone. The package
halted with `ANOMALY:` before T058–T060; no definition was hand-edited.

| Class | Measured | Where | Why the mechanism could not reach it |
|-------|---------:|-------|--------------------------------------|
| A — retired key `goal_slug` | 2 lines | `draw-diagram-interactive/team.md:8`, `command-logic-as-classified-skills/team.md:72` | frontmatter prose; N-1 was body-scoped |
| B — reference to a definition file P1/P2 renamed or moved | 15 lines / 9 teams | frontmatter + body | N-2 matched only the retired-root form (`.specify/goal/<slug>/goal.md`), not the already-anchored form |
| C — frontmatter `delivery_dir` on the retired root | 5 values | 5 teams | N-3 is body-scoped; the frontmatter line is never read by the body mapper |
| SC-005 | 4 bound teams read `goal-terminal/true/5` | achieved anchors | their Anchors were already `achieved`; `run-checks` derives the verdict from the unchanged lifecycle |

## Ruling (driver, 2026-11-12; checkpoint 16)

1. Extend C-46 with **N-8** (frontmatter `goal_slug` → `anchor_slug`), **N-9** (definition-file
   references in both the retired-root and the already-anchored forms → the definition's new path)
   and **N-10** (`delivery_dir` → the new summary root); implement in `goal-utils.py`; re-run
   `cleanup --check` → `--apply`; the three counts reach 0 with per-line receipts; no hand edit;
   archive-not-delete.
2. Correct SC-005's reading: non-terminal bound teams `ok/false/0`; bound teams whose Anchor is
   already `achieved` read `goal-terminal/true/5` (the four measured teams) — a correct reading,
   not a binding defect. The lifecycle itself is not changed.
3. Complete T058–T060 and commit the cleanup.

## `PLAN-EDIT: SC-005`

- **Before** — every still-bound team must read `verdict: ok`, `blocked: false`, exit 0.
- **After** — the reading follows the bound Anchor's lifecycle: non-terminal → `ok/false/0`
  (②–④ `not-evaluated` without `--target`); `achieved` → `goal-terminal/true/5`, recorded as the
  correct terminal reading for a team still bound to an achieved Anchor (measured: `087-arch-diagram-docs`,
  `draw-two-layer-structure`, `session-driven-self-improvement`, `skill-layer-install-separation`).
  R3-archived and unbound teams stay `no-goal-definition/false/0`.
- **Why a correction, not a new decision** — `run-checks` derives `goal-terminal` from
  `TERMINAL_STATES` in the Anchor definition, whose lifecycle this feature does not touch
  (FR-038 renames and normalizes; it never edits `status`). Demanding `ok` from those teams would
  force a rebind or a resurrection of an achieved Anchor, which is a decision the requirements do
  not authorize and the lifecycle owner forbids.
- **Downstream** — `tasks.md` T059's parenthetical and the SC trace row (`SC-005 … 绑定团队
  ok/false`) still carry the pre-correction reading. `tasks.md` is outside WP-04b's write
  territory, so this note records the drift for the review stage; the corrected authority is
  `requirements.md` § SC-005.

## `PLAN-EDIT: C-46 normalization table (N-8…N-10)`

- **N-8** — `\bgoal_slug\b` → `anchor_slug` over the **whole definition** (frontmatter prose
  included). FR-047 / FR-066 forbid the retired key in frontmatter **and** body.
- **N-9** — a definition-file reference in either form (`.specify/goal/<slug>/goal.md`,
  `.specify/anchoring/<slug>/goal.md`) → the definition's post-cleanup path, class mapped exactly as
  N-2/N-3 map it: anchor class (and any unclassified slug under `.specify/anchoring/`) →
  `.specify/anchoring/<slug>/anchor.md`; action-goal → `.specify/goals/<slug>/goal.md`; obsolete →
  `.specify/archive/anchoring/<slug>/goal.md`. Implemented over the whole definition: apart from the
  15 measured anchored-form lines, it also reaches **4 frontmatter retired-root definition
  references** the WP-04 measurement did not enumerate (`command-logic-as-classified-skills:46,69`,
  `draw-two-layer-structure:33`, `session-driven-self-improvement:40`) — the same defect class, so
  closing only 15 would leave the class non-zero.
- **N-10** — frontmatter `delivery_dir` on `.specify/goal/<slug>/summary/` → the class-mapped
  summary root. Four of the five measured values land on `.specify/anchoring/<slug>/summary/`;
  `post-refactor-mechanism-integrity` is classified **obsolete** and its summary tree lives at
  `.specify/archive/anchoring/<slug>/summary/`, so the rule maps it there. Read literally ("the 5
  values → `.specify/anchoring/…`") the ruling's shorthand would write a dead path — the very defect
  this package closes — and would contradict N-3's declared class mapping and FR-049; the intent
  ("point at the definition's real location") is what was implemented. Class mapping is a
  one-reading correction, disclosed here.
- **Zones kept narrow** — in the frontmatter zone N-4/N-5 do **not** rewrite `.specify/goal/**`
  territory entries (a permission scope; repointing a dead root would change what a team may read
  or write), and N-6/N-7 do **not** rewrite a `/speckit.goal` pointer there: the frontmatter prose
  contains quoted dated user directives and handovers (`command-logic…:77`, `post-refactor…:39`)
  that a rewrite would falsify. The retired root therefore remains in **15 territory `**` entries**
  (9 teams) plus one frontmatter description line (`094-goal-team-parallel:9`, prose about the old
  parallel line); they are permission scopes / model prose, not definition references, and no FR
  requires them rewritten.
- **Receipt continuity** — `binding-rename-receipt.json` is the append-only record of every declared
  rewrite a team has received. A declared rule added later appends rows; an exact duplicate appends
  nothing; a reverted line is re-applied without duplicating the row. Prior rows keep their original
  line numbers (for R3 teams those numbers predate P7's binding-line removal), so the receipt is read
  as history, not as an index into the current file.

## What was not changed

- No Anchor/Goal lifecycle value was edited; no definition was hand-edited; the engine is the only
  writer of record.
- Dated records (`runs/**`, SPEC 037/038/042/074/085/094, dated spec dirs, `.specify/history/**`,
  `docs/notes/**`, pre-existing `.specify/archive/**`) were not touched.
- `smoke-081.txt` and `.specify/.specify/` were left as found.
- No push was performed.

## Readings (evidence)

- `test-evidence/cleanup-check-wp04b-2026-11-12.json` — pre-apply plan: 9 teams `normalize`, 25 lines.
- `test-evidence/cleanup-apply-wp04b-2026-11-12.json` — apply: `ok`; P8 four checks `ok`.
- `test-evidence/post-apply-residue-wp04b-2026-11-12.txt` — A 0 / B 0 / C 0.
- `test-evidence/cleanup-check-after-apply-wp04b-2026-11-12.json` — 16/16 `already-normalized`.
- `test-evidence/cleanup-apply-2-wp04b-2026-11-12.json` + store hash comparison — zero writes.
