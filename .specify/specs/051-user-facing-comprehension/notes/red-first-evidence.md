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
