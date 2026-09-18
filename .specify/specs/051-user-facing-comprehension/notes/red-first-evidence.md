# Red-First Evidence — Feature 051 (User-Facing Comprehension)

**Purpose**: a structural contract test necessarily fails before its artifact exists. That
failure is only evidence if the *reason* is "artifact missing" — an import error or a
mis-written assertion produces the same red count and proves nothing. Each phase records
its run here, and per finding B-12 also states **which clauses are green by construction at
that moment and why**, so a passing clause is never read as "the assertion must be wrong"
and weakened.

Append-only: later phases (T016, T024, T035, T040) add sections below, never edit this one.

---

## Phase 2 / US1 — T005 (2026-09-18)

**Deliverables under test**: T003 `tests/contract/test_user_facing_comprehension_doc.py`
(discipline-doc **C-1…C-18** + the four gate-neutrality clauses **C-2/C-3/C-5/C-6** that
`contracts/gate-neutrality.md`'s ownership table assigns to it) and T004
`tests/contract/test_user_facing_comprehension_section.py` (ambient-section **C-1…C-11**).

**Command**

```bash
python3 -m pytest tests/contract/test_user_facing_comprehension_doc.py \
                  tests/contract/test_user_facing_comprehension_section.py -q
```

**Result**: `28 failed, 6 passed` · collection `34 tests collected`, **0 skipped, 0 errors**
(collection succeeded ⇒ no import error; an import failure would report `errors`, not
`failed`).

### Failure reasons — all artifact-missing

| Count | Reason | Missing artifact |
|---|---|---|
| 17 | `FileNotFoundError: [Errno 2] No such file or directory: 'shared/guidelines/user-facing-comprehension.md'` | truth doc (T006) |
| 4 | `AssertionError: section heading '## User-Facing Comprehension' not found` | ambient section body (T007) |
| 3 | `AssertionError: '## User-Facing Comprehension' must appear exactly once in the {template,mirror,live instructions file}, got 0` | STR-004 heading on all three surfaces (T007 → T008 → T009) |
| 1 | `AssertionError: '## User-Facing Comprehension' missing` | C-8's position anchors |
| 1 | `AssertionError: truth document missing at its canonical name: …` | truth doc (C-3's existence half) |
| 1 | `AssertionError: truth document missing: …` | truth doc (C-1) |
| 1 | `AssertionError: mirror missing: .specify/shared/guidelines/… — run sync-mirrors.py --write --only shared` | mirror (T008) |

No failure carries an `ImportError`, `ModuleNotFoundError`, `SyntaxError`, `NameError`, or a
comparison between two wrong values. The reads are deliberately **unguarded**
(`path.read_text`, no `is_file()` pre-check) so the missing artifact surfaces as
`FileNotFoundError` naming the path rather than as a generic assert.

### The 6 green clauses are green *by construction*, not by accident

| Clause | Why it passes before any artifact exists | Becomes a real check at |
|---|---|---|
| doc `test_gn_c2_gate_scan_total_unchanged` | Asserts the scanner still reports `total 23 / violations 0`. The scanner is a **zero-change surface** this feature must not touch — it is untouched today, so the clause holds from the start. Its job is to catch a *later* budget breach (T007's new lines, US2–US5's pointer lines). | Already live; re-proven by T011/T020/T031/T038/T055 |
| doc `test_gn_c3_scanner_constants_unmodified` | Same: `len(BLOCKING_PATTERNS) == 17` and the `POLICY_DOCS` / `SELF_REL` values are this feature's *inputs*, not its outputs. | Already live |
| doc `test_gn_c5_no_new_executable_scripts` | No `.py`/`.sh` outside `tests/contract/` has been added since `BASE_SHA`. True now; the clause exists to keep it true through US2–US5. | Already live |
| doc `test_gn_c6_zero_change_surfaces_untouched` | `src/specify_cli/`, `scripts/`, `templates/plan-template.md` are clean against `BASE_SHA` — T002 measured exactly this and recorded `0`. | Already live |
| section `test_c7_pinned_position_window_is_undisturbed` | Asserts `## Documentation Map` → `## Proactive Flow Trigger` → `## Fact, Correctness…` stay **consecutive**. T007 has not run yet, so the window is trivially intact. The clause's value is that it must *stay* intact after T007 inserts a new section. | T007 (insertion must land outside the window) |
| section `test_c11_no_dangling_guideline_pointer_on_either_instruction_surface` | Every guideline pointer on both instruction surfaces resolves today (measured: template 7, live 8, full set 11, remainder exactly the 3 structurally unpointed files). Adding the 12th guideline's pointer shrinks nothing; **removing** any existing pointer grows the remainder past the three named files and fails — that asymmetry is C-11(b)'s subset semantics, and it is why this clause is green before and after. | Already live; re-proven by T013 scenario 2 |

### Two defects found *in the tests themselves* while taking this evidence

Both were caught by the red-first run rather than by reading, which is what the step is for.

1. **`_changed_files` was blind to untracked files.** gate-neutrality C-5/C-6 derive their
   change set from `git diff --name-only <BASE_SHA>`, which reaches **tracked** paths only.
   This feature's own artifacts are untracked until the phase-boundary commit, so during the
   run window both clauses could not see the very files they exist to judge — a new
   `.sh` anywhere in the repo would have passed C-5 silently. Fixed by unioning
   `git ls-files --others --exclude-standard` into the change set. The fix was verified not
   to drag in the other unit's in-flight work: the only untracked non-test path in the repo
   is `skills/draw-diagram/references/self-deploy-render-service.md` (a `.md`, outside both
   clauses' scope). **This is the third "blind check" defect found this feature** (after the
   `--stat` piping form and `git diff HEAD`'s CI vacuity) and the same shape: a command whose
   output is empty for a reason unrelated to the proposition it was supposed to test.
   The failing assertion that exposed it was C-5's own anti-vacuity sanity guard — a guard
   added for exactly this purpose paid for itself on its first run.

2. **C-3 was vacuous.** As first written it compared two literals inside the test file to
   each other (`DOC.name == DOC_NAME`) and never looked at the tree, so the clause's actual
   normative content — *MUST NOT be renamed* — was unasserted: a rename would fail C-1
   ("missing") and pass C-3. Rewritten to scan `shared/guidelines/*.md` for any
   `*comprehension*` variant that is not the canonical name. **Proven non-blind by
   empirical probe**, not by inspection:

   ```bash
   cp -f shared/guidelines/token-efficiency.md shared/guidelines/user-facing-comprehension-v2.md
   python3 -m pytest tests/contract/test_user_facing_comprehension_doc.py::test_c3_filename_is_exact_and_not_renamed -q
   # → AssertionError: shared/guidelines/ holds a renamed variant of the truth document:
   #   ['user-facing-comprehension-v2.md']. …
   \rm -f shared/guidelines/user-facing-comprehension-v2.md   # probe artifact removed; verified count 0
   ```

   This moved C-3 from the green-by-construction list to the red list, which is the correct
   direction: a clause that cannot fail is not a clause.

### Clause-coverage reconciliation

| File | Clause range | Functions | Derivation |
|---|---|---|---|
| `test_user_facing_comprehension_doc.py` | discipline-doc C-1…C-18 | 19 | C-1…C-17 one each (17) + C-18 split into `c18a`/`c18b` (2) |
| ″ | gate-neutrality C-2, C-3, C-5, C-6 (carried) | 4 | named `test_gn_cN_*` so they do not collide with discipline-doc's own C-2/C-3/C-5/C-6 |
| `test_user_facing_comprehension_section.py` | ambient-section C-1…C-11 | 11 | one per clause |
| **Total** | | **34** | matches the collected count |

Every function name maps one-to-one onto its contract clause number.

**Re-derive**: `python3 -m pytest <both files> --collect-only -q | tail -1` → `34 tests collected`;
per file, `grep -c '^def test_' tests/contract/test_user_facing_comprehension_{doc,section}.py` → `23`, `11`.

---

## Amendment after T013 — one "green by construction" entry was green for the wrong reason

The table above lists section `test_c11` as green before any artifact exists, on the grounds
that "every guideline pointer on both instruction surfaces resolves today". That was true as
measured, and the clause was still **too weak to be worth its name**. SC-017's stated drill —
construct a project state where the ambient section is present but the truth document is
missing — was run during wrap-up:

```bash
mv .specify/shared/guidelines/user-facing-comprehension.md /tmp/   # simulate the downstream state
python3 -m pytest tests/contract/test_user_facing_comprehension_section.py::test_c11_no_dangling_guideline_pointer_on_either_instruction_surface -q
# → 1 passed            <-- the guard did NOT fire
```

**Root cause**: C-11 resolved each pointer's target against the framework **source** tree
(`shared/guidelines/<name>.md`) while the pointer text — and therefore the reader — resolves
`.specify/shared/guidelines/<name>.md`. In this repo both exist, so the source check is a
weaker proxy that happens to agree. In a downstream project only the runtime copy exists, so
the one failure mode the clause exists to catch was structurally invisible to it. Same shape
as the other three blind checks this feature found: the command returns an answer, the answer
just isn't about the proposition.

**Fix**: assert both halves — the runtime copy (what a reader opens) and the framework source
(what regenerates it). Re-drilled in both directions:

| Simulated state | Clause verdict |
|---|---|
| normal | `11 passed` |
| runtime copy removed | **fails** — "no runtime copy under .specify/shared/guidelines/" |
| framework source removed | **fails** — "no framework source under shared/guidelines/" |
| both restored | `34 passed`, `cmp` → BYTE-IDENTICAL |

Lesson for the other green-by-construction entries above: "green today" is not evidence the
clause can go red. Each of the six should be drill-tested the way C-3 and C-11 now have been;
the four gate-neutrality clauses and section C-7 are pinned by equality/ordering assertions
whose failure modes are already demonstrated by existing tests, so C-11 was the exposed one.

---

## Phase 3 / US2 — T016 (2026-09-18)

**Deliverables under test**: T014 `tests/contract/test_user_facing_comprehension_pointers.py`
(surface-pointers **C-1…C-14**) and T015's new assertion in the pre-existing
`tests/contract/test_confirmation_gates_execution_report.py` (FR-034's missing guard).

**Command**

```bash
python3 -m pytest tests/contract/test_user_facing_comprehension_pointers.py \
                  tests/contract/test_confirmation_gates_execution_report.py -q -rx
```

**Result**: `5 passed, 9 xfailed` + `9 passed, 1 xfailed` · collection `24 tests collected`,
**0 errors** (so no import defect) · whole-suite `FAILED` count **unchanged at 26**,
`comm -13` against the frozen baseline **empty**.

### The pending partition is carried by `xfail(strict=True)`, not by failing

surface-pointers' clauses are claimed by three stories (US2 = C-2/C-4/C-5, US4 = C-10,
US5 = the rest), so this file is *designed* to be partly unsatisfied from US2 until US5.
Left as ordinary failures that would add 10 `FAILED` node IDs at T014 and keep them there for
three phases — which collides with GATE-1 ("zero new test failures versus the frozen
baseline") at every phase boundary in between. Marking each not-yet-due clause
`xfail(strict=True, reason=<the task that turns it green>)` resolves the collision without
weakening anything:

* an xfailed case is not a `FAILED` line, so GATE-1 stays satisfiable at each boundary;
* `strict=True` reports **XPASS as a failure**, so a marker cannot outlive its subject — the
  story that lands the work is forced to remove it;
* the reason string names the owning task, so the pending set is self-documenting.

The rejected alternative was re-freezing `baseline-failed.txt` to include the 10 IDs. That
would be undetectable decay: `comm -13` reports *additions* only, so a clause absorbed into
the baseline could stay red forever and no gate would ever notice. This is the same
"green because blind" class recorded in Phase 2 above, arriving through the baseline instead
of through an assertion.

### Red at this point (US2's own取证 targets)

| Clause | Why red | Turn-green task |
|---|---|---|
| C-2 | `confirmation-gates.md` has no pointer line yet, so neither the count nor the header-position half can hold | T017 → T021 |
| FR-034's new guard (`test_doc_carries_comprehension_discipline_pointer`) | same subject as C-2, asserted from the pre-existing execution-report file so the obligation has a second, independent home | T017 → T021 |

### Green at this point, and why that is correct rather than suspicious

| Clause | Why green before any edit |
|---|---|
| C-3 | Mirrors are in sync because nothing has been edited yet. It is a **freeze** assertion: it goes red if a source is edited without re-syncing, which is what T019 exists to prevent. |
| C-4 | The five criteria sections are byte-frozen by SHA-256 and untouched. Green now is the point — it must *stay* green through T017/T018, which edit the header and `:68` only. |
| C-5 | `:58-60`'s triad is still owned by `confirmation-gates.md`, and the truth document already reaches it by path (T006 landed that side). Both halves hold before US2 starts. |
| C-7 | `interview-pattern.md:125-126`'s two pattern-specific rules are untouched; freeze assertion, US5's T041 must not drop them. |
| C-14 | `regen-command-copies.py --check` is EXIT=0 today and `.specify/templates/commands/` does not exist. |

The remaining xfailed clauses (C-1, C-6, C-8, C-9, C-10, C-11, C-12, C-13) are **US4/US5's**
取证 targets, not US2's; T035 and T040 own those runs.

### Two needle defects found while authoring, both proven by measurement

1. **C-13's first needle set was keyed to the owner and therefore vacuous.** It used literals
   from the truth document's own rule text (`白名单之外的行话一律按违规处理`, `长度不设界但形态设界`,
   …). The truth document is brand new, so *nothing* in the repo can be restating its exact
   wording — the clause passed on an empty match and `strict` xfail reported **XPASS**, which
   is how the defect surfaced. C-13's subject is the **pre-existing dispersed wordings**, so
   the needles must be their characteristic literals. Re-keyed and measured:

   | Needle set | Files matched before convergence |
   |---|---|
   | owner's own literals (wrong) | **0** — vacuous |
   | dispersed-wording literals (correct) | **2** (`shared/patterns/interview-pattern.md` ×6 needles, `shared/workflow/feedback-step.md` ×1) |

   Both matched files are convergence targets (T041, T036), so the count must reach 0 after
   US4/US5. **Scope limit recorded in the test rather than hidden**: this is a *literal* scan.
   Research measured 38 dispersed wordings, most of them paraphrases no literal needle can
   match, and FR-033 forbids building a wording scorer — so C-13 pins the
   literally-identifiable subset and the rest are verified per-site by C-6/C-9/C-10/C-11.
2. **C-13 and C-12 would have contradicted C-18 without an explicit exclusion.** Three of the
   dispersed wordings are *required to survive*: `project-overview.md:51`'s landing check and
   `requirements-guidelines.md:24,101`'s baseline declarations are registered override sites
   under discipline-doc C-18(b), and C-12 separately requires `:309` and `:51` kept. Had those
   literals gone into C-13's needle set, C-13 would demand their removal while C-12/C-18
   demand their presence — an unsatisfiable pair of the same shape as the B-09 and B-10
   defects this feature already corrected twice. The exclusion list is written into the test
   with the reason per item.

### C-12(c)'s required pre-rewrite needle measurement

C-12(c) demands the needle's effectiveness be proven by its hit count **before** the rewrite.
C-12's needle is *derived* from the truth document's blacklist section, and T046 is what puts
the identifier literals there — so today the derived set is legitimately empty and the clause's
own anti-vacuity sentinel is what fails (correctly, as `xfail`). Measured with §1.7's literals
standing in for the post-promotion needle:

```
skills/summarize-project/references/reporting-playbook.md   hits=12   e.g. `T1` `E1` `RC-1` `RC-5`
TOTAL FILES = 1
```

So the needle is falsifiable: **1 file / 12 hits before T046, must be 0 after**. The sentinel
asserting the derived set is non-empty is what stops C-12 passing vacuously in the meantime.
