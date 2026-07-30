---
id: "20260730T071029Z-skill-create-agent"
unit_id: "skill:create-agent"
unit_type: "skill"
run_id: "capacity-rename-refactor-20260730"
scope: "local"
partial: false
created: "2026-07-30T07:10:29Z"
summary: "Refactored agent-definition templates to remove the capacity/responsibility confusion. (1) Moved all 8 create-team agent-* templates into templates/agents/ (they express team responsibility), renaming"
---

## Review
Refactored agent-definition templates to remove the capacity/responsibility confusion. (1) Moved all 8 create-team agent-* templates into templates/agents/ (they express team responsibility), renaming the supervisor to agent-team-supervisor-template.md. (2) Renamed the 7 create-agent agent-role-*-template.md to agent-capacity-*-template.md and the role-scope frontmatter key to capacity-scope (7 templates + 14 landed agents), plus the kind:role authoring mode to kind:capacity and the {{ROLE_SCOPE}} placeholder to {{CAPACITY_SCOPE}}. (3) Added Class->Instance framing (capacity template = abstract class; create-agent instantiates to .specify/agents/<slug>.agent.md; run spawns instances) to create-agent/SKILL.md and design.md. Preserved the team-domain Role dimension and roster role: field per user decision. Updated 5 tests (2 also fixed a stale baseline path), conceptual-model, capacity-vs-responsibility, and 5 docs. Validation: zero new failures, 36 baseline failures fixed (74->38); all skills/agents mirrors byte-identical; zero residual live agent-role- refs.

## Optimization Points
- The word "role" carried four distinct meanings (create-agent filename/concept, the role-scope frontmatter key, the team-domain Role×Stage×Type dimension, and roster seat labels). Renaming blindly would have corrupted the team conceptual model. Splitting scope up front — Capacity replaces only the create-agent capability concept, while Role stays as the team seat/responsibility dimension — was the decisive call and should be the template for any future concept rename.
- Two contract tests (test_handoff_chain, test_context_injection, ~42 failures) were already red at baseline because their TEMPLATES_DIR pointed at a stale parents[2]/"templates" path that no longer holds the role templates. A rename refactor is the natural moment to fix such latent path rot: the same edit that applied the new filename also corrected the path, turning 36 baseline failures green. Capture-baseline-first discipline was essential to tell "I fixed a pre-existing bug" apart from "I introduced a regression".
- The `kind: role` authoring selector and the `agent-team-supervisor-template.md` existence assertions were non-obvious couplings the mechanical rename would have broken or inverted: the conformance scenario asserted the bare supervisor name "no longer exists", which became false the moment the supervisor was renamed to exactly that. Auditing test *semantics*, not just filename strings, caught it.
- Both skills/ and .specify/skills/ are independent git copies (an Explore agent wrongly reported root skills/ as empty). Every git mv and edit had to be dual-applied and verified with diff -rq. Trusting the filesystem over the agent summary prevented a half-migrated tree.
