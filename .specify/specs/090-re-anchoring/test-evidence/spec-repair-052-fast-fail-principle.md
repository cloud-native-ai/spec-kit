# Spec Repair — 052-fast-fail-principle

**Date**: 2026-11-10
**Target**: `.specify/specs/052-fast-fail-principle/` (live spec dir; not archived)
**Mode**: read-first, bounded — dead-reference repair only; no commit, no push, no subagents.

## Sources

- Prior audit prose: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-live-batch-1.md` § `052-fast-fail-principle` (verdict BROKEN; 35 dead unique paths = 3 anchor-move + 28 dated snapshot + 4 other).
- Deterministic settled scan: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-settled.json` → key `.specify/specs/052-fast-fail-principle`: `refs 177 / alive 143 / dead 34`, `dead_list` = a 20-path sample only (19 dated snapshot paths + bare `skills/create-team/references/patterns.md`); it does not enumerate the full 34 and omits the anchor-move trio, so the audit prose above is the canonical per-entry source.
- Owner-format cross-check for repaired targets: `.specify/features.md` rows `032`, `040`, `051`, `052` (Feature Details + Spec Path columns), plus the detail files' own H1 titles.

## Counts

| Class | Unique entries | Occurrences | Disposition |
|-------|---------------:|------------:|-------------|
| **Dead total (audit set + 4 additional bare registry tokens)** | **39** | **89** | — |
| live-fixed | 8 | 44 | path rewritten to the live target |
| dated-kept | 30 | 44 | text left unchanged (dated records) |
| non-reference | 1 | 1 | left unchanged (runtime-scratch exclusion operand) |

Arithmetic: 8 + 30 + 1 = 39 unique entries. The "4 additional bare registry tokens" (`features/032.md`, `features/040.md`, `features/051.md`, `features/052.md`) were invisible to both audit scanners because those scanners only count tokens carrying a repo-root prefix (`.specify/`, `skills/`, …); they are dead in live artifacts and are counted here.

Additional tokens inspected beyond the audit dead set: 15 unique, all classified **non-reference**, 0 changed (listed in §4).

Fourteen *occurrences* of otherwise-fixed tokens are deliberately kept because they sit inside dated records — they are broken out in §2.3 under "kept occurrences within otherwise-fixed tokens".

## 1. Live-fixed (8 entries / 44 occurrences, 8 files)

| # | Dead reference (before) | Live target (after) | Occ | Locations (file:line, HEAD numbering) |
|---|-------------------------|---------------------|----:|----------------------------------------|
| 1 | `.specify/memory/constitution.md` | `.specify/constitution.md` | 16 | `contracts/constitution-export.md:22`; `feature-ref.md:162`; `plan.md:41`; `quickstart.md:19,21,96,98,108,110`; `requirements.md:97,166,314`; `tasks.md:13`(×2),`92,178` |
| 2 | `.specify/memory/features.md` | `.specify/features.md` | 4 | `feature-ref.md:7`; `requirements.md:28`; `tasks.md:9,247` |
| 3 | `.specify/memory/features/052.md` | `.specify/features/052-fast-fail-principle.md` | 3 | `feature-ref.md:6`; `requirements.md:24`; `tasks.md:247` |
| 4 | `features/040.md` (bare) | `.specify/features/040-agent-metadata-portability.md` | 1 | `requirements.md:20` |
| 5 | `features/032.md` (bare) | `.specify/features/032-dogfooding-practice.md` | 1 | `requirements.md:21` |
| 6 | `features/051.md` (bare) | `.specify/features/051-user-facing-comprehension.md` | 6 | `checklists/requirements.md:32`; `contracts/constitution-export.md:73`; `quickstart.md:328`; `tasks.md:49,77,232` |
| 7 | `features/052.md` (bare) | `.specify/features/052-fast-fail-principle.md` | 12 | `checklists/requirements.md:32,62,80`; `contracts/constitution-export.md:73`; `feature-ref.md:15`; `plan.md:179,185`; `quickstart.md:328`; `research.md:91,109`; `tasks.md:49,232` |
| 8 | `skills/internal/study-project/SKILL.md` | `skills/external/study-code/SKILL.md` | 1 | `requirements.md:106` (rename `study-project` → `study-code`, layer `internal` → `external`; audit commit reference `cde73a99f`) |

Target-existence evidence (all `-e` true at repair time): `.specify/constitution.md`, `.specify/features.md`, `.specify/features/052-fast-fail-principle.md`, `.specify/features/040-agent-metadata-portability.md`, `.specify/features/032-dogfooding-practice.md`, `.specify/features/051-user-facing-comprehension.md`, `skills/external/study-code/SKILL.md`.

Content check for the two slug-mismatched registry details (the known anchor-rename artefact): `040-agent-metadata-portability.md` H1 = `# Feature Detail: Token Efficiency Discipline`; `032-dogfooding-practice.md` H1 = `# Feature Detail: Task Complexity Rubric`. The slugs do not describe their content, but these are the paths the registry's Feature Details column uses for IDs 040 and 032, so they are the live targets.

Line suffixes (`:59`, `:18`, `:150-166`, etc.) were left exactly as recorded — they are readings taken against the then-current file, and this repair changes paths only.

## 2. Dated-kept (30 entries / 34 occurrences)

### 2.1 Dated pre-change mirror snapshot — 28 paths, `notes/pre-change-measurements.md:47–84`

Measured 2026-09-23, before the two-layer skills layout landed. All 28 are still absent today (verified against the tree); the fence also carries 10 entries that are alive now — the record is a frozen measurement, not a live pointer, so it is preserved verbatim.

| Line | Path (kept as written) | Today |
|-----:|-----------------------|-------|
| 47 | `.specify/skills/archive-session/SKILL.md` | absent (now `internal/archive-session`) |
| 48 | `.specify/skills/code-review/SKILL.md` | absent (now `internal/code-review`) |
| 49 | `.specify/skills/collect-evidence/SKILL.md` | absent (now `internal/collect-evidence`) |
| 50 | `.specify/skills/create-agent/SKILL.md` | absent (now `internal/create-agent`) |
| 54 | `.specify/skills/create-team/SKILL.md` | absent (now `internal/create-team`) |
| 55 | `.specify/skills/create-team/references/operating-loops.md` | absent (now `internal/create-team/...`) |
| 56 | `.specify/skills/create-team/references/summary-mapping.md` | absent (now `internal/create-team/...`) |
| 57 | `.specify/skills/create-team/references/team-presets.md` | absent (now `internal/create-team/...`) |
| 58 | `.specify/skills/create-tools/SKILL.md` | absent (now `internal/create-tools`) |
| 61 | `.specify/skills/draw-d3js/SKILL.md` | absent (merged into `draw-diagram`) |
| 63 | `.specify/skills/draw-drawio/SKILL.md` | absent (merged into `draw-diagram`) |
| 64 | `.specify/skills/draw-echarts/SKILL.md` | absent (merged into `draw-diagram`) |
| 65 | `.specify/skills/draw-excalidraw/SKILL.md` | absent (merged into `draw-diagram`) |
| 66 | `.specify/skills/draw-mermaid/SKILL.md` | absent (merged into `draw-diagram`) |
| 67 | `.specify/skills/draw-plantuml/SKILL.md` | absent (merged into `draw-diagram`) |
| 68 | `.specify/skills/git-fleet/SKILL.md` | absent (merged into `git-utils`) |
| 69 | `.specify/skills/git-server-init/SKILL.md` | absent (merged into `git-utils`) |
| 70 | `.specify/skills/git-submodule-edit/SKILL.md` | absent (merged into `git-utils`) |
| 71 | `.specify/skills/git-workflow/SKILL.md` | absent (merged into `git-utils`) |
| 72 | `.specify/skills/improve-agent/SKILL.md` | absent (now `internal/improve-agent`) |
| 76 | `.specify/skills/improve-team/SKILL.md` | absent (now `internal/improve-team`) |
| 77 | `.specify/skills/improve-tools/SKILL.md` | absent (now `internal/improve-tools`) |
| 78 | `.specify/skills/manage-agents/SKILL.md` | absent (now `internal/manage-agents`) |
| 79 | `.specify/skills/memory-recall/SKILL.md` | absent (now `internal/memory-recall`) |
| 80 | `.specify/skills/memory-record/SKILL.md` | absent (now `internal/memory-record`) |
| 82 | `.specify/skills/study-project/SKILL.md` | absent (renamed `study-code`, layer `external`) |
| 83 | `.specify/skills/summarize-project/SKILL.md` | absent (now `internal/summarize-project`) |
| 84 | `.specify/skills/think-skills/SKILL.md` | absent (skill removed; no replacement) |

### 2.2 Other dated records — 2 entries

| Entry | Locations | Why kept |
|-------|-----------|----------|
| `skills/create-agent/SKILL.md` | `notes/red-first-evidence.md:47` | red-first evidence fence, dated | 
| `skills/create-team/references/patterns.md` | `notes/red-first-evidence.md:47` | same fence, same run |

### 2.3 Kept occurrences inside otherwise-fixed tokens — 14 occurrences

| Token | Kept at | Reason |
|-------|---------|--------|
| `.specify/memory/constitution.md` | `notes/pre-change-measurements.md:107,109,128,248`; `notes/red-first-evidence.md:46` | 5 occurrences: dated measurement table / confirm list |
| `.specify/memory/features.md` | `requirements.md:519`; `notes/derived-command-audit.md:209` | append-only `## Clarifications` record; dated audit table row |
| `.specify/memory/features/052.md` | `requirements.md:519` | append-only `## Clarifications` record |
| `features/052.md` | `requirements.md:506,565`; `verification.md:13,237`(×2); `notes/sc001-dual-review.md:113` | Clarifications sessions 2026-09-22/23 (append-only per this spec's own `tasks.md` T063); `verification.md` is a dated verification record |

`requirements.md` § `## Clarifications` (lines 485–568) is an append-only dated record by this spec's own rule (T063: "append-only, MUST NOT 覆盖首轮记录"), so its path spellings are preserved even though the same tokens were repaired elsewhere in the file.

## 3. Non-reference (audit set, 1 entry)

| Entry | Location | Why not a reference |
|-------|----------|---------------------|
| `.specify/teams/.work` | `requirements.md:100` | exclusion operand of a repo-wide search (`排除 .specify/teams/.work/`); a runtime scratch dir the framework never commits — no stable target by design |

## 4. Additional tokens inspected beyond the audit dead set (15 unique, all non-reference, 0 changed)

| Token | Occurrences (live / dated) | Why non-reference |
|-------|---------------------------:|-------------------|
| `.opencode/agent` | 4 / 4 | quoted *wrong* path in prose that explicitly records the singular-vs-plural correction; the live tree is `.opencode/agents/` (exists) |
| `memory/feature-index.md` | 3 / 1 | quoted as a **non-existent** pointer inside `feature-integration.md` (upstream-defect report), never a target |
| `execution/configs/` | 4 / 1 | store-relative shorthand for `.specify/agents/execution/configs/` (exists) |
| `workflow/feedback-step.md`, `workflow/runtime-mode.md` (bare) | 2 / 0 | scope-relative shorthand inside `--only shared` prose (`shared/workflow/…` exists) |
| `create-agent/SKILL.md` | 1 / 0 | bare sibling filename inside a parallelism note (`tasks.md:283`); sibling names in the same sentence are also bare |
| `../.specify/instructions.md` | 1 / 0 | the relative symlink target of `.github/copilot-instructions.md`; correct by construction |
| `/speckit.`, `/speckit` forms | 3 / 0 | command forms, not paths |
| `/tmp/ffdrill` | 19 / 11 | example sandbox path in quickstart scenarios; dated notes reuse it as a record |
| `/tmp/t058-*`, `/tmp/t058iso.*` | 0 / 4 | transient temp files named in dated audit records |
| `.md/.py/.sh/.toml/.json/.yaml` | 1 / 0 | file-extension enumeration |
| `MARKER_*`, `CLAUSE_BEGIN/CLAUSE_END` | 2 / 0 | code constants |
| `[Pp]roceed…yes/no` | 1 / 1 | regex literal |
| `:65/:66/…`, `:94/:96/…` | 0 / 2 | line-list fragments split by the extractor |
| `qoder/claude/copilot/opencode` | 0 / 1 | render-key enumeration |
| `features/<ID>.md`; `.specify/specs/040-*/`; `.specify/specs/052-fast-fail-principle/*` | 3 / 0 | placeholder, quoted wrong premise, and glob respectively |

## 5. Registry row

`.specify/features.md` row `052`: Feature Details `.specify/features/052-fast-fail-principle.md` (exists), Spec Path `.specify/specs/052-fast-fail-principle/requirements.md` (exists), Status `Implemented`. **Resolves — no registry edit needed** (consistent with the prior audit's "Registry: Resolves").

## 6. Validator readings

Both validators exist and were run against the repaired files.

### `validate-requirements.py`

```
$ python3 scripts/python/validate-requirements.py .specify/specs/052-fast-fail-principle/requirements.md
status: error
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] fail (28)
  [marker-count] pass (0)
  [dup-id] pass (0)
  [path-marker] pass (0)
scanned: 597 lines, 93 definition rows, 13 shared strings
28 error(s), 0 warning(s)
EXIT=1
```

All 28 errors are `ref-resolvable` findings on the `Shared Strings` `Consumed by` cells (lines 469–481): each names FR/SC ids that do not cite `[[STR-xxx]]` back. **Pre-existing and outside this repair**: the same validator run against `git show HEAD:…/requirements.md` produced byte-identical findings (`28 error(s)`), and this repair touched none of those lines. Reported, not fixed — repairing Shared-Strings traceability is a requirements rewrite, not a path repair.

### `validate-tasks.py`

```
$ python3 scripts/python/validate-tasks.py .specify/specs/052-fast-fail-principle/tasks.md
WARN  161: parallel-safe: [P] task T014 ... WRITES ['specify/shared/guidelines/fast-fail.md'] while T015 ...
PASS (with warnings): .specify/specs/052-fast-fail-principle/tasks.md — 0 error(s), 1 warning(s)
EXIT=0
```

The single warning (T014/T015 `[P]` pair) is also pre-existing: the HEAD copy yields the same warning and the same `0 error(s)` / exit 0.

### Post-repair sweep

A normalized excerpt scan over the eight repaired files finds **0 remaining live dead path tokens**. The only surviving hits are the dated/non-reference classes tabulated above.

## 7. Change footprint

`git diff --stat -- .specify/specs/052-fast-fail-principle/`: 8 files changed, 37 insertions(+), 37 deletions(-) — every change is an in-line path substitution; no line added or removed, no number or reading altered, no file outside the spec directory touched. Scratch copies used for the HEAD-vs-now validator comparison were written under `.specify/.tmp/spec-repair-052/` and removed afterwards.

## 8. Anomaly

`validate-requirements.py` exits 1 on this spec with 28 `ref-resolvable` errors on the Shared Strings table — confirmed pre-existing at `HEAD` (identical output), untouched by this repair, and left as-is because fixing it is a requirements-traceability rewrite rather than a dead-reference repair.
