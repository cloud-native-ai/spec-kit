# Reader restatement — Anchor / anchoring archive / Re-Anchoring / action-level Goal (T074)

- date: 2026-11-12
- basis: `.specify/glossary.md` (rows 36–44) as the vocabulary anchor, judged against the two
  owner documents: `shared/definitions/anchor-definitions.md` (Anchor family) and
  `shared/definitions/goal-definitions.md` (action-level Goal); Re-Anchoring is judged against
  its own source `shared/definitions/re-anchoring-definitions.md` as the glossary row directs.

Each entry restates, without reading ahead, **what the object is** and **which directory it
lives in**. The judgement column records whether the restatement agrees with both the glossary
row and the owner; a disagreement would fail the term, and the record would stand rather than be
edited into agreement.

| # | Term | Restatement (object) | Restatement (directory) | Basis lines | Verdict |
|---|------|----------------------|--------------------------|-------------|---------|
| 1 | **Anchor** | A project-level, long-horizon, cross-deliverable *authored* end state — narrative + verifiable criteria + lifecycle state; the top of the control hierarchy; a different plane from Requirement and a different concept from an action-level Goal. | `.specify/anchoring/<anchor-slug>/anchor.md`; the retired file name in this store was `goal.md` and a current store entry still carrying it is a defect. | glossary:36; anchor-definitions:101, 235, 243 | agrees |
| 2 | **anchoring archive** | Not an entity but the **directory**: the materialized "current & historical anchoring list"; terminal (`achieved`/`abandoned`) entries stay, never deleted. | The whole `.specify/anchoring/` tree; definitions are `anchor.md` inside each slug directory, and `summary/` under it is derived. | glossary:37; anchor-definitions:203, 223, 248 | agrees |
| 3 | **Re-Anchoring** | An in-run discipline: after each core step the agent re-reads the direction anchor and the rules in force, recording `on-track` / `correction-applied` / `decision-needed`. It is **not** an Anchor, **not** a directory, and defines no entity; the bare word "anchoring" must not be read as an action-level Goal. | No directory of its own. Its three edges to the `.specify/anchoring/<slug>/` archive (write timing, lifecycle criterion, read surface) are owned by its own document; the entity definition is by reference to `anchor-definitions.md`. | glossary:44; re-anchoring-definitions:83 | agrees |
| 4 | **action-level Goal** | Short-horizon, executable guidance + completion conditions; **not** a project-level end state and **not** a control-hierarchy member; the bare word "goal" always reads as this concept, never as an Anchor. | `.specify/goals/<goal-slug>/goal.md` — a store separate from the Anchor archive; a slug that exists only there must not resolve as an Anchor and no team may bind it. | glossary:42; goal-definitions:6, 32, 39, 87 | agrees |

## Sense checks performed

- "Goal is a project-level end state" — the retired sentence — is contradicted by rows 1 and 4
  above. It appears nowhere in the glossary or the two owners after the inversion.
- Directory separation is absolute in the owner text: `.specify/anchoring/` resolves Anchors
  only, `.specify/goals/` resolves action-level Goals only, and the engine refuses the same slug
  in both stores (`goal-definitions.md` line 39).
- "Anchoring archive" is the *directory*, "Anchor" is the *entity* — the two are distinct rows
  (2 vs 1) and the glossary explicitly marks the archive as "not the entity; not the
  Re-Anchoring discipline" (line 223 of the owner).

## Boundary note (outside this reading's subject)

One live comparison row elsewhere — `shared/definitions/derivation-definitions.md:414` and its
`.specify/shared/` mirror — still reads `| **Goal** | Project-level authored end state … |`, the
retired sense. That file is not one of this restatement's two owners, and it is reported
separately (G-6 residue class C1, see `residue-scan-2026-11-12.txt`); this record neither
rewrites the row nor treats the glossary/owner agreement above as approval of it.
