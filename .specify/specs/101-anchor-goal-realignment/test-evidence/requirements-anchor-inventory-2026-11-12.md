# Requirements Evidence — Anchoring Inventory & Binding Readings (2026-11-12)

**Spec**: `.specify/specs/101-anchor-goal-realignment/`
**Baseline commit**: `d7c9da7a3`
**Measured**: 2026-11-12, working tree at `/storage/project/cloud-native-ai/spec-kit`
**Consumed by**: `requirements.md` § Provisional anchoring inventory, FR-047/FR-048, SC-003/SC-005

All readings below are direct command output, not estimates. Dated records
(`.specify/specs/037*`, `038*`, `042*`, `074*`, `085*`, `094*`, `.specify/archive/**`,
`.specify/history/**`) were not modified and are out of scope.

## 1. Anchoring archive inventory

Command:

```bash
for d in .specify/anchoring/*/; do s=$(basename "$d")
  g=$([ -f "$d/goal.md" ] && echo yes || echo no)
  sm=$([ -d "$d/summary" ] && echo yes || echo no)
  printf '%-40s goal.md=%s summary=%s\n' "$s" "$g" "$sm"; done
```

Result — 14 entries, every one carries `goal.md`:

| # | Slug | `goal.md` | `summary/` | Provisional class (A-5) |
|---|------|-----------|------------|--------------------------|
| 1 | `085-sdd-temporary-goal-team` | yes | no | obsolete |
| 2 | `086-efficient-test-execution` | yes | no | anchor |
| 3 | `087-arch-diagram-docs` | yes | no | anchor |
| 4 | `088-speckit-visualization` | yes | no | action-goal |
| 5 | `090-re-anchoring` | yes | no | anchor |
| 6 | `091-auto-git-closeout` | yes | no | action-goal |
| 7 | `094-goal-team-parallel` | yes | no | anchor |
| 8 | `command-logic-as-classified-skills` | yes | yes | anchor |
| 9 | `draw-diagram-interactive` | yes | yes | action-goal |
| 10 | `draw-two-layer-structure` | yes | no | anchor |
| 11 | `post-refactor-mechanism-integrity` | yes | yes | obsolete |
| 12 | `script-interface-contract` | yes | no | anchor |
| 13 | `session-driven-self-improvement` | yes | yes | anchor |
| 14 | `skill-layer-install-separation` | yes | yes | anchor |

Derived counts: 14 entries = 9 anchor + 3 action-goal + 2 obsolete; 5 `summary/`
trees (`command-logic-as-classified-skills`, `draw-diagram-interactive`,
`post-refactor-mechanism-integrity`, `session-driven-self-improvement`,
`skill-layer-install-separation`). No `.specify/anchoring/<slug>/goal.md` is absent,
so no entry is currently definition-less.

The classification column is the **provisional baseline** required by A-5; the final
call belongs to plan/implement and every deviation must record a rule id and evidence.

## 2. Team definitions and anchor bindings

Command family:

```bash
ls -d .specify/teams/*/ | wc -l                 # 20
grep -rn '^goal_slug:' .specify/teams/*/team.md # 16 bindings
for d in .specify/teams/*/; do s=$(basename "$d")
  grep -q '^goal_slug:' "$d/team.md" || echo "UNBOUND $s"; done
```

Readings:

- **20** team directories, each containing `team.md`.
- **16** teams carry a `goal_slug`; **4** carry none and instead hold an inline
  `goal:` narrative: `cws-workspace-cluster`, `draw-plantuml-optimizer`,
  `requirement-implement-monitor`, `summarize-project-optimizer`.
- **2** of the 16 bound slugs have no matching `.specify/anchoring/<slug>/` directory
  (dangling bindings):

| Team | `goal_slug` | Anchor exists? |
|------|-------------|----------------|
| `viz-skill-arena` | `visualization-skill-selection` | **no** |
| `demo-seat-dispatch` | `demo-seat-dispatch` | **no** |

All other 14 bindings resolve to an existing directory:

| Team | `goal_slug` |
|------|-------------|
| `085-sdd-temporary-goal-team` | `085-sdd-temporary-goal-team` |
| `086-efficient-test-execution` | `086-efficient-test-execution` |
| `087-arch-diagram-docs` | `087-arch-diagram-docs` |
| `088-reporting-dogfood` | `088-speckit-visualization` |
| `089-script-interface-contract` | `script-interface-contract` |
| `090-re-anchoring` | `090-re-anchoring` |
| `091-auto-git-closeout` | `091-auto-git-closeout` |
| `094-goal-team-parallel` | `094-goal-team-parallel` |
| `command-logic-as-classified-skills` | `command-logic-as-classified-skills` |
| `draw-diagram-interactive` | `draw-diagram-interactive` |
| `draw-two-layer-structure` | `draw-two-layer-structure` |
| `post-refactor-mechanism-integrity` | `post-refactor-mechanism-integrity` |
| `session-driven-self-improvement` | `session-driven-self-improvement` |
| `skill-layer-install-separation` | `skill-layer-install-separation` |

Notes for later stages:

- `088-reporting-dogfood` binds `088-speckit-visualization`, which the provisional
  class marks `action-goal`; its team is therefore an affected team under FR-046.
- `091-auto-git-closeout` is marked `action-goal` and its team directory is already
  archived; the disposition must cite that archived state.
- `viz-skill-arena` has an inline `goal:` narrative and a frontmatter binding at
  `team.md:15`; the dangling fact is the binding, not the body prose.
- `demo-seat-dispatch` is the SC-002 demonstration team for spec 054 and binds to
  itself; the target Anchor does not exist.

## 3. Stale live-surface citations of `.specify/goal/`

Command:

```bash
grep -rl '\.specify/goal/' skills/ scripts/ src/ templates/ .specify/shared/ .specify/glossary.md
```

Live hits (excluding `__pycache__` artifacts):

| Path | Kind |
|------|------|
| `skills/external/sdd-house-keeping/scripts/logical-framework.py` | code — checks `.specify/goal/` |
| `skills/external/sdd-project-setup/scripts/logical-framework.py` | code — same engine, mirrored copy |
| `skills/internal/create-team/references/create-mode.md` | reference doc |
| `skills/internal/create-team/references/execution-guide.md` | reference doc |
| `skills/internal/create-team/references/goal.md` | reference doc |
| `skills/internal/create-team/references/summary-mapping.md` | reference doc |
| `skills/internal/create-team/scripts/build-summary-input.py` | code — summary input path |
| `skills/internal/create-team/SKILL.md` | skill entry |
| `skills/internal/improve-team/references/goal-editing.md` | reference doc |
| `skills/internal/run-skills/SKILL.md` | skill entry |
| `.specify/glossary.md` | glossary |
| `.specify/shared/declarations/exclusions/no-harness-asset.yaml` | declaration |
| `.specify/shared/definitions/derivation-definitions.md` | definition |
| `.specify/shared/definitions/goal-definitions.md` | definition (the owner being rewritten) |
| `.specify/shared/guidelines/critique-and-self-critique.md` | guideline |
| `.specify/shared/guidelines/self-explanatory.md` | guideline |

`ls -d .specify/goal` → **does not exist**. Any live citation of `.specify/goal/`
therefore resolves to a missing path today. `logical-framework.py` in both the
`project-setup` and `house-keeping` skills checks `project / ".specify" / "goal"`;
this is the mechanism-drift signal FR-050/FR-056/FR-057 must converge.

## 4. Requirements structural validation

Command:

```bash
python3 scripts/python/validate-requirements.py \
  .specify/specs/101-anchor-goal-realignment/requirements.md
```

Result after the citation fixes:

```text
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] pass (0)
scanned: 338 lines, 81 definition rows, 8 shared strings
0 error(s), 0 warning(s)
```

The earlier failing run reported 19 `ref-resolvable` errors, all from two causes:
`[[STR-NNN]]` citations written inside inline code spans (erased by the validator's
code-span-stripped view) and two `Consumed by` cells naming FR-048 / FR-063 that did
not cite their string. Both were repaired in the requirements text; no validator
check was weakened.

## 5. Scope protections

- During requirements authoring this session wrote only under
  `.specify/specs/101-anchor-goal-realignment/`.
- `.specify/archive/goal-team/`, `.specify/history/`,
  `.specify/specs/037|038|042|074|085|094*` were not modified.
- `.specify/anchoring/` itself was only read; no entry was moved, renamed or deleted
  during requirements authoring.
- Byte-identity of these protected roots is a measured success criterion (SC-009) and
  must be re-read at implement time against baseline `d7c9da7a3`; this file does not
  substitute for that later reading.
