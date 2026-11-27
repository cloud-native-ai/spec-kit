---
id: "20261127T094647Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261127T094343Z-112a"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "112-decision-batch-panel"
feature_id: "112"
partial: false
created: "2026-11-27T09:46:47Z"
summary: "Analyze round 2 (incremental, C/H-only with residue) of 112-decision-batch-panel at 8aad9c47d: 15 domain files re-read in full (touch-volume gate: 8/15 repaired > half -> full-domain C/H adjudication)"
---

## Review
Analyze round 2 (incremental, C/H-only with residue) of 112-decision-batch-panel at 8aad9c47d: 15 domain files re-read in full (touch-volume gate: 8/15 repaired > half -> full-domain C/H adjudication). Verdict: 0 CRITICAL / 0 open HIGH. Round-1 HIGHs I-01 (cross-batch read boundary) and I-02 (supersession append vs batch-record immutability) fixed by the A-26/A-27 repair and confirmed at the rule level by direct re-read (subagent unavailable; worker role forbids dispatch). 4 new findings on the repaired boundary: I-07 MEDIUM (record op writes the batch record before the superseded_by append, so the mandated refusal cannot honour SC-006 no-new-record), U-05 MEDIUM (append has no settled-target qualifier and no same-target concurrency rule; SC-010 absolute wording unaligned), A-03 LOW (the appends constitutive read is outside the four read-only purposes), I-08 LOW (A-27 carve-out missing from the feature detail and from owner-page authoring rows T028/T048/T033). 14 round-1 MEDIUM/LOW carried as residue, all deferred with reasons, none dropped. Gates: validate-requirements ok; validate-tasks PASS; pre-analyze --stage tasks pass 0 errors / 77 missing-path advisories; account-clause-coverage exit 2 baseline-missing (G-01, FR lane 44/45, G-02); decision tensions ok 0 records; mirrors/copies rc 0; gate scan 30 blocking / 0 violations; probe registry 130 objects; knowledge 0 batch entries; workspace guard clean vs the repair snapshot. Gate NOT cleared: G-01/G-02/I-03 and the new MEDIUMs remain. Feature 112 stays Planned; no registry/spine edit.

## Optimization Points
- transaction ordering - the A-27 append sits after write batch record in the record op; FR-029/C-510/SC-006 require refusing the item with no new record when the prior carrier is unwritable. Move the prior-carrier readability/writability check into the preconditions before the write (one sentence, no rule change).
- append target semantics - state that the append target is a settled prior record, and add a conflict rule for two batches appending to the same record (re-read + named refusal, or a documented re-append form); align SC-010 and the T033 test description with the carve-out.
- append read boundary - name the appends constitutive read inside the A-27 exception (FR-037/C-507) or scope the read-purpose sentence to informational reads, so a literal read-side guard cannot forbid the sanctioned write.
- repair fan-out - carry the A-27 carve-out into the live derived carriers that cite its clauses: feature detail line 34, T028, T048, and T033s mutual-write-isolation phrasing.
- analyze coverage ownership - G-01 (coverage-baseline.txt absent; freeze assigned to /speckit.tasks but scheduled at implement T004) still makes the clause-delta lane unjudgeable; give the freeze one owner or declare an analyze-side waiver.
