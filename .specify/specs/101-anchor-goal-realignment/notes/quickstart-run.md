# Quickstart run — feature 101, S-0 … S-8 (T076)

**Date**: 2026-11-12 · **Tree**: working tree on top of `570622221` (WP-04 complete), feature 101 implement stage.
**Engine**: `python3 .specify/scripts/python/goal-utils.py` (flags after the action — subparser precedence).
**Test runs**: `bash scripts/bash/run-tests.sh` only.

Two kinds of readings are kept apart below, as T076 requires:

- **LIVE** — read against the real `.specify/` stores of this repository.
- **SCRATCH** — a drill inside `.specify/.tmp/wp05/qs` (a copy of the live `anchoring/` tree plus an empty
  `goals/` and `teams/`, engine invoked with `--repo-root .`); the drill never writes the live stores.

Step states: `pass` = reading matches the quickstart's Expected; `deviates` = reading differs and the fact is
recorded (not repaired); `not-run` = reason stated.

---

## S-0 — Baseline orientation — LIVE, **deviates** (quickstart text is stale)

The quickstart's own commands and their actual output:

| Command (as written) | Actual |
|---|---|
| `goal-utils.py --scope goal list --json` | **exit 2** — argparse usage error, `invalid choice: 'goal'`, valid set `{anchor,teams,goals,auto}` |
| `goal-utils.py --scope anchor list --json` | exit 0, `goals` key with **10** entries |
| `ls .specify/teams/*/team.md \| wc -l` | **20** |
| `grep -l '^goal_slug:' .specify/teams/*/team.md \| wc -l` | **0** |
| `grep -l '^anchor_slug:' .specify/teams/*/team.md \| wc -l` | **10** |
| `ls -d .specify/goals/*/ \| wc -l` (added reading) | **3** (`088-speckit-visualization`, `091-auto-git-closeout`, `draw-diagram-interactive`) |

**Disposition**: the plan-time Expected ("14 anchor definitions, 16 of 20 teams carry `goal_slug`") describes
the *pre-convergence* tree, and the plan-time claim that `list` ignores `--scope` no longer holds — the scope
set is the closed four members and `goal` is not one of them. Both differences are the convergence itself,
not a defect. The count of 20 teams and the binding frontmatter are read directly, as the quickstart
instructs. **Finding (not repaired here)**: the S-0 text is plan-time and stale; its owner is the quickstart
document. Recorded for FR-071.

## S-1 — Authoring an Anchor — SCRATCH, pass

- `create demo-quickstart-anchor --objective "<outcome phrasing>" --criterion …` → **rc 0**; the directory
  holds `anchor.md` and no `goal.md`.
- A step-shaped objective (`"先做 A，再做 B"`) → **rc 2** with a `GD-2 violation` refusal; no directory
  written.
- The chat-surface half (`/speckit.anchor create`) is covered by `tests/contract/test_anchor_command_surface.py`
  (seven modes, four per-tool copies, owner-cited scope), not re-executed here.

## S-2 — Anchor view, lifecycle, Targets — SCRATCH, pass with one ordering note

- `--scope anchor status <anchor> --set achieved --json` → **rc 0** (terminal `achieved`).
- `--scope anchor targets <anchor> --check "<statement>"` after the anchor is terminal → **rc 4**
  `goal-terminal`; the message reads "终态 goal 只读" (the wording still says *goal*, not *anchor* —
  disclosed observation, not asserted).
- `--scope anchor targets <anchor> --list --json` → **rc 0**, `{"targets": []}`.
- Ordering note: the target check must run **before** the terminal transition; the quickstart's ordering
  (lifecycle first) therefore yields the terminal refusal. Both behaviours are intended; only the order is
  worth knowing.

## S-3 — Action-level Goal — SCRATCH, pass

- `--scope goals goal-create demo-quickstart-goal --guidance … --done … --title …` → **rc 0**;
  `.specify/goals/demo-quickstart-goal/goal.md` exists, `status: active`, anchor store byte-unchanged.
- `--scope goals goal-list --json` → **rc 0** (1 goal, `done_count: 1`).
- `--scope goals goal-status demo-quickstart-goal --json` → **rc 0**, `"changed": false` (report only).

## S-4 — Four-mode Goal command and its named rejection — LIVE, pass

| Mode | `--command goal` | `--command anchor` |
|---|---|---|
| `create` | rc 0 | rc 0 |
| `view` | rc 0 | rc 0 |
| `modify` | rc 0 | rc 0 |
| `status` | rc 0 | rc 0 |
| `targets` | **rc 2** | rc 0 |
| `migrate` | **rc 2** | rc 0 |
| `migrate-archive` | **rc 2** | rc 0 |
| `coordinate` | **rc 2** | rc 0 |

Every rc-2 line carries the literal `anchor-only-mode` and the sentence
`… is an Anchor-only mode — it is declared by /speckit.anchor and not by /speckit.goal; invoke
/speckit.anchor instead. Nothing is written and the call never falls back to a read view.`
Zero writes on the refusal path. Pinned by `tests/contract/test_command_family_101.py` (G-10, T072).

## S-5 — Cleanup: check → apply → re-apply — LIVE check, SCRATCH apply

**LIVE `cleanup --check`** (read-only; full JSON saved):
`goal-utils.py cleanup --check --classification .specify/specs/101-anchor-goal-realignment/classification.json --json`
→ **rc 0**, `mode: check`, **14** decisions, all `noop`:
`anchor / already-normalized` ×9, `action-goal / already-migrated` ×3, `obsolete / already-archived` ×2 —
exactly the 9 / 3 / 2 shape the quickstart expects, plus the team dispositions block in the same payload.
Evidence: `test-evidence/cleanup-check-wp05-2026-11-12.json`.

**Apply / re-apply limbs** were exercised on the scratch fixture, not against the live stores (this package
must not write live state; the live tree is already converged from the WP-03/WP-04 runs):

- first apply → rc 0, one receipt per acted entry, retained anchors additionally get
  `anchor-body-receipt.json`;
- second apply → rc 0, every entry `already-*`, **byte-identical tree** and no new receipt (SC-007),
  asserted by `tests/contract/test_cleanup_idempotency.py` (G-7a, T068) with three injection cases
  (duplicate receipt, injected concept drift, dropped target) still going red;
- interruption (`GOAL_UTILS_CLEANUP_FAULT_AFTER=write-target|write-receipt`) → rc 3 interrupted payload,
  resume reports `resume-receipt/write-receipt` then `resume-remove/remove-source`, and a receipt-less
  target is I5 half-state rc 4 (`C-41 I5`), never silently repaired — `tests/contract/test_cleanup_resume.py`
  (G-7b, T069).

## S-6 — Post-convergence invariants — LIVE, pass on definition surfaces / raw grep deviates

| Reading | Result |
|---|---|
| `ls .specify/anchoring/*/goal.md` | **0** |
| `grep -rn '^# Goal:' .specify/anchoring` | **0** |
| `grep -l '^goal_slug:' .specify/teams/*/team.md` | **0** (all 10 bound teams carry `^anchor_slug:`) |
| `--scope anchor binding goal 086-efficient-test-execution --json` | rc 0 — `anchor.md`, `owner: human`, binding record present |
| `--scope anchor binding team demo-seat-dispatch --json` | rc 0 — `lifecycle: archived`, no binding line; provenance lives in its `disposition-receipt.json` |
| raw `grep -rn goal_slug` over the six roots (quickstart's own command) | **106 line-hits**, all attributable (below) |

Raw-hit attribution (the quickstart's own note says C6 is measured by the declared S-8 scan, not this grep):

- `teams/*/runs/**` — dated run records quoting the retired pointer (excluded by the declared scan);
- `binding-rename-receipt.json` / `disposition-receipt.json` `before` audit fields — audit trail on purpose;
- `.specify/anchoring/*/summary/data/project-input.yaml` — generated inputs inside delivered anchors;
- `skills/internal/create-team/scripts/{build-summary-input,verify-territory-disjoint}.py` — **explicit
  legacy tolerance** (`anchor_slug` wins, `goal_slug` tolerated), the intended compatibility read;
- `skills/internal/create-team/references/handoff-contract-template.md` — the `handoff/v1` contract key is
  named `goal_slug`; that key belongs to the handoff contract schema, whose owner is the `create-team` skill;
  it is **not** the team-binding key and no residue class C1–C7 covers it. Classification: schema key of
  another artifact, owner `skills/internal/create-team/`; recorded, not edited (outside WP-05 territory).

**Disposition**: definition surfaces are clean; the raw-grep deviation is bounded and classified above.

### `.specify/goal/**` in live team frontmatter — write prohibitions, classified not edited

12 live `team.md` files carry `.specify/goal/**` (some with the comment "authored:只经 /speckit.goal
引擎渲染") inside their `forbidden_paths` block — a **write prohibition**, not a binding and not a definition
reference. The closed residue classes do not cover this shape: C5's second pattern would match the pointer
but C5 is scoped to anchor definition files by the declaration, and C6 is the command-mode pointer pattern.
Classification therefore: *stale address inside a prohibition field of the team-definition schema*, owner =
the team-definition surface (`.specify/teams/`, written through the engine / team management, not through
this package). A natural successor fix would list `.specify/goals/**` and `.specify/anchoring/**` instead of
the retired singular root — recorded here, **not edited**, because team definitions are outside WP-05's
write territory and the dispatch forbids changing a team definition for this finding.

## S-7 — Protected history is untouched — LIVE, pass

`git diff --name-status d7c9da7a3 -- .specify/specs .specify/archive .specify/history docs/notes .specify/teams`
(plus the quickstart's narrower form) → **157 additions, 17 modifications, 0 deletions**:

- **M (17)**: 16 `.specify/teams/*/team.md` (binding rename — not a protected prefix; only `teams/*/runs/**`
  is protected) and `smoke-081.txt`, the single pre-existing deviation disclosed in T002's
  `protected-paths-entry.txt` § Reconstruction disclosure (present in every checkpoint since 01).
- **A (157)**: 121 this feature's own spec dir, 13 under `.specify/archive/anchoring/` (the new archival
  destination — the one permitted addition shape), 23 team receipts.
- `.specify/history/**` and `docs/notes/**`: **zero changes**.
- No baseline-existing path is modified or deleted. Pinned by `tests/integration/test_101_protected_paths.py`
  (G-8, T070), which reads `test-evidence/protected-paths-entry.txt` and goes red on any baseline change.

## S-8 — Residue scan (SC-001) — LIVE, **fails** (C1 2, C4 1)

`bash scripts/bash/run-tests.sh tests/contract/test_live_semantic_residue.py -q` →
`test_live_tree_has_no_old_semantic_residue` **FAILED**, listing exactly:

- **C1 (2)**: `shared/definitions/derivation-definitions.md` and its `.specify/shared/` mirror —
  `| **Goal** | Project-level authored end state, measured by degree — a different plane entirely |`
- **C4 (1)**: `.specify/memory/tools/build-summary-input.py.md:35` — stale `--out` default
  `.specify/goal/<goal-slug>/summary/data/project-input.yaml`

C2 / C3 / C5 / C6 / C7 read **0**; the injection case still turns the scan red. T067's "C1–C7 = 0" is
therefore **unmet**; both offenders sit outside WP-05's write territory and are reported as anomalies rather
than edited (see `test-evidence/residue-scan-2026-11-12.txt` and the package report). Pertinent evidence:
`test-evidence/implement-wp05-targeted-tests.txt`.
