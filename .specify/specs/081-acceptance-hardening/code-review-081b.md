# Code Review — Feature 081, slice 081b

**Range**: `97014440..4c07fdc9`
**Scope**: `scripts/python/closure-acceptance-check.py`, `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`, `shared/workflow/{acceptance-hardening,expression-gates}.md`, `templates/plan-template.md`, `tests/fixtures/acceptance-hardening/{premise-mutation,runtime-gap-mutation,runtime-zero-row,inherited-mutation,inherited-clean}/`, `tests/contract/{test_acceptance_premises,test_expression_gates_doc}.py`, the three deliberately adjusted modules (`tests/unit/test_pre_analyze_check.py`, `tests/contract/test_expression_gate_wiring.py`, `tests/contract/test_doc_consistency_checker.py`), the spec artifacts under `.specify/specs/081-acceptance-hardening/`, and the generated mirrors.
**Excluded**: `90de4d7f fix(coaching-skills)` — a concurrent non-081 commit inside the range; its files are not judged as 081 work.

## Findings

### blocking

1. **The dependency extraction was repaired in one producer only** — `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:621` `declared_dependency_files()` still joins **every** backticked `.md` token in § Inherited Blockers against `<spec-dir>`, while `scripts/python/closure-acceptance-check.py:974` reads only the paths inside the `**Dependency artifacts` block. `notes/red-first-evidence-081b.md` §2.4 records the repair as belonging to the closure checker and never says the twin is left behind. Measured on this feature's own plan (`--stage plan --repo . --spec-dir .specify/specs/081-acceptance-hardening`): the gate resolves `requirements.md`, `tasks.md`, `research.md`, `verification.md` — the spec's own four artifacts — and resolves **none** of the four declared `071`/`077` files, producing nine fabricated `inherited-blocker-undisposed: 081:*` reasons in a 10-error failure. The closure checker on the same tree emits no inherited reason. The reason this survived the suite is leg-specific and worth naming: `test_acceptance_premises.py` leg (d) asserts producer equality only on fixtures, and the fixtures declare their dependencies by **fixture-local filenames** that resolve nowhere outside the fixture directory, so the collision cannot occur there.

### important

2. **`inherited-later` cannot be read by the gate** — `pre-analyze-check.py:761` `later_slice_is_legal()` reads the claimed status from `<spec-dir>/feature-detail.md`, a filename only the fixtures use; a real spec dir carries no such file (`False`, measured), so the documented legal reading degrades to `carrier_resolves(("test", path), …) → False` at `pre-analyze-check.py:756` and the row is reported as undisposed. The closure checker resolves the claim from `.specify/memory/features.md` (payload field `claimed_status_source`) and reads the same row as `inherited-later`. One rule, two verdicts, and the failing one is the gate every plan stage runs. The fix also has a contract gap to close: C-17 states the condition ("the parent feature's claimed status is `Blocked`") but no artifact says **where** the claim is read from.
3. **The declaration marker is an undocumented literal with a silent failure mode** — `closure-acceptance-check.py:983` requires the exact string `**Dependency artifacts`; absence yields `[]`, not an input error. The owner states the rule without its shape (`shared/workflow/acceptance-hardening.md:350-353`) and the plan skeleton future plans inherit (`templates/plan-template.md:180-182`) repeats the obligation without the marker. Probe: rewording the marker in `inherited-mutation` drops `inherited-blocker-undisposed: 901:SC-004_status` and leaves exit 1 with one reason — a compliant plan can disable the fourth finding without any red signal. Compare C-13's own lesson (zero data rows must block, never be silent): the declaration's absence is the same shape one level up.

### suggestion

- `ABSENT_LOCATORS` (`pre-analyze-check.py:124`, `closure-acceptance-check.py:222`) invents a second `Source row` grammar. `(none)` is accepted, `—` (the emptiness spelling used in every other cell of the same tables) exits 2, and no artifact documents either. All ten fixture sets and the three adjusted unit fixtures now depend on the undocumented form, so the sentinel has become load-bearing without ever being declared.
- `verification.md:7` `post_change_commit=8ce0f006` and `verification.md:99` `deferred_tasks=T024` describe the previous slice's tree. The template calls the field a mirror of `[~]` rows; the current `tasks.md` has none, so the log asserts a deferral its own task list does not contain, and a dependent feature would extract it as a live locator.
- `tasks.md:234` says `EP-001…EP-009` while `tasks.md:18` and `plan.md` say ten premises. Two ranges in one file is the drift the slice's own one-source rule is aimed at.
- `data-model.md:195` describes `inherited-clean` as five dispositions; the fixture has six rows, and the omitted one is the only fixture row carrying the `gate:<GATE-ID>` form.

### nitpick

- The `_dedupe()` helper is a good call (a runtime row citing a falsified premise and the premise table itself would otherwise double-count one defect), but it is applied only to the closure checker; the gate's `add()` path can still emit two findings that reduce to one fact.
- `run()` re-reads `tasks.md` into `tasks_text` and passes it twice under two names (`tasks_text`, `carrier_tasks_text`); the intent is documented in `check_ownership`'s docstring, so this is only a naming smell.

### question

- The two `declared_dependency_files()` implementations are near-identical and have already diverged once. Is the intended single source a shared helper module, or two copies kept in step by a test? Nothing in `shared/workflow/acceptance-hardening.md` answers it, and the divergence this slice produced is the cost of not answering.

### praise

- `_section_lines()` returns absolute 1-based line numbers and a finding that points at the wrong line would be a defect of the checker. Measured: a runtime-stack heading carrying a Chinese title tail still located its prose declaration at the true line (probe: declared on line 37, reported on line 37) — the heading-tail branch is correct, not merely plausible.
- `test_a3_the_reserved_argument_is_a_member_of_its_own_template_only` asserts non-membership for six outsiders, so the reserved slot cannot quietly widen into a wildcard.
- `test_c5_an_inherited_later_row_neither_blocks_nor_reads_as_resolved` flips the parent's claimed status to `Implemented` and asserts the same row becomes undisposed — the reading is shown to be conditional rather than asserted as a comment.
- `test_b3_the_tasks_duty_is_line_level_and_a_table_row_never_satisfies_it` keeps the whole-file substring intact before asserting the line-level failure, which is the only way that counterexample proves anything.
- The three adjusted fixtures were made **conforming** rather than weakened, with the reason (a delegate `exit 2` would leave the face `not-evaluated`) written at the edit site. That is the right direction when a new mandatory shape lands under older fixtures.

## Gate

One `blocking` entry: the gate's extraction (finding 1), which is a defect in this slice's own deliverable rather than the cause of the feature's status. The feature stays `Blocked` on the acceptance axis (SC-001 1/3 call sites, SC-002 `partial`, closure checker `block` / exit 1 / `zero-final-path-pass`); this slice neither moves it nor should be read as clean until findings 1–3 are repaired and the plan-stage gate plus the closure checker are re-run on this feature's own spec directory.


## Review-fix dispositions

| Finding | Disposition | Evidence |
|---|---|---|
| blocking 1 — one-producer repair | **Fixed**: `declared_dependency_files()` in `pre-analyze-check.py` now uses the same declared-block parser and self-exclusion as the closure checker, and `repo` is threaded through `check_inherited` → `extracted_dependency_rows` | plan gate on this spec dir: `decision=pass errors=0`; real-spec leg `test_d2` |
| important 2 — `inherited-later` unreachable | **Fixed**: `resolve_claimed_status()` reads the spec dir's `feature-detail.md` / `feature-registry.md`, then `.specify/memory/features.md` by spec-dir key; IB-004's `test:`-only later-slice carrier is accepted | plan gate on this spec dir: no `inherited-blocker` finding |
| important 3 — undocumented marker | **Fixed**: the marker is published in `shared/workflow/acceptance-hardening.md` and `templates/plan-template.md`; a dependency set without the block raises `InputError` (exit 2) in both producers | `test_d3`, `test_d5` |
| suggestion — absent sentinel | **Fixed**: `—` (and the legacy `(none)`) is the documented absent-row sentinel and is accepted by both producers | `test_d4` |
| suggestion — stale verification carriers | **Fixed**: `post_change_commit=4c07fdc9`; `deferred_tasks=` empty with the note that T024 belongs to 081a/081d | `verification.md` |
| suggestion — premise range | **Fixed**: `EP-001…EP-010` | `tasks.md` |
| suggestion — fixture census | **Fixed**: all six `inherited-clean` rows are named, including the `gate:GATE-1` carrier | `data-model.md` |
| nitpick — duplicate findings in the gate | **Recorded, not fixed**: `_dedupe()` remains closure-only; the gate's two findings reduce to one fact but do not change a verdict. 081c/081d can decide whether a shared helper is the right owner | this section |
| nitpick — two names for one tasks text | **Recorded, not fixed**: the naming documents two different questions (duty ② vs carrier resolution) | `check_ownership` docstring |
| question — one parser or two copies | **Answered for now**: two copies kept in step by leg (d2)'s real-spec run; extracting a shared stdlib module crosses the `skills/` ↔ `scripts/` boundary and is deferred to a later schema-owner decision | `test_d2` |

Targeted set after the fix: `145 passed`, exit 0
(`test-evidence/tasks-081b-review-fix-tests.txt`). The feature remains `Blocked`.
