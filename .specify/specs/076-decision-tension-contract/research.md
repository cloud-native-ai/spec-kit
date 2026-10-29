# Research: 决策反题与反指标契约（Decision Tension Record）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**Spec**: [requirements.md](requirements.md)
**Phase**: 0 (research review)
**Measurements dated**: 2026-10-29, on branch `076-decision-tension-contract`, baseline commit `ac63fe8c`

Everything below is either a measured fact (command shown, output quoted) or an explicitly
labelled decision with its rejected alternative. Spec-anchored claims were re-measured rather
than inherited: the requirements file is a specification, not a record of current reality
(Constitution VIII).

---

## R-1 — Where the section can land, and what "position" can mean

**Measured.** `grep -n "^## " templates/plan-template.md` yields, in order:
`## Summary` → `## Technical Context` → `## Constitution Check` → `## Project Structure` →
`## Complexity Tracking` → `## Phase 1: Design Artifacts Summary`.

**Decision.** The anchor is `## Constitution Check` → `## Decision Tensions` →
`## Project Structure`, asserted as three adjacent `^## ` lines. The template gains the section;
this plan instance carries it too (first DTR instance, see R-10).

**Rejected alternative.** "After Constitution Check, before Complexity Tracking" — the spec's
own original wording. It has two satisfying positions (`## Project Structure` sits between
them), so it is not decidable; FR-008 already withdrew that reading.

**Consequence for this plan.** The plan instance must place `## Decision Tensions` between the
two headings even though the template does not yet contain it. That is a deliberate divergence
from "fill the template in place" and is disclosed in the plan's Phase 0 section and in the
return report; the template edit lands at implementation.

---

## R-2 — The analyze channel letter, and why not "H"

**Measured.** `skills/internal/analyze-artifacts/SKILL.md` § 5 says: "Seven passes (A duplication
· B ambiguity · C underspecification · D constitution alignment · E coverage gaps · F
inconsistency · G feature relevance & accuracy) plus one checklist pass (H)". So `H` is already
taken — by the checklist-accountability pass, which lives in `SKILL.md` and not in
`detection-and-severity.md`.

**Decision.** The new structural channel is `I. Decision tension records`, added to
`detection-and-severity.md` beside A–G. Two count lines move with it: the file's own
`## The seven passes` heading becomes `## The eight passes`, and the SKILL.md sentence above
becomes "Eight passes (A–G · I decision tensions) plus one checklist pass (H)".

**Rejected alternative.** Reusing `H` would collide with an existing pass and silently re-scope
it; renumbering the checklist pass would move a label that other text and readers already use.

**Consequence.** `skills/internal/analyze-artifacts/SKILL.md` is touched, which FR-025's mirror
row 5 already anticipates ("若 `SKILL.md` 亦需指针则同对"). The enumeration in SKILL.md remains
a pointer-shaped summary: the channel owner stays `detection-and-severity.md`, and a contract
test pins the two enumerations to agree (a legitimate duplicate under
`shared/guidelines/one-source-of-truth.md` — a literal pinned in a test to detect drift).

---

## R-3 — Validator output shape: what precedent actually says

**Measured.** `scripts/python/validate-requirements.py` declares `EXIT_OK = 0`,
`EXIT_ERROR = 1`, `EXIT_INPUT = 2`, prints a `status:` line plus one line per check, and its
docstring states that the two-space-indented `name  description` lines ARE the pinned label set.
`account-clause-coverage.py` already uses `--spec-dir <dir>` (a directory, not a file) because
its verdict spans two artifacts, and emits `[label] pass|fail (count) — detail` lines.

**Decision.** `validate-decision-tensions.py` takes `--spec <spec-dir>`, reads
`<spec-dir>/plan.md` + `<spec-dir>/requirements.md`, exits 0/1/2, prints `status` + one
`[label] pass|fail (count)` line per check in human mode and the FR-016 JSON object under
`--json`.

**Rejected alternative.** A positional file argument (`validate-requirements.py`'s shape) cannot
resolve measurement sources: the mapping target lives in `requirements.md`, a second artifact.
Reusing `validate-tasks.py` with a subcommand would fork both its exit-code semantics and its
output shape for a second artifact kind.

**Consequence.** The six labels are a closed set pinned in the docstring and re-extracted by the
contract test; the contract test asserts the docstring's `name  description` blocks equal the
emitted label set (the house pin pattern).

---

## R-4 — The `expected_sacrifice` grammar and its parser

**Measured.** `requirements.md` § Measurement Sources declares exactly one definition per
criterion in the form `- **SC-001 Source**: …`. Nothing else in the file starts a line with
`**SC-NNN Source**`.

**Decision.** The value is parsed as `<SC-NNN> Source <↓|↑>`; the record resolves when (a) the id
matches a `**SC-NNN Source**` entry, (b) at most one `SC-NNN` appears in the value, and (c) the
direction token is one of `↓` / `↑`. Anything after the direction is free text and is not parsed.

**Rejected alternative.** Bare `SC-NNN`. It shares one namespace with the Success Criterion and
cannot distinguish "the criterion" from "the measurement source that would degrade"; the literal
`Source` connector is the only key that already exists on the target line.

**Consequence.** A record whose sacrifice is real but has no declared source does not parse, and
FR-010's two remedies apply (add a source, or demote the decision to an ordinary trade-off).
That cost is carried as DTR `T-002` in this very plan.

---

## R-5 — What the quartet parser can and cannot decide

**Measured.** `shared/guidelines/critique-and-self-critique.md` today defines the attempt's
*content* ("点名一个具体、可执行的测量或检查") and a verdict, but no result field — so "ran it"
and "claims it ran" are indistinguishable on the artifact. `shared/workflow/self-improvement-workflow.md`
§ SI-3C already carries a pure pointer to that owner and no field list.

**Decision.** Four literal keys, each appearing exactly once (`attempt:`, `exit_code:`,
`observation:`, `would_go_red_if:`), value on the same line or in an indented continuation.
`exit_code` is an integer; `observation` must begin with the literal `raw:`; `would_go_red_if`
is split at the **first** occurrence of the literal `red:` (a later `red:` never moves the
split): at least one backtick span before that point names the broken input, and at least one
backtick span after it names the red signal (an assertion, a check label or a non-zero exit
code). The script never replays `attempt`.

**Rejected alternative.** Semantic judgement by the receiving agent. The same payload would
produce different verdicts across models or runs, which is exactly the failure FR-021 closes;
and the spec's Q5 already recorded the price of the shape route (a forged `raw:` prefix passes).

**Consequence.** Two stated costs, both measured by declared criteria rather than by prose: a
disguised paraphrase passes (bound to `SC-004 Source`), and the grammar can only accept
`would_go_red_if` in the shape it recognises.

---

## R-6 — Mirror pairs, tool copies, and the drift baseline

**Measured (before any edit).** `python3 scripts/python/sync-mirrors.py --check` → exit 0,
`OK: all per-tool command copies match the source templates`, and six pairs `ok` (templates 22 /
skills/external 406 / skills/internal 136 / agents 3 / scripts 115 / shared 59 files).
`python3 scripts/python/regen-command-copies.py --check` → exit 0.

**Decision.** The criterion is "no NEW drift on the rows of FR-025's table (the row count is
owned by that table and is not restated here), relative to this baseline", never "the command
exits 0" — a bare exit code is passable or unpassable by things this spec does not touch.
`templates/commands/**` is not touched, so the per-tool copy set is empty; the row-5 SKILL.md
edit is inside an already-listed mirror pair.

**Rejected alternative.** Freezing an "all green" criterion: it would make the check fail for
pre-existing drift on unrelated pairs and would tell a reader nothing about this spec's surface.

---

## R-7 — Containment claims for the two closed-set files

**Measured.** `git diff --stat ac63fe8c -- shared/guidelines/critique-and-self-critique.md
skills/internal/analyze-artifacts/references/detection-and-severity.md templates/plan-template.md
docs/decisions/template.md shared/workflow/self-improvement-workflow.md` → empty. The baseline
commit is the requirements-registration commit, and none of the five target files has moved
since it, so "byte-identical outside the allowed delta" is a claim about two comparable states.

**Decision.** Both files are handled as **only-add**: the quartet and the new channel arrive as
new paragraphs/sections; existing paragraphs keep their bytes. The two count lines that must
change (`## The seven passes` → `## The eight passes`; the SKILL.md pass enumeration) are inside
the declared allowed delta, named explicitly in the contract. Item-level counts (rejection forms,
boundary declarations, consumer-list rows) must not shrink, and the contract test compares
baseline vs current counts.

**Rejected alternative.** Rewriting the existing "输出形态" paragraph into a quartet paragraph.
It would be the cleaner prose, but it deletes lines the containment claim declares untouchable,
and FR-026's judgement is byte-level. The new subsection therefore *refines* the old one by
declaring the quartet to be the produced form while leaving the old paragraph untouched — the
refinement is normative, the bytes are not.

**Consequence visible to a reader.** `critique-and-self-critique.md` will read as "attempt =
a named, executable check" followed by "the produced form is this quartet". That ordering is
deliberate and is stated in the new subsection's first sentence so it does not read as an
accident.

---

## R-8 — Terminology surface and how zero is measured

**Measured.** The five internal aliases named in requirements § Assumptions A3 do not appear in
`shared/`, `templates/`, `skills/` today (the caller's premise was re-checked: the only current
occurrences are in this spec directory and in the Feature detail's appendix, neither of which is
a distribution surface).

**Decision.** A contract test greps the three trees for the five literals and asserts 0 hits,
and asserts this spec's own `## Assumptions` section still lists them (a positive control, so a
renaming of the alias list cannot make the test vacuously green).

**Rejected alternative.** Counting only in "user-visible" files by an allow-list of extensions —
the surfaces are Markdown by construction and the closed surface is the three trees themselves.

---

## R-9 — Test layout and the red-first order

**Measured.** `tests/contract/` holds 245 entries including `__init__.py`, all pytest; targeted
surfaces run green today: `test_closed_set_claims.py`, `test_self_improvement_conformance.py`,
`test_validation_carrier_contract.py`, `test_user_facing_comprehension_doc.py`,
`test_validate_tasks_parallel_safety.py` → 70 passed (interpreter: a stdlib+pytest environment
supplied via `SPECKIT_PYTHON`; the repo's `.venv` currently has no pytest — an environment fact,
not a spec fact).

**Decision.** Three new contract-test files, written before the implementation they judge:
`test_decision_tension_contract.py` (owner doc, template anchor, analyze channel, ADR slot,
mirror parity, terminology, containment), `test_decision_tension_validator.py` (six labels,
exit codes, one compliant plan plus the six inverse-input classes expanded to twelve runs —
the six field deletions plus `expected_sacrifice: none`, undecidable wording, a duplicate
`tension_id`, a skipped `tension_id` and an unmapped source), `test_falsification_quartet_validator.py`
(one accept plus the six rejection reason codes at 6/6, with four additional `missing-field`
samples — eleven runs in the reason-code matrix — covering exit codes 0/1/2; a separate
double-`red:` fixture pins the first-occurrence split and stays outside that matrix count).
Negative samples live in the tests, never only in prose (FR-017).

**Rejected alternative.** One monolithic file: the two validators are separate programs with
separate exit-code semantics, and a single file would make a red run ambiguous about which
contract broke.

---

## R-10 — This plan as the first DTR instance

**Decision.** `plan.md` carries `## Decision Tensions` with two records (`T-001`, `T-002`)
written by hand, using the exact grammar the future validator will parse (`### T-NNN` sub-heading,
six bold field labels, closed `expected_sacrifice` form). They are the pilot and the first
fixture; the same two cases are re-used as validator fixtures at implementation.

**Rejected alternative.** Publishing the grammar without an instance. Then the first real
parser run would happen at implementation time on a hand-written example produced by the same
author who wrote the parser — the same-author blind spot the objective gate exists to name.

**Consequence.** The plan asserts a section its own template does not yet have. That asymmetry is
intentional and is reported as a deviation rather than hidden.

---

## R-11 — Scope boundaries re-measured, not inherited

**Measured.** `/speckit.*` commands exist as `templates/commands/*.md` plus per-tool copies under
`.qoder/commands/`, `.claude/commands/`, `.github/prompts/`, `.opencode/command/`. This spec adds
none, and `regen-command-copies.py --check` (R-6) confirms the copy set is consistent today.

**Decision.** The scope contract (FR-018) states the negative sets — no new command, storage,
ledger, scheduler, scorer, runtime or model call — and its judgement is a before/after set
difference, not a narrative.

**Rejected alternative.** Restating the command inventory in the plan. It is a generated, drifting
fact; the census is taken at verification time from the directories themselves.
