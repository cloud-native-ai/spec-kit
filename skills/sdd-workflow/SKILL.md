---
name: sdd-workflow
description: |
  Shared knowledge base for Spec Kit SDD (Specification-Driven Development) lifecycle commands.
  Contains common protocols, guidelines, and reference material used across multiple /speckit.* commands.
  This skill is NOT invoked directly — it provides reference documents that commands load on demand.
  Use this when the user mentions ["SDD workflow", "speckit protocols", "command shared references"]
---

# SDD Workflow — Shared Command Protocols

This skill provides shared reference documents consumed by `/speckit.*` commands during execution. Commands reference specific files from `${SKILL_HOME}/references/` to avoid duplicating common logic.

## Reference Index

| File | Used By | Purpose |
|------|---------|---------|
| `user-input-protocol.md` | All commands | Standard `$ARGUMENTS` processing rules |
| `feature-integration.md` | requirements, plan, tasks, implement, checklist, feature | Feature tracking system integration protocol |
| `agent-configuration.md` | agents, tools, skills | Agent detection, per-agent guidance, feedback capture |
| `checklist-methodology.md` | checklist | Detailed examples, anti-examples, quality dimension methodology |
| `requirements-guidelines.md` | requirements | Spec quality validation, success criteria guidelines |
| `dfx-catalog.md` | feature | Design-For-X category catalog for future feature discovery |
| `clarify-taxonomy.md` | clarify | Three-mode taxonomy coverage categories and integration rules |
| `ignore-patterns.md` | implement | Technology-specific ignore file patterns |
| `tool-definitions.md` | tools | Behavioral rules format, edge cases, tool type details |

## Usage Convention

Commands reference these files with:
```
See ${SKILL_HOME}/references/<filename>.md for full details.
```

The AI agent MUST load the referenced file when it needs the detailed protocol. The command itself contains only the minimal workflow steps and command-specific logic.

## Feedback

At the end of a substantial run of this skill, perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/skills/sdd-workflow/references/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this run reached a meaningful wrap-up. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against this skill's declared purpose and produce a short review plus ≥1 concrete, skill-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this skill's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id`; if a parent flow already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "skill:sdd-workflow" --unit-type skill \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
6. **Consolidated submission prompt.** If the returned `should_prompt` is `true`, surface a single consolidated prompt inviting the user to submit collected feedback to the Spec Kit developers; on confirmation run `--action mark-submitted`. Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.
