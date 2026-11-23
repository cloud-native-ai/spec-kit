---
id: "20261123T122840Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "r20261123T121000Z-consume01"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-11-23T12:28:40Z"
summary: "Framework-hat Path A consume of 30 inbound bundles (1,184 entries / 2,228 points). Identity: one self-delivery copy (feedback-spec-kit, 346 byte-identical entries; 555 points counted once), no orphans"
---

## Review
Framework-hat Path A consume of 30 inbound bundles (1,184 entries / 2,228 points). Identity: one self-delivery copy (feedback-spec-kit, 346 byte-identical entries; 555 points counted once), no orphans and no re-deliveries; new client material 838 entries / 1,673 points. 22 read-only verifier groups covered 2,228/2,228 points: 737 STILL-VALID / 552 PARTIAL / 224 ALREADY-FIXED / 715 NOT-OURS. 26 routing backlog rows (F1-F24); introspection-20261123T115631Z confirmed (1 finding, 2 excluded); exec-quant 1,168 records ingested into 20 groups; all 30 bundles removed, intake empty, consume-log appended; no network.

## Optimization Points
- token-efficiency: the 22 verifier groups were dispatched before identifying the self-delivery copy (feedback-spec-kit bundle: 346 entries / 555 points byte-identical to the local store), so roughly a quarter of verification effort re-checked already-consumed material; add an engine identity action (bundle-to-store byte comparison) and run it before group partition.
- record/package write surfaces have no point-shape validation: about 20 'optimization points' in this batch were headings, table separators or bare tokens, and 9 byte-identical duplicate point pairs existed; reject heading-shaped and duplicate points at write/package time (or count them as a degraded read).
- consume inventory: --action list still returns the post-truncation count (default limit 5, corrected here with --limit 0); return a pre-truncation total field (existing backlog root cause).
