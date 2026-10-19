> Dated record — archived 2026-10-20 from `/tmp/sdd-loop-efficiency-brief.md` (verbatim below). This is the requirement source and trade-off authority for spec 063; it is never cited as current runtime reality.

# Optimization Brief — Accelerating Subagent-Driven SDD Runs

## Goal

Create a new Spec Kit optimization feature that improves the end-to-end throughput of
the `sdd-loop-driver` and other workflows that depend on subagent-driven SDD stage
execution. The target project is the Spec Kit framework repository itself
(`/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`).

## Observed baseline (reported by the requester)

- A medium-sized feature run performs the full stage chain; checklist largely repeats
  analyze conclusions and costs about 8 minutes.
- The full test suite ran six times during one feature run, although most stages only
  needed targeted tests.
- Stage progress is invisible under buffered `-p` output, forcing blind polling.
- Stage subagents can be interrupted when the main session's agent process exits,
  because they are not fully decoupled from the driver session.

## Required optimization points

1. **Medium-feature fast lane**
   - For medium-sized features, allow skipping `checklist` because it largely repeats
     `analyze` conclusions.
   - Keep `analyze` and `review`: both caught real defects in the observed run.
   - Define the entry criteria for "medium feature" and the safety conditions under
     which the fast lane is allowed. It must be explicit and auditable, never a silent
     default.

2. **Two full-suite runs only**
   - Run the full test suite exactly twice: once at the start of `implement`, once at
     final closure.
   - Intermediate stages and `review` use targeted test sets.
   - Preserve the ability to detect regressions; document the targeted-set selection
     rule and the evidence each stage must record.

3. **Plan-stage "minor-fix-only, no re-review" constraint**
   - Pre-set a plan-stage constraint that limits downstream changes to small fixes and
     avoids a full re-review loop.
   - The requester notes this requires changing framework command internals and is a
     separate topic; if it cannot be implemented safely in this feature, record it as
     an explicit exclusion or accepted design cost rather than silently dropping it.

4. **Progress visibility and session decoupling**
   - Use `--output-format stream-json` so in-stage progress is visible and blind
     polling is reduced; derive a compact live log and preserve the stage sentinel
     contract.
   - Run stage subagents detached (`nohup`) so an unexpected exit of the main
     session's agent process does not interrupt them; the driver must still be able to
     monitor, verify and re-enter from the state spine.
   - Keep the existing safety rules: no unauthorized push, confirmation gates intact,
     independent verification and stall handling unchanged.

## Scope and constraints

- Primary surface: `skills/external/sdd-loop-driver/` (SKILL.md, references, runner
  recipes and watcher integration). Framework command internals only if the optimization
  cannot be achieved at the orchestration layer.
- The feature must be developed through the complete current SDD chain. The fast lane
  proposed by this feature applies to future runs, not to this run itself.
- Preserve backward compatibility with existing users of the loop driver; new behavior
  must be explicit and opt-in where it changes quality gates.
- No automatic transmission of feedback; no bypass of confirmation gates; no silent
  skipping of required verification.

## Expected outcome

- A documented and implemented mechanism with tests/contracts proving:
  - the medium-feature fast lane is explicit and safe;
  - full-suite executions are bounded to two per feature run with targeted tests in
    between;
  - the plan-stage constraint is either implemented or explicitly recorded as
    out of scope;
  - stream-json progress and nohup decoupling work together without breaking sentinel
    detection, independent verification or re-entry.
