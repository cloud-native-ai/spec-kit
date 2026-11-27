---
id: "20261127T082900Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261127T074400Z-111a-analyze-r2"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "111-general-best-practices"
feature_id: "111"
partial: false
created: "2026-11-27T08:29:00Z"
summary: "Analyze round 2 (incremental) for 111-general-best-practices: re-checked the 12 round-1 loci repaired in the analyze-repair commit 61e3ccfb6 and their one-hop neighbors, then adjudicated the full CRIT"
---

## Review
Analyze round 2 (incremental) for 111-general-best-practices: re-checked the 12 round-1 loci repaired in the analyze-repair commit 61e3ccfb6 and their one-hop neighbors, then adjudicated the full CRITICAL/HIGH set on the repaired tree. All three blocking findings are fixed: AR1-02 (CRITICAL) — the promotion procedure, generality criterion and 来源 shape are now owned by the module manifest 逐步积累机制 section (A-22) across requirements/contracts/data-model/plan/research/tasks/quickstart/feature-ref, and knowledge-promotion.md is cited only for the knowledge-recording obligation it actually defines; AR1-01 (HIGH) — the observation carrier is the engine real --review text with a legal identity convention (/speckit.<command>+command or skill:<name>+skill, else custom:best-practices/observation + --unit-type custom-unit + bp-<yyyy-mm-dd>-<slug> with the probe-inject prerequisite); engine re-measured 2026-11-27: record requires --unit-id/--run-id/--review/--points with no notes field, unit-type pairings enforced at feedback-utils.py:861-873, probe-utils.py exposes probe-inject; AR1-03 (HIGH) — T007A (write-mode mirror regeneration) now precedes T008 and T008 blockedBy includes it, C-404 prelude unchanged, no impossible green checkpoint remains. Two new findings: AR2-01 (MEDIUM) — eight summary/checkpoint loci still characterize accumulation as pointer-only, including the US2 Checkpoint line reused only by pointer, which contradicts A-22/FR-004 and would fail a correct US2 implementation if applied literally; AR2-02 (LOW) — the accumulation contract header owner list omits the 来源 traceability shape that A-22/FR-004/data-model E8 assign to the manifest. Residues: AR1-04/AR1-05/AR1-06 (MEDIUM) and AR1-07..AR1-11 (LOW) deferred (untouched by the round-1 repair, decision-class); AR1-12 closed/rejected (resolved downstream in tasks Environment Prerequisites). Open set: CRITICAL 0 / HIGH 0 / MEDIUM 4 / LOW 6. Gates: validate-requirements 0/0 (229 lines, 7 shared strings), validate-tasks PASS 0/0; 9 FR / 7 SC / 24 A / 24 clauses / 20 tasks / 24 green tags, each clause claimed once. Report: test-evidence/analyze-round2-report.md; findings: test-evidence/analyze-round2-findings.jsonl (14 records).

## Optimization Points
- a normative ownership repair (A-22) must sweep the summary layers too: eight descriptive/checkpoint lines still said accumulation is declared by pointer, and a US2 checkpoint line is a verdict surface. Record the rule, not the instance: after changing an owner, grep every descriptive restatement of the old model, not only the normative clauses.
