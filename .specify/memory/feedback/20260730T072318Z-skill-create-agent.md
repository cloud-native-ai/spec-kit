---
id: "20260730T072318Z-skill-create-agent"
unit_id: "skill:create-agent"
unit_type: "skill"
run_id: "capacity-authority-gate-20260730"
scope: "local"
partial: false
created: "2026-07-30T07:23:18Z"
summary: "Applied the capacity->responsibility gating principle to the three remaining create-agent templates. (1) agent-supervision-delegation.md: replaced the retired hard-coded Evaluator(Meta)/Optimizer(Meta"
---

## Review
Applied the capacity->responsibility gating principle to the three remaining create-agent templates. (1) agent-supervision-delegation.md: replaced the retired hard-coded Evaluator(Meta)/Optimizer(Meta) labels with operating-object judgment — Evaluator scores the deliverable => Worker (process-evaluator would be Meta), Optimizer rewrites the executor prompt/environment => Meta, and only that Meta write-authority lets it edit the agent layer. (2) agent-skill-enablement.md: added a capability->responsibility note (capacity gates responsibility; only agents that can edit agent/skill/team definitions are Meta and may hold optimizer/process-evaluator/team-config responsibilities) in the authoring comment, NOT the C-2 replicated protocol paragraph. (3) agent-project-custom-template.md: noted that tools: is capacity — the default read-only [Read,Grep,Glob] confines it to Worker; write tools are required (deliberately) to be Meta. Incorporated the user's deliverable-vs-process distinction for evaluator Type. Validation: failure set identical to baseline (38), zero new; create-agent mirror byte-identical; replicated protocol paragraph untouched across 15 files.

## Optimization Points
- The EEI delegation snippet still hard-labeled Evaluator(Meta)/Optimizer(Meta) — residue of the retired Type-follows-Stage rule that an earlier pass fixed in the stage templates but missed here. Applying a conceptual correction leaves stragglers wherever the old rule was independently restated; a token sweep for the retired pattern ("evaluator (Meta)", "optimizer (Meta)") should follow any Type-model change, not just the primary files.
- The user's deliverable-vs-process distinction sharpened the criterion: an evaluator scoring the *deliverable* is a Worker, but one scoring the *delivery process* is Meta. This is the same operating-object rule (product = business artifact; process = the agent loop itself), and it belongs in the conceptual model as the canonical way to disambiguate evaluator Type.
- The write-authority note had to live in the authoring HTML comments, not the replicated protocol paragraph: agent-skill-enablement.md's body is byte-identical across 15 files under contract C-2, so any body edit would have required 15-file propagation and risked breaking the identity test. Distinguishing "replicated body" from "authoring-only comment" before editing an SSOT snippet is essential.
