# Quickstart run record — Feature 053

**Purpose**: the real output of actually running this feature's `quickstart.md` scenarios, teardown steps included. A scenario is only recorded as run when its command was executed and its output pasted here.

**Capture date**: 2026-10-03 · **BASE SHA**: see `pre-change-measurements.md`

<!-- one section per scenario, in execution order -->

## 场景 6 — US3 的条款形态普查与 owner 声明(改后实跑,2026-10-04,T027)

Command: `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/053-machine-decidable-artifacts`

Real output, first 11 lines — **no number in this section was copied from the scenario row**, all were re-derived by this run:

```text
spec-dir: .specify/specs/053-machine-decidable-artifacts
corpus:   .specify/specs/*/contracts/*
owner forms (shared/definitions/contract-clause-definitions.md): md-bold-closed, md-bold-paren, md-heading, yaml-openapi, yaml-assertions; md-none named
scanned 117 files: parsed 64 + named-unparseable 53 == 117  [relational sentinel OK]
  per form (counts owned by notes/clause-form-census.md, re-derive, never restate): md-bold-closed 28 files/493 clauses; md-bold-paren 1 files/10 clauses; md-heading 25 files/141 clauses; yaml-openapi 9 files/39 clauses; yaml-assertions 1 files/6 clauses; md-none 53 files/0 clauses
  zero-clause-but-parseable (parse doubt): 0
  .yaml: parsed 10 / total 10 / named 0
named-unparseable: 53 (use --list-named to expand)
clause universe: 665 distinct names over 64 parsed files (689 ids extracted)
  collapsed: 24 extracted ids share a name with another in the same file, …
```

The scenario's expected result is met literally: three numbers, **64 + 53 == 117**, the sentinel relational rather than a literal, and the named list collapsed to a count by default.

**Collapsibility (C-9), both sides measured**: default run prints **0** `  NAMED: ` lines; the same run with `--list-named` prints **53**. So the flag is what expands it, and the default really is collapsed rather than merely short.

**The two "改前可实跑" probes, re-run now that the owner document exists** — the scenario's recorded values were `10 / 0 / 0`:

| probe | 改前(scenario record) | 改后(this run) | why it moved |
|---|---|---|---|
| `grep -c '\*\*C-[0-9]* (' …/031-…/rubric-section.md` | `10` | **10** | unchanged — the fifth form's evidence is a property of that spec, not of this feature |
| clause-syntax definition hits in `templates/ shared/ docs/` | `0` | **3** across **2** files | the probe was an *absence* proof; it now finds `shared/definitions/contract-clause-definitions.md` (the owner this feature created) and `templates/tasks-template.md` (US2's `[green:]` bullet, which uses the phrase "clause id" without defining it — a usage, not a second owner) |
| `find templates -iname '*contract*' -o -iname '*clause*'` | `0` | **0** | unchanged — this feature put the owner in `shared/definitions/`, not in `templates/` |

The middle row is the one worth stating: a probe whose purpose is to prove a thing is absent must be re-read as a *presence* probe once the thing lands, or it silently becomes a check that can only fail.

**A-8, found by this run.** `clause universe` prints **665 distinct names** while **689 ids** were extracted. The owner's `yaml-openapi` form names a clause by its HTTP method key, and 8 corpus files declare the same method under several paths, so 24 operations share a name with another and a name-set collapses them. Re-derived independently before trusting the tool's own number: `extract_clauses` over the corpus gives 689 ids as a list and 665 as a set, and the 24 are distributed over exactly those 8 files (worst case: one file with five `get` keys sharing one name). Disposition: **reported, never absorbed** — both numbers print, with the cause and a pointer to `research.md` A-8, and `tests/contract/test_clause_coverage.py::test_c7b_ids_that_collapse_into_one_name_are_reported_never_absorbed` pins it against a planted two-`post` OpenAPI file. Qualifying those ids by their path is a **syntax change** belonging to the owner document, so it was escalated as A-8 rather than decided inside an implementation task; the owner document now records the fact (non-uniqueness and the duty to report both numbers) without changing the syntax.

## 场景 7 — US3 的冻结基线与 `comm -13` 比对(改后实跑,2026-10-04,T027)

**The idiom on 052's real name sets (改前可实跑, unchanged)**: baseline **76** lines, current **65**, `comm -13` delta **0** — reproducing the scenario's recorded `76 / 65 / 0`.

**The coverage baseline, frozen this phase (T026)** — at the *first* full-tree run, not the first green one, and over the corpus **excluding** this feature's own spec dir:

```text
names: 483   header lines: 2   LC_ALL=C sort -c: OK
header: # frozen-from: .specify/specs/*/contracts/* excluding 053-machine-decidable-artifacts |
        owner-forms: md-bold-closed,…,md-none (md-none named, never silently covered) |
        clause-rules: shared/definitions/contract-clause-definitions.md |
        per-form counts: notes/clause-form-census.md | base-sha: 145b69444d7d |
        files: 110 (parsed 57 + named 53)
items from 053's own spec dir inside the baseline: 0
```

The freeze面 is the census's stable **excl-053** basis — 110 files, parsed 57 + named 53 — and the header carries all four comparability facts C-23 demands (form set, rules owner, corpus selector, base SHA). Zero of this feature's own items are in it, which is what makes the gate below capable of going red.

**Live run against that baseline**, and the paired `comm -13` proof:

```text
claimed clauses (this feature): 0
baseline: …/coverage-baseline.txt (483 names)
baseline-internal existing uncovered: 483
uncovered beyond baseline: 182
FR universe: 48 | FR claimed: 48 | FR uncovered: 0
companion: claimed clauses 0, scanned files 117, clause universe 665, FR universe 48
182 error(s), 0 warning(s)          status: uncovered          ACC_EXIT=1

LC_ALL=C comm -13 coverage-baseline.txt <(live UNCOVERED names)
  → 182 names, comm stderr empty
  → of those, names NOT under 053-machine-decidable-artifacts/: 0
independently re-derived: 053's own contracts hold 182 clause ids
```

So the scenario's expected result is **not yet satisfiable, and that is the correct state at T027**: the criterion is "delta empty **AND** this feature's claimed count non-empty", and both halves fail for the same reason — the claims only land at T045. What this run proves is the stronger property the criterion exists for: the delta is *exactly* this feature's own 182 clauses and nothing else, so the baseline exempts the pre-existing 483 items of other specs while exempting **none** of 053's own. The gate is red now, for the right reason, and T045 is what turns it green — a gate that had been green all along would have been the defect FR-027 § 基线面 was amended to prevent.

**A second measured defect, in the idiom rather than the tool.** The first `comm -13` attempt printed `comm: file 1 is not in sorted order` and then reported a delta of **665** instead of 182 — a wrong verdict that still looked like output. Cause: the names are codepoint-sorted (Python's `sorted`), but glibc collation ignores `#`, `/` and `.` at the first level, so under `en_US.UTF-8` the two `#`-prefixed header lines sort *after* digit-initial names. `LC_ALL=C sort -c` accepts the file and the ambient locale rejects it at line 3. Disposition: the idiom is specified with `LC_ALL=C` in three places that a reader could reach it from — the baseline header itself, the script's docstring, and `tasks.md` GATE-8 — and pinned twice in `test_clause_coverage.py` (`test_c24…` now runs `comm` under `LC_ALL=C` with **both** sides non-empty, because with an empty baseline `comm -13` echoes all of file 2 whatever the ordering and my first version of that test passed for that weak reason; `test_c24b…` pins the file as C-sorted with exactly two header lines). The script's internal delta is a set difference and is locale-independent, so it stayed authoritative throughout — the two agreed at 182 once the locale was fixed.

## 场景 8 — US4 的 `run-checks` 五项 verdict 与零写入(改后实跑,2026-10-04,T036)

### The real tree, read-only: census first, because C-28 makes the sample availability a measured fact

```text
goals: 1 -> draw-two-layer-structure            status=active
teams: 6 directories + hidden .work/            teams declaring goal_slug: 2
  draw-two-layer-structure -> goal 'draw-two-layer-structure'          definition exists: yes
  viz-skill-arena          -> goal 'visualization-skill-selection'     definition exists: NO
```

**So C-28's contingency fires and is recorded rather than papered over**: the only real goal is
`active`, therefore **no real terminal-state goal exists** and SC-007's "对一个 goal 已终态的真实
团队跑" has no real sample. That tier was constructed in a throwaway copy of the real tree
(`mktemp -d` + `\cp -r .specify/goal .specify/teams`), never by mutating a real definition, and
the copy was deleted afterwards (residue **0**). No verdict below is fabricated: each is pasted
from a run, and the tier it belongs to is named.

### R1–R4: the real tree, all five exit tiers except 4

| run | verdict | blocked | exit | what it proves |
|---|---|---|---|---|
| `run-checks draw-two-layer-structure` | `ok` | false | **0** | C-7: with no target, ②③④ are `not-evaluated` while ①⑤ are really evaluated (both `ok`) |
| `run-checks draw-two-layer-structure --target T-001` | `target-terminal` | **true** | **5** | a REAL blocked sample — T-001 is genuinely `dropped` in the live definition; ③ fires, ①② evaluated `ok`, ④ `not-evaluated` (a local-form reference raises no cross-goal question) |
| `run-checks cws-workspace-cluster` | `no-goal-definition` | false | **0** | team.md check 1's own sentence, observable: no goal definition blocks **only** when a `--target` was named |
| `run-checks no-such-team` | `{"error": "team not found: no-such-team"}` | — | **3** | not-found stays its own tier, folded into neither 2 nor 5 |

R2's real message, pasted verbatim — it carries the review bifurcation rather than a bare label
(Principle XV / checker-form C-33):

```text
3. target-terminal  target-terminal — Target T-001 处于终态 'dropped',run 停止——复核二分:
   属实则返回报告结束;证据不符则经 /speckit.goal targets --set open --id T-001 重开后重新
   发起 run。不提供终态执行旁路
```

### The 2 / 4 / 5 tiers, constructed in a throwaway copy

```text
TIER 2  --target not-a-target            verdict=input-error  blocked=False  EXIT=2
        checks: 1 ok · 2 not-evaluated · 3 not-evaluated · 4 not-evaluated · 5 ok
TIER 4  goal.md status: finished         {"error": "goal definition 'draw-two-layer-structure'
        (outside the lifecycle set)       declares status 'finished', outside the lifecycle set
                                          ('active','achieved','abandoned') — the goal-terminal
                                          check has no decidable subject"}                EXIT=4
TIER 5  goal.md status: achieved         verdict=goal-terminal  blocked=True   EXIT=5
        — with NO --target at all, so ⑤ blocks on its own
```

C-18's three tiers are therefore mutually distinguishable on the same team definition: **5**
(a check judged the run blocked), **2** (the argument matched neither grammar), **4** (the
definition could not be interpreted). The tier-5 run also settles the one semantic question
this phase had to resolve: ⑤ goal-terminal blocks with or without a target, because team.md's
check 5 ("终态 goal 只读") is a property of the goal and carries none of the target-scoping
sentence that check 1 carries — and SC-007 expects `blocked` true for a terminal-goal team
without saying whether it has a focus. Both readings of SC-007 are satisfied by this choice;
only one is satisfied by scoping ⑤ to targets.

### Zero writes (C-3 / SC-007 Source), measured as a byte checksum

```text
md5 over every file in .specify/goal/ and .specify/teams/, stable order:
  before all runs  dad5e7c5f584e0efe82e533b965d3485
  after  all runs  dad5e7c5f584e0efe82e533b965d3485      BYTE-IDENTICAL
```

That checksum was taken across R1–R4, the whole-team sweep below, and every constructed tier
(each of which ran against the copy, with `--repo-root` pointing at it). The real definitions
were never opened for writing — `run_checks` contains no write point at all, which
`test_run_checks.py::test_c3…` asserts both by checksum and by a write-point scan.

### A real repo finding this action surfaced on its first run

`viz-skill-arena` declares `goal_slug: visualization-skill-selection`, and **no such definition
exists**. Before this action the dangling binding was invisible: nothing enumerated team
bindings against the archive. Now one read-only call names it, and names the remedy:

```text
run-checks viz-skill-arena                -> goal-binding: no-goal-definition, blocked=false, EXIT=0
    message: 绑定 goal 'visualization-skill-selection' 无定义文件;先经 /speckit.goal migrate 落为定义
run-checks viz-skill-arena --target T-001 -> goal-binding: no-goal-definition, blocked=TRUE,  EXIT=5
```

The pair is the target-scoping rule demonstrated on live data: the same verdict, blocking only
once a Target is named. **Not fixed here** — repairing another feature's team binding is outside
053's declared scope, and the tool's job is to make it visible, which it now does. Recorded for
`/speckit.team` or `improve-team` to act on. The remaining four teams declare no `goal_slug`
at all, so their identity resolves to `none` and they report the same non-blocking verdict:
`cws-workspace-cluster`, `draw-plantuml-optimizer`, `requirement-implement-monitor`,
`summarize-project-optimizer`.

### A pre-existing defect found while wiring this, escalated not fixed (A-9)

`--json` and `--repo-root` are declared on a parser shared by the top level and every subparser,
and the source comment claimed that made them position-independent. **Measured false**: argparse
lets a subparser overwrite a namespace attribute the top level already set, so `--json list`
emits the human form and `--repo-root X list` resolves to the cwd. Evidence: the same `list`
action observed through `_emit` gives `as_json=False` for `["--json","list"]` and `True` for
`["list","--json"]`. Fixing it (suppressing the subparser defaults) would change flag precedence
for all ten actions, which is outside FR-029…FR-034 — so it is escalated as `research.md` **A-9**
and handled the way A-1 was: the false comment and the false Tool-record line
(`.specify/memory/tools/goal-utils.py.md`, which said "accepted **both before and after** the
subcommand") are corrected to state the measured behaviour, `contracts/run-checks.md` C-11's
falsified premise is annotated in place, and `test_run_checks.py` pins **both directions** so a
future fix and a further regression both fail loudly. Every invocation in this record passes the
flags after the action.

## 场景 9 — US5 的 SC-009 双向演示与三档失败(改后实跑,2026-10-04,T042)

Built in `mktemp -d` with `\cp -r skills $repo/skills` — a copy of the **real** skills tree, so the
member set is the seven real `draw-*` skills and not a synthetic stand-in. The goal definition carries
two criteria over the *same* subject set, one in each form, which is what makes the difference visible
in one output rather than across two runs. The real tree is only ever read (verified at the end).

```text
BEFORE   derived: skills/draw-d3js, draw-diagram, draw-drawio, draw-echarts,
                  draw-excalidraw, draw-mermaid, draw-plantuml        state=ok   (7 members)
         enumeration text: "Seven skills (draw-diagram and draw-{d3js,drawio,excalidraw,
                  mermaid,plantuml}) each ask for feedback."

REMOVE skills/draw-d3js
         derived: draw-diagram, draw-drawio, draw-echarts, draw-excalidraw,
                  draw-mermaid, draw-plantuml                          state=ok   (6 members)
         enumeration text: UNCHANGED — still "Seven skills (… draw-{d3js,…})"

ADD skills/draw-xyz
         derived: … draw-plantuml, draw-xyz                            state=ok   (7 members)
         enumeration text: UNCHANGED — still names the old six, and still says "Seven"
```

**This is SC-009 and it is the whole argument in one table.** After the removal the enumeration
criterion asserts a member that no longer exists; after the addition it omits one that does — and in
both cases it still says "Seven", which is now true only by accident (7 ≠ the 6 it names, then 7 ≠ the
7 it names). The derived set is right at every step without anyone editing the criterion. That is the
churn `.specify/goal/draw-two-layer-structure/goal.md`'s own `## History` records having actually
happened (「六个绘图技能」→「七个绘图技能」), so the demonstration reproduces a real defect on real
data rather than a constructed one.

### The three failure tiers, each with its positive control

| counter-sample | real output (decisive line) | EXIT |
|---|---|---|
| `SUBJECT MISSING:` | `criterion 1 references [subjects: nope/nothing-*], whose literal prefix does not exist in the repository — a reference that denotes nothing is not the same fact as one denoting an empty set; fix the glob or restore the directory` | **4** |
| `SUBJECT EMPTY:` | `criterion 1 references [subjects: skills/zzz-*], which exists but matches nothing — an empty subject set would make 'every subject satisfies this' vacuously true; widen the glob or populate the directory` | **4** |
| `SUBJECT CONFLICT:` | `criterion 1 carries both the reference form [subjects: skills/draw-*] and a brace-expanded member list — one subject set must have one source, so drop the retyped members or drop the reference` | **4** |
| **positive control** | the same criterion with the brace enumeration removed → `valid` | **0** |

The two "nothing there" tiers share an exit code and differ by **prefix**, which is the distinction
C-5 actually requires ("退出码/verdict … 互相可区分"): the remedies are opposite (fix the glob vs.
look at the directory), so collapsing them would leave the author unable to act. The positive control
is what makes the three meaningful — without it, a parser that reported every criterion invalid would
produce the same three lines.

### The second parser (C-14's disposition, executed)

```text
build-summary-input.load_goal_definition(...).criteria[0] =
  Every skill under (subjects: skills/draw-diagram, skills/draw-drawio, skills/draw-echarts,
  skills/draw-excalidraw, skills/draw-mermaid, skills/draw-plantuml, skills/draw-xyz)
  delegates its rendering to one engine.
```

Same seven members as the engine derived, and no opaque tag left in front of a summary reader. The
derivation is local by design — `load_goal_definition`'s own comment records that a cross-tree import
of `goal-utils.py` breaks once installed — so the price is two derivations, and the sync is pinned by
`test_criterion_subject.py::test_c15…` rather than left to memory. The owner document names the file
and this disposition, and also records that the same script keeps a **fifth** exit-code convention in
this repository (`EXIT_NO_MATERIAL = 3`, `EXIT_SERIALIZED = 4`) whose 3/4 mean something different from
`goal-utils.py`'s `EXIT_NOT_FOUND`/`EXIT_INVALID`; that divergence is documented, not unified (C-16).

### Backward compatibility and the residue

```text
$ python3 scripts/python/goal-utils.py validate draw-two-layer-structure
valid                                     real goal EXIT=0
residue: 0                                (after \rm -rf $tmp; ls -d $tmp | wc -l → 0)
```

The only real definition is pure enumeration, so it derives no subject set at all
(`parse_goal(...)["subjects"] == []`) and validates exactly as before — SC-010's name-level comparison,
whose anti-vacuity companion (C-12: at least one definition scanned, and a member set actually
produced) is asserted in the same test rather than assumed from an empty delta. Suite state after US5:
`test_criterion_subject.py` + `test_run_checks.py` + `test_goal_definition.py` + `tests/unit/test_goal_utils.py`
→ **165 passed, 0 failed**, so the pre-existing goal suites are unaffected.
