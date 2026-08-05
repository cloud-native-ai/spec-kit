# Data Model: Goal Registry (037)

**Requirement → Feature**: `037-goal-registry` → Feature 041 Goal Registry
**Concept authority**: `shared/definitions/goal-definitions.md` — **read-only** for this requirement (FR-019). Where this document and the authority disagree, the authority wins and this document is the defect.

## Entity overview

| Entity | Kind | Home | Written by |
|--------|------|------|-----------|
| Goal | authored | `.specify/goal/<goal-slug>/goal.md` | `/speckit.goal` only |
| Goal Identity | derived-from-path | the `<goal-slug>` directory name | `/speckit.goal` (at creation) |
| Goal Success Criterion | authored | `goal.md` body | `/speckit.goal` only |
| Goal Lifecycle State | authored | `goal.md` frontmatter | `/speckit.goal` only |
| Goal Archive | authored aggregate | the `.specify/goal/` tree | `/speckit.goal` only |
| Goal–Team Binding | authored (team side) | `team.md` frontmatter `goal_slug` | team maintainer / `/speckit.team` |
| Team Territory | authored (team side) | `team.md` frontmatter `territory` | team maintainer / `/speckit.team`; ratified coordination writes here |
| Team Roster | **derived** | `.specify/goal/<goal-slug>/summary/roster.md` (+ machine form in `summary/data/`) | summary refresh only |
| Overlap Finding | **derived** | same refresh output + run report status line | summary refresh only |
| Contested Area | **derived** classification | subset of Overlap Findings | summary refresh only |
| Coordination Round | **proposal** (no authority) | run-scoped proposal surfaced to the user | coordination round; ratification writes to `team.md` |

The authored/derived split is the load-bearing invariant: it makes FR-007 and SC-008 mechanically checkable as a single-subtree allow-list (`summary/**` writable, `goal.md` not).

## Goal

The project-level objective definition. **Exactly three parts** (authority § "What a Goal Is"); identity is carried by the directory name and is not a fourth part.

| Field | Location | Type | Required | Rules |
|-------|----------|------|----------|-------|
| *(identity)* | directory name | string | yes | `<goal-slug>`; see Goal Identity |
| `status` | frontmatter | enum | yes | `active` \| `achieved` \| `abandoned` (FR-006). Terminal states are retained, never deleted |
| `created` | frontmatter | ISO-8601 date | yes | metadata for change traceability, **not** a composing part (FR-002) |
| `updated` | frontmatter | ISO-8601 date | yes | same |
| narrative | body `## Objective` | prose | yes | the desired end **outcome**. MUST NOT be a task list or implementation plan (FR-027) |
| criteria | body `## Success Criteria` | ordered list | no (may be empty) | zero or more verifiable attainment conditions (FR-002) |
| change history | body `## History` | append-only list | yes when criteria change | records the prior value of a modified criterion (FR-005) |

**Rules**

- **G-1** One goal = one objective. A composite objective MUST be split into separate `<goal-slug>` directories, each with its own lifecycle (FR-028). The project MAY hold multiple `active` goals concurrently.
- **G-2** The goal's object is **unrestricted** — the framework itself, codebase-wide convention convergence, runtime outcomes. A goal MUST NOT be rejected because no FR in this project implements it (FR-029).
- **G-3** Criteria are **measured by degree** (progress / threshold / evaluator score). Consumers MUST NOT treat them as per-clause pass/fail (FR-030). No current-value field is stored, because a current value is derived data and `goal.md` is authored (FR-007) — progress lives in `summary/`.
- **G-4** Criteria authority is **cross-feature** and disjoint from any requirements spec's `SC-xxx`. Criteria MUST NOT be copied in either direction (FR-031).
- **G-5** `goal.md` MUST NOT enumerate the FRs "under" the goal, and no `requirements.md` may carry a goal field (FR-032).
- **G-6** Creating a goal with an existing identity MUST be rejected and MUST point at the modify path; the existing definition MUST NOT be overwritten (FR-004).
- **G-7** An empty criteria set is legal. Consumers MUST then declare "no verifiable criteria provided" rather than inventing any (spec Assumptions).

### Lifecycle

```text
(none) --create--> active
active --achieve--> achieved      (terminal, retained)
active --abandon--> abandoned     (terminal, retained)
```

Terminal goals stay in the archive; deletion is not a transition. `superseded` is **not** a state — the concept authority fixes exactly three, and the spec was conformed to it (Clarifications, session 3).

## Goal Identity

The key that decides "the same goal", reused verbatim from requirement 036 (FR-003) — no second identifier mechanism.

- Grammar: first character alphanumeric; remaining characters limited to `[A-Za-z0-9_.-]`. Enforced today at `build-summary-input.py:187-188`, derived from the invoked skill's DDL constraint.
- MUST additionally be a safe path segment: no `/`, and not `.` or `..`.
- Doubles as the archive directory name, which is why the path-safety constraint is not optional.

## Goal Archive

The whole `.specify/goal/` tree — the materialized list of the project's current and historical goals.

```text
.specify/goal/
└── <goal-slug>/
    ├── goal.md                     # authored definition — write-set EXCLUDED
    └── summary/                    # derived subtree — the ONLY writable face
        ├── project.md              # summarize-project output (relocated from 036)
        ├── roster.md               # participating-team roster + overlap findings
        ├── data/
        │   ├── project-input.yaml  # generator form (relocated from 036)
        │   └── .refresh.lock       # refresh mutual exclusion (900s stale threshold)
        └── *.puml / *.svg / *.png  # charts (relocated from 036)
```

- **A-1** Exactly one goal-indexed directory exists in the project; `.specify/project/` holds no goal artifacts (FR-020, SC-009).
- **A-2** The derived write-set is the allow-list `<goal-slug>/summary/**`. Any write to `<goal-slug>/goal.md` during a refresh is a write-set violation, not an incidental update (FR-023, SC-008).
- **A-3** Pre-migration artifacts sitting at the `<goal-slug>/` root are a to-be-migrated state, not a valid layout (spec Edge Cases).

## Goal–Team Binding

One-way reference, **N teams : 1 goal** (authority § "Goal–Team Binding").

- **B-1** The team declares `goal_slug`; the team side stores the **identity only**, never a copy of the goal content (FR-008).
- **B-2** A team serves exactly one goal at a time; declaring two MUST be rejected (FR-009).
- **B-3** A reference to a nonexistent identity MUST be reported as a broken link naming the missing identity, never silently degraded to an empty goal (FR-010).
- **B-4** A legacy team with only an inline goal MUST keep working with zero edits (FR-011).
- **B-5** When both a reference and an inline goal exist and disagree, the referenced definition is authoritative and the divergence MUST be surfaced for human arbitration (FR-012).
- **B-6** The binding MUST NOT become bidirectional. The goal side learns its teams by derivation, never by storage (FR-033).

## Team Territory *(new — team-level)*

The team's declared coverage, lifting the existing member-level vocabulary one scope up (FR-035). Declared in `team.md` frontmatter, immediately after `goal_slug`.

| Field | Type | Required | Rules |
|-------|------|----------|-------|
| `territory.write` | list of scope entries | no | paths this team may create or modify |
| `territory.read` | list of scope entries | no | paths this team may read |
| `territory.forbidden` | list of scope entries | no | shared entries this team MUST NOT modify |

A **scope entry** is one of two shapes:

| Shape | Form | Overlap decidable mechanically? |
|-------|------|-------------------------------|
| path-shaped | a repo-relative path, glob, or brace form | **yes** — normalize, then intersect |
| typed non-path | `type: <dimension>` + free-text target (e.g. `type: framework`, `type: runtime`) | **no** — listed side by side for human arbitration |

**Rules**

- **T-1** Applies to all four collaboration patterns. It MUST NOT be parallel-only (FR-035) — today's member-level `territory` exists only in the parallel pattern, which is exactly why a team-level key is required rather than derivable.
- **T-2** Path-shaped entries MUST be normalized before comparison: brace expansion (`{a,b}`), glob resolution, relative→canonical. Notation differences MUST NOT cause a missed overlap (FR-036, spec Edge Cases).
- **T-3** Absent territory means **undecidable**, never empty. A team without a declaration MUST be reported as "scope not declared; overlap undecidable" (FR-042, SC-018).
- **T-4** A member-level territory that writes outside its team-level territory is an out-of-bounds violation and MUST be reported (spec Edge Cases).
- **T-5** Territory is authored on the team side. A ratified coordination decision is written here, and nowhere else (FR-040).

## Team Roster *(derived)*

The goal side's view of who is advancing it. Regenerated in full on every refresh; never incrementally patched.

| Field | Source | Rules |
|-------|--------|-------|
| team slug | `team.md` `slug` | attribution is presented as the team slug, never an internal agent id |
| declared territory | `team.md` `territory` | verbatim; absence recorded as undeclared |
| identity type | `explicit` when `goal_slug` is declared, `inferred` when derived from the team's own slug | carries 036's GI-1 semantics |
| advancing? | presence of recent run/ledger activity | distinguishes "defined but not started" from "in progress" (FR-015) |
| participation | `active` \| `departed` | a team that rebound to another goal is marked departed, not removed (FR-034) |

- **R-1** Derived into `summary/` only; never a field of `goal.md` (FR-033, SC-015).
- **R-2** Completeness: every team declaring the goal's `goal_slug` appears. The truth set is the filesystem scan, and the roster is diffed against it (SC-015).

## Overlap Finding and Contested Area *(derived)*

| Field | Type | Rules |
|-------|------|-------|
| team pair | (slug, slug) | unordered |
| kind | `write-write` \| `read-write` \| `read-read` \| `non-path` | only `write-write` violates the invariant |
| entries | list of normalized paths, or the two non-path declarations | `write-write` findings name concrete paths |
| verdict | `overlap` \| `no-overlap` \| `undecidable` | three distinct outcomes (FR-042) |

- **O-1** Zero write overlap: no two teams sharing a goal may have intersecting `territory.write` (FR-037, SC-016). This is the member-level invariant lifted to team level.
- **O-2** Read overlap is allowed. A pair intersecting only on reads MUST NOT be reported as an overlap (FR-037).
- **O-3** A `write-write` finding is a **Contested Area**. It MUST resolve to a single owning team or to the goal's forbidden-write list; it MUST NOT remain multi-writable (FR-038).
- **O-4** Non-path findings are listed side by side. The mechanism MUST NOT judge two non-path declarations equivalent (FR-036).

## Coordination Round

A proposal-only process with no write authority.

```text
detect (rides refresh) → propose (with rationale) → human ratifies → write back to team.md
```

- **C-1** The mechanism detects and proposes only; it MUST NOT rewrite any team's territory (FR-039).
- **C-2** During the proposal stage, writes to `team.md` are zero (SC-017).
- **C-3** The ratified division is written back into each `team.md`; no authored coordination record is created inside the goal directory, preserving the `goal.md` / `summary/` split (FR-040).
- **C-4** Detection rides 036's existing summary refresh — one trigger point, no second mechanism (FR-041, SC-015). The round itself is initiated explicitly by a human.
- **C-5** A single-team goal yields an empty overlap set with the round not initiated; "no overlap" and "undecidable" remain distinct (spec Edge Cases).

## Relationships

```text
Goal Archive 1 ── * Goal
Goal 1 ── 1 Goal Identity            (the directory name)
Goal 1 ── * Goal Success Criterion   (zero allowed)
Goal 1 ── 1 Lifecycle State
Goal 1 ── * Team                     (via one-way goal_slug reference; N teams : 1 goal)
Team 1 ── 0..1 Team Territory
Goal 1 ── 1 Team Roster              (derived; regenerated wholesale)
Team Roster 1 ── * Overlap Finding   (derived)
Overlap Finding (write-write) ── 1 Contested Area
Contested Area * ── 1 Coordination Round
Goal ──╳── Requirement               (no structural link, by rule G-5 / FR-032)
```

The last row is deliberate: goal and requirement sit on different planes with no hierarchy and no connecting field. Their relationship appears only observationally, in evaluation results, team summaries, and run reports.
