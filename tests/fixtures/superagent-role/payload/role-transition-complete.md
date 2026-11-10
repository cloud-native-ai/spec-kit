# Dispatch payload — role-transition injection (complete)

A dispatch payload that grants dispatch duty (`dispatch_duty: granted`). It carries the
literal `role-transition` marker and the closed nine-item pointer list; every item is a
pointer to its owner, never rule text. The seven downlink role fields ride in the same
payload (see `role-fields.md`).

## role-transition — closed nine-item pointer list

1. `role-activation-scope` — the superagent role activation and the dispatchable scope on this edge.
2. `self-identity-parent-edge` — the executor's own identity and its parent edge.
3. `downward-obligation-checklist` — the obligations to inject into each of its own dispatches, by pointer.
4. `concurrency-budget-ref` — the available concurrency budget and the existing slot / reserve facts, by pointer to their owners.
5. `reporting-path` — the reporting path and the reporter duty, by pointer to its owner.
6. `state-carriers-writer-boundary` — the existing state carriers it reads and writes, and the writer boundary, by pointer.
7. `attention-classes-escalation` — the message classes and the escalation rules, by pointer to their owner.
8. `depth-remaining-prohibitions` — the remaining depth and the prohibitions that still bind it, by pointer to their owners.
9. `aggregate-return-contract` — the aggregate return contract: one structured result with per-child attribution.
