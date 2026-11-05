# Phase 0 Research: Self-Explanatory Framework Integration

**Feature**: 082-self-explanatory-integration | **Date**: 2026-11-05 | **Stage base**: `506adf88`

Every figure below was produced by running the stated command in this repository during the plan
stage. Where a figure can move between this stage and implementation time, the re-measurement command
is stated next to it so `/speckit.tasks` re-takes the value instead of inheriting it.

## Measured baseline (before any edit on this branch)

| # | Fact | Command | Reading |
|---|------|---------|---------|
| B-1 | Mirror state — **superseded within this stage, see B-7** | `python3 scripts/python/sync-mirrors.py --check` | First reading: exit **2**; `ok templates/` (22), `ok skills/external/` (409), `ok skills/internal/` (138), `ok agents/` (3), `ok scripts/` (119); exactly three `MISS` lines — `.specify/shared/definitions/self-explanatory-definitions.md`, `.specify/shared/guidelines/self-explanatory.md`, `.specify/shared/workflow/best-practice-optimization.md`; `OK: all per-tool command copies match the source templates.` |
| B-7 | Mirror state, re-measured later in the same stage | `python3 scripts/python/sync-mirrors.py --check` | exit **0**; `shared/ == .specify/shared/` now reports `ok` (65 files), i.e. the three mirrors exist and are byte-identical (`cmp` on all three pairs: identical; identical mtimes, both untracked at HEAD). The three files were created outside this run's reach — no `--write` was issued by the plan stage (see the timing note below) — so C-23's baseline is exit 0 and the implementation's duty is to **keep** it. |
| B-2 | Live instructions size vs budget | `wc -c .specify/instructions.md`; grep of the generator constant | live **32,739 B**; `INSTRUCTIONS_BUDGET_BYTES=32768` (`scripts/bash/generate-instructions.sh:38`, mirrored at `.specify/scripts/bash/generate-instructions.sh:38`); headroom **29 B** |
| B-3 | Roster sizes | `grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md .specify/memory/constitution.md` | template **17**; live constitution **18**; generator mandate list **10** entries (`skills/internal/manage-constitution/SKILL.md`, `- **MUST include**` block) |
| B-4 | Gate scanner | `python3 scripts/python/scan-confirmation-gates.py --json` | `total: 27` (`governance_kept` 7, `destructive` 20), `violations: []`; frozen baseline `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` → `confirmationGates.total: 23` |
| B-5 | Toolchain | `python3 --version`; `git --version`; `python3 -m pytest --version` | `Python 3.11.11`; `git version 2.43.5`; `pytest 8.4.2` |
| B-6 | Pre-existing failed node (independent of this feature) | `.specify/specs/074b-nested-governance` feature detail records the same node red with the same reading (27 vs 23) | `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` — red because of B-4, not because of this feature; MUST be reported by name in each stage's targeted evidence |

**Timing note (disclosed, not repaired).** Two readings (B-1 → B-7) differ inside one stage. The plan
stage ran `sync-mirrors.py --check` only — `--check` never writes — and the three mirror files were
created with the same mtime as their sources while this stage was otherwise reading files. Their
provenance is therefore *not* this stage's action and the plan does not claim it; what the plan does
record is the measured consequence: the mirror baseline this feature will be judged against is exit 0,
so the implementation's mirror obligation is "keep `--check` at exit 0", not "make it reach 0". Both
readings are kept rather than overwritten because the earlier one is why the plan's first draft stated
the obligation in `--write`-then-`--check` form.

## Resolved unknowns

### R-1 — How much must the budget constant move, and what exactly is measured

The generator measures the **live file** (`len(live_text.encode("utf-8"))`) against
`INSTRUCTIONS_BUDGET_BYTES` and writes one `BUDGET: <size> <budget> <over|within>` line plus a
per-section table (`scripts/bash/generate-instructions.sh`, `report_instructions_budget`). The
comparison operator on the report path is `>=` for the `over` verdict — a size exactly equal to the
budget already reports `over` — so the required post-change invariant is
`size <= budget - 1`, i.e. the report must print `within`.

**Decision**: the raise is computed, not chosen. The implementation measures the live file after the
section is injected (`S` bytes), then sets `INSTRUCTIONS_BUDGET_BYTES` to
`S + 1024` rounded **up** to the next multiple of 1024, and records in the commit body:

```text
budget: <old> -> <new> B; live after injection <S> B; reason: <section name> section
(<n> B rendered) landed while <headroom> B of headroom remained; raise = smallest
multiples-of-1024 figure leaving >= 1024 B headroom (T-001).
```

The 1024 B floor is the raise's own slack: a raise that leaves less than 1 KiB makes the *next*
section land in the same position, which is the "raise the constant casually on every new section"
failure T-001's `pole_b` names. The rounding keeps the constant readable and keeps the raise's
magnitude auditable at a glance. `tests/contract/test_instructions_size_budget.py` derives the number
from the script (`_BUDGET_RE`) and pins that the generator is the only definition point, so no test
needs editing for the raise; the tests that must still pass are the six report-shape tests in that
file, none of which pins a literal.

Re-measure at implementation time: `bash scripts/bash/generate-instructions.sh` and read the
`BUDGET:` line. Both readings (before, after) go into `test-evidence/`.

### R-2 — The gate-total drift is real, pre-existing, and not this feature's to repair

`scan-confirmation-gates.py --json` reports 27 (B-4) against a frozen 23. Two contract tests read
that number: `test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` (equality
against the frozen 23 → red today) and the suite-wide zero-hit assertions
(`test_clarify_semantic_completeness.py`'s surfaces, `test_constitution_double_landing.py::test_c13_*`).
Every current hit is on a surface this feature does not edit: `shared/definitions/`,
`shared/guidelines/`, `shared/patterns/`, `shared/workflow/`, `skills/`, `templates/commands/`.

**Decision** (also EP-003): (a) do not touch the frozen baseline or the pin — that measurement belongs
to Feature 050 and repairing it here folds an unrelated change into this feature; (b) make this
feature's own new text provably neutral instead of relying on the already-drifted total: the new
passages are written to produce **zero** `BLOCKING_RE` hits, which is mechanically checked before
landing (`python3 -c` snippet in `quickstart.md` S-4, and contract C-8 extends the double-landing
suite's existing zero-hit assertion to both new surfaces); (c) the implementation's targeted-run
evidence names the pre-existing failed node explicitly rather than reporting "clean".

The wording constraint this imposes is recorded so the writer does not have to rediscover it: a
constitution principle that adds a human-facing rule must avoid the scanner's blocking phrases
(`等待用户确认`, `stop and confirm`, `after user confirmation`, `MUST NOT execute before confirmation`,
`confirm before`, `proceed … yes/no`, and the rest of `BLOCKING_PATTERNS`). The probed candidate text
for this feature's principle produced zero hits.

### R-3 — Both surfaces carry the same literal, and the title matcher is numeral-agnostic

`test_constitution_double_landing.py` matches headings with
`^### ([IVXLC0-9]+)\. (.+)$` (roman or arabic), extracts the generator mandate list with
`^  - \*\*(.+?)\*\* —`, and asserts watchlist titles by **set membership** on both sides; C-8
asserts the matchers contain no pinned numeral. Adding `STR-001` to the watchlist is therefore
literally a one-entry change plus three count bumps (`TEMPLATE_COUNT` 17→18, `LIVE_COUNT` 18→19,
`COMMAND_COUNT` 10→11).

**Decision**: the new principle's **title** is `STR-001` verbatim on all three surfaces (template,
live constitution, generator mandate list) and the instructions section heading is the same literal —
T-002 records why the duplication is accepted. The `_check_structure` helper (C-2 a–g) applies to
every watchlist title via `NEW_TEMPLATE_TITLES`, so the new principle MUST satisfy: heading form
`### <numeral>. <title>`, a claim sentence ending in a colon before the first bullet, **3–6** logical
bullets each containing `MUST`, no physical line ≥ 100 chars, a blank line then a `Rationale:`
paragraph of 1–4 sentences with no intervening content, and no bracket placeholder. Those constraints,
not a stylistic preference, decide the principle's paragraph layout (five bullets: user perspective,
ceiling/floor and the floor's sufficiency, no preventive optimization, one dimension per task, original
source of truth).

### R-4 — Every mechanism already exists (Tool Reuse)

| Need | Existing mechanism | Path | Decision |
|------|--------------------|------|----------|
| Mirror the three owner documents | mirror engine, `shared → .specify/shared` pair | `scripts/python/sync-mirrors.py` (`MIRROR_PAIRS`) | reuse; `--write` then `--check`; no `--only` needed (nothing else is drifted) |
| Rewrite the budget constant | generator constant + report | `scripts/bash/generate-instructions.sh:38` | edit the single definition point; no new parameter |
| Inject the instructions section into the live file | additive section reconcile (top-level `## ` granularity) | same script, `RECONCILE_OUTPUT` block | reuse; injection is verbatim-rendered and idempotent |
| Amend the live constitution | template-guided path of the constitution skill | `skills/internal/manage-constitution/SKILL.md` | reuse; no new generator (spec Assumption A4 + FR-003) |
| Distribute the mirrored documents | `specify init` copies resource `shared/` → `<project>/.specify/shared/` | `src/specify_cli/__init__.py:2504-2516` | reuse; no code change |
| Guard the mirror pairs | parametrized suite deriving from `MIRROR_PAIRS` | `tests/contract/test_mirror_parity_suite.py` | reuse **without modification** — new source files become parameters automatically (FR-010 forbids a second table) |
| Guard the docs page's links | pytest link assertion over the page's inline-code paths | `tests/contract/test_constitution_double_landing.py` file conventions | extend an existing suite; no new link-check engine (FR-012) |

The one place a new assertion is written rather than extended is the instructions-propagation suite,
which today has exactly two tests (C-1 real-tree, C-2 mechanism) and has no mutation leg pointed at the
**template** side. FR-009 requires that leg; it lands as new tests in the existing module.

### R-5 — Distribution depends on source presence, and the mirror is not the distribution input

`specify init` copies the *resource* `shared/` tree (the packaged framework source), never
`.specify/shared/`. Consequences the implementation must respect:

1. A file that exists only under `.specify/shared/` is never distributed. The three owner documents
   are already in `shared/`, so the mirror step is about the *runtime* copy a client project gets
   inside its own `.specify/`, and `--check`'s `extra` reporting is the guard against mirror-only
   files (strict pairs fail on orphans; the `shared` pair is lenient and only notes them).
2. The init assertion (FR-007, SC-005) must run against a **packaged/installed** CLI, not against the
   worktree, and must list `.specify/shared/{definitions,guidelines,workflow}/<name>.md` in the fresh
   project. `quickstart.md` S-6 executes exactly this against the installed entry point and records
   the file listing.

### R-6 — Wording: what the projected surfaces may and may not say

Constitution XIV plus spec Assumption A2/A11 fix the shape of every projected surface:

- the concept **owner** path written on any client-facing surface is the runtime path
  `.specify/shared/definitions/self-explanatory-definitions.md` (`STR-004`), because the template is
  copied verbatim into a project whose only shared tree is that one;
- the framework-source path `shared/definitions/self-explanatory-definitions.md` (`STR-002`) appears
  only as the owner location in the framework's own documents, never as the resolution target of a
  client-facing pointer;
- the instructions section carries a **summary** (the principle restated in one or two sentences) plus
  the pointer, never the owner's sections; the constitution principle carries its five MUST bullets
  (its own normative text, which the owner does not define) plus the pointer.

`research.md` also records the gloss of each owner section the projected text leans on, so the writer
does not re-open the owner to invent wording: `definitions` § 1 (people-first, user view), § 2
(ceiling = direct view, floor = one simple command, floor sufficient), § 3 (not preventive; a concrete
information need is required), § 6 (encoded attribute keeps its original source; names/paths are
reconciled projections), § 7 (dimension order; at most one dimension per optimization task).

### R-7 — Glossary mechanism and the term's shape

`tests/contract/test_glossary_mechanism.py` guards the mechanism (template present + mirrored,
required structure, Documentation Map row, init round-trip) — it does not enumerate terms, so adding
`STR-003` needs no change there; the entry itself must satisfy the store's own schema
(`glossary-utils.py`), with `origin=auto` and `status=proposed` (spec Assumption A6). The retired name
`望文生义` enters as a **variant** of the canonical entry and MUST NOT appear as a second canonical
entry — contract C-30 asserts this by parsing the store rather than by substring search.

## Phase 0 output

No standalone interview round was required: every open question in the specification
(`[NEEDS CLARIFICATION]` count: 0, asserted by `requirements.md` § Assumptions A8) was answerable from
the repository or was already ratified upstream. The seven unknowns above were resolved by measurement
and are carried into `data-model.md` (rules V-1…V-19) and `contracts/` (C-1…C-34) as decidable
assertions.

## Re-measure list (for `/speckit.tasks` and `/speckit.implement`)

These figures are the ones most likely to move between stages; each is listed with the command that
re-takes it, per the execution-verify rule. A stage that inherits one of these values without
re-running its command is inheriting a claim, not measuring a fact.

| Figure | Re-measure with | Plan-stage reading |
|--------|-----------------|--------------------|
| mirror drift | `python3 scripts/python/sync-mirrors.py --check` (read the exit code, not the buffer) | exit 0 (B-7); exit 2 earlier in the stage (B-1) |
| live instructions size | `wc -c .specify/instructions.md` | 32,739 B (B-2) |
| budget constant | `grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh` | 32,768 (B-2) |
| roster counts | `grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md .specify/memory/constitution.md` | 17 / 18 (B-3) |
| mandate-list count | the block parser used by the double-landing suite (`_skill_entry_names`) | 10 (B-3) |
| gate total | `python3 scripts/python/scan-confirmation-gates.py --json` | 27, frozen baseline 23 (B-4) |
| toolchain | `python3 --version`, `git --version`, `python3 -m pytest --version` | 3.11.11 / 2.43.5 / 8.4.2 (B-5) |
