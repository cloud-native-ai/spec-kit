# Critique and Self-Critique Orientation

Spec Kit's improvement mechanisms can observe, qualify, diagnose, and validate —
but nothing in that chain, by itself, decides **what is actually worth changing**.
批评和自我批评 (critique and self-critique) is the method that makes that decision at
the head of the self-improvement flow, 通过更辩证的思索避免「盲目改进」「反复改进」
「越改越差」 (blind improvement, churning improvement, getting-worse improvement).

The method is defined by the decidability of its output, not by good intentions:
every proposed change must survive **one falsification attempt** — a named,
executable inspection that would show either the premise behind the change is
false, or the change made things worse — before it is dispatched. A critique step
whose output cannot fail is worthless; it would be the very 盲检 (blind-check)
class it exists to prevent.

## Where the method is expressed

| Layer | Location | Role |
|-------|----------|------|
| Normative owner | `.specify/shared/guidelines/critique-and-self-critique.md` | Single source of truth: falsification-attempt output form, acceptability criteria, verdict handling, the self-critique half, failure-mode → rule mapping, boundaries |
| Flow landing point | `.specify/shared/workflow/self-improvement-workflow.md` — SI-3C | Critique runs after diagnosis has produced the proposal and before routing dispatches it |
| Reproducibility bar | `.specify/shared/guidelines/user-facing-comprehension.md` § 机械判据 · `.specify/shared/guidelines/fast-fail.md` § 判据同样覆盖机器给出的绿 | Two reviewers executing the same attempt reach the same verdict; a green that could not go red is not evidence |
| Form precedent | `.specify/shared/definitions/derivation-definitions.md` | The falsification-attempt form is isomorphic to the Derivation Step `falsification` field (different object, same house shape) |
| Same-author case | `.specify/shared/workflow/objective-analysis-gate.md` | When proposal and critique share an author, execution of the attempt is delegated |
| Evidence qualification | `.specify/shared/workflow/evidence-step.md` (SI-2) | Critique consumes frozen candidates; it never re-qualifies evidence |

## The three failure modes in one glance

All three were measured in this repository. The rule that closes each is *named*
below; the operative mapping table with evidence anchors lives in the owner.

| Failure mode | Shape it takes | Closing rule (named — details in the owner) |
|--------------|----------------|---------------------------------------------|
| 盲目改进 (blind improvement) | A ruling inferred from prose, falsified only when implementation reaches it — each one costs a full dispatch | Code-first falsification, executed before dispatch |
| 反复改进 (churning improvement) | Objectives and criteria re-cut repeatedly within one round while the core term migrates | A re-cut is itself a proposal |
| 越改越差 (getting worse) | A routed-but-unexecuted fix does not stay static — the wrong claim spreads; the flow's own instrument silently under-reports | Handoff refuses unexecuted attempts; instrument self-check |

## What this is not

- **Not a new user-confirmation flow.** The critique step halts a proposal on
  evidence, never on a prompt; it adds nothing to the governance-kept list of
  `.specify/shared/guidelines/confirmation-gates.md`.
- **Not a replacement for the Fast Fail binary.** Correction-vs-decision still owns
  anomalies found mid-execution (`.specify/shared/guidelines/fast-fail.md`);
  critique owns proposal qualification before dispatch.
- **Not a second feedback store.** Verdicts ride the artifacts the proposal already
  lives in; the red lines of `.specify/shared/workflow/feedback-step.md` §
  Positioning & Red Lines are untouched.
- **Not free-form review.** Concern lists, risk narratives, and "consider
  whether…" entries are rejected forms; the output form is closed and owned.

> **Related**: [better-harness.md](./better-harness.md) — Better Harness names the
> goal all improvement serves; critique and self-critique decides which proposals
> may pursue it.
