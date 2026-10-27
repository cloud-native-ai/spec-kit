# Remediation round 1 — plan-side alignment worklist (071)

**Date**: 2026-10-27
**Trigger**: `.specify/specs/071-review-code-integration/test-evidence/analyze-report.md` — `GATE: CRITICAL=0 HIGH=6` (32 findings: HIGH 6 / MEDIUM 22 / LOW 4).
**Round**: 1 of max 1 (this is the only permitted upstream repair round).
**Scope of what this file is**: the plan-owned and tasks-owned alignments that the requirements-layer repair implies but MUST NOT be landed by the requirements stage. Every item below is *not yet applied*; none of `plan.md`, `research.md` (beyond two fact corrections), `data-model.md`, `contracts/`, `quickstart.md`, `feature-ref.md`, `tasks.md` was edited by this round.

**What this round did change**: `requirements.md` (all 32 findings landed at the requirement layer), `research.md` (two fact corrections only, A-30/A-31), the feature registry (A-28 + this round's own stage record), and the evidence files under `test-evidence/`.

---

## 1. The six driver adjudications, and the plan-side consequence of each

Each row is already encoded as the single mechanical reading in `requirements.md`; the third column is what the next stage must change so the design artifacts stop contradicting the requirement.

| ID | Requirement now says | Plan-side consequence (open work) |
|----|----------------------|-----------------------------------|
| A-01 | The closing summary is a human-facing console/handoff output, **not** a verifiable carrier. Verifiable carriers are exactly two: `review.md`'s code subsection (FR-011) and the feature detail's `## Latest Review` record entry (FR-012). | `contracts/command-orchestration.md` **C-14** still obliges "the closing summary … MUST both present"; `contracts/status-gate-ownership.md` **C-52** and **C-53** still route disclosure into the closing summary. Reword all three to the two carriers and state the summary is a presentation, not a third artifact. `templates/review-template.md` § 2.1 is the carrier of the first one. |
| A-02 | "What counts as a code path" is owned by the `code-review` skill's deterministic script, overridable by `--code-paths`; the requirement cites that owner and does not copy the list. | `contracts/command-orchestration.md` **C-7** currently enumerates the `not-applicable` basis without a path predicate; `data-model.md` **E4 `basis`** carries the same gap. Add the predicate delegation + the `--code-paths` override to C-7 and to E4, and record the closed default set **once**, in the script (see § 2.5). |
| A-03 | Review range is `base..head`; head = explicit `--head` > `HEAD` resolved once at run start (fixed for the run); the range MAY contain unrelated commits; strict slicing requires an explicit head; base source and both SHAs are recorded. | `contracts/code-review-skill.md` **C-18** names base tiers only — add the head rule; `data-model.md` **E5 `head_sha`** ("`HEAD` unless overridden") must carry "resolved once at run start"; **E5 `base_source`** must keep three tiers while a head source is either added or explicitly declared out of scope (choose one and say so). |
| A-04 | The uncommitted-scope disclosure lives in **both** the report's code subsection and the code segment record — two carriers by design, one fact. | `contracts/command-orchestration.md` **C-9** (closed list of the code subsection) must add the disclosure field; `contracts/coverage-receipt.md` **C-44** must stop reading as "record only"; `data-model.md` **E4 `worktree_uncommitted`** must name both carriers; `templates/review-template.md` § 2.1 gains the field. |
| A-05 | The gate is an **existence** predicate over the current record only (`STR-004`): ≥1 `blocking` entry blocks; a later run whose record carries zero `blocking` no longer blocks. No "clearing" action and no "cleared" state exists. | `contracts/status-gate-ownership.md` **C-46** ("no unresolved `blocking` item"), `contracts/coverage-receipt.md` **C-37**/**C-38** (`blocked` derived from "unresolved"), `data-model.md` **E9** column and **V6** (`unresolved_blocking`) all carry the retired vocabulary. Restate as "the current record contains no `blocking` heading / the `blocking` count of the current record is 0", drop "unresolved"/"cleared" everywhere, and keep the instrument's existing presence-based count (`skills/internal/code-review/scripts/git-delta-review.sh`, the `^### .* \[blocking\]` count) as the implementation. |
| A-06 | Exactly one existing assertion change is authorized: `tests/contract/test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition`, rewritten to assert the owner path + the disappearance of the duplicated wording, with a net assertion gain; the rationale must be declared in the feature detail's review-record entry. No other assertion may be deleted or weakened, and the authorization is not precedent. | `contracts/feedback-and-boundaries.md` **C-64** and `contracts/tests-and-docs-sync.md` **C-67** already describe the change but as an unqualified permission; add "this is the one authorized exception, non-precedential" and the declaration duty. `tasks.md` **T030** and **DoD-4** must cite FR-027's exception instead of an absolute prohibition. |

---

## 2. Per-artifact worklist

### 2.1 `contracts/command-orchestration.md`

- **C-6**: replace the bare literal `run` with `[[STR-005]]` (new Shared String) and cite the triage set by id.
- **C-7**: add the code-path-predicate delegation from § 1 A-02, plus the empty-delta rule (zero changed files ⇒ `not-applicable` **before** the receipt runs).
- **C-9**: add the uncommitted-scope disclosure and the base source to the closed list (base source is already there — keep), and add "counts are copied from the receipt block, never recomputed".
- **C-10**: unchanged in substance; keep "no opinion bodies, no per-item counts".
- **C-12**: replace the archive timestamp form with `YYYYMMDDTHHMMSSZ` (UTC, second resolution), add the same-second disposition (wait one second, or exit `2` with the reason), and add the first-run archive value `[[STR-009]]`.
- **C-14**: see § 1 A-01.

### 2.2 `contracts/code-review-skill.md`

- **C-17**: the non-interactive enumeration must be the four steps (base resolution, record creation **and rotation**, opinion capture, receipt + verdict), matching FR-021.
- **C-18**: add the head rule (§ 1 A-03) and the trunk identification order (explicit `--trunk` > resolvable `refs/remotes/origin/HEAD` > existing `main` > existing `master` > `not-evaluated`; no other heuristic).
- **C-21**: the record header must carry the base **source** and the head SHA fixed at run start; keep one header form.
- **C-22**: mode selection is two-conditioned — renderer available **and** stdout is a TTY ⇒ rendered mode with the literal `renderer: delta` (`[[STR-008]]`); otherwise text mode `[[STR-003]]`. Agents / non-interactive calls take text mode even when the renderer exists.
- **C-23**: replace the free-text prohibition with the closed forbidden-phrase list now owned by SC-003 (four literals), and say the test searches those four verbatim.
- **C-30**: add the code-path predicate + `--code-paths` override to the list of capabilities that must land on the existing script entity.

### 2.3 `contracts/coverage-receipt.md`

- **C-31**…**C-35**: unchanged carriers; **C-34**/**C-35** must be restated as the closed exit alphabet: `0` = complete, `1` = coverage gap (missing verdict, set mismatch, **or an unrecognised skip reason**), `2` = cannot evaluate. Do not leave "non-zero" as one meaning.
- **C-36**: add the closed skip-reason set (five values, § 2.5) and state that an unrecognised reason is a gap, not a legal skip.
- **C-37**: `blocked` ⇔ the current record contains `blocking` entries (existence), not "unresolved" ones.
- **C-38**: the verdict conjunction is scoped to `triage = run` with a non-empty changed set; an empty delta never reaches the receipt.
- **C-39**: replace bare `pass`/`blocked` literals with `[[STR-006]]`/`[[STR-007]]`.
- **C-43**: the shortfall must be surfaced in the report's code subsection and the feature detail's record entry (the closing summary is no longer a carrier — § 1 A-01).
- **C-44**: see § 1 A-04.

### 2.4 `contracts/status-gate-ownership.md`

- **C-46**: existence predicate (§ 1 A-05).
- **C-48**: the `/speckit.checklist` row is a **conditional** initiator — it initiates the transition only when it runs after `implement`, cites the same owner criterion then, and does nothing when it runs before `implement`.
- **C-51**: the unattended disposition is halt-and-report with the named refusal literal `blocking-unresolved` (`[[STR-010]]`); a driver/orchestrator confirmation is not an explicit user ruling — only a user-authored waiver artifact or the user's own ruling is.
- **C-52**/**C-53**: carriers are the report's code subsection + the feature detail's record entry; refusal reasons name the failing condition.

### 2.5 `contracts/feedback-and-boundaries.md`

- **C-58**/**C-59**: the per-run unit census is three, not two — `/speckit.review`, `skill:review-sdd-process`, `skill:code-review`; each records itself; the command neither suppresses nor back-fills.
- **C-62**/**C-63**: keep; **C-63** gains the FR-014/FR-027 reading that "coverage" in the receipt means reviewed-files share, never test/compile coverage.
- **C-64**: see § 1 A-06.

### 2.6 `contracts/tests-and-docs-sync.md`

- **C-66**: add the red-first duty as a requirement-level obligation (`requirements.md` FR-028 now carries it): six groups, each with a recorded failing run (command, exit code, failing count).
- **C-67**: see § 1 A-06.
- **C-70**: the mirror criterion stays "no NEW drift against a pre-edit measurement"; the per-pair table stays here in `plan.md` § Mirror Obligations (FR-028 now points at it instead of restating it).
- **C-71**: unchanged (surface comparison, not prose).

### 2.7 `data-model.md`

- **E4** — `value` closed set: cite `[[STR-005]]`; `basis` gains the code-path predicate reference; add "record exists only when `value = run`" (FR-010's existence split) and remove any reading that a `not-evaluated` run writes a record.
- **E5** — `head_sha`: "resolved once at run start; overridable by `--head`"; add `head_source` **or** an explicit statement that head carries no source tier; `base_source` keeps its three tiers; add the trunk identification order to **V9** and the empty-delta rule.
- **E6** — header gains the head SHA at run start; **V12** gains the `YYYYMMDDTHHMMSSZ` form and the same-second rule.
- **E7** — declare the block the single source of the four counts (FR-011's three disclosures copy it) and add the equality assertion to the test obligations; keep the name set closed.
- **E8** — `reason` becomes the closed five-value set, not free text.
- **E9** — the verdict column cites `[[STR-006]]`/`[[STR-007]]`; the blocking column becomes "the current record contains `blocking` entries (presence)".
- **E10** — exit codes: `0`/`1`/`2` with the three meanings, no fourth.
- **E11** — archive filename uses `YYYYMMDDTHHMMSSZ`; first-run value `[[STR-009]]`.
- **E12** — three `unit_id` values, not two.
- **E13** — counts' source is the block; the three consumers copy it (the closing-summary row goes away).
- **V6**, **V12**, **V20**, **V22**, **V24** — align with the above (V6/V20 verdict scoping and existence semantics; V12/V24 timestamp and first-run value; V22 unattended disposition and the `blocking-unresolved` literal).

### 2.8 `plan.md`, `quickstart.md`, `feature-ref.md`, `tasks.md`

- **`plan.md`** — § Mirror Obligations stays the owner of the per-pair table (FR-028 references it); § Risks **R-03** must describe the pin change as the *authorized* exception, not an unqualified permission; record this round's remediation in the plan's change log when the plan is next edited.
- **`quickstart.md`** — the scenarios that print the closing summary must be restated as "report subsection + feature detail entry"; the not-applicable scenario must state that no `code-review.md` is created; the renderer scenario must gain the no-TTY case (agents take text mode even with `delta` present).
- **`feature-ref.md`** — the disclosed pin change row must cite FR-027's exception; the delivery surface is unchanged.
- **`tasks.md`** — **T030**/**DoD-4** must cite FR-027's exception; rows touching the receipt must add the skip-reason rejection case and the exit-code `2` case; rows touching the mode marker must add the no-TTY case; **T002**'s E2 baseline slot is the anchor SC-006 now names (no change to the row, only to its citation); **T021** must state the checklist row is conditional (A-18).

### 2.9 Literal content the next stage must place (decided here, owned elsewhere)

The requirement layer deliberately does **not** copy these sets (one source of truth); the content is recorded here so the next stage does not re-decide it:

- **Closed default code-path set** (to live in the skill's deterministic script, contract C-7 pointing at it): `src/**`, `scripts/**`, `skills/**`, `templates/**`, `agents/**`, `tests/**`, plus executable configuration files — `pyproject.toml`, `*.py`, `*.sh`, `*.js`, `*.mjs`, `*.ts`. `docs/**`, `.specify/specs/**` and `.specify/memory/**` are **not** code paths. `--code-paths` overrides the set; triage is `run` iff the committed delta contains at least one code path.
- **Closed skip-reason set** (owned by `requirements.md` FR-014, mirrored into contract C-36 and data-model E8): `non-code-file`, `generated`, `binary`, `out-of-scope-per-explicit-user-ruling`, `size-guard-focus-not-reviewed`.
- **Closed forbidden-phrase list** (owned by `requirements.md` SC-003, mirrored into contract C-23): `已完成可视化评审`, `rendered review complete`, `visual review performed`, `side-by-side review done`.

---

## 3. What must not be done next stage

- Do not re-open the driver adjudications in § 1: they are encoded as the only mechanical reading in `requirements.md`, and this round is the only permitted repair round.
- Do not add a fifth Shared String for the skip-reason or forbidden-phrase sets — both are multi-value sets owned by one requirement row (FR-014, SC-003); a Shared String row is for a single verbatim literal.
- Do not delete `test_review_p1_review_loop.py::test_c15_...`; it is rewritten, not retired (FR-027).
- Do not hand-edit any `.specify/` runtime projection — the generators produce them (`sync-mirrors.py`, `regen-command-copies.py`).

---

## 4. Evidence for this round

- `test-evidence/requirements-remediation-validate.txt` — `validate-requirements.py` (exit 0).
- `test-evidence/requirements-remediation-pre-analyze.json` — `pre-analyze-check.py --stage requirements` (decision=pass, errors=0).
- `test-evidence/requirements-remediation-decomposition.json` — `decomposition-check.py --mode plan` (decision=proceed).
- `test-evidence/requirements-remediation.jsonl` — the docs-only E3 stage-status row (six reduced fields; no test run, no baseline consumed, no closure slot).
