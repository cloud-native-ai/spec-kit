# Contract — Role-Transition Payload & super↔sub Protocol Fields

**Status**: design contract (Feature 095) · Rule owners referenced, never restated: `.specify/shared/guidelines/fast-fail.md` § 子代理派发注入; `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation / § External Dispatch Visibility Contract / § The Concurrency Obligation; `shared/guidelines/reporting-obligations.md`; `shared/definitions/re-anchoring-definitions.md`.

## C-1. Downlink role fields (FR-008)

Every governed dispatch payload carries six fields (shape in `data-model.md` § 6): `parent_identity`, `child_label`, `role_declaration`, `depth_position`, `authority_ref`, `return_channel`. The four pre-existing injections keep travelling by pointer to their owners; this contract adds fields only.

## C-2. Role-transition injection ([[STR-003]])

When a subagent is granted dispatch duty, its payload MUST carry the literal marker `role-transition` plus the nine pointer items of `data-model.md` § 7. The list is **closed**: removing any item is a payload-construction defect.

## C-3. Physical presence & self-check (FR-018, FR-021)

- The injection MUST be physically present in the payload text; a standing instruction layer does not reach a subagent.
- The **existing** pre-dispatch self-check form (`fast-fail.md` § 派发前自检 — a payload-substring judgement on an identifier) is extended to require the `role-transition` identifier and its item-id slugs. This contract adds the judged identifier, not a new check: the check's owner, owner literal and landing stay where they are. Missing identifier → blocked before dispatch as a payload-construction defect (not a fast-fail "decision").
- Judgement MUST NOT rely on natural-language keyword matching as the sole criterion — the identifier is the criterion.

## C-4. Red lines (anti-nesting)

The payload's red lines — no skill-load instruction, no driver-skill reference, no loop logic, no full driver manual — are owned by FR-017 and `subagent-definitions.md` § Dispatch-Time Governance Obligation; this contract references them and MUST NOT restate them. Violation of any is contract-test red.

## C-5. Upload-side return contract (FR-009, FR-019)

Every return carries: result or deliverable path; evidence pointer(s); an explicit anomaly line (stating "no anomaly" explicitly when none); the concurrency reading triple (`requested` / `effective` / `effective_reason`, `not_evaluated` where intervals are absent); the returning executor's identity. Missing any item → `incomplete`; the parent MUST NOT consume the conclusion and MUST NOT backfill fields.

A dual-role executor retains every upload duty of a subagent; gaining the superagent role reduces none of them.

## C-6. Aggregate return (FR-020)

A dual-role executor returns **one** structured result to its parent: per-child attribution, per-child evidence paths, failures and anomalies surfaced; the aggregate does not replace child evidence (the parent can drill down).

## C-7. Message classes (FR-010)

The closed class set and the no-progress-forwarding rule are declared once by the owner page (FR-010); this contract consumes the four machine tokens (`ack` / `answer` / `result` / `attention-escalation`) and states only that no new attention mechanism, channel or notification service is introduced.

## C-8. Waiting & attempts (FR-012, FR-013)

Waiting is bounded and observable through the existing watch model (`skills/external/sdd-loop-driver/references/watch-model.md`); human abort/redirect stays servable; slow vs stalled uses the existing thresholds. A retry is a new attempt (new label); stale attempts are identified by the existing attribution values; old attempt artifacts are kept.

## C-9. Authorization (FR-014, FR-028)

What an edge may do is decided only by `sdd-route.py --action authorize` (+ recorded routing verdict + team territory). Message content never widens permission. Refusals produce the existing named refusal record. Resume/retry re-validates before acting.

## C-10. Termination (FR-015)

Edge end (`completed` / `failed` / `cancelled`) is written into the edge's existing carrier; no silent orphaning; cancel/terminate follow existing confirmation gates — no new gate.

## C-11. Surface wiring (FR-034)

| Surface | Change (fields/pointers only) |
|---------|------------------------------|
| `skills/internal/run-agent/SKILL.md` — "Dispatch-time injection (mandatory)" block | Add the [[STR-003]] pointer item (one bullet): when dispatch duty is granted, the payload carries the closed nine-item list |
| `skills/internal/create-team/references/patterns.md` — Per-Agent Payload table | Add a `role_fields` row (six fields by reference) |
| `skills/internal/create-team/SKILL.md` — Report contract | Add the mandatory dispatch mapping table `label \| role \| workspace \| parent` inside `## Execution Detail` |
| `skills/external/sdd-loop-driver/SKILL.md` — Driver Topology / U0.5 | One pointer line: the driver is the root super agent; stage dispatch payloads carry the role fields; execution stays with the existing pre-dispatch self-check and U4 — no new gate |
| `skills/external/sdd-loop-driver/references/stage-prompts.md` — envelope sidecar | Add the `role_edge` object (six fields) |

No stage sequence, sentinel, gate or dispatcher changes.

## C-12. Command examples

> **Premises / execution status (per example)**: the surfaces above are documentation edits; their verification is `tests/contract/test_role_transition_payload.py` (route: contract-test pinning). Premise: the payload template tables named above exist at the quoted locations (measured 2026-11-10). No runnable command is emitted by this contract; nothing else is disclaimed.

## C-13. Guarding tests

`tests/contract/test_role_transition_payload.py`: nine-item presence (item-id slugs); delete-one → self-check blocks; anti-nesting red; six downlink fields present in each wired surface; return-contract five items; aggregate per-child attribution; dual-role duties intact (mutation: grant superagent and drop an upload duty → red). `tests/contract/test_superagent_definitions.py` pins the four message-class tokens against the owner page and the no-progress-forwarding rule's presence there.
