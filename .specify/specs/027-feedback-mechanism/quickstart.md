# Quickstart: Framework Feedback Mechanism

**Feature**: 028 Feedback Mechanism | **Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

This quickstart shows how the local feedback layer behaves once implemented, and how to verify each user story.

## What it does (in one line)

At the wrap-up of a qualifying flow (every skill; complex commands only), the executing agent self-reflects and records a local, unit-scoped Feedback Entry to `.specify/memory/feedback/`; once enough accumulate, it prompts you once to submit them to the Spec Kit developers.

## 1. A skill produces feedback (User Story 1 — P1)

Run any skill end-to-end (e.g. `analysis-project`). At its final `## Feedback` step it records:

```bash
python3 .specify/scripts/python/feedback-utils.py --action record \
  --unit-id "skill:analysis-project" --unit-type skill \
  --run-id "analysis-20260713T1730" \
  --review "Reviewed my own run against my stated purpose (deep project analysis)." \
  --points-file points.txt
```

Verify the entry exists and is local-scoped:

```bash
python3 .specify/scripts/python/feedback-utils.py --action list --limit 1
cat .specify/memory/feedback/*-skill-analysis-project.md   # scope: local, ## Review + ## Optimization Points
```

✅ Pass when the entry references the skill's purpose and lists ≥1 optimization point (or the explicit no-op line).

## 2. A complex command produces feedback (User Story 2 — P2)

Run a complex command (e.g. `/speckit.plan`). At its `## Optional: Git Commit` wrap-up it also records a command-scoped entry with `unit-id "/speckit.plan"`, `unit-type command`.

Run a **simple** command (e.g. `/speckit.constitution`) and confirm **no** entry is written:

```bash
python3 .specify/scripts/python/feedback-utils.py --action list --unit-id "/speckit.constitution"
# -> No matching entries
```

✅ Pass when complex commands record and simple commands (`agents`, `constitution`, `feature`, `team`) do not.

## 3. Selective triggering & no duplication (User Story 3 — P3)

- Trivial/short flows produce **zero** feedback (no prompt, no overhead).
- A command that invokes a skill records **at most one** entry per unit per run (dedup on `(unit_id, run_id)`):

```bash
# second record for the same run is a no-op
python3 .specify/scripts/python/feedback-utils.py --action record \
  --unit-id "skill:analysis-project" --unit-type skill --run-id "analysis-20260713T1730" \
  --review "x" --points "y"
# -> {"duplicate": true, ...}  (count_since_submission unchanged)
```

✅ Pass when re-recording the same run does not add an entry or bump the count.

## 4. Threshold submission prompt (FR-011 / SC-007)

Check store state anytime:

```bash
python3 .specify/scripts/python/feedback-utils.py --action status
# {"count_since_submission": 10, "threshold": 10, "should_prompt": true, ...}
```

When `should_prompt` is `true`, the agent surfaces a single consolidated prompt: *"You've accumulated 10 feedback entries — submit them to the Spec Kit developers?"* On confirmation:

```bash
python3 .specify/scripts/python/feedback-utils.py --action mark-submitted
# count_since_submission resets to 0; submitted_at stamped
```

Below the threshold, no prompt appears.

## 5. Aborted run (FR-009)

If a flow fails before wrap-up, either no entry is written, or it is recorded with `--partial` and a `**Partial run** —` labeled review. Never a full review of incomplete work.

## Conformance quick checks

```bash
# every installed skill carries the feedback step
grep -L "## Feedback" skills/*/SKILL.md    # -> should list nothing

# the skill template carries it (so new skills inherit it)
grep -c "## Feedback" templates/skills-template.md   # -> >= 1
```
