# Phase 0 Research — Anchor / Goal Realignment

**Spec**: `.specify/specs/101-anchor-goal-realignment/` | **Measured**: 2026-11-12
**Baseline for protected-path comparison**: `d7c9da7a3` (feature-before commit) | **Plan-stage HEAD**: `d3f85f059`
**Evidence**: `test-evidence/requirements-anchor-inventory-2026-11-12.md`,
`test-evidence/plan-baseline-2026-11-12.txt`, `test-evidence/live-semantic-scan-baseline-2026-11-12.txt`

This file owns three things the rest of the plan consumes: the **final classification record**
(FR-035/FR-037), the **team disposition basis** (FR-046/FR-048), and the **live-surface roots
declaration** (SC-001 Source). Everything else is referenced by path.

## 1. Environment and baseline readings

All values below are direct command output captured in `test-evidence/plan-baseline-2026-11-12.txt`.

| Reading | Value | Command |
|---------|-------|---------|
| Interpreter | `Python 3.11.11` | `python3 --version` |
| Test runner | `pytest 8.4.2` | `python3 -m pytest --version` |
| git | `2.43.5` | `git --version` |
| Engine identity | `goal-utils.py 0.0.22`, `--help` exit 0 | `python3 scripts/python/goal-utils.py --version` |
| Mirror drift (pre-edit) | `sync-mirrors.py --check` exit 0 | recorded in the baseline file |
| Command-copy drift (pre-edit) | `regen-command-copies.py --check` exit 0 | recorded in the baseline file |
| Flow-class ledger | 89 units, 0 findings, floor 39, `--action check` exit 0 | `flow-class-check.py --action check` |
| Flow class of this line | `flow_class: execution` (declaration) | `flow-class-check.py --action lookup --unit-id spec:101-anchor-goal-realignment` |
| Docs build | `hugo --source docs --destination /tmp/hugo-101-probe` exit **1** (zero output with `--quiet`; non-quiet run reports `.Site.Language.Locale: can't evaluate field Locale in type *langs.Language`) | `hugo version` → `v0.141.0+extended` |
| Working tree at plan entry | 1 pre-existing modification outside this feature (`.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`) | `git status --porcelain` |

Two consequences are carried as premises, not prose: the pre-edit mirror checks are **clean**, so
the implement criterion is "no NEW drift"; the docs build is **broken before this feature**, so no
convergence task may be scored against it (see `plan.md` EP-006 / Decision `fallback`).

## 2. Inventory readings

`.specify/anchoring/` holds **14** entries, each with `goal.md`, **5** with a `summary/` tree.
`.specify/teams/` holds **20** team definitions: **16** carry `goal_slug`, **4** carry an inline
`goal:` only (`cws-workspace-cluster`, `draw-plantuml-optimizer`, `requirement-implement-monitor`,
`summarize-project-optimizer`), and **2** of the 16 bind a slug with no directory
(`viz-skill-arena` → `visualization-skill-selection`; `demo-seat-dispatch` → itself).
Full readings: `test-evidence/requirements-anchor-inventory-2026-11-12.md` § 1–§ 3.

## 3. Final classification (authoritative record)

Rules are cited from `requirements.md` FR-036 — this table names the clause, it does not restate
the rule text. `Targets` is the count of `## Targets` rows read from the definition on 2026-11-12.

| # | Slug | Status | Targets | Class | Rule | Evidence (measured) |
|---|------|--------|---------|-------|------|---------------------|
| 1 | `085-sdd-temporary-goal-team` | active | 0 | obsolete | FR-036(b) | The temporary-goal/team model this entry describes was replaced by the unified-archive model (094); the entry is bound to a spec-scoped team of a delivered feature. |
| 2 | `086-efficient-test-execution` | active | 0 | anchor | FR-036(c) | Project-wide quality attribute (test cost), no single deliverable, no terminal event. |
| 3 | `087-arch-diagram-docs` | achieved | 0 | anchor | FR-036(c) | Architecture-documentation theme is continuous; `achieved` is lifecycle, not obsolescence (FR-025 keeps terminal entries). |
| 4 | `088-speckit-visualization` | active | 2 | action-goal | FR-036(a) | Single capability delivery (088 visualization/reporting) with 2 open Targets; Targets preserved per FR-040. |
| 5 | `090-re-anchoring` | active | 0 | anchor | FR-036(c) | A run-wide discipline that applies to every future run; no bounded completion. |
| 6 | `091-auto-git-closeout` | active | 0 | action-goal | FR-036(a) | Single mechanism delivery; its team is already `lifecycle_state: archived`. |
| 7 | `094-goal-team-parallel` | active | 0 | anchor | FR-036(c) | Defines the durable binding model behind goal/team (now Anchor/Team); ongoing reference for every team run. |
| 8 | `command-logic-as-classified-skills` | active | 3 | anchor | FR-036(c) | Framework-wide structural direction; 3 open Targets are slices of one continuous theme. |
| 9 | `draw-diagram-interactive` | active | 0 | action-goal | FR-036(a) | Single capability deliverable (interactive charts); its team runs a bounded iteration (`max_iterations: 5`). |
| 10 | `draw-two-layer-structure` | achieved | 3 | anchor | FR-036(c) | Two-layer drawing architecture is a standing structural invariant; `achieved` lifecycle retained. |
| 11 | `post-refactor-mechanism-integrity` | achieved | 1 | obsolete | FR-036(b) | Records a completed one-off verification of the post-refactor mechanism inventory. |
| 12 | `script-interface-contract` | active | 0 | anchor | FR-036(c) | A contract binding every functional script; continuous by definition. |
| 13 | `session-driven-self-improvement` | achieved | 0 | anchor | FR-036(c) | The improvement loop remains the framework's north star; `achieved` denotes the bootstrap phase only. |
| 14 | `skill-layer-install-separation` | achieved | 4 | anchor | FR-036(c) | Install/package separation is a standing structural boundary; 4 Targets are slices, all closed. |

**Deviation from the A-5 provisional baseline: none.** All 14 entries keep the class recorded in
`requirements.md` § Provisional anchoring inventory. Derived counts: **9 anchor / 3 action-goal /
2 obsolete**; the 5 `summary/` trees belong to `command-logic-as-classified-skills`,
`draw-diagram-interactive`, `post-refactor-mechanism-integrity`,
`session-driven-self-improvement`, `skill-layer-install-separation` — of which 3 stay, 2 are
disposed (FR-049).

**Targets ledger** (FR-040): entries 4, 8, 10, 14 keep their Targets by staying/being anchors;
entry 4 (`088-speckit-visualization`, 2 Targets) is the only *migrated* definition carrying
Targets and its statements MUST be preserved verbatim in the migrated body plus the receipt;
entry 11 (`post-refactor-mechanism-integrity`, 1 Target) archives and its statement is recorded in
the archive receipt.

## 4. Team dispositions (FR-046 / FR-048)

Affected = a team bound to an entry classified `action-goal` or `obsolete`, plus the two dangling
bindings. Every disposition carries its own receipt in the team directory
(`disposition-receipt.json`), referenced by SC-005.

| Team | Bound slug | Disposition | Evidence |
|------|-----------|-------------|----------|
| `088-reporting-dogfood` | `088-speckit-visualization` (action-goal) | **R3** archive team | Purpose is a one-off dogfood proof (`scope: spec`, single >90 s reporting run); no existing Anchor covers "progress reporting"; no continuous-by-degree theme to promote. |
| `091-auto-git-closeout` | `091-auto-git-closeout` (action-goal) | **R3** archive team (apply) | `team.md` carries `lifecycle_state: archived`, but the binding line is still present; apply removes it and writes a `disposition-receipt.json` in the team directory per C-47. |
| `085-sdd-temporary-goal-team` | `085-sdd-temporary-goal-team` (obsolete) | **R3** archive team | Spec-scoped SDD team of a delivered feature; the model it was built for is superseded. |
| `post-refactor-mechanism-integrity` | `post-refactor-mechanism-integrity` (obsolete) | **R3** archive team | Three-stage verification chain keyed to the achieved one-off entry; terminal by construction. |
| `draw-diagram-interactive` | `draw-diagram-interactive` (action-goal) | **R3** archive team | Bounded iteration (`max_iterations: 5`, threshold 0.8) over one skill; no existing Anchor covers it and the theme does not pass the `anchor` criterion. |
| `viz-skill-arena` *(dangling)* | `visualization-skill-selection` (missing) | **R2** create the Anchor via engine `migrate` | Inline goal describes a continuous, threshold-free optimization loop ("逐步建立匹配知识…并持续优化") — passes FR-036(c); FR-048 D-5 fixes R2. |
| `demo-seat-dispatch` *(dangling)* | `demo-seat-dispatch` (missing) | **R3** archive team | One-off SC-002 demonstration for spec 054; no continuous theme, no covering Anchor. |

Ordering constraint: the `viz-skill-arena` R2 anchor creation runs **before** the final
`anchor_slug` resolution assertion (SC-005), and the 16-key rename runs before any disposition
receipt is written, so each receipt records the post-rename spelling.

Unaffected: the 9 teams bound to entries that remain Anchors, and the 4 unbound teams. The unbound
four are **byte-identical** outputs (no binding field, no `.specify/goal/` path), which is itself an
assertion of the FR-047 acceptance scenario.

## 5. Live-surface roots (SC-001 declaration)

The residue scan reads **this** declaration — no test or script hard-codes a second root list.
Exclusions are a closed list with reasons; a live *definitional* page is never excludable.

```yaml
live_surface_roots:
  dirs:
    - templates/            # canonical templates, incl. commands/
    - skills/               # canonical skills (internal + external)
    - agents/               # canonical agent templates
    - shared/               # canonical shared definitions/guidelines/workflow
    - scripts/              # canonical scripts
    - src/                  # CLI source (hardcoded command lists)
    - docs/                 # docs site source
    - .specify/shared/      # runtime mirror
    - .specify/skills/      # runtime mirror
    - .specify/agents/      # runtime mirror
    - .specify/templates/   # runtime mirror
    - .specify/scripts/     # runtime mirror
    - .specify/teams/       # live team definitions (team.md and references)
    - .specify/anchoring/   # anchor definitions (anchor.md), excluding summary/
    - .specify/features/    # live feature detail pages — see the recorded exclusion below
    - .specify/memory/      # knowledge/tools/templates; session+feedback excluded
    - .specify/workflow/    # git workflow declaration
    - .claude/commands/     # generated per-tool copies
    - .github/prompts/
    - .qoder/commands/
    - .opencode/command/
  files:
    - README.md
    - AGENTS.md
    - CLAUDE.md
    - QODER.md
    - .specify/glossary.md
    - .specify/instructions.md
    - .specify/skills.md
    - .specify/tools.md
    - .specify/features.md
  excluded_dirs_any_depth:
    - runs/              # dated team run records (FR-061 protects .specify/teams/**/runs/**)
    - session/           # dated memory session notes
    - feedback/          # dated feedback entries
    - notes/             # docs/notes/** dated notes
    - history/           # .specify/history/** and docs/reference/history/** dated knowledge
    - archive/           # .specify/archive/** archive-not-delete destination
    - summary/           # derived summary trees (regenerated, FR-038)
    - test-evidence/     # dated evidence records
    - __pycache__/, node_modules/, public/
  excluded_files:
    - .specify/features/**/*.md
      # CLOSED, RECORDED EXCLUSION (FR-005's definitional test still applies): a feature detail page
      # is an append-only delivery record — what a feature delivered, in its own words, at its own
      # date. It is not a definitional page; rewriting it would do the kind of dated-record damage
      # FR-061 guards elsewhere — the detail tree is not in FR-061's protected set, so this exclusion
      # is the plan's own closed choice, recorded here rather than derived from that principle.
      # The current-facing claim lives in the index row (root above, class C7) and the
      # correction arrives as a dated successor note inside the page (041 already carries one; 094
      # gains one in WP-06, whose territory owns both detail pages). This exemption is never
      # available to a *definitional* page (a
      # `shared/definitions/**` owner, a glossary/instruction surface, or a canonical template).
    # all dated spec dirs (.specify/specs/**) are outside every root above, by construction.
```

**Classes and baseline patterns** (definitions owned by SC-001 / FR-005; the compiled set lives in
`tests/contract/test_live_semantic_residue.py` and MUST preserve the injection test):

| Class | Meaning | Patterns (baseline) |
|-------|---------|---------------------|
| C1 | Goal defined as project-level / end state | `(?i)^[\s>#*+-]*(a\|an\|the)?\s*\**goal\**\s+(is\|means\|refers to)\s+(a\|an\|the)?\s*(project-level\|long-horizon\|long-term objective)`; `(?i)^\|\s*\**goal\**\s*\|[^\|\n]*project-level`; `^\|\s*(Goal\|目标)\s*\|[^\|\n]*项目级`; `(目标\|Goal)[^\n。\|]{0,12}(是\|定义为)[^\n。\|]{0,15}(项目级\|远期目标)` |
| C2 | Anchor subordinate to Goal | `(?i)\b(goal\|目标)\b[^\n]{0,30}\b(top of\|highest (level\|layer)\|最高层)\b[^\n]{0,30}\b(anchor\|锚点)\b`; `(?i)\b(anchor\|锚点)\b[^\n]{0,40}\b(is\|as)\s+(a\s+)?(sub-?goal\|child goal\|goal slice\|下级目标)\b` |
| C3 | `/speckit.goal` as the anchor-archive authoring entry | `(?i)speckit\.goal[^\n]{0,160}(sole authoring\|only authoring\|唯一撰写)`; `(?i)(sole authoring entry\|唯一撰写入口)[^\n]{0,160}speckit\.goal`; `speckit\.goal[^\n]{0,120}(锚点档案\|anchoring archive)`; `(锚点档案\|anchoring archive)[^\n]{0,120}speckit\.goal` |
| C4 | `.specify/goal/<slug>/summary/` as delivery path | `\.specify/goal/<[^>]+>/summary/` |
| C5 | A retained anchor's own body still speaks the retired terminology | `^\#\s*Goal:`; `\.specify/goal(?![a-z])` — **scoped to `.specify/anchoring/*/goal.md` / `anchor.md`** (the normalization target of C-38 A-N-1…A-N-4) |
| C6 | A live surface still sends the user to `/speckit.goal` for an Anchor-only mode | `/speckit\.goal\s+(targets\|migrate\|migrate-archive\|coordinate)\b` |
| C7 | A live feature-index row still states the retired model | `.specify/features.md` only: `\.specify/goal/<[^>]+>`; `\.specify/anchoring/<[^>]+>/goal\.md`; `(?i)project-level goal`; `goal\s*=\s*设计师` |

**Baseline reading before implement** (`test-evidence/live-semantic-scan-baseline-2026-11-12.txt`),
measured on the declared roots as they stand (21 directories + 9 files; `.specify/features.md` is a
root, so the 041 index row is counted where its classes apply):
C1 **4** · C2 **0** · C3 **8** · C4 **16** · total **28** lines. C1's four
lines are the glossary `Goal` row, the derivation table row (×2 mirror), and
`docs/reference/commands/goal.md`; C3's eight are the goal template, its four generated copies,
`manage-goal/SKILL.md` (×2 mirror) and the 041 feature-index row; C4's sixteen are the team-domain
summary paths named by FR-058 (6 canonical skill-tree lines ×2 mirror layers), the two
`docs/reference/commands/team.md` rows, one memory tool record, and the 041 index row.
Zero C2 lines means the hierarchy inversion lives in prose shapes this baseline does not catch —
the hierarchy itself is asserted by `sdd-routing-definitions.md` (FR-052) and by the C1 rows, so
C2 is a regression net, not the convergence target.

**Classes added by the checklist repair (F-1 / F-2 / F-10), measured 2026-11-12** (full readings:
`test-evidence/checklist-repair-residue-baseline-2026-11-12.txt`): **C5 16** lines over the store as
it stands (14 entry directories, of which 5 leave the store with their migrated/archived entries);
the **11** lines that survive into the 9 retained anchors are the 9 `# Goal:` headings plus 2
retired-path lines in `094-goal-team-parallel` — that 11 is the convergence target, and C-38's A-N
table is the only mechanism allowed to reach it. **C6 40** line-hits: 16 in the engine (8 × two
mirror layers), 16 in team-domain skills/references (8 × two layers: create-mode 3, run-team 1,
goal 1, execution-guide 1, summary-mapping 1, goal-editing 1), 2 in
`docs/reference/commands/team.md`, 2 in `.specify/glossary.md`, 1 in `src/specify_cli/__init__.py`,
1 in a live team definition (rewritten by the declared N-7 rule, `contracts/migration-cleanup.contract.md`
C-46), 1 in `docs/reference/commands/seal.md`, 1 in `.specify/features.md`.
**C7 3** rows of `.specify/features.md` (rows 027, 041, 094) — rewriting those three rows is a WP-03
deliverable, and the 101 row written at close must not reintroduce the patterns.

C6 is deliberately a **pointer** class, not a literal `.specify/goal/` sweep: the retired directory
name also appears in historical narrative that must stay, so a path-literal sweep measured 84
line-hits and was rejected as too broad (it would have demanded rewriting dated prose). The mode
pointer is the behaviourally wrong text — a user following it reaches a command that refuses.

Pattern precision is part of the criterion: an over-broad pattern (`goal` … `project-level` within
80 chars) matched 16 lines including `shared/workflow/feedback-step.md`'s unrelated "goal model's
Harness" sense — the baseline above is the narrowed set. Adding a pattern requires the injection
test to still fire (a freshly injected old-semantic sentence in a live root must turn the scan red).

## 6. Written rulings

- **R-01 — Classification is decided here, executed later.** FR-035 makes plan the decider and
  implement the executor; § 3 is the classification record and the machine-readable
  `classification.json` beside it is what the cleanup engine reads. Deviations are impossible by
  construction (implement has no authority to reclassify) and detectable (the engine renders the
  record it was given).
- **R-02 — `classification.json` is a plan artifact, not a runtime store.** One file, one commit,
  consumed verbatim; per-feature directory, so concurrent branches cannot collide.
- **R-03 — One engine, layer-parameterized.** `goal-utils.py` stays the sole definition writer;
  layer→filename is resolved from the layer (`anchor`→`anchor.md`, `goals`→`goal.md`,
  `teams`→`team.md`) instead of the single `DEFINITION_FILENAME` constant (FR-029). A second engine
  would duplicate the exit-code table, the binding parser and the lifecycle table — three
  independent divergence points for zero benefit. Carried as tension T-001.
- **R-04 — Goal store is `.specify/goals/` (plural) and keeps the filename `goal.md`.** The path is
  pinned by STR-002; the plural directory name prevents a one-letter diff between two stores that
  hold different concepts.
- **R-05 — No compatibility aliases.** Scope member `goal` and the four Anchor-only modes fail with
  a named refusal instead of an alias or a read fallback (FR-020, FR-030, FR-031). An alias would
  let the retired vocabulary survive indefinitely, which is exactly what this feature retires.
  Carried as tension T-004.
- **R-06 — Summary trees are derived, not authored** (`PLAN-EDIT` FR-011 / FR-028 / SC-006). The
  anchor archive has two faces: `anchor.md` (engine-written definition) and `summary/**` (written by
  the existing summary flow, `build-summary-input.py` today). The single-writer audit therefore
  covers definition files; the summary writer keeps its long-standing role. Regeneration applies to
  existing trees only — an anchor without a `summary/` does not get one fabricated.
- **R-07 — Targets survive migration two ways.** A definition with `## Targets` either stays an
  Anchor or migrates with every Target statement verbatim under one fixed heading
  (`## Migrated Targets`), with identity recorded in the receipt. FR-039's closed mapping governs
  field renames; FR-040 governs this preservation container; the two are complementary, not a
  fourth rename.
- **R-08 — Owner rewrite keeps two readable histories.** `anchor-definitions.md` is created with the
  project-level content moved out of `goal-definitions.md`; `goal-definitions.md` is then rewritten
  in a separate commit. Squashing both into one edit would erase the "this text changed owner" step
  from `git log --follow` (FR-006).
- **R-09 — Ledger and probe are regenerated, never hand-edited.** The flow-class rows (FR-054) are
  authored, but the compiled `## Wrap-up` embeddings (FR-055) come from `probe-utils.py`; the
  fingerprint in both command templates changes with the registry and MUST be recompiled.
- **R-10 — Command copies: regenerate only what exists.** Four per-tool copy directories exist in
  this tree (`.claude/commands`, `.github/prompts`, `.qoder/commands`, `.opencode/command`);
  `regen-command-copies.py` writes only existing directories, so `hermes`/`codex` gain no new
  directory from this feature.
- **R-11 — Docs build is a falsified premise, not a silent skip.** Hugo 0.141.0 fails on this tree
  before any edit (`EP-006`, Decision `fallback`). SC-008's docs-build limb reports
  `not-evaluated`; its other limbs (reference page exists, ledger row, probe face) are measured.
  FR-071 forbids reporting an unavailable reading as a pass.
- **R-12 — Protected-path comparison is per file and pre-registered.** `git hash-object` over
  FR-061's roots at `d7c9da7a3` is captured to a file under this spec's `test-evidence/` at
  implement entry and again at closure; equality is compared as sets, never as a directory digest
  (directory digests move when files are added anywhere under a root). Scratch lists live under
  `.specify/.tmp/`.
- **R-13 — Inherited blockers are five rows from three dependency features.** 037 contributes one
  (`SC-016_status`, a `partial` row in its markdown tally), 038/042 one each (`deferred_tasks`, both
  literally `none`), 094 two (`SC-001_status`, `SC-010_status`); 074 and 085 contribute nothing
  extractable (every status row is `pass`, `deferred_tasks=` is empty), and no detail page among the
  six carries a `## Deferred` list item. Dispositions live in `plan.md` § Inherited Blockers: two
  `resolved` (038/042, measured value `none`) and three `not-applicable` (037/094 — decision-gated
  rounds this feature neither runs nor reopens). No row is `inherited`, so no carrier is claimed.
- **R-14 — Disposition receipts are per team, in the team's own directory.** Concurrent Development
  Safety forbids one shared store; `.specify/teams/<slug>/disposition-receipt.json` gives two
  branches disjoint paths and survives the team's archival (the directory stays, only
  `lifecycle_state` changes).

## 7. Not evaluated at plan time

- Real-data migration is **not** executed here (plan produces decisions and contracts only). SC-003
  / SC-004 / SC-007 readings are implement-time outputs and MUST NOT be pre-filled.
- Hugo docs build: not evaluated (see R-11). No other SC-008 limb is blocked.
