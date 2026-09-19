# Quickstart Run — Feature 051 (User-Facing Comprehension)

**Run by**: T013 · **Date**: 2026-09-18 · **Scope**: scenarios **1** and **2** (the two US1
owns). Scenarios 3–6 belong to US2–US5 and are recorded by their own tasks.

Every expectation below is **observed output**, not a prediction. Where the quickstart states
a pre-change baseline, the post-change value is shown beside it.

---

## 场景 1 — 真源文档存在且镜像逐字节相等(US1 / SC-003)

```
$ ls -l shared/guidelines/user-facing-comprehension.md .specify/shared/guidelines/user-facing-comprehension.md
  -rw------- 13110 shared/guidelines/user-facing-comprehension.md
  -rw------- 13110 .specify/shared/guidelines/user-facing-comprehension.md
$ cmp shared/guidelines/user-facing-comprehension.md .specify/shared/guidelines/user-facing-comprehension.md && echo "BYTE-IDENTICAL"
  BYTE-IDENTICAL
$ ls -1 shared/guidelines/*.md | wc -l
  12
```

| Expectation | Observed | Verdict |
|---|---|---|
| both files exist | both present, 13110 bytes each | ✅ |
| `cmp` silent → `BYTE-IDENTICAL` | `BYTE-IDENTICAL` | ✅ |
| guideline count = **12** | **12** (pre-change baseline 11, +1 for this feature) | ✅ |

> Working-tree mode shows `-rw-------` for this file and 6 of its 11 siblings, while 3 show
> `-rw-r--r--`. This is a local umask artifact, **not** a repository defect: `git ls-files -s`
> records `100644` for every one of them (git tracks only the executable bit). No action.

---

## 场景 2 — 常驻章节抵达活动指令文件(US1 / FR-003 / FR-038)

```
$ grep -c '^## User-Facing Comprehension' templates/instructions-template.md \
      .specify/templates/instructions-template.md .specify/instructions.md
  templates/instructions-template.md:1
  .specify/templates/instructions-template.md:1
  .specify/instructions.md:1
$ grep -c '^## ' templates/instructions-template.md
  18
$ grep -c '^## ' .specify/instructions.md
  19
```

| Expectation | Observed | Verdict |
|---|---|---|
| three `grep -c` each = **1** | 1 / 1 / 1 | ✅ |
| template sections **17 → 18** | **18** | ✅ |
| live sections **18 → 19** | **19** (the extra one is the project-owned `## Recurring Operational Lessons`) | ✅ |

### Position window

`grep -n '^## ' templates/instructions-template.md` (excerpt):

```
    8:## Documentation Map
   25:## Proactive Flow Trigger
   35:## Fact, Correctness & Logic Checks (Input Sanity)
   50:## One Source Of Truth
   60:## Task Complexity Rubric
   66:## Token Efficiency Discipline
   74:## User-Facing Comprehension
   86:## Dogfooding Practice
```

| Expectation | Observed | Verdict |
|---|---|---|
| new section **after** `Token Efficiency Discipline` | 66 → **74** | ✅ |
| new section **before** `Dogfooding Practice` | **74** → 86 | ✅ |
| `Documentation Map` → `Proactive Flow Trigger` → `Fact, Correctness…` adjacency unchanged | 8 → 25 → 35, still consecutive, no insertion inside the window | ✅ |

The same order holds in the live file (`.specify/instructions.md`: 74 → **82** → 94), so the
additive reconcile injected the section at its **template-relative** position rather than
appending it at the end.

### Dangling-pointer traversal (FR-038 / SC-017)

```
$ grep -oE '\.specify/shared/guidelines/[a-z0-9-]+\.md' .specify/instructions.md | sort -u | while read -r p; do
    s="shared/guidelines/$(basename "$p")"
    [ -f "$s" ] && echo "ok   $s" || echo "MISSING  $s"
  done
  ok   shared/guidelines/ask-record-repeat.md
  ok   shared/guidelines/better-harness.md
  ok   shared/guidelines/confirmation-gates.md
  ok   shared/guidelines/dogfooding.md
  ok   shared/guidelines/one-source-of-truth.md
  ok   shared/guidelines/proactive-trigger.md
  ok   shared/guidelines/task-complexity-rubric.md
  ok   shared/guidelines/token-efficiency.md
  ok   shared/guidelines/user-facing-comprehension.md
```

| Expectation | Observed | Verdict |
|---|---|---|
| all `ok`, zero `MISSING` | **9 `ok`, 0 `MISSING`** | ✅ |
| pointer surface grows by 1 | pre-change **8** → post-change **9** (the new guideline) | ✅ |
| remainder unchanged | still the same **3** structurally unpointed guidelines | ✅ |

The traversal reaches **9** of the **12** guidelines now on disk. The 3 it cannot reach
(`checklist-methodology.md`, `requirements-guidelines.md`, `self-improvement.md`) have no
pointer on either instruction surface, so no pointer to them can dangle; they are accounted
for by `ambient-section.md` **C-11(b)**'s remainder assertion instead — remainder ⊆ those
three, in subset semantics, so deleting any existing pointer grows the remainder and fails
while adding one does not. That is what makes "all 12 accounted for" true in an implementable
form rather than by a traversal that structurally cannot reach them.

---

## Symlink aliases (T009's fourth verification)

All 8 remain symbolic links into `.specify/instructions.md` — none was replaced by a regular
file by the regeneration:

```
  AGENTS.md -> .specify/instructions.md            .github/copilot-instructions.md -> ../.specify/instructions.md
  CLAUDE.md -> .specify/instructions.md            .qoder/project_rules.md -> ../.specify/instructions.md
  QODER.md  -> .specify/instructions.md            .claude/project_rules.md -> ../.specify/instructions.md
  HERMES.md -> .specify/instructions.md            .opencode/instructions.md -> ../.specify/instructions.md
```

The new section therefore reaches all 8 agent surfaces through the symlink, with no separate
edit per tool.

---

## Regeneration side effects worth recording

`bash scripts/bash/generate-instructions.sh` reported
`Injected missing template section(s): User-Facing Comprehension` and, as designed, kept the
existing live file as the refresh base rather than overwriting it. It also wrote a dated
backup `.specify/instructions.md-2026-09-18-192435` and refreshed the tool JSON manifests.
The backup is the generator's own history mechanism (the log names it as the recovery source
for content dropped by older versions); it is not a feature artifact and is not staged.

---

## 场景 4(部分)— 8 行指针接入 11 类界面(US2 阶段期望)

Run by T022 · 2026-09-18. Scenario 4 spans US2/US4/US5, so it is executed once per phase
against **that phase's partial expectation**; the full 8/8 expectation belongs to T052.

```
$ for f in shared/guidelines/confirmation-gates.md shared/workflow/feedback-step.md \
      shared/patterns/interview-pattern.md templates/commands/clarify.md \
      shared/guidelines/requirements-guidelines.md shared/guidelines/proactive-trigger.md \
      skills/summarize-project/references/reporting-playbook.md shared/workflow/glossary.md; do
    printf '%s  %s\n' "$(grep -c 'shared/guidelines/user-facing-comprehension.md' "$f")" "$f"; done
  1  shared/guidelines/confirmation-gates.md
  0  shared/workflow/feedback-step.md
  0  shared/patterns/interview-pattern.md
  0  templates/commands/clarify.md
  0  shared/guidelines/requirements-guidelines.md
  0  shared/guidelines/proactive-trigger.md
  0  skills/summarize-project/references/reporting-playbook.md
  0  shared/workflow/glossary.md
```

| US2-phase expectation | Observed | Verdict |
|---|---|---|
| `confirmation-gates.md` = **1** | 1 | ✅ |
| other seven = **0** | all 0 | ✅ |
| coverage therefore **1/8**, C-1 still an US5 green point | C-1 remains `xfail` | ✅ |

Second command — the preservation half of the same scenario:

| Expectation | Observed | Verdict |
|---|---|---|
| `interview-pattern.md:125-126`'s two pattern-specific rules still verbatim | `One decision per question` + `Ask what, not whether` → **2/2** | ✅ |
| `非阻塞` / `自动传输` hits ≥ 1 after T018's rewrite of `:68` | **1** line carries both literals | ✅ |

The second row is the one worth recording: T018 rewrote that sentence to converge its
wording rule into a reference, and both literals live *only* on that line, so a rewrite that
dropped either would turn `test_nonblocking_submission_notice_rule` red. Verified after the
edit, not assumed — `grep -c` returns 1 for each.

Also verified in this phase (T020): the gate scan is unchanged at
`total 23 / destructive 13 / governance_kept 10 / violations 0`. That is the specific proof
point T020 exists for — `confirmation-gates.md` is the scanner's `SELF_REL` and is wholly
exempt from counting, so editing it *cannot* move the total. Had the total moved, it would
mean the edit leaked into a different scanned file.

---

## 场景 5a / 5b — 宪章双落点(US3)

Run by T034 · 2026-09-18.

| Expectation | Observed | Verdict |
|---|---|---|
| `templates/constitution-template.md` principles **11 → 13** | 13 | ✅ |
| `.specify/memory/constitution.md` principles **14 → 15** | 15 | ✅ |
| `One Source` hits in template **0 → 1** | 1 | ✅ |
| `One Source` hits in command **0 → 1** | 1 | ✅ |
| `MUST include` entries **5 → 7** | 7 | ✅ |
| version **1.11.0 → 1.12.0** | `**Version**: 1.12.0` | ✅ |
| watchlist lands on both sides (C-7) + mutation probe (C-10) | `3 passed` | ✅ |

`grep -c 'User-Facing Comprehension' .specify/memory/constitution.md` → **4** (the principle
heading, the Sync Impact Report's added-principles line, its backflow note, and the truth-doc
anchor), against an expectation of ≥1.

### 场景 5c deferred — and why that is not a gap in FR-026's evidence

5c is the downstream bootstrap drill (`specify init` in an empty directory, then
`/speckit.constitution`). It cannot prove anything about this feature on this machine: the
installed CLI resolves to `/usr/local/lib/python3.11/site-packages/specify_cli/__init__.py`
(**0.0.22, non-editable**), so `init` renders the *installed package's* templates, not this
working tree's. Reinstalling from the tree would modify global site-packages and needs explicit
consent; T034 is therefore marked `[~]` per its own instruction.

FR-026's acceptance evidence is T033's mechanical verification instead, which tests the actual
mechanism rather than a rendered artifact: `templates/plan-template.md` is **unchanged** versus
`BASE_SHA` (0 files), and its `## Constitution Check` block still carries the instruction to
enumerate `### <roman-or-arabic-numeral>. <name>` headings dynamically with an explicit
"Do NOT hard-code principle names here". Since the enumeration is derived at plan time from the
live constitution, a 15-principle constitution renders 15 rows with no template edit — which is
the property 5c would have demonstrated, checked at the place it is actually implemented.

---

## 场景 4(部分,US4 阶段)— 指针接入进度 2/8

Run by T039 · 2026-09-18.

```
  1  shared/guidelines/confirmation-gates.md      (US2 / T017)
  1  shared/workflow/feedback-step.md             (US4 / T036)
  0  shared/patterns/interview-pattern.md         (US5 / T041)
  0  templates/commands/clarify.md                (US5 / T042)
  0  shared/guidelines/requirements-guidelines.md (US5 / T043)
  0  shared/guidelines/proactive-trigger.md       (US5 / T044)
  0  skills/summarize-project/references/reporting-playbook.md (US5 / T046)
  0  shared/workflow/glossary.md                  (US5 / T045)
```

| US4-phase expectation | Observed | Verdict |
|---|---|---|
| `confirmation-gates.md` and `feedback-step.md` = **1** | 1 / 1 | ✅ |
| other six = **0** | all 0 | ✅ |
| `grep -c 'never paste the raw' shared/workflow/feedback-step.md` ≥ 1 | **1** | ✅ |

The last row is the preservation check that matters here: T036 rewrote the coexistence-authority
line immediately below it, so a careless edit would have taken the preserved rule with it. The
other three pinned passages (`Present the choices in user-facing terms`, `never the raw
feedback-utils.py engine path.`, `do not paste the bare flag`) were each verified present too,
and `defer to this section` — the phrase whose authority C-10 moves — now returns **0**.

Gate scan after this phase: `total 23 / destructive 13 / governance_kept 10 / violations 0`,
with **zero** `BLOCKING_RE` hits inside `feedback-step.md`. That file is in scan scope and not
exempt, so the new pointer line and the rewritten line were both checked against all 17
patterns rather than assumed safe.

---

## 场景 4(完整)与 T053 单源扫描 — US5

Run by T052/T053 · 2026-09-18.

### 场景 4 — 8 行指针接入 11 类界面(完整期望)

```
$ for f in shared/guidelines/confirmation-gates.md shared/workflow/feedback-step.md \
      shared/patterns/interview-pattern.md templates/commands/clarify.md \
      shared/guidelines/requirements-guidelines.md shared/guidelines/proactive-trigger.md \
      skills/summarize-project/references/reporting-playbook.md shared/workflow/glossary.md; do
    printf '%s  %s\n' "$(grep -c 'shared/guidelines/user-facing-comprehension.md' "$f")" "$f"; done
```

| Expectation | Observed | Verdict |
|---|---|---|
| all eight rows = **1** | 1 × 8 | ✅ |
| surface-pointers C-1 (`14 passed`) | 14 passed, 0 failed, **0 xfail** | ✅ |

`interview-pattern.md:125-126`'s two pattern-specific rules remain verbatim (2/2), and
`§1.7`'s heading survives with its body converged — C-11 converges the enumeration, it does not
delete the section.

### T053 — single-source scan (C-13 / SC-003 / DoD-9)

```bash
# needles: the 8 characteristic restatement fragments pinned in
# tests/contract/test_user_facing_comprehension_pointers.py (CONVERGED_RESTATED_FRAGMENTS)
# scope: shared/ + templates/ + skills/, *.md
# exempt: the truth document itself, .specify/**, the 4 per-tool trees, docs/public/**
```

**Result: 0 restatement hits.**

Falsifiability was proven rather than assumed, by running the same needle set against the
pre-convergence revision (`git show HEAD:shared/patterns/interview-pattern.md`): all 7
interview-pattern fragments returned `pre=True, post=False`, and `defer to this section`
returned the same across `feedback-step.md`. A needle that matches nothing before *and* after
would have made this zero meaningless — that is the same vacuity trap C-13 fell into on its
first draft (recorded in `red-first-evidence.md`), so the check is run against the old revision
every time the needle set changes.

**Scope limit, restated where the number is claimed**: this is a *literal* scan. Research
measured 38 dispersed wordings; most are paraphrases no literal needle can match, and FR-033
forbids building a wording scorer. So "0" here means *zero literally-identifiable
restatements*, not "all 38 sites individually verified" — those are converged and checked by
C-6/C-9/C-10/C-11 and by T041–T049's own row-level assertions.

### T049 — docs-space convergence (outside C-13's scan scope, done anyway)

Three hand-written copies in `docs/reference/` were converged to summary pointers: the
`## Question Format` paragraph and two guarantee-table rows in `commands/interview.md` (two rows
became one that names the owner), the raw-engine-path wording rule in `skills/feedback.md`, and
`Write for business stakeholders, not developers` in `commands/requirements.md` — which was a
**third** unregistered copy of class ⑦'s reader baseline, after the command template's copy was
removed during US1. `docs/public/**` was not touched: it is Hugo build output, git-ignored
(`docs/.gitignore:2`), with 0 tracked files.

Summary-pointer form per `one-source-of-truth.md`: a short orienting paraphrase plus the owner's
path, carrying none of the owner's operative detail — a reader who intends to act must still
open the owner.

---

## 场景 3 — 门控预算不变(US2 / SC-012)— 2026-09-19 实测

All four commands run from the repo root. This is the scenario the feature's hardest gate hangs
on, so it is recorded verbatim rather than summarised.

```
$ python3 scripts/python/scan-confirmation-gates.py; echo "EXIT=$?"
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
violations (reversible gates still blocking): 0
EXIT=0

$ python3 scripts/python/scan-confirmation-gates.py --baseline .specify/specs/044-reduce-confirmation-flows/baseline.json; echo "EXIT=$?"
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
baseline delta total: -70
violations (reversible gates still blocking): 0
EXIT=0
```

**Every number is character-identical to the pre-change output** (`total 23`, `destructive 13`,
`governance_kept 10`, `violations 0`, `baseline delta total: -70`, both `EXIT=0`). Both pinned
consumers stay green — `test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target`
(cap 93 × 0.25 = 23.25) and `test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`
(`== 23` equality).

**Scanner-unchanged verification** — the quickstart wrote this as `git diff --stat HEAD`, which is
the vacuous form under a clean CI checkout (§ 十三 of the cross-cutting lessons). Re-run against
the frozen `BASE_SHA` instead, which is the stricter and non-vacuous form:

```
$ git diff --stat 925badb60860fdbbb8a5fade24cecb01627fbc6f -- \
      scripts/python/scan-confirmation-gates.py src/specify_cli/__init__.py scripts/
EXIT=0                      # empty output — 0 files changed across all three zero-change surfaces
```

```
$ python3 - <<'PY' … PY
BLOCKING_PATTERNS: 17
POLICY_DOCS: ['shared/patterns/reconcile-pattern.md', 'shared/patterns/interview-pattern.md']
SELF_REL: shared/guidelines/confirmation-gates.md
```

All three match the quickstart's expectation exactly, including the corrected `17` (the
requirements phase had mis-recorded `18`). FR-032's condition therefore never fired: the budget
held by **design avoidance** — every line added inside scan scope was checked to carry 0
`BLOCKING_RE` hits — not by touching the scanner.

---

## 场景 6 — 收敛、镜像与测试基线(US5 / SC-003 / SC-016)— 2026-09-19 实测

### 6a. 单源扫描(四个新测试文件)

```
$ python3 -m pytest tests/contract/test_user_facing_comprehension_doc.py \
                     tests/contract/test_user_facing_comprehension_section.py \
                     tests/contract/test_user_facing_comprehension_pointers.py \
                     tests/contract/test_constitution_double_landing.py -q
...................................................................      [100%]
67 passed in 0.87s
```

All four files exist and collect (67 cases; the pre-change run reported
`file or directory not found`, as the quickstart predicted). C-13's single-source scan is inside
this set and green: content-form restatements under `shared/` + `templates/` + `skills/` = **0**.

### 6b. 既有测试扩展(FR-034)

```
$ python3 -m pytest tests/contract/test_confirmation_gates_execution_report.py -q
..........                                                               [100%]
10 passed in 0.02s
```

The file went 9 → 10 cases; the added case is
`test_doc_carries_comprehension_discipline_pointer`, which asserts both the **header position**
(the pointer sits in the ownership block, not inside any criteria section) and **exactly one**
occurrence — closing the guard gap FR-034 named (the pre-existing `:44-46` case asserted only
`非阻塞` and `自动传输`, never `用户视角途径`).

### 6c. 镜像与再生

```
$ python3 scripts/python/sync-mirrors.py --check; echo "EXIT=$?"
DIFF  .specify/skills/improve-skills/scripts/redline-check.py
ok    agents/ == .specify/agents/templates/ (2 files)
ok    scripts/ == .specify/scripts/ (104 files)
ok    shared/ == .specify/shared/ (42 files)
ok    templates/ == .specify/templates/ (22 files)
EXIT=2

$ python3 scripts/python/regen-command-copies.py --check; echo "EXIT=$?"
OK: all per-tool command copies match the source templates.
EXIT=0
```

**The whole-tree `EXIT=2` is a recorded deviation, not a failure of this feature.** Its single
cause is the `improve-skills/scripts/redline-check.py` source/mirror divergence that
`notes/pre-change-measurements.md` § ③ re-froze as the new drift baseline after the rebase; the
blob comparison there proves the divergence is present in `gitlab/master` itself, i.e. it is
upstream's, and it is the same line the frozen set already carried. Every pair this feature
touches reports `ok`:

```
$ python3 scripts/python/sync-mirrors.py --check --only shared --only templates \
      --only skills/summarize-project --only agents --only scripts; echo "SCOPED_EXIT=$?"
scope --only: shared, templates, skills/summarize-project, agents, scripts
ok    templates/ == .specify/templates/ (22 files)
ok    skills/ == .specify/skills/ (24 files)
ok    agents/ == .specify/agents/templates/ (2 files)
ok    scripts/ == .specify/scripts/ (104 files)
ok    shared/ == .specify/shared/ (42 files)
SCOPED_EXIT=0
```

`regen-command-copies.py --check` keeps the quickstart's **absolute** criterion and returns
`EXIT=0` — all four per-tool trees (`.claude/commands/`, `.github/prompts/`, `.qoder/commands/`,
`.opencode/command/`) match their source templates, so no hand-sync residue exists. The
`skills/` pair's `24 files` here versus the whole-tree run's absence of an `ok skills/` line is the
engine's normal behaviour: a `DIFF` row replaces the pair's `ok` row in whole-tree mode, and
`--only skills/summarize-project` scopes past the diverging sibling skill.

GATE-2's criterion is therefore satisfied in the form `pre-change-measurements.md` § ③ fixed it to:
**no new `MISS`/`DIFF` lines versus the frozen set**, never a bare whole-tree `EXIT=0`.

### 6d. 全量契约套件与失败基线

```
$ bash .specify/scripts/bash/run-tests.sh tests/contract --names-out /tmp/ui-final-contract.txt
FAILED tests/contract/test_token_efficiency_remediation_summary_first.py::test_mirror_identical[V-003]
FAILED tests/contract/test_token_efficiency_remediation_summary_first.py::test_mirror_identical[V-005]
FAILED tests/contract/test_trigger_engine.py::test_c2_sync_mirrors_check_clean
======================= 26 failed, 2042 passed in 39.62s =======================
# failed-name list written: /tmp/ui-final-contract.txt (26 entries)

$ comm -13 <(sort baseline-failed.txt) <(sort /tmp/ui-final-contract.txt)   # NEW failures
(empty)
$ comm -23 <(sort baseline-failed.txt) <(sort /tmp/ui-final-contract.txt)   # HEALED
(empty)
```

Passed count rose **1924 → 2042** (+118, the four new files' 67 cases plus the other suites this
feature extended); failed count moved **24 → 26**. The `comm` diff is empty in **both** directions
against the frozen name-level baseline, which is what makes the +2 legitimate: the baseline was
re-captured by name after the rebase (`notes/pre-change-measurements.md` § ②), so the two extra
failures are inside it, not new to it. The quickstart's stated expectation — "失败集 ⊆ {049 冻结基线}
∪ {`test_specify_script_paths.py::…test_review_prerequisite_flags_are_supported`}" — is superseded
by the stronger name-level form: set **equality** with the frozen baseline, which also detects a
failure that heals for the wrong reason.

The `test_review_prerequisite_flags_are_supported` self-heal the quickstart predicted did occur
(`tasks.md` now exists), and is accounted for inside the re-frozen baseline.

### 6e. 文档空间(手写源收敛,生成物不手改)

| 探针 | 改前基线 | 改后实测 | 判定 |
|---|---|---|---|
| `grep -c 'plain-language title\|Plain language, your vocabulary' docs/reference/commands/interview.md` | 2 | **1** | 下降 ✓ |
| `grep -c 'never the raw' docs/reference/skills/feedback.md` | 1 | **0** | 下降 ✓ |
| `grep -c 'business stakeholders, not developers' docs/reference/commands/requirements.md` | 1 | **0** | 下降 ✓ |
| `git ls-files docs/public \| wc -l` | 0 | **0** | 不变 ✓ |

All three hand-written restatement counts fell, and `docs/public/**` stayed at 0 tracked files —
it is Hugo build output ignored by `docs/.gitignore`, so it was correctly **not** hand-edited; the
existing create-pages flow rebuilds it from the corrected sources. The residual `1` on the first
probe is the converged pointer row that now *names* the owner instead of restating its rules, which
is the intended end state rather than an unfinished one.

Probe A-03's correction held in practice: the second needle is the single-line-safe fragment
`never the raw`, not the cross-line `never the raw engine path` form that would have been a
provably blind probe (identically 0 before and after, indistinguishable from a successful
convergence). Because the quickstart recorded concrete pre-change numbers, the `0` here reads as
"converged from 1", not as "was already 0".
