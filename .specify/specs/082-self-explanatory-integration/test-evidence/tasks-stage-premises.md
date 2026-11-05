# Tasks-stage premise re-measurement — 082-self-explanatory-integration

**Captured**: 2026-11-05 (tasks stage) | **stage_base**: `dc83514e` | **Working dir**: repository root

Every figure pinned in a `tasks.md` scenario table below was measured at generation time in this
run. The premise-verification rule (`.specify/skills/internal/create-tasks/SKILL.md` § Premise
verification) makes a printed re-derivation command a hypothesis until it is executed; the commands
below were executed, and their output is what the table carries.

## E-1 — Baseline re-measure (executed)

```console
$ python3 --version
Python 3.11.11
$ git --version
git version 2.43.5
$ python3 -m pytest --version
pytest 8.4.2
$ python3 scripts/python/scan-confirmation-gates.py --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["total"])'
27
$ python3 scripts/python/sync-mirrors.py --check; echo "mirror exit=$?"
... (six `ok` lines: templates 22, skills/external 409, skills/internal 138, agents 3, scripts 119, shared 65)
mirror exit=0
$ grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md .specify/memory/constitution.md
templates/constitution-template.md:17
.specify/memory/constitution.md:18
$ wc -c .specify/instructions.md
32739 .specify/instructions.md
$ grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh
38:INSTRUCTIONS_BUDGET_BYTES=32768
```

## E-2 — Spec-owned premises (executed)

```console
$ grep -cE '^## ' templates/instructions-template.md
31
$ grep -cE '^## ' .specify/instructions.md
32
$ python3 -c "import re,pathlib; t=pathlib.Path('shared/definitions/self-explanatory-definitions.md').read_text(); print(len(re.findall(r'(?m)^## .+$', t)))"
7
$ grep -c '不言自明\|望文生义' .specify/memory/glossary.md
0
$ grep -cE '^## ' docs/concepts/self-explanatory.md
0
$ ls .specify/shared/definitions/self-explanatory-definitions.md .specify/shared/guidelines/self-explanatory.md .specify/shared/workflow/best-practice-optimization.md
(three paths listed — already present, untracked at stage base; see plan § Mirror Obligations fact 1)
```

**Trap forms recorded deliberately** (the premise-verification rule asks for the naive variant next
to the deliberate one):

- Section counts are heading lines (`grep -cE '^## '`): template **31**, live **32**. Their
  difference is *not* a missing section — the live file carries one extra section
  (`## Recurring Operational Lessons`) that the template does not, and the live file carries every
  template heading. The naive reading ("live has more headings, so the template is behind") is the
  wrong inference; the propagation gate compares the template's heading set against the live file's
  heading set, not the two totals.
- The first attempt at this measurement was transcribed wrong (33/34 instead of 31/32) and was
  re-run before this row was written. The figures here are the second, executed reading; the
  transcript defect is disclosed rather than silently corrected.
- The mirror pair `shared → .specify/shared` is **lenient**: it reports a mirror-only file as `ok`
  with a note and does not fail the strict-pair orphan rule. Counting `ls .specify/shared/...` as
  proof of distribution is the wrong measurement; the distribution claim is measured by `specify
  init` in a fresh directory (scenario S-4 of `tasks.md`), and a file present only in the mirror
  never ships (plan EP-002).
- The gate-scanner total `27` is **not** the frozen baseline; the frozen value (Feature 050's
  `baseline-gates.json`) is `23` and one pre-existing test pins the equality. A scenario that reads
  "total: 27" as "no new gates" is the naive reading — the measured claim this feature makes is
  **zero new hits in the new blocks**, which is what scenario S-1 asserts.

## E-3 — Pre-existing red carried forward (not repaired here)

```console
$ python3 -m pytest tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged -q -p no:cacheprovider
(red at stage base; the pin is an equality assertion against the frozen 23, live scan reads 27)
```

`Decision: fallback` per `plan.md` § Execution Premises EP-003: this feature MUST NOT repair the pin
(it belongs to Feature 050's frozen baseline) and MUST name this node in every stage's targeted-run
evidence rather than report "clean".

## E-4 — Test budget (this stage)

`status=not-run-docs-only` — the tasks stage produces one Markdown artifact plus this evidence file;
no test selection is owed. The `E-3 stage-status` row lives in `plan-stage-checks.md` (plan) and is
restated by the implement stage's own evidence row; this file records the premise re-measurement the
generation owed.

---

# P-5 — C-19 Documentation Map decision (appended by implement part 5, T028, 2026-11-05)

**Obligation**: `contracts/instructions-propagation.contract.md` § C-19. The clause has an "if"
branch (the map gains or should gain a row → the row MUST point at `STR-004`, the runtime path) and an
"else" branch (no row → satisfied by **the recorded decision not to add one**). T028's `[green:]`
claim is satisfied on the else branch, and this section is the record.

**Decision: `templates/instructions-template.md` § Documentation Map gains NO row for the owner
document. The owner is reachable through the section's pointer.**

## The measurement the decision rests on

```console
$ rows in the Documentation Map: 10
$ grep -n 'self-explanatory-definitions.md' templates/instructions-template.md
81:Full discipline — definitions, practice steps and the ceiling/floor rule — lives in `.specify/shared/definitions/self-explanatory-definitions.md` (do NOT copy its rules; reference the file).
```

- The owner appears **exactly once** in the template, in the `## Self-Explanatory Structure (不言自明)`
  body — which is the `STR-004` runtime path, so the pointer requirement is met there.
- The map section ends ~4 lines above that section; both live in the ambient chain every `/speckit.*`
  command loads, so "reachable through the section's pointer" is a literal reachability claim, not a
  hope.
- Three owner documents exist for this concept (`shared/definitions/self-explanatory-definitions.md`,
  `shared/guidelines/self-explanatory.md`, `shared/workflow/best-practice-optimization.md`) but they
  are **one concept's** definition/practice/workflow trio, not three independent topics. A row-per-document
  reading would add three rows for one concept; a one-row reading would have to choose which document
  the "Location" cell names, and C-19 admits only the definition document's runtime path. Both readings
  buy the reader nothing the pointer line does not already give.

## Why the map's four precedents do not require a row here

Four existing rows cite an ambient discipline owner in the same `shared/` tree —
`**Confirmation Gates**`, `**Objective Analysis**`, `**Critique and Self-Critique**`, `**TODO-in-Context**`.
The distinguishing property is the **trigger**, not the tree:

- those four govern an action that fires on **every** turn or **every** command (confirm before acting;
  detect same-author; critique before proposing; perceive markers at a code location);
- this owner's own trigger (`shared/guidelines/self-explanatory.md` § 1 何时应用) is **conditional**: the
  user points at a name/path/structure, or a request uses 优化 / 改进 / 不满足要求 wording and the flow
  surfaces the practice as a *candidate*.

A map row is a standing instruction to consult a document. Adding one for a conditionally-triggered
practice would tell every reader to consult it unconditionally — and would cost every client project's
instruction chain a row, against a budget this feature had to raise once already.

## Two layers answer the completeness question differently — both recorded

- `checklists/requirements-quality-20261105.md` item **CHK001** asks whether `requirements.md` states
  the row decision. It does **not**, so on the requirements-text layer the row obligation is
  **unspecified**. Per that checklist's own E-6 note, that is a requirement-text gap whose repair
  belongs to a future requirements revision — and `requirements.md` is out of this feature's edit scope
  (PLAN-EDIT none). It is disclosed here rather than silently treated as answered.
- On the artifact layer the question is decidable and is decided: **no row**, `STR-004` satisfied by the
  section pointer. That is the layer C-19 governs, and the one this record closes.

The two layers are stated together on purpose: a reader who opens only `requirements.md` will not find
the rule, and a reader who opens only this record will not learn that the requirement text is silent.

## Consequence for the guards

No guard is added or changed by this decision: C-19's else branch is satisfied by a record, not by an
assertion, and a test asserting the *absence* of a map row would freeze a decision the contract leaves
open. The US2 carrier already asserts the pointer (`test_c10_template_carries_the_section_and_its_runtime_pointer`)
and the no-copy obligation (`test_c11_…`, C-20's parametrised twin); between them the reader-facing
guarantee C-19 protects is covered without a new pin.

