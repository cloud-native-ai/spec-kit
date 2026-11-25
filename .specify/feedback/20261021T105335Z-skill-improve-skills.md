---
id: "20261021T105335Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-sdd-project-setup-20261021"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
disposition: "ignored"
partial: false
created: "2026-10-21T10:53:35Z"
summary: "Improved sdd-project-setup local-mode behavior: S0 defaults to the current project when host+path are absent; local topology uses orchestrator-direct or the host's native subagent and must not launch "
disposition_reason: "introspection-20261021T133447Z: excluded (no actionable framework finding)"
---

## Review
Improved sdd-project-setup local-mode behavior: S0 defaults to the current project when host+path are absent; local topology uses orchestrator-direct or the host's native subagent and must not launch qodercli; S4 marks preflight 1-3 n/a locally. Mirrors, docs, and contract test C-15 synced. Gates: shape pass (~4412/5000), redline PASS, 21 contract tests passed; adjacent wiring failures match clean baseline (zero regression).

## Optimization Points
- Pressure test GREEN quoted the new sections; RED asked for host/path instead of defaulting, confirming the S0 gap. The carrier half was inconclusive because the local host already chose native over qodercli without the skill.
- token-efficiency: SKILL.md controllable estimate rose ~3718 -> ~4412 (+694, +18.7%), still under the 5000 budget; the added S0 table is the main growth and should be kept tight in future comparisons.
- Unresolved: next real execution on a qodercli-default host should confirm local runs stay native/direct.
