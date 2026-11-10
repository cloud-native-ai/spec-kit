# Read-only spec audit — 046-browser-site-memory (batch 6)

**Date**: 2026-11-10
**Tree**: `/storage/project/cloud-native-ai/spec-kit` (branch `master`, HEAD at time of audit)
**Mode**: read-only. No spec, source or git state changed; this file is the only write.
**Audited**: `.specify/archive/specs/046-browser-site-memory/` (13 artifacts: requirements, plan, tasks,
data-model, research, quickstart, verification, feature-ref, 3 contracts, 1 checklist, 2 failed-test lists
`baseline-failed.txt` / `current-failed.txt`).

## Scope & counting rule

Every repository path token in the 13 artifacts, **deduplicated at the string level**. Intra-spec relative
references (`requirements.md`, `data-model.md`, `contracts/*.md`, `research.md`, `../requirements.md`) are
resolved against the archive directory and counted once per named artifact. Runtime data files
(`site/<host>/state.json`, `records/*.jsonl`, `recipe.json`, `validation/*.json`,
`notes.md`) and bare parent-directory tokens (`.specify/scripts/`, `.specify/skills`,
`templates/`, `shared/`) are excluded — they are not repository artifacts this spec ships.

Classification: **alive** = target exists in the current tree; **archived-elsewhere** = the target now
lives under `.specify/archive/specs/046-browser-site-memory/` (or a sibling archive of the same object);
**dead** = no target, including stale pre-archive `.specify/specs/046-browser-site-memory/...` paths.

## Counts

| Refs total | Alive | Archived-elsewhere | Dead |
|---|---|---|---|
| **36** | **9** | **7** | **20** |

## Alive (9)

| Ref | Representative anchor |
|---|---|
| `.gitignore` (file exists; the two site lines do not — see broken #11) | plan.md:83,100; contracts/framework-exclusions.md:4 |
| `pyproject.toml` (static `"skills"` force-include absent, line 48 comment) | plan.md:86; contracts/framework-exclusions.md:26 |
| `src/hatch_build.py` | plan.md:87; contracts/framework-exclusions.md:4,28 |
| `scripts/python/sync-mirrors.py` | plan.md:85 |
| `.specify/scripts/python/sync-mirrors.py` | plan.md:84,99; research.md:21; tasks.md:39,56 |
| `.specify/memory/constitution.md` | plan.md:27 |
| `.specify/memory/features.md` | feature-ref.md:29 |
| `.specify/memory/features/048.md` | tasks.md:109 |
| `.specify/skills/improve-skills/scripts/skill-shape.py` | tasks.md:73 |

## Archived-elsewhere (7)

`requirements.md` (plan.md:3; checklist:5 as `../requirements.md`), `data-model.md` (plan.md:69;
tasks.md:87), `research.md` (plan.md:54,68; contracts/framework-exclusions.md:24),
`contracts/site-memory-engine.md` (plan.md:71; quickstart.md:5), `contracts/site-memory-formats.md`
(plan.md:71; data-model.md:90), `contracts/framework-exclusions.md` (plan.md:72; tasks.md:35;
feature-ref.md:17). All six resolve inside the archive directory; the archive move itself is
commit `c5b17a9fc` (2026-11-09).

## Broken list (20 dead references)

**A. The whole skill surface (removed from `master` 2026-09-22, commit `80a8c1fb0` "remove three skills" —
browser-utils, browser-extension, clone-website-ui). Last content is recoverable only at
`80a8c1fb0^`; `follow-ups` live in `.specify/memory/features/048.md` (relocated to xuanji-extension).**

1. `plan.md:81` — `skills/browser-utils/` → directory absent (no `skills/browser-utils` anywhere in the tree).
2. `plan.md:82` — `.specify/skills/browser-utils/` → directory absent.
3. `plan.md:98`, `tasks.md:70,73` — `skills/browser-utils/SKILL.md` → absent.
4. `plan.md:9`; `tasks.md:55,87,102`; `contracts/site-memory-engine.md:8` —
   `skills/browser-utils/scripts/site-memory.py` → absent (555-line file deleted at `80a8c1fb0`).
5. `contracts/site-memory-engine.md:8` — `.specify/skills/browser-utils/scripts/site-memory.py` (mirror) → absent.
6. `research.md:31` — `skills/browser-utils/scripts/js/run.js` + `scripts/js/package.json` → absent.
7. `research.md:33` — `references/playwright-patterns.md`, `references/mcp-browser-tools.md`,
   `references/extension-bridge-patterns.md` → all absent (deleted with the skill).
8. `plan.md:9`; `tasks.md:66,71`; `contracts/site-memory-formats.md:4` — `references/site-memory.md` → absent.
9. `plan.md:9`; `tasks.md:66,72` — `references/request-level-patterns.md` → absent.
10. `quickstart.md:5,13,20,35,36,47` — `$SKILL_HOME = .specify/skills/browser-utils` and
    `$SKILL_HOME/scripts/site-memory.py` → both absent.

**B. Distribution-exclusion contract (FR-003 / framework-exclusions).**

11. `requirements.md:102,157`; `plan.md:83`; `tasks.md:38`; `contracts/framework-exclusions.md:10-15` —
    the two `.gitignore` lines (`skills/browser-utils/site/`, `.specify/skills/browser-utils/site/`) → **absent**;
    removed in commit `15b5c683b` (2026-10-08). X-1 and X-2 are no longer satisfied.
12. `requirements.md:102,157`; `plan.md:83`; `tasks.md:38` — `skills/browser-utils/site/` and
    `.specify/skills/browser-utils/site/` → absent as paths and as ignore rules; nothing creates them now.
13. `plan.md:84`; `contracts/framework-exclusions.md:19` — the `MIRROR_PAIRS` tuple
    `("skills", ".specify/skills", …)` → **relabelled**, not removed: current `scripts/python/sync-mirrors.py:95-96`
    has `("skills/external", ".specify/skills", False, {"site", "internal"})` and
    `("skills/internal", ".specify/skills/internal", False, {"site"})`. The `site` exclusion semantics survive
    on the successor pairs; the spec's named tuple no longer exists verbatim.

**C. Contract tests (both deleted in commit `15b5c683b`).**

14. `tests/contract/test_browser_site_memory.py` — `plan.md:16,88,100`; `tasks.md:51,56,66,83,98`;
    `quickstart.md:5`; `contracts/site-memory-engine.md:4`; `contracts/site-memory-formats.md:4`;
    `contracts/framework-exclusions.md:4` → path absent (551 lines deleted). No replacement test references
    `site-memory`, `browser-utils` or `browser_site` (grep over `tests/` returns zero).
15. `tests/contract/test_browser_site_exclusions.py` — `plan.md:89`; `tasks.md:37,41` → path absent
    (160 lines deleted).

**D. Stale pre-archive paths (object survives in the archive; the written path is dead).**

16. `plan.md:5,66` — `.specify/specs/046-browser-site-memory/` → now `.specify/archive/specs/046-browser-site-memory/`.
17. `tasks.md:23,31` — `.specify/specs/046-browser-site-memory/baseline-failed.txt` →
    `.specify/archive/specs/046-browser-site-memory/baseline-failed.txt` (present there).
18. `.specify/memory/features.md:57` (Spec Path column) and `.specify/memory/features/048.md` § Related Files —
    `.specify/specs/046-browser-site-memory/requirements.md` → archived path.

**E. A path that never resolved as written.**

19. `research.md:9,32` — `scripts/bridge/` → no top-level `scripts/bridge` exists now or in history; the bridge
    lived at `skills/browser-utils/scripts/bridge/` (deleted at `80a8c1fb0`).

**F. Live-code pointers into the dead pre-archive path (not counted in the 36).**

20. `src/hatch_build.py:15` → `specs/046-browser-site-memory/research.md`; `src/hatch_build.py:21` →
    `.specify/specs/046-browser-site-memory/contracts/framework-exclusions.md`. Both are stale docstring
    contracts in a live build hook; the targets now live under the archive.

## Ledger-target check (`.specify/archive/specs/CONSOLIDATION-LEDGER.md:15`)

Row: `| 046-browser-site-memory | archive | Feature 048 (row already `Relocated`) | review-G4 |`

- **Target resolves**: `Feature 048` is row 57 of `.specify/memory/features.md`; its Status cell is
  `Relocated`, matching the ledger's parenthetical. `.specify/memory/features/048.md` exists.
- **Status prose is accurate**; the row's own claim "already Relocated" matches the index, not the detail file.
- **Residual inaccuracies**:
  - The resolved row's **Spec Path column is dead** (`.specify/specs/046-browser-site-memory/requirements.md`, broken #18).
  - `.specify/memory/features/048.md:6` still says **`Status: Implemented`** while the index says `Relocated`
    (two statuses for one object); its header `Last Updated: 2026-08-24` predates the relocation note
    (2026-09-22) it carries.
  - `review-G4` has **no in-tree record**: the only occurrence of the string is this ledger line.
- **Ledger structural defect** (ledger-wide, not 046-specific): the `054-agent-registration-wiring` row sits
  on line 23, *after* the "Deferred"/"Not executed" prose, i.e. outside the Markdown table it belongs to —
  it will not render as a row and sits below the closing paragraphs.
- Sequence is coherent: skill removed `80a8c1fb0` (2026-09-22) → tests + `.gitignore` lines removed
  `15b5c683b` (2026-10-08) → spec archived `c5b17a9fc` (2026-11-09).

## Missing guards

1. `tests/contract/test_browser_site_memory.py` — **missing** (engine state-machine/redaction/format guard).
2. `tests/contract/test_browser_site_exclusions.py` — **missing** (X-1..X-7 three-closure guard).
3. `.gitignore` X-1/X-2 guard — **missing target**: neither ignore line nor probe-path assertion survives.
4. `src/hatch_build.py::_stage_skills` is still live, but its only content guard (wheel probe, X-7) died with
   the exclusion contract test; `tests/contract/test_build_hook.py` covers provenance probe/write only and has
   no staging or `site`-drop case.
5. `sync-mirrors` `site` exclusion is live but untested; additionally the spec's named pair
   `("skills", ".specify/skills", …)` is now two pairs (`skills/external`, `skills/internal`).
6. `tasks.md:25` GATE-3 (`wheel namelist must not contain specify_cli/skills/browser-utils/site/`) would pass
   vacuously today — the named directory does not exist in any form.

## Spot-checks (three implementation claims)

1. **File** — `skills/browser-utils/scripts/site-memory.py` (plan.md:9; tasks.md:55): **MISSING**. No
   `site-memory.py` anywhere in the tree; the file exists only at `80a8c1fb0^` (555 lines). Mirror
   `.specify/skills/browser-utils/scripts/site-memory.py` also missing.
2. **Symbol / command** — engine CLI `--action {init, get-state, append-record, validate-records, write-recipe,
   record-validation, transition}` (contracts/site-memory-engine.md §1; 7 actions): **unresolvable**. No live
   engine exposes the symbol; at `80a8c1fb0^` the engine had `ACTIONS` with exactly those seven keys and
   `--action choices=sorted(ACTIONS)` — the contract was true at deletion time, false now.
3. **Behaviour surface** — distribution exclusion (FR-003):
   - `src/hatch_build.py:42-59` `_stage_skills()` **LIVE**: copies `skills/` minus every `site` component and
     registers `force_include["specify_cli/skills"]`; `pyproject.toml:42-48` has no static `"skills"` line. ✔
   - `scripts/python/sync-mirrors.py:95-96` **LIVE**: both successor skills pairs retain `{"site", …}`. ✔
   - `.gitignore` site lines (X-1) **ABSENT**, and with them the only end-to-end assertion of the surface. ✘
   Net: the mechanism survives half-orphaned — the code paths run, nothing tests them, and one of the three
   closures is gone.

## Pending anchor-layout rename (`memory/` → `.specify/` root) — references that will move

Observed on branch `rename-anchors` (worktree `.specify/.tmp/sdd-loop/worktrees/rename-anchors/`); no action
taken, current tree audited as-is:

- `.specify/memory/constitution.md` (alive, plan.md:27) → `.specify/constitution.md`
- `.specify/memory/features.md` (alive, feature-ref.md:29) → `.specify/features.md`
- `.specify/memory/features/048.md` (alive, tasks.md:109) → `.specify/features/<ID>-<slug>.md` (that branch
  uses `NNN-slug.md` detail names; its numbering differs, so the 048 detail is not present there under that ID)
- `.specify/specs/...` → `.specify/specs/...` stays; `.specify/archive/...` stays.

Nothing else among the 9 alive references moves; the archived spec's dead references stay dead either way.

## Verdict

**BROKEN** — 20 of 36 repository references are dead, both named contract tests are deleted, the X-1 `.gitignore`
closure is gone, and the registry's artifact pointer for Feature 048 is stale. The spec is internally coherent
and its archive is complete; what broke is the external world it points at (implementation relocated out of the
repo 2026-09-22, guards removed 2026-10-08, spec archived 2026-11-09 without reference repair).

**Anomaly**: the audited feature's entire implementation and both contract guards were deleted from `master`
while the registry and consolidation ledger still describe a resolvable artifact — this is a real
relocation-plus-archive with unrepaired references, not benign path drift.

SPEC-AUDIT-6-DONE
