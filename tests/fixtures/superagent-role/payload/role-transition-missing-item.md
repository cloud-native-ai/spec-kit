# Dispatch payload — role-transition injection (one item deleted)

A copy of the complete payload with exactly one pointer item deleted. The marker is still
present; the pre-dispatch self-check MUST block this payload as a payload-construction
defect because one item-id slug is missing (the identifier alone is insufficient).

## role-transition — closed nine-item pointer list (one deleted)

1. `role-activation-scope` — the superagent role activation and the dispatchable scope on this edge.
2. `self-identity-parent-edge` — the executor's own identity and its parent edge.
3. `downward-obligation-checklist` — the obligations to inject into each of its own dispatches, by pointer.
4. `concurrency-budget-ref` — the available concurrency budget and the existing slot / reserve facts, by pointer to their owners.
5. `reporting-path` — the reporting path and the reporter duty, by pointer to its owner.
7. `attention-classes-escalation` — the message classes and the escalation rules, by pointer to their owner.
8. `depth-remaining-prohibitions` — the remaining depth and the prohibitions that still bind it, by pointer to their owners.
9. `aggregate-return-contract` — the aggregate return contract: one structured result with per-child attribution.
