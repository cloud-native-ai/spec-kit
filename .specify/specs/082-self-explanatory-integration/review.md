# Specification-Driven Development (SDD) Process Review Report: Self-Explanatory Framework Integration (不言自明的框架集成)

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

> **Scope note for this run.** This is the **continuation** of `/speckit.review` for Feature 082. The
> code segment already ran and its record is `.specify/specs/082-self-explanatory-integration/code-review.md`
> (base `2f6b8bbb` → head `b2880fa0`, `renderer: text`). This run completes the three remaining
> segments — process, artifact, implementation — the Acceptance Reality Check, the answers owed to
> each code-segment `important` item, and the status gate. The code segment's full per-file table is
> **not** re-written here; § 2.1 carries its verdict and pointers only.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 082 |
| Requirement Key | 082-self-explanatory-integration |
| Requirement Name | Self-Explanatory Framework Integration (不言自明的框架集成) |
| Related Feature | 082 Self-Explanatory Framework Integration |
| Repository | spec-kit |
| Repository URL | `git@github.com:cloud-native-ai/spec-kit.git` (remote `github`); `origin` is `git@github.com:github/spec-kit.git` — the **upstream** project, which does not contain these commits |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty (the branch is unpushed). Citations below use absolute paths plus `git show <sha>:<path>` recovery instructions |
| Branch | `082-self-explanatory-integration` |
| Commit SHA | `b2880fa081a52b53b3a6b8411c8dcc5c4493db27` (short: `b2880fa0`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-05 |
| Reviewer (Agent) | SDD execution agent (unattended loop), reviewer of record `Qiming Liu (John)` per the code segment |
| Environment | Linux 5.10.134-15.2.al8.x86_64, bash, Python 3.11, pytest; no network in any measurement |
| spec-kit Source Snapshot | `/storage/project/cloud-native-ai/spec-kit` @ `b2880fa0` (self-hosting: framework sources and client runtime in one tree) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 193 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/requirements.md` | 12 FR (FR-001…FR-012) / 9 SC, each SC carrying a `**Path**` marker |
| plan.md | 255 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/plan.md` | Constitution Check with no Fail and no Partial row, 4 execution premises, 10-row mirror obligation table |
| tasks.md | 302 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/tasks.md` | 53 dependency-ordered rows, all `[X]` |
| contracts/constitution-double-landing.contract.md | 107 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/contracts/constitution-double-landing.contract.md` | C-1…C-9 + legs M-1, M-2; C-20 is a pointer to the shared rule the mirror contract owns |
| contracts/instructions-propagation.contract.md | 91 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/contracts/instructions-propagation.contract.md` | C-10…C-19 + legs M-3, M-4 |
| contracts/mirror-distribution.contract.md | 96 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/contracts/mirror-distribution.contract.md` | C-20…C-28 (C-20 "shared by both landing contracts") + legs M-5, M-6 |
| contracts/glossary-integration.contract.md | 52 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/contracts/glossary-integration.contract.md` | C-29…C-34, no mutation leg |
| data-model.md | 140 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/data-model.md` | E-1…E-8 / V-1…V-19 / state machines |
| quickstart.md | 256 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/quickstart.md` | S-0…S-7; 5 executed, 3 pinned with premises |
| verification.md | 144 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/verification.md` | 9 SC status rows, smoke triple, 10 evidence records |
| code-review.md | 176 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/code-review.md` | code segment record (this run added the coverage-receipt block the template requires) |

## 1. Process Execution Timeline

Reconstructed from `git log` on the feature branch, `5085f46ff` first commit `dc83514e`.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Feature registered via `/speckit.clarify` | `dc83514e`, `.specify/memory/features.md` 082 row | none |
| 2 | requirements + plan + tasks + checklist + analyze landed stage by stage | `f712cf58` … `d4d6a396` | none |
| 3 | Implement run split into 10 parts with one E3 evidence file per part | `test-evidence/implement-part-{2..10b}.md`, `part2-stage-checks.md` | none (per-part discipline followed) |
| 4 | US1 carrier landed (`templates/instructions-template.md` unchanged, tpl 31) | `2161ac40` | none |
| 5 | **US2 landed the `## Self-Explanatory Structure (不言自明)` section into the template** — template `##` count 31 → 32 | `567834e2`; measured `git show 567834e2:templates/instructions-template.md \| grep -c '^## '` = 32 | **yes — an unguarded surface moved.** `tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` pins 31/32 and went red here. No evidence file in the delta names it |
| 6 | Live reconcile injected the same section — live `##` count 32 → 33 | `02fd6db5` | same as #5 |
| 7 | Implement closure: Completion Gate GATE-1…GATE-4, `verification.md`, `DoD Status`, feature `Planned → Implemented` | `1f6ab51c`, `test-evidence/implement-part-10a.md`, `implement-part-10b.md` | **yes — GATE-1's "no new failing node" was measured over a set that does not contain `test_fast_fail_discipline.py`**, so the red at #5/#6 was never in front of the gate. Recorded in § 3 F-1 |
| 8 | Spine write recording part 10b's closure lands one commit **after** the part's own evidence and the status flip | `b2880fa0` (9 lines in `.specify/state/082-…md`, 1 file) vs `1f6ab51c` (7 files incl. `implement-part-10b.md`) | minor ordering deviation; see F-4 |
| 9 | Code segment ran; record written without the mandated coverage-receipt block | `code-review.md` (untracked at review start) | **yes — the template calls a missing receipt block an "input error, never a prose-filled count"**. Repaired in this run by running the skill's own `receipt` step (§ 2.1) |
| 10 | Review continuation: process + artifact + implementation segments + ARC | this file | none |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 1 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 4 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 1 |
| Automation / Scripts | 1 |
| Workflow | 3 |
| Documentation | 0 |

Findings by id: `F1` P1/Workflow · `F2` P2/Automation · `F3` P2/Workflow · `F4` P2/Workflow ·
`F5` P2/Command Prompt.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `2f6b8bbbb061563769d6953371714b3494811795` | the resolved diff base |
| Head commit | `b2880fa081a52b53b3a6b8411c8dcc5c4493db27` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the code segment's reported resolution tier |
| Renderer mode | `text` | `code-review.md` header marker |
| Changed / judged / skipped / gap files | 69 / 69 / 0 / 0 | copied from the record's coverage-receipt block (`code-review.md:123`), written by `git-delta-review.sh receipt` |
| Segment verdict | `pass` | the record's `verdict=pass` |
| Gate verdict | `allow` (`blocking_entries=0`); 2 `important` items open and answered in § 3.5 | `git-delta-review.sh report --summary --file code-review.md` |
| Reason, when one applies | none | — |
| Uncommitted scope | 31 paths outside this record's subject (mostly `.specify/memory/session/` and `exec-quant/` records of earlier runs); disclosed, never concluded over | `receipt` line `uncommitted_scope=31` |
| Record | `.specify/specs/082-self-explanatory-integration/code-review.md` | written (triage `run`) |
| Archive | none | first code-segment run for this slice |

This subsection carries the verdict and the pointers only. The findings themselves live in
`code-review.md` and are read there; their answers are § 3.5.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, data-model.md, quickstart.md, verification.md, contracts/ | derived from the standard spec-stage product (`.specify/skills/internal/review-feature-quality/SKILL.md` § Segment A) and `plan.md` § Project Structure |
| Coverage line | 7 / 7 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `pass` | see findings table (zero artifact findings) |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| — | — | — | none | no artifact finding was raised; basis below |

**Basis for an empty artifact finding set** (the dimensions were walked, not skipped):

- **Completeness** — all seven expected members exist; `verification.md` carries one `SC-NNN_status=`
  row for each of the nine criteria (`verification.md:92-129`), so no member is a placeholder.
- **Internal consistency** — the counts that appear in several places are derived, not restated: the
  walk found the template/live/mandate counts (`18 / 19 / 11`) in exactly one owner
  (`tests/contract/test_constitution_double_landing.py:72-79`) and every other site asserts against
  it. The one literal family that *was* a second-order copy —
  `test_x13_double_landing_three_count_pins` — is repaired this run (§ 3.5, SUGGESTION answer).
  `features.md` and `features/082.md` agree on `Implemented`.
- **Traceability** — `SC-001…SC-009` each name an evidence path, and every one of those paths
  resolves on disk (checked by the closure checker's binding condition,
  `every_final_path_pass: true` with `unknown: 0`).
- **Dependency and premise ownership** — `plan.md` EP-003 (the inherited gate-total red) is declared
  with its owner and its `fallback` decision; `verification.md:115` carries the five-field ladder
  rather than rounding the `partial` to `pass`.
- **Acceptance honesty** — the one honest weakness, `SC-006 = partial`, is declared as `partial` with
  its reduced measurement, its run flag and its unblock condition. That is the vocabulary behaving
  correctly, not a finding.

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `2f6b8bbbb061563769d6953371714b3494811795` | the resolved diff base |
| Head commit | `b2880fa081a52b53b3a6b8411c8dcc5c4493db27` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `python3 -m pytest tests/contract/test_self_explanatory_constitution.py tests/contract/test_instructions_section_propagation.py tests/contract/test_self_explanatory_distribution.py tests/contract/test_self_explanatory_glossary.py -q` | recorded verbatim in `verification.md:29` |
| Smoke exit code | 0 | re-executed this run: `42 passed in 9.63s`, `EXIT=0` |
| Smoke evidence path | `.specify/specs/082-self-explanatory-integration/test-evidence/smoke-20261105.txt` | exists, 2321 B, non-empty |
| Scope and regression verdict | scope **pass**, regression **pass after this run's repair** — see the findings table | the segment's own reading |
| Segment verdict | `pass` | — |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | tests/contract/test_fast_fail_discipline.py | 715 | none | `test_a7` was left red by this delta: the feature added one `##` section to the template and the live file, moving the counts 31/32 → 32/33, while the pin stayed at 31/32. Repaired this run (pin raised to 32/33 plus an offset assertion); the green at base and the red at head are both measured and the repair carries its own mutation check. F-1 |
| P2 | tests/contract/test_fast_fail_discipline.py | 1146 | none | `test_x13`'s three counts were hard-coded literals, a second-order copy of a fact the double-landing contract owns; derived from the artifacts this run. F-2 |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | the bound feature detail's claim, copied |
| `final_path` record, copied verbatim (7/7) | pass 4 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 4 | `scripts/python/closure-acceptance-check.py --json`, copied and not recomputed |
| Comparison verdict | `agree` | `accept` agrees with the claim |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

## 3. Findings (Problems & Improvement Targets)

### F1 — A guard on a shared surface went red mid-implement and never reached a gate

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/tests/contract/test_fast_fail_discipline.py:715` (with `567834e2`, `02fd6db5`, `implement-part-10a.md:105-115`)
- **Evidence** (verbatim quote):

  ```
  # measured this run, at the reviewed head
  $ python3 -m pytest tests/contract/test_fast_fail_discipline.py -q
  E       AssertionError: C-7: template has 32 top-level sections; expected 31
  E       assert 32 == 31
  FAILED tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22
  2 failed, 102 passed in 1.75s
  ```

  and the gate that should have seen it (`test-evidence/implement-part-10a.md:105`):

  ```
  # T052 / GATE-1 — the fourth guard class + the baseline-red-adjacent suites, name-level comparison
  $ python3 -m pytest tests/contract/test_constitution_double_landing.py \
        tests/contract/test_instructions_section_propagation.py \
        tests/contract/test_glossary_mechanism.py \
        tests/contract/test_mirror_parity_suite.py \
        tests/contract/test_proactive_trigger_section.py -q --tb=no
  FAILED tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged
  1 failed, 821 passed in 6.80s
  ```

- **Why it's a problem**: `test_a7` guards `templates/instructions-template.md` and
  `.specify/instructions.md`, which is exactly the surface T022/T024 edited. It was green at the base
  (measured: pin 31/32, artifact 31/32) and red at the head, so the regression is this delta's. But
  the module is not in GATE-1's selected set, so `new_failures: none` was reported truthfully over a
  set that could not contain it. A gate that can only see the files it already lists is a gate that
  reports green for its own blind spot — this is the "a green check is a claim, not evidence"
  failure in its most ordinary form.
- **Proposed fix**: (a) immediate — the pin is raised to 32/33 with an offset assertion, repaired in
  this run (§ 3.5, IMPORTANT #1); (b) systemic — `templates/commands/implement.md`'s Completion Gate
  should require the gate set to be derived from the *set of files the delta touched*, not from a
  hand-listed module set; a delta that edits a file with a sibling guard must run that guard.
- **Repair status**: repaired for this feature; the systemic half is a recommendation (REC-W1).

### F2 — A guard's expected values were literals copied from another artifact

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `/storage/project/cloud-native-ai/spec-kit/tests/contract/test_fast_fail_discipline.py:1146`
- **Evidence** (verbatim quote, before this run):

  ```
  for name, want in (("TEMPLATE_COUNT", 18), ("LIVE_COUNT", 19), ("COMMAND_COUNT", 11)):
  ```

- **Why it's a problem**: the values are a second-order copy of facts owned by
  `tests/contract/test_constitution_double_landing.py:72-79`, which itself defers to
  `contracts/constitution-double-landing.contract.md#C-5`. This feature's own assumption A4 says
  "MUST NOT hardcode the template numeral into live or tests" — its counts belong to the same class.
  The cost is paid by whoever lands the next amendment: they must edit a pin inside a foreign
  feature's guard, and if they forget, the guard goes red on a tree that is correct.
- **Proposed fix**: derive the three expectations from the artifacts they describe, which is what
  this run landed (three `len(...)` measurements plus a non-zero anti-vacuity guard).
- **Repair status**: repaired (§ 3.5, SUGGESTION answer).

### F3 — A contract's mutation table does not own the red that proves its clause

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/082-self-explanatory-integration/contracts/instructions-propagation.contract.md:83-88` (`## Mutation legs owned by this file`)
- **Evidence** (verbatim quote):

  ```
  ## Mutation legs owned by this file

  | Leg | Mutation (on a temp copy, never the repository) | Assertion that must go red |
  |-----|------------------------------------------------|---------------------------|
  | M-3 | Delete the `## STR-001` section from a copy of the template | C-14's template-side presence assertion (and C-10 when redirected at the copy) |
  | M-4 | Run the generator on a fixture with no template section and assert nothing is injected | C-13's positive half, in its anti-vacuity form |
  ```

- **Why it's a problem**: C-14's discriminating evidence in this feature was **not** `M-3`. It was a
  real-tree red produced by drafting the section wrongly at T022 (summary and pointer on one physical
  line), which the `test_c21_*` carrier caught. That red proves C-14 can fail on a *real* defect, a
  strictly stronger form than a copy mutation — and no table names it, so a reader following
  "which leg proves C-14" reaches `M-3` and stops.
- **Proposed fix**: add a third row to that table for the real-tree red, carrying its producing task
  (T022) and its carrier (`test_c21_*`), distinguished from the copy-only legs. **Not applied in
  this run**: `contracts/` is a plan-owned artifact for this feature, and editing it here would be an
  undeclared plan edit.
- **Repair status**: recorded; the ownership half that *was* repairable (the `M-N` id collision in
  `notes/red-first-evidence.md`) is repaired — see § 3.5 IMPORTANT #2.
- **Owner path**: `contracts/instructions-propagation.contract.md` § Mutation legs owned by this file.

### F4 — The status flip and its closure are not in the same commit as the part they close

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/082-self-explanatory-integration.md` (spine) and commits `1f6ab51c`, `b2880fa0`
- **Evidence** (verbatim quote):

  ```
  b2880fa0 docs(082-self-explanatory-integration): record implement closure and start review
   .specify/state/082-self-explanatory-integration.md | 9 +++++++++
   1 file changed, 9 insertions(+)
  ```
- **Why it's a problem**: part 10b's own evidence (`implement-part-10b.md`) lands in `1f6ab51c`
  together with the `Planned → Implemented` flip, while the spine write that *records* that part's
  closure lands one commit later in `b2880fa0`. So the artifact that says "part 10b finished" and
  the spine entry that says the same thing are in different commits, and `git show 1f6ab51c` cannot
  show both. The part-8 checkpoint has the same shape from the other direction (`5085f46f` lands
  after part 9's code carrier `32fc3e70`). Every evidence file does declare its `stage_base`, so the
  timeline stays recoverable from artifacts — the degradation is to commit-order legibility, not to
  history.
- **Proposed fix**: a closure commit should carry the spine write for the part it closes, and a
  checkpoint commit whose spine delta is empty should fail an assertion, so a checkpoint that records
  nothing cannot be mistaken for one that recorded.
- **Repair status**: recorded; not repaired (the history is immutable, and rewriting it is out of
  scope).

### F5 — The Completion Gate's own smoke path does not exercise the modules it edits

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md` § Completion Gate
- **Evidence** (verbatim quote, from the feature's GATE-1 record):

  ```
  | GATE-1 | four guard classes green, no new failing node | **PASS** | ... 821 passed / 1 failed, and that failure is enumerated in `baseline-failed.txt` (`grep -c` → 1), so `comm -13` leaves nothing over |
  ```
- **Why it's a problem**: the gate's verdict is "no new failing node", but its *input set* is a
  selection the run makes for itself, and nothing in the gate requires the selection to cover the
  modules that guard the edited files. This is F-1's root cause stated at the template layer: the
  gate has no obligation to be exhaustive over the delta's blast radius, so "PASS" is a statement
  about a set, not about the tree.
- **Proposed fix**: state the input-set obligation in the gate row (the delta's guarded files must be
  covered), so a run cannot satisfy GATE-1 by choosing a small set.
- **Repair status**: recorded; `templates/commands/implement.md` is a framework source edit and is
  outside this feature's plan-owned scope for the review stage (REC-W1).

## 3.5 Answers owed to the code segment's items

The code segment raised two `important` items, one `question` and one `suggestion`
(`git-delta-review.sh report --summary --file code-review.md` → `important 2 / suggestion 1 /
question 1 / blocking 0 / gate=allow`). Each is answered below with a disposition, not merely an
acknowledgement.

### IMPORTANT #1 — `test_fast_fail_discipline.py:715, the a7 count pin` — **DISAGREE with the premise, AGREE with the outcome; repaired**

The item offered two readings ("the stale pin was hit live and repaired in passing but undisclosed"
or "T024 discharged by unconditional rewrite") and asked for either the part-4 transcript or the
re-taken live reconcile evidence. **Both readings are wrong, and the measurement says so:**

| measurement | command | result |
|-------------|---------|--------|
| pin at the reviewed base | `git show 2f6b8bbb:tests/contract/test_fast_fail_discipline.py` lines 724-725 | `expected 31` / `expected 32` |
| artifact at the reviewed base | `git show 2f6b8bbb:templates/instructions-template.md \| grep -c '^## '`; same for `.specify/instructions.md` | `31` / `32` |
| therefore a7 at base | pin == artifact | **GREEN** |
| a7 in the baseline failed-name list | `grep -c test_a7 baseline-failed.txt` | `0` |
| baseline full-suite log | `notes/baseline-full-suite-20261105.log` — 26 failed, and `test_fast_fail_discipline.py` appears once, as `test_g9_total_equals_frozen_baseline` | a7 absent |
| where the 30/31 → 31/32 pin change came from | `git log -S'assert tpl == 31' -- tests/contract/test_fast_fail_discipline.py` → `4e23dad2` ("fix(078): closure-repair") | **Feature 078**, before this feature's base |

The reviewer's claim that `a7 was RED at the reviewed base` and that "at `878c03ab` the test reads
`template has 31 ... expected 30 (FAILED)`" is **correct about `878c03ab` and false about the base**:
`878c03ab` is 078's *review* commit, and 078's own closure-repair `4e23dad2` raised the pin to 31/32
afterwards. Feature 082's base `2f6b8bbb` is downstream of that repair. There is no undisclosed
in-passing repair and no unconditional-rewrite story to tell; T024's reconcile is the ordinary
`generate-instructions.sh` incremental injection already evidenced in
`test-evidence/implement-part-5.md`.

**But the item's underlying observation is right, and it is a live failure the reviewer did not
name.** This delta moved the counts 31/32 → 32/33 and left the pin at 31/32, so at the reviewed head
a7 is **red**:

```
$ python3 -m pytest tests/contract/test_fast_fail_discipline.py -q
E       AssertionError: C-7: template has 32 top-level sections; expected 31
2 failed, 102 passed in 1.75s
```

Disposition: **repaired**. The pin is raised to `TPL_EXPECTED = 32` / `LIVE_EXPECTED = 33`, the two
now carry a named-constant form with a delta-reporting message, and an offset assertion
(`live - tpl == LIVE_EXPECTED - TPL_EXPECTED`) was added so the two pins cannot drift apart in
silence — which is precisely how the previous staleness survived. The repair carries its own
mutation check: deleting one `##` line from the real template turns it red (`assert 31 == 32`), and
the template was then restored and verified byte-identical (`sha256 44ea5381d660…`, equal to
`git show HEAD:`). The feature's own guards are green after the repair:
`55 passed` across the four guard classes plus the budget carrier, and the recorded smoke command
re-runs at `42 passed, EXIT=0`.

### IMPORTANT #2 — `notes/red-first-evidence.md:534, the M-1..M-6 id re-use` — **AGREE; repaired in part, escalated in part**

Agreed on both counts, verified before acting:

- the part-8 section applied `M-1..M-5` to legs whose subjects are the glossary store and the mirror
  enum (`red-first-evidence.md`, part-8 transcript), while the four contracts already spend
  `M-1`/`M-2` (`constitution-double-landing.contract.md:103-104`), `M-3`/`M-4`
  (`instructions-propagation.contract.md:87-88`) and `M-5`/`M-6` (`mirror-distribution.contract.md:93-94`)
  on different mutations;
- the R-3/R-6 rows read `M-1 / M-2 (part 8)` and `M-4 / M-5 (part 8)`, which a reader traces into the
  wrong contract row.

Disposition: **repaired** for the non-plan-owned half. The part-8 legs are re-coined `G-1..G-5`
across every part-8 table and the T051 consolidation table, and the section now opens with an
ownership table that maps each `G-N` to the contract clause it proves and to the contract leg it must
not be confused with. The runner's own verbatim transcript keeps the old `M-N` tokens on purpose:
`.specify/.tmp/082-part8/red_legs.py` is git-ignored scratch, and re-running it to relabel cosmetic
output would replace captured evidence with a re-execution (single-run evidence discipline). The
mapping table is the bridge, and `test-evidence/implement-part-8.md`'s `evidence_ptr` now says so.

The C-21 half is **escalated, not edited**: naming C-21's red in
`contracts/instructions-propagation.contract.md`'s mutation table is a **plan-owned** edit, so this
run recorded the attribution instead (`red-first-evidence.md` § "C-21 red — which run produced it,
and why no contract mutation table names it": the red came from the **part-4 build run** on the real
template, the clause it belongs to is **C-14**, and `C-21` is the carrier's test-name token
(`test_c21_instructions_summary_is_at_most_two_sentences`,
`tests/contract/test_self_explanatory_constitution.py:494`), not a clause id — the instructions
contract's clause list stops at C-19, and the only `C-21` heading in the contracts is
`mirror-distribution.contract.md:20`, "Summary bound", a different clause in a different file). The
same trap holds for `C-27`, which is `test_c27_docs_page_*` in
`tests/contract/test_self_explanatory_distribution.py:486-542`, not a contract clause. The contract
table itself is F-3 above, left for the plan owner.

### QUESTION — `features.md:90, delta hygiene` — **ANSWERED; no repair needed**

Agreed with the reading, including the qualification. The facts as measured: the 082 status flip
landed inside `1f6ab51c` ("close implement", seven files: the `features.md` row status, the feature
detail's status line and `## Latest Review` entry, `tasks.md`'s DoD marker, the part-10b evidence, a
feedback entry and a run record), while the spine write that records that part's closure landed one
commit later in `b2880fa0` (9 inserted lines in `.specify/state/082-self-explanatory-integration.md`,
one file). So the table alone cannot answer "which commit flipped the status", and the spine's part-8
checkpoint (`5085f46f`) sits after part 9's code carrier (`32fc3e70`), so commit order does not
reconstruct part attribution.

What keeps this a recorded degradation rather than a lost history is exactly what the item points
at: **every `test-evidence/implement-part-*.md` file declares its `stage_base`** (verified for all
eleven files, including `implement-part2-stage-checks.md`), so the per-part timeline is recoverable
from the artifacts even where the commit order is not. That is the fallback
`review-sdd-process` § 2 prescribes for ungrouped commits, and this review used it. The finding-side
residue is F-4 (a checkpoint commit with an empty diff). No code or artifact repair is warranted: the
question is answered, the underlying discipline gap is F-4's recommendation (REC-W2).

### SUGGESTION — `test_fast_fail_discipline.py:1146, the three hard-coded counts` — **AGREE; repaired**

Agreed, and the item's reasoning matches this feature's own assumption A4. Disposition: **repaired**.
The three expected values are now derived from the artifacts they describe —
`len(PRINCIPLE_RE.findall(template))`, the same over the live constitution, and the mandate-entry
count the test already extracted — with a non-zero anti-vacuity assertion so a derivation that
returned `0` cannot make the comparison vacuously true. Verified three ways: derived values equal the
double-landing guard's own pins (`18 / 19 / 11`); the test is green (`1 passed`); and the repair was
mutation-checked by lowering `TEMPLATE_COUNT` to 17, which turns `test_x13` red with the message
naming the artifact count — then the file was restored from git and re-verified.

## 4. What Worked — Preserve (Brief)

- The `final_path` / acceptance-honesty vocabulary held: `SC-006` was left an honest `partial` with a
  five-field ladder instead of being rounded up, and the closure checker still returned `accept`
  because a `supporting` row cannot refuse a verdict. That is the closed set doing its job.
- Per-part E3 evidence with a declared `stage_base` in every file recovered the timeline exactly where
  commit order failed (§ 3.5 QUESTION).
- The code skill's `receipt` / `report` pair made the coverage gap mechanically visible: one command
  wrote the missing block and one command produced the gate verdict, with no prose counts in between.
- The feature's own guards (`test_self_explanatory_*`, `test_instructions_section_propagation`,
  `test_instructions_size_budget`) stayed green through every repair in this run — `55 passed`.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-T1 — Make the review code subsection fail loudly on a missing receipt block.** Target:
  `templates/review-template.md` § 2.1 (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/review-template.md`).
  Change: the `changed / judged / skipped / gap` row already says a missing receipt block is an
  input error; add the one-line recovery (`git-delta-review.sh receipt --review-file <record> --spec
  <dir>`) beside it, so the reviewing run repairs rather than reports. Source: this run's § 2.1.
  Expected impact: removes a class of review runs that block on a mechanical omission.

### 5.2 Command Prompt Improvements

- **REC-C1 — Derive the Completion Gate's test set from the delta.** Target:
  `templates/commands/implement.md` § Completion Gate, GATE-1 (absolute:
  `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md`). Change: require the
  gate set to include, for every file the delta touched, the guard modules that assert on that file,
  and to print the derivation. Source: F-1, F-5. Expected impact: a delta can no longer pass GATE-1
  by selecting a set that excludes its own regressions.

### 5.3 Automation / Script Improvements

- **REC-A1 — Fail a checkpoint whose spine delta is empty.** Target: the checkpoint step used by the
  implement flow (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/scripts/`). Change: a
  checkpoint commit whose spine write is empty exits non-zero with a named message, and a closure
  commit is required to carry the spine write for the part it closes. Source: F-4.
  Expected impact: "a checkpoint was recorded" becomes checkable rather than assumed.

### 5.4 Workflow Improvements

- **REC-W1 — Require a guard-coverage obligation on the Completion Gate.** Target:
  `shared/workflow/acceptance-hardening.md` § Gates (absolute:
  `/storage/project/cloud-native-ai/spec-kit/shared/workflow/acceptance-hardening.md`). Change: state
  that a gate verdict is a statement about the set it measured, and that the set must cover the
  delta's guarded surfaces. Source: F-1, F-5. Expected impact: "PASS" stops being portable across
  differently-chosen sets.
- **REC-W2 — Give the state spine a per-part checkpoint contract that survives the last part.**
  Target: `shared/workflow/feature-integration.md` (absolute:
  `/storage/project/cloud-native-ai/spec-kit/shared/workflow/feature-integration.md`). Change: state
  that a closure commit must carry a non-empty spine write, and that an evidence file's `stage_base`
  is the sanctioned fallback when commit order cannot reconstruct attribution. Source: F-4.
  Expected impact: the per-part timeline is legible from either source, never from neither.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Derive the Completion Gate's test set from the delta | `templates/commands/implement.md` § Completion Gate | F-1, F-5 |
| P1 | Guard-coverage obligation on the gate verdict | `shared/workflow/acceptance-hardening.md` § Gates | F-1, F-5 |
| P2 | Fail a checkpoint whose spine delta is empty | implement checkpoint step | F-4 |
| P2 | Per-part checkpoint contract for the spine | `shared/workflow/feature-integration.md` | F-4 |
| P2 | Receipt-block recovery hint in the report template | `templates/review-template.md` § 2.1 | this run § 2.1 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path as a parenthetical supplement.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.**

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
