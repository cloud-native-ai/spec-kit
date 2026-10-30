# Contract: Dispatch Payload

**Scope**: what the coach sends to the single subagent, and what it must never send. The payload is a closed field set.

**Authority**: the two-context rule is owned by [`../requirements.md`](../requirements.md) FR-009 / FR-029; the subagent concept and the three execution modes are owned by [`shared/definitions/subagent-definitions.md`](../../../shared/definitions/subagent-definitions.md). This contract does not restate either.

## C-1 Required Fields

| Field | Content | Rule |
|-------|---------|------|
| `trainee` | Resolved identifier, resolved path, layer | The exact path the run resolved; no alternatives offered |
| `work` | `<work>` verbatim | Byte-for-byte the second positional parameter |
| `instruction` | "Follow the Trainee's own `SKILL.md` as the highest execution guidance" | MUST NOT be replaced by a coach-authored procedure |
| `return-contract` | Structured return: step-by-step actions, tool calls, state changes, artifacts, elapsed time, terminal state | Powers `self-report` when host events are unavailable |
| `anomaly-line` | "State one explicit anomaly line on return; state `none` when there is none" | Silence is not read as clean |
| `fast-fail-clause` | The dispatcher's anomaly discipline, injected at dispatch time | Subagents do not inherit the orchestrator's conversation |
| `confirmation-relay` | "If the Trainee flow reaches a destructive step, stop and report it back instead of approving it yourself" | The answer comes from the user; the subagent never self-approves |

## C-2 Forbidden Fields

The payload MUST NOT contain:

1. the expectation file, any `OC-*` / `PE-*` row, or a summary of them;
2. the coach's deviation guesses or conclusions about `<work>`;
3. a coach-authored simplification or reordering of the Trainee flow;
4. any artifact path inside the run directory (the subagent writes Trainee outputs, not coach records).

## C-3 Dispatch Cardinality

- Exactly one payload is dispatched per run (see `coaching-run.contract.md` C-6).
- A failed dispatch is not re-sent with a modified payload; the failure is recorded.

## C-4 Return Handling

- The returned anomaly line is written into the DispatchRecord unchanged.
- Self-reported steps become `self-report` rows; anything the self-report does not cover becomes an `observation-gap` row rather than an inferred one.
- A return that claims completion without the Trainee's primary artifact is recorded as `partial`, not `completed`.

## C-5 Transport Record

- The payload's transport (native subagent tool, `run-agent` fallback, or `run-skills` explicit-path mode) is recorded in the DispatchRecord `mode` field.
- The rendered payload is stored or referenced by the DispatchRecord (`payload-ref`); its raw text is not injected into the coach's user-facing report.
