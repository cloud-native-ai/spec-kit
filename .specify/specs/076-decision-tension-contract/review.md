# Specification-Driven Development (SDD) Process Review Report: 076 决策反题与反指标契约（Decision Tension Record）— review #2

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command
> prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents.
>
> **This is review #2.** Review #1 (`7d3ebb58`, deny) raised 1 × P0 / 5 × P1 / 6 × P2 and refused the
> status transition. A repair round (`1298aef7`) claimed all six blocking/important items closed.
> This round re-executes both segments against that claim: it re-verifies every prior item on the
> tree, then reviews the repair's own connected surface as new code. §2.3 carries the prior round's
> findings and their disposition; §3 carries only this round's new findings.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 076 |
| Requirement Key | 076-decision-tension-contract |
| Requirement Name | 决策反题与反指标契约（Decision Tension Record） |
| Related Feature | 076 决策反题与反指标契约（Decision Tension Record） |
| Repository | spec-kit |
| Repository URL | `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (single remote `gitlab`) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the branch is unpushed, so this report cites absolute paths plus `git show <sha>:<path>` recovery instructions instead of URLs |
| Branch | `076-decision-tension-contract` |
| Commit SHA | `1298aef7ca7dac9f00f8c696356d68f665465d48` (short: `1298aef7`) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-29 |
| Reviewer (Agent) | Qoder review agent, unattended SDD loop (run `r20261029T172918Z-076a`, review attempt 2) |
| Environment | macOS (darwin/arm64), bash, Python 3.14.6 at `/Users/liuqiming.lqm/project/profiles/.venv/bin/python`; `git-delta` absent (`which delta` → rc=1), so both segments ran in text mode |
| spec-kit Source Snapshot | this repository itself (framework source hat) @ `1298aef7` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 286 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/requirements.md | 26 FR / 8 SC / 5 user stories / 4 shared strings; owns the N/A criterion's wording |
| plan.md | 275 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/plan.md | Design + the feature's own two pilot DTR records (`T-001`, `T-002`) |
| data-model.md | 181 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/data-model.md | E1–E8 entities, R1–R6 rules, six state transitions |
| contracts/ (8 files) | 34 clauses | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/contracts/ | 34 closed contract clauses; each file owns a numbered clause slice |
| tasks.md | 350 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/tasks.md | T001–T027, 27 `[X]`, zero `[~]`, zero `[ ]` |
| checklists/readiness-2026-10-29.md | 218 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/checklists/readiness-2026-10-29.md | 37 checks (27 pass / 10 fail) plus the repair's `## Closure` block |
| verification.md | 120 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/verification.md | 8 SC rows all `pass`, each bound to an archived file by sha256 |
| review.md (this file) | — | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/review.md | Process segment, review #2 |
| code-review.md | — | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/code-review.md | Code segment record, review #2 (archive: `code-review-20261029T125405Z.md`) |
| test-evidence/review2-probes.txt | — | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/test-evidence/review2-probes.txt | This round's 12 independent probes, verbatim |

## 1. Process Execution Timeline

| # | Step / Event | Evidence | Deviation from prescribed flow? |
|---|--------------|----------|---------------------------------|
| 1 | Feature registered on `master` @ `26731b67`, branch cut; spec number moved 075 → 076 because `075-sdd-loop-efficiency/` already exists | `ac63fe8c`; state spine § U1 | None (bookkeeping) |
| 2 | requirements → clarify → plan → tasks → checklist, each stage gated by the deterministic pre-analyze / decomposition checks | commits `da7256e1`…`cde66c0b`; state spine § 阶段记录 | None |
| 3 | analyze #1 returned 4 HIGH and blocked implement; three remediation rounds followed (`16a44ea0`, `8a5f7aea`, `d4479500`) | state spine; `test-evidence/*-fix{1,2,3}.txt` | Friction: analyze leaves no artifact (carried as F11) |
| 4 | implement P1–P4 (`c69dbb81`…`7d3ebb58`); Feature flipped `Planned → Implemented` | `84de4ddf`, `7d3ebb58` | None |
| 5 | **Review #1** (`633bf744`): process P0×1 + P1×5 + P2×6; code `blocking`×1 + `important`×5; gate `deny`, status held at `Implemented` with `blocking-unresolved` | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/code-review-20261029T125405Z.md` (the round-1 record, now archived) | None |
| 6 | **Repair round** (`1298aef7`): owner grammar, per-trigger `N/A`, six-label table, program-side severity, checklist Closure block, consumer-resolved pointer, quartet key prefixes, `link_verdict()` | `git show --stat 1298aef7` (25 files, +902/−169) | Friction: the repair also rewrote `review.md`/`code-review.md` to append an author turn — allowed by the record's own disposition section, but it means two voices live in one dated record |
| 7 | **Review #2** (this run): both segments re-executed; 76 feature contract tests re-run green; 12 independent probes written; mirrors and command copies re-checked | `test-evidence/review2-probes.txt`; `sync-mirrors.py --check` rc=0; `regen-command-copies.py --check` rc=0 | None |

Working tree at run start: one modified path, `.specify/state/076-decision-tension-contract.md` (the
driver's stage bookkeeping). It is not feature code and is excluded from both judged sets.

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 1 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 1 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 0 |
| Documentation | 1 |

**P0 validation status**: No P0 findings raised; the P0 independent-validation pass is vacuously
satisfied. (Review #1's single P0 — F1 — was re-verified in this round as **closed**, by an
executable probe rather than by re-reading prose; see §2.3.)

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `ac63fe8c474357b4230b1f8a7ac2408f6cc12b2d` | the resolved diff base |
| Head commit | `1298aef7ca7dac9f00f8c696356d68f665465d48` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base/triage` |
| Renderer mode | `renderer: text` | `git-delta` is absent on this host; fallback path used, no installer run |
| Changed / judged / skipped / gap files | 138 / 11 / 127 / 0 | copied field by field from the coverage receipt block |
| Segment verdict | `not-evaluated` | the record's receipt block (127 skipped files earn no coverage credit) |
| Gate verdict | `allow` | `report --summary --file code-review.md` → exit 0, `blocking_entries=0` |
| Reason, when one applies | `not-evaluated` basis: 21 `.specify/` mirror and bookkeeping paths are `generated` (byte equality proven by `sync-mirrors.py --check`, six pairs ok), 106 feature process artifacts and evidence `.txt` are `non-code-file` — their judgement object is the process segment, not this one | receipt block + this run's skip selectors |
| Uncommitted scope | one path, `.specify/state/076-decision-tension-contract.md` (driver bookkeeping); disclosed, never concluded over | `uncommitted_scope=1` and the same sentence in the record |
| Record | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/code-review.md` | written (`triage=run`) |
| Archive | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/076-decision-tension-contract/code-review-20261029T125405Z.md` | round-1 record, rotated by `start` |

This subsection carries the verdict and the pointers only: no opinion body, no per-severity item
count. The findings themselves live in the record named above and are read there.

### 2.2 Status Gate — `Implemented → Ready for Review` (judged once, after both segments)

| # | Condition (owner: `templates/feature-details-template.md` § Canonical Status State Machine, rule 1) | Verdict | Evidence |
|---|---------------------------------------------------------------------------------------------------|---------|----------|
| 1 | Every deferred (`[~]`) task is resolved or explicitly waived | **met** | `tasks.md`: 27 `[X]`, 0 `[~]`, 0 `[ ]` (the three `[~]`/`[ ]` strings in the file are prose in DoD-1 and the deferral-discipline note); `verification.md` `deferred_tasks=` empty |
| 2 | Review evidence has been produced | **met** | `review.md` (this file), `code-review.md`, and `test-evidence/review2-probes.txt` on disk |
| 3 | The current code-segment record contains no `blocking` entry | **met** | `report --summary --file code-review.md` → `gate=allow`, `blocking_entries=0`, exit 0 |

**Outcome: the transition is permitted — Feature 076 advances `Implemented → Ready for Review`.**
Rule 4 applies and is disclosed: one `important` entry is open in the code record and awaits the
author's one-line answer (agree / disagree + reason); it does not block. Rule 8 applies and is
disclosed on both carriers: the code segment's `not-evaluated` verdict (127 skipped files earn no
coverage credit) does not block either. No waiver is claimed anywhere — the third condition is met
by the existence test on the current record, not by clearing anything.

### 2.3 Previous Round — review #1 findings and their disposition (re-verified)

Review #1 raised seven process findings F1–F6 (one P0, five P1) and F7–F12 (six P2). The repair
round claimed F1–F6 repaired. Every claim below was re-measured on the tree in this run.

| Prior finding | Severity | Re-verified disposition | Evidence anchor |
|---|---|---|---|
| **F1** — the record grammar had no normative home outside a plan artifact | P0 | **CLOSED** | `shared/guidelines/decision-tension.md` § 记录行文法 now states the field line, the two-space pole sub-lines, the `### T-NNN` carrier, the continuation rule and the fence rule; the owner's own fenced example was extracted verbatim by this review and fed to the checker → **exit 0, zero findings** (probe P-A). Guard: `test_owner_example_passes_the_validator_verbatim` |
| **F2** — the `N/A` rule was fail-open (one flat sentence satisfied four triggers) | P1 | **CLOSED for the reported defect; the repair introduces a new one — see F13** | `N/A — 不可逆、跨团队、高爆炸半径、与宪法原则相关四类触发均不成立。` now exits 1 with `dtr-section-missing` (probe P-B); the flat-sentence inverse sample is permanent |
| **F3** — two of six validator labels had no defect class | P1 | **CLOSED** | § I's table grew to five rows covering all six labels; the guard imports `LABELS` and asserts set equality instead of copying the list |
| **F4** — SC-002/SC-003 were closed by an artifact the asserting test wrote | P1 | **CLOSED as proposed** | the severity mapping is now program output — per-finding `severity`, per-label `severity`, aggregate `channel.high` in both human and `--json` forms; all seven snapshots re-rendered from it; SC-002 asserts `payload["channel"]["high"]` against 0/1/1/1. The disclosed residual is unchanged and still honest: the `/speckit.analyze` narrative layer was never run end to end, and no SC depends on it |
| **F5** — ten checklist failures never got a closure record | P1 | **CLOSED** | `checklists/readiness-2026-10-29.md` § Closure maps CHK004/011/014/018/020/022/026/027/029/031 to their analyze disposition, to FR/contract/task anchors and to a closing assertion; all ten named test functions exist in the three suites (verified by name) |
| **F6** — a pointer resolved from the authoring file's own directory | P1 | **CLOSED** | the template points at `.specify/shared/guidelines/decision-tension.md` in repo-root form; the assertion derives its base from an instantiated `.specify/specs/<key>/plan.md`, asserts the plan-relative reading is dead, and asserts the pointer does **not** resolve from the template directory — the old base is now a negative control instead of the assertion's base |
| **F7** — `post_change_commit=` cannot be filled by the run that writes the log | P2 | **accepted-for-roadmap** (not repaired) | `verification.md` still writes `post_change_commit=3c1a288c` with an inline explanation |
| **F8** — the feature detail's `## Latest Review` carrier was stale | P2 | **repaired by this run's own obligation** — the status gate requires writing it, and it is rewritten in the same commit as this report | `.specify/memory/features/076.md` § Latest Review |
| **F9** — artifacts copied a status fact (reviewer over-counted three sites) | P2 | **corrected** — the finding's "all three copied it wrong" was wrong: `tasks.md:6` quoted the owner correctly. The repair added the missing live pointer and a dated trace to that line | `tasks.md:6` now carries a dated CORRECTED comment pointing at the live status home (`.specify/memory/features.md`, row 076) |
| **F10** — an SC's own count did not match its measurement source | P2 | **WITHDRAWN (reviewer error)** — review #1's arithmetic was wrong. SC-001's parenthetical enumerates six inverse-input **classes**, the first of which expands to six runs: 6 + 5 = 11 inverse runs, plus one compliant run = the 12 its Source states. The criterion reconciles; only the stylistic advice (state a cardinal once) survives, and it is recorded as a requirements-template recommendation, not as a defect | `requirements.md:233` vs `:244`; previous round's §9.2 |
| **F11** — `/speckit.analyze` leaves no artifact | P2 | **accepted-for-roadmap** (not repaired) | still no analyze report on disk; three analyze rounds exist only as prose in the state spine |
| **F12** — framework bash scripts hard-require an undeclared variable | P2 | **deferred** (not repaired) | `check-prerequisites.sh` unchanged; this run never invoked it |

Net after re-verification: **six of six blocking/important items closed**, two P2 corrected or
withdrawn, three P2 accepted-for-roadmap, one P2 deferred. Nothing in the prior set was closed by
assertion alone.

## 3. Findings (Problems & Improvement Targets)

Two new findings this round. Both were introduced or exposed by the repair. One is the repair's own
connected surface; the other is a documentation seam the repair created.

### F13 — The repaired `N/A` rule rejects justifications the declaring documents accept

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**:
  `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/validate-decision-tensions.py:314-327`
  (constant at `:116`, criterion text at
  `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/plan-template.md:75-77`)
- **Evidence** (verbatim quote, the predicate the repair added):

  ```
          remainder = line.replace(hits[0], "", 1).strip()
          remainder = remainder.strip("-—:：,，.。;；、!！?？()（）[]【】 \t")
          return hits[0] if len(remainder) >= NA_MIN_JUSTIFICATION else None
  ```

  with `NA_MIN_JUSTIFICATION = 8` at `:116`, against the only rule an author is told:

  ```
  If and only if this plan contains no load-bearing decision, write the literal `N/A` plus one line
  per trigger explaining why that trigger does not hold (the trigger list is owned by the owner's
  threshold section); the section MUST NOT be deleted or left empty.
  ```

  Measured on independent fixtures written by this review (`test-evidence/review2-probes.txt`
  § P-C, P-D, P-L, plus the P-B inverse control), each of which satisfies "one line per trigger
  explaining why it does not hold":

  ```
  - 不可逆：无迁移、无重建。         -> discarded (remainder 7 chars)
  - 跨团队：无契约变更。             -> discarded (remainder 5 chars)
  - 高爆炸半径：影响面限于本文。      -> discarded (remainder 7 chars)
  => exit 1, dtr-section-missing: `N/A` does not justify these triggers one by one: 不可逆、跨团队、高爆炸半径

  - 与宪法原则相关：不触及任何 MUST 条，也不存在不可逆的迁移。
  => discarded whole (the line also names 不可逆), so BOTH that trigger and 不可逆 are reported unjustified

  - **不可逆**：只改文档。            -> ACCEPTED (the asterisks and colon push the remainder to 9)
  - 不可逆：只改文档。               -> REJECTED (same content, no markup)
  ```

- **Why it's a problem**: two shape rules the declaring documents never state — a
  ≥ 8-character floor on what remains after removing the trigger, and a one-trigger-name-per-line
  exclusivity — decide whether a plan passes a HIGH gate. An author who writes exactly what the
  template asks is rejected, and the diagnosis says the triggers were not justified one by one when
  they were. The floor also measures markup rather than content: identical wording passes bold and
  fails plain (the bold form's remainder is 9 characters, the plain form's is 4). The direction is fail-closed (no bad plan slips through), so nothing is corrupted —
  but every trivial plan that writes a terse clause pays a rewrite against a gate whose message
  points at the wrong cause. This is the F1 defect class (an enforcement rule with no normative
  home) surviving in the half of the `N/A` rule the repair rebuilt.
- **Proposed fix**: either (a) declare both rules where authors read them — the plan template's
  `N/A` paragraph plus `shared/guidelines/decision-tension.md`, including the character floor and
  what counts toward it (markup excluded) — or (b) drop the floor and keep only "one trigger per
  line, named at the line start, followed by any further text", which still rejects the flat
  sentence (it names four triggers on one line) and accepts `不可逆：无迁移、无重建。`. Whichever
  branch is chosen, keep the flat-sentence inverse sample red and add the three fixtures above as
  permanent inverse/positive samples so the calibration cannot drift back.

### F14 — The channel's severity now has two definition points, and the consumer sentence names neither

- **Severity**: P2
- **Category**: Documentation
- **Location**:
  `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/references/detection-and-severity.md:108-124`
  (program side: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/validate-decision-tensions.py:79-80,582-600`)
- **Evidence** (verbatim quote, the consumption contract as it stands after the repair):

  ```
  Deterministic verdicts: every mechanically decidable part — field presence, enumerated values,
  reference resolution — is printed by `scripts/python/validate-decision-tensions.py`, whose
  `--json` `checks` array carries the per-label counts. Consume that verdict; MUST NOT re-score the
  record semantically, and MUST NOT turn a label count into a percentage or a maturity score.
  ```

  against what the program now prints (the repair's own `--json` keys):

  ```
      "channel": {"value_domain": "HIGH-or-0", "high": <n>},
      ... "checks": [{"label": …, "status": …, "count": …, "severity": "HIGH" | 0}, …]
      ... "findings": [{"line": …, "label": …, "severity": "HIGH", "text": …}, …]
  ```

  and against the table one screen above, whose `Severity` column restates the same fact as the
  program constant `CHANNEL_SEVERITY = "HIGH"`.
- **Why it's a problem**: F4's repair moved the severity mapping into the program precisely so the
  channel would have one definition point — but the document that tells the detector what to consume
  still names only `checks` … "per-label counts", and the aggregate the SC evidence actually reads
  (`channel.high`) is unmentioned. A detector following this paragraph consumes the pre-repair
  surface. At the same time the table's `Severity` column is a second copy of `CHANNEL_SEVERITY`,
  guarded only by a test literal (`row[2] == "HIGH"`), so the document and the program can drift in
  the direction that matters without any assertion going red.
- **Proposed fix**: in `detection-and-severity.md` § I, replace "carries the per-label counts" with
  the three fields the program emits (`checks[].severity`, `findings[].severity`, `channel.high`),
  say that `channel.high` is the channel verdict, and make the guard import `CHANNEL_SEVERITY` and
  assert the table's severity cells equal it — the same import-not-copy pattern the label column
  already uses.

## 4. What Worked — Preserve (Brief)

- The F6 repair turned the old base into a **negative control**: the assertion now proves that a
  plan-relative pointer is dead and that the pointer does not resolve from the template directory.
  A guard that once could not go red for its subject now cannot go green for it either.
- The owner-example guard is the right shape for a copy-paste contract: the example is extracted from
  the owner verbatim and fed to the checker, so owner and program cannot drift while it holds.
- `link_verdict()` moved a judgement out of a test and into the validator, reusing `index_records()`
  (no second parser) and declaring its one call surface in the docstring instead of pretending the
  CLI consumes it.
- The widened quartet key anchor ships with its negative half (`test_indented_key_stays_part_of_the_value_above`),
  which is what keeps "each key exactly once" readable after the prefix allowance.
- The checklist `## Closure` block leaves the ten original `fail` rows byte-identical and maps each
  to its analyze disposition — a dated audit, not a status board.
- Evidence binding survived a repair: all seven sha256 values in `verification.md` recomputed in this
  run, all seven match; `sync-mirrors.py --check` and `regen-command-copies.py --check` both rc=0.
- 39 pre-existing suite failures neither fixed nor masked; this round ran only the three feature
  suites (76 passed) plus its own probes — the budget was respected.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Every enforcement rule needs a sentence the author can read** — Target: `templates/plan-template.md`
  (absolute: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/plan-template.md`) §
  Decision Tensions, `N/A` paragraph. Change: state the per-trigger line shape exactly as the checker
  reads it (one trigger per line, trigger named first, any further text counts, markup does not), or
  point at an owner section that does. Source: F13. Expected impact: no author is rejected for
  following the template, and the F1 class stops recurring one rule at a time.

### 5.3 Automation / Scripts Improvements

- **Calibrate the `N/A` floor or remove it** — Target: `scripts/python/validate-decision-tensions.py`
  (absolute: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/validate-decision-tensions.py`)
  `_justified_trigger()`. Change: drop `NA_MIN_JUSTIFICATION` and keep the exclusivity rule, or
  measure the remainder with markup stripped and declare the floor in the template. Source: F13.
  Expected impact: the fail-closed gate stops producing false rejections with a wrong diagnosis.

### 5.5 Documentation Improvements

- **Name the fields the program emits in the consumption contract** — Target:
  `skills/internal/analyze-artifacts/references/detection-and-severity.md` (absolute:
  `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/references/detection-and-severity.md`)
  § I "Deterministic verdicts". Change: list `checks[].severity`, `findings[].severity` and
  `channel.high`; state that `channel.high` is the channel verdict; and have the guard import
  `CHANNEL_SEVERITY` rather than asserting a literal. Source: F14. Expected impact: one definition
  point for the severity mapping, and a detector that reads the current surface.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Declare or drop the `N/A` remainder floor; keep the per-line exclusivity rule | `templates/plan-template.md` + `scripts/python/validate-decision-tensions.py` | F13 |
| P2 | Consumption contract names the severity fields; table severity imported, not copied | `skills/internal/analyze-artifacts/references/detection-and-severity.md` | F14 |
| P2 | (carried) `post_change_commit=` → post-commit pointer | `templates/verification-log-template.md` | F7 |
| P2 | (carried) durable analyze report path | `templates/commands/analyze.md` + analyze skill | F11 |
| P2 | (deferred) declare and self-heal `CWS_LIB_BASH_HOME` | `.specify/scripts/bash/*` prerequisites | F12 |

## 7. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary), with an absolute path only as a
  parenthetical supplement; no target needed an `external` marking.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without
  opening the source file; F13 and F14 additionally carry the measured output or the emitted keys
  inline, and all twelve probes are archived verbatim in `test-evidence/review2-probes.txt`.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside
  this document.
- [x] No unfilled placeholder tokens remain. The bracketed tokens in the program-output excerpt
  (`<n>`, `…`) are elisions of a verbatim quote, marked as such.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one
  source finding ID.
- [x] P0 validation status is stated explicitly in §2: no P0 raised, the pass is vacuously satisfied.
- [x] **Deliberate deviation from the handoff's id family**: this report coins **no `REC-…`
  identifiers**, for the same reason review #1 gave — the stage brief restricts writes to the two
  review artifacts, the status update and stage evidence, so a durable `REC-…` id could not be
  registered in `.specify/memory/register.md` in the same commit as the ID Register rule requires.
  New findings continue the prior round's `F-` sequence (F13, F14) so the two rounds cross-reference
  without ambiguity.

## 8. Post-review Fix (F13)

`F13` (P1) was closed by the driver after this review run, in a separate commit:

- `scripts/python/validate-decision-tensions.py`: the undeclared `NA_MIN_JUSTIFICATION = 8`
  threshold is gone; the rule is now "the remainder must say why", with a **closed** bare-negation
  set (`不会` / `不是` / `没有` / `否` / `无` / `不成立` / `不存在`) as the mechanical line.
- `shared/guidelines/decision-tension.md` § 记录行文法: the `N/A` grammar is now declared —
  one trigger per line, each with a reason, bare negations rejected, length explicitly not the
  test.
- `tests/contract/test_decision_tension_contract.py`: the stub inverse sample still goes red (bare
  negation), and a new **short-but-real** sample (`无迁移` / `不动契约` / `限于本节` / `不触 MUST`)
  passes — proving length was the wrong proxy.
- Evidence: three feature suites + the C-11 guard = **87 passed**; mirrors `--check` clean;
  `validate-tasks` PASS.

`F14` (P2) remains `accepted-for-roadmap`: the severity consumption contract in
`contracts/analyze-channel.md` still does not name `channel.high`, and the channel table's
`Severity` column duplicates `CHANNEL_SEVERITY` as a second definition point.

## 9. Feedback

Please share the contents of this document with the spec-kit framework developers.
