# Specification-Driven Development (SDD) Process Review Report: 087 架构图为核心的文档空间（Architecture-Diagram-Centric Documentation Space）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 087 |
| Requirement Key | 087-arch-diagram-docs |
| Requirement Name | 架构图为核心的文档空间（Architecture-Diagram-Centric Documentation Space） |
| Related Feature | 087 架构图为核心的文档空间（`Planned`) |
| Repository | spec-kit (worktree `087-arch-diagram-docs`, self-hosting framework repository) |
| Repository URL | remotes declared: `gitee` / `github` / `gitlab` = `cloud-native-ai/spec-kit`; `origin` = upstream `github/spec-kit` |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the review head is not pushed to any remote, so no URL citation can resolve. Cite absolute paths plus `git show 37d93787:<path>` recovery instructions instead. |
| Branch | `line/087-arch-diagram-docs` |
| Commit SHA | `37d937872613f97c5141bfb36e8bbc17e678dd1c` (short: `37d93787`) |
| Repo Root (absolute) | `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs` |
| Review Date | 2026-11-06 |
| Reviewer (Agent) | Qoder agent `sdd-review-executor` (unattended run; no user ruling in session) |
| Environment | Linux x86_64; bash; CPython 3.11.13; pytest 9.2.0; typer 0.27.3 |
| spec-kit Source Snapshot | this repository @ `37d93787` (diff base `24cb4edc`), project version `0.0.22` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 313 | `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/.specify/specs/087-arch-diagram-docs/requirements.md` | 23 FR / 10 SC / 5 user stories; A1–A12 assumptions; Clarifications 2026-11-06 |
| plan.md | 577 | `.../087-arch-diagram-docs/plan.md` | 19-row Constitution Check; T-001…T-005 decision tensions; Test Plan tables A/B; residual risk D-001 |
| tasks.md | 334 | `.../087-arch-diagram-docs/tasks.md` | 76 rows T001–T076; DoD-1…DoD-10; GATE-1…GATE-6; 39 machine-decidable `[green:]` claims |
| contracts/diagram-obligation.contract.md | 363 | `.../087-arch-diagram-docs/contracts/diagram-obligation.contract.md` | C-001…C-016: command surface, closed verdict/reason sets, C-016 precedence, records schema |
| contracts/flow-obligations.contract.md | 142 | `.../087-arch-diagram-docs/contracts/flow-obligations.contract.md` | C-001…C-023 plus C-008a: the two writing flows, command dispatch, reader projection |
| data-model.md | 190 | `.../087-arch-diagram-docs/data-model.md` | 8 entities E1–E8 and two state machines; E6 fixture composition table |
| quickstart.md | 333 | `.../087-arch-diagram-docs/quickstart.md` | S1–S9 scenarios with per-example premises; S9 reconcile convergence loop |
| research.md | 164 | `.../087-arch-diagram-docs/research.md` | R1–R7 measured findings (carrier population, engine shape, mirrors, guards) |
| feature-ref.md | 77 | `.../087-arch-diagram-docs/feature-ref.md` | Feature binding, delivery surfaces, FR→contract and SC→measurement maps |
| checklists/requirements.md | 53 | `.../087-arch-diagram-docs/checklists/requirements.md` | Requirements quality checklist, notes N1–N6 |
| checklists/requirements-quality.md | 175 | `.../087-arch-diagram-docs/checklists/requirements-quality.md` | 67 CHK items across ten quality dimensions |
| checkpoints/01…07 | 7 files | `.../087-arch-diagram-docs/checkpoints/` | Per-stage driver checkpoints with U4 evidence and goal/team review |
| test-evidence/ | 22 files | `.../087-arch-diagram-docs/test-evidence/` | Baseline, analyze round-1 report + repair, implement parts 1–5, stage-status rows |
| notes/ | 3 files | `.../087-arch-diagram-docs/notes/` | Pre-change measurements, red-first evidence, executed quickstart run |
| **verification.md** | **0 (absent)** | `.../087-arch-diagram-docs/verification.md` | **Missing expected member** — no SC status rows and no smoke record exist |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements stage | commits `779f1a9b` → `ac1ed706`; `checkpoints/01-requirements.md`: `U4: pass`; `validate-requirements.py` ok | One gate fail (missing Runtime Stack table) repaired in attempt 2, disclosed |
| 2 | clarify stage | commit `e5bc0764`; `checkpoints/02-clarify.md`; requirements bound to new Feature 087; A11/A12 ratified | One directory-listing misstatement corrected in place and disclosed |
| 3 | plan stage | commits `7663ea5b` → `c7b58681` → `3cff4a03` → `61e39e8f`; `checkpoints/03-plan.md` | Four verifier rounds; rounds 1–3 returned `PLAN-VERIFY: fail`; round 4 passed by findings despite a contradictory first line |
| 4 | tasks stage | commit `7c951c23`; `checkpoints/04-tasks.md`; `audit-plan-changes.py --base 61e39e8f` → `undeclared=false`; 76 rows | Two tasks feedback entries: one lacked `--feature`, a second was recorded and the first kept as a disclosed defect |
| 5 | checklist stage | commit `25b90479`; 67 CHK; `OI-087-01` resolved by deleting the count copy (N6) | Checklist worker used bare `/tmp/w087/` staging; `git commit --amend` + `reset --soft` correction, both disclosed |
| 6 | analyze round 1 | `test-evidence/analyze-report-round1.md`: 0 CRITICAL / 2 HIGH / 7 MEDIUM / 7 LOW; repair commit `7b6b6cc6`; coverage baseline 573 | A bounded repair round was run between analyze and implement |
| 7 | analyze round 2 | `checkpoints/06-analyze.md`: 0 CRITICAL / 0 HIGH / 4 MEDIUM / 7 LOW; `analyze-stage-status.jsonl` | Round-2 report itself is not on disk; the row points to a "round-2 return report" that does not exist |
| 8 | implement part 1 (T001–T016) | commits `33a53e3d`, `2129e0d4`, `8a151cbf`, `8d0e0ba9`; 11 fixtures + builder + 13 reds; engine action | plan.md/data-model.md edits; Part 1 declares two corrections in prose, not `PLAN-EDIT:` lines; the `/tmp/087-toolenv` → `/usr/bin/python3` change is undeclared |
| 9 | implement part 2 (T017–T032) | commit `e51a2bd8`; engine tiers; four test files; plan test-file budget raised to 4 with 4 `PLAN-EDIT:` lines | Commit message groups a large behaviour batch; no per-task commit grouping |
| 10 | mirror sync | commit `8fa3252a`; `sync-mirrors.py --write` reportedly reproduced the tree byte for byte | No deviation; a no-op parity pass |
| 11 | implement part 3 (T033–T048) | commit `b8651591`; baseline/reconcile wiring; 10 declared reds carried to Part 4 | Declared reds are recorded, not silenced |
| 12 | implement part 4 (T049–T064) | commit `4945a550`; improve-docs + docs.md + reader projection; five 087 files 121 passed | Part 4 re-measured T054 as already covered by T048 instead of rewriting it |
| 13 | implement part 5 (T065–T076) | commit `e17eee90`; exact guard node id 1 passed; US5 4 passed; 121 passed / 1 baseline failure; mirrors/copies byte-identical; quickstart S1–S9 walked | Three quickstart corrections recorded in `notes/quickstart-run.md`; T076's docs-only premise marked void |
| 14 | implement checkpoint | commit `37d93787`; `checkpoints/07-implement.md`: `U4: pass`; 76/76 `[x]`; `baseline` slot seq=1 (26 failed / 7471 passed / 4 skipped); **verification.md does not exist** | Stage closed as U4 pass without GATE-4/DoD-3's required file — the central process gap |
| 15 | review (this run) | this report + `code-review.md`; code receipt `changed=177 / judged=11 / skipped=166 / gap=0`; `verdict=blocked`; closure checker exit 2 | Review only: targeted sets, no full suite; no P0/P1 repaired locally |

## 2. Findings Summary

**Process segment verdict**: `blocked` — the implement stage's U4 pass is not supported by its own required artifact (`verification.md`), and the analyze round-2 evidence pointer is not resolvable from disk. The artifact segment independently records the missing member as `F1` at `P0`; the implementation and code segments are blocked by the checker defects below.

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 6 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 18 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 7 |
| Workflow | 5 |
| Documentation | 13 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `24cb4edcc53db3cfc86f574e5e6d627c78b2ca08` | the resolved diff base |
| Head commit | `37d937872613f97c5141bfb36e8bbc17e678dd1c` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 177 / 11 / 166 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `blocked` | `blocking` entries: 2 (plus 6 `important`, 1 `suggestion`) |
| Gate verdict | `blocking-unresolved` | `report --summary --file` returned `gate=deny`, exit 1 |
| Reason, when one applies | Two `blocking` entries: the recognisable-diagram suffix list misses the delivery contract's HTML/PDF/drawio/excalidraw faces; a reference to the editable source is reported `satisfied` even though C-007 requires a rendered face | `code-review.md` |
| Uncommitted scope | 39 uncommitted paths disclosed and not reviewed: pre-existing session records, exec-quant/feedback runtime records, and this run's `test-evidence/review-smoke.txt`; the full list lives in the record's disclosure line and in `git status` | same |
| Record | `.specify/specs/087-arch-diagram-docs/code-review.md` | written because the triage value is `run` |
| Archive | `none` | first code-segment record for this slice |

This subsection carries the verdict and the pointers only: no opinion body, no per-severity item count beyond the six-level summary above. The findings themselves live in `code-review.md` and are read there.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `feature-ref.md`, `test-evidence/`, `checklists/` | union of the standard spec-stage product, this plan's § Project Structure additions, and the checklist stage's product |
| Coverage line | 10 / 11 | ten expected members present on disk; `verification.md` is absent |
| Missing members | `verification.md` | absent from disk; it is also the closure checker's first required input |
| Segment verdict | `blocked` | a missing expected member plus two normative contradictions (F2, F3) |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P0 | `.specify/specs/087-arch-diagram-docs/verification.md` | — | The file does not exist on disk (absence is the finding); no line can be cited | No SC status rows and no smoke record; `closure-acceptance-check.py` exits 2; the implement stage's GATE-4/DoD-3 cannot be satisfied; see F1 |
| P1 | `.specify/specs/087-arch-diagram-docs/requirements.md` | 289 | — | Out of Scope still says the repo's `docs/` content is not changed, while FR-001/T064 deliver exactly one `docs/` file; propagated to plan.md:32/81 and feature-ref.md:72; see F2 |
| P1 | `.specify/specs/087-arch-diagram-docs/data-model.md` | 93 | — | E6's "repository copy == registered composition" contradicts the plan/tasks/quickstart "pre-deletion green state" wording; DoD-4 is unsatisfiable as written; see F3 |
| P2 | `.specify/specs/087-arch-diagram-docs/plan.md` | 449 | — | Table B names four assertions that no test file defines (`test_c003_record_same_run`, `test_c003_missing_record_not_satisfied`, `test_c018_improve_docs_literal_kept`, `test_c018_w1_section_byte_unchanged`); see F12 |
| P2 | `.specify/specs/087-arch-diagram-docs/feature-ref.md` | 30 | — | Row 10 still lists the retired `.specify/templates/commands/docs.md`; row 75 still calls `OI-087-01` an open item; see F13 |
| P2 | `.specify/specs/087-arch-diagram-docs/data-model.md` | 46 | — | `verdict` is attributed to `C-004` "closed five + ordered priority", but C-016 is the sole precedence owner; see F14 |
| P2 | `.specify/specs/087-arch-diagram-docs/quickstart.md` | 308 | — | S8 cites `plan.md § Delivery Surfaces`; contract C-014 cites `plan.md § Definition of Done`; neither section exists; see F15 |
| P2 | `.specify/memory/features/087.md` | 69 | — | Related Specifications says the checker contract has `C-001…C-015` and quickstart has `S1–S8`; the artifacts have 16 clauses and 9 scenarios; see F16 |
| P2 | `.specify/specs/087-arch-diagram-docs/quickstart.md` | 145 | — | S3 prints a record filename the fixtures do not carry and a `--record` form that joins the root twice; the three corrections live only in `notes/quickstart-run.md`; see F17 |
| P2 | `.specify/specs/087-arch-diagram-docs/plan.md` | 517 | — | The plan's known-red row says "17 known-red" while the driver's full-suite baseline is 26 (17 `tests/contract` + 9 `tests/unit`); see F18 |
| P2 | `.specify/specs/087-arch-diagram-docs/contracts/flow-obligations.contract.md` | 13 | — | The contract still says the `#### Assets` subsection "当前不在盘"; after delivery it is on disk; see F19 |
| P2 | `.specify/specs/087-arch-diagram-docs/checklists/requirements.md` | 17 | — | Says "FR-014's four verdict values" (there are five) and "A1–A10" (requirements has A1–A12); see F20 |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `24cb4edcc53db3cfc86f574e5e6d627c78b2ca08` | the resolved diff base |
| Head commit | `37d937872613f97c5141bfb36e8bbc17e678dd1c` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `/usr/bin/python3 -m pytest tests/unit/test_docs_utils_obligation.py tests/unit/test_docs_utils_carriers.py tests/unit/test_docs_obligation_reuse.py tests/integration/test_docs_obligation_scenarios.py tests/integration/test_docs_command_scenarios.py -q --no-header -p no:cacheprovider --tb=no -rf` | recorded verbatim |
| Smoke exit code | `0` | `121 passed, 1 warning in 4.68s` |
| Smoke evidence path | `.specify/specs/087-arch-diagram-docs/test-evidence/review-smoke.txt` | exists and is non-empty; also holds the guard set, fixture check, and scope readings |
| Scope and regression verdict | Scope: one unrequested behaviour change (F21) and one declared-floor regression (F22); regression: no new guard failure (1 baseline name / 120 passed), fixtures 11/11, mirrors 6/6 + four per-tool copies byte-identical, `docs/` exactly one line, `draw-diagram` zero diff | measured in `review-smoke.txt` and the code record |
| Segment verdict | `blocked` | two correctness gaps in the checker's core judgement (F4, F5) and a portability defect in the shipped skill text (F6) |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `skills/external/create-docs/scripts/docs-utils.py` | 656 | — | Tier 9 reports a source-only reference as `satisfied`; C-007 condition 2 requires a `rendered[].path`; see F4 |
| P1 | `skills/external/create-docs/scripts/docs-utils.py` | 402 | — | The suffix list omits the D1 HTML face and the D2 drawio/excalidraw/pdf faces; conformant deliveries are false-red; see F5 |
| P1 | `skills/external/create-docs/SKILL.md` | 61 | — | The shipped skill links the obligation to `../../specs/087-arch-diagram-docs/contracts/...`, a path no client project receives; the record schema is unreachable; see F6 |
| P2 | `skills/external/create-docs/scripts/docs-utils.py` | 791 | — | The new global `--root` existence check changes existing actions' exit codes from 0 to 2 on a missing root; see F21 |
| P2 | `skills/external/create-docs/scripts/docs-utils.py` | 520 | — | `str.removeprefix` (520) and `Path.is_relative_to` (604) are 3.9+ APIs against a declared `>=3.8` floor; see F22 |
| P2 | `skills/external/create-docs/scripts/docs-utils.py` | 429 | — | Fenced-code removal deletes newlines and shifts the reported reference line (9 → 5 in the probe); see F23 |
| P2 | `tests/integration/test_docs_obligation_scenarios.py` | 539 | — | SC-001's reference assertion accepts any `../assets/` link and would pass a source reference; see F24 |
| P2 | `tests/fixtures/docs-obligation/build_fixtures.py` | 295 | — | `check()` verifies only path presence/absence; a bare `--help` runs `build_all()` and rewrites a fixture record while `--check` still reports OK; see F25 |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Planned` | `.specify/memory/features/087.md` line 6 and `.specify/memory/features.md` line 94, copied |
| `final_path` record, copied verbatim (7/7) | **not produced** — `closure-acceptance-check.py --spec-dir .specify/specs/087-arch-diagram-docs --json` exited 2 with `input error: required input not found: .../verification.md` | the checker returned an input error, not a verdict; no bucket was recomputed or invented |
| Comparison verdict | `not-evaluated (input error)` | the checker's own refusal; a missing input is never reported as `block` and never as `accept` |
| Failed condition, on refusal | `verification.md` is absent, so the `Planned → Implemented` completeness condition ② and the smoke-record condition ④ cannot be evaluated, and the `Implemented → Ready for Review` judgement has no `final_path` input | named condition, not merely "the transition was refused" |
| Fixed item, on refusal | `none` | `F-ACCEPTANCE` fires only when the claim is `Implemented` or `Ready for Review` and the `pass` bucket reads zero; the claim is `Planned`, so the item does not fire |

## 3. Findings (Problems & Improvement Targets)

### F1 — The expected artifact set has no `verification.md`, so the feature's acceptance has no status rows and the ARC has no input

- **Severity**: P0 (validated: direct re-read, subagent unavailable — the run's dispatch constraint forbids a validation subagent; the absence was re-checked with `test -f` and the checker's own error)
- **Category**: Workflow
- **Location**: `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/.specify/specs/087-arch-diagram-docs/verification.md` (absent); `checkpoints/07-implement.md`; `tasks.md:37`
- **Evidence** (verbatim quote):

  ```
  $ python3 .specify/scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/087-arch-diagram-docs --json
  closure-acceptance-check: input error: required input not found:
    .../.specify/specs/087-arch-diagram-docs/verification.md
  exit 2

  tasks.md T075: "verification.md does not exist, so no SC-NNN_status row exists at all and none can be claimed."
  ```
- **Why it's a problem**: `verification.md` is the one artifact that turns the ten success criteria into a decidable status table; the implement stage's own GATE-4/DoD-3 require it, and the closure checker cannot produce the `final_path` record without it. The stage still closed as `U4: pass`, so the missing member is the first thing every later stage inherits.
- **Proposed fix**: seed `verification.md` from `.specify/templates/verification-log-template.md` at the start of `/speckit.implement`, fill one status row per SC with the honest reading (including `blocked`/`unknown` where the measurement is absent), record the three-field smoke triple, and refuse `U4: pass` while the file is absent.

### F2 — The repository's own `docs/` content is declared out of scope in three places while FR-001 delivers exactly one file

- **Severity**: P1
- **Category**: Documentation
- **Location**: `requirements.md:289` (primary), `plan.md:32` and `:81`, `feature-ref.md:72`
- **Evidence** (verbatim quote):

  ```
  requirements.md:289: "不改动本仓 `docs/` 树的内容——本线是框架改动（Two Hats），`docs/` 与 `.specify/` 只接受生成/镜像；把本仓文档逐份补图属内容工作，A6 已排除。"
  feature-ref.md:72: "本特性**不改**本仓 `docs/` 的内容（Two Hats：框架改动）；`.specify/` 只接受生成。"
  ```
- **Why it's a problem**: FR-001 and T064 require the reader projection in `docs/concepts/documentation-model.md`, and the implementation delivered exactly that one line. The three quoted sentences say the opposite without naming the one-file exception; a maintainer following the spec would reject the delivered change (analyze round-2 M2, still open).
- **Proposed fix**: narrow the Out of Scope bullet to "except the one `docs/concepts/documentation-model.md` reader projection FR-001 requires" and propagate the same wording to `plan.md` § Technical Constraints and `feature-ref.md`; do not widen the delivery to other docs files.

### F3 — The fixture invariant is stated in two incompatible ways, making DoD-4 unsatisfiable as written

- **Severity**: P1
- **Category**: Documentation
- **Location**: `data-model.md:93` (owner) versus `plan.md:493`, `tasks.md:22` (DoD-4), `tasks.md:77` (T005), `quickstart.md:165`
- **Evidence** (verbatim quote):

  ```
  data-model.md E6: "仓库副本 == E6 表登记的构成；任何用例造成的差异只允许存在于 `tmp_path`。"
  tasks.md DoD-4: "the repository copy of each is the pre-deletion green state"
  tasks.md T005: "every space is the **pre-deletion green state** so the repository copy is never mutated by a test"
  ```
- **Why it's a problem**: nine of the eleven fixtures are registered as red by design (`deleted-rendered/`, `orphan-*`, `no-diagram/`, `no-trace/`, `trace-incomplete/`, `exempt-bad/`, `exempt-superseded/`), so "each is the pre-deletion green state" is false; the checker `build_fixtures.py --check` correctly enforces the E6 reading. A DoD that cannot be satisfied is a false gate (analyze round-2 M3, still open in four places).
- **Proposed fix**: replace the four stale readings with the E6 reference ("repository copy == the composition E6 registers; test-induced differences exist only in `tmp_path`") and keep the E6 table as the sole owner.

### F4 — A document that links the editable source is reported `satisfied` even when the rendered face exists

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `skills/external/create-docs/scripts/docs-utils.py:656` (tier 9) with `_trace_entry_for` at `:568`; test gap at `tests/integration/test_docs_obligation_scenarios.py:539`
- **Evidence** (verbatim quote):

  ```
  clean/ copy, document reference changed from ../assets/widget.svg to ../assets/widget.mmd:
  {'path': 'docs/concepts/widget-overview.md', 'line': 5,
   'verdict': 'satisfied', 'reason': 'reference-resolves'}
  ```
- **Why it's a problem**: FR-005 says the document MUST reference the **rendered artifact** by a relative path, and C-007 condition 2 requires the referenced file to be a same-named `rendered[].path`. The checker matches the record entry by `source` too and then falls through to tier 9, so a source-only reference is a full pass; the `test_sc001` assertion only looks for `../assets/` and `](`, so it cannot catch this. This is a false green on the feature's central obligation (also `code-review.md` blocking #2).
- **Proposed fix**: before tier 9, require the resolved reference target to be one of the entry's `rendered[].path` values (a source reference with both faces present should land a named `missing` reason, or the contract needs a new explicit tier); add a negative fixture and tighten the SC-001 assertion.

### F5 — The recognisable-diagram suffix list omits the delivery contract's mandatory HTML face and the drawio/excalidraw/pdf faces

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `skills/external/create-docs/scripts/docs-utils.py:402` (used at `:448`)
- **Evidence** (verbatim quote):

  ```
  DIAGRAM_SUFFIXES = (".mmd", ".mermaid", ".puml", ".plantuml", ".svg", ".png", ".dot", ".gv", ".dotx")

  draw-diagram delivery-contract.md D1: "每次绘图交付 MUST 含一个可直接打开的 HTML 文件"
  D2: drawio source `.drawio` / rendered `.svg` / `.png` / `.pdf`; excalidraw source `.excalidraw`
  ```
- **Why it's a problem**: a conformant delivery that links `widget.html` (the D1 entry), `widget.drawio`/`widget.excalidraw` (the D2 source) or `widget.pdf` (a D2 render) is invisible to the checker and is reported `missing` / `no-diagram-reference`. The hard-coded list is a second, incomplete copy of the delivery contract, exactly the duplication FR-011 forbids; the probes on a `clean/` copy reproduced all three false reds (also `code-review.md` blocking #1).
- **Proposed fix**: derive the recognisable suffix set from `skills/external/draw-diagram/references/delivery-contract.md` (or add `.html`, `.pdf`, `.drawio`, `.excalidraw` with the owner cited), add fixtures for the HTML and drawio faces, and keep `draw-diagram` as the sole extension-table owner.

### F6 — The shipped skills link the obligation to a spec-local contract no client project receives

- **Severity**: P1
- **Category**: Documentation
- **Location**: `skills/external/create-docs/SKILL.md:61`, `:62`, `:63`, `:69`; `skills/external/improve-docs/SKILL.md:57`
- **Evidence** (verbatim quote):

  ```
  create-docs/SKILL.md:61: "The set is owned by the carrier table of
    [`contracts/diagram-obligation.contract.md`](../../specs/087-arch-diagram-docs/contracts/diagram-obligation.contract.md) § `C-003`"
  improve-docs/SKILL.md:57: "whose verdict vocabulary and reason table are owned by
    [`contracts/diagram-obligation.contract.md`](../../specs/087-arch-diagram-docs/contracts/diagram-obligation.contract.md)"
  ```
- **Why it's a problem**: `skills/external/<name>/` is installed into a client as `.specify/skills/<name>/` (the flat runtime layer), so the relative link resolves to `.specify/specs/087-arch-diagram-docs/contracts/...`. That is this repository's development spec, not a shipped asset; in every client project the link is dead and the trace-record schema, carrier table and exemption schema the skill names are unreachable. This is a Two Hats violation in the primary delivered surface (also `code-review.md` important).
- **Proposed fix**: move the normative schema/table into a shipped reference (for example `skills/external/create-docs/references/diagram-obligation.md`) or inline the record schema in the skill; keep the spec contract as the dated design record and cite it only as history.

### F7 — The implement stage closed `U4: pass` while GATE-4/DoD-3 were unmet

- **Severity**: P1
- **Category**: Workflow
- **Location**: `checkpoints/07-implement.md`; `tasks.md:37` (GATE-4), `tasks.md:21` (DoD-3)
- **Evidence** (verbatim quote):

  ```
  checkpoints/07-implement.md: "U4: `pass` — 76/76 任务 `[x]`；零未勾选；`validate-tasks.py` PASS 0/0; …"
  tasks.md GATE-4: "in `verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` … are all present"
  ```
- **Why it's a problem**: the stage's own completion gate requires an artifact that does not exist; the checkpoint discloses the absence but still records the stage as passed. A later stage then treats a stage whose acceptance surface was never produced as a sound predecessor, which is the same failure mode the acceptance-hardening workflow exists to prevent (F1 is its artifact-side consequence).
- **Proposed fix**: gate `U4: pass` on `verification.md` existing with all SC rows and the smoke triple, or record the stage gate as `not-met` and carry the gap explicitly into the next stage instead of a pass.

### F8 — The analyze round-2 evidence pointer names a report that is not on disk

- **Severity**: P2
- **Category**: Workflow
- **Location**: `test-evidence/analyze-stage-status.jsonl:1`; the findings themselves are in `checkpoints/06-analyze.md`
- **Evidence** (verbatim quote):

  ```
  "evidence_ptr": "… analyze-report-round1.md + analyze-repair-round1.md + this row;
   round-2 findings (0 CRITICAL / 0 HIGH, 4 MEDIUM, 7 LOW) carried in the analyze-stage round-2 return report"
  ```
- **Why it's a problem**: no `analyze-report-round2.md` exists; the M1–M4/L1–L7 list survives only in the driver checkpoint, not in the analyze stage's own evidence set. A later reader following the pointer finds nothing and cannot reconstruct the findings from the stage that produced them.
- **Proposed fix**: write the round-2 report to `test-evidence/analyze-report-round2.md` and update the pointer, or make the checkpoint the declared evidence target and stop citing a return report.

### F9 — The active plan constraint was not re-audited at implement close, and one plan-owned edit is undeclared

- **Severity**: P2
- **Category**: Workflow
- **Location**: `checkpoints/04-tasks.md` (last recorded audit); commits `8d0e0ba9`, `e51a2bd8`; `implement-part1.txt` § 7
- **Evidence** (verbatim quote):

  ```
  checkpoints/04-tasks.md: "plan constraint 审计：`audit-plan-changes.py --base 61e39e8f --head HEAD` → `undeclared=false`"
  implement-part1.txt § 7: "Two corrections this stage is making to plan-owned text (declared as PLAN-EDIT)"
  ```
- **Why it's a problem**: the plan constraint is `active@61e39e8f`, but the implement stage changed `plan.md`/`data-model.md` after that audit. Part 1 declares two corrections in prose (not `PLAN-EDIT:` lines), and the `/tmp/087-toolenv` → `/usr/bin/python3` interpreter edit in `plan.md` is not declared at all. The final audit is never recorded, so a reader cannot mechanically separate declared minor edits from undeclared changes.
- **Proposed fix**: run `audit-plan-changes.py` at every stage close (including implement), require the `PLAN-EDIT:` line form, and declare the interpreter-path edit as minor.

### F10 — Plan/checklist scratch used bare `/tmp` paths

- **Severity**: P2
- **Category**: Workflow
- **Location**: `test-evidence/plan-stage-status.md` (`/tmp/087-toolenv/bin/python`); `checkpoints/05-checklist.md` (`/tmp/w087/`)
- **Evidence** (verbatim quote):

  ```
  plan-stage-status.md: "Interpreter: /tmp/087-toolenv/bin/python → CPython 3.11.13 …"
  checkpoints/05-checklist.md: "checklist worker 无文件写入工具，用 `/tmp/w087/` 暂存后 `cat` 合并进工作区"
  ```
- **Why it's a problem**: `.specify/shared/guidelines/temp-directory-discipline.md` § 2 forbids bare `/tmp/...`; the sanctioned roots are `~/tmp/<project>/<purpose>/` and `.specify/.tmp/<purpose>/`. Both uses are recorded and cleaned, so no artifact was damaged, but the practice recurs and is copied by later agents.
- **Proposed fix**: use a sanctioned root, state the purpose in the path, and add the cleanup rule to the stage evidence template.

### F11 — The analyze repair evidence records 84 advisories while the round-2 reading is 77

- **Severity**: P2
- **Category**: Documentation
- **Location**: `test-evidence/analyze-repair-round1.md:129`; `test-evidence/analyze-stage-status.jsonl:1`
- **Evidence** (verbatim quote):

  ```
  analyze-repair-round1.md: "pre-analyze-check.py --stage tasks … advisories=84 waived=0"
  analyze-stage-status.jsonl: "pre-analyze-check.py --stage tasks (pass, errors 0, advisories 77)"
  ```
- **Why it's a problem**: two readings of the same gate disagree by seven, with no commit or date separating them; a later reader cannot tell which one belongs to the repaired tree. This is a dated-record defect, not a gate failure.
- **Proposed fix**: mark the 84 as the pre-repair reading and the 77 as the round-2 reading (or re-run and paste both with their commits); never leave two unlabelled numbers for one gate.

### F12 — Four plan-named assertions have no test function

- **Severity**: P2
- **Category**: Documentation
- **Location**: `plan.md:449` (C-003) and `:465` (C-018); compare `tests/integration/test_docs_command_scenarios.py:297`, `:669`, `:789`; `tests/unit/test_docs_utils_obligation.py:822`
- **Evidence** (verbatim quote):

  ```
  plan.md C-003: "`F::test_c003_record_same_run` … `I::test_c003_missing_record_not_satisfied`"
  plan.md C-018: "`F::test_c018_improve_docs_literal_kept` … `F::test_c018_w1_section_byte_unchanged`"
  actual definitions: `test_c003_same_run_wording`, `test_c007_no_record_not_satisfied`,
    `test_c018_hard_constraints_kept`, `test_c018_top_level_sequence_unchanged_and_confirm_literal_kept`
  ```
- **Why it's a problem**: `plan.md` is the sole owner of assertion names, and its Test Plan claims every clause has a named assertion. Four names resolve to nothing; the behaviour may be covered under other names, but the mapping is no longer mechanically checkable (analyze M1, partially open).
- **Proposed fix**: rename the four test functions to the plan's names (or update table B to the implemented names) and add a mechanical name-resolution check to the plan gate.

### F13 — `feature-ref.md` still lists a retired mirror path and an already-resolved open item

- **Severity**: P2
- **Category**: Documentation
- **Location**: `feature-ref.md:30`, `:75`
- **Evidence** (verbatim quote):

  ```
  feature-ref.md:30: ".specify/skills/create-docs/**、.specify/skills/improve-docs/**、
    .specify/templates/commands/docs.md，加四家 per-tool 命令副本 …"
  feature-ref.md:75: "`checklists/requirements.md` 的派生计数漂移**本阶段不改**，登记为未决项（`OI-087-01`）"
  ```
- **Why it's a problem**: `.specify/templates/commands/` is a retired subtree (the plan's Mirror Obligations says both sides are gone), and `OI-087-01` is `resolved` in `register.md` and closed by checklist N6. The feature-ref is the binding map a later reader uses to find mirrors and open items (analyze L1/L2, only partially repaired).
- **Proposed fix**: remove the retired path from row 10, list only the four per-tool copies, and change row 75 to the resolved status with the N6 pointer.

### F14 — `data-model.md` still attributes the precedence order to `C-004`

- **Severity**: P2
- **Category**: Documentation
- **Location**: `data-model.md:46`
- **Evidence** (verbatim quote):

  ```
  | `verdict` | `C-004`（封闭五值 + 有序优先级） | `satisfied` / `missing` / `stale` / `recorded-exemption` / `not-evaluated` |
  ```
- **Why it's a problem**: after the analyze repair, `C-004` owns only the closed five-value set; the ordered precedence is owned solely by `C-016`. A second attribution is a second owner and will drift (analyze L3, still open).
- **Proposed fix**: change the owner cell to "C-004 (closed five values); order owned by C-016" and keep the E3 state-machine paragraph pointing at C-016.

### F15 — Two artifacts cite plan sections that do not exist

- **Severity**: P2
- **Category**: Documentation
- **Location**: `quickstart.md:308`; `contracts/diagram-obligation.contract.md:322`
- **Evidence** (verbatim quote):

  ```
  quickstart.md S8: "`plan.md` § Delivery Surfaces 列出它"
  diagram-obligation.contract.md C-014: "读数见 `plan.md` § Definition of Done"
  ```
- **Why it's a problem**: the plan has no `## Delivery Surfaces` and no `## Definition of Done` heading; the first is § Project Structure / Source Code, the second lives in `tasks.md` DoD-1…DoD-10. A reader following either pointer lands nowhere (analyze L5, still open).
- **Proposed fix**: cite the real section (`plan.md` § Project Structure) or the real owner (`tasks.md` § Definition of Done), or add the missing headings if they are intended.

### F16 — The bound feature detail misstates the contract and quickstart sizes

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/memory/features/087.md:69`
- **Evidence** (verbatim quote):

  ```
  "`contracts/diagram-obligation.contract.md`（`C-001`…`C-015`，检查器取值域 owner）… `quickstart.md`（S1–S8）"
  ```
- **Why it's a problem**: the contract now has `C-001…C-016` and quickstart has S1–S9. The feature detail is the binding record later sessions read; stale sizes there are the exact drift the One Source Of Truth rule forbids.
- **Proposed fix**: update the two pointers to `C-001…C-016` and `S1–S9` (or remove the counts and cite the owner).

### F17 — The quickstart's S3 commands are not reproducible as printed

- **Severity**: P2
- **Category**: Documentation
- **Location**: `quickstart.md:145`; corrections in `notes/quickstart-run.md` § 3
- **Evidence** (verbatim quote):

  ```
  quickstart.md S3: "docs/.speckit/runs/20261106T000000Z-aaaaaaaa-diagram-trace.json"
  notes/quickstart-run.md: "the fixtures carry …/20261106T090000Z-0870a1b2-diagram-trace.json …
    Against the printed name S3's commands exit 2 (`--record is not readable`)"
  ```
- **Why it's a problem**: a quickstart is an executable contract; as printed, the record filename is absent and the `--record` path is joined under `--root` twice (repository-relative value with a fixture root). The three corrections are recorded only in the notes, so a reader who follows the quickstart gets failures.
- **Proposed fix**: apply the three corrections to `quickstart.md` (record filename, root-relative `--record`, stale-source-on-a-copy premise) or insert a dated correction note at the block that a reader cannot miss.

### F18 — The plan's known-red baseline (17) and the driver's full-suite baseline (26) use different denominators without saying so

- **Severity**: P2
- **Category**: Documentation
- **Location**: `plan.md:517`; `test-evidence/baseline-failed.txt`
- **Evidence** (verbatim quote):

  ```
  plan.md § Residual Risk: "仓库既有失败集 | 17 项已知红（与本特性无关，实施期不修、不计入本特性的红）"
  baseline-failed.txt: 26 names (17 under tests/contract, 9 under tests/unit/test_loop_state_engine.py)
  ```
- **Why it's a problem**: the plan's 17 is the `tests/contract` subset measured in research R6; the implement stage correctly compares against the 26-name full-suite baseline. A reader who takes "17" as the full-suite baseline sees nine unit failures as new.
- **Proposed fix**: qualify the plan row as "17 in tests/contract (research R6); the full-suite baseline is 26 names, recorded in baseline-failed.txt" and keep the implement comparison at 26.

### F19 — The contract still says the `#### Assets` subsection is not on disk

- **Severity**: P2
- **Category**: Documentation
- **Location**: `contracts/flow-obligations.contract.md:13`; also `plan.md:84`
- **Evidence** (verbatim quote):

  ```
  flow-obligations.contract.md: "`skills/external/create-docs/SKILL.md` § Desired-State Baseline **当前没有** `#### Assets` 小节（实测 2026-11-06 …）"
  ```
- **Why it's a problem**: the delivered `create-docs/SKILL.md` now contains the `#### Assets` subsection, and it is the area-convention owner. The note was true at plan time but is now a stale reading that a contract reader will take as current.
- **Proposed fix**: mark the note as a dated pre-implementation reading ("at plan time; the section landed in T038") or remove it and point at the delivered section.

### F20 — The requirements checklist contains two stale counts

- **Severity**: P2
- **Category**: Documentation
- **Location**: `checklists/requirements.md:17`, `:24`
- **Evidence** (verbatim quote):

  ```
  line 17: "FR-014's four verdict values are a closed set."
  line 24: "§ Assumptions carries A1–A10 with an explicit verdict token each"
  ```
- **Why it's a problem**: FR-014 defines five verdict values (and FR-014 itself says five), and the requirements has A1–A12. The checklist was generated before the clarify additions and never re-derived; its owner is `/speckit.checklist`, so this review records it rather than editing it.
- **Proposed fix**: update the two readings (five values, A1–A12) or replace them with a pointer to `requirements.md`; add a re-derivation step to the checklist stage when assumptions change.

### F21 — The new global `--root` existence check changes every existing action's exit code

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `skills/external/create-docs/scripts/docs-utils.py:791`
- **Evidence** (verbatim quote):

  ```
  base 24cb4edc:  $ docs-utils.py --action validate --root /nonexistent  -> exit 0, {"violations": []}
  new  37d93787:  $ docs-utils.py --action validate --root /nonexistent  -> exit 2, "--root does not exist"
  ```
- **Why it's a problem**: the feature's contract C-015 says `validate`'s exit-code semantics are unchanged; the guard is applied to every non-`obligation` action even though the obligation branch already has its own check. Existing callers that rely on an empty report for an absent root now get a hard error, and no task row asked for it.
- **Proposed fix**: scope the check to `obligation` (or move it inside `cmd_obligation`), and if the global behavior change is wanted, declare and test it separately.

### F22 — The new action uses Python 3.9+ APIs while the project declares `>=3.8`

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `skills/external/create-docs/scripts/docs-utils.py:520` (`str.removeprefix`), `:604` (`Path.is_relative_to`); also `tests/fixtures/docs-obligation/conftest.py:80`
- **Evidence** (verbatim quote):

  ```
  pyproject.toml: requires-python = ">=3.8"
  requirements.md RS-001: "新增与改动的测试在 `>=3.8` 解释器上通过；新增脚本无第三方 import"
  code: path = root / EXEMPTIONS_DIR / rel_doc.removeprefix("docs/")
        reference_rel = rel(root, target) if target.is_relative_to(root) else None
  ```
- **Why it's a problem**: both APIs were added in Python 3.9; on a 3.8 interpreter the new action raises `AttributeError` before judging a single document, and the conftest's fixture copy step fails too. The declared floor is therefore not true for this feature's new code.
- **Proposed fix**: use `startswith`/slicing and a `try: target.relative_to(root)` or string-prefix check, or raise the declared floor and record the change; add a 3.8 CI leg if the floor is meant to hold.

### F23 — Removing fenced code blocks shifts every later reference line number

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `skills/external/create-docs/scripts/docs-utils.py:429`
- **Evidence** (verbatim quote):

  ```
  stripped = re.sub(r"```.*?```", "", text, flags=re.S)
  probe: link on line 9 after a 5-line fenced block -> reported "line": 5
  ```
- **Why it's a problem**: C-005 requires `line` to be the reference's line and FR-016 requires every finding to name the document path; a wrong line sends the reader to the wrong place. The regex deletes the block's newlines along with the block.
- **Proposed fix**: replace each fenced block with the same number of newline characters (or parse line-by-line with a fence state) so the line count is preserved, and add a fixture with a fenced block before the link.

### F24 — The SC-001 assertion does not check that the reference targets a rendered face

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `tests/integration/test_docs_obligation_scenarios.py:539`
- **Evidence** (verbatim quote):

  ```
  reference = [line for line in body.splitlines() if "../assets/" in line and "](" in line]
  ```
- **Why it's a problem**: the assertion accepts any `../assets/` link, including `widget.mmd`; it is the test gap behind F4 and lets a source reference pass as the fourth artifact. The test name says "four artifacts present", but the reference half is not tied to the record's rendered path.
- **Proposed fix**: read the trace entry and assert the document's link target equals one of `rendered[].path`; keep the on-disk assertion as the second half.

### F25 — The fixture builder's `--check` cannot detect a record-content drift, and an unknown flag rebuilds the fixtures

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `tests/fixtures/docs-obligation/build_fixtures.py:295` (the `__main__` branch); `:239` (`check()`)
- **Evidence** (verbatim quote):

  ```
  if "--check" in sys.argv:
      sys.exit(check())
  names = build_all()

  $ python3 tests/fixtures/docs-obligation/build_fixtures.py --help   # no --check → build_all()
  built 11 fixture spaces: clean, no-diagram, deleted-rendered, …
  OK: 11 docs-obligation fixture spaces match their registered composition
  # git diff showed orphan-rendered/…/diagram-trace.json gained the PNG face and two sha256 values
  ```
- **Why it's a problem**: `check()` only asserts that each registered path is present or absent; it never compares the bytes of a record, so a fixture can be silently rewritten and the invariant still prints `OK`. The `__main__` branch makes this easy to trigger: any argument other than `--check` (including `--help`) runs `build_all()` and mutates the repository fixtures. This review's own `--help` probe changed `orphan-rendered`'s record; the file was restored to `HEAD` before this report was committed, but the underlying defect remains.
- **Proposed fix**: make `check()` compare each fixture's bytes against the builder's deterministic output (or a committed hash manifest), and make unknown flags exit 2 instead of falling through to `build_all()`; add a negative test that edits a record and expects `check()` to fail.

## 4. What Worked — Preserve (Brief)

- **Red-first evidence with per-task attribution**: 13 reds before `--action obligation` existed, each attributed to T008–T012; the later Part-3 ten reds each name their delivering row, and no red was loosened to go green.
- **Fixture composition as an executable invariant**: `build_fixtures.py --check` verifies all eleven spaces and writes nothing; `copy_fixture` keeps every write/delete case on a `tmp_path` copy.
- **Two-predicate convergence**: `converged` versus `clean`, with `judged_scope_has_carrier`, is defined once in C-013 and asserted on the `exempt-ok` / empty-scope / `--only` faces; an exemption is visibly not a pass.
- **Closed vocabulary with a single precedence owner**: C-016's nine-tier table is implemented as one ordered pass, the two `orphan-*` values are asserted not to swap, and `D-001`'s semantic half is honestly registered as uncovered.
- **Guard preservation with a narrow allowlist**: five guard files keep their baseline failure sets; the only permitted drift (`improve-docs/SKILL.md`) is an `ALLOWED_POST_BASELINE_CHANGES` entry with four literal markers, not a waiver.
- **Generated-copy discipline**: mirrors and four per-tool copies are byte-identical; the two generators reproduce the tree without a manual edit.
- **Single `docs/` line and zero `draw-diagram` diff**: `git diff --name-only 24cb4edc..HEAD -- docs/` is exactly `docs/concepts/documentation-model.md`, and the capability tree is untouched.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Make `verification.md` a seeded artifact, not a closing afterthought** — Target: `templates/verification-log-template.md` and `templates/commands/implement.md` (absolute supplement: `/home/agent/.local/state/spec-kit/worktrees/087-arch-diagram-docs/templates/...`). Change: make the seeding step a hard precondition of the first task row and add the file's existence to the `U4` checklist; a missing file is a stage-gate failure, not a note. Source: F1, F7. Expected impact: the closure checker and ARC always have their first input, and no stage can close on an unproduced acceptance surface.

### 5.2 Command Prompt Improvements

- **Declare plan-owned edits in the line form at every stage close** — Target: `templates/commands/implement.md` (and the driver's stage-close instruction). Change: require `audit-plan-changes.py` with the stage's `PLAN-EDIT:` declarations before the checkpoint commit, and reject a prose-only declaration. Source: F9. Expected impact: the active plan constraint is mechanically auditable at the point it matters.
- **Carry the artifact segment's expected set into the implement close** — Target: `templates/commands/review.md` § Output and placement / `templates/commands/implement.md`. Change: state explicitly that `verification.md` is an implement-stage output and a review input, so a review cannot be asked to invent it. Source: F1. Expected impact: the review's ARTIFACT_EXPECTED_SET is stable across stages.

### 5.3 Automation / Script Improvements

- **Derive the diagram suffix set from the delivery contract** — Target: `skills/external/create-docs/scripts/docs-utils.py` (and its design contract `contracts/diagram-obligation.contract.md`). Change: replace `DIAGRAM_SUFFIXES` with a set read from (or explicitly reconciled against) `skills/external/draw-diagram/references/delivery-contract.md` D1/D2, including `.html`, `.pdf`, `.drawio`, `.excalidraw`; add fixtures for each face. Source: F5. Expected impact: a conformant delivery from any of the six engine layers is judged, and the feature stops carrying a second extension table.
- **Require the reference target to be a rendered face** — Target: `skills/external/create-docs/scripts/docs-utils.py` tier 9. Change: only `rendered[].path` matches may reach `satisfied`; a source-only reference with both faces present gets a named non-pass reason. Source: F4, F24. Expected impact: FR-005's "reference the rendered artifact" is enforced rather than assumed.
- **Preserve line numbers when stripping code fences** — Target: `skills/external/create-docs/scripts/docs-utils.py` `_relative_links`. Change: replace fenced blocks with an equal number of newlines or parse with a fence state. Source: F23. Expected impact: the `line` field points at the real reference.
- **Keep the existing actions' missing-root behaviour unchanged** — Target: `skills/external/create-docs/scripts/docs-utils.py:791`. Change: move the check into the `obligation` branch or make the change a declared, tested behaviour change. Source: F21. Expected impact: C-015's "validate semantics unchanged" holds.
- **Honour the declared Python floor** — Target: `skills/external/create-docs/scripts/docs-utils.py` and `tests/fixtures/docs-obligation/conftest.py`. Change: replace `removeprefix`/`is_relative_to` or raise `requires-python` and record it. Source: F22. Expected impact: the script runs on the floor it advertises.
- **Make the fixture builder's `--check` byte-exact and reject unknown flags** — Target: `tests/fixtures/docs-obligation/build_fixtures.py`. Change: compare each fixture's bytes against the builder's deterministic output (or a committed hash manifest), and exit 2 on an unknown argument instead of rebuilding. Source: F25. Expected impact: a record-content drift cannot pass as `OK`, and a help probe cannot mutate the repository fixtures.

### 5.4 Workflow Improvements

- **Keep the analysis report on disk** — Target: `test-evidence/analyze-report-round2.md` and the analyze stage template. Change: write the round-2 report as an artifact and point the stage row at it. Source: F8. Expected impact: the M1–M4/L1–L7 residue is reconstructable from the stage that produced it.
- **Use sanctioned scratch roots** — Target: `shared/guidelines/temp-directory-discipline.md` (enforcement) and the stage evidence templates. Change: replace `/tmp/087-toolenv` and `/tmp/w087/` with `~/tmp/<project>/<purpose>/` or `.specify/.tmp/<purpose>/`, and add the cleanup statement. Source: F10. Expected impact: scratch does not leak into reproducible commands.
- **Re-derive the plan/quickstart readings after the delivery** — Target: `plan.md` § Residual Risk, `quickstart.md` S3/S8, `contracts/flow-obligations.contract.md` header. Change: mark pre-implementation readings as dated, and correct the 17-vs-26 baseline denominator and the three S3 corrections. Source: F17, F18, F19. Expected impact: a post-delivery reader does not follow a stale command or a stale count.

### 5.5 Documentation Improvements

- **Move the obligation's normative record schema into a shipped reference** — Target: `skills/external/create-docs/references/` (new reference) or the skill body. Change: put the trace-record and exemption-record schema, carrier table and verdict/reason vocabulary in a distributed reference; the spec contract remains the dated design record. Source: F6. Expected impact: a client project can follow the obligation without the authoring spec.
- **Reconcile the feature record and the checklist with the delivered artifacts** — Target: `.specify/memory/features/087.md` line 69, `feature-ref.md` rows 10/75, `data-model.md` line 46, `checklists/requirements.md` lines 17/24. Change: update the counts and pointers (C-001…C-016, S1–S9, resolved OI-087-01, C-016 as the order owner, five verdicts, A1–A12) or replace them with owner pointers. Source: F13, F14, F16, F20. Expected impact: the binding records stop disagreeing with the artifacts they bind.
- **Narrow the `docs/` out-of-scope clause and unify the fixture invariant** — Target: `requirements.md:289`, `plan.md:32/81/493`, `tasks.md:22/77`, `quickstart.md:165`. Change: name the one-file FR-001 exception and replace the four "pre-deletion green state" readings with the E6 reference. Source: F2, F3. Expected impact: the DoD becomes satisfiable and the delivered one-file change stops looking prohibited.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Seed `verification.md` with all SC rows and the smoke triple before any implement close | `templates/verification-log-template.md`, `templates/commands/implement.md` | F1, F7 |
| P1 | Enforce the rendered-face reference and derive the suffix set from the delivery contract | `skills/external/create-docs/scripts/docs-utils.py`, `tests/fixtures/docs-obligation/` | F4, F5, F24 |
| P1 | Move the record schema/carrier table to a shipped reference | `skills/external/create-docs/references/`, `skills/external/improve-docs/SKILL.md` | F6 |
| P1 | Narrow the `docs/` exception and unify the fixture invariant | `requirements.md`, `plan.md`, `tasks.md`, `quickstart.md` | F2, F3 |
| P1 | Gate `U4` on the implement stage's own output and keep the analysis report on disk | `templates/commands/implement.md`, `test-evidence/` | F7, F8 |
| P2 | Reconcile the stale counts, section pointers and checklist readings | `feature-ref.md`, `data-model.md`, `features/087.md`, `checklists/requirements.md`, `quickstart.md` | F12–F20 |
| P2 | Re-audit the active plan constraint at every stage close and use sanctioned scratch roots | `audit-plan-changes.py` usage, stage evidence templates | F9, F10, F11 |
| P2 | Keep existing actions' missing-root behaviour and the Python floor intact | `skills/external/create-docs/scripts/docs-utils.py`, `conftest.py` | F21, F22, F23 |
| P2 | Make the fixture builder byte-exact and reject unknown flags | `tests/fixtures/docs-obligation/build_fixtures.py` | F25 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary) with an absolute supplement where the target is this worktree; no target is left as a bare local path without a repo-relative form.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: one P0 finding (`F1`); its row carries `(validated: direct re-read, subagent unavailable)`. The run's dispatch constraint forbids a validation subagent, so the skill's subagent-unavailable fallback was used: the absence of `verification.md` was re-read directly with `test -f` and the checker's own exit-2 error. No P0 is left unvalidated.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

## 9. Status Transition Verdict (this run)

- **Claimed status**: `Planned` (read from the bound feature detail; never written by this run).
- **Transition judged**: `Implemented → Ready for Review`. The feature is not at `Implemented`, so the transition is not attempted; the feature detail stays `Planned`.
- **Refusal literal**: `blocking-unresolved` — the current `code-review.md` contains two `blocking` entries and no explicit user waiver exists (an agent's confirmation is not a waiver). The same refusal names the missing `verification.md`: the `Planned → Implemented` completeness conditions ② and ④ cannot be met without it, and the ARC has no `final_path` record.
- **Conditions that failed**: (a) `code-review.md` contains `blocking` entries (2); (b) `verification.md` is absent, so no `final`-path criterion can be read as `pass`; (c) the ARC input error leaves the closure verdict `not-evaluated`.
- **Status left unchanged**: `Planned`. No `Implemented` or `Ready for Review` is claimed, no `final`-path pass is fabricated, and no user waiver is inferred.
- **Next actions**: (1) produce `verification.md` with one honest status row per SC and the smoke triple, and record the final smoke evidence; (2) fix the two `blocking` code findings (F4, F5) and the shipped-skill portability finding (F6); (3) close the P1 artifact contradictions (F2, F3); (4) re-run `/speckit.review` after those changes; only then can a later run judge the `Implemented → Ready for Review` transition.
