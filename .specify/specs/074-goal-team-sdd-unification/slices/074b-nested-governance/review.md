# Specification-Driven Development (SDD) Process Review Report: 外层消费、概念扩散与兼容安全 — Feature 074 / Slice 074b

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 074b (slice of Feature 074) |
| Requirement Key | `074b-nested-governance` |
| Requirement Name | 外层消费、概念扩散与兼容安全（Nested Consumption, Diffusion & Compatibility）— Feature 074 / Slice 074b |
| Related Feature | 074 Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation） |
| Repository | `spec-kit` (self-hosted framework source; the same tree is the project under review and the framework that reviewed it) |
| Repository URL | remotes present: `gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`, `gitee.com:cloud-native-ai/spec-kit.git`, `github.com:cloud-native-ai/spec-kit.git`; `origin` is the UPSTREAM `github.com/github/spec-kit.git` and does **not** contain these commits — an `origin`-based URL would be wrong by construction |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — cite absolute paths + `git show <sha>:<path>` instead of URLs |
| Branch | `074b-nested-governance` |
| Commit SHA | `91726a64171c3fcbb265ae0cacabb5ed5390c176` (short: `91726a641`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-29 |
| Reviewer (Agent) | SDD executor agent running `/speckit.review` (process segment via `skill:review-sdd-process`, code segment via `skill:code-review`) |
| Environment | Linux; Python 3.11.11; pytest 8.4.2; git local repository; no network, no container runtime, no cluster |
| spec-kit Source Snapshot | this repository itself @ `91726a641` (templates, skills, scripts and the `.specify/` runtime copies are the tree under review) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 307 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/requirements.md` | 8 FR / 2 SC / 7 shared strings projected from parent 074, with parent mapping and D-1/D-2/D-3 rulings |
| plan.md | 374 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/plan.md` | 18-row Constitution Check, mirror obligations, parent design mapping, one `## Plan Revision` round |
| tasks.md | 256 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/tasks.md` | 26 dependency-ordered rows, 9 DoD rows, 9 completion gates, 30 clause claims |
| data-model.md | 169 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/data-model.md` | 8 entities, 12 validation rules, 2 state machines |
| contracts/compat-and-safety.md | 107 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/contracts/compat-and-safety.md` | C-1…C-12 (default `forbidden`, four-surface additivity, safety negatives) |
| contracts/diffusion.md | 79 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/contracts/diffusion.md` | C-13…C-20 (Stage disambiguation, hosting rule, instructions pointer, trigger conjunction) |
| contracts/report-and-attribution.md | 89 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/contracts/report-and-attribution.md` | C-21…C-30 (report section, attribution boundary, sole writer, verdict by reference) |
| research.md | 296 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/research.md` | RB1–RB10 rulings with measured anchors and rejected alternatives |
| quickstart.md | 245 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/quickstart.md` | S1–S7 scenarios, 4 executed with output pasted, 3 pinned by named tests |
| feature-ref.md | 124 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/feature-ref.md` | Binding, 9-row delivery surface, FR/SC maps, 9 disclosed rulings |
| verification.md | 282 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/verification.md` | Baseline, SC verdicts, DoD close rows, 4 gate re-runs, evidence binding |
| checklists/readiness-2026-10-29.md | 154 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/checklists/readiness-2026-10-29.md` | 31 readiness items (18 pass / 13 fail), fail rows dispositioned after one remediation round |
| checklists/requirements.md | 90 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/checklists/requirements.md` | Requirements-quality checklist, projection-fidelity deltas |
| notes/red-first-evidence.md | 426 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/notes/red-first-evidence.md` | E-1…E-9 red/green runs with pasted output, exit codes, and the two in-run repairs |
| notes/pre-change-measurements.md | 303 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/notes/pre-change-measurements.md` | Frozen mirror/copy/store baselines, containment §10/§11 |
| notes/quickstart-run.md | 399 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/notes/quickstart-run.md` | S2/S3/S4/S5/S6/S7 executions and the refresh/idempotency section |
| test-evidence/ (23 files) | — | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074b-nested-governance/test-evidence/` | Stage check records, the 266-case containment carrier, the targeted-set baseline, `implement.jsonl` run ledger |
| Parent authority (read-only) | 505 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074-goal-team-sdd-unification/` | Parent requirements/plan/contracts; this slice projects its FR 020–024, 026–028 and SC 005/008 |
| Sibling slice (implemented) | — | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/` | Merged at `9360718a1`; its surfaces are cited, never redefined |

## 1. Process Execution Timeline

27 commits carry the slice from an empty spec directory to `Implemented`; the chain is story- and task-grouped, so the timeline below is a commit trace, not an inference.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Requirements landed; spec directory created by hand | `daa0da231`; state record: "父 `create-new-requirements.sh` 未运行，按简报直接建目录" | Yes — the slice has no scripted creation path (see F1's family; recorded, not scored separately) |
| 2 | Cross-slice id qualification fixed | `33269994a` — 074a ids rewritten as "074a 本地 FR 0xx" because `pre-analyze-check` does not strip code spans | No — expected validator behaviour, disclosed |
| 3 | Plan landed | `ce9de5983` — 30 clauses, 18/18 Constitution rows, mirrors measured clean | No |
| 4 | Tasks landed, clause baseline frozen | `61496b869` — 26 rows, four gates pass, `account-clause-coverage --freeze` | No |
| 5 | Readiness checklist | `6e5c13c6f` + `7d9308519` | No |
| 6 | `/speckit.analyze` round 1: 0 CRITICAL / 2 HIGH / 7 MEDIUM / 5 LOW → remediation | `7945a4e9b` — `## Plan Revision` records F-01 as minor; C-3/C-6 reading rule added | No — the command worked as designed |
| 7 | `/speckit.analyze` round 2 dispositions, plan re-anchored | `241a6082b` — A-05/E-05 + checklist dispositions; `plan_constraint` active from here | No |
| 8 | Baseline capture (T001–T003) | `631e0496e` — full suite `6452/21`, targeted `290` collected, mirrors 22/406/136/3/114/59, flow-class 79 | No |
| 9 | US1 report section (T004–T008) | `aa7979fe2` — red-first E-1 (rc=1) then green; single-owner audit rc=0 | No — but leaves three `.specify/` projections stale (F5) |
| 10 | US2 diffusion (T010 red first, then 4 surfaces) | `d7a459f8d`, `8f4c5e832` | No |
| 11 | Supplementary template-reading run finds two defects; both repaired in-run | `b31440576`; E-5b: "named **four** new failures" — the section-count pin and three drifted skill mirrors | Partly — the pin repair lies outside the declared delivery surface (F2) |
| 12 | Compatibility & safety (T017–T020) | `772fe2b84`, `d1ebafea8`, `33073c9c6` | No |
| 13 | Mirror sync + generator idempotency (T021–T022) | `244e073b3` — six pairs clean, `regen-command-copies.py --check` OK, second generator run byte-identical | No, but it lands 10 commits after the sources moved (F5) |
| 14 | Targeted re-run + classification honesty (T023) | `1c8b89778` — 338 collected / 337 passed / 1 pre-existing red, `comm -13` and `comm -23` both empty | No |
| 15 | Structure recheck and SC evidence | `182f526a5`, `c124c7335` | No |
| 16 | Feature 074 flipped to `Implemented`; gates re-run; DoD green | `820f65062`, `a14430450`, `41206c1d0`, `1a66a7b65` | No |
| 17 | Parent-level verification authored as a pointer-only aggregate + split note in the parent `tasks.md` | `91726a641` — new file `.specify/specs/074-goal-team-sdd-unification/verification.md`, 8 `pass` rows, no evidence block | Yes — the template has no such form and its binding rule forbids it (F4) |
| 18 | `/speckit.review` prerequisite run resolves the PARENT spec directory | live re-run at review time: `check-prerequisites.sh --json --require-spec` on branch `074b-nested-governance` returns `"REQUIREMENTS_DIR":".../.specify/specs/074-goal-team-sdd-unification"` | **Yes — and it is silent.** The run had to override `REQUIREMENTS_DIR` by hand (F1) |

Anti-deviation notes worth recording because they are *not* defects: one deliberate red at stage base (`test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`, gate total 27 vs its frozen 23) was disclosed in three artifacts and repaired nowhere; the analyze remediation loop ran exactly once as prescribed; every measure is archived with a command and an exit code.

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 2 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 0 |
| Automation / Scripts | 3 |
| Workflow | 2 |
| Documentation | 0 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `9360718a1801b7686ecb6730df1a6ec028b3d247` | the resolved diff base |
| Head commit | `91726a64171c3fcbb265ae0cacabb5ed5390c176` | the run-start `HEAD`, fixed for the run even if commits land later |
| Base source | `feature-first-commit` | the resolution tier the code segment reported |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 62 / 5 / 57 / 0 | copied field by field from the coverage receipt block |
| Segment verdict | `not-evaluated` | one of the four closed values the `code-review` skill owns |
| Gate verdict | `allow` | merge-gate verdict source (`report --summary --file`, exit 0) |
| Reason, when one applies | 57 of the 62 changed paths are Markdown/txt specification, evidence or generated projections, each skipped with the legal reason `non-code-file`; all five code paths were judged and `gap_files=0`, so no path is unaccounted for — but a skipped file is never coverage credit, which is why the segment verdict is `not-evaluated` rather than `pass` |  |
| Uncommitted scope | 37 uncommitted paths (this run's own wrap-up records, the slice state spine, pre-existing modified session records, and the two reports themselves before they are committed) are outside the review object and carry no conclusion here; the same sentence lives in the code record | disclosed, never concluded over |
| Record | `.specify/specs/074b-nested-governance/code-review.md` | written because the triage value is `run` |
| Archive | `none` | this run's archive path; `none` on a first run |

The code segment records 2 `important`, 3 `suggestion` and 3 `praise` entries; both `important` items were answered in the record itself (agree-and-fix for guidance that the three outcome literals be named where the obligation lands; agree-as-check-shape for the self-declared delivery surface). The findings themselves are read in `.specify/specs/074b-nested-governance/code-review.md`; this subsection carries the verdict and the pointers only.

**Status transition (judged once, both artifacts on disk).** `Implemented → Ready for Review` requires three conjunctive conditions (`templates/feature-details-template.md` § Canonical Status State Machine): every `[~]` task resolved or waived — satisfied, `deferred_tasks=` is empty and no `[~]` row exists; review evidence produced — satisfied, this file and `code-review.md` are on disk; and no `blocking` entry in the current `code-review.md` — satisfied, `report --summary --file` returns `blocking_entries=0`, `gate=allow` with two answered `important` items. The transition is therefore **allowed** — and its application is **not** performed by this dispatch. The dispatch authorizes exactly two files in this commit (`review.md` and `code-review.md`) and forbids staging the run records and the state spine, so the two writes the transition owns — the `features.md` row status and the `## Latest Review` entry in `features/074.md` — are withheld here and left to the closure stage that owns the merge. This mirrors the sibling slice's review commit `0ad2a3f97` (`docs(074a-authorized-routing): add review report`), which landed exactly the same two files and left Feature 074 at `Implemented`. The verdict above is the input that stage needs; nothing in this report claims the flip has happened.

## 3. Findings (Problems & Improvement Targets)

### F1 — A lettered slice branch resolves every `/speckit.*` prerequisite to the PARENT spec directory

- **Severity**: P0
- **Category**: Automation / Scripts
- **Location**: `.specify/scripts/bash/common.sh` L61–L80 (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/scripts/bash/common.sh`); consumer `.specify/scripts/bash/check-prerequisites.sh` L113–L117
- **Evidence** (verbatim quote):

  ```
  # Extract numeric prefix from branch (e.g., "004" from "004-whatever")
  if [[ ! $branch_name =~ ^([0-9]+)- ]]; then
    # If branch doesn't have numeric prefix, fall back to latest spec directory.
  ```

  Live reproduction at review time, same tree, same branch:

  ```
  $ git rev-parse --abbrev-ref HEAD
  074b-nested-governance
  $ bash .specify/scripts/bash/check-prerequisites.sh --json --require-spec --include-spec --include-plan --include-tasks
  {"REQUIREMENTS_DIR":"/storage/project/cloud-native-ai/spec-kit/.specify/specs/074-goal-team-sdd-unification",
   "REQUIREMENT_ID":"074", ...}
  ```

- **Why it's a problem**: `074b-nested-governance` does not match `^([0-9]+)-` — the character after `074` is `b`, not `-` — so the exact-prefix branch is skipped entirely and the "latest spec directory" fallback picks the first directory whose numeric prefix is highest, which among `074-…`, `074a-…`, `074b-…` is the parent. Every command that consumes this script (`requirements`, `clarify`, `plan`, `tasks`, `implement`, `review`) therefore targets the parent's directory while the user believes they are working on the slice: `/speckit.review` writes its two reports into the read-only parent, and `/speckit.implement` reads the parent's 57-row `tasks.md`, silently discarding the split. Nothing in the output says "I resolved your slice to a different directory".
- **Proposed fix**: accept a lettered slice suffix (`^([0-9]+[a-z]?)-`) and prefer an **exact branch-name match** over any prefix heuristic; turn the multi-candidate case into an error instead of "latest wins"; add a `tests/contract/` regression that builds a `074-`/`074a-`/`074b-` fixture tree and asserts each branch resolves to its own directory. This is the second split in this repository (`069a`/`069b` is the first), so the defect is already recurring.
- **Validation**: `(validated: direct re-read, subagent unavailable)` — the source lines and the live run were re-read side by side by the reviewing agent; this environment exposes no subagent dispatch.

### F2 — The delivery surface is a closed table that the delivered change set provably exceeds

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/074b-nested-governance/feature-ref.md` § 2 (delivery table); `.specify/specs/074b-nested-governance/tasks.md` DoD-2; `.specify/specs/074b-nested-governance/verification.md` § DoD close, DoD-2
- **Evidence** (verbatim quotes):

  ```
  交付面按 `feature-ref.md` § 2 的 **9 行 = 3 新 + 6 改**落地
  ```
  ```
  - **DoD-2**: the 9-row delivery surface as `feature-ref.md` § 2 declares
  ```

  The delivered delta carries a tenth code file:

  ```
   tests/contract/test_fast_fail_discipline.py        |  13 +-
  ```

  and the repair is disclosed one file away, in the run evidence:

  ```
  This is the only file this part touches outside the delivery surface `feature-ref.md` § 2 declares
  ```

- **Why it's a problem**: the tenth file is not an accident — C-18 obliges exactly one added `## ` section in `templates/instructions-template.md`, and that section moves two integers pinned by an existing test (`test_a7_section_counts_20_to_21_and_21_to_22`, 29/30 → 30/31). So the consequence is *derivable from the design*, yet the design's own delivery table does not list it, and the two artifacts that carry the verdict (tasks DoD-2 and the verification close) repeat the falsified "9 rows" in its original form. A maintainer asking "did this slice stay inside its declared surface?" gets "yes" from three artifacts and "no" from the tree. The containment claim is void by its own discipline, while the DoD row built on it keeps reading green.
- **Proposed fix**: in `feature-ref.md` § 2 add the row (Kind EDIT, purpose "section-count pin update required by C-18's added section"), or state beside the table that an ambient-section edit necessarily moves the pin owned by `tests/contract/test_fast_fail_discipline.py`; carry one sentence into DoD-2 so claim and delta agree. Separately, where that pin lives, put the update protocol beside the integer as a rule rather than leaving it in a docstring habit — the integer is a counter of ambient sections and every future ambient section pays the same toll.

### F3 — Shared-string ids are slice-scoped with no repo-level owner, and this slice renumbered the parent's mandated ids

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/074b-nested-governance/requirements.md` § Shared Strings and § `Slice STR → Parent STR`; shipped surface `skills/internal/create-team/SKILL.md` L80 and L82; existing registration pointer `shared/definitions/sdd-routing-definitions.md` L16
- **Evidence** (verbatim quotes, the three live registries side by side):

  ```
  # 074b — requirements.md (Slice STR → Parent STR)
  | STR-004 | STR-007 | 嵌套运行 outcome `"completed"` |
  | STR-005 | STR-008 | 嵌套运行 outcome `"blocked"`   |
  | STR-006 | STR-009 | 嵌套运行 outcome `"failed"`    |
  ```
  ```
  # 074a / parent — the SAME ids mean something else
  | `STR-004` | `"sdd"` | routing golden table ... |
  | `STR-005` | `"direct"` | ... |
  | `STR-006` | `"adjudicate"` | ... |
  ```
  ```
  # shared/definitions/sdd-routing-definitions.md:16 — the only registration sentence a shipped document carries
  # (quoted verbatim except that the upper token is written plainly: its registered form does not
  #  resolve against this slice's registry, which is the defect being reported)
  `[[STR-001]]` … STR-010 的取值与语义 owner 是本特性切片的 requirements.md § Shared Strings
  ```
  ```
  # skills/internal/create-team/SKILL.md:80 — the shipped owner of the report section
  `outcome` 取自三值封闭集 `[[STR-004]]` / `[[STR-005]]` / `[[STR-006]]`
  ```

- **Why it's a problem**: "本特性切片" is `074a`, so the one registration pointer a shipped document carries now sends a reader to `"sdd"` / `"direct"` / `"adjudicate"` as the three run outcomes. The parent authority — the higher-priority naming source — calls these literals STR-007/008/009, and `074a`'s shipped `nested-invocation.md` cites them under those ids; this slice renumbered them to 004/005/006 and then cited the renumbered ids from a document that names no registry at all. In a consuming project, which never receives `.specify/specs/074b-nested-governance/requirements.md`, the closed outcome set of a mandatory report section is therefore unreachable and reachable-wrong at the same time. Two further consequences measured in this run: (a) the slice's own resolution test cannot see it, because it resolves citations over the slice directory plus itself and never over shipped documents; (b) that audit sweeps every `*.md` under the slice directory, so any artifact in the slice that *quotes* the sibling registry makes a shipped suite go red — which is what happened twice while this review recorded the finding (once in the code record, once in this report), and is why both quotations write the upper token plainly. A suite whose green depends on the slice never quoting the registry it must reference is not pinning the collision; it is suppressing the evidence of it.
- **Proposed fix**: name the literals where the obligation lands (keep the tokens, add `completed` / `blocked` / `failed` beside them, as `sdd-routing-definitions.md` does for its own three verdicts), or cite the registry by path *and* owning slice, the convention `.specify/memory/glossary.md` already follows when it writes a token with its feature named. Then make the token space decidable at repository level: either a repo-level literal registry that slices extend without renumbering, or a `[[STR-…]]` form that carries its owner (`[[074a:STR-007]]`). A scope-by-directory audit is not a substitute — it hides the collision it exists to find.

### F4 — A split feature has no sanctioned parent-side verification form, and the invented substitute violates the template's binding rule

- **Severity**: P1
- **Category**: Template
- **Location**: `.specify/templates/verification-log-template.md` L55–L66 (`# -- Evidence records` rules); authored artifact `.specify/specs/074-goal-team-sdd-unification/verification.md`; state machine `.specify/templates/feature-details-template.md` § Canonical Status State Machine (`Planned → Implemented` row)
- **Evidence** (verbatim quotes):

  ```
  # Rules: a `pass` verdict REQUIRES a complete evidence row — all four keys, no
  # blanks. ... A `pass` without a complete evidence row is
  ```
  ```
  # .specify/specs/074-goal-team-sdd-unification/verification.md (whole file, 41 lines)
  # Aggregated across the two slices. Per-criterion measurements live in each slice's
  # verification.md; this file is the parent-level pointer set required by the feature
  # status state machine, never a second measurement.

  SC-001_status=pass
  SC-001_value=see 074a verification SC-001
  SC-001_note=.specify/specs/074a-authorized-routing/verification.md (074a local SC-001)
  ```

  Eight such `pass` rows, zero `evidence_path` / `evidence_sha256` rows, in a file whose only purpose is to satisfy the state machine's `Implemented` DoD.
- **Why it's a problem**: the state machine's DoD assumes one requirement ↔ one `verification.md`, while a split feature's measurements live in slices. The implement stage did the honest thing — a pointer aggregate that explicitly refuses to be a second measurement — but the template has no such form and its binding rule forbids `pass` rows without a complete evidence row, so the artifact that carries Feature 074's `Implemented` status violates the owner of the very vocabulary it uses. The gap is not new: `069` (also split) sits at `Implemented` in `.specify/memory/features.md` with **no** parent `verification.md` at all, i.e. the previous split simply could not satisfy the DoD and nobody noticed. Two splits, two different improvisations, no legal path.
- **Proposed fix**: add a sanctioned aggregate row form to `verification-log-template.md` — e.g. `SC-00N_status=pass` with `evidence_path=<slice>/verification.md#SC-…>` and `evidence_sha256` of the slice file — and state in the state machine that a split feature's parent verification aggregates by pointer. A `pass` row with no binding of either shape should be an error, not a silently readable line.

### F5 — Mirror parity is a repo-wide invariant that a multi-commit slice necessarily breaks

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `.specify/specs/074b-nested-governance/plan.md` § Mirror Obligations; `scripts/python/sync-mirrors.py`; `tests/contract/test_mirror_parity_suite.py`
- **Evidence** (verbatim quote from `notes/red-first-evidence.md` § E-5b, the first supplementary run):

  ```
  tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/create-team/SKILL.md->.specify/skills/internal/create-team/SKILL.md]
  tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/create-team/references/conceptual-model.md->.specify/skills/internal/create-team/references/conceptual-model.md]
  tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/run-agent/SKILL.md->.specify/skills/internal/run-agent/SKILL.md]
  ```

  and the cause, in the same section: "the first is part 1's T005–T007 edit, which left the mirror for T021".

- **Why it's a problem**: the plan defers projection to the last polish row, so ten commits on the branch (from `aa7979fe2` to `b31440576`) satisfy neither the repo-wide mirror invariant nor the suite that guards it. Only a supplementary run — launched for a *different* reason — surfaced it, and the repair commit had to be labelled as a defect fix. Any reviewer who checks out an intermediate commit gets a red suite that says nothing about the feature and everything about the plan template's ordering.
- **Proposed fix**: make the projection part of the edit, not of a later row — `sync-mirrors.py --write --only <pair>` in the same commit as each source edit is mechanical and costs one command — and drop "defer mirrors to the polish phase" from the plan template's Mirror Obligations guidance, keeping the verification row as the check rather than as the work.

### F6 — `receipt` re-resolves the review range, so step 4 can silently measure a different review object than step 1

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `.specify/skills/internal/code-review/scripts/git-delta-review.sh` — `cmd_receipt` calls `resolve_range` again (L997 region) instead of reading the range `base` already resolved
- **Evidence** (verbatim, this run, same record, one command apart):

  ```
  $ bash .specify/skills/internal/code-review/scripts/git-delta-review.sh receipt \
      --review-file .specify/specs/074b-nested-governance/code-review.md --skip-with-reason '.specify/*' --reason non-code-file ...
  行数无法测量 (binary): .specify/goal/command-logic-as-classified-skills/summary/assets/wbs.png
  不可量测的数字字段意味着不写块 (C-41 / V16)

  $ # the same command with --spec added
  base=9360718a1801b7686ecb6730df1a6ec028b3d247
  head=91726a64171c3fcbb265ae0cacabb5ed5390c176
  base_source=feature-first-commit
  changed_files=62
  ```

- **Why it's a problem**: `.specify/goal/command-logic-as-classified-skills/summary/assets/wbs.png` is not in the 62-file delta at all — the unqualified `receipt` fell back to the trunk merge base (`main..HEAD`) and measured a completely different change set. The only reason no wrong receipt was written is incidental: the wrong delta happened to contain a binary file, which the line-count rule refuses. With a fallback delta free of binaries, step 4 would have written a coverage receipt naming a base and a changed count that no earlier step in the run had ever seen, and the record — the artifact the merge gate reads — would describe a review object that was never reviewed.
- **Proposed fix**: `start` should persist the resolved `base`, `head`, `base_source` into the record header, and `receipt` / `capture` / `report` should read them from the record instead of re-resolving; when a caller passes a range explicitly and it disagrees with the header, exit `2` with the disagreement named. That also makes the record self-describing, which is what a later reader recomputing `git diff base..head` needs.

## 4. What Worked — Preserve (Brief)

- Red-first evidence as pasted runs (`notes/red-first-evidence.md` E-1…E-9: command, real output, exit code) — the red for `test_sdd_compat_containment.py` is `rc=4 "no such path"`, which is the honest red for a new file.
- Node-id **name-set** containment instead of counts (`notes/pre-change-measurements.md` § 10/§ 11, `comm -13` and `comm -23` both empty; the file states the trap in words).
- `account-clause-coverage.py` with a frozen baseline that excludes the audited spec, so a slice cannot self-exempt its own clauses (`claimed clauses: 30`, `FR 8 / 8`, `uncovered beyond baseline: 0`).
- Reverse-count copy detection whose query set is extracted from the landed owner (`test_sdd_diffusion.py::_routing_owner_query_set`), plus a non-vacuity assertion on the extracted set.
- Absence checks that ship a positive control (`test_sdd_compat_containment.py::test_c10_no_confirmation_gate_is_declared_by_any_delivered_document` proves the scanner sees the document families before concluding an empty intersection).
- `pre-analyze-check.py`'s advisories going from 21 to 0 because the files landed — a gate whose number moves for the right reason.
- The one legal red (`test_c11_gate_scan_total_unchanged`, 27 vs frozen 23) disclosed in three artifacts and repaired in none; re-measured at review time: still 27, still red.

## 5. spec-kit / SDD Improvement Recommendations

> **Identifier note, stated so its absence is not read as an omission**: no `REC-…` id is coined in this report, therefore no register row is owed by this run. The recommendations are addressed by finding id and target path; any later maintainer who wants them registered can coin the ids at that point, in the commit that acts on them.

### 5.1 Template Improvements

- **Slice-aware parent verification form** — Target: `templates/verification-log-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md`). Change: add a sanctioned aggregate row shape (`SC-00N_status=pass` + `evidence_path=<slice>/verification.md#SC-…` + `evidence_sha256` over the slice file), and mirror the rule into `templates/feature-details-template.md` § Canonical Status State Machine so a split feature's `Implemented` DoD has a legal path. Source: F4. Expected impact: ends the improvisation that currently produces an aggregate violating the template's own binding rule, and closes the same hole `069` fell through.

### 5.3 Automation / Script Improvements

- **Slice-aware spec-directory resolution** — Target: `scripts/bash/common.sh` (and its `.specify/` projection; absolute supplement: `/storage/project/cloud-native-ai/spec-kit/scripts/bash/common.sh`). Change: match `^([0-9]+[a-z]?)-`, prefer an exact branch-name match, and error on multiple candidates instead of returning the "latest"; add a `tests/contract/` fixture with `074-`/`074a-`/`074b-` sibling directories. Source: F1. Expected impact: removes a silent wrong-target class from every command that calls `check-prerequisites.sh`; it is the difference between reviewing slice 074b and reviewing its parent.
- **Project the mirror in the same commit as the edit** — Target: `shared/workflow/artifact-commit-step.md` guidance plus the plan template's Mirror Obligations row (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/shared/workflow/artifact-commit-step.md`). Change: make `sync-mirrors.py --write --only <pair>` part of the edit step, and keep the mirror-parity suite as verification rather than as work deferred to a polish row. Source: F5. Expected impact: every intermediate commit on a feature branch satisfies a repo-wide invariant; no branch carries ten commits whose test suite is red for a bookkeeping reason.
- **Persist the resolved range in the code-review record** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh`). Change: `start` writes `base`/`head`/`base_source` into the record header and `receipt`/`capture`/`report` read them from the record; an explicit range that disagrees with the header exits `2` naming the disagreement. Source: F6. Expected impact: step 4 can no longer measure a different object than step 1, and the record becomes recomputable by `git diff base..head` without re-deriving anything.

### 5.4 Workflow Improvements

- **The delivery surface must be reconciled with the delta before the DoD is called green** — Target: `shared/workflow/feature-integration.md` DoD guidance and the plan template's delivery-surface section (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/shared/workflow/feature-integration.md`). Change: require one mechanical reconciliation — `git diff --name-only <base>..HEAD` against the declared table — before any DoD row that names a file count is marked satisfied, and require an added row (not a footnote in run evidence) when the delta exceeds it. Source: F2. Expected impact: closed-set claims about a change set stay decidable at the moment they are asserted, instead of becoming void while still reading green.
- **Give the shared-string token space a repository-level owner** — Target: `templates/requirements-template.md` § Shared Strings plus `shared/definitions/sdd-routing-definitions.md`'s registration convention (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/requirements-template.md`). Change: either register literals once at repository level with slices extending and never renumbering, or require the owner-qualified citation form (`[[<slice>:STR-NNN]]`); and where a shipped document cites a token, require the registration pointer in that document. Source: F3. Expected impact: a token cited from a distributed skill resolves to exactly one meaning; the current state resolves the report contract's outcome set to the routing verdicts.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Slice-aware spec-directory resolution | `scripts/bash/common.sh` + `.specify/scripts/bash/` | F1 |
| P1 | Reconcile the delivery surface with the delta before the DoD reads green | `shared/workflow/feature-integration.md` + plan template | F2 |
| P1 | Repository-level owner for shared-string tokens | `templates/requirements-template.md`, `shared/definitions/sdd-routing-definitions.md` | F3 |
| P1 | Sanctioned parent-side verification form for split features | `templates/verification-log-template.md` + `templates/feature-details-template.md` | F4 |
| P2 | Project the mirror in the same commit as the edit | `shared/workflow/artifact-commit-step.md` + plan template | F5 |
| P2 | Persist the resolved range in the code-review record | `skills/internal/code-review/scripts/git-delta-review.sh` | F6 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a parenthetical supplement; every target has a repo-relative form, so none is marked `external`.
- [x] Every finding in Section 3 carries a quoted excerpt — F1's and F6's include the live command output produced during this review, not a paraphrase.
- [x] No bullet says "see attached", "as discussed earlier", or references context outside this document; every quoted registry, template line and commit id is identified here.
- [x] No placeholder token remains anywhere in the report.
- [x] Section 4 is bullet-only.
- [x] Section 5 recommendations each cite an exact target file and at least one source finding id.
- [x] P0 validation status is stated explicitly: one P0 finding (F1) was raised and carries `(validated: direct re-read, subagent unavailable)` — this environment exposes no subagent dispatch, so the documented fallback was used and its weaker evidence path is stated on the finding row rather than hidden.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
