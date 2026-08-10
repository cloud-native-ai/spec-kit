---
id: "20260810T101804Z-skill-create-skills"
unit_id: "skill:create-skills"
unit_type: "skill"
run_id: "create-improve-docs-20260810"
scope: "local"
feature: "037"
partial: false
created: "2026-08-10T10:18:04Z"
summary: "Created improve-docs as the content-quality half of the docs pair. One clarification resolved a contradiction in the request (the brief said 'improve the skill' while also demanding parity with the ot"
---

## Review
Created improve-docs as the content-quality half of the docs pair. One clarification resolved a contradiction in the request (the brief said 'improve the skill' while also demanding parity with the other create/improve pairs): the user confirmed improve-docs targets documentation artifacts and skill self-improvement stays with improve-skills. Authored a 148-line SKILL.md matching sibling shape (Goal/Input Contract/Workflow/Constraints/Resource ID/Resources/Feedback) with an explicit ownership-boundary table, nine improvement classes with per-class verification obligations, evidence-first workflow over docs-utils/feedback engines, and audit trail via --scope improve-docs. Registered adjacent to create-docs, propagated to knowledge-manager (both sides mirrored), pinned the pair boundary with a new contract test (9 assertions) plus contract clause C-18. Ran the mandated RED-GREEN pressure test on an isolated fixture: GREEN respected the structure boundary and produced hand-offs plus an audit entry where RED mutated notes lifecycle state and left no trace; two loopholes GREEN exposed were closed in REFACTOR. Zero new test failures (15 conformance failures byte-identical to the pre-existing set).

## Optimization Points
- Pressure-test fixture design can contaminate the RED arm. Shipping the project's own engine (docs-utils.py) into the fixture leaked its violation vocabulary into the no-skill baseline: RED discovered and ran `--action validate`, so it behaved far more disciplined than a real baseline and three constraint clauses (wholesale rewrite / delete history / restyle-without-finding) went unobserved rather than proven. Rule for create-skills 6.5: keep deterministic engines OUT of the RED fixture, or run a second RED arm without them, and report unobserved clauses as unobserved.
- Verify pressure-test arms against the filesystem diff, not the subagent's self-report. Snapshotting the fixture before dispatch (`cp -r`) and running `diff -rq` afterwards is what turned "both agents sounded careful" into a measurable difference: RED mutated docs/notes/worker-sizing.md frontmatter (a lifecycle change owned by create-docs) while GREEN handed it off. Make the before-snapshot + diff a required step of the method.
- GREEN exposed two real loopholes that a structural check could not: the one-document-per-run constraint formally contradicted the mandated same-run inbound-anchor repair, and the never-create constraint read as if it covered engine-written audit/feedback artifacts. Both were closed in REFACTOR. Confirms that constraint-dense skills need the RED-GREEN pass, not just a contract test.
- token-efficiency: surveying siblings by heading extraction (grep '^## ') plus one full read of the closest analog (improve-tools, 147 lines) was enough to match house shape without reading all four improve-* skills; the pair boundary was then pinned by a contract test rather than by prose repetition across both SKILL.md files.
