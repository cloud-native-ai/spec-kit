# Red-first evidence — slice 081d

Dated record of slice 081d's pre-change readings, taken before its rows landed. Every entry carries the
command actually run, its real output and its exit status; nothing here is reconstructed from memory, and a
reading that changed during the slice keeps both states.

This file is 081d's own. 081a's `notes/red-first-evidence.md`, 081b's `notes/red-first-evidence-081b.md` and
081c's `notes/red-first-evidence-081c.md` are dated records of other slices: they are cited here and MUST NOT
be rewritten or merged into.

Run context: `2026-11-03`, repository `spec-kit`, branch `081-acceptance-hardening`, entry HEAD
`72c16f33` (`72c16f3323e25fefbb59acf9ed93eb8c201f1df5`). Probes that need a writable registry use
`SPECIFY_LINE_REGISTRY_DIR=.specify/.tmp/…` (FR-025); `git status --porcelain` was `0` lines after them.

---

## 1.1 The line-state registry does not admit `blocked` (T001 (a), T006's gap)

```
$ SPECIFY_LINE_REGISTRY_DIR=.specify/.tmp/081d-t001-probe \
  python3 skills/external/sdd-loop-driver/scripts/line-registry.py --action register \
    --line-id 081d-t001-probe --branch 081-acceptance-hardening \
    --worktree-path /…/spec-kit-wt-probe --project-dir /…/spec-kit --repo-root /…/spec-kit
{"branch": "081-acceptance-hardening", "claimed_ns": 1793694885504073000, "cli": "qodercli",
 "created_at": "2026-11-03T08:34:45Z", "driver_session": "pid:20558", "last_event": "registered",
 "line_id": "081d-t001-probe", …, "state": "active", …, "write_line": false}
exit 0

$ SPECIFY_LINE_REGISTRY_DIR=.specify/.tmp/081d-t001-probe \
  python3 skills/external/sdd-loop-driver/scripts/line-registry.py --action update \
    --line-id 081d-t001-probe --state blocked
{"error": {"code": 2, "message": "invalid state: 'blocked' (expected one of ['active', 'closed',
 'completed', 'orphaned', 'stale', 'stalled', 'waiting'])"}, "ok": false}
exit 2
```

Two earlier attempts failed on the register action's own preconditions, and both are kept because they are
what the row's one-line spelling of the probe does not say: `--project-dir` and `--repo-root` are required,
and `--worktree-path` must be outside `--repo-root`
(`{"error": {"code": 2, "message": "register requires --project-dir"}}`, exit 2; then
`register requires --repo-root`, exit 2; then
`worktree_path must be outside repo_root: /…/spec-kit`, exit 2). The seven-value domain above is the gap
A6 items 1–8 close: `blocked` is not merely undocumented, it is **rejected**.

## 1.2 The `STATE_VALUES` literal is seven values at line 46 (T001 (c))

```
$ grep -n "STATE_VALUES" skills/external/sdd-loop-driver/scripts/line-registry.py
46:STATE_VALUES = {"active", "waiting", "stalled", "completed", "orphaned", "stale", "closed"}
380:    require(state in STATE_VALUES, f"invalid state: {state!r} (expected one of {sorted(STATE_VALUES)})")
exit 0
```

Line 380 is the single validation point every one of A6's eight dispositions has to pass through, which is
why the dispositions are assertions about behaviour and not about the literal's spelling.

Where the literal `blocked` **does** occur in that script, it is not the line state at all — it is the
queue's dependency grouping, the second class § Verification Vocabulary's reconciliation names:

```
$ grep -n "blocked" skills/external/sdd-loop-driver/scripts/line-registry.py
1614:    blocked_by: dict[str, set[str]] = {}
1619:        blocked_by[line_id] = set()
…
1667:            "blocked_by": sorted(blocked_by[line_id]),
exit 0   (10 hits, every one of them `blocked_by`)
```

## 1.3 The two remaining vocabulary owners (T001 (d) and (e), T010's gap)

```
$ grep -c "Blocked" templates/feature-index-template.md
0
exit 1
```

The count is `0` and the file is 21 lines; its only status surface is the `Status` **column header** of the
index table — so the obligation is to **add** a closed value domain, not to insert one value into a list that
is already there. Measured, the whole file:

```
$ cat -n templates/feature-index-template.md
…
18	**Total Features**: [FEATURE_COUNT] _(auto-derived; recompute on every edit — see comment above)_
19
20	| ID | Name | Description | Status | Feature Details | Last Updated |
21	|---|---|---|---|---|---|
```

```
$ grep -n "Status vocabulary" skills/internal/manage-features/SKILL.md
121:- Status vocabulary: `Draft | Planned | Implemented | Ready for Review | Completed`
exit 0
```

Five values, `Blocked` absent — and the skill's `Never regress status` rule (line 62) carries no
`Implemented → Blocked` exception at all:

```
$ grep -n -i "never.regress" skills/internal/manage-features/SKILL.md
3:description: Maintain and refresh the project feature registry — … (tolerance band, archive-not-delete,
   never regress status). …                      [line 3 truncated here; it is the skill's description]
62:- **Never regress status**: registry convergence must not move a feature's status
95:   byte-identical) and the never-regress-status rule.
131:  This skill records statuses per that machine and never regresses them (rule above);
exit 0
```

## 1.4 The four `blocked` literals, as they measured before 081d (T001 / FR-019)

The reconciliation did not exist anywhere: the only place the four were mentioned together was the
§ Extension Points promise this slice has to retire.

```
$ grep -n "blockedBy\|four .blocked. literals\|unrelated facts" shared/workflow/acceptance-hardening.md
667:- Additions to § Verification Vocabulary (**081d**) — the reconciliation of the four `blocked` literals (owner:
exit 0
```

Each owner was measured on its own, and each already carried its own literal — which is why T002's leg
asserts that the mapping is real instead of asserting that the four values are equal:

```
$ grep -n "Blocked" templates/feature-details-template.md | head -2
59:- **Blocked**: [STATUS_BLOCKED_CRITERIA]
73:| Planned | Implemented | `/speckit.implement` | **Four conjunctive conditions, all required** — stated in
    full in the block below. Three of four is `Blocked`, never a partial pass. |
exit 0

$ grep -n "blocked" templates/verification-log-template.md | head -2
16:  4. For every SC whose status is blocked / deferred / partial, emit the five
26:  - `status` is one of: pass | fail | partial | blocked | deferred | unknown. THIS FILE OWNS THAT VOCABULARY:
exit 0

$ grep -n "blockedBy" templates/tasks-template.md | head -2
109:- **[blockedBy: T001,T002]** (optional): explicit dependency tag — this task MUST NOT start until every
     listed task is `[X]`. Machine-checkable alternative to prose like "depends on T012"; prefer it whenever
     a dependency exists. Tasks without the tag follow phase order only.
212:- [ ] T014 [US1] [blockedBy: T012,T013] Implement [Service] in src/services/[service].py
exit 0
```

with the fourth — the line state — absent, per § 1.1 and § 1.2 above.

## 1.5 The driver's closure gate is unwired (T001 (f), T008's gap)

```
$ grep -n "gate-cmd\|gate_cmd" skills/external/sdd-loop-driver/scripts/integrate-lines.py
79:def integrate_line(repo: Path, trunk: str, reg: Path, archive: Path, entry: dict, gate_cmd: str | None) -> dict:
101:    if gate_cmd:
102:        gate = run(["bash", "-c", gate_cmd], cwd=wt)
152:    parser.add_argument("--gate-cmd")
211:        results.append(integrate_line(repo, args.trunk, reg, archive, entry, args.gate_cmd))
exit 0

$ grep -c "closure-acceptance-check" skills/external/sdd-loop-driver/scripts/integrate-lines.py
0
exit 1
```

The hook exists and is **opt-in**: `--gate-cmd` defaults to `None`, so a merge runs with no judgement unless
a caller remembers the flag, and `scripts/python/closure-acceptance-check.py` is named nowhere in the script.
That is the three-call-site shortfall SC-001 reads as 2 of 3 before T008 lands.

## 1.6 The audit mode exits 2 as not implemented (T001 (b), T013's gap)

```
$ python3 scripts/python/closure-acceptance-check.py \
    --spec-dir tests/fixtures/acceptance-hardening/positive --audit-existing
closure-acceptance-check: input error: --audit-existing is not implemented in this slice: FR-020's
read-only audit is 081d work (plan.md § Slice Boundary). Refusing to emit a per-feature verdict from an
audit invocation rather than report the opposite of what the mode must do.
exit 2
```

The flag is on the stable calling surface (C-04) and the mode is not, which is why T013 is an implementation
row and not a wiring row.

## 1.7 Both of this slice's named carriers are absent (T001 (g))

```
$ ls tests/contract/test_line_state_blocked.py tests/contract/test_acceptance_schema_ownership.py
ls: tests/contract/test_acceptance_schema_ownership.py: No such file or directory
ls: tests/contract/test_line_state_blocked.py: No such file or directory
exit 1
```

## 1.8 The coverage lane: `2` of `25` FRs cited, `23` uncovered (T001 (h), DoD-8's remainder)

```
$ python3 scripts/python/account-clause-coverage.py --spec .specify/specs/081-acceptance-hardening
UNCOVERED-FR: FR-001
UNCOVERED-FR: FR-002
UNCOVERED-FR: FR-003
… (23 UNCOVERED-FR lines in total: FR-001…FR-008, FR-010, FR-012…FR-025 — every FR except FR-009 and
   FR-011, the two 081b reached through its citation groups)
FR uncovered: 23

companion (must be non-empty on a green run): claimed clauses 0, scanned files 248, clause universe 1517, FR universe 25
  [clause-uncovered] fail (513) — 513 uncovered, 18 beyond the frozen baseline
  [fr-uncovered] fail (23) — 2 of 25 FRs cited from citation groups
  [clause-unparsable] warn (103) — 103 files yield no clause id under the owner's forms; 0 of them declare a positive form, which is parse doubt and is never read as zero-and-covered
  [coverage-baseline-delta] fail (18) — baseline holds 495 names; 495 uncovered items are baseline-internal and do not block
41 error(s), 0 warning(s)
status: uncovered
exit 1
```

**The `0/25` that `tasks-081c.md` § Deferred Slices carried is stale.** 081b's two citation groups moved the
count to `2 of 25` (FR-009 and FR-011), so T016 measures this reading and not the carried figure. Copying
`0/25` forward would have made that row measure a number that no longer exists.

---

## 2. The slice's own red-then-green runs

### 2.1 T002's leg, before the owner-doc addition — red

The leg `test_the_four_blocked_literals_stay_four` was written first and run against the
unmodified owner document:

```
$ bash scripts/bash/run-tests.sh tests/contract/test_acceptance_state_machine.py -q
FAILED tests/contract/test_acceptance_state_machine.py::test_the_four_blocked_literals_stay_four
FAILED tests/contract/test_acceptance_state_machine.py::test_the_feature_index_template_carries_a_closed_status_vocabulary
FAILED tests/contract/test_acceptance_state_machine.py::test_manage_features_names_blocked_and_points_at_the_machine_for_its_exception
3 failed, 14 passed in 0.12s
exit 1
E   AssertionError: shared/workflow/acceptance-hardening.md § Verification Vocabulary must carry the
    reconciliation of the four `blocked` literals (FR-019); no such subsection exists
```

The other two failures in that run are T003's legs, which are red by design until T010 (see § 2.3).

### 2.2 T002 landed — its leg is green, T003's two stay red

§ Verification Vocabulary gained § The four `blocked` literals are four unrelated facts, and the
§ Extension Points bullet lost the half it promised. **One deliberate deviation from T002's literal
wording**: the row says to delete "the matching bullet", but that bullet carried **two** obligations — the
four-literal reconciliation *and* `templates/feature-index-template.md`'s closed status vocabulary — and
`checklists/081d-2026-11-03.md` CHK009 (P2, "FAIL") records exactly this: deleting the whole bullet would
leave the index-template obligation with neither body nor promise between T002 and T010, and T010 is not
this slice's first phase. The remedy CHK009 names ("delete only the ① half and keep ②'s pointer") is the one
applied: the bullet now carries the index-template value-domain obligation alone and states that the
reconciliation is no longer promised here because it landed. The dead half is gone, no promise of a landed
section remains, and an unlanded obligation was not made bodyless.

```
$ bash scripts/bash/run-tests.sh tests/contract/test_acceptance_state_machine.py -q
FAILED tests/contract/test_acceptance_state_machine.py::test_the_feature_index_template_carries_a_closed_status_vocabulary
FAILED tests/contract/test_acceptance_state_machine.py::test_manage_features_names_blocked_and_points_at_the_machine_for_its_exception
2 failed, 15 passed in 0.06s
exit 1
```

### 2.3 T003's SV-06 legs — red at this tree, and that is the reading (green at T010)

Both legs fail for the reason they exist, and both messages are the measured pre-change state:

```
E   AssertionError: templates/feature-index-template.md carries no status value domain at all; SV-06 requires
    a closed status vocabulary containing `Blocked`, added beside the table (today the file's only status
    surface is the `Status` column header)

E   AssertionError: the `Status vocabulary` line must be the six values ['Draft', 'Planned', 'Implemented',
    'Blocked', 'Ready for Review', 'Completed']; measured ['Draft', 'Planned', 'Implemented',
    'Ready for Review', 'Completed'] — five values is the pre-081d shape, and a seventh would be a value the
    state machine does not admit
```

T003 is red **before T010 by mandate** (tasks.md § Dependencies: "T003 (vocabulary) before T010"). A green
assertion written after its subject cannot show that the subject was missing, so this pair stays red until
T010 lands; `verification.md` reads it as red-by-design, never as a new failure.

### 2.4 T004 — the review-composition run on the final source

T004 is a measurement, not an edit with a red state of its own; its readings are in
`test-evidence/081d-review-site-measurement.txt` (commands, exit codes, the four segment verdicts, the
`7 / 7` coverage line, the smoke triple, the seven-key `final_path` record) and its produced record is
`tests/fixtures/acceptance-hardening/review-implemented-clean/review.md`. Recorded there rather than here so
the run has one evidence file, per C-08's copy-once rule. The one number worth carrying: the composition's
structural carrier re-ran green at this tree (`32 passed`, exit 0), so the record was produced under the
shape the final source carries.
