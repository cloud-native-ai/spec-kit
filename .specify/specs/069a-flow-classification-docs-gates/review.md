# Specification-Driven Development (SDD) Process Review Report: 执行/表达二元分类与文档型门禁（Execution/Expression Classes & Document-Form Gates）— Feature 069 / Slice 069a

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

**Scope of this review**: the **069a slice** only — the SDD process that produced it (requirements → clarify → plan → tasks → checklist → analyze → implement) and the toolchain it exercised. `069b-isomorphism-migration-metrics` (isomorphism mapping, migration, metrics instrument) is out of this slice by the decomposition gate and is **not** scored as missing. The slice's business value is not judged.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 069a |
| Requirement Key | 069a-flow-classification-docs-gates |
| Requirement Name | 执行/表达二元分类与文档型门禁（Execution/Expression Classes & Document-Form Gates）— Feature 069 / Slice 069a |
| Related Feature | 069 执行/表达二元分类与文档型 SDD 同构（Execution/Expression Classes & Document-Form SDD） |
| Repository | spec-kit (self-hosting: framework source **and** its own client runtime) |
| Repository URL | `gitlab` = `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (SSH-only, no HTTPS web remote) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — HEAD is unpushed, and the only remote is SSH-only, so no `blob/` URL can carry these commits. Every citation below is an absolute path plus a recovery command of the form `git show f24c7b6c:<repo-relative-path>`. |
| Branch | `069-execution-expression-sdd` |
| Commit SHA | f24c7b6c5dd17555ae90bcf0e31e138e1f72aa18 (short: f24c7b6c) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-24 |
| Reviewer (Agent) | Fresh-context review session (not the authoring session of any artifact under review); same-author detection gate did not fire — the artifacts were produced in earlier sessions |
| Environment | macOS 26.6.2 (darwin/arm64); Python 3.9.6 (system) and Python 3.14.6 (repo `.venv`); pytest 9.1.1 at `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest` (the repo `.venv` has no pytest — measured); git 2.x |
| spec-kit Source Snapshot | This repository **is** the framework source; `pyproject.toml` version 0.0.22; `.specify/source.json` `commit: c7082866ae71d7fc20bc1e6e1ce0ecff67d63f81`, `stamped_at: 20261021T172020Z` — HEAD f24c7b6c is 069a's own closing commit, unpushed |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 266 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/requirements.md | 27 FR / 8 SC / 4 Shared Strings / SA-1…SA-10; parent-FR projection table |
| plan.md | 259 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/plan.md | 16-principle Constitution Check; W1–W4 minimal wiring; mirror obligations; name-level test strategy |
| tasks.md | 309 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/tasks.md | 36 tasks (3/9/15/4/5), 9 gates, 50-clause green partition, DoD-1…DoD-8 |
| research.md | 204 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/research.md | R1–R14 decisions with dated measurements; self-classification R12 = `execution` |
| data-model.md | 190 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/data-model.md | E1–E10; exactly-six faces; degradation-label invariants |
| contracts/flow-class-ledger.md | 132 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/contracts/flow-class-ledger.md | C-1…C-15: owner, ledger grammar, floors, degradation, closed wiring set |
| contracts/expression-gate-operators.md | 131 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/contracts/expression-gate-operators.md | C-1…C-15: six faces, stage table, call-site registry, baselines, dedupe |
| contracts/doc-consistency-checker.md | 123 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/contracts/doc-consistency-checker.md | C-1…C-10: CLI, S1/S2/S3 sets, four faces, exit codes, call sites |
| contracts/compatibility-distribution.md | 114 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/contracts/compatibility-distribution.md | C-1…C-10: zero new commands/storage, one-package atomicity, two stable states |
| quickstart.md | 250 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/quickstart.md | 6 scenarios with route-a/route-b annotations |
| feature-ref.md | 108 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/feature-ref.md | FR→landing→contract→test mapping; wiring-point table |
| checklists/classification-gates.md | 97 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/checklists/classification-gates.md | CHK001–CHK040 with dispositions; closure summary |
| tasks.md → verification.md | 269 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/verification.md | T032–T036 evidence, 8 SC status rows + machine mirror, DoD table, residuals |
| notes/parent-fr-mapping.md | 114 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/notes/parent-fr-mapping.md | Slice↔parent FR/SC/STR mapping with per-row handling claim |
| notes/pre-change-measurements.md | 152 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-measurements.md | Frozen pre-change baselines + § 8.1 re-freeze delta (31→33) |
| notes/red-first-evidence.md | 950 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/notes/red-first-evidence.md | Per-test red-then-green transcripts (command, output, exit) |
| notes/quickstart-run.md | 236 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/notes/quickstart-run.md | Rerun transcripts for scenarios 1/2/3/4/6 |
| notes/expression-baseline.md | 23 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/notes/expression-baseline.md | Three frozen baselines (gate calls 0 / confirmations 0 / wall clock null) |
| notes/test-baseline-contract.txt | 39 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/notes/test-baseline-contract.txt | 33 frozen failing node ids @ 01d1feaa |
| coverage-baseline.txt | 497 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/coverage-baseline.txt | Frozen uncovered-clause baseline (495 names, excluding 069a) |

**Delivery payload under review** (framework sources, all new/modified in this slice):

| Payload | Lines | Role |
|---------|------:|------|
| `shared/definitions/flow-class-definitions.md` | 208 | class owner: criteria, two values, basis, edge cases, 78-row ledger, neutral list, change log |
| `shared/workflow/expression-gates.md` | 159 | gate owner: six faces, stage operator table, call-site registry, evidence grammar, baselines |
| `scripts/python/flow-class-check.py` | 625 | ledger reconcile (`check`) + class resolve (`lookup`) |
| `scripts/python/doc-consistency-check.py` | 880 | document-form checker (`reader` / `evidence` / `duplicate` / `count`) |
| 8 test modules (`tests/contract/{test_flow_class_ledger,test_flow_class_correctness,test_expression_gates_doc,test_doc_consistency_checker,test_expression_gate_wiring,test_expression_compatibility}.py`, `tests/unit/{test_flow_class_check,test_doc_consistency_rules}.py`) | 3 989 | 124 cases (re-run by this review: `124 passed in 12.82s`) |

## 1. Process Execution Timeline

Reconstructed from `git log 719e5dc7^..f24c7b6c` (18 commits, all 2026-10-24, 20:23 → 23:00 local). The commit series is stage-grouped, so attribution below is commit-traced; anything drawn from artifact state instead says so.

| # | Step / Event | Evidence | Deviation from prescribed flow? |
|---|--------------|----------|---------------------------------|
| 1 | Plan stage lands the full Phase-0/1 set (plan / research / data-model / contracts ×4 / quickstart / feature-ref) | 719e5dc7 (20:23) | No |
| 2 | Plan gate self-correction: engine action count fixed before leaving the stage | 30a41464 (20:24) | No — in-stage correction, disclosed in the commit |
| 3 | Plan revised from "zero touch" to **minimal designated wiring W1–W4** — a scope change made inside the plan stage, before tasks existed | 01275c5c (20:36); plan § Minimal Designated Wiring | Yes — scope re-opened after the Constitution Check had already been written (re-check rows added later: plan.md:63–65) |
| 4 | Tasks generated, then renumbered into execution order | abc49b6d (20:45), 187c8ed1 (20:47) | No — in-stage correction |
| 5 | Checklist generated: **16 `[x]` / 24 `[ ]`** | c92a62de (20:55); `git show c92a62de:.specify/specs/069a-flow-classification-docs-gates/checklists/classification-gates.md` → 24 rows ending "→ 需裁决 / 需规格补写 / 需被测面承认" | No — the checklist did its job (it found 24 real conflicts/ambiguities) |
| 6 | Checklist repair: **13 files, 23 normative edits in 17 minutes**, by the same agent that wrote the requirements. Flips humanize from Complex to Simple, makes `source` mandatory, closes the six-face set, adds a correctness test, renumbers 35→36 tasks | 1361c3e3 (21:12); `git show --stat 1361c3e3` | **Yes** — a 24-item adjudication by the author of the artifact under review, with no independent pass (see F5/F6 origin; the round's own assumptions are recorded at checklist § Assumptions B-1…B-4) |
| 7 | An unrelated upstream commit lands **in the middle of the slice** and changes two global baselines (`templates/instructions-template.md` section count, `skills/internal/memory-*`) | 5b13564b (21:12); `notes/pre-change-measurements.md` § 8.1 | Yes — external churn inside the implementation window; handled by a re-freeze, not by a rebase |
| 8 | Follow-up spec alignment (degradation labels, consumption points, FR citations) | 01d1feaa (21:22) | No — in-passing repair of the round-6 edits |
| 9 | Implement starts: pre-change baselines frozen (T001–T003), including a **contract-failure re-freeze 31 → 33** | f0b8eaed (21:30); `notes/test-baseline-contract.txt` header (`33 failed, 4177 passed`); delta table at `notes/pre-change-measurements.md` § 8.1 | No — the re-freeze is explicitly instructed by T003 and the delta is attributed per name (`inherited`) |
| 10 | Red-first US1 tests (T004–T006), owner + 78-row ledger (T007–T008), engine + US1 green (T009–T012) | 82744713 (21:39), e39cb05b (21:51), 6c519ae1 (21:56) | No — strict test-first; `notes/red-first-evidence.md` holds the red transcripts |
| 11 | Gate owner + US2 red tests (T013–T019) | 854caf1a (22:15) | No |
| 12 | Checker + US2 faces (T020–T021); four wiring points + 8 regenerated copies (T022–T027) | 550539d9 (22:25), d0b3f7dc (22:42) | No — but the wiring is where F1/F2 were introduced and never executed (see below) |
| 13 | Orthogonal-axis pointer + compatibility face (T028–T031) | c3a8f325 (22:49) | No |
| 14 | Close-out: docs sync, mirror sync, full regression, SC evidence, feature registry (T032–T036); status flips Planned → Implemented; lowercase `[x]` normalised to `[X]` | f24c7b6c (23:00); verification.md § Fast-fail record item ③ and the T036 deviation paragraph | **Yes** — T036's text said "status stays Planned"; the run advanced it to Implemented and disclosed the deviation |

**Review-side re-measurements performed for this report** (not copied from the slice's own evidence):

| Claim | Re-measured here | Result |
|-------|------------------|--------|
| 8 new test modules green | `pytest <8 modules> -q` | `124 passed in 12.82s` — matches |
| Contract suite zero NEW failures | full `pytest tests/contract` (249.82 s) + `comm -13` / `comm -23` against the frozen 33 | `33 failed, 4267 passed, 5 skipped`; NEW = ∅, GONE = ∅ — matches |
| Structural baseline | `docs-utils.py --action validate --root .` | `violations: 3` = `broken-link` 2 + `note-frontmatter` 1 — matches |
| Mirror / copy drift | `sync-mirrors.py --check`, `regen-command-copies.py --check` | all pairs `ok` + copies `OK`, exit 0 — matches |
| Task closure | marker count in tasks.md | 36 `[X]`, 0 `[ ]`, 0 `[>]`, 0 `[~]` — matches |
| Checklist closure | marker count + summary line | 40 `[x]`, 0 `[ ]`, **but** the summary says 39 + 1 `[ ]` (F5) |
| Clause count | `grep -c '**C-N**'` per contract | 15 / 15 / 10 / 10 = 50 — matches |
| Wired gate command actually runs | executed the exact commands named in W1/W4/W3 | **fails** — F1, F2 |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 2 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 8 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 3 (F12, F13, F15) |
| Command Prompt | 1 (F7) |
| Automation / Scripts | 4 (F1, F2, F3, F14) |
| Workflow | 5 (F4, F5, F8, F9, F10) |
| Documentation | 2 (F6, F11) |

**P0 validation status**: both P0 findings were confirmed by direct re-execution of the shipped commands in this review session (commands and outputs quoted per finding). The independent read-only validation subagent step could not be dispatched — no subagent/Agent tool is exposed in this environment — so each P0 row carries `(validated: direct re-read, subagent unavailable)` per the skill's documented fallback.

## 3. Findings (Problems & Improvement Targets)

### F1 — The wired document-form gate cannot execute: the exact command the templates name exits 2, then the wiring's own degradation rule turns that into "gates unchanged"

- **Severity**: P0
- **Category**: Automation / Scripts
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/docs.md` (repo-relative: `templates/commands/docs.md:35`; recover: `git show f24c7b6c:templates/commands/docs.md`); same defect in `skills/external/create-docs/SKILL.md:85` and `:114`; root cause in `scripts/python/doc-consistency-check.py:76–86`, `:111–114`, `:128–141`
- **Evidence** (verbatim):

  ```
  # templates/commands/docs.md:35 (W1 — the only wired execution point for the six faces)
  - **按门禁 owner 的调用点行执行算子**：…三面由 `python3 .specify/scripts/python/doc-consistency-check.py --action verify` 承担(计数面委派既有检查器)…

  # skills/external/create-docs/SKILL.md:85 and :114 (W3)
  **门禁补强**:按门禁 owner `shared/workflow/expression-gates.md` 的 `skill:create-docs` 调用点行——当调用方已解析为文档型算子集时,对受触文档执行 `python3 .specify/scripts/python/doc-consistency-check.py --action verify`(复用调用方同一次执行的输出,不重复执行)

  # scripts/python/doc-consistency-check.py:128-141 — the mirror copy resolves its root to .specify/
  def find_repo_root(script_path):
      """The ancestor holding both ``shared/`` and ``skills/``."""
      here = script_path.resolve()
      for parent in [here.parent] + list(here.parents):
          if (parent / "shared").is_dir() and (parent / "skills").is_dir():
              return parent
  ```

  Reproduced in this review (framework repo, HEAD f24c7b6c):

  ```text
  $ python3 .specify/scripts/python/doc-consistency-check.py --action verify
  exit=2
  doc-consistency-check: input error: nothing to check: give --spec-dir and/or --path

  $ python3 .specify/scripts/python/doc-consistency-check.py --action verify --spec-dir .specify/specs/069a-flow-classification-docs-gates
  exit=2
  doc-consistency-check: input error: owner path not resolvable: skills/external/create-docs/SKILL.md, skills/external/create-docs/scripts/docs-utils.py

  $ python3 scripts/python/doc-consistency-check.py --action verify --spec-dir .specify/specs/069a-flow-classification-docs-gates
  exit=0   # the SOURCE copy works — every recorded transcript used this one
  ```

- **Why it's a problem**: two independent defects stack. (a) The wiring names the checker without the scope its own contract requires (C-10 says `--path <每个受触文档>` plus `--spec-dir` when the spec side exists), so the literal command exits 2 with "nothing to check". (b) Even with a scope, the **mirror** copy resolves `find_repo_root` to `<repo>/.specify` — because `.specify/shared` and `.specify/skills` both exist, which is exactly the "two hats" path-resolution trap the project instructions warn about — and then resolves `OWNER_PATHS` (`skills/external/create-docs/SKILL.md`) against `.specify/`, where that path does not exist because the skills mirror is flattened. The wiring's own degradation clause (`docs.md:36`: "所有者不可解析或引擎缺席(退出码 2)时显示 `owner-unavailable` … 降级**不中断**本命令") converts both failures into "report owner-unavailable, keep the existing gates", i.e. the six document-form gates never run and the run still looks normal. The slice's whole claim that "门禁真正被入口执行" (plan § Phase 0, Constitution XIII row) is false on the shipped path; every transcript that supports it (`notes/quickstart-run.md`, `notes/red-first-evidence.md`, all eight test modules) invokes `scripts/python/…`, never the `.specify/…` path the templates name.
- **Proposed fix**: (1) Put the scope into the wiring text — `doc-consistency-check.py --action verify --path <each touched doc> [--spec-dir <spec dir>]` — and add `--strict`. (2) Make `find_repo_root` prefer the payload root (`.specify`) when the script itself lives under `.specify/`, and resolve `OWNER_PATHS`/`DELEGATE_PATHS` against both roots (source first, mirror second). (3) Replace the A1/A3 substring assertions with one contract test that **executes the exact command string the template names** (parse it from the template, run it, assert exit 0/1 and a parsable payload). A grep that would not go red when the call is broken is not evidence.
- **Disposition (2026-10-24, review-fix A)**: **fixed**.
  - Wiring text now carries the scope and strictness: `templates/commands/docs.md` (W1) and `skills/external/create-docs/SKILL.md` (W3, both R6 sites) name `python3 .specify/scripts/python/doc-consistency-check.py --action verify --path <每个受触文档> [--spec-dir <spec-dir>] --strict`. The degradation clause is now an explicit blocking outcome — exit 1/2 or a `not-evaluated` blocking face means the gate is reported as failed and the converged conclusion is blocked — not a silent skip.
  - Root resolution fixed in `scripts/python/doc-consistency-check.py`: `find_repo_root` never returns a directory named `.specify` (two-hats trap) and falls back to the parent of the `.specify/` it lives under; `root_candidates()` returns `[source, .specify]` and `resolve_payload()` tries every root × shape (external skills flatten). `DELEGATE_PATHS` is source-relative only (the dead `.specify/skills/external/...` literal is gone). Mirror-resolved owners are no longer dropped by the C-2 mirror exclusion (`collect_records(..., allow_mirror=True)`), so a client-shape run cannot pass the duplicate face against an empty owner set.
  - Execution evidence: `tests/contract/test_expression_gate_wiring.py::test_a8_the_wired_command_executes_in_both_shapes` parses the command out of the template, fills `--path` / `--spec-dir`, and runs it in **both** shapes (delivered `.specify/…` and source `scripts/…`), asserting exit 0 with all four faces evaluated; `::test_a8_the_wired_command_goes_red_on_a_broken_document` proves the same command exits 1 with `reader-declaration-missing`. Client shape is covered by `tests/contract/test_doc_consistency_checker.py::test_client_shape_resolves_every_owner_from_the_mirror` and `::test_client_shape_duplicate_face_compares_against_mirror_owners` (a `.specify/`-only tree resolves every S3 owner and still reports a copied owner sentence).
- **(validated: direct re-read, subagent unavailable)**

### F2 — The class reader cannot find its owner in any client project, so the "refreshed project" stable state of the compatibility contract does not exist

- **Severity**: P0
- **Category**: Automation / Scripts
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/flow-class-check.py:65` and `:96–107` (repo-relative; recover: `git show f24c7b6c:scripts/python/flow-class-check.py`)
- **Evidence** (verbatim):

  ```python
  # scripts/python/flow-class-check.py:65
  OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"

  # :96-107 — resolves to the project root in a client (skips a parent named .specify)
  for parent in Path(__file__).resolve().parents:
      if parent.name != ".specify" and (parent / ".specify").is_dir():
          return parent
  ```

  The slice's own distribution contract says the owner lands at `.specify/shared/` in a client (`contracts/compatibility-distribution.md` C-3, row 1: "`shared/` → `.specify/shared/`"), and C-4 declares the refreshed state as "接线生效，`/speckit.docs` 在命令分派前…各执行一次 lookup". Reproduced with a client-shaped tree (`.specify/scripts/python/flow-class-check.py` + `.specify/shared/definitions/flow-class-definitions.md` + `.specify/skills/create-docs/SKILL.md`, i.e. exactly what `specify init` + the payload produces):

  ```text
  $ python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.docs" --format json
  owner-unavailable: owner document unreadable: <proj>/shared/definitions/flow-class-definitions.md
  {"flow_class": "execution", "source": "default", "marker": null, ...}
  exit=2
  ```

- **Why it's a problem**: `OWNER_REL` is a source-tree constant with no mirror fallback, while `find_repo_root` deliberately resolves to the **client project root**. In every client the owner is delivered to `<proj>/.specify/shared/…`, so the reader looks one directory too high and degrades on every single call. FR-011 promised "两份分类定义并存时以所有者为准，副本由生成/刷新产生并带漂移检查" — the copy is generated, drift-checked, byte-identical, and **unreadable**. FR-015 ("门禁 MUST 在判定之前从唯一所有者读取类别") can therefore never be satisfied in a client project; every gate read returns `owner-unavailable` + the default class. No test exercises the refreshed-client form: `test_expression_compatibility.py` only asserts payload bytes and force-include patterns, and `test_c4_unrefreshed_form_has_no_call_sites` covers only the *unrefreshed* state.
- **Proposed fix**: add the mirror candidate (`Path(".specify") / "shared" / "definitions" / "flow-class-definitions.md"`) ahead of the source candidate when the resolved root has no `shared/`, and add a contract test that materialises the client shape (mirror engine + mirror owner, no `templates/`, no `skills/`) and asserts `lookup /speckit.docs` returns `source: ledger` — not `owner-unavailable`.
- **Disposition (2026-10-24, review-fix A)**: **fixed**. `flow-class-check.py` no longer hard-codes a source-relative owner constant: `owner_candidates(repo)` returns `[<repo>/shared/…, <repo>/.specify/shared/…]` (tolerating a `--repo` that names the payload root itself), so the owner is unavailable only when **neither** shape exists; `find_repo_root` now falls back to the parent of the `.specify/` it lives under instead of `parents[2]`. Client-shape evidence: `tests/contract/test_expression_compatibility.py::test_c4_refreshed_client_shape_reads_the_delivered_owner` materialises engine + owner + skill under `<client>/.specify/` (no `templates/`, no top-level `skills/`), runs `--action lookup --unit-id "/speckit.docs"` both script-located and with `--repo <client>`, and asserts exit 0 / `source: ledger` / `flow_class: expression` / no `owner-unavailable`; `::test_c4_client_shape_still_degrades_when_the_owner_is_absent` keeps the negative control (exit 2 + the label).
- **(validated: direct re-read, subagent unavailable)**

### F3 — `lookup` hands back a corrupted class value as a decided one, and silently picks the first row of a duplicate

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/flow-class-check.py:564–584` (repo-relative; recover: `git show f24c7b6c:scripts/python/flow-class-check.py`)
- **Evidence** (verbatim):

  ```python
  matches = [row for row in ledger.rows if row["unit_id"] == unit_id]
  ...
  row = matches[0]
  record = {..., CLASS_KEY: row[CLASS_KEY], "source": "ledger", "marker": None, ...}
  ```

  Probe with an owner whose ledger row carries `flow_class = bogus-class`:

  ```text
  $ python3 scripts/python/flow-class-check.py --action lookup --repo <fixture> --unit-id "/speckit.x" --format json
  {"flow_class": "bogus-class", "source": "ledger", "marker": null, "basis": "behavior-oracle", ...}
  exit=0
  ```

- **Why it's a problem**: FR-016 requires that a "缺失、损坏或版本不兼容" class degrade to the default class **and carry a visible label**; FR-001 closes the value domain to two. `lookup` validates neither: an out-of-domain value is returned with `source: ledger` and `marker: null` (i.e. "decided"), and a duplicate/dual-class unit silently returns `matches[0]`. `check` would report `invalid-class` / `dual-class`, but the two gate consumers (W1, W4) call only `lookup` — they never run `check`. So the only reader the gates use is the one path that can emit a class outside the closed set.
- **Proposed fix**: in `action_lookup`, degrade (`DEFAULT_CLASS` + a visible label + exit 2) when the matched row's value is outside `CLASS_VALUES`, when the unit has more than one row, or when rows disagree; extend `tests/unit/test_flow_class_check.py` with those three branches.
- **Disposition (2026-10-24, review-fix A)**: **fixed**. `action_lookup` now returns `source: default` + the closed `owner-unavailable` label + exit 2 (never `source: ledger`, never `matches[0]`) when the only row's value is outside `CLASS_VALUES`, when the unit has several rows (`duplicate`), or when those rows disagree (`dual-class`); `marker` stays null because `未声明·按默认` is reserved for "parsed owner, unit not registered". The precise defect kind rides in `error.detail` and stderr (`owner-unavailable: invalid-class|duplicate|dual-class: …`). Evidence: `tests/unit/test_flow_class_check.py::test_lookup_out_of_domain_class_degrades_with_a_visible_label`, `::test_lookup_duplicate_rows_never_silently_pick_the_first`, `::test_lookup_conflicting_rows_report_dual_class`.

### F4 — SC-002 is recorded `pass` without the runtime sample its own definition requires

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/verification.md:182` (repo-relative; recover: `git show f24c7b6c:.specify/specs/069a-flow-classification-docs-gates/verification.md`); criterion at `requirements.md:212`
- **Evidence** (verbatim):

  ```
  # requirements.md:212
  - **SC-002**: … 「被检查样本」= 接线封闭集中**真正读取类别**的入口（W1 与 W4）所触发的运行时消费点 …

  # verification.md:182
  - **SC-002** — 状态 **pass**。… 消费点分母按 SC 定义只取**真正读取类别**的入口（W1 `/speckit.docs`、W4 `skill:humanize`…）：2/2 = 100% 已接线且都声明标记展示规则 …
    - 边界披露：本条的核验路线是**接线文本 + 引擎实测**，未做一次「未登记单元经 W1/W4 真跑」的端到端演练（命令模板本身不可执行）；该限制在此明示，下游若要求运行期样本需另立样本。
  ```

- **Why it's a problem**: the criterion's denominator is a **runtime** consumption point; the recorded denominator is 2/2 *declarations in the wiring text*. The disclosure admits there was no runtime sample — which makes the sample count 0, not 2 — and still lands `pass`. Under the verification template's own vocabulary an untaken sample is `partial`/`deferred`, not `pass`. Coming one paragraph after an honest `partial` for SC-001, this reads as a downgrade of the recording standard exactly where the evidence was weakest. (It is also downstream of F1: the wired command cannot run at all, so no runtime sample *could* have been taken on the shipped path.)
- **Proposed fix**: re-record SC-002 as `partial` with the reason "runtime sample not taken; denominator is wiring declarations, not consumption events", and add a template rule: a criterion whose denominator is a runtime event cannot be `pass` on static text.

- **Disposition (2026-10-24, review-fix B)**: **fixed**. `verification.md` SC-002 is re-recorded as **`partial`** with the two halves separated: *measured* — ledger reconcile `units: 78` / `findings: []` / exit 0 and the 2/2 wiring declarations (W1 `/speckit.docs`, W4 `skill:humanize` Stage 6); *not measured* — runtime consumption samples = **0**, because the 2/2 figure counted **wiring declarations, not consumption events** (the same denominator error F8 found in SC-004/005). The machine mirror reads `SC-002_status=partial`, DoD-8 now states the distribution (pass 2 / partial 2 / deferred 4), and §Residual carries a new MEDIUM-4 with the lift condition (run one unregistered unit through W1 and W4, record `flow_class` / `source` / `marker`). The recording now obeys REC-069a-01's rule: a runtime-denominator criterion cannot be `pass` on static text.

### F5 — The checklist's "40/40" closure relabels an out-of-slice deferral as resolved, and its own summary still counts it as `[ ]`

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/checklists/classification-gates.md:11`, `:39`, `:96` (repo-relative; recover: `git show f24c7b6c:.specify/specs/069a-flow-classification-docs-gates/checklists/classification-gates.md`)
- **Evidence** (verbatim):

  ```
  # :11 — the checklist's own sigil semantics
  **勾选语义（本次评审的 disposition）**：`[x]` = 要求本身成立，且（如原为问题）已在规格中处置并留可复算证据 … `[ ]` = 仍待处置但**必须带 disposition**：`→ disposition: out-of-slice（069b）: <理由>` …

  # :39 — CHK016 is a deferral, marked [x]
  - [x] CHK016 「只选择算子集、不减少门禁数量、不降 P0/P1、不改阈值」与「与复杂度轴正交」是否有可测分母… [Measurability…] → disposition: out-of-slice（069b）: 门禁数与阈值的对照仪器是父 §G 区父编号 041…

  # :96 — the summary disagrees with the rows
  - **Disposition 汇总**：40 项 = 已核对成立 **39** 项（`[x]`：首轮 16 + 本轮处置 23）+ 待处置 **1** 项（`[ ]`，`out-of-slice（069b）`：CHK016…）
  ```

  Measured in this review: `grep -c '^- \[x\]'` → **40**; `grep -c '^- \[ ]'` → **0**.

- **Why it's a problem**: the "24 pending → 40/40" arc is real in the sense that every one of the 24 rows now carries a disposition and 23 were genuinely repaired. But the last one (CHK016: there is **no measurable denominator** for "gate count and threshold do not change") was not resolved — it was deferred to 069b — and marking it `[x]` contradicts the file's own sigil semantics, which provide `[ ]` + `out-of-slice` for exactly this case. The closing summary even states the correct form (39 + 1 `[ ]`) while the rows say 40 `[x]`, so the checklist cannot tell a reader whether it is closed. A closure claim that the artifact itself refutes is the "green check is a claim, not evidence" pattern applied to process artifacts.
- **Proposed fix**: leave CHK016 as `[ ]` with its `out-of-slice（069b）` disposition (the checklist already allows that form), and make the closure summary machine-derived — assert `count([x]) + count([ ]) == 40` and `count([ ]) == number of out-of-slice rows` in a tiny check, so the two cannot diverge.

- **Disposition (2026-10-24, review-fix B)**: **fixed**. `checklists/classification-gates.md` CHK016 is restored to `[ ]` with its `out-of-slice（069b）` disposition, and the closure summary is now **derived from the markers** instead of hand-written: it states 39 `[x]` + 1 `[ ]` = 40 and says explicitly that this is **not** 40/40 green, with three `grep -c` commands as the reproducible check. Measured after the fix: `grep -c '^- \[x\]'` = 39, `grep -c '^- \[ \]'` = 1, `grep -cE '^- \[[x ]\] CHK'` = 40. A dated §Notes bullet records why the flip happened (an out-of-slice item is not "resolved"), and the round's own `B-2` assumption ("parent unchanged") is marked as superseded by the F6 fix.

### F6 — The slice↔parent "逐字沿用" claim is false for 8 of 10 sampled FRs, and the parent was never updated, so the ratified rules live only in the slice

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/notes/parent-fr-mapping.md:33–59` and `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/requirements.md:184–192` (recover: `git show f24c7b6c:<path>`)
- **Evidence** (verbatim claims, then measured diffs):

  ```
  # requirements.md:184
  切片 FR 与父 requirements 的逐条对应…父规格仍是权威，切片 ID 只是投影。除注明的切片调整外，正文逐字沿用父 FR 语义。
  # requirements.md:191
  | FR-018 … FR-024 | 父编号 023–029（§D 区） | 逐字沿用 |
  ```

  Measured against `069-execution-expression-sdd/requirements.md` (parent unmodified since 2026-10-24, `git log -1 --format=%cs`):

  | Slice FR | Parent FR | Identical? | Slice-only normative addition |
  |---|---|---|---|
  | FR-018 | FR-023 | no | "**本切片恰好六面**" + closure rule (parent says "至少覆盖六面" — open set) |
  | FR-019 | FR-024 | no | definition of 文档型交付物 incl. spec artifacts |
  | FR-020 | FR-025 | no | three-part group, `source` mandatory, object boundary |
  | FR-022 | FR-027 | no | mechanical detection lower bound (24 / 0.90 / 40) |
  | FR-023 | FR-028 | no | reviewer identity + judged object |
  | FR-024 | FR-029 | no | freeze point = first requirements commit; per-stage confirmations ≤ 3 |
  | FR-025 | FR-030 | no | complexity class of both entries (docs Complex / humanize Simple) |
  | FR-009 | FR-009 | no | consumption point = W1/W4; W2/W3 excluded |
  | FR-016 | FR-016 | no | two mutually exclusive degradation labels |
  | FR-021 | FR-026 | yes | — |

- **Why it's a problem**: the checklist repair (commit 1361c3e3) strengthened 13 slice FRs and deliberately left the parent untouched ("B-2 …未改父规格"). That is a legitimate *decision*, but it makes two standing claims false: "父规格仍是权威" (the parent does not contain any of the ratified rules) and "逐字沿用" (8 of 10 sampled rows differ). The consequence is not cosmetic: 069b is defined by parent ranges 018–022 / 033–041 and will read the **parent**; there it finds "至少覆盖六面" and no `source` requirement, so it can legitimately disagree with SA-7 (closed set) and FR-020 without noticing. A projection table that reports "carried verbatim" while the two texts diverge is the silent-disagreement failure One-Source-Of-Truth exists to prevent — and the slice's own FR-022 makes it a defect by its own standard.
- **Proposed fix**: either sync the strengthened clauses into the parent FRs (preferred — the parent is declared authoritative), or change every affected mapping row to a fourth handling value, e.g. `切片补强（父未同步）` with the slice anchor, and state in the parent a pointer to the slice for those FRs. Add a check that `逐字沿用` is only allowed when the two texts are byte-equal.

- **Disposition (2026-10-24, review-fix B)**: **fixed** (the review's preferred option — sync the parent). `069-execution-expression-sdd/requirements.md` now carries the ratified rules in its own FR bodies: FR-002 (main-deliverable口径 + `basis`), FR-006 (independence + machine verifiability), FR-009 (consumption point), FR-011 (replica is not a second source), FR-015 (applicability = the gate execution face), FR-016 (version criterion + mutually exclusive degradation labels), FR-023 (closed six-face set), FR-024 (document-deliverable definition + enforcement face), FR-025 (`source` mandatory three-part group + object boundary), FR-027 (mechanical lower bound), FR-028 (reviewer identity + judged object), FR-029 (freeze point + ≤3), FR-030 (humanize = Simple), plus SC-001/SC-002/SC-003 and the Measurement Sources comparability口径. A dated **§ 修订记录** in the parent maps every changed parent row to its slice anchor and states the invariants (numbering, counts and the 069b range unchanged). Slice side: `notes/parent-fr-mapping.md` now uses three handling values (`逐字沿用` / `父已同步` / `切片本地化`) with an explicit prohibition on calling a strengthened row "逐字沿用" while the parent is stale, and its former "parent was never modified" claim is corrected. Validators after the sync: `validate-requirements.py` 0 error / 0 warning on **both** specs; `pre-analyze-check.py --stage requirements` `decision=pass` on both.

### F7 — Every wired invocation omits `--strict`, so a blocking face can be `not-evaluated` while the command exits 0

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/docs.md:35`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/doc-consistency-check.py:868–876`; contract at `contracts/doc-consistency-checker.md` C-8 (recover: `git show f24c7b6c:<path>`)
- **Evidence** (verbatim):

  ```
  # doc-consistency-checker.md C-8
  | 0 | 零 finding；`not-evaluated` 条目允许存在但必须出现在输出里 |
  | 1 | 至少一条 finding；或 `--strict` 且存在任一 `not-evaluated`（含 `count_check.status = not-run`） |

  # templates/commands/docs.md:35 — no --strict anywhere in the wiring
  …`python3 .specify/scripts/python/doc-consistency-check.py --action verify`…

  # notes/quickstart-run.md § 场景 2 — recorded output, exit 0 with a blocking face unevaluated
  "faces": {"reader": "pass", "evidence": "not-evaluated"} … # exit 0
  ```

- **Why it's a problem**: the gate owner says "MUST NOT 把降级当作通过" and FR-016 (as ratified in this slice) applies "降级不得被当作通过" to **all** degradation paths. The checker implements the opposite default: `not-evaluated` does not affect the exit code unless `--strict` is passed, and no caller passes it. A script or CI consumer that reads the exit status sees success while the `evidence` face was never evaluated; only a reader who parses the JSON learns otherwise. That is precisely the "a green check is a claim, not evidence" failure the constitution's Fast Fail principle names.
- **Proposed fix**: make degraded blocking faces exit non-zero by default (keep `--strict` as an alias for backwards compatibility, or invert the flag to `--allow-degraded`), and put `--strict` into every wired invocation regardless.
- **Disposition (2026-10-24, review-fix A)**: **fixed**. The checker now exits 1 whenever a requested face is `not-evaluated` (or `count_check.status = not-run`); `--strict` is accepted as a same-semantics alias and `--allow-degraded` is the single explicit opt-out (never used at a blocking call site). Contract C-8 was re-recorded accordingly (`contracts/doc-consistency-checker.md`), and both wired invocations pass `--strict`. Evidence: `tests/contract/test_doc_consistency_checker.py::test_c08_not_evaluated_is_never_a_pass`, `::test_c04_evidence_asof_stale_not_evaluated_outside_git`, `::test_c06_unavailable_delegation_is_explicit_not_run`; `tests/unit/test_doc_consistency_rules.py` carries the same default (two existing legs updated from `== 0` to `== 1` plus an `--allow-degraded` control).

### F8 — SC-004/SC-005's zero baseline comes from filtering on the four wiring units, not on the gate calls the requirement defines

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/069a-flow-classification-docs-gates/notes/expression-baseline.md:10`; definition at `requirements.md:224` (recover: `git show f24c7b6c:<path>`)
- **Evidence** (verbatim):

  ```
  # requirements.md:224 — definition (a)
  （a）门禁调用次数 = 本特性运行中执行的检查类单元调用总数（checklist / analyze / review / pre-analyze 检查 / `validate-*`）

  # notes/expression-baseline.md:10 — what was actually counted
  | 门禁调用次数（`gate_calls`） | `0` | `0` | `python3 scripts/python/exec-quant.py --action list-records --since 2026-10-20 --format json`，按声明门禁单元集 `{/speckit.docs, skill:create-docs, /speckit.humanize, skill:humanize}` 过滤 | **无可比降幅**（0 → 0 …） |
  ```

- **Why it's a problem**: the requirement contains two different denominators in one paragraph — (a) the checks actually executed (checklist / analyze / review / pre-analyze / `validate-*`) and (b) "门禁 owner 调用点表的算子名 → 单元 id 映射". The baseline silently adopted (b), which resolves to the four *wiring entry* units that this slice never ran, and therefore measured 0. Under (a) the slice ran at least: one checklist pass, several `pre-analyze-check.py --stage …` runs (the plan records `advisories=79`, the checklist records `advisories=90`), `validate-requirements.py`, `validate-tasks.py`, `decomposition-check.py`, `account-clause-coverage.py` and the full pytest suite — a non-zero count. The `deferred` verdict is honestly labelled ("0 → 0 使下降 ≥30% 在算术上不可定义") and the reason points at 069b for instrumentation, but the zero is a **definitional choice** made after the fact, not a measurement necessity, so SC-004/005 were made unmeasurable by the instrument rather than by the feature.
- **Proposed fix**: pick one denominator in the requirement (the executed-check count, which is what "fewer gates" means), freeze the enumerated unit list at the same time as the baseline, and record the count of checks actually run in the baseline file; if the instrument cannot separate per-check calls, record that limitation as `not-evaluated` **before** the run, not as a zero after it.
- **Disposition (2026-10-24, review-fix A)**: **fixed**. `notes/expression-baseline.md` and `verification.md` SC-004/SC-005 were re-recorded against the requirement's own denominators: (a) checks actually executed — 2 instrument-visible check-class calls for this slice (`/speckit.checklist` ×1, `/speckit.review` ×1) plus an enumerated non-instrumented set (`pre-analyze-check.py --stage {requirements,plan,tasks}`, `validate-requirements.py`, `validate-tasks.py`, `decomposition-check.py`, `account-clause-coverage.py`) that exec-quant cannot split per call; (b) gate confirmations + clarify rounds — 0 + 0. The four W wiring units are explicitly **not** the denominator (that filter is what produced the bogus 0 → 0); both numbers are recorded, and the verdict stays `not-evaluated` / `deferred` because the frozen 0 is a pre-feature zero, not a comparable prior sample.

### F9 — The "classification correctness" oracle repeats the fixture's own class values, so the mutation test proves lookup fidelity, not classification correctness

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_flow_class_correctness.py:49–90` and `:129–171` (recover: `git show f24c7b6c:tests/contract/test_flow_class_correctness.py`)
- **Evidence** (verbatim):

  ```python
  FIXTURE_ROWS = [
      {"unit_id": "/speckit.docs", STR_003: STR_002, "basis": "reader-oracle", ...},
      ...
  ]
  ORACLE = {
      "/speckit.docs": (STR_002, "ledger", "reader-oracle", None, False),
      ...
  }
  ...
  "## 判据",
  "",
  "fixture: 主交付物的验收由什么判定。",      # <- the fixture's "criteria" is a stub
  ```

- **Why it's a problem**: the file's docstring says the fixture is the *input* and the oracle is the *expected output*, "neither is derived from the implementation". That is true of the code, but the oracle's class for every one of the ten units is **the same value written twice in the same file**, and the fixture owner's `§ 判据` is a one-line placeholder rather than the owner's criteria. The mutation test therefore proves: lookup reads the ledger faithfully, and the comparator notices when a ledger row disagrees with a hard-coded table. It cannot prove that `docs → expression` is the *correct* judgment under FR-002's oracle question — which is exactly what FR-006/SC-001 ask for. SC-001's machine half is recorded as "oracle 比对 + 变异断言" (verification § SC-001) and the human half is not executed, so FR-006's "可复现" remains unverified end-to-end while the report reads as if a machine closed it.
- **Proposed fix**: derive the oracle by a second judge from the owner's *criteria text* (not from the ledger), record that judge's worksheet as the oracle source, and load the real owner criteria into the fixture instead of a stub. If that is too expensive, rename the test to `test_lookup_ledger_fidelity` and stop claiming it measures classification correctness.
- **Disposition (2026-10-24, review-fix A)**: **fixed** (first option). The expectation now lives in a separate artifact, `tests/fixtures/flow_class/classification-oracle.md`: a per-unit judgment worksheet (deliverable → judging face → criteria anchor → class / basis / neutral) recording the judge, the date and the owner § 判据 anchor, with an explicit object-boundary note (oracle ≠ data source, oracle ≠ fixture copy). `test_flow_class_correctness.py` parses it and compares fields against it; the fixture carries only the input rows, and its owner's `## 判据` section is now the **real** owner text embedded verbatim instead of the one-line stub. Two mutation legs keep the comparison falsifiable in both directions: flipping a fixture row and flipping an **oracle** row each turn exactly that unit's class field red. New legs: `test_every_oracle_unit_has_a_fixture_row`, `test_fixture_owner_embeds_the_real_criteria`, `test_mutating_the_oracle_turns_the_same_comparison_red`.

### F10 — Feature 069 is marked `Implemented` while 14 of its 41 FRs and 5 of its 13 SCs belong to an unplanned slice

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features.md:77`; allocation at `.specify/specs/069-execution-expression-sdd/notes/decomposition-gate.md` § Proposed slices (recover: `git show f24c7b6c:.specify/memory/features.md`)
- **Evidence** (verbatim):

  ```
  # features.md:77 (status column)
  | 069 | 执行/表达二元分类与文档型 SDD 同构 | … | Implemented | …

  # decomposition-gate.md § Proposed slices
  | 069b | `069b-isomorphism-migration-metrics` | 编号 018–022、033–041 | 14 | 同构映射与边界 + 迁移兼容 + 落地口径与度量仪器 |

  # verification.md § Fast-fail record — the deviation is disclosed
  T036 原文要求 `features.md` 的 069 行状态保持 `Planned`…按 canonical state machine…推进为 `Implemented`
  ```

- **Why it's a problem**: the state machine's `Planned → Implemented` criterion is written per requirement (`tasks.md` closed + one SC status row per SC in **that** requirements file), and 069a satisfies it for *its own* eight SCs. But `features.md` tracks the **Feature**, and the Feature's authority is the parent spec, where 14 FR / 5 SC — including the feature's namesake half ("同构") and the six-face owner pointer — are allocated to 069b, which has no directory, no requirements, and no plan. The index therefore tells every downstream reader that Feature 069 is done. The slice disclosed the deviation (good), but disclosure does not make the projection correct: the state machine has no slice-level status, and the "extension slice" clause it borrowed was written for extensions of an *already Implemented* feature, not for a slice of a feature that is still `Planned`.
- **Proposed fix**: add a slice-aware status rule — either a `Slices` column on the Feature row (`Implemented 1/2`) or a rule that a Feature stays `Planned`/`Partially Implemented` until every declared slice is closed, with the slice's own closure recorded in the detail file. Apply it retroactively to 069.

- **Disposition (2026-10-24, review-fix B)**: **fixed**. `features.md` row 069 and `features/069.md` are back to **`Planned`**, with a new § Slice-aware status in the detail file stating "069a Implemented / 069b unplanned", the slice-level evidence it rests on, and the mechanism gap (no slice-level state; REC-069a-09). The write-up is explicit that this is **a correction of an advance that should not have happened**, not a legal `Implemented → Planned` transition — the state machine's Extension slice rule covers a different case (an extension of an already-Implemented feature). The row's Last Updated cell also stops claiming SC-002 = pass.

### F11 — Three artifacts still freeze the contract baseline at 31 failures while the frozen file holds 33

- **Severity**: P2
- **Category**: Documentation
- **Location**: `plan.md:212`, `plan.md:220`, `tasks.md:21`, `tasks.md:307`, `contracts/compatibility-distribution.md:87` (recover: `git show f24c7b6c:<path>`)
- **Evidence** (verbatim):

  ```
  # contracts/compatibility-distribution.md:87
  | `pytest tests/contract -q` | 与 `notes/test-baseline-contract.txt` 比较，MUST 零新增失败名字（既有 31 失败不修、不掩盖） |
  # tasks.md:307
  - 契约套件判据是「零**新增**失败 nodeid」（基线 31 红）…
  ```

- **Why it's a problem**: T003 re-froze the baseline at implementation start and the file now reads `33 failed, 4177 passed` @ 01d1feaa; the 31→33 delta is properly attributed per name in `notes/pre-change-measurements.md` § 8.1 (`inherited`, from upstream 5b13564b). But the criterion documents named above still say 31, so a reader of the plan/contracts who sees 33 reds will conclude that two new failures appeared. The name-level criterion is unaffected (the comparison is against the file), which is why this is P2 rather than P1.
- **Proposed fix**: replace the literal 31 in the three artifacts with a pointer to `notes/test-baseline-contract.txt` ("count owned by the frozen file"), or update the literals in the same commit that re-freezes.

- **Disposition (2026-10-24, review-fix B)**: **fixed**. The three criterion statements that restated the literal are now pointers to the sole owner of the count and the name list (`notes/test-baseline-contract.txt`): `plan.md` § 判据 (the dated pre-freeze row now labels itself as the pre-refreeze value and names the post-refreeze numbers), `tasks.md` DoD-4 and § 契约基线, and `contracts/compatibility-distribution.md` C-7. Dated Constitution-Check snapshots that recorded 31 at plan time were left alone — they are dated records, not live criteria.

### F12 — The gate owner restates the fact-consistency criteria it says it only points at, and the duplicate face cannot see owner↔owner duplication

- **Severity**: P2
- **Category**: Template
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/workflow/expression-gates.md:8` and `:82–87`; `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/doc-consistency-check.py:516–530` (recover: `git show f24c7b6c:<path>`)
- **Evidence** (verbatim):

  ```
  # expression-gates.md:8
  除「证据分级与 as-of」一面由本文件新增并自持判据外，其余五面的判据句归各自 `owner_pointer`。本文件只登记指针与「在哪一阶段、由哪个入口、以什么阻断级别」执行，**不复述**这些 owner 的判据正文…

  # expression-gates.md:84-86 (the fact-consistency face, whose owner is one-source-of-truth.md)
  - 同一事实 MUST 只有一个所有者并以引用表达；≥ 2 处手写即缺陷。
  - 修复方向 MUST 是改为对唯一 owner 的引用；不是把多处措辞改到一致。MUST NOT 靠改措辞使多处一致。

  # doc-consistency-check.py:528 — only pairs that include a subject file are reported
  if not any(record["pool"] == "subject" for record in group):
      continue  # S3 is the comparison side only (C-2)
  ```

- **Why it's a problem**: a file that declares "I do not restate the five faces' criteria" then restates one face's criteria verbatim in Chinese, against the English owner — a textbook second copy under Principle XIV, and a copy the very checker meant to catch it is structurally blind to (S3 owners are only a comparison side; owner↔owner duplicates are never reported). The slice's own FR-022 makes ≥2 handwritten copies a defect; the delivered pair is one.
- **Proposed fix**: reduce `§ 事实一致性` to the pointer + the two genuinely new items (the mechanical lower bound and the count-delegation rule), and either add an owner↔owner pass to the duplicate face or state in C-2 why the comparison side is excluded.

- **Disposition (2026-10-24, review-fix B)**: **recorded (partially addressed by口径, owner-doc edit deferred)**. The defect is a real second copy: `shared/workflow/expression-gates.md` § 事实一致性 restates `one-source-of-truth.md`'s criteria after declaring it does not restate them. Fixing it means editing a delivered framework owner doc **and** its `.specify/` mirror, which this fix's allowed surface excludes (no code / template / skill / copy changes) — a source-only edit would also turn `sync-mirrors.py --check` red. Note that the normative prohibition already exists in the parent spec (FR-040: 事实一致性面的判据 owner 是 `one-source-of-truth.md`，MUST NOT 复制其判据正文), so no requirement text needs changing: the delivered doc violates an existing rule. REC-069a-11 stays open with the fix shape (pointer + the two genuinely new items; owner↔owner pass or a stated exclusion in checker C-2).

### F13 — FR-019's document deliverables include spec artifacts, but the `reader` face is `not-applicable` for exactly those

- **Severity**: P2
- **Category**: Template
- **Location**: `requirements.md:169`; `scripts/python/doc-consistency-check.py:715–721`; `contracts/doc-consistency-checker.md` C-4 (recover: `git show f24c7b6c:<path>`)
- **Evidence** (verbatim):

  ```
  # requirements.md:169
  「文档型交付物」MUST 指表达类流程产出的、以人阅读验收的 Markdown 产物——规格产物（requirements / plan / tasks / data-model / research / quickstart / feature-ref / contracts / checklists）、技能 `SKILL.md`、命令模板、站点文档…

  # doc-consistency-check.py:715-721 — reader runs only on --path (S2), never on S1
  if "reader" in faces:
      if paths:
          ...
      else:
          statuses["reader"] = "not-applicable"
  ```

- **Why it's a problem**: the blocking requirement names spec artifacts as its primary object, and the checker's reader face is `not-applicable` whenever only `--spec-dir` is passed — which is the normal shape for the SDD flow this gate is meant to serve. Nothing in 069a's own spec artifacts carries a `**Readers**:` line, and the gate that would flag that is switched off for them by construction. The requirement's escape hatch ("S1/S2 是可枚举子集，不构成定义") explains the gap but does not enforce the rule.
- **Proposed fix**: run the reader face over S1 formal artifacts as well (they are the most numerous document deliverables), or narrow FR-019's object list to S2 and say so; either way make the requirement and the checker agree on one scope.

- **Disposition (2026-10-24, review-fix B)**: **partially addressed (the requirement/口径 side is fixed in both specs; checker expansion deferred)**. 069a FR-019 now states the enforcement split explicitly — `reader` runs only on `--path` (S2), `--spec-dir`-only runs record `not-applicable`, and S1 formal artifacts are judged by the review face (FR-023) — and the parent FR-024 carries the same sentence, so 069b cannot read "the reader face covers every deliverable". Running `reader` over S1 remains REC-069a-12 and is deliberately not implemented here: it is a code change (`doc-consistency-check.py`) outside this fix's surface.

### F14 — The shipped client-side `check` action has no passing state

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `scripts/python/flow-class-check.py:318–334`, `:428–445`; `contracts/flow-class-ledger.md` C-14 (recover: `git show f24c7b6c:<path>`)
- **Evidence** (verbatim):

  ```
  # flow-class-ledger.md C-14
  `--action check` 在客户项目中运行时报 `unknown`/`inventory-truncated` 而非"通过"——客户项目没有 `templates/commands` 源树，属预期形态
  ```

- **Why it's a problem**: the payload ships to clients (C-3), and the documented action there always exits 1 with `inventory-truncated` (the review's client-shape probe shows 78 `unknown` findings plus two truncation findings). Declaring that "expected" is honest, but it means a client operator who follows the documentation can never get a green run, and a wrapper script that treats non-zero as failure will always fail. Combined with F2 (lookup also fails there), the client side of the payload is inert.
- **Proposed fix**: either give the client form a meaningful scope (the `.specify/skills` + `.specify/templates` inventory with its own floors) and a passing state, or ship the engine only to the framework repo and let 069b own the client form.

- **Disposition (2026-10-24, review-fix B)**: **recorded**, no spec change (the client form's behaviour is already stated honestly in contract C-14; the open question is a design decision — give the client form its own scan scope and floors, or ship the engine to the framework repo only). REC-069a-06 stays open and the contract already hands it to 069b. Adding a "passing state" note to C-14 would not change that the shipped action has none.

### F15 — The `/speckit.docs` call point claims all six faces including `/speckit.review` and an analyze-stage review line, which inverts "fewer and more precise gates"

- **Severity**: P2
- **Category**: Template
- **Location**: `shared/workflow/expression-gates.md:133` and `:42`; `contracts/expression-gate-operators.md` C-14 W1 row (recover: `git show f24c7b6c:<path>`)
- **Evidence** (verbatim):

  ```
  # expression-gates.md:133 (W1 call point)
  | `/speckit.docs`（W1） | `## Outline` 内… | `flow-class-check.py --action lookup …` | 六面全集：`requirements-clarity` … `review`（评审）；… | 每面 ≥ 1 blocking |

  # expression-gates.md:42 (stage table)
  | analyze | 评审基线确认（`/speckit.review`，按读者基准判定） | review | blocking |
  ```

- **Why it's a problem**: the call-point table binds the *entire* six-face set — including the `review` face, executed by `/speckit.review`, and a `requirements-clarity` operator that only makes sense with a spec dir — to a single documentation command invocation. Under this table, one `/speckit.docs` run is supposed to trigger a review, a requirements validation, and four other faces. That is the opposite of US2's stated goal ("门禁可测地更少更准", SC-004), and it collides with the owner's own dedupe clause (C-10: "同一算子在**同一次产物变更**上 MUST 只跑一次"). The distinction the feature needs — the *expression-class flow* runs six faces across its eight stages, while the *docs command* runs the subset relevant to the documents it touches — is collapsed into one row.
- **Proposed fix**: split the W1 row into "faces applicable to a docs command invocation" (reader / evidence / duplicate / structure, plus a pointer to the review flow) and let the six-face set stay a property of the expression-class *flow*, not of one command call.

- **Disposition (2026-10-24, review-fix B)**: **partially addressed (spec口径 fixed, owner-doc edit deferred)**. The collapse is real: one row binds the whole six-face set (including the `review` face and a spec-dir-only operator) to a single `/speckit.docs` invocation. 069a FR-018 and parent FR-023 now state the distinction the feature needs — the six-face set is a property of the **expression-class flow**, and a single command invocation runs only the subset its call-point row names; it MUST NOT be read as "one call runs all six". Splitting the W1 row itself means editing `shared/workflow/expression-gates.md` § 调用点表 and contract C-14 plus the mirror, which is outside this fix's surface; REC-069a-14 stays open.

## 4. What Worked — Preserve (Brief)

- **Red-first discipline with transcripts**: every test module has a pre-implementation red record (command, real output, exit code) in `notes/red-first-evidence.md`; the eight modules re-run green here (`124 passed`).
- **Name-level baselines instead of "all green"**: the contract suite criterion is a frozen 33-node-id list; this review independently reproduced `33 failed / 4267 passed` with NEW = ∅ and GONE = ∅, including the honest 31→33 re-freeze delta with per-name `inherited` attribution (`notes/pre-change-measurements.md` § 8.1).
- **Anti-vacuous floors**: `flow-class-check.py` distinguishes "zero gaps because the ledger is complete" from "zero gaps because nothing was parsed" (floors 27/51), and the review's client-shape probe confirms the floor fires.
- **Honest SC vocabulary**: SC-001 is `partial` with the human half explicitly not claimed; SC-006 records `null` rather than `0`; the baseline file states that 0 means "not called", not "free".
- **Disclosed deviations**: the docs-sync evaluation states *why* the humanize reference needed no edit; the run discloses its own `[x]`→`[X]` normalisation, the T036 status deviation, and a premise from the dispatch that did not hold (`verification.md` § T033 end + § Fast-fail record).
- **Constrained surface**: five modified framework files + four added payloads, verified by `git diff --name-status`; 25 templates / 49 skills / `src/specify_cli/` untouched; mirrors byte-identical (`sync-mirrors.py --check` and `regen-command-copies.py --check` both re-run here and green).
- **069b boundary held**: no isomorphism rows, migration mechanism, or metric instrument leaked into the slice; the owner carries a one-line pointer only.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-069a-01 — Verification template: a runtime-denominator criterion cannot be `pass` on static evidence** — Target: `templates/verification-log-template.md`. Change: add one rule beside the status vocabulary — when a Success Criterion's denominator is a runtime event (a consumption point, a call, a sample), `pass` requires at least one recorded runtime observation; otherwise the honest value is `partial`/`deferred` with a reason. Source: F4, F9. Expected impact: removes the one upgrade path that survives an honest-looking disclosure paragraph.
- **REC-069a-02 — Checklist template: an out-of-slice item stays `[ ]` and the closure summary is derived** — Target: `templates/checklist-template.md`. Change: state the sigil rule explicitly (`[x]` = resolved; `[ ]` + a disposition = adjudicated-but-deferred) and require the closing summary to be computed from the markers (`n([x]) + n([ ]) = total`). Source: F5. Expected impact: a 40/40 headline can no longer coexist with a 39+1 body.

### 5.2 Command Prompt Improvements

- **REC-069a-03 — Wired gate calls must carry their scope and their strictness** — Target: `templates/commands/docs.md` (and the same sentence in `skills/external/create-docs/SKILL.md`). Change: write the full call (`--path <each touched doc> [--spec-dir <spec dir>] --strict`), not the bare `--action verify`; add the rule to the `create-docs` skill's R6 in the same edit. Source: F1, F7. Expected impact: the shipped instruction becomes executable as written, and a degraded face stops exiting 0.

### 5.3 Automation / Script Improvements

- **REC-069a-04 — Root and payload resolution must survive the two hats** — Target: `scripts/python/doc-consistency-check.py` (`find_repo_root`, `OWNER_PATHS`, `DELEGATE_PATHS`) and `scripts/python/flow-class-check.py` (`OWNER_REL`). Change: resolve against the payload root (`.specify/`) first when the script lives under `.specify/`, fall back to the source root, and fix the dead mirror delegate path (`.specify/skills/external/...` → `.specify/skills/...`). Add a contract test that runs the **exact command the template names**. Source: F1, F2. Expected impact: the refreshed-client stable state of C-4 becomes real, and the wired gates stop being a no-op.
- **REC-069a-05 — A reader must not return an out-of-domain value** — Target: `scripts/python/flow-class-check.py` (`action_lookup`). Change: degrade with a visible label + exit 2 when the matched row's value is outside the closed set, when rows duplicate, or when they disagree. Source: F3. Expected impact: FR-016's "corrupted class" branch becomes reachable instead of impossible.
- **REC-069a-06 — Give the client form a real scope or stop shipping it** — Target: `scripts/python/flow-class-check.py` (`scan_inventory`) + `contracts/flow-class-ledger.md` C-14 (as the 069b hand-off). Change: scan `.specify/templates`/`.specify/skills` with their own floors, or gate the payload to the framework repo. Source: F14. Expected impact: no shipped action with a guaranteed non-zero exit.

### 5.4 Workflow Improvements

- **REC-069a-07 — Slice projection: "carried verbatim" must be byte-equal, and slice-only strengthening must be named** — Target: `.specify/shared/workflow/` slice/decomposition convention (the decomposition-gate record is the natural anchor) + the `parent-fr-mapping` practice. Change: require a fourth handling value (`slice-strengthened`, with the slice anchor) and forbid `逐字沿用` unless the two texts compare equal; on ratification, either sync the parent or record a parent-side pointer. Source: F6. Expected impact: 069b cannot re-open a settled rule by reading the authoritative text.
- **REC-069a-08 — Benchmark instruments must be defined before the run, not after the zero** — Target: the requirements measurement-source section + `templates/verification-log-template.md` (baseline block). Change: freeze the enumerated unit list and the expected count of checks at the freeze commit; if the instrument cannot separate them, record `not-evaluated` **before** the run. Source: F8. Expected impact: SC-004/005 become measurable rather than arithmetically undefined.
- **REC-069a-09 — Feature status must not be advanced by a slice** — Target: `.specify/memory/features/<ID>.md` canonical state machine + `templates/commands/feature.md`. Change: add the slice-aware rule (a Feature with open slices is `Partially Implemented` or carries `Implemented k/n`), and forbid a slice's `/speckit.implement` from flipping the parent status on its own. Source: F10. Expected impact: the index stops overstating scope.
- **REC-069a-10 — Checklist adjudication by the author needs an independent pass** — Target: the objective-analysis gate's application note in `/speckit.checklist`. Change: when the same agent both authors the requirements and adjudicates ≥N checklist findings, require a fresh-context read-only pass over the adjudication commits before implementation. Source: timeline row 6 (24 findings → 23 edits → 17 minutes), F5/F6. Expected impact: the two defects this report found in that window would have had a chance to be caught before they were built on.
- **REC-069a-11 — Owner↔owner duplication is a blind spot of the fact-consistency gate** — Target: `shared/guidelines/one-source-of-truth.md` + `contracts/doc-consistency-checker.md` C-2/S3. Change: add an owner-set pass (or state the exclusion reason in C-2) and reduce `expression-gates.md` § 事实一致性 to a pointer. Source: F12. Expected impact: the gate can detect the class of duplicate the slice itself produced.
- **REC-069a-12 — The reader face must cover the object class FR-019 names** — Target: `contracts/doc-consistency-checker.md` C-4 + `requirements.md` FR-019 (069b edge). Change: run `reader` over S1 formal artifacts, or narrow the requirement. Source: F13. Expected impact: a blocking requirement gains an enforcing face.
- **REC-069a-14 — Separate "faces a command runs" from "faces a flow runs"** — Target: `shared/workflow/expression-gates.md` § 调用点表 + `contracts/expression-gate-operators.md` C-14. Change: keep the six-face set as a property of the expression-class **flow**; give the W1 row only the faces a docs invocation can actually execute (reader / evidence / duplicate / structure) plus a pointer to the review flow. Source: F15. Expected impact: "fewer and more precise gates" stops being contradicted by the registry that implements it.

### 5.5 Documentation Improvements

- **REC-069a-13 — Frozen-baseline literals must be pointers** — Target: `.specify/specs/069a-flow-classification-docs-gates/plan.md`, `tasks.md`, and `contracts/compatibility-distribution.md` C-7 (as the pattern for future specs). Change: cite the frozen file instead of restating "31"; the count is owned by `notes/test-baseline-contract.txt`. Source: F11. Expected impact: a re-freeze stops requiring a four-file sweep.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | REC-069a-03 (wired calls carry scope + strict) | `templates/commands/docs.md`, `skills/external/create-docs/SKILL.md` | F1, F7 |
| P0 | REC-069a-04 (two-hats root/payload resolution + execute-the-wired-command test) | `scripts/python/doc-consistency-check.py`, `scripts/python/flow-class-check.py` | F1, F2 |
| P1 | REC-069a-05 (lookup must degrade, not emit invalid values) | `scripts/python/flow-class-check.py` | F3 |
| P1 | REC-069a-01 (runtime-denominator status rule) | `templates/verification-log-template.md` | F4, F9 |
| P1 | REC-069a-02 (checklist sigil + derived summary) | `templates/checklist-template.md` | F5 |
| P1 | REC-069a-07 (slice projection with `slice-strengthened`) | decomposition/slice convention + parent mapping practice | F6 |
| P1 | REC-069a-08 (freeze instruments before the run) | requirements measurement section + verification baseline block | F8 |
| P1 | REC-069a-09 (slice-aware Feature status) | `features/<ID>.md` state machine, `templates/commands/feature.md` | F10 |
| P1 | REC-069a-10 (independent pass over author adjudication) | `/speckit.checklist` application note | timeline 6, F5, F6 |
| P2 | REC-069a-11 (owner↔owner duplication) | `one-source-of-truth.md`, checker C-2 | F12 |
| P2 | REC-069a-12 (reader face scope) | checker C-4, FR-019 | F13 |
| P2 | REC-069a-06 (client form scope) | `flow-class-check.py`, ledger C-14 | F14 |
| P2 | REC-069a-13 (baseline literals as pointers) | plan/tasks/C-7 | F11 |
| P2 | REC-069a-14 (command faces vs flow faces in the call-site table) | `shared/workflow/expression-gates.md` § 调用点表 | F15 |

## 6.1 Finding Disposition (2026-10-24, review-fix rounds)

> How to read: the findings above are **not rewritten**; this table records what happened to each one. `fixed` = the defect is repaired with evidence named in the row; `partially addressed` = the requirement/口径 side is repaired and the remaining edit is out of this fix's surface, with the owner recorded; `recorded` = accepted as a known condition/decision, no repair in this slice.
>
> Two rounds: **A** = code/payload fixes (commit `1b5f4741`); **B** = spec / registry / review / verification fixes (this commit). Scope exclusion for B: no code, template, skill or mirror edit — anything needing one is recorded rather than patched.

| Finding | Severity | Disposition | Evidence / where it now lives |
|---------|----------|-------------|-------------------------------|
| F1 (gate command not executable) | P0 | fixed (A) | `doc-consistency-check.py` two-hats root resolution + payload-first owner lookup; `templates/commands/docs.md` and `skills/external/create-docs/SKILL.md` carry the full `--path … --strict` call; `test_expression_gate_wiring.py` A8 parses and **executes** the template's own command in both shapes |
| F2 (class reader cannot find its owner in a client) | P0 | fixed (A) | `flow-class-check.py` `owner_candidates()` = `[<repo>/shared/…, <repo>/.specify/shared/…]`; `test_expression_compatibility.py::test_c4_refreshed_client_shape_reads_the_delivered_owner` + the negative control |
| F3 (`lookup` returns an out-of-domain class) | P1 | fixed (A) | `action_lookup` degrades + exit 2 on invalid-class / duplicate / dual-class; three unit legs in `test_flow_class_check.py` |
| F4 (SC-002 recorded pass without a runtime sample) | P1 | **fixed (B)** | `verification.md` SC-002 = `partial` (measured vs not-measured halves; 2/2 was wiring declarations, runtime samples = 0); machine mirror + DoD-8 + new MEDIUM-4 |
| F5 (checklist 40/40 relabels a deferral) | P1 | **fixed (B)** | `checklists/classification-gates.md` CHK016 back to `[ ]` + `out-of-slice（069b）`; summary derived from markers (39 + 1 = 40, explicitly not all-green); dated §Notes entry |
| F6 (slice↔parent "逐字沿用" false; parent never updated) | P1 | **fixed (B)** | Parent `requirements.md` FR-002/006/009/011/015/016/023/024/025/027/028/029/030 + SC-001/002/003 + Measurement Sources re-written, with a dated § 修订记录; `notes/parent-fr-mapping.md` three handling values + prohibition; both specs validate 0 error |
| F7 (no `--strict`, degraded face exits 0) | P1 | fixed (A) | Checker default exit 1 on `not-evaluated`; `--strict` alias, `--allow-degraded` opt-out; contract C-8 re-recorded; wired calls pass `--strict` |
| F8 (SC-004/005 zero from the wrong denominator) | P1 | fixed (A) | `notes/expression-baseline.md` + `verification.md` SC-004/005 re-recorded against definitions (a)/(b); the four W units explicitly are not the denominator |
| F9 (correctness oracle repeats the fixture) | P1 | fixed (A) | `tests/fixtures/flow_class/classification-oracle.md` (separate worksheet, judge + date + criteria anchor); fixture carries inputs only; two mutation legs (fixture and oracle) |
| F10 (Feature 069 over-advanced to Implemented) | P1 | **fixed (B)** | `features.md` row 069 and `features/069.md` back to `Planned`, § Slice-aware status = "069a Implemented / 069b unplanned"; recorded as a correction of an illegitimate advance, not a legal transition; REC-069a-09 for the mechanism gap |
| F11 (baseline literals stuck at 31 vs the frozen 33) | P2 | **fixed (B)** | `plan.md` criteria row, `tasks.md` DoD-4 + § 契约基线, `contracts/compatibility-distribution.md` C-7 now point at `notes/test-baseline-contract.txt` as the sole owner; dated plan-time snapshots left as dated records |
| F12 (gate owner restates the fact-consistency criteria; duplicate face blind to owner↔owner) | P2 | recorded (B); not patched | Editing `shared/workflow/expression-gates.md` + its mirror is outside this fix's surface (and a source-only edit turns `sync-mirrors --check` red). The prohibition already exists in parent FR-040; the delivered doc violates it. REC-069a-11 open |
| F13 (FR-019 names spec artifacts but `reader` is not-applicable for them) | P2 | partially addressed (B) | 069a FR-019 + parent FR-024 now state the enforcement split (reader = S2 only; S1 by the review face). Running `reader` over S1 is a code change → REC-069a-12 open |
| F14 (client `check` has no passing state) | P2 | recorded (B); not patched | Contract C-14 already states the client shape expects `unknown`/`inventory-truncated`; the fix is a design choice (own scan scope/floors, or framework-repo-only payload) → REC-069a-06 open, handed to 069b |
| F15 (W1 claims all six faces for one docs call) | P2 | partially addressed (B) | 069a FR-018 + parent FR-023 now state that the six-face set belongs to the **flow** and a call runs only its call-point subset. Splitting the W1 row needs the gate owner + contract C-14 + mirror → REC-069a-14 open |

**Round-B validator summary** (commands run at the fix commit):

```
python3 scripts/python/validate-requirements.py .specify/specs/069-execution-expression-sdd/requirements.md
  status: ok · 5 checks pass · 0 error / 0 warning
python3 scripts/python/validate-requirements.py .specify/specs/069a-flow-classification-docs-gates/requirements.md
  status: ok · 5 checks pass · 0 error / 0 warning
python3 scripts/python/validate-tasks.py .specify/specs/069a-flow-classification-docs-gates/tasks.md
  PASS · 0 error(s), 0 warning(s)
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --stage requirements --spec-dir <each spec>
  decision=pass · errors=0 · advisories=0
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --stage tasks --spec-dir .specify/specs/069a-flow-classification-docs-gates
  decision=pass · errors=0
```

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. *(No `external` target — every target is inside this repository.)*
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file. *(F1–F15 each carry a verbatim quote, a measured diff, or a reproduced command output.)*
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **two P0 findings (F1, F2) exist**; both were confirmed by direct re-execution of the shipped commands in this review session, because no subagent/Agent dispatch tool is exposed in this environment — each row therefore carries `(validated: direct re-read, subagent unavailable)` per the skill's documented fallback.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
