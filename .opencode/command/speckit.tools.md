## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). If empty, display list of all registered tools. If `tool_id` and natural-language hint conflict, stop and request correction.

## Outline

Goal: Definition-first tool management. Create, modify, view, or invoke tools with explicit behavioral rules that override LLM built-in knowledge.

For detailed tool type semantics, behavioral rules format, edge cases, and invocation preview format, see `.specify/shared/definitions/tool-definitions.md`.

### Execution Steps

1. **Determine intent**: Parse `$ARGUMENTS` → classify as: **define** | **modify** | **view** | **invoke** | **list**.

2. **Resolve existing record**: Check `.specify/memory/tools/<tool-name>.md`. Check alias matches.

3. **Route by intent and record state**:

   | Intent | Record Exists | Action |
   |--------|--------------|--------|
   | define | No | → Collect mandatory fields |
   | define | Yes | → Inform user; offer modify or view |
   | modify | Yes | → Field-level update |
   | modify | No | → Error: use define intent |
   | view | Yes | → Display full definition |
   | view | No | → Error: no definition found |
   | invoke | Yes + Verified | → Preview and confirm |
   | invoke | Yes + Draft | → Error: complete definition first |
   | invoke | No | → Error: define first |
   | list | — | → Show summary table |

4. **Create new tool** (define intent, no record):
   - **CRITICAL**: Mandatory fields MUST be provided by user. Do NOT auto-populate from built-in knowledge.
   - Collect: Tool Name, Tool Type (`project-script`|`system-binary`|`shell-function`|`webhook`), Source Identifier, Description
   - Optionally collect: Behavioral Rules (RFC 2119 format), Parameters, Returns, Aliases
   - If only name provided: offer discovery via `.specify/scripts/bash/create-new-tools.sh --json --name $ARGUMENTS --action find` to bootstrap draft
   - Validate → set status (`Draft` or `Verified`) → persist at `.specify/memory/tools/<name>.md`
   - Generate `tool_id` from canonical path

5. **Modify**: Load record → apply field-level updates only → re-validate → persist.

6. **Invoke**: Load record → display preview (command, params, rules, expected output) → `Proceed? (yes/no)` → execute only on explicit yes.

7. **Register**: Add/update entry in `.specify/instructions.md` `## Resource Registry` → `### Tools`.

8. **View/List**: Display full definition or summary table of all tools.

For agent-specific operational guidance, see `.specify/shared/workflow/agent-configuration.md`.

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/shared/workflow/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this command reached its wrap-up stage. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against `/speckit.tools`'s declared purpose and produce a short review plus ≥1 concrete, command-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this command's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id` (e.g. the feature key + a run timestamp); if a nested skill/command already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "/speckit.tools" --unit-type command \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
6. **Consolidated submission prompt.** If the returned `should_prompt` is `true`, surface a single consolidated prompt inviting the user to submit collected feedback to the Spec Kit developers; on confirmation run `--action mark-submitted`. Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.

## Handoffs

**Before**: Use when you need to externalize and reuse tool records with strict behavioral rules.

**After**: Tool records are available for agent permissions wiring and `/speckit.instructions` registry.