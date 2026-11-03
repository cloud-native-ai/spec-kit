# Driver Completions — Feature 081, slice 081a

**What this file is**: the three places in this feature where the delegated stage subagent stopped
before returning its sentinel and the **loop driver** finished the stage. It is a disclosure record,
not an acceptance claim: a stage marked "done" whose sentinel never came back is a stage the driver
completed, and a reader comparing stage status against subagent self-report needs to see that.

**What it is not**: it changes no verdict and licenses no shortcut. Each completion below was
followed by the same U4 independent validation the stage would have received anyway, and the
validation result is what the stage status is based on.

**Authority for the stage status itself**: `.specify/state/081-acceptance-hardening.md` (the state
spine, owned by the driver). This file adds the per-completion detail the spine's one-line row has no
room for.

| # | Stage | Subagent stop point | What the driver did | Commit |
|---|-------|--------------------|---------------------|--------|
| 1 | `/speckit.plan` (081a) | 120-turn limit reached; sentinel `PLAN-DONE` **not** returned | Ran the full-suite baseline the subagent had left as an empty capture and corrected EP-009's evidence from "empty file / no log" to the real result (`39 failed / 6970 passed / 7 skipped`); appended the final-tree gate evidence; ran the independent re-validation (`validate-requirements` ok, `validate-decision-tensions` 6/6, `pre-analyze-check --stage plan` pass, `regen-command-copies.py --check` / `sync-mirrors.py --check` exit 0); committed the plan set | `ea058fae` |
| 2 | analyze-fix | 120-turn limit reached; sentinel `ANALYZE-FIX-DONE` **not** returned | Accepted the partial edit set, completed `test-evidence/analyze-fix-report.md` itself, ran the validators (`validate-requirements` ok, `validate-tasks` 0/0, `decision-tensions` 6/6, `pre-analyze-check --stage tasks` pass, decomposition `proceed` 24/40) and committed | `f9f6d4f3` |
| 3 | `/speckit.implement` part 2 (T007–T014) | 120-turn limit reached; sentinel `PART2-DONE` **not** returned | Re-ran mirror/copy sync, ran the targeted suites itself (`test_requirements_checker` 40 passed, `test_acceptance_state_machine` 14 passed, `test_checker_form` + `test_measurement_instruments` 50 passed; the two intended reds recorded — `test_closure_acceptance_check` 11F/5P pre-T015, `test_gate_wiring_081` 7F/1P pre-T016), closed T007–T014 and committed | `c9dc8cec` |

## Why these are disclosed rather than smoothed

The failing modes a completion hides are exactly the ones a red-first, evidence-backed slice cannot
afford: a task closed on an artifact the subagent never wrote, a red run claimed without a recorded
run, a validator reported green without being run. Each row above names the driver-performed
substitute for the subagent's own step, so a later reader can re-run that step and check it — the
three commits are the artifacts of record.

**Effect on 081a's own findings**: completion 3 is why `tasks.md` DoD-2 distinguishes the two
modules with a real recorded red run (T007, T010) from the two that went green in the same part
(T008 extended an existing green module; T009's module was new but turned green with T012/T013).
"Every module was red-first" would have been a claim the driver could make only by asserting on the
subagent's behalf; the recorded runs say otherwise.
