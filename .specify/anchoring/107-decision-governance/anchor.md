---
status: active
created: 2026-11-25
updated: 2026-11-25
handoff_ref: .specify/specs/107-decision-governance/handoff.md
---

# Anchor: Decision Governance

## Objective

AI Agent decisions are governed by one contract: every decision item names its object unambiguously (full names, full resource location on possible same-name conflicts), offers a closed option set, is archived and auditable in existing carriers, travels intact from superagent to subagent and is implemented with a receipt tied to its id — with human-interactive decisions optimized for readability and AI-autonomous decisions optimized for rigor.

## Success Criteria

1. All 30 FR and 10 SC of spec 107 are delivered and verified, including red-first machine guards for the M rules and named review obligations for the B rules.
2. Every producer in the closed Decision Producer Inventory archives reconstructable decisions in existing carriers (register, decision-tension, checkpoints, exec records); no second register; superagent-to-subagent transmission and implementation receipts are end-to-end auditable; silent divergence is an explicit anomaly.
3. Preserved surfaces stay byte-stable (sentinel literals, watcher verdicts/exit codes, five-element uplink, seven-field downlink, confirmation discipline, two-slot budget); legacy records are annotated read-only, never rewritten.

## Boundaries

- No push, no second register/store, no automatic decision-making, no machine-coverage claims for behavior-class rules.

## History

- 2026-11-25 — created.
