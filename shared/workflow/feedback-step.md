# Canonical `## Feedback` Step

**Feature 028 — Framework Feedback Mechanism.** This file is the single source of
truth for the `## Feedback` step that every qualifying unit embeds. Skills embed it
as their final workflow section; the 13 **complex** command templates embed it at
their wrap-up / Git-commit-prompt stage. Simple commands MUST NOT embed it.

Do not diverge per surface — copy the canonical block below verbatim (adjusting only
the `<unit-id>` / `<unit-type>` placeholders for the embedding unit).

---

## Canonical block (copy verbatim into the embedding unit)

```markdown
## Feedback

At wrap-up (the same lifecycle point where this unit would prompt for a Git commit),
run this self-reflection step. It is agent self-reflection — **never** solicit feedback
content from the user.

1. **Gate on qualification & completion.** Only proceed if this run reached wrap-up and
   did substantial work. Skip entirely for trivial/no-op runs. If the run was aborted or
   failed before wrap-up, follow the *Abort / partial-run rule* below.
2. **Reflect (no user input).** Review the just-completed run against this unit's declared
   purpose/description. Produce a short prose review plus **≥1 concrete, unit-specific
   optimization point**. If the run was clean, record exactly one line:
   `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to *this* unit's operation. Do NOT produce a
   global/whole-project assessment — that is `/speckit.review`'s job. Every entry is
   `scope: local`.
4. **Dedup guard.** Choose a stable `run_id` for this run (e.g. the feature key + a run
   timestamp). If a parent flow already recorded feedback for this same `(unit_id, run_id)`,
   the engine will no-op — do not force a duplicate.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "<skill:NAME | /speckit.COMMAND>" --unit-type "<skill|command>" \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
6. **Consolidated submission prompt.** Read `should_prompt` from the `record` output
   (or run `--action status`). When it is `true`, surface a **single** consolidated
   notification inviting the user to submit collected feedback to the Spec Kit developers;
   on user confirmation run `--action mark-submitted`. Below threshold, do NOT prompt.

**Abort / partial-run rule.** If the run failed or was interrupted before wrap-up, either
skip recording OR record with `--partial` and a `## Review` that begins with
`**Partial run** — `. Never present a partial run as a complete review.

**Nesting rule.** When a command invokes a skill (or a skill invokes a skill), each
qualifying unit records feedback for **its own** scope only, keyed by its own
`(unit_id, run_id)`. The same unit+run MUST NOT be recorded twice.
```

---

## Notes for embedders

- **Skills**: `--unit-id "skill:<name>"`, `--unit-type skill`. The section is the last
  workflow section of `SKILL.md`.
- **Complex commands**: `--unit-id "/speckit.<command>"`, `--unit-type command`. Place the
  section next to `## Optional: Git Commit`, never mid-flow.
- **Simple commands** (`agents`, `constitution`, `feature`, `team`): omit this step entirely.
- The engine store lives at `.specify/memory/feedback/`; threshold defaults to `10`
  (`--threshold` / `SPECKIT_FEEDBACK_THRESHOLD`).
